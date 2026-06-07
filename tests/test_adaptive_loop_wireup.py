"""Adaptive Loop Wire-up Tests — Session Composer integration.

Demonstrates that adaptive signals from the full pipeline flow correctly into
select_sba_session_items() via question_priorities from the Adaptive Composer.

Six validation points required:
  1. Weak topic → higher selection probability in next session.
  2. Persistent misconception → repair targets → affect composition.
  3. Causal gap → causal reinforcement → affect composition.
  4. Strong topic → progression targets reflected in composition.
  5. Exposure avoidance → items in avoid_repetition_ids do not appear.
  6. Adaptive learner gets different composition than neutral learner (same pool).

Full pipeline under test:
  LES/memory → build_next_session_signals()
  → consume_adaptive_signals()
  → compose_adaptive_session_plan()          [question_priorities]
  → select_sba_session_items(question_priorities=...)
  → session items

Run with: python -m unittest tests.test_adaptive_loop_wireup -v
"""

from __future__ import annotations

import copy
import unittest
from typing import Any

from tools.learner_model.adaptive_signal_consumer import consume_adaptive_signals
from tools.learner_model.adaptive_composer import compose_adaptive_session_plan
from tools.learner_model.learning_event_runtime import build_next_session_signals
from tools.orchestrator.learner_state import DEFAULT_LES
from tools.learner_model.knowledge_tracing import DEFAULT_PEDAGOGICAL_MEMORY
from tools.question_generation.sba_session_composer import (
    compose_sba_session,
    select_sba_session_items,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _fresh_les() -> dict:
    return copy.deepcopy(DEFAULT_LES)


def _fresh_memory() -> dict:
    return copy.deepcopy(DEFAULT_PEDAGOGICAL_MEMORY)


def _make_item(
    qid: str,
    topic: str,
    difficulty: str = "intermediate",
    ra: str = "RA1",
    mc_ids: list[str] | None = None,
    cc_ids: list[str] | None = None,
) -> dict[str, Any]:
    """Build a synthetic SBA item for a fake master bank."""
    curriculum: dict[str, Any] = {
        "ra": ra,
        "topic": topic,
        "difficulty": difficulty,
        "expected_topics": [topic, qid],
        "expected_keywords": [qid],
        "expected_causal_links": cc_ids or [],
    }
    if mc_ids:
        curriculum["mc_ids"] = mc_ids
    return {
        "master_item_id": qid,
        "source_question_id": qid,
        "question_type": "single_best_answer",
        "curriculum": curriculum,
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


def _make_fake_bank(items: list[dict], collection: str = "public_lab") -> dict:
    return {
        "items": items,
        "collections": {collection: [item["master_item_id"] for item in items]},
    }


def _run_pipeline(
    les: dict,
    memory: dict,
    pool: list[dict],
    session_size: int,
) -> list[dict]:
    """Full adaptive pipeline → selected session items."""
    next_signals = build_next_session_signals(memory, les)
    adaptive_signals = consume_adaptive_signals(next_signals, les, memory)
    plan = compose_adaptive_session_plan(
        session_mode="EXPRESS_10",
        eligibility_pool=pool,
        diagnostic_blueprint={},
        adaptive_signals=adaptive_signals,
    )
    bank = _make_fake_bank(pool)
    return select_sba_session_items(
        bank,
        session_size=session_size,
        question_priorities=plan["question_priorities"],
    )


# ---------------------------------------------------------------------------
# Validation 1: Weak topic increases selection probability
# ---------------------------------------------------------------------------

class TestWeakTopicBoostsSelection(unittest.TestCase):
    """Validation 1: a weak topic in LES causes its items to be selected first."""

    def setUp(self):
        # Pool: 15 neutral items first, then 5 fermentation items
        self.neutral_items = [_make_item(f"OAK_{i:03d}", "oak_aging") for i in range(15)]
        self.weak_items = [_make_item(f"FERM_{i:03d}", "fermentation") for i in range(5)]
        self.pool = self.neutral_items + self.weak_items

        self.les = _fresh_les()
        self.les["topic_signals"]["fermentation"] = {
            "topic": "fermentation",
            "exposure_count": 3,
            "correct_count": 1,
            "incorrect_count": 2,
            "confidence_level": "low",
            "last_seen": "2026-06-01",
        }
        self.memory = _fresh_memory()

    def test_weak_topic_items_selected_over_neutral_items(self):
        selected = _run_pipeline(self.les, self.memory, self.pool, session_size=5)
        selected_ids = {item["master_item_id"] for item in selected}
        expected_ids = {item["master_item_id"] for item in self.weak_items}
        self.assertEqual(selected_ids, expected_ids,
                         "All 5 weak fermentation items should be selected first")

    def test_neutral_items_not_selected_when_weak_items_fill_session(self):
        selected = _run_pipeline(self.les, self.memory, self.pool, session_size=5)
        selected_ids = {item["master_item_id"] for item in selected}
        for item in self.neutral_items:
            self.assertNotIn(item["master_item_id"], selected_ids)

    def test_neutral_learner_selects_first_pool_items(self):
        neutral_les = _fresh_les()
        neutral_memory = _fresh_memory()
        selected = _run_pipeline(neutral_les, neutral_memory, self.pool, session_size=5)
        # Neutral learner: no priority signal → stable sort → first 5 pool items (neutral)
        selected_ids = {item["master_item_id"] for item in selected}
        neutral_ids = {item["master_item_id"] for item in self.neutral_items[:5]}
        self.assertEqual(selected_ids, neutral_ids)

    def test_weak_topic_in_reinforcement_targets(self):
        next_signals = build_next_session_signals(self.memory, self.les)
        adaptive_signals = consume_adaptive_signals(next_signals, self.les, self.memory)
        reinforcement_ids = [t["id"] for t in adaptive_signals["reinforcement_targets"]
                             if t.get("type") == "topic"]
        self.assertIn("fermentation", reinforcement_ids)


# ---------------------------------------------------------------------------
# Validation 2: Persistent misconception → repair targets → affect composition
# ---------------------------------------------------------------------------

class TestMisconceptionRepairTargetsAffectComposition(unittest.TestCase):
    """Validation 2: persistent unresolved MC generates max-priority repair targets
    that cause MC-tagged items to be selected over neutral items."""

    _MC_ID = "MC_REPAIR_TEST_01"

    def setUp(self):
        # Pool: 10 neutral items first, then 5 items tagged with the MC
        self.neutral_items = [_make_item(f"NEUT_MC_{i:03d}", "climate") for i in range(10)]
        self.mc_items = [
            _make_item(f"MC_ITEM_{i:03d}", "acidity", mc_ids=[self._MC_ID])
            for i in range(5)
        ]
        self.pool = self.neutral_items + self.mc_items

        self.les = _fresh_les()
        self.les["misconception_signals"][self._MC_ID] = {
            "misconception_id": self._MC_ID,
            "detection_count": 3,
            "last_detected": "2026-06-01",
        }
        self.les["misconception_sessions"] = {
            self._MC_ID: {"session_ids": ["s1", "s2", "s3"]},
        }
        self.les["misconception_resolution"] = {
            self._MC_ID: {"resolved": False, "resolved_at": None},
        }
        self.memory = _fresh_memory()

    def test_mc_tagged_items_selected_over_neutral(self):
        selected = _run_pipeline(self.les, self.memory, self.pool, session_size=5)
        selected_ids = {item["master_item_id"] for item in selected}
        mc_item_ids = {item["master_item_id"] for item in self.mc_items}
        self.assertEqual(selected_ids, mc_item_ids,
                         "All MC-tagged items should be selected over neutral items")

    def test_mc_in_review_targets(self):
        next_signals = build_next_session_signals(self.memory, self.les)
        adaptive_signals = consume_adaptive_signals(next_signals, self.les, self.memory)
        review_mc_ids = [t["mc_id"] for t in adaptive_signals["review_targets"]
                         if t.get("type") == "misconception"]
        self.assertIn(self._MC_ID, review_mc_ids)

    def test_mc_review_target_has_persistence(self):
        next_signals = build_next_session_signals(self.memory, self.les)
        adaptive_signals = consume_adaptive_signals(next_signals, self.les, self.memory)
        mc_targets = [t for t in adaptive_signals["review_targets"]
                      if t.get("type") == "misconception" and t.get("mc_id") == self._MC_ID]
        self.assertTrue(any(t.get("persistence") for t in mc_targets))

    def test_resolved_mc_no_longer_prioritizes_items(self):
        les = copy.deepcopy(self.les)
        les["misconception_resolution"][self._MC_ID] = {"resolved": True, "resolved_at": "2026-06-02"}
        selected = _run_pipeline(les, self.memory, self.pool, session_size=5)
        selected_ids = {item["master_item_id"] for item in selected}
        # Without MC priority boost, neutral items (first in pool) get selected
        neutral_ids = {item["master_item_id"] for item in self.neutral_items[:5]}
        self.assertEqual(selected_ids, neutral_ids)


# ---------------------------------------------------------------------------
# Validation 3: Causal gap → causal reinforcement → affect composition
# ---------------------------------------------------------------------------

class TestCausalGapReinforcement(unittest.TestCase):
    """Validation 3: a superficial causal chain in LES generates causal reinforcement
    targets, causing items linked to that causal chain to be selected first."""

    _CC_ID = "CC_TEST_WIRE_GAP"

    def setUp(self):
        # Pool: 10 neutral items first, then 5 items tagged with CC
        self.neutral_items = [_make_item(f"NEUT_CC_{i:03d}", "structure") for i in range(10)]
        self.cc_items = [
            _make_item(f"CC_ITEM_{i:03d}", "acidity_chain", cc_ids=[self._CC_ID])
            for i in range(5)
        ]
        self.pool = self.neutral_items + self.cc_items

        self.les = _fresh_les()
        self.les["causal_chain_signals"][self._CC_ID] = {
            "causal_chain_id": self._CC_ID,
            "exposure_count": 2,
            "demonstrated_count": 0,
        }
        self.les["causal_strength"] = {self._CC_ID: "superficial"}
        self.memory = _fresh_memory()

    def test_cc_linked_items_selected_over_neutral(self):
        selected = _run_pipeline(self.les, self.memory, self.pool, session_size=5)
        selected_ids = {item["master_item_id"] for item in selected}
        cc_item_ids = {item["master_item_id"] for item in self.cc_items}
        self.assertEqual(selected_ids, cc_item_ids,
                         "CC-linked items should be selected over neutral items")

    def test_superficial_cc_in_review_targets(self):
        next_signals = build_next_session_signals(self.memory, self.les)
        adaptive_signals = consume_adaptive_signals(next_signals, self.les, self.memory)
        cc_ids_in_review = [t["cc_id"] for t in adaptive_signals["review_targets"]
                            if t.get("type") == "causal_chain"]
        self.assertIn(self._CC_ID, cc_ids_in_review)

    def test_superficial_cc_has_high_gap_priority(self):
        next_signals = build_next_session_signals(self.memory, self.les)
        adaptive_signals = consume_adaptive_signals(next_signals, self.les, self.memory)
        cc_targets = [t for t in adaptive_signals["review_targets"]
                      if t.get("type") == "causal_chain" and t.get("cc_id") == self._CC_ID]
        self.assertTrue(any(t.get("gap_priority") == "high" for t in cc_targets))

    def test_superficial_cc_higher_priority_than_strong_cc(self):
        # Mix pool: 5 STRONG-CC items first, then 5 SUPERFICIAL-CC items (this CC), then 10 neutral
        # superficial → HIGH(60), strong → STANDARD(40), neutral → BASE(10)
        # With session_size=5, superficial-CC items should be selected over strong-CC items
        _CC_STRONG = "CC_TEST_WIRE_STRONG"
        les = copy.deepcopy(self.les)
        les["causal_chain_signals"][_CC_STRONG] = {
            "causal_chain_id": _CC_STRONG,
            "exposure_count": 2,
            "demonstrated_count": 0,
        }
        les["causal_strength"][_CC_STRONG] = "strong"
        # Keep _CC_ID as superficial (from setUp)

        strong_items = [
            _make_item(f"STR_CC_{i:03d}", f"soil_s_{i}", cc_ids=[_CC_STRONG])
            for i in range(5)
        ]
        superficial_items = [
            _make_item(f"SUP_CC_{i:03d}", f"acidity_s_{i}", cc_ids=[self._CC_ID])
            for i in range(5)
        ]
        neutral = [_make_item(f"NEU_CC2_{i:03d}", f"climate_c_{i}") for i in range(10)]
        mixed_pool = strong_items + superficial_items + neutral

        memory = _fresh_memory()
        selected = _run_pipeline(les, memory, mixed_pool, session_size=5)
        selected_ids = {item["master_item_id"] for item in selected}
        superficial_ids = {item["master_item_id"] for item in superficial_items}
        self.assertEqual(selected_ids, superficial_ids,
                         "Superficial-CC items (HIGH=60) should outrank strong-CC items (STANDARD=40)")


# ---------------------------------------------------------------------------
# Validation 4: Strong topic → progression/challenge → reflected in composition
# ---------------------------------------------------------------------------

class TestStrongTopicProgressionReflectedInComposition(unittest.TestCase):
    """Validation 4: a strong topic produces progression + challenge targets that
    cause distinction-level items to rank above foundational-level items."""

    _STRONG_TOPIC = "oak_maturation"

    def setUp(self):
        # Pool: 10 neutral items first, then 1 foundational + 1 distinction for the strong topic.
        # Using only 1 item per strong-topic difficulty avoids the composer's exposure-variation
        # penalty (applied after 2+ same-topic items) which would otherwise cancel the challenge boost.
        self.neutral_items = [_make_item(f"NEUT_STR_{i:03d}", f"climate_{i}") for i in range(10)]
        self.foundational_item = _make_item("FOUND_SINGLE", self._STRONG_TOPIC, difficulty="foundational")
        self.distinction_item = _make_item("DIST_SINGLE", self._STRONG_TOPIC, difficulty="distinction")
        self.pool = self.neutral_items + [self.foundational_item, self.distinction_item]

        self.les = _fresh_les()
        self.les["topic_signals"][self._STRONG_TOPIC] = {
            "topic": self._STRONG_TOPIC,
            "exposure_count": 5,
            "correct_count": 5,
            "incorrect_count": 0,
            "confidence_level": "high",
            "last_seen": "2026-06-01",
        }
        self.memory = _fresh_memory()

    def test_strong_topic_in_progression_targets(self):
        next_signals = build_next_session_signals(self.memory, self.les)
        adaptive_signals = consume_adaptive_signals(next_signals, self.les, self.memory)
        progression_ids = [t["id"] for t in adaptive_signals["progression_targets"]]
        self.assertIn(self._STRONG_TOPIC, progression_ids)

    def test_strong_topic_in_challenge_targets(self):
        next_signals = build_next_session_signals(self.memory, self.les)
        adaptive_signals = consume_adaptive_signals(next_signals, self.les, self.memory)
        challenge_topics = [t.get("topic") or t.get("id")
                            for t in adaptive_signals["challenge_targets"]]
        self.assertIn(self._STRONG_TOPIC, challenge_topics)

    def test_distinction_item_selected_before_foundational(self):
        # session_size=1: only 1 item selected — must be the distinction item (score=20)
        # vs foundational (score=10) and neutral (score=10).
        selected = _run_pipeline(self.les, self.memory, self.pool, session_size=1)
        self.assertEqual(len(selected), 1)
        self.assertEqual(selected[0]["master_item_id"], "DIST_SINGLE",
                         "Distinction item (challenge boost=20) should be selected over foundational (10)")

    def test_progression_rationale_in_plan(self):
        next_signals = build_next_session_signals(self.memory, self.les)
        adaptive_signals = consume_adaptive_signals(next_signals, self.les, self.memory)
        plan = compose_adaptive_session_plan(
            session_mode="EXPRESS_10",
            eligibility_pool=self.pool,
            diagnostic_blueprint={},
            adaptive_signals=adaptive_signals,
        )
        self.assertGreater(plan["progression_rationale"]["ready_for_challenge_count"], 0)
        self.assertGreater(plan["challenge_rationale"]["challenge_candidate_count"], 0)

    def test_distinction_outranks_foundational_in_question_priorities(self):
        next_signals = build_next_session_signals(self.memory, self.les)
        adaptive_signals = consume_adaptive_signals(next_signals, self.les, self.memory)
        plan = compose_adaptive_session_plan(
            session_mode="EXPRESS_10",
            eligibility_pool=self.pool,
            diagnostic_blueprint={},
            adaptive_signals=adaptive_signals,
        )
        pmap = {p["question_id"]: p["priority_score"] for p in plan["question_priorities"]}
        self.assertGreater(pmap.get("DIST_SINGLE", 0), pmap.get("FOUND_SINGLE", 0),
                           "Distinction item must have higher priority_score than foundational")


# ---------------------------------------------------------------------------
# Validation 5: Exposure avoidance — avoid_repetition_ids items do not appear
# ---------------------------------------------------------------------------

class TestExposureAvoidanceBlocksRepeatedItems(unittest.TestCase):
    """Validation 5: items in avoid_repetition_ids do not appear in the session."""

    def setUp(self):
        self.pool = [_make_item(f"EXP_{i:03d}", "tannins") for i in range(20)]

        # Mark first 3 items as over-exposed (>= 2 times each)
        self.avoided_ids = [item["master_item_id"] for item in self.pool[:3]]
        self.les = _fresh_les()
        exposure_log = []
        for qid in self.avoided_ids:
            for _ in range(2):
                exposure_log.append({
                    "question_id": qid,
                    "timestamp": "2026-06-01",
                    "mode": "practice",
                    "result": "correct",
                })
        self.les["question_exposure_log"] = exposure_log
        self.memory = _fresh_memory()

    def test_avoided_items_absent_from_session(self):
        selected = _run_pipeline(self.les, self.memory, self.pool, session_size=10)
        selected_ids = {item["master_item_id"] for item in selected}
        for avoided_id in self.avoided_ids:
            self.assertNotIn(avoided_id, selected_ids,
                             f"{avoided_id} should be absent (over-exposed)")

    def test_all_selected_items_are_non_avoided(self):
        selected = _run_pipeline(self.les, self.memory, self.pool, session_size=10)
        for item in selected:
            self.assertNotIn(item["master_item_id"], self.avoided_ids)

    def test_avoid_repetition_ids_populated_by_consumer(self):
        next_signals = build_next_session_signals(self.memory, self.les)
        adaptive_signals = consume_adaptive_signals(next_signals, self.les, self.memory)
        avoid_ids = set(adaptive_signals["avoid_repetition_ids"])
        for qid in self.avoided_ids:
            self.assertIn(qid, avoid_ids)

    def test_session_size_respected_after_avoidance(self):
        selected = _run_pipeline(self.les, self.memory, self.pool, session_size=5)
        self.assertEqual(len(selected), 5)


# ---------------------------------------------------------------------------
# Validation 6: Adaptive learner gets different composition than neutral learner
# ---------------------------------------------------------------------------

class TestAdaptiveDiffersFromNeutralComposition(unittest.TestCase):
    """Validation 6: a learner with active adaptive signals receives a different
    session composition than a neutral (empty LES) learner given the same pool."""

    def setUp(self):
        # Pool: 15 neutral items FIRST, then 5 weak-signal items LAST
        # Neutral learner → selects first 5 (neutral)
        # Adaptive learner → weak topic boosted → selects last 5 (weak)
        self.neutral_items = [_make_item(f"NEU6_{i:03d}", "geography") for i in range(15)]
        self.weak_items = [_make_item(f"WEK6_{i:03d}", "viticulture") for i in range(5)]
        self.pool = self.neutral_items + self.weak_items

    def _adaptive_les(self) -> dict:
        les = _fresh_les()
        les["topic_signals"]["viticulture"] = {
            "topic": "viticulture",
            "exposure_count": 3,
            "correct_count": 0,
            "incorrect_count": 3,
            "confidence_level": "low",
            "last_seen": "2026-06-01",
        }
        return les

    def test_adaptive_and_neutral_produce_different_sessions(self):
        memory = _fresh_memory()
        adaptive_selected = _run_pipeline(self._adaptive_les(), memory, self.pool, session_size=5)
        neutral_selected = _run_pipeline(_fresh_les(), memory, self.pool, session_size=5)

        adaptive_ids = {item["master_item_id"] for item in adaptive_selected}
        neutral_ids = {item["master_item_id"] for item in neutral_selected}
        self.assertNotEqual(adaptive_ids, neutral_ids,
                            "Adaptive and neutral learners should receive different sessions")

    def test_adaptive_learner_gets_weak_topic_items(self):
        memory = _fresh_memory()
        adaptive_selected = _run_pipeline(self._adaptive_les(), memory, self.pool, session_size=5)
        adaptive_ids = {item["master_item_id"] for item in adaptive_selected}
        weak_ids = {item["master_item_id"] for item in self.weak_items}
        self.assertEqual(adaptive_ids, weak_ids)

    def test_neutral_learner_gets_first_pool_items(self):
        memory = _fresh_memory()
        neutral_selected = _run_pipeline(_fresh_les(), memory, self.pool, session_size=5)
        neutral_ids = {item["master_item_id"] for item in neutral_selected}
        expected_neutral_ids = {item["master_item_id"] for item in self.neutral_items[:5]}
        self.assertEqual(neutral_ids, expected_neutral_ids)

    def test_full_loop_governance_clean(self):
        memory = _fresh_memory()
        next_signals = build_next_session_signals(memory, self._adaptive_les())
        adaptive_signals = consume_adaptive_signals(next_signals, self._adaptive_les(), memory)
        plan = compose_adaptive_session_plan(
            session_mode="EXPRESS_10",
            eligibility_pool=self.pool,
            diagnostic_blueprint={},
            adaptive_signals=adaptive_signals,
        )
        self.assertFalse(plan["governance"]["safe_for_examiner"])
        self.assertFalse(plan["governance"]["examiner_scoring_allowed"])
        self.assertFalse(plan["governance"]["uses_llm"])
        self.assertFalse(plan["governance"]["uses_api"])

    def test_question_priorities_param_default_none_preserves_pool_order(self):
        bank = _make_fake_bank(self.pool)
        selected_default = select_sba_session_items(bank, session_size=5)
        selected_none = select_sba_session_items(bank, session_size=5, question_priorities=None)
        self.assertEqual(
            [item["master_item_id"] for item in selected_default],
            [item["master_item_id"] for item in selected_none],
        )


# ---------------------------------------------------------------------------
# Structural: parameter passthrough and backward-compat
# ---------------------------------------------------------------------------

class TestSelectSbaSessionItemsParameterPassthrough(unittest.TestCase):
    """Structural checks: backward compat, empty priorities, no mutation."""

    def setUp(self):
        self.pool = [_make_item(f"PASS_{i:03d}", "soils") for i in range(10)]
        self.bank = _make_fake_bank(self.pool)

    def test_empty_question_priorities_list_has_no_effect(self):
        selected_no_prio = select_sba_session_items(self.bank, session_size=5)
        selected_empty_prio = select_sba_session_items(
            self.bank, session_size=5, question_priorities=[]
        )
        self.assertEqual(
            [item["master_item_id"] for item in selected_no_prio],
            [item["master_item_id"] for item in selected_empty_prio],
        )

    def test_question_priorities_does_not_mutate_bank(self):
        import copy as _copy
        bank_copy = _copy.deepcopy(self.bank)
        priorities = [{"question_id": f"PASS_{i:03d}", "priority_score": 50 - i} for i in range(10)]
        select_sba_session_items(self.bank, session_size=5, question_priorities=priorities)
        self.assertEqual(self.bank, bank_copy)

    def test_priorities_with_unknown_ids_ignored_gracefully(self):
        priorities = [{"question_id": "UNKNOWN_9999", "priority_score": 100}]
        selected = select_sba_session_items(self.bank, session_size=5, question_priorities=priorities)
        self.assertEqual(len(selected), 5)

    def test_compose_sba_session_accepts_question_priorities(self):
        priorities = [
            {"question_id": item["master_item_id"], "priority_score": 50}
            for item in self.pool
        ]
        session = compose_sba_session(self.bank, session_size=5, question_priorities=priorities)
        self.assertIn("items", session)
        self.assertEqual(len(session["items"]), 5)
        self.assertFalse(session["governance"]["safe_for_examiner"])

    def test_priority_score_int_type_not_required_coerced(self):
        priorities = [{"question_id": "PASS_000", "priority_score": "80"}]
        selected = select_sba_session_items(self.bank, session_size=3, question_priorities=priorities)
        self.assertEqual(len(selected), 3)


if __name__ == "__main__":
    unittest.main()
