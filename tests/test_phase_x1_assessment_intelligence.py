"""
Tests for Phase X.1 — Official WSET Assessment Intelligence JSON assets.
Validates schema, governance fields, required keys, and content integrity.
"""
import json
import os
import unittest

BASE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "knowledge")

def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

ASSESSMENT_FRAMEWORK = os.path.join(BASE, "assessment-framework")
SAT_FRAMEWORK = os.path.join(BASE, "sat-framework")
EVALUATOR_FRAMEWORK = os.path.join(BASE, "evaluator-framework")
DISTINCTION_PATTERNS = os.path.join(BASE, "distinction-patterns")
COMMAND_VERBS = os.path.join(BASE, "command-verbs")
MENTOR_FRAMEWORK = os.path.join(BASE, "mentor-framework")

EXPECTED_SCHEMA = "assessment_intelligence_v1"
GOV_REQUIRED_FALSE = ["safe_for_examiner", "examiner_scoring_allowed", "uses_llm", "uses_api"]


def assert_governance(tc, data, path):
    gov = data.get("governance", {})
    for k in GOV_REQUIRED_FALSE:
        tc.assertIn(k, gov, f"{path}: missing governance key '{k}'")
        tc.assertFalse(gov[k], f"{path}: governance['{k}'] must be false")


def assert_schema(tc, data, path):
    tc.assertEqual(data.get("schema_version"), EXPECTED_SCHEMA,
                   f"{path}: wrong schema_version (got {data.get('schema_version')})")


# ─────────────────────────────────────────
# Assessment Framework
# ─────────────────────────────────────────
class TestAssessmentFrameworkFiles(unittest.TestCase):
    def test_learning_outcomes_exists(self):
        path = os.path.join(ASSESSMENT_FRAMEWORK, "learning_outcomes.json")
        self.assertTrue(os.path.exists(path))

    def test_learning_outcomes_schema_governance(self):
        path = os.path.join(ASSESSMENT_FRAMEWORK, "learning_outcomes.json")
        d = load(path)
        assert_schema(self, d, path)
        assert_governance(self, d, path)

    def test_learning_outcomes_unit1_has_five_learning_outcomes(self):
        d = load(os.path.join(ASSESSMENT_FRAMEWORK, "learning_outcomes.json"))
        units = d.get("units", [])
        u1 = next((u for u in units if u.get("unit_id") == "unit_1"), None)
        if u1 is None:
            u1 = units[0] if units else {}
        los = u1.get("learning_outcomes", [])
        self.assertEqual(len(los), 5)

    def test_assessment_structure_exists_and_has_governance(self):
        path = os.path.join(ASSESSMENT_FRAMEWORK, "assessment_structure.json")
        self.assertTrue(os.path.exists(path))
        assert_governance(self, load(path), path)

    def test_assessment_rules_exists_and_has_governance(self):
        path = os.path.join(ASSESSMENT_FRAMEWORK, "assessment_rules.json")
        self.assertTrue(os.path.exists(path))
        assert_governance(self, load(path), path)

    def test_command_verbs_exists_and_has_governance(self):
        path = os.path.join(ASSESSMENT_FRAMEWORK, "command_verbs.json")
        self.assertTrue(os.path.exists(path))
        assert_governance(self, load(path), path)

    def test_command_verbs_has_seven_verbs(self):
        d = load(os.path.join(ASSESSMENT_FRAMEWORK, "command_verbs.json"))
        verbs = d.get("verbs", d.get("command_verbs", []))
        self.assertEqual(len(verbs), 7)


