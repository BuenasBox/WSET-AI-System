"""Phase 2C: Ledger Summary CLI tests.

Verifies that the CLI entry point (python -m tools.orchestrator.ledger_summary)
is read-only, deterministic, governance-clean, and robust to error conditions.

Tests call _cli() / format_report() / load_ledger_file() directly rather than
via subprocess, keeping them fast and deterministic without external processes.
"""

from __future__ import annotations

import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.orchestrator.ledger_summary import (
    TOP_N,
    _cli,
    format_report,
    load_ledger_file,
    summarize_ledger,
)

# ---------------------------------------------------------------------------
# Governance / grading fields that must never appear in output
# ---------------------------------------------------------------------------

GOVERNANCE_FIELDS: frozenset[str] = frozenset({
    "safe_for_examiner",
    "examiner_scoring_allowed",
    "examiner_scoring_active",
})

GRADING_FIELDS: frozenset[str] = frozenset({
    "student_grade",
    "student_score",
    "exam_readiness",
    "predicted_pass_probability",
    "pass_rate",
})

# ---------------------------------------------------------------------------
# Fixture helpers
# ---------------------------------------------------------------------------


def _make_ledger(sessions: list[dict] | None = None) -> dict:
    sessions = sessions or []
    return {
        "version": 1,
        "session_count": len(sessions),
        "retention_policy": "keep_last_100",
        "sessions": sessions,
    }


def _make_session(
    route: str = "normal_tutor",
    cold_start: bool = True,
    planning_confidence: float = 0.3,
    difficulty_progression: str = "stable",
    sat_drill_needed: bool = False,
    review_topics: list[str] | None = None,
    misconceptions_triggered: list[str] | None = None,
    causal_chains_seen: list[str] | None = None,
) -> dict:
    return {
        "timestamp": "2026-01-01T00:00:00+00:00",
        "route": route,
        "cold_start": cold_start,
        "planning_confidence": planning_confidence,
        "difficulty_progression": difficulty_progression,
        "sat_drill_needed": sat_drill_needed,
        "review_topics": review_topics or [],
        "misconceptions_triggered": misconceptions_triggered or [],
        "causal_chains_seen": causal_chains_seen or [],
        "topics_covered": [],
    }


def _write_ledger(path: Path, ledger: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(ledger, indent=2), encoding="utf-8")


def _run_cli(*args: str) -> tuple[int, str, str]:
    """Run _cli() with captured stdout/stderr. Returns (exit_code, stdout, stderr)."""
    stdout_buf = io.StringIO()
    stderr_buf = io.StringIO()
    with patch("sys.stdout", stdout_buf), patch("sys.stderr", stderr_buf):
        code = _cli(list(args))
    return code, stdout_buf.getvalue(), stderr_buf.getvalue()


# ---------------------------------------------------------------------------
# Test 1: CLI loads ledger
# ---------------------------------------------------------------------------


class CliLoadTests(unittest.TestCase):

    def test_cli_loads_existing_ledger_and_exits_zero(self):
        """Required test 1: CLI loads a valid ledger and exits with code 0."""
        ledger = _make_ledger([_make_session()])
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "ledger.json"
            _write_ledger(path, ledger)
            code, stdout, _ = _run_cli("--ledger", str(path))
        self.assertEqual(code, 0)
        self.assertTrue(len(stdout) > 0)

    def test_load_ledger_file_returns_dict(self):
        """load_ledger_file() returns the ledger as a dict."""
        ledger = _make_ledger([_make_session()])
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "ledger.json"
            _write_ledger(path, ledger)
            result = load_ledger_file(path)
        self.assertIsInstance(result, dict)
        self.assertIn("sessions", result)

    def test_load_ledger_file_is_read_only(self):
        """load_ledger_file() does not modify the file on disk."""
        ledger = _make_ledger([_make_session()])
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "ledger.json"
            _write_ledger(path, ledger)
            mtime_before = path.stat().st_mtime
            load_ledger_file(path)
            mtime_after = path.stat().st_mtime
        self.assertEqual(mtime_before, mtime_after)


