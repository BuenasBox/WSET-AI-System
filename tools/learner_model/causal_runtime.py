"""Causal Chain Runtime Consumer — wires causal_chain_signals.json to the LES.

On each open response evaluation, detects which targeted CC_IDs are articulated in
the student response and updates the in-memory LES:

  - causal_chain_signals[cc_id].exposure_count   (incremented per targeted CC_ID)
  - causal_chain_signals[cc_id].demonstrated_count (incremented per articulated CC_ID)
  - causal_strength[cc_id]  — "superficial" | "developing" | "strong"

causal_strength is a runtime-extension top-level key.  It survives LES round-trips
because it is not overwritten by _with_governance_defaults normalization.

Emitted signals: causal_gap_detected, causal_chain_demonstrated, causal_strength_updated
"""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

from tools.constants import KNOWLEDGE_DIR

CAUSAL_SIGNALS_PATH = KNOWLEDGE_DIR / "knowledge-map" / "causal_chain_signals.json"
CAUSAL_CHAINS_DIR = KNOWLEDGE_DIR / "knowledge-map" / "causal-chains"

SIGNAL_GAP = "causal_gap_detected"
SIGNAL_DEMONSTRATED = "causal_chain_demonstrated"
SIGNAL_STRENGTH_UPDATED = "causal_strength_updated"

# Synonym expansion map for keyword derivation from CC_ID tokens (fallback path only).
# Used when a causal chain JSON does not supply trigger_keywords.
_TOKEN_SYNONYMS: dict[str, list[str]] = {
    "MLF": ["malolactic", "malic", "lactic", "mlf"],
    "ACIDITY": ["acidity", "acid", "acidic", "ph"],
    "COOL": ["cool", "cold"],
    "CLIMATE": ["climate", "region", "environment"],
    "OAK": ["oak", "barrel", "wood", "barriques"],
    "TANNIN": ["tannin", "astringency", "astringent", "polyphenol", "tannins"],
    "AGEABILITY": ["ageing", "aging", "age", "potential", "structure"],
    "BOTRYTIS": ["botrytis", "noble rot", "cinerea", "grey rot"],
    "AUTOLYSIS": ["autolysis", "autolytic", "yeast", "lees"],
    "LEES": ["lees", "sur lie", "autolysis"],
    "FLOR": ["flor", "biological", "yeast", "fino", "manzanilla"],
    "NOBLE": ["noble", "botrytis"],
    "ROT": ["rot", "botrytis", "noble"],
    "SUGAR": ["sugar", "sweetness", "residual"],
    "MACERATION": ["maceration", "extraction", "skin contact"],
    "DESTEMMING": ["destemming", "destem", "stems", "raspones"],
    "WHOLE": ["whole", "bunch", "cluster"],
    "BUNCH": ["bunch", "whole", "cluster"],
    "MICROOX": ["micro-oxygenation", "microoxygenation", "oxygen"],
    "TEXTURE": ["texture", "mouthfeel", "body"],
    "DIACETYL": ["diacetyl", "buttery", "butter", "cream"],
    "ALCOHOL": ["alcohol", "ethanol", "abv"],
    "AROMA": ["aroma", "primary", "fruit", "flavour", "flavor"],
    "FRACTIONAL": ["fractional", "solera", "blending"],
    "BLENDING": ["blending", "blend", "solera"],
    "FORTIFICATION": ["fortification", "fortified", "spirit", "brandy"],
    "SPRING": ["spring", "frost"],
    "FROST": ["frost", "freezing", "cold"],
    "TOPOGRAPHY": ["topography", "slope", "aspect"],
    "SOIL": ["soil", "drainage", "geology"],
    "DRAINAGE": ["drainage", "well-drained"],
    "VINE": ["vine", "vigour", "vigor"],
    "VIGOUR": ["vigour", "vigor", "growth", "canopy"],
    "MECHANICAL": ["mechanical", "machine", "harvest"],
    "HARVEST": ["harvest", "picking"],
    "OXIDATION": ["oxidation", "oxidative", "oxygen"],
    "SULPHITES": ["sulphites", "sulfites", "so2", "sulphur", "sulfur"],
    "PRESERVATION": ["preservation", "preserve", "protect"],
    "REDUCTION": ["reduction", "reduce", "lower"],
    "BOTTLE": ["bottle", "glass"],
    "SEDIMENT": ["sediment", "deposit", "throw"],
    "SAT": ["sat", "tasting", "standard"],
    "QUALITY": ["quality", "bicl", "balance", "intensity"],
    "CONCENTRATION": ["concentration", "concentrated", "dehydration"],
    "BARREL": ["barrel", "barrique", "cask", "wood"],
    "ASTRINGENCY": ["astringency", "astringent", "tannin", "grip"],
    "WARM": ["warm", "hot", "tropical"],
    "PH": ["ph", "acidity", "acid"],
}

_SIGNALS_CACHE: dict[str, Any] | None = None
_CC_FILES_CACHE: dict[str, dict] | None = None


def _load_signals(path: Path = CAUSAL_SIGNALS_PATH) -> dict[str, Any]:
    global _SIGNALS_CACHE
    if _SIGNALS_CACHE is None:
        with path.open("r", encoding="utf-8") as f:
            _SIGNALS_CACHE = json.load(f)
    return _SIGNALS_CACHE


