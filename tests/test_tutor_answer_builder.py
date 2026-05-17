import json
import tempfile
import unittest
from pathlib import Path

from tools.tutor.answer_builder import (
    TUTOR_MARKDOWN_LABELS,
    TUTOR_SOURCE_NOTES,
    _source_note,
    _validate_governance,
    build_tutor_answer,
)


class TutorAnswerBuilderTests(unittest.TestCase):
    def test_tutor_source_note_registry_preserves_exact_notes(self):
        self.assertEqual(
            _source_note(_official_package(language="en"), "en"),
            "Source note: from the WSET framework, treat official context as the reference point; use transcript material only as pedagogical support.",
        )
        self.assertEqual(
            _source_note(_misconception_package(language="en"), "en"),
            "Source note: the misconception node is a cognitive correction object, and Wine With Jimmy/manual transcript material is pedagogical support, not official WSET authority.",
        )
        self.assertEqual(
            _source_note(_normal_package(language="en"), "en"),
            "Source note: Wine With Jimmy/manual transcript material is pedagogical support, not official WSET authority.",
        )
        self.assertEqual(
            _source_note(_official_package(language="es"), "es"),
            "Nota de fuentes: desde el marco WSET, el material oficial es la referencia; el material de transcripción sirve solo como apoyo pedagógico.",
        )
        self.assertEqual(
            _source_note(_misconception_package(language="es"), "es"),
            "Nota de fuentes: el misconception_node es un objeto de corrección cognitiva; el material de Wine With Jimmy o transcripciones manuales es apoyo pedagógico, no autoridad oficial WSET.",
        )
        self.assertEqual(
            _source_note(_normal_package(language="es"), "es"),
            "Nota de fuentes: el material de Wine With Jimmy o transcripciones manuales es apoyo pedagógico, no autoridad oficial WSET.",
        )
        self.assertEqual(
            set(TUTOR_SOURCE_NOTES["en"]),
            {"official_reference", "cognitive_correction", "pedagogical_support"},
        )
        self.assertEqual(set(TUTOR_SOURCE_NOTES["es"]), set(TUTOR_SOURCE_NOTES["en"]))

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = build_tutor_answer(
                _write_package(root / "context.json", _normal_package(language="es")),
                output_path=root / "latest.md",
            )

        self.assertFalse(result["governance"]["safe_for_examiner"])

    def test_tutor_markdown_heading_registry_preserves_rendered_structure(self):
        expected_keys = {
            "title",
            "normal_direct",
            "normal_framing",
            "cause_effect",
            "normal_exam",
            "mini_practice",
            "misconception_direct",
            "misconception_confusion",
            "misconception_framing",
            "misconception_cause_effect",
            "misconception_exam",
        }
        self.assertEqual(set(TUTOR_MARKDOWN_LABELS["en"]), expected_keys)
        self.assertEqual(set(TUTOR_MARKDOWN_LABELS["es"]), expected_keys)

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            normal_es = build_tutor_answer(
                _write_package(root / "normal_es.json", _normal_package(language="es")),
                output_path=root / "normal_es.md",
            )
            normal_en = build_tutor_answer(
                _write_package(root / "normal_en.json", _normal_package(language="en")),
                output_path=root / "normal_en.md",
            )
            misconception_es = build_tutor_answer(
                _write_package(root / "misconception_es.json", _misconception_package(language="es")),
                output_path=root / "misconception_es.md",
            )
            misconception_en = build_tutor_answer(
                _write_package(root / "misconception_en.json", _misconception_package(language="en")),
                output_path=root / "misconception_en.md",
            )

            normal_es_answer = Path(normal_es["output_paths"]["latest"]).read_text(encoding="utf-8")
            normal_en_answer = Path(normal_en["output_paths"]["latest"]).read_text(encoding="utf-8")
            misconception_es_answer = Path(misconception_es["output_paths"]["latest"]).read_text(encoding="utf-8")
            misconception_en_answer = Path(misconception_en["output_paths"]["latest"]).read_text(encoding="utf-8")

        self.assertEqual(
            _headings(normal_es_answer),
            [
                "# Borrador del Tutor: ¿Cómo justifico la quality assessment en SAT?",
                "## 1. Respuesta directa",
                "## 2. Marco WSET",
                "## 3. Explicación causa → efecto",
                "## 4. Formulación de examen",
                "## 5. Mini práctica",
            ],
        )
        self.assertEqual(
            _headings(normal_en_answer),
            [
                "# Tutor Draft: How do I justify quality in SAT?",
                "## 1. Short Direct Answer",
                "## 2. WSET Framing",
                "## 3. Cause/Effect Explanation",
                "## 4. Exam Formulation",
                "## 5. Mini Practice",
            ],
        )
        self.assertEqual(
            _headings(misconception_es_answer),
            [
                "# Borrador del Tutor: ¿High acidity significa menor calidad?",
                "## 1. Corrección directa",
                "## 2. Por qué esa idea confunde",
                "## 3. Marco WSET correcto",
                "## 4. Cadena causa → efecto",
                "## 5. Cómo escribirlo para puntos",
                "## 6. Mini práctica",
            ],
        )
        self.assertEqual(
            _headings(misconception_en_answer),
            [
                "# Tutor Draft: So high acidity means the wine is lower quality?",
                "## 1. Direct Correction",
                "## 2. Why The Misconception Is Tempting",
                "## 3. Correct WSET Framing",
                "## 4. Cause/Effect Explanation",
                "## 5. How To Write It For Marks",
                "## 6. Mini Practice",
            ],
        )
        for result in (normal_es, normal_en, misconception_es, misconception_en):
            self.assertFalse(result["governance"]["safe_for_examiner"])

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


def _headings(answer: str) -> list[str]:
    return [line for line in answer.splitlines() if line.startswith("#")]


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


def _official_package(language: str) -> dict:
    package = _normal_package(language)
    package["retrieved_context"][0]["source_type"] = "official_wset_extracted"
    package["retrieved_context"][0]["source_filename"] = "official_wset_chunks.jsonl"
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
