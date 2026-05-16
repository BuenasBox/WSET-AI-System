"""LES Reconciler — wires self-eval feedback into the Learner Epistemic State.

This module closes the loop between the self-eval pipeline and the Orchestrator.
After each self-eval run, call reconcile_les_from_feedback() to propagate
identified weak areas, misconception gaps, and session counts into the canonical
LES that the Orchestrator reads at the start of every session.

Governance: this module never sets safe_for_examiner=True, never writes
Examiner scoring fields, and never connects to external services.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from tools.orchestrator.learner_state import (
    DEFAULT_LES_PATH,
    load_learner_state,
    _governance_false,
    _write_json,
)
from tools.youtube_transcription.config import PROJECT_ROOT


LES_SCHEMA_VERSION = "minimal_brain_v2"
DEFAULT_FEEDBACK_PATH = PROJECT_ROOT / "knowledge" / "nazareth" / "self_eval_feedback.json"
MAX_RECENT_MISCONCEPTIONS = 10
MAX_KNOWN_WEAK_AREAS = 30


def reconcile_les_from_feedback(
    feedback_path: Path = DEFAULT_FEEDBACK_PATH,
    les_path: Path = DEFAULT_LES_PATH,
    dry_run: bool = False,
) -> dict[str, Any]:
    """Read self-eval feedback and write results into the LES.

    Args:
        feedback_path: Path to self_eval_feedback.json produced by evaluation_reporter.
        les_path: Path to epistemic_state.json (canonical learner state).
        dry_run: If True, compute the update but do not write the file.

    Returns:
        A reconciliation report dict describing what changed.
    """
    if not feedback_path.exists():
        return {
            "status": "skipped",
            "reason": f"Feedback file not found: {feedback_path}",
            "les_path": les_path.as_posix(),
            "changes": {},
        }

    with feedback_path.open("r", encoding="utf-8") as fh:
        feedback = json.load(fh)

    if not isinstance(feedback, dict):
        return {
            "status": "error",
            "reason": "Feedback file is not a JSON object.",
            "changes": {},
        }

    current_les = load_learner_state(les_path)
    updated_les, changes = _apply_feedback(current_les, feedback)

    if not dry_run:
        _write_json(les_path, updated_les)

    return {
        "status": "dry_run" if dry_run else "written",
        "les_path": les_path.as_posix(),
        "feedback_path": feedback_path.as_posix(),
        "feedback_strictness": feedback.get("strictness", "unknown"),
        "changes": changes,
        "updated_les_snapshot": {
            "schema_version": updated_les["schema_version"],
            "session_count": updated_les["session_count"],
            "known_weak_areas": updated_les["known_weak_areas"],
            "recent_misconceptions": updated_les["recent_misconceptions"],
        },
    }


def _apply_feedback(les: dict[str, Any], feedback: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    """Compute the updated LES state and a diff of changes.

    Never modifies safe_for_examiner or any Examiner-related flag.
    """
    import copy
    updated = copy.deepcopy(les)
    changes: dict[str, Any] = {}

    # 1. Schema version alignment
    old_schema = updated.get("schema_version", "")
    if old_schema != LES_SCHEMA_VERSION:
        updated["schema_version"] = LES_SCHEMA_VERSION
        changes["schema_version"] = {"from": old_schema, "to": LES_SCHEMA_VERSION}

    # 2. Session count increment
    # Derive the number of questions attempted from the feedback
    questions_attempted = _infer_questions_attempted(feedback)
    old_count = int(updated.get("session_count", 0) or 0)
    updated["session_count"] = old_count + questions_attempted
    if questions_attempted > 0:
        changes["session_count"] = {"from": old_count, "to": updated["session_count"], "delta": questions_attempted}

    # 3. Weak area persistence from fragile concepts
    existing_weak = list(updated.get("known_weak_areas", []) or [])
    new_weak_areas = _extract_weak_areas(feedback)
    added_weak = []
    for area in new_weak_areas:
        if area and area not in existing_weak:
            existing_weak.append(area)
            added_weak.append(area)
    # Cap at MAX_KNOWN_WEAK_AREAS — keep most recent entries
    if len(existing_weak) > MAX_KNOWN_WEAK_AREAS:
        existing_weak = existing_weak[-MAX_KNOWN_WEAK_AREAS:]
    updated["known_weak_areas"] = existing_weak
    if added_weak:
        changes["known_weak_areas"] = {"added": added_weak, "total": len(existing_weak)}

    # 4. Misconception gap persistence
    existing_mc = list(updated.get("recent_misconceptions", []) or [])
    new_mc = _extract_misconception_gaps(feedback)
    added_mc = []
    for mc in new_mc:
        if mc and mc not in existing_mc:
            existing_mc.append(mc)
            added_mc.append(mc)
    # Cap at MAX_RECENT_MISCONCEPTIONS — keep most recent
    if len(existing_mc) > MAX_RECENT_MISCONCEPTIONS:
        existing_mc = existing_mc[-MAX_RECENT_MISCONCEPTIONS:]
    updated["recent_misconceptions"] = existing_mc
    if added_mc:
        changes["recent_misconceptions"] = {"added": added_mc, "total": len(existing_mc)}

    # 5. Governance — always enforce; never trust what came in from LES on disk
    updated["governance"] = _governance_false(updated.get("governance", {}))

    return updated, changes


def _infer_questions_attempted(feedback: dict[str, Any]) -> int:
    """Infer how many questions were attempted from the feedback payload."""
    # weakness_counters.failure_labels sums total label occurrences, not question count
    # Best proxy: len of retrieval_gap_question_ids + count from fragile_concepts
    # Fallback: look for a question_count field added by future versions
    if "questions_attempted" in feedback:
        try:
            return int(feedback["questions_attempted"])
        except (TypeError, ValueError):
            pass

    # Sum unique question IDs from retrieval gaps as a lower bound
    gap_ids = feedback.get("retrieval_gap_question_ids", [])
    if isinstance(gap_ids, list) and gap_ids:
        # This is a lower bound — use it only if nothing better is available
        # We'll return a fixed increment of 1 session if we can't determine more precisely
        pass

    # The evaluation_reporter does not currently write questions_attempted.
    # Until it does, increment by the number of retrieval-gap question IDs (floor 1).
    # When reconcile_les_from_feedback is called by the evaluation pipeline
    # it will pass questions_attempted explicitly.
    return max(1, len(gap_ids)) if gap_ids else 1


def _extract_weak_areas(feedback: dict[str, Any]) -> list[str]:
    """Extract weak area labels from feedback fragile_concepts and causal counters."""
    areas: list[str] = []
    weakness_counters = feedback.get("weakness_counters", {})

    # Causal chain gaps — each missing chain is a weak area
    for chain, count in (weakness_counters.get("causal_chains") or {}).items():
        if isinstance(count, (int, float)) and count >= 1:
            areas.append(f"causal_chain:{chain}")

    # Retrieval weaknesses
    for weakness, count in (weakness_counters.get("retrieval") or {}).items():
        if isinstance(count, (int, float)) and count >= 2:
            areas.append(f"retrieval:{weakness}")

    # High-severity failure labels
    for label, count in (weakness_counters.get("failure_labels") or {}).items():
        if isinstance(count, (int, float)) and count >= 3:
            areas.append(f"label:{label}")

    # Fragile concepts from structured feedback
    for item in feedback.get("fragile_concepts", []):
        if not isinstance(item, dict):
            continue
        concept = str(item.get("concept") or "").strip()
        severity = str(item.get("severity") or "")
        if concept and severity in {"high", "medium"}:
            key = f"fragile:{concept}"
            if key not in areas:
                areas.append(key)

    return areas


def _extract_misconception_gaps(feedback: dict[str, Any]) -> list[str]:
    """Extract misconception IDs from suggested_misconception_investigations."""
    gaps = []
    for mc in feedback.get("suggested_misconception_investigations", []):
        mc_str = str(mc).strip()
        if mc_str:
            gaps.append(mc_str)
    # Also pull from weakness_counters.misconceptions
    weakness_counters = feedback.get("weakness_counters", {})
    for mc, count in (weakness_counters.get("misconceptions") or {}).items():
        if isinstance(count, (int, float)) and count >= 1 and mc not in gaps:
            gaps.append(str(mc).strip())
    return gaps


# ---------------------------------------------------------------------------
# Standalone CLI
# ---------------------------------------------------------------------------

def _cli() -> None:
    parser = argparse.ArgumentParser(
        description="Reconcile self-eval feedback into the Learner Epistemic State."
    )
    parser.add_argument(
        "--feedback",
        type=Path,
        default=DEFAULT_FEEDBACK_PATH,
        help="Path to self_eval_feedback.json (default: knowledge/nazareth/self_eval_feedback.json)",
    )
    parser.add_argument(
        "--les",
        type=Path,
        default=DEFAULT_LES_PATH,
        help="Path to epistemic_state.json (default: knowledge/nazareth/epistemic_state.json)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Compute the update but do not write the LES file.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        dest="json_output",
        help="Output the reconciliation report as JSON.",
    )
    args = parser.parse_args()
    report = reconcile_les_from_feedback(
        feedback_path=args.feedback,
        les_path=args.les,
        dry_run=args.dry_run,
    )
    if args.json_output:
        print(json.dumps(report, indent=2, ensure_ascii=True))
    else:
        _print_report(report)


def _print_report(report: dict[str, Any]) -> None:
    status = report.get("status", "unknown")
    print(f"\n=== LES Reconciliation Report ===")
    print(f"Status:    {status}")
    if "reason" in report:
        print(f"Reason:    {report['reason']}")
    print(f"LES path:  {report.get('les_path', 'n/a')}")
    print(f"Feedback:  {report.get('feedback_path', 'n/a')} (strictness={report.get('feedback_strictness', '?')})")
    changes = report.get("changes", {})
    if not changes:
        print("Changes:   none")
    else:
        print("Changes:")
        for field, delta in changes.items():
            print(f"  {field}: {delta}")
    snapshot = report.get("updated_les_snapshot", {})
    if snapshot:
        print("\nUpdated LES snapshot:")
        print(f"  schema_version:        {snapshot.get('schema_version')}")
        print(f"  session_count:         {snapshot.get('session_count')}")
        print(f"  known_weak_areas:      {len(snapshot.get('known_weak_areas', []))} entries")
        print(f"  recent_misconceptions: {len(snapshot.get('recent_misconceptions', []))} entries")
    print()


if __name__ == "__main__":
    _cli()