def _load_cc_files(cc_dir: Path = CAUSAL_CHAINS_DIR) -> dict[str, dict]:
    """Load all CC JSON files into a dict keyed by normalized (uppercase) CC_ID."""
    global _CC_FILES_CACHE
    if _CC_FILES_CACHE is None:
        result: dict[str, dict] = {}
        if cc_dir.exists():
            for f in sorted(cc_dir.glob("*.json")):
                try:
                    data = json.loads(f.read_text(encoding="utf-8"))
                    # Prefer node_id (governance schema) then fall back to chain_id (legacy)
                    cc_id = str(data.get("node_id") or data.get("chain_id") or "").upper()
                    if cc_id:
                        result[cc_id] = data
                except Exception:
                    continue
        _CC_FILES_CACHE = result
    return _CC_FILES_CACHE


def known_cc_ids(signals_path: Path = CAUSAL_SIGNALS_PATH) -> frozenset[str]:
    """Return all CC_IDs registered in causal_chain_signals.json."""
    data = _load_signals(signals_path)
    return frozenset(c["cc_id"] for c in data.get("causal_chains", []))


def get_keyword_hints(cc_id: str, cc_dir: Path = CAUSAL_CHAINS_DIR) -> list[str]:
    """Return keyword hints for a CC_ID for deterministic text matching.

    Tries trigger_keywords from the CC JSON file first (governance / hybrid schema),
    then falls back to token-based derivation from the cc_id string itself.
    All hints are returned lowercased.
    """
    cc_files = _load_cc_files(cc_dir)
    data = cc_files.get(cc_id.upper(), {})
    raw_hints = data.get("trigger_keywords")
    if raw_hints and isinstance(raw_hints, list):
        return [str(kw).lower() for kw in raw_hints if kw]
    return _derive_from_id(cc_id)


def _derive_from_id(cc_id: str) -> list[str]:
    parts = cc_id.upper().split("_")
    if parts and parts[0] == "CC":
        parts = parts[1:]
    keywords: list[str] = []
    for part in parts:
        keywords.append(part.lower())
        keywords.extend(_TOKEN_SYNONYMS.get(part, []))
    return list(dict.fromkeys(keywords))


def detect_cc_coverage(
    student_response: str,
    cc_ids_targeted: list[str],
    cc_dir: Path = CAUSAL_CHAINS_DIR,
) -> tuple[list[str], list[str]]:
    """Detect which of cc_ids_targeted are articulated in student_response.

    Uses deterministic substring matching — no LLM, no embeddings.

    Returns:
        (chains_present, chains_absent) preserving the order of cc_ids_targeted.
    """
    response_lower = (student_response or "").lower()
    present: list[str] = []
    absent: list[str] = []
    for cc_id in cc_ids_targeted:
        hints = get_keyword_hints(cc_id, cc_dir)
        if _matches_any(response_lower, hints):
            present.append(cc_id)
        else:
            absent.append(cc_id)
    return present, absent


def _matches_any(response_lower: str, hints: list[str]) -> bool:
    return any(h.lower() in response_lower for h in hints if h)


def update_les_causal(
    les: dict[str, Any],
    *,
    cc_ids_targeted: list[str],
    chains_present: list[str],
    signals_path: Path = CAUSAL_SIGNALS_PATH,
    cc_dir: Path = CAUSAL_CHAINS_DIR,
) -> tuple[dict[str, Any], list[str]]:
    """Update the LES with causal chain coverage from an open response evaluation.

    Args:
        les: Current LES dict (not mutated — deep copy returned).
        cc_ids_targeted: CC_IDs the question expected the student to articulate.
        chains_present: CC_IDs detected as present in the student response.
        signals_path: Path override for causal_chain_signals.json (testing).
        cc_dir: Path override for CC JSON directory (testing).

    Returns:
        (updated_les, emitted_signals).  Writes nothing to disk.
    """
    valid_ids = known_cc_ids(signals_path)
    updated = deepcopy(les)
    emitted: list[str] = []

    cc_signals: dict[str, Any] = updated.setdefault("causal_chain_signals", {})
    causal_strength: dict[str, str] = updated.setdefault("causal_strength", {})

    for cc_id in cc_ids_targeted:
        if cc_id not in valid_ids:
            continue
        entry = cc_signals.get(
            cc_id,
            {"causal_chain_id": cc_id, "exposure_count": 0, "demonstrated_count": 0},
        )
        entry["causal_chain_id"] = cc_id
        entry["exposure_count"] = int(entry.get("exposure_count", 0)) + 1

        if cc_id in chains_present:
            entry["demonstrated_count"] = int(entry.get("demonstrated_count", 0)) + 1
            emitted.append(SIGNAL_DEMONSTRATED)
        else:
            emitted.append(SIGNAL_GAP)

        cc_signals[cc_id] = entry

        strength = _compute_strength(
            int(entry.get("demonstrated_count", 0)),
            int(entry.get("exposure_count", 0)),
        )
        old_strength = causal_strength.get(cc_id)
        causal_strength[cc_id] = strength
        if strength != old_strength:
            emitted.append(SIGNAL_STRENGTH_UPDATED)

    return updated, emitted


def _compute_strength(demonstrated: int, exposure: int) -> str:
    if exposure == 0:
        return "superficial"
    ratio = demonstrated / exposure
    if ratio >= 0.8:
        return "strong"
    if ratio >= 0.4:
        return "developing"
    return "superficial"
