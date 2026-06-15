"""Private Open Response Lab runtime helpers.

Phase X.2: Lab is now active_private_lab. All 20 approved OR items are included.
Assessment intelligence (Phase X.1) is embedded as a runtime resource.
Governance flags remain unchanged -- open_response_lab_active stays False because
that flag governs examiner-authority scope, not UI activation.
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
OPEN_RESPONSE_BANK_PATH = Path(
    "knowledge/question-bank/open_response/open_response_bank.json"
)
LAB_PAYLOAD_GLOBAL = "OPEN_RESPONSE_LAB_PAYLOAD"
LAB_STORAGE_KEY = "wset_open_response_lab_private_v1"
LAB_CONTRACT = "private_open_response_lab_runtime_mvp"
LAB_ACTIVATION_STATUS = "active_private_lab"
COMMAND_VERBS_LOADED: tuple[str, ...] = (
    "explain",
    "describe",
    "justify",
    "assess",
    "evaluate",
    "compare",
    "why",
    "how",
    "discuss",
    "identify and explain",
    "outline",
    "state",
    "list",
    "recommend",
)

# Phase X.1 assessment intelligence source paths
_KNOWLEDGE_ROOT = Path("knowledge")
_COMMAND_VERB_PATHS = [
    _KNOWLEDGE_ROOT / "command-verbs" / f"{v}.json"
    for v in (
        "describe",
        "explain",
        "compare",
        "assess",
        "evaluate",
        "discuss",
        "recommend",
        "identify_and_explain",
        "justify",
    )
]
_SAT_QUALITY_PATH = _KNOWLEDGE_ROOT / "sat-framework" / "sat_quality_framework.json"
_EVIDENCE_REQ_PATH = _KNOWLEDGE_ROOT / "evaluator-framework" / "evidence_requirements.json"
_CRF_PATH = _KNOWLEDGE_ROOT / "mentor-framework" / "common_response_failures.json"
_IMPROVEMENT_PATH = _KNOWLEDGE_ROOT / "mentor-framework" / "improvement_patterns.json"
_MENTOR_HINTS_PATH = _KNOWLEDGE_ROOT / "mentor-framework" / "mentor_hints.json"

VISIBLE_QUESTION_FIELDS: tuple[str, ...] = (
    "item_id",
    "source_question_id",
    "stem",
    "topic",
    "RA",
    # Phase P2.3: Evaluation metadata (formative only, safe for learner exposure)
    "command_verb",
    "expected_concepts",
    "evaluation_config",
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
    """Build the static private-lab payload from existing engine outputs.

    Phase X.2: includes all candidates (not just session-union), embeds
    assessment_intelligence from Phase X.1 knowledge assets.
    """
    integrated_bank = candidates is None
    source_records = (
        load_integrated_open_response_candidates()
        if integrated_bank
        else candidates
    )
    records = [dict(candidate) for candidate in source_records]
    candidates_by_id = {
        str(candidate.get("source_question_id", "")).strip(): copy.deepcopy(dict(candidate))
        for candidate in records
    }
    all_source_ids = list(candidates_by_id.keys())

    sessions = (
        _compose_integrated_sessions(records)
        if integrated_bank
        else {
            session_name: compose_session(records, session_size=session_name)
            for session_name in SESSION_SIZES
        }
    )

    payload = {
        "lab_contract": LAB_CONTRACT,
        "activation_status": LAB_ACTIVATION_STATUS,
        "pool_size": len(all_source_ids),
        "storage_key": LAB_STORAGE_KEY,
        "session_options": copy.deepcopy(SESSION_SIZES),
        "sessions": {
            name: {
                "session_size": session["session_size"],
                "item_ids": [
                    _runtime_item_id(candidates_by_id[source_id])
                    for source_id in session["source_question_ids"]
                ],
                "source_question_ids": list(session["source_question_ids"]),
            }
            for name, session in sessions.items()
        },
        "items": [
            _render_item(candidates_by_id[source_id])
            for source_id in all_source_ids
        ],
        "evaluation_by_item_id": {
            _runtime_item_id(candidates_by_id[source_id]): _evaluation_item(
                candidates_by_id[source_id]
            )
            for source_id in all_source_ids
        },
        "feedback_fields": copy.deepcopy(FEEDBACK_FIELD_MAP),
        "feedback_prohibited": list(FEEDBACK_PROHIBITED),
        "evaluation_metadata": {
            "schema_version": "open_response_evaluation_v1",
            "command_verbs_loaded": list(COMMAND_VERBS_LOADED),
            "governance": {
                "safe_for_examiner": False,
                "examiner_scoring_allowed": False,
                "formative_only": True,
            },
        },
        "expansion_history": [
            {
                "phase": "P2.4",
                "items_added": 15,
                "new_pool_size": len(records),
            },
            {
                "phase": "OR_EXPANSION_BATCH_4",
                "items_added": 32,
                "new_pool_size": len(records),
            },
        ],
        "assessment_intelligence": _build_assessment_intelligence(),
        "governance_flags": copy.deepcopy(LAB_GOVERNANCE_FLAGS),
    }
    if integrated_bank:
        payload["source_bank_total"] = len(records)
    return payload


def load_integrated_open_response_candidates(
    path: str | Path = OPEN_RESPONSE_BANK_PATH,
) -> list[dict[str, Any]]:
    """Normalize the canonical OR bank into the existing runtime candidate shape."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    items = data.get("items", [])
    if not isinstance(items, list):
        raise ValueError("open response bank items must be a list")
    return [_adapt_bank_item(item) for item in items if isinstance(item, Mapping)]


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
        errors.append(f"activation_status must be {LAB_ACTIVATION_STATUS!r}")
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


