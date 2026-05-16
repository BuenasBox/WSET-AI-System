import json
import tempfile
import unittest
from pathlib import Path

from tools.orchestrator.orchestrator import run_orchestrator
from tools.retrieval.official_wset_chunks import build_official_wset_chunks, load_official_markdown_chunks
from tools.retrieval.tutor_retrieval_sandbox import run_retrieval_sandbox
from tools.self_eval.answer_comparator import compare_answer
from tools.tutor.answer_builder import build_tutor_answer


class OfficialCorpusRetrievalTests(unittest.TestCase):
    def test_official_markdown_loading(self):
        with tempfile.TemporaryDirectory() as tmp:
            md_dir = _write_official_markdown(Path(tmp))
            chunks = load_official_markdown_chunks(md_dir)

        self.assertTrue(chunks)
        self.assertEqual(chunks[0]["source_type"], "official_wset_extracted")
        self.assertEqual(chunks[0]["agent_corpus"], "tutor")

    def test_official_chunk_creation_and_metadata(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            md_dir = _write_official_markdown(root / "md")
            result = build_official_wset_chunks(md_dir, root / "official-chunks")
            row = json.loads(Path(result["jsonl_path"]).read_text(encoding="utf-8").splitlines()[0])
            self.assertTrue(Path(result["report_path"]).exists())

        self.assertFalse(row["safe_for_examiner"])
        self.assertFalse(row["official_grading_authority"])
        self.assertTrue(row["requires_human_review"])
        self.assertEqual(row["source_trust_tier"], 1)

    def test_retrieval_includes_official_chunks_when_relevant(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = _retrieval_root(Path(tmp))
            run = run_retrieval_sandbox(root, "How does cool climate affect acidity?", top_k=3)

        self.assertTrue(any(chunk["source_type"] == "official_wset_extracted" for chunk in run["retrieved_chunks"]))

    def test_official_first_ranking_when_relevant(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = _retrieval_root(Path(tmp))
            run = run_retrieval_sandbox(root, "How does cool climate affect acidity?", top_k=3)

        self.assertEqual(run["retrieved_chunks"][0]["source_type"], "official_wset_extracted")

    def test_source_diversity(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = _retrieval_root(Path(tmp))
            run = run_retrieval_sandbox(root, "How does cool climate affect acidity?", top_k=3)
            types = {chunk["source_type"] for chunk in run["retrieved_chunks"]}

        self.assertIn("official_wset_extracted", types)
        self.assertIn("manual_curated_srt", types)

    def test_context_package_includes_official_chunks(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = _retrieval_root(Path(tmp))
            result = run_orchestrator(
                "How does cool climate affect acidity?",
                top_k=3,
                root=root,
                context_package_dir=root / "context-packages",
                staging_path=root / "session_staging.json",
                les_path=_write_les(root / "epistemic_state.json"),
                misconception_dir=_write_misconceptions(root / "misconceptions"),
            )

        contexts = result["context_package"]["retrieved_context"]
        self.assertTrue(any(item.get("source_type") == "official_wset_extracted" for item in contexts))
        self.assertFalse(result["context_package"]["governance"]["safe_for_examiner"])

    def test_tutor_answer_distinguishes_official_and_pedagogical_sources(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = _retrieval_root(Path(tmp))
            result = run_orchestrator(
                "How does cool climate affect acidity?",
                top_k=3,
                root=root,
                context_package_dir=root / "context-packages",
                staging_path=root / "session_staging.json",
                les_path=_write_les(root / "epistemic_state.json"),
                misconception_dir=_write_misconceptions(root / "misconceptions"),
            )
            answer = build_tutor_answer(
                Path(result["context_package_paths"]["latest"]),
                output_path=root / "answer.md",
            )["answer"]

        self.assertIn("Desde el marco WSET", answer)
        self.assertIn("apoyo pedagógico", answer)

    def test_self_eval_retrieval_gap_drops_when_official_support_exists(self):
        package = {
            "retrieved_context": [
                {
                    "context_type": "retrieval_sandbox_chunk",
                    "source_type": "official_wset_extracted",
                    "safe_for_examiner": False,
                    "why_retrieved": ["official WSET extracted Tutor support"],
                },
                {"context_type": "retrieval_sandbox_chunk", "source_type": "manual_curated_srt"},
            ]
        }
        question = {
            "question_id": "Q",
            "question_type": "theory",
            "question_text": "How does cool climate affect acidity?",
            "expected_keywords": ["clima fresco", "maduración", "acidity"],
            "expected_causal_links": ["clima fresco -> maduración -> acidity"],
        }
        answer = "Porque el clima fresco ralentiza la maduración, por tanto retiene acidity y da frescura."
        comparison = compare_answer(question, answer, package, strictness="brutal")

        self.assertNotIn("retrieval_gap", comparison["failure_labels"])


def _write_official_markdown(root: Path) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    words = (
        "Cool climate growing environment slows ripening and helps grapes retain acidity. "
        "This causes wines to show freshness, higher acidity, balance, intensity, complexity, length, "
        "and supports quality assessment in the SAT. "
    )
    body = words * 35
    (root / "cool_climate.md").write_text(
        "---\n"
        "title: Cool Climate and Acidity\n"
        "section: Factors Affecting Style Quality and Price\n"
        "subtopic: Growing Environment\n"
        "parent_section: Section 2\n"
        "source: official markdown fixture\n"
        "---\n"
        "# Cool Climate and Acidity\n\n"
        + body,
        encoding="utf-8",
    )
    return root


def _retrieval_root(root: Path) -> Path:
    official_dir = root / "knowledge" / "official-wset" / "study-guide" / "official-chunks"
    official_dir.mkdir(parents=True, exist_ok=True)
    official_chunk = {
        "chunk_id": "OFFICIAL_WSET_COOL_CLIMATE_001",
        "text": "Cool climate slows ripening and helps retain acidity. This causes freshness and supports balance, intensity, complexity, length and quality assessment.",
        "source_type": "official_wset_extracted",
        "source_trust_tier": 1,
        "agent_corpus": "tutor",
        "safe_for_tutor": True,
        "safe_for_examiner": False,
        "official_grading_authority": False,
        "requires_human_review": True,
        "source_file": "official.md",
        "source_filename": "official.md",
        "section": "Growing Environment",
        "subtopic": "Cool Climate",
        "title": "Cool Climate and Acidity",
        "pedagogical_role": "official_reference",
        "retrieval_priority": "high",
    }
    (official_dir / "official_wset_chunks.jsonl").write_text(json.dumps(official_chunk) + "\n", encoding="utf-8")
    chunk_dir = root / "knowledge" / "wine-with-jimmy" / "chunk-ready"
    chunk_dir.mkdir(parents=True, exist_ok=True)
    tutor_chunk = {
        "chunk_id": "TUTOR_COOL_001",
        "text": "Cool climate can make wines fresh because slower ripening preserves acid.",
        "source_type": "manual_curated_srt",
        "agent_corpus": "tutor",
        "safe_for_examiner": False,
        "pedagogical_role": "theory_explanation",
        "source_filename": "cool.srt",
    }
    (chunk_dir / "fixture.chunks.jsonl").write_text(json.dumps(tutor_chunk) + "\n", encoding="utf-8")
    return root


def _write_les(path: Path) -> Path:
    path.write_text(
        json.dumps(
            {
                "learner_id": "nazareth",
                "current_level": "WSET_L3",
                "governance": {"safe_for_examiner": False},
            }
        ),
        encoding="utf-8",
    )
    return path


def _write_misconceptions(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


if __name__ == "__main__":
    unittest.main()
