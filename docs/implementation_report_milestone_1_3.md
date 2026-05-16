# Implementation Report: Milestones 1–3
## WSET-AI-System — Backend Completion Report

**Date:** 2026-05-15
**Scope:** Phases A through G — LES write-back, causal chain substrate, retrieval integration, tutor rendering, misconception engine refactor, test coverage
**Status:** Implementation complete; live self-eval pending (workspace unavailable during session)

---

## Files Created

| File | Phase | Purpose |
|---|---|---|
| `tools/orchestrator/les_reconciler.py` | A | LES write-back pipeline — reconcile_les_from_feedback() |
| `knowledge/knowledge-map/causal-chains/cc_cool_climate_acidity.json` | B | Updated with causal_chain_v1 schema |
| `knowledge/knowledge-map/causal-chains/cc_warm_climate_alcohol.json` | B | New — warm climate → alcohol |
| `knowledge/knowledge-map/causal-chains/cc_flor_biological_ageing.json` | B | New — flor → biological ageing |
| `knowledge/knowledge-map/causal-chains/cc_fortification_residual_sugar.json` | B | New — fortification → residual sugar |
| `knowledge/knowledge-map/causal-chains/cc_mlf_texture.json` | B | New — MLF → texture |
| `knowledge/knowledge-map/causal-chains/cc_tannin_astringency.json` | B | New — tannin → astringency |
| `knowledge/knowledge-map/causal-chains/cc_barrel_ageing_oak_character.json` | B | New — barrel ageing → oak character |
| `knowledge/knowledge-map/causal-chains/cc_bottle_ageing_sediment.json` | B | New — bottle ageing → sediment |
| `knowledge/knowledge-map/causal-chains/cc_fractional_blending_consistency.json` | B | New — solera → consistency |
| `knowledge/knowledge-map/misconceptions/mc_tannin_quality_02.json` | E | New — more tannin ≠ better quality |
| `knowledge/knowledge-map/misconceptions/mc_oak_quality_01.json` | E | New — more oak ≠ higher quality |
| `knowledge/knowledge-map/misconceptions/mc_alcohol_quality_01.json` | E | New — higher alcohol ≠ better |
| `knowledge/knowledge-map/misconceptions/mc_residual_sugar_sweet_01.json` | E | New — RS ≠ always sweet |
| `knowledge/knowledge-map/misconceptions/mc_complexity_length_01.json` | E | New — complexity ≠ length |
| `knowledge/knowledge-map/misconceptions/mc_ageing_improvement_01.json` | E | New — not all wines improve with age |
| `knowledge/knowledge-map/misconceptions/mc_cold_stabilisation_quality_01.json` | E | New — tartrate crystals ≠ fault |
| `tests/test_milestone_1_3.py` | G | 35 new tests covering all phases |
| `knowledge/self-eval/before_vs_after_self_eval.md` | F | Comparative diagnostic report |
| `knowledge/self-eval/causal_chain_impact_report.md` | F | Chain-by-chain impact analysis |

---

## Files Modified

| File | Phase | What Changed |
|---|---|---|
| `tools/orchestrator/learner_state.py` | A | schema_version bumped to `minimal_brain_v2` in DEFAULT_LES and DEFAULT_SESSION_STAGING (R06 fix) |
| `tools/self_eval/evaluation_reporter.py` | A | write_evaluation_reports() now annotates feedback with questions_attempted, calls reconcile_les_from_feedback() after writing feedback; note text updated to reflect live reconciliation |
| `tools/retrieval/tutor_retrieval_sandbox.py` | C | `_knowledge_node_type()` now recognises `node_type` field; `_knowledge_node_id()` now reads `node_id`; `_knowledge_node_primary_phrases()` now includes `trigger_keywords` and `steps[].text`; `run_retrieval_sandbox()` now returns `matched_causal_chain_nodes`; `select_matched_causal_chain_nodes()` added |
| `tools/orchestrator/orchestrator.py` | C | `run_orchestrator()` passes `matched_causal_chain_nodes` to context package; `build_context_package()` now accepts and includes `forced_causal_chains` |
| `tools/tutor/answer_builder.py` | D | `_render_causal_chain()` added; `_select_best_causal_chain()` added; `_cause_effect_line()` now prefers structured chain node over keyword dispatch; falls back to hardcoded strings only when no chain matches |
| `tools/orchestrator/misconception_prepass.py` | E | STOPWORDS no longer contains `cool`, `climate`, `wine`, `wines` (R07 fix); `_concept_bias()` fully refactored to read `detection_keywords` from node files — no hardcoded node IDs remain |
| `knowledge/knowledge-map/misconceptions/mc_acidity_01.json` | E | Added `detection_keywords` + 5 paraphrase detection_signals |
| `knowledge/knowledge-map/misconceptions/mc_tannin_01.json` | E | Added `detection_keywords` + 5 paraphrase detection_signals |
| `knowledge/knowledge-map/misconceptions/mc_cool_climate_02.json` | E | Added `detection_keywords` + 5 paraphrase detection_signals |
| `tests/test_minimal_brain_orchestrator.py` | G | `_write_misconception_fixture()` updated to include `detection_keywords` so existing tests work with refactored `_concept_bias()` |

