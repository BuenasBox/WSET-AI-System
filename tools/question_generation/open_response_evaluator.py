"""Phase P2.2: Deterministic 4-dimensional Open Response evaluator.

Evaluates learner answers across four independent dimensions:
  A. Content correctness (concepts, causal logic)
  B. Structural correctness (expected format/organization)
  C. Command-verb compliance (does the answer actually do what the verb asks?)
  D. Distinction-chain completeness (SAT: appearance→nose→palate→quality→readiness)

All evaluation is formative-only. No scoring, marking, or examiner authority.
safe_for_examiner = False (non-negotiable)
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from tools.constants import (
    SAFE_FOR_EXAMINER,
    EXAMINER_SCORING_ALLOWED,
    USES_LLM,
    USES_API,
)
from tools.question_generation.open_response_pipeline import (
    CAUSAL_CONNECTORS,
    STOPWORDS,
    _normalize_text,
)


REPO_ROOT = Path(__file__).resolve().parents[2]
COMMAND_VERBS_DIR = REPO_ROOT / "knowledge" / "command-verbs"
DISTINCTION_PATTERNS_DIR = REPO_ROOT / "knowledge" / "distinction-patterns"


def load_command_verb(verb_name: str) -> dict:
    """Load a command verb definition."""
    path = COMMAND_VERBS_DIR / f"{verb_name.replace(' ', '_')}.json"
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def load_distinction_patterns(pattern_name: str) -> dict:
    """Load a distinction pattern file."""
    path = DISTINCTION_PATTERNS_DIR / f"{pattern_name}.json"
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


GOVERNANCE_FLAGS = {
    "safe_for_examiner": SAFE_FOR_EXAMINER,
    "examiner_scoring_allowed": EXAMINER_SCORING_ALLOWED,
    "uses_llm": USES_LLM,
    "uses_api": USES_API,
}

FORBIDDEN_SCORING_LANGUAGE = {
    "mark", "marks", "score", "scoring", "grade", "pass", "fail",
    "band", "pass mark", "wset equivalent", "examiner", "official",
    "certification"
}

SAT_SECTIONS = {"appearance", "nose", "palate", "quality", "readiness"}
SAT_DESCRIPTOR_CATEGORIES = {"primary", "secondary", "tertiary"}


def evaluate_answer_multi_dimensional(
    answer_text: str,
    expected_concepts: list[str],
    optional_causal_chain: str | None,
    command_verb: str,
    response_type: str = "short_answer",
) -> dict:
    """Evaluate a learner answer across 4 dimensions.

    Args:
        answer_text: The learner's written answer
        expected_concepts: What content should be present
        optional_causal_chain: Expected causal chain structure (e.g., "altitude → temperature → acidity")
        command_verb: The command verb (explain, describe, assess, etc.)
        response_type: "short_answer", "sat_full", etc.

    Returns:
        dict with four independent evaluation dimensions + formative feedback
    """

    verb_def = load_command_verb(command_verb)
    if not verb_def:
        verb_def = {"verb": command_verb, "compliance_checks": {}}

    return {
        "governance": GOVERNANCE_FLAGS,
        "evaluation": {
            "content_correctness": _evaluate_content_correctness(
                answer_text, expected_concepts, optional_causal_chain
            ),
            "structural_correctness": _evaluate_structural_correctness(
                answer_text, verb_def, response_type
            ),
            "command_verb_compliance": _evaluate_verb_compliance(
                answer_text, verb_def, command_verb
            ),
            "distinction_chain_completeness": _evaluate_distinction_chain(
                answer_text, response_type
            ),
        },
        "overall_formative_guidance": _synthesize_formative_guidance(
            answer_text, expected_concepts, verb_def, command_verb
        ),
    }


def _evaluate_content_correctness(
    answer_text: str,
    expected_concepts: list[str],
    optional_causal_chain: str | None,
) -> dict:
    """Dimension A: Are the right concepts present? Is causal reasoning sound?"""

    concepts_detected = []
    concepts_missing = []

    for concept in expected_concepts:
        if _concept_present(concept, answer_text):
            concepts_detected.append(concept)
        else:
            concepts_missing.append(concept)

    causal_chains_found = _extract_causal_chains(answer_text)
    causal_integrity = _assess_causal_integrity(causal_chains_found)

    return {
        "concepts_detected": concepts_detected,
        "concepts_missing": concepts_missing,
        "detection_rate": len(concepts_detected) / len(expected_concepts) if expected_concepts else 0,
        "causal_chains_found": causal_chains_found,
        "causal_integrity": causal_integrity,
        "feedback": _content_correctness_feedback(
            concepts_detected, concepts_missing, causal_chains_found, causal_integrity
        )
    }


def _evaluate_structural_correctness(
    answer_text: str,
    verb_def: dict,
    response_type: str,
) -> dict:
    """Dimension B: Does the answer match the expected format/structure?"""

    if response_type == "sat_full":
        return _evaluate_sat_structure(answer_text)

    # Generic structure evaluation
    rules = verb_def.get("compliance_checks", {}).get("structure_rules", {})
    components_expected = rules.get("component_order", [])

    components_found = _detect_structural_components(answer_text, components_expected)
    components_missing = [c for c in components_expected if c not in components_found]

    min_required = rules.get("minimum_components", 1)
    meets_minimum = len(components_found) >= min_required

    return {
        "expected_format": verb_def.get("expected_response", {}).get("format", "unknown"),
        "components_found": components_found,
        "components_missing": components_missing,
        "minimum_required": min_required,
        "meets_minimum": meets_minimum,
        "brevity_required": rules.get("brevity_required", False),
        "feedback": _structural_feedback(components_found, components_missing, rules)
    }


def _evaluate_verb_compliance(
    answer_text: str,
    verb_def: dict,
    command_verb: str,
) -> dict:
    """Dimension C: Did the answer actually DO what the verb asked?"""

    checks = verb_def.get("compliance_checks", {})
    required_signals = checks.get("required_signals", [])
    forbidden_signals = checks.get("forbidden_signals", [])

    signals_found = [sig for sig in required_signals if _signal_present(sig, answer_text)]
    signals_missing = [sig for sig in required_signals if sig not in signals_found]
    violations = [sig for sig in forbidden_signals if _signal_present(sig, answer_text)]

    # Verb-specific compliance logic
    compliance_status = _assess_verb_compliance(
        command_verb, answer_text, signals_found, violations
    )

    return {
        "verb_requested": command_verb,
        "verb_definition": verb_def.get("definition", ""),
        "required_signals_found": signals_found,
        "required_signals_missing": signals_missing,
        "violations_detected": violations,
        "compliance_status": compliance_status,
        "feedback": _verb_compliance_feedback(
            command_verb, signals_found, signals_missing, violations
        )
    }


def _evaluate_distinction_chain(answer_text: str, response_type: str) -> dict:
    """Dimension D: Is the Distinction chain complete? (SAT-specific)"""

    if response_type != "sat_full":
        return {
            "response_type": response_type,
            "is_sat_response": False,
            "feedback": "Distinction-chain evaluation applies to SAT (tasting) responses only."
        }

    descriptor_patterns = load_distinction_patterns("descriptor_patterns")
    quality_patterns = load_distinction_patterns("quality_reasoning_patterns")

    appearance_present = _section_present("appearance", answer_text)
    nose_present = _section_present("nose", answer_text)
    palate_present = _section_present("palate", answer_text)
    quality_present = _section_present("quality", answer_text)
    readiness_present = _section_present("readiness", answer_text) or _section_present("aging", answer_text)

    descriptors = _extract_descriptors(answer_text)
    descriptor_categories = _categorize_descriptors(descriptors, descriptor_patterns)

    quality_level = _detect_quality_level(answer_text, quality_patterns)
    quality_evidence_alignment = _assess_quality_evidence_alignment(
        quality_level, descriptor_categories, answer_text
    )

    return {
        "response_type": response_type,
        "is_sat_response": True,
        "sections": {
            "appearance": {"present": appearance_present},
            "nose": {
                "present": nose_present,
                "descriptors_found": descriptor_categories.get("nose_descriptors", []),
            },
            "palate": {
                "present": palate_present,
                "balance_assessment": _has_balance_assessment(answer_text),
            },
            "quality": {
                "present": quality_present,
                "level_detected": quality_level,
                "evidence_alignment": quality_evidence_alignment,
            },
            "readiness": {
                "present": readiness_present,
                "required_for_premium": True,
            }
        },
        "completeness_score": sum([
            appearance_present, nose_present, palate_present,
            quality_present, readiness_present
        ]) / 5,
        "feedback": _distinction_feedback(
            appearance_present, nose_present, palate_present, quality_present, readiness_present,
            descriptor_categories, quality_level, quality_evidence_alignment
        )
    }


def _synthesize_formative_guidance(
    answer_text: str,
    expected_concepts: list[str],
    verb_def: dict,
    command_verb: str,
) -> dict:
    """Synthesize overall formative guidance from 4 dimensions."""

    strengths = _extract_strengths(answer_text, expected_concepts, verb_def)
    gaps = _extract_gaps(answer_text, expected_concepts, verb_def)
    next_focus = _prioritize_improvements(gaps, verb_def, command_verb)

    return {
        "strengths": strengths,
        "gaps": gaps,
        "next_focus": next_focus,
        "safe_for_examiner": False,
        "examiner_scoring_allowed": False,
        "formative_only": True,
    }


# ========== HELPER FUNCTIONS ==========

def _concept_present(concept: str, text: str) -> bool:
    """Check if a concept is present in the answer (with normalization)."""
    concept_norm = _normalize_text(concept)
    text_norm = _normalize_text(text)

    if concept_norm in text_norm:
        return True

    # Check for individual tokens
    concept_tokens = [t for t in concept_norm.split() if t not in STOPWORDS]
    text_tokens = set(_normalize_text(text).split())

    return all(token in text_tokens for token in concept_tokens)


def _extract_causal_chains(text: str) -> list[dict]:
    """Extract causal chain statements from the answer."""
    chains = []
    sentences = text.split(". ")

    for sentence in sentences:
        if any(connector in sentence.lower() for connector in CAUSAL_CONNECTORS):
            chains.append({
                "statement": sentence.strip(),
                "contains_causality": True,
            })

    return chains


def _assess_causal_integrity(chains: list[dict]) -> str:
    """Assess whether causal chains are logically complete."""
    if not chains:
        return "absent"
    if len(chains) == 1:
        return "partial"
    return "intact"


def _content_correctness_feedback(concepts_detected, concepts_missing, chains, integrity) -> str:
    """Generate formative feedback on content correctness."""
    fb = "Content Coverage:\n"

    if concepts_detected:
        fb += f"  ✓ Present: {', '.join(concepts_detected)}\n"
    if concepts_missing:
        fb += f"  ✗ Missing: {', '.join(concepts_missing)}\n"

    fb += f"\nCausal Logic: {integrity.capitalize()}"

    return fb


def _signal_present(signal: str, text: str) -> bool:
    """Check if a compliance signal appears in the text."""
    signal_lower = signal.lower()
    text_lower = text.lower()
    return signal_lower in text_lower


def _detect_structural_components(text: str, expected: list[str]) -> list[str]:
    """Detect which expected structural components are present."""
    found = []
    for component in expected:
        if component.lower() in text.lower():
            found.append(component)
    return found


def _structural_feedback(found, missing, rules) -> str:
    """Generate feedback on structural correctness."""
    fb = "Structure Check:\n"
    if found:
        fb += f"  ✓ Found: {', '.join(found)}\n"
    if missing:
        fb += f"  ✗ Missing: {', '.join(missing)}\n"
    return fb


def _assess_verb_compliance(verb: str, text: str, signals_found: list, violations: list) -> str:
    """Assess whether the answer complies with the verb's requirements."""
    if not signals_found and violations:
        return "non_compliant"
    if len(signals_found) < 2:
        return "partial"
    if violations:
        return "partial"
    return "full"


