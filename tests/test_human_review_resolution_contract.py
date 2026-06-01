from __future__ import annotations

import copy
import unittest


REVIEW_STATUSES = {
    "pending_human_review",
    "approved_for_static_demo",
    "approved_for_training_pilot",
    "requires_revision",
    "rejected",
    "preserve_only",
}
APPROVAL_SCOPES = {
    "static_demo_only",
    "local_training_pilot",
    "internal_review_only",
}
FORBIDDEN_SCOPES = {
    "production",
    "official_exam",
    "examiner_scoring",
    "certification_readiness",
}
CHECKLIST_FIELDS = (
    "source_support_checked",
    "correct_answer_checked",
    "distractor_logic_checked",
    "diagnostic_roles_checked",
    "misconception_links_checked",
    "causal_chain_links_checked",
    "sat_relevance_checked",
    "rationale_quality_checked",
    "remediation_quality_checked",
    "wording_safety_checked",
    "governance_flags_checked",
)
SAFE_GOVERNANCE = {
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
STATUS_SCOPE = {
    "pending_human_review": "internal_review_only",
    "approved_for_static_demo": "static_demo_only",
    "approved_for_training_pilot": "local_training_pilot",
    "requires_revision": "internal_review_only",
    "rejected": "internal_review_only",
    "preserve_only": "internal_review_only",
}


def valid_draft_fixture() -> dict:
    return {
        "identity": {
            "item_id": "draft_diag_sba_structured_1",
            "source_question_id": "1",
        },
        "enrichment_status": "defer_for_human_review",
        "human_review": {
            "required": True,
            "risk_level": "medium",
        },
        "governance": copy.deepcopy(SAFE_GOVERNANCE),
    }


def valid_review_record() -> dict:
    return {
        "review_id": "review_1_20260601_001",
        "source_question_id": "1",
        "draft_id": "draft_diag_sba_structured_1",
        "reviewer": "human_reviewer",
        "reviewed_at": "2026-06-01T00:00:00Z",
        "review_status": "approved_for_static_demo",
        "risk_before": "medium",
        "risk_after": "low",
        "checklist": {field: True for field in CHECKLIST_FIELDS},
        "issues_found": [],
        "required_changes": [],
        "approval_scope": "static_demo_only",
        "governance_confirmation": copy.deepcopy(SAFE_GOVERNANCE),
        "notes": "Approved only for static demo in a future export phase.",
    }


def validate_review_record_contract(record: dict) -> list[str]:
    errors: list[str] = []

    required = (
        "review_id",
        "source_question_id",
        "draft_id",
        "reviewer",
        "reviewed_at",
        "review_status",
        "risk_before",
        "risk_after",
        "checklist",
        "issues_found",
        "required_changes",
        "approval_scope",
        "governance_confirmation",
        "notes",
    )
    for field in required:
        if field not in record:
            errors.append(f"missing field: {field}")

    if not isinstance(record.get("reviewer"), str) or not record.get("reviewer", "").strip():
        errors.append("reviewer must be present")

    status = record.get("review_status")
    if status not in REVIEW_STATUSES:
        errors.append("review_status must be an allowed value")

    scope = record.get("approval_scope")
    if scope not in APPROVAL_SCOPES:
        errors.append("approval_scope must be an allowed value")
    if scope in FORBIDDEN_SCOPES:
        errors.append("approval_scope is forbidden")

    if status in STATUS_SCOPE and scope in APPROVAL_SCOPES and STATUS_SCOPE[status] != scope:
        errors.append("review_status and approval_scope are incompatible")

    checklist = record.get("checklist")
    if not isinstance(checklist, dict):
        errors.append("checklist must be present")
    else:
        for field in CHECKLIST_FIELDS:
            if field not in checklist:
                errors.append(f"checklist missing field: {field}")
            elif checklist[field] is not True and checklist[field] is not False:
                errors.append(f"checklist.{field} must be boolean")

    if status in {"approved_for_static_demo", "approved_for_training_pilot"}:
        if not isinstance(checklist, dict) or any(checklist.get(field) is not True for field in CHECKLIST_FIELDS):
            errors.append("approval requires all checklist items true")

    governance = record.get("governance_confirmation")
    if not isinstance(governance, dict):
        errors.append("governance_confirmation must be present")
    else:
        for field, expected in SAFE_GOVERNANCE.items():
            if governance.get(field) is not expected:
                errors.append(f"governance_confirmation.{field} must remain {str(expected).lower()}")

    return errors


def apply_review_record_contract(draft: dict, review_record: dict) -> dict:
    validate_review_record_contract(review_record)
    return {
        "source_question_id": draft["identity"]["source_question_id"],
        "draft_id": draft["identity"]["item_id"],
        "review_record": copy.deepcopy(review_record),
        "governance": copy.deepcopy(SAFE_GOVERNANCE),
        "training_item_only": True,
    }


class HumanReviewResolutionContractTests(unittest.TestCase):
    def test_valid_review_record_schema_accepted(self) -> None:
        self.assertEqual(validate_review_record_contract(valid_review_record()), [])

    def test_missing_reviewer_fails(self) -> None:
        record = valid_review_record()
        record["reviewer"] = ""

        self.assertIn("reviewer must be present", validate_review_record_contract(record))

    def test_missing_checklist_fails(self) -> None:
        record = valid_review_record()
        record.pop("checklist")

        self.assertIn("missing field: checklist", validate_review_record_contract(record))
        self.assertIn("checklist must be present", validate_review_record_contract(record))

    def test_official_examiner_scope_rejected(self) -> None:
        record = valid_review_record()
        record["approval_scope"] = "examiner_scoring"

        errors = validate_review_record_contract(record)
        self.assertIn("approval_scope must be an allowed value", errors)
        self.assertIn("approval_scope is forbidden", errors)

    def test_production_scope_rejected(self) -> None:
        record = valid_review_record()
        record["approval_scope"] = "production"

        errors = validate_review_record_contract(record)
        self.assertIn("approval_scope must be an allowed value", errors)
        self.assertIn("approval_scope is forbidden", errors)

    def test_approved_for_static_demo_requires_all_checklist_items_true(self) -> None:
        record = valid_review_record()
        record["checklist"]["source_support_checked"] = False

        self.assertIn("approval requires all checklist items true", validate_review_record_contract(record))

    def test_rejected_review_may_have_failed_checklist(self) -> None:
        record = valid_review_record()
        record["review_status"] = "rejected"
        record["approval_scope"] = "internal_review_only"
        record["checklist"]["source_support_checked"] = False
        record["issues_found"] = ["Source support weak."]

        self.assertEqual(validate_review_record_contract(record), [])

    def test_governance_confirmation_required(self) -> None:
        record = valid_review_record()
        record.pop("governance_confirmation")

        self.assertIn("missing field: governance_confirmation", validate_review_record_contract(record))
        self.assertIn("governance_confirmation must be present", validate_review_record_contract(record))

    def test_approval_does_not_mutate_draft(self) -> None:
        draft = valid_draft_fixture()
        before = copy.deepcopy(draft)

        apply_review_record_contract(draft, valid_review_record())

        self.assertEqual(draft, before)

    def test_approval_remains_training_only(self) -> None:
        result = apply_review_record_contract(valid_draft_fixture(), valid_review_record())

        self.assertTrue(result["training_item_only"])
        self.assertEqual(result["governance"], SAFE_GOVERNANCE)

    def test_review_status_enum_enforced(self) -> None:
        record = valid_review_record()
        record["review_status"] = "approved_for_production"

        self.assertIn("review_status must be an allowed value", validate_review_record_contract(record))

    def test_approval_scope_enum_enforced(self) -> None:
        record = valid_review_record()
        record["approval_scope"] = "frontend_runtime"

        self.assertIn("approval_scope must be an allowed value", validate_review_record_contract(record))


if __name__ == "__main__":
    unittest.main()
