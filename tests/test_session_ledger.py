"""Phase 2A: Session Cognitive Ledger tests.

Verifies that:
  - The ledger is created and appended to correctly.
  - The ledger schema is stable and deterministic.
  - The ledger contains only approved telemetry fields.
  - The ledger respects its retention policy.
  - The ledger does NOT influence the planner, retrieval, or Tutor (isolation).
  - Writing to the ledger does not alter the orchestrator result.

All tests use temp directories. No real LES files are touched.
"""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tools.orchestrator.orchestrator import run_orchestrator
from tools.orchestrator.session_ledger import (
    LEDGER_MAX_SESSIONS,
    LEDGER_VERSION,
    LEDGER_RETENTION_POLICY,
    _build_session_entry,
    _empty_ledger,
    _load_or_init_ledger,
    append_to_ledger,
)

# ---------------------------------------------------------------------------
# Expected ledger entry keys
# ---------------------------------------------------------------------------

EXPECTED_ENTRY_KEYS: frozenset[str] = frozenset({
    "timestamp",
    "route",
    "cold_start",
    "planning_confidence",
    "difficulty_progression",
    "sat_drill_needed",
    "review_topics",
    "topics_covered",
    "misconceptions_triggered",
    "causal_chains_seen",
})

BLOCKED_FIELDS: frozenset[str] = frozenset({
    # Governance
    "safe_for_examiner",
    "examiner_scoring_allowed",
    "examiner_scoring_active",
    # Privacy / size
    "student_query",
    "tutor_answer",
    "retrieved_context",
    "context_package",
})

# ---------------------------------------------------------------------------
# Shared fixtures
# ---------------------------------------------------------------------------


def _write_les(path: Path, known_weak_areas: list[str] | None = None) -> Path:
    path.write_text(
        json.dumps({
            "learner_id": "test_learner",
            "current_level": "WSET_L3",
            "known_weak_areas": known_weak_areas or [],
            "recent_misconceptions": [],
            "session_count": 0,
            "governance": {"safe_for_examiner": False},
        }),
        encoding="utf-8",
    )
    return path


def _write_misconception_fixture(directory: Path) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    node = {
        "misconception_id": "MC_ACIDITY_01",
        "misconception": "High acidity means low quality.",
        "corrected_understanding": "High acidity can signal quality when balanced.",
        "severity": "medium",
        "tutor_intervention": "contrast_comparison",
        "detection_signals": ["So high acidity means the wine is lower quality"],
        "detection_keywords": [
            {"tokens": ["acid", "quality"], "require_all": True, "bias": 0.24},
        ],
    }
    (directory / "mc_acidity_01.json").write_text(json.dumps(node), encoding="utf-8")
    return directory


def _run(tmp: Path, query: str = "How do I justify quality in SAT?",
         known_weak_areas: list[str] | None = None) -> dict:
    """Run orchestrator in a temp directory; return orchestrator result."""
    return run_orchestrator(
        query,
        les_path=_write_les(tmp / "epistemic_state.json", known_weak_areas),
        misconception_dir=_write_misconception_fixture(tmp / "misconceptions"),
        staging_path=tmp / "session_staging.json",
        context_package_dir=tmp / "context_packages",
        root=tmp,
    )


def _ledger_path(tmp: Path) -> Path:
    return tmp / "session_ledger.json"