# ---------------------------------------------------------------------------
# Test 2: CLI prints summary
# ---------------------------------------------------------------------------


class CliPrintTests(unittest.TestCase):

    def test_cli_prints_session_count(self):
        """Required test 2: CLI output contains session count."""
        ledger = _make_ledger([_make_session(), _make_session()])
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "ledger.json"
            _write_ledger(path, ledger)
            _, stdout, _ = _run_cli("--ledger", str(path))
        self.assertIn("2", stdout)

    def test_cli_output_contains_key_sections(self):
        """CLI formatted output contains expected section headers."""
        ledger = _make_ledger([_make_session(review_topics=["acidity"])])
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "ledger.json"
            _write_ledger(path, ledger)
            _, stdout, _ = _run_cli("--ledger", str(path))
        self.assertIn("Sessions analysed", stdout)
        self.assertIn("Difficulty", stdout)
        self.assertIn("review topics", stdout.lower())

    def test_cli_output_contains_review_topics(self):
        """Review topics from the ledger appear in the CLI output."""
        ledger = _make_ledger([_make_session(review_topics=["malo_lactic", "acidity"])])
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "ledger.json"
            _write_ledger(path, ledger)
            _, stdout, _ = _run_cli("--ledger", str(path))
        self.assertIn("malo_lactic", stdout)
        self.assertIn("acidity", stdout)


# ---------------------------------------------------------------------------
# Test 3: CLI handles missing file
# ---------------------------------------------------------------------------


class CliMissingFileTests(unittest.TestCase):

    def test_cli_exits_nonzero_for_missing_file(self):
        """Required test 3: missing ledger → exit code 1."""
        code, _, stderr = _run_cli("--ledger", "/nonexistent/path/ledger.json")
        self.assertEqual(code, 1)
        self.assertTrue(len(stderr) > 0)

    def test_cli_missing_file_error_message(self):
        """Error message mentions the missing file."""
        code, _, stderr = _run_cli("--ledger", "/nonexistent/path/ledger.json")
        self.assertEqual(code, 1)
        self.assertIn("not found", stderr.lower())

    def test_load_ledger_file_raises_for_missing(self):
        """load_ledger_file() raises FileNotFoundError for absent path."""
        with self.assertRaises(FileNotFoundError):
            load_ledger_file(Path("/nonexistent/ledger.json"))


# ---------------------------------------------------------------------------
# Test 4: CLI handles malformed JSON
# ---------------------------------------------------------------------------


class CliMalformedJsonTests(unittest.TestCase):

    def test_cli_exits_nonzero_for_invalid_json(self):
        """Required test 4: malformed JSON → exit code 1."""
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "ledger.json"
            path.write_text("{ not valid json !!!", encoding="utf-8")
            code, _, stderr = _run_cli("--ledger", str(path))
        self.assertEqual(code, 1)
        self.assertTrue(len(stderr) > 0)

    def test_load_ledger_file_raises_for_invalid_json(self):
        """load_ledger_file() raises ValueError for invalid JSON."""
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "ledger.json"
            path.write_text("not json", encoding="utf-8")
            with self.assertRaises(ValueError):
                load_ledger_file(path)

    def test_cli_empty_json_object_exits_zero(self):
        """Empty JSON object {} is valid input — exits 0 with empty summary."""
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "ledger.json"
            path.write_text("{}", encoding="utf-8")
            code, stdout, _ = _run_cli("--ledger", str(path))
        self.assertEqual(code, 0)
        self.assertIn("0", stdout)  # sessions_analysed: 0


# ---------------------------------------------------------------------------
# Test 5: CLI deterministic output
# ---------------------------------------------------------------------------


