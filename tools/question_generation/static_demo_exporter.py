"""Pure in-memory exporter skeleton for the diagnostic SBA static demo.

The helpers in this module build split static-demo payloads only. They do not
write ``preguntas.json``, modify frontend files, create production banks, or
mutate draft/review inputs.
"""

from __future__ import annotations

import copy
from collections.abc import Mapping
from typing import Any

from tools.question_generation.diagnostic_sba_validator import validate_diagnostic_sba_item
from tools.question_generation.human_review_resolution import (
    ApprovalScope,
    ReviewStatus,
    SAFE_GOVERNANCE,
    validate_review_record,
)


EXPORT_VERSION = "static_demo_export_v0"
STATIC_DEMO_DISCLAIMER = "PROTOTIPO · ENTRENAMIENTO · NO EVALUACIÓN OFICIAL WSET"
STATIC_DEMO_EXPORTED_AT = "not_written_in_skeleton"
SAFE_ITEM_GOVERNANCE = {
    "training_item_only": True,
    "official_wset_question": False,
    "safe_for_examiner": False,
    "examiner_scoring_allowed": False,
    "static_demo_only": True,
}
FORBIDDEN_RENDER_KEYS = frozenset(
    (
        "is_correct",
        "correct_option_id",
        "diagnostic_role",
        "diagnostic_note",
        "misconception_id",
        "misconception_linkage",
        "causal_chain_linkage",
        "feedback",
        "correct_rationale",
        "why_other_options_are_wrong",
        "remediation_recommendation",
        "remediation_target",
        "source_support",
    )
)
FORBIDDEN_AUTHORITY_PHRASES = (
    "official score",
    "official wset score",
    "pass/fail",
    "certification readiness",
    "examiner authority",
    "approved_for_production",
)


def select_static_demo_eligible_items(drafts: list[dict], reviews: list[dict]) -> list[dict]:
    """Return validator-valid drafts with valid static-demo review records."""
    review_by_source_id = _unique_reviews_by_source_id(reviews)
    eligible: list[dict] = []

    for draft in drafts:
        source_question_id = _source_question_id(draft)
        review = review_by_source_id.get(source_question_id)
        if _is_static_demo_eligible(draft, review):
            eligible.append(copy.deepcopy(draft))

    eligible.sort(key=_source_sort_key)
    return eligible


def build_static_demo_render_payload(draft: dict, review: dict) -> dict:
    """Build frontend pre-submit render data without correctness leakage."""
    identity = _mapping(draft.get("identity"))
    curriculum = _mapping(draft.get("curriculum"))
    question = _mapping(draft.get("question"))

    return {
        "item_id": identity.get("item_id"),
        "source_question_id": identity.get("source_question_id"),
        "draft_id": identity.get("item_id"),
        "review_id": review.get("review_id"),
        "approval_scope": review.get("approval_scope"),
        "static_demo_only": True,
        "training_item_only": True,
        "official_wset_question": False,
        "safe_for_examiner": False,
        "examiner_scoring_allowed": False,
        "disclaimer": STATIC_DEMO_DISCLAIMER,
        "ra_id": curriculum.get("ra_id"),
        "topic": curriculum.get("topic"),
        "subtopic": curriculum.get("subtopic"),
        "difficulty": curriculum.get("difficulty"),
        "learning_objective": curriculum.get("learning_objective"),
        "stem": question.get("stem"),
        "question_type": question.get("question_type"),
        "options": _render_options(draft),
        "governance": copy.deepcopy(SAFE_ITEM_GOVERNANCE),
    }


def build_static_demo_outcome_payload(draft: dict, review: dict) -> dict:
    """Build separated post-submit demo outcome data."""
    identity = _mapping(draft.get("identity"))
    item_id = identity.get("item_id")
    correct_option_id = _correct_option_id(draft)
    feedback = _mapping(draft.get("feedback"))

    return {
        "item_id": item_id,
        "source_question_id": identity.get("source_question_id"),
        "draft_id": item_id,
        "review_id": review.get("review_id"),
        "approval_scope": review.get("approval_scope"),
        "static_demo_only": True,
        "correct_option_id": correct_option_id,
        "result_messaging": {
            "correct": "Respuesta correcta en demo de entrenamiento.",
            "incorrect": "Respuesta incorrecta en demo de entrenamiento.",
            "disclaimer": STATIC_DEMO_DISCLAIMER,
        },
        "option_diagnostics": _option_diagnostics(draft),
        "feedback": copy.deepcopy(dict(feedback)),
        "misconception_linkage": copy.deepcopy(draft.get("misconception_linkage", {})),
        "causal_chain_linkage": copy.deepcopy(draft.get("causal_chain_linkage", {})),
        "sat_relevance": copy.deepcopy(draft.get("sat_relevance", [])),
        "remediation": {
            "recommendation": feedback.get("remediation_recommendation"),
            "target": copy.deepcopy(feedback.get("remediation_target")),
        },
        "governance": copy.deepcopy(SAFE_ITEM_GOVERNANCE),
    }


