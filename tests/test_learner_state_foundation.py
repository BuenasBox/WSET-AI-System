import copy
import json
import tempfile
import unittest
from pathlib import Path

from tools.orchestrator.learner_state import (
    DEFAULT_LES,
    RA_IDS,
    append_question_exposure,
    build_les_context,
    create_causal_chain_signal,
    create_misconception_signal,
    create_question_exposure,
    create_ra_signal,
    create_topic_signal,
    load_learner_state,
    write_learner_state,
)


class LearnerStateSchemaCompatibilityTests(unittest.TestCase):
    def test_default_schema_version_remains_v2(self):
        self.assertEqual(DEFAULT_LES["schema_version"], "minimal_brain_v2")

    def test_default_contains_all_foundation_containers(self):
        self.assertEqual(DEFAULT_LES["topic_signals"], {})
        self.assertEqual(DEFAULT_LES["misconception_signals"], {})
        self.assertEqual(DEFAULT_LES["causal_chain_signals"], {})
        self.assertEqual(DEFAULT_LES["question_exposure_log"], [])
        self.assertEqual(DEFAULT_LES["question_exposure_signals"], {})

    def test_default_ra_signals_cover_ra1_through_ra5(self):
        self.assertEqual(tuple(DEFAULT_LES["RA_signals"]), RA_IDS)
        for ra_id in RA_IDS:
            self.assertEqual(DEFAULT_LES["RA_signals"][ra_id], create_ra_signal(ra_id))

    def test_legacy_state_loads_with_additive_defaults(self):
        legacy = {
            "learner_id": "legacy",
            "schema_version": "minimal_brain_v2",
            "current_level": "WSET_L3",
            "known_weak_areas": ["acidity"],
            "recent_misconceptions": ["MC_ACIDITY_01"],
            "session_count": 4,
            "custom_legacy_field": {"preserve": True},
            "governance": {"safe_for_examiner": False},
        }
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "les.json"
            path.write_text(json.dumps(legacy), encoding="utf-8")
            loaded = load_learner_state(path)

        self.assertEqual(loaded["learner_id"], "legacy")
        self.assertEqual(loaded["known_weak_areas"], ["acidity"])
        self.assertEqual(loaded["custom_legacy_field"], {"preserve": True})
        self.assertEqual(loaded["topic_signals"], {})
        self.assertEqual(tuple(loaded["RA_signals"]), RA_IDS)

    def test_new_signals_are_not_exposed_to_existing_tutor_context(self):
        state = copy.deepcopy(DEFAULT_LES)
        state["topic_signals"]["climate"] = create_topic_signal("climate")
        state["question_exposure_log"].append(
            create_question_exposure(
                "Q1",
                timestamp="2026-06-06T12:00:00Z",
                mode="diagnostic_sba",
                result="correct",
            )
        )

        context = build_les_context(state)

        for field in (
            "topic_signals",
            "RA_signals",
            "misconception_signals",
            "causal_chain_signals",
            "question_exposure_log",
        ):
            self.assertNotIn(field, context)


class SignalContractTests(unittest.TestCase):
    def test_topic_signal_records_observable_fields(self):
        signal = create_topic_signal(
            "cool_climate",
            exposure_count=3,
            correct_count=2,
            incorrect_count=1,
            confidence_level="medium",
            last_seen="2026-06-06T12:00:00Z",
        )

        self.assertEqual(
            signal,
            {
                "topic": "cool_climate",
                "exposure_count": 3,
                "correct_count": 2,
                "incorrect_count": 1,
                "confidence_level": "medium",
                "weakness_level": "not_recorded",
                "last_seen": "2026-06-06T12:00:00Z",
            },
        )

    def test_topic_confidence_is_explicit_not_calculated(self):
        signal = create_topic_signal(
            "acidity",
            exposure_count=10,
            correct_count=10,
            confidence_level="not_recorded",
        )
        self.assertEqual(signal["confidence_level"], "not_recorded")

    def test_ra_signal_records_exposure_performance_and_trend(self):
        signal = create_ra_signal(
            "ra3",
            exposure_count=5,
            correct_count=3,
            incorrect_count=2,
            trend="stable",
            last_seen="2026-06-06T12:00:00Z",
        )

        self.assertEqual(signal["ra_id"], "RA3")
        self.assertEqual(signal["exposure_count"], 5)
        self.assertEqual(signal["performance"], {"correct_count": 3, "incorrect_count": 2})
        self.assertEqual(signal["trend"], "stable")

    def test_ra_trend_is_explicit_not_calculated(self):
        signal = create_ra_signal("RA2", exposure_count=8, correct_count=8)
        self.assertEqual(signal["trend"], "not_observed")

    def test_misconception_signal_contract(self):
        signal = create_misconception_signal(
            "MC_ACIDITY_01",
            detection_count=2,
            last_detected="2026-06-06T12:00:00Z",
        )
        self.assertEqual(
            signal,
            {
                "misconception_id": "MC_ACIDITY_01",
                "detection_count": 2,
                "last_detected": "2026-06-06T12:00:00Z",
            },
        )

    def test_causal_chain_signal_contract(self):
        signal = create_causal_chain_signal(
            "CC_COOL_CLIMATE_ACIDITY",
            exposure_count=4,
            demonstrated_count=1,
        )
        self.assertEqual(
            signal,
            {
                "causal_chain_id": "CC_COOL_CLIMATE_ACIDITY",
                "exposure_count": 4,
                "demonstrated_count": 1,
            },
        )

    def test_negative_counts_are_rejected(self):
        factories = (
            lambda: create_topic_signal("acid", exposure_count=-1),
            lambda: create_ra_signal("RA1", incorrect_count=-1),
            lambda: create_misconception_signal("MC1", detection_count=-1),
            lambda: create_causal_chain_signal("CC1", demonstrated_count=-1),
        )
        for factory in factories:
            with self.subTest(factory=factory):
                with self.assertRaises(ValueError):
                    factory()

    def test_boolean_counts_are_rejected(self):
        with self.assertRaises(ValueError):
            create_topic_signal("acid", exposure_count=True)

    def test_unknown_ra_is_rejected(self):
        with self.assertRaises(ValueError):
            create_ra_signal("RA6")

    def test_unknown_confidence_and_trend_are_rejected(self):
        with self.assertRaises(ValueError):
            create_topic_signal("acid", confidence_level="expert")
        with self.assertRaises(ValueError):
            create_topic_signal("acid", weakness_level="severe")
        with self.assertRaises(ValueError):
            create_ra_signal("RA1", trend="mastered")


