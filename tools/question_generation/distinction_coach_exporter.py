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



# ---------------------------------------------------------------------------
# Phase Z.2 localization guard -- learner-facing output MUST be Spanish.
#
# The knowledge/ source assets keep their original English text (they are
# shared analysis assets). The exporter owns the Spanish learner-facing layer.
# STRICT RULE: every command verb and every mentor-hint topic present in the
# sources must have a Spanish override below; export_coach_payload() raises if
# one is missing, so English can never silently reach coach_data.js again.
# ---------------------------------------------------------------------------

ES_COMMAND_VERBS: dict[str, dict[str, Any]] = {
    "assess": {
        "definition": "Emite un juicio fundamentado sobre el valor, la calidad o la relevancia de algo, basándote en criterios establecidos.",
        "do": ["Declara un juicio claro", "Apóyalo con evidencia específica de cata o de región", "Usa criterios WSET apropiados"],
        "do_not": ["Dar una opinión sin respaldo", "Enumerar observaciones sin conclusión"],
        "mentor_hint": "Empieza por tu juicio («Este vino es de calidad excelente») y aporta de inmediato 3 o más observaciones específicas que lo respalden. No dejes la conclusión para el final.",
    },
    "compare": {
        "definition": "Identifica semejanzas y diferencias entre dos o más elementos. Se esperan semejanzas Y diferencias salvo que se indique lo contrario.",
        "do": ["Aborda semejanzas y diferencias", "Usa estructura paralela para mayor claridad", "Cubre varias dimensiones"],
        "do_not": ["Describir cada elemento por separado sin vincularlos", "Cubrir solo un elemento en detalle"],
        "mentor_hint": "Organiza por dimensión: «En cuanto al clima, X es [fresco/cálido] mientras que Y es [fresco/cálido]…». No escribas un ensayo sobre X y luego otro sobre Y.",
    },
    "describe": {
        "definition": "Enuncia las características, rasgos o apariencia de algo. No expliques causas ni razones.",
        "do": ["Nombra características", "Usa vocabulario SAT (en preguntas de cata)", "Sé específico/a", "Cubre todas las dimensiones relevantes"],
        "do_not": ["Explicar por qué", "Dar opiniones", "Comparar con otros ejemplos", "Añadir causas o mecanismos"],
        "mentor_hint": "Responde solo al «qué». Si te sorprendes escribiendo «porque» o «esto significa», estás explicando, no describiendo.",
    },
    "evaluate": {
        "definition": "Emite un juicio fundamentado, sopesando la relevancia de la evidencia. Suele implicar una consideración más amplia o matizada que «assess».",
        "do": ["Sopesa varias piezas de evidencia", "Declara una conclusión clara", "Reconoce la complejidad cuando sea relevante"],
        "do_not": ["Limitarte a enumerar hechos (eso es describir)", "Dar opinión sin evidencia"],
        "mentor_hint": "Piensa en «evaluar» como «explicar + juzgar»: explica los factores clave y luego indica cuál consideras más significativo y por qué.",
    },
    "explain": {
        "definition": "Da razones o justifica un hecho, fenómeno o resultado. Debe incluir una relación causa-efecto.",
        "do": ["Indica la causa", "Indica el mecanismo o proceso", "Indica el resultado o efecto", "Usa vocabulario técnico WSET"],
        "do_not": ["Limitarte a nombrar o enumerar (eso es describir, no explicar)", "Dar afirmaciones sin respaldo"],
        "mentor_hint": "Usa la estructura: [Factor] → [mecanismo] → [resultado en el vino]. Por ejemplo: «Temperaturas frescas ralentizan la maduración → menos acumulación de azúcar y más ácido málico retenido → mayor acidez en el vino final».",
    },
    "justify": {
        "definition": "Da razones o evidencia que respalden una posición o elección dada. La posición ya está planteada; debes defenderla.",
        "do": ["Selecciona la evidencia más sólida y específica", "Vincula la evidencia directamente con la posición", "Usa vocabulario WSET"],
        "do_not": ["Argumentar en contra de la posición", "Dar descripciones genéricas sin relación con la afirmación"],
        "mentor_hint": "Empieza reformulando la posición en una línea y da 3 o más razones específicas. Cada razón debe conectar directamente con la afirmación.",
    },
}

