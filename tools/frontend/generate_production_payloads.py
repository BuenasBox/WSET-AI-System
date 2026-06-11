"""
generate_production_payloads.py — Production frontend data generator.

Produces three JS data files for the epistemiclab-dashboard static site:
  1. frontend/diagnostic-sba/preguntas_data.js        (523 SBA items, full eligible bank)
  2. frontend/open-response-lab/lab_payload.js         (26 OR items, 4 modes)
  3. frontend/adaptive-session/session_bank.js         (523 SBA + SAT prompts)

Bank filter (Phase Y.0):
  Uses the eligibility engine (master_bank_eligibility.classify_master_item) as the
  authority for SBA pool membership, replacing the stale review_state filter.
  The eligibility engine applies the full resolution layer (Phase 4A.3.8.5.7) and
  suitability classification, yielding 589 private_practice-eligible SBA items.
  A structural completeness gate (stem + 4 non-empty options + correct_answer_letter)
  further reduces this to 523 deployable items.

Usage:
  python tools/frontend/generate_production_payloads.py

Governance:
  safe_for_examiner=False, examiner_scoring_allowed=False
  No LLM, no API, no embeddings, no cloud calls.
"""
import json
import random
import sys
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).parent.parent.parent
MASTER_BANK = REPO / "knowledge" / "question-bank" / "master_bank" / "master_bank.json"
OR_BANK = REPO / "knowledge" / "question-bank" / "open_response" / "open_response_bank.json"
RESPONSE_STRUCTURES = REPO / "knowledge" / "distinction-patterns" / "response_structures.json"
SBA_OUT = REPO / "frontend" / "diagnostic-sba" / "preguntas_data.js"
OR_OUT = REPO / "frontend" / "open-response-lab" / "lab_payload.js"
ADAPTIVE_OUT = REPO / "frontend" / "adaptive-session" / "session_bank.js"

GOVERNANCE = {
    "safe_for_examiner": False,
    "examiner_scoring_allowed": False,
    "training_item_only": True,
    "official_wset_question": False,
    "disclaimer": "PROTOTIPO · ENTRENAMIENTO · NO EVALUACIÓN OFICIAL WSET",
}

# Official Mock Theory Part 1 RA distribution
MOCK_THEORY_RA_DIST = {"RA1": 8, "RA2": 28, "RA3": 5, "RA4": 5, "RA5": 4}

