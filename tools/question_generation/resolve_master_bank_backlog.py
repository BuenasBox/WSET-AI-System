"""Build the traceable recovery-first resolution artifact for 92 bank items."""

from __future__ import annotations

import argparse
import copy
import json
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from tools.constants import PROJECT_ROOT
from tools.question_generation.master_bank import SAFE_GOVERNANCE
from tools.question_generation.master_bank_resolution import RESOLUTION_PATH


REVIEW_IDS = tuple(
    "7 19 23 24 29 33 43 56 59 60 62 75 81 85 102 116 128 218 225 267 "
    "284 296 316 318 335 337 341 346 349 356 362 364 365 368 372 384 "
    "388 390 394 421 426 435 451 454 459 464 473 479 480 490 491 496 "
    "500 509 511 670 712 713 724 727 731 746 785 826 827 842 846 847"
    .split()
)
INACTIVE_TO_SBA_IDS = tuple(
    "1 4 5 12 13 15 17 20 30 44 50 78 87 108 247 253 386 510".split()
)
INACTIVE_TO_OPEN_IDS = ("18", "853", "854", "855", "856", "857")

DRAFT_PATHS = (
    Path("knowledge/question-bank/diagnostic_sba/drafts/first_5_enrichment_drafts.json"),
    Path("knowledge/question-bank/diagnostic_sba/drafts/gold_bank_activation_drafts.json"),
)
STRUCTURED_PATH = Path("knowledge/question-bank/structured/wset3_questions.json")
REVIEW_PACKET_PATH = Path(
    "knowledge/question-bank/review_packets/master_bank_eligibility_review_packet.json"
)

OPEN_OVERRIDES: dict[str, dict[str, Any]] = {
    "18": {
        "question_type": "short_answer",
        "expected_topics": ["RA1", "winemaking", "sulphur_dioxide_management"],
        "expected_keywords": [
            "sulfitos",
            "SO2",
            "inhibición de levaduras salvajes",
            "protección antimicrobiana",
        ],
        "expected_causal_links": [
            "dosis de SO2 -> inhibición microbiana -> menor actividad de levaduras salvajes"
        ],
    },
    "853": {
        "question_text": (
            "Explique qué indica la añada (vintage) en una etiqueta de vino y "
            "por qué no corresponde al año de embotellado."
        ),
        "question_type": "short_answer",
        "expected_topics": ["RA5", "wine_law_and_labelling", "vintage_labelling"],
        "expected_keywords": ["añada", "año", "uva", "cosechada", "vinificada"],
        "expected_causal_links": [
            "añada declarada -> año de cosecha de la uva -> no año de embotellado"
        ],
    },
    "854": {
        "question_text": (
            "Explique por qué los vinos DOP están sujetos a regulaciones más "
            "estrictas que los vinos IGP."
        ),
        "question_type": "short_answer",
        "expected_topics": ["RA5", "wine_law_and_labelling", "dop_igp_hierarchy"],
        "expected_keywords": ["DOP", "IGP", "origen", "producción", "regulaciones"],
        "expected_causal_links": [
            "vínculo más estrecho con el origen -> normas de producción más restrictivas"
        ],
    },
    "855": {
        "question_text": (
            "Explique los requisitos mínimos de crianza asociados al término "
            "Reserva en un vino tinto español."
        ),
        "question_type": "short_answer",
        "expected_topics": ["RA5", "wine_law_and_labelling", "spanish_reserva_ageing"],
        "expected_keywords": ["Reserva", "tres años", "doce meses", "barrica", "botella"],
        "expected_causal_links": [
            "Reserva tinto -> mínimo tres años totales -> al menos doce meses en barrica"
        ],
    },
    "856": {
        "question_text": (
            "Compare Kabinett y Trockenbeerenauslese dentro del sistema "
            "Prädikat alemán en términos de madurez y concentración."
        ),
        "question_type": "short_answer",
        "expected_topics": ["RA5", "wine_law_and_labelling", "german_pradikat"],
        "expected_keywords": [
            "Kabinett",
            "Trockenbeerenauslese",
            "ligero",
            "concentrado",
            "dulce",
        ],
        "expected_causal_links": [
            "mayor madurez de la uva -> mayor concentración -> categoría Prädikat superior"
        ],
    },
    "857": {
        "question_text": (
            "Compare los canales on-trade y off-trade e indique dónde se "
            "consume el vino en cada caso."
        ),
        "question_type": "short_answer",
        "expected_topics": ["RA5", "wine_business", "distribution_channels"],
        "expected_keywords": [
            "on-trade",
            "off-trade",
            "restaurantes",
            "bares",
            "supermercados",
            "vinotecas",
        ],
        "expected_causal_links": [
            "on-trade -> consumo en el punto de venta; off-trade -> consumo posterior"
        ],
    },
}