class CliDeterminismTests(unittest.TestCase):

    def test_same_ledger_produces_same_output(self):
        """Required test 5: identical ledger → identical CLI output."""
        sessions = [
            _make_session(review_topics=["A", "B"], planning_confidence=0.4),
            _make_session(review_topics=["A"], sat_drill_needed=True),
        ]
        ledger = _make_ledger(sessions)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "ledger.json"
            _write_ledger(path, ledger)
            _, out1, _ = _run_cli("--ledger", str(path))
            _, out2, _ = _run_cli("--ledger", str(path))
        self.assertEqual(out1, out2)

    def test_format_report_is_deterministic(self):
        """format_report() produces identical output for identical input."""
        summary = summarize_ledger(_make_ledger([_make_session(review_topics=["X"])]))
        r1 = format_report(summary)
        r2 = format_report(summary)
        self.assertEqual(r1, r2)


# ---------------------------------------------------------------------------
# Test 6: CLI json mode works
# ---------------------------------------------------------------------------


class CliJsonModeTests(unittest.TestCase):

    def test_json_flag_produces_valid_json(self):
        """Required test 6: --json flag outputs parseable JSON."""
        ledger = _make_ledger([_make_session(review_topics=["acidity"])])
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "ledger.json"
            _write_ledger(path, ledger)
            code, stdout, _ = _run_cli("--ledger", str(path), "--json")
        self.assertEqual(code, 0)
        parsed = json.loads(stdout)
        self.assertIsInstance(parsed, dict)
        self.assertIn("session_count", parsed)

    def test_json_output_contains_top_review_topics(self):
        """JSON output preserves top_review_topics field."""
        ledger = _make_ledger([_make_session(review_topics=["malo_lactic"])])
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "ledger.json"
            _write_ledger(path, ledger)
            _, stdout, _ = _run_cli("--ledger", str(path), "--json")
        parsed = json.loads(stdout)
        topics = [item["value"] for item in parsed.get("top_review_topics", [])]
        self.assertIn("malo_lactic", topics)

    def test_top_n_flag_limits_display(self):
        """--top-n 2 limits each ranked list to 2 items in formatted output."""
        topics = [f"topic_{i}" for i in range(10)]
        ledger = _make_ledger([_make_session(review_topics=topics)])
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "ledger.json"
            _write_ledger(path, ledger)
            _, stdout, _ = _run_cli("--ledger", str(path), "--top-n", "2")
        # In formatted output, numbered items use "  1." and "  2."
        self.assertIn("  1.", stdout)
        self.assertIn("  2.", stdout)
        self.assertNotIn("  3.", stdout)


# ---------------------------------------------------------------------------
# Test 7: CLI does not modify ledger
# ---------------------------------------------------------------------------


class CliReadOnlyLedgerTests(unittest.TestCase):

    def test_cli_does_not_modify_ledger_file(self):
        """Required test 7: ledger file is byte-for-byte unchanged after CLI run."""
        ledger = _make_ledger([_make_session(review_topics=["acidity"])])
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "ledger.json"
            _write_ledger(path, ledger)
            content_before = path.read_bytes()
            _run_cli("--ledger", str(path))
            content_after = path.read_bytes()
        self.assertEqual(content_before, content_after)

    def test_cli_does_not_create_extra_files(self):
        """CLI run does not create files other than what already exists."""
        ledger = _make_ledger([_make_session()])
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "ledger.json"
            _write_ledger(path, ledger)
            files_before = set(Path(tmp).iterdir())
            _run_cli("--ledger", str(path))
            files_after = set(Path(tmp).iterdir())
        self.assertEqual(files_before, files_after)


# ---------------------------------------------------------------------------
# Test 8: CLI does not modify LES
# ---------------------------------------------------------------------------


