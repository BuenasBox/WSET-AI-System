"""Target selection for high-value Wine With Jimmy tutor ingestion.

This module uses local discovery/status metadata only. It does not call
YouTube, create embeddings, clean transcripts, or touch examiner logic.
"""

from __future__ import annotations

import csv
import json
import re
from pathlib import Path

from .captions import build_raw_paths


TARGET_COLUMNS = (
    "video_id",
    "video_title",
    "video_url",
    "playlist_names",
    "priority",
    "target_reason",
    "expected_pedagogical_role",
    "academic_level_guess",
    "transcript_status",
    "already_has_transcript",
    "recommended_for_targeted_fetch",
    "first_pass_l3_fetch_priority",
    "exclusion_reason",
)

PRIORITY_ORDER = {"S": 0, "A": 1, "B": 2, "C": 3}
MAX_RECOMMENDED_TARGETS = 30

S_PATTERNS = (
    ("mock exam", "mock exam practice"),
    ("tasting exam", "tasting exam preparation"),
    ("theory exam", "exam technique and theory exam preparation"),
    ("exam technique", "written answer technique"),
    ("exam tips", "exam strategy"),
    ("exam prep", "exam preparation"),
    ("exam practice", "exam practice"),
    ("exam answers", "answer structure practice"),
    ("example questions", "answer structure practice"),
    ("sample questions", "answer structure practice"),
    ("short written", "written answer technique"),
    ("written question", "written answer technique"),
    ("how to pass", "how to pass WSET guidance"),
    ("pass your wset", "how to pass WSET guidance"),
    ("common mistakes", "common mistakes"),
    ("distinction", "distinction tips"),
    ("timing strategy", "time management"),
    ("time management", "time management"),
    ("sat tasting", "SAT tasting guidance"),
    ("answer wset", "answer structure"),
    ("question breakdown", "answer structure"),
)

A_PATTERNS = (
    ("cause", "cause-effect reasoning"),
    ("effect", "cause-effect reasoning"),
    ("acidity", "structural component reasoning"),
    ("tannin", "structural component reasoning"),
    ("balance", "quality assessment"),
    ("complexity", "quality assessment"),
    ("quality", "quality assessment"),
    ("ageing", "readiness and ageing potential"),
    ("aging", "readiness and ageing potential"),
    ("climate", "climate and grape-growing reasoning"),
    ("weather", "climate and grape-growing reasoning"),
    ("viticulture", "viticulture"),
    ("grape growing", "viticulture"),
    ("grapegrowing", "viticulture"),
    ("vineyard", "viticulture"),
    ("winemaking", "winemaking choices"),
    ("wine making", "winemaking choices"),
    ("oak", "oak choices"),
    ("malolactic", "malolactic conversion"),
    ("lees", "lees ageing"),
    ("botrytis", "botrytis"),
    ("sparkling method", "sparkling method"),
    ("traditional method", "sparkling method"),
    ("fortified", "fortified method"),
    ("sherry", "fortified method"),
)

B_PATTERNS = (
    ("understanding", "broad theory explanation"),
    ("explained", "broad theory explanation"),
    ("study guide", "broad theory explanation"),
    ("region", "important region"),
    ("regions", "important region"),
    ("grape varieties", "important grape varieties"),
    ("grape variety", "important grape varieties"),
    ("grapes", "important grape varieties"),
    (" vs ", "regional or varietal comparison"),
    ("comparison", "regional comparison"),
)

LOW_VALUE_PATTERNS = (
    "travel",
    "release",
    "wine bar",
    "taste along",
    "top drops",
    "reviewed",
    "review",
)

FIRST_PASS_L3_PATTERNS = (
    "wset level 3",
    "wset l3",
    "level 3",
    "sat",
    "tasting exam",
    "mock exam question",
    "short written questions",
    "short written question",
    "working written question",
    "exam tips",
)

DIPLOMA_PATTERNS = (
    "diploma",
    "level 4",
    " d3",
    "d3 ",
    " mw",
)


def generate_high_value_targets(root: Path) -> tuple[Path, Path, list[dict]]:
    """Generate prioritized tutor target CSV/JSONL from local metadata."""
    index_dir = root / "index"
    config_dir = root / "config"
    config_dir.mkdir(parents=True, exist_ok=True)

    videos = _read_discovered_csv(index_dir / "videos_discovered.csv")
    status_by_video_id = _read_status_csv(index_dir / "transcript_status.csv")
    targets = build_high_value_targets(videos, status_by_video_id, root)

    csv_path = config_dir / "high_value_tutor_targets.csv"
    jsonl_path = config_dir / "high_value_tutor_targets.jsonl"
    _write_targets_csv(targets, csv_path)
    _write_targets_jsonl(targets, jsonl_path)
    return csv_path, jsonl_path, targets


