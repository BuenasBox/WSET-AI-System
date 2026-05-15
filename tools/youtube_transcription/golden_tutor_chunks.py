"""Derived Golden Tutor Chunk QA reports for manual Wine With Jimmy SRT chunks.

This module only reads existing chunk-ready JSONL files and writes derived
reports. It does not create embeddings, vector stores, agent wiring, or
Examiner-safe artifacts.
"""

from __future__ import annotations

import csv
import json
import re
from collections import Counter
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


SOURCE_TYPE = "manual_curated_srt"
AGENT_CORPUS = "tutor"
REPORT_VERSION = "golden_tutor_chunk_qa_v1.0"
CSV_COLUMNS = (
    "chunk_id",
    "source_filename",
    "video_title_guess",
    "academic_level",
    "pedagogical_role",
    "text_excerpt",
    "golden_tutor_chunk_candidate",
    "pedagogical_value_score",
    "retrieval_priority",
    "reasoning_type",
    "matched_signals",
    "quality_flags",
    "human_review_required",
)
SIGNAL_PATTERNS: tuple[tuple[str, str, float], ...] = (
    ("examiner is looking for", r"\bexaminer(?:s)?\s+(?:is|are|will be)?\s*looking\s+for\b", 0.22),
    ("students lose marks", r"\bstudents?\s+lose\s+marks\b|\blose\s+marks\b", 0.28),
    ("in the exam", r"\bin\s+the\s+exam(?:ination)?\b", 0.16),
    ("WSET wants", r"\bwset\s+wants\b", 0.2),
    ("you need to explain why", r"\byou\s+need\s+to\s+explain\s+why\b|\bexplain\s+why\b", 0.18),
    ("cause and effect", r"\bcause\s+and\s+effect\b", 0.2),
    (
        "balance intensity complexity length",
        r"\bbalance\b.*\bintensity\b.*\bcomplexity\b.*\blength\b",
        0.2,
    ),
    ("quality assessment", r"\bquality\s+assessment\b|\bassess(?:ing)?\s+the\s+quality\b", 0.22),
    ("readiness", r"\breadiness\b|\bready\s+for\s+drinking\b", 0.12),
    ("tasting exam", r"\btasting\s+exam(?:ination)?\b", 0.2),
    ("written question", r"\bwritten\s+question\b|\btheory\s+question\b", 0.18),
    ("marks", r"\bmarks?\b", 0.12),
    ("link", r"\blink(?:ed|ing|s)?\b", 0.1),
    ("justify", r"\bjustify\b|\bjustification\b", 0.16),
    ("because", r"\bbecause\b", 0.08),
    ("therefore", r"\btherefore\b", 0.08),
)
REASONING_PATTERNS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("common_mistake", (r"\b(?:common|classic)\s+mistake\b", r"\bstudents?\s+lose\s+marks\b")),
    ("exam_strategy", (r"\bexam(?:ination)?\b", r"\bmarks?\b", r"\bpass\b")),
    ("tasting_calibration", (r"\bquality\s+assessment\b", r"\bbalance\b", r"\bintensity\b", r"\breadiness\b")),
    ("sat_logic", (r"\bsat\b", r"\bsystematic\s+approach\s+to\s+tasting\b", r"\blink(?:ed|ing|s)?\b")),
    ("answer_structure", (r"\bwritten\s+question\b", r"\bstructure\b", r"\bjustify\b")),
    ("cause_effect", (r"\bcause\s+and\s+effect\b", r"\bbecause\b", r"\btherefore\b", r"\bleads?\s+to\b")),
    ("distinction_tip", (r"\bwhereas\b", r"\bcompared\s+with\b", r"\bdifference\s+between\b")),
    ("memory_hook", (r"\bremember\b", r"\bmemor(?:y|ise|ize)\b", r"\bup\s+here\b")),
    ("theory_foundation", (r"\bclimate\b", r"\bviticulture\b", r"\bwinemaking\b", r"\bfermentation\b")),
)


@dataclass(frozen=True)
class GoldenTutorReport:
    scanned_chunks: int
    candidate_rows: list[dict[str, Any]]
    output_csv: Path
    output_jsonl: Path
    summary_path: Path


