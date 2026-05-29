"""Phase 3A.3 — controlled planner causal-chain hint injection tests.

The experiment is deliberately default-off.  These tests verify that parsed
planner hint IDs can be converted into native ``matched_causal_chains`` only
when the retrieval-local gate is explicitly enabled, and that the existing
causal-chain scoring path sees those injected chains without new weights.
"""

from __future__ import annotations

import copy
import unittest
from unittest.mock import patch

import tools.retrieval.tutor_retrieval_sandbox as retrieval


GOVERNANCE_KEYS = {
    "safe_for_examiner",
    "examiner_scoring_allowed",
    "examiner_scoring_active",
    "uses_llm",
    "uses_api",
    "uses_embeddings",
    "uses_vector_db",
    "cloud_services_active",
}

CHAIN_A = {
    "node_type": "causal_chain",
    "node_id": "CC_COOL_CLIMATE_ACIDITY",
    "chain_id": "CC_COOL_CLIMATE_ACIDITY",
    "chain_name": "Cool climate acidity",
    "trigger_keywords": ["cool climate", "slow ripening", "high acidity"],
    "starting_factor": {
        "concept_id": "C_COOL_CLIMATE",
        "description": "Cool climate",
    },
    "final_outcome": {
        "concept_id": "C_HIGH_ACIDITY",
        "description": "High acidity",
    },
    "steps": [
        {
            "text": "This full causal-chain prose sentence should never be injected verbatim.",
        }
    ],
    "safe_for_examiner": False,
    "examiner_scoring_allowed": False,
}

CHAIN_B = {
    "node_type": "causal_chain",
    "node_id": "CC_WARM_CLIMATE_RIPENESS",
    "chain_id": "CC_WARM_CLIMATE_RIPENESS",
    "chain_name": "Warm climate ripeness",
    "trigger_keywords": ["warm climate", "fast ripening", "higher sugar"],
    "starting_factor": {
        "concept_id": "C_WARM_CLIMATE",
        "description": "Warm climate",
    },
    "final_outcome": {
        "concept_id": "C_HIGHER_SUGAR",
        "description": "Higher sugar",
    },
    "safe_for_examiner": False,
    "examiner_scoring_allowed": False,
}

NON_CAUSAL_NODE = {
    "node_type": "concept",
    "node_id": "CC_LOOKS_LIKE_CHAIN",
    "concept_id": "CC_LOOKS_LIKE_CHAIN",
    "concept_name": "Not a causal chain",
}


def _query_analysis(**overrides):
    base = {
        "query_intent": "cause_effect_explanation",
        "reasoning_intent": "cause_effect",
        "matched_terms": [],
        "matched_concepts": [],
        "matched_causal_chains": [],
        "matched_relationships": [],
        "matched_misconceptions": [],
        "query_expansion_terms": [],
        "query_tokens": ["cool", "climate"],
        "expanded_query_tokens": ["cool", "climate"],
    }
    base.update(overrides)
    return base


def _inject(query_analysis, hint_ids, nodes=None):
    with patch.object(retrieval, "ENABLE_PLANNER_CAUSAL_CHAIN_INJECTION", True):
        return retrieval._inject_planner_causal_chain_hints(
            query_analysis,
            hint_ids,
            nodes if nodes is not None else [CHAIN_A, CHAIN_B, NON_CAUSAL_NODE],
        )