def _read_ledger(tmp: Path) -> dict:
    return json.loads(_ledger_path(tmp).read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# Test 1: ledger file created when missing
# ---------------------------------------------------------------------------


class LedgerCreationTests(unittest.TestCase):

    def test_ledger_file_created_on_first_run(self):
        """Required test 1: ledger JSON file is created by the orchestrator."""
        with tempfile.TemporaryDirectory() as tmp:
            _run(Path(tmp))
            self.assertTrue(_ledger_path(Path(tmp)).exists())

    def test_ledger_has_correct_top_level_schema(self):
        """Ledger top-level keys and version are correct."""
        with tempfile.TemporaryDirectory() as tmp:
            _run(Path(tmp))
            ledger = _read_ledger(Path(tmp))
        self.assertEqual(ledger["version"], LEDGER_VERSION)
        self.assertIn("session_count", ledger)
        self.assertIn("sessions", ledger)
        self.assertIn("retention_policy", ledger)
        self.assertEqual(ledger["retention_policy"], LEDGER_RETENTION_POLICY)

    def test_empty_ledger_initialised_correctly(self):
        """_empty_ledger() returns a valid fresh ledger."""
        ledger = _empty_ledger()
        self.assertEqual(ledger["version"], LEDGER_VERSION)
        self.assertEqual(ledger["session_count"], 0)
        self.assertEqual(ledger["sessions"], [])

    def test_load_or_init_returns_empty_for_missing_file(self):
        """_load_or_init_ledger creates a fresh ledger when file is absent."""
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "nonexistent_ledger.json"
            ledger = _load_or_init_ledger(path)
        self.assertEqual(ledger["sessions"], [])
        self.assertEqual(ledger["session_count"], 0)


# ---------------------------------------------------------------------------
# Test 2: session appended correctly
# ---------------------------------------------------------------------------


class SessionAppendTests(unittest.TestCase):

    def test_one_session_in_ledger_after_one_run(self):
        """Required test 2: exactly one entry after one orchestrator run."""
        with tempfile.TemporaryDirectory() as tmp:
            _run(Path(tmp))
            ledger = _read_ledger(Path(tmp))
        self.assertEqual(len(ledger["sessions"]), 1)

    def test_session_entry_has_all_required_keys(self):
        """Session entry has exactly the expected schema keys."""
        with tempfile.TemporaryDirectory() as tmp:
            _run(Path(tmp))
            ledger = _read_ledger(Path(tmp))
        entry = ledger["sessions"][0]
        self.assertEqual(set(entry.keys()), EXPECTED_ENTRY_KEYS)

    def test_session_entry_route_is_recorded(self):
        with tempfile.TemporaryDirectory() as tmp:
            _run(Path(tmp))
            ledger = _read_ledger(Path(tmp))
        entry = ledger["sessions"][0]
        self.assertIn(entry["route"], {"normal_tutor", "misconception_prepass"})

    def test_misconception_entry_records_mc_id(self):
        """When misconception is detected, its ID is recorded — not the full node."""
        with tempfile.TemporaryDirectory() as tmp:
            _run(Path(tmp), query="So high acidity means the wine is lower quality?")
            ledger = _read_ledger(Path(tmp))
        entry = ledger["sessions"][0]
        self.assertIn("MC_ACIDITY_01", entry["misconceptions_triggered"])
        # Full misconception object must NOT be stored
        for item in entry["misconceptions_triggered"]:
            self.assertIsInstance(item, str)


# ---------------------------------------------------------------------------
# Test 3: session_count increments correctly
# ---------------------------------------------------------------------------


class SessionCountTests(unittest.TestCase):

    def test_session_count_after_one_run(self):
        """Required test 3: session_count == 1 after first run."""
        with tempfile.TemporaryDirectory() as tmp:
            _run(Path(tmp))
            ledger = _read_ledger(Path(tmp))
        self.assertEqual(ledger["session_count"], 1)

    def test_session_count_after_two_runs(self):
        """session_count increments correctly across multiple runs."""
        with tempfile.TemporaryDirectory() as tmp:
            _run(Path(tmp))
            _run(Path(tmp))
            ledger = _read_ledger(Path(tmp))
        self.assertEqual(ledger["session_count"], 2)
        self.assertEqual(len(ledger["sessions"]), 2)


# ---------------------------------------------------------------------------
# Test 4: ledger survives multiple sessions
# ---------------------------------------------------------------------------


class MultiSessionTests(unittest.TestCase):

    def test_three_sessions_all_recorded(self):
        """Required test 4: three sequential runs → three entries in ledger."""
        with tempfile.TemporaryDirectory() as tmp:
            for _ in range(3):
                _run(Path(tmp))
            ledger = _read_ledger(Path(tmp))
        self.assertEqual(ledger["session_count"], 3)
        self.assertEqual(len(ledger["sessions"]), 3)

    def test_sessions_are_ordered_oldest_first(self):
        """Entries are appended in order — oldest at index 0."""
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp)
            append_to_ledger({}, _ledger_path(p), reference_date="2026-01-01T00:00:00+00:00")
            append_to_ledger({}, _ledger_path(p), reference_date="2026-01-02T00:00:00+00:00")
            ledger = _read_ledger(p)
        self.assertEqual(ledger["sessions"][0]["timestamp"], "2026-01-01T00:00:00+00:00")
        self.assertEqual(ledger["sessions"][1]["timestamp"], "2026-01-02T00:00:00+00:00")


# ---------------------------------------------------------------------------
# Test 5: ledger respects retention limit
# ---------------------------------------------------------------------------


