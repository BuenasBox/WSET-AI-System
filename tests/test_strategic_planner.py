"""Tests for tools/orchestrator/strategic_planner.py (Phase 1A).

Covers all 15 required tests plus structural and edge-case tests.

Design constraints:
  - All fixtures are inline — no external files required.
  - reference_date is always passed explicitly → deterministic outputs.
  - No orchestrator, retrieval, or answer_builder imports.
  - Tests are grouped by concern for readability.
"""

from __future__ import annotations

import unittest

from tools.orchestrator.strategic_planner import (
    CAUSAL_CHAIN_RISK_THRESHOLD,
    CONSOLIDATE_REVIEW_MIN,
    ESCALATE_MASTERED_MIN,
    MISCONCEPTION_PERSISTENCE_THRESHOLD,
    run_strategic_planner,
)


# ---------------------------------------------------------------------------
# Shared constants
# ---------------------------------------------------------------------------

REFERENCE_DATE = "2026-05-28T12:00:00+00:00"

REQUIRED_OUTPUT_KEYS = {
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
}

GOVERNANCE_KEYS = {
    "safe_for_examiner",
    "examiner_scoring_allowed",
    "uses_llm",
    "uses_api",
    "uses_embeddings",
    "uses_vector_db",
    "cloud_services_active",
}

VALID_DIFFICULTY_VALUES = {"stable", "consolidate", "escalate"}


# ---------------------------------------------------------------------------
# Minimal inline fixtures
# ---------------------------------------------------------------------------

def _empty_memory() -> dict:
    """Memory summary with no skill signals — triggers cold-start unless LES has data."""
    return {
        "low_mastery_concepts": [],
        "retention_risks": [],
        "recurrent_misconceptions": [],
        "difficult_causal_chains": [],
        "mastered_concepts": [],
        "preferred_depth": "standard",
        "overload_patterns": [],
    }


def _empty_les() -> dict:
    return {
        "learner_id": "nazareth",
        "current_level": "WSET_L3",
        "known_weak_areas": [],
        "recent_misconceptions": [],
        "session_count": 0,
    }


def _memory_with_retention_risk(concept_id: str, risk: float) -> dict:
    mem = _empty_memory()
    mem["retention_risks"] = [{"concept_id": concept_id, "retention_risk": risk}]
    return mem


def _memory_with_low_mastery(concept_id: str, mastery: float) -> dict:
    mem = _empty_memory()
    mem["low_mastery_concepts"] = [{"concept_id": concept_id, "mastery_probability": mastery}]
    return mem


def _memory_with_mastered(concepts: list[str]) -> dict:
    mem = _empty_memory()
    mem["mastered_concepts"] = list(concepts)
    return mem


def _memory_with_misconception(mc_id: str, persistence: float) -> dict:
    mem = _empty_memory()
    mem["recurrent_misconceptions"] = [
        {"misconception_id": mc_id, "hits": 3, "persistence": persistence}
    ]
    return mem


def _memory_with_causal_chain(chain_id: str, risk: float) -> dict:
    mem = _empty_memory()
    mem["difficult_causal_chains"] = [
        {"chain_id": chain_id, "failures": 2, "retention_risk": risk}
    ]
    return mem


def _memory_with_many_review_topics(n: int) -> dict:
    """Memory with n distinct concepts in retention_risks."""
    mem = _empty_memory()
    mem["retention_risks"] = [
        {"concept_id": f"concept_{i}", "retention_risk": 0.7}
        for i in range(n)
    ]
    return mem


def _prepass_detected(mc_id: str) -> dict:
    return {
        "detected": True,
        "matched_misconception_id": mc_id,
        "confidence": 0.75,
        "severity": "medium",
    }


def _prepass_not_detected() -> dict:
    return {
        "detected": False,
        "matched_misconception_id": None,
        "confidence": 0.0,
    }


# ---------------------------------------------------------------------------
# 1. Cold-start behaviour
# ---------------------------------------------------------------------------

