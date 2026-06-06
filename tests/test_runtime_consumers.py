"""Tests for Phase 4A.3.8.7 Runtime Consumers.

Covers four components:
  - tools/learner_model/misconception_runtime.py
  - tools/learner_model/causal_runtime.py
  - tools/learner_model/wwj_remediation.py
  - tools/learner_model/open_response_evaluator.py

All tests are deterministic, use no LLM/API/cloud services, and integrate with
the main test suite (python -m unittest discover -s tests -v).
"""

from __future__ import annotations

import unittest
from copy import deepcopy

from tools.learner_model.misconception_runtime import (
    known_mc_ids,
    process_sba_outcome,
    SIGNAL_TRIGGERED,
    SIGNAL_RESOLVED,
    SIGNAL_PERSISTENT,
)
from tools.learner_model.causal_runtime import (
    detect_cc_coverage,
    get_keyword_hints,
    known_cc_ids,
    update_les_causal,
    SIGNAL_DEMONSTRATED,
    SIGNAL_GAP,
    SIGNAL_STRENGTH_UPDATED,
)
from tools.learner_model.wwj_remediation import get_remediation_path
from tools.learner_model.open_response_evaluator import (
    evaluate_open_response,
    PROFILE_FOUNDATIONAL,
    PROFILE_DEVELOPING,
    PROFILE_STRONG,
)
from tools.orchestrator.learner_state import DEFAULT_LES


def _fresh_les() -> dict:
    return deepcopy(DEFAULT_LES)


# ---------------------------------------------------------------------------
# A. Misconception Runtime Consumer
# ---------------------------------------------------------------------------

class TestMisconcepRuntimeKnownIds(unittest.TestCase):

    def test_known_ids_nonempty(self):
        ids = known_mc_ids()
        self.assertGreater(len(ids), 0)

    def test_sample_ids_present(self):
        ids = known_mc_ids()
        self.assertIn("MC_ACIDITY_01", ids)
        self.assertIn("MC_MLF_01", ids)
        self.assertIn("MC_TANNIN_01", ids)


