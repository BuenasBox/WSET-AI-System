import json
import tempfile
import unittest
from pathlib import Path

from tools.tutor.answer_builder import build_tutor_answer, _validate_governance


class TutorAnswerBuilderTests(unittest.TestCase):
    def test_tutor_answer_created_from_misconception_package(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            package_path = _write_package(root / "context.json", _misconception_package(language="es"))
            result = build_tutor_answer(package_path, output_path=root / "latest.md")
            answer = Path(result["output_paths"]["latest"]).read_text(encoding="utf-8")

        self.assertIn("Corrección directa", answer)
        self.assertIn("Marco WSET correcto", answer)
        self.assertIn("high acidity", answer)
        self.assertEqual(result["pedagogical_act"], "misconception_intervention")

    def test_tutor_answer_created_from_normal_package(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            package_path = _write_package(root / "context.json", _normal_package(language="es"))
            result = build_tutor_answer(package_path, output_path=root / "latest.md")
            answer = Path(result["output_paths"]["latest"]).read_text(encoding="utf-8")

        self.assertIn("Respuesta directa", answer)
        self.assertIn("Formulación de examen", answer)
        self.assertEqual(result["pedagogical_act"], "answer_normally")

    def test_spanish_answer_contains_spanish_framing(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            package_path = _write_package(root / "context.json", _normal_package(language="es"))
            result = build_tutor_answer(package_path, output_path=root / "latest.md")
            answer = Path(result["output_paths"]["latest"]).read_text(encoding="utf-8")

        self.assertIn("Como apoyo pedagógico", answer)
        self.assertTrue(
            any(
                phrase in answer
                for phrase in (
                    "Para efectos del examen",
                    "En el examen",
                    "Desde el marco WSET",
                    "Formulación para el examen",
                    "Formulación de examen",
                )
            )
        )
        self.assertIn("Nota: esta es una respuesta del Tutor", answer)

    def test_english_answer_works(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            package_path = _write_package(root / "context.json", _normal_package(language="en"))
            result = build_tutor_answer(package_path, output_path=root / "latest.md")
            answer = Path(result["output_paths"]["latest"]).read_text(encoding="utf-8")

        self.assertIn("Short Direct Answer", answer)
        self.assertTrue(
            any(
                phrase in answer
                for phrase in (
                    "For exam purposes",
                    "In the exam",
                    "From the WSET perspective",
                    "Exam formulation",
                    "Exam Formulation",
                )
            )
        )
        self.assertIn("Note: this is a Tutor response", answer)

    def test_safe_for_examiner_violation_causes_safe_failure(self):
        package = _normal_package(language="es")
        package["governance"]["safe_for_examiner"] = "violation"

        with self.assertRaises(ValueError):
            _validate_governance(package)

    def test_answer_includes_tutor_disclaimer(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            package_path = _write_package(root / "context.json", _misconception_package(language="es"))
            result = build_tutor_answer(package_path, output_path=root / "latest.md")
            answer = Path(result["output_paths"]["latest"]).read_text(encoding="utf-8")

        self.assertIn("no una calificación oficial", answer)
        self.assertIn("evaluación del Examiner", answer)

    def test_no_api_or_llm_calls(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            package_path = _write_package(root / "context.json", _normal_package(language="es"))
            result = build_tutor_answer(package_path, output_path=root / "latest.md")

        self.assertFalse(result["governance"]["uses_llm"])
        self.assertFalse(result["governance"]["uses_api"])
        self.assertFalse(result["governance"]["uses_embeddings"])
        self.assertFalse(result["governance"]["uses_vector_db"])

    def test_output_file_written_locally(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            package_path = _write_package(root / "context.json", _normal_package(language="es"))
            result = build_tutor_answer(package_path, output_path=root / "latest.md")

            latest = Path(result["output_paths"]["latest"])
            timestamped = Path(result["output_paths"]["timestamped"])
            self.assertTrue(latest.exists())
            self.assertTrue(timestamped.exists())
            self.assertTrue(str(latest).startswith(str(root)))

    def test_natural_spanish_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            package = _misconception_package(language="es")
            package["student_query"] = "Does more tannin mean better wine?"
            package["matched_misconception"] = {
                "misconception_id": "MC_TANNIN_01",
                "misconception": "Tannin is the same as bitterness.",
                "corrected_understanding": "Tannin produces astringency, not bitterness.",
                "why_incorrect": "Tannin produces a tactile, drying sensation.",
            }
            package["retrieved_context"][0]["node_id"] = "MC_TANNIN_01"
            package["retrieved_context"][0]["content"] = package["matched_misconception"]
            package_path = _write_package(root / "context.json", package)
            result = build_tutor_answer(package_path, output_path=root / "latest.md")
            answer = Path(result["output_paths"]["latest"]).read_text(encoding="utf-8")

        self.assertIn("Más tanino", answer)
        self.assertIn("mejor vino", answer)
        self.assertNotIn("Mas tannin", answer)
        self.assertNotIn("better wine", answer)

    def test_no_placeholder_text_remains(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            package_path = _write_package(root / "context.json", _misconception_package(language="es"))
            result = build_tutor_answer(package_path, output_path=root / "latest.md")
            answer = Path(result["output_paths"]["latest"]).read_text(encoding="utf-8")

        self.assertNotIn("usa el contexto recuperado", answer)
        self.assertNotIn("Use the retrieved pedagogical context", answer)

    def test_retrieved_context_is_used(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            package_path = _write_package(root / "context.json", _normal_package(language="es"))
            result = build_tutor_answer(package_path, output_path=root / "latest.md")
            answer = Path(result["output_paths"]["latest"]).read_text(encoding="utf-8")

        self.assertIn("Ideas usadas del contexto", answer)
        self.assertIn("SAT", answer)

    def test_misconception_answer_includes_cause_effect_section(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            package_path = _write_package(root / "context.json", _misconception_package(language="es"))
            result = build_tutor_answer(package_path, output_path=root / "latest.md")
            answer = Path(result["output_paths"]["latest"]).read_text(encoding="utf-8")

        self.assertIn("Cadena causa → efecto", answer)

    def test_source_distinction_appears(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            package_path = _write_package(root / "context.json", _misconception_package(language="es"))
            result = build_tutor_answer(package_path, output_path=root / "latest.md")
            answer = Path(result["output_paths"]["latest"]).read_text(encoding="utf-8")

        self.assertIn("apoyo pedagógico", answer)
        self.assertIn("no autoridad oficial WSET", answer)


def _write_package(path: Path, package: dict) -> Path:
    path.write_text(json.dumps(package), encoding="utf-8")
    return path


def _base_package(language: str) -> dict:
    return {
        "student_query": "How do I justify quality in SAT?",
        "language": language,
        "orchestrator_decision": {"route": "normal_tutor"},
        "learner_state_context": {"learner_id": "nazareth"},
        "retrieval_plan": {
            "uses_llm": False,
            "uses_api": False,
            "uses_embeddings": False,
            "uses_vector_db": False,
        },
        "retrieved_context": [
            {
                "context_type": "retrieval_sandbox_chunk",
                "chunk_id": "chunk-1",
                "source_type": "manual_curated_srt",
                "reasoning_type": "exam_strategy",
                "why_retrieved": ["contains exam or marks strategy language"],
                "text_excerpt": "Students lose marks when they do not put down the SAT elements and link evidence to the quality conclusion.",
                "safe_for_examiner": False,
            }
        ],
        "tutor_directive": {"safe_for_examiner": False},
        "success_criteria": [],
        "governance": {
            "agent_corpus": "tutor",
            "safe_for_examiner": False,
            "examiner_scoring_allowed": False,
        },
    }


def _normal_package(language: str) -> dict:
    package = _base_package(language)
    package["pedagogical_act"] = "answer_normally"
    return package


def _misconception_package(language: str) -> dict:
    package = _base_package(language)
    package.update(
        {
            "student_query": "So high acidity means the wine is lower quality?",
            "pedagogical_act": "misconception_intervention",
            "forced_retrieval_nodes": ["MC_ACIDITY_01"],
            "matched_misconception": {
                "misconception_id": "MC_ACIDITY_01",
                "misconception": "High acidity in a wine means the wine is low quality or unpleasant.",
                "corrected_understanding": "High acidity can be a hallmark of quality when balanced.",
            },
        }
    )
    package["retrieved_context"].insert(
        0,
        {
            "context_type": "misconception_node",
            "node_id": "MC_ACIDITY_01",
                "forced_retrieval": bool("forced"),
                "safe_for_examiner": False,
                "content": package["matched_misconception"],
            },
    )
    return package


if __name__ == "__main__":
    unittest.main()
