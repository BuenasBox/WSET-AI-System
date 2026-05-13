"""Playlist metadata extraction for discovery-only dry runs.

This module uses yt-dlp only for metadata extraction. It must not download
videos, audio, captions, or transcripts.
"""

from __future__ import annotations

import logging
from typing import Any

from .config import load_playlist_config


def load_playlists(config_path=None) -> list[dict]:
    """Load playlist work items from config."""
    return load_playlist_config(config_path) if config_path else load_playlist_config()


def discover_playlist_videos(playlists: list[dict], logger: logging.Logger) -> list[dict]:
    """Discover video metadata for configured playlists using yt-dlp.

    The returned list is deduplicated by video_id and preserves playlist
    membership in the `playlists` field.
    """
    try:
        import yt_dlp
    except ImportError as exc:
        raise RuntimeError(
            "yt-dlp is required for dry-run metadata extraction. "
            "Install dependencies from requirements.txt first."
        ) from exc

    discovered: dict[str, dict] = {}
    ydl_options = {
        "extract_flat": "in_playlist",
        "ignoreerrors": True,
        "quiet": True,
        "skip_download": True,
    }

    with yt_dlp.YoutubeDL(ydl_options) as ydl:
        for configured_playlist in playlists:
            playlist_url = configured_playlist.get("playlist_url", "")
            logger.info("Discovering playlist metadata: %s", playlist_url)

            info = ydl.extract_info(playlist_url, download=False)
            if not info:
                logger.warning("No metadata returned for playlist: %s", playlist_url)
                continue

            playlist_id = str(info.get("id") or configured_playlist.get("playlist_id") or "")
            playlist_title = str(info.get("title") or configured_playlist.get("playlist_name") or "")
            channel_name = str(
                info.get("channel")
                or info.get("uploader")
                or configured_playlist.get("source_channel")
                or ""
            )
            entries = info.get("entries") or []
            logger.info(
                "Playlist discovered: id=%s title=%s entries=%s",
                playlist_id,
                playlist_title,
                len(entries),
            )

            for entry in entries:
                if not entry:
                    continue
                video = _build_video_record(
                    entry=entry,
                    playlist_id=playlist_id,
                    playlist_title=playlist_title,
                    playlist_url=playlist_url,
                    channel_name=channel_name,
                )
                video_id = video["video_id"]
                if not video_id:
                    logger.warning("Skipping entry without video_id in playlist %s", playlist_id)
                    continue

                if video_id not in discovered:
                    discovered[video_id] = video
                else:
                    _merge_playlist_membership(discovered[video_id], video["playlists"][0])

    return list(discovered.values())


def _build_video_record(
    entry: dict[str, Any],
    playlist_id: str,
    playlist_title: str,
    playlist_url: str,
    channel_name: str,
) -> dict:
    """Build a normalized video discovery record from yt-dlp data."""
    video_id = str(entry.get("id") or "")
    video_url = entry.get("url") or entry.get("webpage_url") or ""
    if video_id and not str(video_url).startswith("http"):
        video_url = f"https://www.youtube.com/watch?v={video_id}"

    membership = {
        "playlist_id": playlist_id,
        "playlist_title": playlist_title,
        "playlist_url": playlist_url,
        "playlist_position": entry.get("playlist_index"),
    }

    return {
        "video_id": video_id,
        "video_title": str(entry.get("title") or ""),
        "video_url": str(video_url),
        "duration": entry.get("duration"),
        "upload_date": entry.get("upload_date"),
        "channel_name": str(entry.get("channel") or entry.get("uploader") or channel_name),
        "playlists": [membership],
    }


def _merge_playlist_membership(existing_video: dict, playlist_membership: dict) -> None:
    """Append playlist membership if it is not already recorded."""
    playlist_id = playlist_membership.get("playlist_id")
    known_ids = {
        playlist.get("playlist_id") for playlist in existing_video.get("playlists", [])
    }
    if playlist_id not in known_ids:
        existing_video.setdefault("playlists", []).append(playlist_membership)
