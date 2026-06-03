"""
tools/dashboard/update_architecture_dashboard_state.py
=======================================================
Local dashboard state updater for WSET-AI-System.

Reads only from:
  - git log --oneline
  - CLAUDE.md
  - docs/
  - frontend/architecture-dashboard/system_state.json

Writes only to:
  - frontend/architecture-dashboard/system_state.json

Never reads: knowledge/nazareth/, session artifacts, LES files, .env, secrets.
Never calls: external APIs, network, cloud services.
Never commits or deploys automatically.

Usage:
  python tools/dashboard/update_architecture_dashboard_state.py --dry-run
  python tools/dashboard/update_architecture_dashboard_state.py --write
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
OUTPUT_PATH = REPO_ROOT / "frontend" / "architecture-dashboard" / "system_state.json"

FORBIDDEN_PATHS = [
    "knowledge/nazareth",
    "knowledge/self-eval/attempts",
    "knowledge/self-eval/reports",
    "knowledge/retrieval-sandbox",
    ".env",
    ".env.local",
    ".env.production",
]

ALLOWED_READ_PATHS = [
    "CLAUDE.md",
    "docs/",
    "frontend/architecture-dashboard/system_state.json",
]


def _assert_output_safe(path: Path) -> None:
    """Refuse to write outside the dashboard directory."""
    expected = REPO_ROOT / "frontend" / "architecture-dashboard"
    try:
        path.resolve().relative_to(expected.resolve())
    except ValueError:
        sys.exit(
            f"[SAFETY] Refusing to write outside dashboard directory.\n"
            f"  Output path: {path}\n"
            f"  Allowed root: {expected}"
        )


def _assert_no_forbidden_read(path: str) -> None:
    for forbidden in FORBIDDEN_PATHS:
        if forbidden in path.replace("\\", "/"):
            sys.exit(f"[SAFETY] Refusing to read forbidden path: {path}")


# ---------------------------------------------------------------------------
# Git helpers
# ---------------------------------------------------------------------------

def _git_log(n: int = 20) -> list[str]:
    try:
        result = subprocess.run(
            ["git", "log", f"--oneline", f"-{n}"],
            capture_output=True, text=True, cwd=REPO_ROOT
        )
        return result.stdout.strip().splitlines()
    except Exception:
        return []


def _latest_commit_hash() -> str:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            capture_output=True, text=True, cwd=REPO_ROOT
        )
        return result.stdout.strip()
    except Exception:
        return "unknown"


def _extract_latest_phase_from_log(log_lines: list[str]) -> str:
    """
    Parse phase tags from git log messages.
    Looks for patterns like Phase 4A, Phase 3A.5, Phase 4A.3.7, etc.
    """
    for line in log_lines:
        phase = _extract_phase_from_line(line)
        if phase:
            return phase
    return "unknown"


def _extract_completed_phases_from_log(log_lines: list[str]) -> list[str]:
    """
    Build an ordered list of unique phase tags from git log (oldest → newest
    is reversed since git log is newest-first).
    """
    seen = []
    seen_set = set()
    for line in reversed(log_lines):
        tag = _extract_phase_from_line(line)
        if tag:
            if tag not in seen_set:
                seen.append(tag)
                seen_set.add(tag)
    return seen


def _extract_phase_from_line(line: str) -> str | None:
    """Normalize human-readable and conventional phase commit tags."""
    import re

    readable = re.search(
        r"Phase\s+[\dA-Za-z]+(?:\.[\dA-Za-z]+)*",
        line,
        re.IGNORECASE,
    )
    if readable:
        return readable.group(0)

    conventional = re.search(
        r"phase-(\d+[A-Za-z])(\d+(?:\.\d+)*)",
        line,
        re.IGNORECASE,
    )
    if conventional:
        family = conventional.group(1).upper()
        suffix = conventional.group(2)
        return f"Phase {family}.{suffix}"

    return None


# ---------------------------------------------------------------------------
# CLAUDE.md helpers
# ---------------------------------------------------------------------------

def _read_claude_md() -> str:
    path = REPO_ROOT / "CLAUDE.md"
    _assert_no_forbidden_read(str(path))
    if path.exists():
        return path.read_text(encoding="utf-8")
    return ""


def _extract_test_count_from_claude_md(text: str) -> int | None:
    import re
    m = re.search(r"Test count[:\s*]*\*?\*?(\d+)", text)
    if m:
        return int(m.group(1))
    # fallback: look for standalone "660" near "tests"
    m = re.search(r"(\d{3,4})\s+(?:passing|tests?)", text)
    if m:
        return int(m.group(1))
    return None


def _extract_snapshot_count_from_claude_md(text: str) -> int | None:
    import re
    m = re.search(r"(\d+)\s*/\s*\d+\s+snapshots?", text, re.IGNORECASE)
    if m:
        return int(m.group(1))
    m = re.search(r"Snapshots?[:\s]+(\d+)", text)
    if m:
        return int(m.group(1))
    return None


# ---------------------------------------------------------------------------
# State builder
# ---------------------------------------------------------------------------

def build_new_state(current: dict) -> dict:
    """
    Build the updated state dict from repo evidence.
    Falls back to current values when evidence is unavailable.
    """
    log_lines = _git_log(50)
    latest_commit = _latest_commit_hash()
    latest_phase_from_log = _extract_latest_phase_from_log(log_lines)
    completed_phases_from_log = _extract_completed_phases_from_log(log_lines)

    claude_md = _read_claude_md()
    test_count_from_md = _extract_test_count_from_claude_md(claude_md)
    snapshot_count_from_md = _extract_snapshot_count_from_claude_md(claude_md)

    # Determine latest_phase: prefer git log evidence, fallback to current
    latest_phase = (
        latest_phase_from_log
        if latest_phase_from_log != "unknown"
        else current.get("latest_phase", "unknown")
    )

    # Test / snapshot counts
    tests = max(test_count_from_md or 0, current.get("tests", 0))
    snapshots = snapshot_count_from_md or current.get("snapshots", 35)

    # Completed phases: merge log evidence with existing list
    existing_completed = current.get("phases_completed", [])
    merged = list(existing_completed)
    represented_phase_tags = {
        phase
        for item in existing_completed
        if (phase := _extract_phase_from_line(item))
    }
    for p in completed_phases_from_log:
        if p not in represented_phase_tags:
            merged.append(p)
            represented_phase_tags.add(p)

    # Latest event: derive from most recent git commit message
    latest_event = current.get("latest_event", "")
    if log_lines:
        # strip hash prefix
        parts = log_lines[0].split(" ", 1)
        if len(parts) == 2:
            latest_event = parts[1]

    # Preserve status fields added by later dashboard phases unless this
    # updater explicitly owns and replaces them.
    new_state = dict(current)
    new_state.update({
        # Core phase info
        "current_phase": current.get("current_phase", latest_phase),
        "latest_phase": latest_phase,
        "latest_event": latest_event,
        "latest_commit": latest_commit,
        "current_recommendation": current.get("current_recommendation", ""),
        "updated_at": datetime.now(timezone.utc).isoformat(),

        # Test metrics
        "tests": tests,
        "snapshots": snapshots,
        "maturity": current.get("maturity", 50),

        # Phases
        "phases_completed": merged,
        "in_progress_phase": current.get("in_progress_phase", ""),
        "next_target": current.get("next_target", ""),

        # Governance
        "governance_status": current.get("governance_status", {
            "governance_violations": 0,
            "llm_dependency": 0,
            "vector_db_dependency": 0,
            "cloud_runtime_dependency": 0,
            "official_examiner_authority": False,
            "snapshot_regressions_green": snapshots
        }),

        # Planner / SBA gates
        "planner_influence_status": current.get("planner_influence_status", "gated"),
        "diagnostic_sba_status": current.get("diagnostic_sba_status", "pending"),

        # Knowledge assets
        "knowledge_assets_count": current.get("knowledge_assets_count", 0),
        "knowledge_assets_size_mb": current.get("knowledge_assets_size_mb", 0),
        "official_wset_markdown_count": current.get("official_wset_markdown_count", 0),
        "wine_with_jimmy_transcripts": current.get("wine_with_jimmy_transcripts", 0),
        "tutor_chunks": current.get("tutor_chunks", 0),
        "golden_chunks": current.get("golden_chunks", 0),

        # Knowledge graph
        "knowledge_graph_nodes": current.get("knowledge_graph_nodes", 0),
        "concepts_count": current.get("concepts_count", 0),
        "misconceptions_count": current.get("misconceptions_count", 0),
        "causal_chains_count": current.get("causal_chains_count", 0),
        "relationships_count": current.get("relationships_count", 0),

        # Question bank
        "structured_question_count": current.get("structured_question_count", 0),
        "theory_questions": current.get("theory_questions", 0),
        "short_answer_questions": current.get("short_answer_questions", 0),
        "sba_basic_candidates": current.get("sba_basic_candidates", 0),
        "sba_strict_candidates": current.get("sba_strict_candidates", 0),
        "sba_clean_pilot_candidates": current.get("sba_clean_pilot_candidates", 0),
        "diagnostic_compatible_count": current.get("diagnostic_compatible_count", 0),
    })

    return new_state


# ---------------------------------------------------------------------------
# Diff summary
# ---------------------------------------------------------------------------

def _diff_summary(old: dict, new: dict) -> list[str]:
    lines = []
    all_keys = sorted(set(old) | set(new))
    for k in all_keys:
        ov = old.get(k)
        nv = new.get(k)
        if ov != nv:
            lines.append(f"  {k}: {ov!r} -> {nv!r}")
    return lines


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Update frontend/architecture-dashboard/system_state.json from repo evidence."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--dry-run", action="store_true", help="Show what would change; do not write.")
    group.add_argument("--write", action="store_true", help="Write updated state to system_state.json.")
    args = parser.parse_args()

    # Safety check before anything
    _assert_output_safe(OUTPUT_PATH)

    # Load current state
    if OUTPUT_PATH.exists():
        with open(OUTPUT_PATH, encoding="utf-8") as f:
            current = json.load(f)
    else:
        current = {}

    new_state = build_new_state(current)

    diff = _diff_summary(current, new_state)

    if not diff:
        print("[dashboard-updater] No changes detected.")
        return

    print(f"[dashboard-updater] {'DRY RUN — ' if args.dry_run else ''}Changes:")
    for line in diff:
        print(line)

    if args.write:
        with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
            json.dump(new_state, f, indent=2, ensure_ascii=False)
            f.write("\n")
        print(f"\n[dashboard-updater] Written → {OUTPUT_PATH.relative_to(REPO_ROOT)}")
    else:
        print("\n[dashboard-updater] Dry run complete. Use --write to apply.")


if __name__ == "__main__":
    main()