class TestMisconcepRuntimeTrigger(unittest.TestCase):

    def test_incorrect_emits_triggered_signal(self):
        les = _fresh_les()
        _, signals = process_sba_outcome(
            les, mc_id="MC_ACIDITY_01", outcome="incorrect", session_id="session_1"
        )
        self.assertIn(SIGNAL_TRIGGERED, signals)

    def test_incorrect_increments_detection_count(self):
        les = _fresh_les()
        updated, _ = process_sba_outcome(
            les, mc_id="MC_ACIDITY_01", outcome="incorrect", session_id="session_1"
        )
        self.assertEqual(
            updated["misconception_signals"]["MC_ACIDITY_01"]["detection_count"], 1
        )

    def test_two_incorrect_same_session_no_persistence(self):
        les = _fresh_les()
        updated, _ = process_sba_outcome(
            les, mc_id="MC_ACIDITY_01", outcome="incorrect", session_id="session_1"
        )
        _, signals = process_sba_outcome(
            updated, mc_id="MC_ACIDITY_01", outcome="incorrect", session_id="session_1"
        )
        self.assertNotIn(SIGNAL_PERSISTENT, signals)

    def test_incorrect_in_two_distinct_sessions_emits_persistent(self):
        les = _fresh_les()
        updated, _ = process_sba_outcome(
            les, mc_id="MC_ACIDITY_01", outcome="incorrect", session_id="session_1"
        )
        _, signals = process_sba_outcome(
            updated, mc_id="MC_ACIDITY_01", outcome="incorrect", session_id="session_2"
        )
        self.assertIn(SIGNAL_PERSISTENT, signals)

    def test_correct_after_incorrect_emits_resolved(self):
        les = _fresh_les()
        updated, _ = process_sba_outcome(
            les, mc_id="MC_ACIDITY_01", outcome="incorrect", session_id="session_1"
        )
        _, signals = process_sba_outcome(
            updated, mc_id="MC_ACIDITY_01", outcome="correct", session_id="session_2"
        )
        self.assertIn(SIGNAL_RESOLVED, signals)

    def test_correct_with_no_prior_incorrect_no_resolved_signal(self):
        les = _fresh_les()
        _, signals = process_sba_outcome(
            les, mc_id="MC_ACIDITY_01", outcome="correct", session_id="session_1"
        )
        self.assertNotIn(SIGNAL_RESOLVED, signals)
        self.assertEqual(signals, [])

    def test_unknown_mc_id_returns_empty_signals(self):
        les = _fresh_les()
        _, signals = process_sba_outcome(
            les, mc_id="MC_NONEXISTENT_99", outcome="incorrect", session_id="session_1"
        )
        self.assertEqual(signals, [])

    def test_unknown_mc_id_returns_original_les_object(self):
        les = _fresh_les()
        updated, _ = process_sba_outcome(
            les, mc_id="MC_NONEXISTENT_99", outcome="incorrect", session_id="session_1"
        )
        self.assertIs(updated, les)

    def test_original_les_not_mutated(self):
        les = _fresh_les()
        original_count = (
            les.get("misconception_signals", {})
            .get("MC_ACIDITY_01", {})
            .get("detection_count", 0)
        )
        process_sba_outcome(
            les, mc_id="MC_ACIDITY_01", outcome="incorrect", session_id="s1"
        )
        after_count = (
            les.get("misconception_signals", {})
            .get("MC_ACIDITY_01", {})
            .get("detection_count", 0)
        )
        self.assertEqual(original_count, after_count)

    def test_resolution_recorded_in_les(self):
        les = _fresh_les()
        updated, _ = process_sba_outcome(
            les, mc_id="MC_ACIDITY_01", outcome="incorrect", session_id="s1"
        )
        updated, _ = process_sba_outcome(
            updated, mc_id="MC_ACIDITY_01", outcome="correct", session_id="s2"
        )
        res = updated.get("misconception_resolution", {}).get("MC_ACIDITY_01", {})
        self.assertTrue(res.get("resolved"))
        self.assertIsNotNone(res.get("resolved_at"))

    def test_governance_flags_always_false(self):
        les = _fresh_les()
        updated, _ = process_sba_outcome(
            les, mc_id="MC_ACIDITY_01", outcome="incorrect", session_id="s1"
        )
        gov = updated.get("governance", {})
        self.assertFalse(gov.get("safe_for_examiner", True))
        self.assertFalse(gov.get("examiner_scoring_allowed", True))


# ---------------------------------------------------------------------------
# B. Causal Chain Runtime Consumer
# ---------------------------------------------------------------------------

class TestCausalRuntimeKnownIds(unittest.TestCase):

    def test_known_cc_ids_nonempty(self):
        ids = known_cc_ids()
        self.assertGreater(len(ids), 0)

    def test_sample_ids_present(self):
        ids = known_cc_ids()
        self.assertIn("CC_MLF_ACIDITY", ids)
        self.assertIn("CC_OAK_TANNIN", ids)
        self.assertIn("CC_COOL_CLIMATE_ACIDITY", ids)


class TestCausalRuntimeKeywordHints(unittest.TestCase):

    def test_governance_schema_returns_trigger_keywords(self):
        hints = get_keyword_hints("CC_COOL_CLIMATE_ACIDITY")
        # Should use trigger_keywords from the hybrid JSON file
        self.assertIsInstance(hints, list)
        self.assertGreater(len(hints), 0)

    def test_legacy_schema_derives_from_id(self):
        hints = get_keyword_hints("CC_OAK_TANNIN")
        self.assertIn("oak", hints)
        self.assertIn("tannin", hints)

    def test_mlf_hints_include_malolactic(self):
        hints = get_keyword_hints("CC_MLF_ACIDITY")
        self.assertIn("malolactic", hints)