def _build_assessment_intelligence() -> dict[str, Any]:
    """Load Phase X.1 assessment intelligence assets for runtime embedding.

    Returns an empty dict if any source file is missing (graceful degradation).
    """
    try:
        def _load(p: Path) -> dict[str, Any]:
            return json.loads(p.read_text(encoding="utf-8"))

        command_verbs: dict[str, Any] = {}
        for p in _COMMAND_VERB_PATHS:
            d = _load(p)
            verb = d.get("verb", p.stem)
            command_verbs[verb] = {
                "cognitive_level": d["cognitive_level"],
                "definition": d["definition"],
                "do": d["expected_response"]["do"],
                "do_not": d["expected_response"]["do_not"],
            }

        sat_quality = _load(_SAT_QUALITY_PATH)
        sat_quality_levels: dict[str, Any] = {}
        for lvl in sat_quality.get("quality_levels", []):
            sat_quality_levels[lvl["level"]] = {
                "level_en": lvl["level_en"],
                "description": lvl["description"],
                "signal_observations": lvl["signal_observations"],
            }

        ev_req = _load(_EVIDENCE_REQ_PATH)
        crf_data = _load(_CRF_PATH)
        ip_data = _load(_IMPROVEMENT_PATH)
        hints_data = _load(_MENTOR_HINTS_PATH)

        return {
            "schema_version": "assessment_intelligence_v1",
            "phase": "X.1",
            "activation_status": LAB_ACTIVATION_STATUS,
            "governance": {
                "safe_for_examiner": False,
                "examiner_scoring_allowed": False,
                "training_use_only": True,
            },
            "command_verbs": command_verbs,
            "sat_quality_levels": sat_quality_levels,
            "evidence_requirements": {
                "principles": ev_req["principles"],
                "strong_patterns": ev_req["strong_evidence_patterns"],
            },
            "common_response_failures": [
                {
                    "id": fail["id"],
                    "failure": fail["failure"],
                    "description": fail["description"],
                    "example": fail.get("example"),
                    "correction": fail["correction"],
                }
                for fail in crf_data["failures"]
            ],
            "improvement_patterns": [
                {
                    "id": ip["id"],
                    "from": ip["from"],
                    "to": ip["to"],
                    "example_before": ip["example_before"],
                    "example_after": ip["example_after"],
                }
                for ip in ip_data["improvement_patterns"]
            ],
            "mentor_hints_by_topic": hints_data["hints_by_topic"],
        }
    except (FileNotFoundError, KeyError, json.JSONDecodeError):
        return {}


def _render_item(candidate: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "item_id": _runtime_item_id(candidate),
        "source_question_id": str(candidate.get("source_question_id", "")).strip(),
        "stem": str(candidate.get("stem", "")).strip(),
        "topic": str(candidate.get("topic", "")).strip(),
        "RA": str(candidate.get("RA", "")).strip(),
        "command_verb": str(candidate.get("command_verb", "")).strip(),
        "expected_concepts": _string_list(candidate.get("expected_concepts")),
        "evaluation_config": candidate.get("evaluation_config", {}),
    }


def _evaluation_item(candidate: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "item_id": _runtime_item_id(candidate),
        "source_question_id": str(candidate.get("source_question_id", "")).strip(),
        "expected_concepts": _string_list(candidate.get("expected_concepts")),
        "optional_causal_chain": candidate.get("optional_causal_chain"),
        "causal_chain_reference": _string_list(
            candidate.get("causal_chain_reference")
        ),
        "feedback_profile": copy.deepcopy(candidate.get("feedback_profile", {})),
        "governance_flags": copy.deepcopy(LAB_GOVERNANCE_FLAGS),
    }


