"""Local-only manual SRT import for Wine With Jimmy Tutor transcripts."""

from __future__ import annotations

import csv
import json
import re
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from . import cleaner
from .dictionary import (
    WsetDictionary,
    load_wset_dictionary,
    low_confidence_terms as dictionary_low_confidence_terms,
    summarize_matches,
)


SOURCE_TYPE = "manual_curated_srt"
SOURCE_TRUST_TIER = "pedagogical"
AGENT_CORPUS = "tutor"
MANUAL_IMPORT_VERSION = "manual_srt_import_v1.0"
SRT_TIME_RE = re.compile(
    r"(?P<start>\d{1,2}:\d{2}:\d{2}[,.]\d{1,3})\s*-->\s*"
    r"(?P<end>\d{1,2}:\d{2}:\d{2}[,.]\d{1,3})"
)
VIDEO_ID_VALUE_RE = re.compile(r"(?:v=|youtu\.be/)([A-Za-z0-9_-]{11})")
BRACKETED_VIDEO_ID_RE = re.compile(r"\[([A-Za-z0-9_-]{11})\]")
WORD_RE = re.compile(r"\b[\w'-]+\b", re.UNICODE)

MANUAL_BATCH_COLUMNS = (
    "source_filename",
    "safe_stem",
    "import_status",
    "video_title_guess",
    "video_id",
    "academic_level",
    "pedagogical_role",
    "segment_count",
    "word_count_raw",
    "word_count_clean",
    "chunk_count",
    "quality_flags",
    "safe_for_tutor",
    "safe_for_examiner",
    "processed_at",
    "error_message",
)


@dataclass(frozen=True)
class SrtSegment:
    index: int | None
    start_time: str
    end_time: str
    start_seconds: float | None
    end_seconds: float | None
    text: str


@dataclass(frozen=True)
class ManualSrtPaths:
    source_path: Path
    processed_json_path: Path
    processed_txt_path: Path
    clean_path: Path
    chunk_ready_path: Path
    enrichment_path: Path
    report_path: Path


def import_manual_srt_batch(
    root: Path,
    limit: int | None = None,
    dry_run: bool = False,
    force: bool = False,
) -> list[dict[str, Any]]:
    """Import manually downloaded SRT files without network or media access."""
    ensure_manual_import_directories(root)
    srt_files = discover_srt_files(root)
    if limit is not None:
        srt_files = srt_files[:limit]

    results: list[dict[str, Any]] = []
    batch_rows: list[dict[str, Any]] = []
    for path in srt_files:
        processed_at = _utc_now()
        try:
            classification = classify_filename(path.name)
            safe_stem = safe_filename_stem(path.stem)
            paths = resolve_manual_paths(root, path, safe_stem)
            if dry_run:
                result = {
                    **classification,
                    "source_filename": path.name,
                    "safe_stem": safe_stem,
                    "import_status": "dry_run",
                    "expected_outputs": expected_output_paths(paths),
                    "quality_flags": _metadata_quality_flags(classification),
                    "safe_for_tutor": True,
                    "safe_for_examiner": False,
                    "processed_at": processed_at,
                    "error_message": "",
                }
            else:
                result = import_one_manual_srt(root, path, force=force)
            results.append(result)
            batch_rows.append(_batch_row_from_result(result))
        except Exception as exc:  # noqa: BLE001 - keep batch progress visible.
            result = _error_result(path, processed_at, exc)
            if not dry_run:
                _write_error_report(root, path, result)
            results.append(result)
            batch_rows.append(_batch_row_from_result(result))

    if not dry_run:
        _write_batch_report(root / "manual-import" / "reports" / "manual_srt_import_report.csv", batch_rows)
    return results


