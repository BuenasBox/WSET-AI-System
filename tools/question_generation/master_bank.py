"""Canonical deterministic question-bank importer and collection exporter.

This module consolidates existing repository artifacts. It does not generate,
rewrite, score, ground, or semantically review question content.
"""

from __future__ import annotations

import argparse
import copy
import json
import re
from collections import Counter
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from tools.constants import PROJECT_ROOT
from tools.question_generation.master_bank_resolution import (
    RESOLUTION_PATH,
    apply_source_resolution,
    load_resolution_index,
    resolution_destination,
)


MASTER_BANK_VERSION = "master_bank_v1"
IMPORTER_VERSION = "master_bank_importer_v1"
SOURCE_BANK_PATH = Path("knowledge/question-bank/structured/wset3_questions.json")
MASTER_BANK_PATH = Path("knowledge/question-bank/master_bank/master_bank.json")
SCHEMA_PATH = Path("knowledge/question-bank/master_bank/master_bank.schema.json")
SBA_DRAFT_PATHS = (
    Path("knowledge/question-bank/diagnostic_sba/drafts/first_5_enrichment_drafts.json"),
    Path("knowledge/question-bank/diagnostic_sba/drafts/gold_bank_activation_drafts.json"),
)
SBA_REVIEW_PATHS = (
    Path("knowledge/question-bank/diagnostic_sba/reviews/first_5_human_review_records.json"),
    Path("knowledge/question-bank/diagnostic_sba/reviews/gold_bank_activation_review_records.json"),
)
GOLD_REVIEW_PATH = SBA_REVIEW_PATHS[1]
OPEN_CANDIDATES_PATH = Path(
    "knowledge/question-bank/open_response/normalized/diagnostic_open_response_candidates.json"
)
OPEN_REVIEWS_PATH = Path(
    "knowledge/question-bank/open_response/reviews/open_response_review_records.json"
)
PUBLIC_LAB_PATH = Path("frontend/diagnostic-sba/preguntas.json")

COLLECTION_NAMES = (
    "single_best_answer",
    "open_response",
    "inactive",
    "needs_review",
    "gold",
    "public_lab",
)
SAFE_GOVERNANCE = {
    "safe_for_examiner": False,
    "examiner_scoring_allowed": False,
    "official_wset_question": False,
    "training_item_only": True,
    "uses_llm": False,
    "uses_api": False,
    "uses_embeddings": False,
    "uses_vector_db": False,
    "cloud_services_active": False,
}
OPEN_RESPONSE_TYPES = frozenset({"short_answer", "open_response"})
SBA_APPROVED = "approved_for_static_demo"
OPEN_APPROVED = "approved"


def build_master_bank(root: str | Path = PROJECT_ROOT) -> dict[str, Any]:
    """Build the canonical bank in memory from existing repository artifacts."""
    root_path = Path(root)
    source_records = _load_list(root_path / SOURCE_BANK_PATH)
    sba_drafts = _load_many_lists(root_path, SBA_DRAFT_PATHS)
    sba_reviews = _load_many_lists(root_path, SBA_REVIEW_PATHS)
    gold_reviews = _load_list(root_path / GOLD_REVIEW_PATH)
    open_candidates = _load_list(root_path / OPEN_CANDIDATES_PATH)
    open_reviews = _load_list(root_path / OPEN_REVIEWS_PATH)
    public_payload = _load_mapping(root_path / PUBLIC_LAB_PATH)
    resolution_by_source = load_resolution_index(root=root_path)
    public_items = [
        item for item in public_payload.get("items", []) if isinstance(item, Mapping)
    ]

    draft_by_source = _index_by_source_id(sba_drafts, nested_identity=True)
    sba_review_by_source = _index_by_source_id(sba_reviews)
    open_candidate_by_source = _index_by_source_id(open_candidates)
    open_review_by_source = _index_by_source_id(open_reviews)
    public_by_source = _index_by_source_id(public_items)
    gold_source_ids = {
        _source_id(review)
        for review in gold_reviews
        if review.get("review_status") == SBA_APPROVED
    }

    items = [
        _build_master_item(
            record,
            draft_by_source=draft_by_source,
            sba_review_by_source=sba_review_by_source,
            open_candidate_by_source=open_candidate_by_source,
            open_review_by_source=open_review_by_source,
            public_by_source=public_by_source,
            gold_source_ids=gold_source_ids,
            resolution_by_source=resolution_by_source,
        )
        for record in source_records
    ]
    items.sort(key=lambda item: _numeric_sort_key(item["source_question_id"]))

    collections = {
        name: [
            item["master_item_id"]
            for item in items
            if name in item["collections"]
        ]
        for name in COLLECTION_NAMES
    }
    counts = {
        "total": len(items),
        **{name: len(collections[name]) for name in COLLECTION_NAMES},
        "review_states": dict(
            sorted(Counter(item["status"]["review_state"] for item in items).items())
        ),
    }

    return {
        "schema_version": MASTER_BANK_VERSION,
        "importer_version": IMPORTER_VERSION,
        "source_bank": SOURCE_BANK_PATH.as_posix(),
        "schema_path": SCHEMA_PATH.as_posix(),
        "generated_at": None,
        "counts": counts,
        "collections": collections,
        "items": items,
        "governance": copy.deepcopy(SAFE_GOVERNANCE),
    }