def _runtime_item_id(candidate: Mapping[str, Any]) -> str:
    item_id = str(candidate.get("item_id", "")).strip()
    if item_id:
        return item_id
    return _item_id(candidate.get("source_question_id"))


def _item_id(source_question_id: Any) -> str:
    return f"open_response_{str(source_question_id).strip()}"


def _adapt_bank_item(item: Mapping[str, Any]) -> dict[str, Any]:
    item_id = str(item.get("item_id") or item.get("question_id") or "").strip()
    if not item_id:
        raise ValueError("open response bank item requires item_id")
    verb = _frontend_command_verb(
        str(item.get("command_verb", "")).strip(),
        str(item.get("question_text", "")).strip(),
    )
    concepts = _string_list(item.get("expected_concepts"))
    chains = _string_list(
        item.get("causal_chain_reference", item.get("causal_chain_target"))
    )
    question_text = str(item.get("question_text", "")).strip()
    return {
        "item_id": item_id,
        "question_id": str(item.get("question_id", item_id)).strip(),
        "source_question_id": item_id,
        "question_text": question_text,
        "stem": question_text,
        "topic": str(item.get("topic", "")).strip(),
        "RA": str(item.get("ra_id", "")).strip(),
        "command_verb": verb,
        "expected_concepts": concepts,
        "optional_causal_chain": " -> ".join(chains) if chains else None,
        "causal_chain_reference": chains,
        "feedback_profile": copy.deepcopy(item.get("feedback_profile", {})),
        "evaluation_config": {
            "verb_definition_key": verb,
            "requires_causal_chain": bool(chains),
            "structure_rules": {
                "minimum_components": 2,
                "response_depth_target": str(
                    item.get("response_depth_target", "developing")
                ).strip()
            },
            "required_signals": concepts,
            "forbidden_signals": list(FEEDBACK_PROHIBITED),
            "source": "open_response_bank_v1",
        },
    }


def _frontend_command_verb(verb: str, question_text: str) -> str:
    normalized = verb.replace("_", " ").strip().casefold()
    if normalized:
        return normalized

    stem = question_text.strip().casefold()
    if stem.startswith(("justifica", "justify")):
        return "justify"
    if stem.startswith(("compare", "compara")):
        return "compare"
    if stem.startswith(("analice", "analiza", "assess", "evaluate")):
        return "evaluate"
    if stem.startswith(("describa", "describe")):
        return "describe"
    if stem.startswith(("menciona", "state")):
        return "state"
    if stem.startswith(("nombra", "list")):
        return "list"
    if stem.startswith(("identifica", "identify")):
        return "identify and explain"
    if "por qué" in stem[:40]:
        return "why"
    if stem.startswith(("explica cómo", "explique cómo", "how")):
        return "how"
    return "explain"


def _compose_integrated_sessions(
    records: Sequence[Mapping[str, Any]],
) -> dict[str, dict[str, Any]]:
    """Build deterministic sessions while preserving the established mode contract."""
    source_ids = [
        str(record.get("source_question_id", "")).strip()
        for record in records
        if str(record.get("source_question_id", "")).strip()
    ]
    if len(source_ids) < max(SESSION_SIZES.values()):
        raise ValueError("integrated open response bank is too small for sessions")

    latest_ids = source_ids[-32:] if len(source_ids) >= 32 else source_ids
    by_ra: dict[str, list[str]] = {}
    for record in records:
        source_id = str(record.get("source_question_id", "")).strip()
        if source_id not in latest_ids:
            continue
        by_ra.setdefault(str(record.get("RA", "")).strip(), []).append(source_id)

    mock_ids = by_ra.get("RA2", [])[:3] + by_ra.get("RA4", [])[:1]
    if len(mock_ids) < SESSION_SIZES["mock_theory_2"]:
        mock_ids.extend(
            source_id
            for source_id in latest_ids
            if source_id not in mock_ids
        )
    mock_ids = mock_ids[: SESSION_SIZES["mock_theory_2"]]

    return {
        "short_practice": {
            "session_size": SESSION_SIZES["short_practice"],
            "source_question_ids": latest_ids[:1],
        },
        "standard_practice": {
            "session_size": SESSION_SIZES["standard_practice"],
            "source_question_ids": latest_ids[:2],
        },
        "extended_practice": {
            "session_size": SESSION_SIZES["extended_practice"],
            "source_question_ids": latest_ids[:4],
        },
        "mock_theory_2": {
            "session_size": SESSION_SIZES["mock_theory_2"],
            "source_question_ids": mock_ids,
        },
    }


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
