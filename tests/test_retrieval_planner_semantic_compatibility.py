"""Phase 3A.7 — semantic compatibility gate for planner causal-chain hints."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import tools.orchestrator.orchestrator as orchestrator
import tools.retrieval.tutor_retrieval_sandbox as retrieval
from tests import test_retrieval_planner_adversarial_negatives as adversarial
from tests import test_retrieval_planner_score_delta as score_delta


MAX_WRONG_HINT_SCORE_DELTA = 0.05
GENERIC_TERMS = {"quality", "wine", "fruit", "taste", "structure", "balance"}

COOL_CHAIN = {
    "node_type": "causal_chain",
    "chain_id": "CC_COOL_CLIMATE_ACIDITY",
    "chain_name": "Cool climate acidity",
    "trigger_keywords": ["cool climate", "slow ripening", "high acidity"],
}

WARM_CHAIN = {
    "node_type": "causal_chain",
    "chain_id": "CC_WARM_CLIMATE_RIPENESS",
    "chain_name": "Warm climate ripeness",
    "trigger_keywords": ["warm climate", "fast ripening", "higher sugar"],
}

TANNIN_CHAIN = {
    "node_type": "causal_chain",
    "chain_id": "CC_TANNIN_EXTRACTION_STRUCTURE",
    "chain_name": "Tannin extraction structure",
    "trigger_keywords": ["extended maceration", "tannin extraction", "structured"],
}

NOBLE_ROT_CHAIN = {
    "node_type": "causal_chain",
    "chain_id": "CC_NOBLE_ROT_QUALITY",
    "chain_name": "Noble rot quality",
    "trigger_keywords": ["noble rot", "flavour complexity", "high quality"],
}

SAT_QUALITY_CHAIN = {
    "node_type": "causal_chain",
    "chain_id": "CC_SAT_QUALITY_BALANCE",
    "chain_name": "SAT quality balance",
    "trigger_keywords": ["quality assessment", "balance", "intensity"],
}


def _query_analysis() -> dict:
    return {
        "query_intent": "cause_effect_explanation",
        "reasoning_intent": "cause_effect",
        "matched_terms": [],
        "matched_concepts": [],
        "matched_causal_chains": [],
        "matched_relationships": [],
        "matched_misconceptions": [],
        "query_expansion_terms": [],
        "query_tokens": [],
        "expanded_query_tokens": [],
    }


class RetrievalPlannerSemanticCompatibilityTests(unittest.TestCase):
    def test_compatible_cool_climate_acidity_query_passes_cool_chain(self):
        self.assertTrue(
            retrieval._is_chain_hint_semantically_compatible(
                "Why does cool climate preserve acidity?",
                COOL_CHAIN,
            )
        )

    def test_fresh_acidity_query_rejects_warm_ripeness_chain(self):
        self.assertFalse(
            retrieval._is_chain_hint_semantically_compatible(
                "Why does fresh acidity matter?",
                WARM_CHAIN,
            )
        )

    def test_sat_quality_query_rejects_quality_balance_chain_when_only_generic_terms_overlap(self):
        self.assertFalse(
            retrieval._is_chain_hint_semantically_compatible(
                "What does quality balance mean in wine tasting?",
                SAT_QUALITY_CHAIN,
            )
        )

    def test_high_tannin_query_rejects_noble_rot_chain(self):
        self.assertFalse(
            retrieval._is_chain_hint_semantically_compatible(
                "Why does red wine feel high in tannin?",
                NOBLE_ROT_CHAIN,
            )
        )

    def test_warm_ripeness_query_passes_warm_ripeness_chain(self):
        self.assertTrue(
            retrieval._is_chain_hint_semantically_compatible(
                "Why does warm climate create ripeness?",
                WARM_CHAIN,
            )
        )

    def test_generic_overlap_alone_is_insufficient(self):
        for term in GENERIC_TERMS:
            with self.subTest(term=term):
                self.assertFalse(
                    retrieval._is_chain_hint_semantically_compatible(
                        f"What does {term} mean?",
                        SAT_QUALITY_CHAIN,
                    )
                )

    def test_unknown_chain_remains_ignored(self):
        with patch.object(retrieval, "ENABLE_PLANNER_CAUSAL_CHAIN_INJECTION", True):
            result = retrieval._inject_planner_causal_chain_hints(
                _query_analysis(),
                ["CC_UNKNOWN"],
                [COOL_CHAIN],
                clean_query="cool climate acidity",
            )
        self.assertEqual(result["matched_causal_chains"], [])

    def test_gate_off_still_returns_unchanged_behavior(self):
        analysis = _query_analysis()
        result = retrieval._inject_planner_causal_chain_hints(
            analysis,
            ["CC_COOL_CLIMATE_ACIDITY"],
            [COOL_CHAIN],
            clean_query="cool climate acidity",
        )
        self.assertIs(result, analysis)
        self.assertEqual(result["matched_causal_chains"], [])

    def test_gate_on_incompatible_hint_does_not_inject(self):
        analysis = _query_analysis()
        with patch.object(retrieval, "ENABLE_PLANNER_CAUSAL_CHAIN_INJECTION", True):
            result = retrieval._inject_planner_causal_chain_hints(
                analysis,
                ["CC_WARM_CLIMATE_RIPENESS"],
                [WARM_CHAIN],
                clean_query="fresh acidity",
            )
        self.assertIs(result, analysis)
        self.assertEqual(result["matched_causal_chains"], [])

    def test_gate_on_compatible_hint_injects(self):
        with patch.object(retrieval, "ENABLE_PLANNER_CAUSAL_CHAIN_INJECTION", True):
            result = retrieval._inject_planner_causal_chain_hints(
                _query_analysis(),
                ["CC_COOL_CLIMATE_ACIDITY"],
                [COOL_CHAIN],
                clean_query="cool climate acidity",
            )
        self.assertEqual(
            [chain["id"] for chain in result["matched_causal_chains"]],
            ["CC_COOL_CLIMATE_ACIDITY"],
        )

    def test_adversarial_failures_from_phase_3a6_are_mitigated(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            adversarial._build_fixture_root(root)
            reports = [
                adversarial._adversarial_report(root, case, suffix=f"_{case['name']}_semantic")
                for case in adversarial.ADVERSARIAL_CASES
            ]
        self.assertFalse([report for report in reports if report["classification"] == "failed"])
        self.assertFalse([report for report in reports if report["classification"] == "near_failed"])

    def test_score_delta_for_wrong_hints_is_below_material_threshold(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            adversarial._build_fixture_root(root)
            for case in adversarial.ADVERSARIAL_CASES:
                with self.subTest(case=case["name"]):
                    report = adversarial._adversarial_report(root, case, suffix=f"_{case['name']}_threshold")
                    self.assertLess(report["score_delta"], MAX_WRONG_HINT_SCORE_DELTA)
                    self.assertEqual(report["causal_score_delta"], 0.0)

    def test_positive_fixtures_still_show_causal_signal_when_compatible(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            score_delta._build_fixture_root(root)
            for case in score_delta.POSITIVE_CASES:
                with self.subTest(case=case["hint_chain_id"]):
                    report = score_delta._score_report(root, case, suffix=f"_{case['hint_chain_id']}_semantic")
                    self.assertGreater(report["experimental_causal_score"], 0)
                    self.assertEqual(report["experimental_hint_ids"], [case["hint_chain_id"]])

    def test_negative_fixtures_do_not_promote_wrong_chunks(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            score_delta._build_fixture_root(root)
            for case in score_delta.NEGATIVE_CASES:
                with self.subTest(case=case["hint_chain_id"]):
                    report = score_delta._score_report(root, case, suffix=f"_{case['target_chunk_id']}_semantic")
                    if case["unrelated_chunk_id"] in report["experimental_top_ids"]:
                        unrelated_rank = report["experimental_top_ids"].index(case["unrelated_chunk_id"]) + 1
                        self.assertLess(report["experimental_rank"], unrelated_rank)
                    self.assertLess(report["score_delta"], MAX_WRONG_HINT_SCORE_DELTA)

    def test_no_scoring_weights_changed(self):
        before = dict(retrieval.SCORE_WEIGHTS)
        retrieval._is_chain_hint_semantically_compatible("cool climate acidity", COOL_CHAIN)
        self.assertEqual(retrieval.SCORE_WEIGHTS, before)

    def test_no_governance_fields_introduced(self):
        with patch.object(retrieval, "ENABLE_PLANNER_CAUSAL_CHAIN_INJECTION", True):
            result = retrieval._inject_planner_causal_chain_hints(
                _query_analysis(),
                ["CC_COOL_CLIMATE_ACIDITY"],
                [COOL_CHAIN],
                clean_query="cool climate acidity",
            )
        for chain in result["matched_causal_chains"]:
            self.assertEqual(set(chain), {"id", "name", "terms"})
            self.assertFalse({"safe_for_examiner", "examiner_scoring_allowed"} & set(chain))

    def test_snapshots_unchanged(self):
        self.assertFalse(orchestrator.ENABLE_PLANNER_QUERY_EXPANSION)
        self.assertFalse(retrieval.ENABLE_PLANNER_CAUSAL_CHAIN_INJECTION)
        for query in (
            "How do I justify quality in SAT?",
            "Why does cool climate produce high acidity?",
            "How should I structure a 10-mark SAT answer?",
        ):
            with self.subTest(query=query):
                expanded = orchestrator._apply_planner_query_hints(
                    query,
                    {"causal_chain_focus": ["CC_WARM_CLIMATE_RIPENESS"]},
                )
                clean, hint_ids = retrieval._parse_planner_query_hints(expanded)
                self.assertEqual(expanded, query)
                self.assertEqual(clean, query)
                self.assertEqual(hint_ids, [])

    def test_defaults_remain_off(self):
        self.assertFalse(orchestrator.ENABLE_PLANNER_QUERY_EXPANSION)
        self.assertFalse(retrieval.ENABLE_PLANNER_CAUSAL_CHAIN_INJECTION)


if __name__ == "__main__":
    unittest.main()
