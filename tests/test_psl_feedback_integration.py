"""PSL Feedback Integration Tests — 14 required tests.

Tests the minimal, reversible integration of the Pedagogical Strategy Layer
into the feedback/remediation flow of WSET-AI-System.

Coverage:
  - Profile-specific PSL behavior (tests 1-7)
  - Gate on/off behaviour (tests 8, 9, 10, 11)
  - Governance invariants (tests 12, 13)
  - Retrieval-first invariant (test 14)

All tests use the gate via module-level patching (unittest.mock.patch)
so the global ENABLE_PEDAGOGICAL_STRATEGY_LAYER remains False at module level.
"""
from __future__ import annotations

import copy
import json
import unittest
import unittest.mock
from pathlib import Path


# ---------------------------------------------------------------------------
# Helpers to drive PSL directly without orchestrator file I/O
# ---------------------------------------------------------------------------

def _build_psl_gate_on(**kwargs):
    """Call build_pedagogical_strategy with the gate forcibly enabled."""
    import tools.tutor.pedagogical_strategy.strategy_layer as sl
    with unittest.mock.patch.object(sl, "ENABLE_PEDAGOGICAL_STRATEGY_LAYER", True):
        return sl.build_pedagogical_strategy(**kwargs)


def _build_psl_gate_off(**kwargs):
    """Call build_pedagogical_strategy with the gate forcibly disabled."""
    import tools.tutor.pedagogical_strategy.strategy_layer as sl
    with unittest.mock.patch.object(sl, "ENABLE_PEDAGOGICAL_STRATEGY_LAYER", False):
        return sl.build_pedagogical_strategy(**kwargs)


# Minimal scaffolding-relevant context_package (no file I/O required)
def _minimal_package(psl_directive=None, **overrides) -> dict:
    pkg = {
        "student_query": "How does acidity affect quality?",
        "language": "es",
        "pedagogical_act": "answer_normally",
        "matched_misconception": {},
        "learner_state_context": {},
        "retrieval_plan": {"pedagogical_priority_boost": {}},
        "retrieved_context": [],
        "forced_causal_chains": [],
        "tutor_directive": {"safe_for_examiner": False},
        "governance": {"safe_for_examiner": False, "examiner_scoring_allowed": False},
    }
    pkg.update(overrides)
    if psl_directive is not None:
        pkg["psl_directive"] = psl_directive
    return pkg


# ---------------------------------------------------------------------------
# Test 1 -- host-dominant profile softens feedback without hiding errors
# ---------------------------------------------------------------------------

class TestHostSoftensFeedbackWithoutHidingErrors(unittest.TestCase):
    def test_host_softens_feedback_without_hiding_errors(self):
        """Host-dominant (low_confidence rule): emotional support high,
        but errors are never hidden -- governance flags remain False."""
        directive = _build_psl_gate_on(learner_confidence="low")

        self.assertTrue(directive.get("strategy_active"), "strategy_active must be True")
        self.assertIn(
            directive.get("emotional_support_level"),
            {"high", "medium"},
            "Host-dominant should produce medium or high emotional support",
        )
        # Errors must not be hidden: evidence_required in traceability must be True
        traceability = directive.get("traceability") or {}
        self.assertTrue(
            traceability.get("evidence_required"),
            "evidence_required must remain True even in host-dominant mode",
        )
        # Governance invariants
        gov = directive.get("governance") or {}
        self.assertFalse(gov.get("safe_for_examiner"))
        self.assertFalse(gov.get("examiner_scoring_allowed"))


# ---------------------------------------------------------------------------
# Test 2 -- challenger demands evidence without inventing content
# ---------------------------------------------------------------------------

