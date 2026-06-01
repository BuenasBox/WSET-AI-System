"""Artificial diagnostic SBA enrichment fixtures for tests only.

These fixtures are not generated questions, not migrated bank items, and not
official WSET material. They use generic training wording to exercise
enrichment readiness and validation behavior.
"""

from __future__ import annotations

import copy


SAFE_GOVERNANCE: dict[str, bool] = {
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


def make_fully_enriched_item() -> dict:
    """Return a complete artificial fixture that passes the SBA validator."""
    return {
        "identity": {
            "item_id": "fixture_diag_sba_enriched_001",
            "item_version": "1.0.0",
            "generation_method": "test_fixture_manual",
            "training_item_only": True,
        },
        "curriculum": {
            "ra_id": "RA1",
            "topic": "training_topic",
            "subtopic": "cause_effect_practice",
            "difficulty": "foundational",
            "learning_objective": "Practice identifying a supported cause-effect relationship.",
        },
        "question": {
            "stem": "In this training item, which option best matches the supported cause-effect relationship?",
            "question_type": "single_best_answer",
            "expected_reasoning_type": "cause_effect",
        },
        "options": {
            "A": {
                "option_id": "A",
                "option_text": "The supported factor increases the observed effect.",
                "is_correct": True,
                "diagnostic_role": "correct",
            },
            "B": {
                "option_id": "B",
                "option_text": "The supported factor decreases the observed effect.",
                "is_correct": False,
                "diagnostic_role": "causal_confusion",
            },
            "C": {
                "option_id": "C",
                "option_text": "The observed effect is unrelated to the factor.",
                "is_correct": False,
                "diagnostic_role": "misconception",
                "misconception_id": "MC_FIXTURE_CAUSAL_DISCONNECT",
                "misconception_description": "Artificial fixture misconception for tests only.",
            },
            "D": {
                "option_id": "D",
                "option_text": "The relationship depends only on a similar term.",
                "is_correct": False,
                "diagnostic_role": "terminology_confusion",
            },
        },
        "source_support": {
            "source_ids": ["FIXTURE_KNOWLEDGE_NODE_001"],
            "source_chunks": ["fixture_chunk_001"],
            "support_rationale": "The artificial fixture source supports the correct relationship and the contrast.",
            "source_role": "knowledge_map_support",
        },
        "feedback": {
            "correct_rationale": "The correct option follows the artificial fixture support.",
            "why_other_options_are_wrong": {
                "A": "This is the correct answer.",
                "B": "This reverses the supported relationship.",
                "C": "This ignores the supported relationship.",
                "D": "This confuses a similar term with the supported relationship.",
            },
            "remediation_recommendation": "Review the training topic and repeat one related practice item.",
            "remediation_target": {
                "target_type": "topic",
                "target_id": "training_topic",
            },
        },
        "governance": copy.deepcopy(SAFE_GOVERNANCE),
        "attempt_analytics_placeholders": {
            "response_time": None,
            "confidence": None,
            "answer_changed": None,
            "diagnosed_error_type": None,
            "hesitation": None,
            "recommended_next_action": None,
        },
        "enrichment_status": "enrichment_complete",
        "human_review": {
            "requires_human_review": False,
            "reasons": [],
        },
        "fixture_notice": "Artificial training-only test fixture.",
    }


def make_partially_enriched_item() -> dict:
    """Return an artificial fixture with missing source support."""
    item = make_fully_enriched_item()
    item["identity"]["item_id"] = "fixture_diag_sba_partial_001"
    item["source_support"]["source_ids"] = []
    item["source_support"]["source_chunks"] = []
    item["source_support"]["support_rationale"] = ""
    item["enrichment_status"] = "source_support_missing"
    return item


def make_human_review_item() -> dict:
    """Return an artificial fixture that must be deferred for human review."""
    item = make_fully_enriched_item()
    item["identity"]["item_id"] = "fixture_diag_sba_human_review_001"
    item["options"]["B"]["diagnostic_role"] = "distractor_unknown"
    item["enrichment_status"] = "defer_for_human_review"
    item["human_review"] = {
        "requires_human_review": True,
        "reasons": ["Ambiguous distractor evidence in artificial fixture."],
    }
    return item


def make_unsafe_governance_item() -> dict:
    """Return an artificial fixture with unsafe governance values."""
    item = make_fully_enriched_item()
    item["identity"]["item_id"] = "fixture_diag_sba_unsafe_governance_001"
    item["governance"]["safe_for_examiner"] = True
    item["governance"]["examiner_scoring_allowed"] = True
    item["enrichment_status"] = "governance_incomplete"
    return item
