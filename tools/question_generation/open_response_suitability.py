"""Shadow classification of Master Bank open-response suitability."""

from __future__ import annotations

import argparse
import copy
import json
import re
import unicodedata
from collections import Counter
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from tools.constants import PROJECT_ROOT
from tools.question_generation.master_bank import MASTER_BANK_PATH, SAFE_GOVERNANCE
from tools.question_generation.master_bank_resolution import (
    load_resolution_index,
    resolution_destination,
)


OUTPUT_PATH = Path(
    "knowledge/question-bank/open_response/suitability/"
    "master_bank_open_response_suitability.json"
)
CLASSIFIER_VERSION = "open_response_suitability_v1"
CLASSIFICATIONS = (
    "open_response_candidate",
    "human_review_required",
    "sba_only",
    "inactive",
)
EXPLANATION_PATTERNS = (
    r"\bexplica\b",
    r"\bexplique\b",
    r"\bexplain\b",
    r"\bcomo (?:afecta|contribuye|influye|impacta)\b",
    r"\bque efecto\b",
    r"\bcual es el efecto\b",
    r"\befecto\b",
    r"\bimpacto\b",
    r"\binfluencia\b",
    r"\bconsecuencia\b",
)
JUSTIFICATION_PATTERNS = (
    r"\bjustifica\b",
    r"\bjustifique\b",
    r"\bjustify\b",
    r"\bpor que\b",
)
COMPARISON_PATTERNS = (
    r"\bcompare\b",
    r"\bcompara\b",
    r"\bcontrasta\b",
    r"\bcontrast\b",
    r"\bdiferencia\b",
    r"\bdiferenciar\b",
    r"\bversus\b",
    r"\bvs\b",
)
RECOGNITION_FRAMING_PATTERNS = (
    r"\bcual de (?:los|las) siguientes\b",
    r"\bcual de estas\b",
    r"\bque (?:region|variedad|metodo|componente|factor)\b",
)
INACTIVE_REVIEW_STATES = frozenset({"preserve_only", "requires_revision", "rejected"})


def classify_open_response_suitability(item: Mapping[str, Any]) -> dict[str, Any]:
    """Classify one item from observable stem and metadata evidence."""
    stem = str(item.get("stem", "")).strip()
    normalized = _normalize(stem)
    curriculum = _mapping(item.get("curriculum"))
    status = _mapping(item.get("status"))
    question_type = str(item.get("question_type", "")).strip()
    review_state = str(status.get("review_state", "")).strip()
    causal_links = _string_list(curriculum.get("expected_causal_links"))
    expected_keywords = _string_list(curriculum.get("expected_keywords"))
    expected_topics = _string_list(curriculum.get("expected_topics"))

    requires_explanation = _matches_any(normalized, EXPLANATION_PATTERNS)
    requires_justification = _matches_any(normalized, JUSTIFICATION_PATTERNS)
    requires_comparison = _matches_any(normalized, COMPARISON_PATTERNS)
    requires_causal_chain = bool(causal_links) and (
        requires_explanation or requires_justification or requires_comparison
    )
    recognition_framing = _matches_any(normalized, RECOGNITION_FRAMING_PATTERNS)
    answer_boundary_support = len(expected_keywords) >= 3 or len(expected_topics) >= 3
    cognitive_demand_count = sum(
        (
            requires_explanation,
            requires_causal_chain,
            requires_comparison,
            requires_justification,
        )
    )
    inactive = _is_inactive_master_item(item)
    resolution = load_resolution_index().get(
        str(item.get("source_question_id", "")).strip(), {}
    )
    destination = resolution_destination(resolution)

    if destination == "sba_operational":
        classification = "sba_only"
        confidence = "high"
    elif destination == "open_response_candidate":
        classification = "open_response_candidate"
        confidence = "high"
    elif destination == "quarantine":
        classification = "inactive"
        confidence = "high"
    elif inactive:
        classification = "inactive"
        confidence = "high"
    elif question_type == "open_response" and review_state == "approved_open_response":
        classification = "open_response_candidate"
        confidence = "high"
    elif (
        question_type == "single_best_answer"
        and cognitive_demand_count >= 2
        and answer_boundary_support
        and not recognition_framing
    ):
        classification = "open_response_candidate"
        confidence = "high" if requires_causal_chain else "medium"
    elif (
        question_type == "single_best_answer"
        and cognitive_demand_count >= 1
    ):
        classification = "human_review_required"
        confidence = "medium" if answer_boundary_support else "low"
    else:
        classification = "sba_only"
        confidence = "high" if cognitive_demand_count == 0 else "medium"

    recognition_only_sufficient = classification == "sba_only"
    sba_eligible = classification == "sba_only" or bool(status.get("public_lab"))
    evidence = _evidence(
        question_type=question_type,
        review_state=review_state,
        requires_explanation=requires_explanation,
        requires_causal_chain=requires_causal_chain,
        requires_comparison=requires_comparison,
        requires_justification=requires_justification,
        recognition_framing=recognition_framing,
        answer_boundary_support=answer_boundary_support,
        causal_link_count=len(causal_links),
    )
    if resolution:
        evidence.insert(0, f"resolution:{resolution.get('resolution_id')}")
    return {
        "schema_version": CLASSIFIER_VERSION,
        "master_item_id": str(item.get("master_item_id", "")).strip(),
        "source_question_id": str(item.get("source_question_id", "")).strip(),
        "classification": classification,
        "open_response_candidate": classification == "open_response_candidate",
        "sba_only": classification == "sba_only",
        "sba_eligible": sba_eligible,
        "human_review_required": classification == "human_review_required",
        "signals": {
            "requires_explanation": requires_explanation,
            "requires_causal_chain": requires_causal_chain,
            "requires_comparison": requires_comparison,
            "requires_justification": requires_justification,
            "recognition_only_sufficient": recognition_only_sufficient,
            "recognition_framing_detected": recognition_framing,
            "answer_boundary_support": answer_boundary_support,
        },
        "confidence": confidence,
        "evidence": evidence,
        "review_status": "shadow_classified",
        "activation_status": "inactive",
        "governance": copy.deepcopy(SAFE_GOVERNANCE),
    }


