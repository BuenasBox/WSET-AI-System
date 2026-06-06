"""Deterministic operational eligibility for canonical Master Bank records."""

from __future__ import annotations

import copy
import json
from collections import Counter
from collections.abc import Mapping
from functools import lru_cache
from pathlib import Path
from typing import Any

from tools.constants import PROJECT_ROOT
from tools.question_generation.master_bank import SAFE_GOVERNANCE


OPEN_RESPONSE_SUITABILITY_PATH = Path(
    "knowledge/question-bank/open_response/suitability/"
    "master_bank_open_response_suitability.json"
)
ELIGIBILITY_CATEGORIES = (
    "public_lab",
    "private_practice",
    "adaptive_candidate",
    "open_response_candidate",
    "open_response_review_pool",
    "inactive",
)
INACTIVE_REVIEW_STATES = frozenset({"preserve_only", "requires_revision", "rejected"})
SUPPORTED_DIFFICULTIES = frozenset({"foundational", "intermediate", "distinction"})
SUPPORTED_RAS = frozenset({"RA1", "RA2", "RA3", "RA4", "RA5"})


def load_open_response_suitability_index(
    path: str | Path = OPEN_RESPONSE_SUITABILITY_PATH,
    root: str | Path = PROJECT_ROOT,
) -> dict[str, dict[str, Any]]:
    """Load the shadow suitability artifact as a Master Bank ID index."""
    payload = json.loads((Path(root) / Path(path)).read_text(encoding="utf-8"))
    records = payload.get("records", [])
    if not isinstance(records, list):
        raise ValueError("open response suitability records must be a list")
    index: dict[str, dict[str, Any]] = {}
    for record in records:
        if not isinstance(record, Mapping):
            raise ValueError("every suitability record must be an object")
        item_id = str(record.get("master_item_id", "")).strip()
        if not item_id or item_id in index:
            raise ValueError("suitability master_item_id values must be unique")
        index[item_id] = dict(record)
    return index


@lru_cache(maxsize=1)
def _default_open_response_suitability_index() -> dict[str, dict[str, Any]]:
    return load_open_response_suitability_index()


def classify_master_item(
    item: Mapping[str, Any],
    suitability: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Classify one record without activating public or adaptive behavior."""
    question_type = str(item.get("question_type", "")).strip()
    status = _mapping(item.get("status"))
    review_state = str(status.get("review_state", "")).strip()
    is_public = bool(status.get("public_lab"))
    structurally_usable = _is_structurally_usable(item)
    suitability_record = _mapping(suitability)
    if suitability is None:
        item_id = str(item.get("master_item_id", "")).strip()
        suitability_record = _mapping(
            _default_open_response_suitability_index().get(item_id)
        )
    suitability_classification = _normalized_suitability_classification(
        suitability_record.get("classification")
    )
    explicitly_sba_eligible = suitability_record.get("sba_eligible")
    if not isinstance(explicitly_sba_eligible, bool):
        explicitly_sba_eligible = suitability_classification == "sba_only"
    if is_public and structurally_usable:
        explicitly_sba_eligible = True
    categories: list[str] = []
    reasons: list[str] = []

    if suitability_classification == "inactive":
        primary = "inactive"
        categories.append("inactive")
        reasons.append("suitability:inactive")
    elif suitability_classification == "open_response_candidate":
        primary = "public_lab" if is_public and structurally_usable else "open_response_candidate"
        if is_public and structurally_usable:
            categories.append("public_lab")
        categories.append("open_response_candidate")
        reasons.append("suitability:strong_open_response_candidate")
    elif suitability_classification == "open_response_review_pool":
        primary = "public_lab" if is_public and structurally_usable else "open_response_review_pool"
        if is_public and structurally_usable:
            categories.append("public_lab")
        categories.append("open_response_review_pool")
        reasons.append("suitability:requires_human_review")
    elif is_public and structurally_usable:
        primary = "public_lab"
        categories.append("public_lab")
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

    if (
        primary != "inactive"
        and structurally_usable
        and question_type == "single_best_answer"
        and explicitly_sba_eligible
    ):
        if "private_practice" not in categories:
            categories.append("private_practice")
        reasons.append("explicit_sba_eligible")

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
        "sba_eligible": bool(
            "private_practice" in categories and primary != "inactive"
        ),
        "suitability_classification": suitability_classification,
        "reasons": reasons,
        "governance": copy.deepcopy(SAFE_GOVERNANCE),
    }


def build_eligibility_index(
    master_bank: Mapping[str, Any],
    suitability_index: Mapping[str, Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    """Return classification and category counts for every Master Bank record."""
    suitability_records = (
        dict(suitability_index)
        if suitability_index is not None
        else load_open_response_suitability_index()
    )
    master_ids = {
        str(item.get("master_item_id", "")).strip()
        for item in master_bank.get("items", [])
        if isinstance(item, Mapping) and str(item.get("master_item_id", "")).strip()
    }
    suitability_ids = set(suitability_records)
    if suitability_ids != master_ids:
        missing = sorted(master_ids - suitability_ids)
        extra = sorted(suitability_ids - master_ids)
        raise ValueError(
            "suitability coverage mismatch: "
            f"missing={missing[:5]}, extra={extra[:5]}"
        )
    records: dict[str, dict[str, Any]] = {}
    primary_counts: Counter[str] = Counter()
    category_counts: Counter[str] = Counter()
    for item in master_bank.get("items", []):
        if not isinstance(item, Mapping):
            continue
        item_id = str(item.get("master_item_id", "")).strip()
        if not item_id:
            continue
        eligibility = classify_master_item(item, suitability_records.get(item_id))
        records[item_id] = eligibility
        primary_counts[eligibility["primary_category"]] += 1
        category_counts.update(eligibility["categories"])

    operational_counts = {
        "total_master_bank": len(records),
        "sba_operational_pool": sum(
            1 for record in records.values() if record["sba_eligible"]
        ),
        "open_response_candidate_pool": category_counts.get(
            "open_response_candidate", 0
        ),
        "open_response_review_pool": category_counts.get(
            "open_response_review_pool", 0
        ),
        "inactive": category_counts.get("inactive", 0),
        "public_lab": category_counts.get("public_lab", 0),
    }
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
        "operational_counts": operational_counts,
        "records": records,
        "governance": copy.deepcopy(SAFE_GOVERNANCE),
    }


def is_session_eligible(
    item: Mapping[str, Any],
    *,
    include_open_response: bool = False,
    suitability: Mapping[str, Any] | None = None,
) -> bool:
    """Return whether an item may enter a private composed session."""
    eligibility = classify_master_item(item, suitability)
    categories = set(eligibility["categories"])
    if "inactive" in categories:
        return False
    if item.get("question_type") == "open_response":
        return include_open_response and "open_response_candidate" in categories
    return eligibility["sba_eligible"]


def _normalized_suitability_classification(value: Any) -> str:
    normalized = str(value or "").strip()
    aliases = {
        "strong_open_response_candidate": "open_response_candidate",
        "open_response_candidate": "open_response_candidate",
        "requires_human_review": "open_response_review_pool",
        "human_review_required": "open_response_review_pool",
        "open_response_review_pool": "open_response_review_pool",
        "sba_only": "sba_only",
        "inactive": "inactive",
    }
    return aliases.get(normalized, "")


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
