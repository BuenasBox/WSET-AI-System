"""Private Open Response Lab runtime helpers.

This layer is intentionally local and inactive. It adapts the existing
open-response Session Engine and formative pipeline into a browser-safe payload
for the private lab runtime without adding backend, Tutor, Retrieval, Self-Eval,
Golden, snapshot, or Dashboard dependencies.
"""

from __future__ import annotations

import copy
import json
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from tools.question_generation.open_response_pipeline import evaluate_open_response_answer
from tools.question_generation.open_response_session_engine import (
    FEEDBACK_PROHIBITED,
    LAB_GOVERNANCE_FLAGS,
    SESSION_SIZES,
    compose_session,
    load_open_response_candidates,
)


FRONTEND_LAB_DIR = Path("frontend/open-response-lab")
LAB_PAYLOAD_JS_PATH = FRONTEND_LAB_DIR / "lab_payload.js"
LAB_PAYLOAD_GLOBAL = "OPEN_RESPONSE_LAB_PAYLOAD"
LAB_STORAGE_KEY = "wset_open_response_lab_private_v1"
LAB_CONTRACT = "private_open_response_lab_runtime_mvp"
LAB_ACTIVATION_STATUS = "inactive"

VISIBLE_QUESTION_FIELDS: tuple[str, ...] = (
    "item_id",
    "source_question_id",
    "stem",
    "topic",
    "RA",
)

FEEDBACK_FIELD_MAP: dict[str, str] = {
    "present_concepts": "concepts_detected",
    "missing_concepts": "concepts_absent",
    "causal_link_feedback": "missing_causal_reasoning",
    "revision_suggestion": "improvement_suggestions",
}


