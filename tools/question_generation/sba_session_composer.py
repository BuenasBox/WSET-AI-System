"""Deterministic SBA session composition from the canonical master bank."""

from __future__ import annotations

import copy
import json
import unicodedata
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from tools.constants import PROJECT_ROOT
from tools.question_generation.master_bank import MASTER_BANK_PATH, SAFE_GOVERNANCE


SESSION_SIZES: dict[str, int] = {
    "short": 5,
    "standard": 10,
    "long": 20,
}


def load_master_bank(
    path: str | Path = MASTER_BANK_PATH,
    root: str | Path = PROJECT_ROOT,
) -> dict[str, Any]:
    """Load the canonical master bank from disk."""
    full_path = Path(root) / Path(path)
    data = json.loads(full_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{full_path.as_posix()} must contain a JSON object")
    return data


def select_sba_session_items(
    master_bank: Mapping[str, Any] | None = None,
    *,
    ra: str | None = None,
    topic: str | None = None,
    difficulty: str | None = None,
    session_size: str | int = "standard",
    collection: str = "public_lab",
    question_priorities: list[dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    """Select reproducible SBA items with conceptual duplicate deferral.

    When question_priorities is provided (output of compose_adaptive_session_plan()),
    candidates are sorted by descending priority_score before deduplication and
    selection, so higher-priority items are chosen first.
    """
    bank = master_bank if master_bank is not None else load_master_bank()
    target_size = _resolve_session_size(session_size)
    collection_ids = set(_mapping(bank.get("collections")).get(collection, []))
    candidates = [
        item
        for item in bank.get("items", [])
        if isinstance(item, Mapping)
        and item.get("master_item_id") in collection_ids
        and item.get("question_type") == "single_best_answer"
        and _matches(_curriculum(item).get("ra"), ra)
        and _matches(_curriculum(item).get("topic"), topic, contains=True)
        and _matches(_curriculum(item).get("difficulty"), difficulty)
    ]

    if question_priorities:
        pmap: dict[str, int] = {
            str(p.get("question_id") or ""): int(p.get("priority_score", 0))
            for p in question_priorities
            if p.get("question_id")
        }
        candidates.sort(key=lambda item: -pmap.get(str(item.get("master_item_id") or ""), 0))

    selected: list[dict[str, Any]] = []
    deferred: list[dict[str, Any]] = []
    seen_signatures: set[str] = set()
    for candidate in candidates:
        signature = _concept_signature(candidate)
        if signature and signature in seen_signatures:
            deferred.append(dict(candidate))
            continue
        selected.append(copy.deepcopy(dict(candidate)))
        if signature:
            seen_signatures.add(signature)
        if len(selected) >= target_size:
            return selected

    for candidate in deferred:
        if len(selected) >= target_size:
            break
        selected.append(copy.deepcopy(candidate))
    return selected


def compose_sba_session(
    master_bank: Mapping[str, Any] | None = None,
    *,
    ra: str | None = None,
    topic: str | None = None,
    difficulty: str | None = None,
    session_size: str | int = "standard",
    collection: str = "public_lab",
    question_priorities: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Return a static, training-only session descriptor without file writes."""
    items = select_sba_session_items(
        master_bank,
        ra=ra,
        topic=topic,
        difficulty=difficulty,
        session_size=session_size,
        collection=collection,
        question_priorities=question_priorities,
    )
    return {
        "schema_version": "sba_session_v1",
        "exam_part": "diagnostic_sba",
        "collection": collection,
        "requested_size": _resolve_session_size(session_size),
        "item_count": len(items),
        "filters": {
            "ra": ra,
            "topic": topic,
            "difficulty": difficulty,
        },
        "master_item_ids": [item["master_item_id"] for item in items],
        "source_question_ids": [item["source_question_id"] for item in items],
        "items": items,
        "frontend_route": "frontend/diagnostic-sba/",
        "open_response_route": "frontend/open-response-lab/",
        "governance": copy.deepcopy(SAFE_GOVERNANCE),
    }


def _resolve_session_size(value: str | int) -> int:
    if isinstance(value, int):
        if value <= 0:
            raise ValueError("session_size must be positive")
        return value
    key = str(value).strip().lower()
    if key not in SESSION_SIZES:
        raise ValueError("session_size must be short, standard, long, or a positive integer")
    return SESSION_SIZES[key]


def _matches(value: Any, expected: str | None, *, contains: bool = False) -> bool:
    if expected is None:
        return True
    actual_norm = _normalize(value)
    expected_norm = _normalize(expected)
    return expected_norm in actual_norm if contains else actual_norm == expected_norm


def _concept_signature(item: Mapping[str, Any]) -> str:
    curriculum = _curriculum(item)
    concepts = (
        _string_list(curriculum.get("expected_topics"))
        + _string_list(curriculum.get("expected_keywords"))
        + _string_list(curriculum.get("expected_causal_links"))
    )
    normalized = sorted({_normalize(value) for value in concepts if _normalize(value)})
    return "|".join(normalized)


def _curriculum(item: Mapping[str, Any]) -> Mapping[str, Any]:
    return _mapping(item.get("curriculum"))


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if str(item).strip()]


def _normalize(value: Any) -> str:
    decomposed = unicodedata.normalize("NFD", str(value or "").lower())
    stripped = "".join(
        char for char in decomposed if unicodedata.category(char) != "Mn"
    )
    return " ".join(stripped.split())


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}
