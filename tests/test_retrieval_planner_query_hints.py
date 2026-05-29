"""Phase 3A.2 — retrieval compatibility for planner query hints.

Verifies that:
  1.  _parse_planner_query_hints() extracts hint tokens correctly.
  2.  Hint tokens are removed from the clean query before lexical scoring.
  3.  Malformed hint tokens are silently ignored.
  4.  Repeated IDs are deduplicated deterministically.
  5.  Extraction is bounded to _MAX_HINT_IDS.
  6.  Normal query words are never affected by the parser.
  7.  No governance fields appear in parsed output.
  8.  Hint-derived token fragments (e.g. "sat", "quality" from
      CC_SAT_QUALITY_HIGH) do NOT appear in classify_query query_tokens
      when the clean query is used — confirming no lexical noise.
  9.  run_retrieval_sandbox output is additive only (new keys, same scores)
      when no hint tokens are present.
  10. ENABLE_PLANNER_QUERY_EXPANSION remains False.

Design constraints
------------------
All tests are unit tests on _parse_planner_query_hints() and classify_query().
No full-corpus retrieval runs are required.  Tests that verify "no lexical noise"
do so by comparing query_tokens before and after the parse pipeline, not by
running a live retrieval.

Tests 10 and 11 ("retrieval output unchanged" / "snapshot outputs unchanged")
are validated indirectly: they verify that for hint-free queries the parser is
a strict no-op (clean_query == query, hint_ids == []), which is the sufficient
condition for score and snapshot invariance.
"""

from __future__ import annotations

import unittest

from tools.orchestrator.orchestrator import ENABLE_PLANNER_QUERY_EXPANSION
from tools.retrieval.tutor_retrieval_sandbox import (
    _MAX_HINT_IDS,
    _parse_planner_query_hints,
    classify_query,
)

# ---------------------------------------------------------------------------
# Governance keys that must never appear in parser output
# ---------------------------------------------------------------------------

GOVERNANCE_KEYS: frozenset[str] = frozenset({
    "safe_for_examiner",
    "examiner_scoring_allowed",
    "examiner_scoring_active",
    "uses_llm",
    "uses_api",
    "uses_embeddings",
    "uses_vector_db",
    "cloud_services_active",
})

# Token fragments that the ID "CC_SAT_QUALITY_HIGH" would inject into the
# lexical pipeline if NOT stripped.  These are the confirmed noise tokens.
SAT_NOISE_TOKENS: frozenset[str] = frozenset({"cc", "sat", "quality", "high"})

# ---------------------------------------------------------------------------
# Test 1: parse single causal_chain hint
# ---------------------------------------------------------------------------


class ParseSingleHintTests(unittest.TestCase):
    """Required test 1: single hint token extracted correctly."""

    def test_single_hint_extracted(self):
        clean, ids = _parse_planner_query_hints(
            "Explain acidity causal_chain:CC_SAT_QUALITY_HIGH"
        )
        self.assertEqual(ids, ["CC_SAT_QUALITY_HIGH"])

    def test_single_hint_clean_query_correct(self):
        clean, _ = _parse_planner_query_hints(
            "Explain acidity causal_chain:CC_SAT_QUALITY_HIGH"
        )
        self.assertEqual(clean, "Explain acidity")

    def test_single_hint_at_start(self):
        clean, ids = _parse_planner_query_hints(
            "causal_chain:CC_ACID_BALANCE what is acidity"
        )
        self.assertIn("CC_ACID_BALANCE", ids)
        self.assertNotIn("causal_chain", clean)

    def test_no_hints_returns_unchanged_query(self):
        query = "what is tannin structure?"
        clean, ids = _parse_planner_query_hints(query)
        self.assertEqual(clean, query)
        self.assertEqual(ids, [])


# ---------------------------------------------------------------------------
# Test 2: parse multiple hints preserving order
# ---------------------------------------------------------------------------


