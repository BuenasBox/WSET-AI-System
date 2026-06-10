"""Distinction Coach payload exporter — Phase Y.1.

Compiles existing Phase X.1 assessment-intelligence assets into a single
static, learner-facing payload (``coach_data.js``) consumed by the
adaptive-session frontend. Pure read -> transform -> write; deterministic;
no LLM, no API, no network.

Sources (all existing knowledge assets — no new content is authored here):
- knowledge/sat-framework/sat_structure.json      -> section/element checklist
- knowledge/sat-framework/sat_scales.json         -> valid scale vocabulary
- knowledge/mentor-framework/mentor_hints.json    -> mentor hints by topic
- knowledge/command-verbs/*.json                  -> command-verb guidance
- knowledge/distinction-patterns/quality_reasoning_patterns.json
                                                  -> quality evidence framework

Governance: formative only. ``safe_for_examiner`` stays False. No marks are
assigned anywhere in the payload; structural guidance only.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
_KNOWLEDGE = REPO_ROOT / "knowledge"

SAT_STRUCTURE_PATH = _KNOWLEDGE / "sat-framework" / "sat_structure.json"
SAT_SCALES_PATH = _KNOWLEDGE / "sat-framework" / "sat_scales.json"
MENTOR_HINTS_PATH = _KNOWLEDGE / "mentor-framework" / "mentor_hints.json"
QUALITY_PATTERNS_PATH = (
    _KNOWLEDGE / "distinction-patterns" / "quality_reasoning_patterns.json"
)
COMMAND_VERB_DIR = _KNOWLEDGE / "command-verbs"
COMMAND_VERBS = ("describe", "explain", "compare", "assess", "evaluate", "justify")

DEFAULT_OUTPUT_PATH = REPO_ROOT / "frontend" / "adaptive-session" / "coach_data.js"
COACH_GLOBAL = "DISTINCTION_COACH"
SCHEMA_VERSION = "distinction_coach_v1"

GOVERNANCE = {
    "safe_for_examiner": False,
    "examiner_scoring_allowed": False,
    "formative_only": True,
    "uses_llm": False,
    "uses_api": False,
}

# Deterministic detection keyword maps for the client-side structural check.
# Keys are the official element names (Spanish) from sat_structure.json;
# values are lowercase substrings the learner's free text is scanned for.
SECTION_ALIASES: dict[str, list[str]] = {
    "aspecto": ["aspecto", "apariencia", "vista", "appearance"],
    "nariz": ["nariz", "nose", "aroma"],
    "boca": ["boca", "paladar", "palate"],
    "conclusiones": ["conclusion", "conclusiones", "calidad", "quality"],
}

PALATE_ELEMENT_ALIASES: dict[str, list[str]] = {
    "dulzor": ["dulzor", "dulce", "seco", "semiseco"],
    "acidez": ["acidez", "ácida", "acida"],
    "tanino": ["tanino", "táni", "tani"],
    "alcohol": ["alcohol"],
    "cuerpo": ["cuerpo"],
    "intensidad del sabor": ["intensidad"],
    "características del sabor": ["sabor", "fruta", "notas"],
    "final": ["final", "persistencia"],
}

JUSTIFICATION_CONNECTORS = [
    "porque",
    "ya que",
    "debido",
    "por lo tanto",
    "esto indica",
    "se debe a",
    "lo que sugiere",
]

SIMPLE_WINE_COACH_NOTE = (
    "Para vinos simples, indicar 'simple' es la observación correcta. "
    "No inventes aromas terciarios: en la clave oficial, declarar SIMPLE "
    "es lo que corresponde y los aromas primarios válidos completan la nota."
)


def _load(path: Path) -> dict[str, Any]:
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def _flatten_scales(scales: dict[str, Any]) -> dict[str, list[str]]:
    flat: dict[str, list[str]] = {}
    for section, elements in scales.items():
        for element, spec in elements.items():
            values = spec.get("values")
            if isinstance(values, list):
                flat[f"{section}.{element}"] = list(values)
    return flat


def build_coach_payload() -> dict[str, Any]:
    """Build the Distinction Coach payload from existing knowledge assets."""
    structure = _load(SAT_STRUCTURE_PATH)
    scales = _load(SAT_SCALES_PATH)
    hints = _load(MENTOR_HINTS_PATH)
    quality = _load(QUALITY_PATTERNS_PATH)

    sections = [
        {
            "id": sec.get("section_es", sec.get("section", "")),
            "section": sec.get("section", ""),
            "label": sec.get("section_es", ""),
            "elements": [e.get("element_es", "") for e in sec.get("elements", [])],
            "detect": SECTION_ALIASES.get(
                sec.get("section_es", ""), [sec.get("section_es", "")]
            ),
        }
        for sec in structure.get("sections", [])
    ]

    flat_scales = _flatten_scales(scales.get("scales", {}))

    command_verbs: dict[str, Any] = {}
    for verb in COMMAND_VERBS:
        data = _load(COMMAND_VERB_DIR / f"{verb}.json")
        command_verbs[verb] = {
            "definition": data.get("definition", ""),
            "do": data.get("expected_response", {}).get("do", []),
            "do_not": data.get("expected_response", {}).get("do_not", []),
            "mentor_hint": data.get("mentor_hint", ""),
        }

    framework = quality.get("quality_justification_framework", {})

    return {
        "schema_version": SCHEMA_VERSION,
        "source": "Phase X.1 assessment-intelligence assets (compiled)",
        "governance": dict(GOVERNANCE),
        "sat_sections": sections,
        "palate_element_detect": dict(PALATE_ELEMENT_ALIASES),
        "scales": flat_scales,
        "quality_terms": flat_scales.get("conclusions.quality_level", []),
        "readiness_terms": flat_scales.get("conclusions.readiness_for_drinking", []),
        "justification_connectors": list(JUSTIFICATION_CONNECTORS),
        "quality_principle": framework.get("principle", ""),
        "common_quality_errors": quality.get("common_quality_errors", []),
        "simple_wine_note": SIMPLE_WINE_COACH_NOTE,
        "mentor_hints": hints.get("hints_by_topic", {}),
        "command_verbs": command_verbs,
    }


def render_coach_js(payload: dict[str, Any]) -> str:
    body = json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2)
    return (
        "// Generated by tools/question_generation/distinction_coach_exporter.py\n"
        "// Compiled from knowledge/ assessment-intelligence assets. Do not edit.\n"
        "// Formative guidance only. safe_for_examiner=false.\n"
        f"window.{COACH_GLOBAL} = {body};\n"
    )


def export_coach_payload(output_path: Path | None = None) -> Path:
    target = output_path or DEFAULT_OUTPUT_PATH
    payload = build_coach_payload()
    if payload["governance"]["safe_for_examiner"] is not False:
        raise ValueError("Governance violation: safe_for_examiner must be False")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(render_coach_js(payload), encoding="utf-8")
    return target


if __name__ == "__main__":
    written = export_coach_payload()
    print(f"Distinction Coach payload written: {written}")