---

## Tests Added

`tests/test_milestone_1_3.py` — 35 new tests across 6 test classes:

**LESReconciliationTests (11 tests)**
- session_count increments by questions_attempted
- session_count accumulates across multiple runs
- known_weak_areas populated from feedback
- recent_misconceptions populated from feedback
- governance always false after reconciliation
- weak areas deduplicated
- misconception history capped at MAX_RECENT_MISCONCEPTIONS
- schema_version aligned to v2
- dry_run does not write file
- missing feedback file returns skipped status
- LES written to disk

**CausalChainLoadingTests (8 tests)**
- causal chain node type recognised by load_knowledge_nodes()
- causal chain node_id extracted correctly
- trigger_keywords included in primary phrases for detection
- causal chain detected for matching query
- select_matched_causal_chain_nodes returns full node with steps
- select_matched_causal_chain_nodes enforces governance
- path field stripped from returned node
- forced_causal_chains present in context package after orchestrator run

**CausalChainRenderingTests (9 tests)**
- Spanish labels present (CAUSA/MECANISMO/EFECTO/FORMULACIÓN)
- English labels present (CAUSE/MECHANISM/EFFECT/EXAM FORMULATION)
- Step text content in output (not hardcoded strings)
- SAT relevance included in output
- Blocked when safe_for_examiner=True
- Empty when no steps
- Best chain selection by keyword overlap
- Returns None when no chains
- Tutor answer renders step text from node (not keyword dispatch)

**MisconceptionDetectionRefactorTests (8 tests)**
- Structured require_all=True fires when all tokens present
- Simple list fires when any token matches
- Structured require_all=True does NOT fire when tokens absent
- New node detected via detection_keywords without code change
- STOPWORDS no longer contains domain words (cool/climate/wine/wines)
- cool and climate survive tokenisation
- wine survives tokenisation
- MC_COMPLEXITY_LENGTH_01 detectable via detection_keywords

**SchemaConsistencyTests (4 tests)**
- DEFAULT_LES schema is v2
- DEFAULT_SESSION_STAGING schema is v2
- LES_SCHEMA_VERSION in reconciler is v2
- LES and staging schemas match each other

**GovernanceEnforcementTests (4 tests)**
- Live causal chain nodes: none have safe_for_examiner=True
- Live misconception nodes: none have safe_for_examiner=True
- _apply_feedback cannot inject safe_for_examiner=True
- build_tutor_answer governance output always false

---

## Test Run Status

**Status: Could not execute.** The Linux sandbox workspace failed to start during this session. Command to run manually:

```bash
cd C:\Users\esand\OneDrive\Documents\WSET-AI-System
python -m unittest discover -s tests -v
```

Expected outcome based on code inspection: all 35 new tests should pass. The one risk is `test_causal_chains_present_in_context_package` — this test relies on the knowledge-map directory being present under the root path passed to `run_orchestrator()`. The test fixture builds the chain dir under tmp; whether the real Orchestrator finds the chains depends on `PROJECT_ROOT` resolution.

If any existing test fails, the most likely cause is `test_misconception_detection` — which relies on signal matching reaching confidence ≥ 0.45. The STOPWORDS change (removing `wine`) means "wine" is now a detection token, which should increase not decrease overlap scores. Risk is low.

---

## Misconception Coverage

| Node ID | Status | Intervention | Detection keywords |
|---|---|---|---|
| MC_ACIDITY_01 | Pre-existing, updated | contrast_comparison | ✓ 6 rules |
| MC_TANNIN_01 | Pre-existing, updated | direct_correction | ✓ 6 rules |
| MC_COOL_CLIMATE_02 | Pre-existing, updated | causal_chain_walkthrough | ✓ 8 rules |
| MC_TANNIN_QUALITY_02 | New | contrast_comparison | ✓ 5 rules |
| MC_OAK_QUALITY_01 | New | contrast_comparison | ✓ 5 rules |
| MC_ALCOHOL_QUALITY_01 | New | contrast_comparison | ✓ 5 rules |
| MC_RESIDUAL_SUGAR_SWEET_01 | New | contrast_comparison | ✓ 5 rules |
| MC_COMPLEXITY_LENGTH_01 | New | direct_correction | ✓ 5 rules |
| MC_AGEING_IMPROVEMENT_01 | New | contrast_comparison | ✓ 5 rules |
| MC_COLD_STABILISATION_QUALITY_01 | New | direct_correction | ✓ 5 rules |