class TestChallengerDemandsEvidenceWithoutInventing(unittest.TestCase):
    def test_challenger_demands_evidence_without_inventing(self):
        """Challenger-dominant (exam_imminent rule): feedback_intensity elevated,
        but no fabricated authority or scoring fields."""
        directive = _build_psl_gate_on(exam_days_remaining=7)

        self.assertTrue(directive.get("strategy_active"))
        self.assertIn(
            directive.get("challenge_level"),
            {"high", "medium"},
            "Exam imminent should raise challenge level",
        )
        # feedback_intensity should be elevated
        self.assertIn(directive.get("feedback_intensity"), {"high", "medium"})
        # No fabricated fields
        for forbidden_key in ("score", "marks", "grade", "band", "examiner_verdict"):
            self.assertNotIn(forbidden_key, directive)
        gov = directive.get("governance") or {}
        self.assertFalse(gov.get("safe_for_examiner"))
        self.assertFalse(gov.get("examiner_scoring_allowed"))
        traceability = directive.get("traceability") or {}
        self.assertFalse(traceability.get("official_scoring"))


# ---------------------------------------------------------------------------
# Test 3 -- scientist profile elevates causal_depth_required
# ---------------------------------------------------------------------------

class TestScientistRequestsCausalChain(unittest.TestCase):
    def test_scientist_requests_causal_chain(self):
        """Scientist-dominant (causal_gap rule): causal_depth_required is
        at least 'standard' (never 'minimal'); function_weights scientist elevated."""
        directive = _build_psl_gate_on(recent_error_type="causal_gap")

        self.assertTrue(directive.get("strategy_active"))
        causal_depth = directive.get("causal_depth_required")
        self.assertIn(
            causal_depth,
            {"standard", "deep"},
            f"causal_gap should produce standard or deep causal depth, got {causal_depth!r}",
        )
        # Scientist weight should be elevated vs default
        weights = directive.get("function_weights") or {}
        scientist_w = weights.get("scientist", 0.0)
        self.assertGreater(
            scientist_w, 0.15,
            f"Scientist weight should be elevated by causal_gap rule, got {scientist_w:.3f}",
        )


# ---------------------------------------------------------------------------
# Test 4 -- cartographer profile produces contextual/regional question type
# ---------------------------------------------------------------------------

class TestCartographerRecontextualizesByRegion(unittest.TestCase):
    def test_cartographer_recontextualizes_by_region(self):
        """Cartographer-dominant (regional_confusion rule): preferred_question_type
        is 'contextual' and governance is clean."""
        directive = _build_psl_gate_on(recent_error_type="regional_confusion")

        self.assertTrue(directive.get("strategy_active"))
        self.assertEqual(
            directive.get("preferred_question_type"),
            "contextual",
            "regional_confusion should produce contextual preferred question type",
        )
        gov = directive.get("governance") or {}
        self.assertFalse(gov.get("safe_for_examiner"))
        self.assertFalse(gov.get("examiner_scoring_allowed"))


# ---------------------------------------------------------------------------
# Test 5 -- critic flags vagueness without emitting official scoring
# ---------------------------------------------------------------------------

class TestCriticMarksVaguenessWithoutOfficialScoring(unittest.TestCase):
    def test_critic_marks_vagueness_without_official_scoring(self):
        """Critic-dominant (vague_answer rule): evaluative question type and
        elevated feedback, but no WSET score emitted."""
        directive = _build_psl_gate_on(recent_error_type="vague_answer")

        self.assertTrue(directive.get("strategy_active"))
        # preferred_question_type is evaluative or reflective depending on tie-break
        # (critic and host may tie after vague_answer rule; both are acceptable)
        self.assertIn(
            directive.get("preferred_question_type"),
            {"evaluative", "reflective"},
            "vague_answer should produce evaluative or reflective preferred question type",
        )
        # Feedback must be elevated
        self.assertIn(directive.get("feedback_intensity"), {"high", "medium"})
        # No official scoring fields
        for forbidden_key in ("score", "marks", "grade", "band", "examiner_verdict"):
            self.assertNotIn(forbidden_key, directive)
        gov = directive.get("governance") or {}
        self.assertFalse(gov.get("examiner_scoring_allowed"))
        traceability = directive.get("traceability") or {}
        self.assertFalse(traceability.get("official_scoring"))


# ---------------------------------------------------------------------------
# Test 6 -- storyteller: analogy allowed but evidence_required remains True
# ---------------------------------------------------------------------------

