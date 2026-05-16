"""Tests for Milestones 1–3 backend completions.

Covers:
- Phase A: LES write-back (reconcile_les_from_feedback)
- Phase B/C: Causal chain loading and retrieval
- Phase D: Causal chain rendering in Tutor output
- Phase E: Misconception detection refactor + new nodes
- Schema consistency
- Governance enforcement (no safe_for_examiner=True anywhere)
"""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tools.orchestrator.learner_state import DEFAULT_LES, _governance_false
from tools.orchestrator.les_reconciler import (
    MAX_RECENT_MISCONCEPTIONS,
    reconcile_les_from_feedback,
    _apply_feedback,
    _extract_weak_areas,
    _extract_misconception_gaps,
)
from tools.orchestrator.misconception_prepass import (
    detect_misconception,
    load_misconception_nodes,
    _concept_bias,
    _tokens,
)
from tools.retrieval.tutor_retrieval_sandbox import (
    load_knowledge_nodes,
    detect_knowledge_nodes,
    select_matched_causal_chain_nodes,
    _knowledge_node_type,
    _knowledge_node_id,
)
from tools.tutor.answer_builder import (
    build_tutor_answer,
    render_answer,
    _render_causal_chain,
    _select_best_causal_chain,
)


# ---------------------------------------------------------------------------
# Phase A: LES Write-Back
# ---------------------------------------------------------------------------

