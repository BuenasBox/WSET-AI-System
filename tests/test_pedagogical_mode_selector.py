"""Unit tests for the deterministic pedagogical strategy selector.

Covers every adjustment rule individually, composite rule combinations,
cold-start/no-context safety, derived signals, and governance invariants.

Each rule test follows the pattern:
  1. Build the minimum context that triggers the rule.
  2. Call select_pedagogical_strategy().
  3. Assert the expected function was boosted (relative to an untriggered baseline).
  4. Assert governance is clean.
"""

import unittest

from tools.tutor.pedagogical_strategy.mode_selector import (
    ADJUSTMENT_RULES,
    FUNCTION_MIN_WEIGHT,
    HOST_MIN_WEIGHT,
    _clamp_and_normalise,
    _rule_applies,
    select_pedagogical_strategy,
)


def _baseline() -> dict:
    """Return a neutral directive with no context signals."""
    return select_pedagogical_strategy()


def _weight(directive: dict, fn: str) -> float:
    return directive["function_weights"].get(fn, 0.0)


class TestExamImminentRule(unittest.TestCase):
    """rule_id: exam_imminent — exam_days_remaining <= 14."""

    def _directive(self, days: int) -> dict:
        return select_pedagogical_strategy(exam_days_remaining=days)

    def test_challenger_increases_when_exam_imminent(self):
        d = self._directive(7)
        baseline = _weight(_baseline(), "challenger")
        self.assertGreater(_weight(d, "challenger"), baseline)

    def test_critic_increases_when_exam_imminent(self):
        d = self._directive(14)
        baseline = _weight(_baseline(), "critic")
        self.assertGreater(_weight(d, "critic"), baseline)

    def test_rule_fires_at_exactly_14(self):
        d = self._directive(14)
        self.assertIn("exam_imminent", d["rules_applied"])

    def test_rule_fires_at_zero(self):
        d = self._directive(0)
        self.assertIn("exam_imminent", d["rules_applied"])

    def test_rule_does_not_fire_at_15(self):
        d = select_pedagogical_strategy(exam_days_remaining=15)
        self.assertNotIn("exam_imminent", d["rules_applied"])

    def test_exam_imminent_does_not_activate_examiner_scoring(self):
        d = self._directive(7)
        self.assertFalse(d["governance"]["examiner_scoring_allowed"])

    def test_exam_imminent_does_not_activate_safe_for_examiner(self):
        d = self._directive(7)
        self.assertFalse(d["governance"]["safe_for_examiner"])


class TestExamApproachingRule(unittest.TestCase):
    """rule_id: exam_approaching — 14 < exam_days_remaining <= 60."""

    def test_scientist_increases_when_exam_approaching(self):
        d = select_pedagogical_strategy(exam_days_remaining=30)
        baseline = _weight(_baseline(), "scientist")
        self.assertGreater(_weight(d, "scientist"), baseline)

    def test_challenger_increases_when_exam_approaching(self):
        d = select_pedagogical_strategy(exam_days_remaining=45)
        baseline = _weight(_baseline(), "challenger")
        self.assertGreater(_weight(d, "challenger"), baseline)

    def test_rule_fires_at_60(self):
        d = select_pedagogical_strategy(exam_days_remaining=60)
        self.assertIn("exam_approaching", d["rules_applied"])

    def test_rule_fires_at_15(self):
        d = select_pedagogical_strategy(exam_days_remaining=15)
        self.assertIn("exam_approaching", d["rules_applied"])

    def test_rule_does_not_fire_at_14(self):
        # 14 triggers exam_imminent, not exam_approaching.
        d = select_pedagogical_strategy(exam_days_remaining=14)
        self.assertNotIn("exam_approaching", d["rules_applied"])

    def test_rule_does_not_fire_at_61(self):
        d = select_pedagogical_strategy(exam_days_remaining=61)
        self.assertNotIn("exam_approaching", d["rules_applied"])