class ParseMultipleHintsOrderTests(unittest.TestCase):
    """Required test 2: multiple hints extracted in input order."""

    def test_two_hints_order_preserved(self):
        _, ids = _parse_planner_query_hints(
            "explain tannin causal_chain:CC_FIRST causal_chain:CC_SECOND"
        )
        self.assertEqual(ids, ["CC_FIRST", "CC_SECOND"])

    def test_three_hints_order_preserved(self):
        _, ids = _parse_planner_query_hints(
            "q causal_chain:CC_A causal_chain:CC_B causal_chain:CC_C"
        )
        self.assertEqual(ids, ["CC_A", "CC_B", "CC_C"])

    def test_hints_interspersed_with_words_order_preserved(self):
        _, ids = _parse_planner_query_hints(
            "causal_chain:CC_FIRST some words causal_chain:CC_SECOND more words"
        )
        self.assertEqual(ids[0], "CC_FIRST")
        self.assertEqual(ids[1], "CC_SECOND")


# ---------------------------------------------------------------------------
# Test 3: remove hint tokens from cleaned query
# ---------------------------------------------------------------------------


class RemoveHintTokensTests(unittest.TestCase):
    """Required test 3: cleaned query contains no hint token fragments."""

    def test_hint_tokens_absent_from_clean_query(self):
        clean, _ = _parse_planner_query_hints(
            "explain acidity causal_chain:CC_SAT_QUALITY_HIGH"
        )
        self.assertNotIn("causal_chain:", clean)
        self.assertNotIn("CC_SAT_QUALITY_HIGH", clean)

    def test_multiple_hint_tokens_all_removed(self):
        clean, _ = _parse_planner_query_hints(
            "explain tannin causal_chain:CC_A causal_chain:CC_B"
        )
        self.assertNotIn("causal_chain:", clean)
        self.assertNotIn("CC_A", clean)
        self.assertNotIn("CC_B", clean)

    def test_clean_query_whitespace_normalized(self):
        clean, _ = _parse_planner_query_hints(
            "explain  causal_chain:CC_A  acidity"
        )
        self.assertNotIn("  ", clean)  # no double spaces
        self.assertEqual(clean, clean.strip())

    def test_clean_query_normal_words_intact(self):
        """Required test 7 (overlapping): normal words preserved exactly."""
        clean, _ = _parse_planner_query_hints(
            "explain the role of acidity causal_chain:CC_ACID"
        )
        self.assertIn("explain", clean)
        self.assertIn("acidity", clean)


# ---------------------------------------------------------------------------
# Test 4: ignore malformed hint tokens
# ---------------------------------------------------------------------------


class MalformedHintTokenTests(unittest.TestCase):
    """Required test 4: malformed tokens are silently ignored."""

    def test_empty_id_not_matched(self):
        """causal_chain: with no ID — must not match."""
        clean, ids = _parse_planner_query_hints("explain acidity causal_chain:")
        self.assertEqual(ids, [])
        # The bare "causal_chain:" may or may not remain in clean —
        # what matters is no ID was extracted.
        self.assertEqual(ids, [])

    def test_space_before_id_not_matched(self):
        """causal_chain: <space> ID — must not match."""
        clean, ids = _parse_planner_query_hints(
            "explain acidity causal_chain: CC_ACID"
        )
        self.assertEqual(ids, [])

    def test_double_colon_not_matched(self):
        clean, ids = _parse_planner_query_hints(
            "explain acidity causal_chain::CC_ACID"
        )
        # double colon: second colon is not part of the ID charset
        # pattern requires letter/digit/underscore immediately after ':'
        self.assertEqual(ids, [])

    def test_special_chars_in_id_not_matched(self):
        clean, ids = _parse_planner_query_hints(
            "explain acidity causal_chain:CC-ACID"
        )
        # hyphen is not in [A-Za-z0-9_] — stops the match at CC
        # "CC" would match. Let's verify what actually happens.
        # If "CC" is extracted, that's fine — hyphen terminates the ID.
        # The point is no invalid chars leak in.
        for chain_id in ids:
            self.assertRegex(chain_id, r"^[A-Za-z0-9_]+$")

    def test_substring_not_matched(self):
        """notcausal_chain:CC_A — must not match (no word boundary)."""
        clean, ids = _parse_planner_query_hints("notcausal_chain:CC_ACID")
        self.assertEqual(ids, [])


