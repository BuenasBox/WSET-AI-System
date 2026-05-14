from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
INPUT_DIR = ROOT / "knowledge" / "enrichment" / "wset_master_dictionary"
OUTPUT_DIR = INPUT_DIR / "consolidated"

MASTER_CSV = INPUT_DIR / "master_terms.csv"
MASTER_JSONL = INPUT_DIR / "master_terms.jsonl"
EXTRACTION_FLAGS_CSV = INPUT_DIR / "extraction_quality_flags.csv"

CANONICAL_COLUMNS = [
    "canonical_term",
    "category",
    "official_sources",
    "source_documents",
    "source_count",
    "ra",
    "aliases",
    "confidence",
    "manually_reviewed",
    "safe_for_tutor",
    "safe_for_examiner",
    "official_grading_authority",
    "notes",
    "quality_flags",
]

QUALITY_FLAG_COLUMNS = [
    "canonical_term",
    "category",
    "quality_flags",
    "details",
    "source_count",
    "official_sources",
    "source_documents",
    "aliases",
    "confidence",
]

CONFIDENCE_RANK = {"low": 0, "medium": 1, "high": 2}


def normalize_whitespace(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def split_list(value: object) -> list[str]:
    text = normalize_whitespace(value)
    if not text:
        return []
    return [normalize_whitespace(item) for item in text.split(";") if normalize_whitespace(item)]


def unique_preserve_order(values: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    output: list[str] = []
    for value in values:
        normalized = normalize_whitespace(value)
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        output.append(normalized)
    return output


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return [
            {key: normalize_whitespace(value) for key, value in row.items()}
            for row in csv.DictReader(handle)
        ]


def read_jsonl_rows(path: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                parsed = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSONL at {path}:{line_number}: {exc}") from exc
            rows.append({key: normalize_whitespace(value) for key, value in parsed.items()})
    return rows


def confidence_from_sources(rows: list[dict[str, str]], extraction_flagged_low: bool) -> str:
    if extraction_flagged_low or any(row.get("confidence") == "low" for row in rows):
        return "low"
    sources = {row.get("official_source", "") for row in rows}
    if sources & {"specification", "sat"}:
        return "high"
    if sources == {"study-guide"}:
        return "medium"
    return "medium"


def extraction_flags_by_key(flag_rows: list[dict[str, str]]) -> dict[tuple[str, str], set[str]]:
    flags: dict[tuple[str, str], set[str]] = defaultdict(set)
    for row in flag_rows:
        key = (row.get("canonical_term", ""), row.get("category", ""))
        if row.get("low_confidence_extraction") == "true":
            flags[key].add("needs_human_review")
        if row.get("possible_ocr_issue") == "true":
            flags[key].add("possible_ocr_issue")
    return flags


def consolidate_rows(
    raw_rows: list[dict[str, str]],
    extraction_flag_rows: list[dict[str, str]],
) -> tuple[list[dict[str, object]], list[dict[str, object]], dict[str, object]]:
    groups: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    categories_by_term: dict[str, set[str]] = defaultdict(set)
    for row in raw_rows:
        canonical_term = normalize_whitespace(row.get("canonical_term"))
        category = normalize_whitespace(row.get("category"))
        row["canonical_term"] = canonical_term
        row["category"] = category
        groups[(canonical_term, category)].append(row)
        categories_by_term[canonical_term].add(category)

    extraction_flags = extraction_flags_by_key(extraction_flag_rows)
    alias_owner: dict[str, set[tuple[str, str]]] = defaultdict(set)
    alias_occurrences_by_group: dict[tuple[str, str], Counter[str]] = defaultdict(Counter)
    for key, rows in groups.items():
        for row in rows:
            for alias in split_list(row.get("aliases")):
                alias_owner[alias].add(key)
                alias_occurrences_by_group[key][alias] += 1

    ambiguous_terms = {
        term for term, categories in categories_by_term.items() if term and len(categories) > 1
    }
    colliding_aliases = {
        alias: owners for alias, owners in alias_owner.items() if alias and len(owners) > 1
    }

    consolidated: list[dict[str, object]] = []
    quality_rows: list[dict[str, object]] = []

    for key in sorted(groups, key=lambda item: (item[1], item[0].casefold())):
        term, category = key
        rows = groups[key]
        official_sources = unique_preserve_order(row.get("official_source", "") for row in rows)
        source_documents = unique_preserve_order(row.get("source_document", "") for row in rows)
        ra = unique_preserve_order(row.get("ra", "") for row in rows)
        aliases = unique_preserve_order(alias for row in rows for alias in split_list(row.get("aliases")))
        notes = unique_preserve_order(row.get("notes", "") for row in rows)

        quality_flags = set(extraction_flags.get(key, set()))
        if term in ambiguous_terms:
            quality_flags.add("ambiguous_category")
        if any(not row.get("source_document") for row in rows):
            quality_flags.add("missing_source_document")
        if any(count > 1 for count in alias_occurrences_by_group[key].values()):
            quality_flags.add("duplicate_alias")
        if any(alias in colliding_aliases for alias in aliases):
            quality_flags.add("alias_collision")

        row_confidences = {row.get("confidence", "") for row in rows if row.get("confidence")}
        extraction_flagged_low = "needs_human_review" in quality_flags
        confidence = confidence_from_sources(rows, extraction_flagged_low)
        if len(row_confidences) > 1 or any(
            CONFIDENCE_RANK.get(item, -1) > CONFIDENCE_RANK[confidence]
            for item in row_confidences
        ):
            quality_flags.add("conflicting_confidence")

        if quality_flags - {"ambiguous_category"}:
            quality_flags.add("needs_human_review")

        record = {
            "canonical_term": term,
            "category": category,
            "official_sources": official_sources,
            "source_documents": source_documents,
            "source_count": len(source_documents),
            "ra": ra,
            "aliases": aliases,
            "confidence": confidence,
            "manually_reviewed": False,
            "safe_for_tutor": True,
            "safe_for_examiner": False,
            "official_grading_authority": False,
            "notes": " | ".join(notes),
            "quality_flags": sorted(quality_flags),
        }
        consolidated.append(record)

        if quality_flags:
            quality_rows.append(
                {
                    "canonical_term": term,
                    "category": category,
                    "quality_flags": "; ".join(sorted(quality_flags)),
                    "details": build_quality_details(
                        key,
                        sorted(quality_flags),
                        categories_by_term,
                        colliding_aliases,
                        aliases,
                    ),
                    "source_count": record["source_count"],
                    "official_sources": "; ".join(official_sources),
                    "source_documents": "; ".join(source_documents),
                    "aliases": "; ".join(aliases),
                    "confidence": confidence,
                }
            )

    metrics = {
        "raw_term_count": len(raw_rows),
        "consolidated_count": len(consolidated),
        "duplicates_merged": len(raw_rows) - len(consolidated),
        "counts_by_category": dict(Counter(row["category"] for row in consolidated)),
        "ambiguous_terms": sorted(ambiguous_terms, key=str.casefold),
        "alias_collision_terms": sorted(
            {
                term
                for owners in colliding_aliases.values()
                for term, _category in owners
            },
            key=str.casefold,
        ),
    }
    return consolidated, quality_rows, metrics


def build_quality_details(
    key: tuple[str, str],
    quality_flags: list[str],
    categories_by_term: dict[str, set[str]],
    colliding_aliases: dict[str, set[tuple[str, str]]],
    aliases: list[str],
) -> str:
    term, _category = key
    details: list[str] = []
    if "ambiguous_category" in quality_flags:
        details.append(f"categories: {', '.join(sorted(categories_by_term[term]))}")
    if "alias_collision" in quality_flags:
        collided = [
            f"{alias} -> "
            + ", ".join(f"{owner_term}/{owner_category}" for owner_term, owner_category in sorted(colliding_aliases[alias]))
            for alias in aliases
            if alias in colliding_aliases
        ]
        details.append("; ".join(collided))
    for flag in quality_flags:
        if flag not in {"ambiguous_category", "alias_collision"}:
            details.append(flag)
    return " | ".join(details)


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    key: json.dumps(row[key], ensure_ascii=False)
                    if isinstance(row.get(key), list)
                    else str(row.get(key, "")).lower()
                    if isinstance(row.get(key), bool)
                    else row.get(key, "")
                    for key in fieldnames
                }
            )


def write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def validate_outputs(csv_path: Path, jsonl_path: Path, rows: list[dict[str, object]]) -> None:
    jsonl_rows = []
    with jsonl_path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                jsonl_rows.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid output JSONL at line {line_number}: {exc}") from exc

    with csv_path.open("r", newline="", encoding="utf-8-sig") as handle:
        csv_count = sum(1 for _row in csv.DictReader(handle))

    if csv_count != len(jsonl_rows):
        raise ValueError(f"CSV row count {csv_count} does not match JSONL row count {len(jsonl_rows)}")
    if len(jsonl_rows) != len(rows):
        raise ValueError("Written row count does not match in-memory consolidated rows")
    for index, row in enumerate(jsonl_rows, start=1):
        if not row.get("canonical_term") or not row.get("category") or not row.get("source_documents"):
            raise ValueError(f"Missing required canonical fields in row {index}")
        if row.get("safe_for_examiner") is not False:
            raise ValueError(f"safe_for_examiner must be false in row {index}")


def write_report(
    path: Path,
    rows: list[dict[str, object]],
    quality_rows: list[dict[str, object]],
    metrics: dict[str, object],
    input_hashes_unchanged: bool,
) -> None:
    counts_by_category = metrics["counts_by_category"]
    ambiguous_terms = metrics["ambiguous_terms"]
    alias_collision_terms = metrics["alias_collision_terms"]
    top_terms = sorted(
        rows,
        key=lambda row: (-int(row["source_count"]), str(row["canonical_term"]).casefold(), str(row["category"])),
    )[:30]

    review_priorities = [
        row
        for row in quality_rows
        if "needs_human_review" in str(row["quality_flags"])
        or "ambiguous_category" in str(row["quality_flags"])
    ][:30]

    lines = [
        "# WSET Level 3 Canonical Dictionary Consolidation Report",
        "",
        "Phase 2 consolidation only. No official PDFs, transcript files, question-bank files, raw extraction rows, embeddings, vector DBs, or agents were modified or created.",
        "",
        "## Summary",
        "",
        f"- Raw term count: {metrics['raw_term_count']}",
        f"- Consolidated canonical term count: {metrics['consolidated_count']}",
        f"- Duplicates merged: {metrics['duplicates_merged']}",
        f"- Raw extraction files untouched: {str(input_hashes_unchanged).lower()}",
        "",
        "## Counts By Category",
        "",
    ]
    for category, count in sorted(counts_by_category.items()):
        lines.append(f"- `{category}`: {count}")

    lines.extend(["", "## Ambiguous Category Terms", ""])
    if ambiguous_terms:
        for term in ambiguous_terms:
            categories = sorted(
                row["category"] for row in rows if row["canonical_term"] == term
            )
            lines.append(f"- {term}: {', '.join(categories)}")
    else:
        lines.append("- None")

    lines.extend(["", "## Alias Collision Terms", ""])
    if alias_collision_terms:
        for term in alias_collision_terms:
            lines.append(f"- {term}")
    else:
        lines.append("- None")

    lines.extend(["", "## Top 30 Canonical Terms By Source Count", ""])
    for row in top_terms:
        lines.append(
            f"- {row['canonical_term']} | {row['category']} | sources: {row['source_count']} | "
            f"{', '.join(row['official_sources'])}"
        )

    lines.extend(["", "## Recommended Human Review Priorities", ""])
    if review_priorities:
        for row in review_priorities:
            lines.append(f"- {row['canonical_term']} | {row['category']} | {row['quality_flags']}")
    else:
        lines.append("- None")

    lines.extend(
        [
            "",
            "## Validation",
            "",
            "- JSONL is valid.",
            "- CSV row count matches JSONL row count.",
            "- Every record has `canonical_term`, `category`, and `source_documents`.",
            "- `safe_for_examiner` is `false` on every consolidated record.",
            "- Raw rows categorized as `sat_term` remain category `sat_term` after consolidation.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run_consolidation(
    input_dir: Path = INPUT_DIR,
    output_dir: Path = OUTPUT_DIR,
) -> tuple[list[dict[str, object]], list[dict[str, object]], dict[str, object]]:
    master_csv = input_dir / "master_terms.csv"
    master_jsonl = input_dir / "master_terms.jsonl"
    flags_csv = input_dir / "extraction_quality_flags.csv"

    input_hashes_before = {path: file_sha256(path) for path in [master_csv, master_jsonl, flags_csv]}

    csv_rows = read_csv_rows(master_csv)
    jsonl_rows = read_jsonl_rows(master_jsonl)
    if len(csv_rows) != len(jsonl_rows):
        raise ValueError("Raw CSV and JSONL row counts do not match")
    raw_rows = csv_rows
    extraction_flag_rows = read_csv_rows(flags_csv)

    consolidated, quality_rows, metrics = consolidate_rows(raw_rows, extraction_flag_rows)

    output_dir.mkdir(parents=True, exist_ok=True)
    canonical_csv = output_dir / "canonical_terms_master.csv"
    canonical_jsonl = output_dir / "canonical_terms_master.jsonl"
    quality_csv = output_dir / "consolidation_quality_flags.csv"
    report_md = output_dir / "consolidation_report.md"

    write_csv(canonical_csv, consolidated, CANONICAL_COLUMNS)
    write_jsonl(canonical_jsonl, consolidated)
    write_csv(quality_csv, quality_rows, QUALITY_FLAG_COLUMNS)
    validate_outputs(canonical_csv, canonical_jsonl, consolidated)

    input_hashes_after = {path: file_sha256(path) for path in [master_csv, master_jsonl, flags_csv]}
    input_hashes_unchanged = input_hashes_before == input_hashes_after
    write_report(report_md, consolidated, quality_rows, metrics, input_hashes_unchanged)

    if not input_hashes_unchanged:
        raise ValueError("Raw extraction input files changed during consolidation")

    return consolidated, quality_rows, metrics


def main() -> None:
    consolidated, quality_rows, metrics = run_consolidation()
    print(f"Raw terms: {metrics['raw_term_count']}")
    print(f"Consolidated terms: {metrics['consolidated_count']}")
    print(f"Duplicates merged: {metrics['duplicates_merged']}")
    print(f"Quality flags: {len(quality_rows)}")
    print(f"Output directory: {OUTPUT_DIR}")
    print("\nFirst 20 consolidated terms:")
    for row in consolidated[:20]:
        print(f"{row['canonical_term']} | {row['category']} | {row['confidence']}")


if __name__ == "__main__":
    main()
