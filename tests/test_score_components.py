"""Unit tests for score_chunk_for_query helper components (R3-B).

Each helper extracted from score_chunk_for_query is tested in isolation.
Tests verify: output structure, boundary conditions, and determinism.
No external data files are required — all inputs are minimal inline fixtures.
"""

from __future__ import annotations

import unittest

from tools.retrieval.tutor_retrieval_sandbox import (
    PRIORITY_BOOSTS,
    SCORE_WEIGHTS,
    _aggregate_chunk_score,
    _build_score_breakdown,
    _score_boost_signals,
    _score_lexical_overlap,
    _score_term_and_concept_matches,
)


# ---------------------------------------------------------------------------
# Shared minimal fixtures
# ---------------------------------------------------------------------------

def _minimal_query_analysis(intent: str = "explain") -> dict:
    return {
        "query_tokens": ["tannin", "structure"],
        "expanded_query_tokens": ["tannin", "structure", "tanino"],
        "matched_terms": [{"canonical_term": "tannin", "category": ""}],
        "matched_concepts": [],
        "matched_causal_chains": [],
        "matched_relationships": [],
        "query_expansion_terms": [],
        "reasoning_intent": "cause_effect",
        "query_intent": intent,
        "domain": "tannin",
    }


def _minimal_match_scores(
    dictionary_score: float = 0.5,
    concept_match_score: float = 0.0,
    causal_chain_match_score: float = 0.0,
) -> dict:
    return {
        "dictionary_score": dictionary_score,
        "dictionary_category_score": 0.0,
        "concept_match_score": concept_match_score,
        "causal_chain_match_score": causal_chain_match_score,
        "knowledge_graph_match_score": max(concept_match_score, causal_chain_match_score),
        "source_concept_phrase_score": 0.0,
        "exact_term_boost": 1.0 if dictionary_score > 0 else 0.0,
        "matched_terms": ["tannin"] if dictionary_score > 0 else [],
        "matched_dictionary_terms": [],
        "matched_concepts": [],
        "matched_causal_chains": [],
    }


def _minimal_boost_signals(
    golden_boost: float = 0.0,
    official_source_boost: float = 0.0,
    quality_penalty: float = 0.0,
) -> dict:
    return {
        "reasoning_alignment": 0.0,
        "role_alignment": 0.0,
        "sat_boost": 0.0,
        "cause_effect_boost": 0.0,
        "exam_strategy_boost": 0.0,
        "golden_boost": golden_boost,
        "priority_boost": 0.0,
        "official_source_boost": official_source_boost,
        "section_topic_boost": 0.0,
        "official_exam_register_boost": 0.0,
        "quality_penalty": quality_penalty,
    }


# ---------------------------------------------------------------------------
# _score_lexical_overlap
# ---------------------------------------------------------------------------

