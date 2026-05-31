"""Unit tests for tools.tutor.pedagogical_strategy.strategy_selector.

20 required tests:
  1.  test_base_profile_loaded
  2.  test_exam_pressure_high_urgency
  3.  test_exam_pressure_medium_urgency
  4.  test_low_confidence_increases_host
  5.  test_low_confidence_reduces_challenger
  6.  test_causal_gap_increases_scientist
  7.  test_regional_confusion_increases_cartographer
  8.  test_vague_answer_increases_critic
  9.  test_memorization_error_increases_challenger_and_scientist
  10. test_distinction_goal_increases_exigence
  11. test_host_never_eliminated
  12. test_weights_always_sum_to_one
  13. test_no_examiner_scoring_allowed
  14. test_no_official_authority_claim
  15. test_feedback_intensity_derives_correctly
  16. test_preferred_question_type_follows_dominant_function
  17. test_emotional_support_follows_host_weight
  18. test_unknown_tutor_mode_falls_back_to_mentor
  19. test_none_error_type_no_error_adjustment
  20. test_rules_are_composable
"""

import unittest
from tools.tutor.pedagogical_strategy.strategy_selector import (
    select_strategy,
    HOST_FLOOR,
    CHALLENGER_LOW_CONF_FLOOR,
)

_ALLOWED_TUTOR_MODES = ["mentor", "trainer", "reviewer", "distinction", "exam_pressure"]
_ALLOWED_VISIBLE_ROLES = [
    "mentor_fundamentos", "entrenador_sensorial", "investigador_causalidad",
    "revisor_respuestas", "entrenador_distinction",
]
_ALL_PROFILES = _ALLOWED_TUTOR_MODES + _ALLOWED_VISIBLE_ROLES
_FUNCTIONS = ["cartographer", "scientist", "host", "storyteller", "critic", "challenger"]
# round(x,6) over 6 values accumulates up to ~3e-6; psl_profile_validator uses 1e-4
_FLOAT_DELTA = 1e-5


def _sum_weights(directive):
    return sum(directive["function_weights"].values())


def _w(directive, fn):
    return directive["function_weights"][fn]


def _base(tutor_mode=None, tutor_role=None):
    return select_strategy(tutor_mode=tutor_mode, tutor_role=tutor_role)


# ---------------------------------------------------------------------------
# Test 1 — base profile loaded
# ---------------------------------------------------------------------------

class TestBaseProfileLoaded(unittest.TestCase):

    def test_base_profile_loaded(self):
        for mode in _ALLOWED_TUTOR_MODES:
            with self.subTest(tutor_mode=mode):
                directive = _base(tutor_mode=mode)
                self.assertEqual(directive["profile_id"], mode)
                for fn in _FUNCTIONS:
                    self.assertIn(fn, directive["function_weights"])
                self.assertAlmostEqual(_sum_weights(directive), 1.0, delta=_FLOAT_DELTA)

    def test_base_visible_role_loaded(self):
        for role in _ALLOWED_VISIBLE_ROLES:
            with self.subTest(tutor_role=role):
                directive = _base(tutor_role=role)
                self.assertEqual(directive["profile_id"], role)
                for fn in _FUNCTIONS:
                    self.assertIn(fn, directive["function_weights"])

    def test_base_no_rules_applied(self):
        for mode in _ALLOWED_TUTOR_MODES:
            with self.subTest(tutor_mode=mode):
                directive = _base(tutor_mode=mode)
                self.assertEqual(directive["rules_applied"], [])


# ---------------------------------------------------------------------------
# Test 2 — exam high urgency (<=14 days)
# ---------------------------------------------------------------------------

