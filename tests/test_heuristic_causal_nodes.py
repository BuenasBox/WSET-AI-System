"""Schema, governance, and integration tests for HC_* heuristic causal-chain nodes.

HC_* nodes extend the causal_chain_v1 schema with explicit heuristic governance
fields. These tests verify:
  1. Every HC_*.json in causal-chains/ passes base causal_chain_v1 schema checks.
  2. Every HC_*.json carries the required heuristic governance extension fields.
  3. Governance flags are correct (safe_for_examiner=false, etc.).
  4. HC_* node_ids do not collide with existing CC_* node_ids.
  5. trigger_keywords are non-empty lists of strings (retrieval requirement).
  6. steps follow the 4-label structure required by the Tutor renderer.
  7. HC_* nodes are loadable by the retrieval engine's knowledge-node loader.
  8. Retrieval index detects HC_* nodes as causal_chain type.
  9. ENABLE_PLANNER_CAUSAL_CHAIN_INJECTION remains False after adding HC_* files.
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from tools.constants import KNOWLEDGE_DIR, PROJECT_ROOT

CAUSAL_CHAINS_DIR = KNOWLEDGE_DIR / "knowledge-map" / "causal-chains"

# Required labels in steps, in order.
EXPECTED_STEP_LABELS = ["cause", "mechanism", "effect", "exam_formulation"]

# Fields required by heuristic governance extension.
HC_GOVERNANCE_EXTENSION_FIELDS = {
    "source": "heuristic",
    "classification": "inferred",
    "official": False,
    "formative_only": True,
    "official_mark_scheme": False,
}


def _load_hc_nodes() -> list[tuple[Path, dict]]:
    """Load all HC_*.json files from causal-chains/."""
    paths = sorted(CAUSAL_CHAINS_DIR.glob("HC_*.json"))
    result = []
    for p in paths:
        data = json.loads(p.read_text(encoding="utf-8"))
        result.append((p, data))
    return result


def _load_cc_node_ids() -> set[str]:
    """Load all CC_* node_ids for collision checking."""
    ids = set()
    for p in CAUSAL_CHAINS_DIR.glob("CC_*.json"):
        data = json.loads(p.read_text(encoding="utf-8"))
        nid = data.get("node_id")
        if nid:
            ids.add(nid)
    return ids


class HCNodePresenceTests(unittest.TestCase):
    """At least one HC_* node must exist before other tests are meaningful."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.nodes = _load_hc_nodes()

    def test_at_least_one_hc_node_exists(self) -> None:
        self.assertGreater(len(self.nodes), 0, "No HC_*.json files found in causal-chains/")

    def test_hc_nodes_have_expected_count(self) -> None:
        """Expected >= 6 HC_* nodes (one per keyword gap area)."""
        self.assertGreaterEqual(
            len(self.nodes), 6,
            f"Expected >=6 HC_* nodes, found {len(self.nodes)}"
        )