def build_open_response_suitability_report(
    master_bank: Mapping[str, Any],
) -> dict[str, Any]:
    """Classify the complete bank and expose deterministic aggregate results."""
    records = [
        classify_open_response_suitability(item)
        for item in master_bank.get("items", [])
        if isinstance(item, Mapping)
    ]
    classification_counts = Counter(record["classification"] for record in records)
    signal_counts = Counter()
    for record in records:
        for signal, value in record["signals"].items():
            if value is True:
                signal_counts[signal] += 1
    by_ra = _distribution(records, master_bank, "ra")
    by_question_type = _question_type_distribution(records, master_bank)
    return {
        "schema_version": "open_response_suitability_report_v1",
        "classifier_version": CLASSIFIER_VERSION,
        "source_master_bank": MASTER_BANK_PATH.as_posix(),
        "record_count": len(records),
        "quota_target": None,
        "classification_counts": {
            name: classification_counts.get(name, 0) for name in CLASSIFICATIONS
        },
        "signal_counts": dict(sorted(signal_counts.items())),
        "candidate_distribution_by_ra": by_ra,
        "candidate_distribution_by_question_type": by_question_type,
        "records": records,
        "integration": {
            "runtime_active": False,
            "master_bank_rewritten": False,
            "public_lab_changed": False,
            "open_response_runtime_changed": False,
            "next_consumer": "difficulty_calibration_framework",
        },
        "governance": copy.deepcopy(SAFE_GOVERNANCE),
    }


def validate_open_response_suitability_report(payload: Any) -> list[str]:
    """Return structural and governance errors for the shadow artifact."""
    if not isinstance(payload, Mapping):
        return ["report must be an object"]
    errors: list[str] = []
    if payload.get("schema_version") != "open_response_suitability_report_v1":
        errors.append("invalid schema_version")
    records = payload.get("records")
    if not isinstance(records, list):
        return errors + ["records must be a list"]
    if payload.get("record_count") != len(records):
        errors.append("record_count mismatch")
    if payload.get("quota_target") is not None:
        errors.append("quota_target must remain null")
    ids: list[str] = []
    counts: Counter[str] = Counter()
    for record in records:
        if not isinstance(record, Mapping):
            errors.append("every record must be an object")
            continue
        item_id = str(record.get("master_item_id", ""))
        ids.append(item_id)
        classification = str(record.get("classification", ""))
        counts[classification] += 1
        if classification not in CLASSIFICATIONS:
            errors.append(f"{item_id}: invalid classification")
        if record.get("activation_status") != "inactive":
            errors.append(f"{item_id}: activation_status must be inactive")
        if record.get("governance") != SAFE_GOVERNANCE:
            errors.append(f"{item_id}: unsafe governance")
        if bool(record.get("open_response_candidate")) != (
            classification == "open_response_candidate"
        ):
            errors.append(f"{item_id}: candidate flag mismatch")
        if bool(record.get("sba_only")) != (classification == "sba_only"):
            errors.append(f"{item_id}: sba_only flag mismatch")
        if not isinstance(record.get("sba_eligible"), bool):
            errors.append(f"{item_id}: sba_eligible must be boolean")
    if len(ids) != len(set(ids)):
        errors.append("master_item_id values must be unique")
    expected_counts = payload.get("classification_counts")
    if not isinstance(expected_counts, Mapping):
        errors.append("classification_counts must be an object")
    elif any(expected_counts.get(name) != counts.get(name, 0) for name in CLASSIFICATIONS):
        errors.append("classification_counts mismatch")
    if payload.get("governance") != SAFE_GOVERNANCE:
        errors.append("unsafe report governance")
    return errors


