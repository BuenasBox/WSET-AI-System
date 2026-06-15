"""Governed deterministic integration for the SBA gap-closure batches."""

from __future__ import annotations

import argparse
import copy
import json
import re
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from tools.constants import PROJECT_ROOT
from tools.question_generation.master_bank import (
    MASTER_BANK_PATH,
    build_master_bank,
    validate_master_bank,
    write_master_bank,
)
from tools.question_generation.master_bank_resolution import RESOLUTION_PATH


SOURCE_BANK_PATH = Path("knowledge/question-bank/structured/wset3_questions.json")
ENRICHMENT_PATH = Path("knowledge/question-bank/enrichment/sba_enrichment_v1.json")
BATCH_SCHEMA_VERSION = "sba_gap_closure_batch_v1"
BATCH_SIZE = 47
OPTION_KEYS = ("A", "B", "C", "D")
SUPPORTED_RAS = {"RA1", "RA2", "RA3", "RA4", "RA5"}
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
IDENTIFICATION_ONLY = (
    re.compile(r"^\s*¿?(qué|cuál)\s+(uva|variedad|región|país|zona)\b", re.IGNORECASE),
    re.compile(r"^\s*¿?dónde\b", re.IGNORECASE),
    re.compile(r"^\s*¿?qué\s+es\b", re.IGNORECASE),
)
UNSAFE_LANGUAGE = (
    "official wset question",
    "examiner score",
    "examiner mark",
    "guaranteed pass",
    "predicted pass",
)
REQUIRED_ENRICHMENT_FIELDS = (
    "causal_chain_candidate",
    "feedback_profile",
    "micro_drill_candidate",
    "misconception_linkage_candidate",
)


