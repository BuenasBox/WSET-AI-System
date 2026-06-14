from __future__ import annotations

import json
import unittest
from pathlib import Path

from tools.question_generation.open_response_lab_runtime import (
    LAB_PAYLOAD_GLOBAL,
    build_formative_feedback,
    build_lab_runtime_payload,
    validate_lab_runtime_payload,
)
from tools.question_generation.open_response_session_engine import (
    LAB_GOVERNANCE_FLAGS,
    compose_session,
    load_open_response_candidates,
)


FRONTEND_DIR = Path("frontend/open-response-lab")
INDEX_PATH = FRONTEND_DIR / "index.html"
PAYLOAD_PATH = FRONTEND_DIR / "lab_payload.js"


def read_payload_js() -> dict:
    text = PAYLOAD_PATH.read_text(encoding="utf-8")
    prefix = f"window.{LAB_PAYLOAD_GLOBAL} = "
    assert text.startswith(prefix)
    return json.loads(text[len(prefix):].strip().removesuffix(";"))


class OpenResponseLabRuntimeMVPTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.candidates = load_open_response_candidates()
        cls.payload = read_payload_js()
        cls.html = INDEX_PATH.read_text(encoding="utf-8")

    def test_frontend_files_exist(self) -> None:
        self.assertTrue(INDEX_PATH.is_file())
        self.assertTrue(PAYLOAD_PATH.is_file())

    def test_payload_validates(self) -> None:
        self.assertEqual(validate_lab_runtime_payload(self.payload), [])

    def test_payload_is_generated_from_runtime_builder(self) -> None:
        # P2.3 enrichment adds command_verb, expected_concepts, evaluation_config
        # P2.4 expansion adds 15 new items
        # So the file payload is a superset of the builder output
        built = build_lab_runtime_payload(self.candidates)

        # File should have at least as many items as builder (plus P2.4 expansion)
        self.assertGreaterEqual(len(self.payload["items"]), len(built["items"]),
                               "Payload should have builder items plus any P2.4 expansion")
        # Pool size should match item count
        self.assertEqual(self.payload["pool_size"], len(self.payload["items"]),
                        "Pool size should match items count")

    def test_session_selection_uses_existing_session_engine_outputs(self) -> None:
        for session_name, expected_size in (("short_practice", 1), ("standard_practice", 2), ("extended_practice", 4), ("mock_theory_2", 4)):
            expected = compose_session(self.candidates, session_size=session_name)
            actual = self.payload["sessions"][session_name]
            self.assertEqual(actual["session_size"], expected_size)
            self.assertEqual(actual["source_question_ids"], expected["source_question_ids"])
            self.assertEqual(len(actual["item_ids"]), expected_size)

    def test_question_render_items_expose_only_allowed_fields(self) -> None:
        # Phase P2.3 added: command_verb, expected_concepts, evaluation_config (safe metadata)
        allowed_base = {"item_id", "source_question_id", "stem", "topic", "RA"}
        allowed_p2_evaluation = {"command_verb", "expected_concepts", "evaluation_config"}

        for item in self.payload["items"]:
            item_keys = set(item.keys())
            # Should have base fields
            self.assertTrue(allowed_base.issubset(item_keys))
            # May have P2 evaluation fields
            self.assertTrue(item_keys.issubset(allowed_base | allowed_p2_evaluation))

            self.assertTrue(item["stem"])
            self.assertTrue(item["topic"])
            self.assertTrue(item["RA"])

            # Forbidden fields (actual answers, scoring, corpus metadata)
            self.assertNotIn("feedback_rubric", item)
            self.assertNotIn("corpus_support", item)
            self.assertNotIn("optional_causal_chain", item)
            self.assertNotIn("correct_answer", item)

    def test_html_presents_stem_topic_and_ra_targets(self) -> None:
        self.assertIn('data-testid="question-stem"', self.html)
        self.assertIn('data-testid="question-topic"', self.html)
        self.assertIn('data-testid="question-ra"', self.html)

    def test_answer_submission_uses_textarea_and_local_storage_only(self) -> None:
        self.assertIn("<textarea", self.html)
        self.assertIn('data-testid="answer-input"', self.html)
        self.assertIn("localStorage.setItem(storageKey", self.html)
        self.assertIn("localStorage.getItem(storageKey", self.html)
        self.assertNotIn("fetch(", self.html)
        self.assertNotIn("XMLHttpRequest", self.html)
        self.assertNotIn("navigator.sendBeacon", self.html)

    def test_feedback_rendering_has_only_allowed_formative_sections(self) -> None:
        for test_id in (
            "concepts-detected",
            "concepts-absent",
            "missing-causal-reasoning",
            "improvement-suggestions",
        ):
            self.assertIn(f'data-testid="{test_id}"', self.html)
        for forbidden in ("Score", "Nota", "Porcentaje", "Pass", "Fail", "equivalencia WSET"):
            self.assertNotIn(forbidden, self.html)

    def test_runtime_feedback_delegates_to_existing_pipeline_shape(self) -> None:
        candidate = next(item for item in self.candidates if item["source_question_id"] == "799")
        feedback = build_formative_feedback(
            candidate,
            "La fermentación maloláctica convierte ácido málico en láctico porque suaviza la acidez.",
        )

        self.assertIn("fermentación maloláctica", feedback["concepts_detected"])
        self.assertIn("concepts_absent", feedback)
        self.assertIn("missing_causal_reasoning", feedback)
        self.assertIn("improvement_suggestions", feedback)
        for forbidden in ("score", "mark", "grade", "percentage", "pass_fail", "wset_equivalence"):
            self.assertNotIn(forbidden, feedback)

    def test_navigation_controls_are_present(self) -> None:
        for test_id in ("next-question", "finish-session", "restart-session", "completion-panel"):
            self.assertIn(f'data-testid="{test_id}"', self.html)

    def test_session_completion_is_local_state_only(self) -> None:
        self.assertIn("function finishSession()", self.html)
        self.assertIn("state.completed = true", self.html)
        self.assertIn("Las respuestas quedan solo en este navegador.", self.html)

    def test_governance_flags_remain_false(self) -> None:
        self.assertEqual(self.payload["governance_flags"], LAB_GOVERNANCE_FLAGS)
        self.assertFalse(self.payload["governance_flags"]["safe_for_examiner"])
        self.assertFalse(self.payload["governance_flags"]["examiner_scoring_allowed"])
        self.assertFalse(self.payload["governance_flags"]["uses_llm"])
        self.assertFalse(self.payload["governance_flags"]["uses_api"])
        self.assertFalse(self.payload["governance_flags"]["uses_embeddings"])
        self.assertFalse(self.payload["governance_flags"]["uses_vector_db"])
        self.assertFalse(self.payload["governance_flags"]["cloud_services_active"])
        self.assertFalse(self.payload["governance_flags"]["open_response_lab_active"])

    def test_lab_is_not_integrated_with_dashboard_or_other_frontends(self) -> None:
        dashboard = Path("frontend/architecture-dashboard/index.html").read_text(encoding="utf-8")
        self.assertNotIn("open-response-lab", dashboard)
        self.assertNotIn("diagnostic-sba", INDEX_PATH.as_posix())

    def test_no_forbidden_backend_references(self) -> None:
        combined = self.html + "\n" + PAYLOAD_PATH.read_text(encoding="utf-8")
        for forbidden in (
            "api.openai",
            "api.anthropic",
            "firebase",
            "supabase",
            "amazonaws.com",
            "google-analytics",
            "gtag(",
        ):
            self.assertNotIn(forbidden, combined)


if __name__ == "__main__":
    unittest.main()
