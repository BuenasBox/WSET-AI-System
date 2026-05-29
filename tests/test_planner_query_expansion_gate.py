"""Phase 3A.1: Planner query expansion gate tests.

Verifies that:
  - The gate (ENABLE_PLANNER_QUERY_EXPANSION=False) is a strict no-op.
  - When the gate is patched to True, ONLY causal_chain_focus is used.
  - All other planner signals are explicitly ignored.
  - Expansion is bounded, deterministic, and governance-clean.
  - Default orchestrator behaviour is unchanged with the gate off.

Tests that require the gate to be ON use unittest.mock.patch to temporarily
set tools.orchestrator.orchestrator.ENABLE_PLANNER_QUERY_EXPANSION = True.
All patched tests restore the original value automatically via context manager.
"""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.orchestrator.orchestrator import (
    ENABLE_PLANNER_QUERY_EXPANSION,
    MAX_PLANNER_CHAIN_HINTS,
    _apply_planner_query_hints,
    run_orchestrator,
)

_MODULE = "tools.orchestrator.orchestrator"
_FLAG = f"{_MODULE}.ENABLE_PLANNER_QUERY_EXPANSION"

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

_QUERY = "How do I justify quality in SAT?"


def _plan_with_chains(*chain_ids: str) -> dict:
    return {
        "recommended_next_topics": [],
        "review_topics": ["acidity", "tannin"],
        "avoid_topics": ["malo_lactic"],
        "misconception_focus": ["MC_ACIDITY_01"],
        "causal_chain_focus": list(chain_ids),
        "sat_drill_needed": True,
        "difficulty_progression": "consolidate",
        "planning_confidence": 0.75,
        "plan_generated_at": "2026-01-01T00:00:00+00:00",
        "cold_start": False,
    }


