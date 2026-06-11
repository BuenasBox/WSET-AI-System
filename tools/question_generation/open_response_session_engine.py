"""Deterministic private Open Response Lab session selection.

This module is an inactive foundation layer. It selects candidate IDs for a
private RA1 open-response lab without scoring, grading, Tutor calls, retrieval,
LLMs, APIs, embeddings, vector databases, cloud services, or frontend exposure.
"""

from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from tools.constants import (
    CLOUD_SERVICES_ACTIVE,
    EXAMINER_SCORING_ALLOWED,
    SAFE_FOR_EXAMINER,
    USES_API,
    USES_EMBEDDINGS,
    USES_LLM,
    USES_VECTOR_DB,
)


CANDIDATES_PATH = Path("knowledge/question-bank/open_response/normalized/diagnostic_open_response_candidates.json")

# Phase Z.2 upstream reconciliation: session keys and sizes are the UI contract
# for open-response-lab/index.html (button data-session values). Changing these
# keys breaks production -- the regression gate (tools/frontend/regression_gate)
# must pass before any change here ships.
SESSION_SIZES: dict[str, int] = {
    "short_practice": 1,
    "standard_practice": 2,
    "extended_practice": 4,
    "mock_theory_2": 4,
}

# Mock Theory Part 2 approximation with available RAs (official distribution:
# Q1/Q2=RA1+RA2, Q3=RA1+RA2+RA5, Q4=RA1+RA3+RA4+RA5). With the current OR bank
# (RA1 + RA5 only): 3 questions from RA1, 1 from RA5.
MOCK_THEORY_2_RA_PLAN: tuple[tuple[str, int], ...] = (("RA1", 3), ("RA5", 1))

READY_IDS: tuple[str, ...] = (
    "800",
    "801",
    "802",
    "804",
    "805",
    "806",
    "812",
    "813",
    "814",
    "815",
)

READY_WITH_MINOR_GAPS_IDS: tuple[str, ...] = (
    "798",
    "799",
    "803",
    "808",
    "810",
    "811",
    "816",
    "817",
)

EXCLUDED_SOURCE_IDS: tuple[str, ...] = ("807", "809")

ACTIVE_POOL_IDS: tuple[str, ...] = (
    "798",
    "799",
    "800",
    "801",
    "802",
    "803",
    "804",
    "805",
    "806",
    "808",
    "810",
    "811",
    "812",
    "813",
    "814",
    "815",
    "816",
    "817",
)

POOL_READINESS: dict[str, str] = {
    **{source_id: "READY" for source_id in READY_IDS},
    **{source_id: "READY_WITH_MINOR_GAPS" for source_id in READY_WITH_MINOR_GAPS_IDS},
}

FEEDBACK_ALLOWED: tuple[str, ...] = (
    "present_concepts",
    "missing_concepts",
    "missing_causal_links",
    "revision_suggestions",
    "orientative_answer_model",
)

FEEDBACK_PROHIBITED: tuple[str, ...] = (
    "mark",
    "score",
    "percentage",
    "pass_fail",
    "wset_equivalence",
    "examiner_judgement",
    "official_grade",
)

LAB_GOVERNANCE_FLAGS: dict[str, bool] = {
    "safe_for_examiner": SAFE_FOR_EXAMINER,
    "examiner_scoring_allowed": EXAMINER_SCORING_ALLOWED,
    "official_wset_question": False,
    "training_item_only": True,
    "uses_llm": USES_LLM,
    "uses_api": USES_API,
    "uses_embeddings": USES_EMBEDDINGS,
    "uses_vector_db": USES_VECTOR_DB,
    "cloud_services_active": CLOUD_SERVICES_ACTIVE,
    "public_frontend_active": False,
    "open_response_lab_active": False,
}

REDUNDANT_PAIRS: tuple[frozenset[str], ...] = (
    frozenset(("804", "817")),
    frozenset(("810", "812")),
)


def load_open_response_candidates(path: str | Path = CANDIDATES_PATH) -> list[dict[str, Any]]:
    """Load normalized open-response candidates from disk."""
    candidate_path = Path(path)
    with candidate_path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, list):
        raise ValueError(f"{candidate_path.as_posix()} must contain a JSON list")
    return [dict(item) for item in data if isinstance(item, Mapping)]


