"""Deterministic open response practice pipeline foundation.

This module is intentionally local and pure. It maps structured question-bank
records into training-only open response candidates and evaluates learner text
with simple concept and causal-link checks. It does not call Tutor, retrieval,
LLMs, APIs, embeddings, vector databases, or cloud services.
"""

from __future__ import annotations

import copy
import json
import re
import unicodedata
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from tools.constants import (
    CLOUD_SERVICES_ACTIVE,
    EXAMINER_SCORING_ALLOWED,
    SAFE_FOR_EXAMINER,
    USES_API,
    USES_EMBEDDINGS,
    USES_LLM,
    USES_VECTOR_DB,
    tokenize_term,
)


OPEN_RESPONSE_TYPES: frozenset[str] = frozenset(
    {
        "short_answer",
        "short answer",
        "open_response",
        "open response",
        "abierta",
        "respuesta abierta",
        "pregunta abierta",
    }
)

SOURCE_BANK_PATH = "knowledge/question-bank/structured/wset3_questions.json"
OFFICIAL_CHUNKS_PATH = "knowledge/official-wset/study-guide/official-chunks/official_wset_chunks.jsonl"
SCHEMA_VERSION = "diagnostic_open_response_v1"
QUESTION_TYPE = "diagnostic_open_response"
UNKNOWN = "unknown"
REVIEW_APPROVED = "approved"
REVIEW_REQUIRES_REVISION = "requires_revision"
REVIEW_REJECTED = "rejected"
ACTIVATION_INACTIVE = "inactive"
MAX_EVIDENCE_CHUNKS = 3
MIN_GROUNDING_TERMS = 3

GOVERNANCE_FLAGS: dict[str, bool] = {
    "safe_for_examiner": SAFE_FOR_EXAMINER,
    "examiner_scoring_allowed": EXAMINER_SCORING_ALLOWED,
    "official_wset_question": False,
    "training_item_only": True,
    "uses_llm": USES_LLM,
    "uses_api": USES_API,
    "uses_embeddings": USES_EMBEDDINGS,
    "uses_vector_db": USES_VECTOR_DB,
    "cloud_services_active": CLOUD_SERVICES_ACTIVE,
}

FEEDBACK_RUBRIC: dict[str, str] = {
    "concept_coverage": "expected_concept_presence",
    "causal_link": "formative_causal_link_presence",
    "formative_feedback": "training_guidance_only",
    "needs_review": "derived_from_missing_or_partial_concepts",
}

FORBIDDEN_FIELD_PARTS: tuple[str, ...] = (
    "score",
    "scoring",
    "mark",
    "marks",
    "grade",
    "pass",
    "fail",
    "examiner_authority",
    "official_result",
)

ALLOWED_GOVERNANCE_FIELD_NAMES: frozenset[str] = frozenset(
    {
        "examiner_scoring_allowed",
    }
)

CAUSAL_CONNECTORS: frozenset[str] = frozenset(
    {
        "porque",
        "debido",
        "causa",
        "causar",
        "provoca",
        "produce",
        "resulta",
        "resultado",
        "conduce",
        "influye",
        "afecta",
        "impacta",
        "therefore",
        "because",
        "leads",
        "results",
    }
)

UNSUPPORTED_CLAIM_TERMS: tuple[str, ...] = (
    "siempre",
    "nunca",
    "garantiza",
    "garantizado",
    "solo",
    "unicamente",
    "automáticamente",
    "automatica",
)

STOPWORDS: frozenset[str] = frozenset(
    {
        "a",
        "al",
        "and",
        "de",
        "del",
        "el",
        "en",
        "for",
        "la",
        "las",
        "los",
        "of",
        "the",
        "to",
        "un",
        "una",
        "y",
    }
)

