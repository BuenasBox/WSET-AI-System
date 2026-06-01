"""Skeleton adapter for structured question-bank records.

This module is intentionally small and pure. It does not read the structured
question bank, write converted items, call retrieval, or generate new content.
It only classifies and maps in-memory dictionaries into an incomplete adapter
skeleton that future enrichment phases can build on.
"""

from __future__ import annotations

import copy
from collections.abc import Mapping
from typing import Any


class AdapterStatus:
    ADAPTER_READY_CLEAN_PILOT = "adapter_ready_clean_pilot"
    REQUIRES_SOURCE_GROUNDING = "requires_source_grounding"
    REQUIRES_OPTION_DIAGNOSTICS = "requires_option_diagnostics"
    PRESERVE_FOR_OPEN_RESPONSE = "preserve_for_open_response"
    REJECT_OR_DEFER = "reject_or_defer"


OPTION_KEYS: tuple[str, ...] = ("A", "B", "C", "D")
VALID_ANSWER_LETTERS: frozenset[str] = frozenset(OPTION_KEYS)
SBA_LIKE_QUESTION_TYPES: frozenset[str] = frozenset(
    ("theory", "single_best_answer", "diagnostic_single_best_answer", "sba")
)

GOVERNANCE_SAFE_DEFAULTS: dict[str, bool] = {
    "safe_for_examiner": False,
    "examiner_scoring_allowed": False,
    "official_wset_question": False,
    "training_item_only": True,
    "uses_llm": False,
    "uses_api": False,
    "uses_embeddings": False,
    "uses_vector_db": False,
    "cloud_services_active": False,
}

ENRICHMENT_REQUIRED: tuple[str, ...] = (
    "source_support",
    "support_rationale",
    "diagnostic_role",
    "misconception_id",
    "causal_chain_id",
    "sat_relevance",
    "correct_rationale",
    "why_other_options_are_wrong",
    "remediation_recommendation",
    "attempt_analytics_placeholders",
    "full_governance_constants",
)


def classify_structured_question(item: dict) -> str:
    """Return the conservative adapter classification for an in-memory item."""
    reasons = explain_structured_question_classification(item)
    if _is_short_answer(item):
        return AdapterStatus.PRESERVE_FOR_OPEN_RESPONSE
    if any(_is_rejection_reason(reason) for reason in reasons):
        return AdapterStatus.REJECT_OR_DEFER
    return AdapterStatus.ADAPTER_READY_CLEAN_PILOT


def explain_structured_question_classification(item: dict) -> list[str]:
    """Return deterministic reasons for the adapter classification."""
    if not isinstance(item, dict):
        return ["item must be a dict"]

    if _is_short_answer(item):
        return ["short_answer records are preserved for open-response"]

    reasons: list[str] = []

    question_type = item.get("question_type")
    if question_type not in SBA_LIKE_QUESTION_TYPES:
        reasons.append("question_type must be theory or SBA-like")

    if item.get("safe_for_examiner") is not False:
        reasons.append("safe_for_examiner must be false")

    options = item.get("options")
    if not isinstance(options, Mapping):
        reasons.append("options must be present as a dict")
    else:
        option_keys = set(str(key) for key in options.keys())
        missing = [key for key in OPTION_KEYS if key not in option_keys]
        extra = sorted(option_keys - set(OPTION_KEYS))
        if missing:
            reasons.append("options missing required keys: " + ", ".join(missing))
        if extra:
            reasons.append("options contains unexpected keys: " + ", ".join(extra))

        normalized_texts: list[str] = []
        for key in OPTION_KEYS:
            value = options.get(key)
            if not _non_empty_string(value):
                reasons.append(f"options.{key} must be non-empty")
            else:
                normalized_texts.append(_normalize_text(str(value)))

        if len(normalized_texts) != len(set(normalized_texts)):
            reasons.append("option text must be unique after normalization")

    answer_letter = item.get("correct_answer_letter")
    if answer_letter not in VALID_ANSWER_LETTERS:
        reasons.append("correct_answer_letter must be A, B, C, or D")

    correct_answer_text = item.get("correct_answer_text")
    if not _non_empty_string(correct_answer_text):
        reasons.append("correct_answer_text must be non-empty")
    elif isinstance(options, Mapping) and answer_letter in VALID_ANSWER_LETTERS:
        selected_text = options.get(answer_letter)
        if _normalize_text(str(selected_text)) != _normalize_text(correct_answer_text):
            reasons.append("correct_answer_text must match selected option text")

    if not item.get("expected_topics"):
        reasons.append("expected_topics must be present")
    if not _non_empty_string(item.get("expected_reasoning_type")):
        reasons.append("expected_reasoning_type must be present")

    return reasons