class ColdStartTests(unittest.TestCase):

    def test_cold_start_returns_conservative_plan(self) -> None:
        """Required test 1: with no data at all, plan is conservative."""
        result = run_strategic_planner(
            memory_summary=None,
            les_context=None,
            reference_date=REFERENCE_DATE,
        )
        self.assertTrue(result["cold_start"])
        self.assertAlmostEqual(result["planning_confidence"], 0.0)
        self.assertEqual(result["difficulty_progression"], "stable")
        self.assertFalse(result["sat_drill_needed"])

    def test_cold_start_does_not_recommend_topics(self) -> None:
        """Required test 2: cold-start plan has no invented recommendations."""
        result = run_strategic_planner(
            memory_summary=_empty_memory(),
            les_context=_empty_les(),
            reference_date=REFERENCE_DATE,
        )
        self.assertTrue(result["cold_start"])
        self.assertEqual(result["recommended_next_topics"], [])
        self.assertEqual(result["review_topics"], [])
        self.assertEqual(result["avoid_topics"], [])
        self.assertEqual(result["misconception_focus"], [])
        self.assertEqual(result["causal_chain_focus"], [])

    def test_none_inputs_is_cold_start(self) -> None:
        result = run_strategic_planner(
            memory_summary=None,
            les_context=None,
            reference_date=REFERENCE_DATE,
        )
        self.assertTrue(result["cold_start"])

    def test_empty_dicts_is_cold_start(self) -> None:
        result = run_strategic_planner(
            memory_summary={},
            les_context={},
            reference_date=REFERENCE_DATE,
        )
        self.assertTrue(result["cold_start"])

    def test_les_with_weak_areas_breaks_cold_start(self) -> None:
        """If LES has known_weak_areas, cold-start is False even without skill data."""
        les = _empty_les()
        les["known_weak_areas"] = ["causal_chain:tannin structure"]
        result = run_strategic_planner(
            memory_summary=_empty_memory(),
            les_context=les,
            reference_date=REFERENCE_DATE,
        )
        self.assertFalse(result["cold_start"])

    def test_recent_misconceptions_in_les_breaks_cold_start(self) -> None:
        les = _empty_les()
        les["recent_misconceptions"] = ["MC_ACIDITY_01"]
        result = run_strategic_planner(
            memory_summary=_empty_memory(),
            les_context=les,
            reference_date=REFERENCE_DATE,
        )
        self.assertFalse(result["cold_start"])


# ---------------------------------------------------------------------------
# 2. Output schema
# ---------------------------------------------------------------------------

class OutputSchemaTests(unittest.TestCase):

    def test_output_schema_has_all_required_keys_cold_start(self) -> None:
        """Required test 3 (cold-start branch)."""
        result = run_strategic_planner(
            memory_summary=None,
            les_context=None,
            reference_date=REFERENCE_DATE,
        )
        self.assertEqual(set(result.keys()), REQUIRED_OUTPUT_KEYS)

    def test_output_schema_has_all_required_keys_normal(self) -> None:
        """Required test 3 (normal branch)."""
        result = run_strategic_planner(
            memory_summary=_memory_with_mastered(["tannin"]),
            les_context=_empty_les(),
            reference_date=REFERENCE_DATE,
        )
        self.assertEqual(set(result.keys()), REQUIRED_OUTPUT_KEYS)

    def test_output_values_correct_types_cold_start(self) -> None:
        """Required test 4 (cold-start branch)."""
        result = run_strategic_planner(
            memory_summary=None,
            les_context=None,
            reference_date=REFERENCE_DATE,
        )
        self._assert_types(result)

    def test_output_values_correct_types_normal(self) -> None:
        """Required test 4 (normal branch)."""
        result = run_strategic_planner(
            memory_summary=_memory_with_retention_risk("acidity", 0.7),
            les_context=_empty_les(),
            reference_date=REFERENCE_DATE,
        )
        self._assert_types(result)

    def _assert_types(self, result: dict) -> None:
        self.assertIsInstance(result["recommended_next_topics"], list)
        self.assertIsInstance(result["review_topics"], list)
        self.assertIsInstance(result["avoid_topics"], list)
        self.assertIsInstance(result["misconception_focus"], list)
        self.assertIsInstance(result["causal_chain_focus"], list)
        self.assertIsInstance(result["sat_drill_needed"], bool)
        self.assertIsInstance(result["difficulty_progression"], str)
        self.assertIsInstance(result["planning_confidence"], float)
        self.assertIsInstance(result["plan_generated_at"], str)
        self.assertIsInstance(result["cold_start"], bool)

    def test_difficulty_progression_is_valid_value(self) -> None:
        for mem, les in [
            (None, None),
            (_memory_with_mastered(["a"] * 8), _empty_les()),
            (_memory_with_many_review_topics(CONSOLIDATE_REVIEW_MIN), _empty_les()),
        ]:
            with self.subTest(mem=mem):
                result = run_strategic_planner(
                    memory_summary=mem,
                    les_context=les,
                    reference_date=REFERENCE_DATE,
                )
                self.assertIn(result["difficulty_progression"], VALID_DIFFICULTY_VALUES)

    def test_planning_confidence_in_0_1_range(self) -> None:
        for mem, les in [
            (None, None),
            (_empty_memory(), _empty_les()),
            (_memory_with_mastered(["a"] * 10), _empty_les()),
        ]:
            with self.subTest():
                result = run_strategic_planner(
                    memory_summary=mem,
                    les_context=les,
                    reference_date=REFERENCE_DATE,
                )
                self.assertGreaterEqual(result["planning_confidence"], 0.0)
                self.assertLessEqual(result["planning_confidence"], 1.0)

    def test_plan_generated_at_matches_reference_date(self) -> None:
        result = run_strategic_planner(
            memory_summary=None,
            les_context=None,
            reference_date=REFERENCE_DATE,
        )
        self.assertEqual(result["plan_generated_at"], REFERENCE_DATE)


