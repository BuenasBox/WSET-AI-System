from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from tools.question_generation.human_review_resolution import ReviewStatus
from tools.question_generation.static_demo_exporter import (
    ApprovalScope,
    build_static_demo_export_payload,
    build_static_demo_outcome_payload,
    build_static_demo_render_payload,
    select_static_demo_eligible_items,
    validate_static_demo_export_payload,
)


DRAFTS_PATH = Path("knowledge/question-bank/diagnostic_sba/drafts/first_5_enrichment_drafts.json")
REVIEWS_PATH = Path("knowledge/question-bank/diagnostic_sba/reviews/first_5_human_review_records.json")
FRONTEND_INDEX_PATH = Path("frontend/diagnostic-sba/index.html")
PREGUNTAS_PATH = Path("frontend/diagnostic-sba/preguntas.json")


def load_drafts() -> list[dict]:
    with DRAFTS_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_reviews() -> list[dict]:
    with REVIEWS_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)


class StaticDemoExporterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.drafts = load_drafts()
        cls.reviews = load_reviews()
        cls.drafts_by_source_id = {draft["identity"]["source_question_id"]: draft for draft in cls.drafts}
        cls.reviews_by_source_id = {record["source_question_id"]: record for record in cls.reviews}

    def test_exactly_four_eligible_items_selected_from_first_five(self) -> None:
        # Q1 approved in phase-4a3.7.31; Q13 still requires_revision
        eligible = select_static_demo_eligible_items(self.drafts, self.reviews)

        self.assertEqual(len(eligible), 4)

    def test_selected_ids_are_1_2_12_17(self) -> None:
        # Q1 approved in phase-4a3.7.31
        eligible = select_static_demo_eligible_items(self.drafts, self.reviews)

        self.assertEqual([draft["identity"]["source_question_id"] for draft in eligible], ["1", "2", "12", "17"])

    def test_draft_13_is_excluded_q1_now_included(self) -> None:
        # Q1 approved in phase-4a3.7.31; Q13 still requires_revision
        eligible = select_static_demo_eligible_items(self.drafts, self.reviews)
        selected_ids = {draft["identity"]["source_question_id"] for draft in eligible}

        self.assertNotIn("13", selected_ids)
        self.assertIn("1", selected_ids)

    def test_render_payload_does_not_expose_correct_answer(self) -> None:
        payload = self._render_payload_for("2")
        text = json.dumps(payload, ensure_ascii=False)

        self.assertNotIn("is_correct", text)
        self.assertNotIn("correct_option_id", text)
        self.assertNotIn("correct_rationale", text)

    def test_render_payload_does_not_expose_diagnostic_roles(self) -> None:
        payload = self._render_payload_for("2")
        text = json.dumps(payload, ensure_ascii=False)

        self.assertNotIn("diagnostic_role", text)
        self.assertNotIn("diagnostic_note", text)
        self.assertNotIn("misconception_id", text)

    def test_render_payload_does_not_expose_rationales_or_remediation(self) -> None:
        payload = self._render_payload_for("2")
        text = json.dumps(payload, ensure_ascii=False).lower()

        self.assertNotIn("feedback", text)
        self.assertNotIn("why_other_options_are_wrong", text)
        self.assertNotIn("remediation", text)
        self.assertNotIn("causal_chain", text)

    def test_outcome_payload_is_separated(self) -> None:
        render_payload = self._render_payload_for("2")
        outcome_payload = build_static_demo_outcome_payload(
            self.drafts_by_source_id["2"],
            self.reviews_by_source_id["2"],
        )

        self.assertNotIn("correct_option_id", render_payload)
        self.assertIn("correct_option_id", outcome_payload)
        self.assertIn("option_diagnostics", outcome_payload)

    def test_export_payload_includes_items_and_outcomes_by_item_id(self) -> None:
        payload = build_static_demo_export_payload(self.drafts, self.reviews)

        self.assertIn("items", payload)
        self.assertIn("outcomes_by_item_id", payload)
        self.assertEqual(len(payload["items"]), 4)  # Q1 approved in phase-4a3.7.31
        self.assertEqual(set(payload["outcomes_by_item_id"]), {item["item_id"] for item in payload["items"]})

    def test_export_payload_is_deterministic(self) -> None:
        first = build_static_demo_export_payload(self.drafts, self.reviews)
        second = build_static_demo_export_payload(list(reversed(self.drafts)), list(reversed(self.reviews)))

        self.assertEqual(first, second)

    def test_unsafe_governance_excluded(self) -> None:
        drafts = copy.deepcopy(self.drafts)
        for draft in drafts:
            if draft["identity"]["source_question_id"] == "2":
                draft["governance"]["safe_for_examiner"] = True

        eligible = select_static_demo_eligible_items(drafts, self.reviews)

        self.assertEqual([draft["identity"]["source_question_id"] for draft in eligible], ["1", "12", "17"])  # Q1 also eligible

    def test_forbidden_scopes_excluded(self) -> None:
        reviews = copy.deepcopy(self.reviews)
        for review in reviews:
            if review["source_question_id"] == "2":
                review["approval_scope"] = "production"

        eligible = select_static_demo_eligible_items(self.drafts, reviews)

        self.assertEqual([draft["identity"]["source_question_id"] for draft in eligible], ["1", "12", "17"])  # Q1 also eligible

    def test_missing_review_excluded(self) -> None:
        reviews = [record for record in self.reviews if record["source_question_id"] != "2"]

        eligible = select_static_demo_eligible_items(self.drafts, reviews)

        self.assertEqual([draft["identity"]["source_question_id"] for draft in eligible], ["1", "12", "17"])  # Q1 also eligible

    def test_output_validates(self) -> None:
        payload = build_static_demo_export_payload(self.drafts, self.reviews)

        self.assertEqual(validate_static_demo_export_payload(payload), [])

    def test_build_payload_does_not_modify_preguntas_json(self) -> None:
        before = PREGUNTAS_PATH.read_text(encoding="utf-8") if PREGUNTAS_PATH.exists() else None

        build_static_demo_export_payload(self.drafts, self.reviews)

        after = PREGUNTAS_PATH.read_text(encoding="utf-8") if PREGUNTAS_PATH.exists() else None
        self.assertEqual(after, before)

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

    def test_review_statuses_remain_unchanged(self) -> None:
        statuses = {record["source_question_id"]: record["review_status"] for record in self.reviews}

        # Q1 approved in phase-4a3.7.31
        self.assertEqual(statuses["1"], ReviewStatus.APPROVED_FOR_STATIC_DEMO)
        self.assertEqual(statuses["13"], ReviewStatus.REQUIRES_REVISION)

    def _render_payload_for(self, source_question_id: str) -> dict:
        return build_static_demo_render_payload(
            self.drafts_by_source_id[source_question_id],
            self.reviews_by_source_id[source_question_id],
        )


if __name__ == "__main__":
    unittest.main()
