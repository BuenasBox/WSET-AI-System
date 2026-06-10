# ADAPTIVE_SESSION_MIGRATION_REPORT.md

## Phase X.2 — Objective 3: Adaptive Session Expansion

**Date:** 2026-06-09  
**Status:** COMPLETE

---

## Summary

The adaptive session pool has been expanded from 36 items (public_lab collection) to 116 items (all approved SBA items across `approved_for_static_demo` and `approved_private_sba` review states).

---

## Before → After

| Dimension | Before | After |
|-----------|--------|-------|
| Pool size | 36 | 116 |
| Pool source | `public_lab` collection | `approved_for_static_demo` + `approved_private_sba` review states |
| Session size | 10 | 10 (unchanged) |
| RA stratification | RA1-heavy | Proportional: RA1×4, RA2×3, RA3×1, RA4×1, RA5×1 |
| master_bank.json modified | N/A | NO — importer contract unchanged |
| master_bank collections | `public_lab: 36` (canonical) | Unchanged |

---

## Implementation Approach

The expansion does NOT modify `master_bank.json` collections. The importer contract (`build_master_bank(ROOT)`) still enforces `public_lab: 36`. Instead, session composition filters by `review_state` directly:

```python
ELIGIBLE_REVIEW_STATES = {'approved_for_static_demo', 'approved_private_sba'}
candidates = [
    item for item in bank['items']
    if item.get('status', {}).get('review_state') in ELIGIBLE_REVIEW_STATES
    and item.get('question_type') == 'single_best_answer'
    and len(filled_options) >= 3
]
# → 116 SBA candidates
```

RA distribution of 116-item pool: RA1=47, RA2=39, RA3=14, RA4=8, RA5=8.

Session selected: 10 questions via deterministic SHA-sorted per-RA buckets, proportionally stratified.

---

## Selected Questions (EXPRESS_10)

| question_id | RA | review_state | stem (truncated) |
|-------------|-----|--------------|-----------------|
| wset3_493 | RA1 | approved_for_static_demo | ¿Cuál es el principal riesgo de una vendimia muy tardía? |
| wset3_81 | RA1 | approved_private_sba | ¿Cuál es una consecuencia probable de almacenar vino a temperatura... |
| wset3_349 | RA1 | approved_private_sba | ¿Qué efecto tiene la vendimia nocturna en zonas cálidas? |
| wset3_496 | RA1 | approved_private_sba | ¿Qué efecto tiene una vendimia anticipada sobre el vino? |
| wset3_269 | RA2 | approved_for_static_demo | ¿Qué región portuguesa es famosa por vinos blancos frescos y... |
| wset3_341 | RA2 | approved_private_sba | ¿Qué factor natural explica la alta acidez en los vinos de Minho? |
| wset3_277 | RA2 | approved_for_static_demo | ¿Qué variedad se cultiva en Oregon con prestigio similar al... |
| wset3_23 | RA3 | approved_private_sba | ¿Cuál es el efecto de una presión menor a 3 atmósferas en un vino? |
| wset3_105 | RA4 | approved_for_static_demo | ¿Qué estilo de Jerez representa mejor la complejidad oxidativa? |
| wset3_827 | RA5 | approved_private_sba | ¿Por qué es obligatorio declarar 'contiene sulfitos' en la etiqueta? |

---

## Output File

`frontend/session_data/session_payload.json`
- `session_mode: EXPRESS_10`
- `pool_size: 116`
- `pool_source: master_bank_approved_private_sba+approved_for_static_demo`
- `governance.safe_for_examiner: false`
- `governance.examiner_scoring_allowed: false`

---

## Governance

All governance invariants unchanged. No LLM/API/embeddings calls. No external services. `safe_for_examiner` and `examiner_scoring_allowed` remain `false`. Output is deterministic given fixed master_bank.json.

---

## Test Impact

`tests/test_master_bank.py` — 15/15 OK (importer contract unchanged, public_lab still 36).

---

*Phase X.2 Objective 3: COMPLETE*