class PlannerCausalChainInjectionTests(unittest.TestCase):
    def test_gate_off_returns_original_query_analysis_unchanged(self):
        analysis = _query_analysis()
        result = retrieval._inject_planner_causal_chain_hints(
            analysis,
            ["CC_COOL_CLIMATE_ACIDITY"],
            [CHAIN_A],
        )
        self.assertIs(result, analysis)
        self.assertEqual(result, analysis)

    def test_empty_hint_ids_return_unchanged(self):
        analysis = _query_analysis()
        result = _inject(analysis, [])
        self.assertIs(result, analysis)
        self.assertEqual(result["matched_causal_chains"], [])

    def test_unknown_hint_ids_are_ignored(self):
        analysis = _query_analysis()
        result = _inject(analysis, ["CC_UNKNOWN"])
        self.assertIs(result, analysis)
        self.assertEqual(result["matched_causal_chains"], [])

    def test_valid_hint_id_is_injected(self):
        result = _inject(_query_analysis(), ["CC_COOL_CLIMATE_ACIDITY"])
        self.assertEqual(
            [chain["id"] for chain in result["matched_causal_chains"]],
            ["CC_COOL_CLIMATE_ACIDITY"],
        )

    def test_multiple_valid_ids_are_injected_preserving_order(self):
        result = _inject(
            _query_analysis(),
            ["CC_WARM_CLIMATE_RIPENESS", "CC_COOL_CLIMATE_ACIDITY"],
        )
        self.assertEqual(
            [chain["id"] for chain in result["matched_causal_chains"]],
            ["CC_WARM_CLIMATE_RIPENESS", "CC_COOL_CLIMATE_ACIDITY"],
        )

    def test_duplicate_hint_ids_are_deduplicated(self):
        result = _inject(
            _query_analysis(),
            ["CC_COOL_CLIMATE_ACIDITY", "CC_COOL_CLIMATE_ACIDITY"],
        )
        self.assertEqual(len(result["matched_causal_chains"]), 1)

    def test_organically_matched_causal_chains_are_preserved(self):
        organic = {"id": "CC_ORGANIC", "name": "Organic match", "terms": ["organic"]}
        result = _inject(
            _query_analysis(matched_causal_chains=[organic]),
            ["CC_COOL_CLIMATE_ACIDITY"],
        )
        self.assertEqual(result["matched_causal_chains"][0], organic)
        self.assertEqual(result["matched_causal_chains"][1]["id"], "CC_COOL_CLIMATE_ACIDITY")

    def test_hint_does_not_duplicate_organic_match(self):
        organic = {
            "id": "CC_COOL_CLIMATE_ACIDITY",
            "name": "Cool climate acidity",
            "terms": ["cool climate"],
        }
        analysis = _query_analysis(matched_causal_chains=[organic])
        result = _inject(analysis, ["CC_COOL_CLIMATE_ACIDITY"])
        self.assertIs(result, analysis)
        self.assertEqual(result["matched_causal_chains"], [organic])

    def test_input_query_analysis_is_not_mutated(self):
        analysis = _query_analysis()
        before = copy.deepcopy(analysis)
        result = _inject(analysis, ["CC_COOL_CLIMATE_ACIDITY"])
        self.assertEqual(analysis, before)
        self.assertIsNot(result, analysis)

    def test_injected_shape_matches_existing_matched_causal_chain_expectations(self):
        result = _inject(_query_analysis(), ["CC_COOL_CLIMATE_ACIDITY"])
        injected = result["matched_causal_chains"][0]
        self.assertEqual(set(injected), {"id", "name", "terms"})
        self.assertIsInstance(injected["id"], str)
        self.assertIsInstance(injected["name"], str)
        self.assertIsInstance(injected["terms"], list)
        self.assertTrue(all(isinstance(term, str) for term in injected["terms"]))

    def test_no_governance_fields_are_introduced(self):
        result = _inject(_query_analysis(), ["CC_COOL_CLIMATE_ACIDITY"])
        self.assertFalse(GOVERNANCE_KEYS & set(result))
        for chain in result["matched_causal_chains"]:
            self.assertFalse(GOVERNANCE_KEYS & set(chain))

    def test_no_full_causal_chain_prose_is_injected(self):
        result = _inject(_query_analysis(), ["CC_COOL_CLIMATE_ACIDITY"])
        injected = result["matched_causal_chains"][0]
        self.assertNotIn("steps", injected)
        self.assertNotIn("starting_factor", injected)
        self.assertNotIn("final_outcome", injected)
        serialized = repr(injected)
        self.assertNotIn("This full causal-chain prose sentence", serialized)

    def test_no_scoring_weights_are_changed(self):
        before = dict(retrieval.SCORE_WEIGHTS)
        _inject(_query_analysis(), ["CC_COOL_CLIMATE_ACIDITY"])
        self.assertEqual(retrieval.SCORE_WEIGHTS, before)

    def test_retrieval_default_behavior_unchanged_with_gate_off(self):
        query = "Why does cool climate preserve acidity?"
        direct = retrieval.classify_query(query, [], [CHAIN_A])
        result = retrieval._inject_planner_causal_chain_hints(
            direct,
            ["CC_COOL_CLIMATE_ACIDITY"],
            [CHAIN_A],
        )
        self.assertIs(result, direct)
        self.assertEqual(result, direct)
        self.assertFalse(retrieval.ENABLE_PLANNER_CAUSAL_CHAIN_INJECTION)

    def test_snapshots_unchanged_with_gate_off(self):
        snapshot_queries = [
            "How do I justify quality in SAT?",
            "Why does cool climate produce high acidity?",
            "How should I structure a 10-mark SAT answer?",
        ]
        self.assertFalse(retrieval.ENABLE_PLANNER_CAUSAL_CHAIN_INJECTION)
        for query in snapshot_queries:
            with self.subTest(query=query):
                clean, hint_ids = retrieval._parse_planner_query_hints(query)
                analysis = retrieval.classify_query(clean, [], [CHAIN_A])
                result = retrieval._inject_planner_causal_chain_hints(analysis, hint_ids, [CHAIN_A])
                self.assertEqual(clean, query)
                self.assertEqual(hint_ids, [])
                self.assertIs(result, analysis)

    def test_gate_on_injected_chain_is_seen_by_causal_chain_match_score(self):
        result = _inject(_query_analysis(), ["CC_COOL_CLIMATE_ACIDITY"])
        match_scores = retrieval._score_term_and_concept_matches(
            {},
            result,
            "Cool climate causes slow ripening and high acidity.",
        )
        self.assertGreater(match_scores["causal_chain_match_score"], 0.0)
        self.assertIn("Cool climate acidity", match_scores["matched_causal_chains"])


if __name__ == "__main__":
    unittest.main()
