"""Configuration helpers for the YouTube transcription pipeline.

This module only handles local configuration and folders. No network calls
belong here.
"""

import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
WINE_WITH_JIMMY_ROOT = PROJECT_ROOT / "knowledge" / "wine-with-jimmy"
PLAYLIST_CONFIG_PATH = WINE_WITH_JIMMY_ROOT / "config" / "playlists.json"

REQUIRED_DIRECTORIES = (
    WINE_WITH_JIMMY_ROOT / "raw",
    WINE_WITH_JIMMY_ROOT / "clean",
    WINE_WITH_JIMMY_ROOT / "audio",
    WINE_WITH_JIMMY_ROOT / "metadata",
    WINE_WITH_JIMMY_ROOT / "logs",
    WINE_WITH_JIMMY_ROOT / "config",
    WINE_WITH_JIMMY_ROOT / "index",
)


def ensure_directories() -> None:
    """Create the pipeline directory structure if it is missing."""
    for directory in REQUIRED_DIRECTORIES:
        directory.mkdir(parents=True, exist_ok=True)


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
