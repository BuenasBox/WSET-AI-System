"""Index file writers for discovery-only metadata outputs."""

from __future__ import annotations

import csv
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path


DISCOVERED_COLUMNS = (
    "video_id",
    "video_title",
    "video_url",
    "channel_name",
    "duration",
    "upload_date",
    "playlist_ids",
    "playlist_titles",
    "playlist_urls",
    "playlist_positions",
)


def write_discovered_outputs(videos: list[dict], index_dir: Path) -> tuple[Path, Path]:
    """Write discovered video metadata to CSV and JSONL.

    Existing canonical files are backed up with a UTC timestamp before writing.
    """
    index_dir.mkdir(parents=True, exist_ok=True)
    csv_path = index_dir / "videos_discovered.csv"
    jsonl_path = index_dir / "videos_discovered.jsonl"

    _backup_if_exists(csv_path)
    _backup_if_exists(jsonl_path)

    sorted_videos = sorted(videos, key=lambda item: item.get("video_id", ""))
    _write_csv(sorted_videos, csv_path)
    _write_jsonl(sorted_videos, jsonl_path)
    return csv_path, jsonl_path


def _write_csv(videos: list[dict], path: Path) -> None:
    """Write flattened discovery records to CSV."""
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=DISCOVERED_COLUMNS)
        writer.writeheader()
        for video in videos:
            writer.writerow(_flatten_for_csv(video))


def _write_jsonl(videos: list[dict], path: Path) -> None:
    """Write full discovery records to JSONL."""
    with path.open("w", encoding="utf-8") as file:
        for video in videos:
            file.write(json.dumps(video, ensure_ascii=False) + "\n")


def _flatten_for_csv(video: dict) -> dict:
    """Flatten playlist membership fields for CSV output."""
    playlists = video.get("playlists", [])
    return {
        "video_id": video.get("video_id", ""),
        "video_title": video.get("video_title", ""),
        "video_url": video.get("video_url", ""),
        "channel_name": video.get("channel_name", ""),
        "duration": video.get("duration", ""),
        "upload_date": video.get("upload_date", ""),
        "playlist_ids": _join_values(playlists, "playlist_id"),
        "playlist_titles": _join_values(playlists, "playlist_title"),
        "playlist_urls": _join_values(playlists, "playlist_url"),
        "playlist_positions": _join_values(playlists, "playlist_position"),
    }


def _join_values(items: list[dict], key: str) -> str:
    """Join list values for stable CSV serialization."""
    return "; ".join(str(item.get(key, "")) for item in items if item.get(key) is not None)


def _backup_if_exists(path: Path) -> None:
    """Back up an existing output file before replacing it."""
    if not path.exists():
        return

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup_path = path.with_name(f"{path.stem}.{timestamp}.bak{path.suffix}")
    shutil.copy2(path, backup_path)
