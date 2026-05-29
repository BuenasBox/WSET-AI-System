"""Phase 3A.4 — controlled A/B retrieval comparison for planner hints.

This is a measurement harness only.  It runs baseline retrieval with both
planner influence gates off, then experimental retrieval with both gates
patched on inside the test scope.  No production defaults are changed.
"""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import tools.orchestrator.orchestrator as orchestrator
import tools.retrieval.tutor_retrieval_sandbox as retrieval


GOVERNANCE_KEYS = {
    "examiner_scoring_allowed",
    "examiner_scoring_active",
    "uses_llm",
    "uses_api",
    "uses_embeddings",
    "uses_vector_db",
    "cloud_services_active",
}

PROSE_SENTINEL = "full causal-chain prose should not appear in injected matches"

CASES = [
    {
        "query": "Why does wine taste fresh?",
        "hint_chain_id": "CC_COOL_CLIMATE_ACIDITY",
        "expected_relevant_id": "cool-acidity-mechanism",
        "must_not_promote": ["sat-quality-unrelated", "warm-ripeness-mechanism"],
    },
    {
        "query": "Why can fruit taste riper?",
        "hint_chain_id": "CC_WARM_CLIMATE_RIPENESS",
        "expected_relevant_id": "warm-ripeness-mechanism",
        "must_not_promote": ["sat-quality-unrelated", "cool-acidity-mechanism"],
    },
]


def _chunk(chunk_id: str, text: str, role: str = "theory_explanation") -> dict:
    return {
        "chunk_id": chunk_id,
        "source_type": "manual_curated_srt",
        "agent_corpus": "tutor",
        "safe_for_examiner": False,
        "safe_for_tutor": True,
        "academic_level": "WSET_L3",
        "pedagogical_role": role,
        "video_title_guess": "Phase 3A.4 Fixture",
        "source_filename": "phase_3a4_fixture.srt",
        "text": text,
        "quality_flags": [],
        "sat_terms": [],
        "exam_terms": [],
        "topics_detected": ["viticulture"],
    }