def validate_batch_payload(payload: Any) -> list[str]:
    """Return deterministic validation errors for one 47-item batch."""
    if not isinstance(payload, Mapping):
        return ["batch payload must be an object"]
    errors: list[str] = []
    if payload.get("schema_version") != BATCH_SCHEMA_VERSION:
        errors.append(f"schema_version must be {BATCH_SCHEMA_VERSION}")
    if payload.get("governance") != SAFE_GOVERNANCE:
        errors.append("batch governance must match safe defaults")
    records = payload.get("records")
    if not isinstance(records, list):
        return errors + ["records must be a list"]
    if len(records) != BATCH_SIZE:
        errors.append(f"records must contain exactly {BATCH_SIZE} items")

    ids: list[str] = []
    stems: list[str] = []
    option_sets: list[tuple[str, ...]] = []
    for index, record in enumerate(records):
        prefix = f"records[{index}]"
        if not isinstance(record, Mapping):
            errors.append(f"{prefix} must be an object")
            continue
        question_id = str(record.get("question_id", "")).strip()
        ids.append(question_id)
        if not question_id.isdigit():
            errors.append(f"{prefix}.question_id must be numeric")
        stem = str(record.get("question_text", "")).strip()
        normalized_stem = _normalize(stem)
        stems.append(normalized_stem)
        if not stem:
            errors.append(f"{prefix}.question_text must be non-empty")
        if any(pattern.search(stem) for pattern in IDENTIFICATION_ONLY):
            errors.append(f"{prefix}.question_text is identification-only")
        if not any(
            marker in normalized_stem
            for marker in (
                "qué resultado",
                "que resultado",
                "qué consecuencia",
                "que consecuencia",
                "qué factor explica",
                "que factor explica",
                "qué opción explica",
                "que opcion explica",
                "más probable",
                "mas probable",
                "mejor explica",
                "mejor decisión",
                "mejor decision",
                "mejor recomendación",
                "mejor recomendacion",
                "qué interpretación",
                "que interpretacion",
                "qué secuencia",
                "que secuencia",
                "qué decisión",
                "que decision",
                "qué recomendación",
                "que recomendacion",
                "compar",
                "si el productor",
                "si una bodega",
                "si el sumiller",
                "si un restaurante",
            )
        ):
            errors.append(f"{prefix}.question_text lacks an explicit reasoning frame")

        topics = record.get("expected_topics")
        ra = str(topics[0]).strip() if isinstance(topics, list) and topics else ""
        if ra not in SUPPORTED_RAS:
            errors.append(f"{prefix}.expected_topics must start with a valid RA")
        if record.get("question_type") != "theory":
            errors.append(f"{prefix}.question_type must be theory")
        if record.get("safe_for_examiner") is not False:
            errors.append(f"{prefix}.safe_for_examiner must be false")
        if record.get("governance") != SAFE_GOVERNANCE:
            errors.append(f"{prefix}.governance must match safe defaults")

        options = record.get("options")
        if not isinstance(options, Mapping) or set(options) != set(OPTION_KEYS):
            errors.append(f"{prefix}.options must contain exactly A, B, C, and D")
            normalized_options: tuple[str, ...] = ()
        else:
            normalized_options = tuple(_normalize(options[key]) for key in OPTION_KEYS)
            if any(not value for value in normalized_options):
                errors.append(f"{prefix}.options must all be non-empty")
            if len(set(normalized_options)) != len(OPTION_KEYS):
                errors.append(f"{prefix}.options must be unique")
        option_sets.append(tuple(sorted(normalized_options)))
        correct_letter = str(record.get("correct_answer_letter", "")).strip()
        if correct_letter not in OPTION_KEYS:
            errors.append(f"{prefix}.correct_answer_letter must be A, B, C, or D")
        elif isinstance(options, Mapping):
            correct_text = str(record.get("correct_answer_text", "")).strip()
            if correct_text != str(options.get(correct_letter, "")).strip():
                errors.append(f"{prefix}.correct_answer_text must match the keyed option")

        source_support = record.get("source_support")
        if not isinstance(source_support, Mapping):
            errors.append(f"{prefix}.source_support must be present")
        else:
            for field in ("source_ids", "source_files"):
                if not isinstance(source_support.get(field), list) or not source_support[field]:
                    errors.append(f"{prefix}.source_support.{field} must be non-empty")
            if not str(source_support.get("support_rationale", "")).strip():
                errors.append(
                    f"{prefix}.source_support.support_rationale must be non-empty"
                )

        enrichment = record.get("enrichment")
        if not isinstance(enrichment, Mapping):
            errors.append(f"{prefix}.enrichment must be present")
        else:
            for field in REQUIRED_ENRICHMENT_FIELDS:
                if not isinstance(enrichment.get(field), Mapping) or not enrichment[field]:
                    errors.append(f"{prefix}.enrichment.{field} must be present")

        lowered_blob = json.dumps(record, ensure_ascii=False).lower()
        for phrase in UNSAFE_LANGUAGE:
            if phrase in lowered_blob:
                errors.append(f"{prefix} contains unsafe authority language: {phrase}")

    if len(ids) != len(set(ids)):
        errors.append("question_id values must be unique")
    if len(stems) != len(set(stems)):
        errors.append("question_text values must be unique after normalization")
    if len(option_sets) != len(set(option_sets)):
        errors.append("option sets must be unique after normalization")
    return errors


def load_batch(path: str | Path) -> dict[str, Any]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    errors = validate_batch_payload(payload)
    if errors:
        raise ValueError("invalid SBA batch: " + "; ".join(errors))
    return dict(payload)


