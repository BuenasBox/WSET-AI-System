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
        lines = [
            f"# Tutor Draft: {query}",
            "",
            "## 1. Direct Correction",
            direct_correction,
            "",
            "## 2. Why The Misconception Is Tempting",
            confusion,
            "",
            "## 3. Correct WSET Framing",
            framing,
            "",
            "## 4. Cause/Effect Explanation",
            cause,
            "",
            "## 5. How To Write It For Marks",
            exam,
            "",
            "## 6. Mini Practice",
            _mini_practice(query, language),
            "",
            source_note,
            support,
            "",
            DISCLAIMER_EN,
        ]
    else:
        lines = [
            f"# Borrador del Tutor: {_display_query(query, language)}",
            "",
            "## 1. Corrección directa",
            direct_correction,
            "",
            "## 2. Por qué esa idea confunde",
            confusion,
            "",
            "## 3. Marco WSET correcto",
            framing,
            "",
            "## 4. Cadena causa → efecto",
            cause,
            "",
            "## 5. Cómo escribirlo para puntos",
            exam,
            "",
            "## 6. Mini práctica",
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
    direct = _normal_direct_answer(query, language)
    framing = _wset_framing_line(query, language, "", ideas)
    cause = _cause_effect_line(package, language, ideas, depth)
    exam = _exam_line(query, language, ideas)
    if depth == "minimal":
        support = _compress_explanation(support, depth)
        framing = _compress_explanation(framing, depth)
        exam = _compress_explanation(exam, depth)

    if language == "en":
        lines = [
            f"# Tutor Draft: {query}",
            "",
            "## 1. Short Direct Answer",
            direct,
            "",
            "## 2. WSET Framing",
            framing,
            "",
            "## 3. Cause/Effect Explanation",
            cause,
            "",
            "## 4. Exam Formulation",
            exam,
            "",
            "## 5. Mini Practice",
            _mini_practice(query, language),
            "",
            source_note,
            support,
            "",
            DISCLAIMER_EN,
        ]
    else:
        lines = [
            f"# Borrador del Tutor: {_display_query(query, language)}",
            "",
            "## 1. Respuesta directa",
            direct,
            "",
            "## 2. Marco WSET",
            framing,
            "",
            "## 3. Explicación causa → efecto",
            cause,
            "",
            "## 4. Formulación de examen",
            exam,
            "",
            "## 5. Mini práctica",
            _mini_practice(query, language),
            "",
            source_note,
            support,
            "",
            DISCLAIMER_ES,
        ]
    return "\n".join(line for line in lines if line is not None)


def _normal_direct_answer(query: str, language: str) -> str:
    lowered = query.lower()
    if language == "en":
        if "cool climate" in lowered and "acid" in lowered:
            return "Cool climate generally helps retain acidity because grapes ripen more slowly and lose less acid before harvest."
        if "quality" in lowered and "sat" in lowered:
            return "In SAT, justify quality by linking your conclusion to balance, intensity, complexity, length, and the condition of the fruit and structure."
        return "Answer the question through the WSET framework, then support the conclusion with clear evidence."
    if "cool climate" in lowered and "acid" in lowered:
        return "Un clima fresco suele conservar más acidity porque la uva madura más lentamente y pierde menos ácido antes de la vendimia."
    if "quality" in lowered and "sat" in lowered:
        return "En SAT, justifica la quality assessment vinculando tu conclusión con balance, intensity, complexity, length y la condición de la fruta y la estructura."
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
        return "Cause → effect: identify the driving factor, explain why and how the mechanism operates — because that causal relationship therefore connects directly to the observable result in the wine's style or quality."
    if "tannin" in query or "tannin" in why:
        return "Cadena: compuestos fenólicos de pieles, pepitas o extracción aportan tanino → el tanino se percibe como sequedad/astringencia → puede apoyar la estructura si está maduro e integrado, pero no garantiza calidad por sí solo."
    if "cool climate" in query or ("acid" in query and "climate" in idea_text):
        return "Cadena: clima fresco → maduración más lenta → mayor retención de ácidos → más acidity y sensación de frescura en el vino."
    if "acid" in query:
        return "Cadena: acidity aporta frescura y tensión → su efecto en la calidad depende de balance, fruta, azúcar, alcohol y body."
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


def _official_idea_from_text(text: str, package: dict[str, Any]) -> str:
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
    if lowered:
        return _clean_idea(text)
    return ""


def _exam_line(query: str, language: str, ideas: list[dict[str, str]]) -> str:
    lowered = query.lower()
    if language == "en":
        if "sat" in lowered or "quality" in lowered:
            return "For exam purposes, make the quality claim and support it with balance, intensity, complexity, length, and evidence from the palate."
        return "For exam purposes, state the observation, explain why the mechanism works — because that connection therefore links the causal factor to its outcome in the wine's style or quality."
    if "tannin" in lowered:
        return "Para efectos del examen: no escribas solo 'tiene mucho tanino, por eso es mejor'. Escribe: 'tanino alto pero integrado, junto con concentración de fruta, balance, complexity y length, puede apoyar una quality assessment más alta'."
    if "acid" in lowered and "quality" in lowered:
        return "Para efectos del examen: no escribas 'alta acidity = baja calidad'. Escribe si la acidity está en balance con fruta, alcohol, sweetness/body y length, y explica cómo sostiene el estilo."
    if "sat" in lowered or "quality" in lowered:
        return "Para efectos del examen, formula la quality assessment con BICL: balance, intensity, complexity y length, y añade evidencia concreta del paladar."
    return "Para efectos del examen, describe el rasgo, explica por qué ocurre (el mecanismo), y muestra cómo ese proceso conduce — por tanto — al efecto observable en el vino."


def _mini_practice(query: str, language: str) -> str:
    lowered = query.lower()
    if language == "en":
        if "tannin" in lowered:
            return "Rewrite this: 'More tannin means better wine' using balance, integration, and length."
        if "acid" in lowered:
            return "Rewrite this: 'High acidity means low quality' using balance and wine style."
        return "Write one sentence that links evidence to conclusion."
    if "tannin" in lowered:
        return "Reescribe esta frase: 'más tanino significa mejor vino', usando balance, integración y length."
    if "cool climate" in lowered and "acid" in lowered:
        return "Escribe una frase que conecte clima fresco → maduración lenta → retención de acidity → frescura."
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
