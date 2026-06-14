"""Tests for Phase P2.3: Frontend integration + learner intelligence.

Verifies that command verb loader, evaluation tracker, and lab payload
work together correctly without compromising governance.
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path


class LabPayloadEnrichmentTests(unittest.TestCase):
    """Verify that lab_payload.js has been enriched with evaluation metadata."""

    @classmethod
    def setUpClass(cls) -> None:
        """Load the enriched lab_payload."""
        payload_path = Path(__file__).parents[1] / "frontend" / "open-response-lab" / "lab_payload.js"
        content = payload_path.read_text(encoding="utf-8")
        # Extract JSON from: window.OPEN_RESPONSE_LAB_PAYLOAD = {...}
        import re
        match = re.search(r"window\.OPEN_RESPONSE_LAB_PAYLOAD\s*=\s*(\{.*?\});", content, re.DOTALL)
        if match:
            cls.payload = json.loads(match.group(1))
        else:
            cls.payload = {}

    def test_payload_has_evaluation_metadata(self) -> None:
        """Payload must include evaluation_metadata section."""
        self.assertIn("evaluation_metadata", self.payload)
        meta = self.payload["evaluation_metadata"]
        self.assertEqual(meta["schema_version"], "open_response_evaluation_v1")
        self.assertIn("governance", meta)
        self.assertFalse(meta["governance"]["safe_for_examiner"])
        self.assertFalse(meta["governance"]["examiner_scoring_allowed"])

    def test_all_command_verbs_loaded(self) -> None:
        """All 13 command verbs should be available."""
        expected_verbs = {
            "explain", "describe", "justify", "assess", "evaluate", "compare",
            "why", "how", "discuss", "identify and explain", "outline", "state", "list"
        }
        loaded_verbs = set(self.payload["evaluation_metadata"]["command_verbs_loaded"])
        self.assertTrue(expected_verbs.issubset(loaded_verbs))

    def test_all_items_have_command_verb(self) -> None:
        """Every item must have command_verb assigned."""
        for item in self.payload.get("items", []):
            self.assertIn("command_verb", item,
                         f"Item {item.get('item_id')} missing command_verb")
            self.assertIsNotNone(item["command_verb"])
            self.assertIn(item["command_verb"], {
                "explain", "describe", "justify", "assess", "evaluate", "compare",
                "why", "how", "discuss", "identify and explain", "outline", "state", "list"
            })

    def test_all_items_have_expected_concepts(self) -> None:
        """Every item must have expected_concepts list."""
        for item in self.payload.get("items", []):
            self.assertIn("expected_concepts", item,
                         f"Item {item.get('item_id')} missing expected_concepts")
            self.assertIsInstance(item["expected_concepts"], list)

    def test_all_items_have_evaluation_config(self) -> None:
        """Every item must have evaluation_config."""
        for item in self.payload.get("items", []):
            self.assertIn("evaluation_config", item,
                         f"Item {item.get('item_id')} missing evaluation_config")
            config = item["evaluation_config"]
            self.assertIn("verb_definition_key", config)
            self.assertIn("requires_causal_chain", config)
            self.assertIn("structure_rules", config)
            self.assertIn("required_signals", config)
            self.assertIn("forbidden_signals", config)

    def test_evaluation_config_has_valid_structure_rules(self) -> None:
        """Structure rules should have minimum_components."""
        for item in self.payload.get("items", [])[:5]:  # Check first 5
            config = item.get("evaluation_config", {})
            rules = config.get("structure_rules", {})
            self.assertIn("minimum_components", rules,
                         f"Item {item.get('item_id')} has invalid structure_rules")
            self.assertIsInstance(rules["minimum_components"], int)


class CommandVerbsLoaderTests(unittest.TestCase):
    """Verify the JavaScript command verbs loader is available."""

    def test_command_verbs_loader_file_exists(self) -> None:
        """command_verbs_loader.js must exist."""
        path = Path(__file__).parents[1] / "frontend" / "open-response-lab" / "command_verbs_loader.js"
        self.assertTrue(path.exists())

    def test_command_verbs_loader_has_required_exports(self) -> None:
        """command_verbs_loader.js must export required functions."""
        path = Path(__file__).parents[1] / "frontend" / "open-response-lab" / "command_verbs_loader.js"
        content = path.read_text(encoding="utf-8")

        required_functions = [
            "getVerbDefinition",
            "getAllVerbs",
            "getMentorHint",
            "getComplianceChecks"
        ]

        for func in required_functions:
            self.assertIn(func, content,
                         f"command_verbs_loader.js missing function: {func}")

    def test_command_verbs_loader_has_13_verbs(self) -> None:
        """command_verbs_loader.js should define all 13 command verbs."""
        path = Path(__file__).parents[1] / "frontend" / "open-response-lab" / "command_verbs_loader.js"
        content = path.read_text(encoding="utf-8")

        # Count verb definitions
        import re
        verb_defs = re.findall(r'^\s+(\w+):\s*\{', content, re.MULTILINE)
        self.assertGreaterEqual(len(verb_defs), 13,
                               f"Expected 13+ verb definitions, found {len(verb_defs)}")


class LearnerEvaluationTrackerTests(unittest.TestCase):
    """Verify the JavaScript learner evaluation tracker is available."""

    def test_learner_evaluation_tracker_file_exists(self) -> None:
        """learner_evaluation_tracker.js must exist."""
        path = Path(__file__).parents[1] / "frontend" / "open-response-lab" / "learner_evaluation_tracker.js"
        self.assertTrue(path.exists())

    def test_learner_evaluation_tracker_has_required_functions(self) -> None:
        """learner_evaluation_tracker.js must export required tracking functions."""
        path = Path(__file__).parents[1] / "frontend" / "open-response-lab" / "learner_evaluation_tracker.js"
        content = path.read_text(encoding="utf-8")

        required_functions = [
            "recordEvaluation",
            "getVerbMasterySummary",
            "getConceptCoverageSummary",
            "getCausalReasoningPattern",
            "getLearnerIntelligenceSummary",
            "clearTracker"
        ]

        for func in required_functions:
            self.assertIn(func, content,
                         f"learner_evaluation_tracker.js missing function: {func}")

    def test_learner_evaluation_tracker_uses_localstorage(self) -> None:
        """Tracker should use localStorage for persistence."""
        path = Path(__file__).parents[1] / "frontend" / "open-response-lab" / "learner_evaluation_tracker.js"
        content = path.read_text(encoding="utf-8")
        self.assertIn("localStorage", content)
        self.assertIn("STORAGE_KEY", content)

    def test_learner_evaluation_tracker_includes_governance_flags(self) -> None:
        """Tracker should include governance flags."""
        path = Path(__file__).parents[1] / "frontend" / "open-response-lab" / "learner_evaluation_tracker.js"
        content = path.read_text(encoding="utf-8")
        self.assertIn("safe_for_examiner", content)
        self.assertIn("examiner_scoring_allowed", content)
        self.assertIn("formative_only", content)


class IntegrationCoherenceTests(unittest.TestCase):
    """Verify P2.3 components work together coherently."""

    def test_command_verb_names_match_between_payload_and_loader(self) -> None:
        """Command verb names in payload must match loader definitions."""
        payload_path = Path(__file__).parents[1] / "frontend" / "open-response-lab" / "lab_payload.js"
        content = payload_path.read_text(encoding="utf-8")
        import re
        match = re.search(r"window\.OPEN_RESPONSE_LAB_PAYLOAD\s*=\s*(\{.*?\});", content, re.DOTALL)
        if match:
            payload = json.loads(match.group(1))
            loader_path = Path(__file__).parents[1] / "frontend" / "open-response-lab" / "command_verbs_loader.js"
            loader_content = loader_path.read_text(encoding="utf-8")

            # Find all verbs used in payload
            payload_verbs = set()
            for item in payload.get("items", []):
                if "command_verb" in item:
                    payload_verbs.add(item["command_verb"])

            # Check that all payload verbs are defined in loader
            for verb in payload_verbs:
                # Verb should appear in loader (account for "identify and explain" vs "identify_and_explain")
                search_term = verb.replace(" ", "_")
                self.assertIn(search_term, loader_content,
                             f"Verb '{verb}' used in payload but not defined in loader")


class GovernanceComplianceTests(unittest.TestCase):
    """Ensure all P2.3 components maintain governance compliance."""

    def test_payload_governance_flags_are_safe(self) -> None:
        """Payload governance must be safe."""
        payload_path = Path(__file__).parents[1] / "frontend" / "open-response-lab" / "lab_payload.js"
        content = payload_path.read_text(encoding="utf-8")
        import re
        match = re.search(r"window\.OPEN_RESPONSE_LAB_PAYLOAD\s*=\s*(\{.*?\});", content, re.DOTALL)
        if match:
            payload = json.loads(match.group(1))
            gov = payload.get("evaluation_metadata", {}).get("governance", {})
            self.assertFalse(gov.get("safe_for_examiner"))
            self.assertFalse(gov.get("examiner_scoring_allowed"))

    def test_tracker_maintains_formative_only_semantics(self) -> None:
        """Tracker should not produce scoring language."""
        path = Path(__file__).parents[1] / "frontend" / "open-response-lab" / "learner_evaluation_tracker.js"
        content = path.read_text(encoding="utf-8")

        forbidden_words = ["mark", "score", "grade", "pass", "fail"]
        for word in forbidden_words:
            # Should not have these as output field names (in JavaScript)
            self.assertNotIn(f"'{word}':", content,
                           f"Tracker should not output '{word}' field")
            self.assertNotIn(f'"{word}":',  content,
                           f"Tracker should not output '{word}' field")

    def test_loader_mentor_hints_avoid_scoring_language(self) -> None:
        """Mentor hints should not use scoring language."""
        path = Path(__file__).parents[1] / "frontend" / "open-response-lab" / "command_verbs_loader.js"
        content = path.read_text(encoding="utf-8")

        forbidden = ["mark", "grade", "score", "band", "merit", "distinction"]
        for word in forbidden:
            # Check mentor_hint strings specifically
            import re
            hints = re.findall(r'mentor_hint:\s*"([^"]*)"', content)
            for hint in hints:
                self.assertNotIn(word, hint.lower(),
                               f"Mentor hint contains forbidden word: {word}")


if __name__ == "__main__":
    unittest.main()
