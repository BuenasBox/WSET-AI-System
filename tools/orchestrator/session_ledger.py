"""Session Cognitive Ledger — Phase 2A.

Observational telemetry only. Records structured signals from each session.

This module is WRITE-ONLY in Phase 2A.
The ledger is NEVER consumed by:
  - the strategic planner
  - the retrieval sandbox
  - the Tutor / answer_builder
  - the self-eval harness

Governance: this module never sets safe_for_examiner=True, never writes
governance authority fields into the ledger, and connects to no external
services.

Retention policy: keep the last MAX_SESSIONS entries. Older entries are
silently dropped. The ledger is a rolling window, not an archive.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


# ---------------------------------------------------------------------------
# Module-level constants
# ---------------------------------------------------------------------------

LEDGER_VERSION: int = 1

# Rolling window size — older sessions are dropped beyond this limit.
# 100 sessions ≈ several weeks of daily use. Adjust only via this constant.
LEDGER_MAX_SESSIONS: int = 100

LEDGER_RETENTION_POLICY: str = f"keep_last_{LEDGER_MAX_SESSIONS}"

# Fields that must never appear in a ledger entry
_BLOCKED_FIELDS: frozenset[str] = frozenset({
    # Governance — must never enter telemetry
    "safe_for_examiner",
    "examiner_scoring_allowed",
    "examiner_scoring_active",
    # Privacy — raw queries and answers must not be stored
    "student_query",
    "tutor_answer",
    "retrieved_context",
    "context_package",
})


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def append_to_ledger(
    result: dict[str, Any],
    ledger_path: Path,
    reference_date: str | None = None,
) -> dict[str, Any]:
    """Append one session entry to the cognitive ledger. Write-only.

    Args:
        result:         Orchestrator result dict for the current session.
        ledger_path:    Path to session_ledger.json (created if missing).
        reference_date: ISO timestamp override — pass in tests for determinism.

    Returns:
        The session entry dict that was appended (for test inspection only).
        This return value is never fed back into the planner, retrieval, or Tutor.
    """
    timestamp: str = reference_date or datetime.now(timezone.utc).isoformat()
    ledger: dict[str, Any] = _load_or_init_ledger(ledger_path)
    entry: dict[str, Any] = _build_session_entry(result, timestamp)
    ledger["sessions"].append(entry)
    # Enforce retention policy — keep only the most recent sessions
    if len(ledger["sessions"]) > LEDGER_MAX_SESSIONS:
        ledger["sessions"] = ledger["sessions"][-LEDGER_MAX_SESSIONS:]
    ledger["session_count"] = len(ledger["sessions"])
    _write_ledger(ledger_path, ledger)
    return entry


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _load_or_init_ledger(ledger_path: Path) -> dict[str, Any]:
    """Load an existing ledger file, or return a fresh empty ledger."""
    if ledger_path.exists():
        try:
            with ledger_path.open("r", encoding="utf-8") as fh:
                data = json.load(fh)
            if isinstance(data, dict) and isinstance(data.get("sessions"), list):
                return data
        except (json.JSONDecodeError, OSError):
            pass  # Corrupt or unreadable — start fresh
    return _empty_ledger()


def _empty_ledger() -> dict[str, Any]:
    return {
        "version": LEDGER_VERSION,
        "session_count": 0,
        "retention_policy": LEDGER_RETENTION_POLICY,
        "sessions": [],
    }


def _build_session_entry(result: dict[str, Any], timestamp: str) -> dict[str, Any]:
    """Extract ledger-safe signals from the orchestrator result.

    Records ONLY structured metadata already produced by the system.
    Explicitly excluded:
      - raw user query text (privacy)
      - Tutor answer text (not in result; excluded by design)
      - retrieved chunks (too large; retrieval-internal)
      - governance flags (never in telemetry)
      - full misconception node objects (only IDs are stored)
      - full causal chain objects (only IDs are stored)
    """
    plan: dict[str, Any] = result.get("strategic_plan") or {}
    decision: dict[str, Any] = result.get("orchestrator_decision") or {}
    prepass: dict[str, Any] = result.get("detected_misconception") or {}
    pkg: dict[str, Any] = result.get("context_package") or {}
    forced_chains: list[Any] = pkg.get("forced_causal_chains") or []

    # Causal chain IDs only (not full chain objects)
    causal_chain_ids: list[str] = [
        str(chain.get("chain_id") or chain.get("id") or "").strip()
        for chain in forced_chains
        if isinstance(chain, dict) and (chain.get("chain_id") or chain.get("id"))
    ]

    # Misconception IDs only (not misconception text or corrected understanding)
    misconception_ids: list[str] = []
    mc_id = prepass.get("matched_misconception_id")
    if prepass.get("detected") and mc_id:
        misconception_ids = [str(mc_id).strip()]

    entry: dict[str, Any] = {
        "timestamp": timestamp,
        "route": str(decision.get("route") or "unknown"),
        "cold_start": bool(plan.get("cold_start", True)),
        "planning_confidence": round(float(plan.get("planning_confidence") or 0.0), 3),
        "difficulty_progression": str(plan.get("difficulty_progression") or "stable"),
        "sat_drill_needed": bool(plan.get("sat_drill_needed", False)),
        "review_topics": list(plan.get("review_topics") or []),
        "topics_covered": list(plan.get("recommended_next_topics") or []),
        "misconceptions_triggered": misconception_ids,
        "causal_chains_seen": causal_chain_ids,
    }

    # Final safety pass: strip any blocked field that might have leaked in
    for key in _BLOCKED_FIELDS:
        entry.pop(key, None)

    return entry


def _write_ledger(ledger_path: Path, ledger: dict[str, Any]) -> None:
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    with ledger_path.open("w", encoding="utf-8") as fh:
        json.dump(ledger, fh, indent=2, ensure_ascii=True)
        fh.write("\n")