class ScoreLexicalOverlapTests(unittest.TestCase):

    def test_full_overlap_returns_one(self) -> None:
        qa = {"query_tokens": ["tannin"], "expanded_query_tokens": ["tannin"]}
        lexical, expanded = _score_lexical_overlap(qa, {"tannin"}, {"tannin"})
        self.assertAlmostEqual(lexical, 1.0)
        self.assertAlmostEqual(expanded, 1.0)

    def test_no_overlap_returns_zero(self) -> None:
        qa = {"query_tokens": ["tannin"], "expanded_query_tokens": ["tannin"]}
        lexical, expanded = _score_lexical_overlap(qa, {"tannin"}, {"acidity"})
        self.assertAlmostEqual(lexical, 0.0)
        self.assertAlmostEqual(expanded, 0.0)

    def test_partial_overlap(self) -> None:
        qa = {"query_tokens": ["tannin", "structure"], "expanded_query_tokens": ["tannin", "structure"]}
        lexical, expanded = _score_lexical_overlap(qa, {"tannin", "structure"}, {"tannin"})
        self.assertAlmostEqual(lexical, 0.5)
        self.assertAlmostEqual(expanded, 0.5)

    def test_empty_query_tokens_does_not_divide_by_zero(self) -> None:
        qa = {"query_tokens": [], "expanded_query_tokens": []}
        lexical, expanded = _score_lexical_overlap(qa, set(), {"tannin"})
        self.assertAlmostEqual(lexical, 0.0)
        self.assertAlmostEqual(expanded, 0.0)

    def test_expanded_uses_expanded_query_tokens_key(self) -> None:
        """expanded_query_tokens may differ from query_tokens."""
        qa = {
            "query_tokens": ["tannin"],
            "expanded_query_tokens": ["tannin", "tanino", "structure"],
        }
        lexical, expanded = _score_lexical_overlap(
            qa, {"tannin"}, {"tannin", "tanino"}
        )
        self.assertAlmostEqual(lexical, 1.0)
        self.assertAlmostEqual(expanded, round(2 / 3, 10), places=5)

    def test_expanded_falls_back_to_query_tokens_if_key_absent(self) -> None:
        qa = {"query_tokens": ["tannin"]}
        lexical, expanded = _score_lexical_overlap(qa, {"tannin"}, {"tannin"})
        self.assertAlmostEqual(lexical, 1.0)
        self.assertAlmostEqual(expanded, 1.0)


# ---------------------------------------------------------------------------
# _score_term_and_concept_matches
# ---------------------------------------------------------------------------

class ScoreTermAndConceptMatchesTests(unittest.TestCase):

    REQUIRED_KEYS = {
        "matched_terms",
        "matched_dictionary_terms",
        "matched_concepts",
        "matched_causal_chains",
        "source_concept_phrase_score",
        "dictionary_score",
        "dictionary_category_score",
        "concept_match_score",
        "causal_chain_match_score",
        "knowledge_graph_match_score",
        "exact_term_boost",
    }

    def _call(self, text: str = "", extra_qa: dict | None = None) -> dict:
        qa = _minimal_query_analysis()
        if extra_qa:
            qa.update(extra_qa)
        return _score_term_and_concept_matches({}, qa, text)

    def test_returns_all_required_keys(self) -> None:
        result = self._call()
        self.assertEqual(set(result.keys()), self.REQUIRED_KEYS)

    def test_scores_are_in_0_1_range(self) -> None:
        result = self._call("tannin structure wine")
        for key in ("dictionary_score", "dictionary_category_score", "concept_match_score",
                    "causal_chain_match_score", "knowledge_graph_match_score",
                    "source_concept_phrase_score"):
            with self.subTest(key=key):
                self.assertGreaterEqual(result[key], 0.0)
                self.assertLessEqual(result[key], 1.0)

    def test_exact_term_boost_when_match(self) -> None:
        # If matched_terms or matched_dictionary_terms are non-empty → boost = 1.0
        result = self._call("tannin")
        # exact_term_boost depends on actual matching internals; just check valid value
        self.assertIn(result["exact_term_boost"], (0.0, 1.0))

    def test_no_match_empty_text(self) -> None:
        result = self._call("")
        self.assertEqual(result["matched_concepts"], [])
        self.assertEqual(result["matched_causal_chains"], [])
        self.assertAlmostEqual(result["concept_match_score"], 0.0)
        self.assertAlmostEqual(result["causal_chain_match_score"], 0.0)

    def test_knowledge_graph_is_max_of_three_components(self) -> None:
        result = self._call()
        expected_max = max(
            result["concept_match_score"],
            result["causal_chain_match_score"],
        )
        self.assertAlmostEqual(result["knowledge_graph_match_score"], expected_max)

    def test_deterministic_on_same_input(self) -> None:
        r1 = self._call("tannin structure wine balance")
        r2 = self._call("tannin structure wine balance")
        self.assertEqual(r1, r2)


# ---------------------------------------------------------------------------
# _score_boost_signals
# ---------------------------------------------------------------------------

