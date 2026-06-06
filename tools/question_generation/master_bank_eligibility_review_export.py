"""Export read-only human-review packets for Master Bank eligibility."""

from __future__ import annotations

import argparse
import copy
import json
import re
import unicodedata
from collections import Counter
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from tools.constants import PROJECT_ROOT
from tools.question_generation.master_bank import MASTER_BANK_PATH, SAFE_GOVERNANCE
from tools.question_generation.master_bank_eligibility import (
    OPEN_RESPONSE_SUITABILITY_PATH,
    build_eligibility_index,
    load_open_response_suitability_index,
)


DOCS_OUTPUT_DIR = Path("docs/review_packets/master_bank_eligibility")
JSON_OUTPUT_PATH = Path(
    "knowledge/question-bank/review_packets/"
    "master_bank_eligibility_review_packet.json"
)
RECOMMENDATION_OPTIONS = (
    "keep_inactive",
    "restore_to_sba",
    "move_to_open_response",
    "needs_human_revision",
    "quarantine",
)
REVIEW_REASON_ORDER = (
    "missing_metadata",
    "possible_open_response",
    "weak_support",
    "duplicate_risk",
    "difficulty_uncertainty",
    "governance_concern",
    "other",
)
INACTIVE_GROUP_ORDER = ("truly_inactive", "recoverable", "unclear")
PUBLIC_REVIEW_IDS = ("356", "421", "464")


