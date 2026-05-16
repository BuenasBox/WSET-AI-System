"""Build local Tutor-only chunks from official WSET markdown."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from tools.youtube_transcription.config import PROJECT_ROOT


DEFAULT_MARKDOWN_DIR = PROJECT_ROOT / "knowledge" / "official-wset" / "study-guide" / "wset_markdown"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "knowledge" / "official-wset" / "study-guide" / "official-chunks"
DEFAULT_JSONL_PATH = DEFAULT_OUTPUT_DIR / "official_wset_chunks.jsonl"
DEFAULT_REPORT_PATH = DEFAULT_OUTPUT_DIR / "official_wset_chunk_report.md"


def build_official_wset_chunks(
    markdown_dir: Path = DEFAULT_MARKDOWN_DIR,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
) -> dict[str, Any]:
    """Build deterministic text chunks from official markdown files."""
    chunks = load_official_markdown_chunks(markdown_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    jsonl_path = output_dir / "official_wset_chunks.jsonl"
    report_path = output_dir / "official_wset_chunk_report.md"
    with jsonl_path.open("w", encoding="utf-8") as file:
        for chunk in chunks:
            file.write(json.dumps(chunk, ensure_ascii=True) + "\n")
    report_path.write_text(_render_report(chunks, markdown_dir, jsonl_path), encoding="utf-8")
    return {
        "markdown_files_loaded": len({chunk["source_file"] for chunk in chunks}),
        "chunks_created": len(chunks),
        "jsonl_path": jsonl_path.as_posix(),
        "report_path": report_path.as_posix(),
        "sample_chunks": chunks[:3],
    }


def load_official_markdown_chunks(markdown_dir: Path = DEFAULT_MARKDOWN_DIR) -> list[dict[str, Any]]:
    """Read official markdown files and return Tutor-safe chunks."""
    chunks: list[dict[str, Any]] = []
    for path in sorted(markdown_dir.rglob("*.md"), key=lambda item: item.as_posix().lower()):
        metadata, body = _read_markdown(path)
        if not body.strip() or path.name.lower().startswith("readme"):
            continue
        title = str(metadata.get("title") or _first_heading(body) or path.stem.replace("_", " ").title())
        section = str(metadata.get("section") or _section_from_path(path))
        subtopic = str(metadata.get("subtopic") or metadata.get("topic") or title)
        parent_section = str(metadata.get("parent_section") or path.parent.name)
        source = str(metadata.get("source") or "WSET Level 3 Study Guide official markdown extraction")
        parts = _split_body(body)
        for index, text in enumerate(parts, start=1):
            chunk_id = _chunk_id(path, index)
            chunks.append(
                {
                    "chunk_id": chunk_id,
                    "text": text,
                    "source_type": "official_wset_extracted",
                    "source_trust_tier": 1,
                    "agent_corpus": "tutor",
                    "safe_for_tutor": True,
                    "safe_for_examiner": False,
                    "official_grading_authority": False,
                    "requires_human_review": True,
                    "source_file": _project_relative(path),
                    "source_filename": path.name,
                    "source": source,
                    "section": section,
                    "subtopic": subtopic,
                    "parent_section": parent_section,
                    "title": title,
                    "pedagogical_role": "official_reference",
                    "academic_level": "WSET_L3",
                    "retrieval_priority": "high",
                }
            )
    return chunks


def _read_markdown(path: Path) -> tuple[dict[str, Any], str]:
    text = path.read_text(encoding="utf-8-sig")
    if text.startswith("---"):
        match = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", text, flags=re.DOTALL)
        if match:
            return _parse_frontmatter(match.group(1)), match.group(2)
    return {}, text


def _parse_frontmatter(text: str) -> dict[str, Any]:
    metadata: dict[str, Any] = {}
    for line in text.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip().strip("'\"")
    return metadata


def _split_body(body: str, min_words: int = 250, max_words: int = 500) -> list[str]:
    blocks = _heading_blocks(body)
    chunks = []
    current: list[str] = []
    current_words = 0
    for block in blocks:
        words = _word_count(block)
        if current and current_words + words > max_words:
            chunks.append("\n\n".join(current).strip())
            current = []
            current_words = 0
        current.append(block)
        current_words += words
        if current_words >= min_words:
            chunks.append("\n\n".join(current).strip())
            current = []
            current_words = 0
    if current:
        chunks.append("\n\n".join(current).strip())
    return [chunk for chunk in chunks if _word_count(chunk) >= 20]


def _heading_blocks(body: str) -> list[str]:
    lines = body.splitlines()
    blocks = []
    current: list[str] = []
    for line in lines:
        if line.startswith("#") and current:
            blocks.append("\n".join(current).strip())
            current = [line]
        else:
            current.append(line)
    if current:
        blocks.append("\n".join(current).strip())
    return [block for block in blocks if block.strip()]


def _word_count(text: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", text))


def _first_heading(body: str) -> str:
    for line in body.splitlines():
        if line.startswith("#"):
            return line.lstrip("#").strip()
    return ""


def _section_from_path(path: Path) -> str:
    name = path.parent.name
    return re.sub(r"^seccion_\d+_", "", name).replace("_", " ").strip().title()


def _chunk_id(path: Path, index: int) -> str:
    stem = re.sub(r"[^A-Za-z0-9]+", "_", path.with_suffix("").as_posix())
    tail = "_".join(stem.split("_")[-8:])
    return f"OFFICIAL_WSET_{tail}_{index:03d}".upper()


def _project_relative(path: Path) -> str:
    try:
        return path.relative_to(PROJECT_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _render_report(chunks: list[dict[str, Any]], markdown_dir: Path, jsonl_path: Path) -> str:
    files = sorted({chunk["source_file"] for chunk in chunks})
    lines = [
        "# Official WSET Tutor Chunk Report",
        "",
        "Derived from local official markdown only. No PDFs were modified. No embeddings or vector database were created.",
        "",
        f"Markdown directory: {markdown_dir.as_posix()}",
        f"Output JSONL: {jsonl_path.as_posix()}",
        f"Markdown files loaded: {len(files)}",
        f"Chunks created: {len(chunks)}",
        "",
        "Governance: safe_for_examiner=false; official_grading_authority=false; agent_corpus=tutor.",
        "",
        "## Sample Chunks",
        "",
    ]
    for chunk in chunks[:5]:
        lines.append(f"- {chunk['chunk_id']} | {chunk['title']} | {chunk['section']}")
    return "\n".join(lines) + "\n"
