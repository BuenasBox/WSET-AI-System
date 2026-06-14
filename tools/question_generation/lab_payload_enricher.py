"""Phase P2.3: Enrich lab_payload.js with command verb and evaluation metadata.

Adds command_verb, expected_concepts, and evaluation_config to each OR item.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
COMMAND_VERBS_DIR = REPO_ROOT / "knowledge" / "command-verbs"
LAB_PAYLOAD_PATH = REPO_ROOT / "frontend" / "open-response-lab" / "lab_payload.js"


# Mapping of Spanish/English verb patterns to canonical verbs
VERB_DETECTION_PATTERNS = {
    "explain": [
        r"explica?(?:r|ción)?", r"cómo\s+\w+", r"explain", r"describe how"
    ],
    "justify": [
        r"justifi(?:ca|que)", r"justify", r"defien(?:de|da)"
    ],
    "assess": [
        r"valora?", r"assess", r"evalu(?:á|a)", r"rate"
    ],
    "compare": [
        r"compara?", r"contrasta?", r"compare", r"contrast"
    ],
    "describe": [
        r"describe", r"describ[ía]", r"caracteriz", r"distinguish"
    ],
    "evaluate": [
        r"evalú(?:a|e)", r"evaluate", r"analiz"
    ],
    "discuss": [
        r"discut(?:e|ir)", r"analiza?", r"examine?", r"discuss"
    ],
    "why": [
        r"\¿?por\s*(?:qué|que)", r"why", r"razón"
    ],
    "how": [
        r"cómo", r"how", r"manera"
    ],
    "outline": [
        r"esquem", r"resumen", r"outline", r"summarize"
    ],
    "state": [
        r"enuncia?", r"state", r"menciona?"
    ],
    "list": [
        r"list", r"enumera?", r"lista"
    ],
    "identify and explain": [
        r"identif(?:ica|y)\s+explica?", r"identify and explain"
    ],
}


def load_lab_payload_js(path: Path = LAB_PAYLOAD_PATH) -> dict:
    """Load lab_payload.js and extract the JavaScript object."""
    content = path.read_text(encoding="utf-8")
    # Extract JSON from: window.OPEN_RESPONSE_LAB_PAYLOAD = {...}
    match = re.search(r"window\.OPEN_RESPONSE_LAB_PAYLOAD\s*=\s*(\{.*?\});", content, re.DOTALL)
    if not match:
        raise ValueError("Could not find OPEN_RESPONSE_LAB_PAYLOAD in file")
    return json.loads(match.group(1))


def detect_command_verb(stem: str) -> str | None:
    """Detect the command verb from a question stem."""
    stem_lower = stem.lower()

    for verb, patterns in VERB_DETECTION_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, stem_lower):
                return verb

    return None


def load_all_command_verbs() -> dict[str, dict]:
    """Load all command verb definitions."""
    verbs = {}
    for verb_file in COMMAND_VERBS_DIR.glob("*.json"):
        if verb_file.name.startswith("."):
            continue
        verb_data = json.loads(verb_file.read_text(encoding="utf-8"))
        verb_name = verb_data.get("verb", verb_file.stem.replace("_", " "))
        verbs[verb_name] = verb_data
    return verbs


def extract_expected_concepts_from_stem(stem: str) -> list[str]:
    """Heuristically extract expected concepts from the stem.

    This is a simple approach; more sophisticated extraction would be needed
    for production use. For now, extract capitalized nouns and domain terms.
    """
    concepts = []

    # Common WSET concepts to look for
    wset_concepts = [
        "acidity", "tannin", "alcohol", "color", "aroma", "bouquet",
        "body", "ripening", "harvest", "fermentation", "oak", "climate",
        "altitude", "slope", "orientation", "sustainability", "organic",
        "biodynamic", "malolactic", "élevage", "blend", "terroir",
        "acidez", "tanino", "alcohol", "color", "aroma", "cuerpo",
        "maduración", "cosecha", "fermentación", "roble", "clima",
        "altitud", "pendiente", "orientación", "sostenibilidad", "orgánico",
        "biodinámico", "maloláctica", "crianza", "mezcla", "terroir",
    ]

    stem_lower = stem.lower()
    for concept in wset_concepts:
        if concept in stem_lower:
            concepts.append(concept)

    return concepts


def enrich_item(item: dict, command_verbs: dict[str, dict]) -> dict:
    """Add command_verb and evaluation_config to an item."""
    enriched = item.copy()

    stem = item.get("stem", "")
    detected_verb = detect_command_verb(stem)

    enriched["command_verb"] = detected_verb or "explain"
    enriched["expected_concepts"] = extract_expected_concepts_from_stem(stem)

    # Add evaluation config from verb definition
    verb_def = command_verbs.get(detected_verb or "explain", {})
    enriched["evaluation_config"] = {
        "verb_definition_key": detected_verb or "explain",
        "requires_causal_chain": "causal" in (verb_def.get("cognitive_level") or "").lower(),
        "structure_rules": verb_def.get("compliance_checks", {}).get("structure_rules", {}),
        "required_signals": verb_def.get("compliance_checks", {}).get("required_signals", []),
        "forbidden_signals": verb_def.get("compliance_checks", {}).get("forbidden_signals", []),
    }

    return enriched


def enrich_payload(payload: dict) -> dict:
    """Enrich all items in the payload."""
    enriched = payload.copy()
    command_verbs = load_all_command_verbs()

    enriched_items = []
    for item in payload.get("items", []):
        enriched_items.append(enrich_item(item, command_verbs))

    enriched["items"] = enriched_items
    enriched["evaluation_metadata"] = {
        "schema_version": "open_response_evaluation_v1",
        "command_verbs_loaded": list(command_verbs.keys()),
        "enrichment_timestamp": "phase_p2_3",
        "governance": {
            "safe_for_examiner": False,
            "examiner_scoring_allowed": False,
            "formative_only": True,
        }
    }

    return enriched


def save_enriched_payload(enriched_payload: dict, output_path: Path = LAB_PAYLOAD_PATH) -> None:
    """Save the enriched payload back to JavaScript."""
    js_code = f"window.OPEN_RESPONSE_LAB_PAYLOAD = {json.dumps(enriched_payload, indent=2)};\n"
    output_path.write_text(js_code, encoding="utf-8")


if __name__ == "__main__":
    payload = load_lab_payload_js()
    enriched = enrich_payload(payload)
    save_enriched_payload(enriched)
    print(f"[OK] Enriched {len(enriched['items'])} items with command verb and evaluation metadata")
    print(f"[OK] Command verbs loaded: {enriched['evaluation_metadata']['command_verbs_loaded']}")