def generate_golden_tutor_chunk_reports(root: Path) -> GoldenTutorReport:
    chunk_dir = root / "chunk-ready"
    report_dir = root / "manual-import" / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)

    scanned_chunks = 0
    rows: list[dict[str, Any]] = []
    safe_for_examiner_values: set[Any] = set()
    for path in sorted(chunk_dir.glob("*.chunks.jsonl"), key=lambda item: item.name.lower()):
        for chunk in _read_jsonl(path):
            if not _is_manual_tutor_chunk(chunk):
                continue
            scanned_chunks += 1
            safe_for_examiner_values.add(chunk.get("safe_for_examiner"))
            row = score_chunk(chunk)
            if _is_reportable(row):
                rows.append(row)

    rows.sort(key=lambda row: (-float(row["pedagogical_value_score"]), row["source_filename"], row["chunk_id"]))
    output_csv = report_dir / "golden_tutor_chunk_candidates.csv"
    output_jsonl = report_dir / "golden_tutor_chunk_candidates.jsonl"
    summary_path = report_dir / "golden_chunk_summary.md"
    _write_csv(output_csv, rows)
    _write_jsonl(output_jsonl, rows)
    _write_summary(
        summary_path=summary_path,
        rows=rows,
        scanned_chunks=scanned_chunks,
        safe_for_examiner_values=safe_for_examiner_values,
        output_csv=output_csv,
        output_jsonl=output_jsonl,
    )
    return GoldenTutorReport(scanned_chunks, rows, output_csv, output_jsonl, summary_path)


def score_chunk(chunk: dict[str, Any]) -> dict[str, Any]:
    text = str(chunk.get("text", "") or "")
    matched_signals = _matched_signals(text)
    reasoning_type = _reasoning_type(text, matched_signals, str(chunk.get("pedagogical_role", "") or ""))
    score = _score(text, matched_signals, reasoning_type, chunk)
    quality_flags = _as_list(chunk.get("quality_flags"))
    human_review_required = bool(
        quality_flags
        or chunk.get("academic_level") in {"WSET_DIPLOMA", "MIXED"}
        or 0.5 <= score < 0.75
    )
    return {
        "chunk_id": str(chunk.get("chunk_id", "")),
        "source_filename": str(chunk.get("source_filename", "")),
        "video_title_guess": str(chunk.get("video_title_guess") or chunk.get("video_title") or ""),
        "academic_level": str(chunk.get("academic_level", "")),
        "pedagogical_role": str(chunk.get("pedagogical_role", "")),
        "text_excerpt": _excerpt(text),
        "golden_tutor_chunk_candidate": score >= 0.75,
        "pedagogical_value_score": round(score, 2),
        "retrieval_priority": _priority(score),
        "reasoning_type": reasoning_type,
        "matched_signals": matched_signals,
        "quality_flags": quality_flags,
        "human_review_required": human_review_required,
    }


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    with path.open("r", encoding="utf-8-sig") as file:
        for line_number, line in enumerate(file, start=1):
            if not line.strip():
                continue
            try:
                value = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSONL in {path}:{line_number}") from exc
            if isinstance(value, dict):
                rows.append(value)
    return rows


def _is_manual_tutor_chunk(chunk: dict[str, Any]) -> bool:
    return (
        chunk.get("source_type") == SOURCE_TYPE
        and chunk.get("agent_corpus") == AGENT_CORPUS
        and chunk.get("safe_for_examiner") is False
    )


def _matched_signals(text: str) -> list[str]:
    found = []
    for label, pattern, _ in SIGNAL_PATTERNS:
        if re.search(pattern, text, flags=re.IGNORECASE | re.DOTALL):
            found.append(label)
    return found


def _reasoning_type(text: str, matched_signals: list[str], role: str) -> str:
    lower_signals = set(matched_signals)
    if {"students lose marks"} & lower_signals:
        return "common_mistake"
    if {"you need to explain why", "justify", "link"} & lower_signals:
        return "sat_logic"
    if {"written question"} & lower_signals:
        return "answer_structure"
    if {"examiner is looking for", "in the exam", "tasting exam", "marks", "WSET wants"} & lower_signals:
        return "exam_strategy"
    if {"quality assessment", "readiness", "balance intensity complexity length"} & lower_signals:
        return "tasting_calibration"
    if {"cause and effect", "because", "therefore"} & lower_signals:
        return "cause_effect"
    for label, patterns in REASONING_PATTERNS:
        if any(re.search(pattern, text, flags=re.IGNORECASE) for pattern in patterns):
            return label
    if role == "tasting_practice":
        return "tasting_calibration"
    if role == "exam_strategy":
        return "exam_strategy"
    if role == "theory_explanation":
        return "theory_foundation"
    return "theory_foundation"