**Coverage: 10 of 10 target exam-destructive misconceptions — 100%.**

---

## Causal Chains Loaded

9 nodes, all with `node_type: "causal_chain"`, `safe_for_examiner: false`, `agent_corpus: "tutor"`. Coverage of baseline self-eval failing chains: 6 of 7 (86%). One gap remains: `no flor → oxidative ageing`.

---

## LES Write-Back Status

- `reconcile_les_from_feedback()` implemented in `tools/orchestrator/les_reconciler.py`
- `write_evaluation_reports()` now calls it automatically after every self-eval run
- `session_count` will increment by `questions_attempted` per run
- `known_weak_areas` will accumulate causal chain gaps, retrieval weaknesses, failure labels
- `recent_misconceptions` will accumulate misconception gaps, capped at 10
- Schema aligned to `minimal_brain_v2` across LES, staging, and reconciler
- Standalone CLI: `python -m tools.orchestrator.les_reconciler --help`

**First live test:** run the self-eval, then check `knowledge/nazareth/epistemic_state.json`. `session_count` should be non-zero and `known_weak_areas` should be non-empty.

---

## Self-Eval Delta (Projected)

| Metric | Before (brutal, 25q) | Projected (hard, 25q) | Change |
|---|---|---|---|
| `missing_causal_link` | 76% | 35–45% | −31–41pp |
| `unsupported_conclusion` | 68% | 40–55% | −13–28pp |
| `weak_exam_register` | 36% | 25–35% | −1–11pp |
| `shallow_retrieval` | 28% | 20–28% | 0–8pp |
| Misconception coverage | 3 nodes | 10 nodes | +7 |
| LES adaptive state | None | Operational | — |

These are architectural projections. Actual numbers require a live self-eval run.

---

## Remaining Architecture Gaps

### What still blocks true strategic orchestration

**Gap 1: Orchestrator reads LES but does not plan from it.**
The Orchestrator's binary routing logic (misconception vs. normal) does not use `known_weak_areas` or `recent_misconceptions` to prioritise what to teach. The LES now has real data. The Orchestrator still ignores it. Phase 3/5 of the cognitive planning cycle (generate session plan from LES priorities) is not implemented.

**Gap 2: Tutor synthesis is keyword dispatch for unmatched queries.**
The causal chain rendering applies only when a chain node is matched. Queries not covered by the 9 nodes still receive hardcoded keyword-dispatch content from `_idea_from_context_item()`. The retrieved chunk text is still discarded. LLM integration is the correct fix — but requires the retrieval structure to be correct first (now done).

**Gap 3: SAT cognitive engine not yet implemented.**
The SAT-specific reasoning module described in `sat_cognitive_engine.md` — reverse reasoning from observation to quality conclusion — does not exist as a separate code path. SAT queries go through the same `answer_normally` routing as general theory questions.

**Gap 4: No cross-session progress tracking.**
The Orchestrator writes a staging file per session but does not compare the current session to prior sessions to identify trends. The LES `session_count` grows but the Orchestrator does not use it to vary its approach (e.g., increase difficulty, introduce new topics, spiral back to persistent gaps).

**Gap 5: Causal chain oxidative ageing gap.**
`no flor → oxidative ageing` (1 weighted self-eval failure) has no causal chain node. `CC_OXIDATIVE_AGEING` is needed.

**Gap 6: Live self-eval run not completed.**
Phase F required running `self-eval --limit 25 --strictness hard` to generate actual before/after numbers. The workspace was unavailable. The comparison report uses projections only. Run the command to get real numbers.

---

## What Must Be Done Next

In priority order:

1. **Run the self-eval** to confirm actual numbers and trigger the first real LES write-back
2. **Wire LES weak areas into Orchestrator routing** — when `known_weak_areas` contains a causal chain gap, the Orchestrator should force that chain into retrieval for relevant queries
3. **Add CC_OXIDATIVE_AGEING** — closes the one remaining causal chain gap
4. **LLM integration for Tutor synthesis** — the context package is ready; the chain rendering provides the structural substrate; an LLM reading the package can now produce genuinely grounded synthesis

---

*Generated: 2026-05-15 | Implementation Report | Milestones 1–3*
*Not an official WSET document. Not for learner-facing use.*
