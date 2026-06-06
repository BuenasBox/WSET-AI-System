from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from tools.question_generation.master_bank import (
    COLLECTION_NAMES,
    MASTER_BANK_PATH,
    SAFE_GOVERNANCE,
    SCHEMA_PATH,
    build_collection_export,
    build_master_bank,
    validate_master_bank,
    write_master_bank,
)


ROOT = Path(__file__).resolve().parents[1]


class MasterBankTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.generated = build_master_bank(ROOT)
        cls.persisted = json.loads((ROOT / MASTER_BANK_PATH).read_text(encoding="utf-8"))
        cls.schema = json.loads((ROOT / SCHEMA_PATH).read_text(encoding="utf-8"))
        cls.public_payload = json.loads(
            (ROOT / "frontend/diagnostic-sba/preguntas.json").read_text(encoding="utf-8")
        )
        cls.open_candidates = json.loads(
            (
                ROOT
                / "knowledge/question-bank/open_response/normalized/diagnostic_open_response_candidates.json"
            ).read_text(encoding="utf-8")
        )

    def test_schema_file_is_valid_json_schema_contract(self) -> None:
        self.assertEqual(self.schema["$schema"], "https://json-schema.org/draft/2020-12/schema")
        self.assertEqual(self.schema["properties"]["schema_version"]["const"], "master_bank_v1")
        self.assertEqual(
            set(self.schema["properties"]["collections"]["required"]),
            set(COLLECTION_NAMES),
        )

    def test_generated_master_bank_is_valid(self) -> None:
        self.assertEqual(validate_master_bank(self.generated), [])

    def test_persisted_master_bank_matches_importer_exactly(self) -> None:
        self.assertEqual(self.persisted, self.generated)

    def test_importer_is_deterministic(self) -> None:
        self.assertEqual(build_master_bank(ROOT), build_master_bank(ROOT))

    def test_canonical_counts(self) -> None:
        counts = self.generated["counts"]

        self.assertEqual(counts["total"], 616)
        self.assertEqual(counts["single_best_answer"], 590)
        self.assertEqual(counts["open_response"], 26)
        self.assertEqual(counts["inactive"], 580)
        self.assertEqual(counts["needs_review"], 471)
        self.assertEqual(counts["gold"], 34)
        self.assertEqual(counts["public_lab"], 36)

    def test_review_state_counts(self) -> None:
        self.assertEqual(
            self.generated["counts"]["review_states"],
            {
                "approved_for_static_demo": 36,
                "approved_open_response": 26,
                "approved_private_sba": 83,
                "unreviewed": 471,
            },
        )

    def test_all_items_have_unique_identity_and_structured_lineage(self) -> None:
        items = self.generated["items"]
        master_ids = [item["master_item_id"] for item in items]
        source_ids = [item["source_question_id"] for item in items]

        self.assertEqual(len(master_ids), len(set(master_ids)))
        self.assertEqual(len(source_ids), len(set(source_ids)))
        for item in items:
            self.assertEqual(
                item["lineage"]["structured_source"],
                "knowledge/question-bank/structured/wset3_questions.json",
            )
            self.assertTrue(item["lineage"]["raw_source"])

    def test_sba_open_response_gold_and_public_lineage_exist(self) -> None:
        by_source = {
            item["source_question_id"]: item for item in self.generated["items"]
        }

        self.assertTrue(by_source["2"]["lineage"]["sba_draft_id"])
        self.assertTrue(by_source["2"]["lineage"]["sba_review_id"])
        self.assertTrue(by_source["2"]["lineage"]["public_lab_item_id"])
        self.assertIsNone(by_source["2"]["lineage"]["gold_review_id"])
        self.assertTrue(by_source["21"]["lineage"]["gold_review_id"])
        self.assertTrue(by_source["798"]["lineage"]["open_response_candidate_id"])
        self.assertTrue(by_source["798"]["lineage"]["open_response_review_id"])

    def test_governance_is_safe_at_bank_and_item_level(self) -> None:
        self.assertEqual(self.generated["governance"], SAFE_GOVERNANCE)
        for item in self.generated["items"]:
            self.assertEqual(item["governance"], SAFE_GOVERNANCE)

    def test_current_public_sba_36_are_preserved_exactly(self) -> None:
        source_ids = [
            item["source_question_id"] for item in self.public_payload["items"]
        ]
        master_source_ids = [
            item["source_question_id"]
            for item in self.generated["items"]
            if "public_lab" in item["collections"]
        ]

        self.assertEqual(master_source_ids, source_ids)
        self.assertEqual(len(source_ids), 36)

    def test_open_response_remains_inactive(self) -> None:
        self.assertEqual(len(self.open_candidates), 26)
        self.assertTrue(
            all(item["activation_status"] == "inactive" for item in self.open_candidates)
        )
        master_open = [
            item
            for item in self.generated["items"]
            if item["question_type"] == "open_response"
        ]
        self.assertEqual(len(master_open), 26)
        self.assertTrue(
            all(item["status"]["activation_status"] == "inactive" for item in master_open)
        )
        self.assertTrue(all("public_lab" not in item["collections"] for item in master_open))

    def test_collection_export_contains_only_requested_members(self) -> None:
        export = build_collection_export(self.generated, "gold")

        self.assertEqual(export["collection"], "gold")
        self.assertEqual(export["item_count"], 34)
        self.assertTrue(all("gold" in item["collections"] for item in export["items"]))
        self.assertEqual(export["governance"], SAFE_GOVERNANCE)

    def test_unknown_collection_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            build_collection_export(self.generated, "combined_exam")

    def test_validator_rejects_governance_violation(self) -> None:
        unsafe = copy.deepcopy(self.generated)
        unsafe["items"][0]["governance"]["safe_for_examiner"] = True

        self.assertIn("wset3_1: unsafe governance", validate_master_bank(unsafe))

    def test_write_round_trip_uses_explicit_destination(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = write_master_bank(
                self.generated,
                path=Path("knowledge/question-bank/master_bank/test.json"),
                root=tmp,
            )
            loaded = json.loads(output.read_text(encoding="utf-8"))

        self.assertEqual(loaded, self.generated)


if __name__ == "__main__":
    unittest.main()
