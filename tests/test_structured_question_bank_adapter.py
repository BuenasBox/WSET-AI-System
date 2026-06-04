from __future__ import annotations

import builtins
import copy
import unittest
from unittest.mock import patch

from tools.question_generation.diagnostic_sba_validator import validate_diagnostic_sba_item
from tools.question_generation.structured_question_bank_adapter import (
    AdapterStatus,
    build_adapter_lineage,
    classify_structured_question,
    explain_structured_question_classification,
    map_structured_question_skeleton,
)


SOURCE_BANK_PATH = "knowledge/question-bank/structured/wset3_questions.json"


def clean_source_item() -> dict:
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


class StructuredQuestionBankAdapterTests(unittest.TestCase):
    def test_clean_candidate_classified_as_adapter_ready_clean_pilot(self) -> None:
        self.assertEqual(
            classify_structured_question(clean_source_item()),
            AdapterStatus.ADAPTER_READY_CLEAN_PILOT,
        )

    def test_short_answer_classified_as_preserve_for_open_response(self) -> None:
        item = clean_source_item()
        item["question_type"] = "short_answer"

        self.assertEqual(
            classify_structured_question(item),
            AdapterStatus.PRESERVE_FOR_OPEN_RESPONSE,
        )
        self.assertIn(
            "short_answer records are preserved for open-response",
            explain_structured_question_classification(item),
        )

    def test_missing_options_rejected(self) -> None:
        item = clean_source_item()
        item.pop("options")

        self.assertEqual(classify_structured_question(item), AdapterStatus.REJECT_OR_DEFER)
        self.assertIn("options must be present as a dict", explain_structured_question_classification(item))

    def test_missing_a_d_option_rejected(self) -> None:
        item = clean_source_item()
        item["options"].pop("D")

        self.assertEqual(classify_structured_question(item), AdapterStatus.REJECT_OR_DEFER)
        self.assertIn(
            "options missing required keys: D",
            explain_structured_question_classification(item),
        )

    def test_empty_option_rejected(self) -> None:
        item = clean_source_item()
        item["options"]["B"] = " "

        self.assertEqual(classify_structured_question(item), AdapterStatus.REJECT_OR_DEFER)
        self.assertIn("options.B must be non-empty", explain_structured_question_classification(item))

    def test_duplicate_option_text_rejected(self) -> None:
        item = clean_source_item()
        item["options"]["B"] = " higher   retained acidity "

        self.assertEqual(classify_structured_question(item), AdapterStatus.REJECT_OR_DEFER)
        self.assertIn(
            "option text must be unique after normalization",
            explain_structured_question_classification(item),
        )

    def test_invalid_correct_answer_rejected(self) -> None:
        item = clean_source_item()
        item["correct_answer_letter"] = "Verdadero"

        self.assertEqual(classify_structured_question(item), AdapterStatus.REJECT_OR_DEFER)
        self.assertIn(
            "correct_answer_letter must be A, B, C, or D",
            explain_structured_question_classification(item),
        )

    def test_safe_for_examiner_true_rejected(self) -> None:
        item = clean_source_item()
        item["safe_for_examiner"] = True

        self.assertEqual(classify_structured_question(item), AdapterStatus.REJECT_OR_DEFER)
        self.assertIn("safe_for_examiner must be false", explain_structured_question_classification(item))

    def test_classification_reasons_are_deterministic(self) -> None:
        item = clean_source_item()
        item["safe_for_examiner"] = True
        item["options"]["A"] = ""
        item["correct_answer_letter"] = "Falso"

        first = explain_structured_question_classification(item)
        second = explain_structured_question_classification(copy.deepcopy(item))

        self.assertEqual(first, second)
        self.assertEqual(
            first,
            [
                "safe_for_examiner must be false",
                "options.A must be non-empty",
                "correct_answer_letter must be A, B, C, or D",
            ],
        )

    def test_lineage_preserves_source_question_id_and_path(self) -> None:
        lineage = build_adapter_lineage(clean_source_item(), SOURCE_BANK_PATH)

        self.assertEqual(lineage["source_question_id"], "Q001")
        self.assertEqual(lineage["source_bank_path"], SOURCE_BANK_PATH)
        self.assertEqual(lineage["adapter_version"], "structured_adapter_v0")

    def test_skeleton_preserves_stem_and_options(self) -> None:
        skeleton = map_structured_question_skeleton(clean_source_item(), SOURCE_BANK_PATH)

        self.assertEqual(
            skeleton["question"]["stem"],
            "Which factor best explains the training-only relationship?",
        )
        self.assertEqual(skeleton["options"]["A"]["option_text"], "Higher retained acidity")
        self.assertEqual(skeleton["options"]["D"]["option_text"], "Only oak-derived acidity")

    def test_skeleton_sets_exactly_one_correct_option(self) -> None:
        skeleton = map_structured_question_skeleton(clean_source_item(), SOURCE_BANK_PATH)

        correct_keys = [key for key, option in skeleton["options"].items() if option["is_correct"]]

        self.assertEqual(correct_keys, ["A"])

    def test_skeleton_uses_governance_safe_values(self) -> None:
        skeleton = map_structured_question_skeleton(clean_source_item(), SOURCE_BANK_PATH)

        self.assertEqual(
            skeleton["governance"],
            {
                "safe_for_examiner": False,
                "examiner_scoring_allowed": False,
                "official_wset_question": False,
                "training_item_only": True,
                "uses_llm": False,
                "uses_api": False,
                "uses_embeddings": False,
                "uses_vector_db": False,
                "cloud_services_active": False,
            },
        )

    def test_skeleton_includes_enrichment_required(self) -> None:
        skeleton = map_structured_question_skeleton(clean_source_item(), SOURCE_BANK_PATH)

        self.assertEqual(skeleton["adapter_status"], "requires_enrichment")
        for field in (
            "source_support",
            "support_rationale",
            "diagnostic_role",
            "misconception_id",
            "causal_chain_id",
            "sat_relevance",
            "correct_rationale",
            "why_other_options_are_wrong",
            "remediation_recommendation",
        ):
            self.assertIn(field, skeleton["enrichment_required"])

    def test_skeleton_does_not_mutate_input(self) -> None:
        item = clean_source_item()
        before = copy.deepcopy(item)

        classify_structured_question(item)
        explain_structured_question_classification(item)
        build_adapter_lineage(item, SOURCE_BANK_PATH)
        map_structured_question_skeleton(item, SOURCE_BANK_PATH)

        self.assertEqual(item, before)

    def test_skeleton_does_not_pass_full_diagnostic_validator_before_enrichment(self) -> None:
        skeleton = map_structured_question_skeleton(clean_source_item(), SOURCE_BANK_PATH)

        errors = validate_diagnostic_sba_item(skeleton)

        self.assertTrue(errors)
        self.assertEqual(skeleton["question"]["question_type"], "single_best_answer")
        self.assertNotIn('question.question_type must equal "single_best_answer"', errors)
        self.assertIn("source_support.source_ids must be a non-empty list", errors)

    def test_no_file_writes(self) -> None:
        item = clean_source_item()
        original_open = builtins.open

        def fail_open(*args, **kwargs):
            raise AssertionError("adapter skeleton must not open files")

        with patch("builtins.open", side_effect=fail_open):
            self.assertEqual(
                classify_structured_question(item),
                AdapterStatus.ADAPTER_READY_CLEAN_PILOT,
            )
            build_adapter_lineage(item, SOURCE_BANK_PATH)
            map_structured_question_skeleton(item, SOURCE_BANK_PATH)

        self.assertIs(builtins.open, original_open)

    def test_no_bulk_conversion(self) -> None:
        skeleton = map_structured_question_skeleton(clean_source_item(), SOURCE_BANK_PATH)

        self.assertIsInstance(skeleton, dict)
        self.assertNotIsInstance(skeleton, list)
        self.assertEqual(skeleton["classification_status"], AdapterStatus.ADAPTER_READY_CLEAN_PILOT)


if __name__ == "__main__":
    unittest.main()
