from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from tools.dashboard.master_bank_utilization_data import (
    build_master_bank_utilization_data,
)
from tools.orchestrator.learner_state import (
    DEFAULT_LES,
    load_learner_state,
    record_session_observations,
    write_learner_state,
)
from tools.question_generation.full_master_bank_session_composer import (
    BLUEPRINT_PATH,
    SUPPORTED_MODES,
    compose_master_bank_session,
    load_diagnostic_blueprint,
    validate_diagnostic_blueprint,
)
from tools.question_generation.master_bank import MASTER_BANK_PATH, SAFE_GOVERNANCE
from tools.question_generation.master_bank_eligibility import (
    ELIGIBILITY_CATEGORIES,
    build_eligibility_index,
    classify_master_item,
    is_session_eligible,
    load_open_response_suitability_index,
)


ROOT = Path(__file__).resolve().parents[1]


class FullMasterBankFixture(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.bank = json.loads((ROOT / MASTER_BANK_PATH).read_text(encoding="utf-8"))
        cls.blueprint = load_diagnostic_blueprint(root=ROOT)
        cls.suitability = load_open_response_suitability_index(root=ROOT)


class DiagnosticBlueprintTests(FullMasterBankFixture):
    def test_blueprint_exists_and_is_valid(self) -> None:
        self.assertTrue((ROOT / BLUEPRINT_PATH).exists())
        self.assertEqual(validate_diagnostic_blueprint(self.blueprint), [])

    def test_all_required_modes_exist(self) -> None:
        self.assertEqual(tuple(self.blueprint["modes"]), SUPPORTED_MODES)

    def test_named_mode_sizes(self) -> None:
        modes = self.blueprint["modes"]
        self.assertEqual(modes["EXPRESS_10"]["question_count"], 10)
        self.assertEqual(modes["QUICK_25"]["question_count"], 25)
        self.assertEqual(modes["STANDARD_50"]["question_count"], 50)
        self.assertEqual(modes["FULL_DIAGNOSTIC"]["question_count"], 100)

    def test_blueprint_defines_ra_difficulty_topic_and_composition(self) -> None:
        for mode, config in self.blueprint["modes"].items():
            with self.subTest(mode=mode):
                if mode != "RA_FOCUS":
                    self.assertEqual(set(config["ra_distribution"]), set(DEFAULT_LES["RA_signals"]))
                self.assertEqual(
                    set(config["difficulty_distribution"]),
                    {"foundational", "intermediate", "distinction"},
                )
                self.assertIn("strategy", config["topic_distribution"])
                self.assertIn("question_types", config["composition"])

    def test_governance_is_false(self) -> None:
        self.assertTrue(
            all(value is False for value in self.blueprint["governance"].values())
        )


class MasterBankEligibilityTests(FullMasterBankFixture):
    def test_all_616_records_are_classified(self) -> None:
        index = build_eligibility_index(self.bank)
        self.assertEqual(index["record_count"], 616)
        self.assertEqual(sum(index["primary_counts"].values()), 616)
        self.assertEqual(set(index["primary_counts"]), set(ELIGIBILITY_CATEGORIES))

    def test_primary_classification_counts(self) -> None:
        index = build_eligibility_index(self.bank)
        self.assertEqual(
            index["primary_counts"],
            {
                "public_lab": 36,
                "private_practice": 553,
                "adaptive_candidate": 0,
                "open_response_candidate": 27,
                "open_response_review_pool": 0,
                "inactive": 0,
            },
        )

    def test_adaptive_candidate_is_secondary_not_activation(self) -> None:
        index = build_eligibility_index(self.bank)
        self.assertEqual(index["category_counts"]["adaptive_candidate"], 587)
        self.assertEqual(index["primary_counts"]["adaptive_candidate"], 0)

    def test_operational_pool_metrics_match_suitability_contract(self) -> None:
        index = build_eligibility_index(self.bank)
        self.assertEqual(
            index["operational_counts"],
            {
                "total_master_bank": 616,
                "sba_operational_pool": 589,
                "open_response_candidate_pool": 27,
                "open_response_review_pool": 0,
                "inactive": 0,
                "public_lab": 36,
            },
        )

    def test_public_lab_is_preserved_and_private_eligible(self) -> None:
        public = next(
            item for item in self.bank["items"] if item["status"]["public_lab"]
        )
        eligibility = classify_master_item(public)
        self.assertEqual(eligibility["primary_category"], "public_lab")
        self.assertIn("private_practice", eligibility["categories"])
        self.assertTrue(is_session_eligible(public))

    def test_all_36_public_lab_items_remain_sba_eligible(self) -> None:
        public_items = [
            item for item in self.bank["items"] if item["status"]["public_lab"]
        ]
        self.assertEqual(len(public_items), 36)
        self.assertTrue(
            all(
                is_session_eligible(
                    item,
                    suitability=self.suitability[item["master_item_id"]],
                )
                for item in public_items
            )
        )

    def test_strong_open_response_sba_is_excluded_without_explicit_eligibility(self) -> None:
        q14 = next(
            item for item in self.bank["items"] if item["source_question_id"] == "14"
        )
        suitability = self.suitability[q14["master_item_id"]]
        eligibility = classify_master_item(q14, suitability)
        self.assertEqual(eligibility["primary_category"], "open_response_candidate")
        self.assertFalse(eligibility["sba_eligible"])
        self.assertFalse(is_session_eligible(q14, suitability=suitability))

    def test_private_review_item_is_recovered_as_operational_sba(self) -> None:
        q19 = next(
            item for item in self.bank["items"] if item["source_question_id"] == "19"
        )
        suitability = self.suitability[q19["master_item_id"]]
        eligibility = classify_master_item(q19, suitability)
        self.assertEqual(eligibility["primary_category"], "private_practice")
        self.assertTrue(is_session_eligible(q19, suitability=suitability))

    def test_no_operational_inactive_backlog_remains(self) -> None:
        inactive = [
            item
            for item in self.bank["items"]
            if classify_master_item(item)["primary_category"] == "inactive"
        ]
        self.assertEqual(inactive, [])

    def test_open_response_requires_explicit_private_opt_in(self) -> None:
        candidate = next(
            item
            for item in self.bank["items"]
            if classify_master_item(item)["primary_category"]
            == "open_response_candidate"
            and item["question_type"] == "open_response"
        )
        self.assertFalse(is_session_eligible(candidate))
        self.assertTrue(is_session_eligible(candidate, include_open_response=True))

    def test_eligibility_rejects_suitability_coverage_drift(self) -> None:
        incomplete = dict(self.suitability)
        incomplete.pop(next(iter(incomplete)))
        with self.assertRaisesRegex(ValueError, "suitability coverage mismatch"):
            build_eligibility_index(self.bank, incomplete)

    def test_eligibility_governance_is_safe(self) -> None:
        index = build_eligibility_index(self.bank)
        self.assertEqual(index["governance"], SAFE_GOVERNANCE)
        self.assertTrue(
            all(record["governance"] == SAFE_GOVERNANCE for record in index["records"].values())
        )


class FullSessionComposerTests(FullMasterBankFixture):
    def test_all_fixed_modes_generate_requested_size(self) -> None:
        for mode, expected in (
            ("EXPRESS_10", 10),
            ("QUICK_25", 25),
            ("STANDARD_50", 50),
            ("FULL_DIAGNOSTIC", 100),
        ):
            with self.subTest(mode=mode):
                session = compose_master_bank_session(
                    self.bank, DEFAULT_LES, mode=mode, blueprint=self.blueprint
                )
                self.assertEqual(session["item_count"], expected)
                self.assertEqual(len(set(session["master_item_ids"])), expected)

    def test_ra_focus_requires_and_respects_target(self) -> None:
        with self.assertRaises(ValueError):
            compose_master_bank_session(
                self.bank, DEFAULT_LES, mode="RA_FOCUS", blueprint=self.blueprint
            )
        session = compose_master_bank_session(
            self.bank,
            DEFAULT_LES,
            mode="RA_FOCUS",
            target_ra="RA3",
            blueprint=self.blueprint,
        )
        self.assertEqual(session["item_count"], 25)
        self.assertEqual(session["achieved_composition"]["ra"], {"RA3": 25})

    def test_composer_is_deterministic_and_pure(self) -> None:
        bank_before = copy.deepcopy(self.bank)
        les_before = copy.deepcopy(DEFAULT_LES)
        first = compose_master_bank_session(
            self.bank, DEFAULT_LES, mode="STANDARD_50", blueprint=self.blueprint
        )
        second = compose_master_bank_session(
            copy.deepcopy(self.bank),
            copy.deepcopy(DEFAULT_LES),
            mode="STANDARD_50",
            blueprint=copy.deepcopy(self.blueprint),
        )
        self.assertEqual(first, second)
        self.assertEqual(self.bank, bank_before)
        self.assertEqual(DEFAULT_LES, les_before)

    def test_default_composer_uses_private_sba_without_open_response(self) -> None:
        session = compose_master_bank_session(
            self.bank, DEFAULT_LES, mode="STANDARD_50", blueprint=self.blueprint
        )
        self.assertTrue(
            all(item["question_type"] == "single_best_answer" for item in session["items"])
        )
        self.assertTrue(
            all(is_session_eligible(item) for item in session["items"])
        )
        self.assertGreater(session["active_pool_size"], 36)
        self.assertNotIn("wset3_14", session["master_item_ids"])
        self.assertEqual(session["operational_pool_counts"]["sba_operational_pool"], 589)

    def test_full_diagnostic_can_include_open_response_only_when_explicit(self) -> None:
        default = compose_master_bank_session(
            self.bank, DEFAULT_LES, mode="FULL_DIAGNOSTIC", blueprint=self.blueprint
        )
        opted_in = compose_master_bank_session(
            self.bank,
            DEFAULT_LES,
            mode="FULL_DIAGNOSTIC",
            include_open_response=True,
            blueprint=self.blueprint,
        )
        self.assertEqual(
            default["achieved_composition"]["question_types"],
            {"single_best_answer": 100},
        )
        self.assertGreater(
            opted_in["achieved_composition"]["question_types"].get("open_response", 0),
            0,
        )

    def test_recent_and_high_exposure_questions_are_deferred(self) -> None:
        baseline = compose_master_bank_session(
            self.bank, DEFAULT_LES, mode="EXPRESS_10", blueprint=self.blueprint
        )
        les = copy.deepcopy(DEFAULT_LES)
        timestamp = "2026-06-06T12:00:00Z"
        for _ in range(3):
            les = record_session_observations(
                les, baseline, timestamp=timestamp
            )
        replacement = compose_master_bank_session(
            self.bank, les, mode="EXPRESS_10", blueprint=self.blueprint
        )
        self.assertTrue(
            set(baseline["master_item_ids"]).isdisjoint(replacement["master_item_ids"])
        )

    def test_ra_targets_are_met_even_when_difficulty_is_sparse(self) -> None:
        session = compose_master_bank_session(
            self.bank, DEFAULT_LES, mode="EXPRESS_10", blueprint=self.blueprint
        )
        self.assertEqual(
            session["achieved_composition"]["ra"],
            self.blueprint["modes"]["EXPRESS_10"]["ra_distribution"],
        )
        self.assertTrue(
            any(warning.startswith("difficulty_shortfall:") for warning in session["warnings"])
        )

    def test_governance_and_no_examiner_authority(self) -> None:
        session = compose_master_bank_session(
            self.bank, DEFAULT_LES, mode="QUICK_25", blueprint=self.blueprint
        )
        self.assertEqual(session["governance"], SAFE_GOVERNANCE)
        self.assertNotIn("score", _recursive_keys(session))
        self.assertNotIn("grade", _recursive_keys(session))


class LearnerTrackingTests(FullMasterBankFixture):
    def setUp(self) -> None:
        self.session = compose_master_bank_session(
            self.bank,
            DEFAULT_LES,
            mode="EXPRESS_10",
            blueprint=self.blueprint,
        )
        self.timestamp = "2026-06-06T12:00:00Z"

    def test_session_observation_updates_question_topic_and_ra_tracking(self) -> None:
        first_id = self.session["master_item_ids"][0]
        first_topic = self.session["items"][0]["curriculum"]["topic"]
        first_ra = self.session["items"][0]["curriculum"]["ra"]
        updated = record_session_observations(
            DEFAULT_LES,
            self.session,
            timestamp=self.timestamp,
            results={first_id: "correct"},
            topic_confidence={first_topic: "medium"},
            topic_weakness={first_topic: "cleared"},
        )
        question = updated["question_exposure_signals"][first_id]
        self.assertEqual(question["exposure_count"], 1)
        self.assertEqual(question["last_seen"], self.timestamp)
        self.assertEqual(len(question["recent_history"]), 1)
        self.assertGreater(updated["topic_signals"][first_topic]["exposure_count"], 0)
        self.assertEqual(updated["topic_signals"][first_topic]["confidence_level"], "medium")
        self.assertEqual(updated["topic_signals"][first_topic]["weakness_level"], "cleared")
        self.assertGreater(updated["RA_signals"][first_ra]["exposure_count"], 0)
        self.assertEqual(
            updated["RA_signals"][first_ra]["performance"]["correct_count"], 1
        )

    def test_unanswered_exposure_does_not_create_correct_or_incorrect_indicator(self) -> None:
        updated = record_session_observations(
            DEFAULT_LES, self.session, timestamp=self.timestamp
        )
        for ra_signal in updated["RA_signals"].values():
            self.assertEqual(
                ra_signal["performance"], {"correct_count": 0, "incorrect_count": 0}
            )

    def test_tracking_is_persistent_and_governance_clean(self) -> None:
        updated = record_session_observations(
            DEFAULT_LES, self.session, timestamp=self.timestamp
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "les.json"
            write_learner_state(updated, path)
            loaded = load_learner_state(path)
        self.assertEqual(
            loaded["question_exposure_signals"], updated["question_exposure_signals"]
        )
        self.assertFalse(loaded["governance"]["safe_for_examiner"])
        self.assertFalse(loaded["governance"]["examiner_scoring_allowed"])


class DashboardIntegrationDataTests(FullMasterBankFixture):
    def test_dashboard_projection_contains_required_metrics(self) -> None:
        session = compose_master_bank_session(
            self.bank, DEFAULT_LES, mode="EXPRESS_10", blueprint=self.blueprint
        )
        les = record_session_observations(
            DEFAULT_LES, session, timestamp="2026-06-06T12:00:00Z"
        )
        data = build_master_bank_utilization_data(self.bank, les, session)
        self.assertEqual(data["bank"]["total_bank_size"], 616)
        self.assertEqual(data["bank"]["active_pool"], 589)
        self.assertEqual(data["bank"]["total_master_bank"], 616)
        self.assertEqual(data["bank"]["sba_operational_pool"], 589)
        self.assertEqual(data["bank"]["open_response_candidate_pool"], 27)
        self.assertEqual(data["bank"]["open_response_review_pool"], 0)
        self.assertEqual(data["bank"]["inactive"], 0)
        self.assertEqual(data["bank"]["public_lab"], 36)
        self.assertEqual(data["session_composition"]["item_count"], 10)
        self.assertEqual(set(data["ra_coverage"]), set(DEFAULT_LES["RA_signals"]))
        self.assertTrue(data["topic_coverage"])
        self.assertEqual(data["exposure_statistics"]["total_exposures"], 10)
        self.assertEqual(data["governance"], SAFE_GOVERNANCE)

    def test_dashboard_projection_is_pure(self) -> None:
        bank = copy.deepcopy(self.bank)
        les = copy.deepcopy(DEFAULT_LES)
        before_bank = copy.deepcopy(bank)
        before_les = copy.deepcopy(les)
        build_master_bank_utilization_data(bank, les)
        self.assertEqual(bank, before_bank)
        self.assertEqual(les, before_les)


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