GROUNDING_ALIASES: dict[str, tuple[str, ...]] = {
    "acero inoxidable": ("stainless steel",),
    "acidez": ("acidity",),
    "ácido láctico": ("lactic acid",),
    "ácido málico": ("malic acid",),
    "agua": ("water",),
    "aireación": ("air circulation",),
    "alcohol": ("alcohol",),
    "altura": ("altitude",),
    "altitud": ("altitude",),
    "amargor": ("bitterness",),
    "americano": ("american",),
    "antocianos": ("anthocyanins",),
    "arcilla": ("clay",),
    "arena": ("sand",),
    "aromas": ("aroma", "flavour"),
    "aromas primarios": ("primary aromas",),
    "astringencia": ("astringency",),
    "autóctonas": ("wild",),
    "azúcar": ("sugar",),
    "baya": ("berry", "berries"),
    "bayas pequeñas": ("small berries",),
    "biodinámico": ("biodynamic",),
    "brotes": ("shoots",),
    "calor": ("heat",),
    "canopy": ("canopy",),
    "clima cálido": ("warm climate",),
    "coco": ("coconut",),
    "color": ("colour",),
    "competencia": ("competition",),
    "complejidad": ("complexity",),
    "concentración": ("concentration",),
    "control": ("control",),
    "control de temperatura": ("temperature control",),
    "coste": ("cost",),
    "costo": ("cost",),
    "cuerpo": ("body",),
    "defectos": ("faults",),
    "densidad": ("density",),
    "densidad de plantación": ("density of planting",),
    "deshojado": ("leaf removal",),
    "diacetilo": ("diacetyl",),
    "drenaje": ("drainage",),
    "enfermedad": ("disease",),
    "envejecimiento": ("ageing",),
    "equilibrio": ("balance",),
    "especias": ("spice",),
    "estrés hídrico": ("water stress",),
    "estilo": ("style",),
    "exposición": ("exposure", "sunlight"),
    "extracción": ("extraction",),
    "fenoles": ("phenolics",),
    "fermentación": ("fermentation",),
    "fermentación maloláctica": ("malolactic fermentation", "mlf"),
    "francés": ("french",),
    "gas inerte": ("inert gas",),
    "granizo": ("hail",),
    "grava": ("gravel",),
    "helada": ("frost",),
    "hongos": ("fungal",),
    "inerte": ("inert",),
    "inoxidable": ("stainless steel",),
    "invierno": ("winter",),
    "latitud": ("latitude",),
    "levadura": ("yeast",),
    "levaduras": ("yeast",),
    "maceración": ("maceration",),
    "maceración prolongada": ("extended maceration",),
    "maduración": ("ripening", "maturation"),
    "maloláctica": ("malolactic", "mlf"),
    "manejo del dosel": ("canopy management",),
    "mano de obra": ("labour",),
    "mecanización": ("mechanisation",),
    "moderado": ("moderate",),
    "nutrientes": ("nutrients",),
    "orgánico": ("organic",),
    "orientación": ("aspect",),
    "oxidación": ("oxidation",),
    "oxígeno": ("oxygen",),
    "parada fermentativa": ("stuck fermentation",),
    "pendiente": ("slope",),
    "percepción": ("consumer", "market"),
    "piel": ("skin",),
    "plantación": ("planting",),
    "poda": ("pruning",),
    "poda de invierno": ("winter pruning",),
    "precio": ("price", "cost"),
    "recipiente inerte": ("inert vessel",),
    "rendimiento": ("yield",),
    "retención": ("retention",),
    "riego": ("irrigation",),
    "riesgo": ("risk",),
    "roble": ("oak",),
    "salvajes": ("wild",),
    "seleccionada": ("selected",),
    "selección": ("sorting", "selection"),
    "sequía": ("drought",),
    "SO₂": ("sulfur dioxide", "so2"),
    "so2": ("sulfur dioxide", "so2"),
    "sol": ("sunlight",),
    "sostenibilidad": ("sustainability", "sustainable", "organic", "biodynamic"),
    "sostenible": ("sustainable",),
    "suelo": ("soil",),
    "sulfuroso": ("sulfur dioxide", "so2"),
    "tanino": ("tannin",),
    "temperatura": ("temperature",),
    "textura": ("texture",),
    "tostado": ("toast",),
    "vainilla": ("vanilla",),
    "vendimia": ("harvest",),
    "vigor": ("vigour", "vigor"),
    "yemas": ("buds",),
}


def is_open_response_record(record: Any) -> bool:
    """Return True for structured records preserved for open response use."""
    if not isinstance(record, Mapping):
        return False
    question_type = _normalize_question_type(record.get("question_type"))
    return question_type in {_normalize_question_type(value) for value in OPEN_RESPONSE_TYPES}


