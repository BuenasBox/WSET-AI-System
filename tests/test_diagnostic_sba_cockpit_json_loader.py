from __future__ import annotations

import re
import unittest
from pathlib import Path


COCKPIT_PATH = Path("frontend/diagnostic-sba/index.html")
EXPORT_PATH = Path("frontend/diagnostic-sba/preguntas.json")
DISCLAIMER = "PROTOTIPO ESTÁTICO · ENTRENAMIENTO · NO EVALUACIÓN OFICIAL WSET"


def cockpit_html() -> str:
    return COCKPIT_PATH.read_text(encoding="utf-8")


def function_body(html: str, function_name: str) -> str:
    marker = f"function {function_name}("
    start = html.index(marker)
    next_function = html.find("\n  function ", start + len(marker))
    if next_function == -1:
        return html[start:]
    return html[start:next_function]


class DiagnosticSbaCockpitJsonLoaderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.html = cockpit_html()

    def test_export_file_exists(self) -> None:
        self.assertTrue(EXPORT_PATH.exists())

    def test_cockpit_references_preguntas_json(self) -> None:
        self.assertIn("var DATA_URL = './preguntas.json';", self.html)
        self.assertIn("fetch(DATA_URL)", self.html)

    def test_cockpit_contains_loading_state(self) -> None:
        self.assertIn("function setLoadingState()", self.html)
        self.assertIn("Cargando preguntas desde ./preguntas.json", self.html)

    def test_cockpit_contains_error_state(self) -> None:
        self.assertIn("function setErrorState(message)", self.html)
        self.assertIn("ERROR · Laboratorio privado · No se cargó preguntas.json", self.html)
        self.assertIn("Laboratorio privado estático sin backend", self.html)

    def test_payload_validation_covers_minimum_render_structure(self) -> None:
        validate_item = function_body(self.html, "validateItem")

        for token in ("item.item_id", "item.stem", "item.options", "option.visual_option_id", "option.option_id", "option.option_text"):
            self.assertIn(token, self.html)
        self.assertIn("item.options.length !== 4", validate_item)
        self.assertIn("visualOptionIds.join(',') !== 'A,B,C,D'", validate_item)
        self.assertIn("optionIds.slice().sort().join(',') !== 'A,B,C,D'", validate_item)

    def test_payload_validation_is_governance_fail_closed(self) -> None:
        safe_governance = function_body(self.html, "hasSafeGovernance")
        validate_item = function_body(self.html, "validateItem")
        validate_outcome = function_body(self.html, "validateOutcome")

        for token in (
            "training_item_only === true",
            "static_demo_only === true",
            "official_wset_question === false",
            "safe_for_examiner === false",
            "examiner_scoring_allowed === false",
        ):
            self.assertIn(token, safe_governance)
        self.assertIn("hasSafeGovernance(item.governance)", validate_item)
        self.assertIn("hasSafeGovernance(outcome.governance)", validate_outcome)

    def test_payload_validation_requires_matching_usable_outcome(self) -> None:
        validate_outcome = function_body(self.html, "validateOutcome")
        validate_payload = function_body(self.html, "validatePayload")

        self.assertIn("outcome.item_id === itemId", validate_outcome)
        self.assertIn("outcome.correct_option_id", validate_outcome)
        self.assertIn("optionIds.indexOf(outcome.correct_option_id) !== -1", validate_outcome)
        self.assertIn("new Set(itemIds).size !== itemIds.length", validate_payload)

    def test_loader_validates_before_activating_loaded_data(self) -> None:
        loader = function_body(self.html, "loadStaticDemoPayload")

        validation_index = loader.index("validatePayload(payload)")
        question_assignment_index = loader.index("QS = payload.items")
        outcome_assignment_index = loader.index("OUTCOMES_BY_ITEM_ID = payload.outcomes_by_item_id")

        self.assertLess(validation_index, question_assignment_index)
        self.assertLess(validation_index, outcome_assignment_index)

    def test_error_state_has_no_embedded_question_fallback(self) -> None:
        error_state = function_body(self.html, "setErrorState")

        self.assertIn("document.getElementById('opts').innerHTML = ''", error_state)
        self.assertIn("document.getElementById('btn-confirm').style.display = 'none'", error_state)
        self.assertNotIn("QS =", error_state)

    def test_cockpit_does_not_embed_old_mock_bank_as_primary_source(self) -> None:
        self.assertNotRegex(self.html, r"var\s+QS\s*=\s*\[\s*\{")
        self.assertNotIn("const QUESTIONS", self.html)
        self.assertNotIn("mock — 4 preguntas de demostración", self.html)
        self.assertNotIn("q.diag", self.html)
        self.assertNotIn("correcta:", self.html)

    def test_pre_submit_render_logic_does_not_expose_correctness(self) -> None:
        load_q = function_body(self.html, "loadQ")

        self.assertNotIn("correct_option_id", load_q)
        self.assertNotIn("is_correct", load_q)
        self.assertNotIn("diagnostic_role", load_q)
        self.assertNotIn("remediation", load_q)
        self.assertNotIn("feedback", load_q)
        self.assertNotIn("causal_chain", load_q)

    def test_outcome_access_is_after_submit_only(self) -> None:
        load_q = function_body(self.html, "loadQ")
        confirm = function_body(self.html, "confirmAnswer")

        self.assertNotIn("OUTCOMES_BY_ITEM_ID", load_q)
        self.assertIn("OUTCOMES_BY_ITEM_ID[q.item_id]", confirm)

    def test_data_loading_navigation_and_render_remain_separate(self) -> None:
        loader = function_body(self.html, "loadStaticDemoPayload")
        load_q = function_body(self.html, "loadQ")

        self.assertIn("fetch(DATA_URL)", loader)
        self.assertNotIn("fetch(", load_q)
        self.assertNotIn("validatePayload(", load_q)

    def test_disclaimer_preserved(self) -> None:
        self.assertIn(DISCLAIMER, self.html)
        self.assertIn("LABORATORIO PRIVADO", self.html)
        self.assertIn("SIN AUTORIDAD EXAMINADORA", self.html)

    def test_no_external_dependencies(self) -> None:
        self.assertNotIn("<script src=", self.html.lower())
        self.assertNotIn("<link rel=\"stylesheet\" href=\"http", self.html.lower())

    def test_no_backend_api_or_supabase_calls(self) -> None:
        forbidden = ("api/", "/api", "Supabase", "supabase", "createClient", "POST", "XMLHttpRequest")

        for token in forbidden:
            self.assertNotIn(token, self.html)
        self.assertEqual(re.findall(r"fetch\(([^)]*)\)", self.html), ["DATA_URL"])

    def test_no_non_sba_interaction_types_remain(self) -> None:
        forbidden = (
            "chain-fill",
            "tag selection",
            "ordering",
            "fill-in-the-blank",
            "open response",
            "respuesta abierta",
            "ordenar",
            "rellenar",
        )
        lower = self.html.lower()

        for token in forbidden:
            self.assertNotIn(token, lower)

    def test_sba_interactions_remain(self) -> None:
        self.assertIn("q.options.forEach", self.html)
        self.assertIn("option_id", self.html)
        self.assertIn("conf-btn", self.html)
        self.assertIn("Confirmar respuesta", self.html)
        self.assertIn("Análisis del Distractor", self.html)
        self.assertIn("Cadena Causal", self.html)

    def test_confidence_is_required_before_commit(self) -> None:
        pick_opt = function_body(self.html, "pickOpt")
        confirm_click = self.html[
            self.html.index("document.getElementById('btn-confirm').addEventListener('click'")
            : self.html.index("document.addEventListener('keydown'")
        ]
        keydown = self.html[
            self.html.index("document.addEventListener('keydown'")
            : self.html.index("function confirmAnswer()")
        ]

        self.assertIn("bc.disabled = S.conf === null;", pick_opt)
        self.assertIn("S.conf === null", confirm_click)
        self.assertIn("S.conf !== null", keydown)


if __name__ == "__main__":
    unittest.main()