def _score(text: str, matched_signals: list[str], reasoning_type: str, chunk: dict[str, Any]) -> float:
    weights = {label: weight for label, _, weight in SIGNAL_PATTERNS}
    score = min(0.78, sum(weights[label] for label in matched_signals))
    if matched_signals:
        score += 0.18
    if reasoning_type in {
        "exam_strategy",
        "sat_logic",
        "answer_structure",
        "tasting_calibration",
        "common_mistake",
        "cause_effect",
    }:
        score += 0.08
    if str(chunk.get("pedagogical_role", "")) in {"exam_strategy", "tasting_practice"}:
        score += 0.05
    if chunk.get("exclude_from_retrieval") is True:
        score -= 0.2
    if len(_word_tokens(text)) < 40:
        score -= 0.1
    return max(0.0, min(1.0, score))


def _is_reportable(row: dict[str, Any]) -> bool:
    return bool(row["matched_signals"]) or float(row["pedagogical_value_score"]) >= 0.5


def _priority(score: float) -> str:
    if score >= 0.75:
        return "high"
    if score >= 0.5:
        return "medium"
    return "low"


def _excerpt(text: str, max_length: int = 420) -> str:
    normalized = re.sub(r"\s+", " ", text).strip()
    if len(normalized) <= max_length:
        return normalized
    return normalized[: max_length - 3].rstrip() + "..."


def _word_tokens(text: str) -> list[str]:
    return re.findall(r"\b[\w'-]+\b", text, flags=re.UNICODE)


def _as_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value]
    if value in (None, ""):
        return []
    return [str(value)]


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    **row,
                    "matched_signals": "|".join(row["matched_signals"]),
                    "quality_flags": "|".join(row["quality_flags"]),
                }
            )


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as file:
        for row in rows:
            file.write(json.dumps(row, ensure_ascii=False) + "\n")


def _write_summary(
    summary_path: Path,
    rows: list[dict[str, Any]],
    scanned_chunks: int,
    safe_for_examiner_values: set[Any],
    output_csv: Path,
    output_jsonl: Path,
) -> None:
    reasoning_counts = Counter(row["reasoning_type"] for row in rows)
    priority_counts = Counter(row["retrieval_priority"] for row in rows)
    golden_count = sum(1 for row in rows if row["golden_tutor_chunk_candidate"])
    safe_confirmation = safe_for_examiner_values == {False} if scanned_chunks else True
    generated_at = datetime.now(UTC).isoformat(timespec="seconds")
    lines = [
        "# Golden Tutor Chunk QA Summary",
        "",
        f"Generated at: {generated_at}",
        f"Report version: {REPORT_VERSION}",
        "",
        "## Scope",
        "",
        f"- Manual tutor chunks scanned: {scanned_chunks}",
        f"- Reportable candidate rows: {len(rows)}",
        f"- Golden tutor chunk candidates (score >= 0.75): {golden_count}",
        f"- safe_for_examiner remains false: {str(safe_confirmation).lower()}",
        f"- CSV: {output_csv.as_posix()}",
        f"- JSONL: {output_jsonl.as_posix()}",
        "",
        "## Retrieval Priority Counts",
        "",
        *[f"- {key}: {priority_counts.get(key, 0)}" for key in ("high", "medium", "low")],
        "",
        "## Reasoning Type Counts",
        "",
        *[f"- {key}: {reasoning_counts[key]}" for key in sorted(reasoning_counts)],
        "",
        "## Top 20 Candidates",
        "",
    ]
    for index, row in enumerate(rows[:20], start=1):
        signals = ", ".join(row["matched_signals"]) or "none"
        lines.append(
            f"{index}. {row['pedagogical_value_score']:.2f} "
            f"({row['retrieval_priority']}, {row['reasoning_type']}) "
            f"{row['chunk_id']} - {row['video_title_guess']} | signals: {signals}"
        )
    lines.append("")
    lines.append("Note: These are Tutor-only pedagogical retrieval candidates and are not official WSET material.")
    summary_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    from .config import WINE_WITH_JIMMY_ROOT

    report = generate_golden_tutor_chunk_reports(WINE_WITH_JIMMY_ROOT)
    golden_count = sum(1 for row in report.candidate_rows if row["golden_tutor_chunk_candidate"])
    print(
        "Golden Tutor Chunk QA complete. "
        f"scanned={report.scanned_chunks} "
        f"rows={len(report.candidate_rows)} "
        f"golden={golden_count} "
        f"csv={report.output_csv} "
        f"jsonl={report.output_jsonl} "
        f"summary={report.summary_path}"
    )


if __name__ == "__main__":
    main()
