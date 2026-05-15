import json
import tempfile
import unittest
from pathlib import Path

from tools.orchestrator.learner_state import (
    build_les_context,
    load_learner_state,
    write_session_staging,
)
from tools.orchestrator.misconception_prepass import detect_misconception
from tools.orchestrator.orchestrator import run_orchestrator


class MinimalBrainOrchestratorTests(unittest.TestCase):
    def test_les_loading(self):
        with tempfile.TemporaryDirectory() as tmp:
            les_path = Path(tmp) / "epistemic_state.json"
            les_path.write_text(
                json.dumps(
                    {
                        "learner_id": "nazareth",
                        "current_level": "WSET_L3",
                        "known_weak_areas": ["acidity"],
                        "recent_misconceptions": ["MC_ACIDITY_01"],
                        "session_count": 2,
                        "governance": {"safe_for_examiner": False},
                    }
                ),
                encoding="utf-8",
            )

            state = load_learner_state(les_path)
            context = build_les_context(state)

        self.assertEqual(context["learner_id"], "nazareth")
        self.assertEqual(context["known_weak_areas"], ["acidity"])
        self.assertFalse(context["governance"]["safe_for_examiner"])

    def test_misconception_detection(self):
        with tempfile.TemporaryDirectory() as tmp:
            misconception_dir = _write_misconception_fixture(Path(tmp))
            result = detect_misconception(
                "So high acidity means the wine is lower quality?",
                misconception_dir,
            )

        self.assertTrue(result["detected"])
        self.assertEqual(result["matched_misconception_id"], "MC_ACIDITY_01")
        self.assertEqual(result["severity"], "medium")
        self.assertEqual(result["intervention_type"], "contrast_comparison")

    def test_no_detection_case(self):
        with tempfile.TemporaryDirectory() as tmp:
            misconception_dir = _write_misconception_fixture(Path(tmp))
            result = detect_misconception("How do I justify quality in SAT?", misconception_dir)

        self.assertFalse(result["detected"])
        self.assertIsNone(result["matched_misconception_id"])

    def test_orchestrator_misconception_decision(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            misconception_dir = _write_misconception_fixture(root / "misconceptions")
            les_path = _write_les(root / "epistemic_state.json")
            staging_path = root / "session_staging.json"

            result = run_orchestrator(
                "So high acidity means the wine is lower quality?",
                les_path=les_path,
                misconception_dir=misconception_dir,
                staging_path=staging_path,
                context_package_dir=root / "context_packages",
                root=root,
            )

        self.assertEqual(result["orchestrator_decision"]["route"], "misconception_prepass")
        self.assertEqual(result["tutor_directive"]["pedagogical_act"], "misconception_intervention")
        self.assertEqual(result["tutor_directive"]["forced_retrieval_nodes"], ["MC_ACIDITY_01"])

    def test_orchestrator_normal_decision(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            misconception_dir = _write_misconception_fixture(root / "misconceptions")
            les_path = _write_les(root / "epistemic_state.json")
            staging_path = root / "session_staging.json"

            result = run_orchestrator(
                "How do I justify quality in SAT?",
                les_path=les_path,
                misconception_dir=misconception_dir,
                staging_path=staging_path,
                context_package_dir=root / "context_packages",
                root=root,
            )

        self.assertEqual(result["orchestrator_decision"]["route"], "normal_tutor")
        self.assertEqual(result["tutor_directive"]["pedagogical_act"], "answer_normally")
        self.assertEqual(result["tutor_directive"]["forced_retrieval_nodes"], [])

    def test_safe_for_examiner_always_false(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            misconception_dir = _write_misconception_fixture(root / "misconceptions")
            les_path = _write_les(root / "epistemic_state.json")
            staging_path = root / "session_staging.json"

            result = run_orchestrator(
                "Does more tannin mean better wine?",
                les_path=les_path,
                misconception_dir=misconception_dir,
                staging_path=staging_path,
                context_package_dir=root / "context_packages",
                root=root,
            )

        self.assertFalse(result["tutor_directive"]["safe_for_examiner"])
        self.assertFalse(result["governance_flags"]["safe_for_examiner"])
        self.assertFalse(result["les_context_used"]["governance"]["safe_for_examiner"])

    def test_misconception_context_package_creation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            misconception_dir = _write_misconception_fixture(root / "misconceptions")
            les_path = _write_les(root / "epistemic_state.json")
            staging_path = root / "session_staging.json"

            result = run_orchestrator(
                "So high acidity means the wine is lower quality?",
                top_k=5,
                language="es",
                les_path=les_path,
                misconception_dir=misconception_dir,
                staging_path=staging_path,
                context_package_dir=root / "context_packages",
                root=root,
            )

        package = result["context_package"]
        self.assertEqual(package["language"], "es")
        self.assertEqual(package["pedagogical_act"], "misconception_intervention")
        self.assertEqual(package["matched_misconception"]["misconception_id"], "MC_ACIDITY_01")
        self.assertEqual(package["governance"]["agent_corpus"], "tutor")
        self.assertFalse(package["governance"]["safe_for_examiner"])

    def test_forced_retrieval_node_included(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = run_orchestrator(
                "So high acidity means the wine is lower quality?",
                les_path=_write_les(root / "epistemic_state.json"),
                misconception_dir=_write_misconception_fixture(root / "misconceptions"),
                staging_path=root / "session_staging.json",
                context_package_dir=root / "context_packages",
                root=root,
            )

        forced_items = [item for item in result["context_package"]["retrieved_context"] if item["forced_retrieval"]]
        self.assertEqual(len(forced_items), 1)
        self.assertEqual(forced_items[0]["node_id"], "MC_ACIDITY_01")

    def test_normal_retrieval_package_when_no_misconception(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = run_orchestrator(
                "How do I justify quality in SAT?",
                les_path=_write_les(root / "epistemic_state.json"),
                misconception_dir=_write_misconception_fixture(root / "misconceptions"),
                staging_path=root / "session_staging.json",
                context_package_dir=root / "context_packages",
                root=root,
            )

        package = result["context_package"]
        self.assertEqual(package["pedagogical_act"], "answer_normally")
        self.assertEqual(package["forced_retrieval_nodes"], [])
        self.assertEqual(package["matched_misconception"], {})
        self.assertEqual(package["retrieval_plan"]["mode"], "normal_retrieval")

    def test_spanish_directive_included(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = run_orchestrator(
                "How do I justify quality in SAT?",
                language="es",
                les_path=_write_les(root / "epistemic_state.json"),
                misconception_dir=_write_misconception_fixture(root / "misconceptions"),
                staging_path=root / "session_staging.json",
                context_package_dir=root / "context_packages",
                root=root,
            )

        instruction = result["context_package"]["tutor_directive"]["response_language_instruction"]
        self.assertIn("Respond in Spanish", instruction)
        self.assertIn("Preserve official WSET terms", instruction)

    def test_english_directive_included(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = run_orchestrator(
                "How do I justify quality in SAT?",
                language="en",
                les_path=_write_les(root / "epistemic_state.json"),
                misconception_dir=_write_misconception_fixture(root / "misconceptions"),
                staging_path=root / "session_staging.json",
                context_package_dir=root / "context_packages",
                root=root,
            )

        instruction = result["context_package"]["tutor_directive"]["response_language_instruction"]
        self.assertIn("Respond in English", instruction)
        self.assertIn("Preserve official WSET terms", instruction)

    def test_context_package_written_locally(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = run_orchestrator(
                "How do I justify quality in SAT?",
                les_path=_write_les(root / "epistemic_state.json"),
                misconception_dir=_write_misconception_fixture(root / "misconceptions"),
                staging_path=root / "session_staging.json",
                context_package_dir=root / "context_packages",
                root=root,
            )

            latest_path = Path(result["context_package_paths"]["latest"])
            timestamped_path = Path(result["context_package_paths"]["timestamped"])
            latest = json.loads(latest_path.read_text(encoding="utf-8"))
            self.assertTrue(latest_path.exists())
            self.assertTrue(timestamped_path.exists())
            self.assertEqual(latest["student_query"], "How do I justify quality in SAT?")

    def test_no_llm_or_api_calls_planned(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = run_orchestrator(
                "How do I justify quality in SAT?",
                les_path=_write_les(root / "epistemic_state.json"),
                misconception_dir=_write_misconception_fixture(root / "misconceptions"),
                staging_path=root / "session_staging.json",
                context_package_dir=root / "context_packages",
                root=root,
            )

        plan = result["context_package"]["retrieval_plan"]
        self.assertFalse(plan["uses_llm"])
        self.assertFalse(plan["uses_api"])
        self.assertFalse(plan["uses_embeddings"])
        self.assertFalse(plan["uses_vector_db"])

    def test_session_staging_write(self):
        with tempfile.TemporaryDirectory() as tmp:
            staging_path = Path(tmp) / "session_staging.json"
            write_session_staging(
                {
                    "schema_version": "minimal_brain_v1",
                    "latest_session": {"student_query": "test"},
                    "governance": {"safe_for_examiner": False},
                },
                staging_path,
            )
            staged = json.loads(staging_path.read_text(encoding="utf-8"))

        self.assertEqual(staged["latest_session"]["student_query"], "test")
        self.assertFalse(staged["governance"]["safe_for_examiner"])


def _write_misconception_fixture(directory: Path) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    nodes = [
        {
            "misconception_id": "MC_ACIDITY_01",
            "misconception": "High acidity in a wine means the wine is low quality or unpleasant.",
            "corrected_understanding": "High acidity can be a hallmark of quality when balanced.",
            "severity": "medium",
            "tutor_intervention": "contrast_comparison",
            "detection_signals": [
                "This wine is too acidic so it must be poor quality",
                "High acidity means it's unripe",
            ],
        },
        {
            "misconception_id": "MC_TANNIN_01",
            "misconception": "Tannin is the same as bitterness.",
            "corrected_understanding": "Tannin is astringency, not bitterness.",
            "severity": "high",
            "tutor_intervention": "direct_correction",
            "detection_signals": ["high tannin means bitter taste"],
        },
    ]
    for node in nodes:
        (directory / f"{node['misconception_id'].lower()}.json").write_text(
            json.dumps(node),
            encoding="utf-8",
        )
    return directory


def _write_les(path: Path) -> Path:
    path.write_text(
        json.dumps(
            {
                "learner_id": "nazareth",
                "current_level": "WSET_L3",
                "known_weak_areas": [],
                "recent_misconceptions": [],
                "session_count": 0,
                "governance": {"safe_for_examiner": False},
            }
        ),
        encoding="utf-8",
    )
    return path


if __name__ == "__main__":
    unittest.main()
