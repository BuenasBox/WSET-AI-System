# Misconception Closure Audit

**Date:** 2026-06-15  
**Baseline:** commit `564d93c` plus the existing Y.2/Y.3 consumers  
**Starting state:** 0 of 20 nodes fully detectable end to end

## Audit Method

The audit inspected:

- the 20 JSON nodes in `knowledge/knowledge-map/misconceptions/`
- `misconception_prepass.py`
- `misconception_runtime.py`
- SBA and Open Response paths in `learning_event_runtime.py`
- adaptive signal, recommendation, remediation, coaching, Profile, and Full Simulation consumers

`FULLY DETECTABLE` means evidence can enter an existing answer path, be attributed
to a node, accumulate deterministically, produce recommendation and coaching
output, and reach a student-facing view with an evidence trace.

## Source Schema

All 20 legacy nodes load successfully without migration. Every node has:

- `misconception_id`
- `misconception`
- `why_incorrect`
- `corrected_understanding`
- `related_topics`
- `related_concepts`
- `severity`
- `frequency`
- `tutor_intervention`
- `detection_signals`
- `_meta`

Some nodes additionally have `detection_keywords`. This field is optional.

No node requires `weakness_signal`, `coaching_content`, `remediation_topics`, or
another schema extension. Those are derived adapter views, not source fields.

## Starting-State Findings

| Layer | Evidence |
|---|---|
| Node loading | 20/20 load through the existing pre-pass |
| Free-text matching | 20/20 can match their canonical statement or a detection signal |
| SBA | Runtime can consume an explicit `mc_id`; corpus coverage is not universal |
| Open Response | Runtime accepts `mc_ids_relevant`, but absence of a causal chain was incorrectly treated as misconception evidence |
| SAT | No direct misconception evidence adapter |
| Weakness profiles | Generic topic weakness cannot safely prove a specific misconception |
| Confidence | Detection uses match scores; persistence uses counts, but there is no shared evidence-frequency label |
| Recommendation | Existing adaptive consumers can prioritize an existing `mc_id` |
| Coaching | Source explanations and remediation lookup exist, but no normalized coaching contract |
| Profile | Reads fields that are not produced by the backend runtime |
| Full Simulation | Reads lifetime memory rather than simulation-scoped evidence |

## Node Classification

All nodes share the same starting classification because the missing links are
systemic, not node-specific.

| Misconception node | Starting classification |
|---|---|
| MC_ACIDITY_01 | PARTIALLY DETECTABLE |
| MC_ACIDITY_02 | PARTIALLY DETECTABLE |
| MC_AGEING_IMPROVEMENT_01 | PARTIALLY DETECTABLE |
| MC_ALCOHOL_QUALITY_01 | PARTIALLY DETECTABLE |
| MC_BOTRYTIS_01 | PARTIALLY DETECTABLE |
| MC_COLD_STABILISATION_QUALITY_01 | PARTIALLY DETECTABLE |
| MC_COMPLEXITY_LENGTH_01 | PARTIALLY DETECTABLE |
| MC_COOL_CLIMATE_01 | PARTIALLY DETECTABLE |
| MC_COOL_CLIMATE_02 | PARTIALLY DETECTABLE |
| MC_LEES_AGEING_01 | PARTIALLY DETECTABLE |
| MC_MLF_01 | PARTIALLY DETECTABLE |
| MC_MLF_02 | PARTIALLY DETECTABLE |
| MC_OAK_01 | PARTIALLY DETECTABLE |
| MC_OAK_02 | PARTIALLY DETECTABLE |
| MC_OAK_QUALITY_01 | PARTIALLY DETECTABLE |
| MC_RESIDUAL_SUGAR_SWEET_01 | PARTIALLY DETECTABLE |
| MC_TANNIN_01 | PARTIALLY DETECTABLE |
| MC_TANNIN_02 | PARTIALLY DETECTABLE |
| MC_TANNIN_QUALITY_02 | PARTIALLY DETECTABLE |
| MC_WHOLE_BUNCH_01 | PARTIALLY DETECTABLE |

## Channel Limits

| Channel | Can trigger today? | Limitation |
|---|---|---|
| SBA | Partial | Requires an explicit distractor-to-node mapping or deterministic inference from the selected distractor text |
| Open Response | Partial | Relevant-node lists exist as a contract, but evidence must come from the response text, not merely a missing causal chain |
| SAT | Partial | Free-text evidence can be inspected, but no SAT attempt path records misconception evidence |
| Weakness profiles | Partial | Explicit misconception trend IDs are usable; generic weak topics are supporting context only |

No node is classified `NOT DETECTABLE`: each has direct textual evidence that
the existing deterministic matcher can recognize. No node is `FULLY DETECTABLE`
at baseline because the evidence, accumulation, coaching, and visibility
contracts are not connected.

## Adapter Assumptions

1. The legacy node is the sole pedagogical source of truth.
2. `misconception` describes what the learner is confusing.
3. `why_incorrect` supplies why the misunderstanding matters.
4. `corrected_understanding` supplies the correction and improvement evidence.
5. `related_topics` and `related_concepts` are practice targets, not proof.
6. `detection_signals` and optional `detection_keywords` are direct text evidence.
7. Generic topic weakness alone must not create a misconception hit.
8. Confidence labels describe accumulated evidence frequency only:
   `low`, `medium`, or `high`.
9. Match scores remain internal detector mechanics and are never presented as
   learner probability, readiness, or examiner scoring.

## Required Correction

Add one in-place adapter over the existing nodes. It must:

- normalize legacy fields without mutating the loaded node
- accept explicit IDs and deterministic text evidence
- record source, session, item, timestamp, and matched evidence
- derive evidence-frequency labels
- expose recommendation and formative coaching views
- preserve existing Y.2/Y.3 fields where consumers already depend on them
- provide Profile and simulation-scoped presentation models

This audit creates no new pedagogical content and makes no production claim.