class LearnerStatePersistenceTests(unittest.TestCase):
    def test_full_signal_round_trip(self):
        state = copy.deepcopy(DEFAULT_LES)
        state["topic_signals"]["acidity"] = create_topic_signal(
            "acidity",
            exposure_count=2,
            correct_count=1,
            incorrect_count=1,
            confidence_level="low",
            last_seen="2026-06-06T12:00:00Z",
        )
        state["RA_signals"]["RA1"] = create_ra_signal(
            "RA1",
            exposure_count=2,
            correct_count=1,
            incorrect_count=1,
            trend="improving",
            last_seen="2026-06-06T12:00:00Z",
        )
        state["misconception_signals"]["MC_ACIDITY_01"] = create_misconception_signal(
            "MC_ACIDITY_01",
            detection_count=1,
            last_detected="2026-06-06T12:00:00Z",
        )
        state["causal_chain_signals"]["CC_ACIDITY"] = create_causal_chain_signal(
            "CC_ACIDITY",
            exposure_count=2,
            demonstrated_count=1,
        )

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "les.json"
            write_learner_state(state, path)
            loaded = load_learner_state(path)

        self.assertEqual(loaded["topic_signals"], state["topic_signals"])
        self.assertEqual(loaded["RA_signals"], state["RA_signals"])
        self.assertEqual(loaded["misconception_signals"], state["misconception_signals"])
        self.assertEqual(loaded["causal_chain_signals"], state["causal_chain_signals"])

    def test_write_learner_state_does_not_mutate_input(self):
        state = copy.deepcopy(DEFAULT_LES)
        state["governance"]["safe_for_examiner"] = True
        original = copy.deepcopy(state)

        with tempfile.TemporaryDirectory() as tmp:
            write_learner_state(state, Path(tmp) / "les.json")

        self.assertEqual(state, original)

    def test_deserialization_repairs_invalid_new_containers(self):
        state = copy.deepcopy(DEFAULT_LES)
        state["topic_signals"] = []
        state["RA_signals"] = "invalid"
        state["misconception_signals"] = None
        state["causal_chain_signals"] = 7
        state["question_exposure_log"] = {}

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "les.json"
            path.write_text(json.dumps(state), encoding="utf-8")
            loaded = load_learner_state(path)

        self.assertEqual(loaded["topic_signals"], {})
        self.assertEqual(tuple(loaded["RA_signals"]), RA_IDS)
        self.assertEqual(loaded["misconception_signals"], {})
        self.assertEqual(loaded["causal_chain_signals"], {})
        self.assertEqual(loaded["question_exposure_log"], [])

    def test_deserialization_repairs_invalid_governance_container(self):
        state = copy.deepcopy(DEFAULT_LES)
        state["governance"] = None

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "les.json"
            path.write_text(json.dumps(state), encoding="utf-8")
            loaded = load_learner_state(path)

        self.assertFalse(loaded["governance"]["safe_for_examiner"])
        self.assertFalse(loaded["governance"]["examiner_scoring_allowed"])

    def test_malformed_signal_entries_are_dropped_without_affecting_legacy_state(self):
        state = copy.deepcopy(DEFAULT_LES)
        state["session_count"] = 11
        state["topic_signals"] = {
            "valid": create_topic_signal("valid"),
            "invalid": {"topic": "invalid", "exposure_count": -1},
        }

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "les.json"
            path.write_text(json.dumps(state), encoding="utf-8")
            loaded = load_learner_state(path)

        self.assertEqual(loaded["session_count"], 11)
        self.assertEqual(list(loaded["topic_signals"]), ["valid"])