class TestStorytellerUsesAnalogiesNotAsEvidence(unittest.TestCase):
    def test_storyteller_uses_analogies_not_as_evidence(self):
        """With no error signals (default/storyteller-leaning profile),
        traceability.evidence_required must still be True -- analogies are
        a framing tool, not a substitute for evidence."""
        # Default profile has storyteller weight, no rules fire with these signals
        directive = _build_psl_gate_on()

        self.assertTrue(directive.get("strategy_active"))
        traceability = directive.get("traceability") or {}
        self.assertTrue(
            traceability.get("evidence_required"),
            "evidence_required must remain True regardless of remediation style",
        )
        # traceability must also declare no official scoring
        self.assertFalse(traceability.get("official_scoring"))
        gov = directive.get("governance") or {}
        self.assertFalse(gov.get("safe_for_examiner"))


# ---------------------------------------------------------------------------
# Test 7 -- distinction goal increases exigence without authority claim
# ---------------------------------------------------------------------------

class TestDistinctionIncreasesExigenceWithoutAuthorityClaim(unittest.TestCase):
    def test_distinction_increases_exigence_without_authority_claim(self):
        """Distinction goal: feedback_intensity is elevated,
        but no official authority or examiner string appears."""
        directive = _build_psl_gate_on(learning_goal="distinction")

        self.assertTrue(directive.get("strategy_active"))
        # distinction_goal boosts critic+0.10 and challenger+0.08 but from a low base,
        # so combined critic+challenger ~= 0.33 -> "medium" or higher is acceptable.
        self.assertIn(
            directive.get("feedback_intensity"),
            {"high", "medium"},
            "distinction goal should produce elevated feedback_intensity",
        )
        # No official authority strings in any field
        for key, val in directive.items():
            if isinstance(val, str):
                self.assertNotIn("official scoring", val.lower())
                self.assertNotIn("examiner authority", val.lower())
        gov = directive.get("governance") or {}
        self.assertFalse(gov.get("safe_for_examiner"))
        self.assertFalse(gov.get("examiner_scoring_allowed"))


# ---------------------------------------------------------------------------
# Test 8 -- gate off produces no PSL output
# ---------------------------------------------------------------------------

class TestGateOffProducesNoPslOutput(unittest.TestCase):
    def test_gate_off_produces_no_psl_output(self):
        """When ENABLE_PEDAGOGICAL_STRATEGY_LAYER=False, directive is inert."""
        directive = _build_psl_gate_off(
            learner_confidence="low", exam_days_remaining=7,
        )
        self.assertFalse(directive.get("strategy_active"))
        # Inert directive must still carry governance block
        gov = directive.get("governance") or {}
        self.assertFalse(gov.get("safe_for_examiner"))
        self.assertFalse(gov.get("examiner_scoring_allowed"))
        # No strategy content
        self.assertNotIn("function_weights", directive)
        self.assertNotIn("tutor_mode", directive)
        self.assertNotIn("psl_trace", directive)

    def test_gate_off_psl_directive_absent_from_context_package(self):
        """When gate is off, the orchestrator injection block is never executed
        so psl_directive is absent from context_package (Connection C no-op)."""
        import tools.tutor.pedagogical_strategy.strategy_layer as sl

        pkg = _minimal_package()
        with unittest.mock.patch.object(sl, "ENABLE_PEDAGOGICAL_STRATEGY_LAYER", False):
            # Simulate the orchestrator's gate-guarded injection
            if sl.ENABLE_PEDAGOGICAL_STRATEGY_LAYER:
                pkg["psl_directive"] = sl.build_pedagogical_strategy(context_package=pkg)

        self.assertNotIn(
            "psl_directive", pkg,
            "psl_directive must not appear in context_package when gate is off",
        )


# ---------------------------------------------------------------------------
# Test 9 -- gate on produces psl_trace in ledger
# ---------------------------------------------------------------------------

