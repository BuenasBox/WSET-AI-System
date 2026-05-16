import json
import tempfile
import unittest
from pathlib import Path

from tools.self_eval.evaluation_reporter import write_evaluation_reports
from tools.tutor.answer_builder import (
    _compress_explanation,
    _render_causal_chain,
    _select_explanation_depth,
    build_tutor_answer,
)
from tools.tutor.explanation_priority import (
    build_explanation_priority,
    calculate_tutor_evaluation_signals,
)


class ExplanationPriorityEngineTests(unittest.TestCase):
    def test_ranking_prioritizes_high_severity_misconception(self):
        package = _package()
        plan = build_explanation_priority(package, confidence=0.9)

        self.assertEqual(plan["recommended_sequence"][0], "MC_TANNIN_QUALITY_02")
        self.assertEqual(plan["prioritized_explanations"][0]["type"], "misconception")
        self.assertGreaterEqual(plan["priority_score"], 0.5)
        self.assertFalse(plan["governance"]["safe_for_examiner"])

    def test_low_confidence_selects_deep_explanation(self):
        package = _package()
        package["orchestrator_decision"]["confidence"] = 0.4

        depth = _select_explanation_depth(package, "standard", build_explanation_priority(package))

        self.assertEqual(depth, "deep")

    def test_high_cognitive_load_limits_depth_to_standard(self):
        package = _package()
        package["forced_causal_chains"][0]["steps"].extend(
            [{"step": index, "label": "mechanism", "text": f"extra mechanism {index}"} for index in range(5, 10)]
        )
        package["learner_state_context"]["known_weak_areas"] = [f"weakness-{index}" for index in range(6)]

        plan = build_explanation_priority(package)
        depth = _select_explanation_depth(package, "standard", plan)

        self.assertEqual(plan["cognitive_load_estimate"], "high")
        self.assertEqual(depth, "standard")

    def test_compression_preserves_causal_statement(self):
        text = (
            "Este detalle repite contexto. "
            "Porque el tanino domina, el balance se reduce. "
            "Por eso la conclusión debe explicar el efecto."
        )

        compressed = _compress_explanation(text, "minimal")

        self.assertIn("Porque", compressed)
        self.assertIn("Por eso", compressed)
        self.assertNotIn("repite contexto", compressed)

    def test_causal_chain_rendering_can_limit_steps_without_losing_core(self):
        chain = _causal_chain()
        chain["steps"].append({"step": 5, "label": "extra", "text": "Extra detail."})

        rendered = _render_causal_chain(chain, "es", max_steps=3)

        self.assertIn("CAUSA", rendered)
        self.assertIn("MECANISMO", rendered)
        self.assertIn("EFECTO", rendered)
        self.assertNotIn("FORMULACIÓN DE EXAMEN", rendered)


class AdaptiveTutorBuilderTests(unittest.TestCase):
    def test_tutor_answer_keeps_forced_causal_chain_content(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            package_path = root / "context.json"
            package_path.write_text(json.dumps(_package()), encoding="utf-8")

            result = build_tutor_answer(package_path, output_path=root / "answer.md")
            answer = Path(result["output_paths"]["latest"]).read_text(encoding="utf-8")

        self.assertIn("Phenolic extraction increases tannin.", answer)
        self.assertIn("Tanino alto debe evaluarse con balance", answer)
        self.assertNotIn("safe_for_examiner=true", answer)

    def test_tutor_evaluation_signals_are_written_by_reporter(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            answer_path = root / "attempt.md"
            package_path = root / "context.json"
            answer_path.write_text(
                "## 1. Respuesta\nPorque hay causa, mecanismo y efecto, therefore the answer has reasoning.",
                encoding="utf-8",
            )
            package_path.write_text(json.dumps(_package()), encoding="utf-8")
            results = [
                {
                    "question_id": "Q1",
                    "question_type": "theory",
                    "question_text": "Does more tannin mean better wine?",
                    "tutor_attempt_path": answer_path.as_posix(),
                    "tutor_context_package_path": package_path.as_posix(),
                    "comparison": {"failure_labels": [], "strengths": ["causal_links_present"]},
                    "safe_for_examiner": False,
                }
            ]

            paths = write_evaluation_reports(
                results,
                output_dir=root / "self-eval",
                feedback_path=root / "feedback.json",
                reconcile_les=False,
            )
            jsonl = Path(paths["jsonl"]).read_text(encoding="utf-8")
            csv_text = Path(paths["csv"]).read_text(encoding="utf-8")
            summary = Path(paths["summary"]).read_text(encoding="utf-8")

        self.assertIn("tutor_evaluation_signals", jsonl)
        self.assertIn("explanation_density", csv_text)
        self.assertIn("Tutor evaluation signals", summary)

    def test_evaluation_signals_are_deterministic_and_non_examiner(self):
        signals = calculate_tutor_evaluation_signals(
            "CAUSA: tannin. MECANISMO: extraction. EFECTO: astringency.",
            _package(),
        )

        self.assertGreater(signals["causal_coherence"], 0)
        self.assertFalse(signals["safe_for_examiner"])
        self.assertFalse(signals["examiner_scoring_allowed"])


def _package() -> dict:
    return {
        "student_query": "Does more tannin mean better wine?",
        "language": "es",
        "orchestrator_decision": {"route": "misconception_prepass", "confidence": 0.8},
        "pedagogical_act": "misconception_intervention",
        "matched_misconception": {
            "misconception_id": "MC_TANNIN_QUALITY_02",
            "severity": "high",
            "corrected_understanding": "More tannin does not automatically mean higher quality.",
        },
        "learner_state_context": {
            "learner_id": "nazareth",
            "known_weak_areas": ["causal_chain:tannin -> astringency -> balance"],
        },
        "retrieved_context": [
            {
                "context_type": "misconception_node",
                "node_id": "MC_TANNIN_QUALITY_02",
                "forced_retrieval": True,
                "content": {
                    "corrected_understanding": "More tannin does not automatically mean higher quality.",
                },
                "safe_for_examiner": False,
            }
        ],
        "forced_causal_chains": [_causal_chain()],
        "tutor_directive": {"safe_for_examiner": False},
        "governance": {"safe_for_examiner": False, "examiner_scoring_allowed": False},
    }


def _causal_chain() -> dict:
    return {
        "node_id": "CC_TANNIN_ASTRINGENCY",
        "node_type": "causal_chain",
        "safe_for_examiner": False,
        "sat_relevance": "Tanino alto debe evaluarse con balance, integration y length.",
        "trigger_keywords": ["tannin", "tanino", "quality"],
        "steps": [
            {"step": 1, "label": "cause", "text": "Phenolic extraction increases tannin."},
            {"step": 2, "label": "mechanism", "text": "Tannin creates a drying tactile sensation."},
            {"step": 3, "label": "effect", "text": "Quality depends on balance and integration."},
            {"step": 4, "label": "exam_formulation", "text": "Link tannin to balance, complexity and length."},
        ],
    }


if __name__ == "__main__":
    unittest.main()
