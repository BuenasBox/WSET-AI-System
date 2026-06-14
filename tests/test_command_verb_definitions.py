"""Tests for Phase P2.1 command verb definitions and schema validation."""

from __future__ import annotations

import json
import unittest
from pathlib import Path


COMMAND_VERBS_DIR = Path(__file__).parents[1] / "knowledge" / "command-verbs"


def load_verb(verb_name: str) -> dict:
    """Load a command verb JSON file."""
    path = COMMAND_VERBS_DIR / f"{verb_name}.json"
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


class CommandVerbSchemaTests(unittest.TestCase):
    """Verify all 12 command verbs have required schema fields."""

    ALL_VERBS = [
        "describe", "explain", "assess", "evaluate", "compare", "justify",
        "why", "how", "discuss", "identify_and_explain", "outline", "state", "list"
    ]

    REQUIRED_FIELDS = {
        "schema_version", "verb", "source", "governance",
        "cognitive_level", "definition", "used_in_ras", "expected_response",
        "mark_expectation", "question_stem_examples", "mentor_hint",
        "compliance_checks"
    }

    def test_all_12_verbs_exist(self) -> None:
        """All 12 verbs must have JSON files."""
        for verb in self.ALL_VERBS:
            path = COMMAND_VERBS_DIR / f"{verb}.json"
            self.assertTrue(path.exists(), f"Missing verb file: {verb}.json")

    def test_all_verbs_have_required_fields(self) -> None:
        """Each verb must have all required top-level fields."""
        for verb in self.ALL_VERBS:
            data = load_verb(verb)
            for field in self.REQUIRED_FIELDS:
                self.assertIn(field, data, f"Verb '{verb}' missing field: {field}")

    def test_schema_version_is_correct(self) -> None:
        """schema_version must be assessment_intelligence_v1."""
        for verb in self.ALL_VERBS:
            data = load_verb(verb)
            self.assertEqual(data["schema_version"], "assessment_intelligence_v1",
                           f"Verb '{verb}' has wrong schema_version")

    def test_verb_field_matches_filename(self) -> None:
        """verb field must match the filename (minus .json)."""
        for verb in self.ALL_VERBS:
            data = load_verb(verb)
            # Special case: identify_and_explain filename vs "identify and explain" verb
            expected = verb if verb != "identify_and_explain" else "identify and explain"
            self.assertEqual(data["verb"], expected,
                           f"Verb field mismatch for {verb}")

    def test_governance_flags_correct(self) -> None:
        """All verbs must have safe governance settings."""
        for verb in self.ALL_VERBS:
            data = load_verb(verb)
            gov = data.get("governance", {})
            self.assertFalse(gov.get("safe_for_examiner"),
                           f"Verb '{verb}': safe_for_examiner must be False")
            self.assertFalse(gov.get("examiner_scoring_allowed"),
                           f"Verb '{verb}': examiner_scoring_allowed must be False")
            self.assertFalse(gov.get("uses_llm"),
                           f"Verb '{verb}': uses_llm must be False")
            self.assertFalse(gov.get("uses_api"),
                           f"Verb '{verb}': uses_api must be False")

    def test_used_in_ras_is_list_of_valid_ras(self) -> None:
        """used_in_ras must be a list containing only RA1-RA5."""
        valid_ras = {"RA1", "RA2", "RA3", "RA4", "RA5"}
        for verb in self.ALL_VERBS:
            data = load_verb(verb)
            ras = data.get("used_in_ras", [])
            self.assertIsInstance(ras, list, f"Verb '{verb}': used_in_ras must be a list")
            self.assertTrue(len(ras) > 0, f"Verb '{verb}': used_in_ras must not be empty")
            for ra in ras:
                self.assertIn(ra, valid_ras, f"Verb '{verb}': invalid RA value {ra}")

    def test_expected_response_has_required_keys(self) -> None:
        """expected_response must have format, do, do_not."""
        for verb in self.ALL_VERBS:
            data = load_verb(verb)
            resp = data.get("expected_response", {})
            self.assertIn("format", resp, f"Verb '{verb}': expected_response missing 'format'")
            self.assertIn("do", resp, f"Verb '{verb}': expected_response missing 'do'")
            self.assertIn("do_not", resp, f"Verb '{verb}': expected_response missing 'do_not'")

            self.assertIsInstance(resp["do"], list, f"Verb '{verb}': 'do' must be a list")
            self.assertIsInstance(resp["do_not"], list, f"Verb '{verb}': 'do_not' must be a list")
            self.assertTrue(len(resp["do"]) > 0, f"Verb '{verb}': 'do' must not be empty")
            self.assertTrue(len(resp["do_not"]) > 0, f"Verb '{verb}': 'do_not' must not be empty")

    def test_question_stem_examples_present(self) -> None:
        """Each verb must have at least 2 question stem examples."""
        for verb in self.ALL_VERBS:
            data = load_verb(verb)
            examples = data.get("question_stem_examples", [])
            self.assertIsInstance(examples, list, f"Verb '{verb}': examples must be a list")
            self.assertGreaterEqual(len(examples), 2,
                                   f"Verb '{verb}': need at least 2 question stem examples")

    def test_compliance_checks_structure(self) -> None:
        """compliance_checks must have required_signals, forbidden_signals, structure_rules."""
        for verb in self.ALL_VERBS:
            data = load_verb(verb)
            checks = data.get("compliance_checks", {})
            self.assertIn("required_signals", checks,
                         f"Verb '{verb}': compliance_checks missing 'required_signals'")
            self.assertIn("forbidden_signals", checks,
                         f"Verb '{verb}': compliance_checks missing 'forbidden_signals'")
            self.assertIn("structure_rules", checks,
                         f"Verb '{verb}': compliance_checks missing 'structure_rules'")

            self.assertIsInstance(checks["required_signals"], list,
                                 f"Verb '{verb}': required_signals must be a list")
            self.assertIsInstance(checks["forbidden_signals"], list,
                                 f"Verb '{verb}': forbidden_signals must be a list")
            self.assertIsInstance(checks["structure_rules"], dict,
                                 f"Verb '{verb}': structure_rules must be a dict")

    def test_structure_rules_have_minimum_components(self) -> None:
        """structure_rules must specify minimum_components."""
        for verb in self.ALL_VERBS:
            data = load_verb(verb)
            rules = data.get("compliance_checks", {}).get("structure_rules", {})
            self.assertIn("minimum_components", rules,
                         f"Verb '{verb}': structure_rules missing 'minimum_components'")
            self.assertIsInstance(rules["minimum_components"], int,
                                 f"Verb '{verb}': minimum_components must be an int")
            self.assertGreaterEqual(rules["minimum_components"], 1,
                                   f"Verb '{verb}': minimum_components must be >= 1")


