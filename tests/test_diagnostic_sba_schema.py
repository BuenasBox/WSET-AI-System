"""Tests for the Phase 4A.2 Diagnostic SBA item JSON Schema."""

from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


SCHEMA_PATH = (
    Path(__file__).parents[1]
    / "knowledge"
    / "enrichment"
    / "diagnostic_sba_item.schema.json"
)


def load_schema() -> dict:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def valid_item() -> dict:
    return {
        "schema_version": "diagnostic_sba_item_v1",
        "identity": {
            "item_id": "diag_sba_schema_fixture_001",
            "item_version": "1.0.0",
            "created_by": "phase_4a2_schema_test",
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
            "question_type": "diagnostic_single_best_answer",
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
                "misconception_id": "MC_SCHEMA_EXAMPLE",
                "misconception_description": "Example misconception placeholder.",
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
            "support_rationale": (
                "The cited source supports the cause-effect relation and the "
                "diagnostic contrast among options."
            ),
        },
        "feedback": {
            "correct_rationale": "The correct answer follows the cited source support.",
            "why_other_options_are_wrong": {
                "A": "This is the correct answer.",
                "B": "This reverses the expected acidity relationship.",
                "C": "This notices climate but misses the acidity mechanism.",
                "D": "This confuses vineyard conditions with cellar conditions.",
            },
            "remediation_recommendation": (
                "Review the linked source and retry a related training item."
            ),
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


class DiagnosticSbaSchemaTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = load_schema()
        Draft202012Validator.check_schema(cls.schema)
        cls.validator = Draft202012Validator(cls.schema)

    def assertValid(self, item: dict) -> None:
        errors = sorted(self.validator.iter_errors(item), key=lambda err: list(err.path))
        self.assertEqual(errors, [], [error.message for error in errors])

    def assertInvalid(self, item: dict) -> None:
        errors = sorted(self.validator.iter_errors(item), key=lambda err: list(err.path))
        self.assertGreater(len(errors), 0, "Expected schema validation errors.")


class TestDiagnosticSbaSchema(DiagnosticSbaSchemaTestCase):
    def test_valid_item(self) -> None:
        self.assertValid(valid_item())

    def test_missing_required_top_level_field(self) -> None:
        item = valid_item()
        del item["curriculum"]
        self.assertInvalid(item)

    def test_five_options_rejected(self) -> None:
        item = valid_item()
        item["options"]["E"] = {
            "option_id": "D",
            "option_text": "Extra option must not be allowed.",
            "is_correct": False,
            "diagnostic_role": "keyword_trap",
        }
        self.assertInvalid(item)

    def test_three_options_rejected(self) -> None:
        item = valid_item()
        del item["options"]["D"]
        self.assertInvalid(item)

    def test_multiple_correct_answers_rejected(self) -> None:
        item = valid_item()
        item["options"]["B"]["is_correct"] = True
        self.assertInvalid(item)

    def test_no_correct_answers_rejected(self) -> None:
        item = valid_item()
        for option in item["options"].values():
            option["is_correct"] = False
        self.assertInvalid(item)

    def test_missing_source_support_rejected(self) -> None:
        item = valid_item()
        del item["source_support"]
        self.assertInvalid(item)

    def test_empty_source_ids_rejected(self) -> None:
        item = valid_item()
        item["source_support"]["source_ids"] = []
        self.assertInvalid(item)

    def test_unsafe_safe_for_examiner_rejected(self) -> None:
        item = valid_item()
        item["governance"]["safe_for_examiner"] = True
        self.assertInvalid(item)

    def test_unsafe_examiner_scoring_allowed_rejected(self) -> None:
        item = valid_item()
        item["governance"]["examiner_scoring_allowed"] = True
        self.assertInvalid(item)

    def test_official_wset_question_rejected(self) -> None:
        item = valid_item()
        item["governance"]["official_wset_question"] = True
        self.assertInvalid(item)

    def test_training_item_only_false_rejected(self) -> None:
        item = valid_item()
        item["governance"]["training_item_only"] = False
        self.assertInvalid(item)


if __name__ == "__main__":
    unittest.main()
