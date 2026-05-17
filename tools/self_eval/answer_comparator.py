"""Deterministic Tutor self-evaluation comparator.

This module does not grade, score, or emulate WSET Examiner behavior. It only
labels Tutor-development diagnostics from local answer text.
"""

from __future__ import annotations

import re
from typing import Any


COGNITIVE_ERROR_LABELS = (
    "missing_causal_link",
    "vague_claim",
    "unsupported_conclusion",
    "missing_exam_language",
    "incomplete_balance_justification",
    "weak_sat_commitment",
    "misconception_unresolved",
    "missing_counterexample",
    "retrieval_gap",
    "weak_context_support",
    "shallow_retrieval",
    "shallow_reasoning",
    "misconception_reinforcement_risk",
    "weak_exam_register",
)

COGNITIVE_ERROR_LABEL_METADATA = {
    "missing_causal_link": {
        "label": "missing_causal_link",
        "label_es": "falta_enlace_causal",
        "description_es": "La respuesta no conecta claramente causa, mecanismo y efecto.",
        "severity_hint": "high",
        "learner_facing": True,
    },
    "vague_claim": {
        "label": "vague_claim",
        "label_es": "afirmacion_vaga",
        "description_es": "La respuesta usa una afirmacion general sin suficiente precision.",
        "severity_hint": "medium",
        "learner_facing": True,
    },
    "unsupported_conclusion": {
        "label": "unsupported_conclusion",
        "label_es": "conclusion_sin_apoyo",
        "description_es": "La conclusion no esta suficientemente conectada con evidencia.",
        "severity_hint": "high",
        "learner_facing": True,
    },
    "missing_exam_language": {
        "label": "missing_exam_language",
        "label_es": "falta_lenguaje_de_examen",
        "description_es": "La respuesta no usa suficiente formulacion util para examen.",
        "severity_hint": "medium",
        "learner_facing": True,
    },
    "incomplete_balance_justification": {
        "label": "incomplete_balance_justification",
        "label_es": "justificacion_de_balance_incompleta",
        "description_es": "La justificacion de balance no integra suficientes elementos SAT.",
        "severity_hint": "medium",
        "learner_facing": True,
    },
    "weak_sat_commitment": {
        "label": "weak_sat_commitment",
        "label_es": "compromiso_sat_debil",
        "description_es": "La respuesta no formula una conclusion SAT suficientemente clara.",
        "severity_hint": "medium",
        "learner_facing": True,
    },
    "misconception_unresolved": {
        "label": "misconception_unresolved",
        "label_es": "malentendido_no_resuelto",
        "description_es": "La respuesta no corrige completamente el malentendido detectado.",
        "severity_hint": "high",
        "learner_facing": True,
    },
    "missing_counterexample": {
        "label": "missing_counterexample",
        "label_es": "falta_contraejemplo",
        "description_es": "La respuesta necesita un contraejemplo para evitar una regla absoluta.",
        "severity_hint": "medium",
        "learner_facing": True,
    },
    "retrieval_gap": {
        "label": "retrieval_gap",
        "label_es": "brecha_de_recuperacion",
        "description_es": "El contexto recuperado no aporta suficiente soporte relevante.",
        "severity_hint": "high",
        "learner_facing": False,
    },
    "weak_context_support": {
        "label": "weak_context_support",
        "label_es": "soporte_contextual_debil",
        "description_es": "Hay poco contexto util para sostener la respuesta.",
        "severity_hint": "medium",
        "learner_facing": False,
    },
    "shallow_retrieval": {
        "label": "shallow_retrieval",
        "label_es": "recuperacion_superficial",
        "description_es": "El contexto recuperado tiene senales debiles de prioridad o profundidad.",
        "severity_hint": "medium",
        "learner_facing": False,
    },
    "shallow_reasoning": {
        "label": "shallow_reasoning",
        "label_es": "razonamiento_superficial",
        "description_es": "La explicacion no desarrolla suficientemente el mecanismo.",
        "severity_hint": "medium",
        "learner_facing": True,
    },
    "misconception_reinforcement_risk": {
        "label": "misconception_reinforcement_risk",
        "label_es": "riesgo_de_reforzar_malentendido",
        "description_es": "La respuesta puede repetir el malentendido sin correccion clara.",
        "severity_hint": "high",
        "learner_facing": False,
    },
    "weak_exam_register": {
        "label": "weak_exam_register",
        "label_es": "registro_de_examen_debil",
        "description_es": "El tono o vocabulario no esta suficientemente alineado con examen.",
        "severity_hint": "medium",
        "learner_facing": True,
    },
}