OPEN_SUPPORT: dict[str, dict[str, Any]] = {
    "18": {
        "chunk_id": "CC_SULPHITES_PRESERVATION",
        "source_file": "knowledge/knowledge-map/causal-chains/CC_SULPHITES_PRESERVATION.json",
        "title": "Sulphites preservation causal chain",
        "source_type": "knowledge_map",
        "matched_terms": ["sulfitos", "SO2", "levaduras salvajes"],
    },
    "853": {
        "chunk_id": "structured_question_828",
        "source_file": STRUCTURED_PATH.as_posix(),
        "title": "Existing SBA support for vintage labelling",
        "source_type": "structured_question_bank",
        "matched_terms": ["añada", "año", "cosecha"],
    },
    "854": {
        "chunk_id": "structured_question_822",
        "source_file": STRUCTURED_PATH.as_posix(),
        "title": "Existing SBA support for DOP and IGP",
        "source_type": "structured_question_bank",
        "matched_terms": ["DOP", "IGP", "regulaciones"],
    },
    "855": {
        "chunk_id": "structured_question_832",
        "source_file": STRUCTURED_PATH.as_posix(),
        "title": "Existing SBA support for Spanish Reserva",
        "source_type": "structured_question_bank",
        "matched_terms": ["Reserva", "tres años", "barrica"],
    },
    "856": {
        "chunk_id": "official_wset_germany_kabinett",
        "source_file": (
            "knowledge/official-wset/study-guide/wset_markdown/"
            "seccion_6_section_3_still_wines_of_the_world/6-11_22_germany.md"
        ),
        "title": "Germany Prädikat levels",
        "source_type": "official_wset_markdown",
        "matched_terms": ["Kabinett", "Trockenbeerenauslese", "concentrated"],
    },
    "857": {
        "chunk_id": "structured_question_842",
        "source_file": STRUCTURED_PATH.as_posix(),
        "title": "Existing SBA support for distribution channels",
        "source_type": "structured_question_bank",
        "matched_terms": ["on-trade", "off-trade", "restaurantes"],
    },
}