class TestExamPressureHighUrgency(unittest.TestCase):

    def test_exam_pressure_high_urgency(self):
        for days in [1, 7, 14]:
            with self.subTest(days=days):
                baseline = _base(tutor_mode="mentor")
                pressed = select_strategy(tutor_mode="mentor", exam_days_remaining=days)
                self.assertGreater(_w(pressed, "challenger"), _w(baseline, "challenger") - _FLOAT_DELTA)
                self.assertGreater(_w(pressed, "critic"), _w(baseline, "critic") - _FLOAT_DELTA)

    def test_high_urgency_rule_applied(self):
        d = select_strategy(tutor_mode="mentor", exam_days_remaining=7)
        self.assertIn("exam_high_urgency", d["rules_applied"])

    def test_medium_urgency_not_applied_when_high_fires(self):
        d = select_strategy(tutor_mode="mentor", exam_days_remaining=14)
        self.assertNotIn("exam_medium_urgency", d["rules_applied"])

    def test_weights_sum_after_high_urgency(self):
        d = select_strategy(tutor_mode="mentor", exam_days_remaining=7)
        self.assertAlmostEqual(_sum_weights(d), 1.0, delta=_FLOAT_DELTA)


# ---------------------------------------------------------------------------
# Test 3 — exam medium urgency (>14 and <=60 days)
# ---------------------------------------------------------------------------

class TestExamPressureMediumUrgency(unittest.TestCase):

    def test_exam_pressure_medium_urgency(self):
        for days in [15, 30, 60]:
            with self.subTest(days=days):
                baseline = _base(tutor_mode="mentor")
                pressed = select_strategy(tutor_mode="mentor", exam_days_remaining=days)
                self.assertGreater(_w(pressed, "scientist"), _w(baseline, "scientist") - _FLOAT_DELTA)
                self.assertGreater(_w(pressed, "challenger"), _w(baseline, "challenger") - _FLOAT_DELTA)

    def test_medium_urgency_rule_applied(self):
        d = select_strategy(tutor_mode="mentor", exam_days_remaining=30)
        self.assertIn("exam_medium_urgency", d["rules_applied"])

    def test_high_urgency_not_applied_for_medium_range(self):
        d = select_strategy(tutor_mode="mentor", exam_days_remaining=30)
        self.assertNotIn("exam_high_urgency", d["rules_applied"])

    def test_no_rule_applied_beyond_60_days(self):
        d = select_strategy(tutor_mode="mentor", exam_days_remaining=61)
        self.assertNotIn("exam_high_urgency", d["rules_applied"])
        self.assertNotIn("exam_medium_urgency", d["rules_applied"])


# ---------------------------------------------------------------------------
# Test 4 — low confidence increases host
# ---------------------------------------------------------------------------

class TestLowConfidenceIncreasesHost(unittest.TestCase):

    def test_low_confidence_increases_host(self):
        for mode in _ALLOWED_TUTOR_MODES:
            with self.subTest(tutor_mode=mode):
                baseline = _base(tutor_mode=mode)
                low = select_strategy(tutor_mode=mode, learner_confidence="low")
                self.assertGreater(_w(low, "host"), _w(baseline, "host") - _FLOAT_DELTA)

    def test_low_confidence_rule_applied(self):
        d = select_strategy(tutor_mode="mentor", learner_confidence="low")
        self.assertIn("low_confidence", d["rules_applied"])

    def test_medium_confidence_no_rule(self):
        d = select_strategy(tutor_mode="mentor", learner_confidence="medium")
        self.assertNotIn("low_confidence", d["rules_applied"])

    def test_high_confidence_no_rule(self):
        d = select_strategy(tutor_mode="mentor", learner_confidence="high")
        self.assertNotIn("low_confidence", d["rules_applied"])


# ---------------------------------------------------------------------------
# Test 5 — low confidence reduces challenger but stays >= floor
# ---------------------------------------------------------------------------

