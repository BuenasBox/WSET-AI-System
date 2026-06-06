"""Tests for Phase 4A.3.9.2 — Learning Event Runtime Integration.

Verifies three integration connections:
  1. _remediation_route() -> wwj_remediation.get_remediation_path()
  2. build_next_session_signals() reads LES real signals (not just memory)
  3. process_open_response_attempt() connects evaluate_open_response() to LES/cognitive_map

All tests are deterministic, governance-clean, no LLM/API/cloud services.
Run with: python -m unittest tests.test_learning_event_runtime_integration -v
"""

from __future__ import annotations

import unittest
from copy import deepcopy

from tools.learner_model.learning_event_runtime import (
    build_diagnostic_outcome,
    build_next_session_signals,
    process_open_response_attempt,
    process_question_attempt,
)
from tools.learner_model.misconception_runtime import process_sba_outcome
from tools.learner_model.causal_runtime import update_les_causal
from tools.learner_model.open_response_evaluator import (
    PROFILE_FOUNDATIONAL,
    PROFILE_DEVELOPING,
    PROFILE_STRONG,
)
from tools.orchestrator.learner_state import DEFAULT_LES
from tools.learner_model.knowledge_tracing import DEFAULT_PEDAGOGICAL_MEMORY


FORBIDDEN_STRINGS = ("WSET_PASS", "WSET_MERIT", "WSET_DISTINCTION", "score", "percentage", "pass_fail")

_MC_AVAILABLE = "MC_ACIDITY_01"   # availability="available" in mc_wwj_lookup.json
_MC_PENDING = "MC_WHOLE_BUNCH_01"  # availability="pending"

_CC_MLF = "CC_MLF_ACIDITY"
_CC_OAK = "CC_OAK_TANNIN"
_CC_COOL = "CC_COOL_CLIMATE_ACIDITY"

_SAMPLE_SBA_ITEM = {
    "correct_answer": "A",
    "stem": "Which acid is reduced during MLF?",
    "ra_id": "RA1",
}

_SAMPLE_OR_ITEM = {
    "item_id": "OR_002",
    "question_text": "Explain MLF.",
    "ra_id": "RA1",
    "topic": "fermentación maloláctica",
    "causal_chain_target": [_CC_MLF, _CC_OAK],
    "mc_ids_relevant": [],
}

_OR_ITEM_WITH_MC = {
    **_SAMPLE_OR_ITEM,
    "mc_ids_relevant": [_MC_AVAILABLE],
}


def _fresh_les() -> dict:
    return deepcopy(DEFAULT_LES)


def _fresh_memory() -> dict:
    return deepcopy(DEFAULT_PEDAGOGICAL_MEMORY)


# ---------------------------------------------------------------------------
# 1. WWJ Remediation in SBA Outcome
# ---------------------------------------------------------------------------

