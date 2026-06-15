from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

from tools.learner_model.knowledge_tracing import DEFAULT_PEDAGOGICAL_MEMORY
from tools.learner_model.learning_event_runtime import (
    build_diagnostic_outcome,
    build_formative_event,
    build_les_change_set,
    build_next_session_signals,
    create_question_attempt,
    process_question_attempt,
    reverse_cognitive_map_update,
    reverse_les_update,
    update_cognitive_map,
    update_les_from_learning_event,
)
from tools.orchestrator.learner_state import DEFAULT_LES
from tools.question_generation.master_bank import MASTER_BANK_PATH
from tools.question_generation.master_bank_eligibility import build_eligibility_index


ROOT = Path(__file__).resolve().parents[1]


def _item() -> dict:
    return {
        "master_item_id": "wset3_runtime_1",
        "source_question_id": "runtime_1",
        "question_type": "single_best_answer",
        "stem": "How does cool climate affect acidity?",
        "curriculum": {
            "ra": "RA1",
            "topic": "cool_climate_acidity",
            "subtopic": "climate_effects",
            "difficulty": "intermediate",
        },
        "source_content": {
            "options": {"A": "Low acid", "B": "High acid", "C": "No effect", "D": "Sweet"},
            "correct_answer_letter": "B",
        },
        "learning_links": {
            "causal_chain_id": "CC_COOL_CLIMATE_ACIDITY",
            "options": {
                "A": {
                    "diagnostic_role": "misconception",
                    "misconception_id": "MC_COOL_CLIMATE_01",
                    "causal_chain_id": "CC_COOL_CLIMATE_ACIDITY",
                }
            },
        },
    }


def _attempt(correct: bool = False, confidence: str = "high") -> dict:
    return create_question_attempt(
        session_id="session_runtime_1",
        question_id="wset3_runtime_1",
        selected_option="B" if correct else "A",
        is_correct=correct,
        confidence=confidence,
        answer_changed=True,
        response_time_band="slow",
        mode="EXPRESS_10",
        timestamp="2026-06-06T12:00:00Z",
    )


class QuestionAttemptRuntimeTests(unittest.TestCase):
    def test_attempt_records_required_observations(self) -> None:
        attempt = _attempt()
        self.assertEqual(attempt["session_id"], "session_runtime_1")
        self.assertEqual(attempt["selected_option"], "A")
        self.assertFalse(attempt["is_correct"])
        self.assertTrue(attempt["answer_changed"])
        self.assertEqual(attempt["response_time_band"], "slow")
        self.assertEqual(attempt["mode"], "EXPRESS_10")

    def test_attempt_is_deterministic(self) -> None:
        self.assertEqual(_attempt(), _attempt())

    def test_attempt_rejects_invalid_option(self) -> None:
        with self.assertRaises(ValueError):
            create_question_attempt(
                session_id="s",
                question_id="q",
                selected_option="E",
                is_correct=False,
                mode="EXPRESS_10",
                timestamp="2026-06-06T12:00:00Z",
            )

    def test_attempt_has_no_assessment_authority_fields(self) -> None:
        self.assertTrue({"score", "percentage", "pass", "fail"}.isdisjoint(_keys(_attempt())))

    def test_all_session_modes_use_same_attempt_contract(self) -> None:
        for mode in (
            "EXPRESS_10",
            "QUICK_25",
            "STANDARD_50",
            "FULL_DIAGNOSTIC",
            "RA_FOCUS",
        ):
            with self.subTest(mode=mode):
                attempt = create_question_attempt(
                    session_id="s",
                    question_id="q",
                    selected_option="A",
                    is_correct=False,
                    mode=mode,
                    timestamp="2026-06-06T12:00:00Z",
                )
                self.assertEqual(attempt["mode"], mode)


class DiagnosticOutcomeRuntimeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        schema = json.loads(
            (ROOT / "knowledge/enrichment/diagnostic_outcome.schema.json").read_text(
                encoding="utf-8"
            )
        )
        cls.validator = Draft202012Validator(schema)

    def test_attempt_to_outcome_matches_existing_schema(self) -> None:
        outcome = build_diagnostic_outcome(_attempt(), _item())
        errors = list(self.validator.iter_errors(outcome))
        self.assertEqual(errors, [], [error.message for error in errors])

    def test_outcome_derives_trace_and_distractor_role(self) -> None:
        outcome = build_diagnostic_outcome(_attempt(), _item())
        trace = outcome["source_trace"]
        self.assertEqual(trace["ra_id"], "RA1")
        self.assertEqual(trace["topic"], "cool_climate_acidity")
        self.assertEqual(trace["misconception_id"], "MC_COOL_CLIMATE_01")
        self.assertEqual(trace["causal_chain_id"], "CC_COOL_CLIMATE_ACIDITY")
        self.assertEqual(trace["selected_option_diagnostic_role"], "misconception")

    def test_correct_outcome_routes_to_progression_without_mark(self) -> None:
        outcome = build_diagnostic_outcome(_attempt(correct=True), _item())
        self.assertEqual(outcome["remediation_routing"]["recommended_next_action"], "increase_difficulty")
        self.assertTrue({"score", "percentage", "pass", "fail"}.isdisjoint(_keys(outcome)))


class FormativeEventTests(unittest.TestCase):
    def test_outcome_to_formative_event(self) -> None:
        attempt = _attempt()
        event = build_formative_event(
            attempt, build_diagnostic_outcome(attempt, _item()), _item()
        )
        self.assertEqual(event["difficulty"], "intermediate")
        self.assertEqual(event["topic_signal_delta"], -1)
        self.assertTrue(event["reinforcement_needed"])
        self.assertFalse(event["progression_candidate"])

    def test_correct_high_confidence_is_progression_candidate(self) -> None:
        attempt = _attempt(correct=True)
        event = build_formative_event(
            attempt, build_diagnostic_outcome(attempt, _item()), _item()
        )
        self.assertEqual(event["topic_signal_delta"], 1)
        self.assertTrue(event["progression_candidate"])


class CognitiveMapUpdateTests(unittest.TestCase):
    def test_weak_topic_increases_reinforcement_priority(self) -> None:
        attempt = _attempt()
        event = build_formative_event(
            attempt, build_diagnostic_outcome(attempt, _item()), _item()
        )
        memory, change_set = update_cognitive_map(DEFAULT_PEDAGOGICAL_MEMORY, event)
        skill = memory["skills"]["cool_climate_acidity"]
        self.assertEqual(skill["reinforcement_priority"], "high")
        self.assertEqual(skill["gap_count"], 1)
        self.assertEqual(skill["learning_stage"], "emerging")
        self.assertEqual(change_set["before_skill"]["concept_id"], "cool_climate_acidity")

    def test_strong_topic_becomes_progression_candidate(self) -> None:
        memory = copy.deepcopy(DEFAULT_PEDAGOGICAL_MEMORY)
        memory["skills"]["cool_climate_acidity"] = {
            "concept_id": "cool_climate_acidity",
            "mastery_probability": 0.81,
            "attempts": 4,
            "successes": 4,
            "recent_failures": 0,
            "misconception_hits": 0,
            "confidence_trend": [0.8, 0.8, 0.8, 0.8],
        }
        attempt = _attempt(correct=True)
        event = build_formative_event(
            attempt, build_diagnostic_outcome(attempt, _item()), _item()
        )
        updated, _ = update_cognitive_map(memory, event)
        skill = updated["skills"]["cool_climate_acidity"]
        self.assertEqual(skill["learning_stage"], "ready_for_greater_challenge")
        self.assertTrue(skill["progression_candidate"])

    def test_memory_event_log_is_append_only(self) -> None:
        attempt = _attempt()
        event = build_formative_event(
            attempt, build_diagnostic_outcome(attempt, _item()), _item()
        )
        first, _ = update_cognitive_map(DEFAULT_PEDAGOGICAL_MEMORY, event)
        second, _ = update_cognitive_map(first, event)
        self.assertEqual(len(first["learning_events"]), 1)
        self.assertEqual(len(second["learning_events"]), 2)

    def test_cognitive_map_update_does_not_mutate_input(self) -> None:
        memory = copy.deepcopy(DEFAULT_PEDAGOGICAL_MEMORY)
        before = copy.deepcopy(memory)
        attempt = _attempt()
        event = build_formative_event(
            attempt, build_diagnostic_outcome(attempt, _item()), _item()
        )
        update_cognitive_map(memory, event)
        self.assertEqual(memory, before)

    def test_cognitive_map_change_set_reverses_update(self) -> None:
        original = copy.deepcopy(DEFAULT_PEDAGOGICAL_MEMORY)
        attempt = _attempt()
        event = build_formative_event(
            attempt, build_diagnostic_outcome(attempt, _item()), _item()
        )
        updated, change_set = update_cognitive_map(original, event)
        reversed_memory = reverse_cognitive_map_update(updated, change_set)
        self.assertEqual(
            reversed_memory["skills"],
            original["skills"],
        )
        self.assertNotIn("learning_events", reversed_memory)


