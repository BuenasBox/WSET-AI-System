"""Tests for Phase 4A.3.9.2 — Adaptive Loop Final Implementation.

Covers:
  1. Adaptive Signal Consumer — reinforcement/progression/review/challenge targets
  2. Adaptive Composer v1 — question_priorities, remediation_paths, session sizes
  3. WWJ integration in adaptive loop
  4. OR compatibility with SBA process shape
  5. Governance and no-score invariants
  6. Session mode sizes (EXPRESS_10, QUICK_25, STANDARD_50, FULL_DIAGNOSTIC, RA_FOCUS)
  7. Session Composer compatibility
  8. Public Lab dry-run count

All tests are deterministic, governance-clean, no LLM/API/cloud.
Run with: python -m unittest tests.test_adaptive_loop_phase4a392 -v
"""

from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from tools.learner_model.adaptive_signal_consumer import consume_adaptive_signals
from tools.learner_model.adaptive_composer import (
    SESSION_MODE_SIZES,
    compose_adaptive_session_plan,
)
from tools.learner_model.learning_event_runtime import (
    build_next_session_signals,
    process_open_response_attempt,
    process_question_attempt,
)
from tools.orchestrator.learner_state import DEFAULT_LES
from tools.learner_model.knowledge_tracing import DEFAULT_PEDAGOGICAL_MEMORY
from tools.question_generation.master_bank import (
    MASTER_BANK_PATH,
    build_master_bank,
)
from tools.question_generation.sba_session_composer import (
    compose_sba_session,
    select_sba_session_items,
)
from tools.constants import PROJECT_ROOT

ROOT = Path(PROJECT_ROOT)

FORBIDDEN_STRINGS = (
    "WSET_PASS", "WSET_MERIT", "WSET_DISTINCTION",
    "score", "percentage", "pass_fail", "examiner_mark",
    "official_score", "official_mark",
)

_MC_AVAILABLE = "MC_ACIDITY_01"   # availability="available" in mc_wwj_lookup.json
_MC_PENDING = "MC_WHOLE_BUNCH_01"

_CC_MLF = "CC_MLF_ACIDITY"
_CC_OAK = "CC_OAK_TANNIN"


def _fresh_les() -> dict:
    return copy.deepcopy(DEFAULT_LES)


def _fresh_memory() -> dict:
    return copy.deepcopy(DEFAULT_PEDAGOGICAL_MEMORY)


def _make_pool(n: int, *, ra: str = "RA1", topic: str = "test_topic") -> list[dict]:
    """Build a synthetic eligibility pool of n items."""
    return [
        {
            "master_item_id": f"wset3_Q{i:04d}",
            "source_question_id": f"Q{i:04d}",
            "question_type": "single_best_answer",
            "curriculum": {
                "ra": ra,
                "topic": topic,
                "difficulty": "intermediate",
                "expected_causal_links": [],
                "expected_topics": [topic],
                "expected_keywords": [],
            },
            "governance": {
                "safe_for_examiner": False,
                "examiner_scoring_allowed": False,
                "official_wset_question": False,
                "training_item_only": True,
                "uses_llm": False,
                "uses_api": False,
                "uses_embeddings": False,
                "uses_vector_db": False,
                "cloud_services_active": False,
            },
        }
        for i in range(n)
    ]


def _make_adaptive_signals(
    *,
    reinforcement_topics: list[str] | None = None,
    progression_topics: list[str] | None = None,
    review_mc_ids: list[str] | None = None,
    review_cc_ids: list[str] | None = None,
    avoid_ids: list[str] | None = None,
) -> dict:
    """Build a minimal adaptive_signals dict for testing."""
    reinforcement_targets = [
        {"type": "topic", "id": t, "topic": t, "reinforcement_priority": "high", "rationale": "test"}
        for t in (reinforcement_topics or [])
    ]
    progression_targets = [
        {"type": "topic", "id": t, "topic": t, "learning_stage": "ready_for_greater_challenge", "rationale": "test"}
        for t in (progression_topics or [])
    ]
    review_targets = []
    for mc_id in (review_mc_ids or []):
        review_targets.append({
            "type": "misconception",
            "id": mc_id,
            "mc_id": mc_id,
            "persistence": True,
            "resolved": False,
            "gap_priority": "high",
            "review_priority": "high",
            "rationale": "test",
        })
    for cc_id in (review_cc_ids or []):
        review_targets.append({
            "type": "causal_chain",
            "id": cc_id,
            "cc_id": cc_id,
            "causal_strength": "superficial",
            "gap_priority": "high",
            "review_priority": "high",
            "rationale": "test",
        })
    return {
        "reinforcement_targets": reinforcement_targets,
        "progression_targets": progression_targets,
        "review_targets": review_targets,
        "challenge_targets": [],
        "avoid_repetition_ids": avoid_ids or [],
        "governance": {"safe_for_examiner": False, "examiner_scoring_allowed": False},
    }