ES_MENTOR_HINTS: dict[str, dict[str, Any]] = {
    "MCQ_strategy": {
        "common_errors": ["Sobrepensar los distractores", "Elegir respuestas parcialmente correctas"],
        "hint": "En preguntas SBA, elimina primero las opciones claramente incorrectas. La respuesta correcta es totalmente precisa, no parcialmente. WSET usa vocabulario preciso: «seco» no es lo mismo que «semiseco».",
    },
    "SAT_appearance": {
        "common_errors": ["Olvidar evaluar la limpidez", "Usar vocabulario no SAT (p. ej. «bonito», «oscuro»)"],
        "hint": "Recorre el Aspecto en orden: limpidez → intensidad → color. Cada elemento tiene su propia escala. El color debe corresponder al tipo de vino (blanco, rosado, tinto).",
    },
    "SAT_nose": {
        "common_errors": ["Mezclar primarios/secundarios/terciarios sin asignar categorías", "Enumerar «fruta» genérica sin especificar"],
        "hint": "Tras indicar condición (limpio/defectuoso) e intensidad, identifica aromas por categoría: primarios (fruta, floral, vegetal), secundarios (roble, maloláctica, levadura), terciarios (crianza en botella, oxidación). Al menos un descriptor específico por categoría obtiene la marca.",
    },
    "SAT_palate": {
        "common_errors": ["Omitir la evaluación de acidez o tanino", "Tratar el «cuerpo» como un sabor y no como elemento estructural", "Confundir las escalas del final de boca"],
        "hint": "En boca, cubre los nueve elementos en orden: dulzor, acidez, tanino (solo tintos), alcohol, cuerpo, intensidad de sabor, características de sabor, final. Cuerpo y final son conclusiones estructurales, no sabores.",
    },
    "SAT_quality": {
        "common_errors": ["Elegir el nivel de calidad sin justificarlo con la nota de cata", "Usar «excelente» en vinos sin complejidad terciaria"],
        "hint": "El nivel de calidad debe ser coherente con tu nota de cata. «Excelente» requiere: intensidad pronunciada + las tres categorías de aroma + equilibrio + final largo. Un vino simple no puede ser excelente.",
    },
    "SAT_readiness": {
        "common_errors": ["No alinear el estado de consumo con la etapa de evolución", "Elegir «demasiado joven» para un vino en evolución"],
        "hint": "«Puede beberse ahora pero tiene potencial» es la respuesta correcta para la mayoría de vinos premium con complejidad en desarrollo. Elige «demasiado joven» solo si el vino está claramente sin resolver (tanino sin integrar, sin evolución).",
    },
    "short_answer_structure": {
        "common_errors": ["Dar una sola razón en una pregunta de varias marcas", "Explicar sin especificar la causa"],
        "hint": "Cuenta las marcas. Una pregunta de explicar de 4 marcas necesita 4 vínculos causales distintos. El objetivo es una oración completa por vínculo. No repitas el mismo punto con otras palabras.",
    },
}

ES_QUALITY_PRINCIPLE = (
    "El nivel de calidad debe justificarse con observaciones específicas de la cata. "
    "NO es una opinión: debe derivarse de la evidencia."
)

ES_COMMON_QUALITY_ERRORS = [
    "Elegir «excelente» para un vino simple porque gusta personalmente",
    "No reconocer «simple» como descriptor válido que obtiene marcas en vinos básicos",
    "Elegir «muy bueno» para un vino con solo aromas primarios (debería ser «bueno» o «aceptable»)",
    "Elegir «bueno» cuando el vino muestra claramente las tres categorías de aroma y final largo (debería ser «muy bueno» o «excelente»)",
]


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

    # Phase Z.2: learner-facing strings come from the Spanish override layer.
    # The English knowledge assets define WHICH verbs/topics exist; the ES
    # tables define what the learner reads. A verb without translation is a
    # hard error so English can never silently ship.
    command_verbs: dict[str, Any] = {}
    for verb in COMMAND_VERBS:
        _load(COMMAND_VERB_DIR / f"{verb}.json")  # source must exist (contract)
        if verb not in ES_COMMAND_VERBS:
            raise ValueError(
                f"Localization guard: command verb '{verb}' has no Spanish "
                "translation in ES_COMMAND_VERBS — add it before exporting."
            )
        command_verbs[verb] = dict(ES_COMMAND_VERBS[verb])

    framework = quality.get("quality_justification_framework", {})
    if not framework.get("principle"):
        raise ValueError("quality_reasoning_patterns.json missing quality principle")

    mentor_hints_es: dict[str, Any] = {}
    for tema in hints.get("hints_by_topic", {}):
        if tema not in ES_MENTOR_HINTS:
            raise ValueError(
                f"Localization guard: mentor hint topic '{tema}' has no Spanish "
                "translation in ES_MENTOR_HINTS — add it before exporting."
            )
        mentor_hints_es[tema] = dict(ES_MENTOR_HINTS[tema])

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
        "quality_principle": ES_QUALITY_PRINCIPLE,
        "common_quality_errors": list(ES_COMMON_QUALITY_ERRORS),
        "simple_wine_note": SIMPLE_WINE_COACH_NOTE,
        "mentor_hints": mentor_hints_es,
        "command_verbs": command_verbs,
    }


def render_coach_js(payload: dict[str, Any]) -> str:
    body = json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2)
    return (
        "// Generated by tools/question_generation/distinction_coach_exporter.py\n"
        "// Compiled from knowledge/ assessment-intelligence assets. Do not edit.\n"
        "// Learner-facing strings are Spanish by contract (Phase Z.2 localization guard).\n"
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