def write_master_bank(
    payload: Mapping[str, Any],
    path: str | Path = MASTER_BANK_PATH,
    root: str | Path = PROJECT_ROOT,
) -> Path:
    """Validate and write one deterministic canonical master-bank artifact."""
    errors = validate_master_bank(payload)
    if errors:
        raise ValueError("invalid master bank: " + "; ".join(errors))
    output_path = Path(root) / Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return output_path


def build_collection_export(
    master_bank: Mapping[str, Any],
    collection: str,
) -> dict[str, Any]:
    """Return one collection as a standalone deterministic in-memory export."""
    if collection not in COLLECTION_NAMES:
        raise ValueError(f"collection must be one of: {', '.join(COLLECTION_NAMES)}")
    item_ids = list(_mapping(master_bank.get("collections")).get(collection, []))
    by_id = {
        str(item.get("master_item_id")): item
        for item in master_bank.get("items", [])
        if isinstance(item, Mapping)
    }
    items = [copy.deepcopy(by_id[item_id]) for item_id in item_ids if item_id in by_id]
    return {
        "schema_version": "master_bank_collection_export_v1",
        "master_bank_version": master_bank.get("schema_version"),
        "collection": collection,
        "item_count": len(items),
        "items": items,
        "governance": copy.deepcopy(SAFE_GOVERNANCE),
    }


def validate_master_bank(payload: Any) -> list[str]:
    """Return structural, count, lineage, and governance errors."""
    if not isinstance(payload, Mapping):
        return ["master bank must be an object"]

    errors: list[str] = []
    if payload.get("schema_version") != MASTER_BANK_VERSION:
        errors.append(f"schema_version must be {MASTER_BANK_VERSION}")
    if payload.get("importer_version") != IMPORTER_VERSION:
        errors.append(f"importer_version must be {IMPORTER_VERSION}")
    if payload.get("source_bank") != SOURCE_BANK_PATH.as_posix():
        errors.append("source_bank must point to the structured canonical source")
    if payload.get("governance") != SAFE_GOVERNANCE:
        errors.append("master bank governance must match safe defaults")

    items = payload.get("items")
    collections = payload.get("collections")
    counts = payload.get("counts")
    if not isinstance(items, list):
        return errors + ["items must be a list"]
    if not isinstance(collections, Mapping):
        return errors + ["collections must be an object"]
    if not isinstance(counts, Mapping):
        return errors + ["counts must be an object"]

    ids: list[str] = []
    source_ids: list[str] = []
    for item in items:
        if not isinstance(item, Mapping):
            errors.append("every item must be an object")
            continue
        master_id = str(item.get("master_item_id", ""))
        source_id = str(item.get("source_question_id", ""))
        ids.append(master_id)
        source_ids.append(source_id)
        if master_id != f"wset3_{source_id}":
            errors.append(f"{master_id or source_id}: invalid master_item_id")
        if item.get("question_type") not in {"single_best_answer", "open_response"}:
            errors.append(f"{master_id}: invalid question_type")
        if item.get("governance") != SAFE_GOVERNANCE:
            errors.append(f"{master_id}: unsafe governance")
        lineage = item.get("lineage")
        if not isinstance(lineage, Mapping):
            errors.append(f"{master_id}: lineage must be an object")
        elif lineage.get("structured_source") != SOURCE_BANK_PATH.as_posix():
            errors.append(f"{master_id}: structured_source lineage mismatch")
        item_collections = item.get("collections")
        if not isinstance(item_collections, list) or not item_collections:
            errors.append(f"{master_id}: collections must be a non-empty list")
        elif any(name not in COLLECTION_NAMES for name in item_collections):
            errors.append(f"{master_id}: unknown collection")
        if item.get("status", {}).get("activation_status") == "public_lab":
            if "public_lab" not in item_collections:
                errors.append(f"{master_id}: public status without public_lab collection")
        elif "inactive" not in item_collections:
            errors.append(f"{master_id}: non-public item must be inactive")

    if len(ids) != len(set(ids)):
        errors.append("master_item_id values must be unique")
    if len(source_ids) != len(set(source_ids)):
        errors.append("source_question_id values must be unique")

    id_set = set(ids)
    for name in COLLECTION_NAMES:
        values = collections.get(name)
        if not isinstance(values, list):
            errors.append(f"collections.{name} must be a list")
            continue
        if len(values) != len(set(values)):
            errors.append(f"collections.{name} contains duplicates")
        if not set(values).issubset(id_set):
            errors.append(f"collections.{name} contains unknown item IDs")
        expected = [
            item["master_item_id"]
            for item in items
            if isinstance(item, Mapping) and name in item.get("collections", [])
        ]
        if values != expected:
            errors.append(f"collections.{name} does not match item membership/order")
        if counts.get(name) != len(values):
            errors.append(f"counts.{name} does not match collection")
    if counts.get("total") != len(items):
        errors.append("counts.total does not match items")
    return errors


