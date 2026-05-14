"""Conservative local transcript cleaning utilities.

This module only reads existing local raw transcripts and metadata. It does not
fetch captions, call YouTube, run Whisper, summarize, or build embeddings.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


CLEANING_VERSION = "transcript_cleaning_v0.1"
QUALITY_FLAGS = (
    "possible_asr_error",
    "low_confidence_term",
    "noisy_caption",
    "incomplete_transcript",
    "language_mismatch",
    "possible_appellation_error",
)
CAPTION_ARTIFACT_RE = re.compile(
    r"^\s*\[(?:music|applause|laughter|sound|silence|foreign|inaudible)\]\s*$",
    re.IGNORECASE,
)
TIMESTAMPED_LINE_RE = re.compile(r"^\s*(\[\d{2}:\d{2}:\d{2}\])\s*(.*)$")
WORD_RE = re.compile(r"\b[\w'-]+\b", re.UNICODE)
SUSPICIOUS_ASR_TERMS = (
    "wct",
    "vtic",
    "vticulture",
    "desert likee",
    "great variety",
)
APPELLATION_SUSPECTS = (
    "barosa",
    "burgandy",
    "bugundy",
    "bordeauxx",
    "champagn",
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
    report_path: Path


def clean_one_video(video_id: str, root: Path) -> dict[str, Any]:
    """Clean one local transcript and write clean/chunk/report outputs."""
    paths = resolve_transcript_paths(video_id, root)
    raw_text = paths.raw_txt_path.read_text(encoding="utf-8")
    metadata = _read_json(paths.metadata_path)
    raw_json = _read_json(paths.raw_json_path) if paths.raw_json_path else {}

    raw_lines = _load_caption_lines(raw_text, raw_json)
    clean_lines, removed_artifacts, collapsed_duplicates = _clean_lines(raw_lines)
    quality_flags = _quality_flags(
        raw_text=raw_text,
        clean_lines=clean_lines,
        metadata=metadata,
        raw_json=raw_json,
        removed_artifacts=removed_artifacts,
        collapsed_duplicates=collapsed_duplicates,
    )
    clean_body = "\n".join(line for line in clean_lines if line).strip()
    raw_word_count = _word_count(raw_text)
    clean_word_count = _word_count(clean_body)
    processed_at = datetime.now(UTC).isoformat(timespec="seconds")

    cleaning_metadata = {
        "video_id": video_id,
        "source_raw_path": str(paths.raw_txt_path),
        "source_metadata_path": str(paths.metadata_path),
        "cleaning_version": CLEANING_VERSION,
        "processed_at": processed_at,
        "quality_flags": quality_flags,
        "word_count_raw": raw_word_count,
        "word_count_clean": clean_word_count,
    }
    report = {
        **cleaning_metadata,
        "output_clean_path": str(paths.clean_path),
        "output_chunk_ready_path": str(paths.chunk_ready_path),
        "report_path": str(paths.report_path),
        "removed_caption_artifact_lines": removed_artifacts,
        "collapsed_duplicate_fragments": collapsed_duplicates,
    }

    _ensure_output_directory(paths.clean_path.parent)
    _ensure_output_directory(paths.chunk_ready_path.parent)
    _ensure_output_directory(paths.report_path.parent)
    paths.clean_path.write_text(
        _render_clean_transcript(cleaning_metadata, clean_body),
        encoding="utf-8",
    )
    paths.chunk_ready_path.write_text(
        _render_chunk_ready_draft(cleaning_metadata, clean_body),
        encoding="utf-8",
    )
    paths.report_path.write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return report


def resolve_transcript_paths(video_id: str, root: Path) -> TranscriptPaths:
    """Resolve local raw, metadata, and output paths for a video ID."""
    raw_dir = root / "raw"
    metadata_dir = root / "metadata"
    metadata_path = metadata_dir / f"{video_id}.metadata.json"
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
        clean_path=root / "clean" / f"{base_name}.clean.txt",
        chunk_ready_path=root / "chunk-ready" / f"{base_name}.chunk-ready.txt",
        report_path=root / "reports" / f"{base_name}.cleaning-report.json",
    )


def clean_transcript(raw_text: str) -> str:
    """Return a conservatively cleaned transcript body."""
    clean_lines, _, _ = _clean_lines(_load_caption_lines(raw_text, {}))
    return "\n".join(clean_lines).strip()


def _load_caption_lines(raw_text: str, raw_json: dict[str, Any]) -> list[tuple[str, str]]:
    segments = raw_json.get("segments")
    if isinstance(segments, list) and segments:
        lines = []
        for segment in segments:
            if not isinstance(segment, dict):
                continue
            text = str(segment.get("text") or "")
            start = segment.get("start")
            timestamp = _format_timestamp(start) if isinstance(start, int | float) else ""
            lines.append((timestamp, text))
        if lines:
            return lines

    lines = []
    for raw_line in raw_text.splitlines():
        match = TIMESTAMPED_LINE_RE.match(raw_line)
        if match:
            lines.append((match.group(1), match.group(2)))
        else:
            lines.append(("", raw_line))
    return lines


def _clean_lines(lines: list[tuple[str, str]]) -> tuple[list[str], int, int]:
    clean_lines: list[str] = []
    removed_artifacts = 0
    collapsed_duplicates = 0
    previous_fragment = ""

    for timestamp, text in lines:
        normalized_text = _normalize_whitespace(text)
        if not normalized_text:
            continue
        if CAPTION_ARTIFACT_RE.match(normalized_text):
            removed_artifacts += 1
            continue

        comparison_fragment = _comparison_key(normalized_text)
        if comparison_fragment and comparison_fragment == previous_fragment:
            collapsed_duplicates += 1
            continue
        previous_fragment = comparison_fragment

        clean_lines.append(f"{timestamp} {normalized_text}".strip())

    return clean_lines, removed_artifacts, collapsed_duplicates


def _quality_flags(
    raw_text: str,
    clean_lines: list[str],
    metadata: dict[str, Any],
    raw_json: dict[str, Any],
    removed_artifacts: int,
    collapsed_duplicates: int,
) -> list[str]:
    flags = set()
    clean_text = "\n".join(clean_lines)
    lower_text = clean_text.lower()
    raw_word_count = _word_count(raw_text)
    clean_word_count = _word_count(clean_text)

    if removed_artifacts or collapsed_duplicates or re.search(r"\[[^\]]+\]", raw_text):
        flags.add("noisy_caption")
    if raw_word_count < 100 or clean_word_count < 100:
        flags.add("incomplete_transcript")
    language = (
        raw_json.get("language")
        or metadata.get("caption_language")
        or metadata.get("language_detected")
        or ""
    )
    if isinstance(language, str) and language and not language.lower().startswith("en"):
        flags.add("language_mismatch")
    if any(term in lower_text for term in SUSPICIOUS_ASR_TERMS):
        flags.add("possible_asr_error")
        flags.add("low_confidence_term")
    if any(term in lower_text for term in APPELLATION_SUSPECTS):
        flags.add("possible_appellation_error")

    return [flag for flag in QUALITY_FLAGS if flag in flags]


def _render_clean_transcript(metadata: dict[str, Any], body: str) -> str:
    return f"---\n{json.dumps(metadata, indent=2, ensure_ascii=False)}\n---\n\n{body}\n"


def _render_chunk_ready_draft(metadata: dict[str, Any], body: str) -> str:
    header = {
        "video_id": metadata["video_id"],
        "cleaning_version": metadata["cleaning_version"],
        "processed_at": metadata["processed_at"],
        "quality_flags": metadata["quality_flags"],
    }
    return f"---\n{json.dumps(header, indent=2, ensure_ascii=False)}\n---\n\n{body}\n"


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


def _format_timestamp(seconds: object) -> str:
    total_seconds = int(float(seconds))
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds_part = total_seconds % 60
    return f"[{hours:02d}:{minutes:02d}:{seconds_part:02d}]"


def _normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _comparison_key(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def _word_count(text: str) -> int:
    return len(WORD_RE.findall(text))