class TestWwjRemediationInSbaOutcome(unittest.TestCase):
    """SBA wrong answer with mc_id => wwj_chunks from the lookup."""

    def test_wrong_answer_with_available_mc_id_produces_wwj_chunks(self):
        result = process_question_attempt(
            student_answer="B",
            question_id="q1",
            session_id="s1",
            mode="practice",
            timestamp="2026-06-06T10:00:00Z",
            question_item=_SAMPLE_SBA_ITEM,
            memory=_fresh_memory(),
            les=_fresh_les(),
            mc_id=_MC_AVAILABLE,
        )
        routing = result["diagnostic_outcome"]["remediation_routing"]
        self.assertIsNotNone(routing)
        self.assertTrue(routing["remediation_available"])
        self.assertIsInstance(routing["wwj_chunks"], list)
        self.assertGreater(len(routing["wwj_chunks"]), 0)

    def test_remediation_source_is_wwj_lookup(self):
        result = process_question_attempt(
            student_answer="B",
            question_id="q1",
            session_id="s1",
            mode="practice",
            timestamp="2026-06-06T10:00:00Z",
            question_item=_SAMPLE_SBA_ITEM,
            memory=_fresh_memory(),
            les=_fresh_les(),
            mc_id=_MC_AVAILABLE,
        )
        self.assertEqual(
            result["diagnostic_outcome"]["remediation_routing"]["remediation_source"],
            "wwj_lookup",
        )

    def test_pending_mc_id_produces_empty_chunks(self):
        result = process_question_attempt(
            student_answer="B",
            question_id="q1",
            session_id="s1",
            mode="practice",
            timestamp="2026-06-06T10:00:00Z",
            question_item=_SAMPLE_SBA_ITEM,
            memory=_fresh_memory(),
            les=_fresh_les(),
            mc_id=_MC_PENDING,
        )
        routing = result["diagnostic_outcome"]["remediation_routing"]
        self.assertFalse(routing["remediation_available"])
        self.assertEqual(routing["wwj_chunks"], [])

    def test_correct_answer_no_wwj_chunks(self):
        result = process_question_attempt(
            student_answer="A",
            question_id="q1",
            session_id="s1",
            mode="practice",
            timestamp="2026-06-06T10:00:00Z",
            question_item=_SAMPLE_SBA_ITEM,
            memory=_fresh_memory(),
            les=_fresh_les(),
            mc_id=_MC_AVAILABLE,
        )
        routing = result["diagnostic_outcome"]["remediation_routing"]
        self.assertIsNotNone(routing)
        self.assertFalse(routing["remediation_available"])
        self.assertEqual(routing["wwj_chunks"], [])
        self.assertEqual(routing["remediation_source"], "none")

    def test_no_mc_id_remediation_routing_is_none(self):
        result = process_question_attempt(
            student_answer="B",
            question_id="q1",
            session_id="s1",
            mode="practice",
            timestamp="2026-06-06T10:00:00Z",
            question_item=_SAMPLE_SBA_ITEM,
            memory=_fresh_memory(),
            les=_fresh_les(),
        )
        self.assertIsNone(result["diagnostic_outcome"]["remediation_routing"])

    def test_remediation_message_is_nonempty_for_available(self):
        result = process_question_attempt(
            student_answer="B",
            question_id="q1",
            session_id="s1",
            mode="practice",
            timestamp="2026-06-06T10:00:00Z",
            question_item=_SAMPLE_SBA_ITEM,
            memory=_fresh_memory(),
            les=_fresh_les(),
            mc_id=_MC_AVAILABLE,
        )
        msg = result["diagnostic_outcome"]["remediation_routing"]["remediation_message"]
        self.assertIsInstance(msg, str)
        self.assertGreater(len(msg), 0)


# ---------------------------------------------------------------------------
# 2. Next Session Signals read LES (not just memory)
# ---------------------------------------------------------------------------