class CliReadOnlyLesTests(unittest.TestCase):

    def test_cli_does_not_write_les(self):
        """Required test 8: LES file (epistemic_state.json) is not modified."""
        with tempfile.TemporaryDirectory() as tmp:
            les_path = Path(tmp) / "epistemic_state.json"
            les_content = json.dumps({
                "learner_id": "test",
                "known_weak_areas": [],
                "governance": {"safe_for_examiner": False},
            })
            les_path.write_text(les_content, encoding="utf-8")

            ledger_path = Path(tmp) / "ledger.json"
            _write_ledger(ledger_path, _make_ledger([_make_session()]))

            les_before = les_path.read_bytes()
            _run_cli("--ledger", str(ledger_path))
            les_after = les_path.read_bytes()

        self.assertEqual(les_before, les_after)

    def test_cli_does_not_create_les_if_absent(self):
        """CLI does not create epistemic_state.json when it does not exist."""
        with tempfile.TemporaryDirectory() as tmp:
            les_path = Path(tmp) / "epistemic_state.json"
            ledger_path = Path(tmp) / "ledger.json"
            _write_ledger(ledger_path, _make_ledger([_make_session()]))
            _run_cli("--ledger", str(ledger_path))
            self.assertFalse(les_path.exists())


# ---------------------------------------------------------------------------
# Test 9: CLI does not modify session staging
# ---------------------------------------------------------------------------


class CliReadOnlyStagingTests(unittest.TestCase):

    def test_cli_does_not_write_session_staging(self):
        """Required test 9: session_staging.json is not modified by CLI."""
        with tempfile.TemporaryDirectory() as tmp:
            staging_path = Path(tmp) / "session_staging.json"
            staging_content = json.dumps({
                "schema_version": "minimal_brain_v2",
                "governance": {"safe_for_examiner": False},
            })
            staging_path.write_text(staging_content, encoding="utf-8")

            ledger_path = Path(tmp) / "ledger.json"
            _write_ledger(ledger_path, _make_ledger([_make_session()]))

            staging_before = staging_path.read_bytes()
            _run_cli("--ledger", str(ledger_path))
            staging_after = staging_path.read_bytes()

        self.assertEqual(staging_before, staging_after)

    def test_cli_does_not_create_staging_if_absent(self):
        """CLI does not create session_staging.json when it does not exist."""
        with tempfile.TemporaryDirectory() as tmp:
            staging_path = Path(tmp) / "session_staging.json"
            ledger_path = Path(tmp) / "ledger.json"
            _write_ledger(ledger_path, _make_ledger([_make_session()]))
            _run_cli("--ledger", str(ledger_path))
            self.assertFalse(staging_path.exists())


# ---------------------------------------------------------------------------
# Test 10: CLI output contains no governance fields
# ---------------------------------------------------------------------------


class CliGovernanceTests(unittest.TestCase):

    def test_formatted_output_has_no_governance_strings(self):
        """Required test 10: formatted report does not contain governance field names."""
        ledger = _make_ledger([_make_session()])
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "ledger.json"
            _write_ledger(path, ledger)
            _, stdout, _ = _run_cli("--ledger", str(path))
        for field in GOVERNANCE_FIELDS:
            self.assertNotIn(field, stdout)

    def test_json_output_has_no_governance_fields(self):
        """JSON output does not contain governance keys."""
        ledger = _make_ledger([_make_session()])
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "ledger.json"
            _write_ledger(path, ledger)
            _, stdout, _ = _run_cli("--ledger", str(path), "--json")
        parsed = json.loads(stdout)
        for field in GOVERNANCE_FIELDS:
            self.assertNotIn(field, parsed)

    def test_json_output_has_no_grading_fields(self):
        """JSON output does not contain grading or scoring keys."""
        ledger = _make_ledger([_make_session()])
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "ledger.json"
            _write_ledger(path, ledger)
            _, stdout, _ = _run_cli("--ledger", str(path), "--json")
        parsed = json.loads(stdout)
        for field in GRADING_FIELDS:
            self.assertNotIn(field, parsed)

    def test_format_report_has_no_governance_strings(self):
        """format_report() output does not contain governance field names."""
        summary = summarize_ledger(_make_ledger([_make_session()]))
        report = format_report(summary)
        for field in GOVERNANCE_FIELDS:
            self.assertNotIn(field, report)


if __name__ == "__main__":
    unittest.main()
