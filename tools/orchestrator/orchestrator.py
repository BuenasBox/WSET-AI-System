"""Minimal Brain local orchestrator."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING, Any

from tools.constants import (
    CLOUD_SERVICES_ACTIVE,
    CONTEXT_PACKAGES_DIR,
    EXAMINER_SCORING_ALLOWED,
    PROJECT_ROOT,
    SAFE_FOR_EXAMINER,
    USES_API,
    USES_EMBEDDINGS,
    USES_LLM,
    USES_VECTOR_DB,
)
from tools.retrieval.tutor_retrieval_sandbox import run_retrieval_sandbox

from .learner_state import (
    DEFAULT_LES_PATH,
    DEFAULT_SESSION_STAGING_PATH,
    build_les_context,
    ensure_learner_files,
    load_learner_state,
    write_session_staging,
)
from .misconception_prepass import (
    DEFAULT_MISCONCEPTION_DIR,
    detect_misconception,
    load_misconception_nodes,
)
from .session_ledger import append_to_ledger
from .strategic_planner import run_strategic_planner

if TYPE_CHECKING:
    from .protocols import (
        AnswerBuilderProtocol,
        LearnerStateProtocol,
        RetrievalProtocol,
        ScaffoldingProtocol,
    )


DEFAULT_CONTEXT_PACKAGE_DIR = CONTEXT_PACKAGES_DIR
_retrieval_contract: "RetrievalProtocol"
_learner_state_contract: "LearnerStateProtocol"
_answer_builder_contract: "AnswerBuilderProtocol"
_scaffolding_contract: "ScaffoldingProtocol"


def run_orchestrator(
    query: str,
    top_k: int = 10,
    language: str = "es",
    les_path: Path = DEFAULT_LES_PATH,
    misconception_dir: Path = DEFAULT_MISCONCEPTION_DIR,
    staging_path: Path = DEFAULT_SESSION_STAGING_PATH,
    context_package_dir: Path = DEFAULT_CONTEXT_PACKAGE_DIR,
    root: Path = PROJECT_ROOT,
) -> dict[str, Any]:
    """Run the local Minimal Brain cognitive loop for one student query."""
    ensure_learner_files(les_path=les_path, staging_path=staging_path)
    language = _normalize_language(language)
    learner_state = load_learner_state(les_path)
    les_context = build_les_context(learner_state)
    pedagogical_boost = _pedagogical_priority_boost(les_context)
    prepass = detect_misconception(query, misconception_dir)
    # Phase 1B: strategic planner — informational only, inert.
    # Runs after LES + prepass so prepass_result is available.
    # Output is NOT injected into context_package to guarantee zero
    # impact on retrieval ranking, Tutor rendering, and snapshot outputs.
    strategic_plan = run_strategic_planner(
        memory_summary=les_context.get("pedagogical_memory"),
        les_context=les_context,
        prepass_result=prepass,
    )

    if prepass["detected"]:
        decision = {
            "route": "misconception_prepass",
            "reason": "misconception_detected",
            "matched_misconception_id": prepass["matched_misconception_id"],
            "confidence": prepass.get("confidence", 0.0),
        }
        tutor_directive = {
            "pedagogical_act": "misconception_intervention",
            "forced_retrieval_nodes": [prepass["matched_misconception_id"]],
            "intervention_type": prepass["intervention_type"],
            "corrected_understanding": prepass["corrected_understanding"],
            "confidence": prepass.get("confidence", 0.0),
            "safe_for_examiner": SAFE_FOR_EXAMINER,
        }
        recommended_update = {
            "append_recent_misconception": prepass["matched_misconception_id"],
            "increase_attention_to": prepass["severity"],
        }
        matched_node = load_misconception_node(
            prepass["matched_misconception_id"],
            misconception_dir,
        )
        retrieval_query = _misconception_retrieval_query(query, matched_node)
    else:
        decision = {
            "route": "normal_tutor",
            "reason": "no_misconception_detected",
            "matched_misconception_id": None,
            "confidence": prepass.get("confidence", 0.0),
        }
        tutor_directive = {
            "pedagogical_act": "answer_normally",
            "forced_retrieval_nodes": [],
            "confidence": prepass.get("confidence", 0.0),
            "safe_for_examiner": SAFE_FOR_EXAMINER,
        }
        recommended_update = {
            "append_recent_misconception": None,
            "increase_attention_to": None,
        }
        matched_node = {}
        retrieval_query = query

    governance = {
        "safe_for_examiner": SAFE_FOR_EXAMINER,
        "examiner_scoring_active": False,
        "embeddings_active": False,
        "vector_db_active": False,
        "apis_connected": False,
        "frontend_active": False,
        "cloud_services_active": CLOUD_SERVICES_ACTIVE,
    }
    retrieval_plan = {
        "mode": "forced_plus_supporting_chunks" if prepass["detected"] else "normal_retrieval",
        "query": retrieval_query,
        "top_k": top_k,
        "forced_retrieval_nodes": tutor_directive["forced_retrieval_nodes"],
        "pedagogical_priority_boost": pedagogical_boost,
        "retrieval_engine": "tools.retrieval.tutor_retrieval_sandbox",
        "uses_embeddings": USES_EMBEDDINGS,
        "uses_vector_db": USES_VECTOR_DB,
        "uses_llm": USES_LLM,
        "uses_api": USES_API,
    }
    retrieval_run = run_retrieval_sandbox(
        root=root,
        query=retrieval_query,
        top_k=top_k,
        output_prefix="orchestrator_context_retrieval",
    )
    retrieved_context = build_retrieved_context(
        matched_node=matched_node,
        retrieved_chunks=retrieval_run["retrieved_chunks"],
    )
    matched_causal_chain_nodes = retrieval_run.get("matched_causal_chain_nodes", [])
    context_package = build_context_package(
        query=query,
        language=language,
        decision=decision,
        pedagogical_act=tutor_directive["pedagogical_act"],
        forced_retrieval_nodes=tutor_directive["forced_retrieval_nodes"],
        matched_misconception=matched_node,
        les_context=les_context,
        retrieval_plan=retrieval_plan,
        retrieved_context=retrieved_context,
        tutor_directive=tutor_directive,
        forced_causal_chains=matched_causal_chain_nodes,
    )
    package_paths = write_context_package(context_package, context_package_dir)
    result = {
        "student_query": query,
        "detected_misconception": prepass,
        "les_context_used": les_context,
        "orchestrator_decision": decision,
        "retrieval_plan": retrieval_plan,
        "retrieved_context": retrieved_context,
        "tutor_directive": tutor_directive,
        "recommended_les_update": recommended_update,
        "governance_flags": governance,
        "context_package": context_package,
        "context_package_paths": package_paths,
        "strategic_plan": strategic_plan,
    }
    staging = {
        "schema_version": "minimal_brain_v2",
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "latest_session": result,
        "latest_context_package_path": package_paths["latest"],
        "governance": governance,
        # Phase 1C: top-level observation snapshot — write-only, never read back.
        # The planner re-derives from fresh LES each session; this persisted copy
        # is for session-to-session observability and future Phase 2 ledger work only.
        "strategic_plan": strategic_plan,
    }
    write_session_staging(staging, staging_path)
    # Phase 2A: append to cognitive ledger — write-only telemetry.
    # Ledger lives alongside the LES in les_path.parent so temp dirs in tests
    # automatically get a temp ledger without requiring a new parameter.
    # The ledger is NEVER read back by the planner, retrieval, or Tutor.
    ledger_path = les_path.parent / "session_ledger.json"
    append_to_ledger(result, ledger_path)
    result["session_staging_path"] = staging_path.as_posix()
    return result


def load_misconception_node(misconception_id: str | None, directory: Path = DEFAULT_MISCONCEPTION_DIR) -> dict[str, Any]:
    """Load the full misconception node by id."""
    if not misconception_id:
        return {}
    for node in load_misconception_nodes(directory):
        if node.get("misconception_id") == misconception_id:
            return node
    return {}


def build_retrieved_context(
    matched_node: dict[str, Any],
    retrieved_chunks: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Build Tutor-ready retrieval context entries."""
    context: list[dict[str, Any]] = []
    if matched_node:
        context.append(
            {
                "context_type": "misconception_node",
                "node_id": matched_node.get("misconception_id"),
                "forced_retrieval": True,
                "agent_corpus": "tutor",
                "safe_for_examiner": False,
                "source_path": matched_node.get("_source_path", ""),
                "content": matched_node,
            }
        )
    for chunk in retrieved_chunks:
        context.append(
            {
                "context_type": "retrieval_sandbox_chunk",
                "chunk_id": chunk.get("chunk_id"),
                "forced_retrieval": False,
                "agent_corpus": chunk.get("agent_corpus", "tutor"),
                "safe_for_examiner": False,
                "score": chunk.get("score"),
                "source_type": chunk.get("source_type", ""),
                "source_file": chunk.get("source_file", ""),
                "source_trust_tier": chunk.get("source_trust_tier"),
                "title": chunk.get("title", ""),
                "section": chunk.get("section", ""),
                "subtopic": chunk.get("subtopic", ""),
                "official_grading_authority": False,
                "requires_human_review": bool(chunk.get("requires_human_review", False)),
                "reasoning_type": chunk.get("reasoning_type"),
                "pedagogical_role": chunk.get("pedagogical_role"),
                "why_retrieved": chunk.get("why_retrieved", []),
                "text_excerpt": chunk.get("text_excerpt", ""),
                "source_video": chunk.get("source_video", ""),
                "source_filename": chunk.get("source_filename", ""),
            }
        )
    return context