def build_static_demo_export_payload(drafts: list[dict], reviews: list[dict]) -> dict:
    """Return a split static-demo payload in memory only."""
    review_by_source_id = _unique_reviews_by_source_id(reviews)
    eligible_drafts = select_static_demo_eligible_items(drafts, reviews)

    items: list[dict] = []
    outcomes_by_item_id: dict[str, dict] = {}
    for draft in eligible_drafts:
        review = review_by_source_id[_source_question_id(draft)]
        render_payload = build_static_demo_render_payload(draft, review)
        outcome_payload = build_static_demo_outcome_payload(draft, review)
        item_id = str(render_payload["item_id"])
        items.append(render_payload)
        outcomes_by_item_id[item_id] = outcome_payload

    return {
        "export_version": EXPORT_VERSION,
        "static_demo_only": True,
        "disclaimer": STATIC_DEMO_DISCLAIMER,
        "items": items,
        "outcomes_by_item_id": outcomes_by_item_id,
        "export_metadata": {
            "export_version": EXPORT_VERSION,
            "exported_at": STATIC_DEMO_EXPORTED_AT,
            "eligible_item_count": len(items),
            "source_question_ids": [item["source_question_id"] for item in items],
            "review_ids": [item["review_id"] for item in items],
            "output_written": False,
            "target_path": "frontend/diagnostic-sba/preguntas.json",
        },
    }


def validate_static_demo_export_payload(payload: dict) -> list[str]:
    """Return deterministic validation errors for a static demo payload."""
    errors: list[str] = []
    if not isinstance(payload, dict):
        return ["payload must be a dict"]

    for field in ("export_version", "static_demo_only", "items", "outcomes_by_item_id", "export_metadata"):
        if field not in payload:
            errors.append(f"missing field: {field}")

    if payload.get("export_version") != EXPORT_VERSION:
        errors.append("export_version must be static_demo_export_v0")
    if payload.get("static_demo_only") is not True:
        errors.append("static_demo_only must be true")

    items = payload.get("items")
    outcomes = payload.get("outcomes_by_item_id")
    if not isinstance(items, list):
        errors.append("items must be a list")
        items = []
    if not isinstance(outcomes, dict):
        errors.append("outcomes_by_item_id must be a dict")
        outcomes = {}

    seen_item_ids: list[str] = []
    for item in items:
        if not isinstance(item, dict):
            errors.append("items entries must be dicts")
            continue
        errors.extend(_validate_render_item(item))
        item_id = item.get("item_id")
        if item_id in outcomes:
            errors.extend(_validate_outcome_payload(item_id, outcomes[item_id]))
        else:
            errors.append(f"missing outcome for item_id: {item_id}")
        seen_item_ids.append(str(item_id))

    if sorted(seen_item_ids, key=_numeric_suffix_sort_key) != seen_item_ids:
        errors.append("items must be deterministically ordered by source_question_id/item_id")

    for item_id in outcomes:
        if item_id not in seen_item_ids:
            errors.append(f"outcome without render item: {item_id}")

    metadata = payload.get("export_metadata")
    if isinstance(metadata, dict):
        if metadata.get("output_written") is not False:
            errors.append("export_metadata.output_written must be false in skeleton")
        if metadata.get("export_version") != EXPORT_VERSION:
            errors.append("export_metadata.export_version must match export_version")
    else:
        errors.append("export_metadata must be a dict")

    text = repr(payload).lower()
    for phrase in FORBIDDEN_AUTHORITY_PHRASES:
        if phrase in text:
            errors.append(f"forbidden authority phrase present: {phrase}")

    return errors


def _is_static_demo_eligible(draft: Any, review: Any) -> bool:
    if not isinstance(draft, dict) or not isinstance(review, dict):
        return False
    if validate_diagnostic_sba_item(draft):
        return False
    if validate_review_record(review):
        return False
    if _mapping(draft.get("governance")) != SAFE_GOVERNANCE:
        return False
    if _mapping(review.get("governance_confirmation")) != SAFE_GOVERNANCE:
        return False
    if review.get("review_status") != ReviewStatus.APPROVED_FOR_STATIC_DEMO:
        return False
    if review.get("approval_scope") != ApprovalScope.STATIC_DEMO_ONLY:
        return False
    if review.get("source_question_id") != _source_question_id(draft):
        return False
    if review.get("draft_id") != _mapping(draft.get("identity")).get("item_id"):
        return False
    return True