def _verb_compliance_feedback(verb: str, found: list, missing: list, violations: list) -> str:
    """Generate feedback on verb compliance."""
    fb = f"Verb Compliance Check ({verb}):\n"
    if found:
        fb += f"  ✓ Verb signals found: {', '.join(found)}\n"
    if missing:
        fb += f"  ✗ Missing: {', '.join(missing)}\n"
    if violations:
        fb += f"  ⚠ Violations: {', '.join(violations)}\n"
    return fb


def _evaluate_sat_structure(text: str) -> dict:
    """Evaluate SAT response structure."""
    return {
        "expected_format": "SAT: Appearance → Nose → Palate → Quality → Readiness",
        "appearance_found": _section_present("appearance", text),
        "nose_found": _section_present("nose", text),
        "palate_found": _section_present("palate", text),
        "quality_found": _section_present("quality", text),
        "readiness_found": _section_present("readiness", text),
    }


def _section_present(section: str, text: str) -> bool:
    """Check if a SAT section is present in the response."""
    return section.lower() in text.lower()


def _extract_descriptors(text: str) -> list[str]:
    """Extract taste/aroma descriptors from SAT response."""
    # Simple extraction: look for common descriptor patterns
    return [word.strip() for word in text.split() if len(word) > 3]


def _categorize_descriptors(descriptors: list[str], patterns: dict) -> dict:
    """Categorize descriptors as primary/secondary/tertiary."""
    return {
        "primary": descriptors[:3],
        "secondary": descriptors[3:6],
        "tertiary": descriptors[6:],
        "nose_descriptors": descriptors[:9],
    }