class HCBaseSchemaTests(unittest.TestCase):
    """Every HC_*.json must satisfy the base causal_chain_v1 schema."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.nodes = _load_hc_nodes()

    def test_node_type_is_causal_chain(self) -> None:
        for path, node in self.nodes:
            with self.subTest(file=path.name):
                self.assertEqual(
                    node.get("node_type"), "causal_chain",
                    f"{path.name}: node_type must be 'causal_chain'"
                )

    def test_node_id_starts_with_hc(self) -> None:
        for path, node in self.nodes:
            with self.subTest(file=path.name):
                nid = node.get("node_id", "")
                self.assertTrue(
                    nid.startswith("HC_"),
                    f"{path.name}: node_id must start with 'HC_', got '{nid}'"
                )

    def test_node_id_matches_filename(self) -> None:
        for path, node in self.nodes:
            with self.subTest(file=path.name):
                expected = path.stem
                self.assertEqual(
                    node.get("node_id"), expected,
                    f"{path.name}: node_id must match filename stem"
                )

    def test_topic_is_nonempty_string(self) -> None:
        for path, node in self.nodes:
            with self.subTest(file=path.name):
                topic = node.get("topic")
                self.assertIsInstance(topic, str)
                self.assertTrue(topic.strip(), f"{path.name}: topic must not be empty")

    def test_trigger_keywords_nonempty_list_of_strings(self) -> None:
        for path, node in self.nodes:
            with self.subTest(file=path.name):
                kws = node.get("trigger_keywords")
                self.assertIsInstance(kws, list, f"{path.name}: trigger_keywords must be a list")
                self.assertGreater(len(kws), 0, f"{path.name}: trigger_keywords must not be empty")
                for kw in kws:
                    self.assertIsInstance(kw, str, f"{path.name}: keyword items must be strings")

    def test_trigger_keywords_minimum_count(self) -> None:
        """Each HC_* node needs >=5 trigger keywords for adequate retrieval coverage."""
        for path, node in self.nodes:
            with self.subTest(file=path.name):
                kws = node.get("trigger_keywords", [])
                self.assertGreaterEqual(
                    len(kws), 5,
                    f"{path.name}: expected >=5 trigger_keywords, got {len(kws)}"
                )

    def test_trigger_keywords_bilingual(self) -> None:
        """Each HC_* node must contain keywords spanning multiple distinct words."""
        for path, node in self.nodes:
            with self.subTest(file=path.name):
                kws = node.get("trigger_keywords", [])
                unique_words = {w.lower() for kw in kws for w in kw.split()}
                self.assertGreater(
                    len(unique_words), 4,
                    f"{path.name}: trigger_keywords appear too narrow (bilingual coverage expected)"
                )

    def test_steps_has_four_items(self) -> None:
        for path, node in self.nodes:
            with self.subTest(file=path.name):
                steps = node.get("steps", [])
                self.assertEqual(
                    len(steps), 4,
                    f"{path.name}: expected 4 steps, got {len(steps)}"
                )

    def test_steps_have_correct_labels_in_order(self) -> None:
        for path, node in self.nodes:
            with self.subTest(file=path.name):
                labels = [s.get("label") for s in node.get("steps", [])]
                self.assertEqual(
                    labels, EXPECTED_STEP_LABELS,
                    f"{path.name}: step labels must be {EXPECTED_STEP_LABELS}, got {labels}"
                )

    def test_steps_have_nonempty_text(self) -> None:
        for path, node in self.nodes:
            with self.subTest(file=path.name):
                for step in node.get("steps", []):
                    text = step.get("text", "")
                    self.assertIsInstance(text, str)
                    self.assertTrue(
                        text.strip(),
                        f"{path.name} step {step.get('step')}: text must not be empty"
                    )

    def test_agent_corpus_is_tutor(self) -> None:
        for path, node in self.nodes:
            with self.subTest(file=path.name):
                self.assertEqual(
                    node.get("agent_corpus"), "tutor",
                    f"{path.name}: agent_corpus must be 'tutor'"
                )

    def test_meta_schema_version_is_causal_chain_v1(self) -> None:
        for path, node in self.nodes:
            with self.subTest(file=path.name):
                meta = node.get("_meta", {})
                self.assertEqual(
                    meta.get("schema_version"), "causal_chain_v1",
                    f"{path.name}: _meta.schema_version must be 'causal_chain_v1'"
                )


class HCGovernanceFlagTests(unittest.TestCase):
    """Core governance flags must be False on all HC_* nodes."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.nodes = _load_hc_nodes()

    def test_safe_for_examiner_is_false(self) -> None:
        for path, node in self.nodes:
            with self.subTest(file=path.name):
                self.assertIs(
                    node.get("safe_for_examiner"), False,
                    f"{path.name}: safe_for_examiner must be False"
                )

    def test_examiner_scoring_allowed_is_false(self) -> None:
        for path, node in self.nodes:
            with self.subTest(file=path.name):
                self.assertIs(
                    node.get("examiner_scoring_allowed"), False,
                    f"{path.name}: examiner_scoring_allowed must be False"
                )

    def test_requires_human_review_is_true(self) -> None:
        for path, node in self.nodes:
            with self.subTest(file=path.name):
                self.assertIs(
                    node.get("requires_human_review"), True,
                    f"{path.name}: requires_human_review must be True"
                )

    def test_governance_block_safe_for_examiner_false(self) -> None:
        for path, node in self.nodes:
            with self.subTest(file=path.name):
                gov = node.get("governance", {})
                self.assertIs(
                    gov.get("safe_for_examiner"), False,
                    f"{path.name}: governance.safe_for_examiner must be False"
                )

    def test_governance_block_examiner_scoring_allowed_false(self) -> None:
        for path, node in self.nodes:
            with self.subTest(file=path.name):
                gov = node.get("governance", {})
                self.assertIs(
                    gov.get("examiner_scoring_allowed"), False,
                    f"{path.name}: governance.examiner_scoring_allowed must be False"
                )


class HCHeuristicExtensionTests(unittest.TestCase):
    """HC_* specific governance extension fields must be present and correct."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.nodes = _load_hc_nodes()

    def test_source_is_heuristic(self) -> None:
        for path, node in self.nodes:
            with self.subTest(file=path.name):
                self.assertEqual(
                    node.get("source"), "heuristic",
                    f"{path.name}: source must be 'heuristic'"
                )

    def test_classification_is_inferred(self) -> None:
        for path, node in self.nodes:
            with self.subTest(file=path.name):
                self.assertEqual(
                    node.get("classification"), "inferred",
                    f"{path.name}: classification must be 'inferred'"
                )

    def test_official_is_false(self) -> None:
        for path, node in self.nodes:
            with self.subTest(file=path.name):
                self.assertIs(
                    node.get("official"), False,
                    f"{path.name}: official must be False"
                )

    def test_formative_only_is_true(self) -> None:
        for path, node in self.nodes:
            with self.subTest(file=path.name):
                self.assertIs(
                    node.get("formative_only"), True,
                    f"{path.name}: formative_only must be True"
                )

    def test_official_mark_scheme_is_false(self) -> None:
        for path, node in self.nodes:
            with self.subTest(file=path.name):
                self.assertIs(
                    node.get("official_mark_scheme"), False,
                    f"{path.name}: official_mark_scheme must be False"
                )

    def test_governance_block_source_is_heuristic(self) -> None:
        for path, node in self.nodes:
            with self.subTest(file=path.name):
                gov = node.get("governance", {})
                self.assertEqual(
                    gov.get("source"), "heuristic",
                    f"{path.name}: governance.source must be 'heuristic'"
                )

    def test_governance_block_classification_is_inferred(self) -> None:
        for path, node in self.nodes:
            with self.subTest(file=path.name):
                gov = node.get("governance", {})
                self.assertEqual(
                    gov.get("classification"), "inferred",
                    f"{path.name}: governance.classification must be 'inferred'"
                )

    def test_governance_block_official_is_false(self) -> None:
        for path, node in self.nodes:
            with self.subTest(file=path.name):
                gov = node.get("governance", {})
                self.assertIs(
                    gov.get("official"), False,
                    f"{path.name}: governance.official must be False"
                )

    def test_governance_block_formative_only_is_true(self) -> None:
        for path, node in self.nodes:
            with self.subTest(file=path.name):
                gov = node.get("governance", {})
                self.assertIs(
                    gov.get("formative_only"), True,
                    f"{path.name}: governance.formative_only must be True"
                )

    def test_meta_has_heuristic_extension_key(self) -> None:
        for path, node in self.nodes:
            with self.subTest(file=path.name):
                meta = node.get("_meta", {})
                self.assertIn(
                    "heuristic_extension", meta,
                    f"{path.name}: _meta must contain 'heuristic_extension' key"
                )

    def test_meta_source_note_mentions_not_official(self) -> None:
        for path, node in self.nodes:
            with self.subTest(file=path.name):
                meta = node.get("_meta", {})
                note = meta.get("source_note", "")
                self.assertIn(
                    "not", note.lower(),
                    f"{path.name}: _meta.source_note must clarify this is not official"
                )


class HCNodeIdCollisionTests(unittest.TestCase):
    """HC_* node_ids must not collide with any existing CC_* node_ids."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.hc_nodes = _load_hc_nodes()
        cls.cc_ids = _load_cc_node_ids()

    def test_no_id_collisions_with_cc_nodes(self) -> None:
        for path, node in self.hc_nodes:
            with self.subTest(file=path.name):
                nid = node.get("node_id", "")
                self.assertNotIn(
                    nid, self.cc_ids,
                    f"{path.name}: HC node_id '{nid}' collides with an existing CC node"
                )

    def test_hc_ids_are_unique_among_themselves(self) -> None:
        ids = [node.get("node_id") for _, node in self.hc_nodes]
        self.assertEqual(
            len(ids), len(set(ids)),
            f"Duplicate HC node_ids found: {ids}"
        )


