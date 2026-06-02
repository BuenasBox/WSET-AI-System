from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from tools.question_generation.static_demo_exporter import (
    SAFE_ITEM_GOVERNANCE,
    build_static_demo_export_payload,
    validate_static_demo_export_payload,
)


DRAFTS_PATH = Path("knowledge/question-bank/diagnostic_sba/drafts/first_5_enrichment_drafts.json")
REVIEWS_PATH = Path("knowledge/question-bank/diagnostic_sba/reviews/first_5_human_review_records.json")
REPORT_PATH = Path("docs/STATIC_DEMO_EXPORT_DRY_RUN_REPORT.md")
FRONTEND_INDEX_PATH = Path("frontend/diagnostic-sba/index.html")
FRONTEND_PREGUNTAS_PATH = Path("frontend/diagnostic-sba/preguntas.json")


def load_drafts() -> list[dict]:
    with DRAFTS_PATH.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, list):
        raise AssertionError("drafts fixture must be a list")
    return data


def load_reviews() -> list[dict]:
    with REVIEWS_PATH.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, list):
        raise AssertionError("reviews fixture must be a list")
    return data


class StaticDemoExportDryRunTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.drafts = load_drafts()
        cls.reviews = load_reviews()
        cls.payload = build_static_demo_export_payload(cls.drafts, cls.reviews)

    def test_dry_run_report_exists(self) -> None:
        self.assertTrue(REPORT_PATH.exists())

    def test_dry_run_loads_drafts_and_reviews(self) -> None:
        self.assertEqual(len(self.drafts), 5)
        self.assertEqual(len(self.reviews), 5)

    def test_dry_run_builds_payload_with_exactly_three_items(self) -> None:
        self.assertEqual(len(self.payload["items"]), 3)

    def test_eligible_ids_are_2_12_17(self) -> None:
        self.assertEqual([item["source_question_id"] for item in self.payload["items"]], ["2", "12", "17"])

    def test_excluded_ids_are_absent(self) -> None:
        selected_ids = {item["source_question_id"] for item in self.payload["items"]}

        self.assertNotIn("1", selected_ids)
        self.assertNotIn("13", selected_ids)

    def test_payload_validates(self) -> None:
        self.assertEqual(validate_static_demo_export_payload(self.payload), [])

    def test_pre_submit_payload_has_no_correct_answer_field(self) -> None:
        render_text = self._render_text()

        self.assertNotIn("correct_option_id", render_text)
        self.assertNotIn("correct_answer", render_text)

    def test_pre_submit_payload_has_no_is_correct(self) -> None:
        self.assertNotIn("is_correct", self._render_text())

    def test_pre_submit_payload_has_no_diagnostic_role(self) -> None:
        self.assertNotIn("diagnostic_role", self._render_text())

    def test_pre_submit_payload_has_no_rationales(self) -> None:
        render_text = self._render_text()

        self.assertNotIn("rationale", render_text)
        self.assertNotIn("feedback", render_text)
        self.assertNotIn("why_other_options_are_wrong", render_text)

    def test_pre_submit_payload_has_no_remediation(self) -> None:
        self.assertNotIn("remediation", self._render_text())

    def test_outcomes_are_separated(self) -> None:
        render_text = self._render_text()
        outcome_text = json.dumps(self.payload["outcomes_by_item_id"], ensure_ascii=False)

        self.assertNotIn("correct_option_id", render_text)
        self.assertIn("correct_option_id", outcome_text)
        self.assertIn("option_diagnostics", outcome_text)

    def test_governance_flags_safe(self) -> None:
        for item in self.payload["items"]:
            self.assertEqual(item["governance"], SAFE_ITEM_GOVERNANCE)
            self.assertTrue(item["training_item_only"])
            self.assertTrue(item["static_demo_only"])
            self.assertFalse(item["official_wset_question"])
            self.assertFalse(item["safe_for_examiner"])
            self.assertFalse(item["examiner_scoring_allowed"])

    def test_deterministic_ordering(self) -> None:
        reversed_payload = build_static_demo_export_payload(list(reversed(self.drafts)), list(reversed(self.reviews)))

        self.assertEqual(self.payload, reversed_payload)
        self.assertEqual(self.payload["export_metadata"]["source_question_ids"], ["2", "12", "17"])

    def test_no_frontend_preguntas_json_exists(self) -> None:
        self.assertFalse(FRONTEND_PREGUNTAS_PATH.exists())

    def test_no_frontend_files_modified(self) -> None:
        before = FRONTEND_INDEX_PATH.read_text(encoding="utf-8")

        build_static_demo_export_payload(self.drafts, self.reviews)

        self.assertEqual(FRONTEND_INDEX_PATH.read_text(encoding="utf-8"), before)

    def test_no_draft_or_review_files_mutated(self) -> None:
        drafts_before = copy.deepcopy(self.drafts)
        reviews_before = copy.deepcopy(self.reviews)

        build_static_demo_export_payload(self.drafts, self.reviews)

        self.assertEqual(self.drafts, drafts_before)
        self.assertEqual(self.reviews, reviews_before)
        self.assertEqual(load_drafts(), drafts_before)
        self.assertEqual(load_reviews(), reviews_before)

    def _render_text(self) -> str:
        return json.dumps(self.payload["items"], ensure_ascii=False)


if __name__ == "__main__":
    unittest.main()