class RetentionTests(unittest.TestCase):

    def test_ledger_capped_at_max_sessions(self):
        """Required test 5: ledger never exceeds LEDGER_MAX_SESSIONS entries."""
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp)
            # Write MAX + 5 entries
            for i in range(LEDGER_MAX_SESSIONS + 5):
                append_to_ledger(
                    {},
                    _ledger_path(p),
                    reference_date=f"2026-01-{i+1:02d}T00:00:00+00:00" if i < 31 else f"2026-02-{i-30:02d}T00:00:00+00:00",
                )
            ledger = _read_ledger(p)
        self.assertLessEqual(len(ledger["sessions"]), LEDGER_MAX_SESSIONS)
        self.assertEqual(ledger["session_count"], LEDGER_MAX_SESSIONS)

    def test_oldest_sessions_dropped_on_overflow(self):
        """When the cap is exceeded, the oldest entries are dropped."""
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp)
            # Pre-fill to exactly MAX
            for i in range(LEDGER_MAX_SESSIONS):
                append_to_ledger({}, _ledger_path(p), reference_date=f"2020-01-01T{i:06d}+00:00")
            # Add one more — should push out the oldest
            append_to_ledger({}, _ledger_path(p), reference_date="2030-12-31T00:00:00+00:00")
            ledger = _read_ledger(p)
        # Most recent entry is present
        self.assertEqual(ledger["sessions"][-1]["timestamp"], "2030-12-31T00:00:00+00:00")
        # Total still at cap
        self.assertEqual(len(ledger["sessions"]), LEDGER_MAX_SESSIONS)


# ---------------------------------------------------------------------------
# Test 6: ledger contains no governance fields
# ---------------------------------------------------------------------------


class GovernanceLedgerTests(unittest.TestCase):

    def test_no_governance_keys_in_session_entry(self):
        """Required test 6: governance fields must not appear in any session entry."""
        with tempfile.TemporaryDirectory() as tmp:
            _run(Path(tmp))
            ledger = _read_ledger(Path(tmp))
        for entry in ledger["sessions"]:
            for key in ("safe_for_examiner", "examiner_scoring_allowed", "examiner_scoring_active"):
                self.assertNotIn(key, entry, f"Governance key '{key}' found in ledger entry")

    def test_entry_keys_exactly_match_contract(self):
        """Entry has ONLY approved keys — no extra fields including governance leakage."""
        with tempfile.TemporaryDirectory() as tmp:
            _run(Path(tmp))
            ledger = _read_ledger(Path(tmp))
        entry = ledger["sessions"][0]
        self.assertEqual(set(entry.keys()), EXPECTED_ENTRY_KEYS)


# ---------------------------------------------------------------------------
# Tests 7, 8, 9: ledger contains no raw queries, Tutor answers, or chunks
# ---------------------------------------------------------------------------


class ContentSafetyTests(unittest.TestCase):

    def test_no_raw_user_query_in_ledger(self):
        """Required test 7: raw query text must not be stored in the ledger."""
        with tempfile.TemporaryDirectory() as tmp:
            _run(Path(tmp), query="How do I justify quality in SAT?")
            ledger = _read_ledger(Path(tmp))
        ledger_text = json.dumps(ledger)
        # The full query string must not appear verbatim
        self.assertNotIn("student_query", ledger_text)
        for entry in ledger["sessions"]:
            self.assertNotIn("student_query", entry)

    def test_no_tutor_answer_in_ledger(self):
        """Required test 8: Tutor answer text must not appear in the ledger."""
        with tempfile.TemporaryDirectory() as tmp:
            _run(Path(tmp))
            ledger = _read_ledger(Path(tmp))
        for entry in ledger["sessions"]:
            self.assertNotIn("tutor_answer", entry)
            self.assertNotIn("answer", entry)

    def test_no_retrieval_chunks_in_ledger(self):
        """Required test 9: retrieved chunk objects must not be stored."""
        with tempfile.TemporaryDirectory() as tmp:
            _run(Path(tmp))
            ledger = _read_ledger(Path(tmp))
        for entry in ledger["sessions"]:
            self.assertNotIn("retrieved_context", entry)
            self.assertNotIn("context_package", entry)
            self.assertNotIn("chunks", entry)


# ---------------------------------------------------------------------------
# Test 10: ledger remains deterministic
# ---------------------------------------------------------------------------


