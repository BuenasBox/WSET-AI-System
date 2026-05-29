"""Phase 2B: Ledger Summary Layer tests.

Verifies that summarize_ledger() produces correct, deterministic, governance-clean
aggregate observations — and that the summary is never consumed by any
behavioural component (planner, retrieval, Tutor).

All tests use inline fixtures. No file I/O needed.
"""

from __future__ import annotations

import copy
import unittest

from tools.orchestrator.ledger_summary import (
    DIFFICULTY_VALUES,
    TOP_N,
    _empty_summary,
    _top_n,
    summarize_ledger,
)

# ---------------------------------------------------------------------------
# Expected summary keys
# ---------------------------------------------------------------------------

EXPECTED_SUMMARY_KEYS: frozenset[str] = frozenset({
    "session_count",
    "sessions_analysed",
    "average_planning_confidence",
    "sat_drill_rate",
    "cold_start_rate",
    "top_review_topics",
    "top_misconceptions",
    "top_causal_chains",
    "difficulty_distribution",
    "difficulty_distribution_pct",
    "route_distribution",
})

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
    "examiner_equivalence",
    "pass_rate",
    "grade",
    "score",
})

# ---------------------------------------------------------------------------
# Fixture helpers
# ---------------------------------------------------------------------------


def _make_session(
    route: str = "normal_tutor",
    cold_start: bool = True,
    planning_confidence: float = 0.0,
    difficulty_progression: str = "stable",
    sat_drill_needed: bool = False,
    review_topics: list[str] | None = None,
    misconceptions_triggered: list[str] | None = None,
    causal_chains_seen: list[str] | None = None,
    timestamp: str = "2026-01-01T00:00:00+00:00",
) -> dict:
    return {
        "timestamp": timestamp,
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


def _make_ledger(sessions: list[dict]) -> dict:
    return {
        "version": 1,
        "session_count": len(sessions),
        "retention_policy": "keep_last_100",
        "sessions": sessions,
    }


# ---------------------------------------------------------------------------
# Test 1: empty ledger summary
# ---------------------------------------------------------------------------


class EmptyLedgerTests(unittest.TestCase):

    def test_empty_ledger_returns_zero_summary(self):
        """Required test 1: empty sessions list returns zero-state summary."""
        summary = summarize_ledger(_make_ledger([]))
        self.assertEqual(summary["session_count"], 0)
        self.assertEqual(summary["sessions_analysed"], 0)
        self.assertEqual(summary["average_planning_confidence"], 0.0)
        self.assertEqual(summary["sat_drill_rate"], 0.0)
        self.assertEqual(summary["top_review_topics"], [])
        self.assertEqual(summary["top_misconceptions"], [])
        self.assertEqual(summary["top_causal_chains"], [])

    def test_empty_summary_has_all_keys(self):
        """Empty summary dict has exactly the expected schema keys."""
        summary = _empty_summary()
        self.assertEqual(set(summary.keys()), EXPECTED_SUMMARY_KEYS)

    def test_none_ledger_returns_empty_summary(self):
        summary = summarize_ledger(None)  # type: ignore[arg-type]
        self.assertEqual(summary["session_count"], 0)

    def test_missing_sessions_key_returns_empty_summary(self):
        summary = summarize_ledger({"version": 1})
        self.assertEqual(summary["session_count"], 0)


# ---------------------------------------------------------------------------
# Test 2: single session summary
# ---------------------------------------------------------------------------


class SingleSessionSummaryTests(unittest.TestCase):

    def test_single_session_session_count(self):
        """Required test 2: one session → session_count == 1."""
        session = _make_session(
            planning_confidence=0.15,
            difficulty_progression="stable",
            sat_drill_needed=False,
            review_topics=["malo_lactic"],
        )
        summary = summarize_ledger(_make_ledger([session]))
        self.assertEqual(summary["session_count"], 1)
        self.assertEqual(summary["sessions_analysed"], 1)

    def test_single_session_review_topic_appears(self):
        session = _make_session(review_topics=["acidity_structure"])
        summary = summarize_ledger(_make_ledger([session]))
        self.assertEqual(len(summary["top_review_topics"]), 1)
        self.assertEqual(summary["top_review_topics"][0]["value"], "acidity_structure")
        self.assertEqual(summary["top_review_topics"][0]["count"], 1)
        self.assertEqual(summary["top_review_topics"][0]["frequency"], 1.0)

    def test_single_session_confidence_average(self):
        session = _make_session(planning_confidence=0.6)
        summary = summarize_ledger(_make_ledger([session]))
        self.assertAlmostEqual(summary["average_planning_confidence"], 0.6, places=3)

    def test_single_session_summary_has_all_keys(self):
        session = _make_session()
        summary = summarize_ledger(_make_ledger([session]))
        self.assertEqual(set(summary.keys()), EXPECTED_SUMMARY_KEYS)


# ---------------------------------------------------------------------------
# Test 3: multiple session aggregation
# ---------------------------------------------------------------------------


class MultiSessionAggregationTests(unittest.TestCase):

    def test_multiple_sessions_counted(self):
        """Required test 3: three sessions → session_count == 3."""
        sessions = [_make_session() for _ in range(3)]
        summary = summarize_ledger(_make_ledger(sessions))
        self.assertEqual(summary["session_count"], 3)
        self.assertEqual(summary["sessions_analysed"], 3)

    def test_multiple_sessions_aggregate_review_topics(self):
        sessions = [
            _make_session(review_topics=["acidity", "tannin"]),
            _make_session(review_topics=["acidity", "malo_lactic"]),
            _make_session(review_topics=["acidity"]),
        ]
        summary = summarize_ledger(_make_ledger(sessions))
        # "acidity" appears 3 times — must be first
        top = summary["top_review_topics"]
        self.assertEqual(top[0]["value"], "acidity")
        self.assertEqual(top[0]["count"], 3)

    def test_multiple_sessions_aggregate_confidence(self):
        sessions = [
            _make_session(planning_confidence=0.3),
            _make_session(planning_confidence=0.6),
            _make_session(planning_confidence=0.9),
        ]
        summary = summarize_ledger(_make_ledger(sessions))
        self.assertAlmostEqual(summary["average_planning_confidence"], 0.6, places=3)


# ---------------------------------------------------------------------------
# Test 4: review topic frequency calculation
# ---------------------------------------------------------------------------


class ReviewTopicFrequencyTests(unittest.TestCase):

    def test_review_topic_frequency(self):
        """Required test 4: frequency = count / total_occurrences of that signal."""
        sessions = [
            _make_session(review_topics=["A", "A", "B"]),
            _make_session(review_topics=["A"]),
        ]
        summary = summarize_ledger(_make_ledger(sessions))
        top = {item["value"]: item for item in summary["top_review_topics"]}
        self.assertEqual(top["A"]["count"], 3)
        self.assertEqual(top["B"]["count"], 1)
        # Frequencies must sum to 1.0
        total_freq = sum(item["frequency"] for item in summary["top_review_topics"])
        self.assertAlmostEqual(total_freq, 1.0, places=2)

    def test_review_topics_sorted_descending_by_count(self):
        sessions = [
            _make_session(review_topics=["rare"]),
            _make_session(review_topics=["common", "common", "common"]),
        ]
        # Inline: give common 2 more via another session
        sessions.append(_make_session(review_topics=["common"]))
        summary = summarize_ledger(_make_ledger(sessions))
        # "common" appears more often — must be first
        self.assertEqual(summary["top_review_topics"][0]["value"], "common")

    def test_review_topic_tie_broken_alphabetically(self):
        """Ties in count are broken alphabetically for determinism."""
        sessions = [
            _make_session(review_topics=["zebra"]),
            _make_session(review_topics=["apple"]),
        ]
        summary = summarize_ledger(_make_ledger(sessions))
        # Both have count=1; "apple" < "zebra" alphabetically
        self.assertEqual(summary["top_review_topics"][0]["value"], "apple")
        self.assertEqual(summary["top_review_topics"][1]["value"], "zebra")


# ---------------------------------------------------------------------------
# Test 5: misconception frequency calculation
# ---------------------------------------------------------------------------


class MisconceptionFrequencyTests(unittest.TestCase):

    def test_misconception_frequency(self):
        """Required test 5: misconception IDs are counted correctly."""
        sessions = [
            _make_session(misconceptions_triggered=["MC_ACIDITY_01"]),
            _make_session(misconceptions_triggered=["MC_ACIDITY_01"]),
            _make_session(misconceptions_triggered=["MC_TANNIN_01"]),
            _make_session(misconceptions_triggered=[]),
        ]
        summary = summarize_ledger(_make_ledger(sessions))
        top = {item["value"]: item for item in summary["top_misconceptions"]}
        self.assertEqual(top["MC_ACIDITY_01"]["count"], 2)
        self.assertEqual(top["MC_TANNIN_01"]["count"], 1)

    def test_no_misconceptions_empty_list(self):
        sessions = [_make_session(misconceptions_triggered=[])]
        summary = summarize_ledger(_make_ledger(sessions))
        self.assertEqual(summary["top_misconceptions"], [])


# ---------------------------------------------------------------------------
# Test 6: causal chain frequency calculation
# ---------------------------------------------------------------------------


class CausalChainFrequencyTests(unittest.TestCase):

    def test_causal_chain_frequency(self):
        """Required test 6: causal chain IDs counted correctly."""
        sessions = [
            _make_session(causal_chains_seen=["CC_ACIDITY_STRUCTURE", "CC_TANNIN_ASTRINGENCY"]),
            _make_session(causal_chains_seen=["CC_ACIDITY_STRUCTURE"]),
            _make_session(causal_chains_seen=[]),
        ]
        summary = summarize_ledger(_make_ledger(sessions))
        top = {item["value"]: item for item in summary["top_causal_chains"]}
        self.assertEqual(top["CC_ACIDITY_STRUCTURE"]["count"], 2)
        self.assertEqual(top["CC_TANNIN_ASTRINGENCY"]["count"], 1)

    def test_no_causal_chains_empty_list(self):
        sessions = [_make_session(causal_chains_seen=[])]
        summary = summarize_ledger(_make_ledger(sessions))
        self.assertEqual(summary["top_causal_chains"], [])


# ---------------------------------------------------------------------------
# Test 7: SAT drill rate calculation
# ---------------------------------------------------------------------------


class SatDrillRateTests(unittest.TestCase):

    def test_sat_drill_rate_calculation(self):
        """Required test 7: sat_drill_rate = sessions_with_drill / total_sessions."""
        sessions = [
            _make_session(sat_drill_needed=True),
            _make_session(sat_drill_needed=True),
            _make_session(sat_drill_needed=False),
            _make_session(sat_drill_needed=False),
        ]
        summary = summarize_ledger(_make_ledger(sessions))
        self.assertAlmostEqual(summary["sat_drill_rate"], 0.5, places=3)

    def test_sat_drill_rate_zero_when_no_drills(self):
        sessions = [_make_session(sat_drill_needed=False) for _ in range(5)]
        summary = summarize_ledger(_make_ledger(sessions))
        self.assertEqual(summary["sat_drill_rate"], 0.0)

    def test_sat_drill_rate_one_when_all_drills(self):
        sessions = [_make_session(sat_drill_needed=True) for _ in range(3)]
        summary = summarize_ledger(_make_ledger(sessions))
        self.assertEqual(summary["sat_drill_rate"], 1.0)


# ---------------------------------------------------------------------------
# Test 8: difficulty distribution calculation
# ---------------------------------------------------------------------------


class DifficultyDistributionTests(unittest.TestCase):

    def test_difficulty_distribution(self):
        """Required test 8: counts per difficulty value are correct."""
        sessions = [
            _make_session(difficulty_progression="stable"),
            _make_session(difficulty_progression="stable"),
            _make_session(difficulty_progression="consolidate"),
            _make_session(difficulty_progression="escalate"),
        ]
        summary = summarize_ledger(_make_ledger(sessions))
        dist = summary["difficulty_distribution"]
        self.assertEqual(dist["stable"], 2)
        self.assertEqual(dist["consolidate"], 1)
        self.assertEqual(dist["escalate"], 1)

    def test_difficulty_distribution_pct(self):
        sessions = [
            _make_session(difficulty_progression="stable"),
            _make_session(difficulty_progression="stable"),
            _make_session(difficulty_progression="consolidate"),
            _make_session(difficulty_progression="escalate"),
        ]
        summary = summarize_ledger(_make_ledger(sessions))
        pct = summary["difficulty_distribution_pct"]
        self.assertAlmostEqual(pct["stable"], 0.5, places=3)
        self.assertAlmostEqual(pct["consolidate"], 0.25, places=3)
        self.assertAlmostEqual(pct["escalate"], 0.25, places=3)

    def test_difficulty_distribution_has_all_three_keys(self):
        """All three difficulty values appear in the distribution even if count=0."""
        sessions = [_make_session(difficulty_progression="stable")]
        summary = summarize_ledger(_make_ledger(sessions))
        for key in DIFFICULTY_VALUES:
            self.assertIn(key, summary["difficulty_distribution"])
            self.assertIn(key, summary["difficulty_distribution_pct"])

    def test_unknown_difficulty_value_ignored(self):
        """An unknown difficulty value is silently excluded from the distribution."""
        sessions = [_make_session(difficulty_progression="INVALID_VALUE")]
        summary = summarize_ledger(_make_ledger(sessions))
        # Valid keys still present, all zero
        for key in DIFFICULTY_VALUES:
            self.assertEqual(summary["difficulty_distribution"][key], 0)


# ---------------------------------------------------------------------------
# Test 9: average confidence calculation
# ---------------------------------------------------------------------------


class AverageConfidenceTests(unittest.TestCase):

    def test_average_confidence(self):
        """Required test 9: average_planning_confidence is the arithmetic mean."""
        sessions = [
            _make_session(planning_confidence=0.0),
            _make_session(planning_confidence=0.5),
            _make_session(planning_confidence=1.0),
        ]
        summary = summarize_ledger(_make_ledger(sessions))
        self.assertAlmostEqual(summary["average_planning_confidence"], 0.5, places=3)

    def test_confidence_zero_for_all_zero_sessions(self):
        sessions = [_make_session(planning_confidence=0.0) for _ in range(5)]
        summary = summarize_ledger(_make_ledger(sessions))
        self.assertEqual(summary["average_planning_confidence"], 0.0)

    def test_confidence_rounds_to_three_decimal_places(self):
        sessions = [
            _make_session(planning_confidence=1 / 3),
            _make_session(planning_confidence=1 / 3),
            _make_session(planning_confidence=1 / 3),
        ]
        summary = summarize_ledger(_make_ledger(sessions))
        # Should be 0.333, not 0.3333...
        self.assertEqual(summary["average_planning_confidence"], round(1 / 3, 3))


# ---------------------------------------------------------------------------
# Test 10: deterministic output
# ---------------------------------------------------------------------------


class DeterminismTests(unittest.TestCase):

    def test_same_ledger_same_summary(self):
        """Required test 10: identical inputs always produce identical outputs."""
        sessions = [
            _make_session(review_topics=["A", "B"], planning_confidence=0.3),
            _make_session(review_topics=["A"], planning_confidence=0.6),
        ]
        ledger = _make_ledger(sessions)
        s1 = summarize_ledger(ledger)
        s2 = summarize_ledger(ledger)
        self.assertEqual(s1, s2)

    def test_order_of_sessions_same_counts_produce_same_summary(self):
        """Sessions in same order → same summary."""
        sessions_a = [
            _make_session(review_topics=["X"]),
            _make_session(review_topics=["Y"]),
        ]
        sessions_b = [
            _make_session(review_topics=["X"]),
            _make_session(review_topics=["Y"]),
        ]
        s1 = summarize_ledger(_make_ledger(sessions_a))
        s2 = summarize_ledger(_make_ledger(sessions_b))
        self.assertEqual(s1["top_review_topics"], s2["top_review_topics"])

    def test_top_n_helper_is_deterministic(self):
        """_top_n() produces the same output for the same Counter."""
        from collections import Counter
        c = Counter({"alpha": 3, "beta": 3, "gamma": 1})
        r1 = _top_n(c, 10)
        r2 = _top_n(c, 10)
        self.assertEqual(r1, r2)
        # Tie between alpha and beta broken alphabetically
        self.assertEqual(r1[0]["value"], "alpha")
        self.assertEqual(r1[1]["value"], "beta")


# ---------------------------------------------------------------------------
# Test 11: summary contains no governance fields
# ---------------------------------------------------------------------------


class GovernanceSummaryTests(unittest.TestCase):

    def test_no_governance_fields_in_summary(self):
        """Required test 11: governance fields must never appear in the summary."""
        sessions = [_make_session()]
        summary = summarize_ledger(_make_ledger(sessions))
        for field in GOVERNANCE_FIELDS:
            self.assertNotIn(field, summary)

    def test_summary_keys_exactly_match_contract(self):
        """Summary has ONLY the approved keys — no extra fields."""
        sessions = [_make_session()]
        summary = summarize_ledger(_make_ledger(sessions))
        self.assertEqual(set(summary.keys()), EXPECTED_SUMMARY_KEYS)

    def test_empty_summary_has_no_governance_fields(self):
        summary = _empty_summary()
        for field in GOVERNANCE_FIELDS:
            self.assertNotIn(field, summary)


# ---------------------------------------------------------------------------
# Test 12: summary contains no grading fields
# ---------------------------------------------------------------------------


class GradingSummaryTests(unittest.TestCase):

    def test_no_grading_fields_in_summary(self):
        """Required test 12: grading/scoring fields must never appear in summary."""
        sessions = [_make_session()]
        summary = summarize_ledger(_make_ledger(sessions))
        for field in GRADING_FIELDS:
            self.assertNotIn(field, summary)

    def test_empty_summary_has_no_grading_fields(self):
        summary = _empty_summary()
        for field in GRADING_FIELDS:
            self.assertNotIn(field, summary)


# ---------------------------------------------------------------------------
# Test 13: summary does not modify ledger
# ---------------------------------------------------------------------------


class ImmutabilityTests(unittest.TestCase):

    def test_summarize_does_not_modify_input_ledger(self):
        """Required test 13: summarize_ledger() is a pure function — no mutation."""
        sessions = [
            _make_session(review_topics=["A", "B"], planning_confidence=0.5),
        ]
        ledger = _make_ledger(sessions)
        ledger_before = copy.deepcopy(ledger)
        summarize_ledger(ledger)
        self.assertEqual(ledger, ledger_before)

    def test_summary_is_independent_of_ledger_reference(self):
        """Modifying the ledger after summarize_ledger() does not change the summary."""
        sessions = [_make_session(review_topics=["original"])]
        ledger = _make_ledger(sessions)
        summary = summarize_ledger(ledger)
        # Mutate the source ledger
        ledger["sessions"][0]["review_topics"].append("ADDED_AFTER")
        # Summary must be unchanged
        topic_values = [item["value"] for item in summary["top_review_topics"]]
        self.assertNotIn("ADDED_AFTER", topic_values)


# ---------------------------------------------------------------------------
# Test 14: summary handles malformed sessions safely
# ---------------------------------------------------------------------------


class RobustnessTests(unittest.TestCase):

    def test_malformed_sessions_skipped(self):
        """Required test 14: non-dict session entries are silently skipped."""
        mixed = [
            None,
            "not a dict",
            42,
            _make_session(planning_confidence=0.5),
        ]
        ledger = _make_ledger(mixed)  # type: ignore[arg-type]
        summary = summarize_ledger(ledger)
        # Only the one valid session should be counted
        self.assertEqual(summary["session_count"], 1)
        self.assertAlmostEqual(summary["average_planning_confidence"], 0.5)

    def test_missing_fields_in_session_use_defaults(self):
        """Sessions with missing keys are handled gracefully."""
        minimal = {"timestamp": "2026-01-01T00:00:00+00:00"}
        summary = summarize_ledger(_make_ledger([minimal]))
        self.assertEqual(summary["session_count"], 1)
        self.assertEqual(summary["top_review_topics"], [])
        self.assertEqual(summary["average_planning_confidence"], 0.0)

    def test_none_fields_in_session_do_not_raise(self):
        """None values for list fields do not raise."""
        session = {
            "review_topics": None,
            "misconceptions_triggered": None,
            "causal_chains_seen": None,
            "planning_confidence": None,
        }
        summary = summarize_ledger(_make_ledger([session]))
        self.assertEqual(summary["top_review_topics"], [])
        self.assertEqual(summary["average_planning_confidence"], 0.0)

    def test_top_n_cap_respected(self):
        """top_review_topics never exceeds TOP_N entries."""
        topics = [f"topic_{i}" for i in range(TOP_N + 20)]
        session = _make_session(review_topics=topics)
        summary = summarize_ledger(_make_ledger([session]))
        self.assertLessEqual(len(summary["top_review_topics"]), TOP_N)


if __name__ == "__main__":
    unittest.main()