class CommandVerbConsistencyTests(unittest.TestCase):
    """Check consistency across all verbs."""

    ALL_VERBS = [
        "describe", "explain", "assess", "evaluate", "compare", "justify",
        "why", "how", "discuss", "identify_and_explain", "outline", "state", "list"
    ]

    def test_all_verbs_loadable(self) -> None:
        """All verbs must be loadable as valid JSON."""
        for verb in self.ALL_VERBS:
            data = load_verb(verb)
            self.assertIsInstance(data, dict, f"Verb '{verb}' is not a valid JSON dict")
            self.assertTrue(len(data) > 0, f"Verb '{verb}' loaded as empty dict")

    def test_no_forbidden_language_in_mentor_hints(self) -> None:
        """Mentor hints should not contain scoring language."""
        forbidden = {"mark", "score", "grade", "pass", "fail", "band"}
        for verb in self.ALL_VERBS:
            data = load_verb(verb)
            hint = (data.get("mentor_hint") or "").lower()
            for word in forbidden:
                self.assertNotIn(word, hint,
                               f"Verb '{verb}' mentor_hint contains forbidden word: {word}")

    def test_all_required_signals_are_strings(self) -> None:
        """required_signals must be strings."""
        for verb in self.ALL_VERBS:
            data = load_verb(verb)
            signals = data.get("compliance_checks", {}).get("required_signals", [])
            for signal in signals:
                self.assertIsInstance(signal, str,
                                     f"Verb '{verb}': required_signal '{signal}' is not a string")

    def test_no_overlap_between_required_and_forbidden_signals(self) -> None:
        """A signal should not appear in both required and forbidden lists."""
        for verb in self.ALL_VERBS:
            data = load_verb(verb)
            checks = data.get("compliance_checks", {})
            required = set(checks.get("required_signals", []))
            forbidden = set(checks.get("forbidden_signals", []))

            overlap = required & forbidden
            self.assertEqual(len(overlap), 0,
                           f"Verb '{verb}': signals in both required and forbidden: {overlap}")


if __name__ == "__main__":
    unittest.main()
