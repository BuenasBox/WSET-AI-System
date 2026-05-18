"""Tutor retrieval validation sandbox.

This is a transparent, rule-based retrieval harness. It reads existing chunk
artifacts and derived metadata, then explains which chunks would be retrieved
for a query and why. It does not use embeddings, vector databases, LLM APIs, or
Examiner scoring.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from tools.constants import KNOWLEDGE_DIR, OFFICIAL_WSET_DIR, PROJECT_ROOT, RETRIEVAL_SANDBOX_DIR

ALLOWED_SOURCE_TYPES = {"manual_curated_srt", "youtube_transcript", "official_wset_extracted"}
ALLOWED_AGENT_CORPUS = "tutor"
GOVERNANCE_FILTER_APPLIED = True
INTENTS = (
    "sat_coaching",
    "tasting_exam_strategy",
    "theory_exam_strategy",
    "cause_effect_explanation",
    "answer_structure",
    "misconception_help",
    "wine_law",
    "viticulture",
    "vinification",
    "tasting_calibration",
    "foundational_theory",
    "advanced_enrichment",
    "unknown",
)
STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "be",
    "by",
    "do",
    "does",
    "for",
    "from",
    "how",
    "i",
    "in",
    "is",
    "it",
    "me",
    "of",
    "on",
    "or",
    "should",
    "the",
    "to",
    "what",
    "when",
    "where",
    "why",
    "with",
}
SAT_TERMS = {
    "sat",
    "systematic",
    "approach",
    "tasting",
    "quality",
    "balance",
    "intensity",
    "complexity",
    "length",
    "readiness",
    "acidity",
    "tannin",
    "body",
    "finish",
}
CAUSE_EFFECT_TERMS = {"affect", "because", "cause", "effect", "increase", "decrease", "leads", "therefore", "why"}
EXAM_TERMS = {"exam", "marks", "answer", "question", "structure", "justify", "pass", "wset"}
_EXPANSIONS_PATH = KNOWLEDGE_DIR / "config" / "domain_expansions.json"


def _load_domain_expansions() -> dict:
    if not _EXPANSIONS_PATH.exists():
        raise FileNotFoundError(
            f"domain_expansions.json not found at {_EXPANSIONS_PATH}. "
            "This file is required for retrieval to function."
        )
    return json.loads(_EXPANSIONS_PATH.read_text(encoding="utf-8"))


_EXPANSIONS_CONFIG = _load_domain_expansions()
SAT_EXPANSIONS = _EXPANSIONS_CONFIG["SAT_EXPANSIONS"]
DOMAIN_EXPANSIONS = _EXPANSIONS_CONFIG["DOMAIN_EXPANSIONS"]
REASONING_BY_INTENT = {
    "sat_coaching": "sat_logic",
    "tasting_exam_strategy": "exam_strategy",
    "theory_exam_strategy": "exam_strategy",
    "cause_effect_explanation": "cause_effect",
    "answer_structure": "answer_structure",
    "misconception_help": "common_mistake",
    "tasting_calibration": "tasting_calibration",
    "foundational_theory": "theory_foundation",
    "advanced_enrichment": "theory_foundation",
}
PRIORITY_BOOSTS = {"high": 0.12, "medium": 0.06, "low": 0.02}
ROLE_ALIGNMENT = {
    "sat_coaching": {"tasting_practice", "exam_strategy"},
    "tasting_exam_strategy": {"exam_strategy", "tasting_practice"},
    "theory_exam_strategy": {"exam_strategy", "theory_explanation"},
    "cause_effect_explanation": {"theory_explanation", "foundational", "advanced_enrichment"},
    "answer_structure": {"exam_strategy"},
    "misconception_help": {"exam_strategy", "theory_explanation", "tasting_practice"},
    "wine_law": {"theory_explanation", "foundational", "advanced_enrichment"},
    "viticulture": {"theory_explanation", "foundational", "advanced_enrichment"},
    "vinification": {"theory_explanation", "foundational", "advanced_enrichment"},
    "tasting_calibration": {"tasting_practice", "exam_strategy"},
    "foundational_theory": {"theory_explanation", "foundational"},
    "advanced_enrichment": {"advanced_enrichment", "theory_explanation"},
}


@dataclass(frozen=True)
class RetrievalContext:
    chunks: list[dict[str, Any]]
    golden_by_chunk_id: dict[str, dict[str, Any]]
    dictionary_terms: list[dict[str, Any]]
    knowledge_nodes: list[dict[str, Any]]
    indexed_chunks: int
    excluded_chunks: int


def run_retrieval_sandbox(
    root: Path,
    query: str,
    top_k: int = 10,
    output_prefix: str = "retrieval_run",
) -> dict[str, Any]:
    context = load_retrieval_context(root)
    query_analysis = classify_query(query, context.dictionary_terms, context.knowledge_nodes)
    scored = [
        score_chunk_for_query(chunk, query_analysis, context.golden_by_chunk_id)
        for chunk in context.chunks
        if _advanced_chunk_allowed(chunk, query_analysis["query_intent"])
    ]
    scored = [row for row in scored if row["score"] > 0]
    scored.sort(key=_ranking_key)
    retrieved = _select_diverse_results(scored, top_k)
    # Extract full causal chain node objects for matched chains
    matched_causal_chain_nodes = select_matched_causal_chain_nodes(
        query_analysis.get("matched_causal_chains", []),
        context.knowledge_nodes,
    )
    run = {
        "query": query,
        "generated_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "governance_filter_applied": GOVERNANCE_FILTER_APPLIED,
        "query_analysis": query_analysis,
        "indexed_chunks": context.indexed_chunks,
        "excluded_chunks": context.excluded_chunks,
        "golden_chunks_loaded": len(context.golden_by_chunk_id),
        "dictionary_terms_loaded": len(context.dictionary_terms),
        "knowledge_nodes_loaded": len(context.knowledge_nodes),
        "top_k": top_k,
        "retrieved_chunks": retrieved,
        "matched_causal_chain_nodes": matched_causal_chain_nodes,
        "summary_statistics": _summary_statistics(retrieved),
    }
    write_retrieval_reports(root, run, output_prefix=output_prefix)
    return run


def select_matched_causal_chain_nodes(
    matched_chains: list[dict[str, Any]],
    knowledge_nodes: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Return full causal chain node dicts for each matched chain ID.

    The query analysis contains matched_causal_chains as lightweight {id, name, terms}
    dicts. This function looks up the full node data by ID so the Orchestrator can
    pass structured causal chain objects (with steps) to the Tutor rendering layer.

    Governance: only returns nodes with safe_for_examiner != True and
    agent_corpus == 'tutor'. Path field is stripped for clean output.
    """
    matched_ids = {str(item.get("id", "")) for item in matched_chains if item.get("id")}
    if not matched_ids:
        return []
    result = []
    for node in knowledge_nodes:
        if _knowledge_node_type(node) != "causal_chains":
            continue
        node_id = _knowledge_node_id(node)
        if node_id not in matched_ids:
            continue
        # Enforce governance — never surface nodes that claim examiner authority
        if node.get("safe_for_examiner") is True:
            continue
        if node.get("examiner_scoring_allowed") is True:
            continue
        # Return a clean copy without the internal path field
        clean = {k: v for k, v in node.items() if k != "path"}
        clean.setdefault("node_id", node_id)
        clean.setdefault("id", node_id)
        clean.setdefault("node_type", "causal_chain")
        clean.setdefault("type", "causal_chain")
        clean["safe_for_examiner"] = False
        clean["examiner_scoring_allowed"] = False
        clean["agent_corpus"] = "tutor"
        result.append(clean)
    return result


