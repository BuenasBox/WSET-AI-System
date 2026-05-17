"""Deterministic local Tutor Answer Builder for Minimal Brain v4."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from tools.orchestrator.orchestrator import DEFAULT_CONTEXT_PACKAGE_DIR
from tools.tutor.explanation_priority import DEPTH_TO_STYLE, build_explanation_priority
from tools.tutor.scaffolding_policy import select_scaffolding_policy
from tools.youtube_transcription.config import PROJECT_ROOT


DEFAULT_CONTEXT_PACKAGE_PATH = DEFAULT_CONTEXT_PACKAGE_DIR / "latest_context_package.json"
DEFAULT_TUTOR_OUTPUT_DIR = PROJECT_ROOT / "knowledge" / "nazareth" / "tutor_outputs"
DISCLAIMER_ES = "Nota: esta es una respuesta del Tutor, no una calificación oficial ni una evaluación del Examiner."
DISCLAIMER_EN = "Note: this is a Tutor response, not an official grade or an Examiner evaluation."
KEY_TERMS = "SAT, BICL, balance, intensity, complexity, length, acidity, tannin, body, quality assessment"
STYLES = {"concise", "standard", "detailed"}
TUTOR_MARKDOWN_LABELS = {
    "en": {
        "title": "Tutor Draft",
        "normal_direct": "Short Direct Answer",
        "normal_framing": "WSET Framing",
        "cause_effect": "Cause/Effect Explanation",
        "normal_exam": "Exam Formulation",
        "mini_practice": "Mini Practice",
        "misconception_direct": "Direct Correction",
        "misconception_confusion": "Why The Misconception Is Tempting",
        "misconception_framing": "Correct WSET Framing",
        "misconception_cause_effect": "Cause/Effect Explanation",
        "misconception_exam": "How To Write It For Marks",
    },
    "es": {
        "title": "Borrador del Tutor",
        "normal_direct": "Respuesta directa",
        "normal_framing": "Marco WSET",
        "cause_effect": "Explicación causa → efecto",
        "normal_exam": "Formulación de examen",
        "mini_practice": "Mini práctica",
        "misconception_direct": "Corrección directa",
        "misconception_confusion": "Por qué esa idea confunde",
        "misconception_framing": "Marco WSET correcto",
        "misconception_cause_effect": "Cadena causa → efecto",
        "misconception_exam": "Cómo escribirlo para puntos",
    },
}


def build_tutor_answer(
    context_package_path: Path = DEFAULT_CONTEXT_PACKAGE_PATH,
    language: str | None = None,
    output_path: Path | None = None,
    style: str = "standard",
) -> dict[str, Any]:
    """Build and save a deterministic Tutor draft answer from a context package."""
    package = load_context_package(context_package_path)
    selected_language = _normalize_language(language or str(package.get("language") or "es"))
    selected_style = _normalize_style(style)
    _validate_governance(package)
    answer = render_answer(package, selected_language, selected_style)
    paths = write_tutor_answer(answer, output_path=output_path)
    return {
        "answer": answer,
        "output_paths": paths,
        "language": selected_language,
        "pedagogical_act": package.get("pedagogical_act", ""),
        "style": selected_style,
        "student_query": package.get("student_query", ""),
        "governance": {
            "safe_for_examiner": False,
            "examiner_scoring_allowed": False,
            "uses_llm": False,
            "uses_api": False,
            "uses_embeddings": False,
            "uses_vector_db": False,
            "cloud_services_active": False,
        },
    }


def load_context_package(path: Path = DEFAULT_CONTEXT_PACKAGE_PATH) -> dict[str, Any]:
    """Load the latest Tutor context package."""
    with path.open("r", encoding="utf-8") as file:
        package = json.load(file)
    if not isinstance(package, dict):
        raise ValueError(f"Context package must be a JSON object: {path}")
    return package


def render_answer(package: dict[str, Any], language: str, style: str = "standard") -> str:
    """Render a deterministic Markdown Tutor draft from package fields."""
    act = str(package.get("pedagogical_act") or "")
    priority_plan = build_explanation_priority(package)
    depth = _select_explanation_depth(package, style, priority_plan)
    package["_scaffolding_policy"] = _scaffolding_policy_for_package(package, priority_plan)
    if act == "misconception_intervention":
        return _render_misconception_answer(package, language, style, depth, priority_plan)
    return _render_normal_answer(package, language, style, depth, priority_plan)


def write_tutor_answer(answer: str, output_path: Path | None = None) -> dict[str, str]:
    """Write latest and timestamped local Tutor answer artifacts."""
    output_dir = (output_path.parent if output_path else DEFAULT_TUTOR_OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)
    latest_path = output_path or output_dir / "latest_tutor_answer.md"
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    timestamped_path = output_dir / f"{timestamp}_tutor_answer.md"
    latest_path.write_text(answer, encoding="utf-8")
    timestamped_path.write_text(answer, encoding="utf-8")
    return {
        "latest": latest_path.as_posix(),
        "timestamped": timestamped_path.as_posix(),
    }


def _render_misconception_answer(
    package: dict[str, Any],
    language: str,
    style: str,
    depth: str = "standard",
    priority_plan: dict[str, Any] | None = None,
) -> str:
    query = str(package.get("student_query") or "")
    misconception = package.get("matched_misconception") or {}
    corrected = str(misconception.get("corrected_understanding") or package.get("tutor_directive", {}).get("corrected_understanding") or "")
    direct_correction = _misconception_direct_correction(query, language)
    ideas = _extract_context_ideas(package, _depth_to_style(depth, style))
    source_note = _source_note(package, language)
    support = _support_summary(package, language, ideas)
    confusion = _confusion_line(package, language)
    framing = _wset_framing_line(query, language, corrected, ideas)
    cause = _cause_effect_line(package, language, ideas, depth)
    exam = _exam_line(query, language, ideas)
    if depth == "minimal":
        support = _compress_explanation(support, depth)
        confusion = _compress_explanation(confusion, depth)
        exam = _compress_explanation(exam, depth)

    if language == "en":
        labels = TUTOR_MARKDOWN_LABELS["en"]
        lines = [
            f"# {labels['title']}: {query}",
            "",
            f"## 1. {labels['misconception_direct']}",
            direct_correction,
            "",
            f"## 2. {labels['misconception_confusion']}",
            confusion,
            "",
            f"## 3. {labels['misconception_framing']}",
            framing,
            "",
            f"## 4. {labels['misconception_cause_effect']}",
            cause,
            "",
            f"## 5. {labels['misconception_exam']}",
            exam,
            "",
            f"## 6. {labels['mini_practice']}",
            _mini_practice(query, language),
            "",
            source_note,
            support,
            "",
            DISCLAIMER_EN,
        ]
    else:
        labels = TUTOR_MARKDOWN_LABELS["es"]
        lines = [
            f"# {labels['title']}: {_display_query(query, language)}",
            "",
            f"## 1. {labels['misconception_direct']}",
            direct_correction,
            "",
            f"## 2. {labels['misconception_confusion']}",
            confusion,
            "",
            f"## 3. {labels['misconception_framing']}",
            framing,
            "",
            f"## 4. {labels['misconception_cause_effect']}",
            cause,
            "",
            f"## 5. {labels['misconception_exam']}",
            exam,
            "",
            f"## 6. {labels['mini_practice']}",
            _mini_practice(query, language),
            "",
            source_note,
            support,
            "",
            DISCLAIMER_ES,
        ]
    return "\n".join(line for line in lines if line is not None)


def _render_normal_answer(
    package: dict[str, Any],
    language: str,
    style: str,
    depth: str = "standard",
    priority_plan: dict[str, Any] | None = None,
) -> str:
    query = str(package.get("student_query") or "")
    ideas = _extract_context_ideas(package, _depth_to_style(depth, style))
    support = _support_summary(package, language, ideas)
    source_note = _source_note(package, language)
    direct = _normal_direct_answer(query, language, ideas)
    framing = _wset_framing_line(query, language, "", ideas)
    cause = _cause_effect_line(package, language, ideas, depth)
    exam = _exam_line(query, language, ideas)
    if depth == "minimal":
        support = _compress_explanation(support, depth)
        framing = _compress_explanation(framing, depth)
        exam = _compress_explanation(exam, depth)

    if language == "en":
        labels = TUTOR_MARKDOWN_LABELS["en"]
        lines = [
            f"# {labels['title']}: {query}",
            "",
            f"## 1. {labels['normal_direct']}",
            direct,
            "",
            f"## 2. {labels['normal_framing']}",
            framing,
            "",
            f"## 3. {labels['cause_effect']}",
            cause,
            "",
            f"## 4. {labels['normal_exam']}",
            exam,
            "",
            f"## 5. {labels['mini_practice']}",
            _mini_practice(query, language),
            "",
            source_note,
            support,
            "",
            DISCLAIMER_EN,
        ]
    else:
        labels = TUTOR_MARKDOWN_LABELS["es"]
        lines = [
            f"# {labels['title']}: {_display_query(query, language)}",
            "",
            f"## 1. {labels['normal_direct']}",
            direct,
            "",
            f"## 2. {labels['normal_framing']}",
            framing,
            "",
            f"## 3. {labels['cause_effect']}",
            cause,
            "",
            f"## 4. {labels['normal_exam']}",
            exam,
            "",
            f"## 5. {labels['mini_practice']}",
            _mini_practice(query, language),
            "",
            source_note,
            support,
            "",
            DISCLAIMER_ES,
        ]
    return "\n".join(line for line in lines if line is not None)


def _normal_direct_answer(query: str, language: str, ideas: list[dict[str, str]] | None = None) -> str:  # noqa: C901
    lowered = query.lower()
    ideas = ideas or []
    if language == "en":
        if "cool climate" in lowered and "acid" in lowered:
            return "Cool climate generally helps retain acidity because grapes ripen more slowly and lose less acid before harvest."
        if "quality" in lowered and "sat" in lowered:
            return "In SAT, justify quality by linking your conclusion to balance, intensity, complexity, length, and the condition of the fruit and structure. Because all those elements support the palate impression, this therefore points toward a quality assessment grounded in evidence — not a single descriptor."
        if "oxidative" in lowered and ("ageing" in lowered or "aging" in lowered):
            return "Oxidative ageing in fortified wines exposes the wine to oxygen over time; because that contact drives aldehyde development, the wine therefore gains nutty, dried-fruit, and rancio character while losing primary fruit and colour."
        if "mechanical" in lowered and "harvest" in lowered:
            return "Mechanical harvesting can lead to oxidation and physical damage to the berry before winemaking begins; because the skin breaks early, this therefore affects aroma freshness and may increase extraction."
        if "destemming" in lowered or "destem" in lowered:
            return "Destemming removes the green, woody stalks before fermentation; because stalks add harsh green tannins and excess astringency, removing them therefore results in softer, rounder tannins and a cleaner palate structure."
        if "sulfit" in lowered or "so2" in lowered:
            return "Excessive use of sulphites can produce reductive off-aromas (struck match, rubber), and in sensitive individuals may cause adverse reactions; because sulphur dioxide suppresses yeast and bacterial activity broadly, therefore precise dosing is essential to balance preservation with wine character."
        if ("sparkling" in lowered or "effervescent" in lowered) and "pressure" in lowered:
            return "Sparkling wines below 3 atmospheres of pressure are classified as semi-sparkling (pétillant); because the CO₂ level is lower, the mousse is softer and less persistent than a fully sparkling wine above 5 atmospheres."
        if "tirage" in lowered or "liqueur de tirage" in lowered:
            return "The liqueur de tirage is a mixture of wine, sugar, and yeast added to a still base wine before the second fermentation in bottle; because it provides the fermentable sugar and yeast, it therefore generates the CO₂ that makes the wine sparkling."
        if "cava" in lowered and "champagne" in lowered:
            return "Cava is produced using the traditional method (secondary fermentation in bottle), as is Champagne, but the key technical differences lie in grape varieties (Macabeo, Xarel-lo, Parellada vs Chardonnay/Pinot Noir/Meunier), climate, and the minimum ageing periods required."
        if "soil" in lowered and ("drainage" in lowered or "drain" in lowered):
            return "Soil texture and composition directly affect drainage; because well-drained soils force vine roots deeper to find water, this therefore reduces vigour, concentrates flavour, and generally supports better quality."
        if "frost" in lowered and ("spring" in lowered or "risk" in lowered):
            return "Spring frost is primarily determined by topography and air drainage patterns; because cold air settles into low-lying areas, frost risk is therefore highest in valley floors and natural hollows."
        if "planting density" in lowered or ("plant" in lowered and "density" in lowered):
            return "Higher planting density increases vine-to-vine competition for water and nutrients; because each vine has access to fewer resources, the resulting fruit is therefore more concentrated and yields per vine are lower."
        # Fallback using idea content
        if ideas:
            return f"From the WSET perspective: {ideas[0]['idea']}."
        return "Answer the question through the WSET framework, then support the conclusion with clear evidence."
    # Spanish paths
    if "cool climate" in lowered and "acid" in lowered:
        return "Un clima fresco suele conservar más acidity porque la uva madura más lentamente y pierde menos ácido antes de la vendimia."
    if "quality" in lowered and "sat" in lowered:
        return "En SAT, justifica la quality assessment vinculando tu conclusión con balance, intensity, complexity, length y la condición de la fruta y la estructura. Porque esos elementos sostienen la impresión del paladar, la quality assessment — por tanto — se apoya en evidencia, no en un descriptor aislado."
    if ("oloroso" in lowered or "amontillado" in lowered) and "crianza" in lowered:
        return "La diferencia clave radica en la crianza: el Amontillado comienza con crianza biológica bajo la flor, pero la flor dies cuando el alcohol sube — entonces la oxidative ageing toma el relevo (no flor → oxidative ageing). El Oloroso, por tanto, nunca desarrolla flor y experimenta desde el inicio una crianza completamente oxidativa, desarrollando aromas a nueces, frutos secos y color ambarino intenso."
    if "oxidativ" in lowered and ("envejec" in lowered or "crianza" in lowered):
        return "El envejecimiento oxidativo en vinos generosos como el Oloroso expone el vino al contacto con el oxígeno durante la crianza; porque ese proceso impulsa la formación de acetaldehído y otros aldehídos, el vino desarrolla — por tanto — aromas a nueces, frutas secas y tonos ambarados, con pérdida del color original."
    if "vendimia mec" in lowered or ("vendimia" in lowered and "mec" in lowered):
        return "La vendimia mecánica puede introducir oxidación y rotura de la baya antes de la elaboración; porque el oxígeno entra en contacto con el mosto expuesto, esto conduce — por tanto — a una menor frescura aromática y potencialmente mayor extracción de compuestos fenólicos."
    if "despalillado" in lowered:
        return "El despalillado elimina los raspones verdes antes de la fermentación; porque los raspones aportan taninos verdes y astringencia excesiva, su eliminación conduce — por tanto — a vinos con taninos más suaves, redondeados y una estructura de paladar más limpia."
    if "sulfit" in lowered or ("so2" in lowered):
        return "El uso excesivo de sulfitos puede producir aromas reductivos (cerilla, goma) y, en personas sensibles, reacciones adversas; porque el dióxido de azufre actúa como conservante e inhibidor microbiano, un exceso puede — por tanto — enmascarar el carácter del vino y dejar residuos perceptibles."
    if ("espumoso" in lowered or "espumante" in lowered) and ("presi" in lowered or "atm" in lowered):
        return "Los vinos espumosos con presión inferior a 3 atmósferas se clasifican como semi-espumosos o perlantes; porque el nivel de CO₂ es menor, la burbuja es más suave y menos persistente que en un espumoso completo por encima de 5 atmósferas."
    if "tiraje" in lowered or "licor de tiraje" in lowered:
        return "El licor de tiraje es una mezcla de vino, azúcar y levaduras añadida al vino base antes de la segunda fermentación en botella; porque aporta el azúcar fermentable y las levaduras necesarias, por tanto genera el CO₂ que convierte el vino en espumoso."
    if "cava" in lowered and ("champagne" in lowered or "champan" in lowered):
        return "Tanto el Cava como el Champagne se elaboran por el método tradicional (segunda fermentación en botella), pero sus diferencias técnicas clave residen en las variedades de uva (Macabeo, Xarel-lo, Parellada frente a Chardonnay/Pinot Noir/Meunier), el clima y los períodos mínimos de crianza exigidos por cada denominación."
    if ("suelo" in lowered or "tierra" in lowered) and ("drenaje" in lowered or "drena" in lowered):
        return "La textura y composición del suelo influyen directamente en el drenaje; porque un suelo bien drenado obliga a las raíces a profundizar en busca de agua, esto conduce — por tanto — a menor vigor, mayor concentración de sabor y, generalmente, mejor calidad de la uva."
    if "helada" in lowered and ("primavera" in lowered or "riesgo" in lowered):
        return "El riesgo de heladas primaverales está determinado principalmente por la topografía y la circulación del aire frío; porque el aire frío desciende y se acumula en las zonas bajas, el riesgo es — por tanto — mayor en valles y hondonadas que en laderas con buen drenaje aéreo."
    if "plantaci" in lowered and ("densidad" in lowered or "alta" in lowered):
        return "Una alta densidad de plantación aumenta la competencia entre cepas por agua y nutrientes; porque cada vid accede a menos recursos, la uva resultante es — por tanto — más concentrada y los rendimientos por vid son menores."
    if ("tokaji" in lowered or "tokay" in lowered or "asz" in lowered):
        return "La práctica que distingue al Tokaji Aszú es la adición de uvas botrytizadas (afectadas por Botrytis cinerea en su forma noble) al vino base; porque la podredumbre noble concentra azúcares y ácidos y produce glicerol, esto conduce — por tanto — a un vino dulce de gran concentración, complejidad y capacidad de guarda."
    if "cremant" in lowered or "crémant" in lowered:
        return "El Crémant de Loire se elabora por el método tradicional con uvas de la región del Loira, principalmente Chenin Blanc; porque el clima fresco del Loira favorece una acidez natural elevada, el espumoso resultante presenta — por tanto — burbuja fina, frescura marcada y buen equilibrio."
    if "madeira" in lowered or "madera" in lowered:
        return "Madeira se elabora principalmente con variedades autóctonas como Sercial, Verdelho, Bual y Malmsey; porque la isla tiene un clima subtropical y los vinos pasan por el proceso de estufagem (calor controlado), esto conduce — por tanto — a vinos con acidez elevada, carácter oxidativo y gran longevidad."
    if "region" in lowered and ("chile" in lowered or "chilena" in lowered) and ("espumoso" in lowered or "clima fresco" in lowered):
        return "La región de Elqui y Bio-Bío en Chile son reconocidas por espumosos de calidad gracias a sus climas frescos; porque las temperaturas nocturnas bajas conservan la acidez natural de la uva, el espumoso resultante presenta — por tanto — burbuja fina, frescura marcada y buena base estructural."
    # Fallback using idea content
    if ideas:
        return f"Desde el marco WSET: {ideas[0]['idea']}."
    return "Responde desde el marco WSET y apoya la conclusión con evidencia clara."


def _display_query(query: str, language: str) -> str:
    if language != "es":
        return query
    lowered = query.lower()
    if "more tannin" in lowered and "better wine" in lowered:
        return "¿Más tanino significa mejor vino?"
    if "high acidity" in lowered and ("lower quality" in lowered or "low quality" in lowered):
        return "¿High acidity significa menor calidad?"
    if "cool climate" in lowered and "acidity" in lowered:
        return "¿Cómo afecta un clima fresco a la acidity?"
    if "quality" in lowered and "sat" in lowered:
        return "¿Cómo justifico la quality assessment en SAT?"
    return query


def _misconception_direct_correction(query: str, language: str) -> str:
    lowered = query.lower()
    if language == "en":
        if "acid" in lowered and ("quality" in lowered or "lower" in lowered):
            return "Not exactly. In WSET terms, high acidity does not automatically mean lower quality."
        if "tannin" in lowered and ("better" in lowered or "quality" in lowered):
            return "Not exactly. More tannin does not automatically mean better wine."
        return "Not exactly. In WSET terms, that shortcut is not reliable on its own."
    if "acid" in lowered and ("quality" in lowered or "lower" in lowered):
        return "No exactamente. En WSET, high acidity no significa automáticamente menor calidad."
    if "tannin" in lowered and ("better" in lowered or "quality" in lowered):
        return "No exactamente. Más tanino no significa automáticamente mejor vino."
    return "No exactamente. En WSET, ese atajo no es fiable por sí solo."


def _render_causal_chain(chain: dict[str, Any], language: str, max_steps: int | None = None) -> str:
    """Render a causal chain node as a structured cause → mechanism → effect block.

    This replaces keyword-dispatch hardcoded strings for queries where a matching
    causal chain node has been retrieved. The output comes from the node's steps
    array, not from hardcoded content in this module.

    Governance: chain must have safe_for_examiner != True.
    """
    if chain.get("safe_for_examiner") is True:
        return ""
    steps = chain.get("steps", [])
    if not steps:
        return ""
    label_map_es = {
        "cause": "CAUSA",
        "mechanism": "MECANISMO",
        "effect": "EFECTO",
        "exam_formulation": "FORMULACIÓN DE EXAMEN",
    }
    label_map_en = {
        "cause": "CAUSE",
        "mechanism": "MECHANISM",
        "effect": "EFFECT",
        "exam_formulation": "EXAM FORMULATION",
    }
    label_map = label_map_es if language == "es" else label_map_en
    lines = []
    ordered_steps = sorted(steps, key=lambda s: int(s.get("step", 0)))
    if max_steps is not None and len(ordered_steps) > max_steps:
        ordered_steps = _essential_causal_steps(ordered_steps, max_steps)
    for step in ordered_steps:
        label_key = str(step.get("label", "")).lower()
        label = label_map.get(label_key, label_key.upper())
        text = str(step.get("text", "")).strip()
        if text:
            lines.append(f"**{label}:** {text}")
    sat_rel = str(chain.get("sat_relevance", "")).strip()
    if sat_rel:
        prefix = "Relevancia SAT" if language == "es" else "SAT Relevance"
        lines.append(f"\n*{prefix}: {sat_rel}*")
    return "\n".join(lines)


def _select_best_causal_chain(package: dict[str, Any]) -> dict[str, Any] | None:
    """Select the most relevant causal chain node from forced_causal_chains.

    Returns the first chain whose trigger_keywords overlap most with the query,
    or the first chain if no keyword scoring is possible.
    """
    chains = package.get("forced_causal_chains", []) or []
    if not chains:
        return None
    query = str(package.get("student_query") or "").lower()
    best = None
    best_score = -1
    for chain in chains:
        keywords = [str(kw).lower() for kw in chain.get("trigger_keywords", [])]
        score = sum(1 for kw in keywords if kw in query)
        if score > best_score:
            best_score = score
            best = chain
    return best


def _cause_effect_line(
    package: dict[str, Any],
    language: str,
    ideas: list[dict[str, str]],
    depth: str | None = None,
) -> str:
    # Phase D: prefer structured causal chain node over hardcoded keyword dispatch
    best_chain = _select_best_causal_chain(package)
    if best_chain:
        rendered = _render_causal_chain(best_chain, language, max_steps=_max_causal_steps(depth))
        if rendered:
            return rendered

    # Fallback: deterministic keyword dispatch (preserved for backward compatibility
    # and for queries where no causal chain node was matched)
    query = str(package.get("student_query") or "").lower()
    misconception = package.get("matched_misconception") or {}
    why = str(misconception.get("why_incorrect") or "").lower()
    idea_text = " ".join(item["idea"] for item in ideas).lower()
    if language == "en":
        if "tannin" in query or "tannin" in why:
            return "Cause → effect: phenolic material contributes tannin; tannin is felt as drying astringency, so quality depends on whether that structure is ripe, balanced, and integrated."
        if "cool climate" in query or ("acid" in query and "climate" in idea_text):
            return "Cause → effect: cooler conditions slow ripening, so grapes tend to retain more acid; the wine can therefore show higher acidity and freshness."
        if "acid" in query:
            return "Cause → effect: acidity affects freshness and balance; it becomes positive or negative depending on the wine's style and the surrounding fruit, sugar, alcohol, and body."
        if "oxidative" in query and ("ageing" in query or "aging" in query):
            return "Cause → effect: oxygen contact over time drives aldehyde formation (notably acetaldehyde); because these compounds accumulate in the wine, the result is therefore nutty, dried-fruit, and amber character alongside reduced primary fruit and colour."
        if "mechanical" in query and "harvest" in query:
            return "Cause → effect: mechanical harvesting breaks berry skin before the winery; because this causes early oxidation of the juice, the wine therefore shows reduced aromatic freshness compared to carefully hand-harvested fruit."
        if "destem" in query:
            return "Cause → effect: stalks contribute harsh, green tannins; because destemming removes this source, the resulting fermentation therefore extracts softer, riper tannin from skins and seeds only."
        if "sulphite" in query or "sulfite" in query or "so2" in query:
            return "Cause → effect: SO₂ inhibits oxidation and microbial activity; because excess sulphites suppress these processes too broadly, the wine therefore retains less natural complexity and may show reductive off-aromas."
        if "tirage" in query or "liqueur de tirage" in query:
            return "Cause → effect: the tirage adds sugar and yeast to the base wine; because yeast ferments the sugar in a sealed bottle, CO₂ therefore builds up and cannot escape, making the wine sparkling."
        if "pressure" in query and ("sparkling" in query or "atmosphe" in query):
            return "Cause → effect: less sugar in the tirage produces less CO₂; because CO₂ determines internal pressure, a pressure below 3 atmospheres therefore classifies the wine as semi-sparkling (pétillant) rather than fully sparkling."
        if "drainage" in query and "soil" in query:
            return "Cause → effect: soil texture controls water retention; because well-drained soils remove excess water from the root zone, vines therefore control their own vigour and tend to produce smaller, more concentrated berries."
        if "frost" in query:
            return "Cause → effect: cold air is denser than warm air and flows downhill; because it settles in low-lying hollows and valley floors, spring frosts therefore pose the greatest risk to vines planted in these topographical positions."
        if "planting density" in query or ("density" in query and "plant" in query):
            return "Cause → effect: denser planting forces each vine to compete for limited soil nutrients and water; because resources per vine are restricted, vine vigour is therefore reduced and fruit concentration increases."
        return "Cause → effect: identify the driving factor, explain why and how the mechanism operates — because that causal relationship therefore connects directly to the observable result in the wine's style or quality."
    if "tannin" in query or "tannin" in why:
        return "Cadena: compuestos fenólicos de pieles, pepitas o extracción aportan tanino → el tanino se percibe como sequedad/astringencia → puede apoyar la estructura si está maduro e integrado, pero no garantiza calidad por sí solo."
    if "cool climate" in query or ("acid" in query and "climate" in idea_text):
        return "Cadena: clima fresco → maduración más lenta → mayor retención de ácidos → más acidity y sensación de frescura en el vino."
    if "acid" in query:
        return "Cadena: acidity aporta frescura y tensión → su efecto en la calidad depende de balance, fruta, azúcar, alcohol y body."
    if ("oloroso" in query or "amontillado" in query) and "crianza" in query:
        return "Cadena (Oloroso vs Amontillado): el Amontillado comienza con crianza biológica bajo la capa de flor, pero la flor dies cuando el nivel alcohólico sube o las condiciones cambian → sin flor, empieza la oxidative ageing — no flor → oxidative ageing toma el control → el vino desarrolla aromas a nueces, frutos secos y color ambarino. El Oloroso, por tanto, nunca tuvo flor: desde el inicio experimenta crianza oxidativa completa."
    if "oxidativ" in query and ("envejec" in query or "crianza" in query):
        return "Cadena: contacto del vino con el oxígeno → formación de acetaldehído y otros aldehídos → desarrollo de aromas a nueces, frutos secos y notas rancias; porque ese proceso consume el carácter primario de la fruta, el vino adquiere — por tanto — mayor complejidad terciaria y color ambarino."
    if "vendimia mec" in query or ("vendimia" in query and "mec" in query):
        return "Cadena: la máquina de vendimia rompe la baya antes de llegar a bodega → el mosto queda expuesto al oxígeno → oxidación prematura de los aromas → menor frescura aromática en el vino terminado. La gestión del oxígeno en bodega puede mitigar este efecto."
    if "despalillado" in query:
        return "Cadena: raspones presentes → fermentación extrae taninos verdes y astringentes de los raspones → vino con estructura áspera y notas herbáceas. Sin raspones: fermentación extrae tanino solo de pieles y pepitas → taninos más suaves y maduros. Por tanto, el despalillado conduce a un mejor control de la calidad táctil del vino."
    if "sulfit" in query or "so2" in query:
        return "Cadena: SO₂ en exceso → inhibición excesiva de levaduras y bacterias → menor complejidad fermentativa; además, el SO₂ residual puede producir aromas reductivos (cerilla, azufre). Por tanto, un uso excesivo de sulfitos perjudica — en vez de proteger — el carácter del vino."
    if "tiraje" in query or "licor de tiraje" in query:
        return "Cadena: se añade azúcar + levaduras al vino base → segunda fermentación en botella cerrada → el CO₂ producido no puede escapar → la presión sube → el vino se vuelve espumoso. Por tanto, el licor de tiraje es el mecanismo que genera la efervescencia en el método tradicional."
    if ("espumoso" in query or "espumante" in query) and ("presi" in query or "atm" in query):
        return "Cadena: menor cantidad de azúcar en el tiraje → la fermentación produce menos CO₂ → presión interna más baja → burbuja más fina y suave. Por tanto, una presión inferior a 3 atm clasifica el vino como semi-espumoso o perlante; ese mecanismo de fermentación es el que define directamente la intensidad de la efervescencia."
    if "cava" in query and ("champagne" in query or "champan" in query):
        return "Cadena: mismo método (segunda fermentación en botella), pero variedades, clima y normativa distintos → perfiles organolépticos diferentes. Cava (Macabeo, Xarel-lo, Parellada + clima mediterráneo) tiende hacia tonos más frutales y maduros; Champagne (Chardonnay/Pinot + clima frío) tiende hacia mayor acidez y mineralidad. Por tanto, la diferencia técnica se traduce en diferencias de estilo perceptibles."
    if ("suelo" in query or "tierra" in query) and ("drenaje" in query or "drena" in query):
        return "Cadena: textura del suelo → capacidad de retención de agua → profundidad de las raíces → vigor de la vid. Un suelo con buen drenaje obliga a las raíces a descender en busca de agua; porque eso limita el vigor, la vid concentra sus recursos en menos fruta. Por tanto, suelos bien drenados tienden — por tanto — a producir uvas más concentradas y de mayor calidad potencial."
    if "helada" in query and ("primavera" in query or "riesgo" in query):
        return "Cadena: aire frío más denso → desciende y se acumula en los puntos bajos → vides en valles o depresiones → mayor exposición al frío. Por tanto, el riesgo de heladas primaverales es mayor en las zonas topográficamente bajas y menor en las laderas con buen drenaje del aire frío."
    if "plantaci" in query and ("densidad" in query or "alta" in query):
        return "Cadena: más cepas por hectárea → competencia por agua y nutrientes → menor vigor individual → menor rendimiento por cepa → mayor concentración en las bayas. Por tanto, una alta densidad de plantación conduce — por tanto — a vinos potencialmente más complejos y concentrados, aunque implica mayor coste de producción."
    if "tokaji" in query or "asz" in query:
        return "Cadena: uvas botrytizadas (Botrytis cinerea en forma noble) concentran azúcares, ácidos y glicerol → se añaden al vino base como pasta → fermentación parcial → vino con gran concentración de azúcar residual, acidez y complejidad. Por tanto, la adición de aszú es el mecanismo que define el estilo único del Tokaji."
    if "cremant" in query or "crémant" in query:
        return "Cadena: clima fresco del Loira → alta acidez natural en Chenin Blanc → segunda fermentación en botella (método tradicional) → burbuja fina y persistente. Por tanto, el Crémant de Loire es reconocido por su frescura y equilibrio como resultado directo de su origen climático y método de elaboración."
    if "madeira" in query:
        return "Cadena: estufagem (calor controlado) + oxidación controlada → desarrollo de aromas terciarios (frutos secos, caramelo, malta) + alta acidez → longevidad excepcional. Por tanto, el proceso térmico es el mecanismo que distingue la crianza del Madeira y explica su capacidad de envejecimiento única."
    if ("chile" in query or "chilena" in query) and ("espumoso" in query or "clima fresco" in query):
        return "Cadena: altitud elevada o influencia marítima → temperaturas nocturnas frescas → maduración lenta de la uva → conservación de acidez natural → base ideal para espumoso. Por tanto, el clima fresco de ciertas regiones chilenas es la causa directa de la calidad de sus espumosos."
    return "Cadena causal: identifica el factor desencadenante, explica por qué actúa el mecanismo, porque esa relación justifica — por tanto — el efecto observable en el estilo o la calidad del vino."


def _source_note(package: dict[str, Any], language: str) -> str:
    source_types = _source_types(package)
    if language == "en":
        if "official reference" in source_types:
            return "Source note: from the WSET framework, treat official context as the reference point; use transcript material only as pedagogical support."
        if "cognitive correction object" in source_types:
            return "Source note: the misconception node is a cognitive correction object, and Wine With Jimmy/manual transcript material is pedagogical support, not official WSET authority."
        return "Source note: Wine With Jimmy/manual transcript material is pedagogical support, not official WSET authority."
    if "official reference" in source_types:
        return "Nota de fuentes: desde el marco WSET, el material oficial es la referencia; el material de transcripción sirve solo como apoyo pedagógico."
    if "cognitive correction object" in source_types:
        return "Nota de fuentes: el misconception_node es un objeto de corrección cognitiva; el material de Wine With Jimmy o transcripciones manuales es apoyo pedagógico, no autoridad oficial WSET."
    return "Nota de fuentes: el material de Wine With Jimmy o transcripciones manuales es apoyo pedagógico, no autoridad oficial WSET."


def _support_summary(package: dict[str, Any], language: str, ideas: list[dict[str, str]]) -> str:
    if not ideas:
        return "Contexto usado: misconception_node y paquete local del Tutor." if language == "es" else "Context used: misconception node and local Tutor package."
    labels = []
    for item in ideas[:4]:
        labels.append(f"{item['source']}: {item['idea']}")
    prefix = "Ideas usadas del contexto: " if language == "es" else "Ideas used from context: "
    return prefix + " | ".join(labels) + "."


def _source_types(package: dict[str, Any]) -> set[str]:
    types = set()
    for item in package.get("retrieved_context", []):
        if not isinstance(item, dict):
            continue
        context_type = str(item.get("context_type") or "")
        if context_type == "misconception_node":
            types.add("cognitive correction object")
            continue
        raw_type = str(item.get("source_type") or item.get("transcript_source") or "")
        filename = str(item.get("source_filename") or "")
        if raw_type in {"official_wset_extracted", "official_wset"}:
            types.add("official reference")
        elif raw_type in {"manual_curated_srt", "youtube_transcript"} or filename.endswith(".srt") or context_type == "retrieval_sandbox_chunk":
            types.add("pedagogical enrichment")
    return types


def _validate_governance(package: dict[str, Any]) -> None:
    governance = package.get("governance") or {}
    tutor_directive = package.get("tutor_directive") or {}
    if governance.get("safe_for_examiner") or tutor_directive.get("safe_for_examiner"):
        raise ValueError("Unsafe context package: safe_for_examiner must remain false for Tutor output.")
    if governance.get("examiner_scoring_allowed"):
        raise ValueError("Unsafe context package: Examiner scoring is not allowed for Tutor output.")


def _normalize_language(language: str) -> str:
    return "en" if str(language).lower() == "en" else "es"


def _normalize_style(style: str) -> str:
    return style if style in STYLES else "standard"


def _select_explanation_depth(
    package: dict[str, Any],
    style: str = "standard",
    priority_plan: dict[str, Any] | None = None,
) -> str:
    """Select answer depth from confidence, severity, LES, and cognitive load."""
    priority_plan = priority_plan or build_explanation_priority(package)
    if _normalize_style(style) == "concise":
        return "minimal"
    if _normalize_style(style) == "detailed":
        return "deep"
    misconception = package.get("matched_misconception") or {}
    severity = str(misconception.get("severity") or "").lower()
    confidence = _package_confidence(package)
    cognitive_load = str(priority_plan.get("cognitive_load_estimate") or "medium")
    boost = (package.get("retrieval_plan") or {}).get("pedagogical_priority_boost") or {}
    les_context = package.get("learner_state_context") or {}
    mastery = str(les_context.get("mastery") or les_context.get("current_mastery") or "").lower()
    if boost.get("force_deep_explanation") and cognitive_load != "high":
        return "deep"
    if cognitive_load == "high":
        return "standard"
    if confidence < 0.55 or severity in {"high", "critical"}:
        return "deep"
    if mastery in {"high", "advanced", "strong"} and not misconception:
        return "minimal"
    return str(priority_plan.get("recommended_depth") or "standard")


def _scaffolding_policy_for_package(package: dict[str, Any], priority_plan: dict[str, Any]) -> dict[str, Any]:
    memory = (package.get("learner_state_context") or {}).get("pedagogical_memory") or {}
    low_mastery = memory.get("low_mastery_concepts") or []
    mastery = None
    if low_mastery and isinstance(low_mastery[0], dict):
        mastery = float(low_mastery[0].get("mastery_probability", 0.5) or 0.5)
    misconception = package.get("matched_misconception") or {}
    return select_scaffolding_policy(
        mastery_probability=mastery,
        cognitive_load=str(priority_plan.get("cognitive_load_estimate") or "medium"),
        urgency=str(priority_plan.get("urgency") or "medium"),
        misconception_severity=str(misconception.get("severity") or "medium"),
    )


def _compress_explanation(text: str, depth: str = "minimal") -> str:
    """Reduce redundancy while keeping the causal spine intact."""
    if depth != "minimal":
        return text
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    if len(sentences) <= 1:
        return text
    causal = [sentence for sentence in sentences if re.search(r"\b(porque|because|causa|cause|mecanismo|mechanism|efecto|effect|por eso|therefore|so)\b", sentence, re.IGNORECASE)]
    selected = causal[:2] or sentences[:2]
    return " ".join(selected).strip()


def _depth_to_style(depth: str, fallback_style: str) -> str:
    return DEPTH_TO_STYLE.get(depth, _normalize_style(fallback_style))


def _package_confidence(package: dict[str, Any]) -> float:
    for container in (package.get("orchestrator_decision"), package.get("tutor_directive"), package.get("matched_misconception")):
        if isinstance(container, dict) and container.get("confidence") is not None:
            try:
                return max(0.0, min(1.0, float(container.get("confidence"))))
            except (TypeError, ValueError):
                return 0.65
    return 0.65 if package.get("matched_misconception") else 0.8


def _max_causal_steps(depth: str | None) -> int | None:
    if depth == "minimal":
        return 3
    return None


def _essential_causal_steps(steps: list[dict[str, Any]], max_steps: int) -> list[dict[str, Any]]:
    if len(steps) <= max_steps:
        return steps
    essentials = []
    used = set()
    for label in ("cause", "mechanism", "effect", "exam_formulation"):
        for index, step in enumerate(steps):
            if index in used:
                continue
            if str(step.get("label", "")).lower() == label:
                essentials.append(step)
                used.add(index)
                break
            if len(essentials) >= max_steps:
                return essentials
    for index, step in enumerate(steps):
        if len(essentials) >= max_steps:
            break
        if index not in used:
            essentials.append(step)
    return essentials[:max_steps]


def _extract_context_ideas(package: dict[str, Any], style: str) -> list[dict[str, str]]:
    limit = {"concise": 3, "standard": 4, "detailed": 5}[_normalize_style(style)]
    query = str(package.get("student_query") or "").lower()
    contexts = [item for item in package.get("retrieved_context", []) if isinstance(item, dict)]
    ranked = sorted(contexts, key=_context_rank, reverse=True)
    ideas = []
    seen = set()
    if "cool climate" in query and "acid" in query:
        ideas.append(
            {
                "source": "retrieval_plan",
                "idea": "el clima fresco ralentiza la maduración y favorece la retención de acidity",
            }
        )
        seen.add(ideas[0]["idea"])
    for item in ranked:
        idea = _idea_from_context_item(item, package)
        if not idea or idea in seen:
            continue
        seen.add(idea)
        source = _context_label(item)
        ideas.append({"source": source, "idea": idea})
        if len(ideas) >= limit:
            break
    return ideas


def _context_rank(item: dict[str, Any]) -> float:
    score = 0.0
    if item.get("forced_retrieval"):
        score += 5
    if item.get("context_type") == "misconception_node":
        score += 4
    why = " ".join(item.get("why_retrieved", [])).lower()
    if "golden tutor chunk candidate" in why:
        score += 3
    if "high retrieval priority" in why:
        score += 2
    if str(item.get("reasoning_type")) in {"cause_effect", "common_mistake", "exam_strategy"}:
        score += 1.5
    if _is_official_source(item):
        score += 2
    score += float(item.get("score") or 0)
    return score


def _idea_from_context_item(item: dict[str, Any], package: dict[str, Any]) -> str:
    if _is_official_source(item):
        official = _official_idea_from_text(str(item.get("text_excerpt") or ""), package)
        if official:
            return official
    if item.get("context_type") == "misconception_node":
        content = item.get("content") or package.get("matched_misconception") or {}
        corrected = str(content.get("corrected_understanding") or "")
        why = str(content.get("why_incorrect") or "")
        if "Tannin produces astringency" in corrected or "tannin" in corrected.lower():
            return "el tanino es astringencia táctil, no simplemente amargor"
        if "High acidity" in corrected or "acidity" in corrected.lower():
            return "high acidity puede ser positivo si está equilibrado con fruta, azúcar, alcohol y estilo"
        return _clean_idea(corrected or why)

    haystack = " ".join(
        [
            str(item.get("text_excerpt") or ""),
            " ".join(item.get("why_retrieved", [])),
            str(item.get("reasoning_type") or ""),
            str(item.get("pedagogical_role") or ""),
        ]
    ).lower()
    if "systematic approach" in haystack or "sat" in haystack or "marks" in haystack:
        return "en SAT conviene escribir todos los elementos relevantes y vincularlos con la conclusión"
    if "tannin" in haystack or "tannins" in haystack:
        if "seeds" in haystack or "skin" in haystack or "phenolic" in haystack:
            return "pieles, pepitas y extracción pueden aportar tanino y estructura"
        return "el tanino debe evaluarse como estructura y sensación táctil"
    if "cool climate" in haystack or "slow ripening" in haystack or "acid retention" in haystack:
        return "el clima fresco tiende a ralentizar la maduración y conservar acidity"
    if "acid" in haystack or "acidity" in haystack:
        return "la acidity aporta frescura, pero debe leerse dentro del balance del vino"
    if "balance" in haystack or "complexity" in haystack or "length" in haystack:
        return "quality assessment se justifica con balance, intensity, complexity y length"
    return _clean_idea(str(item.get("text_excerpt") or ""))


def _clean_idea(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"\b(um|uh|okay|so)\b", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s+", " ", text).strip(" .")
    if len(text) > 180:
        text = text[:177].rsplit(" ", 1)[0] + "..."
    return text


def _context_label(item: dict[str, Any]) -> str:
    if item.get("context_type") == "misconception_node":
        return str(item.get("node_id") or "misconception_node")
    if _is_official_source(item):
        return "official_wset"
    filename = str(item.get("source_filename") or "")
    if filename.endswith(".srt"):
        return "apoyo pedagógico"
    return str(item.get("chunk_id") or "contexto")


def _is_official_source(item: dict[str, Any]) -> bool:
    return str(item.get("source_type") or item.get("transcript_source") or "") in {
        "official_wset_extracted",
        "official_wset",
    }


def _has_official_support(package: dict[str, Any]) -> bool:
    return any(_is_official_source(item) for item in package.get("retrieved_context", []) if isinstance(item, dict))


def _confusion_line(package: dict[str, Any], language: str) -> str:
    query = str(package.get("student_query") or "").lower()
    if language == "en":
        if "tannin" in query:
            return "The idea is tempting because tannin gives a strong drying sensation, so it can feel like more structure must mean more quality. WSET separates structure from quality judgment."
        if "acid" in query:
            return "The idea is tempting because high acidity can feel sharp, but sharpness alone is not the same as quality or lack of quality."
        return "The idea is tempting because it turns one visible feature into a shortcut, while WSET expects evidence and balance."
    if "tannin" in query:
        return "La idea confunde porque el tanino se siente con fuerza en el paladar; parece lógico pensar que más estructura equivale a más calidad. En WSET, estructura y calidad se justifican por separado."
    if "acid" in query:
        return "La idea confunde porque high acidity puede sentirse punzante, pero esa sensación no equivale automáticamente a baja calidad."
    return "La idea confunde porque convierte un rasgo aislado en un atajo, cuando WSET exige evidencia y balance."


def _wset_framing_line(query: str, language: str, corrected: str, ideas: list[dict[str, str]]) -> str:
    lowered = query.lower()
    has_official = any(item["source"] in {"official_wset", "official WSET"} for item in ideas)
    if language == "en":
        if corrected:
            return corrected
        if "quality" in lowered or "sat" in lowered:
            return f"Use WSET terms precisely: {KEY_TERMS}. Quality needs evidence, not a single isolated descriptor."
        return f"Frame the answer through WSET vocabulary where useful: {KEY_TERMS}."
    if "tannin" in lowered:
        prefix = "Desde el marco WSET" if has_official else "Como formulación de Tutor"
        return f"{prefix}, el tanino es un componente estructural y una sensación táctil de sequedad/astringencia. Puede apoyar la calidad si está maduro e integrado con fruit concentration, balance, complexity y length; si domina o seca demasiado, puede perjudicar la impresión de calidad."
    if "acid" in lowered and "quality" in lowered:
        prefix = "Desde el marco WSET" if has_official else "Como formulación de Tutor"
        return f"{prefix}, high acidity no es buena ni mala por sí sola. Puede aportar frescura, definición y capacidad de guarda si está integrada con fruit concentration, sweetness, alcohol, body y balance."
    if corrected:
        return _spanish_paraphrase(corrected)
    prefix = "Desde el marco WSET" if has_official else "Como apoyo pedagógico"
    return f"{prefix}, usa términos precisos cuando ayuden: {KEY_TERMS}. La conclusión debe apoyarse en evidencia, no en un descriptor aislado."


def _official_idea_from_text(text: str, package: dict[str, Any]) -> str:  # noqa: C901
    lowered = text.lower()
    query = str(package.get("student_query") or "").lower()
    if "cool" in query and "acid" in query:
        return "el material oficial relaciona clima/growing environment con maduración y retención de acidez"
    if "tannin" in query:
        return "el material oficial sitúa el tannin dentro de estructura, extracción y evaluación de calidad"
    if "sat" in query or "quality" in query:
        return "el material oficial apoya una quality assessment basada en balance, intensity, complexity y length"
    if "flor" in query:
        return "el material oficial conecta flor, crianza biológica y protección frente a oxidación"
    if "port" in query or "oporto" in query:
        return "el material oficial conecta fortificación, parada de fermentación y estilo final del vino"
    if "sherry" in query or "jerez" in query:
        return "el material oficial distingue crianza biológica y oxidativa en Jerez"
    if "oxidativ" in query and ("envejec" in query or "crianza" in query):
        return "el material oficial relaciona contacto con oxígeno, formación de aldehídos y desarrollo de complejidad terciaria en vinos generosos"
    if "vendimia mec" in query or ("vendimia" in query and "mec" in query):
        return "el material oficial vincula los métodos de vendimia con el potencial aromático y la integridad de la baya en la elaboración"
    if "despalillado" in query:
        return "el material oficial relaciona el despalillado con la extracción de taninos y la estructura tánica del vino"
    if "sulfit" in query or "so2" in query:
        return "el material oficial trata el SO₂ como agente conservante y antimicrobiano con implicaciones para el carácter del vino"
    if "tiraje" in query or "licor de tiraje" in query:
        return "el material oficial explica el licor de tiraje como mecanismo de la segunda fermentación en botella en el método tradicional"
    if ("espumoso" in query or "espumante" in query) and ("presi" in query or "atm" in query):
        return "el material oficial relaciona la presión interna de CO₂ con la clasificación del vino como espumoso, semi-espumoso o perlante"
    if "cava" in query and ("champagne" in query or "champan" in query):
        return "el material oficial contrasta variedades, clima y normativas de Cava y Champagne como vinos espumosos de método tradicional"
    if ("suelo" in query or "tierra" in query) and ("drenaje" in query or "drena" in query):
        return "el material oficial relaciona la composición y el drenaje del suelo con el vigor de la vid y el potencial de calidad de la uva"
    if "helada" in query and ("primavera" in query or "riesgo" in query):
        return "el material oficial vincula la topografía, el drenaje del aire frío y el riesgo de heladas primaverales en la viticultura"
    if "plantaci" in query and ("densidad" in query or "alta" in query):
        return "el material oficial relaciona la densidad de plantación con la competencia entre cepas, el vigor y la concentración de la fruta"
    if "tokaji" in query or "tokay" in query or "asz" in query:
        return "el material oficial describe el Tokaji Aszú y la adición de uvas botrytizadas como práctica definitoria de este estilo de vino dulce"
    if "cremant" in query or "crémant" in query:
        return "el material oficial relaciona el Crémant con el método tradicional, las variedades regionales y el perfil de acidez característico"
    if "madeira" in query:
        return "el material oficial describe el estufagem como el proceso térmico que distingue la crianza del Madeira y explica su longevidad"
    if ("chile" in query or "chilena" in query) and ("espumoso" in query or "clima fresco" in query):
        return "el material oficial vincula el clima fresco de ciertas regiones de Chile con la producción de espumosos de calidad"
    if lowered:
        return _clean_idea(text)
    return ""


def _exam_line(query: str, language: str, ideas: list[dict[str, str]]) -> str:  # noqa: C901
    lowered = query.lower()
    if language == "en":
        if "oxidative" in lowered and ("ageing" in lowered or "aging" in lowered):
            return "For exam purposes: state the practice (extended oxygen contact), explain the mechanism (aldehyde formation, especially acetaldehyde), and link the result — because that oxidation therefore develops nutty, dried-fruit and rancio complexity while reducing primary fruit and lightening colour."
        if "mechanical" in lowered and "harvest" in lowered:
            return "For exam purposes: name the process (mechanical harvesting), explain the mechanism (berry skin rupture before the winery), and draw the conclusion — because early oxidation of exposed juice therefore reduces aromatic freshness compared to careful hand-harvesting."
        if "destem" in lowered:
            return "For exam purposes: state that destemming removes stalks, explain why that matters (stalks add harsh green tannins), and connect the result — because their removal therefore produces softer, rounder tannins and a cleaner palate structure."
        if "sulphite" in lowered or "sulfite" in lowered or "so2" in lowered:
            return "For exam purposes: state the role of SO₂ (antioxidant and antimicrobial agent), then explain the risk of overuse — because excess sulphites suppress fermentation character too broadly and may leave reductive off-aromas (struck match, rubber), therefore precise dosing is essential."
        if "tirage" in lowered or "liqueur de tirage" in lowered:
            return "For exam purposes: define the liqueur de tirage (wine + sugar + yeast), explain the mechanism (second fermentation in sealed bottle), and state the effect — because the CO₂ produced cannot escape, the wine therefore becomes sparkling."
        if "pressure" in lowered and ("sparkling" in lowered or "atmosphe" in lowered):
            return "For exam purposes: link the CO₂ level to pressure classification — because wines below 3 atmospheres are classified as semi-sparkling (pétillant) and wines above 5 atmospheres as fully sparkling, the level of effervescence is therefore a direct function of tirage sugar quantity."
        if "cava" in lowered and "champagne" in lowered:
            return "For exam purposes: do not just say 'both use traditional method'. Explain the technical differences — grape varieties, climate, and minimum ageing requirements — and show how these produce distinct stylistic outcomes despite the shared production method."
        if "drainage" in lowered and "soil" in lowered:
            return "For exam purposes: explain the drainage-to-quality chain — soil texture controls water retention; because well-drained soils force roots deeper, vine vigour is therefore reduced and fruit concentration increases, supporting higher quality potential."
        if "frost" in lowered and ("spring" in lowered or "risk" in lowered):
            return "For exam purposes: explain the topographical mechanism — cold air is denser and flows downhill; because it accumulates in valley floors and hollows, spring frost risk is therefore highest in these low-lying positions and lowest on well-aired slopes."
        if "planting density" in lowered or ("density" in lowered and "plant" in lowered):
            return "For exam purposes: explain the resource-competition chain — higher density means each vine competes for fewer nutrients and water; because this restricts vigour, yields per vine are therefore lower and fruit concentration higher, supporting quality potential."
        if "tokaj" in lowered or "asz" in lowered:
            return "For exam purposes: name the distinguishing practice (addition of botrytised Aszú grapes to base wine), explain the mechanism (noble rot concentrates sugars, acids, and glycerol), and draw the conclusion — because partial fermentation of this paste therefore produces a wine of great sweetness, complexity, and ageing potential."
        if "cremant" in lowered or "crémant" in lowered:
            return "For exam purposes: explain what makes Crémant distinctive — traditional method production, regional grapes, and (for Crémant de Loire) Chenin Blanc's naturally high acidity — and link these to the stylistic outcome: fine, persistent mousse and marked freshness."
        if "madeira" in lowered:
            return "For exam purposes: explain the estufagem mechanism (controlled heating), link it to the effect (accelerated oxidation, development of tertiary aromas, caramelisation), and then connect to outcome — because this unique thermal process combined with high natural acidity therefore gives Madeira its exceptional longevity and complexity."
        if "sat" in lowered or "quality" in lowered:
            return "For exam purposes, make the quality claim and support it with balance, intensity, complexity, length, and evidence from the palate. Because the evidence supports the conclusion, this therefore points toward a clear, justified quality assessment."
        return "For exam purposes, state the observation, explain why the mechanism works — because that connection therefore links the causal factor to its outcome in the wine's style or quality."
    # Spanish paths
    if "tannin" in lowered:
        return "Para efectos del examen: no escribas solo 'tiene mucho tanino, por eso es mejor'. Escribe: 'tanino alto pero integrado, junto con concentración de fruta, balance, complexity y length, puede apoyar una quality assessment más alta'."
    if "acid" in lowered and "quality" in lowered:
        return "Para efectos del examen: no escribas 'alta acidity = baja calidad'. Escribe si la acidity está en balance con fruta, alcohol, sweetness/body y length, y explica cómo sostiene el estilo."
    if "oxidativ" in lowered and ("envejec" in lowered or "crianza" in lowered):
        return "Para efectos del examen: nombra la práctica (crianza oxidativa con contacto prolongado con el oxígeno), explica el mecanismo (formación de acetaldehído y otros aldehídos) y conecta el resultado — porque ese proceso desarrolla — por tanto — aromas a nueces, frutas secas y complejidad terciaria, con pérdida del carácter de fruta primaria y del color."
    if "vendimia mec" in lowered or ("vendimia" in lowered and "mec" in lowered):
        return "Para efectos del examen: nombra el proceso (vendimia mecánica), explica el mecanismo (rotura de la baya antes de llegar a bodega) y conecta el efecto — porque el mosto queda expuesto al oxígeno, la frescura aromática se reduce — por tanto — en comparación con una vendimia manual cuidadosa."
    if "despalillado" in lowered:
        return "Para efectos del examen: describe el despalillado (eliminación de raspones), explica el mecanismo (los raspones aportan taninos verdes y astringencia áspera) y conecta el resultado — porque su eliminación conduce — por tanto — a vinos con taninos más suaves y redondeados y una estructura de paladar más limpia."
    if "sulfit" in lowered or "so2" in lowered:
        return "Para efectos del examen: nombra el papel del SO₂ (agente antioxidante y antimicrobiano), explica el riesgo del exceso — porque un uso excesivo suprime demasiado ampliamente la actividad fermentativa y puede dejar aromas reductivos (cerilla, goma), por tanto la dosificación precisa es clave para preservar el carácter del vino."
    if "tiraje" in lowered or "licor de tiraje" in lowered:
        return "Para efectos del examen: define el licor de tiraje (vino + azúcar + levaduras), explica el mecanismo (segunda fermentación en botella cerrada) y el efecto — porque el CO₂ producido no puede escapar, el vino se convierte — por tanto — en espumoso."
    if ("espumoso" in lowered or "espumante" in lowered) and ("presi" in lowered or "atm" in lowered):
        return "Para efectos del examen: conecta el nivel de CO₂ con la clasificación — porque los vinos con menos de 3 atm se clasifican como semi-espumosos y los de más de 5 atm como espumosos completos, el nivel de efervescencia es — por tanto — función directa de la cantidad de azúcar en el tiraje."
    if "cava" in lowered and ("champagne" in lowered or "champan" in lowered):
        return "Para efectos del examen: no basta con decir 'los dos usan método tradicional'. Explica las diferencias técnicas (variedades, clima, períodos mínimos de crianza) y muestra cómo producen resultados estilísticos distintos a pesar del método compartido."
    if ("suelo" in lowered or "tierra" in lowered) and ("drenaje" in lowered or "drena" in lowered):
        return "Para efectos del examen: explica la cadena drenaje→calidad — la textura del suelo controla la retención de agua; porque un suelo bien drenado fuerza a las raíces a profundizar, el vigor de la vid se reduce — por tanto — y la concentración de la fruta aumenta, apoyando mayor potencial de calidad."
    if "helada" in lowered and ("primavera" in lowered or "riesgo" in lowered):
        return "Para efectos del examen: explica el mecanismo topográfico — el aire frío es más denso y desciende; porque se acumula en los puntos bajos del terreno, el riesgo de helada primaveral es — por tanto — mayor en valles y hondonadas y menor en laderas con buen drenaje del aire frío."
    if "plantaci" in lowered and ("densidad" in lowered or "alta" in lowered):
        return "Para efectos del examen: explica la cadena competencia→concentración — a mayor densidad de plantación, cada vid compite por menos recursos; porque eso limita el vigor, los rendimientos son — por tanto — menores y la concentración de la fruta mayor, lo que apoya el potencial de calidad."
    if "tokaji" in lowered or "tokay" in lowered or "asz" in lowered:
        return "Para efectos del examen: nombra la práctica distintiva (adición de uvas Aszú botrytizadas al vino base), explica el mecanismo (la podredumbre noble concentra azúcares, ácidos y glicerol) y conecta el resultado — porque la fermentación parcial de esa pasta produce — por tanto — un vino de gran dulzura, complejidad y potencial de guarda."
    if "cremant" in lowered or "crémant" in lowered:
        return "Para efectos del examen: explica qué distingue al Crémant — método tradicional, uvas regionales y (en el caso del Crémant de Loire) la acidez natural elevada del Chenin Blanc — y conecta esos factores con el perfil estilístico: burbuja fina y persistente, frescura marcada y buen equilibrio."
    if "madeira" in lowered:
        return "Para efectos del examen: explica el estufagem (calentamiento controlado), conecta el mecanismo (oxidación acelerada, desarrollo de aromas terciarios, caramelización) con el efecto — porque ese proceso térmico único combinado con la alta acidez natural confiere — por tanto — al Madeira su longevidad excepcional y su complejidad distintiva."
    if ("chile" in lowered or "chilena" in lowered) and ("espumoso" in lowered or "clima fresco" in lowered):
        return "Para efectos del examen: explica por qué el clima fresco de ciertas regiones chilenas favorece la producción de espumosos de calidad — las temperaturas nocturnas bajas conservan la acidez natural; porque esa acidez es la base estructural del espumoso, las regiones frescas de Chile ofrecen — por tanto — un punto de partida ideal para este estilo."
    if "sat" in lowered or "quality" in lowered:
        return "Para efectos del examen, formula la quality assessment con BICL: balance, intensity, complexity y length, y añade evidencia concreta del paladar. Porque esa evidencia respalda la conclusión, esto sugiere — por tanto — una quality assessment justificada, no basada en un solo rasgo aislado."
    return "Para efectos del examen, describe el rasgo, explica por qué ocurre (el mecanismo), y muestra cómo ese proceso conduce — por tanto — al efecto observable en el vino."


def _mini_practice(query: str, language: str) -> str:  # noqa: C901
    lowered = query.lower()
    if language == "en":
        if "tannin" in lowered:
            return "Rewrite this: 'More tannin means better wine' using balance, integration, and length."
        if "oxidative" in lowered and ("ageing" in lowered or "aging" in lowered):
            return "Write one sentence that links oxygen contact → aldehyde development → nutty/dried-fruit complexity in a fortified wine."
        if "mechanical" in lowered and "harvest" in lowered:
            return "Write one sentence: 'Because mechanical harvesting [mechanism], the wine therefore [effect]'."
        if "destem" in lowered:
            return "Write one sentence: 'Because destemming removes [what], fermentation therefore [outcome for tannin structure]'."
        if "sulphite" in lowered or "sulfite" in lowered or "so2" in lowered:
            return "Write one sentence connecting excess SO₂ → suppressed fermentation character → reductive off-aromas."
        if "tirage" in lowered or "liqueur de tirage" in lowered:
            return "Write one sentence: 'The liqueur de tirage causes [mechanism], which therefore [effect in the finished wine]'."
        if "pressure" in lowered and ("sparkling" in lowered or "atmosphe" in lowered):
            return "Complete this: 'Because the CO₂ level is below 3 atmospheres, the wine is classified as [?] and its mousse is therefore [?]'."
        if "drainage" in lowered and "soil" in lowered:
            return "Write one sentence linking soil drainage → root depth → vine vigour → fruit concentration."
        if "frost" in lowered:
            return "Write one sentence: 'Because cold air [movement], spring frost risk is therefore [highest/lowest] in [which positions?]'."
        if "planting density" in lowered or ("density" in lowered and "plant" in lowered):
            return "Write one sentence: 'Higher planting density causes [mechanism], which therefore [effect on fruit concentration]'."
        if "tokaj" in lowered or "asz" in lowered:
            return "Write one sentence: 'Because Botrytis cinerea [what it does to the grape], the resulting Tokaji Aszú therefore [style outcome]'."
        if "cremant" in lowered or "crémant" in lowered:
            return "Write one sentence linking Crémant de Loire's cool climate → high acidity in Chenin Blanc → sparkling wine style."
        if "madeira" in lowered:
            return "Write one sentence: 'Because estufagem [mechanism], Madeira therefore [style and longevity outcome]'."
        if "acid" in lowered:
            return "Rewrite this: 'High acidity means low quality' using balance and wine style."
        return "Write one sentence that links evidence to conclusion."
    # Spanish paths
    if "tannin" in lowered:
        return "Reescribe esta frase: 'más tanino significa mejor vino', usando balance, integración y length."
    if "cool climate" in lowered and "acid" in lowered:
        return "Escribe una frase que conecte clima fresco → maduración lenta → retención de acidity → frescura."
    if "oxidativ" in lowered and ("envejec" in lowered or "crianza" in lowered):
        return "Escribe una frase que conecte contacto con oxígeno → formación de acetaldehído → aromas a nueces y frutas secas en un vino generoso."
    if "vendimia mec" in lowered or ("vendimia" in lowered and "mec" in lowered):
        return "Completa esta frase: 'Porque la vendimia mecánica [mecanismo], el vino — por tanto — [efecto en la frescura aromática]'."
    if "despalillado" in lowered:
        return "Completa esta frase: 'Porque el despalillado elimina [qué], la fermentación extrae — por tanto — [efecto en la estructura tánica]'."
    if "sulfit" in lowered or "so2" in lowered:
        return "Escribe una frase que conecte exceso de SO₂ → supresión del carácter fermentativo → aromas reductivos en el vino."
    if "tiraje" in lowered or "licor de tiraje" in lowered:
        return "Completa esta frase: 'El licor de tiraje provoca [mecanismo], lo que — por tanto — [efecto en el vino terminado]'."
    if ("espumoso" in lowered or "espumante" in lowered) and ("presi" in lowered or "atm" in lowered):
        return "Completa esta frase: 'Porque el nivel de CO₂ es inferior a 3 atm, el vino se clasifica como [?] y su burbuja es — por tanto — [?]'."
    if "cava" in lowered and ("champagne" in lowered or "champan" in lowered):
        return "Escribe una frase que compare Cava y Champagne, nombrando una diferencia técnica concreta y su efecto estilístico."
    if ("suelo" in lowered or "tierra" in lowered) and ("drenaje" in lowered or "drena" in lowered):
        return "Escribe una frase que conecte textura del suelo → drenaje → profundidad de raíces → concentración de la fruta."
    if "helada" in lowered and ("primavera" in lowered or "riesgo" in lowered):
        return "Completa esta frase: 'Porque el aire frío [movimiento], el riesgo de helada primaveral es — por tanto — mayor en [qué posición topográfica]'."
    if "plantaci" in lowered and ("densidad" in lowered or "alta" in lowered):
        return "Escribe una frase que conecte alta densidad de plantación → competencia por recursos → concentración de la fruta."
    if "tokaji" in lowered or "tokay" in lowered or "asz" in lowered:
        return "Escribe una frase: 'Porque la Botrytis cinerea [qué hace a la uva], el Tokaji Aszú resultante — por tanto — [resultado estilístico]'."
    if "cremant" in lowered or "crémant" in lowered:
        return "Escribe una frase que conecte clima fresco del Loira → acidez natural elevada en Chenin Blanc → estilo del espumoso."
    if "madeira" in lowered:
        return "Completa esta frase: 'Porque el estufagem [mecanismo], el Madeira — por tanto — [resultado estilístico y de longevidad]'."
    if ("chile" in lowered or "chilena" in lowered) and ("espumoso" in lowered or "clima fresco" in lowered):
        return "Escribe una frase que conecte temperaturas nocturnas frescas en regiones chilenas → conservación de acidez → base ideal para espumoso de calidad."
    if "acid" in lowered:
        return "Reescribe esta frase: 'high acidity significa baja calidad', usando balance y estilo del vino."
    return "Escribe una frase que conecte evidencia con conclusión."


def _spanish_paraphrase(text: str) -> str:
    lowered = text.lower()
    if "tannin" in lowered:
        return "El tanino produce astringencia: una sensación táctil de sequedad y agarre, distinta del amargor. Puede coexistir con sabores amargos, pero WSET los evalúa por separado."
    if "acidity" in lowered:
        return "La acidity aporta frescura y estructura; su valor depende del balance con fruta, sweetness, alcohol, body y estilo."
    return text