class QuestionExposureLogTests(unittest.TestCase):
    def test_question_exposure_contract(self):
        exposure = create_question_exposure(
            "Q_RA1_001",
            timestamp="2026-06-06T12:00:00Z",
            mode="diagnostic_sba",
            result="incorrect",
        )
        self.assertEqual(
            exposure,
            {
                "question_id": "Q_RA1_001",
                "timestamp": "2026-06-06T12:00:00Z",
                "mode": "diagnostic_sba",
                "result": "incorrect",
            },
        )

    def test_append_returns_copy_and_preserves_order(self):
        state = copy.deepcopy(DEFAULT_LES)
        first = create_question_exposure(
            "Q1",
            timestamp="2026-06-06T12:00:00Z",
            mode="diagnostic_sba",
            result="correct",
        )
        second = create_question_exposure(
            "Q2",
            timestamp="2026-06-06T12:01:00Z",
            mode="open_response_lab",
            result="unanswered",
        )

        updated = append_question_exposure(state, first)
        updated = append_question_exposure(updated, second)

        self.assertEqual(state["question_exposure_log"], [])
        self.assertEqual([item["question_id"] for item in updated["question_exposure_log"]], ["Q1", "Q2"])

    def test_exposure_log_persists_round_trip(self):
        state = append_question_exposure(
            DEFAULT_LES,
            create_question_exposure(
                "Q1",
                timestamp="2026-06-06T12:00:00Z",
                mode="diagnostic_sba",
                result="correct",
            ),
        )

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "les.json"
            write_learner_state(state, path)
            loaded = load_learner_state(path)

        self.assertEqual(loaded["question_exposure_log"], state["question_exposure_log"])

    def test_unknown_result_is_rejected(self):
        for forbidden in ("pass", "fail", "85%", "grade_a"):
            with self.subTest(result=forbidden):
                with self.assertRaises(ValueError):
                    create_question_exposure(
                        "Q1",
                        timestamp="2026-06-06T12:00:00Z",
                        mode="diagnostic_sba",
                        result=forbidden,
                    )

    def test_blank_question_fields_are_rejected(self):
        with self.assertRaises(ValueError):
            create_question_exposure(
                "",
                timestamp="2026-06-06T12:00:00Z",
                mode="diagnostic_sba",
                result="correct",
            )


class LearnerStateGovernanceTests(unittest.TestCase):
    def test_default_governance_disables_examiner_authority(self):
        self.assertFalse(DEFAULT_LES["governance"]["safe_for_examiner"])
        self.assertFalse(DEFAULT_LES["governance"]["examiner_scoring_allowed"])

    def test_load_forces_examiner_authority_flags_false(self):
        state = copy.deepcopy(DEFAULT_LES)
        state["governance"]["safe_for_examiner"] = True
        state["governance"]["examiner_scoring_allowed"] = True

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "les.json"
            path.write_text(json.dumps(state), encoding="utf-8")
            loaded = load_learner_state(path)

        self.assertFalse(loaded["governance"]["safe_for_examiner"])
        self.assertFalse(loaded["governance"]["examiner_scoring_allowed"])

    def test_write_forces_examiner_authority_flags_false_on_disk(self):
        state = copy.deepcopy(DEFAULT_LES)
        state["governance"]["safe_for_examiner"] = "truthy"
        state["governance"]["examiner_scoring_allowed"] = 1

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "les.json"
            write_learner_state(state, path)
            persisted = json.loads(path.read_text(encoding="utf-8"))

        self.assertIs(persisted["governance"]["safe_for_examiner"], False)
        self.assertIs(persisted["governance"]["examiner_scoring_allowed"], False)

    def test_foundation_contracts_do_not_contain_prohibited_assessment_fields(self):
        state = copy.deepcopy(DEFAULT_LES)
        state["topic_signals"]["acid"] = create_topic_signal("acid")
        state["misconception_signals"]["MC1"] = create_misconception_signal("MC1")
        state["causal_chain_signals"]["CC1"] = create_causal_chain_signal("CC1")
        state["question_exposure_log"].append(
            create_question_exposure(
                "Q1",
                timestamp="2026-06-06T12:00:00Z",
                mode="diagnostic_sba",
                result="correct",
            )
        )
        prohibited = {"score", "grade", "percentage", "pass", "fail", "proficiency"}

        keys = _recursive_keys(state)

        self.assertTrue(prohibited.isdisjoint(keys))


def _recursive_keys(value):
    keys = set()
    if isinstance(value, dict):
        for key, nested in value.items():
            keys.add(str(key).lower())
            keys.update(_recursive_keys(nested))
    elif isinstance(value, list):
        for nested in value:
            keys.update(_recursive_keys(nested))
    return keys


if __name__ == "__main__":
    unittest.main()