class LesAdapterTests(unittest.TestCase):
    def test_cognitive_event_updates_existing_les_containers(self) -> None:
        attempt = _attempt()
        event = build_formative_event(
            attempt, build_diagnostic_outcome(attempt, _item()), _item()
        )
        les, emitted = update_les_from_learning_event(DEFAULT_LES, event, _item())
        self.assertEqual(les["topic_signals"]["cool_climate_acidity"]["incorrect_count"], 1)
        self.assertEqual(les["RA_signals"]["RA1"]["performance"]["incorrect_count"], 1)
        self.assertEqual(les["question_exposure_signals"]["wset3_runtime_1"]["exposure_count"], 1)
        self.assertEqual(les["misconception_signals"]["MC_COOL_CLIMATE_01"]["detection_count"], 1)
        self.assertIn("misconception_triggered", emitted)
        self.assertIn("causal_gap_detected", emitted)

    def test_les_learning_log_is_traceable(self) -> None:
        attempt = _attempt()
        event = build_formative_event(
            attempt, build_diagnostic_outcome(attempt, _item()), _item()
        )
        les, _ = update_les_from_learning_event(DEFAULT_LES, event, _item())
        self.assertEqual(les["learning_event_log"][0]["event_id"], event["event_id"])

    def test_les_adapter_is_deterministic(self) -> None:
        attempt = _attempt()
        event = build_formative_event(
            attempt, build_diagnostic_outcome(attempt, _item()), _item()
        )
        self.assertEqual(
            update_les_from_learning_event(DEFAULT_LES, event, _item()),
            update_les_from_learning_event(DEFAULT_LES, event, _item()),
        )

    def test_les_change_set_reverses_update(self) -> None:
        original = copy.deepcopy(DEFAULT_LES)
        attempt = _attempt()
        event = build_formative_event(
            attempt, build_diagnostic_outcome(attempt, _item()), _item()
        )
        updated, _ = update_les_from_learning_event(original, event, _item())
        change_set = build_les_change_set(original, updated, event)
        self.assertEqual(reverse_les_update(updated, change_set), original)