class TestCausalRuntimeDetection(unittest.TestCase):

    def test_mlf_detected_in_relevant_response(self):
        response = "During malolactic fermentation, malic acid is converted to lactic acid."
        present, absent = detect_cc_coverage(response, ["CC_MLF_ACIDITY"])
        self.assertIn("CC_MLF_ACIDITY", present)
        self.assertNotIn("CC_MLF_ACIDITY", absent)

    def test_unrelated_response_produces_gap(self):
        response = "The wine is stored in stainless steel tanks at low temperature."
        present, absent = detect_cc_coverage(response, ["CC_MLF_ACIDITY"])
        self.assertIn("CC_MLF_ACIDITY", absent)
        self.assertNotIn("CC_MLF_ACIDITY", present)

    def test_empty_targeted_list_returns_empty(self):
        present, absent = detect_cc_coverage("any response", [])
        self.assertEqual(present, [])
        self.assertEqual(absent, [])

    def test_cool_climate_acidity_detected(self):
        response = "Cool climate regions retain higher acidity and lower alcohol."
        present, _ = detect_cc_coverage(response, ["CC_COOL_CLIMATE_ACIDITY"])
        self.assertIn("CC_COOL_CLIMATE_ACIDITY", present)

    def test_oak_tannin_detected(self):
        response = "New oak barrels contribute tannin and vanilla character to the wine."
        present, _ = detect_cc_coverage(response, ["CC_OAK_TANNIN"])
        self.assertIn("CC_OAK_TANNIN", present)

    def test_multiple_targets_partial_match(self):
        response = "Malolactic fermentation converts malic acid to lactic acid."
        present, absent = detect_cc_coverage(
            response, ["CC_MLF_ACIDITY", "CC_OAK_TANNIN"]
        )
        self.assertIn("CC_MLF_ACIDITY", present)
        self.assertIn("CC_OAK_TANNIN", absent)


class TestCausalRuntimeLesUpdate(unittest.TestCase):

    def test_exposure_count_incremented(self):
        les = _fresh_les()
        updated, _ = update_les_causal(
            les, cc_ids_targeted=["CC_MLF_ACIDITY"], chains_present=[]
        )
        self.assertEqual(
            updated["causal_chain_signals"]["CC_MLF_ACIDITY"]["exposure_count"], 1
        )

    def test_demonstrated_count_incremented_when_present(self):
        les = _fresh_les()
        updated, signals = update_les_causal(
            les,
            cc_ids_targeted=["CC_MLF_ACIDITY"],
            chains_present=["CC_MLF_ACIDITY"],
        )
        self.assertEqual(
            updated["causal_chain_signals"]["CC_MLF_ACIDITY"]["demonstrated_count"], 1
        )
        self.assertIn(SIGNAL_DEMONSTRATED, signals)

    def test_gap_signal_emitted_when_absent(self):
        les = _fresh_les()
        _, signals = update_les_causal(
            les, cc_ids_targeted=["CC_MLF_ACIDITY"], chains_present=[]
        )
        self.assertIn(SIGNAL_GAP, signals)

    def test_causal_strength_key_set(self):
        les = _fresh_les()
        updated, _ = update_les_causal(
            les, cc_ids_targeted=["CC_MLF_ACIDITY"], chains_present=[]
        )
        self.assertIn("causal_strength", updated)
        self.assertIn("CC_MLF_ACIDITY", updated["causal_strength"])

    def test_strength_becomes_strong_with_consistent_demonstration(self):
        les = _fresh_les()
        for _ in range(5):
            les, _ = update_les_causal(
                les,
                cc_ids_targeted=["CC_OAK_FLAVOUR"],
                chains_present=["CC_OAK_FLAVOUR"],
            )
        self.assertEqual(les["causal_strength"]["CC_OAK_FLAVOUR"], "strong")

    def test_strength_stays_superficial_with_zero_demonstration(self):
        les = _fresh_les()
        for _ in range(3):
            les, _ = update_les_causal(
                les, cc_ids_targeted=["CC_MLF_ACIDITY"], chains_present=[]
            )
        self.assertEqual(les["causal_strength"]["CC_MLF_ACIDITY"], "superficial")

    def test_strength_updated_signal_emitted_on_change(self):
        les = _fresh_les()
        _, signals = update_les_causal(
            les, cc_ids_targeted=["CC_MLF_ACIDITY"], chains_present=[]
        )
        self.assertIn(SIGNAL_STRENGTH_UPDATED, signals)

    def test_original_les_not_mutated(self):
        les = _fresh_les()
        original = deepcopy(les)
        update_les_causal(les, cc_ids_targeted=["CC_MLF_ACIDITY"], chains_present=[])
        self.assertEqual(les, original)

    def test_unknown_cc_id_silently_ignored(self):
        les = _fresh_les()
        updated, signals = update_les_causal(
            les, cc_ids_targeted=["CC_NONEXISTENT_99"], chains_present=[]
        )
        self.assertNotIn("CC_NONEXISTENT_99", updated.get("causal_chain_signals", {}))
        self.assertEqual(signals, [])


