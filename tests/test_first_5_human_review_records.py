from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from tools.question_generation.human_review_resolution import (
    APPROVAL_SCOPES,
    FORBIDDEN_SCOPES,
    REQUIRED_REVIEW_FIELDS,
    ReviewStatus,
    SAFE_GOVERNANCE,
    can_promote_to_static_demo,
    validate_review_record,
)


DRAFTS_PATH = Path("knowledge/question-bank/diagnostic_sba/drafts/first_5_enrichment_drafts.json")
REVIEWS_PATH = Path("knowledge/question-bank/diagnostic_sba/reviews/first_5_human_review_records.json")
EXPECTED_SOURCE_IDS = ["1", "2", "12", "13", "17"]
FORBIDDEN_OUTPUT_PATHS = (
    Path("knowledge/question-bank/diagnostic_sba/preguntas.json"),
    Path("knowledge/question-bank/diagnostic_sba/converted"),
    Path("knowledge/question-bank/diagnostic_sba/pilot_bank.json"),
    Path("frontend/diagnostic-sba/preguntas.json"),
)
FORBIDDEN_AUTHORITY_PHRASES = (
    "official score",
    "pass/fail",
    "certification readiness",
    "examiner authority",
)


def load_drafts() -> list[dict]:
    with DRAFTS_PATH.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, list):
        raise AssertionError("first 5 enrichment drafts must be a list")
    return data


def load_reviews() -> list[dict]:
    with REVIEWS_PATH.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, list):
        raise AssertionError("first 5 human review records must be a list")
    return data


class FirstFiveHumanReviewRecordsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.drafts = load_drafts()
        cls.reviews = load_reviews()
        cls.drafts_by_source_id = {draft["identity"]["source_question_id"]: draft for draft in cls.drafts}

    def test_review_file_exists(self) -> None:
        self.assertTrue(REVIEWS_PATH.exists())

    def test_exactly_five_review_records(self) -> None:
        self.assertEqual(len(self.reviews), 5)

    def test_draft_ids_are_expected(self) -> None:
        ids = [record["source_question_id"] for record in self.reviews]

        self.assertEqual(ids, EXPECTED_SOURCE_IDS)

    def test_every_review_has_required_fields(self) -> None:
        for record in self.reviews:
            for field in REQUIRED_REVIEW_FIELDS:
                self.assertIn(field, record)

    def test_every_review_validates(self) -> None:
        for record in self.reviews:
            self.assertEqual(validate_review_record(record), [], record["review_id"])

    def test_every_approval_scope_is_allowed(self) -> None:
        for record in self.reviews:
            self.assertIn(record["approval_scope"], APPROVAL_SCOPES)

    def test_no_forbidden_scope_appears(self) -> None:
        for record in self.reviews:
            self.assertNotIn(record["approval_scope"], FORBIDDEN_SCOPES)

    def test_no_production_approval_appears(self) -> None:
        text = json.dumps(self.reviews, ensure_ascii=False).lower()

        self.assertNotIn("production", text)
        for record in self.reviews:
            self.assertNotEqual(record["review_status"], "approved_for_production")

    def test_governance_confirmation_is_present(self) -> None:
        for record in self.reviews:
            self.assertEqual(record["governance_confirmation"], SAFE_GOVERNANCE)

    def test_no_official_scoring_or_certification_authority(self) -> None:
        text = json.dumps(self.reviews, ensure_ascii=False).lower()

        for phrase in FORBIDDEN_AUTHORITY_PHRASES:
            self.assertNotIn(phrase, text)

    def test_approved_for_static_demo_records_can_promote_to_static_demo(self) -> None:
        approved = [record for record in self.reviews if record["review_status"] == ReviewStatus.APPROVED_FOR_STATIC_DEMO]
        self.assertGreater(len(approved), 0)

        for record in approved:
            draft = self.drafts_by_source_id[record["source_question_id"]]
            self.assertTrue(can_promote_to_static_demo(draft, record), record["review_id"])

    def test_non_approved_records_cannot_promote(self) -> None:
        non_approved = [record for record in self.reviews if record["review_status"] != ReviewStatus.APPROVED_FOR_STATIC_DEMO]
        self.assertGreater(len(non_approved), 0)

        for record in non_approved:
            draft = self.drafts_by_source_id[record["source_question_id"]]
            self.assertFalse(can_promote_to_static_demo(draft, record), record["review_id"])

    def test_original_draft_file_remains_unchanged(self) -> None:
        before = copy.deepcopy(self.drafts)
        after = load_drafts()

        self.assertEqual(after, before)
        for draft in after:
            self.assertEqual(draft["enrichment_status"], "defer_for_human_review")
            self.assertIs(draft["human_review"]["required"], True)
            self.assertNotIn("review_resolution", draft)

    def test_no_preguntas_json_exists(self) -> None:
        self.assertFalse(Path("knowledge/question-bank/diagnostic_sba/preguntas.json").exists())

    def test_no_approved_or_exported_frontend_file_exists(self) -> None:
        for path in FORBIDDEN_OUTPUT_PATHS:
            self.assertFalse(path.exists(), str(path))

    def test_review_records_are_additive_only(self) -> None:
        draft_ids = {draft["identity"]["item_id"] for draft in self.drafts}
        review_draft_ids = {record["draft_id"] for record in self.reviews}

        self.assertEqual(review_draft_ids, draft_ids)
        self.assertNotEqual(REVIEWS_PATH, DRAFTS_PATH)


if __name__ == "__main__":
    unittest.main()
