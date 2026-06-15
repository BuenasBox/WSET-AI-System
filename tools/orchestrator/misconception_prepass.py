"""Rule-based misconception pre-pass for Minimal Brain v1."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from tools.learner_model.misconception_adapter import detect_text_evidence
from tools.youtube_transcription.config import PROJECT_ROOT


DEFAULT_MISCONCEPTION_DIR = PROJECT_ROOT / "knowledge" / "knowledge-map" / "misconceptions"
STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "because",
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
    "of",
    "or",
    "right",
    "so",
    "the",
    "this",
    "to",
}
# Domain terms removed from STOPWORDS (R07 fix):
# "cool", "climate", "wine", "wines" were removed because they are
# meaningful detection vocabulary for WSET L3 misconception queries.

# Explanatory-intent guard (R09 fix)
# Queries that are purely explanatory (how/why/affect framing) without asserting a
# misconception should not be routed as misconception interventions. This prevents
# false positives for theory questions whose lexical tokens happen to overlap with
# misconception signal vocabulary (e.g. "How does cool climate affect acidity?"
# contains "cool" + "climate" which triggers MC_COOL_CLIMATE_02).
EXPLANATORY_INTENT_WORDS: frozenset = frozenset({
    "how", "why", "affect", "affects", "affected", "explain", "explains",
    "explanation", "relationship", "influence", "influences", "impact",
    "impacts", "causes", "mechanism", "process", "leads",
})
MISCONCEPTION_FRAMING_WORDS: frozenset = frozenset({
    "always", "never", "underripe", "green", "herbaceous", "bad", "thin", "weak",
})
MISCONCEPTION_FRAMING_PHRASES: frozenset = frozenset({"low quality", "poor quality"})
# Confidence reduction applied to all nodes when query is identified as explanatory.
# Sized to suppress the worst observed false positive (confidence=0.48) to below
# the detection threshold (0.45) while leaving genuine misconception queries
# (which lack explanatory framing or carry framing markers) unaffected.
EXPLANATORY_PENALTY: float = 0.22


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
    result = detect_text_evidence(
        query,
        source_type="tutor",
        directory=directory,
    )
    if not result["detected"]:
        return {
            "detected": False,
            "matched_misconception_id": None,
            "confidence": 0.0,
            "severity": None,
            "intervention_type": None,
            "corrected_understanding": None,
            "matched_signals": [],
        }

    nodes = {
        str(node.get("misconception_id") or ""): node
        for node in load_misconception_nodes(directory)
    }
    node = nodes[result["misconception_id"]]
    return {
        "detected": True,
        "matched_misconception_id": result["misconception_id"],
        "confidence": result["match_strength"],
        "severity": node.get("severity"),
        "intervention_type": node.get("tutor_intervention"),
        "corrected_understanding": node.get("corrected_understanding"),
        "matched_signals": result["matched_signals"],
        "misconception": node.get("misconception"),
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
    if _is_explanatory_query(query):
        confidence -= EXPLANATORY_PENALTY
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
    """Data-driven concept bias — reads detection_keywords from the node file.

    Previously contained hardcoded references to specific node IDs (MC_ACIDITY_01,
    MC_TANNIN_01, MC_COOL_CLIMATE_02). This created a maintenance coupling where
    adding a new node did not automatically extend detection bias.

    Now: each misconception node may define a 'detection_keywords' list of objects:
      [{"tokens": ["acid", "quality"], "require_all": true, "bias": 0.24}, ...]

    Or a simpler flat list of token strings for basic category-level boosting:
      ["acid", "acidic", "acidity"]

    The node file is the single source of truth for detection behavior (R02 fix).
    """
    bias = 0.0
    misconception_tokens = _tokens(str(node.get("misconception", "")))

    # Universal: always/never pattern boost (applies to all nodes)
    if "always" in misconception_tokens and {"always", "never"} & query_tokens:
        bias += 0.1

    # Data-driven detection_keywords from node schema
    detection_keywords = node.get("detection_keywords", [])
    if not detection_keywords:
        # Backward compatibility: nodes without detection_keywords get no extra bias
        # (the old hardcoded ID-based logic is NOT reproduced here — it was the problem)
        return bias

    if isinstance(detection_keywords, list) and detection_keywords:
        first = detection_keywords[0]
        if isinstance(first, dict):
            # Structured form: [{"tokens": [...], "require_all": bool, "bias": float}]
            for rule in detection_keywords:
                if not isinstance(rule, dict):
                    continue
                rule_tokens = {str(t).lower() for t in rule.get("tokens", [])}
                rule_bias = float(rule.get("bias", 0.1))
                require_all = bool(rule.get("require_all", False))
                if require_all:
                    if rule_tokens and rule_tokens.issubset(query_tokens):
                        bias += rule_bias
                else:
                    if rule_tokens & query_tokens:
                        bias += rule_bias
        else:
            # Simple list of token strings — category-level boost
            kw_tokens = {str(kw).lower() for kw in detection_keywords}
            if kw_tokens & query_tokens:
                bias += 0.14

    return bias


def _is_explanatory_query(query: str) -> bool:
    """Return True when the query is framed as a theory/explanation question
    with no misconception-assertion markers.

    Examples that return True (explanatory, no framing — should NOT detect):
      "How does cool climate affect acidity?"
      "Why does flor protect the wine?"
      "Explain the relationship between tannin and astringency."

    Examples that return False (framing words present — SHOULD detect):
      "Cool climate always means underripe grapes."
      "Does high acidity mean poor quality?"  (no explanatory word)
      "Why does cool climate always produce green, herbaceous wines?"  (has "always")

    The check uses raw query text (not tokens) because key intent words
    such as "how" and "why" are in STOPWORDS and would be stripped before
    _tokens() is called.
    """
    query_lower = query.lower()
    query_words = set(re.findall(r"[a-z]+", query_lower))
    if not (query_words & EXPLANATORY_INTENT_WORDS):
        return False
    has_framing = bool(query_words & MISCONCEPTION_FRAMING_WORDS) or any(
        phrase in query_lower for phrase in MISCONCEPTION_FRAMING_PHRASES
    )
    return not has_framing


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