# ---------------------------------------------------------------------------
# 3. Determinism
# ---------------------------------------------------------------------------

class DeterminismTests(unittest.TestCase):

    def test_same_input_same_reference_date_same_output(self) -> None:
        """Required test 5."""
        mem = _memory_with_retention_risk("tannin", 0.7)
        les = _empty_les()
        r1 = run_strategic_planner(memory_summary=mem, les_context=les, reference_date=REFERENCE_DATE)
        r2 = run_strategic_planner(memory_summary=mem, les_context=les, reference_date=REFERENCE_DATE)
        self.assertEqual(r1, r2)

    def test_same_cold_start_input_same_output(self) -> None:
        r1 = run_strategic_planner(memory_summary=None, les_context=None, reference_date=REFERENCE_DATE)
        r2 = run_strategic_planner(memory_summary=None, les_context=None, reference_date=REFERENCE_DATE)
        self.assertEqual(r1, r2)

    def test_different_reference_dates_produce_different_timestamps(self) -> None:
        date_a = "2026-05-28T10:00:00+00:00"
        date_b = "2026-05-28T14:00:00+00:00"
        r1 = run_strategic_planner(memory_summary=None, les_context=None, reference_date=date_a)
        r2 = run_strategic_planner(memory_summary=None, les_context=None, reference_date=date_b)
        self.assertNotEqual(r1["plan_generated_at"], r2["plan_generated_at"])


# ---------------------------------------------------------------------------
# 4. review_topics
# ---------------------------------------------------------------------------