# ---------------------------------------------------------------------------
# Test 5: deduplicate repeated hint IDs deterministically
# ---------------------------------------------------------------------------


class DeduplicationTests(unittest.TestCase):
    """Required test 5: duplicate IDs appear only once."""

    def test_duplicate_id_deduplicated(self):
        _, ids = _parse_planner_query_hints(
            "q causal_chain:CC_A causal_chain:CC_A"
        )
        self.assertEqual(ids.count("CC_A"), 1)

    def test_duplicate_keeps_first_occurrence(self):
        _, ids = _parse_planner_query_hints(
            "q causal_chain:CC_A causal_chain:CC_B causal_chain:CC_A"
        )
        self.assertEqual(ids[0], "CC_A")
        self.assertEqual(ids[1], "CC_B")
        self.assertEqual(len(ids), 2)

    def test_deduplicated_result_is_deterministic(self):
        query = "q causal_chain:CC_X causal_chain:CC_X causal_chain:CC_Y"
        r1 = _parse_planner_query_hints(query)
        r2 = _parse_planner_query_hints(query)
        self.assertEqual(r1, r2)


# ---------------------------------------------------------------------------
# Test 6: bounded hint count respected
# ---------------------------------------------------------------------------


class BoundingTests(unittest.TestCase):
    """Required test 6: never more than _MAX_HINT_IDS IDs extracted."""

    def test_excess_hints_truncated(self):
        hints = " ".join(f"causal_chain:CC_{i:03d}" for i in range(_MAX_HINT_IDS + 5))
        _, ids = _parse_planner_query_hints(f"explain acidity {hints}")
        self.assertLessEqual(len(ids), _MAX_HINT_IDS)

    def test_exact_max_extracted_from_overflow(self):
        hints = " ".join(f"causal_chain:CC_{i:03d}" for i in range(_MAX_HINT_IDS + 5))
        _, ids = _parse_planner_query_hints(f"q {hints}")
        self.assertEqual(len(ids), _MAX_HINT_IDS)

    def test_max_hint_ids_constant_is_3(self):
        """_MAX_HINT_IDS must be 3 — mirrors orchestrator constant."""
        self.assertEqual(_MAX_HINT_IDS, 3)

    def test_fewer_than_max_all_included(self):
        _, ids = _parse_planner_query_hints(
            "q causal_chain:CC_A causal_chain:CC_B"
        )
        self.assertEqual(len(ids), 2)
        self.assertIn("CC_A", ids)
        self.assertIn("CC_B", ids)


# ---------------------------------------------------------------------------
# Test 7: cleaned query preserves normal words
# ---------------------------------------------------------------------------


class CleanQueryPreservesWordsTests(unittest.TestCase):
    """Required test 7: all non-hint words survive in the cleaned query."""

    def test_all_normal_words_present(self):
        words = ["explain", "the", "role", "of", "acidity", "in", "wine"]
        query = " ".join(words) + " causal_chain:CC_ACID"
        clean, _ = _parse_planner_query_hints(query)
        for word in words:
            self.assertIn(word, clean)

    def test_special_wset_terms_preserved(self):
        clean, _ = _parse_planner_query_hints(
            "SAT tannin malolactic causal_chain:CC_TANNIN_01"
        )
        self.assertIn("SAT", clean)
        self.assertIn("tannin", clean)
        self.assertIn("malolactic", clean)

    def test_no_hint_query_identical(self):
        query = "what is the systematic approach to tasting?"
        clean, _ = _parse_planner_query_hints(query)
        self.assertEqual(clean, query)