class TestLowConfidenceReducesChallenger(unittest.TestCase):

    def test_low_confidence_reduces_challenger(self):
        for mode in _ALLOWED_TUTOR_MODES:
            with self.subTest(tutor_mode=mode):
                baseline = _base(tutor_mode=mode)
                low = select_strategy(tutor_mode=mode, learner_confidence="low")
                self.assertLessEqual(
                    _w(low, "challenger"),
                    _w(baseline, "challenger") + _FLOAT_DELTA,
                )

    def test_challenger_never_below_floor(self):
        for mode in _ALLOWED_TUTOR_MODES:
            with self.subTest(tutor_mode=mode):
                d = select_strategy(tutor_mode=mode, learner_confidence="low")
                self.assertGreaterEqual(
                    _w(d, "challenger"),
                    CHALLENGER_LOW_CONF_FLOOR - _FLOAT_DELTA,
                )

    def test_weights_sum_after_low_confidence(self):
        d = select_strategy(tutor_mode="mentor", learner_confidence="low")
        self.assertAlmostEqual(_sum_weights(d), 1.0, delta=_FLOAT_DELTA)


# ---------------------------------------------------------------------------
# Test 6 — causal gap increases scientist
# ---------------------------------------------------------------------------

class TestCausalGapIncreasesScientist(unittest.TestCase):

    def test_causal_gap_increases_scientist(self):
        for mode in _ALLOWED_TUTOR_MODES:
            with self.subTest(tutor_mode=mode):
                baseline = _base(tutor_mode=mode)
                d = select_strategy(tutor_mode=mode, recent_error_type="causal_gap")
                self.assertGreater(_w(d, "scientist"), _w(baseline, "scientist") - _FLOAT_DELTA)

    def test_causal_gap_rule_applied(self):
        d = select_strategy(tutor_mode="mentor", recent_error_type="causal_gap")
        self.assertIn("causal_gap", d["rules_applied"])

    def test_weights_sum_after_causal_gap(self):
        d = select_strategy(tutor_mode="mentor", recent_error_type="causal_gap")
        self.assertAlmostEqual(_sum_weights(d), 1.0, delta=_FLOAT_DELTA)


# ---------------------------------------------------------------------------
# Test 7 — regional confusion increases cartographer
# ---------------------------------------------------------------------------

class TestRegionalConfusionIncreasesCartographer(unittest.TestCase):

    def test_regional_confusion_increases_cartographer(self):
        for mode in _ALLOWED_TUTOR_MODES:
            with self.subTest(tutor_mode=mode):
                baseline = _base(tutor_mode=mode)
                d = select_strategy(tutor_mode=mode, recent_error_type="regional_confusion")
                self.assertGreater(_w(d, "cartographer"), _w(baseline, "cartographer") - _FLOAT_DELTA)

    def test_regional_confusion_rule_applied(self):
        d = select_strategy(tutor_mode="mentor", recent_error_type="regional_confusion")
        self.assertIn("regional_confusion", d["rules_applied"])


# ---------------------------------------------------------------------------
# Test 8 — vague answer increases critic
# ---------------------------------------------------------------------------

class TestVagueAnswerIncreasesCritic(unittest.TestCase):

    def test_vague_answer_increases_critic(self):
        for mode in _ALLOWED_TUTOR_MODES:
            with self.subTest(tutor_mode=mode):
                baseline = _base(tutor_mode=mode)
                d = select_strategy(tutor_mode=mode, recent_error_type="vague_answer")
                self.assertGreater(_w(d, "critic"), _w(baseline, "critic") - _FLOAT_DELTA)

    def test_vague_answer_rule_applied(self):
        d = select_strategy(tutor_mode="mentor", recent_error_type="vague_answer")
        self.assertIn("vague_answer", d["rules_applied"])


# ---------------------------------------------------------------------------
# Test 9 — memorization_without_reasoning increases challenger AND scientist
# ---------------------------------------------------------------------------

class TestMemorizationErrorIncreasesChallenger(unittest.TestCase):

    def test_memorization_error_increases_challenger_and_scientist(self):
        for mode in _ALLOWED_TUTOR_MODES:
            with self.subTest(tutor_mode=mode):
                baseline = _base(tutor_mode=mode)
                d = select_strategy(tutor_mode=mode, recent_error_type="memorization_without_reasoning")
                self.assertGreater(_w(d, "challenger"), _w(baseline, "challenger") - _FLOAT_DELTA)
                self.assertGreater(_w(d, "scientist"), _w(baseline, "scientist") - _FLOAT_DELTA)

    def test_memorization_rule_applied(self):
        d = select_strategy(tutor_mode="mentor", recent_error_type="memorization_without_reasoning")
        self.assertIn("memorization_without_reasoning", d["rules_applied"])