def _write_les(path: Path) -> Path:
    path.write_text(
        json.dumps({
            "learner_id": "test",
            "current_level": "WSET_L3",
            "known_weak_areas": [],
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


def _run(tmp: Path, query: str = _QUERY) -> dict:
    return run_orchestrator(
        query,
        les_path=_write_les(tmp / "epistemic_state.json"),
        misconception_dir=_write_misconception_fixture(tmp / "misconceptions"),
        staging_path=tmp / "session_staging.json",
        context_package_dir=tmp / "context_packages",
        root=tmp,
    )


# ---------------------------------------------------------------------------
# Test 1: flag off returns original query
# ---------------------------------------------------------------------------


class FlagOffTests(unittest.TestCase):

    def test_flag_is_off_by_default(self):
        """Required: ENABLE_PLANNER_QUERY_EXPANSION is False in production code."""
        self.assertFalse(ENABLE_PLANNER_QUERY_EXPANSION)

    def test_flag_off_returns_original_query(self):
        """Required test 1: with gate off, function returns query unchanged."""
        plan = _plan_with_chains("CC_ACIDITY_STRUCTURE", "CC_TANNIN")
        result = _apply_planner_query_hints(_QUERY, plan)
        self.assertEqual(result, _QUERY)

    def test_flag_off_even_with_many_chains(self):
        """Gate off → original query, regardless of how many chains are present."""
        plan = _plan_with_chains(*[f"CC_{i}" for i in range(20)])
        result = _apply_planner_query_hints(_QUERY, plan)
        self.assertEqual(result, _QUERY)


# ---------------------------------------------------------------------------
# Test 2: missing strategic_plan returns original query
# ---------------------------------------------------------------------------


class NullInputTests(unittest.TestCase):

    def test_none_plan_returns_original(self):
        """Required test 2: None strategic_plan → original query."""
        with patch(_FLAG, True):
            result = _apply_planner_query_hints(_QUERY, None)
        self.assertEqual(result, _QUERY)

    def test_empty_dict_returns_original(self):
        """Empty dict plan (no causal_chain_focus) → original query."""
        with patch(_FLAG, True):
            result = _apply_planner_query_hints(_QUERY, {})
        self.assertEqual(result, _QUERY)

    def test_non_dict_plan_returns_original(self):
        """Non-dict plan → original query."""
        with patch(_FLAG, True):
            result = _apply_planner_query_hints(_QUERY, "not_a_dict")  # type: ignore
        self.assertEqual(result, _QUERY)


# ---------------------------------------------------------------------------
# Test 3: empty causal_chain_focus returns original query
# ---------------------------------------------------------------------------


class EmptyChainFocusTests(unittest.TestCase):

    def test_empty_causal_chain_focus_returns_original(self):
        """Required test 3: empty causal_chain_focus → original query."""
        plan = _plan_with_chains()  # no chain IDs
        with patch(_FLAG, True):
            result = _apply_planner_query_hints(_QUERY, plan)
        self.assertEqual(result, _QUERY)

    def test_none_causal_chain_focus_returns_original(self):
        """causal_chain_focus=None → original query."""
        plan = {"causal_chain_focus": None}
        with patch(_FLAG, True):
            result = _apply_planner_query_hints(_QUERY, plan)
        self.assertEqual(result, _QUERY)


# ---------------------------------------------------------------------------
# Test 4: only causal_chain_focus is used
# ---------------------------------------------------------------------------


class SignalIsolationTests(unittest.TestCase):

    def test_only_causal_chain_focus_used(self):
        """Required test 4: expansion uses ONLY causal_chain_focus IDs."""
        plan = _plan_with_chains("CC_ACID_STRUCT")
        with patch(_FLAG, True):
            result = _apply_planner_query_hints(_QUERY, plan)
        self.assertIn("CC_ACID_STRUCT", result)
        self.assertTrue(result.startswith(_QUERY))

    def test_review_topics_are_ignored(self):
        """Required test 5: review_topics must not appear in the expansion."""
        plan = _plan_with_chains("CC_ACID")
        plan["review_topics"] = ["REVIEW_TOPIC_MUST_NOT_APPEAR"]
        with patch(_FLAG, True):
            result = _apply_planner_query_hints(_QUERY, plan)
        self.assertNotIn("REVIEW_TOPIC_MUST_NOT_APPEAR", result)

    def test_misconception_focus_is_ignored(self):
        """Required test 6: misconception_focus must not appear in expansion."""
        plan = _plan_with_chains("CC_ACID")
        plan["misconception_focus"] = ["MC_MUST_NOT_APPEAR"]
        with patch(_FLAG, True):
            result = _apply_planner_query_hints(_QUERY, plan)
        self.assertNotIn("MC_MUST_NOT_APPEAR", result)

    def test_difficulty_progression_is_ignored(self):
        """Required test 7: difficulty_progression must not appear in expansion."""
        plan = _plan_with_chains("CC_ACID")
        plan["difficulty_progression"] = "escalate"
        with patch(_FLAG, True):
            result = _apply_planner_query_hints(_QUERY, plan)
        self.assertNotIn("escalate", result)
        self.assertNotIn("difficulty", result)

    def test_planning_confidence_is_ignored(self):
        """Required test 8: planning_confidence must not appear in expansion."""
        plan = _plan_with_chains("CC_ACID")
        plan["planning_confidence"] = 0.99
        with patch(_FLAG, True):
            result = _apply_planner_query_hints(_QUERY, plan)
        self.assertNotIn("0.99", result)
        self.assertNotIn("confidence", result)


# ---------------------------------------------------------------------------
# Test 9: expansion bounded to max 3 hints
# ---------------------------------------------------------------------------


class BoundingTests(unittest.TestCase):

    def test_expansion_bounded_to_max_hints(self):
        """Required test 9: never more than MAX_PLANNER_CHAIN_HINTS tokens appended."""
        many_chains = [f"CC_{i:03d}" for i in range(20)]
        plan = _plan_with_chains(*many_chains)
        with patch(_FLAG, True):
            result = _apply_planner_query_hints(_QUERY, plan)
        # Count "causal_chain:" occurrences in the suffix
        suffix = result[len(_QUERY):].strip()
        hint_count = suffix.count("causal_chain:")
        self.assertLessEqual(hint_count, MAX_PLANNER_CHAIN_HINTS)
        self.assertEqual(hint_count, MAX_PLANNER_CHAIN_HINTS)

    def test_fewer_chains_than_max_all_included(self):
        """When fewer chains than the cap, all are included."""
        plan = _plan_with_chains("CC_A", "CC_B")
        with patch(_FLAG, True):
            result = _apply_planner_query_hints(_QUERY, plan)
        self.assertIn("causal_chain:CC_A", result)
        self.assertIn("causal_chain:CC_B", result)

    def test_max_chains_constant_is_three(self):
        """MAX_PLANNER_CHAIN_HINTS must be 3 (Section 4 design decision)."""
        self.assertEqual(MAX_PLANNER_CHAIN_HINTS, 3)


# ---------------------------------------------------------------------------
# Test 10: expansion is deterministic
# ---------------------------------------------------------------------------


class DeterminismTests(unittest.TestCase):

    def test_same_input_same_output(self):
        """Required test 10: identical inputs produce identical expansion."""
        plan = _plan_with_chains("CC_ACID_STRUCT", "CC_TANNIN")
        with patch(_FLAG, True):
            r1 = _apply_planner_query_hints(_QUERY, plan)
            r2 = _apply_planner_query_hints(_QUERY, plan)
        self.assertEqual(r1, r2)

    def test_expansion_format_uses_causal_chain_prefix(self):
        """Hint tokens use the 'causal_chain:<id>' format."""
        plan = _plan_with_chains("CC_ACIDITY_STRUCTURE")
        with patch(_FLAG, True):
            result = _apply_planner_query_hints(_QUERY, plan)
        self.assertIn("causal_chain:CC_ACIDITY_STRUCTURE", result)

    def test_expansion_appends_to_original_query(self):
        """Expanded query starts with the original query verbatim."""
        plan = _plan_with_chains("CC_ACID")
        with patch(_FLAG, True):
            result = _apply_planner_query_hints(_QUERY, plan)
        self.assertTrue(result.startswith(_QUERY + " "))


# ---------------------------------------------------------------------------
# Tests 11–12: governance and prose safety
# ---------------------------------------------------------------------------


class GovernanceExpansionTests(unittest.TestCase):

    def test_expansion_contains_no_governance_fields(self):
        """Required test 11: governance field names must not appear in expansion."""
        plan = _plan_with_chains("CC_ACID", "CC_TANNIN")
        plan["safe_for_examiner"] = False  # attempt to inject governance
        with patch(_FLAG, True):
            result = _apply_planner_query_hints(_QUERY, plan)
        self.assertNotIn("safe_for_examiner", result)
        self.assertNotIn("examiner_scoring_allowed", result)
        self.assertNotIn("governance", result)

    def test_expansion_contains_no_full_prose(self):
        """Required test 12: expansion tokens are compact IDs, not prose."""
        plan = _plan_with_chains("CC_ACID_STRUCTURE")
        with patch(_FLAG, True):
            result = _apply_planner_query_hints(_QUERY, plan)
        suffix = result[len(_QUERY):].strip()
        # The suffix must be compact tokens (no spaces within each token)
        for token in suffix.split():
            self.assertTrue(
                token.startswith("causal_chain:"),
                f"Unexpected non-causal-chain token in expansion: {token!r}",
            )

    def test_expansion_does_not_contain_causal_chain_prose_text(self):
        """Chain steps, descriptions, and mechanism text must not appear."""
        plan = _plan_with_chains("CC_ACID")
        # Simulate a plan that also has full chain objects stored somewhere
        plan["_full_chain_text"] = "High acidity causes sharp, fresh sensations on the palate"
        with patch(_FLAG, True):
            result = _apply_planner_query_hints(_QUERY, plan)
        self.assertNotIn("sharp", result)
        self.assertNotIn("palate", result)


# ---------------------------------------------------------------------------
# Tests 13–15: orchestrator default behavior unchanged
# ---------------------------------------------------------------------------


class OrchestratorGateTests(unittest.TestCase):

    def test_orchestrator_retrieval_query_matches_input_when_flag_off(self):
        """Required test 13: retrieval_plan.query equals original query with gate off."""
        with tempfile.TemporaryDirectory() as tmp:
            result = _run(Path(tmp), _QUERY)
        # When gate is off, retrieval_plan.query must equal the bare input query
        self.assertEqual(result["retrieval_plan"]["query"], _QUERY)

    def test_retrieval_query_in_context_package_unchanged(self):
        """Required test 14: context package retrieval_plan query equals input."""
        with tempfile.TemporaryDirectory() as tmp:
            result = _run(Path(tmp), _QUERY)
        pkg_plan = result["context_package"]["retrieval_plan"]
        self.assertEqual(pkg_plan["query"], _QUERY)

    def test_snapshots_unchanged_with_flag_off(self):
        """Required test 15: no expansion tokens present in retrieval query.

        With the flag off, the retrieval_plan.query must exactly equal the
        input query — no 'causal_chain:' tokens may be present. This is the
        in-process equivalent of the snapshot regression gate.
        """
        with tempfile.TemporaryDirectory() as tmp:
            result = _run(Path(tmp), _QUERY)
        query_used = result["retrieval_plan"]["query"]
        self.assertNotIn("causal_chain:", query_used)
        self.assertEqual(query_used, _QUERY)

    def test_governance_flags_unchanged_by_gate_wiring(self):
        """Wiring the expansion gate does not alter governance flags."""
        with tempfile.TemporaryDirectory() as tmp:
            result = _run(Path(tmp), _QUERY)
        self.assertFalse(result["governance_flags"]["safe_for_examiner"])
        self.assertFalse(result["tutor_directive"]["safe_for_examiner"])


if __name__ == "__main__":
    unittest.main()
