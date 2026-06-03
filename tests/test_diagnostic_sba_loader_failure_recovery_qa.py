from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from tests.fixtures.diagnostic_sba.loader_failure_recovery_server import (
    COCKPIT_PATH,
    PREGUNTAS_PATH,
    SCENARIOS,
    build_scenario_response,
    load_payload,
)


REPORT_PATH = Path("docs/DIAGNOSTIC_SBA_DEPLOYED_LOADER_FAILURE_RECOVERY_QA.md")


class DiagnosticSbaLoaderFailureRecoveryQaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.payload = load_payload()

    def test_fixture_uses_real_cockpit_and_preguntas_paths_read_only(self) -> None:
        self.assertTrue(COCKPIT_PATH.exists())
        self.assertTrue(PREGUNTAS_PATH.exists())

    def test_required_scenarios_are_defined(self) -> None:
        self.assertEqual(
            SCENARIOS,
            (
                "valid",
                "missing",
                "forbidden",
                "server_error",
                "corrupt_json",
                "invalid_structure",
                "missing_options",
                "missing_outcome",
                "inconsistent_outcome",
                "recovery",
            ),
        )

    def test_http_failure_scenarios_return_expected_statuses(self) -> None:
        expected = {"missing": 404, "forbidden": 403, "server_error": 500}

        for scenario, status in expected.items():
            with self.subTest(scenario=scenario):
                actual_status, _, _ = build_scenario_response(scenario, self.payload)
                self.assertEqual(actual_status, status)

    def test_corrupt_json_scenario_is_not_parseable(self) -> None:
        status, content_type, body = build_scenario_response("corrupt_json", self.payload)

        self.assertEqual(status, 200)
        self.assertIn("application/json", content_type)
        with self.assertRaises(json.JSONDecodeError):
            json.loads(body.decode("utf-8"))

    def test_invalid_structure_scenario_has_non_list_items(self) -> None:
        _, _, body = build_scenario_response("invalid_structure", self.payload)
        payload = json.loads(body.decode("utf-8"))

        self.assertEqual(payload["items"], "not-a-list")

    def test_missing_options_scenario_has_incomplete_a_to_d_options(self) -> None:
        _, _, body = build_scenario_response("missing_options", self.payload)
        payload = json.loads(body.decode("utf-8"))

        self.assertEqual([option["option_id"] for option in payload["items"][0]["options"]], ["A", "B", "C"])

    def test_missing_outcome_scenario_removes_matching_outcome(self) -> None:
        _, _, body = build_scenario_response("missing_outcome", self.payload)
        payload = json.loads(body.decode("utf-8"))
        first_item_id = payload["items"][0]["item_id"]

        self.assertNotIn(first_item_id, payload["outcomes_by_item_id"])

    def test_inconsistent_outcome_scenario_mismatches_item_id(self) -> None:
        _, _, body = build_scenario_response("inconsistent_outcome", self.payload)
        payload = json.loads(body.decode("utf-8"))
        first_item_id = payload["items"][0]["item_id"]

        self.assertNotEqual(payload["outcomes_by_item_id"][first_item_id]["item_id"], first_item_id)

    def test_recovery_scenario_returns_invalid_then_valid_payload(self) -> None:
        _, _, first_body = build_scenario_response("recovery", self.payload, request_count=0)
        _, _, second_body = build_scenario_response("recovery", self.payload, request_count=1)
        first_payload = json.loads(first_body.decode("utf-8"))
        second_payload = json.loads(second_body.decode("utf-8"))

        self.assertEqual(first_payload["items"], "not-a-list")
        self.assertEqual(second_payload, self.payload)

    def test_scenarios_do_not_mutate_source_payload_or_real_file(self) -> None:
        payload_before = copy.deepcopy(self.payload)
        file_before = PREGUNTAS_PATH.read_text(encoding="utf-8")

        for scenario in SCENARIOS:
            build_scenario_response(scenario, self.payload)

        self.assertEqual(self.payload, payload_before)
        self.assertEqual(PREGUNTAS_PATH.read_text(encoding="utf-8"), file_before)

    def test_qa_report_exists(self) -> None:
        self.assertTrue(REPORT_PATH.exists())


if __name__ == "__main__":
    unittest.main()
