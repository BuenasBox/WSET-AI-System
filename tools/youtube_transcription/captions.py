"""YouTube caption retrieval for discovered videos.

This module retrieves existing YouTube captions only. It does not download
audio or video, run Whisper, summarize, clean, or create embeddings.
"""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PREFERRED_LANGUAGES = ("en", "en-US", "en-GB")


def read_discovered_videos(path: Path) -> list[dict]:
    """Read discovered video records from JSONL."""
    videos: list[dict] = []
    with path.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                videos.append(json.loads(stripped))
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSONL at line {line_number}: {path}") from exc
    return videos


def fetch_captions(video_id: str) -> tuple[list[dict], str]:
    """Fetch timestamped captions for a video, preferring English."""
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
    except ImportError as exc:
        raise RuntimeError(
            "youtube-transcript-api is required for caption retrieval. "
            "Install dependencies from requirements.txt first."
        ) from exc

    if hasattr(YouTubeTranscriptApi, "get_transcript"):
        return _fetch_with_legacy_api(YouTubeTranscriptApi, video_id)

    api = YouTubeTranscriptApi()
    try:
        fetched = api.fetch(video_id, languages=list(PREFERRED_LANGUAGES))
        return _normalize_fetched_transcript(fetched, "en")
    except Exception:
        transcript_list = api.list(video_id)
        transcript = next(iter(transcript_list))
        fetched = transcript.fetch()
        language = getattr(transcript, "language_code", "") or ""
        return _normalize_fetched_transcript(fetched, language)


def build_raw_paths(video: dict, raw_dir: Path) -> tuple[Path, Path]:
    """Return raw JSON and TXT paths for a video."""
    safe_title = safe_filename(video.get("video_title") or "untitled")
    video_id = video.get("video_id", "")
    base_name = f"{video_id}__{safe_title}"
    return raw_dir / f"{base_name}.raw.json", raw_dir / f"{base_name}.raw.txt"


def save_raw_transcript(
    video: dict,
    segments: list[dict],
    language: str,
    raw_json_path: Path,
    raw_txt_path: Path,
) -> None:
    """Save raw transcript as timestamped JSON and TXT."""
    raw_json_path.parent.mkdir(parents=True, exist_ok=True)
    raw_txt_path.parent.mkdir(parents=True, exist_ok=True)

    payload = {
        "video_id": video.get("video_id", ""),
        "video_title": video.get("video_title", ""),
        "video_url": video.get("video_url", ""),
        "source": "youtube_caption",
        "language": language,
        "last_processed": utc_now(),
        "segments": segments,
    }

    with raw_json_path.open("w", encoding="utf-8") as file:
        json.dump(payload, file, ensure_ascii=False, indent=2)

    with raw_txt_path.open("w", encoding="utf-8") as file:
        for segment in segments:
            timestamp = format_timestamp(float(segment.get("start") or 0.0))
            text = str(segment.get("text") or "").replace("\n", " ").strip()
            file.write(f"[{timestamp}] {text}\n")


def safe_filename(value: str, max_length: int = 120) -> str:
    """Create a conservative Windows-safe filename component."""
    safe = re.sub(r'[<>:"/\\\\|?*]+', "", value)
    safe = re.sub(r"\s+", "_", safe.strip())
    safe = re.sub(r"_+", "_", safe)
    return (safe[:max_length].strip("._ ") or "untitled")


def format_timestamp(seconds: float) -> str:
    """Format seconds as HH:MM:SS."""
    seconds_int = max(0, int(seconds))
    hours, remainder = divmod(seconds_int, 3600)
    minutes, seconds_part = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds_part:02d}"


def utc_now() -> str:
    """Return current UTC timestamp in ISO 8601 format."""
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _normalize_segments(segments: list[Any]) -> list[dict]:
    """Normalize transcript segments from different API versions."""
    normalized = []
    for segment in segments:
        if isinstance(segment, dict):
            text = segment.get("text", "")
            start = segment.get("start", 0.0)
            duration = segment.get("duration", 0.0)
        else:
            text = getattr(segment, "text", "")
            start = getattr(segment, "start", 0.0)
            duration = getattr(segment, "duration", 0.0)

        normalized.append(
            {
                "start": float(start or 0.0),
                "duration": float(duration or 0.0),
                "text": str(text or ""),
            }
        )
    return normalized


def _detect_language_from_segments(segments: list[Any]) -> str:
    """Return language if the API segment payload exposes it."""
    for segment in segments:
        if isinstance(segment, dict) and segment.get("language"):
            return str(segment["language"])
    return ""


def _fetch_with_legacy_api(api: Any, video_id: str) -> tuple[list[dict], str]:
    """Fetch captions using older youtube-transcript-api versions."""
    try:
        segments = api.get_transcript(video_id, languages=list(PREFERRED_LANGUAGES))
        return _normalize_segments(segments), _detect_language_from_segments(segments) or "en"
    except Exception:
        transcript_list = api.list_transcripts(video_id)
        transcript = next(iter(transcript_list))
        fetched = transcript.fetch()
        language = getattr(transcript, "language_code", "") or ""
        return _normalize_segments(fetched), language


def _normalize_fetched_transcript(fetched: Any, default_language: str) -> tuple[list[dict], str]:
    """Normalize fetched transcript data from newer API versions."""
    if hasattr(fetched, "to_raw_data"):
        segments = fetched.to_raw_data()
    else:
        segments = list(fetched)

    language = getattr(fetched, "language_code", "") or default_language
    return _normalize_segments(segments), language