class TestLowConfidenceRule(unittest.TestCase):
    """rule_id: low_confidence — learner_confidence in {"low", "baja"}."""

    def test_host_increases_when_confidence_low(self):
        d = select_pedagogical_strategy(learner_confidence="low")
        baseline = _weight(_baseline(), "host")
        self.assertGreater(_weight(d, "host"), baseline)

    def test_challenger_decreases_when_confidence_low(self):
        d = select_pedagogical_strategy(learner_confidence="low")
        baseline = _weight(_baseline(), "challenger")
        self.assertLess(_weight(d, "challenger"), baseline)

    def test_rule_fires_for_spanish_baja(self):
        d = select_pedagogical_strategy(learner_confidence="baja")
        self.assertIn("low_confidence", d["rules_applied"])

    def test_rule_fires_case_insensitive_LOW(self):
        d = select_pedagogical_strategy(learner_confidence="LOW")
        self.assertIn("low_confidence", d["rules_applied"])

    def test_rule_does_not_fire_for_high(self):
        d = select_pedagogical_strategy(learner_confidence="high")
        self.assertNotIn("low_confidence", d["rules_applied"])

    def test_rule_does_not_fire_for_medium(self):
        d = select_pedagogical_strategy(learner_confidence="medium")
        self.assertNotIn("low_confidence", d["rules_applied"])


class TestCausalGapRule(unittest.TestCase):
    """rule_id: causal_gap — recent_error_type == "causal_gap"."""

    def test_scientist_increases_for_causal_gap(self):
        d = select_pedagogical_strategy(recent_error_type="causal_gap")
        baseline = _weight(_baseline(), "scientist")
        self.assertGreater(_weight(d, "scientist"), baseline)

    def test_rule_fires_for_causal_gap(self):
        d = select_pedagogical_strategy(recent_error_type="causal_gap")
        self.assertIn("causal_gap", d["rules_applied"])

    def test_cartographer_increases_for_causal_gap(self):
        d = select_pedagogical_strategy(recent_error_type="causal_gap")
        baseline = _weight(_baseline(), "cartographer")
        self.assertGreater(_weight(d, "cartographer"), baseline)

    def test_rule_does_not_fire_for_other_errors(self):
        d = select_pedagogical_strategy(recent_error_type="vague_answer")
        self.assertNotIn("causal_gap", d["rules_applied"])


class TestRegionalConfusionRule(unittest.TestCase):
    """rule_id: regional_confusion — recent_error_type == "regional_confusion"."""

    def test_cartographer_increases_for_regional_confusion(self):
        d = select_pedagogical_strategy(recent_error_type="regional_confusion")
        baseline = _weight(_baseline(), "cartographer")
        self.assertGreater(_weight(d, "cartographer"), baseline)

    def test_rule_fires_for_regional_confusion(self):
        d = select_pedagogical_strategy(recent_error_type="regional_confusion")
        self.assertIn("regional_confusion", d["rules_applied"])

    def test_cartographer_is_dominant_after_regional_confusion(self):
        d = select_pedagogical_strategy(recent_error_type="regional_confusion")
        cartographer_w = _weight(d, "cartographer")
        other_weights = [_weight(d, fn) for fn in
                         ["scientist", "host", "storyteller", "critic", "challenger"]]
        self.assertEqual(
            cartographer_w, max([cartographer_w] + other_weights),
            "cartographer should dominate after regional_confusion."
        )


class TestVagueAnswerRule(unittest.TestCase):
    """rule_id: vague_answer — recent_error_type == "vague_answer"."""

    def test_critic_increases_for_vague_answer(self):
        d = select_pedagogical_strategy(recent_error_type="vague_answer")
        baseline = _weight(_baseline(), "critic")
        self.assertGreater(_weight(d, "critic"), baseline)

    def test_challenger_increases_for_vague_answer(self):
        d = select_pedagogical_strategy(recent_error_type="vague_answer")
        baseline = _weight(_baseline(), "challenger")
        self.assertGreater(_weight(d, "challenger"), baseline)

    def test_rule_fires_for_vague_answer(self):
        d = select_pedagogical_strategy(recent_error_type="vague_answer")
        self.assertIn("vague_answer", d["rules_applied"])