def find_open_response_records(records: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    """Return deep-copied open response records in source order."""
    return [copy.deepcopy(dict(record)) for record in records if is_open_response_record(record)]


def build_open_response_candidate(
    record: Mapping[str, Any],
    source_bank_path: str = SOURCE_BANK_PATH,
) -> dict[str, Any]:
    """Map one structured open response record into the internal contract."""
    topics = _string_list(record.get("expected_topics"))
    expected_concepts = _expected_concepts(record)
    causal_links = _string_list(record.get("expected_causal_links"))
    ra = _extract_ra(topics)
    topic, subtopic = _extract_topic_subtopic(topics, ra)

    return {
        "schema_version": SCHEMA_VERSION,
        "source_question_id": str(record.get("question_id", "")).strip(),
        "question_type": QUESTION_TYPE,
        "stem": str(record.get("question_text", "")).strip(),
        "RA": ra,
        "topic": topic,
        "subtopic": subtopic,
        "difficulty": _difficulty(record.get("difficulty")),
        "expected_concepts": expected_concepts,
        "optional_causal_chain": causal_links[0] if causal_links else None,
        "corpus_support": {
            "status": "source_metadata_only",
            "source_question_bank": source_bank_path,
            "source_type": str(record.get("source_type", "") or UNKNOWN).strip(),
            "support_terms": expected_concepts,
            "evidence_chunks": [],
        },
        "review_status": REVIEW_REQUIRES_REVISION,
        "activation_status": ACTIVATION_INACTIVE,
        "feedback_rubric": copy.deepcopy(FEEDBACK_RUBRIC),
        "governance_flags": copy.deepcopy(GOVERNANCE_FLAGS),
    }


def build_open_response_candidates(
    records: Sequence[Mapping[str, Any]],
    source_bank_path: str = SOURCE_BANK_PATH,
) -> list[dict[str, Any]]:
    """Build normalized candidates from all open response records."""
    return [
        build_open_response_candidate(record, source_bank_path)
        for record in find_open_response_records(records)
    ]


def build_grounded_open_response_candidate(
    record: Mapping[str, Any],
    corpus_chunks: Sequence[Mapping[str, Any]] | None = None,
    source_bank_path: str = SOURCE_BANK_PATH,
) -> dict[str, Any]:
    """Build a cleaned candidate with deterministic corpus grounding and review gate."""
    candidate = build_open_response_candidate(record, source_bank_path)
    candidate["corpus_support"] = ground_candidate_to_corpus(
        candidate,
        corpus_chunks if corpus_chunks is not None else load_official_corpus_chunks(),
    )
    candidate["review_status"] = _review_status_for_candidate(candidate, record)
    candidate["activation_status"] = ACTIVATION_INACTIVE
    return candidate


def build_grounded_open_response_candidates(
    records: Sequence[Mapping[str, Any]],
    corpus_chunks: Sequence[Mapping[str, Any]] | None = None,
    source_bank_path: str = SOURCE_BANK_PATH,
) -> list[dict[str, Any]]:
    """Build all cleaned and grounded open response candidates in source order."""
    loaded_chunks = corpus_chunks if corpus_chunks is not None else load_official_corpus_chunks()
    return [
        build_grounded_open_response_candidate(record, loaded_chunks, source_bank_path)
        for record in find_open_response_records(records)
    ]


def build_open_response_review_record(
    candidate: Mapping[str, Any],
    source_record: Mapping[str, Any],
) -> dict[str, Any]:
    """Create the canonical human-review record for a normalized candidate."""
    review_status = _review_status_for_candidate(candidate, source_record)
    issues = _review_issues(candidate, source_record)
    source_question_id = str(candidate.get("source_question_id", "")).strip()
    return {
        "review_id": f"open_response_review_{source_question_id}_20260604_001",
        "source_question_id": source_question_id,
        "candidate_id": f"diagnostic_open_response_{source_question_id}",
        "reviewer": "phase_4a_3_7_45_structural_review",
        "reviewed_at": "2026-06-04T00:00:00Z",
        "review_status": review_status,
        "activation_status": ACTIVATION_INACTIVE,
        "checklist": {
            "ra_checked": candidate.get("RA") != UNKNOWN,
            "causal_metadata_checked": _non_empty_string(candidate.get("optional_causal_chain")),
            "corpus_support_checked": _corpus_support_is_approved(candidate),
            "sba_residue_removed": not _candidate_has_sba_residue(candidate),
            "official_scoring_absent": not _has_forbidden_fields(candidate),
            "governance_checked": _mapping(candidate.get("governance_flags")) == GOVERNANCE_FLAGS,
        },
        "issues_found": issues,
        "required_changes": _required_changes(issues),
        "approval_scope": "open_response_internal_review_only",
        "governance_confirmation": copy.deepcopy(GOVERNANCE_FLAGS),
        "notes": _review_notes(review_status),
    }


def build_open_response_review_records(
    source_records: Sequence[Mapping[str, Any]],
    candidates: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    """Create review records aligned by source_question_id."""
    source_by_id = {
        str(record.get("question_id", "")).strip(): record
        for record in find_open_response_records(source_records)
    }
    return [
        build_open_response_review_record(candidate, source_by_id.get(str(candidate.get("source_question_id")), {}))
        for candidate in candidates
    ]


def load_official_corpus_chunks(path: str | Path = OFFICIAL_CHUNKS_PATH) -> list[dict[str, Any]]:
    """Load official chunks available for local deterministic grounding."""
    chunk_path = Path(path)
    if not chunk_path.exists():
        return []
    chunks: list[dict[str, Any]] = []
    for line in chunk_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        chunk = json.loads(line)
        if _chunk_can_ground_open_response(chunk):
            chunks.append(chunk)
    return chunks


def ground_candidate_to_corpus(
    candidate: Mapping[str, Any],
    corpus_chunks: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    """Attach chunk/document support only where deterministic term evidence exists."""
    support_terms = _string_list(candidate.get("expected_concepts"))
    evidence: list[dict[str, Any]] = []
    for chunk in corpus_chunks:
        matched_terms = _matched_grounding_terms(support_terms, chunk)
        if len(matched_terms) < MIN_GROUNDING_TERMS:
            continue
        evidence.append(
            {
                "chunk_id": str(chunk.get("chunk_id", "")).strip(),
                "source_file": str(chunk.get("source_file", "")).strip(),
                "title": str(chunk.get("title", "") or chunk.get("subtopic", "")).strip(),
                "source_type": str(chunk.get("source_type", "")).strip(),
                "matched_terms": matched_terms,
            }
        )

    evidence = sorted(
        evidence,
        key=lambda item: (-len(item["matched_terms"]), item["chunk_id"]),
    )[:MAX_EVIDENCE_CHUNKS]
    return {
        "status": "supported" if evidence else "missing",
        "source_question_bank": SOURCE_BANK_PATH,
        "source_type": str(_mapping(candidate.get("corpus_support")).get("source_type") or UNKNOWN),
        "support_terms": support_terms,
        "evidence_chunks": evidence,
    }


def validate_open_response_candidate(candidate: Any) -> list[str]:
    """Return deterministic validation errors for one open response candidate."""
    if not isinstance(candidate, Mapping):
        return ["candidate must be a dict"]

    errors: list[str] = []
    required = (
        "schema_version",
        "source_question_id",
        "question_type",
        "stem",
        "RA",
        "topic",
        "subtopic",
        "difficulty",
        "expected_concepts",
        "optional_causal_chain",
        "corpus_support",
        "review_status",
        "activation_status",
        "feedback_rubric",
        "governance_flags",
    )
    for field in required:
        if field not in candidate:
            errors.append(f"missing field: {field}")

    if candidate.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"schema_version must be {SCHEMA_VERSION}")
    if candidate.get("question_type") != QUESTION_TYPE:
        errors.append(f"question_type must be {QUESTION_TYPE}")
    for field in ("source_question_id", "stem", "RA", "topic", "subtopic", "difficulty"):
        if not _non_empty_string(candidate.get(field)):
            errors.append(f"{field} must be present and non-empty")
    if not _string_list(candidate.get("expected_concepts")):
        errors.append("expected_concepts must be a non-empty list of strings")

    corpus_support = _mapping(candidate.get("corpus_support"))
    if corpus_support.get("status") not in {"source_metadata_only", "supported", "missing"}:
        errors.append("corpus_support.status must be source_metadata_only, supported, or missing")
    for field in ("source_question_bank", "source_type"):
        if not _non_empty_string(corpus_support.get(field)):
            errors.append(f"corpus_support.{field} must be present and non-empty")
    if not isinstance(corpus_support.get("support_terms"), list):
        errors.append("corpus_support.support_terms must be a list")
    if not isinstance(corpus_support.get("evidence_chunks"), list):
        errors.append("corpus_support.evidence_chunks must be a list")
    if candidate.get("review_status") not in {REVIEW_APPROVED, REVIEW_REQUIRES_REVISION, REVIEW_REJECTED}:
        errors.append("review_status must be approved, requires_revision, or rejected")
    if candidate.get("activation_status") != ACTIVATION_INACTIVE:
        errors.append("activation_status must remain inactive")
    if candidate.get("review_status") == REVIEW_APPROVED:
        if candidate.get("RA") == UNKNOWN:
            errors.append("approved candidates require RA")
        if corpus_support.get("status") != "supported" or not corpus_support.get("evidence_chunks"):
            errors.append("approved candidates require corpus support")
        if _candidate_has_sba_residue(candidate):
            errors.append("approved candidates must not contain SBA residue")

    if _mapping(candidate.get("feedback_rubric")) != FEEDBACK_RUBRIC:
        errors.append("feedback_rubric must match open response formative contract")
    if _mapping(candidate.get("governance_flags")) != GOVERNANCE_FLAGS:
        errors.append("governance_flags must match safe training-only defaults")

    _validate_forbidden_fields(candidate, errors)
    return errors


def evaluate_open_response_answer(candidate: Mapping[str, Any], learner_answer: str) -> dict[str, Any]:
    """Return formative, non-authoritative feedback for a learner response."""
    expected_concepts = _string_list(candidate.get("expected_concepts"))
    answer_text = str(learner_answer or "")
    present: list[str] = []
    partial: list[str] = []
    missing: list[str] = []

    for concept in expected_concepts:
        state = _concept_state(concept, answer_text)
        if state == "present":
            present.append(concept)
        elif state == "partial":
            partial.append(concept)
        else:
            missing.append(concept)

    causal_feedback = _causal_link_feedback(candidate.get("optional_causal_chain"), answer_text)
    unsupported_claims = _detect_unsupported_claims(answer_text)
    needs_review = bool(missing or partial or causal_feedback == "weak_causal_link")

    return {
        "present_concepts": present,
        "missing_concepts": missing,
        "partial_concepts": partial,
        "causal_link_feedback": causal_feedback,
        "unsupported_claims": unsupported_claims,
        "feedback_summary": _feedback_summary(present, missing, partial, causal_feedback),
        "revision_suggestion": _revision_suggestion(missing, partial, causal_feedback),
        "feedback_level": "needs_review" if needs_review else "concepts_present",
        "needs_review": needs_review,
        "governance_disclaimer": (
            "Formative training feedback only; not WSET examiner marking or official evaluation."
        ),
    }


def _normalize_question_type(value: Any) -> str:
    return " ".join(str(value or "").strip().lower().replace("-", "_").replace("_", " ").split())


def _chunk_can_ground_open_response(chunk: Mapping[str, Any]) -> bool:
    if chunk.get("safe_for_examiner") is True:
        return False
    if chunk.get("official_grading_authority") is True:
        return False
    title = _normalize_text(chunk.get("title") or chunk.get("subtopic") or "")
    source_file = _normalize_text(chunk.get("source_file") or "")
    return title != "index" and "repair_report" not in source_file


def _matched_grounding_terms(support_terms: list[str], chunk: Mapping[str, Any]) -> list[str]:
    text = _normalize_text(
        " ".join(
            [
                str(chunk.get("text", "")),
                str(chunk.get("title", "")),
                str(chunk.get("subtopic", "")),
            ]
        )
    )
    matched: list[str] = []
    for term in support_terms:
        variants = _grounding_variants(term)
        if any(_term_in_text(variant, text) for variant in variants):
            normalized_term = " ".join(str(term).split())
            if normalized_term not in matched:
                matched.append(normalized_term)
    return matched


def _grounding_variants(term: str) -> list[str]:
    normalized = _normalize_text(term)
    variants = [normalized]
    for alias in GROUNDING_ALIASES.get(str(term), ()) + GROUNDING_ALIASES.get(normalized, ()):
        alias_norm = _normalize_text(alias)
        if alias_norm and alias_norm not in variants:
            variants.append(alias_norm)
    return [variant for variant in variants if len(variant) > 2]


def _term_in_text(term: str, text: str) -> bool:
    if " " in term:
        return term in text
    return re.search(rf"\b{re.escape(term)}\b", text) is not None


def _review_status_for_candidate(candidate: Mapping[str, Any], source_record: Mapping[str, Any]) -> str:
    issues = _review_issues(candidate, source_record)
    if "structural anomaly: source carries populated SBA answer/options residue" in issues:
        return REVIEW_REJECTED
    return REVIEW_REQUIRES_REVISION if issues else REVIEW_APPROVED


def _review_issues(candidate: Mapping[str, Any], source_record: Mapping[str, Any]) -> list[str]:
    issues: list[str] = []
    if candidate.get("RA") == UNKNOWN:
        issues.append("missing RA metadata")
    if not _non_empty_string(candidate.get("optional_causal_chain")):
        issues.append("missing causal metadata")
    if not _corpus_support_is_approved(candidate):
        issues.append("missing corpus chunk support")
    if _candidate_has_sba_residue(candidate):
        issues.append("normalized candidate still contains SBA residue")
    if _source_has_populated_sba_residue(source_record):
        issues.append("structural anomaly: source carries populated SBA answer/options residue")
    if _has_forbidden_fields(candidate):
        issues.append("official scoring field detected")
    if _mapping(candidate.get("governance_flags")) != GOVERNANCE_FLAGS:
        issues.append("governance flags do not match training-only defaults")
    return issues


def _required_changes(issues: list[str]) -> list[str]:
    changes: list[str] = []
    for issue in issues:
        if issue == "missing RA metadata":
            changes.append("Add verified RA mapping before approval.")
        elif issue == "missing causal metadata":
            changes.append("Add or explicitly waive causal metadata during human review.")
        elif issue == "missing corpus chunk support":
            changes.append("Attach verified corpus chunk support before approval.")
        elif "SBA" in issue:
            changes.append("Remove SBA residue from the normalized open-response layer.")
        elif "scoring" in issue:
            changes.append("Remove official scoring fields.")
        elif "governance" in issue:
            changes.append("Restore governance-safe defaults.")
    return changes


def _review_notes(review_status: str) -> str:
    if review_status == REVIEW_APPROVED:
        return "Approved for internal open-response structural review only; cockpit activation remains off."
    if review_status == REVIEW_REJECTED:
        return "Rejected from the open-response candidate set until the source anomaly is resolved."
    return "Requires revision before any future learner-facing activation."


def _corpus_support_is_approved(candidate: Mapping[str, Any]) -> bool:
    corpus_support = _mapping(candidate.get("corpus_support"))
    return corpus_support.get("status") == "supported" and bool(corpus_support.get("evidence_chunks"))


def _source_has_populated_sba_residue(record: Mapping[str, Any]) -> bool:
    options = _mapping(record.get("options"))
    if any(str(value).strip() for value in options.values()):
        return True
    for field in ("correct_answer_letter", "correct_answer", "correct_answer_text"):
        if str(record.get(field, "")).strip():
            return True
    return False


def _candidate_has_sba_residue(candidate: Mapping[str, Any]) -> bool:
    residue_fields = {
        "options",
        "option_a",
        "option_b",
        "option_c",
        "option_d",
        "correct_answer",
        "correct_answer_letter",
        "correct_answer_text",
        "distractors",
    }
    return any(field in candidate for field in residue_fields)


def _has_forbidden_fields(value: Any) -> bool:
    errors: list[str] = []
    _validate_forbidden_fields(value, errors)
    return bool(errors)


def _expected_concepts(record: Mapping[str, Any]) -> list[str]:
    concepts: list[str] = []
    for value in _string_list(record.get("expected_keywords")) + _string_list(record.get("expected_topics")):
        normalized = " ".join(value.split())
        if normalized and normalized not in concepts:
            concepts.append(normalized)
    return concepts or [UNKNOWN]


def _extract_ra(topics: list[str]) -> str:
    for topic in topics:
        match = re.search(r"\bRA\s*([1-5])\b", topic, flags=re.IGNORECASE)
        if match:
            return "RA" + match.group(1)
    return UNKNOWN


def _extract_topic_subtopic(topics: list[str], ra: str) -> tuple[str, str]:
    non_ra_topics = [topic for topic in topics if not topic.upper().startswith(ra)]
    if non_ra_topics:
        topic = non_ra_topics[0]
        subtopic = non_ra_topics[1] if len(non_ra_topics) > 1 else non_ra_topics[0]
        return topic, subtopic
    return UNKNOWN, UNKNOWN


def _difficulty(value: Any) -> str:
    text = str(value or "").strip().lower()
    return text if text in {"foundational", "intermediate", "advanced", "distinction"} else UNKNOWN


def _concept_state(concept: str, answer_text: str) -> str:
    concept_norm = _normalize_text(concept)
    answer_norm = _normalize_text(answer_text)
    if concept_norm and concept_norm in answer_norm:
        return "present"

    concept_tokens = _meaningful_tokens(concept)
    answer_tokens = set(_meaningful_tokens(answer_text))
    if not concept_tokens:
        return "missing"
    hits = [token for token in concept_tokens if token in answer_tokens]
    if len(hits) == len(concept_tokens):
        return "present"
    if hits:
        return "partial"
    return "missing"


def _causal_link_feedback(optional_causal_chain: Any, answer_text: str) -> str:
    if not _non_empty_string(optional_causal_chain):
        return "not_applicable"

    segments = [
        segment.strip()
        for segment in str(optional_causal_chain).split("->")
        if segment.strip()
    ]
    matched_segments = [
        segment for segment in segments if _concept_state(segment, answer_text) in {"present", "partial"}
    ]
    answer_tokens = set(_meaningful_tokens(answer_text))
    has_connector = bool(answer_tokens & CAUSAL_CONNECTORS)

    if len(matched_segments) >= 2 and has_connector:
        return "causal_link_present"
    if len(matched_segments) >= 2 or (len(matched_segments) == 1 and has_connector):
        return "weak_causal_link"
    return "causal_link_missing"


def _detect_unsupported_claims(answer_text: str) -> list[str]:
    tokens = set(_meaningful_tokens(answer_text))
    return [term for term in UNSUPPORTED_CLAIM_TERMS if _normalize_text(term) in tokens]


def _feedback_summary(
    present: list[str],
    missing: list[str],
    partial: list[str],
    causal_feedback: str,
) -> str:
    if not missing and not partial and causal_feedback in {"not_applicable", "causal_link_present"}:
        return "Key expected concepts are present in this formative check."
    parts = []
    if missing:
        parts.append("Some expected concepts are missing.")
    if partial:
        parts.append("Some concepts are only partially expressed.")
    if causal_feedback == "weak_causal_link":
        parts.append("The causal link needs clearer wording.")
    elif causal_feedback == "causal_link_missing":
        parts.append("The expected causal link is not yet visible.")
    return " ".join(parts)


def _revision_suggestion(missing: list[str], partial: list[str], causal_feedback: str) -> str:
    targets = missing[:3] + partial[:2]
    if targets:
        return "Revise by explicitly addressing: " + ", ".join(targets) + "."
    if causal_feedback == "weak_causal_link":
        return "Revise by connecting cause and effect with explicit causal language."
    if causal_feedback == "causal_link_missing":
        return "Revise by adding the relevant cause-effect relationship."
    return "Use the same structure and keep the explanation source-grounded."


def _meaningful_tokens(text: Any) -> list[str]:
    return [
        _normalize_text(token)
        for token in tokenize_term(str(text or ""))
        if _normalize_text(token) and _normalize_text(token) not in STOPWORDS
    ]


def _normalize_text(text: Any) -> str:
    decomposed = unicodedata.normalize("NFD", str(text or "").lower())
    stripped = "".join(char for char in decomposed if unicodedata.category(char) != "Mn")
    return " ".join(stripped.replace("₂", "2").split())


def _validate_forbidden_fields(value: Any, errors: list[str], path: str = "$") -> None:
    if isinstance(value, Mapping):
        for key in sorted(value.keys(), key=str):
            lowered = str(key).lower()
            if (
                lowered not in ALLOWED_GOVERNANCE_FIELD_NAMES
                and any(part in lowered for part in FORBIDDEN_FIELD_PARTS)
            ):
                errors.append(f"forbidden field detected at {path}: {key}")
            _validate_forbidden_fields(value[key], errors, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _validate_forbidden_fields(child, errors, f"{path}[{index}]")


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item).strip() for item in value if str(item).strip()]


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())
