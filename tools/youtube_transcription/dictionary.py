"""Read-only WSET canonical dictionary support for tutor enrichment."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DICTIONARY_JSONL = (
    ROOT
    / "knowledge"
    / "enrichment"
    / "wset_master_dictionary"
    / "consolidated"
    / "canonical_terms_master.jsonl"
)


@dataclass(frozen=True)
class DictionaryTerm:
    canonical_term: str
    category: str
    aliases: tuple[str, ...]
    confidence: str


@dataclass(frozen=True)
class DictionaryMatch:
    canonical_term: str
    category: str
    confidence: str
    matched_text: str
    match_type: str

    def as_dict(self) -> dict[str, str]:
        return {
            "canonical_term": self.canonical_term,
            "category": self.category,
            "confidence": self.confidence,
            "matched_text": self.matched_text,
            "match_type": self.match_type,
        }


class WsetDictionary:
    def __init__(self, terms: Iterable[DictionaryTerm], version: str) -> None:
        self.terms = tuple(terms)
        self.version = version

    @property
    def high_confidence_alias_corrections(self) -> tuple[tuple[str, str], ...]:
        corrections: list[tuple[str, str]] = []
        seen: set[tuple[str, str]] = set()
        for term in self.terms:
            if term.confidence != "high":
                continue
            for alias in term.aliases:
                if _comparison_key(alias) == _comparison_key(term.canonical_term):
                    continue
                pair = (alias, term.canonical_term)
                if pair not in seen:
                    seen.add(pair)
                    corrections.append(pair)
        return tuple(corrections)

    def find_matches(self, text: str) -> list[DictionaryMatch]:
        matches: list[DictionaryMatch] = []
        seen: set[tuple[str, str, str]] = set()
        for term in self.terms:
            candidates = [(term.canonical_term, "canonical")]
            candidates.extend((alias, "alias") for alias in term.aliases)
            for candidate, match_type in candidates:
                pattern = _term_pattern(candidate)
                if not pattern.search(text):
                    continue
                key = (term.canonical_term, term.category, candidate)
                if key in seen:
                    continue
                seen.add(key)
                matches.append(
                    DictionaryMatch(
                        canonical_term=term.canonical_term,
                        category=term.category,
                        confidence=term.confidence,
                        matched_text=candidate,
                        match_type=match_type,
                    )
                )
        return sorted(
            matches,
            key=lambda item: (item.category, item.canonical_term.casefold(), item.matched_text.casefold()),
        )


@lru_cache(maxsize=4)
def load_wset_dictionary(path: str | Path = DEFAULT_DICTIONARY_JSONL) -> WsetDictionary:
    dictionary_path = Path(path)
    if not dictionary_path.exists():
        return WsetDictionary(terms=(), version="missing")

    terms: list[DictionaryTerm] = []
    with dictionary_path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            record = json.loads(line)
            if _has_quality_flag(record, "needs_human_review"):
                continue
            canonical_term = _normalize_whitespace(record.get("canonical_term"))
            category = _normalize_whitespace(record.get("category"))
            confidence = _normalize_whitespace(record.get("confidence")).lower()
            if not canonical_term or not category:
                raise ValueError(f"Dictionary record missing canonical fields at line {line_number}")
            aliases = tuple(_unique(_normalize_whitespace(alias) for alias in record.get("aliases", [])))
            terms.append(
                DictionaryTerm(
                    canonical_term=canonical_term,
                    category=category,
                    aliases=aliases,
                    confidence=confidence or "low",
                )
            )

    return WsetDictionary(terms=terms, version=_dictionary_version(dictionary_path))


def summarize_matches(matches: list[DictionaryMatch]) -> dict[str, Any]:
    terms = _unique(match.canonical_term for match in matches)
    categories = _unique(match.category for match in matches)
    return {
        "canonical_terms_detected": terms,
        "dictionary_categories_detected": categories,
        "official_term_matches": [match.as_dict() for match in matches],
    }


def low_confidence_terms(matches: list[DictionaryMatch]) -> list[str]:
    return _unique(
        match.canonical_term for match in matches if match.confidence and match.confidence != "high"
    )


def _has_quality_flag(record: dict[str, Any], flag: str) -> bool:
    flags = record.get("quality_flags", [])
    if isinstance(flags, str):
        return flag in {item.strip() for item in flags.split(";")}
    if isinstance(flags, list):
        return flag in flags
    return False


def _dictionary_version(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return f"{path.name}:sha256:{digest.hexdigest()[:12]}"


def _term_pattern(term: str) -> re.Pattern[str]:
    escaped = re.escape(term).replace(r"\ ", r"\s+")
    return re.compile(r"(?<!\w)" + escaped + r"(?!\w)", re.IGNORECASE)


def _normalize_whitespace(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def _comparison_key(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def _unique(values: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    output: list[str] = []
    for value in values:
        if not value or value in seen:
            continue
        seen.add(value)
        output.append(value)
    return output