def write_open_response_suitability_report(
    payload: Mapping[str, Any],
    path: str | Path = OUTPUT_PATH,
    root: str | Path = PROJECT_ROOT,
) -> Path:
    """Validate and write the deterministic shadow report."""
    errors = validate_open_response_suitability_report(payload)
    if errors:
        raise ValueError("invalid suitability report: " + "; ".join(errors))
    output = Path(root) / Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return output


def _evidence(**signals: Any) -> list[str]:
    evidence: list[str] = []
    for key, value in signals.items():
        if isinstance(value, bool) and value:
            evidence.append(key)
        elif isinstance(value, int) and value:
            evidence.append(f"{key}:{value}")
        elif isinstance(value, str) and value:
            evidence.append(f"{key}:{value}")
    return evidence


def _distribution(
    records: list[dict[str, Any]],
    master_bank: Mapping[str, Any],
    field: str,
) -> dict[str, int]:
    items = {
        str(item.get("master_item_id")): item
        for item in master_bank.get("items", [])
        if isinstance(item, Mapping)
    }
    counts = Counter()
    for record in records:
        if not record["open_response_candidate"]:
            continue
        curriculum = _mapping(items.get(record["master_item_id"], {}).get("curriculum"))
        counts[str(curriculum.get(field, "unknown"))] += 1
    return dict(sorted(counts.items()))


def _question_type_distribution(
    records: list[dict[str, Any]],
    master_bank: Mapping[str, Any],
) -> dict[str, int]:
    items = {
        str(item.get("master_item_id")): item
        for item in master_bank.get("items", [])
        if isinstance(item, Mapping)
    }
    counts = Counter(
        str(items[record["master_item_id"]].get("question_type", "unknown"))
        for record in records
        if record["open_response_candidate"] and record["master_item_id"] in items
    )
    return dict(sorted(counts.items()))


def _matches_any(text: str, patterns: tuple[str, ...]) -> bool:
    return any(re.search(pattern, text) for pattern in patterns)


def _normalize(value: Any) -> str:
    decomposed = unicodedata.normalize("NFD", str(value or "").lower())
    stripped = "".join(
        char for char in decomposed if unicodedata.category(char) != "Mn"
    )
    return " ".join(stripped.split())


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item).strip() for item in value if str(item).strip()]


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _is_inactive_master_item(item: Mapping[str, Any]) -> bool:
    status = _mapping(item.get("status"))
    review_state = str(status.get("review_state", "")).strip()
    if review_state in INACTIVE_REVIEW_STATES:
        return True
    if item.get("governance") != SAFE_GOVERNANCE:
        return True
    if not str(item.get("master_item_id", "")).strip():
        return True
    if not str(item.get("stem", "")).strip():
        return True
    question_type = item.get("question_type")
    if question_type == "open_response":
        return False
    if question_type != "single_best_answer":
        return True
    source_content = _mapping(item.get("source_content"))
    options = _mapping(source_content.get("options"))
    answer = str(source_content.get("correct_answer_letter", "")).strip().upper()
    return set(options) != {"A", "B", "C", "D"} or answer not in options


def _load_master_bank(root: Path) -> dict[str, Any]:
    data = json.loads((root / MASTER_BANK_PATH).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("master bank must be an object")
    return data


def _cli() -> int:
    parser = argparse.ArgumentParser(
        description="Build the shadow Open Response suitability report."
    )
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    if args.check == args.write:
        parser.error("choose exactly one of --check or --write")
    report = build_open_response_suitability_report(_load_master_bank(PROJECT_ROOT))
    errors = validate_open_response_suitability_report(report)
    if errors:
        raise SystemExit("\n".join(errors))
    print(json.dumps({
        "record_count": report["record_count"],
        "classification_counts": report["classification_counts"],
        "candidate_distribution_by_ra": report["candidate_distribution_by_ra"],
    }, indent=2))
    if args.write:
        print(write_open_response_suitability_report(report).as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(_cli())
