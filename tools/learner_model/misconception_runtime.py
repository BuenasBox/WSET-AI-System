"""Misconception Runtime Consumer — wires misconception_signals.json to the LES.

On each SBA outcome, detects if the selected option is linked to a known MC_ID
and updates the in-memory LES:

  - misconception_signals[mc_id].detection_count  (existing LES schema)
  - misconception_sessions[mc_id]  — session_ids list for persistence tracking
  - misconception_resolution[mc_id] — resolved flag and timestamp

Both extra top-level keys survive LES round-trips via _with_governance_defaults
because they are not in DEFAULT_LES (and therefore never overwritten by normalization).

Emitted signals (returned as strings, never written to UI):
  misconception_triggered, misconception_resolved, misconception_persistent
"""

from __future__ import annotations

import json
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from tools.constants import KNOWLEDGE_DIR

MISCONCEPTION_SIGNALS_PATH = KNOWLEDGE_DIR / "knowledge-map" / "misconception_signals.json"

SIGNAL_TRIGGERED = "misconception_triggered"
SIGNAL_RESOLVED = "misconception_resolved"
SIGNAL_PERSISTENT = "misconception_persistent"

_SIGNALS_CACHE: dict[str, Any] | None = None


def _load_signals(path: Path = MISCONCEPTION_SIGNALS_PATH) -> dict[str, Any]:
    global _SIGNALS_CACHE
    if _SIGNALS_CACHE is None:
        with path.open("r", encoding="utf-8") as f:
            _SIGNALS_CACHE = json.load(f)
    return _SIGNALS_CACHE


def known_mc_ids(signals_path: Path = MISCONCEPTION_SIGNALS_PATH) -> frozenset[str]:
    """Return the set of MC_IDs defined in misconception_signals.json."""
    data = _load_signals(signals_path)
    return frozenset(m["mc_id"] for m in data.get("misconceptions", []))


def process_sba_outcome(
    les: dict[str, Any],
    *,
    mc_id: str,
    outcome: str,
    session_id: str,
    signals_path: Path = MISCONCEPTION_SIGNALS_PATH,
) -> tuple[dict[str, Any], list[str]]:
    """Update in-memory LES for one SBA item linked to a misconception.

    Args:
        les: Current LES dict (not mutated — a deep copy is returned).
        mc_id: The misconception ID linked to the selected distractor.
        outcome: "incorrect" triggers the misconception; "correct" may resolve it.
        session_id: Caller-supplied opaque session identifier for persistence tracking.
        signals_path: Path to misconception_signals.json (override in tests).

    Returns:
        (updated_les, emitted_signals).  emitted_signals is a list of signal name
        strings.  Writes nothing to disk — caller is responsible for persistence.
    """
    if not mc_id or mc_id not in known_mc_ids(signals_path):
        return les, []

    updated = deepcopy(les)
    emitted: list[str] = []
    now = _utc_now()

    # --- Existing LES key: misconception_signals ---
    mc_signals: dict[str, Any] = updated.setdefault("misconception_signals", {})
    entry = mc_signals.get(mc_id, {})
    detection_count = int(entry.get("detection_count", 0))
    last_detected: str | None = entry.get("last_detected")

    # --- Runtime-extension key: misconception_sessions (persistence) ---
    mc_sessions: dict[str, Any] = updated.setdefault("misconception_sessions", {})
    sess = mc_sessions.get(mc_id, {"session_ids": [], "first_detected": None})
    if not isinstance(sess.get("session_ids"), list):
        sess["session_ids"] = []

    # --- Runtime-extension key: misconception_resolution ---
    mc_resolution: dict[str, Any] = updated.setdefault("misconception_resolution", {})
    res = mc_resolution.get(mc_id, {"first_detected": None, "resolved": False, "resolved_at": None})

    if outcome == "incorrect":
        detection_count += 1
        last_detected = now
        emitted.append(SIGNAL_TRIGGERED)

        if res["first_detected"] is None:
            res["first_detected"] = now

        if session_id and session_id not in sess["session_ids"]:
            sess["session_ids"].append(session_id)
        if sess["first_detected"] is None and session_id:
            sess["first_detected"] = now

        if len(sess["session_ids"]) > 1:
            emitted.append(SIGNAL_PERSISTENT)

    elif outcome == "correct":
        if detection_count > 0 and not res.get("resolved"):
            res["resolved"] = True
            res["resolved_at"] = now
            emitted.append(SIGNAL_RESOLVED)

    mc_signals[mc_id] = {
        "misconception_id": mc_id,
        "detection_count": detection_count,
        "last_detected": last_detected,
    }
    mc_sessions[mc_id] = sess
    mc_resolution[mc_id] = res

    return updated, emitted


def _utc_now() -> str:
    return datetime.now(tz=timezone.utc).isoformat()