class NextSessionSignalTests(unittest.TestCase):
    def test_weak_event_prepares_next_session_signals(self) -> None:
        result = process_question_attempt(
            attempt=_attempt(),
            item=_item(),
            memory=DEFAULT_PEDAGOGICAL_MEMORY,
            les=DEFAULT_LES,
        )
        signals = result["next_session_signals"]
        self.assertEqual(signals["weak_topic_priority"][0]["topic"], "cool_climate_acidity")
        self.assertEqual(signals["RA_reinforcement_priority"][0]["ra_id"], "RA1")
        self.assertIn("MC_COOL_CLIMATE_01", signals["misconception_repair_candidate"])
        self.assertIn("CC_COOL_CLIMATE_ACIDITY", signals["causal_chain_reinforcement_candidate"])
        self.assertEqual(signals["recommended_next_mode"], "RA_FOCUS")

    def test_strong_topic_signal_recommends_higher_challenge(self) -> None:
        memory = copy.deepcopy(DEFAULT_PEDAGOGICAL_MEMORY)
        memory["skills"]["cool_climate_acidity"] = {
            "concept_id": "cool_climate_acidity",
            "mastery_probability": 0.84,
            "attempts": 5,
            "successes": 5,
            "recent_failures": 0,
            "misconception_hits": 0,
            "confidence_trend": [0.8] * 4,
            "reinforcement_priority": "low",
            "learning_stage": "ready_for_greater_challenge",
            "progression_candidate": True,
        }
        signals = build_next_session_signals(memory, DEFAULT_LES)
        self.assertEqual(
            signals["strong_topic_progression_candidate"][0]["next_challenge"],
            "integration",
        )
        self.assertEqual(signals["recommended_next_mode"], "STANDARD_50")

    def test_exposure_avoidance_uses_existing_les_signal(self) -> None:
        les = copy.deepcopy(DEFAULT_LES)
        les["question_exposure_signals"]["q1"] = {
            "question_id": "q1",
            "exposure_count": 2,
            "last_seen": "2026-06-06T12:00:00Z",
            "recent_history": [],
        }
        signals = build_next_session_signals(DEFAULT_PEDAGOGICAL_MEMORY, les)
        self.assertEqual(signals["exposure_avoidance"], ["q1"])


class BoundaryTests(unittest.TestCase):
    def test_runtime_environment_uses_canonical_operational_eligibility(self) -> None:
        bank = json.loads((ROOT / MASTER_BANK_PATH).read_text(encoding="utf-8"))
        counts = build_eligibility_index(bank)["operational_counts"]
        self.assertEqual(
            counts,
            {
                "total_master_bank": 710,
                "sba_operational_pool": 670,
                "open_response_candidate_pool": 38,
                "open_response_review_pool": 2,
                "inactive": 0,
                "public_lab": 36,
            },
        )

    def test_end_to_end_is_deterministic_and_governance_clean(self) -> None:
        kwargs = {
            "attempt": _attempt(),
            "item": _item(),
            "memory": DEFAULT_PEDAGOGICAL_MEMORY,
            "les": DEFAULT_LES,
        }
        first = process_question_attempt(**kwargs)
        second = process_question_attempt(**kwargs)
        self.assertEqual(first, second)
        self.assertTrue(_all_governance_false(first))

    def test_runtime_does_not_modify_public_lab_or_open_response(self) -> None:
        public_path = ROOT / "frontend/diagnostic-sba/preguntas.json"
        open_path = ROOT / "tools/learner_model/open_response_evaluator.py"
        before = (public_path.read_bytes(), open_path.read_bytes())
        process_question_attempt(
            attempt=_attempt(),
            item=_item(),
            memory=DEFAULT_PEDAGOGICAL_MEMORY,
            les=DEFAULT_LES,
        )
        self.assertEqual(before, (public_path.read_bytes(), open_path.read_bytes()))

    def test_no_score_percentage_or_pass_fail_in_runtime_output(self) -> None:
        result = process_question_attempt(
            attempt=_attempt(),
            item=_item(),
            memory=DEFAULT_PEDAGOGICAL_MEMORY,
            les=DEFAULT_LES,
        )
        self.assertTrue({"score", "percentage", "pass", "fail"}.isdisjoint(_keys(result)))


def _keys(value) -> set[str]:
    keys: set[str] = set()
    if isinstance(value, dict):
        for key, nested in value.items():
            keys.add(str(key).lower())
            keys.update(_keys(nested))
    elif isinstance(value, list):
        for nested in value:
            keys.update(_keys(nested))
    return keys


def _all_governance_false(value) -> bool:
    if isinstance(value, dict):
        for key, nested in value.items():
            if key in {
                "safe_for_examiner",
                "examiner_scoring_allowed",
                "uses_llm",
                "uses_api",
                "uses_embeddings",
                "uses_vector_db",
                "cloud_services_active",
            } and nested is not False:
                return False
            if not _all_governance_false(nested):
                return False
    elif isinstance(value, list):
        return all(_all_governance_false(item) for item in value)
    return True


if __name__ == "__main__":
    unittest.main()