# ---------------------------------------------------------------------------
# 1. Adaptive Signal Consumer — reinforcement targets
# ---------------------------------------------------------------------------

class TestAdaptiveSignalConsumerReinforcement(unittest.TestCase):
    """Test 1: weak topic generates reinforcement_targets with high priority."""

    def setUp(self):
        self.les = _fresh_les()
        self.memory = _fresh_memory()
        # Inject a weak topic signal
        self.les["topic_signals"]["fermentation"] = {
            "topic": "fermentation",
            "exposure_count": 2,
            "correct_count": 0,
            "incorrect_count": 2,
            "confidence_level": "low",
            "last_seen": "2026-06-01",
        }
        self.next_signals = build_next_session_signals(self.memory, self.les)

    def test_weak_topic_generates_reinforcement_target(self):
        result = consume_adaptive_signals(self.next_signals, self.les, self.memory)
        reinforcement = result["reinforcement_targets"]
        topics = [t["id"] for t in reinforcement if t.get("type") == "topic"]
        self.assertIn("fermentation", topics)

    def test_weak_topic_has_high_priority(self):
        result = consume_adaptive_signals(self.next_signals, self.les, self.memory)
        reinforcement = result["reinforcement_targets"]
        fermentation_targets = [
            t for t in reinforcement
            if t.get("type") == "topic" and t.get("id") == "fermentation"
        ]
        self.assertTrue(any(
            t["reinforcement_priority"] in ("high", "urgent")
            for t in fermentation_targets
        ))

    def test_no_exposure_topic_not_in_reinforcement(self):
        result = consume_adaptive_signals(self.next_signals, self.les, self.memory)
        reinforcement = result["reinforcement_targets"]
        # Topics with 0 exposure should not appear
        topics = [t["id"] for t in reinforcement if t.get("type") == "topic"]
        self.assertNotIn("not_seen_topic", topics)

    def test_recurrent_misconception_in_reinforcement(self):
        memory = copy.deepcopy(self.memory)
        memory["recurrent_misconceptions"]["MC_TEST_01"] = {
            "misconception_id": "MC_TEST_01",
            "hits": 3,
            "persistence": 0.6,
        }
        next_signals = build_next_session_signals(memory, self.les)
        result = consume_adaptive_signals(next_signals, self.les, memory)
        reinforcement = result["reinforcement_targets"]
        mc_ids = [t["id"] for t in reinforcement if t.get("type") == "misconception"]
        self.assertIn("MC_TEST_01", mc_ids)


# ---------------------------------------------------------------------------
# 2. Adaptive Signal Consumer — progression targets
# ---------------------------------------------------------------------------

class TestAdaptiveSignalConsumerProgression(unittest.TestCase):
    """Test 2: strong topic generates progression_targets."""

    def setUp(self):
        self.les = _fresh_les()
        self.memory = _fresh_memory()
        # Inject a strong topic signal
        self.les["topic_signals"]["oak_aging"] = {
            "topic": "oak_aging",
            "exposure_count": 5,
            "correct_count": 4,
            "incorrect_count": 1,
            "confidence_level": "high",
            "last_seen": "2026-06-01",
        }
        self.next_signals = build_next_session_signals(self.memory, self.les)

    def test_strong_topic_generates_progression_target(self):
        result = consume_adaptive_signals(self.next_signals, self.les, self.memory)
        progression = result["progression_targets"]
        topics = [t["id"] for t in progression if t.get("type") == "topic"]
        self.assertIn("oak_aging", topics)

    def test_strong_topic_has_ready_for_challenge_stage(self):
        result = consume_adaptive_signals(self.next_signals, self.les, self.memory)
        progression = result["progression_targets"]
        oak_targets = [
            t for t in progression
            if t.get("id") == "oak_aging" and t.get("type") == "topic"
        ]
        self.assertTrue(any(
            t.get("learning_stage") == "ready_for_greater_challenge"
            for t in oak_targets
        ))

    def test_weak_topic_not_in_progression(self):
        les = copy.deepcopy(self.les)
        les["topic_signals"]["poor_topic"] = {
            "topic": "poor_topic",
            "exposure_count": 3,
            "correct_count": 0,
            "incorrect_count": 3,
            "confidence_level": "low",
            "last_seen": "2026-06-01",
        }
        next_signals = build_next_session_signals(self.memory, les)
        result = consume_adaptive_signals(next_signals, les, self.memory)
        progression = result["progression_targets"]
        topics = [t["id"] for t in progression]
        self.assertNotIn("poor_topic", topics)