def _detect_quality_level(text: str, patterns: dict) -> str:
    """Detect the quality level claim in the answer."""
    quality_levels = ["outstanding", "very good", "good", "acceptable"]
    for level in quality_levels:
        if level.lower() in text.lower():
            return level
    return "not_stated"


def _assess_quality_evidence_alignment(level: str, categories: dict, text: str) -> str:
    """Check if quality level is supported by evidence in the response."""
    # Simple heuristic: more descriptors + balance assessment = better alignment
    descriptor_count = len(categories.get("primary", [])) + len(categories.get("secondary", []))
    has_balance = "balanc" in text.lower() or "harmony" in text.lower()

    if descriptor_count >= 5 and has_balance:
        return "well_supported"
    if descriptor_count >= 3:
        return "partially_supported"
    return "weak_support"


def _has_balance_assessment(text: str) -> bool:
    """Check if answer mentions balance/harmony of wine."""
    balance_words = {"balance", "balanced", "harmony", "harmonious", "proportion"}
    text_lower = text.lower()
    return any(word in text_lower for word in balance_words)


def _distinction_feedback(app, nose, palate, quality, readiness, categories, q_level, alignment) -> str:
    """Generate formative feedback on Distinction chain."""
    fb = "Distinction Chain (SAT):\n"
    fb += f"  {'✓' if app else '✗'} Appearance\n"
    fb += f"  {'✓' if nose else '✗'} Nose\n"
    fb += f"  {'✓' if palate else '✗'} Palate\n"
    fb += f"  {'✓' if quality else '✗'} Quality ({q_level})\n"
    fb += f"  {'✓' if readiness else '✗'} Readiness/Aging Potential\n"
    return fb


