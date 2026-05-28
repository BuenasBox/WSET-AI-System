"""Phase 1C: strategic plan persistence tests.

Verifies that session_staging.json receives a top-level "strategic_plan" key
that is an exact, unmodified copy of the planner output — and that the
persisted plan is never consumed as a planner input (no feedback loop).

All tests use temp directories and inline fixtures. No real LES or corpus.
"""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tools.orchestrator.orchestrator import run_orchestrator

# ---------------------------------------------------------------------------
# Expected plan keys (Phase 1A contract)
# ---------------------------------------------------------------------------

EXPECTED_PLAN_KEYS: frozenset[str] = frozenset({
    "recommended_next_topics",
    "review_topics",
    "avoid_topics",
    "misconception_focus",
    "causal_chain_focus",
    "sat_drill_needed",
    "difficulty_progression",
    "planning_confidence",
    "plan_generated_at",
    "cold_start",
})

GOVERNANCE_KEYS: frozenset[str] = frozenset({
    "safe_for_examiner",
    "examiner_scoring_allowed",
    "examiner_scoring_active",
})

# ---------------------------------------------------------------------------
# Fixtures
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


def _run(
    query: str,
    tmp: Path,
    known_weak_areas: list[str] | None = None,
) -> dict:
    staging_path = tmp / "session_staging.json"
    run_orchestrator(
        query,
        les_path=_write_les(tmp / "epistemic_state.json", known_weak_areas),
        misconception_dir=_write_misconception_fixture(tmp / "misconceptions"),
        staging_path=staging_path,
        context_package_dir=tmp / "context_packages",
        root=tmp,
    )
    return json.loads(staging_path.read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# Test 1: strategic_plan is written to session staging
# ---------------------------------------------------------------------------


class PlanWrittenToStagingTests(unittest.TestCase):

    def test_strategic_plan_key_present_at_top_level(self):
        """Required test 1: staging file has a top-level 'strategic_plan' key."""
        with tempfile.TemporaryDirectory() as tmp:
            staging = _run("How do I justify quality in SAT?", Path(tmp))
        self.assertIn("strategic_plan", staging)

    def test_strategic_plan_is_dict(self):
        with tempfile.TemporaryDirectory() as tmp:
            staging = _run("How do I justify quality in SAT?", Path(tmp))
        self.assertIsInstance(staging["strategic_plan"], dict)

    def test_strategic_plan_survives_json_round_trip(self):
        """Plan must survive JSON serialization without type loss."""
        with tempfile.TemporaryDirectory() as tmp:
            staging = _run("How do I justify quality in SAT?", Path(tmp))
        plan = staging["strategic_plan"]
        # Re-serialize and deserialize to confirm round-trip stability
        plan_rt = json.loads(json.dumps(plan))
        self.assertEqual(plan, plan_rt)


# ---------------------------------------------------------------------------
# Test 2: persisted plan matches planner output exactly
# ---------------------------------------------------------------------------


class PersistenceExactnessTests(unittest.TestCase):

    def test_persisted_plan_matches_orchestrator_result_plan(self):
        """Required test 2: staging["strategic_plan"] == result["strategic_plan"]."""
        with tempfile.TemporaryDirectory() as tmp:
            staging_path = Path(tmp) / "session_staging.json"
            result = run_orchestrator(
                "How do I justify quality in SAT?",
                les_path=_write_les(Path(tmp) / "epistemic_state.json"),
                misconception_dir=_write_misconception_fixture(Path(tmp) / "misconceptions"),
                staging_path=Path(staging_path),
                context_package_dir=Path(tmp) / "context_packages",
                root=Path(tmp),
            )
            staging = json.loads(Path(staging_path).read_text(encoding="utf-8"))
        self.assertEqual(result["strategic_plan"], staging["strategic_plan"])

    def test_persisted_plan_matches_nested_plan_in_latest_session(self):
        """Plan at top level equals plan nested inside latest_session."""
        with tempfile.TemporaryDirectory() as tmp:
            staging = _run("How do I justify quality in SAT?", Path(tmp))
        top_level = staging["strategic_plan"]
        nested = staging["latest_session"]["strategic_plan"]
        self.assertEqual(top_level, nested)

    def test_persisted_plan_has_all_required_keys(self):
        with tempfile.TemporaryDirectory() as tmp:
            staging = _run("How do I justify quality in SAT?", Path(tmp))
        self.assertEqual(set(staging["strategic_plan"].keys()), EXPECTED_PLAN_KEYS)


# ---------------------------------------------------------------------------
# Test 3: cold-start plan persists correctly
# ---------------------------------------------------------------------------


class ColdStartPersistenceTests(unittest.TestCase):

    def test_cold_start_plan_persisted(self):
        """Required test 3: cold-start plan (empty LES) is persisted correctly."""
        with tempfile.TemporaryDirectory() as tmp:
            staging = _run("How do I justify quality in SAT?", Path(tmp))
        plan = staging["strategic_plan"]
        self.assertTrue(plan["cold_start"])
        self.assertEqual(plan["planning_confidence"], 0.0)
        self.assertEqual(plan["review_topics"], [])

    def test_cold_start_plan_schema_correct(self):
        with tempfile.TemporaryDirectory() as tmp:
            staging = _run("How do I justify quality in SAT?", Path(tmp))
        self.assertEqual(set(staging["strategic_plan"].keys()), EXPECTED_PLAN_KEYS)


# ---------------------------------------------------------------------------
# Test 4: LES warm-state plan persists correctly
# ---------------------------------------------------------------------------


class WarmStatePersistenceTests(unittest.TestCase):

    def test_warm_les_plan_persisted_with_review_topics(self):
        """Required test 4: warm LES plan (known_weak_areas) persists non-empty topics."""
        weak_areas = ["causal_chain:malo_lactic", "fragile:acidity_quality"]
        with tempfile.TemporaryDirectory() as tmp:
            staging = _run(
                "How do I justify quality in SAT?",
                Path(tmp),
                known_weak_areas=weak_areas,
            )
        plan = staging["strategic_plan"]
        self.assertFalse(plan["cold_start"])
        self.assertIn("malo_lactic", plan["review_topics"])
        self.assertIn("acidity_quality", plan["review_topics"])

    def test_warm_les_plan_has_positive_confidence(self):
        weak_areas = ["causal_chain:malo_lactic"]
        with tempfile.TemporaryDirectory() as tmp:
            staging = _run(
                "How do I justify quality in SAT?",
                Path(tmp),
                known_weak_areas=weak_areas,
            )
        self.assertGreater(staging["strategic_plan"]["planning_confidence"], 0.0)


# ---------------------------------------------------------------------------
# Test 5: persisted plan contains no governance fields
# ---------------------------------------------------------------------------


class GovernancePersistenceTests(unittest.TestCase):

    def test_no_governance_keys_in_persisted_plan(self):
        """Required test 5: persisted plan has no governance fields."""
        with tempfile.TemporaryDirectory() as tmp:
            staging = _run("How do I justify quality in SAT?", Path(tmp))
        plan = staging["strategic_plan"]
        for key in GOVERNANCE_KEYS:
            self.assertNotIn(
                key, plan,
                msg=f"Governance key '{key}' must not appear in persisted strategic_plan",
            )

    def test_persisted_plan_keys_exactly_match_contract(self):
        """No extra keys (including governance leakage) in persisted plan."""
        with tempfile.TemporaryDirectory() as tmp:
            staging = _run("How do I justify quality in SAT?", Path(tmp))
        self.assertEqual(set(staging["strategic_plan"].keys()), EXPECTED_PLAN_KEYS)

    def test_staging_governance_block_unchanged(self):
        """Persisting strategic_plan must not alter the top-level governance block."""
        with tempfile.TemporaryDirectory() as tmp:
            staging = _run("How do I justify quality in SAT?", Path(tmp))
        self.assertFalse(staging["governance"]["safe_for_examiner"])


# ---------------------------------------------------------------------------
# Test 6: planner execution does not read persisted plan
# ---------------------------------------------------------------------------


class NoPlanReadBackTests(unittest.TestCase):

    def test_staging_file_pre_populated_does_not_influence_planner(self):
        """Required test 6: a pre-existing staging file does not affect planner output.

        We write a staging file with a fabricated strategic_plan before running
        the orchestrator, then confirm the planner produces a fresh plan from
        LES signals only — not from the pre-existing staging data.
        """
        with tempfile.TemporaryDirectory() as tmp:
            staging_path = Path(tmp) / "session_staging.json"
            # Pre-populate staging with a fabricated plan
            fabricated_plan = {
                "recommended_next_topics": ["FABRICATED_TOPIC"],
                "review_topics": ["FABRICATED_REVIEW"],
                "avoid_topics": ["FABRICATED_AVOID"],
                "misconception_focus": ["FABRICATED_MC"],
                "causal_chain_focus": ["FABRICATED_CHAIN"],
                "sat_drill_needed": True,
                "difficulty_progression": "escalate",
                "planning_confidence": 0.99,
                "plan_generated_at": "2000-01-01T00:00:00+00:00",
                "cold_start": False,
            }
            staging_path.write_text(
                json.dumps({
                    "schema_version": "minimal_brain_v2",
                    "strategic_plan": fabricated_plan,
                    "latest_session": {},
                    "governance": {"safe_for_examiner": False},
                }),
                encoding="utf-8",
            )
            # Run orchestrator with empty LES → should cold-start regardless
            result = run_orchestrator(
                "How do I justify quality in SAT?",
                les_path=_write_les(Path(tmp) / "epistemic_state.json"),
                misconception_dir=_write_misconception_fixture(Path(tmp) / "misconceptions"),
                staging_path=staging_path,
                context_package_dir=Path(tmp) / "context_packages",
                root=Path(tmp),
            )

        # The planner must cold-start from the empty LES, ignoring the fabricated plan
        plan = result["strategic_plan"]
        self.assertTrue(plan["cold_start"], "Planner must cold-start with empty LES")
        self.assertNotIn("FABRICATED_TOPIC", plan["recommended_next_topics"])
        self.assertNotIn("FABRICATED_REVIEW", plan["review_topics"])
        self.assertNotEqual(plan["planning_confidence"], 0.99)

    def test_staging_schema_has_no_planner_input_field(self):
        """Staging schema must not have a 'previous_strategic_plan' input field."""
        with tempfile.TemporaryDirectory() as tmp:
            staging = _run("How do I justify quality in SAT?", Path(tmp))
        self.assertNotIn("previous_strategic_plan", staging)
        self.assertNotIn("planner_input", staging)


# ---------------------------------------------------------------------------
# Test 7: re-running planner with same inputs produces same output regardless
#         of persisted plan contents
# ---------------------------------------------------------------------------


class DeterminismWithPersistenceTests(unittest.TestCase):

    def test_same_les_same_plan_regardless_of_prior_staging(self):
        """Required test 7: planner is deterministic even when staging differs.

        Run the orchestrator twice with identical LES. Between runs the staging
        file from run 1 exists with a different plan content. Run 2 must produce
        the same plan as run 1, proving the planner does not read staging.
        """
        query = "How do I justify quality in SAT?"
        weak_areas = ["causal_chain:malo_lactic", "fragile:acidity_quality"]

        with tempfile.TemporaryDirectory() as tmp1:
            # Run 1: produces a plan and writes it to staging
            result1 = run_orchestrator(
                query,
                les_path=_write_les(Path(tmp1) / "epistemic_state.json", weak_areas),
                misconception_dir=_write_misconception_fixture(Path(tmp1) / "misconceptions"),
                staging_path=Path(tmp1) / "session_staging.json",
                context_package_dir=Path(tmp1) / "context_packages",
                root=Path(tmp1),
            )

        with tempfile.TemporaryDirectory() as tmp2:
            # Run 2: staging pre-populated with DIFFERENT data from run 1
            staging_path_2 = Path(tmp2) / "session_staging.json"
            # Write a staging file with fabricated contents to simulate "prior session"
            staging_path_2.write_text(
                json.dumps({
                    "schema_version": "minimal_brain_v2",
                    "strategic_plan": {"cold_start": True, "planning_confidence": 0.0,
                                       "review_topics": [], "avoid_topics": [],
                                       "recommended_next_topics": [], "misconception_focus": [],
                                       "causal_chain_focus": [], "sat_drill_needed": False,
                                       "difficulty_progression": "stable",
                                       "plan_generated_at": "1970-01-01T00:00:00+00:00"},
                    "latest_session": {},
                    "governance": {"safe_for_examiner": False},
                }),
                encoding="utf-8",
            )
            result2 = run_orchestrator(
                query,
                les_path=_write_les(Path(tmp2) / "epistemic_state.json", weak_areas),
                misconception_dir=_write_misconception_fixture(Path(tmp2) / "misconceptions"),
                staging_path=staging_path_2,
                context_package_dir=Path(tmp2) / "context_packages",
                root=Path(tmp2),
            )

        plan1 = {k: v for k, v in result1["strategic_plan"].items() if k != "plan_generated_at"}
        plan2 = {k: v for k, v in result2["strategic_plan"].items() if k != "plan_generated_at"}
        self.assertEqual(
            plan1, plan2,
            msg="Planner must produce identical output regardless of staging file contents",
        )

    def test_plan_generated_at_is_fresh_not_from_staging(self):
        """plan_generated_at must be a fresh timestamp, not copied from staging."""
        with tempfile.TemporaryDirectory() as tmp:
            staging_path = Path(tmp) / "session_staging.json"
            # Pre-populate with an old timestamp
            staging_path.write_text(
                json.dumps({
                    "schema_version": "minimal_brain_v2",
                    "strategic_plan": {"plan_generated_at": "2000-01-01T00:00:00+00:00",
                                       "cold_start": True, "planning_confidence": 0.0,
                                       "review_topics": [], "avoid_topics": [],
                                       "recommended_next_topics": [], "misconception_focus": [],
                                       "causal_chain_focus": [], "sat_drill_needed": False,
                                       "difficulty_progression": "stable"},
                    "latest_session": {},
                    "governance": {"safe_for_examiner": False},
                }),
                encoding="utf-8",
            )
            result = run_orchestrator(
                "How do I justify quality in SAT?",
                les_path=_write_les(Path(tmp) / "epistemic_state.json"),
                misconception_dir=_write_misconception_fixture(Path(tmp) / "misconceptions"),
                staging_path=staging_path,
                context_package_dir=Path(tmp) / "context_packages",
                root=Path(tmp),
            )
        # Fresh timestamp must differ from the old fabricated one
        self.assertNotEqual(
            result["strategic_plan"]["plan_generated_at"],
            "2000-01-01T00:00:00+00:00",
        )


if __name__ == "__main__":
    unittest.main()