def _unique_reviews_by_source_id(reviews: list[dict]) -> dict[str, dict]:
    by_source_id: dict[str, dict] = {}
    duplicates: set[str] = set()
    for review in reviews:
        if not isinstance(review, dict):
            continue
        source_id = str(review.get("source_question_id", ""))
        if source_id in by_source_id:
            duplicates.add(source_id)
        by_source_id[source_id] = review
    for source_id in duplicates:
        by_source_id.pop(source_id, None)
    return by_source_id


def _validate_render_item(item: dict) -> list[str]:
    errors: list[str] = []
    required = (
        "item_id",
        "source_question_id",
        "stem",
        "options",
        "review_id",
        "approval_scope",
        "static_demo_only",
        "training_item_only",
        "official_wset_question",
        "safe_for_examiner",
        "examiner_scoring_allowed",
    )
    for field in required:
        if field not in item:
            errors.append(f"render item missing field: {field}")
    if item.get("governance") != SAFE_ITEM_GOVERNANCE:
        errors.append("render item governance must be safe")
    for field, expected in SAFE_ITEM_GOVERNANCE.items():
        if item.get(field) is not expected:
            errors.append(f"render item {field} must be {str(expected).lower()}")
    if item.get("approval_scope") != ApprovalScope.STATIC_DEMO_ONLY:
        errors.append("render item approval_scope must be static_demo_only")
    if _contains_forbidden_render_key(item):
        errors.append("render item contains forbidden pre-submit diagnostic/correctness fields")
    options = item.get("options")
    if not isinstance(options, list) or len(options) != 4:
        errors.append("render item options must contain four entries")
    else:
        option_ids = [option.get("option_id") for option in options if isinstance(option, dict)]
        if option_ids != ["A", "B", "C", "D"]:
            errors.append("render item options must be ordered A-D")
        for option in options:
            if not isinstance(option, dict) or set(option.keys()) != {"option_id", "option_text"}:
                errors.append("render item options must contain option_id and option_text only")
                break
    return errors


def _validate_outcome_payload(item_id: str, outcome: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(outcome, dict):
        return [f"outcome for {item_id} must be a dict"]
    if outcome.get("item_id") != item_id:
        errors.append(f"outcome item_id mismatch for {item_id}")
    if outcome.get("static_demo_only") is not True:
        errors.append(f"outcome static_demo_only must be true for {item_id}")
    if outcome.get("governance") != SAFE_ITEM_GOVERNANCE:
        errors.append(f"outcome governance must be safe for {item_id}")
    if not outcome.get("correct_option_id"):
        errors.append(f"outcome correct_option_id must be present for {item_id}")
    if not isinstance(outcome.get("option_diagnostics"), dict):
        errors.append(f"outcome option_diagnostics must be present for {item_id}")
    return errors


def _contains_forbidden_render_key(value: Any) -> bool:
    if isinstance(value, Mapping):
        for key, child in value.items():
            if key in FORBIDDEN_RENDER_KEYS:
                return True
            if _contains_forbidden_render_key(child):
                return True
    elif isinstance(value, list):
        return any(_contains_forbidden_render_key(child) for child in value)
    return False


def _render_options(draft: dict) -> list[dict]:
    options = _mapping(draft.get("options"))
    return [
        {
            "option_id": option_id,
            "option_text": _mapping(options.get(option_id)).get("option_text"),
        }
        for option_id in ("A", "B", "C", "D")
    ]


def _option_diagnostics(draft: dict) -> dict[str, dict]:
    options = _mapping(draft.get("options"))
    diagnostics: dict[str, dict] = {}
    for option_id in ("A", "B", "C", "D"):
        option = _mapping(options.get(option_id))
        diagnostics[option_id] = {
            "is_correct": option.get("is_correct"),
            "diagnostic_role": option.get("diagnostic_role"),
            "misconception_id": option.get("misconception_id"),
            "diagnostic_note": option.get("diagnostic_note"),
        }
    return diagnostics


def _correct_option_id(draft: dict) -> str | None:
    for option_id, option in _mapping(draft.get("options")).items():
        if _mapping(option).get("is_correct") is True:
            return str(option_id)
    return None


def _source_question_id(draft: dict) -> str:
    return str(_mapping(draft.get("identity")).get("source_question_id", ""))


def _source_sort_key(draft: dict) -> tuple[int, str]:
    source_id = _source_question_id(draft)
    return _numeric_suffix_sort_key(source_id)


def _numeric_suffix_sort_key(value: Any) -> tuple[int, str]:
    text = str(value)
    digits = "".join(char for char in text if char.isdigit())
    return (int(digits) if digits else 0, text)


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}
