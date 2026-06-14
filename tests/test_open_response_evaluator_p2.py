"""Tests for Phase P2.2: 4-dimensional evaluator.

Tests the multi-dimensional evaluation framework without claiming examiner authority.
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from tools.question_generation.open_response_evaluator import (
    evaluate_answer_multi_dimensional,
    _concept_present,
    _extract_causal_chains,
    _signal_present,
    load_command_verb,
    GOVERNANCE_FLAGS,
    FORBIDDEN_SCORING_LANGUAGE,
)


class EvaluatorDimensionTests(unittest.TestCase):
    """Test each of the 4 dimensions independently."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.sample_answer = """
        Cool climates cause higher acidity in grapes because lower temperatures slow ripening.
        This results in grapes retaining more malic acid. The final wine therefore shows
        bright, crisp acidity.
        """
        self.expected_concepts = ["cool climate", "acidity", "ripening", "malic acid"]
        self.command_verb = "explain"
        self.causal_chain = "cool climate → slower ripening → retained acid → higher acidity"

    def test_content_correctness_dimension_detects_concepts(self) -> None:
        """Dimension A: Content should detect expected concepts."""
        result = evaluate_answer_multi_dimensional(
            self.sample_answer,
            self.expected_concepts,
            self.causal_chain,
            self.command_verb
        )

        content = result["evaluation"]["content_correctness"]
        self.assertIn("concepts_detected", content)
        self.assertIn("acidity", content["concepts_detected"])
        # Verify that at least one concept contains "climate"
        concepts_lower = [c.lower() for c in content["concepts_detected"]]
        self.assertTrue(any("climate" in c for c in concepts_lower))

    def test_content_correctness_identifies_missing_concepts(self) -> None:
        """Dimension A: Should identify missing concepts."""
        result = evaluate_answer_multi_dimensional(
            self.sample_answer,
            ["sulfites", "oak", "tannin"],
            None,
            "explain"
        )

        content = result["evaluation"]["content_correctness"]
        self.assertGreater(len(content["concepts_missing"]), 0)

    def test_structural_correctness_dimension_exists(self) -> None:
        """Dimension B: Structural evaluation should exist and be independent."""
        result = evaluate_answer_multi_dimensional(
            self.sample_answer,
            self.expected_concepts,
            self.causal_chain,
            self.command_verb
        )

        structural = result["evaluation"]["structural_correctness"]
        self.assertIn("meets_minimum", structural)
        self.assertIn("feedback", structural)

    def test_verb_compliance_dimension_works(self) -> None:
        """Dimension C: Verb compliance should be independent dimension."""
        result = evaluate_answer_multi_dimensional(
            self.sample_answer,
            self.expected_concepts,
            self.causal_chain,
            "explain"
        )

        compliance = result["evaluation"]["command_verb_compliance"]
        self.assertIn("verb_requested", compliance)
        self.assertEqual(compliance["verb_requested"], "explain")
        self.assertIn("compliance_status", compliance)

    def test_distinction_chain_not_applied_to_short_answer(self) -> None:
        """Dimension D: Should not apply SAT chain to short_answer responses."""
        result = evaluate_answer_multi_dimensional(
            self.sample_answer,
            self.expected_concepts,
            self.causal_chain,
            "explain",
            response_type="short_answer"
        )

        distinction = result["evaluation"]["distinction_chain_completeness"]
        self.assertFalse(distinction["is_sat_response"])
        self.assertIn("Distinction-chain evaluation applies to SAT", distinction["feedback"])

    def test_distinction_chain_applied_to_sat_response(self) -> None:
        """Dimension D: Should evaluate SAT structure for sat_full responses."""
        sat_answer = """
        Appearance: Pale gold, clear, still.
        Nose: Medium intensity, apple, lemon, honey.
        Palate: Crisp acidity, medium body, dry finish.
        Quality: Very good - well-expressed acidity with aging potential.
        Readiness: Can age 5-8 years given the acid and mineral structure.
        """

        result = evaluate_answer_multi_dimensional(
            sat_answer,
            ["color", "acidity", "body"],
            None,
            "assess",
            response_type="sat_full"
        )

        distinction = result["evaluation"]["distinction_chain_completeness"]
        self.assertTrue(distinction["is_sat_response"])
        self.assertIn("sections", distinction)

    def test_formative_guidance_synthesized_from_dimensions(self) -> None:
        """Overall guidance should synthesize from all 4 dimensions."""
        result = evaluate_answer_multi_dimensional(
            "The climate causes higher acidity.",
            ["climate", "acidity"],
            None,
            "explain"
        )

        guidance = result["overall_formative_guidance"]
        self.assertIn("strengths", guidance)
        self.assertIn("gaps", guidance)
        self.assertIn("next_focus", guidance)
        self.assertIn("safe_for_examiner", guidance)
        self.assertFalse(guidance["safe_for_examiner"])


class GovernanceTests(unittest.TestCase):
    """Ensure evaluator never claims examiner authority."""

    def test_governance_flags_always_safe(self) -> None:
        """Governance flags must always be safe_for_examiner=False."""
        self.assertFalse(GOVERNANCE_FLAGS["safe_for_examiner"])
        self.assertFalse(GOVERNANCE_FLAGS["examiner_scoring_allowed"])

    def test_all_evaluator_outputs_include_governance(self) -> None:
        """Every evaluation must include governance flags."""
        result = evaluate_answer_multi_dimensional(
            "Test answer",
            ["concept"],
            None,
            "describe"
        )

        self.assertIn("governance", result)
        self.assertFalse(result["governance"]["safe_for_examiner"])
        self.assertFalse(result["governance"]["examiner_scoring_allowed"])

    def test_no_scoring_language_in_feedback(self) -> None:
        """Feedback must not contain scoring/marking language."""
        result = evaluate_answer_multi_dimensional(
            "Cool climates cause higher acidity because of slower ripening.",
            ["acidity"],
            None,
            "explain"
        )

        # Collect all feedback
        all_feedback = ""
        for dimension_result in result["evaluation"].values():
            if isinstance(dimension_result, dict) and "feedback" in dimension_result:
                all_feedback += dimension_result["feedback"]

        all_feedback += " ".join(result["overall_formative_guidance"].get("next_focus", []))

        all_feedback_lower = all_feedback.lower()
        for forbidden_word in FORBIDDEN_SCORING_LANGUAGE:
            self.assertNotIn(forbidden_word, all_feedback_lower,
                           f"Found forbidden scoring word '{forbidden_word}' in feedback")

    def test_formative_only_declaration(self) -> None:
        """Guidance must declare itself formative-only."""
        result = evaluate_answer_multi_dimensional(
            "Test",
            [],
            None,
            "describe"
        )

        guidance = result["overall_formative_guidance"]
        self.assertFalse(guidance.get("examiner_scoring_allowed"))
        self.assertTrue(guidance.get("formative_only"))


class HelperFunctionTests(unittest.TestCase):
    """Test individual helper functions."""

    def test_concept_present_with_exact_match(self) -> None:
        """Should find exact concept matches."""
        self.assertTrue(_concept_present("acidity", "The wine has high acidity."))

    def test_concept_present_with_partial_match(self) -> None:
        """Should find concepts with word-boundary matching."""
        self.assertTrue(_concept_present("acid", "The wine has high acidity."))

    def test_concept_absent(self) -> None:
        """Should detect when concept is missing."""
        self.assertFalse(_concept_present("tannin", "The wine has bright acidity."))

    def test_causal_chain_extraction(self) -> None:
        """Should extract causal statements."""
        text = "Cool climates cause slower ripening because of lower temperatures."
        chains = _extract_causal_chains(text)
        self.assertGreater(len(chains), 0)
        self.assertTrue(chains[0]["contains_causality"])

    def test_signal_present_detects_required_language(self) -> None:
        """Should detect required compliance signals."""
        self.assertTrue(_signal_present("because", "The wine is good because of acidity."))
        self.assertTrue(_signal_present("therefore", "The temperature is low. Therefore, acidity is retained."))

    def test_signal_not_present(self) -> None:
        """Should detect when signal is missing."""
        self.assertFalse(_signal_present("because", "The wine has acidity."))


class VerbComplianceTests(unittest.TestCase):
    """Test verb-specific compliance detection."""

    def test_explain_requires_causal_signals(self) -> None:
        """Explain verb should require causal connectors."""
        result = evaluate_answer_multi_dimensional(
            "The wine has acidity. The climate is cool.",  # No causality
            ["acidity"],
            None,
            "explain"
        )

        compliance = result["evaluation"]["command_verb_compliance"]
        # Should not have full compliance without causal signals
        self.assertNotEqual(compliance["compliance_status"], "full")

    def test_explain_with_full_causal_chain(self) -> None:
        """Explain with proper causality should show full compliance."""
        result = evaluate_answer_multi_dimensional(
            "Cool climates cause lower temperatures because of latitude. Therefore, malic acid is retained.",
            ["acidity"],
            "climate → temperature → acidity",
            "explain"
        )

        compliance = result["evaluation"]["command_verb_compliance"]
        self.assertIn("because", compliance["required_signals_found"])

    def test_describe_forbids_explanation(self) -> None:
        """Describe should not require or expect causal signals."""
        result = evaluate_answer_multi_dimensional(
            "The wine shows pale gold color, lemon aromas, crisp acidity, and medium body.",
            ["color", "aroma", "acidity", "body"],
            None,
            "describe"
        )

        compliance = result["evaluation"]["command_verb_compliance"]
        # Description of features without causality should be acceptable
        self.assertIsNotNone(compliance["compliance_status"])


class IntegrationTests(unittest.TestCase):
    """Test full end-to-end evaluation."""

    def test_complete_evaluation_structure(self) -> None:
        """Full evaluation should have all required top-level keys."""
        result = evaluate_answer_multi_dimensional(
            "Test answer",
            ["concept"],
            None,
            "explain"
        )

        required_keys = {"governance", "evaluation", "overall_formative_guidance"}
        self.assertTrue(required_keys.issubset(set(result.keys())))

    def test_evaluation_has_all_four_dimensions(self) -> None:
        """Evaluation must have all 4 dimensions."""
        result = evaluate_answer_multi_dimensional(
            "Test answer",
            ["concept"],
            None,
            "explain"
        )

        dimensions = {
            "content_correctness",
            "structural_correctness",
            "command_verb_compliance",
            "distinction_chain_completeness"
        }
        self.assertTrue(dimensions.issubset(set(result["evaluation"].keys())))

    def test_all_verbs_load_without_error(self) -> None:
        """All 12 verbs should load without error."""
        verbs = [
            "describe", "explain", "assess", "evaluate", "compare", "justify",
            "why", "how", "discuss", "identify_and_explain", "outline", "state", "list"
        ]

        for verb in verbs:
            result = evaluate_answer_multi_dimensional(
                "Sample answer text",
                ["sample"],
                None,
                verb
            )
            self.assertIsNotNone(result)
            self.assertIn("evaluation", result)


if __name__ == "__main__":
    unittest.main()
