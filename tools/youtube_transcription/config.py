"""Configuration helpers for the YouTube transcription pipeline.

This module only handles local configuration and folders. No network calls
belong here.
"""

import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
WINE_WITH_JIMMY_ROOT = PROJECT_ROOT / "knowledge" / "wine-with-jimmy"
PLAYLIST_CONFIG_PATH = WINE_WITH_JIMMY_ROOT / "config" / "playlists.json"
DEFAULT_SLEEP_MIN_SECONDS = 2.0
DEFAULT_SLEEP_MAX_SECONDS = 5.0
RETRY_BACKOFF_SECONDS = (10, 30, 90)
RETRYABLE_ERROR_TYPES = ("network_error", "parsing_error")

REQUIRED_DIRECTORIES = (
    WINE_WITH_JIMMY_ROOT / "raw",
    WINE_WITH_JIMMY_ROOT / "clean",
    WINE_WITH_JIMMY_ROOT / "chunk-ready",
    WINE_WITH_JIMMY_ROOT / "enrichment-ready",
    WINE_WITH_JIMMY_ROOT / "reports",
    WINE_WITH_JIMMY_ROOT / "audio",
    WINE_WITH_JIMMY_ROOT / "metadata",
    WINE_WITH_JIMMY_ROOT / "logs",
    WINE_WITH_JIMMY_ROOT / "config",
    WINE_WITH_JIMMY_ROOT / "index",
)


def ensure_directories() -> None:
    """Create the pipeline directory structure if it is missing."""
    for directory in REQUIRED_DIRECTORIES:
        existed = directory.exists()
        directory.mkdir(parents=True, exist_ok=True)
        gitkeep_path = directory / ".gitkeep"
        if not existed and not gitkeep_path.exists():
            gitkeep_path.write_text("", encoding="utf-8")


def get_playlist_config_path() -> Path:
    """Return the default playlist configuration path."""
    return PLAYLIST_CONFIG_PATH


def load_playlist_config(config_path: Path = PLAYLIST_CONFIG_PATH) -> list[dict]:
    """Load playlist configuration records from JSON."""
    with config_path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, list):
        raise ValueError("Playlist config must contain a JSON list.")

    return data
