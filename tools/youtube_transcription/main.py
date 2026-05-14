"""Command entry point for the YouTube transcription pipeline.

The current implemented command is discovery-only dry-run playlist metadata
extraction. It does not download videos, audio, captions, or transcripts.
"""

import argparse
import random
import re
import time

from .config import (
    DEFAULT_SLEEP_MAX_SECONDS,
    DEFAULT_SLEEP_MIN_SECONDS,
    RETRY_BACKOFF_SECONDS,
    RETRYABLE_ERROR_TYPES,
    WINE_WITH_JIMMY_ROOT,
    ensure_directories,
    get_playlist_config_path,
)
from .captions import (
    build_raw_paths,
    fetch_captions,
    read_discovered_videos,
    save_raw_transcript,
    utc_now,
)
from .cleaner import clean_batch, clean_one_video
from .indexer import (
    read_transcript_status_index,
    update_transcript_status_index,
    write_discovered_outputs,
)
from .logger import configure_logging
from .metadata import write_video_metadata
from .playlist_loader import discover_playlist_videos, load_playlists


def main() -> None:
    """Run the command-line interface."""
    parser = _build_parser()
    args = parser.parse_args()

    ensure_directories()

    if args.command == "clean-one":
        report = clean_one_video(args.video_id, WINE_WITH_JIMMY_ROOT, force=args.force)
        print("Clean-one complete.")
        print(f"Clean transcript: {report['output_clean_path']}")
        print(f"Chunk-ready JSONL: {report['output_chunk_ready_path']}")
        print(f"Enrichment metadata: {report['output_enrichment_path']}")
        print(f"Cleaning report: {report['report_path']}")
        print(f"Quality flags: {', '.join(report['quality_flags']) or 'none'}")
        return

    if args.command == "clean-batch":
        results = clean_batch(
            WINE_WITH_JIMMY_ROOT,
            limit=args.limit,
            dry_run=args.dry_run,
            force=args.force,
        )
        completed = sum(1 for result in results if result.get("clean_status") == "completed")
        dry_runs = sum(1 for result in results if result.get("clean_status") == "dry_run")
        errors = sum(1 for result in results if result.get("clean_status") == "error")
        print(
            "Clean-batch complete. "
            f"completed={completed} dry_run={dry_runs} errors={errors} "
            f"report={WINE_WITH_JIMMY_ROOT / 'reports' / 'cleaning_batch_report.csv'}"
        )
        return

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

    if args.command == "fetch-captions":
        discovered_path = WINE_WITH_JIMMY_ROOT / "index" / "videos_discovered.jsonl"
        videos = read_discovered_videos(discovered_path)
        if args.retry_failed_only:
            status_by_video_id = read_transcript_status_index(
                WINE_WITH_JIMMY_ROOT / "index"
            )
            failed_video_ids = {
                video_id
                for video_id, status in status_by_video_id.items()
                if status.get("transcript_status") == "failed"
            }
            videos = [
                video for video in videos if video.get("video_id") in failed_video_ids
            ]
        if args.limit:
            videos = videos[: args.limit]

        logger.info("Starting caption retrieval. Videos queued: %s", len(videos))
        totals = {"completed": 0, "failed": 0, "skipped": 0}
        status_path = WINE_WITH_JIMMY_ROOT / "index" / "transcript_status.csv"
        for index, video in enumerate(videos, start=1):
            status = _process_video_captions(
                video,
                force=args.force,
                logger=logger,
                sleep_min=args.sleep_min,
                sleep_max=args.sleep_max,
            )
            write_video_metadata(
                video,
                status,
                WINE_WITH_JIMMY_ROOT / "metadata",
            )
            status_path = update_transcript_status_index(
                [status],
                WINE_WITH_JIMMY_ROOT / "index",
            )
            transcript_status = status.get("transcript_status", "")
            if transcript_status in totals:
                totals[transcript_status] += 1
            remaining = len(videos) - index
            logger.info(
                "Progress: completed=%s failed=%s skipped=%s remaining=%s",
                totals["completed"],
                totals["failed"],
                totals["skipped"],
                remaining,
            )
        logger.info("Caption retrieval complete. Status index: %s", status_path)
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
    fetch_parser = subparsers.add_parser(
        "fetch-captions",
        help="Fetch existing YouTube captions for discovered videos.",
    )
    fetch_parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Process only the first N discovered videos.",
    )
    fetch_parser.add_argument(
        "--force",
        action="store_true",
        help="Refetch captions even when raw transcript files already exist.",
    )
    fetch_parser.add_argument(
        "--sleep-min",
        type=float,
        default=DEFAULT_SLEEP_MIN_SECONDS,
        help="Minimum seconds to sleep before caption requests.",
    )
    fetch_parser.add_argument(
        "--sleep-max",
        type=float,
        default=DEFAULT_SLEEP_MAX_SECONDS,
        help="Maximum seconds to sleep before caption requests.",
    )
    fetch_parser.add_argument(
        "--retry-failed-only",
        action="store_true",
        help="Process only videos currently marked failed in transcript_status.csv.",
    )
    clean_parser = subparsers.add_parser(
        "clean-one",
        help="Clean one existing local raw transcript without fetching or summarizing.",
    )
    clean_parser.add_argument(
        "--video-id",
        required=True,
        help="YouTube video ID for one existing local raw transcript.",
    )
    clean_parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite derived clean/chunk/enrichment/report outputs for this video.",
    )
    clean_batch_parser = subparsers.add_parser(
        "clean-batch",
        help="Clean a batch of existing completed/skipped local raw transcripts.",
    )
    clean_batch_parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Process only the first N processable transcripts.",
    )
    clean_batch_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="List/write batch report entries without creating per-video derived outputs.",
    )
    clean_batch_parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite derived outputs during real batch processing.",
    )
    return parser