class HCRetrievalIndexTests(unittest.TestCase):
    """HC_* nodes must be loadable by the retrieval engine with no code changes."""

    @classmethod
    def setUpClass(cls) -> None:
        from tools.retrieval.tutor_retrieval_sandbox import load_knowledge_nodes
        km_dir = KNOWLEDGE_DIR / "knowledge-map"
        all_nodes = load_knowledge_nodes(km_dir)
        # load_knowledge_nodes returns a flat list; filter to causal_chain nodes
        cls.causal_chains = [
            n for n in all_nodes if n.get("node_type") == "causal_chain"
        ]
        cls.hc_paths = sorted(CAUSAL_CHAINS_DIR.glob("HC_*.json"))

    def test_retrieval_loads_at_least_one_hc_node(self) -> None:
        hc_ids = {p.stem for p in self.hc_paths}
        loaded_ids = {n.get("node_id") for n in self.causal_chains}
        intersection = hc_ids & loaded_ids
        self.assertGreater(
            len(intersection), 0,
            f"Retrieval engine loaded no HC_* nodes. HC files: {sorted(hc_ids)}, "
            f"loaded causal_chain ids: {sorted(loaded_ids)}"
        )

    def test_retrieval_loads_all_hc_nodes(self) -> None:
        hc_ids = {p.stem for p in self.hc_paths}
        loaded_ids = {n.get("node_id") for n in self.causal_chains}
        missing = hc_ids - loaded_ids
        self.assertEqual(
            missing, set(),
            f"HC nodes not loaded by retrieval: {missing}"
        )

    def test_loaded_hc_nodes_have_governance_flags_false(self) -> None:
        for node in self.causal_chains:
            if not str(node.get("node_id", "")).startswith("HC_"):
                continue
            with self.subTest(node_id=node.get("node_id")):
                self.assertIs(node.get("safe_for_examiner"), False)
                self.assertIs(node.get("examiner_scoring_allowed"), False)

    def test_hc_nodes_do_not_require_injection_flag(self) -> None:
        """HC nodes must be indexable with ENABLE_PLANNER_CAUSAL_CHAIN_INJECTION = False."""
        from tools.retrieval.tutor_retrieval_sandbox import ENABLE_PLANNER_CAUSAL_CHAIN_INJECTION
        self.assertFalse(
            ENABLE_PLANNER_CAUSAL_CHAIN_INJECTION,
            "ENABLE_PLANNER_CAUSAL_CHAIN_INJECTION must remain False"
        )
        hc_ids = {p.stem for p in self.hc_paths}
        loaded_ids = {n.get("node_id") for n in self.causal_chains}
        self.assertTrue(
            hc_ids.issubset(loaded_ids),
            "HC nodes are not retrievable without ENABLE_PLANNER_CAUSAL_CHAIN_INJECTION"
        )


if __name__ == "__main__":
    unittest.main()
