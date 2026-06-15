from __future__ import annotations

import copy
import json
import os
import tempfile
import unittest
from pathlib import Path

from tools.learner_model.adaptive_loop import (
    persist_learning_state_atomically,
    run_adaptive_learning_loop,
)
from tools.learner_model.knowledge_tracing import DEFAULT_PEDAGOGICAL_MEMORY
from tools.learner_model.learning_event_runtime import create_question_attempt
from tools.orchestrator.learner_state import DEFAULT_LES
from tools.question_generation.full_master_bank_session_composer import (
    compose_adaptive_master_bank_session,
    compose_master_bank_session,
    load_diagnostic_blueprint,
)
from tools.question_generation.master_bank import MASTER_BANK_PATH, SAFE_GOVERNANCE


ROOT = Path(__file__).resolve().parents[1]


def _signals(**overrides) -> dict:
    value = {
        "schema_version": "next_session_learning_signals_v1",
        "weak_topic_priority": [],
        "strong_topic_progression_candidate": [],
        "RA_reinforcement_priority": [],
        "misconception_repair_candidate": [],
        "causal_chain_reinforcement_candidate": [],
        "exposure_avoidance": [],
        "recommended_next_mode": "EXPRESS_10",
        "governance": copy.deepcopy(SAFE_GOVERNANCE),
    }
    value.update(overrides)
    return value


def _runtime_item() -> dict:
    return {
        "master_item_id": "wset3_runtime_loop",
        "source_question_id": "runtime_loop",
        "question_type": "single_best_answer",
        "curriculum": {
            "ra": "RA1",
            "topic": "RA1",
            "subtopic": "adaptive_loop",
            "difficulty": "intermediate",
        },
        "source_content": {
            "options": {"A": "Wrong", "B": "Correct", "C": "Wrong", "D": "Wrong"},
            "correct_answer_letter": "B",
        },
    }


class AdaptiveComposerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.bank = json.loads((ROOT / MASTER_BANK_PATH).read_text(encoding="utf-8"))
        cls.blueprint = load_diagnostic_blueprint(root=ROOT)

    def test_base_composer_shape_is_unchanged_without_signals(self) -> None:
        session = compose_master_bank_session(
            self.bank,
            DEFAULT_LES,
            mode="EXPRESS_10",
            blueprint=self.blueprint,
        )
        self.assertNotIn("adaptive_selection", session)
        self.assertEqual(session["schema_version"], "full_master_bank_session_v1")

    def test_recommended_mode_and_ra_are_consumed(self) -> None:
        session = compose_adaptive_master_bank_session(
            _signals(
                recommended_next_mode="RA_FOCUS",
                RA_reinforcement_priority=[
                    {"ra_id": "RA3", "priority": "high"}
                ],
            ),
            self.bank,
            DEFAULT_LES,
            question_count=5,
            blueprint=self.blueprint,
        )
        self.assertEqual(session["mode"], "RA_FOCUS")
        self.assertEqual(session["target_ra"], "RA3")
        self.assertEqual(session["achieved_composition"]["ra"], {"RA3": 5})
        self.assertTrue(session["adaptive_selection"]["signals_consumed"])

    def test_weak_topic_changes_candidate_order_without_changing_pool(self) -> None:
        baseline = compose_master_bank_session(
            self.bank,
            DEFAULT_LES,
            mode="RA_FOCUS",
            target_ra="RA4",
            question_count=1,
            blueprint=self.blueprint,
        )
        adaptive = compose_adaptive_master_bank_session(
            _signals(
                weak_topic_priority=[
                    {"topic": "RA4", "priority": "high", "stage": "emerging"}
                ]
            ),
            self.bank,
            DEFAULT_LES,
            mode="RA_FOCUS",
            target_ra="RA4",
            question_count=1,
            blueprint=self.blueprint,
        )
        self.assertNotEqual(
            baseline["master_item_ids"],
            adaptive["master_item_ids"],
        )
        self.assertEqual(adaptive["items"][0]["curriculum"]["topic"], "RA4")
        self.assertEqual(
            adaptive["operational_pool_counts"],
            baseline["operational_pool_counts"],
        )

    def test_exposure_avoidance_defers_explicit_item(self) -> None:
        baseline = compose_master_bank_session(
            self.bank,
            DEFAULT_LES,
            mode="EXPRESS_10",
            blueprint=self.blueprint,
        )
        avoided = baseline["master_item_ids"][0]
        adaptive = compose_adaptive_master_bank_session(
            _signals(exposure_avoidance=[avoided]),
            self.bank,
            DEFAULT_LES,
            mode="EXPRESS_10",
            blueprint=self.blueprint,
        )
        self.assertNotIn(avoided, adaptive["master_item_ids"])

    def test_learning_links_enable_misconception_targeting(self) -> None:
        bank = copy.deepcopy(self.bank)
        target = next(
            item for item in bank["items"] if item["master_item_id"] == "wset3_31"
        )
        target["learning_links"] = {
            "options": {
                "A": {
                    "diagnostic_role": "misconception",
                    "misconception_id": "MC_TARGET",
                }
            }
        }
        session = compose_adaptive_master_bank_session(
            _signals(misconception_repair_candidate=["MC_TARGET"]),
            bank,
            DEFAULT_LES,
            mode="RA_FOCUS",
            target_ra="RA1",
            question_count=1,
            blueprint=self.blueprint,
        )
        self.assertEqual(session["master_item_ids"], ["wset3_31"])

    def test_unsafe_signal_governance_fails_closed(self) -> None:
        signals = _signals()
        signals["governance"]["uses_llm"] = True
        with self.assertRaisesRegex(ValueError, "fail closed"):
            compose_adaptive_master_bank_session(
                signals,
                self.bank,
                DEFAULT_LES,
                blueprint=self.blueprint,
            )


class AtomicPersistenceTests(unittest.TestCase):
    def test_both_states_are_committed(self) -> None:
        memory = copy.deepcopy(DEFAULT_PEDAGOGICAL_MEMORY)
        memory["skills"]["RA1"] = {"concept_id": "RA1", "attempts": 1}
        les = copy.deepcopy(DEFAULT_LES)
        les["session_count"] = 3
        with tempfile.TemporaryDirectory() as tmp:
            memory_path = Path(tmp) / "pedagogical_memory.json"
            les_path = Path(tmp) / "epistemic_state.json"
            persist_learning_state_atomically(
                memory,
                les,
                memory_path=memory_path,
                les_path=les_path,
                updated_at="2026-06-06T12:00:00Z",
            )
            saved_memory = json.loads(memory_path.read_text(encoding="utf-8"))
            saved_les = json.loads(les_path.read_text(encoding="utf-8"))
        self.assertEqual(saved_memory["updated_at"], "2026-06-06T12:00:00Z")
        self.assertEqual(saved_les["session_count"], 3)
        self.assertTrue(
            all(value is False for value in saved_memory["governance"].values())
        )
        self.assertFalse(saved_les["governance"]["safe_for_examiner"])

    def test_second_install_failure_restores_both_originals(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            memory_path = Path(tmp) / "pedagogical_memory.json"
            les_path = Path(tmp) / "epistemic_state.json"
            memory_original = b'{"original":"memory"}\n'
            les_original = b'{"original":"les"}\n'
            memory_path.write_bytes(memory_original)
            les_path.write_bytes(les_original)
            install_count = 0

            def fail_second_install(source, destination):
                nonlocal install_count
                source_path = Path(source)
                if source_path.suffix == ".tmp":
                    install_count += 1
                    if install_count == 2:
                        raise OSError("simulated second install failure")
                os.replace(source, destination)

            with self.assertRaisesRegex(OSError, "second install failure"):
                persist_learning_state_atomically(
                    DEFAULT_PEDAGOGICAL_MEMORY,
                    DEFAULT_LES,
                    memory_path=memory_path,
                    les_path=les_path,
                    updated_at="2026-06-06T12:00:00Z",
                    replace_function=fail_second_install,
                )
            self.assertEqual(memory_path.read_bytes(), memory_original)
            self.assertEqual(les_path.read_bytes(), les_original)
            self.assertEqual(
                [path for path in Path(tmp).iterdir() if path.name.startswith(".")],
                [],
            )


class AdaptiveLoopIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.bank = json.loads((ROOT / MASTER_BANK_PATH).read_text(encoding="utf-8"))
        cls.blueprint = load_diagnostic_blueprint(root=ROOT)

    def test_event_changes_the_next_session(self) -> None:
        attempt = create_question_attempt(
            session_id="loop_session",
            question_id="wset3_runtime_loop",
            selected_option="A",
            is_correct=False,
            confidence="high",
            mode="EXPRESS_10",
            timestamp="2026-06-06T12:00:00Z",
        )
        with tempfile.TemporaryDirectory() as tmp:
            result = run_adaptive_learning_loop(
                attempt=attempt,
                item=_runtime_item(),
                memory=DEFAULT_PEDAGOGICAL_MEMORY,
                les=DEFAULT_LES,
                master_bank=self.bank,
                blueprint=self.blueprint,
                memory_path=Path(tmp) / "pedagogical_memory.json",
                les_path=Path(tmp) / "epistemic_state.json",
            )
        self.assertTrue(result["state_persisted"])
        self.assertEqual(result["next_session"]["mode"], "RA_FOCUS")
        self.assertEqual(result["next_session"]["target_ra"], "RA1")
        self.assertEqual(result["next_session"]["schema_version"], "adaptive_master_bank_session_v1")
        self.assertEqual(result["governance"], SAFE_GOVERNANCE)

    def test_paths_must_be_supplied_as_a_pair(self) -> None:
        attempt = create_question_attempt(
            session_id="loop_session",
            question_id="wset3_runtime_loop",
            selected_option="B",
            is_correct=True,
            mode="EXPRESS_10",
            timestamp="2026-06-06T12:00:00Z",
        )
        with self.assertRaisesRegex(ValueError, "provided together"):
            run_adaptive_learning_loop(
                attempt=attempt,
                item=_runtime_item(),
                memory=DEFAULT_PEDAGOGICAL_MEMORY,
                les=DEFAULT_LES,
                master_bank=self.bank,
                blueprint=self.blueprint,
                memory_path="memory.json",
            )


if __name__ == "__main__":
    unittest.main()