def _process_video_captions(
    video: dict,
    force: bool,
    logger,
    sleep_min: float,
    sleep_max: float,
) -> dict:
    """Fetch and save captions for one video, returning a status row."""
    video_id = video.get("video_id", "")
    video_title = video.get("video_title", "")
    raw_json_path, raw_txt_path = build_raw_paths(video, WINE_WITH_JIMMY_ROOT / "raw")
    last_processed = utc_now()

    base_status = {
        "video_id": video_id,
        "video_title": video_title,
        "video_url": video.get("video_url", ""),
        "transcript_status": "pending",
        "transcript_source": "",
        "language": "",
        "raw_json_path": str(raw_json_path),
        "raw_txt_path": str(raw_txt_path),
        "error_type": "",
        "error_message": "",
        "last_processed": last_processed,
    }

    if raw_json_path.exists() and not force:
        logger.info("Skipping existing transcript: %s", video_id)
        return {
            **base_status,
            "transcript_status": "skipped",
            "transcript_source": "youtube_caption",
        }

    try:
        logger.info("Fetching captions: %s %s", video_id, video_title)
        segments, language = _fetch_captions_with_retries(
            video_id=video_id,
            logger=logger,
            sleep_min=sleep_min,
            sleep_max=sleep_max,
        )
        save_raw_transcript(video, segments, language, raw_json_path, raw_txt_path)
        logger.info("Caption saved: %s segments=%s language=%s", video_id, len(segments), language)
        return {
            **base_status,
            "transcript_status": "completed",
            "transcript_source": "youtube_caption",
            "language": language,
        }
    except Exception as exc:  # noqa: BLE001 - preserve batch progress on all API failures.
        error_type = _classify_caption_error(exc)
        raw_error_message = f"{type(exc).__name__}: {exc}"
        logger.exception("Caption retrieval failed for %s", video_id)
        _log_throttling_if_suspected(video_id, error_type, raw_error_message, logger)
        return {
            **base_status,
            "transcript_status": "failed",
            "transcript_source": "unavailable",
            "error_type": error_type,
            "error_message": _normalize_error_message(raw_error_message),
        }