def build_context_package(
    query: str,
    language: str,
    decision: dict[str, Any],
    pedagogical_act: str,
    forced_retrieval_nodes: list[str],
    matched_misconception: dict[str, Any],
    les_context: dict[str, Any],
    retrieval_plan: dict[str, Any],
    retrieved_context: list[dict[str, Any]],
    tutor_directive: dict[str, Any],
    forced_causal_chains: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Create the Minimal Brain v2 Tutor-ready context package."""
    directive = {
        **tutor_directive,
        "language": language,
        "response_language_instruction": _language_instruction(language),
        "source_handling": [
            "Use this as a context package only; do not treat it as a final answer.",
            "Use official WSET support first when available.",
            "Use pedagogical transcript chunks only as enrichment.",
            "Do not present pedagogical sources as official authority.",
            "Distinguish official WSET content from pedagogical enrichment when explaining.",
            "Do not translate source chunks; preserve official WSET terms where useful.",
            "Do not translate key terms if translation would reduce precision.",
            "If forced_causal_chains is populated, render the causal chain steps for the Cadena causa → efecto section.",
        ],
        "safe_for_examiner": SAFE_FOR_EXAMINER,
    }
    return {
        "student_query": query,
        "language": language,
        "orchestrator_decision": decision,
        "pedagogical_act": pedagogical_act,
        "forced_retrieval_nodes": forced_retrieval_nodes,
        "matched_misconception": matched_misconception,
        "learner_state_context": les_context,
        "retrieval_plan": retrieval_plan,
        "retrieved_context": retrieved_context,
        "forced_causal_chains": forced_causal_chains or [],
        "tutor_directive": directive,
        "success_criteria": _success_criteria(pedagogical_act),
        "governance": {
            "agent_corpus": "tutor",
            "safe_for_examiner": SAFE_FOR_EXAMINER,
            "examiner_scoring_allowed": EXAMINER_SCORING_ALLOWED,
        },
    }


def write_context_package(package: dict[str, Any], output_dir: Path = DEFAULT_CONTEXT_PACKAGE_DIR) -> dict[str, str]:
    """Write latest and timestamped local context package artifacts."""
    output_dir.mkdir(parents=True, exist_ok=True)
    latest_path = output_dir / "latest_context_package.json"
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    timestamped_path = output_dir / f"{timestamp}_context_package.json"
    _write_json(latest_path, package)
    _write_json(timestamped_path, package)
    return {
        "latest": latest_path.as_posix(),
        "timestamped": timestamped_path.as_posix(),
    }


def _misconception_retrieval_query(query: str, matched_node: dict[str, Any]) -> str:
    parts = [
        query,
        str(matched_node.get("misconception", "")),
        str(matched_node.get("corrected_understanding", "")),
        " ".join(str(item) for item in matched_node.get("related_concepts", [])),
    ]
    return " ".join(part for part in parts if part).strip()


def _language_instruction(language: str) -> str:
    if language == "en":
        return (
            "Respond in English. Preserve official WSET terms where useful, "
            "and distinguish official WSET content from pedagogical content."
        )
    return (
        "Respond in Spanish. Preserve official WSET terms where useful, "
        "and do not translate key terms if translation would reduce precision. "
        "Distinguish official WSET content from pedagogical content."
    )


def _success_criteria(pedagogical_act: str) -> list[str]:
    if pedagogical_act == "misconception_intervention":
        return [
            "Identify the misconception before answering the learner's underlying question.",
            "State the corrected understanding clearly.",
            "Use supporting Tutor-context chunks only as pedagogical support.",
            "Keep Examiner scoring disabled and safe_for_examiner false.",
        ]
    return [
        "Answer the learner's question using the retrieved Tutor context.",
        "Preserve official WSET terminology where precision matters.",
        "Distinguish official WSET content from pedagogical enrichment.",
        "Keep Examiner scoring disabled and safe_for_examiner false.",
    ]


def _pedagogical_priority_boost(les_context: dict[str, Any]) -> dict[str, Any]:
    """Build retrieval-facing memory hints without changing retrieval contracts."""
    memory = les_context.get("pedagogical_memory") or {}
    low_mastery = memory.get("low_mastery_concepts") or []
    recurrent = memory.get("recurrent_misconceptions") or []
    retention = memory.get("retention_risks") or []
    difficult_chains = memory.get("difficult_causal_chains") or []
    force_deep = any(float(item.get("persistence", 0) or 0) >= 0.6 for item in recurrent if isinstance(item, dict))
    return {
        "low_mastery_concepts": [item.get("concept_id") for item in low_mastery if isinstance(item, dict) and item.get("concept_id")],
        "causal_chain_boosts": [item.get("chain_id") for item in difficult_chains if isinstance(item, dict) and item.get("chain_id")],
        "misconception_persistence_boost": force_deep,
        "force_deep_explanation": force_deep,
        "resurfacing_concepts": [item.get("concept_id") for item in retention if isinstance(item, dict) and item.get("concept_id")],
        "preferred_depth": memory.get("preferred_depth", "standard"),
        "safe_for_examiner": SAFE_FOR_EXAMINER,
        "examiner_scoring_allowed": EXAMINER_SCORING_ALLOWED,
    }


def _normalize_language(language: str) -> str:
    return "en" if str(language).lower() == "en" else "es"


def _write_json(path: Path, data: dict[str, Any]) -> None:
    with path.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=True)
        file.write("\n")
