"""
One-time generator for Tutor snapshot fixtures.

Usage:
    python tests/generate_tutor_snapshots.py

Run this manually after a DELIBERATE baseline update (e.g., intentional content
change to answer_builder.py). Do NOT run this during the test suite — it will
silently overwrite the golden baseline.

What it does:
1. Reads all 25 attempt directories under knowledge/self-eval/attempts/{1..25}/
2. Copies the frozen context package (tutor_context_package.json) to the fixture dir.
3. Copies the golden answer (tutor_attempt.md) as expected_answer.txt.
4. Writes question metadata to question.json (volatile paths stripped).
5. Writes manifest.json listing all generated snapshots.

After running, commit tests/fixtures/tutor_snapshots/ to version control.
"""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
ATTEMPTS_ROOT = REPO_ROOT / "knowledge" / "self-eval" / "attempts"
SNAPSHOTS_ROOT = Path(__file__).parent / "fixtures" / "tutor_snapshots"


def _attempt_dirs() -> list[Path]:
    """Return attempt dirs with numeric names, sorted numerically."""
    if not ATTEMPTS_ROOT.exists():
        return []
    return sorted(
        (d for d in ATTEMPTS_ROOT.iterdir() if d.is_dir() and d.name.isdigit()),
        key=lambda d: int(d.name),
    )


def _generate() -> int:
    SNAPSHOTS_ROOT.mkdir(parents=True, exist_ok=True)
    manifest: list[dict] = []
    skipped: list[str] = []

    dirs = _attempt_dirs()
    if not dirs:
        print(f"ERROR: No numeric attempt directories found under {ATTEMPTS_ROOT}", file=sys.stderr)
        return 1

    for attempt_dir in dirs:
        result_path = attempt_dir / "self_eval_result.json"
        context_path = attempt_dir / "tutor_context_package.json"
        answer_path = attempt_dir / "tutor_attempt.md"

        missing = [p.name for p in (result_path, context_path, answer_path) if not p.exists()]
        if missing:
            print(f"  SKIP  {attempt_dir.name}: missing {', '.join(missing)}")
            skipped.append(attempt_dir.name)
            continue

        result = json.loads(result_path.read_text(encoding="utf-8"))
        question_id = str(result.get("question_id", attempt_dir.name))

        snapshot_dir = SNAPSHOTS_ROOT / question_id
        snapshot_dir.mkdir(parents=True, exist_ok=True)

        # question.json — metadata only, volatile absolute paths stripped
        question_meta: dict = {
            "question_id": result.get("question_id", ""),
            "question_type": result.get("question_type", ""),
            "question_text": result.get("question_text", ""),
            "expected_topics": result.get("expected_topics", []),
            "expected_causal_links": result.get("expected_causal_links", []),
            "expected_keywords": result.get("expected_keywords", []),
            "expected_reasoning_type": result.get("expected_reasoning_type", ""),
            "difficulty": result.get("difficulty", ""),
            "safe_for_examiner": False,
        }
        (snapshot_dir / "question.json").write_text(
            json.dumps(question_meta, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

        # context_package.json — frozen input to build_tutor_answer()
        shutil.copyfile(context_path, snapshot_dir / "context_package.json")

        # expected_answer.txt — golden output
        shutil.copyfile(answer_path, snapshot_dir / "expected_answer.txt")

        manifest.append(
            {
                "question_id": question_id,
                "question_type": result.get("question_type", ""),
                "question_text": result.get("question_text", ""),
                "difficulty": result.get("difficulty", ""),
            }
        )
        print(f"  OK    {question_id}: {result.get('question_text', '')[:65]}")

    (SNAPSHOTS_ROOT / "manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print(f"\nGenerated {len(manifest)} snapshots → {SNAPSHOTS_ROOT}")
    if skipped:
        print(f"Skipped {len(skipped)}: {', '.join(skipped)}")
    return 0 if len(manifest) > 0 else 1


if __name__ == "__main__":
    sys.exit(_generate())
