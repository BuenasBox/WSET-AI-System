"""Read-only contract tests for future knowledge-map manifest regeneration."""

from __future__ import annotations

import hashlib
import json
import re
import unittest
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).parents[1]
KNOWLEDGE_MAP_ROOT = ROOT / "knowledge" / "knowledge-map"
MANIFEST_PATH = KNOWLEDGE_MAP_ROOT / "manifests" / "knowledge_map_manifest.json"
CONTRACT_PATH = ROOT / "docs" / "KNOWLEDGE_MAP_MANIFEST_REGENERATION_CONTRACT.md"

NODE_DIRS = {
    "concept": KNOWLEDGE_MAP_ROOT / "concepts",
    "misconception": KNOWLEDGE_MAP_ROOT / "misconceptions",
    "causal_chain": KNOWLEDGE_MAP_ROOT / "causal-chains",
    "relationship": KNOWLEDGE_MAP_ROOT / "relationships",
}

ID_FIELDS = (
    "concept_id",
    "misconception_id",
    "chain_id",
    "node_id",
    "relationship_id",
)

ID_PATTERNS = {
    "concept_id": re.compile(r"^C_[A-Z0-9_]+$"),
    "misconception_id": re.compile(r"^MC_[A-Z0-9_]+$"),
    "chain_id": re.compile(r"^CC_[A-Z0-9_]+$"),
    "node_id": re.compile(r"^CC_[A-Z0-9_]+$"),
    "relationship_id": re.compile(r"^R_[A-Z0-9_]+__[A-Z_]+__[A-Z0-9_]+$"),
}


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _manifest() -> dict[str, Any]:
    return _read_json(MANIFEST_PATH)


def _manifest_file_hash() -> str:
    return hashlib.sha256(MANIFEST_PATH.read_bytes()).hexdigest()


def _node_files() -> list[Path]:
    files: list[Path] = []
    for node_dir in NODE_DIRS.values():
        files.extend(sorted(node_dir.glob("*.json")))
    return sorted(files)


def _node_data() -> list[tuple[Path, dict[str, Any]]]:
    return [(path, _read_json(path)) for path in _node_files()]


def _node_id(data: dict[str, Any]) -> str:
    for field in ID_FIELDS:
        value = data.get(field)
        if value:
            return str(value)
    return ""


def _manifest_registered_files(manifest: dict[str, Any]) -> set[Path]:
    files: set[Path] = set()
    for section in ("concepts", "misconceptions", "causal_chains", "relationships"):
        for entry in manifest.get(section, []):
            file_path = entry.get("file")
            if file_path:
                files.add(ROOT / file_path)
    return files


def _actual_node_count() -> int:
    return len(_node_files())


def _manifest_total_nodes(manifest: dict[str, Any]) -> int:
    summary = manifest.get("summary", {})
    if "total_nodes" in summary:
        return int(summary["total_nodes"])
    return sum(
        len(manifest.get(section, []))
        for section in ("concepts", "misconceptions", "causal_chains", "relationships")
    )


def _detect_causal_chain_family(data: dict[str, Any]) -> str:
    has_legacy = bool(
        data.get("chain_id")
        and data.get("starting_factor")
        and data.get("intermediate_steps")
        and data.get("final_outcome")
    )
    has_governance = bool(
        data.get("node_id")
        and data.get("trigger_keywords")
        and data.get("steps")
        and ("safe_for_examiner" in data or "governance" in data)
    )
    if has_legacy and has_governance:
        return "causal_chain_hybrid"
    if has_legacy:
        return "causal_chain_legacy"
    if has_governance:
        return "causal_chain_governance"
    return "unknown"


def _known_ids() -> set[str]:
    return {_node_id(data) for _, data in _node_data() if _node_id(data)}


def _unresolved_references() -> list[tuple[Path, str, str]]:
    known = _known_ids()
    unresolved: list[tuple[Path, str, str]] = []
    reference_fields = (
        "common_misconceptions",
        "related_concepts",
        "cause_effect_links",
        "linked_misconceptions",
        "linked_topics",
        "related_topics",
        "source_concept",
        "target_concept",
    )
    for path, data in _node_data():
        for field in reference_fields:
            value = data.get(field)
            values = value if isinstance(value, list) else [value]
            for item in values:
                if not isinstance(item, str) or not item:
                    continue
                if item.startswith("T_"):
                    unresolved.append((path, field, item))
                elif item.startswith(("C_", "MC_", "CC_", "R_")) and item not in known:
                    unresolved.append((path, field, item))
    return unresolved


class KnowledgeMapManifestContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self._manifest_hash_before = _manifest_file_hash()

    def tearDown(self) -> None:
        self.assertEqual(
            self._manifest_hash_before,
            _manifest_file_hash(),
            "Contract tests must not modify knowledge_map_manifest.json",
        )

    def test_current_manifest_file_exists(self) -> None:
        self.assertTrue(MANIFEST_PATH.exists())
        self.assertIsInstance(_manifest(), dict)

    def test_tree_contains_more_substantive_nodes_than_manifest(self) -> None:
        manifest = _manifest()
        self.assertGreater(_actual_node_count(), _manifest_total_nodes(manifest))

    def test_no_manifest_listed_file_is_missing(self) -> None:
        missing = [
            path
            for path in sorted(_manifest_registered_files(_manifest()))
            if not path.exists()
        ]
        self.assertEqual(missing, [])

    def test_no_duplicate_ids_in_actual_tree(self) -> None:
        ids = [_node_id(data) for _, data in _node_data()]
        duplicates = [node_id for node_id, count in Counter(ids).items() if count > 1]
        self.assertEqual(duplicates, [])

    def test_no_substantive_json_node_is_missing_id(self) -> None:
        missing = [path.as_posix() for path, data in _node_data() if not _node_id(data)]
        self.assertEqual(missing, [])

    def test_no_malformed_ids_in_actual_tree(self) -> None:
        malformed: list[str] = []
        for path, data in _node_data():
            for field, pattern in ID_PATTERNS.items():
                value = data.get(field)
                if value and not pattern.match(str(value)):
                    malformed.append(f"{path.as_posix()}:{field}={value}")
        self.assertEqual(malformed, [])

    def test_unresolved_references_are_detectable(self) -> None:
        unresolved = _unresolved_references()
        values = {value for _, _, value in unresolved}
        self.assertIn("C_ALCOHOL", values)
        self.assertTrue(any(value.startswith("T_RA") for value in values))

    def test_causal_chain_schema_families_are_mixed(self) -> None:
        families = {
            _detect_causal_chain_family(_read_json(path))
            for path in sorted(NODE_DIRS["causal_chain"].glob("*.json"))
        }
        self.assertIn("causal_chain_legacy", families)
        self.assertIn("causal_chain_governance", families)
        self.assertIn("causal_chain_hybrid", families)

    def test_future_manifest_contract_requires_unresolved_references(self) -> None:
        text = CONTRACT_PATH.read_text(encoding="utf-8")
        self.assertIn("unresolved_references", text)

    def test_future_manifest_contract_requires_schema_families(self) -> None:
        text = CONTRACT_PATH.read_text(encoding="utf-8")
        self.assertIn("schema_families", text)

    def test_future_manifest_contract_requires_governance_summary(self) -> None:
        text = CONTRACT_PATH.read_text(encoding="utf-8")
        self.assertIn("governance_summary", text)


if __name__ == "__main__":
    unittest.main()