# ---------------------------------------------------------------------------
# C. WWJ Remediation Runtime
# ---------------------------------------------------------------------------

class TestWwjRemediation(unittest.TestCase):

    def test_known_available_mc_id_returns_chunks(self):
        path = get_remediation_path("MC_ACIDITY_01")
        self.assertEqual(path["mc_id"], "MC_ACIDITY_01")
        self.assertEqual(path["availability"], "available")
        self.assertIsInstance(path["wwj_chunks"], list)
        self.assertGreater(len(path["wwj_chunks"]), 0)

    def test_known_pending_mc_id_returns_empty_chunks(self):
        path = get_remediation_path("MC_WHOLE_BUNCH_01")
        self.assertEqual(path["mc_id"], "MC_WHOLE_BUNCH_01")
        self.assertEqual(path["availability"], "pending")
        self.assertEqual(path["wwj_chunks"], [])

    def test_unknown_mc_id_returns_pending(self):
        path = get_remediation_path("MC_NONEXISTENT_ZZZZZ")
        self.assertEqual(path["availability"], "pending")
        self.assertEqual(path["wwj_chunks"], [])

    def test_remediation_message_is_nonempty_string(self):
        path = get_remediation_path("MC_ACIDITY_01")
        self.assertIsInstance(path["remediation_message"], str)
        self.assertGreater(len(path["remediation_message"]), 0)

    def test_pending_mc_remediation_message_nonempty(self):
        path = get_remediation_path("MC_NONEXISTENT_ZZZZZ")
        self.assertIsInstance(path["remediation_message"], str)
        self.assertGreater(len(path["remediation_message"]), 0)

    def test_content_type_returned_for_available(self):
        path = get_remediation_path("MC_ACIDITY_01")
        self.assertIsNotNone(path["content_type"])

    def test_content_type_none_for_unknown(self):
        path = get_remediation_path("MC_NONEXISTENT_ZZZZZ")
        self.assertIsNone(path["content_type"])

    def test_output_does_not_contain_safe_for_examiner(self):
        path = get_remediation_path("MC_ACIDITY_01")
        self.assertNotIn("safe_for_examiner", path)

    def test_chunk_ids_are_strings(self):
        path = get_remediation_path("MC_MLF_01")
        for chunk in path["wwj_chunks"]:
            self.assertIsInstance(chunk, str)
            self.assertTrue(chunk.strip())

    def test_partial_availability_message_differs(self):
        path_partial = get_remediation_path("MC_LEES_AGEING_01")
        self.assertEqual(path_partial["availability"], "partial")
        self.assertIn("partial", path_partial["remediation_message"].lower())


# ---------------------------------------------------------------------------
# D. Open Response Evaluator v1
# ---------------------------------------------------------------------------

class TestOpenResponseEvaluatorProfiles(unittest.TestCase):

    def _ctx(self, cc_ids=None, mc_ids=None):
        return {
            "cc_ids_targeted": cc_ids or [],
            "mc_ids_relevant": mc_ids or [],
            "topic": "malolactic_fermentation",
            "ra_id": "RA2",
        }

    def test_strong_response_classified_correctly(self):
        response = (
            "Malolactic fermentation converts malic acid to lactic acid through "
            "bacterial action. Cool climate wines retain high acidity. "
            "New oak barrels add tannin and vanilla character."
        )
        ctx = self._ctx(
            cc_ids=["CC_MLF_ACIDITY", "CC_COOL_CLIMATE_ACIDITY", "CC_OAK_TANNIN"]
        )
        result = evaluate_open_response(response, ctx)
        self.assertEqual(result["profile"], PROFILE_STRONG)
        self.assertEqual(result["reasoning_quality"], "strong")

    def test_foundational_response_classified_correctly(self):
        response = "The wine is red and tastes nice with some fruit."
        ctx = self._ctx(
            cc_ids=["CC_MLF_ACIDITY", "CC_COOL_CLIMATE_ACIDITY", "CC_OAK_TANNIN"]
        )
        result = evaluate_open_response(response, ctx)
        self.assertEqual(result["profile"], PROFILE_FOUNDATIONAL)
        self.assertEqual(result["reasoning_quality"], "superficial")

    def test_developing_response_classified_correctly(self):
        # Hits 2 out of 3 targeted CC_IDs
        response = (
            "Malolactic fermentation changes the malic acid in the wine. "
            "Cool climate helps retain acidity."
        )
        ctx = self._ctx(
            cc_ids=["CC_MLF_ACIDITY", "CC_COOL_CLIMATE_ACIDITY", "CC_OAK_TANNIN"]
        )
        result = evaluate_open_response(response, ctx)
        # 2/3 = 0.667 → DEVELOPING
        self.assertEqual(result["profile"], PROFILE_DEVELOPING)


