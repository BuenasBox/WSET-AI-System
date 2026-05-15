"""Rule-based misconception pre-pass for Minimal Brain v1."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from tools.youtube_transcription.config import PROJECT_ROOT


DEFAULT_MISCONCEPTION_DIR = PROJECT_ROOT / "knowledge" / "knowledge-map" / "misconceptions"
STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "because",
    "climate",
    "cool",
    "do",
    "does",
    "for",
    "from",
    "how",
    "i",
    "in",
    "is",
    "it",
    "its",
    "mean",
    "means",
    "more",
    "of",
    "or",
    "right",
    "so",
    "the",
    "this",
    "to",
    "wine",
    "wines",
}


def load_misconception_nodes(directory: Path = DEFAULT_MISCONCEPTION_DIR) -> list[dict[str, Any]]:
    """Load misconception JSON nodes from the local knowledge map."""
    nodes: list[dict[str, Any]] = []
    for path in sorted(directory.glob("*.json")):
        with path.open("r", encoding="utf-8") as file:
            node = json.load(file)
        if not isinstance(node, dict):
            continue
        node["_source_path"] = path.as_posix()
        nodes.append(node)
    return nodes


def detect_misconception(
    query: str,
    directory: Path = DEFAULT_MISCONCEPTION_DIR,
) -> dict[str, Any]:
    """Return the highest-recall local misconception match for a student query."""
    nodes = load_misconception_nodes(directory)
    scored = [_score_node(query, node) for node in nodes]
    scored = [row for row in scored if row["confidence"] >= 0.45]
    if not scored:
        return {
            "detected": False,
            "matched_misconception_id": None,
            "confidence": 0.0,
            "severity": None,
            "intervention_type": None,
            "corrected_understanding": None,
            "matched_signals": [],
        }

    best = max(scored, key=lambda row: (row["confidence"], row["signal_overlap"], row["node_id"]))
    return {
        "detected": True,
        "matched_misconception_id": best["node_id"],
        "confidence": round(min(best["confidence"], 0.99), 2),
        "severity": best["severity"],
        "intervention_type": best["intervention_type"],
        "corrected_understanding": best["corrected_understanding"],
        "matched_signals": best["matched_signals"],
        "misconception": best["misconception"],
    }


def _score_node(query: str, node: dict[str, Any]) -> dict[str, Any]:
    query_tokens = _tokens(query)
    query_text = _normalize(query)
    signal_texts = [
        str(node.get("misconception", "")),
        *[str(signal) for signal in node.get("detection_signals", [])],
    ]
    matched_signals = []
    best_overlap = 0.0
    confidence = 0.0

    for signal in signal_texts:
        signal_tokens = _tokens(signal)
        if not signal_tokens:
            continue
        overlap_tokens = query_tokens & signal_tokens
        overlap = len(overlap_tokens) / len(signal_tokens)
        best_overlap = max(best_overlap, overlap)
        if overlap >= 0.35:
            matched_signals.append(signal)
        confidence = max(confidence, overlap * 0.75)
        if _normalize(signal) in query_text or query_text in _normalize(signal):
            confidence = max(confidence, 0.9)

    confidence += _concept_bias(query_tokens, query_text, node)
    return {
        "node_id": node.get("misconception_id", ""),
        "misconception": node.get("misconception", ""),
        "severity": node.get("severity"),
        "intervention_type": node.get("tutor_intervention"),
        "corrected_understanding": node.get("corrected_understanding"),
        "confidence": confidence,
        "signal_overlap": best_overlap,
        "matched_signals": matched_signals[:3],
    }


def _concept_bias(query_tokens: set[str], query_text: str, node: dict[str, Any]) -> float:
    node_id = str(node.get("misconception_id", ""))
    misconception_tokens = _tokens(str(node.get("misconception", "")))
    bias = 0.0
    if "always" in misconception_tokens and {"always", "never"} & query_tokens:
        bias += 0.1
    if node_id.startswith("MC_ACIDITY") and {"acid", "acidic", "acidity"} & query_tokens:
        bias += 0.14
    if node_id.startswith("MC_TANNIN") and {"tannin", "tannins", "tannic"} & query_tokens:
        bias += 0.14
    if node_id.startswith("MC_COOL_CLIMATE") and "cool climate" in query_text:
        bias += 0.18
    if node_id == "MC_COOL_CLIMATE_02" and {"unripe", "underripe", "green", "vegetal"} & query_tokens:
        bias += 0.3
    if (
        node_id == "MC_ACIDITY_01"
        and {"acid", "acidic", "acidity"} & query_tokens
        and {"quality", "lower", "poor", "unripe"} & query_tokens
    ):
        bias += 0.24
    if (
        node_id == "MC_TANNIN_01"
        and {"tannin", "tannins", "tannic"} & query_tokens
        and {"better", "quality", "bitter", "bitterness"} & query_tokens
    ):
        bias += 0.18
    return bias


def _tokens(text: str) -> set[str]:
    normalized = _normalize(text)
    raw_tokens = re.findall(r"[a-z0-9]+", normalized)
    tokens = {token for token in raw_tokens if token not in STOPWORDS and len(token) > 1}
    if "underripe" in tokens:
        tokens.add("unripe")
    if "acidic" in tokens:
        tokens.add("acidity")
    if "tannins" in tokens:
        tokens.add("tannin")
    return tokens


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", str(text or "").lower()).strip()