class ReviewTopicsTests(unittest.TestCase):

    def test_high_retention_risk_goes_to_review_topics(self) -> None:
        """Required test 6."""
        risk = CAUSAL_CHAIN_RISK_THRESHOLD + 0.2  # well above threshold
        result = run_strategic_planner(
            memory_summary=_memory_with_retention_risk("tannin_structure", risk),
            les_context=_empty_les(),
            reference_date=REFERENCE_DATE,
        )
        self.assertIn("tannin_structure", result["review_topics"])
        self.assertFalse(result["cold_start"])

    def test_low_mastery_goes_to_review_topics(self) -> None:
        """Required test 7."""
        mastery = 0.30  # below LOW_MASTERY_THRESHOLD
        result = run_strategic_planner(
            memory_summary=_memory_with_low_mastery("acidity_balance", mastery),
            les_context=_empty_les(),
            reference_date=REFERENCE_DATE,
        )
        self.assertIn("acidity_balance", result["review_topics"])
        self.assertFalse(result["cold_start"])

    def test_review_topics_deduplicated(self) -> None:
        """A concept appearing in both retention_risks and low_mastery appears once."""
        concept = "cool_climate_acidity"
        mem = _empty_memory()
        mem["retention_risks"] = [{"concept_id": concept, "retention_risk": 0.7}]
        mem["low_mastery_concepts"] = [{"concept_id": concept, "mastery_probability": 0.3}]
        result = run_strategic_planner(
            memory_summary=mem,
            les_context=_empty_les(),
            reference_date=REFERENCE_DATE,
        )
        self.assertEqual(result["review_topics"].count(concept), 1)

    def test_known_weak_areas_from_les_influence_review_topics(self) -> None:
        """Required test 14: causal_chain: and fragile: prefixes extracted as topics."""
        les = _empty_les()
        les["known_weak_areas"] = [
            "causal_chain:flor biological ageing",
            "fragile:cool climate alcohol",
            "retrieval:missing_keyword_support",   # should be ignored
            "label:shallow_retrieval",             # should be ignored
        ]
        result = run_strategic_planner(
            memory_summary=_empty_memory(),
            les_context=les,
            reference_date=REFERENCE_DATE,
        )
        self.assertFalse(result["cold_start"])
        self.assertIn("flor biological ageing", result["review_topics"])
        self.assertIn("cool climate alcohol", result["review_topics"])
        # Infrastructure labels must not appear as topics
        self.assertNotIn("missing_keyword_support", result["review_topics"])
        self.assertNotIn("shallow_retrieval", result["review_topics"])
        self.assertNotIn("retrieval:missing_keyword_support", result["review_topics"])
        self.assertNotIn("label:shallow_retrieval", result["review_topics"])

    def test_retention_risk_appears_before_les_weak_areas(self) -> None:
        """Retention risks (urgent) appear before LES weak areas (coarser signal)."""
        mem = _memory_with_retention_risk("urgent_concept", 0.8)
        les = _empty_les()
        les["known_weak_areas"] = ["causal_chain:coarser_topic"]
        result = run_strategic_planner(
            memory_summary=mem,
            les_context=les,
            reference_date=REFERENCE_DATE,
        )
        review = result["review_topics"]
        self.assertIn("urgent_concept", review)
        self.assertIn("coarser_topic", review)
        self.assertLess(review.index("urgent_concept"), review.index("coarser_topic"))


# ---------------------------------------------------------------------------
# 5. avoid_topics
# ---------------------------------------------------------------------------

class AvoidTopicsTests(unittest.TestCase):

    def test_mastered_concept_goes_to_avoid_topics(self) -> None:
        """Required test 8."""
        result = run_strategic_planner(
            memory_summary=_memory_with_mastered(["tannin_astringency"]),
            les_context=_empty_les(),
            reference_date=REFERENCE_DATE,
        )
        self.assertIn("tannin_astringency", result["avoid_topics"])
        self.assertFalse(result["cold_start"])

    def test_multiple_mastered_concepts_in_avoid_topics(self) -> None:
        mastered = ["tannin", "acidity", "oak_flavour"]
        result = run_strategic_planner(
            memory_summary=_memory_with_mastered(mastered),
            les_context=_empty_les(),
            reference_date=REFERENCE_DATE,
        )
        for concept in mastered:
            with self.subTest(concept=concept):
                self.assertIn(concept, result["avoid_topics"])


# ---------------------------------------------------------------------------
# 6. misconception_focus
# ---------------------------------------------------------------------------