class TestMemorizationWithoutReasoningRule(unittest.TestCase):
    """rule_id: memorization_without_reasoning."""

    def test_challenger_increases(self):
        d = select_pedagogical_strategy(recent_error_type="memorization_without_reasoning")
        baseline = _weight(_baseline(), "challenger")
        self.assertGreater(_weight(d, "challenger"), baseline)

    def test_scientist_increases(self):
        d = select_pedagogical_strategy(recent_error_type="memorization_without_reasoning")
        baseline = _weight(_baseline(), "scientist")
        self.assertGreater(_weight(d, "scientist"), baseline)

    def test_rule_fires(self):
        d = select_pedagogical_strategy(recent_error_type="memorization_without_reasoning")
        self.assertIn("memorization_without_reasoning", d["rules_applied"])


class TestDistinctionGoalRule(unittest.TestCase):
    """rule_id: distinction_goal — learning_goal == "distinction"."""

    def test_scientist_increases(self):
        d = select_pedagogical_strategy(learning_goal="distinction")
        baseline = _weight(_baseline(), "scientist")
        self.assertGreater(_weight(d, "scientist"), baseline)

    def test_critic_increases(self):
        d = select_pedagogical_strategy(learning_goal="distinction")
        baseline = _weight(_baseline(), "critic")
        self.assertGreater(_weight(d, "critic"), baseline)

    def test_challenger_increases(self):
        d = select_pedagogical_strategy(learning_goal="distinction")
        baseline = _weight(_baseline(), "challenger")
        self.assertGreater(_weight(d, "challenger"), baseline)

    def test_rule_fires(self):
        d = select_pedagogical_strategy(learning_goal="distinction")
        self.assertIn("distinction_goal", d["rules_applied"])

    def test_distinction_goal_does_not_activate_examiner_scoring(self):
        d = select_pedagogical_strategy(learning_goal="distinction")
        self.assertFalse(d["governance"]["examiner_scoring_allowed"])

    def test_distinction_goal_does_not_activate_safe_for_examiner(self):
        d = select_pedagogical_strategy(learning_goal="distinction")
        self.assertFalse(d["governance"]["safe_for_examiner"])


class TestClampingInvariants(unittest.TestCase):
    """Host never below HOST_MIN_WEIGHT. All functions never below FUNCTION_MIN_WEIGHT."""

    def test_host_never_below_minimum_under_exam_imminent(self):
        d = select_pedagogical_strategy(exam_days_remaining=1)
        self.assertGreaterEqual(_weight(d, "host"), HOST_MIN_WEIGHT)

    def test_host_never_below_minimum_under_distinction_goal(self):
        d = select_pedagogical_strategy(learning_goal="distinction")
        self.assertGreaterEqual(_weight(d, "host"), HOST_MIN_WEIGHT)

    def test_all_functions_at_or_above_minimum_under_combined_rules(self):
        d = select_pedagogical_strategy(
            exam_days_remaining=7,
            learning_goal="distinction",
            recent_error_type="vague_answer",
        )
        for fn, w in d["function_weights"].items():
            floor = HOST_MIN_WEIGHT if fn == "host" else FUNCTION_MIN_WEIGHT
            self.assertGreaterEqual(w, floor, f"{fn} weight {w:.4f} below floor {floor}")

    def test_clamp_and_normalise_host_floor(self):
        weights = {fn: 0.0 for fn in
                   ["cartographer", "scientist", "host", "storyteller", "critic", "challenger"]}
        result = _clamp_and_normalise(weights)
        self.assertGreaterEqual(result["host"], HOST_MIN_WEIGHT)

    def test_clamp_and_normalise_function_floor(self):
        weights = {fn: 0.0 for fn in
                   ["cartographer", "scientist", "host", "storyteller", "critic", "challenger"]}
        result = _clamp_and_normalise(weights)
        for fn, w in result.items():
            floor = HOST_MIN_WEIGHT if fn == "host" else FUNCTION_MIN_WEIGHT
            self.assertGreaterEqual(w, floor)