def build_adapter_lineage(
    item: dict, source_bank_path: str, adapter_version: str = "structured_adapter_v0"
) -> dict:
    """Return lineage metadata only for a structured question-bank record."""
    return {
        "source_bank_path": source_bank_path,
        "source_question_id": item.get("question_id") if isinstance(item, Mapping) else None,
        "source_question_type": item.get("question_type") if isinstance(item, Mapping) else None,
        "source_source_type": item.get("source_type") if isinstance(item, Mapping) else None,
        "adapter_version": adapter_version,
        "adapted_at": None,
        "transformation_notes": [
            "skeleton mapping only",
            "source support, diagnostics, feedback, and remediation are not generated",
        ],
    }


def map_structured_question_skeleton(item: dict, source_bank_path: str) -> dict:
    """Map an in-memory source item to an intentionally incomplete skeleton."""
    status = classify_structured_question(item)
    reasons = explain_structured_question_classification(item)
    lineage = build_adapter_lineage(item, source_bank_path)
    options = item.get("options") if isinstance(item.get("options"), Mapping) else {}
    correct_answer_letter = item.get("correct_answer_letter")

    return {
        "schema_version": "diagnostic_sba_item_v1",
        "adapter_status": "requires_enrichment",
        "classification_status": status,
        "classification_reasons": reasons,
        "identity": {
            "item_id": f"diag_sba_from_structured_{item.get('question_id')}",
            "item_version": "0.0.0-skeleton",
            "created_by": "structured_question_bank_adapter_skeleton",
            "generation_method": "structured_question_bank_adapter_skeleton",
            "training_item_only": True,
            "source_question_id": item.get("question_id"),
        },
        "curriculum": {
            "ra_id": None,
            "topic": None,
            "subtopic": None,
            "difficulty": item.get("difficulty"),
            "learning_objective": None,
            "topic_candidates": copy.deepcopy(item.get("expected_topics")),
            "causal_chain_candidates": copy.deepcopy(item.get("expected_causal_links")),
            "keyword_candidates": copy.deepcopy(item.get("expected_keywords")),
        },
        "question": {
            "stem": item.get("question_text"),
            "question_type": "diagnostic_single_best_answer",
            "expected_reasoning_type": item.get("expected_reasoning_type"),
        },
        "options": {
            key: {
                "option_id": key,
                "option_text": options.get(key),
                "is_correct": key == correct_answer_letter,
                "diagnostic_role": None,
                "misconception_id": None,
                "misconception_description": None,
            }
            for key in OPTION_KEYS
        },
        "source_support": {
            "source_ids": [],
            "source_chunks": [],
            "support_rationale": None,
            "status": "missing",
        },
        "feedback": {
            "correct_rationale": None,
            "why_other_options_are_wrong": {key: None for key in OPTION_KEYS},
            "remediation_recommendation": None,
            "status": "missing",
        },
        "governance": dict(GOVERNANCE_SAFE_DEFAULTS),
        "attempt_analytics_placeholders": {
            "response_time": None,
            "confidence": None,
            "answer_changed": None,
            "diagnosed_error_type": None,
            "hesitation": None,
            "recommended_next_action": None,
        },
        "adapter_lineage": lineage,
        "original_answer": {
            "correct_answer_letter": item.get("correct_answer_letter"),
            "correct_answer_text": item.get("correct_answer_text"),
        },
        "enrichment_required": list(ENRICHMENT_REQUIRED),
        "valid_diagnostic_item": False,
    }


def _is_short_answer(item: Any) -> bool:
    return isinstance(item, Mapping) and item.get("question_type") == "short_answer"


def _missing_source_grounding(item: Mapping[str, Any]) -> bool:
    source_support = item.get("source_support")
    if not isinstance(source_support, Mapping):
        return True
    return not (
        _non_empty_sequence(source_support.get("source_ids"))
        and _non_empty_sequence(source_support.get("source_chunks"))
        and _non_empty_string(source_support.get("support_rationale"))
    )


def _missing_option_diagnostics(item: Mapping[str, Any]) -> bool:
    option_metadata = item.get("option_metadata")
    if not isinstance(option_metadata, Mapping):
        return True
    for key in OPTION_KEYS:
        metadata = option_metadata.get(key)
        if not isinstance(metadata, Mapping):
            return True
        if not _non_empty_string(metadata.get("diagnostic_role")):
            return True
    return False


def _is_rejection_reason(reason: str) -> bool:
    return reason not in {
        "source grounding enrichment required",
        "option diagnostic enrichment required",
    }


def _non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _non_empty_sequence(value: Any) -> bool:
    return isinstance(value, (list, tuple)) and bool(value)


def _normalize_text(value: str) -> str:
    return " ".join(value.lower().split())