# SAT wine prompts (formative practice, not official exam wines)
SAT_WINE_PROMPTS = [
    {
        "prompt_id": "SAT_P01",
        "wine_name": "Vino blanco complejo con crianza en roble",
        "description": (
            "Vino blanco de color amarillo limón pálido. En nariz: intensidad media(+), "
            "aromas primarios de limón, melocotón y melón, aromas secundarios de vainilla "
            "y galleta, aromas terciarios de miel. En evolución. "
            "En boca: seco, acidez media(+), alcohol medio, cuerpo medio(+), "
            "intensidad media(+), final medio(+)."
        ),
        "wine_type": "white",
        "is_simple": False,
        "expected_quality": "muy bueno",
        "expected_readiness": "se puede beber ahora, pero tiene potencial para el envejecimiento",
        "training_note": "Practica identificar aromas secundarios (roble) y terciarios (crianza en botella).",
    },
    {
        "prompt_id": "SAT_P02",
        "wine_name": "Vino tinto de alta calidad con complejidad terciaria",
        "description": (
            "Vino tinto de color rubí granate. En nariz: intensidad pronunciada, "
            "aromas primarios de cereza roja, frambuesa, grosella, violeta; "
            "aromas secundarios de vainilla, cedro, clavo; "
            "aromas terciarios de tierra, cuero, fruta seca. En evolución. "
            "En boca: seco, acidez alta, tanino medio, alcohol alto, "
            "cuerpo medio(+), intensidad pronunciada, final largo."
        ),
        "wine_type": "red",
        "is_simple": False,
        "expected_quality": "excelente",
        "expected_readiness": "se puede beber ahora, pero tiene potencial para el envejecimiento",
        "training_note": "Practica distinguir aromas secundarios de terciarios en vinos con crianza.",
    },
    {
        "prompt_id": "SAT_P03",
        "wine_name": "Vino blanco simple y fresco",
        "description": (
            "Vino blanco de color amarillo pálido. En nariz: intensidad media(-), "
            "simple, aromas primarios de pera, manzana verde, melocotón blanco. Joven. "
            "En boca: seco, acidez media, alcohol bajo, cuerpo ligero, "
            "intensidad media(-), final corto."
        ),
        "wine_type": "white",
        "is_simple": True,
        "expected_quality": "aceptable",
        "expected_readiness": "beber ahora: no adecuado para el envejecimiento o para un mayor envejecimiento",
        "training_note": "Practica reconocer y declarar 'simple' en los vinos sin complejidad secundaria/terciaria.",
    },
    {
        "prompt_id": "SAT_P04",
        "wine_name": "Vino dulce envejecido de alta calidad",
        "description": (
            "Vino blanco de color oro profundo. En nariz: intensidad pronunciada, "
            "en evolución, aromas primarios de flor de saúco, melocotón, albaricoque, piña, mango; "
            "frutas cocidas, pasas; aromas secundarios de vainilla, clavo, cedro; "
            "aromas terciarios de miel, almendra, mermelada, albaricoque seco. "
            "En boca: dulce, acidez alta, alcohol medio(+), cuerpo pleno, "
            "intensidad pronunciada, final largo."
        ),
        "wine_type": "sweet",
        "is_simple": False,
        "expected_quality": "excelente",
        "expected_readiness": "se puede beber ahora, pero tiene potencial para el envejecimiento",
        "training_note": "Clave: la acidez alta en un vino dulce es una señal estructural fundamental.",
    },
    {
        "prompt_id": "SAT_P05",
        "wine_name": "Vino tinto simple y frutado",
        "description": (
            "Vino tinto de color rubí de intensidad media. En nariz: intensidad media, "
            "simple, aromas primarios de fresa, cereza, ciruela roja. Joven. "
            "En boca: seco, acidez media, tanino bajo, alcohol medio, "
            "cuerpo medio(-), intensidad media(-), final corto."
        ),
        "wine_type": "red",
        "is_simple": True,
        "expected_quality": "aceptable",
        "expected_readiness": "beber ahora: no adecuado para el envejecimiento o para un mayor envejecimiento",
        "training_note": "Practica describir un vino tinto simple con estructura mínima.",
    },
    {
        "prompt_id": "SAT_P06",
        "wine_name": "Vino blanco complejo sin crianza en roble",
        "description": (
            "Vino blanco de color amarillo verdoso pálido. En nariz: intensidad pronunciada, "
            "aromas primarios de pomelo, lima, hierba recién cortada, manzana verde; "
            "aromas secundarios de levadura, pan tostado (de lías); "
            "sin terciarios. Joven. "
            "En boca: seco, acidez alta, alcohol medio, cuerpo medio, "
            "intensidad pronunciada, final largo."
        ),
        "wine_type": "white",
        "is_simple": False,
        "expected_quality": "muy bueno",
        "expected_readiness": "beber ahora: no adecuado para el envejecimiento o para un mayor envejecimiento",
        "training_note": "Practica identificar crianza sobre lías (aromas secundarios) sin madera.",
    },
]


def load_master_bank():
    data = json.loads(MASTER_BANK.read_text(encoding="utf-8"))
    return data["items"]


def load_or_bank():
    data = json.loads(OR_BANK.read_text(encoding="utf-8"))
    return data["items"]


def _is_structurally_complete_sba(item):
    """Return True only if item has stem, 4 non-empty options, and a valid answer letter."""
    stem = item.get("stem", "").strip()
    sc = item.get("source_content", {})
    opts = sc.get("options", {})
    has_4_opts = all(opts.get(k, "").strip() for k in ("A", "B", "C", "D"))
    has_answer = sc.get("correct_answer_letter", "").strip() in ("A", "B", "C", "D")
    return bool(stem) and has_4_opts and has_answer


