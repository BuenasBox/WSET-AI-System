"""Pure dashboard-data projection for private Master Bank utilization."""

from __future__ import annotations

import copy
from collections import Counter
from collections.abc import Mapping
from typing import Any

from tools.question_generation.master_bank import SAFE_GOVERNANCE
from tools.question_generation.master_bank_eligibility import build_eligibility_index


def build_master_bank_utilization_data(
    master_bank: Mapping[str, Any],
    les: Mapping[str, Any],
    session: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Expose aggregate metrics without writing dashboard or learner files."""
    eligibility = build_eligibility_index(master_bank)
    operational_counts = eligibility["operational_counts"]
    active_pool = operational_counts["sba_operational_pool"]
    ra_signals = les.get("RA_signals", {})
    topic_signals = les.get("topic_signals", {})
    exposure_signals = les.get("question_exposure_signals", {})
    normalized_ra = _mapping(ra_signals)
    normalized_topics = _mapping(topic_signals)
    normalized_exposure = _mapping(exposure_signals)
    exposure_counts = [
        int(signal.get("exposure_count", 0) or 0)
        for signal in normalized_exposure.values()
        if isinstance(signal, Mapping)
    ]

    return {
        "schema_version": "master_bank_utilization_dashboard_data_v1",
        "bank": {
            "total_bank_size": len(master_bank.get("items", [])),
            "active_pool": active_pool,
            "total_master_bank": operational_counts["total_master_bank"],
            "sba_operational_pool": operational_counts["sba_operational_pool"],
            "open_response_candidate_pool": operational_counts[
                "open_response_candidate_pool"
            ],
            "open_response_review_pool": operational_counts[
                "open_response_review_pool"
            ],
            "inactive": operational_counts["inactive"],
            "public_lab": operational_counts["public_lab"],
            "eligibility_primary": copy.deepcopy(eligibility["primary_counts"]),
            "eligibility_categories": copy.deepcopy(eligibility["category_counts"]),
        },
        "session_composition": _session_composition(session),
        "ra_coverage": {
            ra_id: {
                "exposure_count": int(signal.get("exposure_count", 0) or 0),
                "performance_indicators": copy.deepcopy(
                    _mapping(signal.get("performance"))
                ),
                "last_seen": signal.get("last_seen"),
            }
            for ra_id, signal in normalized_ra.items()
            if isinstance(signal, Mapping)
        },
        "topic_coverage": {
            topic: {
                "exposure_count": int(signal.get("exposure_count", 0) or 0),
                "confidence_level": signal.get("confidence_level", "not_recorded"),
                "weakness_level": signal.get("weakness_level", "not_recorded"),
                "last_seen": signal.get("last_seen"),
            }
            for topic, signal in normalized_topics.items()
            if isinstance(signal, Mapping)
        },
        "exposure_statistics": {
            "questions_seen": len(normalized_exposure),
            "total_exposures": sum(exposure_counts),
            "never_seen_active_questions": max(active_pool - len(normalized_exposure), 0),
            "maximum_question_exposure": max(exposure_counts, default=0),
            "repeat_exposure_count": sum(max(count - 1, 0) for count in exposure_counts),
        },
        "governance": copy.deepcopy(SAFE_GOVERNANCE),
    }


def _session_composition(session: Mapping[str, Any] | None) -> dict[str, Any] | None:
    if not isinstance(session, Mapping):
        return None
    achieved = _mapping(session.get("achieved_composition"))
    return {
        "session_id": session.get("session_id"),
        "mode": session.get("mode"),
        "item_count": int(session.get("item_count", 0) or 0),
        "ra": copy.deepcopy(_mapping(achieved.get("ra"))),
        "difficulty": copy.deepcopy(_mapping(achieved.get("difficulty"))),
        "topics": copy.deepcopy(_mapping(achieved.get("topics"))),
        "question_types": copy.deepcopy(_mapping(achieved.get("question_types"))),
        "warnings": list(session.get("warnings", [])),
    }


def summarize_bank_topics(master_bank: Mapping[str, Any]) -> dict[str, int]:
    """Return deterministic bank topic counts for reporting and tests."""
    counts = Counter(
        str(_mapping(item.get("curriculum")).get("topic", "unknown"))
        for item in master_bank.get("items", [])
        if isinstance(item, Mapping)
    )
    return dict(sorted(counts.items()))


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}