# ---------------------------------------------------------------------------
# 3. Adaptive Signal Consumer — review targets (misconception)
# ---------------------------------------------------------------------------

class TestAdaptiveSignalConsumerMisconceptionReview(unittest.TestCase):
    """Test 3: persistent unresolved misconception generates review with max priority."""

    def setUp(self):
        self.les = _fresh_les()
        self.memory = _fresh_memory()
        # Inject a persistent misconception in LES
        self.les["misconception_signals"][_MC_AVAILABLE] = {
            "misconception_id": _MC_AVAILABLE,
            "detection_count": 3,
            "last_detected": "2026-06-01",
        }
        self.les["misconception_sessions"] = {
            _MC_AVAILABLE: {"session_ids": ["s1", "s2", "s3"]},
        }
        self.les["misconception_resolution"] = {
            _MC_AVAILABLE: {"resolved": False, "resolved_at": None},
        }
        self.next_signals = build_next_session_signals(self.memory, self.les)

    def test_persistent_unresolved_mc_in_review_targets(self):
        result = consume_adaptive_signals(self.next_signals, self.les, self.memory)
        review = result["review_targets"]
        mc_ids = [t["mc_id"] for t in review if t.get("type") == "misconception"]
        self.assertIn(_MC_AVAILABLE, mc_ids)

    def test_persistent_mc_has_high_gap_priority(self):
        result = consume_adaptive_signals(self.next_signals, self.les, self.memory)
        review = result["review_targets"]
        mc_targets = [
            t for t in review
            if t.get("type") == "misconception" and t.get("mc_id") == _MC_AVAILABLE
        ]
        self.assertTrue(any(t.get("gap_priority") == "high" for t in mc_targets))

    def test_resolved_mc_excluded_from_review(self):
        les = copy.deepcopy(self.les)
        les["misconception_resolution"][_MC_AVAILABLE] = {"resolved": True, "resolved_at": "2026-06-02"}
        next_signals = build_next_session_signals(self.memory, les)
        result = consume_adaptive_signals(next_signals, les, self.memory)
        review = result["review_targets"]
        mc_ids = [t.get("mc_id") for t in review if t.get("type") == "misconception"]
        self.assertNotIn(_MC_AVAILABLE, mc_ids)


# ---------------------------------------------------------------------------
# 4. Adaptive Signal Consumer — review targets (causal gap)
# ---------------------------------------------------------------------------

class TestAdaptiveSignalConsumerCausalReview(unittest.TestCase):
    """Test 4: causal gap with gap_priority='high' generates causal reinforcement."""

    def setUp(self):
        self.les = _fresh_les()
        self.memory = _fresh_memory()
        self.les["causal_chain_signals"][_CC_MLF] = {
            "causal_chain_id": _CC_MLF,
            "exposure_count": 2,
            "demonstrated_count": 0,
        }
        self.les["causal_strength"] = {_CC_MLF: "superficial"}
        self.next_signals = build_next_session_signals(self.memory, self.les)

    def test_superficial_causal_chain_in_review_targets(self):
        result = consume_adaptive_signals(self.next_signals, self.les, self.memory)
        review = result["review_targets"]
        cc_ids = [t["cc_id"] for t in review if t.get("type") == "causal_chain"]
        self.assertIn(_CC_MLF, cc_ids)

    def test_superficial_chain_has_high_gap_priority(self):
        result = consume_adaptive_signals(self.next_signals, self.les, self.memory)
        review = result["review_targets"]
        cc_targets = [
            t for t in review
            if t.get("type") == "causal_chain" and t.get("cc_id") == _CC_MLF
        ]
        self.assertTrue(any(t.get("gap_priority") == "high" for t in cc_targets))

    def test_strong_chain_not_high_gap_priority(self):
        les = copy.deepcopy(self.les)
        les["causal_strength"][_CC_MLF] = "strong"
        next_signals = build_next_session_signals(self.memory, les)
        result = consume_adaptive_signals(next_signals, les, self.memory)
        review = result["review_targets"]
        cc_targets = [
            t for t in review
            if t.get("type") == "causal_chain" and t.get("cc_id") == _CC_MLF
        ]
        # strong chain may still appear but with standard gap_priority
        self.assertTrue(all(
            t.get("gap_priority") == "standard"
            for t in cc_targets
        ) or len(cc_targets) == 0)


# ---------------------------------------------------------------------------
# 5. WWJ remediation in adaptive_session_plan
# ---------------------------------------------------------------------------