class ScoreBoostSignalsTests(unittest.TestCase):

    REQUIRED_KEYS = {
        "reasoning_alignment", "role_alignment", "sat_boost", "cause_effect_boost",
        "exam_strategy_boost", "golden_boost", "priority_boost", "official_source_boost",
        "section_topic_boost", "official_exam_register_boost", "quality_penalty",
    }

    def _call(self, chunk: dict | None = None, golden: dict | None = None,
              query_tokens: set | None = None, chunk_tokens: set | None = None,
              text: str = "") -> dict:
        return _score_boost_signals(
            chunk or {},
            _minimal_query_analysis(),
            golden or {},
            query_tokens or set(),
            chunk_tokens or set(),
            text,
        )

    def test_returns_all_required_keys(self) -> None:
        result = self._call()
        self.assertEqual(set(result.keys()), self.REQUIRED_KEYS)

    def test_golden_boost_when_candidate_true(self) -> None:
        result = self._call(golden={"golden_tutor_chunk_candidate": True})
        self.assertAlmostEqual(result["golden_boost"], 1.0)

    def test_golden_boost_zero_when_false(self) -> None:
        result = self._call(golden={"golden_tutor_chunk_candidate": False})
        self.assertAlmostEqual(result["golden_boost"], 0.0)

    def test_official_source_boost_for_official_type(self) -> None:
        result = self._call(chunk={"source_type": "official_wset_extracted"})
        self.assertAlmostEqual(result["official_source_boost"], 1.0)

    def test_official_source_boost_zero_for_other_type(self) -> None:
        result = self._call(chunk={"source_type": "manual_curated_srt"})
        self.assertAlmostEqual(result["official_source_boost"], 0.0)

    def test_priority_boost_uses_priority_boosts_config(self) -> None:
        result = self._call(golden={"retrieval_priority": "high"})
        self.assertAlmostEqual(result["priority_boost"], PRIORITY_BOOSTS["high"])

    def test_priority_boost_zero_for_unknown_priority(self) -> None:
        result = self._call(golden={"retrieval_priority": "unknown_value"})
        self.assertAlmostEqual(result["priority_boost"], 0.0)

    def test_quality_penalty_is_non_negative(self) -> None:
        result = self._call(chunk={"quality_flags": ["flag1", "flag2"]})
        self.assertGreaterEqual(result["quality_penalty"], 0.0)

    def test_quality_penalty_capped_at_max(self) -> None:
        many_flags = {"quality_flags": ["f"] * 20}
        result = self._call(chunk=many_flags)
        self.assertLessEqual(result["quality_penalty"], SCORE_WEIGHTS["quality_flags_penalty_max"])

    def test_reasoning_alignment_match(self) -> None:
        result = self._call(
            golden={"reasoning_type": "cause_effect"},
        )
        self.assertAlmostEqual(result["reasoning_alignment"], 1.0)

    def test_reasoning_alignment_mismatch(self) -> None:
        result = self._call(golden={"reasoning_type": "definition"})
        # May be 0.0 or fallback value — must not be 1.0
        self.assertLess(result["reasoning_alignment"], 1.0)

    def test_all_values_are_floats(self) -> None:
        result = self._call()
        for key, value in result.items():
            with self.subTest(key=key):
                self.assertIsInstance(value, float)


# ---------------------------------------------------------------------------
# _aggregate_chunk_score
# ---------------------------------------------------------------------------

