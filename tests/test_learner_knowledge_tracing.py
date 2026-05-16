import json
import tempfile
import unittest
from pathlib import Path

from tools.learner_model.knowledge_tracing import (
    build_memory_summary,
    decay_mastery,
    estimate_learning_velocity,
    estimate_retention_risk,
    load_pedagogical_memory,
    save_pedagogical_memory,
    update_mastery,
    update_memory_from_results,
)
from tools.orchestrator.orchestrator import build_context_package
from tools.self_eval.evaluation_reporter import write_evaluation_reports
from tools.tutor.answer_builder import _select_explanation_depth
from tools.tutor.explanation_priority import build_explanation_priority
from tools.tutor.scaffolding_policy import select_scaffolding_policy


class KnowledgeTracingTests(unittest.TestCase):
    def test_mastery_updates_up_on_success_and_tracks_attempts(self):
        state = {"concept_id": "cool_climate", "mastery_probability": 0.4}

        updated = update_mastery(state, success=True, confidence=0.8, now="2026-05-16T00:00:00+00:00")

        self.assertGreater(updated["mastery_probability"], 0.4)
        self.assertEqual(updated["attempts"], 1)
        self.assertEqual(updated["successes"], 1)
        self.assertEqual(updated["last_seen"], "2026-05-16T00:00:00+00:00")

    def test_mastery_decay_and_retention_risk(self):
        state = {"concept_id": "acid", "mastery_probability": 0.8, "recent_failures": 2, "misconception_hits": 1}

        decayed = decay_mastery(state, days_since_seen=14)
        risk = estimate_retention_risk(decayed, days_since_seen=14)

        self.assertLess(decayed["mastery_probability"], 0.8)
        self.assertGreater(risk, 0.4)

    def test_learning_velocity_uses_success_rate_and_trend(self):
        state = {
            "concept_id": "sat_quality",
            "mastery_probability": 0.6,
            "attempts": 4,
            "successes": 3,
            "confidence_trend": [0.4, 0.5, 0.6, 0.7],
        }

        velocity = estimate_learning_velocity(state)

        self.assertGreater(velocity, 0.6)

    def test_pedagogical_memory_load_save(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "memory.json"
            save_pedagogical_memory({"skills": {"acid": {"concept_id": "acid", "mastery_probability": 0.9}}}, path)
            loaded = load_pedagogical_memory(path)

        self.assertIn("acid", loaded["skills"])
        self.assertFalse(loaded["governance"]["safe_for_examiner"])

    def test_persistent_misconceptions_accumulate(self):
        memory = update_memory_from_results({}, [_failed_result(), _failed_result()])

        self.assertIn("MC_TANNIN_QUALITY_02", memory["recurrent_misconceptions"])
        self.assertGreater(memory["recurrent_misconceptions"]["MC_TANNIN_QUALITY_02"]["persistence"], 0)
        self.assertIn("tannin -> balance", memory["difficult_causal_chains"])


class PedagogicalMemoryIntegrationTests(unittest.TestCase):
    def test_memory_summary_exposes_resurfacing_candidates(self):
        memory = {
            "skills": {
                "acid": {
                    "concept_id": "acid",
                    "mastery_probability": 0.2,
                    "attempts": 3,
                    "successes": 0,
                    "recent_failures": 3,
                    "misconception_hits": 1,
                }
            }
        }

        summary = build_memory_summary(memory)

        self.assertEqual(summary["low_mastery_concepts"][0]["concept_id"], "acid")
        self.assertEqual(summary["retention_risks"][0]["concept_id"], "acid")

    def test_context_package_preserves_pedagogical_priority_boost(self):
        package = build_context_package(
            query="How does cool climate affect acidity?",
            language="es",
            decision={"route": "normal_tutor"},
            pedagogical_act="answer_normally",
            forced_retrieval_nodes=[],
            matched_misconception={},
            les_context={"pedagogical_memory": _memory_summary()},
            retrieval_plan={"pedagogical_priority_boost": {"resurfacing_concepts": ["acid"]}},
            retrieved_context=[],
            tutor_directive={"safe_for_examiner": False},
            forced_causal_chains=[],
        )

        self.assertEqual(package["retrieval_plan"]["pedagogical_priority_boost"]["resurfacing_concepts"], ["acid"])
        self.assertFalse(package["governance"]["safe_for_examiner"])

    def test_persistent_misconception_forces_deep_depth(self):
        package = _package_with_memory()

        plan = build_explanation_priority(package)
        depth = _select_explanation_depth(package, "standard", plan)

        self.assertEqual(plan["recommended_depth"], "deep")
        self.assertEqual(depth, "deep")

    def test_scaffolding_policy_selects_direct_correction_for_high_severity(self):
        policy = select_scaffolding_policy(
            mastery_probability=0.8,
            cognitive_load="medium",
            urgency="high",
            misconception_severity="high",
        )

        self.assertEqual(policy["scaffolding_act"], "direct_correction")
        self.assertFalse(policy["governance"]["safe_for_examiner"])

    def test_reporter_writes_memory_and_reflection_signals(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            answer_path = root / "answer.md"
            package_path = root / "context.json"
            answer_path.write_text("CAUSA porque MECANISMO therefore EFECTO.", encoding="utf-8")
            package_path.write_text(json.dumps(_package_with_memory()), encoding="utf-8")
            paths = write_evaluation_reports(
                [_failed_result(answer_path=answer_path, package_path=package_path)],
                output_dir=root / "self-eval",
                feedback_path=root / "feedback.json",
                memory_path=root / "pedagogical_memory.json",
                reconcile_les=False,
            )

            memory = json.loads(Path(paths["pedagogical_memory"]).read_text(encoding="utf-8"))
            csv_text = Path(paths["csv"]).read_text(encoding="utf-8")

        self.assertIn("MC_TANNIN_QUALITY_02", memory["recurrent_misconceptions"])
        self.assertIn("retention_risk", csv_text)
        self.assertIn("scaffolding_effectiveness", csv_text)


def _failed_result(answer_path: Path | None = None, package_path: Path | None = None) -> dict:
    result = {
        "question_id": "Q_TANNIN",
        "question_type": "theory",
        "question_text": "Does more tannin mean better wine?",
        "expected_topics": ["tannin"],
        "expected_causal_links": ["tannin -> balance"],
        "expected_keywords": ["balance"],
        "comparison": {
            "failure_labels": ["misconception_unresolved", "missing_causal_link"],
            "likely_misconception_gaps": ["MC_TANNIN_QUALITY_02"],
            "missing_causal_links": ["tannin -> balance"],
            "retrieval_weaknesses": [],
        },
        "safe_for_examiner": False,
    }
    if answer_path:
        result["tutor_attempt_path"] = answer_path.as_posix()
    if package_path:
        result["tutor_context_package_path"] = package_path.as_posix()
    return result


def _memory_summary() -> dict:
    return {
        "low_mastery_concepts": [{"concept_id": "acid", "mastery_probability": 0.25}],
        "retention_risks": [{"concept_id": "acid", "retention_risk": 0.7}],
        "recurrent_misconceptions": [{"misconception_id": "MC_ACIDITY_01", "persistence": 0.8}],
        "difficult_causal_chains": [{"chain_id": "cool climate -> acid retention", "retention_risk": 0.75}],
        "preferred_depth": "deep",
        "governance": {"safe_for_examiner": False},
    }


def _package_with_memory() -> dict:
    return {
        "student_query": "Does more tannin mean better wine?",
        "pedagogical_act": "misconception_intervention",
        "orchestrator_decision": {"confidence": 0.8},
        "matched_misconception": {"misconception_id": "MC_TANNIN_QUALITY_02", "severity": "medium"},
        "learner_state_context": {"pedagogical_memory": _memory_summary()},
        "retrieval_plan": {"pedagogical_priority_boost": {"force_deep_explanation": True}},
        "retrieved_context": [],
        "forced_causal_chains": [],
        "tutor_directive": {"safe_for_examiner": False},
        "governance": {"safe_for_examiner": False, "examiner_scoring_allowed": False},
    }


if __name__ == "__main__":
    unittest.main()