class MisconceptionFocusTests(unittest.TestCase):

    def test_high_persistence_misconception_in_focus(self) -> None:
        """Required test 9."""
        persistence = MISCONCEPTION_PERSISTENCE_THRESHOLD + 0.2
        result = run_strategic_planner(
            memory_summary=_memory_with_misconception("MC_TANNIN_01", persistence),
            les_context=_empty_les(),
            reference_date=REFERENCE_DATE,
        )
        self.assertIn("MC_TANNIN_01", result["misconception_focus"])

    def test_low_persistence_misconception_not_in_focus(self) -> None:
        """Misconceptions below threshold must not appear in focus."""
        persistence = MISCONCEPTION_PERSISTENCE_THRESHOLD - 0.1
        result = run_strategic_planner(
            memory_summary=_memory_with_misconception("MC_TANNIN_01", persistence),
            les_context=_empty_les(),
            reference_date=REFERENCE_DATE,
        )
        self.assertNotIn("MC_TANNIN_01", result["misconception_focus"])

    def test_active_prepass_misconception_appears_first(self) -> None:
        """Required test 10: active query misconception precedes persistent ones."""
        # MC_PERSISTENT has high persistence but is NOT the active query misconception
        mem = _memory_with_misconception("MC_PERSISTENT", 0.8)
        # MC_ACTIVE is from the current session prepass
        prepass = _prepass_detected("MC_ACTIVE")
        result = run_strategic_planner(
            memory_summary=mem,
            les_context=_empty_les(),
            prepass_result=prepass,
            reference_date=REFERENCE_DATE,
        )
        focus = result["misconception_focus"]
        self.assertIn("MC_ACTIVE", focus)
        self.assertIn("MC_PERSISTENT", focus)
        self.assertEqual(focus[0], "MC_ACTIVE")
        self.assertLess(focus.index("MC_ACTIVE"), focus.index("MC_PERSISTENT"))

    def test_no_prepass_result_does_not_error(self) -> None:
        result = run_strategic_planner(
            memory_summary=_memory_with_misconception("MC_X", 0.6),
            les_context=_empty_les(),
            prepass_result=None,
            reference_date=REFERENCE_DATE,
        )
        self.assertIn("MC_X", result["misconception_focus"])

    def test_prepass_not_detected_does_not_add_to_focus(self) -> None:
        result = run_strategic_planner(
            memory_summary=_empty_memory(),
            les_context=_empty_les(),
            prepass_result=_prepass_not_detected(),
            reference_date=REFERENCE_DATE,
        )
        # cold_start because no data; misconception_focus must be empty
        self.assertTrue(result["cold_start"])
        self.assertEqual(result["misconception_focus"], [])

    def test_prepass_detected_but_cold_start_memory(self) -> None:
        """When prepass detects a misconception but memory is empty and no les data,
        it is still cold_start — prepass alone does not break cold-start."""
        prepass = _prepass_detected("MC_ACTIVE")
        result = run_strategic_planner(
            memory_summary=_empty_memory(),
            les_context=_empty_les(),
            prepass_result=prepass,
            reference_date=REFERENCE_DATE,
        )
        # Cold-start because no LES or memory data
        self.assertTrue(result["cold_start"])
        # In cold_start, misconception_focus is empty
        self.assertEqual(result["misconception_focus"], [])

    def test_active_prepass_misconception_deduplicated(self) -> None:
        """If the active misconception is also persistent, it appears only once."""
        mc_id = "MC_SHARED"
        mem = _memory_with_misconception(mc_id, 0.8)
        prepass = _prepass_detected(mc_id)
        result = run_strategic_planner(
            memory_summary=mem,
            les_context=_empty_les(),
            prepass_result=prepass,
            reference_date=REFERENCE_DATE,
        )
        self.assertEqual(result["misconception_focus"].count(mc_id), 1)


# ---------------------------------------------------------------------------
# 7. causal_chain_focus
# ---------------------------------------------------------------------------

class CausalChainFocusTests(unittest.TestCase):

    def test_high_risk_causal_chain_in_focus(self) -> None:
        """Required test 11."""
        risk = CAUSAL_CHAIN_RISK_THRESHOLD + 0.1
        result = run_strategic_planner(
            memory_summary=_memory_with_causal_chain("cc_flor_biological_ageing", risk),
            les_context=_empty_les(),
            reference_date=REFERENCE_DATE,
        )
        self.assertIn("cc_flor_biological_ageing", result["causal_chain_focus"])

    def test_low_risk_causal_chain_not_in_focus(self) -> None:
        risk = CAUSAL_CHAIN_RISK_THRESHOLD - 0.1
        result = run_strategic_planner(
            memory_summary=_memory_with_causal_chain("cc_flor_biological_ageing", risk),
            les_context=_empty_les(),
            reference_date=REFERENCE_DATE,
        )
        self.assertNotIn("cc_flor_biological_ageing", result["causal_chain_focus"])

    def test_multiple_chains_filtered_by_threshold(self) -> None:
        mem = _empty_memory()
        mem["difficult_causal_chains"] = [
            {"chain_id": "chain_high", "failures": 3, "retention_risk": 0.8},
            {"chain_id": "chain_low",  "failures": 1, "retention_risk": 0.3},
        ]
        result = run_strategic_planner(
            memory_summary=mem,
            les_context=_empty_les(),
            reference_date=REFERENCE_DATE,
        )
        self.assertIn("chain_high", result["causal_chain_focus"])
        self.assertNotIn("chain_low", result["causal_chain_focus"])


