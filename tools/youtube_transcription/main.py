"""Command entry point for the YouTube transcription pipeline.

The current implemented command is discovery-only dry-run playlist metadata
extraction. It does not download videos, audio, captions, or transcripts.
"""

import argparse

from .config import WINE_WITH_JIMMY_ROOT, ensure_directories, get_playlist_config_path
from .indexer import write_discovered_outputs
from .logger import configure_logging
from .playlist_loader import discover_playlist_videos, load_playlists


def main() -> None:
    """Run the command-line interface."""
    parser = _build_parser()
    args = parser.parse_args()

    ensure_directories()
    logger = configure_logging(WINE_WITH_JIMMY_ROOT / "logs")

    if args.command == "dry-run":
        playlists = load_playlists(get_playlist_config_path())
        logger.info("Starting dry-run metadata extraction.")
        logger.info("Playlist config path: %s", get_playlist_config_path())
        videos = discover_playlist_videos(playlists, logger)
        csv_path, jsonl_path = write_discovered_outputs(
            videos,
            WINE_WITH_JIMMY_ROOT / "index",
        )
        logger.info("Dry-run complete. Unique videos discovered: %s", len(videos))
        logger.info("CSV output: %s", csv_path)
        logger.info("JSONL output: %s", jsonl_path)
        return

    logger.info("YouTube transcription scaffold initialized.")
    logger.info("No videos were processed. Use the dry-run command for discovery.")


def _build_parser() -> argparse.ArgumentParser:
    """Build CLI parser."""
    parser = argparse.ArgumentParser(
        description="YouTube transcription ingestion pipeline tools."
    )
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser(
        "dry-run",
        help="Discover playlist/video metadata without downloading media or transcripts.",
    )
    return parser


if __name__ == "__main__":
    main()