class TestNextSessionSignalsReadLes(unittest.TestCase):
    """build_next_session_signals() must expose LES persistence and causal_strength."""

    def _les_with_persistent_mc(self, mc_id: str = _MC_AVAILABLE) -> dict:
        les = _fresh_les()
        les, _ = process_sba_outcome(
            les, mc_id=mc_id, outcome="incorrect", session_id="session_A"
        )
        les, _ = process_sba_outcome(
            les, mc_id=mc_id, outcome="incorrect", session_id="session_B"
        )
        return les

    def _les_with_resolved_mc(self, mc_id: str = _MC_AVAILABLE) -> dict:
        les = _fresh_les()
        les, _ = process_sba_outcome(
            les, mc_id=mc_id, outcome="incorrect", session_id="session_A"
        )
        les, _ = process_sba_outcome(
            les, mc_id=mc_id, outcome="correct", session_id="session_B"
        )
        return les

    def _les_with_cc_signals(self, cc_id: str = _CC_MLF, strength: str = "developing") -> dict:
        les = _fresh_les()
        # update_les_causal to put a signal into LES
        les, _ = update_les_causal(
            les,
            cc_ids_targeted=[cc_id],
            chains_present=[cc_id] if strength != "superficial" else [],
        )
        if strength == "strong":
            # make it strong: 5 demonstrated out of 5 exposed
            for _ in range(4):
                les, _ = update_les_causal(
                    les, cc_ids_targeted=[cc_id], chains_present=[cc_id]
                )
        return les

    def test_mc_in_two_sessions_persistence_true(self):
        les = self._les_with_persistent_mc()
        signals = build_next_session_signals(_fresh_memory(), les)
        repair = signals["misconception_repair_candidate"]
        mc_entry = next((r for r in repair if r["mc_id"] == _MC_AVAILABLE), None)
        self.assertIsNotNone(mc_entry)
        self.assertTrue(mc_entry["persistence"])

    def test_mc_in_one_session_persistence_false(self):
        les = _fresh_les()
        les, _ = process_sba_outcome(
            les, mc_id=_MC_AVAILABLE, outcome="incorrect", session_id="session_A"
        )
        signals = build_next_session_signals(_fresh_memory(), les)
        repair = signals["misconception_repair_candidate"]
        mc_entry = next((r for r in repair if r["mc_id"] == _MC_AVAILABLE), None)
        self.assertIsNotNone(mc_entry)
        self.assertFalse(mc_entry["persistence"])

    def test_resolved_mc_not_in_repair_candidates(self):
        les = self._les_with_resolved_mc()
        signals = build_next_session_signals(_fresh_memory(), les)
        mc_ids_in_candidates = [r["mc_id"] for r in signals["misconception_repair_candidate"]]
        self.assertNotIn(_MC_AVAILABLE, mc_ids_in_candidates)

    def test_resolved_mc_has_resolved_true_in_les(self):
        les = self._les_with_resolved_mc()
        res = les.get("misconception_resolution", {}).get(_MC_AVAILABLE, {})
        self.assertTrue(res.get("resolved"))

    def test_persistent_unresolved_mc_priority_high(self):
        les = self._les_with_persistent_mc()
        signals = build_next_session_signals(_fresh_memory(), les)
        repair = signals["misconception_repair_candidate"]
        mc_entry = next((r for r in repair if r["mc_id"] == _MC_AVAILABLE), None)
        self.assertIsNotNone(mc_entry)
        self.assertEqual(mc_entry["priority"], "high")

    def test_non_persistent_unresolved_mc_priority_standard(self):
        les = _fresh_les()
        les, _ = process_sba_outcome(
            les, mc_id=_MC_AVAILABLE, outcome="incorrect", session_id="session_A"
        )
        signals = build_next_session_signals(_fresh_memory(), les)
        repair = signals["misconception_repair_candidate"]
        mc_entry = next((r for r in repair if r["mc_id"] == _MC_AVAILABLE), None)
        self.assertIsNotNone(mc_entry)
        self.assertEqual(mc_entry["priority"], "standard")

    def test_causal_strength_appears_in_reinforcement_candidates(self):
        les = self._les_with_cc_signals(_CC_MLF, strength="superficial")
        signals = build_next_session_signals(_fresh_memory(), les)
        cc_candidates = signals["causal_chain_reinforcement_candidate"]
        cc_entry = next((c for c in cc_candidates if c["cc_id"] == _CC_MLF), None)
        self.assertIsNotNone(cc_entry)
        self.assertIn("causal_strength", cc_entry)
        self.assertEqual(cc_entry["causal_strength"], "superficial")

    def test_superficial_causal_strength_gap_priority_high(self):
        les = self._les_with_cc_signals(_CC_MLF, strength="superficial")
        signals = build_next_session_signals(_fresh_memory(), les)
        cc_entry = next(
            (c for c in signals["causal_chain_reinforcement_candidate"] if c["cc_id"] == _CC_MLF),
            None,
        )
        self.assertIsNotNone(cc_entry)
        self.assertEqual(cc_entry["gap_priority"], "high")

    def test_strong_causal_strength_gap_priority_standard(self):
        les = self._les_with_cc_signals(_CC_MLF, strength="strong")
        signals = build_next_session_signals(_fresh_memory(), les)
        cc_entry = next(
            (c for c in signals["causal_chain_reinforcement_candidate"] if c["cc_id"] == _CC_MLF),
            None,
        )
        self.assertIsNotNone(cc_entry)
        self.assertEqual(cc_entry["gap_priority"], "standard")

    def test_no_exposure_cc_not_in_candidates(self):
        les = _fresh_les()
        signals = build_next_session_signals(_fresh_memory(), les)
        # Fresh LES has no causal_chain_signals, so no candidates
        self.assertEqual(signals["causal_chain_reinforcement_candidate"], [])

    def test_empty_les_returns_empty_candidates(self):
        signals = build_next_session_signals(_fresh_memory(), _fresh_les())
        self.assertEqual(signals["misconception_repair_candidate"], [])
        self.assertEqual(signals["causal_chain_reinforcement_candidate"], [])