# ---------------------------------------------------------------------------
# 8. difficulty_progression
# ---------------------------------------------------------------------------

class DifficultyProgressionTests(unittest.TestCase):

    def test_many_review_topics_causes_consolidate(self) -> None:
        """Required test 12."""
        n = CONSOLIDATE_REVIEW_MIN  # exactly at threshold
        result = run_strategic_planner(
            memory_summary=_memory_with_many_review_topics(n),
            les_context=_empty_les(),
            reference_date=REFERENCE_DATE,
        )
        self.assertEqual(result["difficulty_progression"], "consolidate")

    def test_more_than_consolidate_min_also_consolidates(self) -> None:
        result = run_strategic_planner(
            memory_summary=_memory_with_many_review_topics(CONSOLIDATE_REVIEW_MIN + 2),
            les_context=_empty_les(),
            reference_date=REFERENCE_DATE,
        )
        self.assertEqual(result["difficulty_progression"], "consolidate")

    def test_many_mastered_no_reviews_causes_escalate(self) -> None:
        """Required test 13."""
        mastered = [f"concept_{i}" for i in range(ESCALATE_MASTERED_MIN)]
        result = run_strategic_planner(
            memory_summary=_memory_with_mastered(mastered),
            les_context=_empty_les(),
            reference_date=REFERENCE_DATE,
        )
        self.assertEqual(result["difficulty_progression"], "escalate")
        self.assertEqual(result["review_topics"], [])

    def test_preferred_depth_deep_causes_consolidate(self) -> None:
        mem = _memory_with_mastered(["tannin"])
        mem["preferred_depth"] = "deep"
        result = run_strategic_planner(
            memory_summary=mem,
            les_context=_empty_les(),
            reference_date=REFERENCE_DATE,
        )
        self.assertEqual(result["difficulty_progression"], "consolidate")

    def test_default_case_is_stable(self) -> None:
        """Few mastered, few review topics → stable."""
        mem = _memory_with_mastered(["tannin", "acidity"])  # only 2, below escalate min
        result = run_strategic_planner(
            memory_summary=mem,
            les_context=_empty_les(),
            reference_date=REFERENCE_DATE,
        )
        self.assertEqual(result["difficulty_progression"], "stable")

    def test_consolidate_takes_priority_over_escalate(self) -> None:
        """Even with many mastered, if there are enough review topics → consolidate."""
        mastered = [f"mastered_{i}" for i in range(ESCALATE_MASTERED_MIN + 2)]
        mem = _memory_with_mastered(mastered)
        # Add enough retention risks to also trigger consolidate
        mem["retention_risks"] = [
            {"concept_id": f"review_{i}", "retention_risk": 0.7}
            for i in range(CONSOLIDATE_REVIEW_MIN)
        ]
        result = run_strategic_planner(
            memory_summary=mem,
            les_context=_empty_les(),
            reference_date=REFERENCE_DATE,
        )
        self.assertEqual(result["difficulty_progression"], "consolidate")


# ---------------------------------------------------------------------------
# 9. Governance
# ---------------------------------------------------------------------------

