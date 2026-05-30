"""Phase 3A.5 — score delta measurement harness for planner hints.

Measurement only: planner influence gates are patched on only inside selected
test scopes.  Production defaults remain off and no scoring weights are
modified.
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

PROSE_SENTINEL = "full causal-chain prose must not be injected into retrieval matches"

POSITIVE_CASES = [
    {
        "query": "Why does cool climate make wine taste fresh?",
        "hint_chain_id": "CC_COOL_CLIMATE_ACIDITY",
        "expected_chain": "Cool climate acidity",
        "target_chunk_id": "cool-acidity-mechanism",
    },
    {
        "query": "Why can warm climate fruit taste riper?",
        "hint_chain_id": "CC_WARM_CLIMATE_RIPENESS",
        "expected_chain": "Warm climate ripeness",
        "target_chunk_id": "warm-ripeness-mechanism",
    },
    {
        "query": "Why can extended maceration make tannin feel firmer?",
        "hint_chain_id": "CC_TANNIN_EXTRACTION_STRUCTURE",
        "expected_chain": "Tannin extraction structure",
        "target_chunk_id": "tannin-extraction-mechanism",
    },
    {
        "query": "Why can noble rot make sweet wines taste intense?",
        "hint_chain_id": "CC_NOBLE_ROT_QUALITY",
        "expected_chain": "Noble rot quality",
        "target_chunk_id": "noble-rot-quality-mechanism",
    },
]

NEGATIVE_CASES = [
    {
        "query": "How should I structure a tasting answer?",
        "hint_chain_id": "CC_COOL_CLIMATE_ACIDITY",
        "expected_chain": "Cool climate acidity",
        "target_chunk_id": "answer-structure-strategy",
        "unrelated_chunk_id": "cool-acidity-mechanism",
    },
    {
        "query": "What does balance mean in quality assessment?",
        "hint_chain_id": "CC_WARM_CLIMATE_RIPENESS",
        "expected_chain": "Warm climate ripeness",
        "target_chunk_id": "sat-quality-unrelated",
        "unrelated_chunk_id": "warm-ripeness-mechanism",
    },
    {
        "query": "Why can fruit taste riper?",
        "hint_chain_id": "CC_TANNIN_EXTRACTION_STRUCTURE",
        "expected_chain": "Tannin extraction structure",
        "target_chunk_id": "warm-ripeness-mechanism",
        "unrelated_chunk_id": "tannin-extraction-mechanism",
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
        "video_title_guess": "Phase 3A.5 Fixture",
        "source_filename": "phase_3a5_fixture.srt",
        "text": text,
        "quality_flags": [],
        "sat_terms": [],
        "exam_terms": [],
        "topics_detected": ["viticulture"],
    }


def _write_jsonl(path: Path, rows: list[dict]) -> None:
    path.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def _write_chain(path: Path, chain_id: str, name: str, trigger_keywords: list[str]) -> None:
    path.write_text(
        json.dumps(
            {
                "node_type": "causal_chain",
                "chain_id": chain_id,
                "chain_name": name,
                "trigger_keywords": trigger_keywords,
                "safe_for_examiner": False,
                "examiner_scoring_allowed": False,
                "note": PROSE_SENTINEL,
            },
            sort_keys=True,
        ),
        encoding="utf-8",
    )


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
        chunk_dir / "phase_3a5.chunks.jsonl",
        [
            _chunk(
                "cool-acidity-mechanism",
                "Cool climate causes slow ripening and high acidity, so the wine tastes fresh, crisp and bright.",
            ),
            _chunk(
                "warm-ripeness-mechanism",
                "Warm climate causes fast ripening and higher sugar, so fruit can taste riper.",
            ),
            _chunk(
                "tannin-extraction-mechanism",
                "Extended maceration increases tannin extraction, making red wine feel firmer and more structured.",
            ),
            _chunk(
                "noble-rot-quality-mechanism",
                "Noble rot concentrates sugar, acidity and flavour complexity, helping sweet wines taste intense and reach high quality.",
            ),
            _chunk(
                "answer-structure-strategy",
                "A tasting answer should be structured with clear observations, evidence and a concise conclusion.",
                role="exam_strategy",
            ),
            _chunk(
                "sat-quality-unrelated",
                "SAT quality assessment considers balance, intensity, complexity, length and readiness.",
                role="tasting_practice",
            ),
        ],
    )
    _write_jsonl(golden_dir / "golden_tutor_chunk_candidates.jsonl", [])
    _write_jsonl(dictionary_dir / "canonical_terms_master.jsonl", [])
    _write_chain(
        chain_dir / "cc_cool_climate_acidity.json",
        "CC_COOL_CLIMATE_ACIDITY",
        "Cool climate acidity",
        ["cool climate", "slow ripening", "high acidity"],
    )
    _write_chain(
        chain_dir / "cc_warm_climate_ripeness.json",
        "CC_WARM_CLIMATE_RIPENESS",
        "Warm climate ripeness",
        ["warm climate", "fast ripening", "higher sugar"],
    )
    _write_chain(
        chain_dir / "cc_tannin_extraction_structure.json",
        "CC_TANNIN_EXTRACTION_STRUCTURE",
        "Tannin extraction structure",
        ["extended maceration", "tannin extraction", "structured"],
    )
    _write_chain(
        chain_dir / "cc_noble_rot_quality.json",
        "CC_NOBLE_ROT_QUALITY",
        "Noble rot quality",
        ["noble rot", "flavour complexity", "high quality"],
    )


def _expanded_query(case: dict) -> str:
    return orchestrator._apply_planner_query_hints(
        case["query"],
        {"causal_chain_focus": [case["hint_chain_id"]]},
    )


def _run_baseline(root: Path, case: dict, suffix: str = "") -> dict:
    return retrieval.run_retrieval_sandbox(
        root,
        _expanded_query(case),
        top_k=6,
        output_prefix=f"phase_3a5_baseline{suffix}",
    )


def _run_experimental(root: Path, case: dict, suffix: str = "") -> dict:
    with (
        patch.object(orchestrator, "ENABLE_PLANNER_QUERY_EXPANSION", True),
        patch.object(retrieval, "ENABLE_PLANNER_CAUSAL_CHAIN_INJECTION", True),
    ):
        return retrieval.run_retrieval_sandbox(
            root,
            _expanded_query(case),
            top_k=6,
            output_prefix=f"phase_3a5_experimental{suffix}",
        )


def _top_ids(run: dict) -> list[str]:
    return [chunk["chunk_id"] for chunk in run["retrieved_chunks"]]


def _rank(run: dict, chunk_id: str) -> int:
    ids = _top_ids(run)
    return ids.index(chunk_id) + 1


def _chunk_by_id(run: dict, chunk_id: str) -> dict:
    return next(chunk for chunk in run["retrieved_chunks"] if chunk["chunk_id"] == chunk_id)


def _governance_safe(run: dict) -> bool:
    if not run.get("governance_filter_applied"):
        return False
    if GOVERNANCE_KEYS & set(run):
        return False
    for chain in run["query_analysis"].get("matched_causal_chains", []):
        if set(chain) != {"id", "name", "terms"}:
            return False
        if GOVERNANCE_KEYS & set(chain):
            return False
        if PROSE_SENTINEL in repr(chain):
            return False
    for chunk in run["retrieved_chunks"]:
        if chunk.get("safe_for_examiner") is not False:
            return False
        if chunk.get("agent_corpus") != "tutor":
            return False
        if GOVERNANCE_KEYS & set(chunk):
            return False
    return True


def _score_report(root: Path, case: dict, suffix: str = "") -> dict:
    baseline = _run_baseline(root, case, suffix=suffix)
    experimental = _run_experimental(root, case, suffix=suffix)
    baseline_chunk = _chunk_by_id(baseline, case["target_chunk_id"])
    experimental_chunk = _chunk_by_id(experimental, case["target_chunk_id"])
    baseline_score = baseline_chunk["score"]
    experimental_score = experimental_chunk["score"]
    baseline_causal_score = baseline_chunk["scoring_breakdown"]["causal_chain_match"]
    experimental_causal_score = experimental_chunk["scoring_breakdown"]["causal_chain_match"]
    baseline_count = len(baseline_chunk["matched_causal_chains"])
    experimental_count = len(experimental_chunk["matched_causal_chains"])
    return {
        "query": case["query"],
        "hint_chain_id": case["hint_chain_id"],
        "expected_chain": case["expected_chain"],
        "target_chunk_id": case["target_chunk_id"],
        "baseline_score": baseline_score,
        "experimental_score": experimental_score,
        "score_delta": round(experimental_score - baseline_score, 4),
        "baseline_rank": _rank(baseline, case["target_chunk_id"]),
        "experimental_rank": _rank(experimental, case["target_chunk_id"]),
        "rank_delta": _rank(experimental, case["target_chunk_id"]) - _rank(baseline, case["target_chunk_id"]),
        "baseline_causal_score": baseline_causal_score,
        "experimental_causal_score": experimental_causal_score,
        "causal_score_delta": round(experimental_causal_score - baseline_causal_score, 4),
        "baseline_matched_causal_chain_count": baseline_count,
        "experimental_matched_causal_chain_count": experimental_count,
        "matched_causal_chain_count_delta": experimental_count - baseline_count,
        "baseline_top_ids": _top_ids(baseline),
        "experimental_top_ids": _top_ids(experimental),
        "baseline_hint_ids": baseline["planner_hint_chain_ids"],
        "experimental_hint_ids": experimental["planner_hint_chain_ids"],
        "governance_safe": _governance_safe(experimental),
    }


class RetrievalPlannerScoreDeltaTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        _build_fixture_root(self.root)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_positive_fixture_preserves_causal_score_when_compatible(self):
        for case in POSITIVE_CASES:
            with self.subTest(case=case["hint_chain_id"]):
                report = _score_report(self.root, case, suffix=f"_{case['hint_chain_id']}_positive")
                self.assertGreater(report["experimental_causal_score"], 0)
                self.assertGreaterEqual(report["experimental_causal_score"], report["baseline_causal_score"])

    def test_negative_fixture_does_not_increase_causal_score_materially(self):
        for case in NEGATIVE_CASES:
            with self.subTest(case=case["hint_chain_id"]):
                report = _score_report(self.root, case, suffix=f"_{case['target_chunk_id']}_negative")
                self.assertLessEqual(report["causal_score_delta"], 0.0)

    def test_score_delta_deterministic(self):
        case = POSITIVE_CASES[0]
        first = _score_report(self.root, case, suffix="_score_det1")
        second = _score_report(self.root, case, suffix="_score_det2")
        self.assertEqual(first["score_delta"], second["score_delta"])
        self.assertEqual(first["causal_score_delta"], second["causal_score_delta"])

    def test_rank_delta_deterministic(self):
        case = POSITIVE_CASES[1]
        first = _score_report(self.root, case, suffix="_rank_det1")
        second = _score_report(self.root, case, suffix="_rank_det2")
        self.assertEqual(first["rank_delta"], second["rank_delta"])
        self.assertEqual(first["baseline_top_ids"], second["baseline_top_ids"])
        self.assertEqual(first["experimental_top_ids"], second["experimental_top_ids"])

    def test_baseline_gates_off(self):
        self.assertFalse(orchestrator.ENABLE_PLANNER_QUERY_EXPANSION)
        self.assertFalse(retrieval.ENABLE_PLANNER_CAUSAL_CHAIN_INJECTION)
        run = _run_baseline(self.root, POSITIVE_CASES[0], suffix="_baseline_flags")
        self.assertEqual(run["query"], POSITIVE_CASES[0]["query"])
        self.assertEqual(run["planner_hint_chain_ids"], [])

    def test_experimental_gates_on_only_inside_test(self):
        case = POSITIVE_CASES[0]
        with (
            patch.object(orchestrator, "ENABLE_PLANNER_QUERY_EXPANSION", True),
            patch.object(retrieval, "ENABLE_PLANNER_CAUSAL_CHAIN_INJECTION", True),
        ):
            self.assertTrue(orchestrator.ENABLE_PLANNER_QUERY_EXPANSION)
            self.assertTrue(retrieval.ENABLE_PLANNER_CAUSAL_CHAIN_INJECTION)
            run = retrieval.run_retrieval_sandbox(
                self.root,
                _expanded_query(case),
                top_k=6,
                output_prefix="phase_3a5_scope",
            )
            self.assertEqual(run["planner_hint_chain_ids"], [case["hint_chain_id"]])
        self.assertFalse(orchestrator.ENABLE_PLANNER_QUERY_EXPANSION)
        self.assertFalse(retrieval.ENABLE_PLANNER_CAUSAL_CHAIN_INJECTION)

    def test_global_defaults_restored_after_test(self):
        _run_experimental(self.root, POSITIVE_CASES[0], suffix="_defaults")
        self.assertFalse(orchestrator.ENABLE_PLANNER_QUERY_EXPANSION)
        self.assertFalse(retrieval.ENABLE_PLANNER_CAUSAL_CHAIN_INJECTION)

    def test_no_governance_fields_introduced(self):
        for case in POSITIVE_CASES + NEGATIVE_CASES:
            with self.subTest(case=case["hint_chain_id"]):
                report = _score_report(self.root, case, suffix=f"_{case['target_chunk_id']}_gov")
                self.assertTrue(report["governance_safe"])

    def test_no_scoring_weights_changed(self):
        before = dict(retrieval.SCORE_WEIGHTS)
        _score_report(self.root, POSITIVE_CASES[0], suffix="_weights")
        self.assertEqual(retrieval.SCORE_WEIGHTS, before)

    def test_no_snapshot_changes(self):
        snapshot_queries = [
            "How do I justify quality in SAT?",
            "Why does cool climate produce high acidity?",
            "How should I structure a 10-mark SAT answer?",
        ]
        self.assertFalse(orchestrator.ENABLE_PLANNER_QUERY_EXPANSION)
        self.assertFalse(retrieval.ENABLE_PLANNER_CAUSAL_CHAIN_INJECTION)
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

    def test_positive_fixtures_produce_compatible_causal_signal(self):
        for case in POSITIVE_CASES:
            with self.subTest(case=case["hint_chain_id"]):
                report = _score_report(self.root, case, suffix=f"_{case['hint_chain_id']}_signal")
                self.assertGreater(report["experimental_causal_score"], 0)
                self.assertGreaterEqual(
                    report["experimental_matched_causal_chain_count"],
                    report["baseline_matched_causal_chain_count"],
                )
                self.assertEqual(report["experimental_hint_ids"], [case["hint_chain_id"]])

    def test_negative_fixtures_remain_bounded(self):
        for case in NEGATIVE_CASES:
            with self.subTest(case=case["hint_chain_id"]):
                report = _score_report(self.root, case, suffix=f"_{case['target_chunk_id']}_bounded")
                self.assertLessEqual(report["score_delta"], 0.0)
                if case["unrelated_chunk_id"] in report["experimental_top_ids"]:
                    unrelated_rank = report["experimental_top_ids"].index(case["unrelated_chunk_id"]) + 1
                    self.assertLess(report["experimental_rank"], unrelated_rank)
                self.assertLessEqual(abs(report["rank_delta"]), 1)

    def test_report_object_deterministic(self):
        case = POSITIVE_CASES[2]
        first = _score_report(self.root, case, suffix="_report_det1")
        second = _score_report(self.root, case, suffix="_report_det2")
        self.assertEqual(first, second)
        self.assertEqual(
            set(first),
            {
                "query",
                "hint_chain_id",
                "expected_chain",
                "target_chunk_id",
                "baseline_score",
                "experimental_score",
                "score_delta",
                "baseline_rank",
                "experimental_rank",
                "rank_delta",
                "baseline_causal_score",
                "experimental_causal_score",
                "causal_score_delta",
                "baseline_matched_causal_chain_count",
                "experimental_matched_causal_chain_count",
                "matched_causal_chain_count_delta",
                "baseline_top_ids",
                "experimental_top_ids",
                "baseline_hint_ids",
                "experimental_hint_ids",
                "governance_safe",
            },
        )

    def test_all_measurement_cases_execute_with_defaults_off_afterward(self):
        for case in POSITIVE_CASES + NEGATIVE_CASES:
            with self.subTest(case=case["target_chunk_id"]):
                report = _score_report(self.root, case, suffix=f"_{case['target_chunk_id']}_all")
                self.assertIsInstance(report["score_delta"], float)
                self.assertTrue(report["governance_safe"])
        self.assertFalse(orchestrator.ENABLE_PLANNER_QUERY_EXPANSION)
        self.assertFalse(retrieval.ENABLE_PLANNER_CAUSAL_CHAIN_INJECTION)


if __name__ == "__main__":
    unittest.main()