# ---------------------------------------------------------------------------
# 3. process_open_response_attempt
# ---------------------------------------------------------------------------

class TestOpenResponseAttemptCallsEvaluator(unittest.TestCase):
    """OR attempt must call evaluate_open_response internally."""

    def _run_mlf_attempt(self, response: str) -> dict:
        return process_open_response_attempt(
            student_response_text=response,
            question_id="OR_002",
            session_id="s1",
            mode="practice",
            timestamp="2026-06-06T10:00:00Z",
            or_item=_SAMPLE_OR_ITEM,
            memory=_fresh_memory(),
            les=_fresh_les(),
        )

    def test_strong_response_produces_strong_profile(self):
        response = (
            "Malolactic fermentation converts malic acid to lactic acid through bacterial action. "
            "New oak barrels contribute tannin and structure to the wine."
        )
        result = self._run_mlf_attempt(response)
        self.assertEqual(result["diagnostic_outcome"]["profile"], PROFILE_STRONG)

    def test_foundational_response_produces_foundational_profile(self):
        result = self._run_mlf_attempt("The wine is nice and fruity.")
        self.assertEqual(result["diagnostic_outcome"]["profile"], PROFILE_FOUNDATIONAL)

    def test_output_contains_chains_present_and_absent(self):
        result = self._run_mlf_attempt("Malolactic fermentation converts malic to lactic.")
        diag = result["diagnostic_outcome"]
        self.assertIn("chains_present", diag)
        self.assertIn("chains_absent", diag)
        self.assertIn(_CC_MLF, diag["chains_present"])

    def test_formative_event_type_is_open_response(self):
        result = self._run_mlf_attempt("some response")
        self.assertEqual(result["formative_event"]["event_type"], "open_response_attempt")


class TestOpenResponseLesUpdate(unittest.TestCase):
    """OR attempt must update LES causal_chain_signals and memory.difficult_causal_chains."""

    def test_chain_absent_updates_les_causal_chain_signals(self):
        # Response that does NOT mention oak/tannin
        response = "Malolactic fermentation converts malic to lactic acid through bacteria."
        result = process_open_response_attempt(
            student_response_text=response,
            question_id="OR_002",
            session_id="s1",
            mode="practice",
            timestamp="2026-06-06T10:00:00Z",
            or_item=_SAMPLE_OR_ITEM,
            memory=_fresh_memory(),
            les=_fresh_les(),
        )
        # CC_OAK_TANNIN should be absent → LES should record exposure
        les = result["les"]
        cc_signals = les.get("causal_chain_signals", {})
        # At least CC_MLF_ACIDITY should be recorded
        self.assertIn(_CC_MLF, cc_signals)
        self.assertGreaterEqual(cc_signals[_CC_MLF]["exposure_count"], 1)

    def test_chain_absent_updates_memory_difficult_causal_chains(self):
        # Response that mentions nothing relevant
        response = "The wine is stored in stainless steel."
        result = process_open_response_attempt(
            student_response_text=response,
            question_id="OR_002",
            session_id="s1",
            mode="practice",
            timestamp="2026-06-06T10:00:00Z",
            or_item=_SAMPLE_OR_ITEM,
            memory=_fresh_memory(),
            les=_fresh_les(),
        )
        diff_cc = result["cognitive_map"].get("difficult_causal_chains", {})
        # Both CC_MLF and CC_OAK are targeted; at least one should be absent
        self.assertGreater(len(diff_cc), 0)

    def test_chain_present_does_not_add_to_difficult_chains(self):
        # Strong response that covers both targeted chains
        response = (
            "Malolactic fermentation converts malic acid to lactic acid. "
            "New oak barrels add tannin and vanilla."
        )
        result = process_open_response_attempt(
            student_response_text=response,
            question_id="OR_002",
            session_id="s1",
            mode="practice",
            timestamp="2026-06-06T10:00:00Z",
            or_item=_SAMPLE_OR_ITEM,
            memory=_fresh_memory(),
            les=_fresh_les(),
        )
        diff_cc = result["cognitive_map"].get("difficult_causal_chains", {})
        # Both chains were covered, so no entries expected
        self.assertEqual(len(diff_cc), 0)

    def test_les_change_set_includes_causal_chain_signals(self):
        response = "The wine is aged in stainless steel."
        result = process_open_response_attempt(
            student_response_text=response,
            question_id="OR_002",
            session_id="s1",
            mode="practice",
            timestamp="2026-06-06T10:00:00Z",
            or_item=_SAMPLE_OR_ITEM,
            memory=_fresh_memory(),
            les=_fresh_les(),
        )
        # Change set should reflect causal_chain_signals changed
        self.assertIn("causal_chain_signals", result["les_change_set"])

    def test_cognitive_map_change_set_reflects_difficult_chains(self):
        response = "The wine is aged in stainless steel."
        result = process_open_response_attempt(
            student_response_text=response,
            question_id="OR_002",
            session_id="s1",
            mode="practice",
            timestamp="2026-06-06T10:00:00Z",
            or_item=_SAMPLE_OR_ITEM,
            memory=_fresh_memory(),
            les=_fresh_les(),
        )
        self.assertIn("difficult_causal_chains", result["cognitive_map_change_set"])