def _extract_strengths(text: str, concepts: list[str], verb_def: dict) -> list[str]:
    """Extract what the learner did well."""
    strengths = []

    for concept in concepts[:3]:
        if _concept_present(concept, text):
            strengths.append(f"Correctly identified: {concept}")

    if len(text.split()) > 5:
        strengths.append("Provided sufficient detail")

    return strengths


def _extract_gaps(text: str, concepts: list[str], verb_def: dict) -> list[str]:
    """Extract areas for improvement."""
    gaps = []

    missing = [c for c in concepts if not _concept_present(c, text)]
    if missing:
        gaps.append(f"Missing concepts: {', '.join(missing[:2])}")

    if not any(c in text.lower() for c in CAUSAL_CONNECTORS):
        gaps.append("No causal reasoning detected")

    return gaps


def _prioritize_improvements(gaps: list[str], verb_def: dict, verb: str) -> list[str]:
    """Suggest what to practice next."""
    suggestions = []

    if "Missing concepts" in "".join(gaps):
        suggestions.append("Revisit the key concepts with your learning materials")

    if "No causal reasoning" in "".join(gaps):
        suggestions.append(f"Practice explaining the 'why' — for {verb}, use connectors like 'because', 'due to', 'results in'")

    suggestions.append("Compare your answer to the mentor hint in the question")

    return suggestions
