# Master Bank Runtime Usage Report
**Phase:** V4.3 Part 2  
**Date:** 2026-06-09

---

## Reachability

**5.8% of the bank is reachable by a learner today** (36 of 616 items, all in `public_lab`).

The remaining 94.2% (580 items) are inactive and unreachable through any current interface.

---

## Modules That Consume `master_bank.json`

### Core API / Data Layer
| Module | Role |
|--------|------|
| `tools/question_generation/master_bank.py` | Primary loader: `MASTER_BANK_PATH`, `build_master_bank()`, `validate_master_bank()`, `write_master_bank()`, `SAFE_GOVERNANCE` |
| `tools/question_generation/master_bank_eligibility.py` | Builds eligibility index from bank items |
| `tools/question_generation/master_bank_resolution.py` | Reads resolution artifact from `master_bank_review_inactive_resolution.json` |
| `tools/question_generation/sba_session_composer.py` | `load_master_bank()`, `select_sba_session_items()` — selects short (5) or standard (10) SBA sessions |
| `tools/question_generation/full_master_bank_session_composer.py` | `compose_master_bank_session()` — full-bank session with eligibility gating |
| `tools/question_generation/generate_session_payload.py` | Fetches `public_lab` collection from bank for session payload generation |
| `tools/question_generation/open_response_suitability.py` | Filters bank for open-response-suitable items |
| `tools/question_generation/open_response_pipeline.py` | Uses resolution layer to process open response items |

### Dashboard
| Module | Role |
|--------|------|
| `tools/dashboard/master_bank_utilization_data.py` | `build_master_bank_utilization_data()` — computes utilization metrics for dashboard |
| `tools/dashboard/update_architecture_dashboard_state.py` | Updates `system_state.json` with bank counts |
| `frontend/architecture-dashboard/system_state.json` | Stores bank totals for dashboard display |

### Learner Model
| Module | Role |
|--------|------|
| `tools/learner_model/learning_event_runtime.py` | Imports `SAFE_GOVERNANCE` from master_bank module |

### Config / Knowledge
| File | Role |
|------|------|
| `knowledge/config/diagnostic_blueprint.json` | References `master_bank_total: 616`; RA item counts |
| `knowledge/question-bank/open_response/open_response_bank.json` | References master bank as source; notes SBA pool |
| `knowledge/question-bank/master_bank/master_bank.schema.json` | JSON schema for validation |

---

## Routes and Frontends

| Route/Frontend | Bank items served |
|----------------|------------------|
| `frontend/diagnostic-sba/index.html` + `preguntas.json` | 36 items (approved_for_static_demo = public_lab) |
| SBA session composer | Selects from public_lab collection (36 items) |
| Full master bank session (when enabled) | Reads all 616 items; gates by eligibility |
| Dashboard | Reads bank counts only (no question content) |

---

## What Routes Do NOT Exist Yet

| Missing route | Items affected |
|---------------|----------------|
| Activation pipeline for `approved_private_sba` items | 83 items |
| Bulk activation of unreviewed items | 471 items |
| Open response session route | 26 items (bank exists; no live route) |
| RA-filtered session routes (RA2, RA3, etc.) | All 616 items |

---

## Conclusion

The master bank is fully wired into the runtime toolchain. The utilization gap is entirely an **activation gap**, not a missing-code gap. The infrastructure to serve more items exists; the decision gate is human review and activation status, not engineering work.
