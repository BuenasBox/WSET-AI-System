"""Ledger Summary Layer — Phase 2B.

Computes deterministic aggregate observations from the session cognitive ledger.
This is a reporting layer only.

This module is NEVER consumed by:
  - the strategic planner
  - the retrieval sandbox
  - the Tutor / answer_builder
  - the self-eval harness
  - the SAT reasoner

It answers the question: "What has happened historically?"
It does NOT answer: "What should happen next?" — that is strategic_planner's job.

Design principles:
  - Pure function: same input → same output, always.
  - No side effects: no file writes, no I/O, no logging.
  - No external dependencies beyond stdlib.
  - Governance-clean: no safe_for_examiner, no examiner scoring, no grading.
  - Deterministic ordering: ties broken alphabetically.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any


# ---------------------------------------------------------------------------
# Configuration constants
# ---------------------------------------------------------------------------

# Maximum items in each "top" frequency list
TOP_N: int = 10

# Valid difficulty progression values (from strategic_planner.py)
DIFFICULTY_VALUES: tuple[str, ...] = ("stable", "consolidate", "escalate")

# Governance and grading fields that must NEVER appear in the summary
_BLOCKED_SUMMARY_FIELDS: frozenset[str] = frozenset({
    "safe_for_examiner",
    "examiner_scoring_allowed",
    "examiner_scoring_active",
    "exam_readiness",
    "student_grade",
    "student_score",
    "predicted_pass_probability",
    "examiner_equivalence",
    "pass_rate",
    "grade",
    "score",
})


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def summarize_ledger(ledger: dict[str, Any]) -> dict[str, Any]:
    """Return a deterministic aggregate summary of the session cognitive ledger.

    Args:
        ledger: A ledger dict as written by session_ledger.py. Must have a
                "sessions" key containing a list of session entry dicts.
                Malformed or missing sessions are silently skipped.

    Returns:
        A summary dict with only aggregate observations. Deterministic for
        any given input. Never modifies the input ledger.

    The summary is a reporting artifact only. It must not be fed back into
    the planner, retrieval, Tutor, or any component that influences session
    behaviour.
    """
    if not isinstance(ledger, dict):
        return _empty_summary()

    raw_sessions: list[Any] = ledger.get("sessions") or []
    sessions: list[dict[str, Any]] = [
        s for s in raw_sessions
        if isinstance(s, dict)
    ]
    n: int = len(sessions)

    if n == 0:
        return _empty_summary()

    # -----------------------------------------------------------------------
    # Frequency counters
    # -----------------------------------------------------------------------
    review_topic_counter: Counter[str] = Counter()
    misconception_counter: Counter[str] = Counter()
    causal_chain_counter: Counter[str] = Counter()
    difficulty_counter: Counter[str] = Counter()
    route_counter: Counter[str] = Counter()

    sat_drill_count: int = 0
    cold_start_count: int = 0
    confidence_total: float = 0.0
    valid_confidence_count: int = 0

    for session in sessions:
        # Review topics
        for topic in _safe_list(session.get("review_topics")):
            if topic:
                review_topic_counter[str(topic)] += 1

        # Misconceptions
        for mc in _safe_list(session.get("misconceptions_triggered")):
            if mc:
                misconception_counter[str(mc)] += 1

        # Causal chains
        for chain in _safe_list(session.get("causal_chains_seen")):
            if chain:
                causal_chain_counter[str(chain)] += 1

        # Difficulty progression
        diff = str(session.get("difficulty_progression") or "stable").strip()
        if diff in DIFFICULTY_VALUES:
            difficulty_counter[diff] += 1

        # Route
        route = str(session.get("route") or "unknown").strip()
        route_counter[route] += 1

        # SAT drill
        if session.get("sat_drill_needed"):
            sat_drill_count += 1

        # Cold start
        if session.get("cold_start"):
            cold_start_count += 1

        # Planning confidence
        raw_conf = session.get("planning_confidence")
        if raw_conf is not None:
            try:
                conf = float(raw_conf)
                confidence_total += conf
                valid_confidence_count += 1
            except (TypeError, ValueError):
                pass

    # -----------------------------------------------------------------------
    # Derived metrics
    # -----------------------------------------------------------------------
    avg_confidence: float = round(
        confidence_total / valid_confidence_count, 3
    ) if valid_confidence_count > 0 else 0.0

    sat_drill_rate: float = round(sat_drill_count / n, 3)
    cold_start_rate: float = round(cold_start_count / n, 3)

    diff_dist: dict[str, int] = {
        d: difficulty_counter.get(d, 0) for d in DIFFICULTY_VALUES
    }
    diff_dist_pct: dict[str, float] = {
        d: round(difficulty_counter.get(d, 0) / n, 3) for d in DIFFICULTY_VALUES
    }
    route_dist: dict[str, int] = dict(
        sorted(route_counter.items())  # alphabetical for determinism
    )

    summary: dict[str, Any] = {
        "session_count": n,
        "sessions_analysed": n,
        "average_planning_confidence": avg_confidence,
        "sat_drill_rate": sat_drill_rate,
        "cold_start_rate": cold_start_rate,
        "top_review_topics": _top_n(review_topic_counter, TOP_N),
        "top_misconceptions": _top_n(misconception_counter, TOP_N),
        "top_causal_chains": _top_n(causal_chain_counter, TOP_N),
        "difficulty_distribution": diff_dist,
        "difficulty_distribution_pct": diff_dist_pct,
        "route_distribution": route_dist,
    }

    # Final safety pass — strip any blocked field that might have leaked in
    for key in _BLOCKED_SUMMARY_FIELDS:
        summary.pop(key, None)

    return summary


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _empty_summary() -> dict[str, Any]:
    """Return a valid zero-state summary for an empty or invalid ledger."""
    return {
        "session_count": 0,
        "sessions_analysed": 0,
        "average_planning_confidence": 0.0,
        "sat_drill_rate": 0.0,
        "cold_start_rate": 0.0,
        "top_review_topics": [],
        "top_misconceptions": [],
        "top_causal_chains": [],
        "difficulty_distribution": {d: 0 for d in DIFFICULTY_VALUES},
        "difficulty_distribution_pct": {d: 0.0 for d in DIFFICULTY_VALUES},
        "route_distribution": {},
    }


def _top_n(counter: Counter[str], n: int) -> list[dict[str, Any]]:
    """Return the top-N items from a counter as a sorted frequency list.

    Ordering: descending by count, then ascending alphabetically for ties.
    This ensures the output is deterministic regardless of insertion order.
    """
    # Sort: primary key = -count (descending), secondary = item (ascending)
    sorted_items = sorted(counter.items(), key=lambda pair: (-pair[1], pair[0]))
    total: int = sum(counter.values())
    return [
        {
            "value": item,
            "count": count,
            "frequency": round(count / total, 3) if total > 0 else 0.0,
        }
        for item, count in sorted_items[:n]
    ]


def _safe_list(value: Any) -> list[Any]:
    """Return value as a list, or an empty list if it is not iterable or is a str."""
    if isinstance(value, list):
        return value
    return []


# ---------------------------------------------------------------------------
# CLI — Phase 2C (read-only observability entry point)
# ---------------------------------------------------------------------------

# Default ledger path — used when --ledger is not supplied
try:
    from tools.constants import NAZARETH_DIR as _NAZARETH_DIR
    DEFAULT_LEDGER_PATH: Path = _NAZARETH_DIR / "session_ledger.json"
except Exception:  # pragma: no cover — constants may not be importable in all envs
    DEFAULT_LEDGER_PATH = Path("knowledge/nazareth/session_ledger.json")


def load_ledger_file(path: Path) -> dict[str, Any]:
    """Load and return the ledger JSON from *path*.

    Raises:
        FileNotFoundError: if the file does not exist.
        ValueError: if the file contains invalid JSON.

    This function is read-only — it never writes to any file.
    """
    if not path.exists():
        raise FileNotFoundError(f"Ledger file not found: {path}")
    try:
        with path.open("r", encoding="utf-8") as fh:
            return json.load(fh)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Ledger file contains invalid JSON: {path}") from exc


def format_report(summary: dict[str, Any], top_n: int = TOP_N) -> str:
    """Render *summary* as a deterministic, human-readable report string.

    Args:
        summary: Output of summarize_ledger().
        top_n:   Maximum items to show in each ranked list. Defaults to TOP_N.

    Returns:
        A multi-line string suitable for printing to stdout.
        Output is deterministic for any given summary dict.
    """
    lines: list[str] = []
    _h = lines.append  # shorthand

    _h("=" * 52)
    _h("  WSET-AI-System — Ledger Summary")
    _h("=" * 52)
    _h("")

    n = summary.get("sessions_analysed", 0)
    _h(f"Sessions analysed:          {n}")
    _h(f"Average planning confidence:{summary.get('average_planning_confidence', 0.0):>8.3f}")
    _h(f"SAT drill rate:             {summary.get('sat_drill_rate', 0.0):>8.3f}")
    _h(f"Cold-start rate:            {summary.get('cold_start_rate', 0.0):>8.3f}")
    _h("")

    # Difficulty distribution
    diff = summary.get("difficulty_distribution", {})
    diff_pct = summary.get("difficulty_distribution_pct", {})
    _h("Difficulty distribution:")
    for key in DIFFICULTY_VALUES:
        count = diff.get(key, 0)
        pct = diff_pct.get(key, 0.0)
        _h(f"  {key:<14} {count:>4}  ({pct:.1%})")
    _h("")

    # Route distribution
    route_dist = summary.get("route_distribution", {})
    if route_dist:
        _h("Route distribution:")
        for route, count in sorted(route_dist.items()):
            _h(f"  {route:<30} {count:>4}")
        _h("")

    # Top review topics
    top_topics = summary.get("top_review_topics", [])[:top_n]
    _h(f"Top review topics (top {top_n}):")
    if top_topics:
        for i, item in enumerate(top_topics, 1):
            _h(f"  {i:>2}. {item['value']}  (×{item['count']}, {item['frequency']:.1%})")
    else:
        _h("  (none recorded)")
    _h("")

    # Top misconceptions
    top_mc = summary.get("top_misconceptions", [])[:top_n]
    _h(f"Top misconceptions (top {top_n}):")
    if top_mc:
        for i, item in enumerate(top_mc, 1):
            _h(f"  {i:>2}. {item['value']}  (×{item['count']}, {item['frequency']:.1%})")
    else:
        _h("  (none recorded)")
    _h("")

    # Top causal chains
    top_cc = summary.get("top_causal_chains", [])[:top_n]
    _h(f"Top causal chains (top {top_n}):")
    if top_cc:
        for i, item in enumerate(top_cc, 1):
            _h(f"  {i:>2}. {item['value']}  (×{item['count']}, {item['frequency']:.1%})")
    else:
        _h("  (none recorded)")
    _h("")

    _h("=" * 52)
    return "\n".join(lines)


def _cli(argv: list[str] | None = None) -> int:
    """CLI entry point for ledger summary inspection.

    Returns exit code (0 = success, 1 = error).
    Read-only: never writes to any file.
    """
    parser = argparse.ArgumentParser(
        prog="python -m tools.orchestrator.ledger_summary",
        description=(
            "Inspect the WSET-AI-System session cognitive ledger. "
            "Read-only — never modifies the ledger, LES, or session staging."
        ),
    )
    parser.add_argument(
        "--ledger",
        type=Path,
        default=DEFAULT_LEDGER_PATH,
        metavar="PATH",
        help=f"Path to session_ledger.json (default: {DEFAULT_LEDGER_PATH})",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        dest="json_output",
        help="Output raw summary as JSON instead of formatted report.",
    )
    parser.add_argument(
        "--top-n",
        type=int,
        default=TOP_N,
        metavar="N",
        dest="top_n",
        help=f"Maximum items in each ranked list (default: {TOP_N}).",
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Explicit formatted output (default when --json is not set).",
    )

    args = parser.parse_args(argv)

    try:
        ledger = load_ledger_file(args.ledger)
    except FileNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        print(
            "Tip: Run at least one tutoring session first to populate the ledger.",
            file=sys.stderr,
        )
        return 1
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    summary = summarize_ledger(ledger)

    if args.json_output:
        print(json.dumps(summary, indent=2, ensure_ascii=True))
    else:
        print(format_report(summary, top_n=args.top_n))

    return 0


if __name__ == "__main__":
    sys.exit(_cli())
