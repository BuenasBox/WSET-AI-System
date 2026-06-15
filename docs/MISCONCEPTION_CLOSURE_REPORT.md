# Misconception Closure Report

**Date:** 2026-06-15
**Status:** M.1-M.6 implemented with an in-place adapter
**Starting state:** 0/20 fully detectable end to end
**Ending state:** 20/20 supported by the shared detection, evidence, coaching,
recommendation, and presentation contracts

## Result

The 20 legacy misconception nodes remain the sole pedagogical source of truth.
No source node schema was extended. A read-only adapter now derives:

- normalized detection phrases
- weakness and recommendation relationships
- evidence history
- low/medium/high evidence-frequency labels
- coaching and remediation views
- Profile and Full Simulation presentation models

## Phase Results

### M.1 Audit

- Restored all 20 nodes to their pre-sprint schemas.
- Replaced the earlier assumption-based audit.
- Documented every adapter field assumption.

### M.2 Detection

- The existing tutor pre-pass delegates to the shared adapter.
- Explicit IDs remain backward compatible.
- SBA selected distractor text can be inferred deterministically.
- Open Response text is constrained to the item’s relevant node IDs.
- SAT uses the same text-evidence runtime path.
- Explicit weakness-profile misconception IDs are accepted.
- Generic topic weakness alone does not create a misconception hit.

### M.3 Evidence Confidence

Evidence is accumulated as events, not probabilities:

- low: one active observation
- medium: two active observations
- high: at least three active observations across at least two sessions

A correction closes the active run and preserves lifetime history. Duplicate
events are idempotent.

### M.4 Coaching And Recommendation

Every node produces:

- why the misunderstanding matters
- what the learner is confusing
- the triggering evidence trace
- topics, concepts, intervention, and available WWJ remediation to practise
- corrected understanding as the improvement signal

Existing adaptive signals and question composition continue to consume the
legacy `mc_id` contract.

### M.5 Profile

The production dashboard now accepts backend-shaped insights or legacy memory
through `MisconceptionEngine.adaptMisconceptionInsights()`. Profile output:

- uses student-facing statements
- shows evidence counts and ordinal frequency labels
- does not render technical IDs
- does not render percentages or prediction language

### M.6 Full Simulation

Full Simulation:

- assigns one stable simulation session ID
- filters findings to that session
- recomputes evidence count and frequency for that simulation
- shows source/item trace, practice priority, and next activity
- excludes lifetime evidence from the simulation trace

## Detectability Matrix

All 20 nodes have the same ending classification because the adapter is
data-driven and the tests exercise every source node.

| Node | Ending classification |
|---|---|
| MC_ACIDITY_01 | FULLY DETECTABLE |
| MC_ACIDITY_02 | FULLY DETECTABLE |
| MC_AGEING_IMPROVEMENT_01 | FULLY DETECTABLE |
| MC_ALCOHOL_QUALITY_01 | FULLY DETECTABLE |
| MC_BOTRYTIS_01 | FULLY DETECTABLE |
| MC_COLD_STABILISATION_QUALITY_01 | FULLY DETECTABLE |
| MC_COMPLEXITY_LENGTH_01 | FULLY DETECTABLE |
| MC_COOL_CLIMATE_01 | FULLY DETECTABLE |
| MC_COOL_CLIMATE_02 | FULLY DETECTABLE |
| MC_LEES_AGEING_01 | FULLY DETECTABLE |
| MC_MLF_01 | FULLY DETECTABLE |
| MC_MLF_02 | FULLY DETECTABLE |
| MC_OAK_01 | FULLY DETECTABLE |
| MC_OAK_02 | FULLY DETECTABLE |
| MC_OAK_QUALITY_01 | FULLY DETECTABLE |
| MC_RESIDUAL_SUGAR_SWEET_01 | FULLY DETECTABLE |
| MC_TANNIN_01 | FULLY DETECTABLE |
| MC_TANNIN_02 | FULLY DETECTABLE |
| MC_TANNIN_QUALITY_02 | FULLY DETECTABLE |
| MC_WHOLE_BUNCH_01 | FULLY DETECTABLE |

`FULLY DETECTABLE` means a direct node ID or qualifying text observation can
travel through the implemented contracts to an evidence-based presentation
model. It does not mean every current SBA, OR, or SAT corpus item contains an
authored mapping for every node.

## Files Modified

Backend:

- `tools/learner_model/misconception_adapter.py`
- `tools/learner_model/misconception_runtime.py`
- `tools/learner_model/learning_event_runtime.py`
- `tools/orchestrator/misconception_prepass.py`
- `tests/test_misconception_adapter.py`
- `tests/test_learning_event_runtime_integration.py`
- closure audit, design, plan, report, and validation documents

Dashboard:

- `shared/misconception-engine.js`
- `shared/simulation-coaching.js`
- `profile/profile.js`
- `full-simulation/index.html`
- `tests/test_misconception_visibility.js`

## Remaining Limitations

1. The local Python backend and static production dashboard remain separate
   deployments. The dashboard consumes an injected insight payload or
   `wset_misconception_insights_v1`; this sprint did not create a new transport
   service.
2. Corpus mapping density is uneven. A node is detectable when direct evidence
   exists, but not every current item supplies relevant node IDs.
3. Generic weakness topics are deliberately insufficient evidence for a
   specific misconception.
4. The legacy Y.2 weakness engine retains its numeric fields for backward
   compatibility. New learner-facing misconception views use only ordinal
   evidence labels.
5. The frontend Profile route already violated its older isolation test by
   importing `learner_intelligence.js`; this sprint did not remove Y.2/Y.3
   imports.

No new content, architecture, ML, AI, LLM, embedding, vector database, or
external service was introduced.