class TestOpenResponseWwjRemediation(unittest.TestCase):
    """OR remediation includes wwj_chunks when mc_ids_relevant has an available mc_id."""

    def test_mc_ids_relevant_with_available_mc_produces_wwj_chunks(self):
        result = process_open_response_attempt(
            student_response_text="The wine is fruity.",
            question_id="OR_002",
            session_id="s1",
            mode="practice",
            timestamp="2026-06-06T10:00:00Z",
            or_item=_OR_ITEM_WITH_MC,
            memory=_fresh_memory(),
            les=_fresh_les(),
        )
        wwj = result["diagnostic_outcome"]["remediation"]["wwj_chunks"]
        self.assertIsInstance(wwj, list)
        self.assertGreater(len(wwj), 0)

    def test_empty_mc_ids_relevant_wwj_chunks_empty_or_evaluator_driven(self):
        # or_item with no mc_ids_relevant — wwj_chunks come only from evaluator
        result = process_open_response_attempt(
            student_response_text="The wine is fruity.",
            question_id="OR_002",
            session_id="s1",
            mode="practice",
            timestamp="2026-06-06T10:00:00Z",
            or_item=_SAMPLE_OR_ITEM,  # mc_ids_relevant = []
            memory=_fresh_memory(),
            les=_fresh_les(),
        )
        # wwj_chunks may be empty or populated by evaluator; must be a list
        wwj = result["diagnostic_outcome"]["remediation"]["wwj_chunks"]
        self.assertIsInstance(wwj, list)


class TestOpenResponseMisconcepSignals(unittest.TestCase):
    """mc_ids_relevant in OR item should update LES misconception signals."""

    def test_absent_chains_trigger_mc_as_incorrect(self):
        response = "The wine is aged in stainless steel."  # no MLF, no oak
        result = process_open_response_attempt(
            student_response_text=response,
            question_id="OR_002",
            session_id="s1",
            mode="practice",
            timestamp="2026-06-06T10:00:00Z",
            or_item=_OR_ITEM_WITH_MC,
            memory=_fresh_memory(),
            les=_fresh_les(),
        )
        mc_signals = result["les"].get("misconception_signals", {})
        # MC_AVAILABLE should have been triggered (incorrect)
        self.assertIn(_MC_AVAILABLE, mc_signals)
        self.assertGreaterEqual(mc_signals[_MC_AVAILABLE]["detection_count"], 1)

    def test_misconception_signals_in_next_session_signals(self):
        response = "The wine is aged in stainless steel."
        result = process_open_response_attempt(
            student_response_text=response,
            question_id="OR_002",
            session_id="s1",
            mode="practice",
            timestamp="2026-06-06T10:00:00Z",
            or_item=_OR_ITEM_WITH_MC,
            memory=_fresh_memory(),
            les=_fresh_les(),
        )
        repair = result["next_session_signals"]["misconception_repair_candidate"]
        mc_ids = [r["mc_id"] for r in repair]
        self.assertIn(_MC_AVAILABLE, mc_ids)