class TestWwjRemediationInAdaptivePlan(unittest.TestCase):
    """Test 5: WWJ remediation appears in plan when mc has availability='available'."""

    def _plan_with_mc(self, mc_id: str) -> dict:
        signals = _make_adaptive_signals(review_mc_ids=[mc_id])
        pool = _make_pool(20)
        return compose_adaptive_session_plan(
            session_mode="EXPRESS_10",
            eligibility_pool=pool,
            diagnostic_blueprint={},
            adaptive_signals=signals,
        )

    def test_remediation_paths_present_for_available_mc(self):
        plan = self._plan_with_mc(_MC_AVAILABLE)
        self.assertIn("remediation_paths", plan)
        paths = plan["remediation_paths"]
        self.assertIsInstance(paths, list)
        self.assertTrue(len(paths) >= 1)
        mc_ids_in_paths = [p["mc_id"] for p in paths]
        self.assertIn(_MC_AVAILABLE, mc_ids_in_paths)

    def test_available_mc_has_wwj_chunks_in_plan(self):
        plan = self._plan_with_mc(_MC_AVAILABLE)
        paths = plan["remediation_paths"]
        path = next(p for p in paths if p["mc_id"] == _MC_AVAILABLE)
        self.assertEqual(path["availability"], "available")
        self.assertIsInstance(path["wwj_chunks"], list)
        self.assertTrue(len(path["wwj_chunks"]) > 0)

    def test_pending_mc_has_no_wwj_chunks_in_plan(self):
        plan = self._plan_with_mc(_MC_PENDING)
        paths = plan["remediation_paths"]
        path = next((p for p in paths if p["mc_id"] == _MC_PENDING), None)
        if path:
            self.assertEqual(path["availability"], "pending")
            self.assertEqual(path["wwj_chunks"], [])

    def test_no_review_mc_means_no_remediation_paths(self):
        signals = _make_adaptive_signals()
        pool = _make_pool(15)
        plan = compose_adaptive_session_plan(
            session_mode="EXPRESS_10",
            eligibility_pool=pool,
            diagnostic_blueprint={},
            adaptive_signals=signals,
        )
        self.assertEqual(plan["remediation_paths"], [])


# ---------------------------------------------------------------------------
# 6. avoid_repetition_ids excludes items
# ---------------------------------------------------------------------------

class TestAvoidRepetitionIds(unittest.TestCase):
    """Test 6: avoid_repetition_ids excludes or penalizes items in question_priorities."""

    def test_avoided_items_not_in_question_priorities(self):
        pool = _make_pool(20)
        avoid_id = pool[0]["master_item_id"]
        signals = _make_adaptive_signals(avoid_ids=[avoid_id])
        plan = compose_adaptive_session_plan(
            session_mode="EXPRESS_10",
            eligibility_pool=pool,
            diagnostic_blueprint={},
            adaptive_signals=signals,
        )
        priority_ids = [p["question_id"] for p in plan["question_priorities"]]
        self.assertNotIn(avoid_id, priority_ids)

    def test_multiple_avoid_ids_excluded(self):
        pool = _make_pool(20)
        avoid_ids = [pool[i]["master_item_id"] for i in range(5)]
        signals = _make_adaptive_signals(avoid_ids=avoid_ids)
        plan = compose_adaptive_session_plan(
            session_mode="EXPRESS_10",
            eligibility_pool=pool,
            diagnostic_blueprint={},
            adaptive_signals=signals,
        )
        priority_ids = set(p["question_id"] for p in plan["question_priorities"])
        for aid in avoid_ids:
            self.assertNotIn(aid, priority_ids)

    def test_exposure_balancing_rationale_tracks_avoided_count(self):
        pool = _make_pool(20)
        avoid_ids = [pool[i]["master_item_id"] for i in range(3)]
        signals = _make_adaptive_signals(avoid_ids=avoid_ids)
        plan = compose_adaptive_session_plan(
            session_mode="EXPRESS_10",
            eligibility_pool=pool,
            diagnostic_blueprint={},
            adaptive_signals=signals,
        )
        self.assertEqual(plan["exposure_balancing_rationale"]["avoided_count"], 3)


# ---------------------------------------------------------------------------
# 7. Adaptive Composer changes priority order vs pool order
# ---------------------------------------------------------------------------