def compare_answer(
    question: dict[str, Any],
    answer_text: str,
    context_package: dict[str, Any],
    strictness: str = "hard",
) -> dict[str, Any]:
    """Compare a Tutor attempt to expected answer structure deterministically."""
    strictness = _normalize_strictness(strictness)
    normalized = _normalize(answer_text)
    expected_keywords = _as_list(question.get("expected_keywords"))
    expected_links = _as_list(question.get("expected_causal_links"))
    expected_topics = _as_list(question.get("expected_topics"))
    expected_reasoning = str(question.get("expected_reasoning_type") or "").lower()

    present_keywords = [term for term in expected_keywords if _contains(normalized, term)]
    missing_keywords = [term for term in expected_keywords if term not in present_keywords]
    present_links = [link for link in expected_links if _link_present(normalized, link)]
    missing_links = [link for link in expected_links if link not in present_links]
    present_topics = [topic for topic in expected_topics if _topic_present(normalized, topic)]
    missing_topics = [topic for topic in expected_topics if topic not in present_topics]

    labels = []
    if missing_links or _requires_causal_structure(question, strictness) and not _has_cause_mechanism_effect(normalized, strictness):
        labels.append("missing_causal_link")
        if _requires_causal_structure(question, strictness):
            missing_links = missing_links or ["cause -> mechanism -> effect"]
    if _requires_causal_structure(question, strictness) and not _has_mechanism_explanation(normalized):
        labels.append("shallow_reasoning")
    if _has_vague_claim(normalized):
        labels.append("vague_claim")
    if _has_unsupported_conclusion(normalized) or _lists_observations_without_inference(normalized, strictness):
        labels.append("unsupported_conclusion")
    if _requires_exam_language(question, strictness) and not _has_exam_language(normalized, strictness):
        labels.append("missing_exam_language")
    if question.get("question_type") == "sat" and not _has_balance_justification(normalized, strictness):
        labels.append("incomplete_balance_justification")
    if question.get("question_type") == "sat" and not _has_commitment_language(normalized):
        labels.append("weak_sat_commitment")
    if _misconception_unresolved(question, normalized, context_package):
        labels.append("misconception_unresolved")
    if _misconception_reinforcement_risk(normalized, context_package):
        labels.append("misconception_reinforcement_risk")
    if _needs_counterexample(question) and "no siempre" not in normalized and "not always" not in normalized:
        labels.append("missing_counterexample")
    retrieval_audit = _audit_retrieval(context_package, strictness)
    if retrieval_audit["retrieval_gap"]:
        labels.append("retrieval_gap")
    if retrieval_audit["weak_context_support"]:
        labels.append("weak_context_support")
    if retrieval_audit["shallow_retrieval"]:
        labels.append("shallow_retrieval")
    if expected_keywords and len(present_keywords) < max(1, len(expected_keywords) // 2):
        labels.append("shallow_reasoning")
    if _weak_exam_register(normalized, question, strictness):
        labels.append("weak_exam_register")

    labels = [label for label in COGNITIVE_ERROR_LABELS if label in set(labels)]
    strengths = _strengths(present_keywords, present_links, present_topics, expected_reasoning, normalized, strictness)
    return {
        "question_id": question.get("question_id", ""),
        "question_type": question.get("question_type", "theory"),
        "strengths": strengths,
        "present_keywords": present_keywords,
        "missing_keywords": missing_keywords,
        "present_causal_links": present_links,
        "missing_causal_links": missing_links,
        "present_topics": present_topics,
        "missing_official_concepts": missing_topics,
        "expected_reasoning_type_present": _reasoning_present(expected_reasoning, normalized, context_package),
        "failure_labels": labels,
        "strictness": strictness,
        "difficulty": question.get("difficulty", "intermediate"),
        "vague_claims": ["claim needs more support"] if "vague_claim" in labels else [],
        "unsupported_conclusions": ["conclusion is not fully tied to evidence"] if "unsupported_conclusion" in labels else [],
        "likely_misconception_gaps": [question.get("question_id", "")] if "misconception_unresolved" in labels else [],
        "retrieval_weaknesses": _retrieval_weaknesses(context_package, missing_keywords, missing_links, retrieval_audit),
    }


def _strengths(
    present_keywords: list[str],
    present_links: list[str],
    present_topics: list[str],
    expected_reasoning: str,
    normalized: str,
    strictness: str,
) -> list[str]:
    strengths = []
    if present_keywords:
        strengths.append("expected_keywords_present")
    if present_links:
        strengths.append("causal_links_present")
    if present_topics:
        strengths.append("expected_topics_present")
    if expected_reasoning and expected_reasoning in normalized:
        strengths.append("reasoning_type_visible")
    if _has_exam_language(normalized, strictness):
        strengths.append("exam_language_present")
    return strengths


def _retrieval_weaknesses(
    context_package: dict[str, Any],
    missing_keywords: list[str],
    missing_links: list[str],
    retrieval_audit: dict[str, bool],
) -> list[str]:
    weaknesses = []
    contexts = context_package.get("retrieved_context") or []
    if not contexts:
        weaknesses.append("no_retrieved_context")
    if missing_keywords:
        weaknesses.append("missing_keyword_support")
    if missing_links:
        weaknesses.append("missing_causal_link_support")
    if not any(item.get("context_type") == "misconception_node" for item in contexts if isinstance(item, dict)):
        if context_package.get("pedagogical_act") == "misconception_intervention":
            weaknesses.append("missing_forced_misconception_node")
    if retrieval_audit["pedagogical_only"]:
        weaknesses.append("pedagogical_only_no_official_support")
    if retrieval_audit["weak_context_support"]:
        weaknesses.append("weak_context_support")
    if retrieval_audit["shallow_retrieval"]:
        weaknesses.append("shallow_retrieval")
    return weaknesses


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", str(text or "").lower()).strip()


def _contains(normalized: str, term: str) -> bool:
    term = _normalize(term)
    return term in normalized


def _link_present(normalized: str, link: str) -> bool:
    parts = [part.strip() for part in re.split(r"->|→|=>|causes|leads to", str(link)) if part.strip()]
    if len(parts) < 2:
        return _contains(normalized, link)
    return all(_contains(normalized, part) for part in parts)


def _topic_present(normalized: str, topic: str) -> bool:
    topic = _normalize(topic).replace("_", " ")
    return topic in normalized or any(part and part in normalized for part in topic.split())


def _reasoning_present(expected_reasoning: str, normalized: str, context_package: dict[str, Any]) -> bool:
    if not expected_reasoning:
        return True
    context_text = _normalize(str(context_package.get("retrieval_plan", {})) + str(context_package.get("retrieved_context", [])))
    return expected_reasoning in normalized or expected_reasoning in context_text


def _has_vague_claim(normalized: str) -> bool:
    vague_terms = ("good quality", "better wine", "buen vino", "mejor vino")
    return any(term in normalized for term in vague_terms) and not _has_balance_justification(normalized)


def _has_unsupported_conclusion(normalized: str) -> bool:
    conclusion_terms = ("quality assessment", "calidad", "quality")
    evidence_terms = ("because", "porque", "balance", "intensity", "complexity", "length", "evidence", "evidencia")
    return any(term in normalized for term in conclusion_terms) and not any(term in normalized for term in evidence_terms)


def _has_exam_language(normalized: str, strictness: str = "hard") -> bool:
    required = ("balance", "quality", "calidad", "concentration", "concentración", "integration", "integración", "complexity", "length")
    basic = any(term in normalized for term in ("sat", "examen", "exam", "quality assessment", "para efectos del examen"))
    if strictness == "normal":
        return basic
    return basic and any(term in normalized for term in required)


def _has_balance_justification(normalized: str, strictness: str = "hard") -> bool:
    terms = ("balance", "intensity", "complexity", "length")
    present = sum(1 for term in terms if term in normalized)
    if strictness == "brutal":
        return present >= 4 or "quality assessment" in normalized and present >= 3
    return present >= 3 or "quality assessment" in normalized and present >= 2


def _misconception_unresolved(question: dict[str, Any], normalized: str, context_package: dict[str, Any]) -> bool:
    expected = " ".join(_as_list(question.get("expected_keywords")) + _as_list(question.get("expected_causal_links"))).lower()
    if "misconception" not in expected and not context_package.get("matched_misconception"):
        return False
    correction_terms = ("no significa", "not automatically", "no siempre", "not always", "not the same", "distinta", "separately", "no exactamente")
    replacement_terms = ("marco wset", "correcto", "replacement", "en su lugar", "astringencia", "balance")
    return not (any(term in normalized for term in correction_terms) and any(term in normalized for term in replacement_terms))


def _misconception_reinforcement_risk(normalized: str, context_package: dict[str, Any]) -> bool:
    misconception = context_package.get("matched_misconception") or {}
    text = _normalize(misconception.get("misconception", ""))
    if not text:
        return False
    risky_tokens = [token for token in re.findall(r"[a-záéíóúñ]+", text) if len(token) > 4]
    risk_phrase_present = sum(1 for token in risky_tokens if token in normalized) >= max(2, len(risky_tokens) // 2)
    has_correction = any(term in normalized for term in ("no significa", "not automatically", "no exactamente", "not the same"))
    return risk_phrase_present and not has_correction


def _needs_counterexample(question: dict[str, Any]) -> bool:
    text = _normalize(question.get("question_text", ""))
    return "always" in text or "siempre" in text or "automatically" in text


def _retrieval_gap(context_package: dict[str, Any]) -> bool:
    contexts = context_package.get("retrieved_context") or []
    return len(contexts) == 0


def _audit_retrieval(context_package: dict[str, Any], strictness: str) -> dict[str, bool]:
    contexts = [item for item in context_package.get("retrieved_context", []) if isinstance(item, dict)]
    non_forced = [item for item in contexts if item.get("context_type") != "misconception_node"]
    threshold = {"normal": 1, "hard": 3, "brutal": 4}[strictness]
    official = [item for item in contexts if str(item.get("source_type") or item.get("transcript_source") or "") in {"official_wset", "official_wset_extracted"}]
    pedagogical = [
        item
        for item in contexts
        if item.get("context_type") == "retrieval_sandbox_chunk"
        or str(item.get("source_filename") or "").endswith(".srt")
        or str(item.get("source_type") or "") in {"manual_curated_srt", "youtube_transcript"}
    ]
    priority_text = " ".join(" ".join(item.get("why_retrieved", [])) + " " + str(item.get("retrieval_priority", "")) for item in contexts).lower()
    high_priority = priority_text.count("high") + priority_text.count("golden")
    # Forced causal chains are high-priority curated content: count them toward
    # priority signal so that chain-injected answers are not penalised as shallow.
    forced_chains = [c for c in (context_package.get("forced_causal_chains") or []) if isinstance(c, dict)]
    if forced_chains:
        high_priority += len(forced_chains)
    return {
        "retrieval_gap": len(contexts) == 0 or (strictness == "brutal" and pedagogical and not official),
        "weak_context_support": len(non_forced) < threshold,
        "shallow_retrieval": non_forced and high_priority == 0,
        "pedagogical_only": bool(pedagogical) and not official,
    }


def _requires_causal_structure(question: dict[str, Any], strictness: str) -> bool:
    if strictness == "normal":
        return bool(_as_list(question.get("expected_causal_links")))
    return question.get("question_type") in {"theory", "sat"} or bool(_as_list(question.get("expected_causal_links")))


def _has_cause_mechanism_effect(normalized: str, strictness: str) -> bool:
    # Structured causal chain output (CAUSA/MECANISMO/EFECTO labels from _render_causal_chain)
    # is valid causal structure even when its step texts lack explicit connector words.
    # Recognise at least 2 of the 3 core labels being present, plus an effect term.
    chain_labels = ("causa:", "mecanismo:", "efecto:", "cause:", "mechanism:", "effect:")
    effect_terms_present = any(term in normalized for term in ("efecto", "effect", "resultado", "result", "frescura", "quality", "calidad", "estructura", "length", "complexity", "alcohol"))
    if sum(1 for label in chain_labels if label in normalized) >= 2 and effect_terms_present:
        return True
    connectors = ("because", "therefore", "leads to", "results in", "causes", "increases", "decreases", "porque", "por eso", "por tanto", "conduce", "provoca", "aumenta", "disminuye", "→")
    connector_count = sum(1 for term in connectors if term in normalized)
    mechanism_terms = ("mechanism", "mecanismo", "maduración", "retención", "fermentación", "oxidación", "flor", "extracción", "phenolic", "fenólico", "ácido", "astringencia")
    effect_terms = ("therefore", "por tanto", "results", "resultado", "frescura", "quality", "calidad", "estructura", "length", "complexity", "alcohol", "sweetness")
    required_connectors = 2 if strictness == "brutal" else 1
    return connector_count >= required_connectors and any(term in normalized for term in mechanism_terms) and any(term in normalized for term in effect_terms)


def _has_mechanism_explanation(normalized: str) -> bool:
    mechanism_terms = ("mecanismo", "because", "porque", "leads to", "results in", "causes", "→", "retención", "maduración", "extracción", "fermentación", "oxidación", "flor", "astringencia")
    return any(term in normalized for term in mechanism_terms)


def _has_commitment_language(normalized: str) -> bool:
    return any(term in normalized for term in ("likely", "therefore", "this suggests", "this points toward", "probable", "por tanto", "esto sugiere", "apunta a", "indica"))


def _lists_observations_without_inference(normalized: str, strictness: str) -> bool:
    if strictness == "normal":
        return False
    observation_terms = ("acidity", "tannin", "body", "alcohol", "fruit", "aroma", "flavour", "appearance")
    has_observations = sum(1 for term in observation_terms if term in normalized) >= 3
    has_inference = _has_commitment_language(normalized) or any(term in normalized for term in ("because", "porque", "therefore", "por tanto"))
    return has_observations and not has_inference


def _requires_exam_language(question: dict[str, Any], strictness: str) -> bool:
    if question.get("question_type") == "sat":
        return True
    if strictness == "brutal" and question.get("question_type") == "theory":
        return True
    return False


def _weak_exam_register(normalized: str, question: dict[str, Any], strictness: str) -> bool:
    if strictness == "normal":
        return False
    # "ok" as a bare 2-char substring matches wine terms like "tokaji" (t-ok-aji); require
    # a leading space so mid-word occurrences in wine names do not false-positive.
    conversational = ("basically", "kind of", "sort of", "muy fácil", "simplemente", "bueno,", " ok")
    if any(term in normalized for term in conversational):
        return True
    if strictness == "brutal" and question.get("question_type") in {"theory", "sat"}:
        register_terms = ("para efectos del examen", "wset", "quality assessment", "balance", "calidad", "evidencia")
        return not any(term in normalized for term in register_terms)
    return False


def _normalize_strictness(strictness: str) -> str:
    return strictness if strictness in {"normal", "hard", "brutal"} else "hard"


def _as_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value if str(item).strip()]
    return [str(value)] if str(value).strip() else []
