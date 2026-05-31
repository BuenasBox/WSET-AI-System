"""Deterministic validator for diagnostic single-best-answer items.

The validator is intentionally pure: no file I/O, no network access, no
external dependencies, and no mutation of the input item.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any


REQUIRED_TOP_LEVEL_SECTIONS: tuple[str, ...] = (
    "identity",
    "curriculum",
    "question",
    "options",
    "source_support",
    "feedback",
    "governance",
    "attempt_analytics_placeholders",
)

OPTION_KEYS: tuple[str, ...] = ("A", "B", "C", "D")

GOVERNANCE_EXPECTED: tuple[tuple[str, bool], ...] = (
    ("safe_for_examiner", False),
    ("examiner_scoring_allowed", False),
    ("official_wset_question", False),
    ("training_item_only", True),
    ("uses_llm", False),
    ("uses_api", False),
    ("uses_embeddings", False),
    ("uses_vector_db", False),
    ("cloud_services_active", False),
)

FORBIDDEN_KEY_PARTS: tuple[str, ...] = (
    "official_score",
    "official_mark",
    "examiner_mark",
    "examiner_score",
    "pass_fail",
    "predicted_pass",
    "certified",
    "certification",
    "grade_band",
    "wset_official",
)

UNSAFE_TEXT_CLAIMS: tuple[str, ...] = (
    "official wset question",
    "official wset score",
    "examiner mark",
    "certified result",
    "guaranteed pass",
)


def validate_diagnostic_sba_item(item: dict) -> list[str]:
    """Return deterministic validation errors for a diagnostic SBA item.

    An empty list means the item passed the Phase 4A.3 validator. Normal
    validation failures are returned as strings rather than raised.
    """
    errors: list[str] = []

    if not isinstance(item, dict):
        return ["item must be a dict"]

    _validate_required_sections(item, errors)
    _validate_identity(_as_mapping(item.get("identity")), errors)
    _validate_curriculum(_as_mapping(item.get("curriculum")), errors)
    _validate_question(_as_mapping(item.get("question")), errors)
    _validate_options(_as_mapping(item.get("options")), errors)
    _validate_source_support(_as_mapping(item.get("source_support")), errors)
    _validate_feedback(_as_mapping(item.get("feedback")), errors)
    _validate_governance(_as_mapping(item.get("governance")), errors)
    _validate_forbidden_content(item, errors)

    return errors


def is_valid_diagnostic_sba_item(item: dict) -> bool:
    """Return True when ``validate_diagnostic_sba_item(item)`` has no errors."""
    return not validate_diagnostic_sba_item(item)


def _validate_required_sections(item: Mapping[str, Any], errors: list[str]) -> None:
    for section in REQUIRED_TOP_LEVEL_SECTIONS:
        if section not in item:
            errors.append(f"missing top-level section: {section}")


def _validate_identity(identity: Mapping[str, Any], errors: list[str]) -> None:
    for field in ("item_id", "item_version", "generation_method"):
        if not _non_empty_string(identity.get(field)):
            errors.append(f"identity.{field} must be present and non-empty")
    if identity.get("training_item_only") is not True:
        errors.append("identity.training_item_only must be true")


def _validate_curriculum(curriculum: Mapping[str, Any], errors: list[str]) -> None:
    for field in ("ra_id", "topic", "subtopic", "difficulty", "learning_objective"):
        if not _non_empty_string(curriculum.get(field)):
            errors.append(f"curriculum.{field} must be present and non-empty")


def _validate_question(question: Mapping[str, Any], errors: list[str]) -> None:
    if not _non_empty_string(question.get("stem")):
        errors.append("question.stem must be present and non-empty")
    if question.get("question_type") != "single_best_answer":
        errors.append('question.question_type must equal "single_best_answer"')
    if not _non_empty_string(question.get("expected_reasoning_type")):
        errors.append("question.expected_reasoning_type must be present and non-empty")


def _validate_options(options: Mapping[str, Any], errors: list[str]) -> None:
    option_key_set = set(options.keys()) if isinstance(options, Mapping) else set()
    expected_key_set = set(OPTION_KEYS)

    missing = sorted(expected_key_set - option_key_set)
    extra = sorted(option_key_set - expected_key_set)
    if missing:
        errors.append(f"options missing required keys: {', '.join(missing)}")
    if extra:
        errors.append(f"options contains unexpected keys: {', '.join(extra)}")
    if len(option_key_set) != 4:
        errors.append("options must contain exactly A, B, C, and D")

    correct_count = 0
    normalized_texts: list[str] = []

    for key in OPTION_KEYS:
        option = _as_mapping(options.get(key))
        if not option:
            continue

        option_id = option.get("option_id")
        if option_id != key:
            errors.append(f"options.{key}.option_id must match key {key}")

        option_text = option.get("option_text")
        if not _non_empty_string(option_text):
            errors.append(f"options.{key}.option_text must be present and non-empty")
        else:
            normalized_texts.append(" ".join(str(option_text).lower().split()))

        is_correct = option.get("is_correct")
        if is_correct is True:
            correct_count += 1
        elif is_correct is not False:
            errors.append(f"options.{key}.is_correct must be true or false")

        diagnostic_role = option.get("diagnostic_role")
        if not _non_empty_string(diagnostic_role):
            errors.append(f"options.{key}.diagnostic_role must be present and non-empty")
        elif is_correct is True and diagnostic_role != "correct":
            errors.append(f"options.{key}.diagnostic_role must be correct for the correct option")
        elif is_correct is False and diagnostic_role == "correct":
            errors.append(f"options.{key}.diagnostic_role must not be correct for an incorrect option")

    if correct_count != 1:
        errors.append("options must contain exactly one correct answer")

    if len(normalized_texts) != len(set(normalized_texts)):
        errors.append("options.option_text values must be unique")


def _validate_source_support(source_support: Mapping[str, Any], errors: list[str]) -> None:
    source_ids = source_support.get("source_ids")
    if not _non_empty_list(source_ids):
        errors.append("source_support.source_ids must be a non-empty list")
    source_chunks = source_support.get("source_chunks")
    if not _non_empty_list(source_chunks):
        errors.append("source_support.source_chunks must be a non-empty list")
    if not _non_empty_string(source_support.get("support_rationale")):
        errors.append("source_support.support_rationale must be present and non-empty")


def _validate_feedback(feedback: Mapping[str, Any], errors: list[str]) -> None:
    if not _non_empty_string(feedback.get("correct_rationale")):
        errors.append("feedback.correct_rationale must be present and non-empty")

    why_wrong = _as_mapping(feedback.get("why_other_options_are_wrong"))
    if not why_wrong:
        errors.append("feedback.why_other_options_are_wrong must be present")
    else:
        missing = [key for key in OPTION_KEYS if not _non_empty_string(why_wrong.get(key))]
        if missing:
            errors.append(
                "feedback.why_other_options_are_wrong must include non-empty entries for: "
                + ", ".join(missing)
            )

    if not _non_empty_string(feedback.get("remediation_recommendation")):
        errors.append("feedback.remediation_recommendation must be present and non-empty")


def _validate_governance(governance: Mapping[str, Any], errors: list[str]) -> None:
    for field, expected in GOVERNANCE_EXPECTED:
        if governance.get(field) is not expected:
            expected_text = "true" if expected else "false"
            errors.append(f"governance.{field} must be {expected_text}")


def _validate_forbidden_content(value: Any, errors: list[str]) -> None:
    for path, key, nested_value in _walk(value):
        lowered_key = key.lower() if key is not None else ""
        for forbidden in FORBIDDEN_KEY_PARTS:
            if forbidden in lowered_key:
                errors.append(f"forbidden field detected at {path}: {key}")
                break

        if isinstance(nested_value, str):
            lowered_value = nested_value.lower()
            for claim in UNSAFE_TEXT_CLAIMS:
                if claim in lowered_value:
                    errors.append(f"unsafe official-authority language at {path}: {claim}")
                    break


def _walk(value: Any, path: str = "$", key: str | None = None):
    yield path, key, value
    if isinstance(value, Mapping):
        for child_key in sorted(value.keys(), key=str):
            child_path = f"{path}.{child_key}"
            yield from _walk(value[child_key], child_path, str(child_key))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from _walk(child, f"{path}[{index}]", None)


def _as_mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _non_empty_list(value: Any) -> bool:
    return isinstance(value, list) and bool(value)
