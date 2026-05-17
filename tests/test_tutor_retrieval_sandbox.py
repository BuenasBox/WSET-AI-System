import json
import tempfile
import unittest
from pathlib import Path

from tools.retrieval.tutor_retrieval_sandbox import (
    _tokens,
    classify_query,
    load_chunks,
    run_retrieval_sandbox,
    score_chunk_for_query,
)


class TutorRetrievalSandboxTests(unittest.TestCase):
    def test_tokens_preserve_unicode_accents_hyphens_and_apostrophes(self):
        tokens = _tokens(
            "biológica fermentación oxidación acidez azúcar tanino espumoso "
            "cool climate biological ageing bottle-ageing wine's acidity"
        )

        for expected in (
            "biológica",
            "fermentación",
            "oxidación",
            "acidez",
            "azúcar",
            "tanino",
            "espumoso",
            "cool",
            "climate",
            "biological",
            "ageing",
            "bottle-ageing",
            "wine's",
            "acidity",
        ):
            self.assertIn(expected, tokens)

        self.assertNotIn("biol", tokens)
        self.assertNotIn("gica", tokens)
        self.assertNotIn("fermentaci", tokens)
        self.assertNotIn("oxidaci", tokens)
        self.assertNotIn("az", tokens)
        self.assertNotIn("car", tokens)

    def test_query_intent_classification(self):
        self.assertEqual(classify_query("How do I justify quality in SAT?")["query_intent"], "sat_coaching")
        self.assertEqual(
            classify_query("Why do students lose marks in tasting?")["query_intent"],
            "tasting_exam_strategy",
        )
        self.assertEqual(
            classify_query("How should I structure a 10 mark answer?")["query_intent"],
            "answer_structure",
        )
        self.assertEqual(
            classify_query("Why does acidity increase?")["reasoning_intent"],
            "cause_effect",
        )

    def test_golden_chunk_boost_and_explanation(self):
        chunk = _chunk("gold-0001", "In the exam you need to justify quality in SAT and link balance.")
        analysis = classify_query("How do I justify quality in SAT?")
        row = score_chunk_for_query(
            chunk,
            analysis,
            {
                "gold-0001": {
                    "golden_tutor_chunk_candidate": True,
                    "retrieval_priority": "high",
                    "reasoning_type": "sat_logic",
                    "quality_flags": [],
                }
            },
        )

        self.assertGreater(row["scoring_breakdown"]["golden_chunk_boost"], 0)
        self.assertGreater(row["score"], 0.5)
        self.assertIn("golden tutor chunk candidate", row["why_retrieved"])
        self.assertIn("matched SAT/tasting vocabulary", row["why_retrieved"])

    def test_query_expansion_adds_sat_cluster_terms(self):
        analysis = classify_query("How do I justify quality in SAT?")

        self.assertIn("quality assessment", analysis["query_expansion_terms"])
        self.assertIn("balance", analysis["query_expansion_terms"])
        self.assertIn("readiness", analysis["query_expansion_terms"])

    def test_knowledge_graph_boosts_causal_climate_chunk(self):
        knowledge_nodes = [
            {
                "path": "knowledge/knowledge-map/concepts/cool_climate.json",
                "concept_id": "C_COOL_CLIMATE",
                "concept_name": "Cool Climate",
                "definition": "Slow ripening retains malic acid and gives higher acidity.",
            },
            {
                "path": "knowledge/knowledge-map/causal-chains/cc_cool_climate_acidity.json",
                "chain_id": "CC_COOL_CLIMATE_ACIDITY",
                "chain_name": "Cool climate high acidity",
                "intermediate_steps": [
                    {
                        "concept_id": "C_ACIDITY",
                        "description": "Slow ripening means malic acid is retained at higher levels.",
                    }
                ],
                "final_outcome": {"concept_id": "C_ACIDITY", "description": "Higher acidity and freshness."},
            },
        ]
        analysis = classify_query("How does cool climate affect acidity?", knowledge_nodes=knowledge_nodes)
        chunk = {
            **_chunk(
                "climate-0001",
                "Cool climate causes slower ripening, so malic acid is retained and acidity stays high.",
            ),
            "pedagogical_role": "theory_explanation",
            "sat_terms": ["acidity"],
        }

        row = score_chunk_for_query(chunk, analysis, {})

        self.assertIn("slow ripening", analysis["query_expansion_terms"])
        self.assertGreater(row["scoring_breakdown"]["knowledge_graph_match"], 0)
        self.assertGreater(row["scoring_breakdown"]["causal_chain_match"], 0)
        self.assertTrue(row["knowledge_graph_boost_applied"])
        self.assertTrue(any("causal-chain" in reason for reason in row["why_retrieved"]))

    def test_sat_cluster_scoring_boosts_quality_assessment_chunk(self):
        analysis = classify_query("What does balance mean in WSET tasting?")
        chunk = {
            **_chunk(
                "sat-0001",
                "Quality assessment depends on balance, intensity, complexity, length and readiness.",
            ),
            "pedagogical_role": "tasting_practice",
        }

        row = score_chunk_for_query(chunk, analysis, {})

        self.assertGreater(row["scoring_breakdown"]["sat_term_boost"], 0)
        self.assertIn("quality assessment", row["matched_terms"])
        self.assertIn("matched SAT/tasting vocabulary", row["why_retrieved"])

    def test_safe_for_examiner_true_is_excluded(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            chunk_dir = Path(temp_dir) / "chunks"
            chunk_dir.mkdir()
            rows = [
                _chunk("safe-false", "Quality assessment."),
                {**_chunk("safe-true", "Quality assessment."), "safe_for_examiner": True},
            ]
            (chunk_dir / "fixture.chunks.jsonl").write_text(
                "".join(json.dumps(row) + "\n" for row in rows),
                encoding="utf-8",
            )

            chunks, excluded = load_chunks(chunk_dir)

            self.assertEqual([chunk["chunk_id"] for chunk in chunks], ["safe-false"])
            self.assertEqual(excluded, 1)

    def test_run_retrieval_writes_reports_and_stable_top_k(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            chunk_dir = root / "knowledge" / "wine-with-jimmy" / "chunk-ready"
            golden_dir = root / "knowledge" / "wine-with-jimmy" / "manual-import" / "reports"
            dictionary_dir = root / "knowledge" / "enrichment" / "wset_master_dictionary" / "consolidated"
            kg_dir = root / "knowledge" / "knowledge-map" / "concepts"
            chunk_dir.mkdir(parents=True)
            golden_dir.mkdir(parents=True)
            dictionary_dir.mkdir(parents=True)
            kg_dir.mkdir(parents=True)
            chunks = [
                _chunk("b-chunk", "Quality in SAT needs justification and balance."),
                _chunk("a-chunk", "Quality in SAT needs justification and balance."),
            ]
            (chunk_dir / "fixture.chunks.jsonl").write_text(
                "".join(json.dumps(row) + "\n" for row in chunks),
                encoding="utf-8",
            )
            (golden_dir / "golden_tutor_chunk_candidates.jsonl").write_text(
                json.dumps(
                    {
                        "chunk_id": "a-chunk",
                        "golden_tutor_chunk_candidate": True,
                        "retrieval_priority": "high",
                        "reasoning_type": "sat_logic",
                        "quality_flags": [],
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            (dictionary_dir / "canonical_terms_master.jsonl").write_text(
                json.dumps(
                    {
                        "canonical_term": "quality",
                        "category": "sat",
                        "aliases": [],
                        "safe_for_examiner": False,
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            (kg_dir / "quality.json").write_text(json.dumps({"id": "quality"}), encoding="utf-8")

            run = run_retrieval_sandbox(root, "How do I justify quality in SAT?", top_k=2)

            self.assertEqual(run["retrieved_chunks"][0]["chunk_id"], "a-chunk")
            self.assertTrue(run["governance_filter_applied"])
            self.assertTrue((root / "knowledge" / "retrieval-sandbox" / "retrieval_run.json").exists())
            self.assertTrue((root / "knowledge" / "retrieval-sandbox" / "retrieval_run.md").exists())
            self.assertTrue((root / "knowledge" / "retrieval-sandbox" / "retrieval_debug.csv").exists())

    def test_causal_chain_ranking_stability_prefers_mechanism_chunk(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            chunk_dir = root / "knowledge" / "wine-with-jimmy" / "chunk-ready"
            golden_dir = root / "knowledge" / "wine-with-jimmy" / "manual-import" / "reports"
            dictionary_dir = root / "knowledge" / "enrichment" / "wset_master_dictionary" / "consolidated"
            kg_dir = root / "knowledge" / "knowledge-map" / "causal-chains"
            chunk_dir.mkdir(parents=True)
            golden_dir.mkdir(parents=True)
            dictionary_dir.mkdir(parents=True)
            kg_dir.mkdir(parents=True)
            chunks = [
                {
                    **_chunk("generic-0001", "Acidity appears in many tasting notes."),
                    "pedagogical_role": "theory_explanation",
                },
                {
                    **_chunk(
                        "mechanism-0001",
                        "Cool climate slows ripening because low temperatures retain malic acid and increase acidity.",
                    ),
                    "pedagogical_role": "theory_explanation",
                },
            ]
            (chunk_dir / "fixture.chunks.jsonl").write_text(
                "".join(json.dumps(row) + "\n" for row in chunks),
                encoding="utf-8",
            )
            (golden_dir / "golden_tutor_chunk_candidates.jsonl").write_text("", encoding="utf-8")
            (dictionary_dir / "canonical_terms_master.jsonl").write_text("", encoding="utf-8")
            (kg_dir / "cc_cool_climate_acidity.json").write_text(
                json.dumps(
                    {
                        "chain_id": "CC_COOL_CLIMATE_ACIDITY",
                        "chain_name": "Cool climate high acidity",
                        "intermediate_steps": [
                            {"concept_id": "C_COOL_CLIMATE", "description": "Low temperatures slow ripening."},
                            {"concept_id": "C_ACIDITY", "description": "Malic acid is retained at higher levels."},
                        ],
                    }
                ),
                encoding="utf-8",
            )

            run = run_retrieval_sandbox(root, "How does cool climate affect acidity?", top_k=2)

            self.assertEqual(run["retrieved_chunks"][0]["chunk_id"], "mechanism-0001")


def _chunk(chunk_id: str, text: str) -> dict:
    return {
        "chunk_id": chunk_id,
        "source_type": "manual_curated_srt",
        "agent_corpus": "tutor",
        "safe_for_examiner": False,
        "safe_for_tutor": True,
        "academic_level": "WSET_L3",
        "pedagogical_role": "exam_strategy",
        "video_title_guess": "Fixture",
        "source_filename": "fixture.srt",
        "text": text,
        "quality_flags": [],
        "sat_terms": ["quality", "balance"],
        "exam_terms": ["SAT"],
        "topics_detected": ["exam_strategy"],
    }


if __name__ == "__main__":
    unittest.main()
