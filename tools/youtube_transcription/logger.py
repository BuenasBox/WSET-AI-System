"""Logging setup for the YouTube transcription pipeline."""

import logging
from pathlib import Path


def configure_logging(log_dir: Path) -> logging.Logger:
    """Configure a basic file and console logger for future pipeline runs."""
    log_dir.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("youtube_transcription")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()

    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s %(name)s %(message)s"
    )

    file_handler = logging.FileHandler(log_dir / "ingestion.log", encoding="utf-8")
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger
