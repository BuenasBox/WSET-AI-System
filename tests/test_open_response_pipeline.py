from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

from tools.question_generation.open_response_pipeline import (
    GOVERNANCE_FLAGS,
    build_open_response_candidate,
    build_open_response_candidates,
    evaluate_open_response_answer,
    find_open_response_records,
    is_open_response_record,
    validate_open_response_candidate,
)


REPO_ROOT = Path(__file__).parents[1]
SCHEMA_PATH = REPO_ROOT / "knowledge" / "enrichment" / "diagnostic_open_response.schema.json"
QUESTION_BANK_PATH = REPO_ROOT / "knowledge" / "question-bank" / "structured" / "wset3_questions.json"


def source_record() -> dict:
    return {
        "question_id": "OR001",
        "question_text": "Explica cómo la altitud puede influir en el estilo de un vino tinto.",
        "question_type": "short_answer",
        "expected_topics": ["RA1", "altitud", "clima", "maduración"],
        "expected_causal_links": ["altitud -> temperatura -> maduración"],
        "expected_keywords": ["altitud", "temperatura", "maduración", "acidez"],
        "difficulty": "intermediate",
        "source_type": "contract_fixture",
        "safe_for_examiner": False,
    }


class OpenResponseSchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(cls.schema)
        cls.validator = Draft202012Validator(cls.schema)

    def assertValid(self, item: dict) -> None:
        errors = sorted(self.validator.iter_errors(item), key=lambda err: list(err.path))
        self.assertEqual(errors, [], [error.message for error in errors])

    def assertInvalid(self, item: dict) -> None:
        errors = sorted(self.validator.iter_errors(item), key=lambda err: list(err.path))
        self.assertGreater(len(errors), 0)

    def test_adapter_candidate_matches_schema(self) -> None:
        self.assertValid(build_open_response_candidate(source_record()))

    def test_question_type_is_canonical_open_response_value(self) -> None:
        item = build_open_response_candidate(source_record())
        item["question_type"] = "short_answer"
        self.assertInvalid(item)

    def test_governance_flags_reject_unsafe_truthy_values(self) -> None:
        item = build_open_response_candidate(source_record())
        item["governance_flags"]["safe_for_examiner"] = True
        self.assertInvalid(item)

    def test_contract_uses_formative_language_fields(self) -> None:
        item = build_open_response_candidate(source_record())
        text = json.dumps(item, ensure_ascii=False).lower()
        self.assertIn("concept_coverage", text)
        self.assertIn("formative_feedback", text)
        self.assertIn("needs_review", text)


class OpenResponseAdapterTests(unittest.TestCase):
    def test_open_response_type_detection_accepts_known_equivalents(self) -> None:
        for value in ("short_answer", "open_response", "Abierta", "respuesta abierta"):
            record = source_record()
            record["question_type"] = value
            self.assertTrue(is_open_response_record(record))

    def test_non_open_response_type_is_ignored(self) -> None:
        record = source_record()
        record["question_type"] = "theory"
        self.assertFalse(is_open_response_record(record))

    def test_find_open_response_records_preserves_source_order(self) -> None:
        records = [source_record(), {**source_record(), "question_id": "OR002"}, {"question_type": "theory"}]
        self.assertEqual([record["question_id"] for record in find_open_response_records(records)], ["OR001", "OR002"])

    def test_adapter_maps_required_contract_fields(self) -> None:
        candidate = build_open_response_candidate(source_record())
        self.assertEqual(candidate["source_question_id"], "OR001")
        self.assertEqual(candidate["question_type"], "diagnostic_open_response")
        self.assertEqual(candidate["RA"], "RA1")
        self.assertEqual(candidate["topic"], "altitud")
        self.assertEqual(candidate["subtopic"], "clima")
        self.assertEqual(candidate["optional_causal_chain"], "altitud -> temperatura -> maduración")
        self.assertIn("acidez", candidate["expected_concepts"])

    def test_adapter_uses_unknown_for_missing_ra_without_inventing_authority(self) -> None:
        record = source_record()
        record["expected_topics"] = ["sulfitos", "SO2"]
        candidate = build_open_response_candidate(record)
        self.assertEqual(candidate["RA"], "unknown")
        self.assertEqual(validate_open_response_candidate(candidate), [])

    def test_adapter_does_not_mutate_input(self) -> None:
        record = source_record()
        before = copy.deepcopy(record)
        build_open_response_candidate(record)
        self.assertEqual(record, before)

    def test_adapter_output_is_deterministic(self) -> None:
        first = build_open_response_candidate(source_record())
        second = build_open_response_candidate(copy.deepcopy(source_record()))
        self.assertEqual(first, second)

    def test_validator_rejects_forbidden_training_authority_fields(self) -> None:
        candidate = build_open_response_candidate(source_record())
        candidate["official_score"] = "not allowed"
        errors = validate_open_response_candidate(candidate)
        self.assertTrue(any("forbidden field" in error for error in errors), errors)

    def test_governance_matches_project_safe_defaults(self) -> None:
        candidate = build_open_response_candidate(source_record())
        self.assertEqual(candidate["governance_flags"], GOVERNANCE_FLAGS)
        self.assertFalse(candidate["governance_flags"]["safe_for_examiner"])
        self.assertFalse(candidate["governance_flags"]["examiner_scoring_allowed"])
        self.assertFalse(candidate["governance_flags"]["uses_llm"])
        self.assertFalse(candidate["governance_flags"]["uses_api"])

    def test_real_question_bank_has_twenty_six_open_response_candidates(self) -> None:
        records = json.loads(QUESTION_BANK_PATH.read_text(encoding="utf-8"))
        candidates = build_open_response_candidates(records)
        self.assertEqual(len(candidates), 26)
        self.assertEqual([candidate["source_question_id"] for candidate in candidates[:2]], ["18", "798"])
        for candidate in candidates:
            self.assertEqual(validate_open_response_candidate(candidate), [])


