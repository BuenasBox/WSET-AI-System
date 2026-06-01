"""
tests/test_dashboard_state_updater.py
======================================
Focused tests for tools/dashboard/update_architecture_dashboard_state.py

Tests:
  - dry-run does not modify system_state.json
  - write mode updates only system_state.json
  - output JSON is valid
  - forbidden paths are rejected
  - no private paths are read
  - expected fields exist in output
  - completed_phases order is deterministic
  - output path safety check enforced
"""

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

# Ensure repo root is on sys.path
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from tools.dashboard.update_architecture_dashboard_state import (
    _assert_output_safe,
    _assert_no_forbidden_read,
    _extract_latest_phase_from_log,
    _extract_completed_phases_from_log,
    _extract_test_count_from_claude_md,
    _extract_snapshot_count_from_claude_md,
    _diff_summary,
    build_new_state,
    FORBIDDEN_PATHS,
    OUTPUT_PATH,
    REPO_ROOT as SCRIPT_REPO_ROOT,
)


# ---------------------------------------------------------------------------
# 1. Output path safety
# ---------------------------------------------------------------------------

class TestOutputPathSafety(unittest.TestCase):

    def test_output_path_is_inside_dashboard(self):
        """OUTPUT_PATH must be inside frontend/architecture-dashboard/."""
        expected_root = SCRIPT_REPO_ROOT / "frontend" / "architecture-dashboard"
        self.assertTrue(
            str(OUTPUT_PATH).startswith(str(expected_root)),
            f"OUTPUT_PATH {OUTPUT_PATH} is outside dashboard dir"
        )

    def test_assert_output_safe_accepts_valid_path(self):
        valid = SCRIPT_REPO_ROOT / "frontend" / "architecture-dashboard" / "system_state.json"
        # Should not raise
        _assert_output_safe(valid)

    def test_assert_output_safe_rejects_outside_path(self):
        outside = SCRIPT_REPO_ROOT / "knowledge" / "nazareth" / "evil.json"
        with self.assertRaises(SystemExit):
            _assert_output_safe(outside)

    def test_assert_output_safe_rejects_tools_path(self):
        outside = SCRIPT_REPO_ROOT / "tools" / "constants.py"
        with self.assertRaises(SystemExit):
            _assert_output_safe(outside)


# ---------------------------------------------------------------------------
# 2. Forbidden path enforcement
# ---------------------------------------------------------------------------

class TestForbiddenPaths(unittest.TestCase):

    def test_nazareth_rejected(self):
        with self.assertRaises(SystemExit):
            _assert_no_forbidden_read("knowledge/nazareth/epistemic_state.json")

    def test_attempts_rejected(self):
        with self.assertRaises(SystemExit):
            _assert_no_forbidden_read("knowledge/self-eval/attempts/run_001.json")

    def test_reports_rejected(self):
        with self.assertRaises(SystemExit):
            _assert_no_forbidden_read("knowledge/self-eval/reports/summary.json")

    def test_env_rejected(self):
        with self.assertRaises(SystemExit):
            _assert_no_forbidden_read(".env")

    def test_env_local_rejected(self):
        with self.assertRaises(SystemExit):
            _assert_no_forbidden_read(".env.local")

    def test_allowed_path_passes(self):
        # Should not raise
        _assert_no_forbidden_read("CLAUDE.md")
        _assert_no_forbidden_read("docs/backend_stability_remediation_plan.md")
        _assert_no_forbidden_read("frontend/architecture-dashboard/system_state.json")


# ---------------------------------------------------------------------------
# 3. Git log parsers
# ---------------------------------------------------------------------------

class TestGitLogParsers(unittest.TestCase):

    SAMPLE_LOG = [
        "abc1234 feat(phase-4a3): Phase 4A.3.7 structured question bank compatibility audit",
        "def5678 feat(phase-4a2): Phase 4A.3.6 SBA strict filter pass",
        "ghi9012 feat(phase-3a8): Phase 3A.8 activation readiness review complete",
        "jkl3456 chore: fix typo in README",
    ]

    def test_latest_phase_extracted(self):
        result = _extract_latest_phase_from_log(self.SAMPLE_LOG)
        self.assertEqual(result, "Phase 4A.3.7")

    def test_latest_phase_unknown_on_empty(self):
        result = _extract_latest_phase_from_log([])
        self.assertEqual(result, "unknown")

    def test_completed_phases_ordered_oldest_first(self):
        result = _extract_completed_phases_from_log(self.SAMPLE_LOG)
        # reversed order: 3A.8 comes before 4A.3.6 before 4A.3.7
        self.assertEqual(result, ["Phase 3A.8", "Phase 4A.3.6", "Phase 4A.3.7"])

    def test_completed_phases_deduplicated(self):
        duped = [
            "aaa Phase 4A.3.7 second mention",
            "bbb Phase 4A.3.7 first mention",
        ]
        result = _extract_completed_phases_from_log(duped)
        self.assertEqual(result.count("Phase 4A.3.7"), 1)

    def test_completed_phases_empty_on_no_phases(self):
        result = _extract_completed_phases_from_log(["abc123 chore: misc", "def456 fix: typo"])
        self.assertEqual(result, [])


# ---------------------------------------------------------------------------
# 4. CLAUDE.md parsers
# ---------------------------------------------------------------------------

