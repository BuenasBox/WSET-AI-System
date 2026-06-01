"""Skeleton enrichment helpers for structured question-bank adapter outputs.

The functions in this module are pure and standard-library only. They do not
read source banks, inspect knowledge assets, write converted items, or generate
new content. Their job is to make missing enrichment explicit.
"""

from __future__ import annotations

import copy
from collections.abc import Mapping
from typing import Any


class EnrichmentStatus:
    ENRICHMENT_COMPLETE = "enrichment_complete"
    SOURCE_SUPPORT_MISSING = "source_support_missing"
    OPTION_DIAGNOSTICS_MISSING = "option_diagnostics_missing"
    RATIONALE_MISSING = "rationale_missing"
    REMEDIATION_MISSING = "remediation_missing"
    GOVERNANCE_INCOMPLETE = "governance_incomplete"
    DEFER_FOR_HUMAN_REVIEW = "defer_for_human_review"


OPTION_KEYS: tuple[str, ...] = ("A", "B", "C", "D")

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

STATUS_SUMMARIES: tuple[tuple[str, str], ...] = (
    (EnrichmentStatus.SOURCE_SUPPORT_MISSING, "source support is missing or incomplete"),
    (EnrichmentStatus.OPTION_DIAGNOSTICS_MISSING, "option diagnostic metadata is missing or incomplete"),
    (EnrichmentStatus.RATIONALE_MISSING, "correct or distractor rationales are missing"),
    (EnrichmentStatus.REMEDIATION_MISSING, "remediation recommendation or target is missing"),
    (EnrichmentStatus.GOVERNANCE_INCOMPLETE, "governance fields are missing or unsafe"),
    (EnrichmentStatus.DEFER_FOR_HUMAN_REVIEW, "human review is required before enrichment can complete"),
)


def evaluate_enrichment_readiness(skeleton: dict) -> list[str]:
    """Return deterministic incomplete enrichment statuses for a skeleton."""
    if not isinstance(skeleton, dict):
        return [
            EnrichmentStatus.SOURCE_SUPPORT_MISSING,
            EnrichmentStatus.OPTION_DIAGNOSTICS_MISSING,
            EnrichmentStatus.RATIONALE_MISSING,
            EnrichmentStatus.REMEDIATION_MISSING,
            EnrichmentStatus.GOVERNANCE_INCOMPLETE,
            EnrichmentStatus.DEFER_FOR_HUMAN_REVIEW,
        ]

    statuses: list[str] = []

    if _source_support_missing(skeleton):
        statuses.append(EnrichmentStatus.SOURCE_SUPPORT_MISSING)
    if _option_diagnostics_missing(skeleton):
        statuses.append(EnrichmentStatus.OPTION_DIAGNOSTICS_MISSING)
    if _rationale_missing(skeleton):
        statuses.append(EnrichmentStatus.RATIONALE_MISSING)
    if _remediation_missing(skeleton):
        statuses.append(EnrichmentStatus.REMEDIATION_MISSING)
    if _governance_incomplete(skeleton):
        statuses.append(EnrichmentStatus.GOVERNANCE_INCOMPLETE)
    if _explicit_human_review_required(skeleton):
        statuses.append(EnrichmentStatus.DEFER_FOR_HUMAN_REVIEW)

    return statuses


def build_enrichment_placeholders(skeleton: dict) -> dict:
    """Return a copy with explicit enrichment placeholder sections."""
    state = copy.deepcopy(skeleton)

    state["enrichment_statuses"] = evaluate_enrichment_readiness(state)
    state["enrichment_ready"] = False
    state["validator_ready"] = False

    state["source_support"] = {
        "source_ids": [],
        "source_chunks": [],
        "support_rationale": None,
        "source_role": None,
        "status": "missing",
        "allowed_future_sources": [
            "knowledge_map",
            "official_grounding",
            "wine_with_jimmy_pedagogy",
            "sat_aliases",
            "canonical_dictionary",
            "original_structured_item",
        ],
    }
    state["option_diagnostics"] = {
        key: {
            "diagnostic_role": None,
            "status": "unknown",
            "requires_human_review": True,
        }
        for key in OPTION_KEYS
    }
    state["misconception_linkage"] = {
        key: {
            "misconception_id": None,
            "evidence": [],
            "status": "unknown",
        }
        for key in OPTION_KEYS
    }
    state["causal_chain_linkage"] = {
        "causal_chain_id": None,
        "evidence": [],
        "status": "unknown",
    }
    state["sat_relevance"] = {
        "aliases": [],
        "evidence": [],
        "status": "unknown",
    }
    state["rationales"] = {
        "correct_rationale": None,
        "distractor_rationales": {key: None for key in OPTION_KEYS},
        "status": "missing",
    }
    state["remediation"] = {
        "recommendation": None,
        "target_type": None,
        "target_id": None,
        "status": "missing",
    }
    state["human_review"] = {
        "requires_human_review": True,
        "reasons": summarize_enrichment_gaps(state),
    }

    state["enrichment_statuses"] = evaluate_enrichment_readiness(state)
    return state


