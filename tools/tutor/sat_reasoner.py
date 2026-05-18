"""Deterministic SAT observation reasoning helpers.

This module is intentionally standalone. It does not call Tutor rendering,
retrieval, orchestration, self-eval, external services, or write files.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

try:
    from tools.constants import EXAMINER_SCORING_ALLOWED, KNOWLEDGE_DIR, SAFE_FOR_EXAMINER
except ImportError:  # pragma: no cover - defensive fallback for direct file execution
    KNOWLEDGE_DIR = Path(__file__).resolve().parents[2] / "knowledge"
    SAFE_FOR_EXAMINER = False
    EXAMINER_SCORING_ALLOWED = False


ALIAS_TABLE_PATH = KNOWLEDGE_DIR / "config" / "sat_observation_aliases.json"

QUALITY_TIERS = ("outstanding", "very_good", "good", "acceptable", "poor")
TIER_LABELS_EN = {
    "outstanding": "outstanding",
    "very_good": "very good",
    "good": "good",
    "acceptable": "acceptable",
    "poor": "poor",
}
TIER_LABELS_ES = {
    "outstanding": "sobresaliente",
    "very_good": "muy buena",
    "good": "buena",
    "acceptable": "aceptable",
    "poor": "deficiente",
}

SAT_QUERY_TERMS = {
    "balance",
    "finish",
    "intensity",
    "complexity",
    "colour",
    "color",
    "nose",
    "palate",
    "condition",
    "development",
    "acidity",
    "tannin",
    "body",
    "alcohol",
    "length",
    "aroma",
    "bouquet",
    "equilibrio",
    "final",
    "intensidad",
    "complejidad",
    "nariz",
    "paladar",
    "condición",
    "desarrollo",
    "acidez",
    "tanino",
    "cuerpo",
    "longitud",
}

POSITIVE_SIGNALS = {
    ("acidity", "high"),
    ("complexity", "present"),
    ("complexity", "high"),
    ("finish", "medium(+)"),
    ("finish", "long"),
    ("intensity", "pronounced"),
    ("balance", "balanced"),
    ("condition", "clean"),
    ("development", "some development"),
    ("development", "fully developed"),
    ("body", "medium(+)"),
    ("body", "full"),
}

NEGATIVE_SIGNALS = {
    ("acidity", "low"),
    ("complexity", "absent"),
    ("finish", "short"),
    ("balance", "unbalanced"),
    ("condition", "faulty"),
    ("development", "past its best"),
    ("body", "light"),
}

AUTHORITY_TERMS = (
    "i grade",
    "i score",
    "mark",
    "award",
    "pass",
    "fail",
    "i certify",
)


def _load_alias_table() -> dict[str, Any]:
    return json.loads(ALIAS_TABLE_PATH.read_text(encoding="utf-8"))


def _normalise_text(text: str) -> str:
    return " ".join(str(text).casefold().split())


def _contains_term(text: str, term: str) -> bool:
    normalised_text = _normalise_text(text)
    normalised_term = _normalise_text(term)
    if not normalised_term:
        return False
    pattern = rf"(?<!\w){re.escape(normalised_term)}(?!\w)"
    return re.search(pattern, normalised_text) is not None


def _iter_aliases(alias_table: dict[str, Any]) -> list[tuple[str, str, str]]:
    aliases: list[tuple[str, str, str]] = []
    for parameter, config in alias_table.get("parameters", {}).items():
        for alias_key in ("aliases_es", "aliases_en"):
            for level, level_aliases in config.get(alias_key, {}).items():
                for alias in level_aliases:
                    aliases.append((str(parameter), str(level), str(alias)))
    aliases.sort(key=lambda row: len(_normalise_text(row[2])), reverse=True)
    return aliases


def is_sat_query(query: str, language: str) -> bool:
    """Return True when a query asks about SAT-style observations."""
    del language
    if not query:
        return False

    alias_table = _load_alias_table()
    for term in SAT_QUERY_TERMS:
        if _contains_term(query, term):
            return True
    for parameter in alias_table.get("parameters", {}):
        if _contains_term(query, parameter):
            return True
    return any(_contains_term(query, alias) for _, _, alias in _iter_aliases(alias_table))


def extract_sat_observations(
    query: str, language: str, alias_table: dict[str, Any] | None = None
) -> dict[str, str]:
    """Return canonical SAT observations detected through exact alias matches."""
    del language
    if not query:
        return {}

    table = alias_table if alias_table is not None else _load_alias_table()
    observations: dict[str, str] = {}
    for parameter, level, alias in _iter_aliases(table):
        if parameter not in observations and _contains_term(query, alias):
            observations[parameter] = level
    return observations


def score_quality_hypotheses(observations: dict[str, str]) -> dict[str, int]:
    """Score quality hypotheses deterministically with integer-only rules."""
    scores = {
        "outstanding": 4,
        "very_good": 5,
        "good": 5,
        "acceptable": 0,
        "poor": 0,
    }

    for parameter, level in sorted(observations.items()):
        signal = (parameter, level)
        if signal in POSITIVE_SIGNALS:
            scores["outstanding"] += 1
            scores["very_good"] += 1
            scores["good"] += 1
        elif signal in NEGATIVE_SIGNALS:
            scores["outstanding"] -= 1
            scores["very_good"] -= 1
            scores["good"] -= 1
            scores["acceptable"] += 1
            scores["poor"] += 1

    return {tier: max(0, min(10, score)) for tier, score in scores.items()}


def discard_invalid_hypotheses(scored: dict[str, int], observations: dict[str, str]) -> dict[str, int]:
    """Apply hard quality exclusions without mutating the input score dict."""
    surviving = {tier: max(0, min(10, int(scored.get(tier, 0)))) for tier in QUALITY_TIERS}
    values = {_normalise_text(value) for value in observations.values()}

    if "faulty" in values or "defectuoso" in values:
        surviving["outstanding"] = 0
        surviving["very_good"] = 0
    if observations.get("finish") == "short" or "final corto" in values:
        surviving["outstanding"] = 0
    if observations.get("balance") == "unbalanced" or "desequilibrado" in values:
        surviving["outstanding"] = 0
    return surviving


def _select_quality_tier(surviving_hypotheses: dict[str, int]) -> str:
    conservative_order = {
        "poor": 0,
        "acceptable": 1,
        "good": 2,
        "very_good": 3,
        "outstanding": 4,
    }
    return max(
        QUALITY_TIERS,
        key=lambda tier: (surviving_hypotheses.get(tier, 0), -conservative_order[tier]),
    )


def _evidence_phrase(observations: dict[str, str], language: str) -> str:
    if language.lower().startswith("es"):
        return ", ".join(f"{parameter}={level}" for parameter, level in sorted(observations.items()))
    return ", ".join(f"{parameter}={level}" for parameter, level in sorted(observations.items()))


def formulate_quality_assessment(
    observations: dict[str, str],
    surviving_hypotheses: dict[str, int],
    language: str,
    causal_chains: list[dict] | None = None,
) -> str:
    """Return a deterministic WSET-register quality assessment paragraph."""
    del causal_chains
    if not observations:
        if language.lower().startswith("es"):
            return "Observaciones insuficientes para evaluar la calidad."
        return "Insufficient observations to assess quality."

    tier = _select_quality_tier(surviving_hypotheses)
    evidence = _evidence_phrase(observations, language)

    if language.lower().startswith("es"):
        label = TIER_LABELS_ES[tier]
        return (
            f"El vino muestra características propias de una calidad {label}. "
            f"La evidencia apunta a una calidad {label} porque las observaciones SAT "
            f"({evidence}) se relacionan con balance, intensity, complexity y length "
            "en un registro WSET de calidad."
        )

    label = TIER_LABELS_EN[tier]
    return (
        f"The wine shows characteristics consistent with {label} quality. "
        f"The evidence suggests {label} quality because the SAT observations "
        f"({evidence}) relate to balance, intensity, complexity and length "
        "in a WSET quality-assessment register."
    )
