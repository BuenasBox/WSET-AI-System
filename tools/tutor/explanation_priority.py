"""Adaptive explanation priority utilities for the local Tutor.

This module is deterministic and local-only. It does not call LLMs, APIs,
embeddings, vector databases, or Examiner scoring.
"""

from __future__ import annotations

import re
from typing import Any


SEVERITY_WEIGHT = {"low": 0.2, "medium": 0.45, "high": 0.75, "critical": 0.9}
DEPTH_TO_STYLE = {"minimal": "concise", "standard": "standard", "deep": "detailed"}


def build_explanation_priority(package: dict[str, Any], confidence: float | None = None) -> dict[str, Any]:
    """Build a deterministic explanation priority plan from a context package."""
    matched_misconception = package.get("matched_misconception") or {}
    causal_chains = [item for item in package.get("forced_causal_chains", []) if isinstance(item, dict)]
    les_context = package.get("learner_state_context") or {}
    memory = les_context.get("pedagogical_memory") or {}
    resolved_confidence = _resolve_confidence(package, confidence)
    ranked = _rank_explanations(matched_misconception, causal_chains, les_context, resolved_confidence)
    cognitive_load = estimate_cognitive_load(package, ranked)
    top_ranked = ranked[:4]
    priority_score = _clamp(sum(item["score"] for item in top_ranked) / len(top_ranked) if top_ranked else 0.25)
    priority_score = _clamp(priority_score + _memory_priority_boost(memory))
    urgency = _urgency(priority_score, cognitive_load)
    return {
        "priority_score": round(priority_score, 2),
        "urgency": urgency,
        "recommended_depth": _recommended_depth(priority_score, cognitive_load, les_context),
        "cognitive_load_estimate": cognitive_load,
        "recommended_sequence": [item["id"] for item in ranked],
        "prioritized_explanations": ranked,
        "governance": {
            "safe_for_examiner": False,
            "examiner_scoring_allowed": False,
            "uses_llm": False,
            "uses_api": False,
            "uses_embeddings": False,
            "uses_vector_db": False,
        },
    }


def estimate_cognitive_load(package: dict[str, Any], ranked: list[dict[str, Any]] | None = None) -> str:
    """Estimate learner-facing cognitive load from package complexity."""
    ranked = ranked or []
    chain_steps = sum(len(item.get("steps", [])) for item in package.get("forced_causal_chains", []) if isinstance(item, dict))
    support_count = len([item for item in package.get("retrieved_context", []) if isinstance(item, dict)])
    weak_areas = len(_as_list((package.get("learner_state_context") or {}).get("known_weak_areas")))
    score = chain_steps + support_count + min(weak_areas, 5) + len(ranked)
    if score >= 12:
        return "high"
    if score >= 6:
        return "medium"
    return "low"


def calculate_tutor_evaluation_signals(answer_text: str, context_package: dict[str, Any]) -> dict[str, Any]:
    """Create Tutor-development metrics from a generated answer.

    These are not scores, grades, marks, or Examiner signals.
    """
    normalized = _normalize(answer_text)
    words = re.findall(r"[a-zA-ZáéíóúüñÁÉÍÓÚÜÑ]+", answer_text)
    causal_terms = re.findall(r"\b(causa|cause|mecanismo|mechanism|efecto|effect|porque|because|therefore|por tanto|leads?|results?|causes?|aumenta|reduce|increases?|decreases?)\b", normalized)
    misconception = context_package.get("matched_misconception") or {}
    corrected = str(misconception.get("corrected_understanding") or "").lower()
    correction_terms = [term for term in re.findall(r"[a-zA-Záéíóúüñ]+", corrected) if len(term) > 4]
    covered_terms = [term for term in correction_terms[:8] if term in normalized]
    sections = len(re.findall(r"^##\s+", answer_text, flags=re.MULTILINE))
    memory = (context_package.get("learner_state_context") or {}).get("pedagogical_memory") or {}
    retention_risks = memory.get("retention_risks") or []
    recurrent = memory.get("recurrent_misconceptions") or []
    learning_velocity = _memory_learning_velocity(memory)
    scaffolding_effectiveness = min(1.0, (len(set(causal_terms)) / 4) * 0.6 + (len(covered_terms) / max(1, min(len(correction_terms), 8)) if misconception else 1.0) * 0.4)
    return {
        "explanation_density": round(len(causal_terms) / max(1, len(words)) * 100, 2),
        "causal_coherence": round(min(1.0, len(set(causal_terms)) / 4), 2),
        "misconception_coverage": round(len(covered_terms) / max(1, min(len(correction_terms), 8)), 2) if misconception else 1.0,
        "reasoning_depth_score": round(min(1.0, (sections / 6) * 0.4 + min(len(causal_terms), 8) / 8 * 0.6), 2),
        "retention_risk": round(max([float(item.get("retention_risk", 0) or 0) for item in retention_risks if isinstance(item, dict)] or [0.0]), 2),
        "learning_velocity": round(learning_velocity, 2),
        "misconception_persistence": round(max([float(item.get("persistence", 0) or 0) for item in recurrent if isinstance(item, dict)] or [0.0]), 2),
        "scaffolding_effectiveness": round(scaffolding_effectiveness, 2),
        "safe_for_examiner": False,
        "examiner_scoring_allowed": False,
    }