def _fetch_captions_with_retries(
    video_id: str,
    logger,
    sleep_min: float,
    sleep_max: float,
) -> tuple[list[dict], str]:
    """Fetch captions sequentially with conservative pacing and retry backoff."""
    attempts_allowed = 1 + len(RETRY_BACKOFF_SECONDS)
    last_exception = None

    for attempt in range(1, attempts_allowed + 1):
        _sleep_before_request(video_id, sleep_min, sleep_max, logger)
        try:
            return fetch_captions(video_id)
        except Exception as exc:  # noqa: BLE001 - preserve retry control.
            last_exception = exc
            error_type = _classify_caption_error(exc)
            raw_error_message = f"{type(exc).__name__}: {exc}"
            logger.warning(
                "Caption attempt failed: video_id=%s attempt=%s/%s error_type=%s error=%s",
                video_id,
                attempt,
                attempts_allowed,
                error_type,
                _normalize_error_message(raw_error_message),
            )
            _log_throttling_if_suspected(video_id, error_type, raw_error_message, logger)

            if error_type not in RETRYABLE_ERROR_TYPES or attempt == attempts_allowed:
                raise

            backoff_seconds = RETRY_BACKOFF_SECONDS[attempt - 1]
            logger.info(
                "Retrying caption retrieval after %s seconds: video_id=%s",
                backoff_seconds,
                video_id,
            )
            time.sleep(backoff_seconds)

    raise last_exception or RuntimeError("Caption retrieval failed without exception.")


def _sleep_before_request(video_id: str, sleep_min: float, sleep_max: float, logger) -> None:
    """Sleep for a conservative random delay before a YouTube caption request."""
    minimum = max(0.0, sleep_min)
    maximum = max(minimum, sleep_max)
    delay = random.uniform(minimum, maximum)
    if delay <= 0:
        return
    logger.info("Sleeping %.2f seconds before request: video_id=%s", delay, video_id)
    time.sleep(delay)


def _normalize_error_message(message: object, max_length: int = 300) -> str:
    """Make an exception message single-line, readable, and CSV-safe."""
    text = str(message or "")
    text = re.sub(r"[\r\n\t]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) > max_length:
        return f"{text[: max_length - 3]}..."
    return text


def _classify_caption_error(exc: Exception) -> str:
    """Map caption exceptions to stable status categories."""
    haystack = f"{type(exc).__name__} {exc}".lower()

    if "disabled" in haystack:
        return "transcript_disabled"
    if "private" in haystack:
        return "private_video"
    if "age" in haystack and "restrict" in haystack:
        return "age_restricted"
    if "unavailable" in haystack or "deleted" in haystack:
        return "unavailable_video"
    if "no transcript" in haystack or "notranscript" in haystack:
        return "no_transcript_found"
    if "parse" in haystack or "json" in haystack or "decode" in haystack:
        return "parsing_error"
    if any(
        token in haystack
        for token in (
            "network",
            "connection",
            "timeout",
            "ssl",
            "http",
            "429",
            "rate",
            "throttle",
            "too many requests",
        )
    ):
        return "network_error"
    return "unknown_error"


def _log_throttling_if_suspected(
    video_id: str,
    error_type: str,
    raw_error_message: str,
    logger,
) -> None:
    """Log a clear warning when YouTube throttling appears likely."""
    haystack = raw_error_message.lower()
    if error_type == "network_error" and any(
        token in haystack
        for token in ("429", "rate", "throttle", "too many requests")
    ):
        logger.warning(
            "Possible YouTube throttling detected for %s. "
            "Use smaller batches or wider --sleep-min/--sleep-max values.",
            video_id,
        )


if __name__ == "__main__":
    main()
