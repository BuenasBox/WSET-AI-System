import json
import unittest
from collections import Counter
from pathlib import Path

from tools.question_generation.sba_gap_closure import validate_batch_payload


BATCH_PATH = Path("knowledge/question-bank/sba_expansion/sba_batch_02.json")


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


if __name__ == "__main__":
    unittest.main()
