"""CLI helper for writing the diagnostic SBA static demo payload.

Dynamic scanning: scans drafts/ and reviews/ subdirectories for all
*_drafts.json and *_review_records.json files, merging before filtering.
The legacy first_5_* files continue to work automatically.
Override with --drafts-dir to scan a different directory root.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from tools.question_generation.static_demo_exporter import (
    build_static_demo_export_payload,
    validate_static_demo_export_payload,
)

DEFAULT_DRAFTS_DIR = Path("knowledge/question-bank/diagnostic_sba")
TARGET_DIR = Path("frontend/diagnostic-sba")
TARGET_PATH = TARGET_DIR / "preguntas.json"
_DRAFTS_SUBDIR = "drafts"
_REVIEWS_SUBDIR = "reviews"


def load_json_list(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, list):
        raise ValueError(f"{path.as_posix()} must contain a JSON list")
    return data


def scan_and_merge(drafts_dir: Path) -> tuple[list[dict], list[dict]]:
    """Scan drafts_dir/drafts/ and drafts_dir/reviews/ for JSON list files."""
    drafts: list[dict] = []
    reviews: list[dict] = []

    drafts_subdir = drafts_dir / _DRAFTS_SUBDIR
    reviews_subdir = drafts_dir / _REVIEWS_SUBDIR

    if drafts_subdir.is_dir():
        for path in sorted(drafts_subdir.glob("*_drafts.json")):
            drafts.extend(load_json_list(path))

    if reviews_subdir.is_dir():
        for path in sorted(reviews_subdir.glob("*_review_records.json")):
            reviews.extend(load_json_list(path))

    return drafts, reviews


def build_payload(drafts_dir: Path) -> dict[str, Any]:
    drafts, reviews = scan_and_merge(drafts_dir)
    return build_static_demo_export_payload(drafts, reviews)


def assert_allowed_output_path(path: Path) -> Path:
    target_dir = TARGET_DIR.resolve()
    resolved = path.resolve()
    if resolved.parent != target_dir or resolved.name != TARGET_PATH.name:
        raise ValueError("output path must be frontend/diagnostic-sba/preguntas.json")
    return resolved


def format_summary(payload: dict[str, Any]) -> str:
    item_ids = [str(item["source_question_id"]) for item in payload.get("items", [])]
    validation_errors = validate_static_demo_export_payload(payload)
    return "\n".join([
        "export_version: " + str(payload.get("export_version")),
        "static_demo_only: " + str(payload.get("static_demo_only")),
        "eligible_item_count: " + str(len(item_ids)),
        "source_question_ids: " + ", ".join(item_ids),
        "validation_errors: " + str(len(validation_errors)),
        "target_path: " + TARGET_PATH.as_posix(),
    ])


def _cli() -> int:
    parser = argparse.ArgumentParser(
        description="Build the static demo diagnostic SBA export payload."
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Print a summary without writing files."
    )
    parser.add_argument(
        "--write", action="store_true",
        help="Write frontend/diagnostic-sba/preguntas.json."
    )
    parser.add_argument(
        "--output", default=TARGET_PATH.as_posix(),
        help="Must be frontend/diagnostic-sba/preguntas.json."
    )
    parser.add_argument(
        "--drafts-dir", default=DEFAULT_DRAFTS_DIR.as_posix(),
        help=(
            "Root directory containing drafts/ and reviews/ subdirectories. "
            "Default: knowledge/question-bank/diagnostic_sba/"
        ),
    )
    args = parser.parse_args()

    if args.write and args.dry_run:
        parser.error("--write and --dry-run are mutually exclusive")
    if not args.write and not args.dry_run:
        parser.error("choose --dry-run or --write")

    drafts_dir = Path(args.drafts_dir)
    output_path = assert_allowed_output_path(Path(args.output))
    payload = build_payload(drafts_dir)
    validation_errors = validate_static_demo_export_payload(payload)
    if validation_errors:
        raise ValueError(
            "static demo payload validation failed: " + "; ".join(validation_errors)
        )

    print(format_summary(payload))
    if args.write:
        output_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8"
        )
        print("wrote: " + output_path.as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(_cli())
