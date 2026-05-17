import json
import tempfile
import unittest
from pathlib import Path

from tools.self_eval.answer_comparator import COGNITIVE_ERROR_LABELS, COGNITIVE_ERROR_LABEL_METADATA, compare_answer
from tools.self_eval.evaluation_reporter import write_evaluation_reports
from tools.self_eval.question_runner import load_questions, run_question_attempt, run_self_eval


class SelfEvalLoopTests(unittest.TestCase):
    def test_cognitive_error_label_metadata_preserves_internal_labels(self):
        expected_labels = (
            "missing_causal_link",
            "vague_claim",
            "unsupported_conclusion",
            "missing_exam_language",
            "incomplete_balance_justification",
            "weak_sat_commitment",
            "misconception_unresolved",
            "missing_counterexample",
            "retrieval_gap",
            "weak_context_support",
            "shallow_retrieval",
            "shallow_reasoning",
            "misconception_reinforcement_risk",
            "weak_exam_register",
        )

        self.assertEqual(COGNITIVE_ERROR_LABELS, expected_labels)
        self.assertEqual(len(COGNITIVE_ERROR_LABELS), len(set(COGNITIVE_ERROR_LABELS)))
        self.assertEqual(set(COGNITIVE_ERROR_LABEL_METADATA), set(COGNITIVE_ERROR_LABELS))
        for label in COGNITIVE_ERROR_LABELS:
            metadata = COGNITIVE_ERROR_LABEL_METADATA[label]
            self.assertEqual(metadata["label"], label)
            self.assertTrue(metadata["label_es"])
            self.assertTrue(metadata["description_es"])
            self.assertIn(metadata["severity_hint"], {"low", "medium", "high"})
            self.assertIsInstance(metadata["learner_facing"], bool)

    def test_question_loading(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            structured = root / "structured"
            structured.mkdir()
            (structured / "questions.json").write_text(
                json.dumps(
                    [
                        {
                            "question_id": "Q1",
                            "question_text": "How does cool climate affect acidity?",
                            "question_type": "theory",
                            "expected_keywords": ["acidity"],
                        }
                    ]
                ),
                encoding="utf-8",
            )

            questions = load_questions(question_bank_root=root, limit=10)

        self.assertEqual(len(questions), 1)
        self.assertEqual(questions[0]["question_id"], "Q1")
        self.assertFalse(questions[0]["safe_for_examiner"])

    def test_tutor_attempt_generation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            question = _question()
            result = run_question_attempt(question, root / "attempts")

            attempt_path = Path(result["tutor_attempt_path"])
            context_path = Path(result["tutor_context_package_path"])
            self.assertTrue(attempt_path.exists())
            self.assertTrue(context_path.exists())
            self.assertFalse(result["safe_for_examiner"])

    def test_deterministic_comparator(self):
        question = _question()
        answer = (
            "Desde el marco WSET, un clima fresco ralentiza la maduración, "
            "retiene acidity y aporta frescura."
        )
        comparison = compare_answer(question, answer, {"retrieved_context": [{}]}, strictness="normal")

        self.assertIn("acidity", comparison["present_keywords"])
        self.assertIn("clima fresco", comparison["present_keywords"])

    def test_failure_label_generation(self):
        question = _question()
        comparison = compare_answer(question, "Respuesta vaga sin mecanismo.", {"retrieved_context": []}, strictness="hard")

        self.assertIn("missing_causal_link", comparison["failure_labels"])
        self.assertIn("retrieval_gap", comparison["failure_labels"])

    def test_report_generation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            results = [
                {
                    "question_id": "Q1",
                    "question_type": "theory",
                    "question_text": "How does cool climate affect acidity?",
                    "comparison": {
                        "failure_labels": ["missing_causal_link"],
                        "strengths": [],
                        "missing_keywords": ["acidity"],
                        "missing_causal_links": ["cool climate -> acid retention"],
                        "retrieval_weaknesses": ["missing_causal_link_support"],
                    },
                }
            ]
            paths = write_evaluation_reports(results, output_dir=root / "self-eval", feedback_path=root / "feedback.json")

            self.assertTrue(Path(paths["summary"]).exists())
            self.assertTrue(Path(paths["csv"]).exists())
            self.assertTrue(Path(paths["jsonl"]).exists())
            self.assertTrue(Path(paths["feedback"]).exists())

    def test_governance_enforcement(self):
        question = _question()
        question["safe_for_examiner"] = "violation"

        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                run_question_attempt(question, Path(tmp) / "attempts")

    def test_safe_for_examiner_remains_false(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = run_self_eval(limit=1, output_dir=Path(tmp) / "self-eval")

        self.assertFalse(result["governance"]["safe_for_examiner"])
        self.assertFalse(result["results"][0]["safe_for_examiner"])

    def test_shallow_reasoning_detection(self):
        question = _question()
        comparison = compare_answer(question, "La acidity es importante.", {"retrieved_context": [{}]}, strictness="hard")

        self.assertIn("shallow_reasoning", comparison["failure_labels"])

    def test_missing_causal_link_detection(self):
        question = _question()
        comparison = compare_answer(
            question,
            "Un clima fresco tiene acidity.",
            {"retrieved_context": [{"context_type": "retrieval_sandbox_chunk"}]},
            strictness="brutal",
        )

        self.assertIn("missing_causal_link", comparison["failure_labels"])

    def test_sat_weakness_detection(self):
        question = {
            **_question(),
            "question_type": "sat",
            "question_text": "How do I justify quality in SAT?",
            "expected_keywords": ["balance", "intensity", "complexity", "length"],
            "expected_causal_links": ["evidence -> conclusion"],
        }
        comparison = compare_answer(
            question,
            "The wine has fruit and acidity.",
            {"retrieved_context": [{"context_type": "retrieval_sandbox_chunk"}]},
            strictness="hard",
        )

        self.assertIn("incomplete_balance_justification", comparison["failure_labels"])
        self.assertIn("weak_sat_commitment", comparison["failure_labels"])

    def test_misconception_unresolved_detection(self):
        question = {
            **_question(),
            "expected_keywords": ["misconception", "tannin"],
            "question_text": "Does more tannin mean better wine?",
        }
        package = {
            "matched_misconception": {"misconception": "More tannin means better wine."},
            "retrieved_context": [{"context_type": "misconception_node"}],
        }
        comparison = compare_answer(question, "More tannin means better wine.", package, strictness="hard")

        self.assertIn("misconception_unresolved", comparison["failure_labels"])
        self.assertIn("misconception_reinforcement_risk", comparison["failure_labels"])

    def test_retrieval_gap_detection(self):
        question = _question()
        package = {
            "retrieved_context": [
                {
                    "context_type": "retrieval_sandbox_chunk",
                    "source_filename": "manual.srt",
                    "why_retrieved": [],
                }
            ]
        }
        comparison = compare_answer(question, "Porque hay maduración.", package, strictness="brutal")

        self.assertIn("retrieval_gap", comparison["failure_labels"])
        self.assertIn("weak_context_support", comparison["failure_labels"])
        self.assertIn("shallow_retrieval", comparison["failure_labels"])

    def test_fragile_concept_accumulation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            results = [
                {
                    "question_id": "Q1",
                    "question_type": "theory",
                    "difficulty": "distinction",
                    "comparison": {
                        "failure_labels": ["missing_causal_link"],
                        "missing_causal_links": ["flor -> oxygen protection -> biological ageing"],
                        "likely_misconception_gaps": [],
                        "retrieval_weaknesses": ["weak_context_support"],
                    },
                }
            ]
            paths = write_evaluation_reports(results, output_dir=root / "self-eval", feedback_path=root / "feedback.json", strictness="brutal")
            feedback = json.loads(Path(paths["feedback"]).read_text(encoding="utf-8"))

        self.assertEqual(feedback["strictness"], "brutal")
        self.assertTrue(feedback["fragile_concepts"])
        self.assertTrue(feedback["orchestrator_recommendations"])

    def test_strictness_mode_behavior(self):
        question = _question()
        answer = "Un clima fresco porque retiene acidity."
        package = {"retrieved_context": [{"context_type": "retrieval_sandbox_chunk"}]}

        normal = compare_answer(question, answer, package, strictness="normal")
        brutal = compare_answer(question, answer, package, strictness="brutal")

        self.assertLessEqual(len(normal["failure_labels"]), len(brutal["failure_labels"]))


def _question() -> dict:
    return {
        "question_id": "TEST_CLIMATE_01",
        "question_text": "How does cool climate affect acidity?",
        "question_type": "theory",
        "expected_topics": ["cool climate", "acidity"],
        "expected_causal_links": ["clima fresco -> maduración -> acidity"],
        "expected_keywords": ["clima fresco", "maduración", "acidity"],
        "expected_reasoning_type": "cause_effect",
        "source_type": "test",
        "safe_for_examiner": False,
    }


if __name__ == "__main__":
    unittest.main()