def _rank_explanations(
    misconception: dict[str, Any],
    causal_chains: list[dict[str, Any]],
    les_context: dict[str, Any],
    confidence: float,
) -> list[dict[str, Any]]:
    ranked: list[dict[str, Any]] = []
    if misconception:
        severity = str(misconception.get("severity") or "medium").lower()
        ranked.append(
            {
                "id": str(misconception.get("misconception_id") or "matched_misconception"),
                "type": "misconception",
                "score": round(_clamp(0.35 + SEVERITY_WEIGHT.get(severity, 0.45) + (1 - confidence) * 0.2), 2),
                "reason": f"{severity}_severity_misconception",
            }
        )
    weak_text = " ".join(_as_list(les_context.get("known_weak_areas"))).lower()
    for chain in causal_chains:
        chain_id = str(chain.get("node_id") or chain.get("chain_id") or chain.get("id") or "causal_chain")
        chain_text = " ".join([chain_id, str(chain.get("title") or ""), str(chain.get("sat_relevance") or "")]).lower()
        score = 0.35
        if any(token and token in weak_text for token in re.split(r"[_:\-\s]+", chain_text) if len(token) > 4):
            score += 0.25
        if chain.get("sat_relevance"):
            score += 0.15
        score += min(0.25, len(chain.get("steps", [])) * 0.05)
        ranked.append({"id": chain_id, "type": "causal_chain", "score": round(_clamp(score), 2), "reason": "causal_support"})
    for weakness in _as_list(les_context.get("known_weak_areas"))[:5]:
        ranked.append({"id": str(weakness), "type": "learner_weakness", "score": 0.45, "reason": "les_weak_area"})
    ranked.sort(key=lambda item: (item["score"], item["type"] == "misconception"), reverse=True)
    return ranked


def _resolve_confidence(package: dict[str, Any], confidence: float | None) -> float:
    if confidence is not None:
        return _clamp(float(confidence))
    for container in (package.get("orchestrator_decision"), package.get("tutor_directive"), package.get("matched_misconception")):
        if isinstance(container, dict) and container.get("confidence") is not None:
            return _clamp(float(container.get("confidence") or 0))
    return 0.65 if package.get("matched_misconception") else 0.8


def _recommended_depth(priority_score: float, cognitive_load: str, les_context: dict[str, Any]) -> str:
    mastery = str(les_context.get("mastery") or les_context.get("current_mastery") or "").lower()
    memory = les_context.get("pedagogical_memory") or {}
    if _has_persistent_misconception(memory) or memory.get("preferred_depth") == "deep":
        return "deep" if cognitive_load != "high" else "standard"
    if cognitive_load == "high":
        return "standard"
    if mastery in {"high", "advanced", "strong"} and priority_score < 0.6:
        return "minimal"
    if priority_score >= 0.7:
        return "deep"
    if priority_score <= 0.35:
        return "minimal"
    return "standard"


def _memory_priority_boost(memory: dict[str, Any]) -> float:
    boost = 0.0
    if memory.get("low_mastery_concepts"):
        boost += 0.08
    if memory.get("retention_risks"):
        boost += 0.08
    if _has_persistent_misconception(memory):
        boost += 0.12
    return boost


def _has_persistent_misconception(memory: dict[str, Any]) -> bool:
    return any(
        isinstance(item, dict) and float(item.get("persistence", 0) or 0) >= 0.6
        for item in memory.get("recurrent_misconceptions", []) or []
    )


def _memory_learning_velocity(memory: dict[str, Any]) -> float:
    low_mastery_count = len(memory.get("low_mastery_concepts") or [])
    mastered_count = len(memory.get("mastered_concepts") or [])
    return _clamp(0.5 + mastered_count * 0.05 - low_mastery_count * 0.04)


def _urgency(priority_score: float, cognitive_load: str) -> str:
    if priority_score >= 0.75:
        return "high"
    if priority_score >= 0.5 or cognitive_load == "high":
        return "medium"
    return "low"


def _as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _clamp(value: float) -> float:
    return max(0.0, min(1.0, value))


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()
