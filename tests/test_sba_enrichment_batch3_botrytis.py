"""Batch 3 Botrytis candidate coverage under matcher v2."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tools.question_generation.generate_batch3_candidate import (
    ACTIVE_SIDECAR,
    build_candidate_payload,
    write_candidate_sidecar,
)
from tools.question_generation.sba_enrichment_deriver import (
    MIN_KEYWORD_HITS,
    NODE_ES,
    REQUIRE_CORRECT_OPTION_HIT,
    REQUIRE_STEM_HIT,
    REQUIRE_UNIQUE_BEST,
    derive,
    load_chain_nodes,
)


BOTRYTIS_NODE_IDS = {
    "HC_BOTRYTIS_CONCENTRATION",
    "HC_NOBLE_ROT_DEVELOPMENT_CONDITIONS",
}


class Batch3BotrytisCandidateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.nodes = {node["node_id"]: node for node in load_chain_nodes()}
        cls.payload = derive()
        cls.records = {
            record["item_id"]: record
            for record in cls.payload["items_by_source_question_id"].values()
        }

    def test_candidate_nodes_are_matcher_compatible_and_localized(self):
        for node_id in BOTRYTIS_NODE_IDS:
            self.assertIn(node_id, self.nodes)
            self.assertIn(node_id, NODE_ES)

    def test_exact_botrytis_candidate_ids(self):
        candidate_ids = {
            item_id
            for item_id, record in self.records.items()
            if record["_provenance"]["causal_chain"]["derived_from"] in BOTRYTIS_NODE_IDS
        }
        self.assertEqual(candidate_ids, {"wset3_372", "wset3_426", "wset3_510"})

    def test_candidate_assignments_are_mechanism_specific(self):
        expected = {
            "wset3_372": "HC_BOTRYTIS_CONCENTRATION",
            "wset3_426": "HC_BOTRYTIS_CONCENTRATION",
            "wset3_510": "HC_NOBLE_ROT_DEVELOPMENT_CONDITIONS",
        }
        for item_id, node_id in expected.items():
            provenance = self.records[item_id]["_provenance"]["causal_chain"]
            self.assertEqual(provenance["derived_from"], node_id)
            self.assertTrue(provenance["stem_hits"])
            self.assertTrue(provenance["correct_option_hits"])
            self.assertGreaterEqual(provenance["match_score"], MIN_KEYWORD_HITS)

    def test_concentration_chain_preserves_botrytis_acidity_nuance(self):
        chain = self.records["wset3_372"]["causal_chain"]
        joined = " ".join(chain.values()).lower()
        self.assertIn("ácidos", joined)
        self.assertIn("metaboliza parte de los ácidos", joined)
        self.assertIn("no debe interpretarse como una regla simple", joined)

    def test_known_false_positive_classes_remain_excluded(self):
        for item_id in ("wset3_8", "wset3_350", "wset3_489", "wset3_783"):
            record = self.records.get(item_id)
            if record is None:
                continue
            node_id = record["_provenance"]["causal_chain"]["derived_from"]
            self.assertNotIn(node_id, BOTRYTIS_NODE_IDS)

    def test_matcher_v2_thresholds_are_unchanged(self):
        self.assertEqual(MIN_KEYWORD_HITS, 2)
        self.assertIs(REQUIRE_STEM_HIT, True)
        self.assertIs(REQUIRE_CORRECT_OPTION_HIT, True)
        self.assertIs(REQUIRE_UNIQUE_BEST, True)


class Batch3CandidateSidecarTests(unittest.TestCase):
    def test_candidate_payload_identifies_only_botrytis_additions(self):
        payload = build_candidate_payload()
        self.assertEqual(payload["phase"], "P.3-botrytis-candidate")
        self.assertEqual(payload["candidate_domain"], "botrytis_concentration")
        self.assertEqual(
            payload["candidate_item_ids"],
            ["wset3_372", "wset3_426", "wset3_510"],
        )
        self.assertEqual(payload["candidate_item_count"], 3)
        self.assertGreaterEqual(len(payload["items_by_source_question_id"]), 14)

    def test_candidate_writer_does_not_modify_active_sidecar(self):
        active_before = ACTIVE_SIDECAR.read_bytes()
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "candidate.json"
            written = write_candidate_sidecar(output)
            self.assertEqual(written, output)
            data = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(data["candidate_item_count"], 3)
        self.assertEqual(ACTIVE_SIDECAR.read_bytes(), active_before)


class Batch3PromotionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.active = json.loads(ACTIVE_SIDECAR.read_text(encoding="utf-8"))
        cls.records = {
            record["item_id"]: record
            for record in cls.active["items_by_source_question_id"].values()
        }

    def test_active_sidecar_retains_at_least_the_batch3_total(self):
        self.assertGreaterEqual(len(self.records), 14)

    def test_active_sidecar_contains_approved_batch3_items(self):
        for item_id in ("wset3_372", "wset3_426", "wset3_510"):
            self.assertIn(item_id, self.records)

    def test_promoted_copy_explains_water_loss_and_acid_nuance(self):
        chain = self.records["wset3_372"]["causal_chain"]
        joined = " ".join(chain.values()).lower()
        self.assertIn("agua se evapore", joined)
        self.assertIn("azúcares", joined)
        self.assertIn("compuestos de sabor", joined)
        self.assertIn("metaboliza parte de los ácidos", joined)
        self.assertIn("acidez neta", joined)

    def test_promoted_copy_requires_misty_mornings_followed_by_dry_afternoons(self):
        chain = self.records["wset3_510"]["causal_chain"]
        joined = " ".join(chain.values()).lower()
        self.assertIn("mañanas húmedas o con niebla", joined)
        self.assertIn("seguidas de tardes más cálidas y secas", joined)
        self.assertIn("tardes secas", joined)

    def test_rejected_items_remain_absent_from_active_sidecar(self):
        for item_id in ("wset3_8", "wset3_309", "wset3_350", "wset3_783"):
            self.assertNotIn(item_id, self.records)


if __name__ == "__main__":
    unittest.main()
