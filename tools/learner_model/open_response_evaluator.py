"""Open Response Evaluator v1 — deterministic evaluation of student open responses.

Evaluates a student's free-text response against targeted CC_IDs and MC_IDs.
Returns a structured profile with concept and causal coverage, reasoning quality,
and remediation pointers from the WWJ lookup.

Profile constants:
  FOUNDATIONAL_RESPONSE — covers < 50% of targeted concepts, superficial reasoning
  DEVELOPING_RESPONSE   — covers 50–79% of targeted concepts, developing reasoning
  STRONG_RESPONSE       — covers ≥ 80% of targeted concepts, strong reasoning

Internal-only lab profiles (ACCEPTABLE / MERIT / DISTINCTION_LIKE) may exist as
private constants but are never exposed in default output.

Forbidden strings — must never appear in any output, comment, or constant:
  WSET_PASS, WSET_MERIT, WSET_DISTINCTION

Governance: never grades or scores for examiner purposes; never calls LLM, API,
embeddings, or cloud services; safe_for_examiner is always False.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from tools.learner_model.causal_runtime import (
    CAUSAL_CHAINS_DIR,
    CAUSAL_SIGNALS_PATH,
    detect_cc_coverage,
)
from tools.learner_model.wwj_remediation import WWJ_LOOKUP_PATH, get_remediation_path

# Public profile identifiers
PROFILE_FOUNDATIONAL = "FOUNDATIONAL_RESPONSE"
PROFILE_DEVELOPING = "DEVELOPING_RESPONSE"
PROFILE_STRONG = "STRONG_RESPONSE"

# Private lab-only profile constants (not exposed in output)
_LAB_PROFILE_ACCEPTABLE = "ACCEPTABLE_RESPONSE"
_LAB_PROFILE_MERIT = "MERIT_RESPONSE"
_LAB_PROFILE_DISTINCTION = "DISTINCTION_LIKE_RESPONSE"


def evaluate_open_response(
    student_response: str,
    question_context: dict[str, Any],
    *,
    signals_path: Path = CAUSAL_SIGNALS_PATH,
    cc_dir: Path = CAUSAL_CHAINS_DIR,
    lookup_path: Path = WWJ_LOOKUP_PATH,
) -> dict[str, Any]:
    """Evaluate a student open response against targeted CC_IDs and MC_IDs.

    Args:
        student_response: Free-text response from the student.
        question_context: Dict with cc_ids_targeted, mc_ids_relevant, topic, ra_id.
        signals_path: Path override for causal_chain_signals.json (testing).
        cc_dir: Path override for causal chain JSON files (testing).
        lookup_path: Path override for mc_wwj_lookup.json (testing).

    Returns:
        Evaluation result dict.  Governance flags always False.
        profile is one of FOUNDATIONAL_RESPONSE, DEVELOPING_RESPONSE, STRONG_RESPONSE.
    """
    cc_ids_targeted: list[str] = list(question_context.get("cc_ids_targeted") or [])
    mc_ids_relevant: list[str] = list(question_context.get("mc_ids_relevant") or [])

    # --- Causal and concept coverage ---
    chains_present, chains_absent = detect_cc_coverage(
        student_response, cc_ids_targeted, cc_dir=cc_dir
    )
    total_targeted = len(cc_ids_targeted)
    present_count = len(chains_present)
    coverage_ratio = present_count / total_targeted if total_targeted > 0 else 0.0

    # --- Reasoning quality and profile ---
    reasoning_quality = _score_reasoning_quality(present_count, total_targeted)
    profile = _classify_profile(coverage_ratio)

    # --- Remediation from WWJ lookup ---
    wwj_chunks: list[str] = []
    for mc_id in mc_ids_relevant:
        path_obj = get_remediation_path(mc_id, lookup_path=lookup_path)
        wwj_chunks.extend(path_obj["wwj_chunks"])
    seen: set[str] = set()
    wwj_deduped: list[str] = []
    for chunk in wwj_chunks:
        if chunk not in seen:
            seen.add(chunk)
            wwj_deduped.append(chunk)

    return {
        "profile": profile,
        "concept_coverage": {
            "concepts_present": list(chains_present),
            "concepts_absent": list(chains_absent),
        },
        "causal_coverage": {
            "chains_present": list(chains_present),
            "chains_absent": list(chains_absent),
        },
        "reasoning_quality": reasoning_quality,
        "remediation": {
            "concepts_to_reinforce": list(chains_absent),
            "causality_to_reinforce": list(chains_absent),
            "wwj_chunks": wwj_deduped,
        },
        "governance": {
            "safe_for_examiner": False,
            "examiner_scoring_allowed": False,
            "official_wset_question": False,
            "training_item_only": True,
        },
    }


def _classify_profile(coverage_ratio: float) -> str:
    if coverage_ratio >= 0.8:
        return PROFILE_STRONG
    if coverage_ratio >= 0.5:
        return PROFILE_DEVELOPING
    return PROFILE_FOUNDATIONAL


def _score_reasoning_quality(present_count: int, total_targeted: int) -> str:
    if total_targeted == 0:
        return "superficial"
    ratio = present_count / total_targeted
    if ratio >= 0.8:
        return "strong"
    if ratio >= 0.4:
        return "developing"
    return "superficial"