def import_one_manual_srt(root: Path, source_path: Path, force: bool = False) -> dict[str, Any]:
    """Parse and import one local SRT file into Tutor-only derived artifacts."""
    ensure_manual_import_directories(root)
    classification = classify_filename(source_path.name)
    safe_stem = safe_filename_stem(source_path.stem)
    paths = resolve_manual_paths(root, source_path, safe_stem)
    outputs = (
        paths.processed_json_path,
        paths.processed_txt_path,
        paths.clean_path,
        paths.chunk_ready_path,
        paths.enrichment_path,
        paths.report_path,
    )
    if not force:
        existing = [path for path in outputs if path.exists()]
        if existing:
            raise FileExistsError(
                "Derived output already exists; rerun with --force to overwrite: "
                + ", ".join(str(path) for path in existing)
            )

    parsed = parse_srt_file(source_path)
    if not parsed["segments"]:
        raise ValueError("empty_srt")

    report = build_manual_outputs(paths, parsed, classification, safe_stem)
    for output_path in outputs:
        output_path.parent.mkdir(parents=True, exist_ok=True)

    paths.processed_json_path.write_text(
        json.dumps(report["manual_raw_json"], indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    paths.processed_txt_path.write_text(report["manual_raw_text"], encoding="utf-8")
    paths.clean_path.write_text(report["clean_markdown"], encoding="utf-8")
    paths.chunk_ready_path.write_text(report["chunk_jsonl"], encoding="utf-8")
    paths.enrichment_path.write_text(
        json.dumps(report["enrichment"], indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    paths.report_path.write_text(
        json.dumps(report["import_report"], indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    _write_batch_report(
        root / "manual-import" / "reports" / "manual_srt_import_report.csv",
        [_batch_row_from_result(report["import_report"])],
    )
    return report["import_report"]


def discover_srt_files(root: Path) -> list[Path]:
    return sorted((root / "manual-import" / "srt").glob("*.srt"), key=lambda path: path.name.lower())


def ensure_manual_import_directories(root: Path) -> None:
    for directory in (
        root / "manual-import" / "srt",
        root / "manual-import" / "processed",
        root / "manual-import" / "rejected",
        root / "manual-import" / "manifests",
        root / "manual-import" / "reports",
        root / "clean",
        root / "chunk-ready",
        root / "enrichment-ready",
    ):
        directory.mkdir(parents=True, exist_ok=True)


def parse_srt_file(path: Path) -> dict[str, Any]:
    """Parse imperfect UTF-8/UTF-8-SIG SRT into deduplicated segments."""
    raw_text = _read_srt_text(path)
    raw_segments, malformed = parse_srt_text(raw_text)
    segments: list[SrtSegment] = []
    duplicate_count = 0
    previous_key = ""
    for segment in raw_segments:
        text = _normalize_caption_text(segment.text)
        if not text:
            continue
        key = cleaner._comparison_key(text)
        if key and key == previous_key:
            duplicate_count += 1
            continue
        previous_key = key
        segments.append(
            SrtSegment(
                index=segment.index,
                start_time=segment.start_time,
                end_time=segment.end_time,
                start_seconds=segment.start_seconds,
                end_seconds=segment.end_seconds,
                text=text,
            )
        )
    return {
        "raw_text": raw_text,
        "segments": segments,
        "raw_segment_count": len(raw_segments),
        "duplicate_caption_lines_removed": duplicate_count,
        "malformed_srt": malformed,
    }


def parse_srt_text(text: str) -> tuple[list[SrtSegment], bool]:
    normalized = text.replace("\r\n", "\n").replace("\r", "\n").strip("\ufeff")
    if not normalized.strip():
        return [], False

    segments: list[SrtSegment] = []
    malformed = False
    blocks = re.split(r"\n\s*\n", normalized)
    fallback_index = 1
    for block in blocks:
        lines = [line.strip() for line in block.split("\n") if line.strip()]
        if not lines:
            continue
        time_line_position = next((i for i, line in enumerate(lines) if SRT_TIME_RE.search(line)), None)
        if time_line_position is None:
            malformed = True
            text_lines = [line for line in lines if not line.isdigit()]
            if text_lines:
                segments.append(
                    SrtSegment(None, "", "", None, None, _normalize_caption_text(" ".join(text_lines)))
                )
            continue
        index_value = _parse_index(lines[0]) if time_line_position > 0 else None
        match = SRT_TIME_RE.search(lines[time_line_position])
        assert match is not None
        text_lines = lines[time_line_position + 1 :]
        if not text_lines:
            malformed = True
            continue
        segments.append(
            SrtSegment(
                index=index_value if index_value is not None else fallback_index,
                start_time=_normalize_time(match.group("start")),
                end_time=_normalize_time(match.group("end")),
                start_seconds=_time_to_seconds(match.group("start")),
                end_seconds=_time_to_seconds(match.group("end")),
                text=_normalize_caption_text(" ".join(text_lines)),
            )
        )
        fallback_index += 1
    return segments, malformed


def classify_filename(source_filename: str) -> dict[str, Any]:
    title = _title_guess_from_filename(source_filename)
    level = classify_academic_level(title)
    role = classify_pedagogical_role(title, level)
    video_id = infer_video_id(source_filename)
    return {
        "source_filename": source_filename,
        "video_title_guess": title,
        "video_id": video_id,
        "source_type": SOURCE_TYPE,
        "source_trust_tier": SOURCE_TRUST_TIER,
        "agent_corpus": AGENT_CORPUS,
        "safe_for_tutor": True,
        "safe_for_examiner": False,
        "academic_level": level,
        "academic_level_guess": level,
        "pedagogical_role": role,
        "pedagogical_role_guess": role,
    }


def classify_academic_level(title: str) -> str:
    lower = title.lower()
    has_diploma = bool(re.search(r"\b(?:diploma|d3|level\s*4|l4|mw)\b", lower))
    has_l3 = bool(re.search(r"\b(?:wset\s*l3|wset\s*level\s*3|level\s*3|\bl3\b)\b", lower))
    if has_diploma and has_l3:
        return "MIXED"
    if has_diploma:
        return "WSET_DIPLOMA"
    if has_l3:
        return "WSET_L3"
    return "UNKNOWN"


def classify_pedagogical_role(title: str, academic_level: str = "UNKNOWN") -> str:
    lower = title.lower()
    if re.search(r"\b(?:mock|exam|question|how to pass|prepare|prep)\b", lower):
        return "exam_strategy"
    if re.search(r"\b(?:sat|tasting|acidity|quality)\b", lower):
        return "tasting_practice"
    if re.search(
        r"\b(?:winemaking|viticulture|climate|growing environment|soils?|water|sunlight|vineyard|vine)\b",
        lower,
    ):
        return "theory_explanation"
    if academic_level == "WSET_DIPLOMA":
        return "advanced_enrichment"
    if academic_level == "WSET_L3":
        return "foundational"
    return "unknown"


def infer_video_id(source_filename: str) -> str:
    direct_match = VIDEO_ID_VALUE_RE.search(source_filename)
    if direct_match:
        return direct_match.group(1)
    for candidate in BRACKETED_VIDEO_ID_RE.findall(source_filename):
        if candidate.lower() not in {"downsub.com"}:
            return candidate
    return ""


def safe_filename_stem(stem: str) -> str:
    value = re.sub(r"\[(?:English \(auto-generated\)|DownSub\.com|DownloadYoutubeSubtitles\.com)\]", " ", stem)
    value = re.sub(r"[^A-Za-z0-9._-]+", "_", value)
    value = re.sub(r"_+", "_", value).strip("._-")
    return value[:160] or "manual_srt"


def resolve_manual_paths(root: Path, source_path: Path, safe_stem: str) -> ManualSrtPaths:
    return ManualSrtPaths(
        source_path=source_path,
        processed_json_path=root / "manual-import" / "processed" / f"{safe_stem}.manual_raw.json",
        processed_txt_path=root / "manual-import" / "processed" / f"{safe_stem}.manual_raw.txt",
        clean_path=root / "clean" / f"{safe_stem}.clean.md",
        chunk_ready_path=root / "chunk-ready" / f"{safe_stem}.chunks.jsonl",
        enrichment_path=root / "enrichment-ready" / f"{safe_stem}.enrichment.json",
        report_path=root / "manual-import" / "reports" / f"{safe_stem}.manual_import_report.json",
    )


def expected_output_paths(paths: ManualSrtPaths) -> dict[str, str]:
    return {
        "manual_raw_json": str(paths.processed_json_path),
        "manual_raw_txt": str(paths.processed_txt_path),
        "clean_transcript": str(paths.clean_path),
        "chunk_ready_jsonl": str(paths.chunk_ready_path),
        "enrichment_metadata": str(paths.enrichment_path),
        "import_report": str(paths.report_path),
    }


def build_manual_outputs(
    paths: ManualSrtPaths,
    parsed: dict[str, Any],
    classification: dict[str, Any],
    safe_stem: str,
) -> dict[str, Any]:
    segments: list[SrtSegment] = parsed["segments"]
    dictionary = load_wset_dictionary()
    raw_text = _manual_raw_text(segments)
    clean_segments, removed_artifacts, collapsed_duplicates = _clean_segments(segments)
    title = classification["video_title_guess"]
    clean_lines = [segment["text"] for segment in clean_segments]
    clean_lines, asr_corrections, low_confidence = cleaner._apply_asr_corrections(
        clean_lines,
        f"{title}\n{raw_text}",
        dictionary,
    )
    clean_segments = [{**segment, "text": clean_lines[index]} for index, segment in enumerate(clean_segments)]
    clean_paragraphs = cleaner._paragraphize([(segment["text"]) for segment in clean_segments])
    clean_body = "\n\n".join(clean_paragraphs).strip()
    academic_level = classification["academic_level"]
    pedagogical_role = classification["pedagogical_role"]
    detected = cleaner.detect_terms(f"{title}\n{clean_body}")
    dictionary_matches = dictionary.find_matches(f"{title}\n{clean_body}")
    dictionary_summary = summarize_matches(dictionary_matches)
    low_confidence = sorted(set(low_confidence) | set(dictionary_low_confidence_terms(dictionary_matches)))
    quality_flags = _manual_quality_flags(
        source_path=paths.source_path,
        parsed=parsed,
        raw_text=raw_text,
        clean_text=clean_body,
        classification=classification,
        removed_artifacts=removed_artifacts,
        collapsed_duplicates=collapsed_duplicates,
        low_confidence_terms=low_confidence,
    )
    chunks = _make_manual_chunks(
        clean_segments=clean_segments,
        clean_body=clean_body,
        safe_stem=safe_stem,
        classification=classification,
        document_quality_flags=quality_flags,
        dictionary=dictionary,
    )
    processed_at = _utc_now()
    common = {
        "source_filename": paths.source_path.name,
        "video_title_guess": title,
        "video_id": classification["video_id"],
        "source_type": SOURCE_TYPE,
        "source_trust_tier": SOURCE_TRUST_TIER,
        "agent_corpus": AGENT_CORPUS,
        "safe_for_tutor": True,
        "safe_for_examiner": False,
        "academic_level": academic_level,
        "pedagogical_role": pedagogical_role,
        "quality_flags": quality_flags,
        "asr_corrections_applied": asr_corrections,
        "low_confidence_terms": low_confidence,
        "dictionary_version": dictionary.version,
        "canonical_terms_detected": dictionary_summary["canonical_terms_detected"],
        "dictionary_categories_detected": dictionary_summary["dictionary_categories_detected"],
        "official_term_matches": dictionary_summary["official_term_matches"],
        "manual_import_version": MANUAL_IMPORT_VERSION,
        "processed_at": processed_at,
    }
    manual_raw_json = {
        **common,
        "source_srt_path": str(paths.source_path),
        "segments": [_segment_as_dict(segment) for segment in segments],
        "duplicate_caption_lines_removed": parsed["duplicate_caption_lines_removed"],
        "raw_segment_count": parsed["raw_segment_count"],
    }
    enrichment = {
        **common,
        "source_srt_path": str(paths.source_path),
        "manual_raw_json_path": str(paths.processed_json_path),
        "manual_raw_txt_path": str(paths.processed_txt_path),
        "clean_transcript_path": str(paths.clean_path),
        "chunk_ready_path": str(paths.chunk_ready_path),
        "word_count_raw": _word_count(raw_text),
        "word_count_clean": _word_count(clean_body),
        "chunk_count": len(chunks),
        **detected,
    }
    import_report = {
        **enrichment,
        "safe_stem": safe_stem,
        "import_status": "completed",
        "segment_count": len(segments),
        "output_paths": expected_output_paths(paths),
        "removed_caption_artifact_lines": removed_artifacts,
        "collapsed_duplicate_fragments": collapsed_duplicates,
        "duplicate_caption_lines_removed": parsed["duplicate_caption_lines_removed"],
        "error_message": "",
    }
    return {
        "manual_raw_json": manual_raw_json,
        "manual_raw_text": raw_text,
        "clean_markdown": cleaner._render_clean_transcript(common, clean_body),
        "chunk_jsonl": "".join(json.dumps(chunk, ensure_ascii=False) + "\n" for chunk in chunks),
        "enrichment": enrichment,
        "import_report": import_report,
    }


def _make_manual_chunks(
    clean_segments: list[dict[str, Any]],
    clean_body: str,
    safe_stem: str,
    classification: dict[str, Any],
    document_quality_flags: list[str],
    dictionary: WsetDictionary,
) -> list[dict[str, Any]]:
    base_chunks = cleaner._make_chunks(
        clean_body=clean_body,
        video_id=safe_stem,
        video_title=classification["video_title_guess"],
        academic_level=classification["academic_level"],
        pedagogical_role=classification["pedagogical_role"],
        document_detected=cleaner.detect_terms(clean_body),
        document_quality_flags=document_quality_flags,
        dictionary=dictionary,
    )
    cursor = 0
    for index, chunk in enumerate(base_chunks):
        chunk_segment_count = _estimate_segment_span(chunk["text"], clean_segments, cursor)
        span = clean_segments[cursor : cursor + chunk_segment_count]
        cursor += chunk_segment_count
        start_time = _first_non_empty(segment.get("start_time", "") for segment in span)
        end_time = _last_non_empty(segment.get("end_time", "") for segment in span)
        chunk.update(
            {
                "chunk_id": f"{safe_stem}-{index:04d}",
                "source_filename": classification["source_filename"],
                "video_title_guess": classification["video_title_guess"],
                "video_id": classification["video_id"],
                "video_title": classification["video_title_guess"],
                "source_type": SOURCE_TYPE,
                "source_trust_tier": SOURCE_TRUST_TIER,
                "agent_corpus": AGENT_CORPUS,
                "safe_for_tutor": True,
                "safe_for_examiner": False,
                "academic_level": classification["academic_level"],
                "pedagogical_role": chunk.get("pedagogical_role") or classification["pedagogical_role"],
                "start_time": start_time,
                "end_time": end_time,
            }
        )
    return base_chunks


def _clean_segments(segments: list[SrtSegment]) -> tuple[list[dict[str, Any]], int, int]:
    cleaned_lines, removed_artifacts, collapsed_duplicates = cleaner._clean_lines(
        [(segment.start_time, segment.text) for segment in segments]
    )
    output = []
    segment_cursor = 0
    for clean_text in cleaned_lines:
        comparison = cleaner._comparison_key(clean_text)
        while segment_cursor < len(segments):
            segment = segments[segment_cursor]
            segment_cursor += 1
            if cleaner._comparison_key(segment.text) == comparison:
                output.append(
                    {
                        "start_time": segment.start_time,
                        "end_time": segment.end_time,
                        "start_seconds": segment.start_seconds,
                        "end_seconds": segment.end_seconds,
                        "text": clean_text,
                    }
                )
                break
    return output, removed_artifacts, collapsed_duplicates


def _manual_quality_flags(
    source_path: Path,
    parsed: dict[str, Any],
    raw_text: str,
    clean_text: str,
    classification: dict[str, Any],
    removed_artifacts: int,
    collapsed_duplicates: int,
    low_confidence_terms: list[str],
) -> list[str]:
    flags = set(_metadata_quality_flags(classification))
    if source_path.stat().st_size == 0 or not clean_text.strip():
        flags.add("empty_srt")
    if parsed["malformed_srt"]:
        flags.add("malformed_srt")
    if parsed["duplicate_caption_lines_removed"] or collapsed_duplicates:
        flags.add("duplicate_caption_lines")
    if "auto-generated" in source_path.name.lower():
        flags.add("likely_auto_generated_caption")
    if _word_count(clean_text) < 100:
        flags.add("very_short_transcript")
    if removed_artifacts or re.search(r"\[[^\]]+\]", raw_text):
        flags.add("noisy_caption")
    if any(term in clean_text.lower() for term in cleaner.SUSPICIOUS_ASR_TERMS):
        flags.add("possible_asr_error")
    if low_confidence_terms:
        flags.add("low_confidence_term")
    order = (
        "empty_srt",
        "malformed_srt",
        "duplicate_caption_lines",
        "likely_auto_generated_caption",
        "title_indicates_diploma",
        "title_indicates_mixed_level",
        "no_video_id_in_filename",
        "very_short_transcript",
        "noisy_caption",
        "possible_asr_error",
        "low_confidence_term",
    )
    return [flag for flag in order if flag in flags]


def _metadata_quality_flags(classification: dict[str, Any]) -> list[str]:
    flags = []
    if classification["academic_level"] == "WSET_DIPLOMA":
        flags.append("title_indicates_diploma")
    if classification["academic_level"] == "MIXED":
        flags.append("title_indicates_mixed_level")
    if not classification["video_id"]:
        flags.append("no_video_id_in_filename")
    return flags


def _title_guess_from_filename(source_filename: str) -> str:
    title = Path(source_filename).stem
    title = re.sub(r"\[English \(auto-generated\)\]", " ", title, flags=re.IGNORECASE)
    title = re.sub(r"\[DownSub\.com\]", " ", title, flags=re.IGNORECASE)
    title = re.sub(r"\[DownloadYoutubeSubtitles\.com\]", " ", title, flags=re.IGNORECASE)
    title = re.sub(r"\s+", " ", title).strip(" -_[]")
    return title


def _read_srt_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8")


def _manual_raw_text(segments: list[SrtSegment]) -> str:
    return "\n".join(
        f"[{segment.start_time} --> {segment.end_time}] {segment.text}"
        if segment.start_time or segment.end_time
        else segment.text
        for segment in segments
    ).strip() + "\n"


def _normalize_caption_text(text: str) -> str:
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def _parse_index(value: str) -> int | None:
    return int(value) if value.isdigit() else None


def _normalize_time(value: str) -> str:
    value = value.replace(",", ".")
    hours, minutes, seconds = value.split(":")
    if "." not in seconds:
        seconds = f"{seconds}.000"
    whole, millis = seconds.split(".", 1)
    return f"{int(hours):02d}:{int(minutes):02d}:{int(whole):02d}.{millis[:3].ljust(3, '0')}"


def _time_to_seconds(value: str) -> float:
    normalized = _normalize_time(value)
    hours, minutes, seconds = normalized.split(":")
    return int(hours) * 3600 + int(minutes) * 60 + float(seconds)


def _segment_as_dict(segment: SrtSegment) -> dict[str, Any]:
    return {
        "index": segment.index,
        "start_time": segment.start_time,
        "end_time": segment.end_time,
        "start_seconds": segment.start_seconds,
        "end_seconds": segment.end_seconds,
        "text": segment.text,
    }


def _estimate_segment_span(text: str, segments: list[dict[str, Any]], cursor: int) -> int:
    if cursor >= len(segments):
        return 0
    target_words = max(1, _word_count(text))
    words = 0
    count = 0
    while cursor + count < len(segments) and words < target_words:
        words += _word_count(segments[cursor + count]["text"])
        count += 1
    return max(1, count)


def _first_non_empty(values: Any) -> str:
    for value in values:
        if value:
            return str(value)
    return ""


def _last_non_empty(values: Any) -> str:
    found = ""
    for value in values:
        if value:
            found = str(value)
    return found


def _word_count(text: str) -> int:
    return len(WORD_RE.findall(text))


def _batch_row_from_result(result: dict[str, Any]) -> dict[str, Any]:
    flags = result.get("quality_flags", [])
    return {
        "source_filename": result.get("source_filename", ""),
        "safe_stem": result.get("safe_stem", ""),
        "import_status": result.get("import_status", ""),
        "video_title_guess": result.get("video_title_guess", ""),
        "video_id": result.get("video_id", ""),
        "academic_level": result.get("academic_level", result.get("academic_level_guess", "")),
        "pedagogical_role": result.get("pedagogical_role", result.get("pedagogical_role_guess", "")),
        "segment_count": result.get("segment_count", ""),
        "word_count_raw": result.get("word_count_raw", ""),
        "word_count_clean": result.get("word_count_clean", ""),
        "chunk_count": result.get("chunk_count", ""),
        "quality_flags": "|".join(flags) if isinstance(flags, list) else flags,
        "safe_for_tutor": result.get("safe_for_tutor", True),
        "safe_for_examiner": result.get("safe_for_examiner", False),
        "processed_at": result.get("processed_at", _utc_now()),
        "error_message": result.get("error_message", ""),
    }


def _write_batch_report(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        return
    existing = []
    if path.exists():
        with path.open("r", encoding="utf-8-sig", newline="") as file:
            existing = list(csv.DictReader(file))
    by_source = {row.get("source_filename", ""): row for row in existing if row.get("source_filename")}
    for row in rows:
        by_source[str(row.get("source_filename", ""))] = {
            column: row.get(column, "") for column in MANUAL_BATCH_COLUMNS
        }
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=MANUAL_BATCH_COLUMNS)
        writer.writeheader()
        writer.writerows(by_source.values())


def _error_result(path: Path, processed_at: str, exc: Exception) -> dict[str, Any]:
    classification = classify_filename(path.name)
    quality_flags = _metadata_quality_flags(classification)
    if str(exc) == "empty_srt" or (path.exists() and path.stat().st_size == 0):
        quality_flags.insert(0, "empty_srt")
    return {
        **classification,
        "safe_stem": safe_filename_stem(path.stem),
        "import_status": "error",
        "segment_count": 0,
        "word_count_raw": 0,
        "word_count_clean": 0,
        "chunk_count": 0,
        "quality_flags": quality_flags,
        "safe_for_tutor": True,
        "safe_for_examiner": False,
        "processed_at": processed_at,
        "error_message": _normalize_error_message(exc),
    }


def _write_error_report(root: Path, path: Path, result: dict[str, Any]) -> None:
    safe_stem = result.get("safe_stem") or safe_filename_stem(path.stem)
    report_path = root / "manual-import" / "reports" / f"{safe_stem}.manual_import_report.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def _normalize_error_message(message: object, max_length: int = 300) -> str:
    text = re.sub(r"[\r\n\t]+", " ", str(message or ""))
    text = re.sub(r"\s+", " ", text).strip()
    return f"{text[: max_length - 3]}..." if len(text) > max_length else text


def _utc_now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds")
