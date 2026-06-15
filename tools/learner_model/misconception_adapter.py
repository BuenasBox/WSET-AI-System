"""Read-only adapter for legacy misconception knowledge-map nodes."""

from __future__ import annotations

import json
import re
from copy import deepcopy
from pathlib import Path
from typing import Any, Iterable

from tools.constants import KNOWLEDGE_DIR

DEFAULT_MISCONCEPTION_DIR = KNOWLEDGE_DIR / "knowledge-map" / "misconceptions"
DETECTION_THRESHOLD = 0.45

_STOPWORDS = {
    "a", "an", "and", "are", "as", "because", "do", "does", "for", "from",
    "how", "i", "in", "is", "it", "its", "mean", "means", "of", "or",
    "right", "so", "the", "this", "to",
}
_EXPLANATORY_WORDS = {
    "affect", "affects", "causes", "explain", "how", "impact", "influence",
    "mechanism", "process", "relationship", "why",
}
_ASSERTION_WORDS = {"always", "bad", "green", "never", "thin", "underripe", "weak"}
_ASSERTION_PHRASES = {"low quality", "poor quality"}


def load_node_index(
    directory: Path = DEFAULT_MISCONCEPTION_DIR,
) -> dict[str, dict[str, Any]]:
    """Load the legacy nodes unchanged and index them by misconception ID."""
    index: dict[str, dict[str, Any]] = {}
    for path in sorted(directory.glob("*.json")):
        with path.open("r", encoding="utf-8") as file:
            node = json.load(file)
        if not isinstance(node, dict):
            continue
        mc_id = str(node.get("misconception_id") or "").strip()
        if mc_id:
            index[mc_id] = node
    return index


def normalize_node(node: dict[str, Any]) -> dict[str, Any]:
    """Return a derived consumer view without mutating the source node."""
    source = deepcopy(node)
    related_topics = _string_list(source.get("related_topics"))
    related_concepts = _string_list(source.get("related_concepts"))
    detection_signals = _string_list(source.get("detection_signals"))
    misconception = str(source.get("misconception") or "").strip()

    return {
        "misconception_id": str(source.get("misconception_id") or "").strip(),
        "source": source,
        "detection": {
            "canonical_statement": misconception,
            "signals": detection_signals,
            "keywords": deepcopy(source.get("detection_keywords") or []),
        },
        "weakness_relationships": {
            "topics": related_topics,
            "concepts": related_concepts,
            "requires_direct_evidence": True,
        },
        "recommendation_relationships": {
            "practice_topics": related_topics,
            "practice_concepts": related_concepts,
            "intervention": str(source.get("tutor_intervention") or "").strip(),
        },
        "governance": {
            "safe_for_examiner": False,
            "examiner_scoring_allowed": False,
            "uses_llm": False,
            "uses_embeddings": False,
            "uses_vector_db": False,
            "cloud_services_active": False,
            "formative_only": True,
        },
    }


def detect_text_evidence(
    text: str,
    *,
    explicit_id: str | None = None,
    candidate_ids: Iterable[str] | None = None,
    source_type: str = "tutor",
    directory: Path = DEFAULT_MISCONCEPTION_DIR,
) -> dict[str, Any]:
    """Detect direct misconception evidence from an ID or learner text."""
    index = load_node_index(directory)

    if explicit_id:
        mc_id = str(explicit_id).strip()
        if mc_id not in index:
            return _not_detected("unknown_misconception_id", source_type)
        return {
            "detected": True,
            "misconception_id": mc_id,
            "detection_method": "explicit_id",
            "source_type": source_type,
            "matched_signals": [],
            "match_strength": None,
        }

    normalized_text = _normalize(text)
    if not normalized_text:
        return _not_detected("no_evidence_text", source_type)

    allowed = set(candidate_ids) if candidate_ids is not None else set(index)
    scored: list[dict[str, Any]] = []
    for mc_id in sorted(allowed):
        node = index.get(mc_id)
        if node is None:
            continue
        row = _score_text(normalized_text, node)
        if row["match_strength"] >= DETECTION_THRESHOLD:
            scored.append(row)

    if not scored:
        return _not_detected("no_direct_match", source_type)

    best = max(
        scored,
        key=lambda row: (
            row["match_strength"],
            len(row["matched_signals"]),
            row["misconception_id"],
        ),
    )
    best["detected"] = True
    best["detection_method"] = "text_evidence"
    best["source_type"] = source_type
    return best


def _score_text(text: str, node: dict[str, Any]) -> dict[str, Any]:
    query_tokens = _tokens(text)
    phrases = [
        str(node.get("misconception") or ""),
        *_string_list(node.get("detection_signals")),
    ]
    matched: list[str] = []
    strength = 0.0

    for phrase in phrases:
        normalized_phrase = _normalize(phrase)
        phrase_tokens = _tokens(phrase)
        if not normalized_phrase or not phrase_tokens:
            continue
        overlap = len(query_tokens & phrase_tokens) / len(phrase_tokens)
        if overlap >= 0.35:
            matched.append(phrase)
        strength = max(strength, overlap * 0.75)
        if normalized_phrase in text or text in normalized_phrase:
            strength = max(strength, 0.9)

    strength += _keyword_bias(query_tokens, node.get("detection_keywords"))
    if _is_explanatory(text):
        strength -= 0.22

    return {
        "misconception_id": str(node.get("misconception_id") or ""),
        "matched_signals": matched[:3],
        "match_strength": round(max(0.0, min(strength, 0.99)), 2),
    }


def _keyword_bias(tokens: set[str], raw_keywords: Any) -> float:
    if not isinstance(raw_keywords, list) or not raw_keywords:
        return 0.0
    if isinstance(raw_keywords[0], dict):
        bias = 0.0
        for rule in raw_keywords:
            if not isinstance(rule, dict):
                continue
            rule_tokens = {str(item).lower() for item in rule.get("tokens", [])}
            if not rule_tokens:
                continue
            matched = (
                rule_tokens.issubset(tokens)
                if bool(rule.get("require_all"))
                else bool(rule_tokens & tokens)
            )
            if matched:
                bias += float(rule.get("bias", 0.1))
        return bias
    keyword_tokens = {str(item).lower() for item in raw_keywords}
    return 0.14 if keyword_tokens & tokens else 0.0


def _not_detected(reason: str, source_type: str) -> dict[str, Any]:
    return {
        "detected": False,
        "misconception_id": None,
        "detection_method": None,
        "source_type": source_type,
        "matched_signals": [],
        "match_strength": 0.0,
        "reason": reason,
    }


def _is_explanatory(text: str) -> bool:
    words = set(re.findall(r"[a-z]+", text))
    if not words & _EXPLANATORY_WORDS:
        return False
    has_assertion = bool(words & _ASSERTION_WORDS) or any(
        phrase in text for phrase in _ASSERTION_PHRASES
    )
    return not has_assertion


def _tokens(text: str) -> set[str]:
    tokens = {
        token
        for token in re.findall(r"[a-z0-9]+", _normalize(text))
        if token not in _STOPWORDS and len(token) > 1
    }
    if "acidic" in tokens:
        tokens.add("acidity")
    if "tannins" in tokens:
        tokens.add("tannin")
    if "underripe" in tokens:
        tokens.add("unripe")
    return tokens


def _normalize(text: Any) -> str:
    return re.sub(r"\s+", " ", str(text or "").lower()).strip()


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if str(item).strip()]