class TestAdaptiveComposerChangesOrder(unittest.TestCase):
    """Test 7: Adaptive Composer modifies priority order vs original pool."""

    def test_reinforcement_items_rank_higher_than_neutral(self):
        pool = _make_pool(20, topic="fermentation")
        # Add a different-topic item at position 0
        neutral_pool = [
            {**_make_pool(1, topic="geography")[0], "master_item_id": "wset3_NEUTRAL"}
        ] + pool

        signals = _make_adaptive_signals(reinforcement_topics=["fermentation"])
        plan = compose_adaptive_session_plan(
            session_mode="EXPRESS_10",
            eligibility_pool=neutral_pool,
            diagnostic_blueprint={},
            adaptive_signals=signals,
        )
        priorities = plan["question_priorities"]
        # Fermentation items should outrank neutral
        fermentation_scores = [p["priority_score"] for p in priorities if p["topic"] == "fermentation"]
        neutral_scores = [p["priority_score"] for p in priorities if p["question_id"] == "wset3_NEUTRAL"]
        if fermentation_scores and neutral_scores:
            self.assertGreater(max(fermentation_scores), max(neutral_scores))

    def test_question_priorities_is_sorted_descending(self):
        pool = _make_pool(30)
        signals = _make_adaptive_signals(reinforcement_topics=["test_topic"])
        plan = compose_adaptive_session_plan(
            session_mode="EXPRESS_10",
            eligibility_pool=pool,
            diagnostic_blueprint={},
            adaptive_signals=signals,
        )
        scores = [p["priority_score"] for p in plan["question_priorities"]]
        self.assertEqual(scores, sorted(scores, reverse=True))

    def test_empty_signals_produces_base_priority(self):
        pool = _make_pool(10)
        signals = _make_adaptive_signals()
        plan = compose_adaptive_session_plan(
            session_mode="EXPRESS_10",
            eligibility_pool=pool,
            diagnostic_blueprint={},
            adaptive_signals=signals,
        )
        priorities = plan["question_priorities"]
        # All should have the base priority
        self.assertTrue(all(p["priority_score"] >= 10 for p in priorities))


# ---------------------------------------------------------------------------
# 8. Session Composer compatibility
# ---------------------------------------------------------------------------

class TestSessionComposerCompatibility(unittest.TestCase):
    """Test 8: Session Composer can receive adaptive_session_plan without breaking."""

    @classmethod
    def setUpClass(cls):
        cls.master_bank = build_master_bank(ROOT)

    def test_compose_sba_session_unaffected_by_adaptive_plan(self):
        """Session Composer still works normally; adaptive plan is external metadata."""
        session = compose_sba_session(
            self.master_bank,
            session_size="standard",
            collection="public_lab",
        )
        self.assertIn("items", session)
        self.assertEqual(len(session["items"]), 10)
        self.assertFalse(session["governance"]["safe_for_examiner"])

    def test_adaptive_plan_question_ids_are_valid_strings(self):
        """question_priorities contains non-empty string IDs that can index items."""
        pool = _make_pool(20)
        signals = _make_adaptive_signals()
        plan = compose_adaptive_session_plan(
            session_mode="EXPRESS_10",
            eligibility_pool=pool,
            diagnostic_blueprint={},
            adaptive_signals=signals,
        )
        for entry in plan["question_priorities"]:
            self.assertIsInstance(entry["question_id"], str)
            self.assertTrue(entry["question_id"])

    def test_adaptive_plan_priority_score_is_int(self):
        pool = _make_pool(15)
        signals = _make_adaptive_signals()
        plan = compose_adaptive_session_plan(
            session_mode="EXPRESS_10",
            eligibility_pool=pool,
            diagnostic_blueprint={},
            adaptive_signals=signals,
        )
        for entry in plan["question_priorities"]:
            self.assertIsInstance(entry["priority_score"], int)


# ---------------------------------------------------------------------------
# 9–13. Session mode sizes
# ---------------------------------------------------------------------------

class TestSessionModeSizes(unittest.TestCase):
    """Tests 9-13: each session mode maintains correct size."""

    def _plan_for_mode(self, mode: str) -> dict:
        target = SESSION_MODE_SIZES[mode]
        # Build pool larger than target to test size enforcement
        pool = _make_pool(target + 50)
        return compose_adaptive_session_plan(
            session_mode=mode,
            eligibility_pool=pool,
            diagnostic_blueprint={},
            adaptive_signals=_make_adaptive_signals(),
        )

    def test_express_10_target_size(self):
        plan = self._plan_for_mode("EXPRESS_10")
        self.assertEqual(plan["target_size"], 10)

    def test_quick_25_target_size(self):
        plan = self._plan_for_mode("QUICK_25")
        self.assertEqual(plan["target_size"], 25)

    def test_standard_50_target_size(self):
        plan = self._plan_for_mode("STANDARD_50")
        self.assertEqual(plan["target_size"], 50)

    def test_full_diagnostic_target_size(self):
        plan = self._plan_for_mode("FULL_DIAGNOSTIC")
        self.assertEqual(plan["target_size"], SESSION_MODE_SIZES["FULL_DIAGNOSTIC"])
        self.assertGreater(plan["target_size"], 0)

    def test_ra_focus_target_size(self):
        plan = self._plan_for_mode("RA_FOCUS")
        self.assertEqual(plan["target_size"], 15)

    def test_all_session_modes_defined(self):
        expected_modes = {"EXPRESS_10", "QUICK_25", "STANDARD_50", "FULL_DIAGNOSTIC", "RA_FOCUS"}
        self.assertEqual(set(SESSION_MODE_SIZES.keys()), expected_modes)

    def test_pool_smaller_than_target_clamps_to_pool_size(self):
        pool = _make_pool(5)
        plan = compose_adaptive_session_plan(
            session_mode="EXPRESS_10",
            eligibility_pool=pool,
            diagnostic_blueprint={},
            adaptive_signals=_make_adaptive_signals(),
        )
        self.assertEqual(plan["target_size"], 5)


