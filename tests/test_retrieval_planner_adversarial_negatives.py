"""Phase 3A.6 — adversarial negative fixtures for planner hint injection.

This is a red-team measurement harness.  It deliberately tries to produce
false-positive planner influence while keeping both planner influence gates off
by default.  Some fixtures are expected to expose weaknesses; the tests assert
that those weaknesses are measured deterministically, not that the mechanism is
safe for activation.
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

PROSE_SENTINEL = "full adversarial causal-chain prose must not be injected"
MATERIAL_SCORE_DELTA = 0.08
NEAR_FAILURE_DELTA = 0.04

ADVERSARIAL_CASES = [
    {
        "category": "A_semantic_opposition",
        "name": "fresh_acidity_query_with_warm_ripeness_hint",
        "query": "Why does wine taste fresh?",
        "hint_chain_ids": ["CC_WARM_CLIMATE_RIPENESS"],
        "target_chunk_id": "cool-acidity-mechanism",
        "incorrect_chunk_id": "warm-ripeness-mechanism",
        "expected_classification": "safe",
    },
    {
        "category": "A_semantic_opposition",
        "name": "high_tannin_query_with_noble_rot_hint",
        "query": "Why does red wine feel firm and high in tannin?",
        "hint_chain_ids": ["CC_NOBLE_ROT_QUALITY"],
        "target_chunk_id": "tannin-structure-mechanism",
        "incorrect_chunk_id": "noble-rot-quality-mechanism",
        "expected_classification": "safe",
    },
    {
        "category": "B_near_neighbor_confusion",
        "name": "freshness_query_with_sweetness_balance_hint",
        "query": "Why can acidity make a wine taste fresh and balanced?",
        "hint_chain_ids": ["CC_ACIDITY_SWEETNESS_BALANCE"],
        "target_chunk_id": "cool-acidity-mechanism",
        "incorrect_chunk_id": "sweetness-balance-neighbor",
        "expected_classification": "safe",
    },
    {
        "category": "C_sat_contamination",
        "name": "sat_quality_query_with_quality_balance_chain_hint",
        "query": "How do I judge a wine?",
        "hint_chain_ids": ["CC_SAT_QUALITY_BALANCE"],
        "target_chunk_id": "sat-quality-relevant",
        "incorrect_chunk_id": "sat-quality-relevant",
        "expected_classification": "safe",
    },
    {
        "category": "D_keyword_overlap_trap",
        "name": "sweetness_query_with_warm_ripeness_hint",
        "query": "Why can sweetness change the balance of a wine?",
        "hint_chain_ids": ["CC_WARM_CLIMATE_RIPENESS"],
        "target_chunk_id": "sweetness-balance-neighbor",
        "incorrect_chunk_id": "warm-ripeness-mechanism",
        "expected_classification": "safe",
    },
    {
        "category": "E_maximum_hint_stress",
        "name": "answer_structure_query_with_four_hints_bounded_to_three",
        "query": "How should I structure a tasting answer?",
        "hint_chain_ids": [
            "CC_COOL_CLIMATE_ACIDITY",
            "CC_WARM_CLIMATE_RIPENESS",
            "CC_NOBLE_ROT_QUALITY",
            "CC_TANNIN_EXTRACTION_STRUCTURE",
        ],
        "target_chunk_id": "answer-structure-strategy",
        "incorrect_chunk_id": "cool-acidity-mechanism",
        "expected_classification": "safe",
        "expected_hint_count": 3,
    },
    {
        "category": "F_contradictory_hints",
        "name": "fresh_query_with_cool_and_warm_hints",
        "query": "Why does cool climate make wine taste fresh?",
        "hint_chain_ids": ["CC_COOL_CLIMATE_ACIDITY", "CC_WARM_CLIMATE_RIPENESS"],
        "target_chunk_id": "cool-acidity-mechanism",
        "incorrect_chunk_id": "warm-ripeness-mechanism",
        "expected_classification": "safe",
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
        "video_title_guess": "Phase 3A.6 Fixture",
        "source_filename": "phase_3a6_fixture.srt",
        "text": text,
        "quality_flags": [],
        "sat_terms": [],
        "exam_terms": [],
        "topics_detected": ["adversarial_retrieval"],
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
        chunk_dir / "phase_3a6.chunks.jsonl",
        [
            _chunk(
                "cool-acidity-mechanism",
                "Cool climate causes slow ripening and high acidity, so the wine tastes fresh, crisp and bright.",
            ),
            _chunk(
                "warm-ripeness-mechanism",
                "Warm climate causes fast ripening and higher sugar, so the wine tastes ripe, sweet and rounded.",
            ),
            _chunk(
                "tannin-structure-mechanism",
                "Extended maceration increases tannin extraction, making red wine feel firm, high in tannin and structured.",
            ),
            _chunk(
                "noble-rot-quality-mechanism",
                "Noble rot concentrates sugar, acidity and flavour complexity, helping sweet wines taste intense and reach high quality.",
            ),
            _chunk(
                "sweetness-balance-neighbor",
                "Residual sugar increases sweetness and can change perceived balance against acidity.",
            ),
            _chunk(
                "sat-quality-relevant",
                "To judge a wine in SAT, quality assessment uses balance, intensity, complexity, length and readiness.",
                role="tasting_practice",
            ),
            _chunk(
                "answer-structure-strategy",
                "A tasting answer should be structured with clear observations, evidence and a concise conclusion.",
                role="exam_strategy",
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
    _write_chain(
        chain_dir / "cc_acidity_sweetness_balance.json",
        "CC_ACIDITY_SWEETNESS_BALANCE",
        "Acidity sweetness balance",
        ["acidity", "sweetness", "balance"],
    )
    _write_chain(
        chain_dir / "cc_sat_quality_balance.json",
        "CC_SAT_QUALITY_BALANCE",
        "SAT quality balance",
        ["quality assessment", "balance", "intensity"],
    )


def _expanded_query(case: dict) -> str:
    return orchestrator._apply_planner_query_hints(
        case["query"],
        {"causal_chain_focus": case["hint_chain_ids"]},
    )


def _run_baseline(root: Path, case: dict, suffix: str = "") -> dict:
    return retrieval.run_retrieval_sandbox(
        root,
        _expanded_query(case),
        top_k=7,
        output_prefix=f"phase_3a6_baseline{suffix}",
    )


def _run_experimental(root: Path, case: dict, suffix: str = "") -> dict:
    with (
        patch.object(orchestrator, "ENABLE_PLANNER_QUERY_EXPANSION", True),
        patch.object(retrieval, "ENABLE_PLANNER_CAUSAL_CHAIN_INJECTION", True),
    ):
        return retrieval.run_retrieval_sandbox(
            root,
            _expanded_query(case),
            top_k=7,
            output_prefix=f"phase_3a6_experimental{suffix}",
        )


def _top_ids(run: dict) -> list[str]:
    return [chunk["chunk_id"] for chunk in run["retrieved_chunks"]]


def _chunk_by_id(run: dict, chunk_id: str) -> dict | None:
    return next((chunk for chunk in run["retrieved_chunks"] if chunk["chunk_id"] == chunk_id), None)


def _rank(run: dict, chunk_id: str) -> int | None:
    ids = _top_ids(run)
    return ids.index(chunk_id) + 1 if chunk_id in ids else None


def _score(run: dict, chunk_id: str) -> float:
    chunk = _chunk_by_id(run, chunk_id)
    return float(chunk["score"]) if chunk else 0.0


def _causal_score(run: dict, chunk_id: str) -> float:
    chunk = _chunk_by_id(run, chunk_id)
    return float(chunk["scoring_breakdown"]["causal_chain_match"]) if chunk else 0.0


def _matched_chain_count(run: dict, chunk_id: str) -> int:
    chunk = _chunk_by_id(run, chunk_id)
    return len(chunk["matched_causal_chains"]) if chunk else 0


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


def _classification(report: dict) -> str:
    if report["incorrect_chain_promoted"]:
        return "failed"
    if report["score_delta"] >= NEAR_FAILURE_DELTA or report["causal_score_delta"] > 0:
        return "near_failed"
    return "safe"


def _adversarial_report(root: Path, case: dict, suffix: str = "") -> dict:
    baseline = _run_baseline(root, case, suffix=suffix)
    experimental = _run_experimental(root, case, suffix=suffix)
    incorrect = case["incorrect_chunk_id"]
    baseline_rank = _rank(baseline, incorrect)
    experimental_rank = _rank(experimental, incorrect)
    target_experimental_rank = _rank(experimental, case["target_chunk_id"])
    baseline_score = _score(baseline, incorrect)
    experimental_score = _score(experimental, incorrect)
    baseline_causal = _causal_score(baseline, incorrect)
    experimental_causal = _causal_score(experimental, incorrect)
    rank_delta = None
    if baseline_rank is not None and experimental_rank is not None:
        rank_delta = experimental_rank - baseline_rank
    incorrect_chain_promoted = (
        target_experimental_rank is not None
        and experimental_rank is not None
        and experimental_rank <= target_experimental_rank
        and incorrect != case["target_chunk_id"]
    )
    if incorrect == case["target_chunk_id"]:
        incorrect_chain_promoted = (experimental_score - baseline_score) >= MATERIAL_SCORE_DELTA
    report = {
        "category": case["category"],
        "name": case["name"],
        "query": case["query"],
        "hint_chain_ids": case["hint_chain_ids"],
        "target_chunk_id": case["target_chunk_id"],
        "incorrect_chunk_id": incorrect,
        "baseline_score": baseline_score,
        "experimental_score": experimental_score,
        "score_delta": round(experimental_score - baseline_score, 4),
        "baseline_rank": baseline_rank,
        "experimental_rank": experimental_rank,
        "target_experimental_rank": target_experimental_rank,
        "rank_delta": rank_delta,
        "baseline_causal_score": baseline_causal,
        "experimental_causal_score": experimental_causal,
        "causal_score_delta": round(experimental_causal - baseline_causal, 4),
        "matched_causal_chain_count_delta": (
            _matched_chain_count(experimental, incorrect) - _matched_chain_count(baseline, incorrect)
        ),
        "baseline_top_ids": _top_ids(baseline),
        "experimental_top_ids": _top_ids(experimental),
        "baseline_hint_ids": baseline["planner_hint_chain_ids"],
        "experimental_hint_ids": experimental["planner_hint_chain_ids"],
        "incorrect_chain_promoted": incorrect_chain_promoted,
        "governance_safe": _governance_safe(experimental),
    }
    report["classification"] = _classification(report)
    return report


class RetrievalPlannerAdversarialNegativeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        _build_fixture_root(self.root)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_all_adversarial_categories_are_covered(self):
        categories = {case["category"] for case in ADVERSARIAL_CASES}
        self.assertEqual(
            categories,
            {
                "A_semantic_opposition",
                "B_near_neighbor_confusion",
                "C_sat_contamination",
                "D_keyword_overlap_trap",
                "E_maximum_hint_stress",
                "F_contradictory_hints",
            },
        )

    def test_adversarial_reports_are_deterministic(self):
        for case in ADVERSARIAL_CASES:
            with self.subTest(case=case["name"]):
                first = _adversarial_report(self.root, case, suffix=f"_{case['name']}_det1")
                second = _adversarial_report(self.root, case, suffix=f"_{case['name']}_det2")
                self.assertEqual(first, second)

    def test_former_failure_modes_are_mitigated(self):
        reports = [_adversarial_report(self.root, case, suffix=f"_{case['name']}_failure") for case in ADVERSARIAL_CASES]
        failed = [report for report in reports if report["classification"] == "failed"]
        self.assertEqual(failed, [])

    def test_near_failures_are_mitigated_below_material_threshold(self):
        reports = [_adversarial_report(self.root, case, suffix=f"_{case['name']}_near") for case in ADVERSARIAL_CASES]
        near_failed = [report for report in reports if report["classification"] == "near_failed"]
        self.assertEqual(near_failed, [])
        for report in reports:
            self.assertLess(report["score_delta"], NEAR_FAILURE_DELTA)

    def test_case_classifications_match_current_red_team_observations(self):
        for case in ADVERSARIAL_CASES:
            with self.subTest(case=case["name"]):
                report = _adversarial_report(self.root, case, suffix=f"_{case['name']}_class")
                self.assertEqual(report["classification"], case["expected_classification"])

    def test_maximum_hint_stress_is_bounded_to_configured_limit(self):
        case = next(item for item in ADVERSARIAL_CASES if item["category"] == "E_maximum_hint_stress")
        report = _adversarial_report(self.root, case, suffix="_max_hint")
        self.assertEqual(len(report["experimental_hint_ids"]), case["expected_hint_count"])
        self.assertLessEqual(len(report["experimental_hint_ids"]), retrieval._MAX_HINT_IDS)
        self.assertEqual(report["experimental_hint_ids"], case["hint_chain_ids"][: retrieval._MAX_HINT_IDS])

    def test_contradictory_hints_are_measured_without_default_activation(self):
        case = next(item for item in ADVERSARIAL_CASES if item["category"] == "F_contradictory_hints")
        report = _adversarial_report(self.root, case, suffix="_contradictory")
        self.assertEqual(report["baseline_hint_ids"], [])
        self.assertEqual(report["experimental_hint_ids"], case["hint_chain_ids"])
        self.assertFalse(orchestrator.ENABLE_PLANNER_QUERY_EXPANSION)
        self.assertFalse(retrieval.ENABLE_PLANNER_CAUSAL_CHAIN_INJECTION)

    def test_sat_contamination_case_is_vetoed_by_semantic_gate(self):
        case = next(item for item in ADVERSARIAL_CASES if item["category"] == "C_sat_contamination")
        report = _adversarial_report(self.root, case, suffix="_sat")
        self.assertEqual(report["classification"], "safe")
        self.assertLess(report["score_delta"], NEAR_FAILURE_DELTA)
        self.assertEqual(report["causal_score_delta"], 0.0)

    def test_governance_remains_safe_for_all_adversarial_runs(self):
        for case in ADVERSARIAL_CASES:
            with self.subTest(case=case["name"]):
                report = _adversarial_report(self.root, case, suffix=f"_{case['name']}_gov")
                self.assertTrue(report["governance_safe"])

    def test_no_scoring_weights_changed(self):
        before = dict(retrieval.SCORE_WEIGHTS)
        for case in ADVERSARIAL_CASES:
            _adversarial_report(self.root, case, suffix=f"_{case['name']}_weights")
        self.assertEqual(retrieval.SCORE_WEIGHTS, before)

    def test_snapshot_noop_conditions_remain_unchanged(self):
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
                    {"causal_chain_focus": ["CC_WARM_CLIMATE_RIPENESS"]},
                )
                clean, hint_ids = retrieval._parse_planner_query_hints(expanded)
                self.assertEqual(expanded, query)
                self.assertEqual(clean, query)
                self.assertEqual(hint_ids, [])

    def test_report_object_has_required_metrics(self):
        report = _adversarial_report(self.root, ADVERSARIAL_CASES[0], suffix="_schema")
        self.assertEqual(
            set(report),
            {
                "category",
                "name",
                "query",
                "hint_chain_ids",
                "target_chunk_id",
                "incorrect_chunk_id",
                "baseline_score",
                "experimental_score",
                "score_delta",
                "baseline_rank",
                "experimental_rank",
                "target_experimental_rank",
                "rank_delta",
                "baseline_causal_score",
                "experimental_causal_score",
                "causal_score_delta",
                "matched_causal_chain_count_delta",
                "baseline_top_ids",
                "experimental_top_ids",
                "baseline_hint_ids",
                "experimental_hint_ids",
                "incorrect_chain_promoted",
                "governance_safe",
                "classification",
            },
        )

    def test_global_defaults_restored_after_adversarial_runs(self):
        for case in ADVERSARIAL_CASES:
            _adversarial_report(self.root, case, suffix=f"_{case['name']}_defaults")
        self.assertFalse(orchestrator.ENABLE_PLANNER_QUERY_EXPANSION)
        self.assertFalse(retrieval.ENABLE_PLANNER_CAUSAL_CHAIN_INJECTION)


if __name__ == "__main__":
    unittest.main()
