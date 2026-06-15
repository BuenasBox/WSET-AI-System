import json
import unittest
from collections import Counter
from pathlib import Path

from tools.question_generation.sba_gap_closure import validate_batch_payload


BATCH_PATH = Path("knowledge/question-bank/sba_expansion/sba_batch_02.json")
STRUCTURED_PATH = Path("knowledge/question-bank/structured/wset3_questions.json")
MASTER_PATH = Path("knowledge/question-bank/master_bank/master_bank.json")
ENRICHMENT_PATH = Path("knowledge/question-bank/enrichment/sba_enrichment_v1.json")


class Batch2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.payload = json.loads(BATCH_PATH.read_text(encoding="utf-8"))
        cls.records = cls.payload["records"]

    def test_batch_contract(self):
        self.assertEqual(validate_batch_payload(self.payload), [])

    def test_ids_and_count(self):
        self.assertEqual(
            [record["question_id"] for record in self.records],
            [str(value) for value in range(905, 952)],
        )

    def test_all_items_map_to_ra4(self):
        distribution = Counter(record["expected_topics"][0] for record in self.records)
        self.assertEqual(distribution, {"RA4": 47})

    def test_required_fortified_domains_are_present(self):
        blob = json.dumps(self.records, ensure_ascii=False).lower()
        for term in (
            "port",
            "sherry",
            "madeira",
            "rutherglen",
            "fortificación",
            "biológica",
            "oxidativa",
            "compar",
        ):
            self.assertIn(term, blob)

    def test_every_linked_misconception_exists(self):
        known = set()
        for path in Path("knowledge/knowledge-map/misconceptions").glob("*.json"):
            known.add(
                json.loads(path.read_text(encoding="utf-8-sig"))["misconception_id"]
            )
        for record in self.records:
            self.assertIn(
                record["enrichment"]["misconception_linkage_candidate"][
                    "misconception_id"
                ],
                known,
            )

    def test_batch_is_integrated_into_backend_corpus(self):
        structured = json.loads(STRUCTURED_PATH.read_text(encoding="utf-8"))
        master = json.loads(MASTER_PATH.read_text(encoding="utf-8"))
        enrichment = json.loads(ENRICHMENT_PATH.read_text(encoding="utf-8"))
        expected_ids = {str(value) for value in range(905, 952)}

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


if __name__ == "__main__":
    unittest.main()