# ─────────────────────────────────────────
# SAT Framework
# ─────────────────────────────────────────
class TestSATFrameworkFiles(unittest.TestCase):
    FILES = ["sat_structure.json", "sat_vocabulary.json", "sat_scales.json", "sat_quality_framework.json"]

    def test_all_sat_files_exist(self):
        for f in self.FILES:
            path = os.path.join(SAT_FRAMEWORK, f)
            self.assertTrue(os.path.exists(path), f"Missing: {f}")

    def test_sat_files_governance(self):
        for f in self.FILES:
            path = os.path.join(SAT_FRAMEWORK, f)
            assert_governance(self, load(path), path)

    def test_sat_structure_has_four_sections(self):
        d = load(os.path.join(SAT_FRAMEWORK, "sat_structure.json"))
        sections = d.get("sections", [])
        self.assertEqual(len(sections), 4)

    def test_sat_vocabulary_has_primary_secondary_tertiary(self):
        d = load(os.path.join(SAT_FRAMEWORK, "sat_vocabulary.json"))
        # Support both key conventions used across files
        cats = d.get("aroma_flavour_categories", d.get("wset_lexicon", {}))
        raw = json.dumps(cats).lower()
        self.assertIn("primary", raw)
        self.assertIn("secondary", raw)
        self.assertIn("tertiary", raw)

    def test_sat_quality_framework_has_six_levels(self):
        d = load(os.path.join(SAT_FRAMEWORK, "sat_quality_framework.json"))
        levels = d.get("quality_levels", [])
        self.assertEqual(len(levels), 6)


# ─────────────────────────────────────────
# Evaluator Framework
# ─────────────────────────────────────────
class TestEvaluatorFrameworkFiles(unittest.TestCase):
    FILES = ["mark_allocation_rules.json", "evidence_requirements.json", "assessment_expectations.json"]

    def test_all_evaluator_files_exist(self):
        for f in self.FILES:
            path = os.path.join(EVALUATOR_FRAMEWORK, f)
            self.assertTrue(os.path.exists(path), f"Missing: {f}")

    def test_evaluator_files_governance(self):
        for f in self.FILES:
            path = os.path.join(EVALUATOR_FRAMEWORK, f)
            assert_governance(self, load(path), path)

    def test_mark_allocation_white_20_red_21(self):
        d = load(os.path.join(EVALUATOR_FRAMEWORK, "mark_allocation_rules.json"))
        # Support both structural conventions
        obs = d.get("observed_mark_totals", {})
        alloc = d.get("sat_mark_allocation", {})
        white_total = (obs.get("white_wine", {}).get("total") or
                       alloc.get("white_wine_total") or
                       alloc.get("white_wine", {}).get("total_marks"))
        red_total = (obs.get("red_wine", {}).get("total") or
                     alloc.get("red_wine_total") or
                     alloc.get("red_wine", {}).get("total_marks"))
        self.assertEqual(white_total, 20, f"white_wine total should be 20, got {white_total}")
        self.assertEqual(red_total, 21, f"red_wine total should be 21, got {red_total}")

    def test_simple_wine_exception_documented(self):
        d = load(os.path.join(EVALUATOR_FRAMEWORK, "mark_allocation_rules.json"))
        raw = json.dumps(d).lower()
        self.assertIn("simple", raw)


# ─────────────────────────────────────────
# Distinction Patterns
# ─────────────────────────────────────────
class TestDistinctionPatternsFiles(unittest.TestCase):
    FILES = ["response_structures.json", "descriptor_patterns.json",
             "quality_reasoning_patterns.json", "readiness_reasoning_patterns.json"]

    def test_all_distinction_files_exist(self):
        for f in self.FILES:
            path = os.path.join(DISTINCTION_PATTERNS, f)
            self.assertTrue(os.path.exists(path), f"Missing: {f}")

    def test_distinction_files_governance(self):
        for f in self.FILES:
            path = os.path.join(DISTINCTION_PATTERNS, f)
            assert_governance(self, load(path), path)

    def test_quality_reasoning_has_excelente_key(self):
        d = load(os.path.join(DISTINCTION_PATTERNS, "quality_reasoning_patterns.json"))
        mapping = d.get("quality_justification_framework", {}).get("evidence_to_quality_mapping", {})
        self.assertIn("excelente", mapping)

    def test_readiness_has_model_answer_examples(self):
        d = load(os.path.join(DISTINCTION_PATTERNS, "readiness_reasoning_patterns.json"))
        examples = d.get("observed_model_answer_conclusions", [])
        self.assertGreaterEqual(len(examples), 4)


