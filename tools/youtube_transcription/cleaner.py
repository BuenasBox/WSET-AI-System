"""Safe local transcript cleaning and chunk preparation.

This module only reads existing local raw transcripts, metadata, and the
transcript status index. It does not fetch captions, run Whisper, summarize,
build embeddings, or touch Examiner agent logic.
"""

from __future__ import annotations

import csv
import json
import re
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .dictionary import (
    WsetDictionary,
    load_wset_dictionary,
    low_confidence_terms as dictionary_low_confidence_terms,
    summarize_matches,
)


CLEANING_VERSION = "transcript_cleaning_v1.2"
ALLOWED_TRANSCRIPT_STATUSES = {"completed", "skipped"}
QUALITY_FLAGS = (
    "possible_asr_error",
    "low_confidence_term",
    "noisy_caption",
    "incomplete_transcript",
    "language_mismatch",
    "possible_appellation_error",
    "diploma_level_content",
    "mixed_level_content",
    "l3_relevant_content",
    "exam_strategy_content",
    "tasting_content",
    "theory_content",
)
BATCH_REPORT_COLUMNS = (
    "video_id",
    "video_title",
    "clean_status",
    "academic_level",
    "pedagogical_role",
    "word_count_raw",
    "word_count_clean",
    "chunk_count",
    "dictionary_match_count",
    "dictionary_categories_detected",
    "asr_corrections_count",
    "low_confidence_terms_count",
    "quality_flags",
    "safe_for_tutor",
    "safe_for_examiner",
    "processed_at",
    "error_message",
)
CAPTION_ARTIFACT_RE = re.compile(
    r"^\s*\[(?:music|applause|laughter|sound|silence|foreign|inaudible)\]\s*$",
    re.IGNORECASE,
)
INLINE_ARTIFACT_RE = re.compile(
    r"\s*\[(?:music|applause|laughter|sound|silence|foreign|inaudible)\]\s*",
    re.IGNORECASE,
)
TIMESTAMPED_LINE_RE = re.compile(r"^\s*(?:\[\d{2}:\d{2}:\d{2}\]|\d{1,2}:\d{2}(?::\d{2})?)\s*(.*)$")
WORD_RE = re.compile(r"\b[\w'-]+\b", re.UNICODE)
SENTENCE_END_RE = re.compile(r"[.!?][\"')\]]?$")
QUESTION_START_RE = re.compile(r"^(?:q|question)\s*[:.-]|\?$", re.IGNORECASE)
ANSWER_START_RE = re.compile(r"^(?:a|answer)\s*[:.-]", re.IGNORECASE)
SUSPICIOUS_ASR_TERMS = (
    "wct",
    "wsct",
    "vtic",
    "vticulture",
    "desert likee",
)
APPELLATION_SUSPECTS = (
    "barosa",
    "burgandy",
    "bugundy",
    "bordeauxx",
    "champagn",
)

REGION_TERMS = (
    "Bordeaux",
    "Burgundy",
    "Champagne",
    "Rioja",
    "Southern France",
    "Provence",
    "Languedoc-Roussillon",
    "Roussillon",
    "Rhône",
    "Alsace",
)
APPELLATION_TERMS = ("Port", "Sherry", "IGP Pays d'Oc")
GRAPE_TERMS = (
    "Riesling",
    "Chardonnay",
    "Sauvignon Blanc",
    "Pinot Noir",
    "Cabernet Sauvignon",
    "Merlot",
    "Syrah",
    "Grenache",
    "Sangiovese",
    "Nebbiolo",
)
SAT_TERMS = (
    "appearance",
    "nose",
    "palate",
    "conclusions",
    "balance",
    "intensity",
    "complexity",
    "length",
    "readiness",
    "quality assessment",
)
WINEMAKING_TERMS = (
    "oak",
    "lees",
    "malolactic",
    "botrytis",
    "noble rot",
    "whole bunch",
    "fermentation",
    "maceration",
    "Mediterranean climate",
    "drought",
    "disease pressure",
    "mildew",
    "rot",
)
EXAM_TERMS = ("SAT", "BICL", "WSET Level 3", "Diploma", "Level 4")
TERM_GROUPS = {
    "regions": REGION_TERMS,
    "appellations": APPELLATION_TERMS,
    "grape_varieties": GRAPE_TERMS,
    "sat_terms": SAT_TERMS,
    "exam_terms": EXAM_TERMS,
}
GENERAL_ASR_CORRECTIONS = (
    ("wsct", "WSET"),
    ("wct", "WSET"),
    ("longodop rusilion", "Languedoc-Roussillon"),
    ("victor culture", "viticulture"),
    ("igp day paid dock", "IGP Pays d'Oc"),
    ("santia basie", "Sangiovese"),
)