def build_review_packet(
    master_bank: Mapping[str, Any],
    suitability_index: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    """Build the complete structured packet without mutating source artifacts."""
    eligibility = build_eligibility_index(master_bank, suitability_index)
    items = [
        item
        for item in master_bank.get("items", [])
        if isinstance(item, Mapping)
    ]
    duplicate_ids = _duplicate_risk_ids(items)
    inactive: list[dict[str, Any]] = []
    review_pool: list[dict[str, Any]] = []

    for item in items:
        item_id = str(item.get("master_item_id", ""))
        suitability = suitability_index[item_id]
        record = _review_record(
            item,
            eligibility["records"][item_id],
            suitability,
            duplicate_risk=item_id in duplicate_ids,
        )
        classification = suitability.get("classification")
        if classification == "inactive":
            record["inactive_review_group"] = _inactive_group(item, record)
            inactive.append(record)
        elif classification == "human_review_required":
            record["review_reason_group"] = _review_reason_group(record)
            review_pool.append(record)

    public_exceptions = [
        record
        for record in review_pool
        if record["question_id"] in PUBLIC_REVIEW_IDS
    ]
    inactive_counts = Counter(
        record["inactive_review_group"] for record in inactive
    )
    review_counts = Counter(record["review_reason_group"] for record in review_pool)
    urgent = [
        {
            "question_id": record["question_id"],
            "reason": "structurally_invalid_inactive_record",
            "recommended_first_action": "quarantine",
        }
        for record in inactive
        if not record["eligibility_flags"]["structurally_usable"]
    ]

    return {
        "schema_version": "master_bank_eligibility_review_packet_v1",
        "source_commit": "f409433",
        "source_master_bank": MASTER_BANK_PATH.as_posix(),
        "source_suitability": OPEN_RESPONSE_SUITABILITY_PATH.as_posix(),
        "classification_changes_applied": False,
        "eligibility_changes_applied": False,
        "open_response_runtime_active": False,
        "counts": {
            "total_master_bank": len(items),
            "inactive": len(inactive),
            "review_pool": len(review_pool),
            "public_lab_review_exceptions": len(public_exceptions),
            "inactive_groups": {
                group: inactive_counts.get(group, 0)
                for group in INACTIVE_GROUP_ORDER
            },
            "review_reason_groups": {
                group: review_counts.get(group, 0)
                for group in REVIEW_REASON_ORDER
            },
        },
        "urgent_cases": urgent,
        "inactive_items": inactive,
        "review_pool_items": review_pool,
        "public_lab_review_exceptions": public_exceptions,
        "recommendation_options": list(RECOMMENDATION_OPTIONS),
        "governance": copy.deepcopy(SAFE_GOVERNANCE),
    }


def validate_review_packet(payload: Any) -> list[str]:
    """Return packet integrity and governance errors."""
    if not isinstance(payload, Mapping):
        return ["packet must be an object"]
    errors: list[str] = []
    inactive = payload.get("inactive_items")
    review = payload.get("review_pool_items")
    public = payload.get("public_lab_review_exceptions")
    if not isinstance(inactive, list) or len(inactive) != 24:
        errors.append("inactive_items must contain 24 records")
    if not isinstance(review, list) or len(review) != 68:
        errors.append("review_pool_items must contain 68 records")
    if not isinstance(public, list) or {
        str(record.get("question_id")) for record in public
    } != set(PUBLIC_REVIEW_IDS):
        errors.append("public review exceptions must be 356, 421, and 464")
    all_records = (
        (inactive if isinstance(inactive, list) else [])
        + (review if isinstance(review, list) else [])
    )
    required = {
        "question_id",
        "stem",
        "question_type",
        "current_pool",
        "eligibility_flags",
        "ra",
        "topic",
        "subtopic",
        "difficulty",
        "open_response_suitability",
        "review_reason",
        "source_support",
        "options",
        "correct_answer",
        "recommendation",
        "recommendation_options",
    }
    for record in all_records:
        if not isinstance(record, Mapping):
            errors.append("every review record must be an object")
            continue
        missing = required - set(record)
        if missing:
            errors.append(f"{record.get('question_id')}: missing {sorted(missing)}")
        if record.get("recommendation") is not None:
            errors.append(f"{record.get('question_id')}: recommendation must be null")
        if tuple(record.get("recommendation_options", [])) != RECOMMENDATION_OPTIONS:
            errors.append(f"{record.get('question_id')}: invalid recommendation options")
        flags = record.get("eligibility_flags")
        if not isinstance(flags, Mapping):
            errors.append(f"{record.get('question_id')}: eligibility flags missing")
    if payload.get("governance") != SAFE_GOVERNANCE:
        errors.append("unsafe packet governance")
    if payload.get("classification_changes_applied") is not False:
        errors.append("classification changes must remain false")
    if payload.get("eligibility_changes_applied") is not False:
        errors.append("eligibility changes must remain false")
    return errors


def write_review_packet(
    payload: Mapping[str, Any],
    *,
    root: str | Path = PROJECT_ROOT,
) -> list[Path]:
    """Write the JSON and four Markdown projections."""
    errors = validate_review_packet(payload)
    if errors:
        raise ValueError("invalid review packet: " + "; ".join(errors))
    root_path = Path(root)
    json_path = root_path / JSON_OUTPUT_PATH
    docs_dir = root_path / DOCS_OUTPUT_DIR
    json_path.parent.mkdir(parents=True, exist_ok=True)
    docs_dir.mkdir(parents=True, exist_ok=True)
    json_path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    outputs = [
        json_path,
        _write_text(
            docs_dir / "inactive_items_review_packet.md",
            _render_grouped_packet(
                "Inactive Items Review Packet",
                payload["inactive_items"],
                "inactive_review_group",
                INACTIVE_GROUP_ORDER,
            ),
        ),
        _write_text(
            docs_dir / "review_pool_items_review_packet.md",
            _render_grouped_packet(
                "Review Pool Items Review Packet",
                payload["review_pool_items"],
                "review_reason_group",
                REVIEW_REASON_ORDER,
            ),
        ),
        _write_text(
            docs_dir / "public_lab_review_exceptions.md",
            _render_public_exceptions(payload["public_lab_review_exceptions"]),
        ),
        _write_text(
            docs_dir / "master_bank_eligibility_review_summary.md",
            _render_summary(payload),
        ),
    ]
    return outputs


def _review_record(
    item: Mapping[str, Any],
    eligibility: Mapping[str, Any],
    suitability: Mapping[str, Any],
    *,
    duplicate_risk: bool,
) -> dict[str, Any]:
    curriculum = _mapping(item.get("curriculum"))
    source_content = _mapping(item.get("source_content"))
    status = _mapping(item.get("status"))
    lineage = _mapping(item.get("lineage"))
    options = _mapping(source_content.get("options"))
    subtopic = _subtopic(curriculum)
    secondary_reasons: list[str] = []
    if duplicate_risk:
        secondary_reasons.append("duplicate_risk")
    if curriculum.get("difficulty") == "intermediate" and suitability.get("confidence") == "low":
        secondary_reasons.append("difficulty_uncertainty")
    if not _governance_safe(item):
        secondary_reasons.append("governance_concern")

    return {
        "master_item_id": item.get("master_item_id"),
        "question_id": str(item.get("source_question_id", "")),
        "stem": item.get("stem"),
        "question_type": item.get("question_type"),
        "current_pool": eligibility.get("primary_category"),
        "eligibility_flags": {
            "categories": list(eligibility.get("categories", [])),
            "sba_eligible": bool(eligibility.get("sba_eligible")),
            "structurally_usable": bool(eligibility.get("structurally_usable")),
            "public_lab": bool(status.get("public_lab")),
            "gold": bool(status.get("gold")),
            "activation_status": status.get("activation_status"),
            "review_state": status.get("review_state"),
        },
        "ra": curriculum.get("ra"),
        "topic": curriculum.get("topic"),
        "subtopic": subtopic,
        "difficulty": curriculum.get("difficulty"),
        "open_response_suitability": {
            "classification": suitability.get("classification"),
            "confidence": suitability.get("confidence"),
            "signals": copy.deepcopy(_mapping(suitability.get("signals"))),
            "evidence": list(suitability.get("evidence", [])),
            "sba_eligible": bool(suitability.get("sba_eligible")),
            "activation_status": suitability.get("activation_status"),
        },
        "review_reason": _reason_text(item, eligibility, suitability),
        "secondary_review_reasons": secondary_reasons,
        "source_support": {
            "status": _source_support_status(lineage, status),
            "structured_source": lineage.get("structured_source"),
            "raw_source": lineage.get("raw_source"),
            "sba_draft_id": lineage.get("sba_draft_id"),
            "sba_review_id": lineage.get("sba_review_id"),
            "open_response_candidate_id": lineage.get("open_response_candidate_id"),
            "open_response_review_id": lineage.get("open_response_review_id"),
            "gold_review_id": lineage.get("gold_review_id"),
            "public_lab_item_id": lineage.get("public_lab_item_id"),
        },
        "options": dict(options) if item.get("question_type") == "single_best_answer" else None,
        "correct_answer": {
            "letter": source_content.get("correct_answer_letter"),
            "text": source_content.get("correct_answer_text"),
        } if item.get("question_type") == "single_best_answer" else None,
        "recommendation": None,
        "recommendation_options": list(RECOMMENDATION_OPTIONS),
        "review_notes": None,
    }


def _inactive_group(
    item: Mapping[str, Any],
    record: Mapping[str, Any],
) -> str:
    review_state = _mapping(item.get("status")).get("review_state")
    if review_state == "rejected" or not record["eligibility_flags"]["structurally_usable"]:
        return "truly_inactive"
    if review_state == "requires_revision":
        return "recoverable"
    return "unclear"


def _review_reason_group(record: Mapping[str, Any]) -> str:
    flags = _mapping(record.get("eligibility_flags"))
    signals = _mapping(_mapping(record.get("open_response_suitability")).get("signals"))
    secondary = set(record.get("secondary_review_reasons", []))
    if "governance_concern" in secondary:
        return "governance_concern"
    if "duplicate_risk" in secondary:
        return "duplicate_risk"
    if not flags.get("structurally_usable") or record.get("ra") in {None, "", "unknown"}:
        return "missing_metadata"
    if signals.get("requires_comparison") or signals.get("requires_justification"):
        return "possible_open_response"
    if signals.get("requires_explanation"):
        return "weak_support"
    if "difficulty_uncertainty" in secondary:
        return "difficulty_uncertainty"
    return "other"


def _reason_text(
    item: Mapping[str, Any],
    eligibility: Mapping[str, Any],
    suitability: Mapping[str, Any],
) -> str:
    status = _mapping(item.get("status"))
    classification = suitability.get("classification")
    if classification == "inactive":
        if not eligibility.get("structurally_usable"):
            return "Structural SBA requirements are not met."
        return f"Master Bank review_state is {status.get('review_state')}."
    evidence = ", ".join(str(value) for value in suitability.get("evidence", []))
    return (
        "Open Response suitability requires human review at "
        f"{suitability.get('confidence')} confidence; evidence: {evidence or 'none'}."
    )


def _source_support_status(
    lineage: Mapping[str, Any],
    status: Mapping[str, Any],
) -> str:
    if status.get("public_lab") and lineage.get("gold_review_id"):
        return "gold_reviewed_public"
    if lineage.get("sba_review_id"):
        return "human_review_record_available"
    if lineage.get("sba_draft_id"):
        return "enrichment_draft_available"
    if lineage.get("open_response_review_id"):
        return "open_response_review_available"
    if lineage.get("raw_source"):
        return "source_reference_only"
    return "not_recorded"


def _subtopic(curriculum: Mapping[str, Any]) -> str | None:
    topic = str(curriculum.get("topic", "")).strip()
    ra = str(curriculum.get("ra", "")).strip()
    for value in curriculum.get("expected_topics", []):
        text = str(value).strip()
        if text and text not in {topic, ra}:
            return text
    return None


def _duplicate_risk_ids(items: Sequence[Mapping[str, Any]]) -> set[str]:
    by_stem: dict[str, list[str]] = {}
    for item in items:
        normalized = _normalize_text(item.get("stem"))
        if normalized:
            by_stem.setdefault(normalized, []).append(str(item.get("master_item_id")))
    return {
        item_id
        for item_ids in by_stem.values()
        if len(item_ids) > 1
        for item_id in item_ids
    }


def _normalize_text(value: Any) -> str:
    decomposed = unicodedata.normalize("NFD", str(value or "").lower())
    ascii_like = "".join(
        char for char in decomposed if unicodedata.category(char) != "Mn"
    )
    return re.sub(r"\W+", " ", ascii_like).strip()


def _governance_safe(item: Mapping[str, Any]) -> bool:
    return item.get("governance") == SAFE_GOVERNANCE


def _render_grouped_packet(
    title: str,
    records: Sequence[Mapping[str, Any]],
    group_field: str,
    group_order: Sequence[str],
) -> str:
    lines = [
        f"# {title}",
        "",
        "Read-only review projection. No classification or eligibility change is applied.",
        "",
        f"Total items: **{len(records)}**",
        "",
    ]
    for group in group_order:
        grouped = [record for record in records if record.get(group_field) == group]
        lines.extend((f"## {group.replace('_', ' ').title()} ({len(grouped)})", ""))
        if not grouped:
            lines.extend(("_No items in this group._", ""))
            continue
        for record in grouped:
            lines.extend(_render_record(record))
    return "\n".join(lines).rstrip() + "\n"


def _render_public_exceptions(records: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "# Public Lab Review Exceptions",
        "",
        "These three records remain `sba_eligible=true` because public-lab membership",
        "is an explicit reviewed SBA override. Their suitability signal is retained",
        "for editorial review and does not activate Open Response.",
        "",
    ]
    for record in records:
        lines.extend(_render_record(record))
        lines.extend(
            (
                "**Exception rationale:** The item is approved for the 36-item public",
                "lab and has a gold review record. Suitability detected explanatory",
                "wording but only low-confidence evidence, so the review flag coexists",
                "with explicit SBA eligibility.",
                "",
            )
        )
    return "\n".join(lines).rstrip() + "\n"


def _render_summary(payload: Mapping[str, Any]) -> str:
    counts = _mapping(payload.get("counts"))
    inactive = _mapping(counts.get("inactive_groups"))
    review = _mapping(counts.get("review_reason_groups"))
    urgent = payload.get("urgent_cases", [])
    lines = [
        "# Master Bank Eligibility Review Summary",
        "",
        "## Scope",
        "",
        "- Source commit: `f409433`",
        f"- Master Bank: {counts.get('total_master_bank')}",
        f"- Inactive review packet: {counts.get('inactive')}",
        f"- Review pool packet: {counts.get('review_pool')}",
        f"- Public review exceptions: {counts.get('public_lab_review_exceptions')}",
        "- Classification changes: none",
        "- Eligibility changes: none",
        "- Open Response activation: none",
        "",
        "## Inactive Groups",
        "",
        *[f"- `{group}`: {inactive.get(group, 0)}" for group in INACTIVE_GROUP_ORDER],
        "",
        "## Review Reason Groups",
        "",
        *[f"- `{group}`: {review.get(group, 0)}" for group in REVIEW_REASON_ORDER],
        "",
        "## Urgent Cases",
        "",
    ]
    if urgent:
        lines.extend(
            f"- Q{case['question_id']}: {case['reason']} "
            f"(first action: `{case['recommended_first_action']}`)"
            for case in urgent
        )
    else:
        lines.append("- None detected.")
    lines.extend(
        (
            "",
            "## Human Decision Values",
            "",
            *[f"- `{value}`" for value in RECOMMENDATION_OPTIONS],
        )
    )
    return "\n".join(lines).rstrip() + "\n"


def _render_record(record: Mapping[str, Any]) -> list[str]:
    flags = _mapping(record.get("eligibility_flags"))
    suitability = _mapping(record.get("open_response_suitability"))
    source = _mapping(record.get("source_support"))
    lines = [
        f"### Q{record.get('question_id')} - {record.get('stem')}",
        "",
        f"- Master ID: `{record.get('master_item_id')}`",
        f"- Question type: `{record.get('question_type')}`",
        f"- Current pool: `{record.get('current_pool')}`",
        f"- Eligibility: `sba_eligible={str(flags.get('sba_eligible')).lower()}`, "
        f"`structurally_usable={str(flags.get('structurally_usable')).lower()}`, "
        f"`public_lab={str(flags.get('public_lab')).lower()}`",
        f"- Categories: {', '.join(f'`{value}`' for value in flags.get('categories', []))}",
        f"- RA: `{record.get('ra')}`",
        f"- Topic / subtopic: `{record.get('topic')}` / `{record.get('subtopic')}`",
        f"- Current difficulty: `{record.get('difficulty')}`",
        f"- OR suitability: `{suitability.get('classification')}` "
        f"({suitability.get('confidence')} confidence)",
        f"- Review reason: {record.get('review_reason')}",
        f"- Source/support: `{source.get('status')}`; "
        f"raw source: `{source.get('raw_source')}`",
    ]
    options = record.get("options")
    if isinstance(options, Mapping):
        lines.extend(("", "**Options**", ""))
        lines.extend(
            f"- {key}. {value if str(value).strip() else '(empty)'}"
            for key, value in options.items()
        )
        answer = _mapping(record.get("correct_answer"))
        lines.extend(
            (
                "",
                f"**Correct answer:** {answer.get('letter')}. {answer.get('text')}",
            )
        )
    lines.extend(("", "**Human recommendation**", ""))
    lines.extend(f"- [ ] `{value}`" for value in RECOMMENDATION_OPTIONS)
    lines.extend(("- Notes:", "", "---", ""))
    return lines


def _write_text(path: Path, content: str) -> Path:
    path.write_text(content, encoding="utf-8")
    return path


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain an object")
    return payload


def _cli() -> int:
    parser = argparse.ArgumentParser(
        description="Export Master Bank eligibility human-review packets."
    )
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    if args.check == args.write:
        parser.error("choose exactly one of --check or --write")
    bank = _load_json(PROJECT_ROOT / MASTER_BANK_PATH)
    suitability = load_open_response_suitability_index()
    packet = build_review_packet(bank, suitability)
    errors = validate_review_packet(packet)
    if errors:
        raise SystemExit("\n".join(errors))
    print(json.dumps(packet["counts"], indent=2))
    print(json.dumps({"urgent_cases": packet["urgent_cases"]}, indent=2))
    if args.write:
        for output in write_review_packet(packet):
            print(output.relative_to(PROJECT_ROOT).as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(_cli())