def _write_jsonl(path: Path, rows: list[dict]) -> None:
    path.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def _build_fixture_root(root: Path) -> None:
    chunk_dir = root / "knowledge" / "wine-with-jimmy" / "chunk-ready"
    golden_dir = root / "knowledge" / "wine-with-jimmy" / "manual-import" / "reports"
    dictionary_dir = root / "knowledge" / "enrichment" / "wset_master_dictionary" / "consolidated"
    chain_dir = root / "knowledge" / "knowledge-map" / "causal-chains"
    chunk_dir.mkdir(parents=True)
    golden_dir.mkdir(parents=True)
    dictionary_dir.mkdir(parents=True)
    chain_dir.mkdir(parents=True)

    _write_jsonl(
        chunk_dir / "phase_3a4.chunks.jsonl",
        [
            _chunk(
                "cool-acidity-mechanism",
                "Cool climate causes slow ripening and high acidity, so the wine tastes fresh.",
            ),
            _chunk(
                "warm-ripeness-mechanism",
                "Warm climate causes fast ripening and higher sugar, so fruit can taste riper.",
            ),
            _chunk(
                "sat-quality-unrelated",
                "SAT quality assessment considers balance, intensity, complexity, length and readiness.",
                role="tasting_practice",
            ),
            _chunk(
                "freshness-generic",
                "Freshness can be a tasting impression, but this note gives no mechanism.",
            ),
        ],
    )
    _write_jsonl(golden_dir / "golden_tutor_chunk_candidates.jsonl", [])
    _write_jsonl(dictionary_dir / "canonical_terms_master.jsonl", [])

    (chain_dir / "cc_cool_climate_acidity.json").write_text(
        json.dumps(
            {
                "node_type": "causal_chain",
                "chain_id": "CC_COOL_CLIMATE_ACIDITY",
                "chain_name": "Cool climate acidity",
                "trigger_keywords": ["cool climate", "slow ripening", "high acidity"],
                "safe_for_examiner": False,
                "examiner_scoring_allowed": False,
                "note": PROSE_SENTINEL,
            },
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    (chain_dir / "cc_warm_climate_ripeness.json").write_text(
        json.dumps(
            {
                "node_type": "causal_chain",
                "chain_id": "CC_WARM_CLIMATE_RIPENESS",
                "chain_name": "Warm climate ripeness",
                "trigger_keywords": ["warm climate", "fast ripening", "higher sugar"],
                "safe_for_examiner": False,
                "examiner_scoring_allowed": False,
                "note": PROSE_SENTINEL,
            },
            sort_keys=True,
        ),
        encoding="utf-8",
    )


def _expanded_query(case: dict) -> str:
    plan = {"causal_chain_focus": [case["hint_chain_id"]]}
    return orchestrator._apply_planner_query_hints(case["query"], plan)


def _run_baseline(root: Path, case: dict, suffix: str = "") -> dict:
    baseline_query = _expanded_query(case)
    return retrieval.run_retrieval_sandbox(
        root,
        baseline_query,
        top_k=4,
        output_prefix=f"phase_3a4_baseline{suffix}",
    )


def _run_experimental(root: Path, case: dict, suffix: str = "") -> dict:
    with (
        patch.object(orchestrator, "ENABLE_PLANNER_QUERY_EXPANSION", True),
        patch.object(retrieval, "ENABLE_PLANNER_CAUSAL_CHAIN_INJECTION", True),
    ):
        experimental_query = _expanded_query(case)
        return retrieval.run_retrieval_sandbox(
            root,
            experimental_query,
            top_k=4,
            output_prefix=f"phase_3a4_experimental{suffix}",
        )


def _top_ids(run: dict) -> list[str]:
    return [chunk["chunk_id"] for chunk in run["retrieved_chunks"]]


def _rank(ids: list[str], chunk_id: str) -> int | None:
    try:
        return ids.index(chunk_id) + 1
    except ValueError:
        return None


def _rank_delta(baseline_ids: list[str], experimental_ids: list[str]) -> list[dict]:
    rows = []
    for chunk_id in sorted(set(baseline_ids) | set(experimental_ids)):
        baseline_rank = _rank(baseline_ids, chunk_id)
        experimental_rank = _rank(experimental_ids, chunk_id)
        delta = None
        if baseline_rank is not None and experimental_rank is not None:
            delta = experimental_rank - baseline_rank
        rows.append(
            {
                "chunk_id": chunk_id,
                "baseline_rank": baseline_rank,
                "experimental_rank": experimental_rank,
                "delta": delta,
            }
        )
    return rows


def _chunk_by_id(run: dict, chunk_id: str) -> dict:
    return next(chunk for chunk in run["retrieved_chunks"] if chunk["chunk_id"] == chunk_id)


def _causal_signal_visible(run: dict, chunk_id: str) -> bool:
    chunk = _chunk_by_id(run, chunk_id)
    return (
        chunk["scoring_breakdown"]["causal_chain_match"] > 0
        and bool(chunk["matched_causal_chains"])
    )


def _governance_safe(run: dict) -> bool:
    if not run.get("governance_filter_applied"):
        return False
    for chunk in run["retrieved_chunks"]:
        if chunk.get("safe_for_examiner") is not False:
            return False
        if chunk.get("agent_corpus") != "tutor":
            return False
        if GOVERNANCE_KEYS & set(chunk):
            return False
    for chain in run["query_analysis"].get("matched_causal_chains", []):
        if GOVERNANCE_KEYS & set(chain):
            return False
    return True


def _comparison_report(root: Path, case: dict, suffix: str = "") -> dict:
    baseline = _run_baseline(root, case, suffix=suffix)
    experimental = _run_experimental(root, case, suffix=suffix)
    baseline_ids = _top_ids(baseline)
    experimental_ids = _top_ids(experimental)
    return {
        "query": case["query"],
        "hint_chain_id": case["hint_chain_id"],
        "baseline_top_ids": baseline_ids,
        "experimental_top_ids": experimental_ids,
        "rank_delta": _rank_delta(baseline_ids, experimental_ids),
        "baseline_hint_ids": baseline["planner_hint_chain_ids"],
        "experimental_hint_ids": experimental["planner_hint_chain_ids"],
        "expected_signal_present": _causal_signal_visible(experimental, case["expected_relevant_id"]),
        "baseline_signal_present": _causal_signal_visible(baseline, case["expected_relevant_id"]),
        "governance_safe": _governance_safe(experimental),
    }


class RetrievalPlannerABComparisonTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        _build_fixture_root(self.root)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_baseline_and_experimental_runs_are_both_deterministic(self):
        for case in CASES:
            with self.subTest(case=case["hint_chain_id"]):
                first = _comparison_report(self.root, case, suffix="_det1")
                second = _comparison_report(self.root, case, suffix="_det2")
                self.assertEqual(first, second)

    def test_baseline_run_has_both_gates_off(self):
        self.assertFalse(orchestrator.ENABLE_PLANNER_QUERY_EXPANSION)
        self.assertFalse(retrieval.ENABLE_PLANNER_CAUSAL_CHAIN_INJECTION)
        run = _run_baseline(self.root, CASES[0], suffix="_baseline_flags")
        self.assertEqual(run["query"], CASES[0]["query"])
        self.assertEqual(run["planner_hint_chain_ids"], [])

    def test_experimental_run_enables_gates_only_inside_test_scope(self):
        case = CASES[0]
        with (
            patch.object(orchestrator, "ENABLE_PLANNER_QUERY_EXPANSION", True),
            patch.object(retrieval, "ENABLE_PLANNER_CAUSAL_CHAIN_INJECTION", True),
        ):
            self.assertTrue(orchestrator.ENABLE_PLANNER_QUERY_EXPANSION)
            self.assertTrue(retrieval.ENABLE_PLANNER_CAUSAL_CHAIN_INJECTION)
            query = _expanded_query(case)
            run = retrieval.run_retrieval_sandbox(
                self.root,
                query,
                top_k=4,
                output_prefix="phase_3a4_scope",
            )
            self.assertEqual(run["planner_hint_chain_ids"], [case["hint_chain_id"]])
        self.assertFalse(orchestrator.ENABLE_PLANNER_QUERY_EXPANSION)
        self.assertFalse(retrieval.ENABLE_PLANNER_CAUSAL_CHAIN_INJECTION)

    def test_global_defaults_remain_off_after_test(self):
        _run_experimental(self.root, CASES[0], suffix="_defaults")
        self.assertFalse(orchestrator.ENABLE_PLANNER_QUERY_EXPANSION)
        self.assertFalse(retrieval.ENABLE_PLANNER_CAUSAL_CHAIN_INJECTION)

    def test_experimental_run_exposes_planner_hint_chain_ids(self):
        for case in CASES:
            with self.subTest(case=case["hint_chain_id"]):
                run = _run_experimental(self.root, case, suffix=f"_{case['hint_chain_id']}_hint")
                self.assertEqual(run["planner_hint_chain_ids"], [case["hint_chain_id"]])

    def test_experimental_run_injects_valid_hint_into_matched_causal_chains(self):
        for case in CASES:
            with self.subTest(case=case["hint_chain_id"]):
                run = _run_experimental(self.root, case, suffix=f"_{case['hint_chain_id']}_inject")
                chain_ids = [
                    chain["id"]
                    for chain in run["query_analysis"]["matched_causal_chains"]
                ]
                self.assertIn(case["hint_chain_id"], chain_ids)

    def test_experimental_run_shows_causal_chain_match_signal_when_applicable(self):
        for case in CASES:
            with self.subTest(case=case["hint_chain_id"]):
                run = _run_experimental(self.root, case, suffix=f"_{case['hint_chain_id']}_signal")
                self.assertTrue(_causal_signal_visible(run, case["expected_relevant_id"]))

    def test_baseline_run_does_not_show_planner_injected_causal_chain_match(self):
        for case in CASES:
            with self.subTest(case=case["hint_chain_id"]):
                run = _run_baseline(self.root, case, suffix=f"_{case['hint_chain_id']}_baseline_signal")
                self.assertFalse(_causal_signal_visible(run, case["expected_relevant_id"]))
                self.assertEqual(run["planner_hint_chain_ids"], [])

    def test_top_result_list_remains_governance_safe(self):
        for case in CASES:
            with self.subTest(case=case["hint_chain_id"]):
                report = _comparison_report(self.root, case, suffix=f"_{case['hint_chain_id']}_gov")
                self.assertTrue(report["governance_safe"])

    def test_experimental_run_does_not_introduce_examiner_scoring_fields(self):
        run = _run_experimental(self.root, CASES[0], suffix="_fields")
        self.assertTrue(_governance_safe(run))
        for chain in run["query_analysis"]["matched_causal_chains"]:
            self.assertFalse(GOVERNANCE_KEYS & set(chain))

    def test_experimental_run_does_not_include_full_causal_chain_prose(self):
        run = _run_experimental(self.root, CASES[0], suffix="_prose")
        for chain in run["query_analysis"]["matched_causal_chains"]:
            self.assertEqual(set(chain), {"id", "name", "terms"})
            self.assertNotIn(PROSE_SENTINEL, repr(chain))

    def test_ranking_delta_is_bounded_and_inspectable(self):
        for case in CASES:
            with self.subTest(case=case["hint_chain_id"]):
                report = _comparison_report(self.root, case, suffix=f"_{case['hint_chain_id']}_delta")
                self.assertIsInstance(report["rank_delta"], list)
                self.assertGreaterEqual(len(report["rank_delta"]), 1)
                for row in report["rank_delta"]:
                    self.assertEqual(set(row), {"chunk_id", "baseline_rank", "experimental_rank", "delta"})
                    if row["delta"] is not None:
                        self.assertLessEqual(abs(row["delta"]), 4)

    def test_unrelated_topics_are_not_promoted_above_expected_relevant_results(self):
        for case in CASES:
            with self.subTest(case=case["hint_chain_id"]):
                report = _comparison_report(self.root, case, suffix=f"_{case['hint_chain_id']}_unrelated")
                expected_rank = _rank(report["experimental_top_ids"], case["expected_relevant_id"])
                self.assertIsNotNone(expected_rank)
                for unrelated_id in case["must_not_promote"]:
                    unrelated_rank = _rank(report["experimental_top_ids"], unrelated_id)
                    if unrelated_rank is not None:
                        self.assertLess(expected_rank, unrelated_rank)

    def test_ab_comparison_report_object_is_deterministic(self):
        case = CASES[0]
        first = _comparison_report(self.root, case, suffix="_report1")
        second = _comparison_report(self.root, case, suffix="_report2")
        self.assertEqual(first, second)
        self.assertEqual(
            set(first),
            {
                "query",
                "hint_chain_id",
                "baseline_top_ids",
                "experimental_top_ids",
                "rank_delta",
                "baseline_hint_ids",
                "experimental_hint_ids",
                "expected_signal_present",
                "baseline_signal_present",
                "governance_safe",
            },
        )

    def test_snapshots_unchanged(self):
        self.assertFalse(orchestrator.ENABLE_PLANNER_QUERY_EXPANSION)
        self.assertFalse(retrieval.ENABLE_PLANNER_CAUSAL_CHAIN_INJECTION)
        snapshot_queries = [
            "How do I justify quality in SAT?",
            "Why does cool climate produce high acidity?",
            "How should I structure a 10-mark SAT answer?",
        ]
        for query in snapshot_queries:
            with self.subTest(query=query):
                expanded = orchestrator._apply_planner_query_hints(
                    query,
                    {"causal_chain_focus": ["CC_COOL_CLIMATE_ACIDITY"]},
                )
                clean, hint_ids = retrieval._parse_planner_query_hints(expanded)
                self.assertEqual(expanded, query)
                self.assertEqual(clean, query)
                self.assertEqual(hint_ids, [])


if __name__ == "__main__":
    unittest.main()