def build_resolution_artifact(root: str | Path = PROJECT_ROOT) -> dict[str, Any]:
    root_path = Path(root)
    packet = _load_mapping(root_path / REVIEW_PACKET_PATH)
    packet_items = {
        str(item.get("question_id")): item
        for section in ("review_pool_items", "inactive_items")
        for item in packet.get(section, [])
        if isinstance(item, Mapping)
    }
    drafts = {}
    for path in DRAFT_PATHS:
        for draft in _load_list(root_path / path):
            source_id = str(_mapping(draft.get("identity")).get("source_question_id", ""))
            drafts[source_id] = draft

    records: list[dict[str, Any]] = []
    for source_id in REVIEW_IDS:
        records.append(
            _record(
                source_id,
                "open_response_review_pool",
                "sba_operational",
                packet_items.get(source_id),
                resolution_reason=(
                    "Valid four-option SBA with a traceable answer. Open-response "
                    "signals are insufficient because the existing metadata does "
                    "not define a supported free-response answer boundary."
                ),
                repairs=["finalized eligibility as private SBA"],
            )
        )
    for source_id in INACTIVE_TO_SBA_IDS:
        draft = drafts.get(source_id, {})
        curriculum = _mapping(draft.get("curriculum"))
        overrides = {
            "expected_topics": [
                str(curriculum.get("ra_id", "")).strip(),
                str(curriculum.get("topic", "")).strip(),
                str(curriculum.get("subtopic", "")).strip(),
            ],
            "difficulty": str(curriculum.get("difficulty", "")).strip(),
        }
        records.append(
            _record(
                source_id,
                "inactive",
                "sba_operational",
                packet_items.get(source_id),
                resolution_reason=(
                    "The existing structured SBA is valid and an internal enrichment "
                    "draft supplies reviewed curriculum metadata. Prior inactivity "
                    "was an activation/review state, not unrecoverable corruption."
                ),
                repairs=[
                    "restored private SBA eligibility",
                    "applied existing draft curriculum metadata",
                ],
                source_overrides=overrides,
                evidence_paths=[
                    next(
                        path.as_posix()
                        for path in DRAFT_PATHS
                        if any(
                            str(_mapping(item.get("identity")).get("source_question_id", ""))
                            == source_id
                            for item in _load_list(root_path / path)
                        )
                    )
                ],
            )
        )
    for source_id in INACTIVE_TO_OPEN_IDS:
        overrides = copy.deepcopy(OPEN_OVERRIDES[source_id])
        overrides.update(
            {
                "options": {},
                "correct_answer_letter": None,
                "correct_answer": None,
                "correct_answer_text": None,
            }
        )
        records.append(
            _record(
                source_id,
                "inactive",
                "open_response_candidate",
                packet_items.get(source_id),
                resolution_reason=(
                    "The repository contains a traceable explanatory answer boundary. "
                    "The item is more safely recovered as open response than rebuilt "
                    "as a four-option SBA."
                ),
                repairs=[
                    "converted source view to short_answer",
                    "removed SBA/True-False residue from normalized candidate",
                    "added existing repository support and curriculum metadata",
                ],
                source_overrides=overrides,
                evidence_paths=[
                    STRUCTURED_PATH.as_posix(),
                    OPEN_SUPPORT[source_id]["source_file"],
                ],
                corpus_support={
                    "status": "supported",
                    "source_question_bank": STRUCTURED_PATH.as_posix(),
                    "source_type": "repository_resolution_evidence",
                    "support_terms": overrides["expected_keywords"],
                    "evidence_chunks": [copy.deepcopy(OPEN_SUPPORT[source_id])],
                },
            )
        )

    records.sort(key=lambda item: int(item["source_question_id"]))
    return {
        "schema_version": "master_bank_review_inactive_resolution_v1",
        "phase": "4A.3.8.5.7",
        "strategy": "recovery_first",
        "source_review_packet": REVIEW_PACKET_PATH.as_posix(),
        "record_count": len(records),
        "initial_counts": {"review": 68, "inactive": 24},
        "transitions": {
            "review_to_sba": 68,
            "review_to_open_response": 0,
            "review_to_quarantine": 0,
            "inactive_to_sba": 18,
            "inactive_to_open_response": 6,
            "inactive_to_quarantine": 0,
        },
        "final_backlog": {"review": 0, "inactive": 0, "quarantine": 0},
        "records": records,
        "governance": copy.deepcopy(SAFE_GOVERNANCE),
    }


def write_resolution_artifact(
    payload: Mapping[str, Any],
    root: str | Path = PROJECT_ROOT,
) -> Path:
    output = Path(root) / RESOLUTION_PATH
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return output


def _record(
    source_id: str,
    source_pool: str,
    destination: str,
    packet_item: Any,
    *,
    resolution_reason: str,
    repairs: list[str],
    source_overrides: Mapping[str, Any] | None = None,
    evidence_paths: list[str] | None = None,
    corpus_support: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    packet = _mapping(packet_item)
    evidence = [
        STRUCTURED_PATH.as_posix(),
        REVIEW_PACKET_PATH.as_posix(),
    ]
    for path in evidence_paths or []:
        if path not in evidence:
            evidence.append(path)
    record = {
        "resolution_id": f"phase_4a_3_8_5_7_{source_id}",
        "source_question_id": source_id,
        "source_pool": source_pool,
        "destination": destination,
        "resolution_reason": resolution_reason,
        "repairs": repairs,
        "evidence_reviewed": evidence,
        "prior_review_reason": packet.get("reason_for_inactive_or_review"),
        "prior_recommendation": packet.get("recommendation_placeholder"),
        "source_overrides": copy.deepcopy(dict(source_overrides or {})),
        "quarantine_analysis": {
            "required": destination == "quarantine",
            "why_sba_not_possible": None,
            "why_open_response_not_possible": None,
        },
    }
    if corpus_support is not None:
        record["corpus_support"] = copy.deepcopy(dict(corpus_support))
    return record


def _load_list(path: Path) -> list[dict[str, Any]]:
    value = json.loads(path.read_text(encoding="utf-8"))
    return [dict(item) for item in value if isinstance(item, Mapping)]


def _load_mapping(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    return dict(value) if isinstance(value, Mapping) else {}


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _cli() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    payload = build_resolution_artifact()
    if payload["record_count"] != 92:
        raise SystemExit("resolution artifact must contain exactly 92 records")
    if args.check:
        print(json.dumps(payload["transitions"], indent=2))
    else:
        print(write_resolution_artifact(payload).as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(_cli())