def _build_master_item(
    record: Mapping[str, Any],
    *,
    draft_by_source: Mapping[str, Mapping[str, Any]],
    sba_review_by_source: Mapping[str, Mapping[str, Any]],
    open_candidate_by_source: Mapping[str, Mapping[str, Any]],
    open_review_by_source: Mapping[str, Mapping[str, Any]],
    public_by_source: Mapping[str, Mapping[str, Any]],
    gold_source_ids: set[str],
    resolution_by_source: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    source_id = str(record.get("question_id", "")).strip()
    resolution = resolution_by_source.get(source_id, {})
    record = apply_source_resolution(record, resolution)
    is_open = str(record.get("question_type", "")).strip().lower() in OPEN_RESPONSE_TYPES
    question_type = "open_response" if is_open else "single_best_answer"
    sba_draft = draft_by_source.get(source_id, {})
    sba_review = sba_review_by_source.get(source_id, {})
    open_candidate = open_candidate_by_source.get(source_id, {})
    open_review = open_review_by_source.get(source_id, {})
    public_item = public_by_source.get(source_id, {})
    is_public = bool(public_item)
    is_gold = source_id in gold_source_ids

    review_state = _review_state(
        is_open=is_open,
        sba_review=sba_review,
        open_review=open_review,
    )
    destination = resolution_destination(resolution)
    if destination == "sba_operational" and not is_public:
        review_state = "approved_private_sba"
    elif destination == "open_response_candidate":
        review_state = "approved_open_response"
    elif destination == "quarantine":
        review_state = "quarantine"
    collections = [question_type]
    if not is_public:
        collections.append("inactive")
    if review_state in {"unreviewed", "requires_revision", "preserve_only", "rejected"}:
        collections.append("needs_review")
    if is_gold:
        collections.append("gold")
    if is_public:
        collections.append("public_lab")

    topics = _string_list(record.get("expected_topics"))
    public_ra = str(public_item.get("ra_id", "")).strip()
    ra = public_ra or _extract_ra(topics)
    public_topic = str(public_item.get("topic", "")).strip()
    topic = public_topic or _topic_from_expected(topics, ra)
    difficulty = str(
        public_item.get("difficulty") or record.get("difficulty") or "unknown"
    ).strip().lower()

    return {
        "master_item_id": f"wset3_{source_id}",
        "source_question_id": source_id,
        "question_type": question_type,
        "stem": str(record.get("question_text", "")).strip(),
        "curriculum": {
            "ra": ra or "unknown",
            "topic": topic or "unknown",
            "difficulty": difficulty or "unknown",
            "expected_topics": topics,
            "expected_keywords": _string_list(record.get("expected_keywords")),
            "expected_causal_links": _string_list(record.get("expected_causal_links")),
            "expected_reasoning_type": str(
                record.get("expected_reasoning_type", "")
            ).strip(),
        },
        "source_content": {
            "options": copy.deepcopy(record.get("options")),
            "correct_answer_letter": record.get("correct_answer_letter"),
            "correct_answer_text": record.get("correct_answer_text"),
        },
        "status": {
            "review_state": review_state,
            "activation_status": "public_lab" if is_public else "inactive",
            "gold": is_gold,
            "public_lab": is_public,
        },
        "collections": collections,
        "lineage": {
            "structured_source": SOURCE_BANK_PATH.as_posix(),
            "raw_source": str(record.get("source_type", "")).strip() or "unknown",
            "sba_draft_id": _nested_value(sba_draft, "identity", "item_id"),
            "sba_review_id": sba_review.get("review_id"),
            "open_response_candidate_id": (
                f"diagnostic_open_response_{source_id}" if open_candidate else None
            ),
            "open_response_review_id": open_review.get("review_id"),
            "gold_review_id": (
                sba_review.get("review_id") if is_gold else None
            ),
            "public_lab_item_id": public_item.get("item_id"),
            **(
                {
                    "resolution_artifact": RESOLUTION_PATH.as_posix(),
                    "resolution_id": resolution.get("resolution_id"),
                }
                if resolution
                else {}
            ),
        },
        "governance": copy.deepcopy(SAFE_GOVERNANCE),
    }


def _review_state(
    *,
    is_open: bool,
    sba_review: Mapping[str, Any],
    open_review: Mapping[str, Any],
) -> str:
    if is_open:
        status = str(open_review.get("review_status", "")).strip()
        if status == OPEN_APPROVED:
            return "approved_open_response"
        return status or "unreviewed"
    return str(sba_review.get("review_status", "")).strip() or "unreviewed"


def _load_list(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError(f"{path.as_posix()} must contain a JSON list")
    return [dict(item) for item in data if isinstance(item, Mapping)]


def _load_mapping(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, Mapping):
        raise ValueError(f"{path.as_posix()} must contain a JSON object")
    return dict(data)


def _load_many_lists(root: Path, paths: Sequence[Path]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for path in paths:
        records.extend(_load_list(root / path))
    return records


def _index_by_source_id(
    records: Sequence[Mapping[str, Any]],
    *,
    nested_identity: bool = False,
) -> dict[str, Mapping[str, Any]]:
    indexed: dict[str, Mapping[str, Any]] = {}
    for record in records:
        source_id = (
            str(_nested_value(record, "identity", "source_question_id") or "").strip()
            if nested_identity
            else _source_id(record)
        )
        if source_id:
            indexed[source_id] = record
    return indexed


def _source_id(record: Mapping[str, Any]) -> str:
    return str(record.get("source_question_id", "")).strip()


def _nested_value(record: Mapping[str, Any], parent: str, field: str) -> Any:
    return _mapping(record.get(parent)).get(field)


def _extract_ra(topics: Sequence[str]) -> str:
    for topic in topics:
        match = re.search(r"\bRA\s*([1-5])\b", topic, flags=re.IGNORECASE)
        if match:
            return f"RA{match.group(1)}"
    return ""


def _topic_from_expected(topics: Sequence[str], ra: str) -> str:
    for topic in topics:
        if ra and topic.upper().startswith(ra.upper()):
            continue
        return topic
    return topics[0] if topics else ""


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item).strip() for item in value if str(item).strip()]


def _numeric_sort_key(value: Any) -> tuple[int, str]:
    text = str(value)
    digits = "".join(char for char in text if char.isdigit())
    return (int(digits) if digits else 0, text)


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _cli() -> int:
    parser = argparse.ArgumentParser(description="Build the canonical master bank.")
    parser.add_argument("--check", action="store_true", help="Validate without writing.")
    parser.add_argument(
        "--collection",
        choices=COLLECTION_NAMES,
        help="Print one collection export as JSON without writing.",
    )
    args = parser.parse_args()

    payload = build_master_bank()
    errors = validate_master_bank(payload)
    if errors:
        raise SystemExit("\n".join(errors))
    if args.collection:
        print(json.dumps(build_collection_export(payload, args.collection), indent=2, ensure_ascii=False))
    elif args.check:
        print(json.dumps(payload["counts"], indent=2, ensure_ascii=False))
    else:
        output = write_master_bank(payload)
        print(output.as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(_cli())