def build_high_value_targets(
    videos: list[dict],
    status_by_video_id: dict[str, dict],
    root: Path,
) -> list[dict]:
    """Return sorted target rows with at most 30 fetch recommendations."""
    rows = []
    for video in videos:
        row = classify_video_title(video, status_by_video_id.get(video.get("video_id", ""), {}), root)
        rows.append(row)

    rows.sort(key=_target_sort_key)
    recommended_count = 0
    for row in rows:
        if recommended_count >= MAX_RECOMMENDED_TARGETS:
            row["recommended_for_targeted_fetch"] = "false"
            continue
        if _is_first_pass_l3_fetch_candidate(row):
            row["recommended_for_targeted_fetch"] = "true"
            recommended_count += 1
        else:
            row["recommended_for_targeted_fetch"] = "false"
    return rows


def classify_video_title(video: dict, status: dict, root: Path) -> dict:
    """Classify one video by title only, adding local status fields."""
    title = str(video.get("video_title", "") or "")
    priority, reason = _classify_priority(title)
    role = _expected_role(priority, reason)
    transcript_status = str(status.get("transcript_status", "") or "")
    error_type = str(status.get("error_type", "") or "")
    already_has_transcript = _already_has_transcript(video, status, root)
    academic_level_guess = _guess_academic_level(title)
    first_pass_l3 = _is_l3_first_pass_title(title, academic_level_guess)
    exclusion_reason = _exclusion_reason(
        title=title,
        transcript_status=transcript_status,
        error_type=error_type,
        already_has_transcript=already_has_transcript,
        first_pass_l3=first_pass_l3,
        priority=priority,
        academic_level_guess=academic_level_guess,
    )

    return {
        "video_id": str(video.get("video_id", "") or ""),
        "video_title": title,
        "video_url": str(video.get("video_url", "") or ""),
        "playlist_names": str(
            video.get("playlist_names")
            or video.get("playlist_titles")
            or _playlist_names_from_jsonl_record(video)
        ),
        "priority": priority,
        "target_reason": reason,
        "expected_pedagogical_role": role,
        "academic_level_guess": academic_level_guess,
        "transcript_status": transcript_status or error_type or "unknown",
        "already_has_transcript": _bool_text(already_has_transcript),
        "recommended_for_targeted_fetch": "false",
        "first_pass_l3_fetch_priority": _bool_text(first_pass_l3 and not exclusion_reason),
        "exclusion_reason": exclusion_reason,
    }


