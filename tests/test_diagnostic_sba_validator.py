"""Tests for the Phase 4A.3 Diagnostic SBA item validator."""

from __future__ import annotations

import ast
import copy
import inspect
import unittest
from unittest.mock import patch

from tools.question_generation import diagnostic_sba_validator as validator_module
from tools.question_generation.diagnostic_sba_validator import (
    is_valid_diagnostic_sba_item,
    validate_diagnostic_sba_item,
)


def valid_item() -> dict:
    return {
        "identity": {
            "item_id": "diag_sba_validator_fixture_001",
            "item_version": "1.0.0",
            "generation_method": "manual_schema_fixture",
            "training_item_only": True,
        },
        "curriculum": {
            "ra_id": "RA1",
            "topic": "viticulture",
            "subtopic": "climate_and_acidity",
            "difficulty": "foundational",
            "learning_objective": "Identify a source-grounded cause-effect relationship.",
        },
        "question": {
            "stem": "Which option best describes the source-grounded relationship?",
            "question_type": "single_best_answer",
            "expected_reasoning_type": "cause_effect",
        },
        "options": {
            "A": {
                "option_id": "A",
                "option_text": "Cooler growing conditions can help grapes retain acidity.",
                "is_correct": True,
                "diagnostic_role": "correct",
            },
            "B": {
                "option_id": "B",
                "option_text": "Cooler growing conditions always make wine lower in acidity.",
                "is_correct": False,
                "diagnostic_role": "misconception",
            },
            "C": {
                "option_id": "C",
                "option_text": "Climate affects ripeness but has no link to acidity.",
                "is_correct": False,
                "diagnostic_role": "partial_reasoning",
            },
            "D": {
                "option_id": "D",
                "option_text": "Acidity is determined only by cellar temperature.",
                "is_correct": False,
                "diagnostic_role": "causal_confusion",
            },
        },
        "source_support": {
            "source_ids": ["CC_SCHEMA_EXAMPLE"],
            "source_chunks": ["chunk_schema_example_001"],
            "support_rationale": "Source supports the correct answer and diagnostic contrast.",
        },
        "feedback": {
            "correct_rationale": "The correct answer follows the cited source support.",
            "why_other_options_are_wrong": {
                "A": "This is the correct answer.",
                "B": "This reverses the expected acidity relationship.",
                "C": "This notices climate but misses the acidity mechanism.",
                "D": "This confuses vineyard conditions with cellar conditions.",
            },
            "remediation_recommendation": "Review the linked source and retry.",
        },
        "governance": {
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
        "attempt_analytics_placeholders": {
            "response_time": None,
            "confidence": None,
            "answer_changed": None,
            "diagnosed_error_type": None,
            "hesitation": None,
            "recommended_next_action": None,
        },
    }


class TestDiagnosticSbaValidator(unittest.TestCase):
    def assertInvalidWith(self, item: dict, expected_substring: str) -> list[str]:
        errors = validate_diagnostic_sba_item(item)
        self.assertTrue(
            any(expected_substring in error for error in errors),
            f"Expected {expected_substring!r} in errors: {errors}",
        )
        return errors

    def test_valid_item_returns_empty_list(self) -> None:
        self.assertEqual(validate_diagnostic_sba_item(valid_item()), [])

    def test_missing_top_level_section_fails(self) -> None:
        item = valid_item()
        del item["curriculum"]
        self.assertInvalidWith(item, "missing top-level section: curriculum")

    def test_missing_identity_fields_fail(self) -> None:
        item = valid_item()
        item["identity"]["item_id"] = ""
        del item["identity"]["item_version"]
        self.assertInvalidWith(item, "identity.item_id")
        self.assertInvalidWith(item, "identity.item_version")

    def test_missing_curriculum_fields_fail(self) -> None:
        item = valid_item()
        item["curriculum"]["ra_id"] = ""
        del item["curriculum"]["topic"]
        self.assertInvalidWith(item, "curriculum.ra_id")
        self.assertInvalidWith(item, "curriculum.topic")

    def test_wrong_question_type_fails(self) -> None:
        item = valid_item()
        item["question"]["question_type"] = "diagnostic_single_best_answer"
        self.assertInvalidWith(item, 'question.question_type must equal "single_best_answer"')

    def test_fewer_than_four_options_fails(self) -> None:
        item = valid_item()
        del item["options"]["D"]
        self.assertInvalidWith(item, "options must contain exactly A, B, C, and D")

    def test_more_than_four_options_fails(self) -> None:
        item = valid_item()
        item["options"]["E"] = {
            "option_id": "E",
            "option_text": "Extra option.",
            "is_correct": False,
            "diagnostic_role": "keyword_trap",
        }
        self.assertInvalidWith(item, "options contains unexpected keys: E")

    def test_missing_option_key_fails(self) -> None:
        item = valid_item()
        del item["options"]["B"]
        self.assertInvalidWith(item, "options missing required keys: B")

    def test_extra_option_key_fails(self) -> None:
        item = valid_item()
        item["options"]["Z"] = item["options"]["D"]
        self.assertInvalidWith(item, "options contains unexpected keys: Z")

    def test_option_id_mismatch_fails(self) -> None:
        item = valid_item()
        item["options"]["C"]["option_id"] = "B"
        self.assertInvalidWith(item, "options.C.option_id must match key C")

    def test_duplicate_option_text_fails(self) -> None:
        item = valid_item()
        item["options"]["C"]["option_text"] = item["options"]["B"]["option_text"].upper()
        self.assertInvalidWith(item, "options.option_text values must be unique")

    def test_no_correct_answer_fails(self) -> None:
        item = valid_item()
        for option in item["options"].values():
            option["is_correct"] = False
        self.assertInvalidWith(item, "options must contain exactly one correct answer")

    def test_multiple_correct_answers_fail(self) -> None:
        item = valid_item()
        item["options"]["B"]["is_correct"] = True
        self.assertInvalidWith(item, "options must contain exactly one correct answer")

    def test_correct_option_diagnostic_role_not_correct_fails(self) -> None:
        item = valid_item()
        item["options"]["A"]["diagnostic_role"] = "causal_confusion"
        self.assertInvalidWith(item, "options.A.diagnostic_role must be correct")

    def test_incorrect_option_diagnostic_role_correct_fails(self) -> None:
        item = valid_item()
        item["options"]["B"]["diagnostic_role"] = "correct"
        self.assertInvalidWith(item, "options.B.diagnostic_role must not be correct")

    def test_missing_source_support_fails(self) -> None:
        item = valid_item()
        item["source_support"]["source_ids"] = []
        item["source_support"]["support_rationale"] = ""
        self.assertInvalidWith(item, "source_support.source_ids")
        self.assertInvalidWith(item, "source_support.support_rationale")

    def test_missing_feedback_fails(self) -> None:
        item = valid_item()
        item["feedback"]["correct_rationale"] = ""
        del item["feedback"]["why_other_options_are_wrong"]["C"]
        item["feedback"]["remediation_recommendation"] = ""
        self.assertInvalidWith(item, "feedback.correct_rationale")
        self.assertInvalidWith(item, "why_other_options_are_wrong")
        self.assertInvalidWith(item, "feedback.remediation_recommendation")

    def test_unsafe_governance_true_fails(self) -> None:
        item = valid_item()
        item["governance"]["safe_for_examiner"] = True
        item["governance"]["uses_api"] = True
        self.assertInvalidWith(item, "governance.safe_for_examiner must be false")
        self.assertInvalidWith(item, "governance.uses_api must be false")

    def test_forbidden_field_detected_anywhere_fails(self) -> None:
        item = valid_item()
        item["feedback"]["nested"] = {"examiner_score_value": "nope"}
        self.assertInvalidWith(item, "forbidden field detected")

    def test_unsafe_official_wording_fails(self) -> None:
        item = valid_item()
        item["feedback"]["remediation_recommendation"] = "This is a guaranteed pass."
        self.assertInvalidWith(item, "unsafe official-authority language")

    def test_validator_does_not_mutate_input(self) -> None:
        item = valid_item()
        before = copy.deepcopy(item)
        validate_diagnostic_sba_item(item)
        self.assertEqual(item, before)

    def test_error_list_order_deterministic(self) -> None:
        item = valid_item()
        item["governance"]["safe_for_examiner"] = True
        item["options"]["A"]["diagnostic_role"] = "keyword_trap"
        first = validate_diagnostic_sba_item(item)
        second = validate_diagnostic_sba_item(item)
        self.assertEqual(first, second)

    def test_is_valid_helper_works(self) -> None:
        self.assertTrue(is_valid_diagnostic_sba_item(valid_item()))
        item = valid_item()
        item["governance"]["examiner_scoring_allowed"] = True
        self.assertFalse(is_valid_diagnostic_sba_item(item))

    def test_no_file_io(self) -> None:
        with patch("builtins.open", side_effect=AssertionError("open called")):
            self.assertEqual(validate_diagnostic_sba_item(valid_item()), [])

    def test_no_external_dependencies(self) -> None:
        source = inspect.getsource(validator_module)
        tree = ast.parse(source)
        imports: list[str] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.extend(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imports.append(node.module.split(".")[0])
        self.assertEqual(sorted(set(imports)), ["__future__", "collections", "typing"])


if __name__ == "__main__":
    unittest.main()