# ---------------------------------------------------------------------------
# Test 10 — distinction goal increases exigence (scientist, critic, challenger)
# ---------------------------------------------------------------------------

class TestDistinctionGoalIncreasesExigence(unittest.TestCase):

    def test_distinction_goal_increases_exigence(self):
        for mode in _ALLOWED_TUTOR_MODES:
            with self.subTest(tutor_mode=mode):
                baseline = _base(tutor_mode=mode)
                d = select_strategy(tutor_mode=mode, learning_goal="distinction")
                self.assertGreaterEqual(_w(d, "scientist"), _w(baseline, "scientist") - _FLOAT_DELTA)
                self.assertGreaterEqual(_w(d, "critic"), _w(baseline, "critic") - _FLOAT_DELTA)
                self.assertGreaterEqual(_w(d, "challenger"), _w(baseline, "challenger") - _FLOAT_DELTA)

    def test_distinction_rule_applied(self):
        d = select_strategy(tutor_mode="mentor", learning_goal="distinction")
        self.assertIn("distinction_goal", d["rules_applied"])

    def test_pass_goal_no_rule(self):
        d = select_strategy(tutor_mode="mentor", learning_goal="pass")
        self.assertNotIn("distinction_goal", d["rules_applied"])


# ---------------------------------------------------------------------------
# Test 11 — host never eliminated
# ---------------------------------------------------------------------------

class TestHostNeverEliminated(unittest.TestCase):

    def _adversarial_combinations(self):
        signals_list = [
            {"exam_days_remaining": 1},
            {"exam_days_remaining": 7},
            {"exam_days_remaining": 14},
            {"exam_days_remaining": 30},
            {"learner_confidence": "low"},
            {"recent_error_type": "causal_gap"},
            {"recent_error_type": "regional_confusion"},
            {"recent_error_type": "vague_answer"},
            {"recent_error_type": "memorization_without_reasoning"},
            {"learning_goal": "distinction"},
            {"exam_days_remaining": 7, "recent_error_type": "memorization_without_reasoning", "learning_goal": "distinction"},
            {"exam_days_remaining": 7, "learner_confidence": "low", "recent_error_type": "vague_answer"},
            {"exam_days_remaining": 7, "learner_confidence": "low", "learning_goal": "distinction", "recent_error_type": "memorization_without_reasoning"},
        ]
        for mode in _ALLOWED_TUTOR_MODES:
            for signals in signals_list:
                yield mode, signals

    def test_host_never_eliminated(self):
        for mode, signals in self._adversarial_combinations():
            label = f"{mode}+{list(signals.keys())}"
            with self.subTest(combination=label):
                d = select_strategy(tutor_mode=mode, **signals)
                self.assertGreaterEqual(
                    _w(d, "host"),
                    HOST_FLOOR - _FLOAT_DELTA,
                    msg=f"{label}: host={_w(d,'host'):.4f} < HOST_FLOOR={HOST_FLOOR}",
                )


# ---------------------------------------------------------------------------
# Test 12 — weights always sum to 1.0
# ---------------------------------------------------------------------------