def sba_eligible(items):
    """Return all SBA items eligible for production training use.

    Uses the master_bank eligibility engine (Phase 4A.3.8.5.7 resolution layer +
    suitability classification) as the authority.  A structural completeness gate
    further ensures every emitted item has stem, 4 non-empty options, and a valid
    correct_answer_letter.  Governance flags are verified clean (safe_for_examiner
    and examiner_scoring_allowed must be False).
    """
    try:
        import sys as _sys
        _sys.path.insert(0, str(REPO))
        from tools.question_generation.master_bank_eligibility import (
            classify_master_item,
            load_open_response_suitability_index,
        )
        suitability_index = load_open_response_suitability_index()
        use_engine = True
    except Exception as _e:
        print(f"  WARNING: eligibility engine unavailable ({_e}); falling back to review_state filter", file=sys.stderr)
        use_engine = False

    result = []
    for i in items:
        if i.get("question_type") != "single_best_answer":
            continue
        # Governance hard-gate — never True
        gov = i.get("governance", {})
        if gov.get("safe_for_examiner") or gov.get("examiner_scoring_allowed"):
            continue
        # Eligibility check
        if use_engine:
            suit = suitability_index.get(i.get("master_item_id", ""))
            classification = classify_master_item(i, suit)
            if "private_practice" not in classification.get("categories", []):
                continue
        else:
            # Fallback: stale review_state filter
            if not (
                i["status"].get("gold")
                or i["status"].get("review_state") in (
                    "approved_private_sba",
                    "approved_for_static_demo",
                )
            ):
                continue
        # Structural completeness gate
        if not _is_structurally_complete_sba(i):
            continue
        result.append(i)
    return result


def or_eligible(items):
    """Return all open-response items eligible for training use."""
    return [
        i for i in items
        if i["question_type"] == "open_response"
        and i["status"].get("review_state") == "approved_open_response"
    ]


def master_to_sba_item(item):
    """Convert master_bank SBA item to frontend format."""
    c = item.get("curriculum", {})
    sc = item.get("source_content", {})
    opts_dict = sc.get("options", {})
    # Build options list in A/B/C/D order
    opts_list = [opts_dict.get(k, "") for k in ("A", "B", "C", "D") if opts_dict.get(k)]
    correct_letter = sc.get("correct_answer_letter", "A")
    correct_idx = ord(correct_letter) - ord("A") if correct_letter else 0
    correct_idx = min(correct_idx, len(opts_list) - 1)

    return {
        "id": item.get("master_item_id", ""),
        "source_question_id": str(item.get("source_question_id", "")),
        "topic": c.get("topic", ""),
        "ra": c.get("ra", ""),
        "difficulty": c.get("difficulty", "intermediate"),
        "text": item.get("stem", ""),
        "options": opts_list,
        "correct_index": correct_idx,
        "correct_letter": correct_letter,
        "keywords": c.get("expected_keywords", []),
        "gold": item["status"].get("gold", False),
        "governance": GOVERNANCE,
    }


def master_to_or_item(item):
    """Convert master_bank OR item to frontend format."""
    c = item.get("curriculum", {})
    return {
        "id": item.get("master_item_id", ""),
        "source_question_id": str(item.get("source_question_id", "")),
        "topic": c.get("topic", ""),
        "ra": c.get("ra", ""),
        "difficulty": c.get("difficulty", "intermediate"),
        "text": item.get("stem", ""),
        "expected_keywords": c.get("expected_keywords", []),
        "expected_topics": c.get("expected_topics", []),
        "governance": GOVERNANCE,
    }


def select_mock_theory_50(sba_items):
    """Select 50 items respecting official RA distribution."""
    by_ra = {}
    for item in sba_items:
        ra = item["ra"]
        by_ra.setdefault(ra, []).append(item)

    selected = []
    for ra, count in MOCK_THEORY_RA_DIST.items():
        pool = by_ra.get(ra, [])
        random.shuffle(pool)
        picked = pool[:count]
        if len(picked) < count:
            print(f"  WARNING: {ra} needs {count} but only {len(picked)} available", file=sys.stderr)
        selected.extend(picked)

    return selected


def avoid_recent(items, recent_ids, max_avoid=25):
    """Prioritize items not in recent_ids."""
    recent_set = set(str(x) for x in (recent_ids or []))
    fresh = [i for i in items if str(i.get("source_question_id", "")) not in recent_set]
    stale = [i for i in items if str(i.get("source_question_id", "")) in recent_set]
    return fresh + stale


# ---------------------------------------------------------------------------
# Generator: Diagnostic SBA preguntas_data.js
# ---------------------------------------------------------------------------