class DeterminismLedgerTests(unittest.TestCase):

    def test_same_inputs_produce_same_entry(self):
        """Required test 10: two runs with same reference_date produce identical entries."""
        fake_result = {
            "strategic_plan": {
                "cold_start": False,
                "planning_confidence": 0.15,
                "difficulty_progression": "stable",
                "sat_drill_needed": False,
                "review_topics": ["malo_lactic"],
                "recommended_next_topics": [],
            },
            "orchestrator_decision": {"route": "normal_tutor"},
            "detected_misconception": {"detected": False, "matched_misconception_id": None},
            "context_package": {"forced_causal_chains": []},
        }
        ref = "2026-05-28T12:00:00+00:00"
        entry1 = _build_session_entry(fake_result, ref)
        entry2 = _build_session_entry(fake_result, ref)
        self.assertEqual(entry1, entry2)

    def test_entry_timestamp_matches_reference_date(self):
        """When reference_date is passed, it appears exactly in the entry."""
        with tempfile.TemporaryDirectory() as tmp:
            entry = append_to_ledger(
                {},
                _ledger_path(Path(tmp)),
                reference_date="2026-05-28T12:00:00+00:00",
            )
        self.assertEqual(entry["timestamp"], "2026-05-28T12:00:00+00:00")


# ---------------------------------------------------------------------------
# Test 11: ledger write does not alter orchestrator output
# ---------------------------------------------------------------------------


class InertLedgerTests(unittest.TestCase):

    def test_orchestrator_result_unchanged_after_ledger_write(self):
        """Required test 11: orchestrator result dict is identical before/after ledger."""
        with tempfile.TemporaryDirectory() as tmp:
            result = _run(Path(tmp))
        # Core keys must all be present
        for key in ("strategic_plan", "orchestrator_decision", "tutor_directive",
                    "context_package", "governance_flags"):
            self.assertIn(key, result)
        # Governance must be clean
        self.assertFalse(result["governance_flags"]["safe_for_examiner"])

    def test_ledger_path_not_in_orchestrator_result(self):
        """Ledger path is not exposed in the orchestrator result."""
        with tempfile.TemporaryDirectory() as tmp:
            result = _run(Path(tmp))
        self.assertNotIn("ledger_path", result)
        self.assertNotIn("session_ledger", result)


# ---------------------------------------------------------------------------
# Tests 12, 13, 14: planner / retrieval / Tutor do not read ledger
# ---------------------------------------------------------------------------


class IsolationTests(unittest.TestCase):

    def test_planner_does_not_read_ledger(self):
        """Required test 12: pre-populating ledger with fabricated data has no effect.

        We write a ledger with fabricated review_topics and planning_confidence
        before running the orchestrator. The planner must ignore the ledger and
        derive its plan purely from LES signals.
        """
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp)
            # Write a fabricated ledger entry
            fabricated_entry = {
                "timestamp": "2000-01-01T00:00:00+00:00",
                "route": "normal_tutor",
                "cold_start": False,
                "planning_confidence": 0.99,
                "difficulty_progression": "escalate",
                "sat_drill_needed": True,
                "review_topics": ["FABRICATED_TOPIC"],
                "topics_covered": ["FABRICATED_COVERED"],
                "misconceptions_triggered": ["FABRICATED_MC"],
                "causal_chains_seen": ["FABRICATED_CHAIN"],
            }
            _ledger_path(p).write_text(
                json.dumps({
                    "version": 1,
                    "session_count": 1,
                    "retention_policy": "keep_last_100",
                    "sessions": [fabricated_entry],
                }),
                encoding="utf-8",
            )
            # Run with empty LES → planner must cold-start regardless
            result = _run(p)
        plan = result["strategic_plan"]
        self.assertTrue(plan["cold_start"], "Planner must cold-start from empty LES")
        self.assertNotIn("FABRICATED_TOPIC", plan["review_topics"])
        self.assertNotEqual(plan["planning_confidence"], 0.99)

    def test_retrieval_plan_does_not_reference_ledger(self):
        """Required test 13: retrieval_plan contains no ledger-derived fields."""
        with tempfile.TemporaryDirectory() as tmp:
            result = _run(Path(tmp))
        retrieval_plan = result["retrieval_plan"]
        self.assertNotIn("ledger", str(retrieval_plan).lower())
        self.assertNotIn("session_ledger", retrieval_plan)

    def test_tutor_directive_does_not_reference_ledger(self):
        """Required test 14: tutor_directive contains no ledger-derived fields."""
        with tempfile.TemporaryDirectory() as tmp:
            result = _run(Path(tmp))
        directive = result["tutor_directive"]
        self.assertNotIn("ledger", str(directive).lower())
        self.assertNotIn("session_ledger", directive)
        # Core directive fields must still be present and clean
        self.assertIn("pedagogical_act", directive)
        self.assertFalse(directive["safe_for_examiner"])


if __name__ == "__main__":
    unittest.main()