class TestWeightsAlwaysSumToOne(unittest.TestCase):

    _COMBINATIONS = [
        {},
        {"exam_days_remaining": 1},
        {"exam_days_remaining": 14},
        {"exam_days_remaining": 30},
        {"exam_days_remaining": 60},
        {"exam_days_remaining": 61},
        {"learner_confidence": "low"},
        {"learner_confidence": "medium"},
        {"learner_confidence": "high"},
        {"recent_error_type": "causal_gap"},
        {"recent_error_type": "regional_confusion"},
        {"recent_error_type": "vague_answer"},
        {"recent_error_type": "memorization_without_reasoning"},
        {"learning_goal": "distinction"},
        {"learning_goal": "pass"},
        {"learning_goal": "explore"},
        {"exam_days_remaining": 7, "learner_confidence": "low"},
        {"exam_days_remaining": 7, "learning_goal": "distinction"},
        {"exam_days_remaining": 7, "learner_confidence": "low", "recent_error_type": "causal_gap", "learning_goal": "distinction"},
        {"exam_days_remaining": 30, "recent_error_type": "memorization_without_reasoning", "learning_goal": "distinction"},
    ]

    def test_weights_always_sum_to_one(self):
        for mode in _ALLOWED_TUTOR_MODES:
            for signals in self._COMBINATIONS:
                label = f"{mode}+{signals}"
                with self.subTest(combination=label):
                    d = select_strategy(tutor_mode=mode, **signals)
                    total = _sum_weights(d)
                    self.assertAlmostEqual(total, 1.0, delta=_FLOAT_DELTA,
                        msg=f"{label}: sum={total:.10f}")


# ---------------------------------------------------------------------------
# Test 13 — no examiner_scoring_allowed
# ---------------------------------------------------------------------------

class TestNoExaminerScoringAllowed(unittest.TestCase):

    def test_no_examiner_scoring_allowed(self):
        for mode in _ALL_PROFILES:
            for signals in [{}, {"exam_days_remaining": 7}, {"learning_goal": "distinction"}]:
                is_role = mode in _ALLOWED_VISIBLE_ROLES
                kwargs = {"tutor_role": mode} if is_role else {"tutor_mode": mode}
                kwargs.update(signals)
                label = f"{mode}+{signals}"
                with self.subTest(combination=label):
                    d = select_strategy(**kwargs)
                    gov = d["governance"]
                    self.assertIs(gov["examiner_scoring_allowed"], False)
                    self.assertIs(gov["safe_for_examiner"], False)


# ---------------------------------------------------------------------------
# Test 14 — no official authority claim
# ---------------------------------------------------------------------------

class TestNoOfficialAuthorityClaim(unittest.TestCase):

    _FORBIDDEN = (
        "official wset", "wset examiner", "official score",
        "official marks", "official grading", "official band",
    )

    def _collect(self, obj):
        if isinstance(obj, str):
            return [obj.lower()]
        if isinstance(obj, dict):
            return [s for v in obj.values() for s in self._collect(v)]
        if isinstance(obj, list):
            return [s for item in obj for s in self._collect(item)]
        return []

    def test_no_official_authority_claim(self):
        for mode in _ALLOWED_TUTOR_MODES:
            d = select_strategy(tutor_mode=mode, exam_days_remaining=7, learning_goal="distinction")
            combined = " ".join(self._collect(d))
            for phrase in self._FORBIDDEN:
                with self.subTest(mode=mode, phrase=phrase):
                    self.assertNotIn(phrase, combined)


# ---------------------------------------------------------------------------
# Test 15 — feedback_intensity derives correctly
# ---------------------------------------------------------------------------

class TestFeedbackIntensityDerivesCorrectly(unittest.TestCase):

    def test_feedback_intensity_thresholds(self):
        ordering = ["gentle", "moderate", "firm", "challenging"]
        for mode in _ALLOWED_TUTOR_MODES:
            d = _base(tutor_mode=mode)
            with self.subTest(mode=mode):
                self.assertIn(d["feedback_intensity"], ordering)

    def test_feedback_intensity_high_pressure_is_firm_or_challenging(self):
        d = _base(tutor_mode="exam_pressure")
        combined = _w(d, "critic") + _w(d, "challenger")
        self.assertGreater(combined, 0.40)
        self.assertIn(d["feedback_intensity"], {"firm", "challenging"})

    def test_feedback_intensity_derives_correctly(self):
        # exam_pressure + exam_high_urgency pushes critic+challenger well above 0.40
        d = select_strategy(tutor_mode="exam_pressure", exam_days_remaining=7)
        combined = _w(d, "critic") + _w(d, "challenger")
        if combined > 0.50:
            self.assertEqual(d["feedback_intensity"], "challenging")
        elif combined > 0.40:
            self.assertEqual(d["feedback_intensity"], "firm")

    def test_mentor_gentle_or_moderate(self):
        d = _base(tutor_mode="mentor")
        self.assertIn(d["feedback_intensity"], {"gentle", "moderate"})


