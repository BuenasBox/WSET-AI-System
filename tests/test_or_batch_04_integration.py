"""Integration contract for the 138-item Open Response bank."""

from __future__ import annotations

import json
import re
import tempfile
import unittest
from pathlib import Path

from tools.question_generation.open_response_lab_runtime import (
    LAB_PAYLOAD_GLOBAL,
    build_lab_runtime_payload,
    load_integrated_open_response_candidates,
    validate_lab_runtime_payload,
    write_lab_payload_js,
)


ROOT = Path(__file__).resolve().parents[1]
PAYLOAD_PATH = ROOT / "frontend/open-response-lab/lab_payload.js"


def _read_payload(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    match = re.fullmatch(
        rf"window\.{LAB_PAYLOAD_GLOBAL}\s*=\s*(\{{.*\}});\s*",
        text,
        re.DOTALL,
    )
    if not match:
        raise AssertionError("lab payload is not valid generated JavaScript")
    return json.loads(match.group(1))


class OpenResponseBatch4IntegrationTests(unittest.TestCase):
    def test_adapter_loads_all_bank_items_without_parallel_schema(self) -> None:
        candidates = load_integrated_open_response_candidates()
        self.assertEqual(len(candidates), 138)
        self.assertEqual(candidates[0]["item_id"], "OR_001")
        self.assertEqual(candidates[-1]["item_id"], "OR_138")
        self.assertEqual(candidates[-1]["source_question_id"], "OR_138")
        self.assertEqual(candidates[-1]["stem"], candidates[-1]["question_text"])

    def test_runtime_payload_contains_all_items_and_validates(self) -> None:
        payload = build_lab_runtime_payload()
        self.assertEqual(payload["pool_size"], 138)
        self.assertEqual(len(payload["items"]), 138)
        self.assertEqual(validate_lab_runtime_payload(payload), [])
        self.assertIn("OR_138", {item["item_id"] for item in payload["items"]})

    def test_generated_payload_round_trips(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "lab_payload.js"
            write_lab_payload_js(path=target)
            payload = _read_payload(target)
        self.assertEqual(payload["pool_size"], 138)
        self.assertEqual(len(payload["evaluation_by_item_id"]), 138)

    def test_committed_payload_was_regenerated_from_bank(self) -> None:
        payload = _read_payload(PAYLOAD_PATH)
        self.assertEqual(payload["pool_size"], 138)
        self.assertEqual(len(payload["items"]), 138)
        self.assertEqual(payload["source_bank_total"], 138)

    def test_full_simulation_mock_pool_has_four_valid_items(self) -> None:
        payload = build_lab_runtime_payload()
        session = payload["sessions"]["mock_theory_2"]
        self.assertEqual(session["session_size"], 4)
        self.assertEqual(len(session["item_ids"]), 4)
        self.assertEqual(len(set(session["item_ids"])), 4)
        item_ras = {
            item["item_id"]: item["RA"]
            for item in payload["items"]
        }
        self.assertEqual(
            [item_ras[item_id] for item_id in session["item_ids"]],
            ["RA2", "RA2", "RA2", "RA4"],
        )

    def test_y3_coaching_metadata_is_available_for_every_batch_item(self) -> None:
        payload = build_lab_runtime_payload()
        evaluation = payload["evaluation_by_item_id"]
        self.assertIn(
            "recommend",
            payload["assessment_intelligence"]["command_verbs"],
        )
        for number in range(107, 139):
            item_id = f"OR_{number:03d}"
            self.assertIn(item_id, evaluation)
            self.assertTrue(evaluation[item_id]["expected_concepts"])
            self.assertIn("feedback_profile", evaluation[item_id])
            self.assertIn("causal_chain_reference", evaluation[item_id])

    def test_legacy_item_ids_remain_stable(self) -> None:
        payload = build_lab_runtime_payload()
        ids = {item["item_id"] for item in payload["items"]}
        self.assertTrue({f"OR_{number:03d}" for number in range(1, 107)} <= ids)


if __name__ == "__main__":
    unittest.main()