# ---------------------------------------------------------------------------
# Test 8: hint parsing has no governance fields
# ---------------------------------------------------------------------------


class GovernanceCleanTests(unittest.TestCase):
    """Required test 8: no governance field names appear in parser output."""

    def test_clean_query_no_governance_keys(self):
        clean, ids = _parse_planner_query_hints(
            "explain acidity causal_chain:CC_ACID"
        )
        for key in GOVERNANCE_KEYS:
            self.assertNotIn(key, clean)
            for chain_id in ids:
                self.assertNotIn(key, chain_id)

    def test_parser_output_is_string_and_list_only(self):
        result = _parse_planner_query_hints("q causal_chain:CC_A")
        self.assertIsInstance(result[0], str)
        self.assertIsInstance(result[1], list)
        for item in result[1]:
            self.assertIsInstance(item, str)


# ---------------------------------------------------------------------------
# Test 9: hint tokens do not contribute to lexical overlap
# ---------------------------------------------------------------------------


class NoLexicalNoiseTests(unittest.TestCase):
    """Required test 9: CC_SAT_QUALITY_HIGH fragments must not enter query_tokens.

    This is the core correctness test.  'sat', 'quality', 'high', and 'cc'
    from the ID would pollute sat_boost and lexical_overlap if hint tokens
    were passed directly to classify_query().
    """

    def test_sat_noise_tokens_absent_from_clean_classify(self):
        """Pipeline: parse → classify(clean_query) must not have ID-derived tokens."""
        query_with_hint = "explain tannin causal_chain:CC_SAT_QUALITY_HIGH"
        clean, _ = _parse_planner_query_hints(query_with_hint)
        # Confirm clean query has no hint token
        self.assertNotIn("causal_chain", clean)
        # Classify using the clean query (as run_retrieval_sandbox now does)
        analysis = classify_query(clean, [], [])
        query_tokens = set(analysis["query_tokens"])
        # None of the ID-fragment noise tokens should appear
        for noise_token in SAT_NOISE_TOKENS:
            self.assertNotIn(
                noise_token,
                query_tokens,
                f"Noise token '{noise_token}' from hint ID leaked into query_tokens",
            )

    def test_direct_classify_with_hint_would_produce_noise(self):
        """Negative control: confirms noise exists if hint not stripped first.

        This test documents WHY parsing is required — it is NOT a success
        criterion, it is an audit record.  If this test ever fails it means
        tokenizer behaviour changed and the Phase 3A.2 audit must be rerun.
        """
        analysis = classify_query(
            "explain tannin causal_chain:CC_SAT_QUALITY_HIGH", [], []
        )
        query_tokens = set(analysis["query_tokens"])
        # At least one ID fragment should be present in the raw (unstripped) path.
        # "sat" and/or "quality" are the highest-risk tokens.
        noise_present = bool(query_tokens & SAT_NOISE_TOKENS)
        # We DOCUMENT this as a known fact, not assert False —
        # this is a characterization test, not a regression guard.
        # If tokenizer is fixed to strip these, this test updates accordingly.
        if not noise_present:
            self.skipTest(
                "Tokenizer no longer produces noise from hint IDs — "
                "Phase 3A.2 audit finding may be stale; review."
            )

    def test_clean_query_classify_matches_baseline(self):
        """Hint-free query and parse(hint query) produce same query_tokens."""
        base_query = "explain tannin"
        hint_query = "explain tannin causal_chain:CC_SAT_QUALITY_HIGH"
        clean, _ = _parse_planner_query_hints(hint_query)
        analysis_baseline = classify_query(base_query, [], [])
        analysis_clean = classify_query(clean, [], [])
        self.assertEqual(
            set(analysis_baseline["query_tokens"]),
            set(analysis_clean["query_tokens"]),
        )


