import json
import tempfile
import unittest
from pathlib import Path

from tools.constants import PROJECT_ROOT
from tools.retrieval.tutor_retrieval_sandbox import (
    STOPWORDS,
    classify_query,
    load_retrieval_context,
    select_matched_causal_chain_nodes,
)
from tools.self_eval.question_runner import run_question_attempt
from tools.tutor.answer_builder import _select_best_causal_chain


Q24_TEXT = "¿Cuál es una diferencia técnica entre Cava y Champagne?"
CANOPY_NODE_ID = "HC_CANOPY_VIGOUR_EXPOSURE"
VITICULTURE_NODE_PREFIXES = (
    "CC_MECHANICAL_HARVEST",
    "CC_SOIL_",
    "CC_SPRING_FROST",
    "HC_ALTITUDE_",
    "HC_CANOPY_",
    "HC_COVER_CROP",
    "HC_DRIP_IRRIGATION",
    "HC_EARLY_GROWTH",
    "HC_FROST_",
    "HC_LOW_VIGOUR",
    "HC_NIGHT_HARVEST",
    "HC_SANDY_SOIL",
    "HC_SOLAR_EXPOSURE",
    "HC_SOUTH_FACING",
    "HC_WATER_STRESS",
    "HC_YIELD_",
)


class SpanishRetrievalFalsePositiveTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.context = load_retrieval_context(PROJECT_ROOT)

    def _matched_chain_ids(self, query):
        analysis = classify_query(
            query,
            self.context.dictionary_terms,
            self.context.knowledge_nodes,
        )
        return [item["id"] for item in analysis["matched_causal_chains"]]

    def test_required_spanish_and_low_signal_stopwords_are_excluded(self):
        required = {
            "es",
            "son",
            "ser",
            "estar",
            "está",
            "están",
            "fue",
            "fueron",
            "ha",
            "han",
            "hay",
            "que",
            "qué",
            "el",
            "la",
            "los",
            "las",
            "un",
            "una",
            "unos",
            "unas",
            "de",
            "del",
            "al",
            "en",
            "con",
            "por",
            "para",
            "como",
            "más",
            "menos",
            "muy",
            "también",
            "pero",
            "porque",
            "sobre",
            "entre",
            "donde",
            "cuando",
            "cual",
            "cuál",
            "cuáles",
            "técnica",
            "técnicas",
            "método",
            "métodos",
            "proceso",
            "procesos",
            "vino",
            "vinos",
            "uva",
            "uvas",
        }
        self.assertTrue(required.issubset(STOPWORDS))

    def test_es_and_tecnica_cannot_trigger_canopy_node(self):
        self.assertNotIn(
            CANOPY_NODE_ID,
            self._matched_chain_ids("¿Es una técnica?"),
        )

    def test_q24_does_not_retrieve_canopy_chain(self):
        self.assertNotIn(CANOPY_NODE_ID, self._matched_chain_ids(Q24_TEXT))

    def test_sparkling_questions_do_not_receive_viticulture_chains(self):
        sparkling_questions = (
            Q24_TEXT,
            "¿Cuál es el propósito del licor de tiraje?",
            "¿Qué distingue al método tradicional del método de tanque en vinos espumosos?",
            "¿Qué papel juega la autólisis en los vinos espumosos tradicionales?",
            "¿Qué país produce espumosos de calidad bajo el nombre de Cap Classique?",
            "¿Qué país produce espumosos de alta calidad en regiones como Marlborough y Tasmania?",
            "¿Qué distingue a un espumoso rosado hecho por sangrado frente a uno de mezcla?",
            "¿Qué término se usa en Champagne para referirse al prensado suave?",
        )
        for question in sparkling_questions:
            with self.subTest(question=question):
                leaking = [
                    node_id
                    for node_id in self._matched_chain_ids(question)
                    if node_id.startswith(VITICULTURE_NODE_PREFIXES)
                ]
                self.assertEqual(leaking, [])

    def test_cool_climate_sparkling_query_does_not_receive_mosel_chain(self):
        chain_ids = self._matched_chain_ids(
            "¿Qué región chilena es reconocida por espumosos de calidad debido a su clima fresco?"
        )
        self.assertIn("HC_COOL_CLIMATE_STYLE", chain_ids)
        self.assertNotIn("HC_MOSEL_COOL_SLOPE_ACIDITY", chain_ids)

    def test_valid_canopy_vigour_query_still_matches_canopy_node(self):
        self.assertIn(
            CANOPY_NODE_ID,
            self._matched_chain_ids(
                "¿Cómo influye el manejo del dosel en el vigor y la exposición de los racimos?"
            ),
        )

    def test_valid_viticulture_query_still_matches_soil_drainage_chain(self):
        self.assertIn(
            "CC_SOIL_DRAINAGE_VINE_VIGOUR",
            self._matched_chain_ids(
                "¿Cómo influye el drenaje del suelo en el vigor de la vid?"
            ),
        )

    def test_matched_nodes_remain_governance_safe(self):
        analysis = classify_query(
            "¿Cómo influye el manejo del dosel en el vigor y la exposición de los racimos?",
            self.context.dictionary_terms,
            self.context.knowledge_nodes,
        )
        nodes = select_matched_causal_chain_nodes(
            analysis["matched_causal_chains"],
            self.context.knowledge_nodes,
        )
        self.assertTrue(nodes)
        for node in nodes:
            self.assertIs(node["safe_for_examiner"], False)
            self.assertIs(node["examiner_scoring_allowed"], False)

    def test_zero_score_candidates_are_not_selected(self):
        package = {
            "student_query": Q24_TEXT,
            "forced_causal_chains": [
                {
                    "node_id": CANOPY_NODE_ID,
                    "trigger_keywords": [
                        "manejo del dosel",
                        "reducir el vigor",
                    ],
                }
            ],
        }
        self.assertIsNone(_select_best_causal_chain(package))

    def test_q24_self_eval_has_no_unsupported_conclusion(self):
        question = json.loads(
            (PROJECT_ROOT / "tests/fixtures/tutor_snapshots/24/question.json").read_text(
                encoding="utf-8"
            )
        )
        with tempfile.TemporaryDirectory() as tmp:
            result = run_question_attempt(
                question,
                Path(tmp) / "attempts",
                strictness="brutal",
            )
        self.assertNotIn(
            "unsupported_conclusion",
            result["comparison"]["failure_labels"],
        )


if __name__ == "__main__":
    unittest.main()