# ─────────────────────────────────────────
# Command Verbs (standalone files)
# ─────────────────────────────────────────
class TestCommandVerbFiles(unittest.TestCase):
    VERBS = ["describe", "explain", "compare", "assess", "evaluate", "justify"]

    def test_all_verb_files_exist(self):
        for v in self.VERBS:
            path = os.path.join(COMMAND_VERBS, f"{v}.json")
            self.assertTrue(os.path.exists(path), f"Missing: {v}.json")

    def test_verb_files_governance(self):
        for v in self.VERBS:
            path = os.path.join(COMMAND_VERBS, f"{v}.json")
            assert_governance(self, load(path), path)

    def test_verb_files_have_required_keys(self):
        required = {"verb", "cognitive_level", "expected_response", "mark_expectation"}
        for v in self.VERBS:
            path = os.path.join(COMMAND_VERBS, f"{v}.json")
            d = load(path)
            for k in required:
                self.assertIn(k, d, f"{v}.json missing key '{k}'")

    def test_explain_includes_causal_chain_guidance(self):
        d = load(os.path.join(COMMAND_VERBS, "explain.json"))
        raw = json.dumps(d).lower()
        self.assertTrue("cause" in raw or "causal" in raw or "mechanism" in raw)

    def test_compare_mentions_similarities_and_differences(self):
        d = load(os.path.join(COMMAND_VERBS, "compare.json"))
        raw = json.dumps(d).lower()
        self.assertIn("similarities", raw)
        self.assertIn("differences", raw)


# ─────────────────────────────────────────
# Mentor Framework
# ─────────────────────────────────────────
class TestMentorFrameworkFiles(unittest.TestCase):
    FILES = ["mentor_hints.json", "mentor_guidance.json",
             "improvement_patterns.json", "common_response_failures.json"]

    def test_all_mentor_files_exist(self):
        for f in self.FILES:
            path = os.path.join(MENTOR_FRAMEWORK, f)
            self.assertTrue(os.path.exists(path), f"Missing: {f}")

    def test_mentor_files_governance(self):
        for f in self.FILES:
            path = os.path.join(MENTOR_FRAMEWORK, f)
            assert_governance(self, load(path), path)

    def test_improvement_patterns_has_minimum_entries(self):
        d = load(os.path.join(MENTOR_FRAMEWORK, "improvement_patterns.json"))
        patterns = d.get("improvement_patterns", [])
        self.assertGreaterEqual(len(patterns), 4)

    def test_common_response_failures_has_minimum_entries(self):
        d = load(os.path.join(MENTOR_FRAMEWORK, "common_response_failures.json"))
        failures = d.get("failures", [])
        self.assertGreaterEqual(len(failures), 5)

    def test_no_examiner_scoring_language_in_mentor_files(self):
        forbidden = ["official_grade", "examiner_grade", "official_score", "examiner_score"]
        for f in self.FILES:
            path = os.path.join(MENTOR_FRAMEWORK, f)
            raw = json.dumps(load(path)).lower()
            for term in forbidden:
                self.assertNotIn(term, raw, f"{f} contains forbidden term '{term}'")


# ─────────────────────────────────────────
# Cross-file governance invariant scan
# ─────────────────────────────────────────
class TestGlobalGovernanceInvariants(unittest.TestCase):
    def _all_files(self):
        dirs = [ASSESSMENT_FRAMEWORK, SAT_FRAMEWORK, EVALUATOR_FRAMEWORK,
                DISTINCTION_PATTERNS, COMMAND_VERBS, MENTOR_FRAMEWORK]
        files = []
        for d in dirs:
            if os.path.isdir(d):
                for fn in os.listdir(d):
                    if fn.endswith(".json"):
                        files.append(os.path.join(d, fn))
        return files

    def test_no_file_sets_safe_for_examiner_true(self):
        for path in self._all_files():
            raw = open(path, encoding="utf-8").read().replace(" ", "").lower()
            self.assertNotIn('"safe_for_examiner":true', raw,
                             f"{path}: safe_for_examiner must not be true")

    def test_no_file_sets_examiner_scoring_allowed_true(self):
        for path in self._all_files():
            raw = open(path, encoding="utf-8").read().replace(" ", "").lower()
            self.assertNotIn('"examiner_scoring_allowed":true', raw,
                             f"{path}: examiner_scoring_allowed must not be true")

    def test_all_files_have_schema_version(self):
        for path in self._all_files():
            d = load(path)
            self.assertIn("schema_version", d, f"{path}: missing schema_version")


if __name__ == "__main__":
    unittest.main()