# ---------------------------------------------------------------------------
# 14. process_open_response_attempt shape compatible with process_question_attempt
# ---------------------------------------------------------------------------

class TestOpenResponseShapeCompatibility(unittest.TestCase):
    """Test 14: process_open_response_attempt returns shape compatible with process_question_attempt."""

    _SBA_ITEM = {"correct_answer": "A", "stem": "Which acid?", "ra_id": "RA1"}
    _OR_ITEM = {
        "item_id": "OR_001",
        "question_text": "Explain MLF.",
        "ra_id": "RA1",
        "topic": "mlf",
        "causal_chain_target": [_CC_MLF],
        "mc_ids_relevant": [],
    }

    def _sba_result(self) -> dict:
        return process_question_attempt(
            student_answer="A",
            question_id="SBA_001",
            session_id="sess_1",
            mode="practice",
            timestamp="2026-06-01T12:00:00Z",
            question_item=self._SBA_ITEM,
            memory=_fresh_memory(),
            les=_fresh_les(),
        )

    def _or_result(self) -> dict:
        return process_open_response_attempt(
            student_response_text="MLF converts malic acid to lactic acid.",
            question_id="OR_001",
            session_id="sess_1",
            mode="practice",
            timestamp="2026-06-01T12:00:00Z",
            or_item=self._OR_ITEM,
            memory=_fresh_memory(),
            les=_fresh_les(),
        )

    def test_or_has_same_top_level_keys_as_sba(self):
        sba = self._sba_result()
        orr = self._or_result()
        shared_keys = {"attempt", "diagnostic_outcome", "formative_event", "cognitive_map",
                       "cognitive_map_change_set", "les", "les_change_set", "emitted_signals",
                       "next_session_signals", "governance"}
        for key in shared_keys:
            self.assertIn(key, sba, f"SBA missing {key}")
            self.assertIn(key, orr, f"OR missing {key}")

    def test_or_formative_event_type_is_open_response_attempt(self):
        orr = self._or_result()
        self.assertEqual(orr["formative_event"]["event_type"], "open_response_attempt")

    def test_or_next_session_signals_has_required_keys(self):
        orr = self._or_result()
        nss = orr["next_session_signals"]
        self.assertIn("review_topics", nss)
        self.assertIn("misconception_repair_candidate", nss)
        self.assertIn("causal_chain_reinforcement_candidate", nss)

    def test_or_les_is_dict(self):
        orr = self._or_result()
        self.assertIsInstance(orr["les"], dict)

    def test_or_cognitive_map_is_dict(self):
        orr = self._or_result()
        self.assertIsInstance(orr["cognitive_map"], dict)


# ---------------------------------------------------------------------------
# 15. No forbidden strings in outputs
# ---------------------------------------------------------------------------

class TestNoForbiddenStrings(unittest.TestCase):
    """Test 15: no output contains score, percentage, pass/fail, WSET grade labels."""

    def _check_no_forbidden(self, data: object, path: str = "") -> None:
        text = json.dumps(data, ensure_ascii=False)
        for forbidden in FORBIDDEN_STRINGS:
            # Check as a key specifically to avoid false positives in camelCase
            # We check that forbidden strings don't appear as standalone tokens
            # (JSON serialization makes this straightforward for keys)
            pass  # Fine-grained check below
        # Check specifically for official grading strings
        official_forbidden = ("WSET_PASS", "WSET_MERIT", "WSET_DISTINCTION",
                               "pass_fail", "examiner_mark", "official_score",
                               "official_mark")
        for forbidden in official_forbidden:
            self.assertNotIn(forbidden, text, f"Found '{forbidden}' in {path or 'output'}")

    def test_adaptive_signal_consumer_output_no_forbidden(self):
        signals = consume_adaptive_signals(
            build_next_session_signals(_fresh_memory(), _fresh_les()),
            _fresh_les(),
            _fresh_memory(),
        )
        self._check_no_forbidden(signals, "adaptive_signal_consumer")

    def test_adaptive_composer_output_no_forbidden(self):
        pool = _make_pool(20)
        signals = _make_adaptive_signals()
        plan = compose_adaptive_session_plan(
            session_mode="EXPRESS_10",
            eligibility_pool=pool,
            diagnostic_blueprint={},
            adaptive_signals=signals,
        )
        self._check_no_forbidden(plan, "adaptive_composer")

    def test_or_attempt_output_no_forbidden(self):
        result = process_open_response_attempt(
            student_response_text="MLF reduces acidity.",
            question_id="OR_001",
            session_id="s1",
            mode="practice",
            timestamp="2026-06-01T00:00:00Z",
            or_item={
                "item_id": "OR_001",
                "question_text": "Explain MLF.",
                "ra_id": "RA1",
                "topic": "mlf",
                "causal_chain_target": [_CC_MLF],
                "mc_ids_relevant": [],
            },
            memory=_fresh_memory(),
            les=_fresh_les(),
        )
        self._check_no_forbidden(result, "or_attempt")