def integrate_batch(
    batch_path: str | Path,
    *,
    root: str | Path = PROJECT_ROOT,
) -> dict[str, Any]:
    """Integrate one validated batch into backend corpus artifacts."""
    root_path = Path(root)
    payload = load_batch(batch_path)
    source_path = root_path / SOURCE_BANK_PATH
    resolution_path = root_path / RESOLUTION_PATH
    enrichment_path = root_path / ENRICHMENT_PATH

    source_records = _load_json(source_path)
    resolution_payload = _load_json(resolution_path)
    enrichment_payload = _load_json(enrichment_path)
    if not isinstance(source_records, list):
        raise ValueError("structured source bank must be a list")
    existing_ids = {str(record.get("question_id", "")).strip() for record in source_records}
    new_ids = [str(record["question_id"]) for record in payload["records"]]
    overlap = sorted(existing_ids.intersection(new_ids), key=int)
    if overlap:
        raise ValueError(f"batch IDs already exist in structured bank: {overlap}")

    updated_source = copy.deepcopy(source_records) + [
        _structured_record(record) for record in payload["records"]
    ]
    updated_resolutions = _updated_resolution_payload(
        resolution_payload, payload["batch_id"], payload["records"]
    )
    updated_enrichment = _updated_enrichment_payload(
        enrichment_payload, payload["batch_id"], payload["records"]
    )

    source_path.write_text(
        json.dumps(updated_source, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    resolution_path.write_text(
        json.dumps(updated_resolutions, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    master_bank = build_master_bank(root_path)
    master_errors = validate_master_bank(master_bank)
    if master_errors:
        raise ValueError("invalid rebuilt master bank: " + "; ".join(master_errors))
    write_master_bank(master_bank, path=MASTER_BANK_PATH, root=root_path)
    enrichment_path.write_text(
        json.dumps(updated_enrichment, ensure_ascii=False, sort_keys=True, indent=2)
        + "\n",
        encoding="utf-8",
    )
    return {
        "batch_id": payload["batch_id"],
        "added": len(payload["records"]),
        "source_total": len(updated_source),
        "master_counts": master_bank["counts"],
        "enrichment_total": len(updated_enrichment["items_by_source_question_id"]),
        "governance": copy.deepcopy(SAFE_GOVERNANCE),
    }


def refresh_batch_enrichment(
    batch_path: str | Path,
    *,
    root: str | Path = PROJECT_ROOT,
) -> dict[str, Any]:
    """Refresh enrichment records for an already integrated validated batch."""
    root_path = Path(root)
    payload = load_batch(batch_path)
    enrichment_path = root_path / ENRICHMENT_PATH
    enrichment_payload = _load_json(enrichment_path)
    by_source = enrichment_payload.get("items_by_source_question_id")
    if not isinstance(by_source, dict):
        raise ValueError("enrichment sidecar items_by_source_question_id must be an object")
    for record in payload["records"]:
        source_id = str(record["question_id"])
        if source_id not in by_source:
            raise ValueError(f"cannot refresh missing enrichment record {source_id}")
        by_source[source_id] = _enrichment_record(record, payload["batch_id"])
    enrichment_path.write_text(
        json.dumps(enrichment_payload, ensure_ascii=False, sort_keys=True, indent=2)
        + "\n",
        encoding="utf-8",
    )
    return {
        "batch_id": payload["batch_id"],
        "refreshed": len(payload["records"]),
        "enrichment_total": len(by_source),
        "governance": copy.deepcopy(SAFE_GOVERNANCE),
    }


def _structured_record(record: Mapping[str, Any]) -> dict[str, Any]:
    return {
        key: copy.deepcopy(value)
        for key, value in record.items()
        if key not in {"enrichment", "governance", "source_support"}
    }


def _updated_resolution_payload(
    payload: Any,
    batch_id: str,
    records: list[dict[str, Any]],
) -> dict[str, Any]:
    if not isinstance(payload, Mapping) or not isinstance(payload.get("records"), list):
        raise ValueError("resolution artifact has invalid shape")
    updated = copy.deepcopy(dict(payload))
    existing = {
        str(record.get("source_question_id", "")).strip()
        for record in updated["records"]
        if isinstance(record, Mapping)
    }
    for record in records:
        source_id = str(record["question_id"])
        if source_id in existing:
            raise ValueError(f"resolution already exists for {source_id}")
        updated["records"].append(
            {
                "resolution_id": f"sba_gap_closure_{batch_id.lower()}_{source_id}",
                "source_question_id": source_id,
                "source_pool": "sba_gap_closure",
                "destination": "sba_operational",
                "resolution_reason": (
                    "Governed specification-gap SBA authored with explicit source "
                    "support, reasoning focus, and enrichment candidates."
                ),
                "repairs": ["added targeted specification-gap SBA"],
                "evidence_reviewed": list(record["source_support"]["source_files"]),
                "prior_review_reason": None,
                "prior_recommendation": None,
                "source_overrides": {},
                "quarantine_analysis": {
                    "required": False,
                    "why_sba_not_possible": None,
                    "why_open_response_not_possible": None,
                },
            }
        )
    updated["record_count"] = len(updated["records"])
    updated["governance"] = copy.deepcopy(SAFE_GOVERNANCE)
    return updated


def _updated_enrichment_payload(
    payload: Any,
    batch_id: str,
    records: list[dict[str, Any]],
) -> dict[str, Any]:
    if not isinstance(payload, Mapping):
        raise ValueError("enrichment sidecar must be an object")
    updated = copy.deepcopy(dict(payload))
    by_source = updated.get("items_by_source_question_id")
    if not isinstance(by_source, dict):
        raise ValueError("enrichment sidecar items_by_source_question_id must be an object")
    for record in records:
        source_id = str(record["question_id"])
        if source_id in by_source:
            raise ValueError(f"enrichment already exists for {source_id}")
        by_source[source_id] = _enrichment_record(record, batch_id)
    updated["phase"] = f"{updated.get('phase', 'sba_enrichment_v1')} + {batch_id}"
    updated["gap_closure_batch_count"] = int(updated.get("gap_closure_batch_count", 0)) + 1
    updated["governance"] = {
        "safe_for_examiner": False,
        "examiner_scoring_allowed": False,
        "formative_only": True,
        "derived_content": False,
        "uses_llm": False,
        "uses_api": False,
    }
    return updated


def _enrichment_record(record: Mapping[str, Any], batch_id: str) -> dict[str, Any]:
    enrichment = record["enrichment"]
    chain = enrichment["causal_chain_candidate"]
    feedback = enrichment["feedback_profile"]
    drill = enrichment["micro_drill_candidate"]
    misconception = enrichment["misconception_linkage_candidate"]
    options = record["options"]
    correct_letter = record["correct_answer_letter"]
    correct_index = OPTION_KEYS.index(correct_letter)
    return {
        "item_id": f"wset3_{record['question_id']}",
        "causal_chain": {
            "causa": chain["cause"],
            "mecanismo": chain["mechanism"],
            "efecto": chain["effect"],
        },
        "feedback_by_mode": {
            "mentor": feedback["correct_rationale"],
            "trainer": feedback["remediation_recommendation"],
            "reviewer": " ".join(
                feedback["distractor_rationales"][key]
                for key in OPTION_KEYS
                if key != correct_letter
            ),
        },
        "micro_drill": {
            "prompt": drill["prompt"],
            "options": [options[key] for key in OPTION_KEYS],
            "correct_index": correct_index,
            "explanation": feedback["correct_rationale"],
            "remediation_signal": feedback["remediation_recommendation"],
        },
        "misconception_linkage_candidate": copy.deepcopy(misconception),
        "_provenance": {
            "batch_id": batch_id,
            "causal_chain": {
                "candidate_id": chain["candidate_id"],
                "derived_from": "manual_gap_closure_v1",
            },
            "feedback_by_mode": {"derived_from": "manual_gap_closure_v1"},
            "micro_drill": {"derived_from": "manual_gap_closure_v1"},
            "source_support": copy.deepcopy(record["source_support"]),
        },
    }


def _normalize(value: Any) -> str:
    return " ".join(str(value).lower().split())


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _cli() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--batch", required=True, help="Path to one SBA batch JSON file.")
    parser.add_argument("--check", action="store_true", help="Validate without writing.")
    parser.add_argument(
        "--refresh-enrichment",
        action="store_true",
        help="Refresh enrichment records for an already integrated batch.",
    )
    args = parser.parse_args()
    payload = load_batch(args.batch)
    if args.check:
        print(
            json.dumps(
                {
                    "batch_id": payload["batch_id"],
                    "record_count": len(payload["records"]),
                    "governance": payload["governance"],
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    elif args.refresh_enrichment:
        print(
            json.dumps(
                refresh_batch_enrichment(args.batch),
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        print(json.dumps(integrate_batch(args.batch), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(_cli())