def requires_human_review(enrichment_state: dict) -> bool:
    """Return True when enrichment is incomplete or explicitly deferred."""
    if not isinstance(enrichment_state, dict):
        return True
    human_review = enrichment_state.get("human_review")
    if isinstance(human_review, Mapping) and human_review.get("requires_human_review") is True:
        return True
    return bool(evaluate_enrichment_readiness(enrichment_state))


def summarize_enrichment_gaps(enrichment_state: dict) -> list[str]:
    """Return deterministic human-readable gap reasons."""
    statuses = set(evaluate_enrichment_readiness(enrichment_state))
    return [summary for status, summary in STATUS_SUMMARIES if status in statuses]


def is_enrichment_complete(enrichment_state: dict) -> bool:
    """Return True only when no enrichment statuses remain."""
    return not evaluate_enrichment_readiness(enrichment_state) and not requires_human_review(enrichment_state)


def _source_support_missing(state: Mapping[str, Any]) -> bool:
    source_support = _as_mapping(state.get("source_support"))
    return not (
        _non_empty_list(source_support.get("source_ids"))
        and _non_empty_list(source_support.get("source_chunks"))
        and _non_empty_string(source_support.get("support_rationale"))
    )


def _option_diagnostics_missing(state: Mapping[str, Any]) -> bool:
    options = _as_mapping(state.get("options"))
    for key in OPTION_KEYS:
        option = _as_mapping(options.get(key))
        role = option.get("diagnostic_role")
        if not _non_empty_string(role):
            diagnostics = _as_mapping(_as_mapping(state.get("option_diagnostics")).get(key))
            role = diagnostics.get("diagnostic_role")
        if not _non_empty_string(role) or role == "distractor_unknown":
            return True
    return False


def _rationale_missing(state: Mapping[str, Any]) -> bool:
    feedback = _as_mapping(state.get("feedback"))
    correct_rationale = feedback.get("correct_rationale")
    why_wrong = _as_mapping(feedback.get("why_other_options_are_wrong"))

    rationales = _as_mapping(state.get("rationales"))
    if not _non_empty_string(correct_rationale):
        correct_rationale = rationales.get("correct_rationale")
    if not _non_empty_string(correct_rationale):
        return True

    distractor_rationales = _as_mapping(rationales.get("distractor_rationales"))
    for key in OPTION_KEYS:
        if not _non_empty_string(why_wrong.get(key)) and not _non_empty_string(distractor_rationales.get(key)):
            return True
    return False


def _remediation_missing(state: Mapping[str, Any]) -> bool:
    feedback = _as_mapping(state.get("feedback"))
    remediation = _as_mapping(state.get("remediation"))
    recommendation = feedback.get("remediation_recommendation") or remediation.get("recommendation")
    target_type = _as_mapping(feedback.get("remediation_target")).get("target_type") or remediation.get("target_type")
    return not (_non_empty_string(recommendation) and _non_empty_string(target_type))


def _governance_incomplete(state: Mapping[str, Any]) -> bool:
    governance = _as_mapping(state.get("governance"))
    return any(governance.get(field) is not expected for field, expected in GOVERNANCE_SAFE_DEFAULTS.items())


def _explicit_human_review_required(state: Mapping[str, Any]) -> bool:
    human_review = state.get("human_review")
    if isinstance(human_review, Mapping) and human_review.get("requires_human_review") is True:
        return True
    return False


def _as_mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _non_empty_list(value: Any) -> bool:
    return isinstance(value, list) and bool(value)