class TestWeightNormalisationAfterAdjustment(unittest.TestCase):
    def _assert_sums_to_one(self, directive: dict):
        total = sum(directive["function_weights"].values())
        self.assertAlmostEqual(total, 1.0, places=4,
                               msg=f"Weights sum to {total:.6f}, expected 1.0")

    def test_weights_sum_to_one_no_context(self):
        self._assert_sums_to_one(_baseline())

    def test_weights_sum_to_one_exam_imminent(self):
        self._assert_sums_to_one(select_pedagogical_strategy(exam_days_remaining=7))

    def test_weights_sum_to_one_low_confidence(self):
        self._assert_sums_to_one(select_pedagogical_strategy(learner_confidence="low"))

    def test_weights_sum_to_one_multiple_rules(self):
        d = select_pedagogical_strategy(
            exam_days_remaining=10,
            learner_confidence="low",
            learning_goal="distinction",
            recent_error_type="causal_gap",
        )
        self._assert_sums_to_one(d)


class TestColdStart(unittest.TestCase):
    def test_cold_start_returns_default_profile(self):
        d = select_pedagogical_strategy()
        self.assertEqual(d["profile_id"], "default")
        self.assertEqual(d["source"], "default")

    def test_cold_start_rules_applied_is_empty(self):
        d = select_pedagogical_strategy()
        self.assertEqual(d["rules_applied"], [])

    def test_cold_start_governance_clean(self):
        d = select_pedagogical_strategy()
        self.assertFalse(d["governance"]["examiner_scoring_allowed"])
        self.assertFalse(d["governance"]["safe_for_examiner"])
        self.assertFalse(d["governance"]["uses_llm"])


class TestCompositeRules(unittest.TestCase):
    def test_multiple_rules_can_fire_simultaneously(self):
        d = select_pedagogical_strategy(
            exam_days_remaining=7,
            learning_goal="distinction",
        )
        self.assertIn("exam_imminent", d["rules_applied"])
        self.assertIn("distinction_goal", d["rules_applied"])

    def test_rules_applied_reflects_all_fired_rules(self):
        d = select_pedagogical_strategy(
            exam_days_remaining=30,
            learner_confidence="low",
            recent_error_type="causal_gap",
        )
        self.assertIn("exam_approaching", d["rules_applied"])
        self.assertIn("low_confidence", d["rules_applied"])
        self.assertIn("causal_gap", d["rules_applied"])


class TestDerivedSignals(unittest.TestCase):
    def test_feedback_intensity_low_when_critic_and_challenger_low(self):
        # mentor mode baseline — critic 0.05, challenger 0.05 → combined 0.10 → "low"
        d = select_pedagogical_strategy(tutor_mode="mentor")
        self.assertEqual(d["feedback_intensity"], "low")

    def test_feedback_intensity_high_when_exam_imminent(self):
        d = select_pedagogical_strategy(exam_days_remaining=7)
        self.assertEqual(d["feedback_intensity"], "high")

    def test_causal_depth_required_deep_when_scientist_dominant(self):
        d = select_pedagogical_strategy(
            tutor_role="investigador_causalidad",
            recent_error_type="causal_gap",
        )
        self.assertEqual(d["causal_depth_required"], "deep")

    def test_causal_depth_required_minimal_when_scientist_low(self):
        # mentor_fundamentos has scientist=0.15 (below 0.20 threshold after normalisation)
        d = select_pedagogical_strategy(tutor_role="mentor_fundamentos")
        self.assertIn(d["causal_depth_required"], ["minimal", "standard"])

    def test_emotional_support_high_when_host_dominant(self):
        d = select_pedagogical_strategy(tutor_role="mentor_fundamentos")
        self.assertEqual(d["emotional_support_level"], "high")

    def test_emotional_support_low_when_host_reduced(self):
        d = select_pedagogical_strategy(exam_days_remaining=7, learning_goal="distinction")
        self.assertIn(d["emotional_support_level"], ["low", "medium"])

    def test_challenge_level_high_when_challenger_dominant(self):
        d = select_pedagogical_strategy(exam_days_remaining=7, learning_goal="distinction")
        self.assertEqual(d["challenge_level"], "high")

    def test_challenge_level_low_for_foundational_mentor(self):
        d = select_pedagogical_strategy(tutor_role="mentor_fundamentos")
        self.assertEqual(d["challenge_level"], "low")

    def test_preferred_question_type_contextual_for_regional_confusion(self):
        d = select_pedagogical_strategy(recent_error_type="regional_confusion")
        self.assertEqual(d["preferred_question_type"], "contextual")

    def test_preferred_question_type_causal_for_causal_specialist(self):
        d = select_pedagogical_strategy(
            tutor_role="investigador_causalidad",
            recent_error_type="causal_gap",
        )
        self.assertEqual(d["preferred_question_type"], "causal")

    def test_remediation_style_scaffolded_for_host_dominant(self):
        d = select_pedagogical_strategy(tutor_role="mentor_fundamentos")
        self.assertEqual(d["remediation_style"], "scaffolded")


