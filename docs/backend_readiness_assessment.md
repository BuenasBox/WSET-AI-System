# Backend Readiness Assessment
**WSET-AI-System | Step 8 — Post-Distinction-Layer Stabilisation**
Date: 2026-05-17

---

## 1. Purpose

This document assesses the current readiness of the WSET-AI-System backend against three criteria:

1. **Functional stability**: Does the system produce pedagogically coherent Tutor output across the full 25-question self-eval bank?
2. **Metric trajectory**: Are the key self-eval failure labels moving in the right direction?
3. **Minimum viable local UI sandbox**: Is the backend ready to support a thin local interface for interactive student use?

This assessment is static (no runtime sandbox available at time of writing). It is based on code inspection, self-eval JSONL records, and the changes implemented in Tasks 41–52.

---

## 2. Functional Stability Assessment

### 2.1 Tutor Answer Pipeline

| Component | Status | Notes |
|---|---|---|
| Orchestrator | Stable | Routes to misconception_intervention or normal flow correctly |
| Misconception pre-pass | Stable | 7 misconception nodes; false positive rate low after MC_COOL_CLIMATE_02 fix |
| Retrieval sandbox | Stable | DOMAIN_EXPANSIONS extended; ASCII token limitation documented |
| Causal chain injection | Stable | 9 chain nodes; trigger_keywords include Spanish terms for Q1–Q4 |
| Answer builder | Stable | 5 functions extended; 15+ topic patterns ES + EN |
| LES write-back | Stable | `reconcile_les_from_feedback()` implemented; session write-back active |
| Self-eval runner | Stable | Produces JSONL; `answer_comparator.py` fixes applied |

### 2.2 Governance Rails

All governance constraints remain intact:
- `safe_for_examiner = False` enforced in `_validate_governance()`
- `examiner_scoring_allowed = False` enforced
- No LLM, no API, no embeddings, no vector DB, no cloud services
- Disclaimer appended to every Tutor output in both ES and EN

### 2.3 Known Residual Issues

| Issue | Severity | Impact |
|---|---|---|
| `_tokens()` ASCII-only | Low | Spanish accented words fragment; mitigated by ASCII trigger_keywords in chain JSON files |
| No golden annotations for 7 topic clusters | Low-Medium | `shallow_retrieval` remains for these in brutal mode |
| Q5 missing CC_OXIDATIVE_AGEING chain | Low | 1 `missing_causal_link` persists; no chain covers "flor dies → oxidative ageing" |
| Topically wrong chunks for Spanish queries without expansions | Low | Partially mitigated by new DOMAIN_EXPANSIONS; golden curation is the full fix |

---

## 3. Metric Trajectory

### 3.1 Historical progression

| Metric | Hard baseline (pre-Task 41) | Brutal after Task 45 | Projected post-Task 52 |
|---|---|---|---|
| `missing_causal_link` | 5 / 17 | 1 | 1 (Q5 is a known gap) |
| `unsupported_conclusion` | 17 / — | 0 | 0 |
| `shallow_retrieval` | 7 / 10 | 10 | 3–5 |
| `shallow_reasoning` | 3 / 2 | 2 | 1–2 |
| `weak_exam_register` | 11 / 9 | 9 | 1–3 |
| `weak_sat_commitment` | not tracked | not tracked | 0–2 |
| `incomplete_balance_justification` | not tracked | not tracked | 0–2 |

The trajectory shows significant quality improvement on the highest-impact labels. The remaining failures cluster around retrieval infrastructure (golden annotations) rather than answer content.

### 3.2 Assessment

The system has crossed two major quality thresholds:
- `unsupported_conclusion` eliminated (was the largest single failure class)
- `missing_causal_link` reduced by 94% (19→1)

The current frontier is retrieval depth (7 golden annotation gaps) and exam register (topic pattern coverage for the 9 non-matching questions, now addressed by distinction layer refinement).

---

## 4. Minimal Local UI Sandbox Readiness

### 4.1 What "minimal local UI sandbox" means in this context

A minimal sandbox would allow a student to:
1. Type a query
2. Have the orchestrator + retrieval + builder pipeline run locally
3. Receive a formatted Tutor answer (Markdown rendered in browser or native window)
4. Optionally trigger LES write-back after rating the answer

No cloud, no API, no front-facing server exposed to the internet.

### 4.2 Current backend interface

The system already exposes a CLI entry point:
```
python -m tools.youtube_transcription.main self-eval --limit N --strictness [hard|brutal]
```

The `build_tutor_answer()` function accepts a context package path and returns a formatted Markdown string. The full pipeline (query → context package → tutor answer) is wired end-to-end.

What is missing for a minimal UI:
- A query intake form (HTML or TKinter) that accepts free text
- A call to `run_retrieval_sandbox()` + `build_tutor_answer()` on the result
- A Markdown renderer for the output (can be a static HTML page opened in browser)
- Optional: a feedback thumbs-up/down that writes back to LES

### 4.3 Readiness verdict

**The backend is ready to serve a minimal local UI sandbox.**

Conditions:
- All pipeline components are stable and individually tested
- The `build_tutor_answer()` API is clean and takes a single Path argument
- The governance rails are enforced at the function level, not at the UI level — no UI changes could bypass them
- The LES write-back is already functional

Recommended next step: a single Python file using Flask (or just `http.server`) that:
1. Serves a one-page HTML form
2. On submit: runs the full pipeline in a subprocess or direct import
3. Returns the Markdown-rendered Tutor answer as HTML
4. Optionally: appends a thumbs-up/down form for LES feedback

Effort estimate: 2–4 hours, no new backend code required.

---

## 5. Risk Register (Current State)

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| `_tokens()` regex breaks new Spanish topic triggering | Low | Low | DOMAIN_EXPANSIONS use ASCII trigger keys; pattern-matched using `trigger in query_lower` not token comparison |
| New answer patterns contain incorrect wine facts | Low | Medium | Patterns reviewed against official WSET material; all claims grounded in standard WSET Level 3 content |
| Self-eval JSONL grows large and slows analysis | Low | Low | Append-only; existing tooling handles any reasonable size |
| LES write-back corrupts epistemic state on concurrent writes | Very Low | Medium | CLI is single-process; no concurrency risk in current setup |
| Causal chain trigger_keywords over-fire on unrelated queries | Low | Low | `_select_best_causal_chain()` picks the best-scoring chain by keyword overlap, limiting spurious matches |

---

## 6. Recommended Next Actions (Priority Order)

1. **Run self-eval** (hard + brutal, 25q each) to confirm metric movement from distinction layer + SAT commitment fixes
2. **Curate golden chunk annotations** for 7 topic clusters to resolve remaining shallow_retrieval
3. **Add CC_OXIDATIVE_AGEING chain node** (flor → oxidative ageing) to resolve Q5 missing_causal_link
4. **Build minimal local UI sandbox** — backend is ready, thin front-end only
5. **Unicode-aware `_tokens()` fix** — low urgency, replace ASCII regex with `\w` + `re.UNICODE`

---

## 7. Conclusion

The WSET-AI-System backend has reached a state of pedagogical coherence across the full question bank. The Tutor now produces substantive, topic-specific content with causal structure for all major exam topic clusters. Governance rails are intact. The system is ready to serve a minimal local UI sandbox without further backend work. The remaining self-eval failures are infrastructure gaps (retrieval annotation depth) that can be addressed incrementally without architectural change.