def load_retrieval_context(root: Path) -> RetrievalContext:
    chunk_dir = root / "knowledge" / "wine-with-jimmy" / "chunk-ready"
    official_chunk_path = root / OFFICIAL_WSET_DIR.relative_to(PROJECT_ROOT) / "study-guide" / "official-chunks" / "official_wset_chunks.jsonl"
    golden_path = (
        root / "knowledge" / "wine-with-jimmy" / "manual-import" / "reports" / "golden_tutor_chunk_candidates.jsonl"
    )
    dictionary_path = root / "knowledge" / "enrichment" / "wset_master_dictionary" / "consolidated" / "canonical_terms_master.jsonl"
    knowledge_map_dir = root / "knowledge" / "knowledge-map"
    chunks, excluded = load_chunks(chunk_dir)
    official_chunks, official_excluded = load_official_chunks(official_chunk_path)
    chunks.extend(official_chunks)
    excluded += official_excluded
    return RetrievalContext(
        chunks=chunks,
        golden_by_chunk_id=load_golden_chunks(golden_path),
        dictionary_terms=load_dictionary_terms(dictionary_path),
        knowledge_nodes=load_knowledge_nodes(knowledge_map_dir),
        indexed_chunks=len(chunks),
        excluded_chunks=excluded,
    )


def load_chunks(chunk_dir: Path) -> tuple[list[dict[str, Any]], int]:
    chunks: list[dict[str, Any]] = []
    excluded = 0
    for path in sorted(chunk_dir.glob("*.chunks.jsonl"), key=lambda item: item.name.lower()):
        for chunk in _read_jsonl(path):
            if _passes_governance_filter(chunk):
                chunks.append(chunk)
            else:
                excluded += 1
    return chunks, excluded


def load_official_chunks(path: Path) -> tuple[list[dict[str, Any]], int]:
    chunks: list[dict[str, Any]] = []
    excluded = 0
    for chunk in _read_jsonl(path):
        if _passes_governance_filter(chunk):
            chunks.append(chunk)
        else:
            excluded += 1
    return chunks, excluded


def load_golden_chunks(path: Path) -> dict[str, dict[str, Any]]:
    if not path.exists():
        return {}
    rows = {}
    for row in _read_jsonl(path):
        chunk_id = str(row.get("chunk_id", ""))
        if chunk_id:
            rows[chunk_id] = row
    return rows