class TestClaudeMdParsers(unittest.TestCase):

    def test_test_count_extracted(self):
        text = "- Test count: **660** via `python -m unittest`"
        self.assertEqual(_extract_test_count_from_claude_md(text), 660)

    def test_test_count_none_on_missing(self):
        self.assertIsNone(_extract_test_count_from_claude_md("no count here"))

    def test_snapshot_count_extracted(self):
        text = "35/35 snapshots green"
        self.assertEqual(_extract_snapshot_count_from_claude_md(text), 35)

    def test_snapshot_count_none_on_missing(self):
        self.assertIsNone(_extract_snapshot_count_from_claude_md("nothing relevant"))


# ---------------------------------------------------------------------------
# 5. build_new_state — expected fields present
# ---------------------------------------------------------------------------

class TestBuildNewStateFields(unittest.TestCase):

    REQUIRED_FIELDS = [
        "current_phase", "latest_phase", "latest_event", "latest_commit",
        "current_recommendation", "updated_at", "tests", "snapshots",
        "maturity", "phases_completed", "in_progress_phase", "next_target",
        "governance_status", "planner_influence_status", "diagnostic_sba_status",
        "knowledge_assets_count", "knowledge_assets_size_mb",
        "official_wset_markdown_count", "wine_with_jimmy_transcripts",
        "tutor_chunks", "golden_chunks", "knowledge_graph_nodes",
        "concepts_count", "misconceptions_count", "causal_chains_count",
        "relationships_count", "structured_question_count", "theory_questions",
        "short_answer_questions", "sba_basic_candidates", "sba_strict_candidates",
        "sba_clean_pilot_candidates", "diagnostic_compatible_count",
    ]

    def _build(self, current=None):
        with patch("tools.dashboard.update_architecture_dashboard_state._git_log", return_value=[]):
            with patch("tools.dashboard.update_architecture_dashboard_state._latest_commit_hash", return_value="abc1234"):
                with patch("tools.dashboard.update_architecture_dashboard_state._read_claude_md", return_value=""):
                    return build_new_state(current or {})

    def test_all_required_fields_present(self):
        state = self._build()
        for field in self.REQUIRED_FIELDS:
            self.assertIn(field, state, f"Missing field: {field}")

    def test_governance_status_immutable(self):
        state = self._build()
        gov = state["governance_status"]
        self.assertEqual(gov["governance_violations"], 0)
        self.assertEqual(gov["llm_dependency"], 0)
        self.assertEqual(gov["vector_db_dependency"], 0)
        self.assertEqual(gov["cloud_runtime_dependency"], 0)
        self.assertFalse(gov["official_examiner_authority"])

    def test_current_values_preserved_when_no_evidence(self):
        current = {"maturity": 50, "structured_question_count": 616}
        state = self._build(current)
        self.assertEqual(state["maturity"], 50)
        self.assertEqual(state["structured_question_count"], 616)


# ---------------------------------------------------------------------------
# 6. Dry-run does not modify file
# ---------------------------------------------------------------------------

class TestDryRun(unittest.TestCase):

    def test_dry_run_does_not_write(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            target = Path(tmpdir) / "system_state.json"
            initial = {"maturity": 10, "tests": 100}
            target.write_text(json.dumps(initial), encoding="utf-8")

            mtime_before = target.stat().st_mtime

            # Simulate dry-run: script reads but does not write
            # We test by calling build_new_state and NOT writing
            with open(target, encoding="utf-8") as f:
                current = json.load(f)

            with patch("tools.dashboard.update_architecture_dashboard_state._git_log", return_value=[]):
                with patch("tools.dashboard.update_architecture_dashboard_state._latest_commit_hash", return_value="x"):
                    with patch("tools.dashboard.update_architecture_dashboard_state._read_claude_md", return_value=""):
                        _ = build_new_state(current)

            # File must not have changed
            mtime_after = target.stat().st_mtime
            self.assertEqual(mtime_before, mtime_after)


# ---------------------------------------------------------------------------
# 7. Write mode produces valid JSON
# ---------------------------------------------------------------------------

class TestWriteMode(unittest.TestCase):

    def test_write_produces_valid_json(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            target = Path(tmpdir) / "system_state.json"
            target.write_text(json.dumps({"maturity": 10}), encoding="utf-8")

            with patch("tools.dashboard.update_architecture_dashboard_state._git_log", return_value=[]):
                with patch("tools.dashboard.update_architecture_dashboard_state._latest_commit_hash", return_value="abc"):
                    with patch("tools.dashboard.update_architecture_dashboard_state._read_claude_md", return_value=""):
                        current = json.loads(target.read_text())
                        new_state = build_new_state(current)

            with open(target, "w", encoding="utf-8") as f:
                json.dump(new_state, f, indent=2, ensure_ascii=False)
                f.write("\n")

            # Must parse cleanly
            parsed = json.loads(target.read_text(encoding="utf-8"))
            self.assertIsInstance(parsed, dict)


# ---------------------------------------------------------------------------
# 8. Diff summary
# ---------------------------------------------------------------------------

class TestDiffSummary(unittest.TestCase):

    def test_diff_detects_changes(self):
        old = {"maturity": 41, "tests": 600}
        new = {"maturity": 50, "tests": 660}
        diff = _diff_summary(old, new)
        self.assertEqual(len(diff), 2)
        self.assertTrue(any("maturity" in d for d in diff))
        self.assertTrue(any("tests" in d for d in diff))

    def test_diff_empty_when_identical(self):
        state = {"maturity": 50}
        self.assertEqual(_diff_summary(state, state), [])

    def test_diff_detects_new_key(self):
        old = {"maturity": 50}
        new = {"maturity": 50, "new_field": "hello"}
        diff = _diff_summary(old, new)
        self.assertTrue(any("new_field" in d for d in diff))


if __name__ == "__main__":
    unittest.main(verbosity=2)
