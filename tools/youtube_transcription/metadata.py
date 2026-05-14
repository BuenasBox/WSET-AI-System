"""Metadata writers for video transcript retrieval status.

Path portability contract
-------------------------
All file-path fields (``raw_json_path``, ``raw_txt_path``) stored in metadata
records MUST be project-relative POSIX strings, never absolute OS paths.

The caller is responsible for converting absolute Path objects to relative
strings before passing them in the ``status`` dict.  The canonical helper is
``_to_project_relative()`` in ``main.py``, which converts any path under
``PROJECT_ROOT`` to a POSIX-relative string.

Rationale: absolute paths are machine-specific and break reproducibility when
the project is cloned on a different machine or OS.
"""

from __future__ import annotations

import json
from pathlib import Path


def build_video_metadata(video: dict, status: dict) -> dict:
    """Build a per-video metadata record for caption retrieval.

    The ``raw_json_path`` and ``raw_txt_path`` values in ``status`` must be
    project-relative POSIX strings (e.g. ``knowledge/wine-with-jimmy/raw/xyz.raw.json``).
    Absolute paths are forbidden. See module docstring for the path portability contract.
    """
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
        # ----------------------------------------------------------------
        # Curriculum-level governance (Task 3 — added 2026-05-14)
        # ----------------------------------------------------------------
        # curriculum_level: classification of the video's WSET curriculum scope.
        # Valid values:
        #   "l3_eligible"   — content confirmed as appropriate for WSET Level 3 use
        #   "diploma_only"  — content is WSET Diploma (Level 4) only; must never
        #                     enter L3 Tutor Agent corpus without L3-downgrade annotation
        #   "mixed"         — video contains both L3 and Diploma content; requires
        #                     manual chunk-level review before ingestion
        #   "unclassified"  — not yet reviewed; default for all new records
        #
        # Governance rules:
        #   - Only "l3_eligible" records may enter the Tutor Agent corpus.
        #   - "diploma_only" and "mixed" records require explicit L3-downgrade
        #     annotation per trust-tier-matrix.json § diploma_content.
        #   - Classification must be performed by a human reviewer before any
        #     record is promoted to ingestion_status: "validated".
        #   - safe_for_examiner is ALWAYS False for Wine With Jimmy content
        #     regardless of curriculum_level. This is unconditional per
        #     trust-tier-matrix.json § wine_with_jimmy.
        "curriculum_level": status.get("curriculum_level", "unclassified"),
        "safe_for_examiner": False,
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
