"""WWJ Remediation Runtime — maps MC_IDs to Wine With Jimmy chunk remediation paths.

Implements get_remediation_path(mc_id) -> dict, which is the bridge between a
LES misconception_triggered signal and the Tutor's content delivery.

Returns a static lookup result — no LLM, no API, no text generation.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, TypedDict

from tools.constants import KNOWLEDGE_DIR

WWJ_LOOKUP_PATH = KNOWLEDGE_DIR / "knowledge-map" / "mc_wwj_lookup.json"

_LOOKUP_CACHE: dict[str, Any] | None = None


class RemediationPath(TypedDict):
    mc_id: str
    wwj_chunks: list[str]
    availability: str
    content_type: str | None
    remediation_message: str


def _load_lookup(path: Path = WWJ_LOOKUP_PATH) -> dict[str, Any]:
    global _LOOKUP_CACHE
    if _LOOKUP_CACHE is None:
        with path.open("r", encoding="utf-8") as f:
            _LOOKUP_CACHE = json.load(f)
    return _LOOKUP_CACHE


def _build_index(lookup_data: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        entry["mc_id"]: entry
        for entry in lookup_data.get("lookup", [])
        if "mc_id" in entry
    }


def get_remediation_path(
    mc_id: str,
    lookup_path: Path = WWJ_LOOKUP_PATH,
) -> dict[str, Any]:
    """Return the WWJ remediation path for a given MC_ID.

    For unknown MC_IDs, returns availability='pending' with an empty chunk list.
    Never calls external services; all data is from the static lookup file.
    The returned dict matches the RemediationPath schema.
    """
    lookup_data = _load_lookup(lookup_path)
    index = _build_index(lookup_data)

    if mc_id not in index:
        return {
            "mc_id": mc_id,
            "wwj_chunks": [],
            "availability": "pending",
            "content_type": None,
            "remediation_message": (
                "No Wine With Jimmy remediation content is available for this "
                "misconception yet. Return to the relevant chapter of the "
                "WSET Level 3 study guide."
            ),
        }

    entry = index[mc_id]
    raw_chunks = entry.get("wwj_chunks") or []
    chunks: list[str] = (
        [c for c in raw_chunks if isinstance(c, str) and c]
        if isinstance(raw_chunks, list)
        else []
    )
    availability = str(entry.get("availability") or "pending")
    content_type: str | None = entry.get("content_type") or None

    if availability == "pending" or not chunks:
        message = (
            "No Wine With Jimmy remediation content is currently available for "
            "this misconception. Return to the relevant chapter of the "
            "WSET Level 3 study guide."
        )
    elif availability == "partial":
        message = (
            "Partial Wine With Jimmy content is available. Review the linked "
            "video chunks and supplement with the WSET Level 3 study guide."
        )
    else:
        message = (
            "Wine With Jimmy remediation content is available for this misconception. "
            "Review the linked video chunks to reinforce understanding."
        )

    return {
        "mc_id": mc_id,
        "wwj_chunks": chunks,
        "availability": availability,
        "content_type": content_type,
        "remediation_message": message,
    }
