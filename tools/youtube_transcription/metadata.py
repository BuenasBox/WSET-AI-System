"""Metadata writers for video transcript retrieval status."""

from __future__ import annotations

import json
from pathlib import Path


def build_video_metadata(video: dict, status: dict) -> dict:
    """Build a per-video metadata record for caption retrieval."""
    return {
        "video_id": video.get("video_id", ""),
        "video_title": video.get("video_title", ""),
        "video_url": video.get("video_url", ""),
        "playlist_ids": [
            playlist.get("playlist_id", "") for playlist in video.get("playlists", [])
        ],
        "playlist_names": [
            playlist.get("playlist_title", "") for playlist in video.get("playlists", [])
        ],
        "channel_name": video.get("channel_name", ""),
        "channel_url": video.get("channel_url", ""),
        "duration": video.get("duration", ""),
        "upload_date": video.get("upload_date", ""),
        "transcript_source": status.get("transcript_source", ""),
        "caption_language": status.get("language", ""),
        "language_detected": "",
        "topics_detected": [],
        "wset_learning_outcomes": [],
        "sat_topics": [],
        "contains_exam_tips": False,
        "contains_tasting_content": False,
        "contains_theory_content": False,
        "contains_cause_effect_reasoning": False,
        "processing_status": status.get("transcript_status", ""),
        "error_type": status.get("error_type", ""),
        "error_message": status.get("error_message", ""),
        "raw_json_path": status.get("raw_json_path", ""),
        "raw_txt_path": status.get("raw_txt_path", ""),
        "last_processed": status.get("last_processed", ""),
    }


def write_video_metadata(video: dict, status: dict, metadata_dir: Path) -> Path:
    """Write per-video metadata JSON."""
    metadata_dir.mkdir(parents=True, exist_ok=True)
    video_id = video.get("video_id", "")
    metadata_path = metadata_dir / f"{video_id}.metadata.json"
    payload = build_video_metadata(video, status)
    with metadata_path.open("w", encoding="utf-8") as file:
        json.dump(payload, file, ensure_ascii=False, indent=2)
    return metadata_path