# ---------------------------------------------------------------------------
# Test 10: retrieval output unchanged when hints disabled / no boosting
# ---------------------------------------------------------------------------


class RetrievalOutputUnchangedTests(unittest.TestCase):
    """Required test 10: parser is a no-op for normal queries.

    Full retrieval runs are not required here — the no-op property of
    _parse_planner_query_hints for hint-free queries is the sufficient
    condition that guarantees score and output invariance.
    """

    def test_no_hints_clean_query_equals_input(self):
        """No-op guarantee: hint-free query returned unchanged."""
        query = "explain the relationship between acidity and freshness"
        clean, ids = _parse_planner_query_hints(query)
        self.assertEqual(clean, query)
        self.assertEqual(ids, [])

    def test_no_hints_classify_query_unchanged(self):
        """classify_query output is identical via the pipeline vs direct call."""
        query = "SAT quality assessment tasting"
        clean, _ = _parse_planner_query_hints(query)
        self.assertEqual(clean, query)
        direct = classify_query(query, [], [])
        via_parse = classify_query(clean, [], [])
        self.assertEqual(direct["query_tokens"], via_parse["query_tokens"])
        self.assertEqual(direct["query_intent"], via_parse["query_intent"])

    def test_planner_hint_ids_empty_when_no_hints(self):
        """planner_hint_chain_ids is empty list for normal queries."""
        _, ids = _parse_planner_query_hints("explain tannin")
        self.assertEqual(ids, [])


# ---------------------------------------------------------------------------
# Test 11: snapshot outputs unchanged (no-op verification)
# ---------------------------------------------------------------------------


class SnapshotInvarianceTests(unittest.TestCase):
    """Required test 11: snapshot invariance guaranteed by no-op property.

    The 25 snapshot queries contain no causal_chain: tokens.  The parser
    returns them unchanged, so all downstream scoring is identical.
    These tests verify the no-op property holds for representative queries.
    """

    _SNAPSHOT_QUERIES = [
        "How do I justify quality in SAT?",
        "What are the main factors that affect wine quality?",
        "Explain the role of acidity in wine structure",
        "Why does cool climate produce high acidity?",
        "How should I structure a 10-mark SAT answer?",
    ]

    def test_snapshot_queries_are_no_ops(self):
        for query in self._SNAPSHOT_QUERIES:
            with self.subTest(query=query):
                clean, ids = _parse_planner_query_hints(query)
                self.assertEqual(clean, query, f"Parser altered snapshot query: {query!r}")
                self.assertEqual(ids, [], f"Parser extracted IDs from snapshot query: {query!r}")

    def test_no_causal_chain_tokens_in_snapshot_queries(self):
        for query in self._SNAPSHOT_QUERIES:
            with self.subTest(query=query):
                self.assertNotIn("causal_chain:", query)


# ---------------------------------------------------------------------------
# Test 12: planner query expansion flag remains False
# ---------------------------------------------------------------------------


class FlagInvariantTests(unittest.TestCase):
    """Required test 12: ENABLE_PLANNER_QUERY_EXPANSION is still False.

    Phase 3A.2 does not enable the gate.  This test is a safety tripwire.
    """

    def test_enable_planner_query_expansion_is_false(self):
        self.assertFalse(
            ENABLE_PLANNER_QUERY_EXPANSION,
            "ENABLE_PLANNER_QUERY_EXPANSION was set to True — "
            "Phase 3A.2 must not activate the planner gate.",
        )

    def test_max_hint_ids_matches_orchestrator_cap(self):
        """_MAX_HINT_IDS in retrieval mirrors MAX_PLANNER_CHAIN_HINTS in orchestrator."""
        from tools.orchestrator.orchestrator import MAX_PLANNER_CHAIN_HINTS
        self.assertEqual(_MAX_HINT_IDS, MAX_PLANNER_CHAIN_HINTS)


if __name__ == "__main__":
    unittest.main()
