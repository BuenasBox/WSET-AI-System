from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

from tools.question_generation.export_static_demo_questions import build_payload
from tools.question_generation.open_response_pipeline import (
    REVIEW_APPROVED,
    REVIEW_REJECTED,
    build_grounded_open_response_candidates,
    build_open_response_review_records,
    validate_open_response_candidate,
)
from tools.question_generation.static_demo_exporter import validate_static_demo_export_payload


REPO_ROOT = Path(__file__).parents[1]
QUESTION_BANK_PATH = REPO_ROOT / "knowledge" / "question-bank" / "structured" / "wset3_questions.json"
NORMALIZED_PATH = (
    REPO_ROOT
    / "knowledge"
    / "question-bank"
    / "open_response"
    / "normalized"
    / "diagnostic_open_response_candidates.json"
)
REVIEW_RECORDS_PATH = (
    REPO_ROOT
    / "knowledge"
    / "question-bank"
    / "open_response"
    / "reviews"
    / "open_response_review_records.json"
)
SCHEMA_PATH = REPO_ROOT / "knowledge" / "enrichment" / "diagnostic_open_response.schema.json"


def load_source_records() -> list[dict]:
    return json.loads(QUESTION_BANK_PATH.read_text(encoding="utf-8"))


def load_candidates() -> list[dict]:
    return json.loads(NORMALIZED_PATH.read_text(encoding="utf-8"))


class OpenResponseGroundingReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.source_records = load_source_records()
        cls.candidates = load_candidates()
        cls.reviews = json.loads(REVIEW_RECORDS_PATH.read_text(encoding="utf-8"))
        cls.by_id = {candidate["source_question_id"]: candidate for candidate in cls.candidates}
        cls.review_by_id = {record["source_question_id"]: record for record in cls.reviews}

    def test_normalized_artifacts_have_twenty_one_records(self) -> None:
        self.assertEqual(len(self.candidates), 21)
        self.assertEqual(len(self.reviews), 21)

    def test_id_18_is_blocked_by_structural_anomaly(self) -> None:
        candidate = self.by_id["18"]
        review = self.review_by_id["18"]
        self.assertEqual(candidate["review_status"], REVIEW_REJECTED)
        self.assertEqual(review["review_status"], REVIEW_REJECTED)
        self.assertEqual(candidate["activation_status"], "inactive")
        self.assertIn("missing RA metadata", review["issues_found"])
        self.assertIn(
            "structural anomaly: source carries populated SBA answer/options residue",
            review["issues_found"],
        )

    def test_approved_candidates_require_ra(self) -> None:
        candidate = copy.deepcopy(self.by_id["798"])
        candidate["RA"] = "unknown"
        candidate["review_status"] = REVIEW_APPROVED
        errors = validate_open_response_candidate(candidate)
        self.assertIn("approved candidates require RA", errors)

    def test_approved_candidates_require_corpus_support(self) -> None:
        candidate = copy.deepcopy(self.by_id["798"])
        candidate["corpus_support"]["status"] = "missing"
        candidate["corpus_support"]["evidence_chunks"] = []
        candidate["review_status"] = REVIEW_APPROVED
        errors = validate_open_response_candidate(candidate)
        self.assertIn("approved candidates require corpus support", errors)

    def test_approved_candidates_do_not_allow_sba_residue(self) -> None:
        candidate = copy.deepcopy(self.by_id["798"])
        candidate["options"] = {"A": "", "B": "", "C": "", "D": ""}
        candidate["review_status"] = REVIEW_APPROVED
        errors = validate_open_response_candidate(candidate)
        self.assertIn("approved candidates must not contain SBA residue", errors)

    def test_normalized_candidates_remove_source_sba_residue(self) -> None:
        forbidden_fields = {
            "options",
            "option_a",
            "option_b",
            "option_c",
            "option_d",
            "correct_answer",
            "correct_answer_letter",
            "correct_answer_text",
            "distractors",
        }
        for candidate in self.candidates:
            self.assertTrue(forbidden_fields.isdisjoint(candidate), candidate["source_question_id"])

    def test_no_official_scoring_fields_allowed(self) -> None:
        candidate = copy.deepcopy(self.by_id["798"])
        candidate["official_marks"] = 2
        errors = validate_open_response_candidate(candidate)
        self.assertTrue(any("forbidden field" in error for error in errors), errors)

    def test_approved_candidates_have_chunk_grounding(self) -> None:
        approved = [candidate for candidate in self.candidates if candidate["review_status"] == REVIEW_APPROVED]
        self.assertEqual(len(approved), 20)
        for candidate in approved:
            support = candidate["corpus_support"]
            self.assertEqual(support["status"], "supported", candidate["source_question_id"])
            self.assertGreaterEqual(len(support["evidence_chunks"]), 1, candidate["source_question_id"])
            for chunk in support["evidence_chunks"]:
                self.assertGreaterEqual(len(chunk["matched_terms"]), 3, candidate["source_question_id"])
                self.assertNotEqual(chunk["title"], "Index")

    def test_grounded_output_is_deterministic_against_artifact(self) -> None:
        generated = build_grounded_open_response_candidates(copy.deepcopy(self.source_records))
        self.assertEqual(generated, self.candidates)
        reviews = build_open_response_review_records(self.source_records, generated)
        self.assertEqual(reviews, self.reviews)

    def test_candidates_match_open_response_schema(self) -> None:
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        validator = Draft202012Validator(schema)
        for candidate in self.candidates:
            errors = sorted(validator.iter_errors(candidate), key=lambda err: list(err.path))
            self.assertEqual(errors, [], [error.message for error in errors])
            self.assertEqual(validate_open_response_candidate(candidate), [])

    def test_sba_dry_run_payload_stays_at_thirty_six(self) -> None:
        payload = build_payload(REPO_ROOT / "knowledge" / "question-bank" / "diagnostic_sba")
        self.assertEqual(len(payload["items"]), 36)
        self.assertEqual(validate_static_demo_export_payload(payload), [])


if __name__ == "__main__":
    unittest.main()