@dataclass(frozen=True)
class TranscriptPaths:
    """Resolved input and output paths for one local transcript."""

    video_id: str
    raw_json_path: Path | None
    raw_txt_path: Path
    metadata_path: Path
    clean_path: Path
    chunk_ready_path: Path
    enrichment_path: Path
    report_path: Path


def clean_one_video(video_id: str, root: Path, force: bool = False) -> dict[str, Any]:
    """Clean one local transcript and write derived outputs."""
    status_by_video_id = _read_status_index(root / "index" / "transcript_status.csv")
    status_row = status_by_video_id.get(video_id, {})
    _validate_processable_status(video_id, status_row)

    paths = resolve_transcript_paths(video_id, root)
    output_paths = (
        paths.clean_path,
        paths.chunk_ready_path,
        paths.enrichment_path,
        paths.report_path,
    )
    if not force:
        existing = [path for path in output_paths if path.exists()]
        if existing:
            raise FileExistsError(
                "Derived output already exists; rerun with --force to overwrite: "
                + ", ".join(str(path) for path in existing)
            )

    report = _build_outputs(paths, status_row)
    for path in output_paths:
        _ensure_output_directory(path.parent)

    paths.clean_path.write_text(report["clean_markdown"], encoding="utf-8")
    paths.chunk_ready_path.write_text(report["chunk_jsonl"], encoding="utf-8")
    paths.enrichment_path.write_text(
        json.dumps(report["enrichment"], indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    paths.report_path.write_text(
        json.dumps(report["cleaning_report"], indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    _upsert_batch_report(root / "reports" / "cleaning_batch_report.csv", report["batch_row"])
    return report["cleaning_report"]


def clean_batch(root: Path, limit: int | None = None, dry_run: bool = False, force: bool = False) -> list[dict[str, Any]]:
    """Process processable local transcripts from the status index."""
    status_by_video_id = _read_status_index(root / "index" / "transcript_status.csv")
    rows = [
        row
        for row in status_by_video_id.values()
        if row.get("transcript_status") in ALLOWED_TRANSCRIPT_STATUSES
        and (_path_exists(row.get("raw_txt_path")) or _path_exists(row.get("raw_json_path")))
    ]
    if limit is not None:
        rows = rows[:limit]

    results: list[dict[str, Any]] = []
    batch_rows: list[dict[str, Any]] = []
    for row in rows:
        video_id = row.get("video_id", "")
        processed_at = _utc_now()
        try:
            paths = resolve_transcript_paths(video_id, root)
            if dry_run:
                result = {
                    "video_id": video_id,
                    "video_title": _video_title(row, {}),
                    "clean_status": "dry_run",
                    "output_clean_path": str(paths.clean_path),
                    "output_chunk_ready_path": str(paths.chunk_ready_path),
                    "output_enrichment_path": str(paths.enrichment_path),
                    "report_path": str(paths.report_path),
                    "safe_for_tutor": True,
                    "safe_for_examiner": False,
                    "processed_at": processed_at,
                    "dictionary_match_count": 0,
                    "dictionary_categories_detected": [],
                    "asr_corrections_applied": [],
                    "low_confidence_terms": [],
                    "quality_flags": [],
                }
                batch_rows.append(_batch_row_from_result(result, "dry_run", ""))
            else:
                result = clean_one_video(video_id, root, force=force)
            results.append(result)
        except Exception as exc:  # noqa: BLE001 - preserve batch progress.
            error = _normalize_error_message(exc)
            result = {
                "video_id": video_id,
                "video_title": row.get("video_title", ""),
                "clean_status": "error",
                "academic_level": "UNKNOWN",
                "pedagogical_role": "enrichment",
                "word_count_raw": 0,
                "word_count_clean": 0,
                "chunk_count": 0,
                "dictionary_match_count": 0,
                "dictionary_categories_detected": [],
                "asr_corrections_applied": [],
                "low_confidence_terms": [],
                "quality_flags": [],
                "safe_for_tutor": True,
                "safe_for_examiner": False,
                "processed_at": processed_at,
                "error_message": error,
            }
            results.append(result)
            batch_rows.append(_batch_row_from_result(result, "error", error))

    if dry_run or batch_rows:
        _ensure_output_directory(root / "reports")
        _upsert_many_batch_rows(root / "reports" / "cleaning_batch_report.csv", batch_rows)
    return results


def resolve_transcript_paths(video_id: str, root: Path) -> TranscriptPaths:
    """Resolve local raw, metadata, and requested output paths for a video ID."""
    raw_dir = root / "raw"
    metadata_path = root / "metadata" / f"{video_id}.metadata.json"
    if not metadata_path.exists():
        raise FileNotFoundError(f"Metadata not found for video_id={video_id}: {metadata_path}")

    metadata = _read_json(metadata_path)
    raw_txt_path = _metadata_path(metadata.get("raw_txt_path"))
    raw_json_path = _metadata_path(metadata.get("raw_json_path"))
    if not raw_txt_path or not raw_txt_path.exists():
        raw_txt_path = _single_match(raw_dir.glob(f"{video_id}__*.raw.txt"), "raw text", video_id)
    if raw_json_path and not raw_json_path.exists():
        raw_json_path = None
    if raw_json_path is None:
        matches = list(raw_dir.glob(f"{video_id}__*.raw.json"))
        raw_json_path = matches[0] if len(matches) == 1 else None

    base_name = raw_txt_path.name.removesuffix(".raw.txt")
    return TranscriptPaths(
        video_id=video_id,
        raw_json_path=raw_json_path,
        raw_txt_path=raw_txt_path,
        metadata_path=metadata_path,
        clean_path=root / "clean" / f"{base_name}.clean.md",
        chunk_ready_path=root / "chunk-ready" / f"{base_name}.chunks.jsonl",
        enrichment_path=root / "enrichment-ready" / f"{video_id}.enrichment.json",
        report_path=root / "reports" / f"{video_id}.cleaning_report.json",
    )


def clean_transcript(raw_text: str) -> str:
    """Return a conservatively cleaned transcript body."""
    clean_lines, _, _ = _clean_lines(_load_caption_lines(raw_text, {}))
    return "\n\n".join(_paragraphize(clean_lines)).strip()


def _build_outputs(paths: TranscriptPaths, status_row: dict[str, str]) -> dict[str, Any]:
    raw_text = paths.raw_txt_path.read_text(encoding="utf-8")
    metadata = _read_json(paths.metadata_path)
    raw_json = _read_json(paths.raw_json_path) if paths.raw_json_path else {}
    dictionary = load_wset_dictionary()

    raw_lines = _load_caption_lines(raw_text, raw_json)
    clean_lines, removed_artifacts, collapsed_duplicates = _clean_lines(raw_lines)
    title = _video_title(status_row, metadata)
    clean_lines, asr_corrections_applied, low_confidence_terms = _apply_asr_corrections(
        clean_lines,
        f"{title}\n{raw_text}",
        dictionary,
    )
    clean_paragraphs = _paragraphize(clean_lines)
    clean_body = "\n\n".join(clean_paragraphs).strip()
    raw_word_count = _word_count(raw_text)
    clean_word_count = _word_count(clean_body)
    processed_at = _utc_now()
    detected = detect_terms(f"{title}\n{clean_body}")
    dictionary_matches = dictionary.find_matches(f"{title}\n{clean_body}")
    dictionary_summary = summarize_matches(dictionary_matches)
    low_confidence_terms = sorted(
        set(low_confidence_terms) | set(dictionary_low_confidence_terms(dictionary_matches))
    )
    academic_level = _academic_level(f"{title}\n{clean_body}")
    pedagogical_role = _pedagogical_role(f"{title}\n{clean_body}", academic_level)
    quality_flags = _quality_flags(
        raw_text=raw_text,
        clean_text=clean_body,
        metadata=metadata,
        raw_json=raw_json,
        removed_artifacts=removed_artifacts,
        collapsed_duplicates=collapsed_duplicates,
        academic_level=academic_level,
        pedagogical_role=pedagogical_role,
    )
    chunks = _make_chunks(
        clean_body=clean_body,
        video_id=paths.video_id,
        video_title=title,
        academic_level=academic_level,
        pedagogical_role=pedagogical_role,
        document_detected=detected,
        document_quality_flags=quality_flags,
        dictionary=dictionary,
    )
    common = {
        "video_id": paths.video_id,
        "video_title": title,
        "source_type": "youtube_transcript",
        "source_trust_tier": "pedagogical",
        "agent_corpus": "tutor",
        "safe_for_tutor": True,
        "safe_for_examiner": False,
        "academic_level": academic_level,
        "pedagogical_role": pedagogical_role,
        "quality_flags": quality_flags,
        "asr_corrections_applied": asr_corrections_applied,
        "low_confidence_terms": low_confidence_terms,
        "dictionary_version": dictionary.version,
        "dictionary_terms_matched": dictionary_summary["canonical_terms_detected"],
        "dictionary_categories_detected": dictionary_summary["dictionary_categories_detected"],
        "dictionary_match_count": len(dictionary_matches),
        "cleaning_version": CLEANING_VERSION,
        "processed_at": processed_at,
    }
    enrichment = {
        **common,
        "source_raw_txt_path": str(paths.raw_txt_path),
        "source_raw_json_path": str(paths.raw_json_path) if paths.raw_json_path else "",
        "source_metadata_path": str(paths.metadata_path),
        "clean_transcript_path": str(paths.clean_path),
        "chunk_ready_path": str(paths.chunk_ready_path),
        "word_count_raw": raw_word_count,
        "word_count_clean": clean_word_count,
        "chunk_count": len(chunks),
        "asr_corrections_applied": asr_corrections_applied,
        "low_confidence_terms": low_confidence_terms,
        "dictionary_version": dictionary.version,
        "dictionary_terms_matched": dictionary_summary["canonical_terms_detected"],
        "dictionary_categories_detected": dictionary_summary["dictionary_categories_detected"],
        "dictionary_match_count": len(dictionary_matches),
        "official_term_matches": dictionary_summary["official_term_matches"],
        **detected,
    }
    cleaning_report = {
        **common,
        "clean_status": "completed",
        "word_count_raw": raw_word_count,
        "word_count_clean": clean_word_count,
        "chunk_count": len(chunks),
        "output_clean_path": str(paths.clean_path),
        "output_chunk_ready_path": str(paths.chunk_ready_path),
        "output_enrichment_path": str(paths.enrichment_path),
        "report_path": str(paths.report_path),
        "removed_caption_artifact_lines": removed_artifacts,
        "collapsed_duplicate_fragments": collapsed_duplicates,
        "asr_corrections_applied": asr_corrections_applied,
        "low_confidence_terms": low_confidence_terms,
        "error_message": "",
    }
    return {
        "clean_markdown": _render_clean_transcript(common, clean_body),
        "chunk_jsonl": "".join(json.dumps(chunk, ensure_ascii=False) + "\n" for chunk in chunks),
        "enrichment": enrichment,
        "cleaning_report": cleaning_report,
        "batch_row": _batch_row_from_result(cleaning_report, "completed", ""),
    }


def detect_terms(text: str) -> dict[str, list[str]]:
    """Rule-based wine term detection without LLM extraction."""
    return {key: _find_terms(text, terms) for key, terms in TERM_GROUPS.items()} | {
        "topics_detected": _topics_detected(text)
    }


def _apply_asr_corrections(
    clean_lines: list[str],
    context_text: str,
    dictionary: WsetDictionary | None = None,
) -> tuple[list[str], list[dict[str, Any]], list[str]]:
    corrected_lines = clean_lines[:]
    applied: list[dict[str, Any]] = []
    low_confidence_terms: list[str] = []
    context_lower = context_text.lower()
    southern_france_context = bool(
        re.search(r"\b(?:southern france|provence|languedoc|roussillon|pays d'oc)\b", context_lower)
    )
    wine_law_context = bool(
        re.search(r"\b(?:wine law|appellation|appellations|aoc|doc|igp|classification)\b", context_lower)
    )

    for original, replacement in GENERAL_ASR_CORRECTIONS:
        corrected_lines, count = _replace_phrase(corrected_lines, original, replacement)
        if count:
            applied.append(
                {
                    "original": original,
                    "corrected": replacement,
                    "occurrences": count,
                    "confidence": "high",
                }
            )

    if dictionary is not None:
        for original, replacement in dictionary.high_confidence_alias_corrections:
            corrected_lines, count = _replace_phrase(corrected_lines, original, replacement)
            if count:
                applied.append(
                    {
                        "original": original,
                        "corrected": replacement,
                        "occurrences": count,
                        "confidence": "high",
                        "source": "wset_master_dictionary",
                    }
                )

    corrected_lines, count = _replace_phrase(corrected_lines, "roan", "Rhône")
    if count:
        applied.append(
            {
                "original": "roan",
                "corrected": "Rhône",
                "occurrences": count,
                "confidence": "high",
            }
        )

    if southern_france_context:
        corrected_lines, count = _replace_phrase(corrected_lines, "russian", "Roussillon")
        if count:
            applied.append(
                {
                    "original": "russian",
                    "corrected": "Roussillon",
                    "occurrences": count,
                    "confidence": "high",
                    "context": "Southern France",
                }
            )
    elif any(re.search(r"\brussian\b", line, flags=re.IGNORECASE) for line in corrected_lines):
        low_confidence_terms.append("russian")

    if wine_law_context:
        corrected_lines, count = _replace_phrase(corrected_lines, "appalachians", "appellations")
        if count:
            applied.append(
                {
                    "original": "appalachians",
                    "corrected": "appellations",
                    "occurrences": count,
                    "confidence": "high",
                    "context": "wine law",
                }
            )
    elif any(re.search(r"\bappalachians\b", line, flags=re.IGNORECASE) for line in corrected_lines):
        low_confidence_terms.append("appalachians")

    return corrected_lines, applied, sorted(set(low_confidence_terms))


def _replace_phrase(lines: list[str], original: str, replacement: str) -> tuple[list[str], int]:
    pattern = re.compile(r"(?<!\w)" + re.escape(original).replace(r"\ ", r"\s+") + r"(?!\w)", re.IGNORECASE)
    count = 0
    updated = []
    for line in lines:
        new_line, line_count = pattern.subn(replacement, line)
        updated.append(new_line)
        count += line_count
    return updated, count


def _make_chunks(
    clean_body: str,
    video_id: str,
    video_title: str,
    academic_level: str,
    pedagogical_role: str,
    document_detected: dict[str, list[str]],
    document_quality_flags: list[str],
    dictionary: WsetDictionary | None = None,
) -> list[dict[str, Any]]:
    paragraphs = [paragraph.strip() for paragraph in clean_body.split("\n\n") if paragraph.strip()]
    chunks_text: list[str] = []
    current: list[str] = []
    current_words = 0
    previous_questionish = False
    current_topic = ""

    for paragraph in paragraphs:
        words = _word_count(paragraph)
        paragraph_questionish = _is_question_answerish(paragraph)
        paragraph_topic = _primary_topic(paragraph)
        should_flush = (
            current
            and current_words >= 150
            and (
                current_words + words > 350
                or (paragraph_topic and current_topic and paragraph_topic != current_topic)
            )
            and not previous_questionish
            and not paragraph_questionish
        )
        if should_flush:
            chunks_text.append("\n\n".join(current).strip())
            current = []
            current_words = 0
            current_topic = ""

        current.append(paragraph)
        current_words += words
        current_topic = current_topic or paragraph_topic
        previous_questionish = paragraph_questionish

    if current:
        chunks_text.append("\n\n".join(current).strip())
    if not chunks_text and clean_body.strip():
        chunks_text = [clean_body.strip()]

    chunks: list[dict[str, Any]] = []
    dictionary = dictionary or load_wset_dictionary()
    for index, text in enumerate(chunks_text):
        chunk_detected = detect_terms(text)
        dictionary_summary = summarize_matches(dictionary.find_matches(text))
        chunk_role = _pedagogical_role(text, academic_level)
        segment_type = _segment_type(text, index, len(chunks_text))
        chunk_flags = [
            flag
            for flag in document_quality_flags
            if flag in {"diploma_level_content", "mixed_level_content", "l3_relevant_content"}
            or _flag_matches_text(flag, text)
        ]
        chunks.append(
            {
                "chunk_id": f"{video_id}-{index:04d}",
                "video_id": video_id,
                "video_title": video_title,
                "chunk_index": index,
                "text": text,
                "source_type": "youtube_transcript",
                "source_trust_tier": "pedagogical",
                "agent_corpus": "tutor",
                "safe_for_tutor": True,
                "safe_for_examiner": False,
                "academic_level": academic_level,
                "pedagogical_role": chunk_role or pedagogical_role,
                "segment_type": segment_type,
                "exclude_from_retrieval": segment_type in {"intro", "outro", "promotional"},
                "topics_detected": chunk_detected["topics_detected"],
                "grape_varieties": chunk_detected["grape_varieties"],
                "regions": chunk_detected["regions"],
                "appellations": chunk_detected["appellations"],
                "sat_terms": chunk_detected["sat_terms"],
                "exam_terms": chunk_detected["exam_terms"],
                "canonical_terms_detected": dictionary_summary["canonical_terms_detected"],
                "dictionary_categories_detected": dictionary_summary["dictionary_categories_detected"],
                "official_term_matches": dictionary_summary["official_term_matches"],
                "quality_flags": chunk_flags,
            }
        )
    return chunks


def _load_caption_lines(raw_text: str, raw_json: dict[str, Any]) -> list[tuple[str, str]]:
    segments = raw_json.get("segments")
    if isinstance(segments, list) and segments:
        lines = []
        for segment in segments:
            if not isinstance(segment, dict):
                continue
            lines.append(("", str(segment.get("text") or "")))
        if lines:
            return lines

    lines = []
    for raw_line in raw_text.splitlines():
        match = TIMESTAMPED_LINE_RE.match(raw_line)
        lines.append(("", match.group(1) if match else raw_line))
    return lines


def _clean_lines(lines: list[tuple[str, str]]) -> tuple[list[str], int, int]:
    clean_lines: list[str] = []
    removed_artifacts = 0
    collapsed_duplicates = 0
    previous_fragment = ""

    for _, text in lines:
        normalized_text = _normalize_whitespace(INLINE_ARTIFACT_RE.sub(" ", text))
        if not normalized_text:
            if CAPTION_ARTIFACT_RE.match(text):
                removed_artifacts += 1
            continue
        if CAPTION_ARTIFACT_RE.match(normalized_text):
            removed_artifacts += 1
            continue

        comparison_fragment = _comparison_key(normalized_text)
        if comparison_fragment and comparison_fragment == previous_fragment:
            collapsed_duplicates += 1
            continue
        previous_fragment = comparison_fragment
        clean_lines.append(normalized_text)

    return clean_lines, removed_artifacts, collapsed_duplicates


def _paragraphize(clean_lines: list[str]) -> list[str]:
    paragraphs: list[str] = []
    current: list[str] = []
    current_words = 0
    current_topic = ""

    for line in clean_lines:
        line_topic = _primary_topic(line)
        if current and current_topic == "promotional" and line_topic != "promotional":
            paragraphs.append(_normalize_whitespace(" ".join(current)))
            current = []
            current_words = 0
            current_topic = ""
        current.append(line)
        current_words += _word_count(line)
        current_topic = current_topic or line_topic
        if SENTENCE_END_RE.search(line) or current_words >= 90 or _is_question_answerish(line):
            paragraphs.append(_normalize_whitespace(" ".join(current)))
            current = []
            current_words = 0
            current_topic = ""
    if current:
        paragraphs.append(_normalize_whitespace(" ".join(current)))
    return paragraphs


def _quality_flags(
    raw_text: str,
    clean_text: str,
    metadata: dict[str, Any],
    raw_json: dict[str, Any],
    removed_artifacts: int,
    collapsed_duplicates: int,
    academic_level: str,
    pedagogical_role: str,
) -> list[str]:
    flags = set()
    lower_text = clean_text.lower()
    raw_word_count = _word_count(raw_text)
    clean_word_count = _word_count(clean_text)

    if removed_artifacts or collapsed_duplicates or re.search(r"\[[^\]]+\]", raw_text):
        flags.add("noisy_caption")
    if raw_word_count < 100 or clean_word_count < 100:
        flags.add("incomplete_transcript")
    language = raw_json.get("language") or metadata.get("caption_language") or metadata.get("language_detected") or ""
    if isinstance(language, str) and language and not language.lower().startswith("en"):
        flags.add("language_mismatch")
    if any(term in lower_text for term in SUSPICIOUS_ASR_TERMS):
        flags.add("possible_asr_error")
        flags.add("low_confidence_term")
    if any(term in lower_text for term in APPELLATION_SUSPECTS):
        flags.add("possible_appellation_error")
    if academic_level == "WSET_DIPLOMA":
        flags.add("diploma_level_content")
    if academic_level == "MIXED":
        flags.add("mixed_level_content")
    if re.search(r"\b(?:wset\s*(?:level\s*)?3|level\s*3|l3)\b", lower_text):
        flags.add("l3_relevant_content")
    if pedagogical_role == "exam_strategy":
        flags.add("exam_strategy_content")
    if pedagogical_role == "tasting_practice" or _find_terms(lower_text, SAT_TERMS):
        flags.add("tasting_content")
    if pedagogical_role == "theory_explanation" or re.search(r"\b(?:climate|soil|grape growing|vinification|fermentation|maceration)\b", lower_text):
        flags.add("theory_content")

    return [flag for flag in QUALITY_FLAGS if flag in flags]


def _academic_level(text: str) -> str:
    lower_text = text.lower()
    has_diploma = bool(re.search(r"\b(?:diploma|level\s*4|wset\s*(?:level\s*)?4)\b", lower_text))
    has_l3 = bool(re.search(r"\b(?:wset\s*(?:level\s*)?3|level\s*3|l3)\b", lower_text))
    if has_diploma and has_l3:
        return "MIXED"
    if has_diploma:
        return "WSET_DIPLOMA"
    if has_l3:
        return "WSET_L3"
    return "UNKNOWN"


def _pedagogical_role(text: str, academic_level: str) -> str:
    lower_text = text.lower()
    if academic_level == "WSET_DIPLOMA":
        return "advanced_enrichment"
    if re.search(
        r"\b(?:exam technique|exam tips?|how to pass|written question|"
        r"working written question|bicl|marks?|for the exam)\b",
        lower_text,
    ):
        return "exam_strategy"
    if re.search(r"\btasting\b", lower_text) or _find_terms(text, SAT_TERMS):
        return "tasting_practice"
    if re.search(r"\b(?:climate|soil|grape growing|vinification|fermentation|maceration|theory)\b", lower_text):
        return "theory_explanation"
    if academic_level == "WSET_L3":
        return "foundational"
    return "enrichment"


def _render_clean_transcript(metadata: dict[str, Any], body: str) -> str:
    return f"---\n{json.dumps(metadata, indent=2, ensure_ascii=False)}\n---\n\n{body}\n"


def _read_status_index(path: Path) -> dict[str, dict[str, str]]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return {
            row.get("video_id", ""): row
            for row in csv.DictReader(file)
            if row.get("video_id")
        }


def _validate_processable_status(video_id: str, status_row: dict[str, str]) -> None:
    if not status_row:
        return
    transcript_status = status_row.get("transcript_status", "")
    if transcript_status not in ALLOWED_TRANSCRIPT_STATUSES:
        raise ValueError(
            f"Video {video_id} has transcript_status={transcript_status!r}; "
            "only completed or skipped transcripts may be cleaned."
        )


def _upsert_batch_report(path: Path, row: dict[str, Any]) -> None:
    _upsert_many_batch_rows(path, [row])


def _upsert_many_batch_rows(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        return
    existing = []
    if path.exists():
        with path.open("r", encoding="utf-8-sig", newline="") as file:
            existing = list(csv.DictReader(file))
    by_video_id = {row.get("video_id", ""): row for row in existing if row.get("video_id")}
    for row in rows:
        by_video_id[str(row.get("video_id", ""))] = {column: row.get(column, "") for column in BATCH_REPORT_COLUMNS}
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=BATCH_REPORT_COLUMNS)
        writer.writeheader()
        writer.writerows(by_video_id.values())


def _batch_row_from_result(result: dict[str, Any], status: str, error_message: str) -> dict[str, Any]:
    flags = result.get("quality_flags", [])
    dictionary_categories = result.get("dictionary_categories_detected", [])
    asr_corrections = result.get("asr_corrections_applied", [])
    low_confidence = result.get("low_confidence_terms", [])
    return {
        "video_id": result.get("video_id", ""),
        "video_title": result.get("video_title", ""),
        "clean_status": status,
        "academic_level": result.get("academic_level", ""),
        "pedagogical_role": result.get("pedagogical_role", ""),
        "word_count_raw": result.get("word_count_raw", ""),
        "word_count_clean": result.get("word_count_clean", ""),
        "chunk_count": result.get("chunk_count", ""),
        "dictionary_match_count": result.get("dictionary_match_count", 0),
        "dictionary_categories_detected": "|".join(dictionary_categories)
        if isinstance(dictionary_categories, list)
        else dictionary_categories,
        "asr_corrections_count": len(asr_corrections) if isinstance(asr_corrections, list) else 0,
        "low_confidence_terms_count": len(low_confidence) if isinstance(low_confidence, list) else 0,
        "quality_flags": "|".join(flags) if isinstance(flags, list) else flags,
        "safe_for_tutor": result.get("safe_for_tutor", True),
        "safe_for_examiner": result.get("safe_for_examiner", False),
        "processed_at": result.get("processed_at", _utc_now()),
        "error_message": error_message,
    }


def _find_terms(text: str, terms: tuple[str, ...]) -> list[str]:
    found = []
    for term in terms:
        pattern = r"(?<!\w)" + re.escape(term).replace(r"\ ", r"\s+") + r"(?!\w)"
        if re.search(pattern, text, flags=re.IGNORECASE):
            found.append(term)
    return found


def _topics_detected(text: str) -> list[str]:
    lower_text = text.lower()
    topics = []
    if any(term.lower() in lower_text for term in REGION_TERMS + APPELLATION_TERMS):
        topics.append("regions")
    if any(term.lower() in lower_text for term in GRAPE_TERMS):
        topics.append("grape_varieties")
    if _find_terms(text, SAT_TERMS):
        topics.append("sat")
    if any(term.lower() in lower_text for term in WINEMAKING_TERMS):
        topics.append("winemaking")
    if re.search(r"\b(?:exam technique|exam tips?|how to pass|written question|working written question|marks?|bicl|for the exam)\b", lower_text):
        topics.append("exam_strategy")
    if re.search(r"\b(?:climate|soil|grape growing)\b", lower_text):
        topics.append("viticulture")
    return topics


def _primary_topic(text: str) -> str:
    lower_text = text.lower()
    if re.search(r"\b(?:welcome|channel|subscribe|portal|website|social media|contact|cheers goodbye|goodbye)\b", lower_text):
        return "promotional"
    if re.search(r"\b(?:location|border|southern france|provence|languedoc|roussillon|rhône)\b", lower_text):
        return "location"
    if re.search(r"\b(?:climate|mediterranean|rainfall|temperature|summer|winter|sunlight)\b", lower_text):
        return "climate"
    if re.search(r"\b(?:viticulture|grape growing|vine|drought|disease pressure|mildew|rot|yield)\b", lower_text):
        return "viticulture"
    if any(term.lower() in lower_text for term in GRAPE_TERMS):
        return "grape_varieties"
    if re.search(r"\b(?:style|body|alcohol|acidity|tannin|colour|aroma|flavour)\b", lower_text):
        return "wine_style"
    if re.search(r"\b(?:exam technique|exam tips?|how to pass|written question|working written question|marks?|bicl|for the exam)\b", lower_text):
        return "exam_tip"
    if re.search(r"\b(?:tasting|appearance|nose|palate|conclusions|quality assessment)\b", lower_text):
        return "tasting"
    if re.search(r"\b(?:market|price|volume|commercial|export|cost|affordable)\b", lower_text):
        return "commercial_factors"
    return "educational"


def _segment_type(text: str, chunk_index: int, chunk_count: int) -> str:
    lower_text = text.lower()
    promotional_score = sum(
        1
        for pattern in (
            r"\bwelcome\b",
            r"\bsubscribe\b",
            r"\bchannel\b",
            r"\bsocial media\b",
            r"\bcontact\b",
            r"\bportal\b",
            r"\bpayment\b",
            r"\bwebsite\b",
            r"\bwinewithjimmy\.com\b",
            r"\bclicking on the video\b",
            r"\bcheers goodbye\b",
            r"\bgoodbye\b",
        )
        if re.search(pattern, lower_text)
    )
    educational_score = sum(
        1
        for pattern in (
            r"\bclimate\b",
            r"\bviticulture\b",
            r"\bgrape\b",
            r"\bregion\b",
            r"\bappellation\b",
            r"\bfermentation\b",
            r"\bmaceration\b",
            r"\bmediterranean\b",
            r"\bdrought\b",
        )
        if re.search(pattern, lower_text)
    )
    if promotional_score >= 2 and promotional_score > educational_score:
        if chunk_index == 0 and re.search(r"\b(?:welcome|channel|clicking on the video)\b", lower_text):
            return "intro"
        if chunk_index >= max(0, chunk_count - 2) and re.search(r"\b(?:subscribe|channel|social media|website|cheers goodbye|goodbye)\b", lower_text):
            return "outro"
        return "promotional"
    if chunk_index >= max(0, chunk_count - 2) and re.search(r"\b(?:cheers goodbye|goodbye)\b", lower_text):
        return "outro"
    return "educational"


def _flag_matches_text(flag: str, text: str) -> bool:
    lower_text = text.lower()
    if flag == "exam_strategy_content":
        return bool(re.search(r"\b(?:exam technique|exam tips?|how to pass|written question|working written question|marks?|bicl|for the exam)\b", lower_text))
    if flag == "tasting_content":
        return bool(re.search(r"\btasting\b", lower_text) or _find_terms(text, SAT_TERMS))
    if flag == "theory_content":
        return bool(re.search(r"\b(?:climate|soil|fermentation|maceration|theory)\b", lower_text))
    return False


def _is_question_answerish(text: str) -> bool:
    stripped = text.strip()
    return bool(QUESTION_START_RE.search(stripped) or ANSWER_START_RE.search(stripped))


def _read_json(path: Path | None) -> dict[str, Any]:
    if path is None:
        return {}
    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)
    if not isinstance(data, dict):
        raise ValueError(f"Expected JSON object: {path}")
    return data


def _metadata_path(value: object) -> Path | None:
    if not isinstance(value, str) or not value:
        return None
    return Path(value)


def _single_match(matches: Any, label: str, video_id: str) -> Path:
    paths = list(matches)
    if not paths:
        raise FileNotFoundError(f"No {label} transcript found for video_id={video_id}")
    if len(paths) > 1:
        raise ValueError(f"Multiple {label} transcripts found for video_id={video_id}")
    return paths[0]


def _ensure_output_directory(directory: Path) -> None:
    existed = directory.exists()
    directory.mkdir(parents=True, exist_ok=True)
    gitkeep_path = directory / ".gitkeep"
    if not existed and not gitkeep_path.exists():
        gitkeep_path.write_text("", encoding="utf-8")


def _path_exists(value: object) -> bool:
    return isinstance(value, str) and bool(value) and Path(value).exists()


def _video_title(status_row: dict[str, str], metadata: dict[str, Any]) -> str:
    return str(status_row.get("video_title") or metadata.get("video_title") or "")


def _normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _comparison_key(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def _word_count(text: str) -> int:
    return len(WORD_RE.findall(text))


def _utc_now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds")


def _normalize_error_message(message: object, max_length: int = 300) -> str:
    text = str(message or "")
    text = re.sub(r"[\r\n\t]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) > max_length:
        return f"{text[: max_length - 3]}..."
    return text
