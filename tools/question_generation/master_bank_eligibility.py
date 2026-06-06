"""Deterministic operational eligibility for canonical Master Bank records."""

from __future__ import annotations

import copy
from collections import Counter
from collections.abc import Mapping
from typing import Any

from tools.question_generation.master_bank import SAFE_GOVERNANCE


ELIGIBILITY_CATEGORIES = (
    "public_lab",
    "private_practice",
    "adaptive_candidate",
    "open_response_candidate",
    "inactive",
)
INACTIVE_REVIEW_STATES = frozenset({"preserve_only", "requires_revision", "rejected"})
SUPPORTED_DIFFICULTIES = frozenset({"foundational", "intermediate", "distinction"})
SUPPORTED_RAS = frozenset({"RA1", "RA2", "RA3", "RA4", "RA5"})


def classify_master_item(item: Mapping[str, Any]) -> dict[str, Any]:
    """Classify one record without activating public or adaptive behavior."""
    question_type = str(item.get("question_type", "")).strip()
    status = _mapping(item.get("status"))
    review_state = str(status.get("review_state", "")).strip()
    is_public = bool(status.get("public_lab"))
    structurally_usable = _is_structurally_usable(item)
    categories: list[str] = []
    reasons: list[str] = []

    if is_public and structurally_usable:
        primary = "public_lab"
        categories.extend(("public_lab", "private_practice"))
        reasons.append("stable_public_lab_member")
    elif question_type == "open_response" and review_state == "approved_open_response":
        primary = "open_response_candidate"
        categories.append("open_response_candidate")
        reasons.append("approved_open_response_record")
    elif (
        question_type == "single_best_answer"
        and structurally_usable
        and review_state not in INACTIVE_REVIEW_STATES
    ):
        primary = "private_practice"
        categories.append("private_practice")
        reasons.append("structurally_usable_private_sba")
    else:
        primary = "inactive"
        categories.append("inactive")
        if review_state in INACTIVE_REVIEW_STATES:
            reasons.append(f"review_state:{review_state}")
        if not structurally_usable:
            reasons.append("structural_requirements_not_met")

    curriculum = _mapping(item.get("curriculum"))
    if (
        "private_practice" in categories
        and curriculum.get("ra") in SUPPORTED_RAS
        and curriculum.get("difficulty") in SUPPORTED_DIFFICULTIES
    ):
        categories.append("adaptive_candidate")
        reasons.append("metadata_complete_for_future_adaptation")

    return {
        "schema_version": "master_bank_eligibility_v1",
        "primary_category": primary,
        "categories": categories,
        "structurally_usable": structurally_usable,
        "reasons": reasons,
        "governance": copy.deepcopy(SAFE_GOVERNANCE),
    }


def build_eligibility_index(master_bank: Mapping[str, Any]) -> dict[str, Any]:
    """Return classification and category counts for every Master Bank record."""
    records: dict[str, dict[str, Any]] = {}
    primary_counts: Counter[str] = Counter()
    category_counts: Counter[str] = Counter()
    for item in master_bank.get("items", []):
        if not isinstance(item, Mapping):
            continue
        item_id = str(item.get("master_item_id", "")).strip()
        if not item_id:
            continue
        eligibility = classify_master_item(item)
        records[item_id] = eligibility
        primary_counts[eligibility["primary_category"]] += 1
        category_counts.update(eligibility["categories"])

    return {
        "schema_version": "master_bank_eligibility_index_v1",
        "record_count": len(records),
        "primary_counts": {
            category: primary_counts.get(category, 0)
            for category in ELIGIBILITY_CATEGORIES
        },
        "category_counts": {
            category: category_counts.get(category, 0)
            for category in ELIGIBILITY_CATEGORIES
        },
        "records": records,
        "governance": copy.deepcopy(SAFE_GOVERNANCE),
    }


def is_session_eligible(
    item: Mapping[str, Any],
    *,
    include_open_response: bool = False,
) -> bool:
    """Return whether an item may enter a private composed session."""
    eligibility = classify_master_item(item)
    categories = set(eligibility["categories"])
    if "inactive" in categories:
        return False
    if item.get("question_type") == "open_response":
        return include_open_response and "open_response_candidate" in categories
    return "private_practice" in categories


def _is_structurally_usable(item: Mapping[str, Any]) -> bool:
    if item.get("governance") != SAFE_GOVERNANCE:
        return False
    if not str(item.get("master_item_id", "")).strip():
        return False
    if not str(item.get("stem", "")).strip():
        return False
    question_type = item.get("question_type")
    if question_type == "open_response":
        return True
    if question_type != "single_best_answer":
        return False
    source_content = _mapping(item.get("source_content"))
    options = _mapping(source_content.get("options"))
    answer = str(source_content.get("correct_answer_letter", "")).strip().upper()
    return set(options) == {"A", "B", "C", "D"} and answer in options


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}
