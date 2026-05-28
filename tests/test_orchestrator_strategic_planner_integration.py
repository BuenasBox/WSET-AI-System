"""Integration tests: strategic_planner wired into run_orchestrator() (Phase 1B).

These tests verify that:
  1. run_orchestrator() exposes strategic_plan in its result.
  2. The plan schema matches the Phase 1A contract exactly.
  3. Integration is inert: no existing orchestrator fields are altered.
  4. No governance fields leak into the plan.
  5. Output is deterministic across identical calls.
  6. The orchestrator is robust to both cold-start and warm-start LES states.

All tests use temp directories and inline fixtures — no real LES files,
no real retrieval corpus. The planner is side-effect-free so no cleanup needed.
"""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tools.orchestrator.orchestrator import run_orchestrator

# ---------------------------------------------------------------------------
# Expected plan keys from Phase 1A contract
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

VALID_DIFFICULTY_VALUES: frozenset[str] = frozenset({
    "stable", "consolidate", "escalate",
})

# ---------------------------------------------------------------------------
# Shared fixtures (mirrors test_minimal_brain_orchestrator.py helpers)
# ---------------------------------------------------------------------------


def _write_misconception_fixture(directory: Path) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    node = {
        "misconception_id": "MC_ACIDITY_01",
        "misconception": "High acidity in a wine means the wine is low quality.",
        "corrected_understanding": "High acidity can be a hallmark of quality when balanced.",
        "severity": "medium",
        "tutor_intervention": "contrast_comparison",
        "detection_signals": [
            "So high acidity means the wine is lower quality",
        ],
        "detection_keywords": [
            {"tokens": ["acid", "quality"], "require_all": True, "bias": 0.24},
            {"tokens": ["acidity", "lower"], "require_all": True, "bias": 0.20},
        ],
    }
    (directory / "mc_acidity_01.json").write_text(json.dumps(node), encoding="utf-8")
    return directory


def _write_les(path: Path, known_weak_areas: list[str] | None = None) -> Path:
    """Write a minimal LES file. Pass known_weak_areas to simulate warm LES."""
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


def _run(
    query: str,
    tmp: Path,
    *,
    known_weak_areas: list[str] | None = None,
    language: str = "es",
) -> dict:
    """Run orchestrator with temp fixtures and return result."""
    return run_orchestrator(
        query,
        language=language,
        les_path=_write_les(tmp / "epistemic_state.json", known_weak_areas),
        misconception_dir=_write_misconception_fixture(tmp / "misconceptions"),
        staging_path=tmp / "session_staging.json",
        context_package_dir=tmp / "context_packages",
        root=tmp,
    )


# ---------------------------------------------------------------------------
# Test 1: planner output exists in orchestrator result
# ---------------------------------------------------------------------------