def select_session_question_ids(
    candidates: Sequence[Mapping[str, Any]] | None = None,
    *,
    ra: str | None = None,
    topic: str | None = None,
    difficulty: str | None = None,
    session_size: str | int = "standard_practice",
) -> list[str]:
    """Return deterministic source_question_id values for one private lab session."""
    records = list(candidates) if candidates is not None else load_open_response_candidates()
    target_size = _resolve_session_size(session_size)

    # Mock Theory Part 2: RA-aware deterministic composition (no learner filters).
    if (
        str(session_size).strip().lower() == "mock_theory_2"
        and ra is None and topic is None and difficulty is None
    ):
        return _select_mock_theory_2_ids(records, target_size)

    filtered = [
        candidate
        for candidate in _active_pool_candidates(records)
        if _matches(candidate, "RA", ra)
        and _matches(candidate, "topic", topic)
        and _matches(candidate, "difficulty", difficulty)
    ]

    selected: list[str] = []
    deferred: list[str] = []
    for candidate in filtered:
        source_id = _source_id(candidate)
        if len(selected) >= target_size:
            break
        if _would_create_redundant_pair(source_id, selected):
            deferred.append(source_id)
            continue
        selected.append(source_id)

    for source_id in deferred:
        if len(selected) >= target_size:
            break
        selected.append(source_id)

    return selected


def compose_session(
    candidates: Sequence[Mapping[str, Any]] | None = None,
    *,
    ra: str | None = None,
    topic: str | None = None,
    difficulty: str | None = None,
    session_size: str | int = "standard_practice",
) -> dict[str, Any]:
    """Return an inactive, governance-bounded private lab session descriptor."""
    selected_ids = select_session_question_ids(
        candidates,
        ra=ra,
        topic=topic,
        difficulty=difficulty,
        session_size=session_size,
    )
    return {
        "lab_contract": "private_open_response_lab_ra1_foundation",
        "activation_status": "inactive",
        "session_size": _resolve_session_size(session_size),
        "source_question_ids": selected_ids,
        "pool_ids": list(ACTIVE_POOL_IDS),
        "excluded_source_question_ids": list(EXCLUDED_SOURCE_IDS),
        "feedback_allowed": list(FEEDBACK_ALLOWED),
        "feedback_prohibited": list(FEEDBACK_PROHIBITED),
        "governance_flags": dict(LAB_GOVERNANCE_FLAGS),
    }


def active_pool_manifest() -> list[dict[str, str]]:
    """Return the exact initial private lab pool in deterministic source order."""
    return [
        {"source_question_id": source_id, "readiness": POOL_READINESS[source_id]}
        for source_id in ACTIVE_POOL_IDS
    ]


def _select_mock_theory_2_ids(
    records: Sequence[Mapping[str, Any]], target_size: int
) -> list[str]:
    """Deterministic Mock Theory Part 2 composition: 3xRA1 (active pool first) + 1xRA5.

    RA5 items live outside the legacy active pool, so the RA5 slot draws from the
    full candidate list (minus excluded ids) in source order. Falls back to plain
    pool order if an RA bucket cannot be filled.
    """
    excluded = set(EXCLUDED_SOURCE_IDS)
    pool = list(_active_pool_candidates(records))
    pool_ids = {_source_id(c) for c in pool}
    extended = pool + [
        c for c in records
        if _source_id(c) not in pool_ids and _source_id(c) not in excluded
    ]

    selected: list[str] = []
    for ra_value, count in MOCK_THEORY_2_RA_PLAN:
        taken = 0
        for candidate in extended:
            if taken >= count or len(selected) >= target_size:
                break
            source_id = _source_id(candidate)
            if source_id in selected:
                continue
            if str(candidate.get("RA", "")).strip() == ra_value:
                selected.append(source_id)
                taken += 1

    # Fallback fill (bank without enough RA coverage): plain deterministic order.
    for candidate in extended:
        if len(selected) >= target_size:
            break
        source_id = _source_id(candidate)
        if source_id not in selected:
            selected.append(source_id)

    return selected[:target_size]


def _active_pool_candidates(candidates: Sequence[Mapping[str, Any]]) -> list[Mapping[str, Any]]:
    by_id = {_source_id(candidate): candidate for candidate in candidates}
    return [by_id[source_id] for source_id in ACTIVE_POOL_IDS if source_id in by_id]


def _resolve_session_size(session_size: str | int) -> int:
    if isinstance(session_size, int):
        if session_size <= 0:
            raise ValueError("session_size must be positive")
        return session_size
    key = str(session_size).strip().lower()
    if key not in SESSION_SIZES:
        raise ValueError(
            "session_size must be one of "
            + ", ".join(SESSION_SIZES)
            + ", or a positive integer"
        )
    return SESSION_SIZES[key]


def _matches(candidate: Mapping[str, Any], field: str, expected: str | None) -> bool:
    if expected is None:
        return True
    return _normalize(candidate.get(field)) == _normalize(expected)


def _would_create_redundant_pair(source_id: str, selected_ids: Sequence[str]) -> bool:
    current = set(selected_ids)
    return any(source_id in pair and bool(current & pair) for pair in REDUNDANT_PAIRS)


def _source_id(candidate: Mapping[str, Any]) -> str:
    return str(candidate.get("source_question_id", "")).strip()


def _normalize(value: Any) -> str:
    return " ".join(str(value or "").strip().lower().split())