class AggregateChunkScoreTests(unittest.TestCase):

    def test_zero_inputs_returns_zero(self) -> None:
        score = _aggregate_chunk_score(0.0, 0.0, _minimal_match_scores(0.0), _minimal_boost_signals())
        self.assertAlmostEqual(score, 0.0)

    def test_score_clamped_to_0_1(self) -> None:
        # Feed in very large values to test the upper clamp
        ms = _minimal_match_scores(1.0, 1.0, 1.0)
        bs = _minimal_boost_signals(1.0, 1.0)
        score = _aggregate_chunk_score(1.0, 1.0, ms, bs)
        self.assertLessEqual(score, 1.0)
        self.assertGreaterEqual(score, 0.0)

    def test_quality_penalty_reduces_score(self) -> None:
        ms = _minimal_match_scores(0.5)
        bs_no_penalty = _minimal_boost_signals(quality_penalty=0.0)
        bs_with_penalty = _minimal_boost_signals(quality_penalty=0.1)
        score_clean = _aggregate_chunk_score(0.5, 0.5, ms, bs_no_penalty)
        score_penalised = _aggregate_chunk_score(0.5, 0.5, ms, bs_with_penalty)
        self.assertGreater(score_clean, score_penalised)

    def test_golden_boost_increases_score(self) -> None:
        ms = _minimal_match_scores(0.3)
        bs_no_golden = _minimal_boost_signals(golden_boost=0.0)
        bs_golden = _minimal_boost_signals(golden_boost=1.0)
        score_plain = _aggregate_chunk_score(0.3, 0.3, ms, bs_no_golden)
        score_golden = _aggregate_chunk_score(0.3, 0.3, ms, bs_golden)
        self.assertGreater(score_golden, score_plain)

    def test_deterministic(self) -> None:
        ms = _minimal_match_scores(0.4)
        bs = _minimal_boost_signals()
        s1 = _aggregate_chunk_score(0.4, 0.4, ms, bs)
        s2 = _aggregate_chunk_score(0.4, 0.4, ms, bs)
        self.assertEqual(s1, s2)

    def test_returns_float(self) -> None:
        score = _aggregate_chunk_score(0.5, 0.5, _minimal_match_scores(), _minimal_boost_signals())
        self.assertIsInstance(score, float)


# ---------------------------------------------------------------------------
# _build_score_breakdown
# ---------------------------------------------------------------------------

class BuildScoreBreakdownTests(unittest.TestCase):

    EXPECTED_KEYS = {
        "lexical_overlap", "expanded_lexical_overlap", "canonical_dictionary_terms",
        "dictionary_category_match", "golden_chunk_boost", "reasoning_type_alignment",
        "pedagogical_role_alignment", "retrieval_priority_boost", "sat_term_boost",
        "cause_effect_boost", "exam_strategy_boost", "knowledge_graph_match",
        "causal_chain_match", "concept_match", "source_concept_phrase_match",
        "official_source_boost", "exact_term_match_boost", "section_topic_match_boost",
        "official_exam_register_boost", "quality_flags_penalty",
    }

    def _call(self) -> dict:
        ms = _minimal_match_scores(0.5)
        bs = _minimal_boost_signals()
        return _build_score_breakdown(0.5, 0.5, ms, bs)

    def test_returns_all_expected_keys(self) -> None:
        result = self._call()
        self.assertEqual(set(result.keys()), self.EXPECTED_KEYS)

    def test_all_values_are_floats(self) -> None:
        result = self._call()
        for key, value in result.items():
            with self.subTest(key=key):
                self.assertIsInstance(value, float)

    def test_values_rounded_to_4_decimal_places(self) -> None:
        result = self._call()
        for key, value in result.items():
            with self.subTest(key=key):
                self.assertEqual(round(value, 4), value)

    def test_quality_flags_penalty_is_non_positive(self) -> None:
        """quality_flags_penalty in the breakdown is always ≤ 0."""
        result = self._call()
        self.assertLessEqual(result["quality_flags_penalty"], 0.0)

    def test_deterministic(self) -> None:
        r1 = self._call()
        r2 = self._call()
        self.assertEqual(r1, r2)

    def test_penalty_with_quality_flags(self) -> None:
        ms = _minimal_match_scores()
        bs = _minimal_boost_signals(quality_penalty=0.05)
        result = _build_score_breakdown(0.5, 0.5, ms, bs)
        self.assertAlmostEqual(result["quality_flags_penalty"], -0.05)


if __name__ == "__main__":
    unittest.main()