class TestOpenResponseEvaluatorOutput(unittest.TestCase):

    def _ctx(self, cc_ids=None, mc_ids=None):
        return {
            "cc_ids_targeted": cc_ids or [],
            "mc_ids_relevant": mc_ids or [],
            "topic": "test",
            "ra_id": "RA1",
        }

    def test_output_schema_has_all_required_keys(self):
        result = evaluate_open_response("any text", self._ctx())
        for key in (
            "profile",
            "concept_coverage",
            "causal_coverage",
            "reasoning_quality",
            "remediation",
            "governance",
        ):
            self.assertIn(key, result)

    def test_governance_always_false(self):
        result = evaluate_open_response("any text", self._ctx())
        gov = result["governance"]
        self.assertFalse(gov["safe_for_examiner"])
        self.assertFalse(gov["examiner_scoring_allowed"])
        self.assertFalse(gov["official_wset_question"])
        self.assertTrue(gov["training_item_only"])

    def test_wwj_chunks_populated_from_lookup(self):
        response = "MLF converts malic to lactic acid."
        ctx = self._ctx(cc_ids=["CC_MLF_ACIDITY"], mc_ids=["MC_MLF_02"])
        result = evaluate_open_response(response, ctx)
        self.assertIsInstance(result["remediation"]["wwj_chunks"], list)
        self.assertGreater(len(result["remediation"]["wwj_chunks"]), 0)

    def test_wwj_chunks_deduplicated(self):
        # Two MC_IDs that share WWJ chunk IDs should not produce duplicates
        ctx = self._ctx(cc_ids=[], mc_ids=["MC_MLF_01", "MC_MLF_02"])
        result = evaluate_open_response("", ctx)
        chunks = result["remediation"]["wwj_chunks"]
        self.assertEqual(len(chunks), len(set(chunks)))

    def test_no_forbidden_profile_strings_in_output(self):
        response = "MLF converts malic acid to lactic acid."
        ctx = self._ctx(cc_ids=["CC_MLF_ACIDITY"], mc_ids=[])
        result = evaluate_open_response(response, ctx)
        result_str = str(result)
        for forbidden in ("WSET_PASS", "WSET_MERIT", "WSET_DISTINCTION"):
            self.assertNotIn(forbidden, result_str)

    def test_empty_response_and_context_no_crash(self):
        result = evaluate_open_response("", {})
        self.assertIn("profile", result)
        self.assertEqual(result["profile"], PROFILE_FOUNDATIONAL)

    def test_present_chains_in_concept_coverage(self):
        response = "Malolactic fermentation converts malic to lactic acid."
        ctx = self._ctx(cc_ids=["CC_MLF_ACIDITY"])
        result = evaluate_open_response(response, ctx)
        self.assertIn("CC_MLF_ACIDITY", result["concept_coverage"]["concepts_present"])

    def test_absent_chains_in_remediation(self):
        response = "The wine is aged in stainless steel."
        ctx = self._ctx(cc_ids=["CC_MLF_ACIDITY"])
        result = evaluate_open_response(response, ctx)
        self.assertIn("CC_MLF_ACIDITY", result["remediation"]["concepts_to_reinforce"])


if __name__ == "__main__":
    unittest.main()
