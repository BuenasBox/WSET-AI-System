from __future__ import annotations

import builtins
import copy
import json
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.question_generation.human_review_resolution import (
    ApprovalScope,
    CHECKLIST_KEYS,
    ReviewStatus,
    SAFE_GOVERNANCE,
    apply_review_status,
    build_review_record,
    can_promote_to_static_demo,
    validate_review_record,
)


DRAFTS_PATH = Path("knowledge/question-bank/diagnostic_sba/drafts/first_5_enrichment_drafts.json")


def all_true_checklist() -> dict:
    return {key: True for key in CHECKLIST_KEYS}


def load_first_draft() -> dict:
    with DRAFTS_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)[0]


def load_all_drafts() -> list[dict]:
    with DRAFTS_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)


class HumanReviewResolutionTests(unittest.TestCase):
    def test_build_valid_review_record(self) -> None:
        record = build_review_record(
            load_first_draft(),
            reviewer="human_reviewer",
            review_status=ReviewStatus.APPROVED_FOR_STATIC_DEMO,
            approval_scope=ApprovalScope.STATIC_DEMO_ONLY,
            checklist=all_true_checklist(),
            notes="Static demo only.",
        )

        self.assertEqual(validate_review_record(record), [])
        self.assertEqual(record["source_question_id"], "1")
        self.assertEqual(record["draft_id"], "draft_diag_sba_structured_1")
        self.assertTrue(record["review_id"].startswith("review_1_draft_diag_sba_structured_1"))

    def test_missing_reviewer_rejected(self) -> None:
        record = build_review_record(
            load_first_draft(),
            reviewer="",
            review_status=ReviewStatus.APPROVED_FOR_STATIC_DEMO,
            approval_scope=ApprovalScope.STATIC_DEMO_ONLY,
            checklist=all_true_checklist(),
        )

        self.assertIn("reviewer must be present", validate_review_record(record))

    def test_invalid_review_status_rejected(self) -> None:
        record = build_review_record(
            load_first_draft(),
            reviewer="human_reviewer",
            review_status="approved_for_production",
            approval_scope=ApprovalScope.STATIC_DEMO_ONLY,
            checklist=all_true_checklist(),
        )

        self.assertIn("review_status must be an allowed value", validate_review_record(record))

    def test_forbidden_approval_scope_rejected(self) -> None:
        record = build_review_record(
            load_first_draft(),
            reviewer="human_reviewer",
            review_status=ReviewStatus.APPROVED_FOR_STATIC_DEMO,
            approval_scope="examiner_scoring",
            checklist=all_true_checklist(),
        )

        errors = validate_review_record(record)
        self.assertIn("approval_scope must be an allowed value", errors)
        self.assertIn("approval_scope is forbidden", errors)

    def test_missing_checklist_rejected(self) -> None:
        record = build_review_record(
            load_first_draft(),
            reviewer="human_reviewer",
            review_status=ReviewStatus.APPROVED_FOR_STATIC_DEMO,
            approval_scope=ApprovalScope.STATIC_DEMO_ONLY,
            checklist=all_true_checklist(),
        )
        record.pop("checklist")

        errors = validate_review_record(record)
        self.assertIn("missing field: checklist", errors)
        self.assertIn("checklist must be present", errors)

    def test_incomplete_checklist_prevents_approval(self) -> None:
        checklist = all_true_checklist()
        checklist["source_support_checked"] = False
        record = build_review_record(
            load_first_draft(),
            reviewer="human_reviewer",
            review_status=ReviewStatus.APPROVED_FOR_STATIC_DEMO,
            approval_scope=ApprovalScope.STATIC_DEMO_ONLY,
            checklist=checklist,
        )

        self.assertIn("approval requires all checklist items true", validate_review_record(record))

    def test_approved_for_static_demo_requires_all_checklist_true(self) -> None:
        record = build_review_record(
            load_first_draft(),
            reviewer="human_reviewer",
            review_status=ReviewStatus.APPROVED_FOR_STATIC_DEMO,
            approval_scope=ApprovalScope.STATIC_DEMO_ONLY,
            checklist=all_true_checklist(),
        )

        self.assertEqual(validate_review_record(record), [])

    def test_governance_confirmation_required(self) -> None:
        record = build_review_record(
            load_first_draft(),
            reviewer="human_reviewer",
            review_status=ReviewStatus.APPROVED_FOR_STATIC_DEMO,
            approval_scope=ApprovalScope.STATIC_DEMO_ONLY,
            checklist=all_true_checklist(),
        )
        record.pop("governance_confirmation")

        errors = validate_review_record(record)
        self.assertIn("missing field: governance_confirmation", errors)
        self.assertIn("governance_confirmation must be present", errors)

    def test_can_promote_to_static_demo_true_only_for_valid_approved_record(self) -> None:
        draft = load_first_draft()
        record = build_review_record(
            draft,
            reviewer="human_reviewer",
            review_status=ReviewStatus.APPROVED_FOR_STATIC_DEMO,
            approval_scope=ApprovalScope.STATIC_DEMO_ONLY,
            checklist=all_true_checklist(),
        )

        self.assertTrue(can_promote_to_static_demo(draft, record))

    def test_can_promote_to_static_demo_false_for_rejected_or_required_revision(self) -> None:
        draft = load_first_draft()
        rejected = build_review_record(
            draft,
            reviewer="human_reviewer",
            review_status=ReviewStatus.REJECTED,
            approval_scope=ApprovalScope.INTERNAL_REVIEW_ONLY,
            checklist=all_true_checklist(),
        )
        revision = build_review_record(
            draft,
            reviewer="human_reviewer",
            review_status=ReviewStatus.REQUIRES_REVISION,
            approval_scope=ApprovalScope.INTERNAL_REVIEW_ONLY,
            checklist=all_true_checklist(),
        )

        self.assertFalse(can_promote_to_static_demo(draft, rejected))
        self.assertFalse(can_promote_to_static_demo(draft, revision))

    def test_apply_review_status_returns_copy(self) -> None:
        draft = load_first_draft()
        record = build_review_record(
            draft,
            reviewer="human_reviewer",
            review_status=ReviewStatus.APPROVED_FOR_STATIC_DEMO,
            approval_scope=ApprovalScope.STATIC_DEMO_ONLY,
            checklist=all_true_checklist(),
        )

        reviewed = apply_review_status(draft, record)

        self.assertIsNot(reviewed, draft)
        self.assertIn("review_resolution", reviewed)

    def test_apply_review_status_does_not_mutate_draft(self) -> None:
        draft = load_first_draft()
        before = copy.deepcopy(draft)
        record = build_review_record(
            draft,
            reviewer="human_reviewer",
            review_status=ReviewStatus.APPROVED_FOR_STATIC_DEMO,
            approval_scope=ApprovalScope.STATIC_DEMO_ONLY,
            checklist=all_true_checklist(),
        )

        apply_review_status(draft, record)

        self.assertEqual(draft, before)

    def test_apply_review_status_preserves_safe_governance_flags(self) -> None:
        draft = load_first_draft()
        record = build_review_record(
            draft,
            reviewer="human_reviewer",
            review_status=ReviewStatus.APPROVED_FOR_STATIC_DEMO,
            approval_scope=ApprovalScope.STATIC_DEMO_ONLY,
            checklist=all_true_checklist(),
        )

        reviewed = apply_review_status(draft, record)

        self.assertEqual(reviewed["governance"], SAFE_GOVERNANCE)
        self.assertFalse(reviewed["review_resolution"]["production_approved"])
        self.assertFalse(reviewed["review_resolution"]["frontend_export_created"])

    def test_production_scope_rejected(self) -> None:
        self._assert_scope_rejected("production")

    def test_official_exam_examiner_scoring_certification_readiness_scopes_rejected(self) -> None:
        for scope in ("official_exam", "examiner_scoring", "certification_readiness"):
            self._assert_scope_rejected(scope)

    def test_no_file_writes(self) -> None:
        draft = load_first_draft()
        record = build_review_record(
            draft,
            reviewer="human_reviewer",
            review_status=ReviewStatus.APPROVED_FOR_STATIC_DEMO,
            approval_scope=ApprovalScope.STATIC_DEMO_ONLY,
            checklist=all_true_checklist(),
        )
        original_open = builtins.open

        def fail_open(*args, **kwargs):
            raise AssertionError("human review resolution helpers must not open files")

        with patch("builtins.open", side_effect=fail_open):
            validate_review_record(record)
            can_promote_to_static_demo(draft, record)
            apply_review_status(draft, record)

        self.assertIs(builtins.open, original_open)

    def test_existing_first_5_drafts_remain_defer_for_human_review(self) -> None:
        drafts = load_all_drafts()

        self.assertEqual(len(drafts), 5)
        for draft in drafts:
            self.assertEqual(draft["enrichment_status"], "defer_for_human_review")
            self.assertTrue(draft["human_review"]["required"])
            self.assertNotIn("review_resolution", draft)

    def _assert_scope_rejected(self, scope: str) -> None:
        record = build_review_record(
            load_first_draft(),
            reviewer="human_reviewer",
            review_status=ReviewStatus.APPROVED_FOR_STATIC_DEMO,
            approval_scope=scope,
            checklist=all_true_checklist(),
        )
        errors = validate_review_record(record)
        self.assertIn("approval_scope must be an allowed value", errors)
        self.assertIn("approval_scope is forbidden", errors)


if __name__ == "__main__":
    unittest.main()
