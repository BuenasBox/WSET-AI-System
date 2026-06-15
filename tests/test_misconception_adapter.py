from __future__ import annotations

import copy
import unittest

from tools.learner_model.misconception_adapter import (
    detect_text_evidence,
    load_node_index,
    normalize_node,
)


class LegacyNodeCompatibilityTests(unittest.TestCase):
    def test_all_legacy_nodes_load_without_schema_migration(self) -> None:
        index = load_node_index()

        self.assertEqual(len(index), 20)
        for mc_id, node in index.items():
            with self.subTest(mc_id=mc_id):
                self.assertEqual(node["misconception_id"], mc_id)
                self.assertNotIn("weakness_signal", node)
                self.assertNotIn("coaching_content", node)
                self.assertNotIn("remediation_topics", node)

    def test_normalization_does_not_mutate_legacy_node(self) -> None:
        node = load_node_index()["MC_MLF_01"]
        before = copy.deepcopy(node)

        adapted = normalize_node(node)

        self.assertEqual(node, before)
        self.assertEqual(adapted["misconception_id"], "MC_MLF_01")
        self.assertEqual(adapted["source"]["misconception"], node["misconception"])
        self.assertEqual(adapted["weakness_relationships"]["topics"], node["related_topics"])
        self.assertEqual(adapted["weakness_relationships"]["concepts"], node["related_concepts"])


class TextEvidenceDetectionTests(unittest.TestCase):
    def test_each_node_is_detectable_from_its_canonical_statement(self) -> None:
        for mc_id, node in load_node_index().items():
            with self.subTest(mc_id=mc_id):
                result = detect_text_evidence(
                    node["misconception"],
                    candidate_ids=[mc_id],
                )
                self.assertTrue(result["detected"])
                self.assertEqual(result["misconception_id"], mc_id)
                self.assertTrue(result["matched_signals"])

    def test_detection_can_be_constrained_to_relevant_nodes(self) -> None:
        result = detect_text_evidence(
            "MLF always makes a wine taste buttery.",
            candidate_ids=["MC_OAK_01"],
        )

        self.assertFalse(result["detected"])
        self.assertIsNone(result["misconception_id"])

    def test_unknown_explicit_id_is_rejected(self) -> None:
        result = detect_text_evidence("", explicit_id="MC_DOES_NOT_EXIST")

        self.assertFalse(result["detected"])
        self.assertEqual(result["reason"], "unknown_misconception_id")

    def test_known_explicit_id_remains_backward_compatible(self) -> None:
        result = detect_text_evidence(
            "",
            explicit_id="MC_TANNIN_01",
            source_type="sba",
        )

        self.assertTrue(result["detected"])
        self.assertEqual(result["misconception_id"], "MC_TANNIN_01")
        self.assertEqual(result["detection_method"], "explicit_id")

    def test_generic_topic_weakness_is_not_direct_evidence(self) -> None:
        result = detect_text_evidence(
            "The learner is weak on winemaking.",
            source_type="weakness_profile",
        )

        self.assertFalse(result["detected"])

    def test_sba_or_sat_and_explicit_weakness_sources_use_same_adapter(self) -> None:
        statement = load_node_index()["MC_OAK_QUALITY_01"]["misconception"]
        for source_type in ("sba", "open_response", "sat"):
            with self.subTest(source_type=source_type):
                result = detect_text_evidence(
                    statement,
                    candidate_ids=["MC_OAK_QUALITY_01"],
                    source_type=source_type,
                )
                self.assertTrue(result["detected"])
                self.assertEqual(result["source_type"], source_type)

        weakness_result = detect_text_evidence(
            "",
            explicit_id="MC_OAK_QUALITY_01",
            source_type="weakness_profile",
        )
        self.assertTrue(weakness_result["detected"])
        self.assertEqual(weakness_result["source_type"], "weakness_profile")


if __name__ == "__main__":
    unittest.main()