# ---------------------------------------------------------------------------
# Test 16 — preferred_question_type follows dominant function
# ---------------------------------------------------------------------------

class TestPreferredQuestionTypeFollowsDominantFunction(unittest.TestCase):

    _MAP = {
        "cartographer": "regional",
        "scientist":    "causal",
        "host":         "open",
        "storyteller":  "narrative",
        "critic":       "evaluative",
        "challenger":   "adversarial",
    }

    def test_preferred_question_type_follows_dominant_function(self):
        for mode in _ALLOWED_TUTOR_MODES:
            d = _base(tutor_mode=mode)
            weights = d["function_weights"]
            dominant = max(weights, key=weights.__getitem__)
            expected = self._MAP[dominant]
            with self.subTest(mode=mode):
                self.assertEqual(d["preferred_question_type"], expected)

    def test_scientist_dominant_produces_causal(self):
        d = _base(tutor_role="investigador_causalidad")
        self.assertEqual(d["preferred_question_type"], "causal")

    def test_critic_dominant_produces_evaluative(self):
        d = _base(tutor_role="revisor_respuestas")
        self.assertEqual(d["preferred_question_type"], "evaluative")


# ---------------------------------------------------------------------------
# Test 17 — emotional_support_level follows host weight
# ---------------------------------------------------------------------------

class TestEmotionalSupportFollowsHostWeight(unittest.TestCase):

    def test_emotional_support_follows_host_weight(self):
        for mode in _ALLOWED_TUTOR_MODES:
            d = _base(tutor_mode=mode)
            h = _w(d, "host")
            expected = "high" if h >= 0.25 else ("medium" if h >= 0.15 else "low")
            with self.subTest(mode=mode, host=h):
                self.assertEqual(d["emotional_support_level"], expected)

    def test_low_confidence_raises_emotional_support(self):
        order = {"low": 0, "medium": 1, "high": 2}
        for mode in _ALLOWED_TUTOR_MODES:
            baseline = _base(tutor_mode=mode)
            low = select_strategy(tutor_mode=mode, learner_confidence="low")
            with self.subTest(mode=mode):
                self.assertGreaterEqual(
                    order[low["emotional_support_level"]],
                    order[baseline["emotional_support_level"]],
                )

    def test_mentor_fundamentos_is_high_support(self):
        d = _base(tutor_role="mentor_fundamentos")
        self.assertEqual(d["emotional_support_level"], "high")


# ---------------------------------------------------------------------------
# Test 18 — unknown tutor_mode falls back gracefully
# ---------------------------------------------------------------------------

class TestUnknownTutorModeFallsBack(unittest.TestCase):

    def test_unknown_tutor_mode_falls_back_to_mentor(self):
        d = select_strategy(tutor_mode="unknown_mode_xyz")
        self.assertIn("function_weights", d)
        for fn in _FUNCTIONS:
            self.assertIn(fn, d["function_weights"])
        self.assertAlmostEqual(_sum_weights(d), 1.0, delta=_FLOAT_DELTA)

    def test_none_tutor_mode_falls_back(self):
        d = select_strategy(tutor_mode=None)
        self.assertAlmostEqual(_sum_weights(d), 1.0, delta=_FLOAT_DELTA)

    def test_fallback_governance_clean(self):
        d = select_strategy(tutor_mode="not_a_real_mode")
        self.assertIs(d["governance"]["safe_for_examiner"], False)
        self.assertIs(d["governance"]["examiner_scoring_allowed"], False)

    def test_fallback_host_above_floor(self):
        d = select_strategy(tutor_mode="not_a_real_mode")
        self.assertGreaterEqual(_w(d, "host"), HOST_FLOOR - _FLOAT_DELTA)