# ---------------------------------------------------------------------------
# 4. Governance — no forbidden strings in any output
# ---------------------------------------------------------------------------

class TestGovernanceNoForbiddenStrings(unittest.TestCase):
    """No output may contain score, percentage, pass/fail, or WSET exam strings."""

    def _check_output(self, result: dict, label: str) -> None:
        result_str = str(result)
        for forbidden in FORBIDDEN_STRINGS:
            # "score" as a substring check needs careful scoping to avoid false positives
            # in legitimate field names like "reasoning_quality"
            if forbidden in ("score", "percentage", "pass_fail"):
                # Check for these as standalone keys or values
                self.assertNotIn(f'"{forbidden}"', result_str, msg=f"Forbidden '{forbidden}' in {label}")
                self.assertNotIn(f"'{forbidden}'", result_str, msg=f"Forbidden '{forbidden}' in {label}")
            else:
                self.assertNotIn(forbidden, result_str, msg=f"Forbidden '{forbidden}' in {label}")

    def test_sba_correct_answer_no_forbidden(self):
        result = process_question_attempt(
            student_answer="A",
            question_id="q1",
            session_id="s1",
            mode="practice",
            timestamp="2026-06-06T10:00:00Z",
            question_item=_SAMPLE_SBA_ITEM,
            memory=_fresh_memory(),
            les=_fresh_les(),
            mc_id=_MC_AVAILABLE,
        )
        self._check_output(result, "sba_correct")

    def test_sba_wrong_answer_no_forbidden(self):
        result = process_question_attempt(
            student_answer="B",
            question_id="q1",
            session_id="s1",
            mode="practice",
            timestamp="2026-06-06T10:00:00Z",
            question_item=_SAMPLE_SBA_ITEM,
            memory=_fresh_memory(),
            les=_fresh_les(),
            mc_id=_MC_AVAILABLE,
        )
        self._check_output(result, "sba_wrong")

    def test_or_attempt_no_forbidden(self):
        result = process_open_response_attempt(
            student_response_text="Malolactic fermentation reduces malic acid.",
            question_id="OR_002",
            session_id="s1",
            mode="practice",
            timestamp="2026-06-06T10:00:00Z",
            or_item=_OR_ITEM_WITH_MC,
            memory=_fresh_memory(),
            les=_fresh_les(),
        )
        self._check_output(result, "or_attempt")

    def test_governance_flags_always_false_sba(self):
        result = process_question_attempt(
            student_answer="B",
            question_id="q1",
            session_id="s1",
            mode="practice",
            timestamp="2026-06-06T10:00:00Z",
            question_item=_SAMPLE_SBA_ITEM,
            memory=_fresh_memory(),
            les=_fresh_les(),
        )
        gov = result["governance"]
        for flag in ("safe_for_examiner", "examiner_scoring_allowed", "uses_llm",
                     "uses_api", "uses_embeddings", "uses_vector_db", "cloud_services_active"):
            self.assertFalse(gov[flag], msg=f"Governance flag {flag} must be False")

    def test_governance_flags_always_false_or(self):
        result = process_open_response_attempt(
            student_response_text="response",
            question_id="OR_002",
            session_id="s1",
            mode="practice",
            timestamp="2026-06-06T10:00:00Z",
            or_item=_SAMPLE_OR_ITEM,
            memory=_fresh_memory(),
            les=_fresh_les(),
        )
        gov = result["governance"]
        for flag in ("safe_for_examiner", "examiner_scoring_allowed", "uses_llm",
                     "uses_api", "uses_embeddings", "uses_vector_db", "cloud_services_active"):
            self.assertFalse(gov[flag], msg=f"Governance flag {flag} must be False")


# ---------------------------------------------------------------------------
# 5. Return shape contract
# ---------------------------------------------------------------------------