def read_high_value_targets(path: Path) -> list[dict]:
    """Read the high-value target CSV."""
    with path.open("r", encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def target_row_to_video(row: dict) -> dict:
    """Convert a target CSV row to the video shape used by caption fetching."""
    return {
        "video_id": row.get("video_id", ""),
        "video_title": row.get("video_title", ""),
        "video_url": row.get("video_url", ""),
        "playlists": [
            {"playlist_title": item.strip()}
            for item in str(row.get("playlist_names", "")).split(";")
            if item.strip()
        ],
    }


def is_truthy_text(value: object) -> bool:
    """Return True for stable CSV boolean strings."""
    return str(value or "").strip().lower() in {"true", "1", "yes", "y"}


def _classify_priority(title: str) -> tuple[str, str]:
    title_lower = _normalize_title(title)
    for pattern, reason in S_PATTERNS:
        if pattern in title_lower:
            return "S", reason
    for pattern, reason in A_PATTERNS:
        if pattern in title_lower:
            return "A", reason
    for pattern, reason in B_PATTERNS:
        if pattern in title_lower:
            return "B", reason
    if any(pattern in title_lower for pattern in LOW_VALUE_PATTERNS):
        return "C", "general wine culture or promotional/lifestyle content"
    return "C", "narrow regional or varietal content"


def _expected_role(priority: str, reason: str) -> str:
    if priority == "S":
        if "tasting" in reason.lower() or "sat" in reason.lower():
            return "tasting_exam_guidance"
        return "exam_strategy"
    if priority == "A":
        if "quality" in reason.lower() or "ageing" in reason.lower():
            return "quality_assessment_reasoning"
        return "cause_effect_theory_explanation"
    if priority == "B":
        return "regional_or_varietal_theory_explanation"
    return "low_priority_context"


def _guess_academic_level(title: str) -> str:
    title_lower = _normalize_title(title)
    has_l3 = any(token in title_lower for token in ("level 3", " l3", "wset 3"))
    has_diploma = _has_diploma_signal(title)
    if has_l3 and has_diploma:
        return "MIXED"
    if has_diploma:
        return "WSET_DIPLOMA"
    if has_l3:
        return "WSET_L3"
    if "wset" in title_lower:
        return "MIXED"
    return "UNKNOWN"


def _already_has_transcript(video: dict, status: dict, root: Path) -> bool:
    if status.get("transcript_status") in {"completed", "skipped"}:
        return True
    raw_json_path = status.get("raw_json_path")
    if raw_json_path and Path(raw_json_path).exists():
        return True
    fallback_json_path, _ = build_raw_paths(video, root / "raw")
    return fallback_json_path.exists()


def _is_first_pass_l3_fetch_candidate(row: dict) -> bool:
    if not is_truthy_text(row.get("first_pass_l3_fetch_priority")):
        return False
    if row.get("exclusion_reason"):
        return False
    if row.get("priority") not in {"S", "A", "B"}:
        return False
    if row.get("academic_level_guess") == "WSET_DIPLOMA":
        return False
    return True


def _target_sort_key(row: dict) -> tuple[int, int, int, int, str]:
    first_pass_penalty = (
        0
        if is_truthy_text(row.get("first_pass_l3_fetch_priority"))
        and not row.get("exclusion_reason")
        else 1
    )
    diploma_penalty = 1 if row.get("academic_level_guess") in {"WSET_DIPLOMA", "MIXED"} else 0
    has_transcript_penalty = 1 if is_truthy_text(row.get("already_has_transcript")) else 0
    return (
        first_pass_penalty,
        PRIORITY_ORDER.get(row.get("priority", "C"), 99),
        diploma_penalty,
        has_transcript_penalty,
        row.get("video_title", "").lower(),
    )


def _is_l3_first_pass_title(title: str, academic_level_guess: str) -> bool:
    if academic_level_guess == "WSET_DIPLOMA":
        return False
    title_lower = _normalize_title(title)
    if _has_diploma_signal(title):
        return False
    return any(pattern in title_lower for pattern in FIRST_PASS_L3_PATTERNS)


def _exclusion_reason(
    title: str,
    transcript_status: str,
    error_type: str,
    already_has_transcript: bool,
    first_pass_l3: bool,
    priority: str,
    academic_level_guess: str,
) -> str:
    status_text = f"{transcript_status} {error_type}".lower()
    if academic_level_guess in {"WSET_DIPLOMA", "MIXED"} and _has_diploma_signal(title):
        return "diploma_level_content"
    if already_has_transcript:
        return "already_has_transcript"
    if "private" in status_text or "transcript_disabled" in status_text:
        return "private_or_disabled"
    if "[private video]" in title.lower():
        return "private_or_disabled"
    if priority == "C" or not first_pass_l3:
        return "low_pedagogical_value"
    return ""


def _has_diploma_signal(title: str) -> bool:
    title_lower = f" {_normalize_title(title)} "
    return any(pattern in title_lower for pattern in DIPLOMA_PATTERNS)


def _read_discovered_csv(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def _read_status_csv(path: Path) -> dict[str, dict]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8", newline="") as file:
        return {
            row.get("video_id", ""): row
            for row in csv.DictReader(file)
            if row.get("video_id")
        }


def _write_targets_csv(rows: list[dict], path: Path) -> None:
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=TARGET_COLUMNS)
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in TARGET_COLUMNS})


def _write_targets_jsonl(rows: list[dict], path: Path) -> None:
    with path.open("w", encoding="utf-8") as file:
        for row in rows:
            file.write(json.dumps(row, ensure_ascii=False) + "\n")


def _playlist_names_from_jsonl_record(video: dict) -> str:
    return "; ".join(
        str(item.get("playlist_title", ""))
        for item in video.get("playlists", [])
        if item.get("playlist_title")
    )


def _normalize_title(title: str) -> str:
    return re.sub(r"\s+", " ", title.lower()).strip()


def _bool_text(value: bool) -> str:
    return "true" if value else "false"