def build_lab_runtime_payload(
    candidates: Sequence[Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    """Build the static private-lab payload from existing engine outputs."""
    records = [dict(candidate) for candidate in (candidates or load_open_response_candidates())]
    candidates_by_id = {
        str(candidate.get("source_question_id", "")).strip(): copy.deepcopy(dict(candidate))
        for candidate in records
    }

    sessions = {
        session_name: compose_session(records, session_size=session_name)
        for session_name in SESSION_SIZES
    }
    selected_ids: list[str] = []
    for session in sessions.values():
        for source_id in session["source_question_ids"]:
            if source_id not in selected_ids:
                selected_ids.append(source_id)

    return {
        "lab_contract": LAB_CONTRACT,
        "activation_status": LAB_ACTIVATION_STATUS,
        "storage_key": LAB_STORAGE_KEY,
        "session_options": copy.deepcopy(SESSION_SIZES),
        "sessions": {
            name: {
                "session_size": session["session_size"],
                "item_ids": [_item_id(source_id) for source_id in session["source_question_ids"]],
                "source_question_ids": list(session["source_question_ids"]),
            }
            for name, session in sessions.items()
        },
        "items": [
            _render_item(candidates_by_id[source_id])
            for source_id in selected_ids
            if source_id in candidates_by_id
        ],
        "evaluation_by_item_id": {
            _item_id(source_id): _evaluation_item(candidates_by_id[source_id])
            for source_id in selected_ids
            if source_id in candidates_by_id
        },
        "feedback_fields": copy.deepcopy(FEEDBACK_FIELD_MAP),
        "feedback_prohibited": list(FEEDBACK_PROHIBITED),
        "governance_flags": copy.deepcopy(LAB_GOVERNANCE_FLAGS),
    }


def build_formative_feedback(candidate: Mapping[str, Any], learner_answer: str) -> dict[str, Any]:
    """Return lab-safe feedback by delegating evaluation to the existing pipeline."""
    raw_feedback = evaluate_open_response_answer(candidate, learner_answer)
    causal_feedback = str(raw_feedback.get("causal_link_feedback", "not_applicable"))
    return {
        "concepts_detected": list(raw_feedback.get("present_concepts", []))
        + list(raw_feedback.get("partial_concepts", [])),
        "concepts_absent": list(raw_feedback.get("missing_concepts", [])),
        "missing_causal_reasoning": _missing_causal_reasoning(causal_feedback),
        "improvement_suggestions": [str(raw_feedback.get("revision_suggestion", "")).strip()],
        "unsupported_claims": list(raw_feedback.get("unsupported_claims", [])),
        "governance_disclaimer": str(raw_feedback.get("governance_disclaimer", "")),
    }


def validate_lab_runtime_payload(payload: Any) -> list[str]:
    """Return deterministic validation errors for the static lab payload."""
    if not isinstance(payload, Mapping):
        return ["payload must be a dict"]

    errors: list[str] = []
    if payload.get("lab_contract") != LAB_CONTRACT:
        errors.append(f"lab_contract must be {LAB_CONTRACT}")
    if payload.get("activation_status") != LAB_ACTIVATION_STATUS:
        errors.append("activation_status must remain inactive")
    if payload.get("governance_flags") != LAB_GOVERNANCE_FLAGS:
        errors.append("governance_flags must match private lab defaults")
    if payload.get("session_options") != SESSION_SIZES:
        errors.append("session_options must match Session Engine sizes")

    items = payload.get("items")
    if not isinstance(items, list) or not items:
        errors.append("items must be a non-empty list")
    else:
        for item in items:
            keys = tuple(item.keys()) if isinstance(item, Mapping) else ()
            if keys != VISIBLE_QUESTION_FIELDS:
                errors.append("items may expose only render-safe question fields")

    sessions = payload.get("sessions")
    if not isinstance(sessions, Mapping):
        errors.append("sessions must be a dict")
    else:
        for name, size in SESSION_SIZES.items():
            session = sessions.get(name)
            if not isinstance(session, Mapping):
                errors.append(f"missing session: {name}")
                continue
            if session.get("session_size") != size:
                errors.append(f"{name} session_size must be {size}")
            if len(session.get("item_ids", [])) != size:
                errors.append(f"{name} item_ids length must be {size}")

    feedback_prohibited = set(payload.get("feedback_prohibited", []))
    for field in FEEDBACK_PROHIBITED:
        if field not in feedback_prohibited:
            errors.append(f"missing prohibited feedback field: {field}")

    _validate_no_forbidden_result_fields(payload, errors)
    return errors


def write_lab_payload_js(
    payload: Mapping[str, Any] | None = None,
    path: str | Path = LAB_PAYLOAD_JS_PATH,
) -> Path:
    """Write the static payload JavaScript consumed by the private lab HTML."""
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    data = dict(payload or build_lab_runtime_payload())
    errors = validate_lab_runtime_payload(data)
    if errors:
        raise ValueError("; ".join(errors))
    serialized = json.dumps(data, ensure_ascii=False, indent=2)
    target.write_text(
        f"window.{LAB_PAYLOAD_GLOBAL} = {serialized};\n",
        encoding="utf-8",
    )
    return target


def _render_item(candidate: Mapping[str, Any]) -> dict[str, str]:
    return {
        "item_id": _item_id(candidate.get("source_question_id")),
        "source_question_id": str(candidate.get("source_question_id", "")).strip(),
        "stem": str(candidate.get("stem", "")).strip(),
        "topic": str(candidate.get("topic", "")).strip(),
        "RA": str(candidate.get("RA", "")).strip(),
    }


def _evaluation_item(candidate: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "item_id": _item_id(candidate.get("source_question_id")),
        "source_question_id": str(candidate.get("source_question_id", "")).strip(),
        "expected_concepts": _string_list(candidate.get("expected_concepts")),
        "optional_causal_chain": candidate.get("optional_causal_chain"),
        "governance_flags": copy.deepcopy(LAB_GOVERNANCE_FLAGS),
    }


def _item_id(source_question_id: Any) -> str:
    return f"open_response_{str(source_question_id).strip()}"


def _missing_causal_reasoning(causal_feedback: str) -> list[str]:
    if causal_feedback == "weak_causal_link":
        return ["Make the cause-effect relationship explicit."]
    if causal_feedback == "causal_link_missing":
        return ["Add the expected cause-effect relationship."]
    return []


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item).strip() for item in value if str(item).strip()]


def _validate_no_forbidden_result_fields(value: Any, errors: list[str], path: str = "$") -> None:
    forbidden = ("score", "mark", "grade", "percentage", "pass_fail", "wset_equivalence")
    if isinstance(value, Mapping):
        for key, child in value.items():
            lowered = str(key).lower()
            if any(term in lowered for term in forbidden):
                errors.append(f"forbidden result field at {path}: {key}")
            _validate_no_forbidden_result_fields(child, errors, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _validate_no_forbidden_result_fields(child, errors, f"{path}[{index}]")


if __name__ == "__main__":
    print(write_lab_payload_js().as_posix())
