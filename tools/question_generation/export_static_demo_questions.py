"""CLI helper for writing the diagnostic SBA static demo payload.

This script writes only ``frontend/diagnostic-sba/preguntas.json`` and only
when ``--write`` is supplied. It is intentionally narrow: no frontend HTML,
draft, review, source-bank, production-bank, retrieval, or schema writes.
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


DRAFTS_PATH = Path("knowledge/question-bank/diagnostic_sba/drafts/first_5_enrichment_drafts.json")
REVIEWS_PATH = Path("knowledge/question-bank/diagnostic_sba/reviews/first_5_human_review_records.json")
TARGET_DIR = Path("frontend/diagnostic-sba")
TARGET_PATH = TARGET_DIR / "preguntas.json"


def load_json_list(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, list):
        raise ValueError(f"{path.as_posix()} must contain a JSON list")
    return data


def build_payload() -> dict[str, Any]:
    drafts = load_json_list(DRAFTS_PATH)
    reviews = load_json_list(REVIEWS_PATH)
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
    return "\n".join(
        (
            f"export_version: {payload.get('export_version')}",
            f"static_demo_only: {payload.get('static_demo_only')}",
            f"eligible_item_count: {len(item_ids)}",
            f"source_question_ids: {', '.join(item_ids)}",
            f"validation_errors: {len(validation_errors)}",
            f"target_path: {TARGET_PATH.as_posix()}",
        )
    )


def _cli() -> int:
    parser = argparse.ArgumentParser(description="Build the static demo diagnostic SBA export payload.")
    parser.add_argument("--dry-run", action="store_true", help="Print a summary without writing files.")
    parser.add_argument("--write", action="store_true", help="Write frontend/diagnostic-sba/preguntas.json.")
    parser.add_argument("--output", default=TARGET_PATH.as_posix(), help="Must be frontend/diagnostic-sba/preguntas.json.")
    args = parser.parse_args()

    if args.write and args.dry_run:
        parser.error("--write and --dry-run are mutually exclusive")
    if not args.write and not args.dry_run:
        parser.error("choose --dry-run or --write")

    output_path = assert_allowed_output_path(Path(args.output))
    payload = build_payload()
    validation_errors = validate_static_demo_export_payload(payload)
    if validation_errors:
        raise ValueError("static demo payload validation failed: " + "; ".join(validation_errors))

    print(format_summary(payload))
    if args.write:
        output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("wrote: " + output_path.as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(_cli())
