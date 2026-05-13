"""Configuration helpers for the YouTube transcription pipeline.

Future implementation will load playlist configuration, validate settings, and
create required output folders. No network calls belong in this module.
"""

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
