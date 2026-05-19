import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAUSAL_CHAIN_DIR = ROOT / "knowledge" / "knowledge-map" / "causal-chains"
SAT_CHAIN_FILES = {
    "CC_SAT_QUALITY_HIGH": CAUSAL_CHAIN_DIR / "CC_SAT_QUALITY_HIGH.json",
    "CC_SAT_QUALITY_MEDIUM": CAUSAL_CHAIN_DIR / "CC_SAT_QUALITY_MEDIUM.json",
}


def _load_node(node_id: str) -> dict:
    path = SAT_CHAIN_FILES[node_id]
    return json.loads(path.read_text(encoding="utf-8"))


class SatCausalChainTests(unittest.TestCase):
    def test_sat_quality_chain_files_exist_and_load_as_json(self) -> None:
        for node_id, path in SAT_CHAIN_FILES.items():
            with self.subTest(node_id=node_id):
                self.assertTrue(path.exists())
                self.assertIsInstance(_load_node(node_id), dict)

    def test_sat_quality_chain_schema_and_governance(self) -> None:
        for node_id, path in SAT_CHAIN_FILES.items():
            with self.subTest(node_id=node_id):
                node = _load_node(node_id)
                self.assertEqual(node["node_type"], "causal_chain")
                self.assertEqual(node["node_id"], path.stem)
                self.assertEqual(node["node_id"], node_id)
                self.assertIsInstance(node["steps"], list)
                self.assertTrue(node["steps"])
                self.assertTrue(any(step.get("label") == "exam_formulation" for step in node["steps"]))
                self.assertIs(node["safe_for_examiner"], False)
                self.assertIs(node["governance"]["safe_for_examiner"], False)
                self.assertIs(node["examiner_scoring_allowed"], False)
                self.assertIs(node["governance"]["examiner_scoring_allowed"], False)
                self.assertIsInstance(node["sat_relevance"], str)
                self.assertTrue(node["sat_relevance"].strip())
                self.assertIsInstance(node["trigger_keywords"], list)
                self.assertTrue(node["trigger_keywords"])
                self.assertEqual(node["_meta"]["schema_version"], "causal_chain_v1")
                self.assertEqual(node["_meta"]["ingestion_status"], "draft")
                self.assertIs(node["requires_human_review"], True)

    def test_sat_quality_chains_have_bidirectional_links(self) -> None:
        high = _load_node("CC_SAT_QUALITY_HIGH")
        medium = _load_node("CC_SAT_QUALITY_MEDIUM")
        self.assertIn("CC_SAT_QUALITY_MEDIUM", high["linked_topics"])
        self.assertIn("CC_SAT_QUALITY_HIGH", medium["linked_topics"])


if __name__ == "__main__":
    unittest.main()