class PlannerExistsInResultTests(unittest.TestCase):

    def test_strategic_plan_key_present_in_result(self):
        """Required test 1: orchestrator result contains 'strategic_plan'."""
        with tempfile.TemporaryDirectory() as tmp:
            result = _run("How do I justify quality in SAT?", Path(tmp))
        self.assertIn("strategic_plan", result)

    def test_strategic_plan_is_dict(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = _run("How do I justify quality in SAT?", Path(tmp))
        self.assertIsInstance(result["strategic_plan"], dict)

    def test_strategic_plan_present_on_misconception_route(self):
        """Planner appears even when the orchestrator routes to misconception_prepass."""
        with tempfile.TemporaryDirectory() as tmp:
            result = _run(
                "So high acidity means the wine is lower quality?",
                Path(tmp),
            )
        self.assertIn("strategic_plan", result)
        self.assertIsInstance(result["strategic_plan"], dict)


# ---------------------------------------------------------------------------
# Test 2: planner output schema is preserved
# ---------------------------------------------------------------------------


class PlannerSchemaTests(unittest.TestCase):

    def test_plan_has_all_required_keys(self):
        """Required test 2: plan schema matches Phase 1A contract exactly."""
        with tempfile.TemporaryDirectory() as tmp:
            result = _run("How do I justify quality in SAT?", Path(tmp))
        plan = result["strategic_plan"]
        self.assertEqual(set(plan.keys()), EXPECTED_PLAN_KEYS)

    def test_plan_value_types(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = _run("How do I justify quality in SAT?", Path(tmp))
        plan = result["strategic_plan"]
        self.assertIsInstance(plan["recommended_next_topics"], list)
        self.assertIsInstance(plan["review_topics"], list)
        self.assertIsInstance(plan["avoid_topics"], list)
        self.assertIsInstance(plan["misconception_focus"], list)
        self.assertIsInstance(plan["causal_chain_focus"], list)
        self.assertIsInstance(plan["sat_drill_needed"], bool)
        self.assertIsInstance(plan["difficulty_progression"], str)
        self.assertIsInstance(plan["planning_confidence"], float)
        self.assertIsInstance(plan["plan_generated_at"], str)
        self.assertIsInstance(plan["cold_start"], bool)

    def test_difficulty_progression_is_valid_value(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = _run("How do I justify quality in SAT?", Path(tmp))
        self.assertIn(
            result["strategic_plan"]["difficulty_progression"],
            VALID_DIFFICULTY_VALUES,
        )

    def test_planning_confidence_in_0_1_range(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = _run("How do I justify quality in SAT?", Path(tmp))
        confidence = result["strategic_plan"]["planning_confidence"]
        self.assertGreaterEqual(confidence, 0.0)
        self.assertLessEqual(confidence, 1.0)


# ---------------------------------------------------------------------------
# Test 3: orchestrator works when planner returns cold-start plan
# ---------------------------------------------------------------------------


class ColdStartIntegrationTests(unittest.TestCase):

    def test_orchestrator_survives_cold_start_planner(self):
        """Required test 3: orchestrator completes normally when planner cold-starts."""
        with tempfile.TemporaryDirectory() as tmp:
            # Empty LES → cold start
            result = _run("How do I justify quality in SAT?", Path(tmp))
        plan = result["strategic_plan"]
        self.assertTrue(plan["cold_start"])
        self.assertEqual(plan["planning_confidence"], 0.0)
        # Orchestrator core fields must still be present
        self.assertIn("orchestrator_decision", result)
        self.assertIn("tutor_directive", result)
        self.assertIn("context_package", result)

    def test_cold_start_plan_has_empty_lists(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = _run("How do I justify quality in SAT?", Path(tmp))
        plan = result["strategic_plan"]
        self.assertTrue(plan["cold_start"])
        self.assertEqual(plan["recommended_next_topics"], [])
        self.assertEqual(plan["review_topics"], [])
        self.assertEqual(plan["avoid_topics"], [])
        self.assertEqual(plan["misconception_focus"], [])
        self.assertEqual(plan["causal_chain_focus"], [])
        self.assertFalse(plan["sat_drill_needed"])


# ---------------------------------------------------------------------------
# Test 4: orchestrator works when LES contains known weak areas
# ---------------------------------------------------------------------------


class WarmLesIntegrationTests(unittest.TestCase):

    def test_planner_not_cold_start_when_les_has_weak_areas(self):
        """Required test 4: known_weak_areas in LES → planner is not cold-start."""
        with tempfile.TemporaryDirectory() as tmp:
            result = _run(
                "How do I justify quality in SAT?",
                Path(tmp),
                known_weak_areas=["causal_chain:malo_lactic", "fragile:acidity_quality"],
            )
        plan = result["strategic_plan"]
        self.assertFalse(plan["cold_start"])

    def test_actionable_weak_areas_reach_review_topics(self):
        """causal_chain: and fragile: prefixes surface in review_topics."""
        with tempfile.TemporaryDirectory() as tmp:
            result = _run(
                "How do I justify quality in SAT?",
                Path(tmp),
                known_weak_areas=["causal_chain:malo_lactic", "fragile:acidity_quality"],
            )
        plan = result["strategic_plan"]
        self.assertIn("malo_lactic", plan["review_topics"])
        self.assertIn("acidity_quality", plan["review_topics"])

    def test_infrastructure_weak_areas_do_not_reach_review_topics(self):
        """retrieval: and label: prefixes are infrastructure signals, not topics."""
        with tempfile.TemporaryDirectory() as tmp:
            result = _run(
                "How do I justify quality in SAT?",
                Path(tmp),
                known_weak_areas=["retrieval:keyword_coverage", "label:incomplete"],
            )
        plan = result["strategic_plan"]
        self.assertNotIn("keyword_coverage", plan["review_topics"])
        self.assertNotIn("incomplete", plan["review_topics"])


# ---------------------------------------------------------------------------
# Test 5: planner integration does not alter existing orchestrator fields
# ---------------------------------------------------------------------------


class InertIntegrationTests(unittest.TestCase):

    def test_existing_orchestrator_fields_unchanged(self):
        """Required test 5: adding strategic_plan does not alter any existing key."""
        expected_core_keys = {
            "student_query",
            "detected_misconception",
            "les_context_used",
            "orchestrator_decision",
            "retrieval_plan",
            "retrieved_context",
            "tutor_directive",
            "recommended_les_update",
            "governance_flags",
            "context_package",
            "context_package_paths",
            "session_staging_path",
        }
        with tempfile.TemporaryDirectory() as tmp:
            result = _run("How do I justify quality in SAT?", Path(tmp))
        for key in expected_core_keys:
            self.assertIn(key, result, f"Existing key '{key}' missing from result")

    def test_strategic_plan_not_in_context_package(self):
        """Plan is NOT injected into context_package — zero risk to Tutor rendering."""
        with tempfile.TemporaryDirectory() as tmp:
            result = _run("How do I justify quality in SAT?", Path(tmp))
        package = result["context_package"]
        self.assertNotIn("strategic_plan", package)

    def test_strategic_plan_not_in_retrieval_plan(self):
        """Plan is NOT injected into retrieval_plan — zero risk to retrieval ranking."""
        with tempfile.TemporaryDirectory() as tmp:
            result = _run("How do I justify quality in SAT?", Path(tmp))
        self.assertNotIn("strategic_plan", result["retrieval_plan"])

    def test_governance_flags_unchanged(self):
        """Governance flags in result are not affected by planner integration."""
        with tempfile.TemporaryDirectory() as tmp:
            result = _run("How do I justify quality in SAT?", Path(tmp))
        flags = result["governance_flags"]
        self.assertFalse(flags["safe_for_examiner"])
        self.assertFalse(flags["examiner_scoring_active"])

    def test_tutor_directive_safe_for_examiner_unchanged(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = _run("How do I justify quality in SAT?", Path(tmp))
        self.assertFalse(result["tutor_directive"]["safe_for_examiner"])


# ---------------------------------------------------------------------------
# Test 6: planner output contains no governance fields
# ---------------------------------------------------------------------------


class GovernanceTests(unittest.TestCase):

    def test_plan_contains_no_governance_fields(self):
        """Required test 6: plan output has ONLY the Phase 1A contract keys."""
        with tempfile.TemporaryDirectory() as tmp:
            result = _run("How do I justify quality in SAT?", Path(tmp))
        plan = result["strategic_plan"]
        for key in GOVERNANCE_KEYS:
            self.assertNotIn(key, plan, f"Governance key '{key}' must not be in plan")

    def test_plan_keys_exactly_match_contract(self):
        """Plan has neither extra keys (governance leakage) nor missing keys."""
        with tempfile.TemporaryDirectory() as tmp:
            result = _run("How do I justify quality in SAT?", Path(tmp))
        self.assertEqual(set(result["strategic_plan"].keys()), EXPECTED_PLAN_KEYS)

    def test_cold_start_plan_contains_no_governance_fields(self):
        """Governance check also passes on the cold-start branch."""
        with tempfile.TemporaryDirectory() as tmp:
            result = _run("How do I justify quality in SAT?", Path(tmp))
        plan = result["strategic_plan"]
        self.assertTrue(plan["cold_start"])
        for key in GOVERNANCE_KEYS:
            self.assertNotIn(key, plan)


# ---------------------------------------------------------------------------
# Test 7: planner integration remains deterministic
# ---------------------------------------------------------------------------


class DeterminismTests(unittest.TestCase):

    def test_same_query_same_les_produces_same_plan(self):
        """Required test 7: two identical calls → identical strategic_plan content."""
        query = "How do I justify quality in SAT?"
        weak_areas = ["causal_chain:malo_lactic"]

        with tempfile.TemporaryDirectory() as tmp1:
            r1 = _run(query, Path(tmp1), known_weak_areas=weak_areas)

        with tempfile.TemporaryDirectory() as tmp2:
            r2 = _run(query, Path(tmp2), known_weak_areas=weak_areas)

        # Exclude plan_generated_at (wall-clock timestamp)
        plan1 = {k: v for k, v in r1["strategic_plan"].items() if k != "plan_generated_at"}
        plan2 = {k: v for k, v in r2["strategic_plan"].items() if k != "plan_generated_at"}
        self.assertEqual(plan1, plan2)

    def test_different_les_produces_different_plan(self):
        """Different LES weak areas → different review_topics in plan."""
        query = "How do I justify quality in SAT?"

        with tempfile.TemporaryDirectory() as tmp1:
            r1 = _run(query, Path(tmp1), known_weak_areas=["causal_chain:malo_lactic"])

        with tempfile.TemporaryDirectory() as tmp2:
            r2 = _run(query, Path(tmp2), known_weak_areas=[])

        self.assertNotEqual(
            r1["strategic_plan"]["review_topics"],
            r2["strategic_plan"]["review_topics"],
        )


if __name__ == "__main__":
    unittest.main()