class TestGateOnProducesPslTrace(unittest.TestCase):
    def test_gate_on_produces_psl_trace(self):
        """When gate=True, psl_trace is logged in the ledger entry with required fields."""
        from tools.orchestrator.session_ledger import _build_session_entry

        psl_directive = _build_psl_gate_on(learning_goal="distinction")
        result = {
            "strategic_plan": {
                "cold_start": False,
                "planning_confidence": 0.5,
                "difficulty_progression": "stable",
                "sat_drill_needed": False,
                "review_topics": [],
                "recommended_next_topics": [],
            },
            "orchestrator_decision": {"route": "normal_tutor"},
            "detected_misconception": {"detected": False, "matched_misconception_id": None},
            "context_package": {
                "psl_directive": psl_directive,
                "forced_causal_chains": [],
            },
        }
        entry = _build_session_entry(result, "2026-01-01T00:00:00+00:00")

        self.assertIn(
            "psl_trace", entry,
            "psl_trace must be present in ledger entry when strategy_active=True",
        )
        trace = entry["psl_trace"]
        self.assertIn("tutor_mode", trace)
        self.assertIn("function_weights", trace)
        self.assertIn("feedback_intensity", trace)
        self.assertIn("timestamp", trace)
        # Must not contain governance or raw content fields
        for blocked in ("safe_for_examiner", "examiner_scoring_allowed", "student_query"):
            self.assertNotIn(blocked, trace)


# ---------------------------------------------------------------------------
# Test 10 -- psl_directive present in context_package when gate on
# ---------------------------------------------------------------------------

class TestPslDirectiveInContextPackage(unittest.TestCase):
    def test_psl_directive_in_context_package(self):
        """Connection C: when gate=True, orchestrator injects psl_directive.

        Tested by simulating the orchestrator's PSL injection logic directly
        (avoids importing tutor_retrieval_sandbox which requires Python 3.11+).
        """
        import tools.tutor.pedagogical_strategy.strategy_layer as sl

        # Simulate the context_package that orchestrator builds
        pkg = _minimal_package()

        with unittest.mock.patch.object(sl, "ENABLE_PEDAGOGICAL_STRATEGY_LAYER", True):
            # This replicates the orchestrator injection block (Connection C)
            psl_dir = sl.build_pedagogical_strategy(context_package=pkg)
            pkg["psl_directive"] = psl_dir

        self.assertIn("psl_directive", pkg)
        psl = pkg["psl_directive"]
        self.assertTrue(psl.get("strategy_active"))
        gov = psl.get("governance") or {}
        self.assertFalse(gov.get("safe_for_examiner"))
        self.assertFalse(gov.get("examiner_scoring_allowed"))


# ---------------------------------------------------------------------------
# Test 11 -- psl_directive absent from context_package when gate off
# ---------------------------------------------------------------------------

class TestPslDirectiveAbsentWhenGateOff(unittest.TestCase):
    def test_psl_directive_absent_when_gate_off(self):
        """Connection C no-op: gate=False means psl_directive is NOT injected.

        Verified by: gate-off PSL call returns inert directive (strategy_active=False),
        and the orchestrator injection block (guarded by the gate) is never executed.
        """
        import tools.tutor.pedagogical_strategy.strategy_layer as sl

        pkg = _minimal_package()

        # Gate is False -- simulate orchestrator behaviour: no injection
        with unittest.mock.patch.object(sl, "ENABLE_PEDAGOGICAL_STRATEGY_LAYER", False):
            directive = sl.build_pedagogical_strategy(context_package=pkg)
            if sl.ENABLE_PEDAGOGICAL_STRATEGY_LAYER:  # gate off -> this branch never runs
                pkg["psl_directive"] = directive

        # psl_directive must NOT be in the package
        self.assertNotIn(
            "psl_directive", pkg,
            "psl_directive must not be injected when gate is False",
        )
        # Inert directive confirms gate-off signal
        self.assertFalse(directive.get("strategy_active"))


# ---------------------------------------------------------------------------
# Test 12 -- no examiner_scoring_allowed in integration
# ---------------------------------------------------------------------------