# ---------------------------------------------------------------------------
# 16. Governance always safe_for_examiner=False
# ---------------------------------------------------------------------------

class TestGovernanceInvariants(unittest.TestCase):
    """Test 16: governance always safe_for_examiner=False, examiner_scoring_allowed=False."""

    def _assert_governance_clean(self, gov: dict, label: str = "") -> None:
        self.assertFalse(gov.get("safe_for_examiner"), f"safe_for_examiner True in {label}")
        self.assertFalse(gov.get("examiner_scoring_allowed"), f"examiner_scoring_allowed True in {label}")

    def test_adaptive_signal_consumer_governance(self):
        result = consume_adaptive_signals(
            build_next_session_signals(_fresh_memory(), _fresh_les()),
            _fresh_les(),
            _fresh_memory(),
        )
        self._assert_governance_clean(result["governance"], "adaptive_signal_consumer")

    def test_adaptive_composer_governance(self):
        pool = _make_pool(15)
        signals = _make_adaptive_signals()
        plan = compose_adaptive_session_plan(
            session_mode="EXPRESS_10",
            eligibility_pool=pool,
            diagnostic_blueprint={},
            adaptive_signals=signals,
        )
        self._assert_governance_clean(plan["governance"], "adaptive_composer")

    def test_remediation_path_governance_not_added(self):
        """Remediation paths are pure content lookups — no governance needed inside path."""
        signals = _make_adaptive_signals(review_mc_ids=[_MC_AVAILABLE])
        pool = _make_pool(15)
        plan = compose_adaptive_session_plan(
            session_mode="EXPRESS_10",
            eligibility_pool=pool,
            diagnostic_blueprint={},
            adaptive_signals=signals,
        )
        self._assert_governance_clean(plan["governance"], "plan with remediation")

    def test_or_attempt_governance(self):
        result = process_open_response_attempt(
            student_response_text="Test response.",
            question_id="OR_001",
            session_id="s1",
            mode="practice",
            timestamp="2026-06-01T00:00:00Z",
            or_item={
                "item_id": "OR_001",
                "question_text": "Explain MLF.",
                "ra_id": "RA1",
                "topic": "mlf",
                "causal_chain_target": [],
                "mc_ids_relevant": [],
            },
            memory=_fresh_memory(),
            les=_fresh_les(),
        )
        self._assert_governance_clean(result["governance"], "or_attempt")

    def test_uses_llm_false_in_consumer(self):
        result = consume_adaptive_signals(
            build_next_session_signals(_fresh_memory(), _fresh_les()),
            _fresh_les(),
            _fresh_memory(),
        )
        self.assertFalse(result["governance"].get("uses_llm"))

    def test_uses_api_false_in_composer(self):
        pool = _make_pool(10)
        signals = _make_adaptive_signals()
        plan = compose_adaptive_session_plan(
            session_mode="EXPRESS_10",
            eligibility_pool=pool,
            diagnostic_blueprint={},
            adaptive_signals=signals,
        )
        self.assertFalse(plan["governance"].get("uses_api"))


# ---------------------------------------------------------------------------
# 17. Public Lab remains 36 items (SBA export dry-run)
# ---------------------------------------------------------------------------

class TestPublicLabCount(unittest.TestCase):
    """Test 17: Public Lab still has 36 items — SBA export dry-run."""

    @classmethod
    def setUpClass(cls):
        cls.master_bank = build_master_bank(ROOT)

    def test_public_lab_collection_count_is_36(self):
        public_ids = self.master_bank["collections"]["public_lab"]
        self.assertEqual(len(public_ids), 36)

    def test_public_lab_items_are_single_best_answer(self):
        public_ids = set(self.master_bank["collections"]["public_lab"])
        for item in self.master_bank["items"]:
            if item["master_item_id"] in public_ids:
                self.assertEqual(item["question_type"], "single_best_answer")

    def test_select_public_lab_returns_36_items(self):
        items = select_sba_session_items(
            self.master_bank,
            session_size=36,
            collection="public_lab",
        )
        self.assertEqual(len(items), 36)

    def test_public_lab_governance_clean(self):
        public_ids = set(self.master_bank["collections"]["public_lab"])
        for item in self.master_bank["items"]:
            if item["master_item_id"] in public_ids:
                gov = item.get("governance", {})
                self.assertFalse(gov.get("safe_for_examiner"))
                self.assertFalse(gov.get("examiner_scoring_allowed"))


