"""Tests for Phase P2.4: Open Response Item Expansion

Verifies that the lab_payload has been expanded with 10-15 new items,
all properly configured with command verbs and evaluation metadata.
"""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


class ItemExpansionTests(unittest.TestCase):
    """Verify the OR item expansion was successful."""

    @classmethod
    def setUpClass(cls) -> None:
        """Load the expanded lab_payload."""
        payload_path = Path(__file__).parents[1] / "frontend" / "open-response-lab" / "lab_payload.js"
        content = payload_path.read_text(encoding="utf-8")
        match = re.search(r"window\.OPEN_RESPONSE_LAB_PAYLOAD\s*=\s*(\{.*?\});", content, re.DOTALL)
        if match:
            cls.payload = json.loads(match.group(1))
        else:
            cls.payload = {}

    def test_payload_expanded_to_40_plus_items(self) -> None:
        """Payload should have expanded to 40+ items (was 26, added 15)."""
        items = self.payload.get("items", [])
        self.assertGreaterEqual(len(items), 40,
                               f"Expected 40+ items, found {len(items)}")

    def test_pool_size_updated(self) -> None:
        """Pool size should match the number of items."""
        items = self.payload.get("items", [])
        pool_size = self.payload.get("pool_size", 0)
        self.assertEqual(pool_size, len(items),
                        f"Pool size {pool_size} doesn't match items count {len(items)}")

    def test_expansion_history_recorded(self) -> None:
        """Expansion history should record the P2.4 expansion."""
        history = self.payload.get("expansion_history", [])
        self.assertGreater(len(history), 0, "No expansion history recorded")

        # Find P2.4 expansion
        p2_4_expansion = next((h for h in history if h.get("phase") == "P2.4"), None)
        self.assertIsNotNone(p2_4_expansion, "P2.4 expansion not recorded")
        self.assertGreaterEqual(p2_4_expansion["items_added"], 10,
                               "P2.4 should add 10+ items")
        self.assertEqual(p2_4_expansion["new_pool_size"], len(self.payload["items"]))

    def test_all_items_have_required_fields(self) -> None:
        """Every item must have required fields."""
        required_fields = {
            "item_id", "source_question_id", "stem", "topic", "RA",
            "command_verb", "expected_concepts", "evaluation_config"
        }

        for item in self.payload.get("items", []):
            missing = required_fields - set(item.keys())
            self.assertEqual(len(missing), 0,
                           f"Item {item.get('item_id')} missing fields: {missing}")

    def test_no_duplicate_item_ids(self) -> None:
        """No duplicate item IDs should exist."""
        items = self.payload.get("items", [])
        item_ids = [item.get("item_id") for item in items]
        self.assertEqual(len(item_ids), len(set(item_ids)),
                        "Duplicate item IDs found")

    def test_command_verb_distribution(self) -> None:
        """Expanded items should use all 13 command verbs."""
        items = self.payload.get("items", [])
        verbs = set(item.get("command_verb") for item in items if item.get("command_verb"))

        # Should have at least 10 different verbs represented
        self.assertGreaterEqual(len(verbs), 10,
                               f"Only {len(verbs)} verbs represented, expected 10+")

    def test_expected_concepts_not_empty(self) -> None:
        """Most items should have expected_concepts."""
        items = self.payload.get("items", [])
        items_with_concepts = sum(
            1 for item in items
            if item.get("expected_concepts") and len(item.get("expected_concepts", [])) > 0
        )

        # At least 50% of items should have concepts (accounting for old items)
        threshold = len(items) * 0.5
        self.assertGreater(items_with_concepts, threshold,
                          f"Only {items_with_concepts}/{len(items)} items have concepts")

    def test_evaluation_config_structure(self) -> None:
        """All evaluation configs must have required structure."""
        required_config_fields = {
            "verb_definition_key", "requires_causal_chain",
            "structure_rules", "required_signals", "forbidden_signals"
        }

        for item in self.payload.get("items", []):
            config = item.get("evaluation_config", {})
            missing = required_config_fields - set(config.keys())
            self.assertEqual(len(missing), 0,
                           f"Item {item.get('item_id')} config missing: {missing}")

    def test_ra_distribution(self) -> None:
        """Items should be distributed across RA1-RA3."""
        items = self.payload.get("items", [])
        ras = set(item.get("RA") for item in items if item.get("RA"))

        # Should have RA1, RA2, RA3
        expected_ras = {"RA1", "RA2", "RA3"}
        self.assertTrue(expected_ras.issubset(ras),
                       f"Missing RAs: {expected_ras - ras}")

    def test_topics_are_diverse(self) -> None:
        """Items should cover diverse topics."""
        items = self.payload.get("items", [])
        topics = set(item.get("topic") for item in items if item.get("topic"))

        # Should have at least 15 different topics
        self.assertGreater(len(topics), 15,
                          f"Only {len(topics)} unique topics, expected 15+")