class LESReconciliationTests(unittest.TestCase):
    """reconcile_les_from_feedback() must update epistemic_state.json correctly."""

    def _write_feedback(self, path: Path, questions_attempted: int = 10) -> Path:
        feedback = {
            "schema_version": "self_eval_feedback_v2",
            "strictness": "hard",
            "safe_for_examiner": False,
            "examiner_scoring_allowed": False,
            "questions_attempted": questions_attempted,
            "fragile_concepts": [
                {"concept": "cause -> mechanism -> effect", "weakness_count": 8, "severity": "high"},
                {"concept": "missing_causal_link_support", "weakness_count": 5, "severity": "medium"},
            ],
            "weakness_counters": {
                "causal_chains": {"cause -> mechanism -> effect": 8, "flor -> oxygen protection -> biological ageing": 2},
                "misconceptions": {"MC_ACIDITY_01": 3},
                "retrieval": {"missing_causal_link_support": 5, "shallow_retrieval": 3},
                "failure_labels": {"missing_causal_link": 8, "unsupported_conclusion": 5},
            },
            "suggested_misconception_investigations": ["MC_ACIDITY_01"],
            "orchestrator_recommendations": [
                "Increase forced causal-chain retrieval for 'cause -> mechanism -> effect' (weighted failures=8)."
            ],
            "retrieval_gap_question_ids": ["Q1", "Q2"],
            "note": "Self-eval feedback artifact; real LES is updated by les_reconciler.",
        }
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(feedback), encoding="utf-8")
        return path

    def _write_les(self, path: Path) -> Path:
        import copy
        les = copy.deepcopy(DEFAULT_LES)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(les), encoding="utf-8")
        return path

    def test_session_count_increments(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            feedback_path = self._write_feedback(root / "feedback.json", questions_attempted=25)
            les_path = self._write_les(root / "epistemic_state.json")
            report = reconcile_les_from_feedback(feedback_path, les_path)

        self.assertEqual(report["status"], "written")
        self.assertEqual(report["updated_les_snapshot"]["session_count"], 25)

    def test_session_count_accumulates(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            feedback_path = self._write_feedback(root / "feedback.json", questions_attempted=10)
            les = json.loads(json.dumps(DEFAULT_LES))
            les["session_count"] = 7
            les_path = root / "epistemic_state.json"
            les_path.write_text(json.dumps(les), encoding="utf-8")
            report = reconcile_les_from_feedback(feedback_path, les_path)

        self.assertEqual(report["updated_les_snapshot"]["session_count"], 17)

    def test_weak_areas_populated_from_feedback(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            feedback_path = self._write_feedback(root / "feedback.json")
            les_path = self._write_les(root / "epistemic_state.json")
            report = reconcile_les_from_feedback(feedback_path, les_path)

        weak_areas = report["updated_les_snapshot"]["known_weak_areas"]
        # Should include causal chain and retrieval entries
        self.assertTrue(len(weak_areas) > 0)
        joined = " ".join(weak_areas)
        self.assertIn("cause -> mechanism -> effect", joined)

    def test_misconceptions_populated_from_feedback(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            feedback_path = self._write_feedback(root / "feedback.json")
            les_path = self._write_les(root / "epistemic_state.json")
            report = reconcile_les_from_feedback(feedback_path, les_path)

        mc = report["updated_les_snapshot"]["recent_misconceptions"]
        self.assertIn("MC_ACIDITY_01", mc)

    def test_governance_always_false_after_reconciliation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            feedback_path = self._write_feedback(root / "feedback.json")
            les_path = self._write_les(root / "epistemic_state.json")
            reconcile_les_from_feedback(feedback_path, les_path)
            updated = json.loads(les_path.read_text(encoding="utf-8"))

        self.assertFalse(updated["governance"]["safe_for_examiner"])
        self.assertFalse(updated["governance"]["examiner_scoring_active"])

    def test_weak_areas_deduplicated(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            feedback_path = self._write_feedback(root / "feedback.json", questions_attempted=5)
            les = json.loads(json.dumps(DEFAULT_LES))
            les["known_weak_areas"] = ["causal_chain:cause -> mechanism -> effect"]
            les_path = root / "epistemic_state.json"
            les_path.write_text(json.dumps(les), encoding="utf-8")
            report = reconcile_les_from_feedback(feedback_path, les_path)

        weak_areas = report["updated_les_snapshot"]["known_weak_areas"]
        # Should not duplicate an existing entry
        count = weak_areas.count("causal_chain:cause -> mechanism -> effect")
        self.assertEqual(count, 1)

    def test_misconception_history_capped(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            # Build a LES that already has MAX entries
            les = json.loads(json.dumps(DEFAULT_LES))
            les["recent_misconceptions"] = [f"MC_X_{i:02d}" for i in range(MAX_RECENT_MISCONCEPTIONS)]
            les_path = root / "epistemic_state.json"
            les_path.write_text(json.dumps(les), encoding="utf-8")
            feedback_path = self._write_feedback(root / "feedback.json")
            reconcile_les_from_feedback(feedback_path, les_path)
            updated = json.loads(les_path.read_text(encoding="utf-8"))

        self.assertLessEqual(len(updated["recent_misconceptions"]), MAX_RECENT_MISCONCEPTIONS)

    def test_schema_version_aligned_to_v2(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            feedback_path = self._write_feedback(root / "feedback.json")
            les_path = self._write_les(root / "epistemic_state.json")
            report = reconcile_les_from_feedback(feedback_path, les_path)

        self.assertEqual(report["updated_les_snapshot"]["schema_version"], "minimal_brain_v2")

    def test_dry_run_does_not_write_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            feedback_path = self._write_feedback(root / "feedback.json")
            les_path = self._write_les(root / "epistemic_state.json")
            original_content = les_path.read_text(encoding="utf-8")
            report = reconcile_les_from_feedback(feedback_path, les_path, dry_run=True)
            after_content = les_path.read_text(encoding="utf-8")

        self.assertEqual(report["status"], "dry_run")
        self.assertEqual(original_content, after_content)

    def test_missing_feedback_file_returns_skipped(self):
        with tempfile.TemporaryDirectory() as tmp:
            les_path = Path(tmp) / "epistemic_state.json"
            les_path.write_text(json.dumps(DEFAULT_LES), encoding="utf-8")
            report = reconcile_les_from_feedback(
                Path(tmp) / "nonexistent_feedback.json",
                les_path,
            )

        self.assertEqual(report["status"], "skipped")

    def test_les_written_to_disk(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            feedback_path = self._write_feedback(root / "feedback.json", questions_attempted=5)
            les_path = self._write_les(root / "epistemic_state.json")
            reconcile_les_from_feedback(feedback_path, les_path)
            on_disk = json.loads(les_path.read_text(encoding="utf-8"))

        self.assertEqual(on_disk["session_count"], 5)
        self.assertFalse(on_disk["governance"]["safe_for_examiner"])


# ---------------------------------------------------------------------------
# Phase B/C: Causal Chain Loading and Retrieval
# ---------------------------------------------------------------------------

def _write_causal_chain_fixture(directory: Path) -> Path:
    """Write a minimal but valid causal chain node for testing."""
    directory.mkdir(parents=True, exist_ok=True)
    node = {
        "node_type": "causal_chain",
        "node_id": "CC_COOL_CLIMATE_ACIDITY",
        "chain_id": "CC_COOL_CLIMATE_ACIDITY",
        "topic": "cool climate and acidity retention",
        "trigger_keywords": ["cool climate", "acidity", "freshness", "slow ripening"],
        "steps": [
            {"step": 1, "label": "cause", "text": "Cool growing environment"},
            {"step": 2, "label": "mechanism", "text": "Slow ripening preserves malic acid"},
            {"step": 3, "label": "effect", "text": "Higher acidity and freshness in the wine"},
            {"step": 4, "label": "exam_formulation", "text": "Cool climates slow ripening, preserving acidity."},
        ],
        "sat_relevance": "Use when justifying high acidity in SAT quality assessment.",
        "linked_misconceptions": ["MC_ACIDITY_01"],
        "agent_corpus": "tutor",
        "safe_for_examiner": False,
        "examiner_scoring_allowed": False,
        "requires_human_review": True,
        "governance": {"safe_for_examiner": False, "examiner_scoring_allowed": False},
        "_meta": {"schema_version": "causal_chain_v1"},
    }
    (directory / "cc_cool_climate_acidity.json").write_text(json.dumps(node), encoding="utf-8")
    return directory


class CausalChainLoadingTests(unittest.TestCase):
    def test_causal_chain_node_recognised_by_type(self):
        with tempfile.TemporaryDirectory() as tmp:
            chain_dir = _write_causal_chain_fixture(Path(tmp) / "causal-chains")
            nodes = load_knowledge_nodes(Path(tmp))

        causal = [n for n in nodes if _knowledge_node_type(n) == "causal_chains"]
        self.assertTrue(len(causal) >= 1)

    def test_causal_chain_node_id_extracted(self):
        with tempfile.TemporaryDirectory() as tmp:
            _write_causal_chain_fixture(Path(tmp) / "causal-chains")
            nodes = load_knowledge_nodes(Path(tmp))

        causal = [n for n in nodes if _knowledge_node_type(n) == "causal_chains"]
        ids = [_knowledge_node_id(n) for n in causal]
        self.assertIn("CC_COOL_CLIMATE_ACIDITY", ids)

    def test_trigger_keywords_in_primary_phrases(self):
        """Trigger keywords must be included in primary phrase extraction for detection."""
        from tools.retrieval.tutor_retrieval_sandbox import _knowledge_node_primary_phrases
        with tempfile.TemporaryDirectory() as tmp:
            _write_causal_chain_fixture(Path(tmp) / "causal-chains")
            nodes = load_knowledge_nodes(Path(tmp))

        causal = [n for n in nodes if _knowledge_node_type(n) == "causal_chains"]
        self.assertTrue(len(causal) >= 1)
        phrases = _knowledge_node_primary_phrases(causal[0])
        # At least one trigger_keyword phrase should appear
        self.assertTrue(
            any("acidity" in phrase or "freshness" in phrase for phrase in phrases),
            f"Expected acidity/freshness in phrases, got: {phrases[:10]}"
        )

    def test_causal_chain_detected_for_matching_query(self):
        with tempfile.TemporaryDirectory() as tmp:
            _write_causal_chain_fixture(Path(tmp) / "causal-chains")
            nodes = load_knowledge_nodes(Path(tmp))
            matched = detect_knowledge_nodes(
                "How does cool climate affect acidity?",
                nodes,
            )

        # The causal chain node should appear in matched_causal_chains
        chain_ids = [item["id"] for item in matched["causal_chains"]]
        self.assertIn("CC_COOL_CLIMATE_ACIDITY", chain_ids)

    def test_select_matched_causal_chain_nodes_returns_full_node(self):
        with tempfile.TemporaryDirectory() as tmp:
            _write_causal_chain_fixture(Path(tmp) / "causal-chains")
            nodes = load_knowledge_nodes(Path(tmp))
            matched_chains = [{"id": "CC_COOL_CLIMATE_ACIDITY", "name": "Cool climate acidity", "terms": []}]
            result = select_matched_causal_chain_nodes(matched_chains, nodes)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["node_id"], "CC_COOL_CLIMATE_ACIDITY")
        self.assertIn("steps", result[0])
        self.assertEqual(len(result[0]["steps"]), 4)

    def test_select_matched_causal_chain_nodes_enforces_governance(self):
        """A causal chain node with safe_for_examiner=True must be excluded."""
        with tempfile.TemporaryDirectory() as tmp:
            chain_dir = Path(tmp) / "causal-chains"
            chain_dir.mkdir(parents=True, exist_ok=True)
            bad_node = {
                "node_type": "causal_chain",
                "node_id": "CC_BAD_NODE",
                "chain_id": "CC_BAD_NODE",
                "safe_for_examiner": True,  # governance violation
                "steps": [],
                "trigger_keywords": ["test"],
            }
            (chain_dir / "cc_bad_node.json").write_text(json.dumps(bad_node), encoding="utf-8")
            nodes = load_knowledge_nodes(Path(tmp))
            matched_chains = [{"id": "CC_BAD_NODE", "name": "Bad", "terms": []}]
            result = select_matched_causal_chain_nodes(matched_chains, nodes)

        self.assertEqual(len(result), 0)

    def test_path_field_stripped_from_causal_chain_result(self):
        with tempfile.TemporaryDirectory() as tmp:
            _write_causal_chain_fixture(Path(tmp) / "causal-chains")
            nodes = load_knowledge_nodes(Path(tmp))
            matched_chains = [{"id": "CC_COOL_CLIMATE_ACIDITY", "name": "Cool climate acidity", "terms": []}]
            result = select_matched_causal_chain_nodes(matched_chains, nodes)

        # Internal path field must not be present in output
        for chain in result:
            self.assertNotIn("path", chain)

    def test_causal_chains_present_in_context_package(self):
        """Orchestrator must include forced_causal_chains in context package when chains match."""
        from tools.orchestrator.orchestrator import run_orchestrator
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            # Seed a causal chain node
            chain_dir = root / "knowledge" / "knowledge-map" / "causal-chains"
            _write_causal_chain_fixture(chain_dir)
            les_path = root / "epistemic_state.json"
            les_path.write_text(json.dumps(DEFAULT_LES), encoding="utf-8")
            result = run_orchestrator(
                "How does cool climate affect acidity?",
                les_path=les_path,
                misconception_dir=root / "misconceptions",
                staging_path=root / "session_staging.json",
                context_package_dir=root / "context_packages",
                root=root,
            )

        package = result["context_package"]
        self.assertIn("forced_causal_chains", package)
        # With chain node available, at least one should be matched for this query
        chain_ids = [c.get("node_id") for c in package["forced_causal_chains"]]
        self.assertIn("CC_COOL_CLIMATE_ACIDITY", chain_ids)


# ---------------------------------------------------------------------------
# Phase D: Causal Chain Rendering
# ---------------------------------------------------------------------------

class CausalChainRenderingTests(unittest.TestCase):

    def _chain_fixture(self) -> dict:
        return {
            "node_type": "causal_chain",
            "node_id": "CC_COOL_CLIMATE_ACIDITY",
            "trigger_keywords": ["cool climate", "acidity"],
            "steps": [
                {"step": 1, "label": "cause", "text": "Cool growing environment"},
                {"step": 2, "label": "mechanism", "text": "Slow ripening preserves malic acid"},
                {"step": 3, "label": "effect", "text": "Higher acidity and freshness"},
                {"step": 4, "label": "exam_formulation", "text": "Cool climates slow ripening, preserving acidity."},
            ],
            "sat_relevance": "Justify high acidity as positive structural element.",
            "safe_for_examiner": False,
        }

    def test_render_causal_chain_spanish_labels(self):
        chain = self._chain_fixture()
        result = _render_causal_chain(chain, "es")
        self.assertIn("CAUSA:", result)
        self.assertIn("MECANISMO:", result)
        self.assertIn("EFECTO:", result)
        self.assertIn("FORMULACIÓN DE EXAMEN:", result)

    def test_render_causal_chain_english_labels(self):
        chain = self._chain_fixture()
        result = _render_causal_chain(chain, "en")
        self.assertIn("CAUSE:", result)
        self.assertIn("MECHANISM:", result)
        self.assertIn("EFFECT:", result)
        self.assertIn("EXAM FORMULATION:", result)

    def test_render_causal_chain_step_text_in_output(self):
        chain = self._chain_fixture()
        result = _render_causal_chain(chain, "es")
        self.assertIn("Cool growing environment", result)
        self.assertIn("Slow ripening preserves malic acid", result)
        self.assertIn("Higher acidity and freshness", result)
        self.assertIn("Cool climates slow ripening, preserving acidity.", result)

    def test_render_causal_chain_includes_sat_relevance(self):
        chain = self._chain_fixture()
        result = _render_causal_chain(chain, "es")
        self.assertIn("Relevancia SAT", result)
        self.assertIn("Justify high acidity", result)

    def test_render_causal_chain_blocked_when_safe_for_examiner_true(self):
        chain = self._chain_fixture()
        chain["safe_for_examiner"] = True
        result = _render_causal_chain(chain, "es")
        self.assertEqual(result, "")

    def test_render_causal_chain_empty_when_no_steps(self):
        chain = self._chain_fixture()
        chain["steps"] = []
        result = _render_causal_chain(chain, "es")
        self.assertEqual(result, "")

    def test_select_best_causal_chain_picks_highest_keyword_overlap(self):
        package = {
            "student_query": "How does cool climate affect acidity?",
            "forced_causal_chains": [
                {
                    "node_id": "CC_MLF_TEXTURE",
                    "trigger_keywords": ["malolactic fermentation", "mlf", "lactic acid"],
                },
                {
                    "node_id": "CC_COOL_CLIMATE_ACIDITY",
                    "trigger_keywords": ["cool climate", "acidity", "freshness"],
                },
            ],
        }
        best = _select_best_causal_chain(package)
        self.assertIsNotNone(best)
        self.assertEqual(best["node_id"], "CC_COOL_CLIMATE_ACIDITY")

    def test_select_best_causal_chain_returns_none_when_empty(self):
        package = {"student_query": "test", "forced_causal_chains": []}
        self.assertIsNone(_select_best_causal_chain(package))

    def test_tutor_answer_renders_cause_mechanism_effect_from_node(self):
        """Tutor output must contain CAUSA/MECANISMO/EFECTO from chain node, not keyword dispatch."""
        import tempfile, json
        chain = {
            "node_type": "causal_chain",
            "node_id": "CC_COOL_CLIMATE_ACIDITY",
            "trigger_keywords": ["cool climate", "acidity"],
            "steps": [
                {"step": 1, "label": "cause", "text": "TestCause: cool environment"},
                {"step": 2, "label": "mechanism", "text": "TestMechanism: slow ripening"},
                {"step": 3, "label": "effect", "text": "TestEffect: high acidity"},
                {"step": 4, "label": "exam_formulation", "text": "TestExam: cool preserves acidity."},
            ],
            "sat_relevance": "TestSAT relevance",
            "safe_for_examiner": False,
        }
        package = {
            "student_query": "How does cool climate affect acidity?",
            "pedagogical_act": "answer_normally",
            "language": "es",
            "forced_causal_chains": [chain],
            "retrieved_context": [],
            "matched_misconception": {},
            "learner_state_context": {},
            "retrieval_plan": {"uses_llm": False, "uses_api": False, "uses_embeddings": False, "uses_vector_db": False},
            "tutor_directive": {"safe_for_examiner": False},
            "success_criteria": [],
            "governance": {"agent_corpus": "tutor", "safe_for_examiner": False, "examiner_scoring_allowed": False},
        }
        with tempfile.TemporaryDirectory() as tmp:
            pkg_path = Path(tmp) / "context.json"
            pkg_path.write_text(json.dumps(package), encoding="utf-8")
            result = build_tutor_answer(pkg_path, output_path=Path(tmp) / "answer.md")

        answer = result["answer"]
        # Must contain step text from the node, not a hardcoded string
        self.assertIn("TestCause: cool environment", answer)
        self.assertIn("TestMechanism: slow ripening", answer)
        self.assertIn("TestEffect: high acidity", answer)
        self.assertIn("TestExam: cool preserves acidity.", answer)


# ---------------------------------------------------------------------------
# Phase E: Misconception Detection Refactor
# ---------------------------------------------------------------------------

class MisconceptionDetectionRefactorTests(unittest.TestCase):

    def _write_node_with_detection_keywords(self, directory: Path, node_id: str, bias_rules: list) -> Path:
        directory.mkdir(parents=True, exist_ok=True)
        node = {
            "misconception_id": node_id,
            "misconception": f"Test misconception for {node_id}.",
            "corrected_understanding": "Corrected.",
            "severity": "medium",
            "tutor_intervention": "direct_correction",
            "detection_signals": [f"A signal for {node_id}"],
            "detection_keywords": bias_rules,
            "_meta": {"schema_version": "1.0"},
        }
        (directory / f"{node_id.lower()}.json").write_text(json.dumps(node), encoding="utf-8")
        return directory

    def test_detection_keywords_structured_require_all_true(self):
        """Bias fires when all required tokens are present."""
        with tempfile.TemporaryDirectory() as tmp:
            node_dir = Path(tmp)
            self._write_node_with_detection_keywords(
                node_dir,
                "MC_TEST_01",
                [{"tokens": ["oak", "quality"], "require_all": True, "bias": 0.30}],
            )
            nodes = load_misconception_nodes(node_dir)

        node = next(n for n in nodes if n["misconception_id"] == "MC_TEST_01")
        query_tokens = _tokens("does more oak mean better quality wine")
        bias = _concept_bias(query_tokens, "does more oak mean better quality wine", node)
        self.assertAlmostEqual(bias, 0.30, places=2)

    def test_detection_keywords_require_all_false_partial_match(self):
        """Simple list fires when any token matches."""
        with tempfile.TemporaryDirectory() as tmp:
            node_dir = Path(tmp)
            self._write_node_with_detection_keywords(
                node_dir,
                "MC_TEST_02",
                ["oak", "vanilla"],
            )
            nodes = load_misconception_nodes(node_dir)

        node = next(n for n in nodes if n["misconception_id"] == "MC_TEST_02")
        query_tokens = _tokens("the wine has oak influence")
        bias = _concept_bias(query_tokens, "the wine has oak influence", node)
        # "oak" token should match; bias is 0.14 for simple list
        self.assertGreater(bias, 0.0)

    def test_detection_keywords_require_all_true_no_match(self):
        """No bias when required tokens are not all present."""
        with tempfile.TemporaryDirectory() as tmp:
            node_dir = Path(tmp)
            self._write_node_with_detection_keywords(
                node_dir,
                "MC_TEST_03",
                [{"tokens": ["oak", "quality"], "require_all": True, "bias": 0.30}],
            )
            nodes = load_misconception_nodes(node_dir)

        node = next(n for n in nodes if n["misconception_id"] == "MC_TEST_03")
        query_tokens = _tokens("the wine smells of vanilla")
        bias = _concept_bias(query_tokens, "the wine smells of vanilla", node)
        self.assertAlmostEqual(bias, 0.0, places=2)

    def test_new_node_detected_via_detection_keywords_without_code_change(self):
        """A new misconception node is detectable through detection_keywords alone,
        without any change to _concept_bias() source code."""
        with tempfile.TemporaryDirectory() as tmp:
            node_dir = Path(tmp)
            # This node was never mentioned in _concept_bias() previously
            self._write_node_with_detection_keywords(
                node_dir,
                "MC_OAK_QUALITY_01",
                [
                    {"tokens": ["oak", "quality"], "require_all": True, "bias": 0.22},
                    {"tokens": ["oak", "better"], "require_all": True, "bias": 0.20},
                ],
            )
            result = detect_misconception(
                "Does more time in oak mean the wine is better quality?",
                node_dir,
            )

        self.assertTrue(result["detected"])
        self.assertEqual(result["matched_misconception_id"], "MC_OAK_QUALITY_01")

    def test_stopwords_no_longer_contain_domain_words(self):
        """cool, climate, wine, wines must NOT be in STOPWORDS (R07 fix)."""
        from tools.orchestrator.misconception_prepass import STOPWORDS
        self.assertNotIn("cool", STOPWORDS)
        self.assertNotIn("climate", STOPWORDS)
        self.assertNotIn("wine", STOPWORDS)
        self.assertNotIn("wines", STOPWORDS)

    def test_cool_climate_tokens_in_query_not_filtered(self):
        """cool and climate must survive tokenisation and appear in query tokens."""
        query_tokens = _tokens("cool climate wines tend to have high acidity")
        self.assertIn("cool", query_tokens)
        self.assertIn("climate", query_tokens)

    def test_wine_token_in_query_not_filtered(self):
        query_tokens = _tokens("does this wine have high tannin")
        self.assertIn("wine", query_tokens)

    def test_mc_complexity_length_detected(self):
        """MC_COMPLEXITY_LENGTH_01 should be detectable via detection_keywords."""
        with tempfile.TemporaryDirectory() as tmp:
            node_dir = Path(tmp)
            self._write_node_with_detection_keywords(
                node_dir,
                "MC_COMPLEXITY_LENGTH_01",
                [
                    {"tokens": ["complexity", "length"], "require_all": True, "bias": 0.24},
                    {"tokens": ["complex", "finish"], "require_all": True, "bias": 0.16},
                ],
            )
            result = detect_misconception(
                "Isn't complexity and length the same thing on the SAT?",
                node_dir,
            )

        self.assertTrue(result["detected"])
        self.assertEqual(result["matched_misconception_id"], "MC_COMPLEXITY_LENGTH_01")


# ---------------------------------------------------------------------------
# Schema Consistency
# ---------------------------------------------------------------------------

class SchemaConsistencyTests(unittest.TestCase):

    def test_les_default_schema_is_v2(self):
        from tools.orchestrator.learner_state import DEFAULT_LES
        self.assertEqual(DEFAULT_LES["schema_version"], "minimal_brain_v2")

    def test_staging_default_schema_is_v2(self):
        from tools.orchestrator.learner_state import DEFAULT_SESSION_STAGING
        self.assertEqual(DEFAULT_SESSION_STAGING["schema_version"], "minimal_brain_v2")

    def test_reconciler_writes_v2_schema(self):
        from tools.orchestrator.les_reconciler import LES_SCHEMA_VERSION
        self.assertEqual(LES_SCHEMA_VERSION, "minimal_brain_v2")

    def test_les_schema_aligns_with_staging_schema(self):
        from tools.orchestrator.learner_state import DEFAULT_LES, DEFAULT_SESSION_STAGING
        self.assertEqual(
            DEFAULT_LES["schema_version"],
            DEFAULT_SESSION_STAGING["schema_version"],
            "LES and staging schema versions must match (R06 fix)."
        )


# ---------------------------------------------------------------------------
# Governance Enforcement
# ---------------------------------------------------------------------------

class GovernanceEnforcementTests(unittest.TestCase):

    def test_causal_chain_nodes_governance_flags(self):
        """All causal chain nodes in the live knowledge-map must have safe_for_examiner=False."""
        from tools.youtube_transcription.config import PROJECT_ROOT
        chain_dir = PROJECT_ROOT / "knowledge" / "knowledge-map" / "causal-chains"
        if not chain_dir.exists():
            self.skipTest("causal-chains directory not found in live project")
        nodes = load_knowledge_nodes(chain_dir)
        for node in nodes:
            with self.subTest(node_id=_knowledge_node_id(node)):
                self.assertIsNot(
                    node.get("safe_for_examiner"),
                    True,
                    f"Node {_knowledge_node_id(node)} has safe_for_examiner=True — governance violation."
                )

    def test_misconception_nodes_governance_flags(self):
        """All misconception nodes in the live knowledge-map must have safe_for_examiner not True."""
        from tools.youtube_transcription.config import PROJECT_ROOT
        mc_dir = PROJECT_ROOT / "knowledge" / "knowledge-map" / "misconceptions"
        if not mc_dir.exists():
            self.skipTest("misconceptions directory not found in live project")
        nodes = load_misconception_nodes(mc_dir)
        for node in nodes:
            with self.subTest(node_id=node.get("misconception_id", "unknown")):
                self.assertIsNot(
                    node.get("safe_for_examiner"),
                    True,
                    f"Misconception {node.get('misconception_id')} has safe_for_examiner=True."
                )

    def test_les_reconciler_never_sets_safe_for_examiner_true(self):
        """_apply_feedback must enforce safe_for_examiner=False regardless of input."""
        import copy
        les = copy.deepcopy(DEFAULT_LES)
        # Attempt to inject safe_for_examiner=True via feedback
        feedback = {
            "questions_attempted": 1,
            "fragile_concepts": [],
            "weakness_counters": {"causal_chains": {}, "misconceptions": {}, "retrieval": {}, "failure_labels": {}},
            "suggested_misconception_investigations": [],
        }
        les["governance"]["safe_for_examiner"] = True  # attempt injection
        updated, _ = _apply_feedback(les, feedback)
        self.assertFalse(updated["governance"]["safe_for_examiner"])

    def test_tutor_answer_builder_governance_output(self):
        """build_tutor_answer must report safe_for_examiner=False in its governance output."""
        import json, tempfile
        package = {
            "student_query": "How does cool climate affect acidity?",
            "pedagogical_act": "answer_normally",
            "language": "es",
            "forced_causal_chains": [],
            "retrieved_context": [],
            "matched_misconception": {},
            "retrieval_plan": {"uses_llm": False, "uses_api": False, "uses_embeddings": False, "uses_vector_db": False},
            "tutor_directive": {"safe_for_examiner": False},
            "success_criteria": [],
            "governance": {"agent_corpus": "tutor", "safe_for_examiner": False, "examiner_scoring_allowed": False},
        }
        with tempfile.TemporaryDirectory() as tmp:
            pkg_path = Path(tmp) / "context.json"
            pkg_path.write_text(json.dumps(package), encoding="utf-8")
            result = build_tutor_answer(pkg_path, output_path=Path(tmp) / "answer.md")

        self.assertFalse(result["governance"]["safe_for_examiner"])
        self.assertFalse(result["governance"]["uses_llm"])
        self.assertFalse(result["governance"]["uses_api"])


if __name__ == "__main__":
    unittest.main()