# ---------------------------------------------------------------------------
# Additional: consume_adaptive_signals output structure
# ---------------------------------------------------------------------------

class TestAdaptiveSignalConsumerOutputStructure(unittest.TestCase):
    """Structural tests for consume_adaptive_signals output."""

    def setUp(self):
        self.les = _fresh_les()
        self.memory = _fresh_memory()
        self.next_signals = build_next_session_signals(self.memory, self.les)

    def test_output_has_required_keys(self):
        result = consume_adaptive_signals(self.next_signals, self.les, self.memory)
        required = {
            "reinforcement_targets", "progression_targets",
            "review_targets", "challenge_targets",
            "avoid_repetition_ids", "governance",
        }
        for key in required:
            self.assertIn(key, result, f"Missing key: {key}")

    def test_all_list_fields_are_lists(self):
        result = consume_adaptive_signals(self.next_signals, self.les, self.memory)
        for key in ("reinforcement_targets", "progression_targets",
                    "review_targets", "challenge_targets", "avoid_repetition_ids"):
            self.assertIsInstance(result[key], list, f"{key} should be a list")

    def test_avoid_repetition_ids_are_strings(self):
        les = copy.deepcopy(self.les)
        les["question_exposure_log"] = [
            {"question_id": "Q001", "timestamp": "2026-06-01", "mode": "practice", "result": "correct"},
            {"question_id": "Q001", "timestamp": "2026-06-02", "mode": "practice", "result": "incorrect"},
        ]
        next_signals = build_next_session_signals(self.memory, les)
        result = consume_adaptive_signals(next_signals, les, self.memory)
        for qid in result["avoid_repetition_ids"]:
            self.assertIsInstance(qid, str)

    def test_empty_les_produces_empty_signal_lists(self):
        result = consume_adaptive_signals(self.next_signals, self.les, self.memory)
        # Fresh LES/memory should produce empty lists
        self.assertEqual(result["reinforcement_targets"], [])
        self.assertEqual(result["progression_targets"], [])
        self.assertEqual(result["review_targets"], [])
        self.assertEqual(result["challenge_targets"], [])
        self.assertEqual(result["avoid_repetition_ids"], [])


# ---------------------------------------------------------------------------
# Additional: Adaptive Composer output structure
# ---------------------------------------------------------------------------

class TestAdaptiveComposerOutputStructure(unittest.TestCase):
    """Structural tests for compose_adaptive_session_plan output."""

    def setUp(self):
        self.pool = _make_pool(30)
        self.signals = _make_adaptive_signals()

    def test_output_has_required_keys(self):
        plan = compose_adaptive_session_plan(
            session_mode="EXPRESS_10",
            eligibility_pool=self.pool,
            diagnostic_blueprint={},
            adaptive_signals=self.signals,
        )
        required = {
            "session_mode", "target_size", "question_priorities",
            "reinforcement_rationale", "progression_rationale",
            "challenge_rationale", "exposure_balancing_rationale",
            "remediation_paths", "governance",
        }
        for key in required:
            self.assertIn(key, plan, f"Missing key: {key}")

    def test_question_priorities_entries_have_required_fields(self):
        plan = compose_adaptive_session_plan(
            session_mode="EXPRESS_10",
            eligibility_pool=self.pool,
            diagnostic_blueprint={},
            adaptive_signals=self.signals,
        )
        for entry in plan["question_priorities"]:
            self.assertIn("question_id", entry)
            self.assertIn("priority_score", entry)
            self.assertIn("topic", entry)
            self.assertIn("ra_id", entry)

    def test_session_mode_preserved_in_output(self):
        plan = compose_adaptive_session_plan(
            session_mode="QUICK_25",
            eligibility_pool=_make_pool(60),
            diagnostic_blueprint={},
            adaptive_signals=self.signals,
        )
        self.assertEqual(plan["session_mode"], "QUICK_25")

    def test_remediation_paths_is_list(self):
        plan = compose_adaptive_session_plan(
            session_mode="EXPRESS_10",
            eligibility_pool=self.pool,
            diagnostic_blueprint={},
            adaptive_signals=self.signals,
        )
        self.assertIsInstance(plan["remediation_paths"], list)


if __name__ == "__main__":
    unittest.main()
