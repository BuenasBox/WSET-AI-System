from __future__ import annotations

import copy
import unittest

from tools.question_generation.diagnostic_sba_validator import validate_diagnostic_sba_item


ALLOWED_SOURCE_ROLES = {
    "official_grounding",
    "pedagogical_explanation",
    "knowledge_map_support",
}
ALLOWED_REMEDIATION_TARGET_TYPES = {
    "topic",
    "causal_chain",
    "misconception",
    "sat_skill",
    "source_chunk",
}
ALLOWED_DIAGNOSTIC_ROLES = {
    "correct",
    "misconception",
    "partial_reasoning",
    "keyword_trap",
    "causal_confusion",
    "sat_confusion",
    "terminology_confusion",
    "process_confusion",
    "regional_confusion",
    "distractor_unknown",
}
SAFE_GOVERNANCE = {
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


def complete_enriched_item() -> dict:
    return {
        "identity": {
            "item_id": "diag_sba_enriched_contract_001",
            "item_version": "1.0.0",
            "generation_method": "structured_question_bank_enrichment_contract_fixture",
            "training_item_only": True,
        },
        "curriculum": {
            "ra_id": "RA1",
            "topic": "climate",
            "subtopic": "acidity",
            "difficulty": "intermediate",
            "learning_objective": "Identify a source-grounded cause-effect relationship.",
        },
        "question": {
            "stem": "Which factor best explains the training-only relationship?",
            "question_type": "single_best_answer",
            "expected_reasoning_type": "cause_effect",
        },
        "options": {
            "A": {
                "option_id": "A",
                "option_text": "Higher retained acidity",
                "is_correct": True,
                "diagnostic_role": "correct",
            },
            "B": {
                "option_id": "B",
                "option_text": "Lower retained acidity",
                "is_correct": False,
                "diagnostic_role": "causal_confusion",
            },
            "C": {
                "option_id": "C",
                "option_text": "No relationship to acidity",
                "is_correct": False,
                "diagnostic_role": "misconception",
                "misconception_id": "MC_COOL_CLIMATE_LOW_ACIDITY",
                "misconception_evidence": {
                    "option_keyword_overlap": ["cool climate", "acidity"],
                    "expected_topic_support": ["climate", "acidity"],
                    "known_misconception_node_exists": True,
                },
            },
            "D": {
                "option_id": "D",
                "option_text": "Only oak-derived acidity",
                "is_correct": False,
                "diagnostic_role": "terminology_confusion",
            },
        },
        "source_support": {
            "source_ids": ["CC_COOL_CLIMATE_ACIDITY"],
            "source_chunks": ["official_chunk_ra1_climate_acidity"],
            "support_rationale": "The cited support grounds the relationship and the diagnostic contrast.",
            "source_role": "knowledge_map_support",
        },
        "feedback": {
            "correct_rationale": "The correct option follows the cited source support.",
            "why_other_options_are_wrong": {
                "A": "This is the correct answer.",
                "B": "This reverses the supported cause-effect relationship.",
                "C": "This reflects the linked misconception about cool climates and acidity.",
                "D": "This confuses structural acidity with oak terminology.",
            },
            "remediation_recommendation": "Review the climate and acidity causal chain.",
            "remediation_target": {
                "target_type": "causal_chain",
                "target_id": "CC_COOL_CLIMATE_ACIDITY",
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
        "sat_relevance": [],
    }


def validate_enrichment_contract(item: dict) -> list[str]:
    errors: list[str] = []

    source_support = item.get("source_support", {})
    if source_support.get("source_role") not in ALLOWED_SOURCE_ROLES:
        errors.append("source_support.source_role must be an allowed value")
    if not source_support.get("source_ids") or not source_support.get("source_chunks"):
        errors.append("source support must include source_ids and source_chunks")

    correct_count = 0
    for key in ("A", "B", "C", "D"):
        option = item.get("options", {}).get(key, {})
        role = option.get("diagnostic_role")
        if role not in ALLOWED_DIAGNOSTIC_ROLES:
            errors.append(f"options.{key}.diagnostic_role must be an allowed value")
        if option.get("is_correct") is True:
            correct_count += 1
            if role != "correct":
                errors.append(f"options.{key}.diagnostic_role must be correct")
        elif role == "correct":
            errors.append(f"options.{key}.diagnostic_role must not be correct")
        if role == "distractor_unknown" and item.get("enrichment_status") == "enrichment_complete":
            errors.append("distractor_unknown cannot be enrichment_complete")
        if option.get("misconception_id") and not option.get("misconception_evidence"):
            errors.append(f"options.{key}.misconception_id requires evidence")

    if correct_count != 1:
        errors.append("exactly one option must be correct")

    remediation_target = item.get("feedback", {}).get("remediation_target", {})
    if remediation_target.get("target_type") not in ALLOWED_REMEDIATION_TARGET_TYPES:
        errors.append("feedback.remediation_target.target_type must be an allowed value")

    for field, expected in SAFE_GOVERNANCE.items():
        if item.get("governance", {}).get(field) is not expected:
            errors.append(f"governance.{field} must remain {str(expected).lower()}")

    if "official WSET question" in str(item):
        errors.append("official wording claim is forbidden")

    return errors


class StructuredQuestionBankEnrichmentContractTests(unittest.TestCase):
    def test_complete_enrichment_fixture_can_pass_diagnostic_validator(self) -> None:
        item = complete_enriched_item()

        self.assertEqual(validate_enrichment_contract(item), [])
        self.assertEqual(validate_diagnostic_sba_item(item), [])

    def test_missing_source_support_remains_invalid(self) -> None:
        item = complete_enriched_item()
        item["source_support"]["source_ids"] = []

        self.assertIn("source support must include source_ids and source_chunks", validate_enrichment_contract(item))
        self.assertIn("source_support.source_ids must be a non-empty list", validate_diagnostic_sba_item(item))

    def test_correct_option_role_must_be_correct(self) -> None:
        item = complete_enriched_item()
        item["options"]["A"]["diagnostic_role"] = "causal_confusion"

        self.assertIn("options.A.diagnostic_role must be correct", validate_enrichment_contract(item))
        self.assertIn(
            "options.A.diagnostic_role must be correct for the correct option",
            validate_diagnostic_sba_item(item),
        )

    def test_incorrect_options_cannot_be_correct(self) -> None:
        item = complete_enriched_item()
        item["options"]["B"]["diagnostic_role"] = "correct"

        self.assertIn("options.B.diagnostic_role must not be correct", validate_enrichment_contract(item))
        self.assertIn(
            "options.B.diagnostic_role must not be correct for an incorrect option",
            validate_diagnostic_sba_item(item),
        )

    def test_unknown_distractor_role_allowed_only_as_incomplete_or_defer_state(self) -> None:
        item = complete_enriched_item()
        item["options"]["B"]["diagnostic_role"] = "distractor_unknown"

        self.assertIn("distractor_unknown cannot be enrichment_complete", validate_enrichment_contract(item))
        item["enrichment_status"] = "option_diagnostics_missing"
        self.assertNotIn("distractor_unknown cannot be enrichment_complete", validate_enrichment_contract(item))

    def test_unsafe_governance_rejected(self) -> None:
        item = complete_enriched_item()
        item["governance"]["examiner_scoring_allowed"] = True

        self.assertIn("governance.examiner_scoring_allowed must remain false", validate_enrichment_contract(item))
        self.assertIn("governance.examiner_scoring_allowed must be false", validate_diagnostic_sba_item(item))

    def test_misconception_id_cannot_be_invented_if_evidence_absent(self) -> None:
        item = complete_enriched_item()
        item["options"]["C"].pop("misconception_evidence")

        self.assertIn("options.C.misconception_id requires evidence", validate_enrichment_contract(item))

    def test_source_support_role_must_be_allowed_enum(self) -> None:
        item = complete_enriched_item()
        item["source_support"]["source_role"] = "official_authority"

        self.assertIn("source_support.source_role must be an allowed value", validate_enrichment_contract(item))

    def test_remediation_target_must_be_allowed_type(self) -> None:
        item = complete_enriched_item()
        item["feedback"]["remediation_target"]["target_type"] = "official_score"

        self.assertIn(
            "feedback.remediation_target.target_type must be an allowed value",
            validate_enrichment_contract(item),
        )

    def test_enrichment_checks_do_not_mutate_item(self) -> None:
        item = complete_enriched_item()
        before = copy.deepcopy(item)

        validate_enrichment_contract(item)
        validate_diagnostic_sba_item(item)

        self.assertEqual(item, before)

    def test_official_wording_claim_rejected(self) -> None:
        item = complete_enriched_item()
        item["feedback"]["correct_rationale"] = "This is an official WSET question."

        self.assertIn("official wording claim is forbidden", validate_enrichment_contract(item))
        self.assertIn(
            "unsafe official-authority language at $.feedback.correct_rationale: official wset question",
            validate_diagnostic_sba_item(item),
        )

    def test_full_enriched_item_passes_validate_diagnostic_sba_item(self) -> None:
        self.assertEqual(validate_diagnostic_sba_item(complete_enriched_item()), [])


if __name__ == "__main__":
    unittest.main()