class TestReturnShapeContract(unittest.TestCase):
    """Both pipeline functions return the same top-level key set."""

    _EXPECTED_KEYS = frozenset({
        "attempt", "diagnostic_outcome", "formative_event", "cognitive_map",
        "cognitive_map_change_set", "les", "les_change_set", "emitted_signals",
        "next_session_signals", "governance",
    })

    def test_sba_return_shape(self):
        result = process_question_attempt(
            student_answer="A",
            question_id="q1",
            session_id="s1",
            mode="practice",
            timestamp="2026-06-06T10:00:00Z",
            question_item=_SAMPLE_SBA_ITEM,
            memory=_fresh_memory(),
            les=_fresh_les(),
        )
        self.assertEqual(set(result.keys()), self._EXPECTED_KEYS)

    def test_or_return_shape(self):
        result = process_open_response_attempt(
            student_response_text="response",
            question_id="OR_002",
            session_id="s1",
            mode="practice",
            timestamp="2026-06-06T10:00:00Z",
            or_item=_SAMPLE_OR_ITEM,
            memory=_fresh_memory(),
            les=_fresh_les(),
        )
        self.assertEqual(set(result.keys()), self._EXPECTED_KEYS)

    def test_next_session_signals_has_required_keys(self):
        signals = build_next_session_signals(_fresh_memory(), _fresh_les())
        self.assertIn("review_topics", signals)
        self.assertIn("misconception_repair_candidate", signals)
        self.assertIn("causal_chain_reinforcement_candidate", signals)

    def test_original_les_not_mutated_sba(self):
        les = _fresh_les()
        import copy
        original = copy.deepcopy(les)
        process_question_attempt(
            student_answer="B",
            question_id="q1",
            session_id="s1",
            mode="practice",
            timestamp="2026-06-06T10:00:00Z",
            question_item=_SAMPLE_SBA_ITEM,
            memory=_fresh_memory(),
            les=les,
            mc_id=_MC_AVAILABLE,
        )
        self.assertEqual(les, original)

    def test_original_les_not_mutated_or(self):
        les = _fresh_les()
        import copy
        original = copy.deepcopy(les)
        process_open_response_attempt(
            student_response_text="response",
            question_id="OR_002",
            session_id="s1",
            mode="practice",
            timestamp="2026-06-06T10:00:00Z",
            or_item=_SAMPLE_OR_ITEM,
            memory=_fresh_memory(),
            les=les,
        )
        self.assertEqual(les, original)

    def test_original_memory_not_mutated_or(self):
        import copy
        memory = _fresh_memory()
        original = copy.deepcopy(memory)
        process_open_response_attempt(
            student_response_text="response",
            question_id="OR_002",
            session_id="s1",
            mode="practice",
            timestamp="2026-06-06T10:00:00Z",
            or_item=_SAMPLE_OR_ITEM,
            memory=memory,
            les=_fresh_les(),
        )
        self.assertEqual(memory, original)


# ---------------------------------------------------------------------------
# 6. build_diagnostic_outcome — direct unit tests
# ---------------------------------------------------------------------------

class TestBuildDiagnosticOutcome(unittest.TestCase):

    def test_incorrect_with_mc_id_builds_remediation(self):
        diag = build_diagnostic_outcome(
            outcome="incorrect",
            question_id="q1",
            mc_id=_MC_AVAILABLE,
        )
        self.assertEqual(diag["outcome"], "incorrect")
        self.assertIsNotNone(diag["remediation_routing"])

    def test_correct_with_mc_id_no_wwj_chunks(self):
        diag = build_diagnostic_outcome(
            outcome="correct",
            question_id="q1",
            mc_id=_MC_AVAILABLE,
        )
        routing = diag["remediation_routing"]
        self.assertIsNotNone(routing)
        self.assertEqual(routing["wwj_chunks"], [])

    def test_no_mc_id_routing_is_none(self):
        diag = build_diagnostic_outcome(
            outcome="incorrect",
            question_id="q1",
            mc_id=None,
        )
        self.assertIsNone(diag["remediation_routing"])


if __name__ == "__main__":
    unittest.main()