class ExpansionQualityTests(unittest.TestCase):
    """Verify the quality and coherence of expanded items."""

    @classmethod
    def setUpClass(cls) -> None:
        """Load the expanded lab_payload."""
        payload_path = Path(__file__).parents[1] / "frontend" / "open-response-lab" / "lab_payload.js"
        content = payload_path.read_text(encoding="utf-8")
        match = re.search(r"window\.OPEN_RESPONSE_LAB_PAYLOAD\s*=\s*(\{.*?\});", content, re.DOTALL)
        if match:
            cls.payload = json.loads(match.group(1))
        else:
            cls.payload = {}

    def test_stems_are_substantive(self) -> None:
        """All stems should have reasonable length (>20 chars)."""
        items = self.payload.get("items", [])
        short_stems = [
            item for item in items
            if len(item.get("stem", "")) < 20
        ]

        self.assertEqual(len(short_stems), 0,
                        f"Found {len(short_stems)} items with short stems (<20 chars)")

    def test_command_verb_matches_stem_language(self) -> None:
        """Command verbs should be appropriate for the stem (check expansion items)."""
        items = self.payload.get("items", [])

        # Check only P2.4 expansion items (source_question_id 2001-2015)
        expansion_items = [
            item for item in items
            if item.get("source_question_id") in [str(2000+i) for i in range(1, 16)]
        ]

        # Sample check: "explain" items should have "explain" or "how" in stem
        explain_items = [item for item in expansion_items if item.get("command_verb") == "explain"]
        for item in explain_items:
            stem = item.get("stem", "").lower()
            self.assertTrue(
                any(word in stem for word in ["explain", "how", "why", "cómo"]),
                f"Explain item stem doesn't match verb: {item.get('stem')}"
            )

    def test_concepts_are_wset_relevant(self) -> None:
        """Expected concepts should be WSET-relevant (check expansion items)."""
        wset_concepts = {
            "acidity", "tannin", "alcohol", "body", "aroma", "color",
            "climate", "altitude", "terroir", "fermentation", "oak", "ripening",
            "aging", "sugar", "structure", "style", "method", "bubbles"
        }

        items = self.payload.get("items", [])

        # Check only P2.4 expansion items
        expansion_items = [
            item for item in items
            if item.get("source_question_id") in [str(2000+i) for i in range(1, 16)]
        ]

        unmatched_items = 0

        for item in expansion_items:
            concepts = item.get("expected_concepts", [])
            # At least one concept should match WSET vocabulary
            if concepts:
                has_wset_concept = any(
                    any(term in concept.lower() for term in wset_concepts)
                    for concept in concepts
                )
                if not has_wset_concept:
                    unmatched_items += 1

        # Allow some flexibility, but most expansion items should match
        self.assertLess(unmatched_items, len(expansion_items) * 0.2,
                       f"Too many expansion items ({unmatched_items}/{len(expansion_items)}) with non-WSET concepts")

    def test_evaluation_config_matches_verb(self) -> None:
        """Evaluation config should match the command verb."""
        items = self.payload.get("items", [])

        for item in items:
            verb = item.get("command_verb")
            config = item.get("evaluation_config", {})
            verb_key = config.get("verb_definition_key")

            self.assertEqual(verb, verb_key,
                           f"Item {item.get('item_id')}: verb '{verb}' != config verb '{verb_key}'")


class GovernanceTests(unittest.TestCase):
    """Ensure expansion maintains governance compliance."""

    @classmethod
    def setUpClass(cls) -> None:
        """Load the expanded lab_payload."""
        payload_path = Path(__file__).parents[1] / "frontend" / "open-response-lab" / "lab_payload.js"
        content = payload_path.read_text(encoding="utf-8")
        match = re.search(r"window\.OPEN_RESPONSE_LAB_PAYLOAD\s*=\s*(\{.*?\});", content, re.DOTALL)
        if match:
            cls.payload = json.loads(match.group(1))
        else:
            cls.payload = {}

    def test_evaluation_metadata_preserved(self) -> None:
        """Evaluation metadata should be intact."""
        meta = self.payload.get("evaluation_metadata", {})
        self.assertIsNotNone(meta)
        self.assertFalse(meta.get("governance", {}).get("safe_for_examiner"))
        self.assertFalse(meta.get("governance", {}).get("examiner_scoring_allowed"))

    def test_all_new_items_have_governance_source(self) -> None:
        """Expanded items should be marked with P2.4 source."""
        items = self.payload.get("items", [])

        # Check items from expansion (q_id 2001-2015)
        expansion_ids = {f"open_response_{2000+i}" for i in range(1, 16)}
        expansion_items = [item for item in items if item.get("item_id") in expansion_ids]

        for item in expansion_items:
            config = item.get("evaluation_config", {})
            self.assertEqual(config.get("source"), "phase_p2_4_expansion",
                           f"Item {item.get('item_id')} not marked as P2.4 expansion")


if __name__ == "__main__":
    unittest.main()
