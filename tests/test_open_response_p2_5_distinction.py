"""Tests for Phase P2.5: Distinction-Chain Coaching

Validates SAT structure templates, descriptor categorization, quality reasoning,
and readiness assessment coaching patterns.
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path


class SATChainTemplateTests(unittest.TestCase):
    """Verify SAT chain templates structure and content."""

    @classmethod
    def setUpClass(cls) -> None:
        """Load SAT chain templates."""
        path = Path(__file__).parents[1] / "knowledge" / "distinction-patterns" / "sat_chain_templates.json"
        cls.templates = json.loads(path.read_text(encoding="utf-8"))

    def test_templates_file_exists(self) -> None:
        """SAT templates file must exist."""
        path = Path(__file__).parents[1] / "knowledge" / "distinction-patterns" / "sat_chain_templates.json"
        self.assertTrue(path.exists())

    def test_schema_version_correct(self) -> None:
        """Schema version should be sat_distinction_v1."""
        self.assertEqual(self.templates["schema_version"], "sat_distinction_v1")

    def test_governance_flags_safe(self) -> None:
        """Governance flags must be safe."""
        gov = self.templates.get("governance", {})
        self.assertFalse(gov.get("safe_for_examiner"))
        self.assertFalse(gov.get("examiner_scoring_allowed"))
        self.assertTrue(gov.get("formative_only"))

    def test_all_five_sat_sections_present(self) -> None:
        """All 5 SAT sections must be defined."""
        sections = self.templates.get("sat_sections", {})
        required = {"appearance", "nose", "palate", "quality", "readiness"}
        self.assertEqual(set(sections.keys()), required)

    def test_appearance_section_complete(self) -> None:
        """Appearance section must have required fields."""
        app = self.templates["sat_sections"]["appearance"]
        self.assertTrue(app.get("required"))
        self.assertIn("assessment_dimensions", app)
        self.assertIn("color_descriptors_primary", app)
        self.assertIn("clarity_descriptors", app)
        self.assertGreater(len(app["color_descriptors_primary"]), 0)

    def test_nose_section_descriptor_categories(self) -> None:
        """Nose must have primary, secondary, tertiary categorization."""
        nose = self.templates["sat_sections"]["nose"]
        cats = nose.get("descriptor_categories", {})
        self.assertIn("primary", cats)
        self.assertIn("secondary", cats)
        self.assertIn("tertiary", cats)

        # Each should have description and examples
        for cat_name, cat_data in cats.items():
            self.assertIn("description", cat_data)
            self.assertIn("examples", cat_data)
            self.assertGreater(len(cat_data["examples"]), 0)

    def test_palate_section_comprehensive(self) -> None:
        """Palate must cover all key dimensions."""
        palate = self.templates["sat_sections"]["palate"]
        assessment_dims = palate.get("assessment_dimensions", [])
        required_dims = {"sweetness", "acidity", "tannin", "alcohol", "body", "flavor", "length"}
        self.assertTrue(required_dims.issubset(set(assessment_dims)))

        # Key assessments should have guidance
        self.assertIn("acidity_assessment", palate)
        self.assertIn("tannin_assessment", palate)
        self.assertIn("body_assessment", palate)
        self.assertIn("finish_assessment", palate)

    def test_quality_section_has_levels(self) -> None:
        """Quality section must define quality levels."""
        quality = self.templates["sat_sections"]["quality"]
        levels = quality.get("quality_levels", {})

        expected_levels = {"outstanding", "excellent", "very_good", "good", "acceptable"}
        self.assertEqual(set(levels.keys()), expected_levels)

        # Each level should have score and evidence requirements
        for level_name, level_data in levels.items():
            self.assertIn("score", level_data)
            self.assertIn("descriptor", level_data)
            self.assertIn("evidence_requirements", level_data)
            self.assertGreater(len(level_data["evidence_requirements"]), 0)

    def test_readiness_section_aging_framework(self) -> None:
        """Readiness must have aging duration framework."""
        readiness = self.templates["sat_sections"]["readiness"]
        framework = readiness.get("assessment_framework", {})

        expected_timeframes = {"immediate", "short_term", "medium_term", "long_term"}
        self.assertEqual(set(framework.keys()), expected_timeframes)

        # Each timeframe should have indicators
        for tf, tf_data in framework.items():
            self.assertIn("description", tf_data)
            self.assertIn("indicators", tf_data)
            self.assertGreater(len(tf_data["indicators"]), 0)

    def test_descriptor_categorization_defined(self) -> None:
        """Descriptor categorization schema must be present."""
        cats = self.templates.get("descriptor_categorization", {})
        self.assertIn("primary_descriptors", cats)
        self.assertIn("secondary_descriptors", cats)
        self.assertIn("tertiary_descriptors", cats)

        # Each should have category, types, and quality_indication
        for cat_name, cat_data in cats.items():
            self.assertIn("category", cat_data)
            self.assertIn("types", cat_data)
            self.assertIn("quality_indication", cat_data)


class EvaluationGuidanceTests(unittest.TestCase):
    """Test evaluation guidance and coaching patterns."""

    @classmethod
    def setUpClass(cls) -> None:
        """Load SAT chain templates."""
        path = Path(__file__).parents[1] / "knowledge" / "distinction-patterns" / "sat_chain_templates.json"
        cls.templates = json.loads(path.read_text(encoding="utf-8"))

    def test_evaluation_guidance_present(self) -> None:
        """Evaluation guidance must be present."""
        guidance = self.templates.get("evaluation_guidance", {})
        self.assertIn("completeness_checklist", guidance)
        self.assertIn("distinction_indicators", guidance)
        self.assertIn("common_issues_to_avoid", guidance)

        # Each should have content
        self.assertGreater(len(guidance["completeness_checklist"]), 0)
        self.assertGreater(len(guidance["distinction_indicators"]), 0)
        self.assertGreater(len(guidance["common_issues_to_avoid"]), 0)

    def test_coaching_patterns_comprehensive(self) -> None:
        """Coaching patterns must cover all sections."""
        coaching = self.templates.get("coaching_patterns", {})

        expected_sections = {
            "appearance_coaching", "nose_coaching", "palate_coaching",
            "quality_coaching", "readiness_coaching"
        }
        self.assertEqual(set(coaching.keys()), expected_sections)

        # Each section should have if_ patterns
        for section, patterns in coaching.items():
            self.assertGreater(len(patterns), 0)
            for pattern_key in patterns.keys():
                self.assertTrue(pattern_key.startswith("if_"),
                              f"Pattern key should start with 'if_': {pattern_key}")

    def test_appearance_coaching_patterns(self) -> None:
        """Appearance coaching should address missing elements."""
        coaching = self.templates["coaching_patterns"]["appearance_coaching"]
        self.assertIn("if_missing_color", coaching)
        self.assertIn("if_missing_clarity", coaching)
        self.assertIn("if_missing_viscosity", coaching)
        self.assertIn("if_superficial", coaching)

    def test_nose_coaching_patterns(self) -> None:
        """Nose coaching should address common issues."""
        coaching = self.templates["coaching_patterns"]["nose_coaching"]
        self.assertIn("if_closed", coaching)
        self.assertIn("if_one_descriptor", coaching)
        self.assertIn("if_generic", coaching)
        self.assertIn("if_missing_intensity", coaching)

    def test_palate_coaching_patterns(self) -> None:
        """Palate coaching should be comprehensive."""
        coaching = self.templates["coaching_patterns"]["palate_coaching"]
        self.assertIn("if_missing_acidity", coaching)
        self.assertIn("if_missing_tannin", coaching)
        self.assertIn("if_missing_body", coaching)
        self.assertIn("if_no_finish", coaching)

    def test_quality_coaching_patterns(self) -> None:
        """Quality coaching should address reasoning."""
        coaching = self.templates["coaching_patterns"]["quality_coaching"]
        self.assertIn("if_missing_evidence", coaching)
        self.assertIn("if_vague", coaching)
        self.assertIn("if_all_negative", coaching)
        self.assertIn("if_no_reasoning", coaching)


class SATValidationIntegrationTests(unittest.TestCase):
    """Test how SAT templates integrate with evaluator."""

    @classmethod
    def setUpClass(cls) -> None:
        """Load SAT templates and check evaluator integration."""
        templates_path = Path(__file__).parents[1] / "knowledge" / "distinction-patterns" / "sat_chain_templates.json"
        cls.templates = json.loads(templates_path.read_text(encoding="utf-8"))

        evaluator_path = Path(__file__).parents[1] / "tools" / "question_generation" / "open_response_evaluator.py"
        cls.evaluator_content = evaluator_path.read_text(encoding="utf-8")

    def test_evaluator_references_sat_sections(self) -> None:
        """Evaluator should reference SAT sections."""
        expected_refs = ["appearance", "nose", "palate", "quality", "readiness"]
        for section in expected_refs:
            self.assertIn(section, self.evaluator_content,
                         f"Evaluator should reference '{section}'")

    def test_evaluator_uses_sat_distinction_patterns(self) -> None:
        """Evaluator should use distinction patterns."""
        self.assertIn("distinction", self.evaluator_content)
        self.assertIn("DISTINCTION_PATTERNS_DIR", self.evaluator_content)

    def test_sat_sections_order_defined(self) -> None:
        """SAT sections must have defined order."""
        sections = self.templates["sat_sections"]
        for section_name, section_data in sections.items():
            if section_name != "readiness":  # readiness is optional
                self.assertIn("order", section_data,
                            f"Section '{section_name}' must have defined order")

    def test_quality_levels_have_numeric_scores(self) -> None:
        """Quality levels must have numeric scores for consistency."""
        quality = self.templates["sat_sections"]["quality"]
        levels = quality.get("quality_levels", {})

        scores = {level_data["score"] for level_data in levels.values()}
        # Should have 5 distinct scores
        self.assertEqual(len(scores), 5)
        # Scores should be 1-5
        self.assertEqual(scores, {1, 2, 3, 4, 5})


class DistinctionChainCoachingTests(unittest.TestCase):
    """Test distinction-chain specific coaching scenarios."""

    @classmethod
    def setUpClass(cls) -> None:
        """Load templates."""
        path = Path(__file__).parents[1] / "knowledge" / "distinction-patterns" / "sat_chain_templates.json"
        cls.templates = json.loads(path.read_text(encoding="utf-8"))

    def test_comprehensive_sat_response_elements(self) -> None:
        """A comprehensive SAT response should address all key elements."""
        checklist = self.templates["evaluation_guidance"]["completeness_checklist"]
        # Should have 5 items (one per section)
        self.assertGreaterEqual(len(checklist), 5)

    def test_distinction_indicators_clear(self) -> None:
        """Distinction indicators should clearly define excellence."""
        indicators = self.templates["evaluation_guidance"]["distinction_indicators"]
        # Should have multiple indicators
        self.assertGreater(len(indicators), 5)

        # Each should be specific
        for indicator in indicators:
            self.assertGreater(len(indicator), 10)

    def test_quality_reasoning_drivers_defined(self) -> None:
        """Quality assessment should be driven by defined factors."""
        quality = self.templates["sat_sections"]["quality"]
        drivers = quality.get("quality_reasoning_drivers", [])

        expected_drivers = {
            "expression of terroir", "balance", "complexity",
            "aging potential", "execution"
        }
        # Should cover these themes
        drivers_lower = [d.lower() for d in drivers]
        self.assertTrue(any("terroir" in d for d in drivers_lower))
        self.assertTrue(any("balanc" in d for d in drivers_lower))
        self.assertTrue(any("complex" in d for d in drivers_lower))


if __name__ == "__main__":
    unittest.main()
