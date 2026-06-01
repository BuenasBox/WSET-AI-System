"""Pure helpers for diagnostic SBA human-review records.

This module creates and validates review records as data structures only. It
does not modify draft files, approve items in place, export frontend data, or
write any outputs.
"""

from __future__ import annotations

import copy
from collections.abc import Mapping
from typing import Any

from tools.question_generation.diagnostic_sba_validator import validate_diagnostic_sba_item


class ReviewStatus:
    PENDING_HUMAN_REVIEW = "pending_human_review"
    APPROVED_FOR_STATIC_DEMO = "approved_for_static_demo"
    APPROVED_FOR_TRAINING_PILOT = "approved_for_training_pilot"
    REQUIRES_REVISION = "requires_revision"
    REJECTED = "rejected"
    PRESERVE_ONLY = "preserve_only"


class ApprovalScope:
    STATIC_DEMO_ONLY = "static_demo_only"
    LOCAL_TRAINING_PILOT = "local_training_pilot"
    INTERNAL_REVIEW_ONLY = "internal_review_only"


REVIEW_STATUSES: frozenset[str] = frozenset(
    (
        ReviewStatus.PENDING_HUMAN_REVIEW,
        ReviewStatus.APPROVED_FOR_STATIC_DEMO,
        ReviewStatus.APPROVED_FOR_TRAINING_PILOT,
        ReviewStatus.REQUIRES_REVISION,
        ReviewStatus.REJECTED,
        ReviewStatus.PRESERVE_ONLY,
    )
)

APPROVAL_SCOPES: frozenset[str] = frozenset(
    (
        ApprovalScope.STATIC_DEMO_ONLY,
        ApprovalScope.LOCAL_TRAINING_PILOT,
        ApprovalScope.INTERNAL_REVIEW_ONLY,
    )
)

FORBIDDEN_SCOPES: frozenset[str] = frozenset(
    (
        "production",
        "official_exam",
        "examiner_scoring",
        "certification_readiness",
    )
)

CHECKLIST_KEYS: tuple[str, ...] = (
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
    "governance_checked",
)

SAFE_GOVERNANCE: dict[str, bool] = {
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

STATUS_SCOPE: dict[str, str] = {
    ReviewStatus.PENDING_HUMAN_REVIEW: ApprovalScope.INTERNAL_REVIEW_ONLY,
    ReviewStatus.APPROVED_FOR_STATIC_DEMO: ApprovalScope.STATIC_DEMO_ONLY,
    ReviewStatus.APPROVED_FOR_TRAINING_PILOT: ApprovalScope.LOCAL_TRAINING_PILOT,
    ReviewStatus.REQUIRES_REVISION: ApprovalScope.INTERNAL_REVIEW_ONLY,
    ReviewStatus.REJECTED: ApprovalScope.INTERNAL_REVIEW_ONLY,
    ReviewStatus.PRESERVE_ONLY: ApprovalScope.INTERNAL_REVIEW_ONLY,
}

REQUIRED_REVIEW_FIELDS: tuple[str, ...] = (
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


def build_review_record(
    draft: dict,
    reviewer: str,
    review_status: str,
    approval_scope: str,
    checklist: dict,
    issues_found: list[str] | None = None,
    required_changes: list[str] | None = None,
    notes: str = "",
) -> dict:
    """Build a deterministic review record for an in-memory draft."""
    source_question_id = str(_nested_get(draft, ("identity", "source_question_id"), "unknown"))
    draft_id = str(_nested_get(draft, ("identity", "item_id"), "unknown"))
    reviewer_text = reviewer.strip() if isinstance(reviewer, str) else ""
    risk_before = str(_nested_get(draft, ("human_review", "risk_level"), "unknown"))

    return {
        "review_id": _build_review_id(source_question_id, draft_id, review_status, reviewer_text),
        "source_question_id": source_question_id,
        "draft_id": draft_id,
        "reviewer": reviewer_text,
        "reviewed_at": "not_set_in_skeleton",
        "review_status": review_status,
        "risk_before": risk_before,
        "risk_after": risk_before,
        "checklist": copy.deepcopy(checklist),
        "issues_found": list(issues_found or []),
        "required_changes": list(required_changes or []),
        "approval_scope": approval_scope,
        "governance_confirmation": copy.deepcopy(_as_mapping(draft.get("governance"))),
        "notes": notes,
    }


def validate_review_record(record: dict) -> list[str]:
    """Return deterministic validation errors for a human-review record."""
    errors: list[str] = []

    if not isinstance(record, dict):
        return ["review record must be a dict"]

    for field in REQUIRED_REVIEW_FIELDS:
        if field not in record:
            errors.append(f"missing field: {field}")

    if not _non_empty_string(record.get("reviewer")):
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
        for key in CHECKLIST_KEYS:
            if key not in checklist:
                errors.append(f"checklist missing field: {key}")
            elif checklist[key] is not True and checklist[key] is not False:
                errors.append(f"checklist.{key} must be boolean")

    if status in (ReviewStatus.APPROVED_FOR_STATIC_DEMO, ReviewStatus.APPROVED_FOR_TRAINING_PILOT):
        if not isinstance(checklist, dict) or any(checklist.get(key) is not True for key in CHECKLIST_KEYS):
            errors.append("approval requires all checklist items true")

    governance = record.get("governance_confirmation")
    if not isinstance(governance, dict):
        errors.append("governance_confirmation must be present")
    else:
        for field, expected in SAFE_GOVERNANCE.items():
            if governance.get(field) is not expected:
                errors.append(f"governance_confirmation.{field} must remain {str(expected).lower()}")

    return errors


def can_promote_to_static_demo(draft: dict, record: dict) -> bool:
    """Return True only when draft and review record allow static-demo promotion."""
    if validate_diagnostic_sba_item(draft):
        return False
    if validate_review_record(record):
        return False
    return (
        record.get("review_status") == ReviewStatus.APPROVED_FOR_STATIC_DEMO
        and record.get("approval_scope") == ApprovalScope.STATIC_DEMO_ONLY
    )


def apply_review_status(draft: dict, record: dict) -> dict:
    """Return a draft copy with additive review metadata only."""
    reviewed = copy.deepcopy(draft)
    reviewed["review_resolution"] = {
        "review_record": copy.deepcopy(record),
        "review_record_valid": not validate_review_record(record),
        "can_promote_to_static_demo": can_promote_to_static_demo(draft, record),
        "production_approved": False,
        "frontend_export_created": False,
    }
    reviewed["governance"] = copy.deepcopy(_as_mapping(draft.get("governance")))
    return reviewed


def _build_review_id(source_question_id: str, draft_id: str, review_status: str, reviewer: str) -> str:
    return "review_{source}_{draft}_{status}_{reviewer}".format(
        source=_slug(source_question_id),
        draft=_slug(draft_id),
        status=_slug(review_status),
        reviewer=_slug(reviewer or "missing_reviewer"),
    )


def _slug(value: str) -> str:
    safe = [char.lower() if char.isalnum() else "_" for char in str(value)]
    return "_".join("".join(safe).split("_"))


def _nested_get(mapping: Any, path: tuple[str, ...], default: Any) -> Any:
    current = mapping
    for key in path:
        if not isinstance(current, Mapping) or key not in current:
            return default
        current = current[key]
    return current


def _as_mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())
