"""Contract tests for the future structured question bank adapter.

These tests intentionally do not import production adapter code because the
adapter does not exist yet. They use small in-memory fixtures to pin the
expected behavior that Phase 4A.3.7.3 should implement.
"""

from __future__ import annotations

import copy
import unittest

from tools.question_generation.diagnostic_sba_validator import validate_diagnostic_sba_item


SOURCE_BANK_PATH = "knowledge/question-bank/structured/wset3_questions.json"
REQUIRED_OPTION_KEYS = ("A", "B", "C", "D")
VALID_ANSWER_LETTERS = set(REQUIRED_OPTION_KEYS)
FULL_GOVERNANCE = {
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
REQUIRED_ENRICHMENT_FIELDS = (
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


def clean_source_record() -> dict:
    return {
        "question_id": "Q001",
        "question_text": "Which factor best explains the training-only relationship?",
        "question_type": "theory",
        "expected_topics": ["RA1", "climate", "acidity"],
        "expected_causal_links": ["CC_COOL_CLIMATE_ACIDITY"],
        "expected_keywords": ["cool climate", "acidity"],
        "expected_reasoning_type": "cause_effect",
        "difficulty": "intermediate",
        "source_type": "structured_question_bank",
        "safe_for_examiner": False,
        "options": {
            "A": "Higher retained acidity",
            "B": "Lower retained acidity",
            "C": "No relationship to acidity",
            "D": "Only oak-derived acidity",
        },
        "correct_answer_letter": "A",
        "correct_answer_text": "Higher retained acidity",
    }


def classify_source_record_contract(record: dict) -> tuple:
    reasons: list = []

    if record.get("question_type") == "short_answer":
        return "preserve_for_open_response", ("short_answer records are not forced into SBA",)

    if record.get("safe_for_examiner") is not False:
        reasons.append("safe_for_examiner must remain false")

    options = record.get("options")
    if not isinstance(options, dict):
        reasons.append("options must be present")
    else:
        option_keys = set(options)
        if option_keys != set(REQUIRED_OPTION_KEYS):
            reasons.append("options must contain exactly A, B, C, and D")
        for key in REQUIRED_OPTION_KEYS:
            if not str(options.get(key, "")).strip():
                reasons.append(f"options.{key} must be non-empty")
        normalized = [" ".join(str(options.get(key, "")).lower().split()) for key in REQUIRED_OPTION_KEYS]
        normalized_non_empty = [text for text in normalized if text]
        if len(normalized_non_empty) != len(set(normalized_non_empty)):
            reasons.append("option text must be unique after normalization")

    answer_letter = record.get("correct_answer_letter")
    if answer_letter not in VALID_ANSWER_LETTERS:
        reasons.append("correct_answer_letter must be A, B, C, or D")

    correct_answer_text = record.get("correct_answer_text")
    if not isinstance(correct_answer_text, str) or not correct_answer_text.strip():
        reasons.append("correct_answer_text must be non-empty")
    elif isinstance(options, dict) and answer_letter in VALID_ANSWER_LETTERS:
        selected_text = str(options.get(answer_letter, "")).strip()
        if selected_text != correct_answer_text.strip():
            reasons.append("correct_answer_text must match selected option text")

    if not record.get("expected_topics"):
        reasons.append("expected_topics must be present")
    if not record.get("expected_reasoning_type"):
        reasons.append("expected_reasoning_type must be present")

    if reasons:
        return "reject_or_defer", tuple(reasons)
    return "adapter_ready_clean_pilot", ()


def map_direct_draft_contract(record: dict) -> dict:
    category, reasons = classify_source_record_contract(record)
    options = record.get("options") if isinstance(record.get("options"), dict) else {}
    answer_letter = record.get("correct_answer_letter")
    return {
        "state": "mapped_draft",
        "classification_category": category,
        "rejection_or_deferral_reasons": list(reasons),
        "identity": {
            "item_id": f"diag_sba_from_structured_{record.get('question_id')}",
            "source_question_id": record.get("question_id"),
            "source_bank_path": SOURCE_BANK_PATH,
            "source_question_type": record.get("question_type"),
            "source_source_type": record.get("source_type"),
            "adapter_version": "contract-test",
            "adapted_at": "not_set_in_contract_test",
            "transformation_notes": ["direct mapping draft only"],
        },
        "curriculum": {
            "difficulty": record.get("difficulty"),
            "topic_candidates": copy.deepcopy(record.get("expected_topics")),
            "causal_chain_candidates": copy.deepcopy(record.get("expected_causal_links")),
            "keyword_candidates": copy.deepcopy(record.get("expected_keywords")),
        },
        "question": {
            "stem": record.get("question_text"),
            "question_type": "single_best_answer",
            "expected_reasoning_type": record.get("expected_reasoning_type"),
        },
        "options": {
            key: {
                "option_id": key,
                "option_text": options.get(key),
                "is_correct": key == answer_letter,
            }
            for key in REQUIRED_OPTION_KEYS
        },
        "governance": {
            "safe_for_examiner": record.get("safe_for_examiner"),
        },
        "required_enrichment_missing": list(REQUIRED_ENRICHMENT_FIELDS),
    }


def enriched_validator_compatible_item() -> dict:
    return {
        "identity": {
            "item_id": "diag_sba_from_structured_Q001",
            "item_version": "1.0.0",
            "generation_method": "structured_question_bank_adapter_contract_fixture",
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
                "diagnostic_role": "scope_error",
            },
            "D": {
                "option_id": "D",
                "option_text": "Only oak-derived acidity",
                "is_correct": False,
                "diagnostic_role": "term_confusion",
            },
        },
        "source_support": {
            "source_ids": ["CC_COOL_CLIMATE_ACIDITY"],
            "source_chunks": ["contract_fixture_chunk"],
            "support_rationale": "Contract fixture source support is present for validator compatibility.",
        },
        "feedback": {
            "correct_rationale": "The correct option follows the cited contract fixture support.",
            "why_other_options_are_wrong": {
                "A": "This is the correct answer.",
                "B": "This reverses the causal relationship.",
                "C": "This denies the tested relationship.",
                "D": "This confuses source of acidity with oak terminology.",
            },
            "remediation_recommendation": "Review the linked cause-effect relationship.",
        },
        "governance": copy.deepcopy(FULL_GOVERNANCE),
        "attempt_analytics_placeholders": {
            "response_time": None,
            "confidence": None,
            "answer_changed": None,
            "diagnosed_error_type": None,
            "hesitation": None,
            "recommended_next_action": None,
        },
    }


class StructuredQuestionBankAdapterContractTests(unittest.TestCase):
    def test_clean_sba_candidate_is_classified_for_pilot(self) -> None:
        category, reasons = classify_source_record_contract(clean_source_record())
        self.assertEqual(category, "adapter_ready_clean_pilot")
        self.assertEqual(reasons, ())

    def test_missing_options_rejects_or_defers(self) -> None:
        record = clean_source_record()
        record.pop("options")
        category, reasons = classify_source_record_contract(record)
        self.assertEqual(category, "reject_or_defer")
        self.assertIn("options must be present", reasons)

    def test_empty_options_reject_or_defer(self) -> None:
        record = clean_source_record()
        record["options"]["C"] = " "
        category, reasons = classify_source_record_contract(record)
        self.assertEqual(category, "reject_or_defer")
        self.assertIn("options.C must be non-empty", reasons)

    def test_duplicate_option_text_rejects_or_defers(self) -> None:
        record = clean_source_record()
        record["options"]["B"] = "Higher retained acidity"
        category, reasons = classify_source_record_contract(record)
        self.assertEqual(category, "reject_or_defer")
        self.assertIn("option text must be unique after normalization", reasons)

    def test_invalid_correct_answer_letter_rejects_or_defers(self) -> None:
        record = clean_source_record()
        record["correct_answer_letter"] = "Verdadero"
        category, reasons = classify_source_record_contract(record)
        self.assertEqual(category, "reject_or_defer")
        self.assertIn("correct_answer_letter must be A, B, C, or D", reasons)

    def test_short_answer_is_preserved_for_open_response(self) -> None:
        record = clean_source_record()
        record["question_type"] = "short_answer"
        record["options"] = {}
        record["correct_answer_letter"] = ""
        record["correct_answer_text"] = ""
        category, reasons = classify_source_record_contract(record)
        self.assertEqual(category, "preserve_for_open_response")
        self.assertIn("short_answer records are not forced into SBA", reasons)

    def test_unsafe_governance_rejects_or_defers(self) -> None:
        record = clean_source_record()
        record["safe_for_examiner"] = True
        category, reasons = classify_source_record_contract(record)
        self.assertEqual(category, "reject_or_defer")
        self.assertIn("safe_for_examiner must remain false", reasons)

    def test_field_mapping_expectations_for_direct_draft(self) -> None:
        draft = map_direct_draft_contract(clean_source_record())
        self.assertEqual(draft["identity"]["source_question_id"], "Q001")
        self.assertEqual(draft["question"]["stem"], clean_source_record()["question_text"])
        self.assertEqual(draft["curriculum"]["difficulty"], "intermediate")
        self.assertEqual(draft["options"]["A"]["option_text"], "Higher retained acidity")
        self.assertTrue(draft["options"]["A"]["is_correct"])
        self.assertFalse(draft["options"]["B"]["is_correct"])
        self.assertFalse(draft["governance"]["safe_for_examiner"])

    def test_lineage_preservation_fields_are_required(self) -> None:
        draft = map_direct_draft_contract(clean_source_record())
        identity = draft["identity"]
        for field in (
            "source_bank_path",
            "source_question_id",
            "source_question_type",
            "source_source_type",
            "adapter_version",
            "adapted_at",
            "transformation_notes",
        ):
            self.assertIn(field, identity)
        self.assertEqual(identity["source_bank_path"], SOURCE_BANK_PATH)

    def test_required_enrichment_fields_are_not_satisfied_by_direct_mapping(self) -> None:
        draft = map_direct_draft_contract(clean_source_record())
        for field in REQUIRED_ENRICHMENT_FIELDS:
            self.assertIn(field, draft["required_enrichment_missing"])

    def test_contract_helpers_do_not_mutate_input(self) -> None:
        record = clean_source_record()
        before = copy.deepcopy(record)
        classify_source_record_contract(record)
        map_direct_draft_contract(record)
        self.assertEqual(record, before)

    def test_no_bulk_conversion_contract(self) -> None:
        record = clean_source_record()
        draft = map_direct_draft_contract(record)
        self.assertIsInstance(draft, dict)
        self.assertNotIsInstance(draft, list)
        self.assertEqual(draft["state"], "mapped_draft")

    def test_future_validator_compatibility_after_full_enrichment(self) -> None:
        item = enriched_validator_compatible_item()
        self.assertEqual(validate_diagnostic_sba_item(item), [])

    def test_adapter_output_question_type_matches_canonical_value(self) -> None:
        """Adapter must write 'single_best_answer', never 'diagnostic_single_best_answer'."""
        from tools.question_generation.structured_question_bank_adapter import (
            map_structured_question_skeleton,
        )
        draft = map_structured_question_skeleton(clean_source_record(), SOURCE_BANK_PATH)
        self.assertEqual(draft["question"]["question_type"], "single_best_answer")

    def test_adapter_output_passes_validator_after_enrichment(self) -> None:
        """A minimally-enriched adapter output must pass the diagnostic SBA validator with 0 errors."""
        item = enriched_validator_compatible_item()
        errors = validate_diagnostic_sba_item(item)
        self.assertEqual(errors, [], errors)


if __name__ == "__main__":
    unittest.main()
