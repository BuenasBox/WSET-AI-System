import json
import unittest
from collections import Counter
from pathlib import Path

from tools.frontend.generate_production_payloads import sba_eligible
from tools.question_generation.sba_gap_closure import validate_batch_payload


BATCH_PATH = Path("knowledge/question-bank/sba_expansion/sba_batch_01.json")
STRUCTURED_PATH = Path("knowledge/question-bank/structured/wset3_questions.json")
MASTER_PATH = Path("knowledge/question-bank/master_bank/master_bank.json")
ENRICHMENT_PATH = Path("knowledge/question-bank/enrichment/sba_enrichment_v1.json")


class Batch1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.payload = json.loads(BATCH_PATH.read_text(encoding="utf-8"))
        cls.records = cls.payload["records"]

    def test_batch_contract(self):
        self.assertEqual(validate_batch_payload(self.payload), [])

    def test_ids_and_count(self):
        self.assertEqual(
            [record["question_id"] for record in self.records],
            [str(value) for value in range(858, 905)],
        )

    def test_ra_distribution(self):
        distribution = Counter(record["expected_topics"][0] for record in self.records)
        self.assertEqual(distribution, {"RA1": 4, "RA2": 36, "RA5": 7})

    def test_required_sweet_wine_domains_are_present(self):
        blob = json.dumps(self.records, ensure_ascii=False).lower()
        for term in (
            "icewine",
            "eiswein",
            "botrytis",
            "tokaji",
            "sauternes",
            "concentración",
            "servicio",
            "maridaje",
            "almacenamiento",
        ):
            self.assertIn(term, blob)

    def test_every_item_is_enrichment_ready(self):
        known_misconceptions = set()
        for path in Path("knowledge/knowledge-map/misconceptions").glob("*.json"):
            try:
                known_misconceptions.add(
                    json.loads(path.read_text(encoding="utf-8-sig"))["misconception_id"]
                )
            except (KeyError, json.JSONDecodeError):
                continue
        for record in self.records:
            enrichment = record["enrichment"]
            self.assertIn("causal_chain_candidate", enrichment)
            self.assertIn("feedback_profile", enrichment)
            self.assertIn("micro_drill_candidate", enrichment)
            self.assertIn("misconception_linkage_candidate", enrichment)
            self.assertIn(
                enrichment["misconception_linkage_candidate"]["misconception_id"],
                known_misconceptions,
            )

    def test_batch_is_integrated_into_backend_corpus(self):
        structured = json.loads(STRUCTURED_PATH.read_text(encoding="utf-8"))
        master = json.loads(MASTER_PATH.read_text(encoding="utf-8"))
        enrichment = json.loads(ENRICHMENT_PATH.read_text(encoding="utf-8"))
        expected_ids = {str(value) for value in range(858, 905)}
        self.assertTrue(
            expected_ids.issubset(
                {str(record["question_id"]) for record in structured}
            )
        )
        master_by_source = {
            item["source_question_id"]: item for item in master["items"]
        }
        for source_id in expected_ids:
            self.assertEqual(
                master_by_source[source_id]["status"]["review_state"],
                "approved_private_sba",
            )
            self.assertIn(
                source_id, enrichment["items_by_source_question_id"]
            )
        self.assertEqual(len(sba_eligible(master["items"])), 625)
        self.assertEqual(len(enrichment["items_by_source_question_id"]), 407)


if __name__ == "__main__":
    unittest.main()