class TestDeterminism(unittest.TestCase):
    def test_same_input_produces_same_output(self):
        kwargs = dict(
            tutor_role="revisor_respuestas",
            exam_days_remaining=20,
            learner_confidence="low",
            recent_error_type="vague_answer",
        )
        d1 = select_pedagogical_strategy(**kwargs)
        d2 = select_pedagogical_strategy(**kwargs)
        self.assertEqual(d1["function_weights"], d2["function_weights"])
        self.assertEqual(d1["rules_applied"], d2["rules_applied"])
        self.assertEqual(d1["feedback_intensity"], d2["feedback_intensity"])


class TestRuleEvaluation(unittest.TestCase):
    def test_lte_operator(self):
        rule = {"condition_field": "exam_days_remaining", "condition_op": "lte",
                "condition_value": 14}
        self.assertTrue(_rule_applies(rule, {"exam_days_remaining": 14}))
        self.assertTrue(_rule_applies(rule, {"exam_days_remaining": 0}))
        self.assertFalse(_rule_applies(rule, {"exam_days_remaining": 15}))
        self.assertFalse(_rule_applies(rule, {}))

    def test_range_hi_exclusive_operator(self):
        rule = {"condition_field": "exam_days_remaining",
                "condition_op": "range_hi_exclusive",
                "condition_value": (14, 60)}
        self.assertTrue(_rule_applies(rule, {"exam_days_remaining": 15}))
        self.assertTrue(_rule_applies(rule, {"exam_days_remaining": 60}))
        self.assertFalse(_rule_applies(rule, {"exam_days_remaining": 14}))
        self.assertFalse(_rule_applies(rule, {"exam_days_remaining": 61}))

    def test_in_set_operator(self):
        rule = {"condition_field": "learner_confidence", "condition_op": "in_set",
                "condition_value": {"low", "baja"}}
        self.assertTrue(_rule_applies(rule, {"learner_confidence": "low"}))
        self.assertTrue(_rule_applies(rule, {"learner_confidence": "baja"}))
        self.assertTrue(_rule_applies(rule, {"learner_confidence": "BAJA"}))
        self.assertFalse(_rule_applies(rule, {"learner_confidence": "high"}))
        self.assertFalse(_rule_applies(rule, {}))

    def test_eq_operator(self):
        rule = {"condition_field": "recent_error_type", "condition_op": "eq",
                "condition_value": "causal_gap"}
        self.assertTrue(_rule_applies(rule, {"recent_error_type": "causal_gap"}))
        self.assertTrue(_rule_applies(rule, {"recent_error_type": "CAUSAL_GAP"}))
        self.assertFalse(_rule_applies(rule, {"recent_error_type": "vague_answer"}))
        self.assertFalse(_rule_applies(rule, {}))

    def test_all_rule_ids_are_unique(self):
        ids = [r["rule_id"] for r in ADJUSTMENT_RULES]
        self.assertEqual(len(ids), len(set(ids)), "Duplicate rule_ids detected.")


if __name__ == "__main__":
    unittest.main()