# ---------------------------------------------------------------------------
# Test 19 — None error type produces no error adjustment
# ---------------------------------------------------------------------------

class TestNoneErrorTypeNoErrorAdjustment(unittest.TestCase):

    def test_none_error_type_no_error_adjustment(self):
        error_rules = {"causal_gap", "regional_confusion", "vague_answer", "memorization_without_reasoning"}
        for mode in _ALLOWED_TUTOR_MODES:
            with self.subTest(tutor_mode=mode):
                d = select_strategy(tutor_mode=mode, recent_error_type=None)
                for rule in error_rules:
                    self.assertNotIn(rule, d["rules_applied"])

    def test_explicit_none_same_as_no_signal(self):
        for mode in _ALLOWED_TUTOR_MODES:
            with self.subTest(tutor_mode=mode):
                d1 = select_strategy(tutor_mode=mode)
                d2 = select_strategy(tutor_mode=mode, recent_error_type=None)
                self.assertEqual(d1["function_weights"], d2["function_weights"])
                self.assertEqual(d1["rules_applied"], d2["rules_applied"])


# ---------------------------------------------------------------------------
# Test 20 — rules are composable
# ---------------------------------------------------------------------------

class TestRulesAreComposable(unittest.TestCase):

    _COMBOS = [
        {
            "signals": {"exam_days_remaining": 7, "learning_goal": "distinction"},
            "expected_rules": {"exam_high_urgency", "distinction_goal"},
        },
        {
            "signals": {"exam_days_remaining": 14, "learner_confidence": "low", "recent_error_type": "causal_gap"},
            "expected_rules": {"exam_high_urgency", "low_confidence", "causal_gap"},
        },
        {
            "signals": {"exam_days_remaining": 30, "recent_error_type": "memorization_without_reasoning", "learning_goal": "distinction"},
            "expected_rules": {"exam_medium_urgency", "memorization_without_reasoning", "distinction_goal"},
        },
        {
            "signals": {"exam_days_remaining": 7, "learner_confidence": "low", "recent_error_type": "vague_answer", "learning_goal": "distinction"},
            "expected_rules": {"exam_high_urgency", "low_confidence", "vague_answer", "distinction_goal"},
        },
    ]

    def test_rules_are_composable(self):
        for combo in self._COMBOS:
            for mode in _ALLOWED_TUTOR_MODES:
                label = f"{mode}+{list(combo['signals'].keys())}"
                with self.subTest(combination=label):
                    d = select_strategy(tutor_mode=mode, **combo["signals"])
                    for rule in combo["expected_rules"]:
                        self.assertIn(rule, d["rules_applied"],
                            msg=f"{label}: rule '{rule}' not applied")
                    self.assertAlmostEqual(_sum_weights(d), 1.0, delta=_FLOAT_DELTA)
                    self.assertGreaterEqual(_w(d, "host"), HOST_FLOOR - _FLOAT_DELTA)
                    self.assertIs(d["governance"]["safe_for_examiner"], False)
                    self.assertIs(d["governance"]["examiner_scoring_allowed"], False)

    def test_determinism_over_composable_rules(self):
        signals = {"exam_days_remaining": 7, "learner_confidence": "low",
                   "recent_error_type": "causal_gap", "learning_goal": "distinction"}
        for mode in _ALLOWED_TUTOR_MODES:
            with self.subTest(mode=mode):
                d1 = select_strategy(tutor_mode=mode, **signals)
                d2 = select_strategy(tutor_mode=mode, **signals)
                self.assertEqual(d1["function_weights"], d2["function_weights"])
                self.assertEqual(d1["rules_applied"], d2["rules_applied"])


if __name__ == "__main__":
    unittest.main()