def load_dictionary_terms(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    terms = []
    for row in _read_jsonl(path):
        if row.get("safe_for_examiner") is True:
            continue
        canonical = str(row.get("canonical_term", "")).strip()
        if not canonical:
            continue
        aliases = [str(alias).strip() for alias in row.get("aliases", []) if str(alias).strip()]
        terms.append(
            {
                "canonical_term": canonical,
                "category": str(row.get("category", "")),
                "aliases": aliases,
            }
        )
    return terms


def load_knowledge_nodes(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    nodes = []
    for item in sorted(path.rglob("*.json"), key=lambda value: value.as_posix().lower()):
        try:
            data = json.loads(item.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            continue
        if isinstance(data, dict):
            nodes.append({"path": item.as_posix(), **data})
    return nodes


def classify_query(
    query: str,
    dictionary_terms: list[dict[str, Any]] | None = None,
    knowledge_nodes: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    text = query.lower()
    matched_terms = detect_dictionary_terms(query, dictionary_terms or [])
    matched_knowledge = detect_knowledge_nodes(query, knowledge_nodes or [])
    token_set = set(_tokens(query))
    if re.search(r"\b(?:sat|systematic approach|justify quality|quality in sat)\b", text):
        intent = "sat_coaching"
    elif re.search(r"\b(?:lose marks|tasting exam|level 3 tasting)\b", text):
        intent = "tasting_exam_strategy"
    elif re.search(r"\b(?:10 mark|ten mark|structure|how should i answer|written answer)\b", text):
        intent = "answer_structure"
    elif re.search(r"\b(?:why|how does|affect|cause|effect|increase|decrease|because)\b", text):
        intent = "cause_effect_explanation"
    elif re.search(r"\b(?:wine law|appellation|aoc|doc|igp|classification)\b", text):
        intent = "wine_law"
    elif re.search(r"\b(?:climate|vineyard|viticulture|soil|drought|disease)\b", text):
        intent = "viticulture"
    elif re.search(r"\b(?:fermentation|maceration|oak|lees|malolactic|winemaking|vinification)\b", text):
        intent = "vinification"
    elif re.search(r"\b(?:balance|intensity|complexity|length|readiness|quality assessment)\b", text):
        intent = "tasting_calibration"
    elif re.search(r"\b(?:mistake|confus|misconception)\b", text):
        intent = "misconception_help"
    elif re.search(r"\b(?:diploma|level 4|advanced|mw)\b", text):
        intent = "advanced_enrichment"
    elif token_set:
        intent = "foundational_theory"
    else:
        intent = "unknown"

    reasoning_intent = REASONING_BY_INTENT.get(intent, "unknown")
    if intent == "cause_effect_explanation":
        reasoning_intent = "cause_effect"
    expansion_terms = expand_query_terms(query, matched_terms, matched_knowledge)
    return {
        "query_intent": intent,
        "reasoning_intent": reasoning_intent,
        "matched_terms": matched_terms,
        "matched_concepts": matched_knowledge["concepts"],
        "matched_causal_chains": matched_knowledge["causal_chains"],
        "matched_relationships": matched_knowledge["relationships"],
        "matched_misconceptions": matched_knowledge["misconceptions"],
        "query_expansion_terms": expansion_terms,
        "query_tokens": sorted(token_set),
        "expanded_query_tokens": sorted(token_set | set(_tokens(" ".join(expansion_terms)))),
    }


def detect_dictionary_terms(query: str, dictionary_terms: list[dict[str, Any]]) -> list[dict[str, str]]:
    query_lower = query.lower()
    matched = []
    for term in dictionary_terms:
        names = [term["canonical_term"], *term.get("aliases", [])]
        if any(_contains_phrase(query_lower, name) for name in names):
            matched.append({"canonical_term": term["canonical_term"], "category": term.get("category", "")})
    return matched


def detect_knowledge_nodes(query: str, knowledge_nodes: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    matched = {"concepts": [], "causal_chains": [], "relationships": [], "misconceptions": []}
    query_lower = query.lower()
    query_tokens = set(_tokens(query))
    strong_query_tokens = query_tokens - {
        "affect",
        "answer",
        "exam",
        "level",
        "mark",
        "marks",
        "mean",
        "question",
        "structure",
        "tasting",
        "wset",
    }
    for node in knowledge_nodes:
        node_type = _knowledge_node_type(node)
        if node_type not in matched:
            continue
        node_name = _knowledge_node_name(node).lower()
        node_id_phrase = _identifier_to_phrase(_knowledge_node_id(node))
        phrases = _knowledge_node_primary_phrases(node)
        phrase_hit = _contains_phrase(query_lower, node_name) or _contains_phrase(query_lower, node_id_phrase)
        node_tokens = set(_tokens(" ".join([node_name, node_id_phrase, *phrases])))
        strong_hits = strong_query_tokens & node_tokens
        if node_type in {"causal_chains", "relationships"}:
            token_hit = len(strong_hits) >= 2
        elif node_type == "concepts":
            name_tokens = set(_tokens(f"{node_name} {node_id_phrase}"))
            token_hit = bool(strong_query_tokens & name_tokens)
        else:
            token_hit = len(strong_hits) >= 2
        if phrase_hit or token_hit:
            matched[node_type].append(
                {
                    "id": _knowledge_node_id(node),
                    "name": _knowledge_node_name(node),
                    "terms": sorted(set(phrases))[:18],
                }
            )
    return matched


def expand_query_terms(
    query: str,
    matched_terms: list[dict[str, str]],
    matched_knowledge: dict[str, list[dict[str, Any]]],
) -> list[str]:
    expanded = set()
    query_lower = query.lower()
    token_set = set(_tokens(query))
    for term in matched_terms:
        expanded.add(term["canonical_term"])
    for trigger, terms in SAT_EXPANSIONS.items():
        if trigger.lower() in query_lower or trigger.lower() in token_set:
            expanded.update(terms)
    for trigger, terms in DOMAIN_EXPANSIONS.items():
        if trigger in query_lower or set(_tokens(trigger)).issubset(token_set):
            expanded.update(terms)
    for group in matched_knowledge.values():
        for node in group:
            expanded.update(node.get("terms", [])[:14])
    return sorted(term for term in expanded if term and term.lower() not in STOPWORDS)


def score_chunk_for_query(
    chunk: dict[str, Any],
    query_analysis: dict[str, Any],
    golden_by_chunk_id: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    text = str(chunk.get("text", "") or "")
    chunk_id = str(chunk.get("chunk_id", ""))
    golden = golden_by_chunk_id.get(chunk_id, {})
    query_tokens = set(query_analysis.get("query_tokens", []))
    expanded_query_tokens = set(query_analysis.get("expanded_query_tokens", query_analysis.get("query_tokens", [])))
    chunk_tokens = set(_tokens(text))
    lexical_overlap = len(query_tokens & chunk_tokens) / max(1, len(query_tokens))
    expanded_overlap = len(expanded_query_tokens & chunk_tokens) / max(1, len(expanded_query_tokens))
    matched_terms = _matched_chunk_terms(chunk, query_analysis, text)
    matched_dictionary_terms = _matched_dictionary_terms(query_analysis, text)
    matched_concepts = _matched_knowledge_terms(query_analysis.get("matched_concepts", []), text)
    matched_causal_chains = _matched_knowledge_terms(query_analysis.get("matched_causal_chains", []), text)
    matched_relationships = _matched_knowledge_terms(query_analysis.get("matched_relationships", []), text)
    source_concept_phrase_score = _source_concept_phrase_score(query_analysis, text)
    dictionary_score = min(1.0, len(matched_terms) / max(1, len(query_analysis.get("matched_terms", []))))
    dictionary_category_score = _dictionary_category_score(chunk, query_analysis)
    concept_match_score = min(1.0, len(matched_concepts) / max(1, len(query_analysis.get("matched_concepts", [])) * 2))
    causal_chain_match_score = min(1.0, len(matched_causal_chains) / max(1, len(query_analysis.get("matched_causal_chains", [])) * 3))
    relationship_match_score = min(1.0, len(matched_relationships) / max(1, len(query_analysis.get("matched_relationships", [])) * 2))
    knowledge_graph_match_score = max(concept_match_score, causal_chain_match_score, relationship_match_score)
    reasoning_alignment = 1.0 if golden.get("reasoning_type") == query_analysis.get("reasoning_intent") else 0.0
    if not reasoning_alignment and _chunk_text_aligns_reasoning(text, query_analysis.get("reasoning_intent", "")):
        reasoning_alignment = 0.65
    role_alignment = 1.0 if chunk.get("pedagogical_role") in ROLE_ALIGNMENT.get(query_analysis["query_intent"], set()) else 0.0
    sat_boost = 1.0 if query_tokens & SAT_TERMS and chunk_tokens & SAT_TERMS else 0.0
    cause_effect_boost = 1.0 if query_tokens & CAUSE_EFFECT_TERMS and _chunk_text_aligns_reasoning(text, "cause_effect") else 0.0
    exam_strategy_boost = 1.0 if query_tokens & EXAM_TERMS and chunk_tokens & EXAM_TERMS else 0.0
    golden_boost = 1.0 if golden.get("golden_tutor_chunk_candidate") is True else 0.0
    priority_boost = PRIORITY_BOOSTS.get(str(golden.get("retrieval_priority", "")), 0.0)
    quality_penalty = min(0.18, 0.04 * len(_as_list(chunk.get("quality_flags")) + _as_list(golden.get("quality_flags"))))
    official_source_boost = 1.0 if chunk.get("source_type") == "official_wset_extracted" else 0.0
    exact_term_boost = 1.0 if matched_terms or matched_dictionary_terms else 0.0
    section_topic_boost = _section_topic_match_score(chunk, query_analysis)
    official_exam_register_boost = 1.0 if official_source_boost and _chunk_text_aligns_reasoning(text, "exam_strategy") else 0.0
    score = (
        0.18 * min(1.0, lexical_overlap)
        + 0.1 * min(1.0, expanded_overlap)
        + 0.08 * dictionary_score
        + 0.05 * dictionary_category_score
        + 0.1 * golden_boost
        + 0.14 * reasoning_alignment
        + 0.1 * role_alignment
        + priority_boost
        + 0.09 * sat_boost
        + 0.1 * cause_effect_boost
        + 0.07 * exam_strategy_boost
        + 0.1 * knowledge_graph_match_score
        + 0.08 * causal_chain_match_score
        + 0.06 * concept_match_score
        + 0.12 * source_concept_phrase_score
        + 0.18 * official_source_boost
        + 0.08 * exact_term_boost
        + 0.08 * section_topic_boost
        + 0.06 * official_exam_register_boost
        - quality_penalty
    )
    score = max(0.0, min(1.0, score))
    breakdown = {
        "lexical_overlap": round(0.18 * min(1.0, lexical_overlap), 4),
        "expanded_lexical_overlap": round(0.1 * min(1.0, expanded_overlap), 4),
        "canonical_dictionary_terms": round(0.08 * dictionary_score, 4),
        "dictionary_category_match": round(0.05 * dictionary_category_score, 4),
        "golden_chunk_boost": round(0.1 * golden_boost, 4),
        "reasoning_type_alignment": round(0.14 * reasoning_alignment, 4),
        "pedagogical_role_alignment": round(0.1 * role_alignment, 4),
        "retrieval_priority_boost": round(priority_boost, 4),
        "sat_term_boost": round(0.09 * sat_boost, 4),
        "cause_effect_boost": round(0.1 * cause_effect_boost, 4),
        "exam_strategy_boost": round(0.07 * exam_strategy_boost, 4),
        "knowledge_graph_match": round(0.1 * knowledge_graph_match_score, 4),
        "causal_chain_match": round(0.08 * causal_chain_match_score, 4),
        "concept_match": round(0.06 * concept_match_score, 4),
        "source_concept_phrase_match": round(0.12 * source_concept_phrase_score, 4),
        "official_source_boost": round(0.18 * official_source_boost, 4),
        "exact_term_match_boost": round(0.08 * exact_term_boost, 4),
        "section_topic_match_boost": round(0.08 * section_topic_boost, 4),
        "official_exam_register_boost": round(0.06 * official_exam_register_boost, 4),
        "quality_flags_penalty": round(-quality_penalty, 4),
    }
    why = explain_retrieval(
        chunk=chunk,
        golden=golden,
        matched_terms=matched_terms,
        query_analysis=query_analysis,
        breakdown=breakdown,
    )
    return {
        "chunk_id": chunk_id,
        "score": round(score, 4),
        "source_video": str(chunk.get("video_title_guess") or chunk.get("video_title") or ""),
        "source_filename": str(chunk.get("source_filename", "")),
        "source_type": str(chunk.get("source_type", "")),
        "source_file": str(chunk.get("source_file", "")),
        "source_trust_tier": chunk.get("source_trust_tier"),
        "title": str(chunk.get("title", "")),
        "section": str(chunk.get("section", "")),
        "subtopic": str(chunk.get("subtopic", "")),
        "official_grading_authority": bool(chunk.get("official_grading_authority", False)),
        "requires_human_review": bool(chunk.get("requires_human_review", False)),
        "reasoning_type": str(golden.get("reasoning_type") or query_analysis.get("reasoning_intent") or "unknown"),
        "pedagogical_role": str(chunk.get("pedagogical_role", "")),
        "retrieval_priority": str(golden.get("retrieval_priority", "none")),
        "matched_terms": matched_terms,
        "matched_concepts": matched_concepts,
        "matched_causal_chains": matched_causal_chains,
        "matched_dictionary_terms": matched_dictionary_terms,
        "query_expansion_terms": query_analysis.get("query_expansion_terms", []),
        "knowledge_graph_boost_applied": breakdown["knowledge_graph_match"] > 0
        or breakdown["causal_chain_match"] > 0
        or breakdown["concept_match"] > 0,
        "why_retrieved": why,
        "text_excerpt": _excerpt(text),
        "scoring_breakdown": breakdown,
        "safe_for_examiner": False,
        "agent_corpus": ALLOWED_AGENT_CORPUS,
    }


def explain_retrieval(
    chunk: dict[str, Any],
    golden: dict[str, Any],
    matched_terms: list[str],
    query_analysis: dict[str, Any],
    breakdown: dict[str, float],
) -> list[str]:
    reasons = []
    if matched_terms:
        reasons.append("matched canonical/query terms: " + ", ".join(matched_terms[:8]))
    if golden.get("golden_tutor_chunk_candidate") is True:
        reasons.append("golden tutor chunk candidate")
    if golden.get("retrieval_priority") in {"high", "medium"}:
        reasons.append(f"{golden['retrieval_priority']} retrieval priority in golden QA report")
    if breakdown["reasoning_type_alignment"] > 0:
        reasons.append(f"aligns with {query_analysis['reasoning_intent']} reasoning intent")
    if breakdown["pedagogical_role_alignment"] > 0:
        reasons.append(f"pedagogical role fits {query_analysis['query_intent']}")
    if breakdown["sat_term_boost"] > 0:
        reasons.append("matched SAT/tasting vocabulary")
    if breakdown["cause_effect_boost"] > 0:
        reasons.append("supports cause/effect explanation")
    if breakdown["exam_strategy_boost"] > 0:
        reasons.append("contains exam or marks strategy language")
    if breakdown.get("knowledge_graph_match", 0) > 0:
        reasons.append("matches knowledge-map concept or relationship terms")
    if breakdown.get("causal_chain_match", 0) > 0:
        reasons.append("matches knowledge-map causal-chain mechanism")
    if breakdown.get("concept_match", 0) > 0:
        reasons.append("matches knowledge-map concept vocabulary")
    if breakdown.get("source_concept_phrase_match", 0) > 0:
        reasons.append("contains the source concept phrase from the query")
    if breakdown.get("official_source_boost", 0) > 0:
        reasons.append("official WSET extracted Tutor support")
    if breakdown.get("section_topic_match_boost", 0) > 0:
        reasons.append("matched official section/topic metadata")
    if breakdown.get("exact_term_match_boost", 0) > 0:
        reasons.append("exact term match")
    if not reasons:
        reasons.append("low-confidence lexical match retained for ranking comparison")
    if _as_list(chunk.get("quality_flags")) or _as_list(golden.get("quality_flags")):
        reasons.append("quality flags reduced the score and require review")
    return reasons


def write_retrieval_reports(root: Path, run: dict[str, Any], output_prefix: str = "retrieval_run") -> None:
    output_dir = root / RETRIEVAL_SANDBOX_DIR.relative_to(PROJECT_ROOT)
    output_dir.mkdir(parents=True, exist_ok=True)
    safe_prefix = _safe_output_prefix(output_prefix)
    json_path = output_dir / f"{safe_prefix}.json"
    md_path = output_dir / f"{safe_prefix}.md"
    csv_name = "retrieval_debug.csv" if safe_prefix == "retrieval_run" else f"{safe_prefix}_debug.csv"
    csv_path = output_dir / csv_name
    json_path.write_text(json.dumps(run, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    md_path.write_text(_render_markdown(run), encoding="utf-8")
    _write_debug_csv(csv_path, run)


def _render_markdown(run: dict[str, Any]) -> str:
    analysis = run["query_analysis"]
    lines = [
        "# Tutor Retrieval Sandbox Run",
        "",
        f"Query: {run['query']}",
        f"Generated at: {run['generated_at']}",
        f"Governance filter applied: {str(run['governance_filter_applied']).lower()}",
        "",
        "## Query Analysis",
        "",
        f"- query_intent: {analysis['query_intent']}",
        f"- reasoning_intent: {analysis['reasoning_intent']}",
        f"- matched_terms: {', '.join(term['canonical_term'] for term in analysis['matched_terms']) or 'none'}",
        f"- query_expansion_terms: {', '.join(analysis.get('query_expansion_terms', [])) or 'none'}",
        f"- matched_concepts: {', '.join(item['name'] for item in analysis.get('matched_concepts', [])) or 'none'}",
        f"- matched_causal_chains: {', '.join(item['name'] for item in analysis.get('matched_causal_chains', [])) or 'none'}",
        "",
        "## Corpus",
        "",
        f"- indexed_chunks: {run['indexed_chunks']}",
        f"- excluded_chunks: {run['excluded_chunks']}",
        f"- golden_chunks_loaded: {run['golden_chunks_loaded']}",
        f"- dictionary_terms_loaded: {run['dictionary_terms_loaded']}",
        f"- knowledge_nodes_loaded: {run['knowledge_nodes_loaded']}",
        "",
        "## Retrieved Chunks",
        "",
    ]
    for index, chunk in enumerate(run["retrieved_chunks"], start=1):
        lines.extend(
            [
                f"{index}. {chunk['score']:.4f} {chunk['chunk_id']} - {chunk['source_video']}",
                f"   - reasoning_type: {chunk['reasoning_type']}",
                f"   - pedagogical_role: {chunk['pedagogical_role']}",
                f"   - retrieval_priority: {chunk['retrieval_priority']}",
                f"   - matched_terms: {', '.join(chunk['matched_terms']) or 'none'}",
                f"   - matched_concepts: {', '.join(chunk.get('matched_concepts', [])) or 'none'}",
                f"   - matched_causal_chains: {', '.join(chunk.get('matched_causal_chains', [])) or 'none'}",
                f"   - query_expansion_terms: {', '.join(chunk.get('query_expansion_terms', [])[:12]) or 'none'}",
                f"   - knowledge_graph_boost_applied: {str(chunk.get('knowledge_graph_boost_applied', False)).lower()}",
                f"   - why: {'; '.join(chunk['why_retrieved'])}",
                f"   - excerpt: {chunk['text_excerpt']}",
                "",
            ]
        )
    lines.append("No tutoring answer was generated. This run validates retrieval and ranking only.")
    return "\n".join(lines) + "\n"


def _write_debug_csv(path: Path, run: dict[str, Any]) -> None:
    fields = [
        "query",
        "query_intent",
        "reasoning_intent",
        "rank",
        "chunk_id",
        "score",
        "source_video",
        "reasoning_type",
        "pedagogical_role",
        "retrieval_priority",
        "matched_terms",
        "matched_concepts",
        "matched_causal_chains",
        "matched_dictionary_terms",
        "query_expansion_terms",
        "knowledge_graph_boost_applied",
        "why_retrieved",
        *(
            [f"score_{key}" for key in run["retrieved_chunks"][0]["scoring_breakdown"].keys()]
            if run["retrieved_chunks"]
            else []
        ),
    ]
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        for rank, chunk in enumerate(run["retrieved_chunks"], start=1):
            row = {
                "query": run["query"],
                "query_intent": run["query_analysis"]["query_intent"],
                "reasoning_intent": run["query_analysis"]["reasoning_intent"],
                "rank": rank,
                "chunk_id": chunk["chunk_id"],
                "score": chunk["score"],
                "source_video": chunk["source_video"],
                "reasoning_type": chunk["reasoning_type"],
                "pedagogical_role": chunk["pedagogical_role"],
                "retrieval_priority": chunk["retrieval_priority"],
                "matched_terms": "|".join(chunk["matched_terms"]),
                "matched_concepts": "|".join(chunk.get("matched_concepts", [])),
                "matched_causal_chains": "|".join(chunk.get("matched_causal_chains", [])),
                "matched_dictionary_terms": "|".join(chunk.get("matched_dictionary_terms", [])),
                "query_expansion_terms": "|".join(chunk.get("query_expansion_terms", [])),
                "knowledge_graph_boost_applied": chunk.get("knowledge_graph_boost_applied", False),
                "why_retrieved": "|".join(chunk["why_retrieved"]),
            }
            for key, value in chunk["scoring_breakdown"].items():
                row[f"score_{key}"] = value
            writer.writerow(row)


def _passes_governance_filter(chunk: dict[str, Any]) -> bool:
    return (
        chunk.get("source_type") in ALLOWED_SOURCE_TYPES
        and chunk.get("agent_corpus") == ALLOWED_AGENT_CORPUS
        and chunk.get("safe_for_examiner") is False
        and chunk.get("official_grading_authority") is not True
    )


def _advanced_chunk_allowed(chunk: dict[str, Any], query_intent: str) -> bool:
    if chunk.get("academic_level") == "WSET_DIPLOMA":
        return query_intent == "advanced_enrichment"
    return True


def _matched_chunk_terms(chunk: dict[str, Any], query_analysis: dict[str, Any], text: str) -> list[str]:
    matched = set()
    lower = text.lower()
    for term in query_analysis.get("matched_terms", []):
        canonical = term["canonical_term"]
        if _contains_phrase(lower, canonical):
            matched.add(canonical)
    for token in query_analysis.get("query_tokens", []):
        if len(token) >= 4 and re.search(r"\b" + re.escape(token) + r"\b", lower):
            matched.add(token)
    for term in query_analysis.get("query_expansion_terms", []):
        if _contains_phrase(lower, term):
            matched.add(term)
    for key in ("sat_terms", "exam_terms", "canonical_terms_detected", "topics_detected", "grape_varieties", "regions"):
        for value in _as_list(chunk.get(key)):
            if value and _contains_phrase(" ".join(query_analysis.get("query_tokens", [])), value):
                matched.add(value)
    return sorted(matched)


def _matched_dictionary_terms(query_analysis: dict[str, Any], text: str) -> list[str]:
    lower = text.lower()
    return sorted(
        {
            term["canonical_term"]
            for term in query_analysis.get("matched_terms", [])
            if _contains_phrase(lower, term["canonical_term"])
        }
    )


def _matched_knowledge_terms(nodes: list[dict[str, Any]], text: str) -> list[str]:
    lower = text.lower()
    matched = set()
    for node in nodes:
        node_hits = [term for term in node.get("terms", []) if _contains_phrase(lower, term)]
        if node_hits:
            matched.add(node.get("name") or node.get("id") or node_hits[0])
            matched.update(node_hits[:4])
    return sorted(matched)


def _dictionary_category_score(chunk: dict[str, Any], query_analysis: dict[str, Any]) -> float:
    categories = {term.get("category", "") for term in query_analysis.get("matched_terms", []) if term.get("category")}
    if not categories:
        return 0.0
    chunk_fields = {
        "grape_varieties": "grape_variety",
        "regions": "region",
        "appellations": "appellation",
        "sat_terms": "sat",
        "exam_terms": "exam",
    }
    hits = 0
    for field, category in chunk_fields.items():
        if category in categories and _as_list(chunk.get(field)):
            hits += 1
    return min(1.0, hits / max(1, len(categories)))


def _source_concept_phrase_score(query_analysis: dict[str, Any], text: str) -> float:
    lower = text.lower()
    concept_names = [
        str(concept.get("name", "")).lower()
        for concept in query_analysis.get("matched_concepts", [])
        if len(_tokens(str(concept.get("name", "")))) >= 2
    ]
    if not concept_names:
        return 0.0
    hits = sum(1 for name in concept_names if _contains_phrase(lower, name))
    return min(1.0, hits / len(concept_names))


def _chunk_text_aligns_reasoning(text: str, reasoning_intent: str) -> bool:
    lower = text.lower()
    if reasoning_intent == "cause_effect":
        return bool(re.search(r"\b(?:because|therefore|leads? to|result(?:s)? in|cause|effect)\b", lower))
    if reasoning_intent == "sat_logic":
        return bool(re.search(r"\b(?:sat|systematic approach|quality assessment|justify|link)\b", lower))
    if reasoning_intent == "exam_strategy":
        return bool(re.search(r"\b(?:exam|marks|pass|question)\b", lower))
    if reasoning_intent == "answer_structure":
        return bool(re.search(r"\b(?:structure|answer|marks|question|paragraph)\b", lower))
    if reasoning_intent == "tasting_calibration":
        return bool(re.search(r"\b(?:balance|intensity|complexity|length|readiness|quality)\b", lower))
    return False


def _ranking_key(row: dict[str, Any]) -> tuple[float, str]:
    return (-float(row["score"]), row["chunk_id"])


def _select_diverse_results(scored: list[dict[str, Any]], top_k: int) -> list[dict[str, Any]]:
    limit = max(1, top_k)
    selected = scored[:limit]
    has_official = any(row.get("source_type") == "official_wset_extracted" for row in selected)
    has_pedagogical = any(row.get("source_type") != "official_wset_extracted" for row in selected)
    if has_official and has_pedagogical:
        return selected
    official = next((row for row in scored if row.get("source_type") == "official_wset_extracted"), None)
    pedagogical = next((row for row in scored if row.get("source_type") != "official_wset_extracted"), None)
    if official is None:
        return selected
    if not has_official and len(selected) < limit:
        return selected + [official]
    if not has_official:
        return [official, *selected[: limit - 1]]
    if pedagogical is not None and limit > 1:
        return [*selected[: limit - 1], pedagogical]
    return selected


def _section_topic_match_score(chunk: dict[str, Any], query_analysis: dict[str, Any]) -> float:
    metadata_text = " ".join(
        str(chunk.get(key, ""))
        for key in ("title", "section", "subtopic", "parent_section", "source_file")
    ).lower()
    if not metadata_text:
        return 0.0
    query_terms = set(query_analysis.get("query_tokens", [])) | set(_tokens(" ".join(query_analysis.get("query_expansion_terms", []))))
    if not query_terms:
        return 0.0
    hits = sum(1 for term in query_terms if len(term) >= 4 and _contains_phrase(metadata_text, term))
    return min(1.0, hits / max(1, min(len(query_terms), 6)))


def _summary_statistics(retrieved: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "retrieved_count": len(retrieved),
        "reasoning_type_counts": dict(Counter(row["reasoning_type"] for row in retrieved)),
        "pedagogical_role_counts": dict(Counter(row["pedagogical_role"] for row in retrieved)),
        "retrieval_priority_counts": dict(Counter(row["retrieval_priority"] for row in retrieved)),
    }


def _knowledge_node_type(node: dict[str, Any]) -> str:
    # Prefer explicit node_type field (causal_chain_v1 schema)
    explicit_type = str(node.get("node_type", "")).strip()
    if explicit_type == "causal_chain":
        return "causal_chains"
    if explicit_type in {"concept", "concepts"}:
        return "concepts"
    if explicit_type in {"relationship", "relationships"}:
        return "relationships"
    if explicit_type in {"misconception", "misconceptions"}:
        return "misconceptions"
    # Fall back to path and legacy field heuristics
    path = str(node.get("path", "")).replace("\\", "/")
    if "/concepts/" in path or node.get("concept_id"):
        return "concepts"
    if "/causal-chains/" in path or node.get("chain_id"):
        return "causal_chains"
    if "/relationships/" in path or node.get("relationship_id"):
        return "relationships"
    if "/misconceptions/" in path or node.get("misconception_id"):
        return "misconceptions"
    return ""


def _knowledge_node_id(node: dict[str, Any]) -> str:
    for key in ("concept_id", "chain_id", "node_id", "relationship_id", "misconception_id", "id"):
        if node.get(key):
            return str(node[key])
    return Path(str(node.get("path", ""))).stem


def _knowledge_node_name(node: dict[str, Any]) -> str:
    for key in ("concept_name", "chain_name", "relationship_id", "misconception", "name"):
        if node.get(key):
            value = str(node[key])
            return _identifier_to_phrase(value) if key == "relationship_id" else value
    return _identifier_to_phrase(_knowledge_node_id(node))


def _knowledge_node_primary_phrases(node: dict[str, Any]) -> list[str]:
    phrases = {_knowledge_node_name(node), _identifier_to_phrase(_knowledge_node_id(node))}
    for key in (
        "definition",
        "distinction_note",
        "conditions",
        "explanation",
        "why_incorrect",
        "corrected_understanding",
        "relationship_type",
    ):
        if node.get(key):
            phrases.update(_important_phrases(str(node[key])))
    for key in ("source_concept", "target_concept", "related_concepts", "cause_effect_links"):
        for value in _as_list(node.get(key)):
            phrases.add(_identifier_to_phrase(value))
    for item in _as_list(node.get("distinction_insights")):
        phrases.update(_important_phrases(item))
    for item in _as_list(node.get("related_exam_questions")):
        phrases.update(_important_phrases(item))
    for section in ("starting_factor", "final_outcome"):
        value = node.get(section)
        if isinstance(value, dict):
            phrases.add(_identifier_to_phrase(str(value.get("concept_id", ""))))
            phrases.update(_important_phrases(str(value.get("description", ""))))
    for step in node.get("intermediate_steps", []) if isinstance(node.get("intermediate_steps"), list) else []:
        if isinstance(step, dict):
            phrases.add(_identifier_to_phrase(str(step.get("concept_id", ""))))
            phrases.update(_important_phrases(str(step.get("description", ""))))
            phrases.update(_important_phrases(str(step.get("relationship_type", ""))))
    # Include trigger_keywords from causal chain nodes (causal_chain_v1 schema)
    for kw in _as_list(node.get("trigger_keywords")):
        phrases.add(str(kw).lower().strip())
    # Include step texts from causal_chain_v1 schema
    for step in node.get("steps", []) if isinstance(node.get("steps"), list) else []:
        if isinstance(step, dict):
            phrases.update(_important_phrases(str(step.get("text", ""))))
    return sorted({phrase.lower().strip() for phrase in phrases if len(phrase.strip()) >= 3})


def _important_phrases(text: str) -> set[str]:
    lower = text.lower()
    phrases = set()
    candidates = (
        "cool climate",
        "slow ripening",
        "slower ripening",
        "high acidity",
        "higher acidity",
        "acid retention",
        "malic acid",
        "tartaric acid",
        "lower ph",
        "growing season",
        "quality assessment",
        "balance",
        "intensity",
        "complexity",
        "length",
        "readiness",
        "cause and effect",
        "whole bunch",
        "malolactic conversion",
        "noble rot",
        "lees ageing",
        "oak influence",
    )
    for candidate in candidates:
        if candidate in lower:
            phrases.add(candidate)
    phrases.update(_identifier_to_phrase(token) for token in re.findall(r"\bC_[A-Z0-9_]+\b", text))
    return {phrase for phrase in phrases if phrase}


def _identifier_to_phrase(value: str) -> str:
    text = str(value or "")
    text = re.sub(r"^(?:C|CC|R|MC|T)_", "", text, flags=re.IGNORECASE)
    text = text.replace("__", " ").replace("_", " ").replace("→", " ")
    text = re.sub(r"\b(?:increases|reduces|contrasts|often|confused|with|produces|influences)\b", " ", text, flags=re.IGNORECASE)
    return re.sub(r"\s+", " ", text).strip().lower()


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    if not path.exists():
        return rows
    with path.open("r", encoding="utf-8-sig") as file:
        for line_number, line in enumerate(file, start=1):
            if not line.strip():
                continue
            try:
                value = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSONL in {path}:{line_number}") from exc
            if isinstance(value, dict):
                rows.append(value)
    return rows


def _tokens(text: str) -> list[str]:
    return [
        token
        for token in re.findall(r"(?u)\b[^\W\d_](?:[^\W_]|['-])*\b", text.lower())
        if token not in STOPWORDS and len(token) > 1
    ]


def _contains_phrase(haystack_lower: str, phrase: str) -> bool:
    phrase_lower = str(phrase).lower().strip()
    if not phrase_lower:
        return False
    return bool(re.search(r"(?<!\w)" + re.escape(phrase_lower) + r"(?!\w)", haystack_lower))


def _excerpt(text: str, max_length: int = 360) -> str:
    normalized = re.sub(r"\s+", " ", text).strip()
    if len(normalized) <= max_length:
        return normalized
    return normalized[: max_length - 3].rstrip() + "..."


def _as_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value]
    if value in (None, ""):
        return []
    return [str(value)]


def _safe_output_prefix(value: str) -> str:
    safe = re.sub(r"[^A-Za-z0-9._-]+", "_", value).strip("._-")
    return safe or "retrieval_run"


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Tutor retrieval validation sandbox.")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--query", required=True)
    parser.add_argument("--top-k", type=int, default=10)
    parser.add_argument("--output-prefix", default="retrieval_run")
    args = parser.parse_args(argv)
    run = run_retrieval_sandbox(
        root=args.root,
        query=args.query,
        top_k=args.top_k,
        output_prefix=args.output_prefix,
    )
    print(f"Query intent: {run['query_analysis']['query_intent']}")
    print(f"Reasoning intent: {run['query_analysis']['reasoning_intent']}")
    print(f"Indexed chunks: {run['indexed_chunks']}")
    print(f"Golden chunks loaded: {run['golden_chunks_loaded']}")
    print(f"Dictionary terms loaded: {run['dictionary_terms_loaded']}")
    for index, chunk in enumerate(run["retrieved_chunks"], start=1):
        print(
            f"{index}. {chunk['score']:.4f} {chunk['chunk_id']} "
            f"[{chunk['reasoning_type']} / {chunk['retrieval_priority']}]"
        )
        print(f"   why: {'; '.join(chunk['why_retrieved'])}")


if __name__ == "__main__":
    main()