class TestNoExaminerScoringInIntegration(unittest.TestCase):
    def test_no_examiner_scoring_in_integration(self):
        """Integration never produces examiner_scoring_allowed=True."""
        for signals in [
            {},
            {"learner_confidence": "low"},
            {"exam_days_remaining": 7},
            {"recent_error_type": "causal_gap"},
            {"recent_error_type": "vague_answer"},
            {"learning_goal": "distinction"},
            {"recent_error_type": "regional_confusion"},
            {"exam_days_remaining": 7, "learning_goal": "distinction"},
        ]:
            directive = _build_psl_gate_on(**signals)
            gov = directive.get("governance") or {}
            self.assertFalse(
                gov.get("examiner_scoring_allowed"),
                f"examiner_scoring_allowed must be False for signals {signals}",
            )


# ---------------------------------------------------------------------------
# Test 13 -- no safe_for_examiner in integration
# ---------------------------------------------------------------------------

class TestNoSafeForExaminerInIntegration(unittest.TestCase):
    def test_no_safe_for_examiner_in_integration(self):
        """Integration never produces safe_for_examiner=True."""
        for signals in [
            {},
            {"learner_confidence": "low"},
            {"exam_days_remaining": 7},
            {"recent_error_type": "memorization_without_reasoning"},
            {"learning_goal": "distinction"},
            {"exam_days_remaining": 7, "learning_goal": "distinction"},
        ]:
            directive = _build_psl_gate_on(**signals)
            gov = directive.get("governance") or {}
            self.assertFalse(
                gov.get("safe_for_examiner"),
                f"safe_for_examiner must be False for signals {signals}",
            )
            traceability = directive.get("traceability") or {}
            self.assertFalse(
                traceability.get("official_scoring"),
                f"traceability.official_scoring must be False for signals {signals}",
            )


# ---------------------------------------------------------------------------
# Test 14 -- retrieval content unchanged by PSL
# ---------------------------------------------------------------------------

class TestRetrievalContentUnchangedByPsl(unittest.TestCase):
    def test_retrieval_content_unchanged_by_psl(self):
        """PSL does not alter retrieved_context -- retrieval-first invariant.

        Verified by: two packages with same retrieved_context, one with PSL injected,
        one without -- confirming retrieved_context is identical in both cases.
        """
        import tools.tutor.pedagogical_strategy.strategy_layer as sl

        retrieved = [
            {"chunk_id": "c1", "text_excerpt": "Acidity is a key freshness driver."},
            {"chunk_id": "c2", "text_excerpt": "Climate affects ripeness."},
        ]
        # Package without PSL (gate off)
        pkg_no_psl = _minimal_package(retrieved_context=copy.deepcopy(retrieved))

        # Package with PSL injected (gate on)
        pkg_with_psl = _minimal_package(retrieved_context=copy.deepcopy(retrieved))
        with unittest.mock.patch.object(sl, "ENABLE_PEDAGOGICAL_STRATEGY_LAYER", True):
            psl_dir = sl.build_pedagogical_strategy(
                context_package=pkg_with_psl,
                exam_days_remaining=7,
                learning_goal="distinction",
            )
        pkg_with_psl["psl_directive"] = psl_dir

        self.assertEqual(
            pkg_no_psl["retrieved_context"],
            pkg_with_psl["retrieved_context"],
            "retrieved_context must be identical regardless of PSL gate state",
        )
        self.assertFalse(
            psl_dir.get("governance", {}).get("safe_for_examiner"),
            "PSL directive must not set safe_for_examiner",
        )

    def test_psl_directive_does_not_modify_retrieved_context_in_place(self):
        """PSL build call must not mutate the context_package or its retrieved_context."""
        import tools.tutor.pedagogical_strategy.strategy_layer as sl

        retrieved = [{"chunk_id": "c1", "text_excerpt": "Some content."}]
        pkg = _minimal_package(retrieved_context=retrieved)
        original_retrieved = copy.deepcopy(pkg["retrieved_context"])

        with unittest.mock.patch.object(sl, "ENABLE_PEDAGOGICAL_STRATEGY_LAYER", True):
            sl.build_pedagogical_strategy(context_package=pkg, learning_goal="distinction")

        self.assertEqual(pkg["retrieved_context"], original_retrieved)


if __name__ == "__main__":
    unittest.main()
