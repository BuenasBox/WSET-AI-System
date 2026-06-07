"""Tests for Phase 3B — WSET L3 topic sequence integration in strategic_planner.

Covers:
  - Sequence JSON file: existence, schema, governance fields, minimum topic count
  - _compute_recommended_next_topics: cold-start empty, no-prereq baseline,
    prerequisite blocking, mastered detection by topic_id, cap, determinism,
    graceful degradation with empty/None sequence
  - run_strategic_planner integration: warm-start populates recommended_next_topics,
    cold-start still returns [], output type is list[str], governance clean

Design constraints:
  - All fixtures are inline.
  - reference_date always passed explicitly for determinism.
  - No retrieval or answer_builder imports.
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from tools.constants import KNOWLEDGE_DIR
from tools.orchestrator.strategic_planner import (
    RECOMMENDED_TOPICS_MAX,
    _TOPIC_SEQUENCE,
    _compute_recommended_next_topics,
    run_strategic_planner,
)

SEQUENCE_PATH = KNOWLEDGE_DIR / "config" / "wset3_topic_sequence.json"
REFERENCE_DATE = "2026-06-07T10:00:00+00:00"

REQUIRED_TOPIC_KEYS = {
    "topic_id",
    "topic_name",
    "domain",
    "sequence_position",
    "difficulty_level",
    "prerequisite_topic_ids",
    "keywords",
}

GOVERNANCE_FORBIDDEN_KEYS = {
    "safe_for_examiner",
    "examiner_scoring_allowed",
    "uses_llm",
    "uses_api",
}


# ---------------------------------------------------------------------------
# Shared inline fixtures
# ---------------------------------------------------------------------------

def _empty_memory() -> dict:
    return {
        "low_mastery_concepts": [],
        "retention_risks": [],
        "recurrent_misconceptions": [],
        "difficult_causal_chains": [],
        "mastered_concepts": [],
        "preferred_depth": "standard",
        "overload_patterns": [],
    }


def _empty_les() -> dict:
    return {
        "learner_id": "test",
        "current_level": "WSET_L3",
        "known_weak_areas": [],
        "recent_misconceptions": [],
        "session_count": 0,
    }


def _memory_with_mastered(concepts: list[str]) -> dict:
    mem = _empty_memory()
    mem["mastered_concepts"] = list(concepts)
    return mem


def _minimal_sequence() -> list[dict]:
    """Tiny inline sequence for unit testing _compute_recommended_next_topics."""
    return [
        {
            "topic_id": "topic_a",
            "topic_name": "Topic A",
            "domain": "test",
            "sequence_position": 1,
            "difficulty_level": 1,
            "prerequisite_topic_ids": [],
            "keywords": ["topic_a", "test_a"],
        },
        {
            "topic_id": "topic_b",
            "topic_name": "Topic B",
            "domain": "test",
            "sequence_position": 2,
            "difficulty_level": 1,
            "prerequisite_topic_ids": ["topic_a"],
            "keywords": ["topic_b", "test_b"],
        },
        {
            "topic_id": "topic_c",
            "topic_name": "Topic C",
            "domain": "test",
            "sequence_position": 3,
            "difficulty_level": 2,
            "prerequisite_topic_ids": ["topic_b"],
            "keywords": ["topic_c"],
        },
        {
            "topic_id": "topic_d",
            "topic_name": "Topic D",
            "domain": "test",
            "sequence_position": 4,
            "difficulty_level": 2,
            "prerequisite_topic_ids": [],
            "keywords": ["topic_d"],
        },
        {
            "topic_id": "topic_e",
            "topic_name": "Topic E",
            "domain": "test",
            "sequence_position": 5,
            "difficulty_level": 3,
            "prerequisite_topic_ids": ["topic_d"],
            "keywords": ["topic_e"],
        },
    ]


# ---------------------------------------------------------------------------
# 1. Sequence file — existence and schema
# ---------------------------------------------------------------------------


class SequenceFileExistsTests(unittest.TestCase):

    def test_sequence_file_exists(self) -> None:
        self.assertTrue(SEQUENCE_PATH.exists(), f"Missing file: {SEQUENCE_PATH}")

    def test_sequence_file_is_valid_json(self) -> None:
        data = json.loads(SEQUENCE_PATH.read_text(encoding="utf-8"))
        self.assertIsInstance(data, dict)

    def test_sequence_has_topics_key(self) -> None:
        data = json.loads(SEQUENCE_PATH.read_text(encoding="utf-8"))
        self.assertIn("topics", data, "wset3_topic_sequence.json must have 'topics' key")

    def test_sequence_has_meta_key(self) -> None:
        data = json.loads(SEQUENCE_PATH.read_text(encoding="utf-8"))
        self.assertIn("_meta", data)

    def test_sequence_has_at_least_ten_topics(self) -> None:
        data = json.loads(SEQUENCE_PATH.read_text(encoding="utf-8"))
        self.assertGreaterEqual(
            len(data["topics"]), 10,
            "Sequence must have at least 10 topics for meaningful recommendations"
        )

    def test_module_level_sequence_is_loaded(self) -> None:
        """_TOPIC_SEQUENCE must be non-empty after successful import."""
        self.assertIsInstance(_TOPIC_SEQUENCE, list)
        self.assertGreater(len(_TOPIC_SEQUENCE), 0, "_TOPIC_SEQUENCE failed to load from JSON")


# ---------------------------------------------------------------------------
# 2. Sequence schema — each topic must have all required fields
# ---------------------------------------------------------------------------


class SequenceSchemaTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        data = json.loads(SEQUENCE_PATH.read_text(encoding="utf-8"))
        cls.topics: list[dict] = data["topics"]

    def test_each_topic_has_required_keys(self) -> None:
        for topic in self.topics:
            with self.subTest(topic_id=topic.get("topic_id", "<missing>")):
                missing = REQUIRED_TOPIC_KEYS - set(topic.keys())
                self.assertEqual(
                    missing, set(),
                    f"Topic {topic.get('topic_id')} missing keys: {missing}"
                )

    def test_topic_ids_are_strings(self) -> None:
        for topic in self.topics:
            with self.subTest(topic_id=topic.get("topic_id")):
                self.assertIsInstance(topic["topic_id"], str)
                self.assertTrue(topic["topic_id"].strip(), "topic_id must not be blank")

    def test_topic_ids_are_unique(self) -> None:
        ids = [t["topic_id"] for t in self.topics]
        self.assertEqual(len(ids), len(set(ids)), f"Duplicate topic_ids: {ids}")

    def test_sequence_positions_are_integers(self) -> None:
        for topic in self.topics:
            with self.subTest(topic_id=topic.get("topic_id")):
                self.assertIsInstance(topic["sequence_position"], int)

    def test_sequence_positions_are_unique(self) -> None:
        positions = [t["sequence_position"] for t in self.topics]
        self.assertEqual(
            len(positions), len(set(positions)),
            f"Duplicate sequence_positions: {positions}"
        )

    def test_difficulty_levels_are_1_to_3(self) -> None:
        for topic in self.topics:
            with self.subTest(topic_id=topic.get("topic_id")):
                self.assertIn(topic["difficulty_level"], {1, 2, 3})

    def test_prerequisite_topic_ids_are_lists(self) -> None:
        for topic in self.topics:
            with self.subTest(topic_id=topic.get("topic_id")):
                self.assertIsInstance(topic["prerequisite_topic_ids"], list)

    def test_all_prerequisites_reference_valid_topic_ids(self) -> None:
        all_ids = {t["topic_id"] for t in self.topics}
        for topic in self.topics:
            for prereq in topic["prerequisite_topic_ids"]:
                with self.subTest(topic_id=topic["topic_id"], prereq=prereq):
                    self.assertIn(
                        prereq, all_ids,
                        f"Topic '{topic['topic_id']}' has unknown prereq '{prereq}'"
                    )

    def test_keywords_are_non_empty_lists(self) -> None:
        for topic in self.topics:
            with self.subTest(topic_id=topic.get("topic_id")):
                self.assertIsInstance(topic["keywords"], list)
                self.assertGreater(
                    len(topic["keywords"]), 0,
                    f"Topic '{topic['topic_id']}' has empty keywords list"
                )

    def test_domains_are_strings(self) -> None:
        for topic in self.topics:
            with self.subTest(topic_id=topic.get("topic_id")):
                self.assertIsInstance(topic["domain"], str)
                self.assertTrue(topic["domain"].strip())

    def test_meta_governance_fields_correct(self) -> None:
        data = json.loads(SEQUENCE_PATH.read_text(encoding="utf-8"))
        meta = data["_meta"]
        self.assertFalse(meta.get("safe_for_examiner", False))
        self.assertFalse(meta.get("examiner_scoring_allowed", False))
        self.assertFalse(meta.get("official", True))
        self.assertTrue(meta.get("formative_only", False))


# ---------------------------------------------------------------------------
# 3. _compute_recommended_next_topics — unit tests with inline sequence
# ---------------------------------------------------------------------------


class RecommendedTopicsEmptySequenceTests(unittest.TestCase):

    def test_empty_sequence_returns_empty_list(self) -> None:
        result = _compute_recommended_next_topics(_empty_memory(), sequence=[])
        self.assertEqual(result, [])

    def test_none_sequence_uses_module_level_sequence(self) -> None:
        """Passing sequence=None should use _TOPIC_SEQUENCE (non-empty after load)."""
        mem = _memory_with_mastered([])
        # We can't assert exact topics since they'd depend on mastered state,
        # but result must be a list.
        result = _compute_recommended_next_topics(mem, sequence=None)
        self.assertIsInstance(result, list)

    def test_all_mastered_returns_empty(self) -> None:
        seq = _minimal_sequence()
        all_ids = [t["topic_id"] for t in seq]
        mem = _memory_with_mastered(all_ids)
        result = _compute_recommended_next_topics(mem, sequence=seq)
        self.assertEqual(result, [])


class RecommendedTopicsNoPrereqTests(unittest.TestCase):
    """When nothing is mastered, only topics with no prerequisites are eligible."""

    def test_empty_mastered_returns_no_prereq_topics_only(self) -> None:
        seq = _minimal_sequence()
        result = _compute_recommended_next_topics(_empty_memory(), sequence=seq)
        # topic_a (pos 1, no prereq) and topic_d (pos 4, no prereq) are eligible
        self.assertIn("topic_a", result)
        # topic_b requires topic_a → must NOT appear
        self.assertNotIn("topic_b", result)
        # topic_c requires topic_b → must NOT appear
        self.assertNotIn("topic_c", result)

    def test_returns_at_most_recommended_topics_max(self) -> None:
        seq = _minimal_sequence()
        result = _compute_recommended_next_topics(_empty_memory(), sequence=seq)
        self.assertLessEqual(len(result), RECOMMENDED_TOPICS_MAX)

    def test_results_ordered_by_sequence_position(self) -> None:
        seq = _minimal_sequence()
        result = _compute_recommended_next_topics(_empty_memory(), sequence=seq)
        # topic_a is position 1, topic_d is position 4 — a must come before d
        if "topic_a" in result and "topic_d" in result:
            self.assertLess(result.index("topic_a"), result.index("topic_d"))


class RecommendedTopicsPrereqBlockingTests(unittest.TestCase):

    def test_prereq_unsatisfied_blocks_topic(self) -> None:
        seq = _minimal_sequence()
        # topic_b requires topic_a — without mastering topic_a, topic_b must not appear
        mem = _empty_memory()
        result = _compute_recommended_next_topics(mem, sequence=seq)
        self.assertNotIn("topic_b", result)

    def test_prereq_satisfied_unlocks_topic(self) -> None:
        seq = _minimal_sequence()
        mem = _memory_with_mastered(["topic_a"])
        result = _compute_recommended_next_topics(mem, sequence=seq)
        # topic_b requires only topic_a → now eligible
        self.assertIn("topic_b", result)
        # topic_a is mastered — should not appear in recommendations
        self.assertNotIn("topic_a", result)

    def test_chain_prereq_requires_transitive_mastery(self) -> None:
        seq = _minimal_sequence()
        # topic_c requires topic_b which requires topic_a
        # Mastering only topic_a is not enough to unlock topic_c
        mem = _memory_with_mastered(["topic_a"])
        result = _compute_recommended_next_topics(mem, sequence=seq)
        self.assertNotIn("topic_c", result)

    def test_all_prereqs_satisfied_unlocks_chained_topic(self) -> None:
        seq = _minimal_sequence()
        mem = _memory_with_mastered(["topic_a", "topic_b"])
        result = _compute_recommended_next_topics(mem, sequence=seq)
        self.assertIn("topic_c", result)

    def test_mastered_topic_not_recommended_again(self) -> None:
        seq = _minimal_sequence()
        mem = _memory_with_mastered(["topic_a"])
        result = _compute_recommended_next_topics(mem, sequence=seq)
        self.assertNotIn("topic_a", result)


class RecommendedTopicsCapTests(unittest.TestCase):

    def test_cap_is_respected_with_many_eligible_topics(self) -> None:
        # Build a sequence with 10 no-prereq topics
        seq = [
            {
                "topic_id": f"topic_{i}",
                "topic_name": f"Topic {i}",
                "domain": "test",
                "sequence_position": i,
                "difficulty_level": 1,
                "prerequisite_topic_ids": [],
                "keywords": [f"topic_{i}"],
            }
            for i in range(1, 11)
        ]
        result = _compute_recommended_next_topics(_empty_memory(), sequence=seq)
        self.assertEqual(len(result), RECOMMENDED_TOPICS_MAX)

    def test_fewer_than_max_returns_all_eligible(self) -> None:
        # Only 2 no-prereq topics — both should be returned (below cap)
        seq = [
            {
                "topic_id": "only_a",
                "topic_name": "Only A",
                "domain": "test",
                "sequence_position": 1,
                "difficulty_level": 1,
                "prerequisite_topic_ids": [],
                "keywords": [],
            },
            {
                "topic_id": "only_b",
                "topic_name": "Only B",
                "domain": "test",
                "sequence_position": 2,
                "difficulty_level": 1,
                "prerequisite_topic_ids": [],
                "keywords": [],
            },
        ]
        result = _compute_recommended_next_topics(_empty_memory(), sequence=seq)
        self.assertEqual(len(result), 2)
        self.assertIn("only_a", result)
        self.assertIn("only_b", result)


class RecommendedTopicsDeterminismTests(unittest.TestCase):

    def test_same_inputs_same_output(self) -> None:
        seq = _minimal_sequence()
        mem = _memory_with_mastered(["topic_a"])
        r1 = _compute_recommended_next_topics(mem, sequence=seq)
        r2 = _compute_recommended_next_topics(mem, sequence=seq)
        self.assertEqual(r1, r2)

    def test_different_mastered_sets_give_different_output(self) -> None:
        seq = _minimal_sequence()
        r1 = _compute_recommended_next_topics(_empty_memory(), sequence=seq)
        r2 = _compute_recommended_next_topics(_memory_with_mastered(["topic_a"]), sequence=seq)
        self.assertNotEqual(r1, r2)

    def test_output_is_list_of_strings(self) -> None:
        seq = _minimal_sequence()
        result = _compute_recommended_next_topics(_empty_memory(), sequence=seq)
        self.assertIsInstance(result, list)
        for item in result:
            self.assertIsInstance(item, str)


# ---------------------------------------------------------------------------
# 4. run_strategic_planner integration — recommended_next_topics
# ---------------------------------------------------------------------------


class PlannerIntegrationRecommendedTests(unittest.TestCase):

    def test_cold_start_recommended_next_topics_is_empty(self) -> None:
        """Cold start must never yield topic recommendations."""
        result = run_strategic_planner(
            memory_summary=None,
            les_context=None,
            reference_date=REFERENCE_DATE,
        )
        self.assertTrue(result["cold_start"])
        self.assertEqual(result["recommended_next_topics"], [])

    def test_warm_start_recommended_next_topics_is_list(self) -> None:
        """Non-cold-start must produce a list (possibly empty if all mastered)."""
        les = _empty_les()
        les["known_weak_areas"] = ["causal_chain:tannin"]
        result = run_strategic_planner(
            memory_summary=_empty_memory(),
            les_context=les,
            reference_date=REFERENCE_DATE,
        )
        self.assertFalse(result["cold_start"])
        self.assertIsInstance(result["recommended_next_topics"], list)

    def test_warm_start_with_empty_mastered_recommends_foundational_topics(self) -> None:
        """With no mastered concepts, planner recommends foundational (no-prereq) topics."""
        les = _empty_les()
        les["known_weak_areas"] = ["causal_chain:tannin"]
        result = run_strategic_planner(
            memory_summary=_empty_memory(),
            les_context=les,
            reference_date=REFERENCE_DATE,
        )
        topics = result["recommended_next_topics"]
        # Foundational WSET L3 topics with no prerequisites should appear
        # (e.g., sat_appearance, viticulture_climate_types, vinification_white_basic)
        self.assertGreater(
            len(topics), 0,
            "Expected at least one foundational topic recommendation for empty mastered set"
        )
        self.assertLessEqual(len(topics), RECOMMENDED_TOPICS_MAX)

    def test_mastered_topic_not_in_recommended(self) -> None:
        """A topic that is mastered must not appear in recommended_next_topics."""
        # sat_appearance is position 1 in the real sequence
        les = _empty_les()
        les["known_weak_areas"] = ["causal_chain:acidity"]
        mem = _memory_with_mastered(["sat_appearance"])
        result = run_strategic_planner(
            memory_summary=mem,
            les_context=les,
            reference_date=REFERENCE_DATE,
        )
        self.assertNotIn("sat_appearance", result["recommended_next_topics"])

    def test_recommended_next_topics_count_within_cap(self) -> None:
        """run_strategic_planner must never return more than RECOMMENDED_TOPICS_MAX topics."""
        les = _empty_les()
        les["known_weak_areas"] = ["causal_chain:oak"]
        result = run_strategic_planner(
            memory_summary=_empty_memory(),
            les_context=les,
            reference_date=REFERENCE_DATE,
        )
        self.assertLessEqual(len(result["recommended_next_topics"]), RECOMMENDED_TOPICS_MAX)

    def test_output_key_still_present_in_schema(self) -> None:
        """recommended_next_topics must always be present in the output dict."""
        for mem, les in [
            (None, None),
            (_empty_memory(), _empty_les()),
            (_memory_with_mastered(["sat_appearance"]), _empty_les()),
        ]:
            with self.subTest(mem_type=type(mem).__name__):
                result = run_strategic_planner(
                    memory_summary=mem,
                    les_context=les,
                    reference_date=REFERENCE_DATE,
                )
                self.assertIn("recommended_next_topics", result)

    def test_planner_output_no_governance_fields(self) -> None:
        """recommended_next_topics strings must not contain governance flag values."""
        les = _empty_les()
        les["known_weak_areas"] = ["causal_chain:tannin"]
        result = run_strategic_planner(
            memory_summary=_empty_memory(),
            les_context=les,
            reference_date=REFERENCE_DATE,
        )
        # The output dict itself must not contain governance flag keys
        for key in GOVERNANCE_FORBIDDEN_KEYS:
            self.assertNotIn(key, result)


if __name__ == "__main__":
    unittest.main()