class GovernanceTests(unittest.TestCase):

    def test_planner_output_does_not_contain_governance_fields_cold_start(self) -> None:
        """Required test 15 (cold-start branch)."""
        result = run_strategic_planner(
            memory_summary=None,
            les_context=None,
            reference_date=REFERENCE_DATE,
        )
        for key in GOVERNANCE_KEYS:
            with self.subTest(key=key):
                self.assertNotIn(key, result)

    def test_planner_output_does_not_contain_governance_fields_normal(self) -> None:
        """Required test 15 (normal branch)."""
        result = run_strategic_planner(
            memory_summary=_memory_with_mastered(["tannin"]),
            les_context=_empty_les(),
            reference_date=REFERENCE_DATE,
        )
        for key in GOVERNANCE_KEYS:
            with self.subTest(key=key):
                self.assertNotIn(key, result)

    def test_output_has_no_extra_keys(self) -> None:
        """Output has ONLY the required keys — nothing more, nothing less."""
        result = run_strategic_planner(
            memory_summary=_memory_with_retention_risk("tannin", 0.7),
            les_context=_empty_les(),
            reference_date=REFERENCE_DATE,
        )
        self.assertEqual(set(result.keys()), REQUIRED_OUTPUT_KEYS)


# ---------------------------------------------------------------------------
# 10. Edge cases and robustness
# ---------------------------------------------------------------------------

class RobustnessTests(unittest.TestCase):

    def test_none_memory_does_not_raise(self) -> None:
        try:
            run_strategic_planner(memory_summary=None, les_context=None, reference_date=REFERENCE_DATE)
        except Exception as e:
            self.fail(f"run_strategic_planner raised {type(e).__name__}: {e}")

    def test_empty_strings_in_memory_items_are_skipped(self) -> None:
        mem = _empty_memory()
        mem["retention_risks"] = [{"concept_id": "", "retention_risk": 0.9}]
        result = run_strategic_planner(
            memory_summary=mem,
            les_context=_empty_les(),
            reference_date=REFERENCE_DATE,
        )
        # Empty concept_id must not appear in review_topics
        self.assertNotIn("", result["review_topics"])

    def test_weak_area_retrieval_prefix_is_ignored(self) -> None:
        les = _empty_les()
        les["known_weak_areas"] = ["retrieval:missing_keyword_support"]
        result = run_strategic_planner(
            memory_summary=_empty_memory(),
            les_context=les,
            reference_date=REFERENCE_DATE,
        )
        # "retrieval:" prefix is not actionable — must not produce a review topic
        self.assertNotIn("missing_keyword_support", result["review_topics"])
        self.assertNotIn("retrieval:missing_keyword_support", result["review_topics"])

    def test_weak_area_label_prefix_is_ignored(self) -> None:
        les = _empty_les()
        les["known_weak_areas"] = ["label:shallow_retrieval"]
        result = run_strategic_planner(
            memory_summary=_empty_memory(),
            les_context=les,
            reference_date=REFERENCE_DATE,
        )
        self.assertNotIn("shallow_retrieval", result["review_topics"])

    def test_planning_confidence_increases_with_more_signals(self) -> None:
        """Planner knows it knows more when it has more data."""
        sparse_mem = _memory_with_mastered(["tannin"])
        rich_mem = _memory_with_mastered([f"c_{i}" for i in range(10)])
        rich_mem["retention_risks"] = [{"concept_id": f"r_{i}", "retention_risk": 0.7} for i in range(5)]

        result_sparse = run_strategic_planner(
            memory_summary=sparse_mem, les_context=_empty_les(), reference_date=REFERENCE_DATE
        )
        result_rich = run_strategic_planner(
            memory_summary=rich_mem, les_context=_empty_les(), reference_date=REFERENCE_DATE
        )
        self.assertGreater(
            result_rich["planning_confidence"],
            result_sparse["planning_confidence"],
        )

    def test_sat_drill_triggered_by_sat_topic_in_review(self) -> None:
        """A review topic containing 'balance' triggers SAT drill."""
        mem = _memory_with_retention_risk("sat_balance_intensity", 0.7)
        result = run_strategic_planner(
            memory_summary=mem,
            les_context=_empty_les(),
            reference_date=REFERENCE_DATE,
        )
        self.assertTrue(result["sat_drill_needed"])

    def test_sat_drill_false_when_no_sat_topics(self) -> None:
        mem = _memory_with_retention_risk("tannin_structure", 0.7)
        result = run_strategic_planner(
            memory_summary=mem,
            les_context=_empty_les(),
            reference_date=REFERENCE_DATE,
        )
        self.assertFalse(result["sat_drill_needed"])


if __name__ == "__main__":
    unittest.main()