def generate_sba_data():
    items = load_master_bank()
    eligible = sba_eligible(items)
    frontend_items = [master_to_sba_item(i) for i in eligible]

    # Sort for stability: gold first, then by ra, then by source_question_id
    frontend_items.sort(
        key=lambda x: (
            0 if x["gold"] else 1,
            x["ra"],
            int(x["source_question_id"]) if x["source_question_id"].isdigit() else 9999,
        )
    )

    # RA distribution check
    from collections import Counter
    ra_dist = Counter(i["ra"] for i in frontend_items)

    payload = {
        "schema_version": "sba_bank_v1",
        "generated_at": datetime.now().isoformat(),
        "total_items": len(frontend_items),
        "ra_distribution": dict(sorted(ra_dist.items())),
        "mock_theory_feasible": all(
            ra_dist.get(ra, 0) >= n for ra, n in MOCK_THEORY_RA_DIST.items()
        ),
        "modes": {
            "quick_drill": {"size": 5, "label": "Quick Drill · 5"},
            "express": {"size": 10, "label": "Express · 10"},
            "standard": {"size": 25, "label": "Estándar · 25"},
            "mock_theory_1": {
                "size": 50,
                "label": "Mock Theory · 50",
                "ra_distribution": MOCK_THEORY_RA_DIST,
            },
        },
        "governance": GOVERNANCE,
        "items": frontend_items,
    }

    js = f"window.PREGUNTAS_BANK = {json.dumps(payload, ensure_ascii=False, indent=2)};\n"
    SBA_OUT.write_text(js, encoding="utf-8")
    print(f"  SBA data: {len(frontend_items)} items → {SBA_OUT.name}")
    return frontend_items


# ---------------------------------------------------------------------------
# Generator: Open Response lab_payload.js
# ---------------------------------------------------------------------------

def generate_or_payload():
    """Delegate to the authoritative ORL generator (Phase Z.2 reconciliation).

    The Open Response Lab payload contract (session keys short_practice /
    standard_practice / extended_practice / mock_theory_2 with sizes 1/2/4/4,
    plus evaluation_by_item_id) is owned by
    tools/question_generation/open_response_lab_runtime.py. This module used to
    emit a parallel, incompatible schema (short/standard/long, no evaluation
    data) — that drift broke production ORL on 2026-06-10 (see
    docs/FRONTEND_STABILIZATION_AUDIT.md, Issues #9-#11). Never reintroduce a
    second lab_payload.js writer here.
    """
    from tools.question_generation.open_response_lab_runtime import write_lab_payload_js

    target = write_lab_payload_js(path=OR_OUT)
    print(f"  OR data: delegated to open_response_lab_runtime → {target.name}")
    return target


# ---------------------------------------------------------------------------
# Generator: Adaptive Session session_bank.js
# ---------------------------------------------------------------------------

def generate_adaptive_bank(sba_items):
    payload = {
        "schema_version": "session_bank_v1",
        "generated_at": datetime.now().isoformat(),
        "total_sba": len(sba_items),
        "total_sat_prompts": len(SAT_WINE_PROMPTS),
        "modes": {
            "express_10": {"type": "sba", "size": 10, "label": "Express · 10"},
            "standard_25": {"type": "sba", "size": 25, "label": "Estándar · 25"},
            "mock_theory_50": {
                "type": "sba",
                "size": 50,
                "label": "Mock Theory Part 1 · 50",
                "ra_distribution": MOCK_THEORY_RA_DIST,
            },
            "sat_sprint": {"type": "sat", "wines": 1, "label": "SAT Sprint · 1 vino"},
            "sat_practice": {"type": "sat", "wines": 2, "label": "SAT Practice · 2 vinos"},
            "sat_mock": {
                "type": "sat",
                "wines": 2,
                "duration_minutes": 30,
                "label": "SAT Mock Exam · 2 vinos · 30 min",
            },
        },
        "governance": GOVERNANCE,
        "sba_items": sba_items,
        "sat_prompts": SAT_WINE_PROMPTS,
        "ra_distribution": {
            ra: sum(1 for i in sba_items if i["ra"] == ra)
            for ra in ("RA1", "RA2", "RA3", "RA4", "RA5")
        },
    }

    js = f"window.SESSION_BANK = {json.dumps(payload, ensure_ascii=False, indent=2)};\n"
    ADAPTIVE_OUT.write_text(js, encoding="utf-8")
    print(f"  Adaptive bank: {len(sba_items)} SBA + {len(SAT_WINE_PROMPTS)} SAT → {ADAPTIVE_OUT.name}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("Generating production payloads...")
    print(f"  Source: {MASTER_BANK.name}")

    # Seed for reproducible default sessions
    random.seed(42)

    sba_items = generate_sba_data()
    generate_or_payload()
    generate_adaptive_bank(sba_items)

    print("Done.")


if __name__ == "__main__":
    main()