class OpenResponseEvaluatorTests(unittest.TestCase):
    def test_evaluator_detects_present_and_missing_concepts(self) -> None:
        candidate = build_open_response_candidate(source_record())
        result = evaluate_open_response_answer(candidate, "La altitud baja la temperatura y conserva acidez.")
        self.assertIn("altitud", result["present_concepts"])
        self.assertIn("temperatura", result["present_concepts"])
        self.assertIn("maduración", result["missing_concepts"])
        self.assertEqual(result["feedback_level"], "needs_review")

    def test_evaluator_detects_partial_concepts(self) -> None:
        record = source_record()
        record["expected_keywords"] = ["fermentación maloláctica"]
        candidate = build_open_response_candidate(record)
        result = evaluate_open_response_answer(candidate, "La fermentación cambia la textura.")
        self.assertIn("fermentación maloláctica", result["partial_concepts"])

    def test_evaluator_detects_causal_link_presence(self) -> None:
        candidate = build_open_response_candidate(source_record())
        result = evaluate_open_response_answer(
            candidate,
            "La altitud reduce la temperatura porque ralentiza la maduración.",
        )
        self.assertEqual(result["causal_link_feedback"], "causal_link_present")

    def test_evaluator_detects_weak_causal_link(self) -> None:
        candidate = build_open_response_candidate(source_record())
        result = evaluate_open_response_answer(candidate, "Altitud, temperatura y maduración.")
        self.assertEqual(result["causal_link_feedback"], "weak_causal_link")

    def test_evaluator_handles_no_causal_chain(self) -> None:
        record = source_record()
        record["expected_causal_links"] = []
        candidate = build_open_response_candidate(record)
        result = evaluate_open_response_answer(candidate, "La altitud puede conservar acidez.")
        self.assertEqual(result["causal_link_feedback"], "not_applicable")

    def test_evaluator_reports_unsupported_absolute_claim_terms(self) -> None:
        candidate = build_open_response_candidate(source_record())
        result = evaluate_open_response_answer(candidate, "La altitud siempre garantiza calidad.")
        self.assertIn("siempre", result["unsupported_claims"])
        self.assertIn("garantiza", result["unsupported_claims"])

    def test_evaluator_output_has_no_official_result_fields(self) -> None:
        candidate = build_open_response_candidate(source_record())
        result = evaluate_open_response_answer(candidate, "La altitud afecta la temperatura.")
        forbidden = ("score", "mark", "grade", "pass", "fail", "examiner_score")
        for key in result:
            lowered = key.lower()
            self.assertFalse(any(term in lowered for term in forbidden), key)

    def test_evaluator_output_is_deterministic(self) -> None:
        candidate = build_open_response_candidate(source_record())
        answer = "La altitud reduce la temperatura porque ralentiza la maduración."
        first = evaluate_open_response_answer(candidate, answer)
        second = evaluate_open_response_answer(copy.deepcopy(candidate), answer)
        self.assertEqual(first, second)

    def test_evaluator_does_not_mutate_candidate(self) -> None:
        candidate = build_open_response_candidate(source_record())
        before = copy.deepcopy(candidate)
        evaluate_open_response_answer(candidate, "La altitud afecta la temperatura.")
        self.assertEqual(candidate, before)


if __name__ == "__main__":
    unittest.main()
