"""Command entry point for the YouTube transcription pipeline scaffold.

This module only verifies local scaffold readiness. It does not process
playlists, call YouTube, download audio, run Whisper, or write transcripts.
"""

from .config import WINE_WITH_JIMMY_ROOT, ensure_directories, get_playlist_config_path
from .logger import configure_logging


def main() -> None:
    """Prepare local folders and report scaffold status."""
    ensure_directories()
    logger = configure_logging(WINE_WITH_JIMMY_ROOT / "logs")
    logger.info("YouTube transcription scaffold initialized.")
    logger.info("Playlist config path: %s", get_playlist_config_path())
    logger.info("No videos were processed. Pipeline implementation is pending.")


if __name__ == "__main__":
    main()
