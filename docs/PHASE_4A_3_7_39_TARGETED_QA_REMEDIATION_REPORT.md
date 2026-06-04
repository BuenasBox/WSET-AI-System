# Phase 4A.3.7.39 - Targeted Gold Bank QA Remediation Report

Date: 2026-06-04

Decision: **READY FOR HUMAN REVIEW, NO SET MUTATION APPLIED**

This phase performed targeted QA on the active 36-question Gold Bank set only. It did not expand the set, re-audit the 524-item bank, alter RA weighting, force difficulty balancing, modify Tutor/Retrieval/Self-Eval/Golden/Snapshots/Governance/Causal Chains, or implement option shuffle.

## 1. Initial Worktree State

Branch: `codex/phase-4a3-7-32-gold-bank`

Commit: `29e50d4`

Initial `git status --short` was not clean. Changes were classified before any phase work continued.

Runtime / local artifacts:

- `knowledge/nazareth/self_eval_feedback.json`
- `knowledge/retrieval-sandbox/orchestrator_context_retrieval_debug.csv`
- `knowledge/self-eval/attempts/*`
- `knowledge/self-eval/pedagogical_memory.json`
- `knowledge/self-eval/self_eval_results.csv`
- `knowledge/self-eval/self_eval_results.jsonl`
- `knowledge/self-eval/self_eval_summary.md`

Safe handling recommendation for runtime artifacts: do not commit them. A safe cleanup, if desired before commit, is a path-scoped restore of tracked runtime files only, for example:

```powershell
git restore -- knowledge/nazareth/self_eval_feedback.json knowledge/retrieval-sandbox/orchestrator_context_retrieval_debug.csv knowledge/self-eval/attempts knowledge/self-eval/pedagogical_memory.json knowledge/self-eval/self_eval_results.csv knowledge/self-eval/self_eval_results.jsonl knowledge/self-eval/self_eval_summary.md
```

Real pre-existing Gold Bank changes:

- `frontend/diagnostic-sba/preguntas.json`
- `knowledge/question-bank/diagnostic_sba/reviews/first_5_human_review_records.json`
- `tests/test_static_demo_export_dry_run.py`
- `tests/test_static_demo_export_file.py`
- `tests/test_static_demo_exporter.py`
- `docs/ACTIVE_SET_RECONCILIATION_PLAN.md`
- `docs/GOLD_BANK_ACTIVATION_READINESS.md`
- `docs/PHASE_4A_3_7_37_GOLD_BANK_IMPLEMENTATION_REPORT.md`
- `docs/PHASE_4A_3_7_38_GOLD_BANK_QA_AUDIT.md`
- `knowledge/question-bank/diagnostic_sba/drafts/gold_bank_activation_drafts.json`
- `knowledge/question-bank/diagnostic_sba/reviews/gold_bank_activation_review_records.json`

This phase added only this report.

## 2. Q515 Analysis

Locations reviewed:

- Structured source: `knowledge/question-bank/structured/wset3_questions.json`
- Draft: `knowledge/question-bank/diagnostic_sba/drafts/gold_bank_activation_drafts.json`
- Review: `knowledge/question-bank/diagnostic_sba/reviews/gold_bank_activation_review_records.json`
- Active payload: `frontend/diagnostic-sba/preguntas.json`
- Gold Bank docs: `docs/CORPUS_GROUNDED_GOLD_BANK.md`, `docs/GOLD_BANK_ACTIVATION_READINESS.md`, `docs/PHASE_4A_3_7_38_GOLD_BANK_QA_AUDIT.md`
- Remediation dataset: `docs/CORPUS_REMEDIATION_DATASET.json`
- Full verification: `docs/FULL_BANK_CORPUS_VERIFICATION.json`
- Official corpus search for `troncoc`, `truncated`, `open vat`, `open ferment`, `malolactic`, `MLF`, `vats`

Item:

| Field | Value |
|---|---|
| ID | Q515 |
| RA | RA1 |
| Topic | `winemaking` |
| Subtopic | `open_vats_malolactic_fermentation` |
| Stem | `Que tipo de fermentacion se favorece con depositos troncoconicos abiertos?` |
| Correct | A: `Fermentacion malolactica` |
| Distractors | B spontaneous fermentation; C low-temperature fermentation; D aerobic fermentation with submerged cap |
| Gold class | Gold-B |
| Audit warning | Vessel-to-fermentation link may be over-inferred |

Support found:

- Official corpus supports malolactic fermentation as a process after alcoholic fermentation.
- Official corpus supports that MLF can be encouraged by temperature management and withholding SO2 after alcoholic fermentation.
- Official corpus supports that winemakers may ferment or mature wine in different vessels and allow only a proportion of wine to undergo MLF.

Support not found:

- No clean official-corpus passage was found linking open truncated/conical vats specifically to favoring malolactic fermentation.
- The strongest passages support MLF generally, not the vessel-to-MLF causal claim.

Reason for semantic risk:

Q515 asks for a vessel-driven fermentation outcome. The evidence available in the repo supports MLF and vessel choice separately, but not a clean causal relationship that open truncated vats favor MLF. This matches the Phase 4A.3.7.38 warning that the item is the clearest residual semantic risk.

## 3. Q515 Decision

Decision: **mark Q515 as requires_review in this report; do not auto-correct and do not mutate active artifacts.**

Rationale:

- There is no unequivocal minimal correction that preserves the original pedagogical intent.
- Changing the correct answer or stem would be editorial question rewriting, not targeted metadata remediation.
- Setting the review record to `requires_review` would remove Q515 from exporter eligibility and break the required active count of 36 unless a replacement is available.
- No inactive Gold-A or Gold-B replacement exists. The active set already consumes all 15 Gold-A and all 20 Gold-B items.

Recommended human-review action:

- Either retire Q515 from the active 36 after one PARTIAL item is promoted, or rewrite/repair Q515 in a separate source-specific hardening phase with explicit evidence for the vessel/process relationship.

## 4. Q21 vs Q216 Redundancy Analysis

Locations reviewed:

- Structured source, Gold Bank drafts/reviews, active payload, Gold Bank docs, remediation dataset, and full verification for Q21 and Q216.

Comparison:

| Field | Q21 | Q216 |
|---|---|---|
| Stem | `Cual es una variedad comunmente utilizada en el espumoso Cremant de Loire?` | `Que variedad blanca domina los espumosos Cremant de Loire?` |
| Correct | C: Chenin Blanc | A: Chenin Blanc |
| Topic/subtopic | `sparkling_wines / cremant_de_loire_chenin_blanc` | `sparkling_wines / cremant_de_loire_chenin_blanc` |
| Gold class | Gold-C exception | Gold-B |
| Distractors | Broad international red grapes | Plausible white-grape alternatives |
| Review note | Source specificity and distractor strength require significant review | Needs Cremant-specific source review |
| Diagnostic depth | Lower | Higher |

Classification: **Redundant**

Reasoning:

- Both test the same exact concept: Chenin Blanc in Cremant de Loire.
- Same RA, same topic, same subtopic, same correct concept.
- Q216 is the stronger item because it has a cleaner stem and more plausible same-category distractors.
- Q21 is the weaker item because it is the only Gold-C active item and uses broad grape-name distractors.

## 5. Redundancy Decision

Decision: **keep both temporarily; mark Q21 as the replacement target for human review.**

Rationale:

- Replacing Q21 is semantically justified.
- However, within the user constraints, replacement must come from Gold-A first or Gold-B second.
- There are no inactive Gold-A or Gold-B candidates left; the active 36 already includes all Gold-A/B candidates from the Gold Bank.
- Replacing Q21 with another Gold-C would violate the requested replacement priority and would not improve the Gold-C exception problem.
- Replacing Q21 with a PARTIAL candidate would require a source-specific promotion phase, which is explicitly outside this targeted remediation.

Recommended human-review action:

- Prefer Q216 over Q21 when one Cremant/Chenin item must be retained.
- Replace Q21 only after a PARTIAL candidate is promoted to Gold-A/B, or after Q21 is repaired and reclassified.

## 6. Correct Answer Distribution A/B/C/D

Active 36 distribution:

| Position | Count | Percent |
|---|---:|---:|
| A | 5 | 13.9% |
| B | 13 | 36.1% |
| C | 15 | 41.7% |
| D | 3 | 8.3% |

B/C together: 28/36 = 77.8%.

Other measured composition:

| Dimension | Distribution |
|---|---|
| RA | RA1=5, RA2=22, RA3=5, RA4=3, RA5=1 |
| Difficulty | intermediate=36 |

RA2 and intermediate skew were intentionally not treated as automatic defects in this phase, per human decision.

## 7. Option Shuffle Recommendation

Do not rewrite question text or answer keys to fix position bias.

Recommended contract for a future option-shuffle subphase:

1. Preserve canonical option order and canonical `option_id` values in JSON.
2. Generate a visual order deterministically or pseudo-randomly at render/session time.
3. Store mapping `visual_slot -> option_id` and evaluate by `option_id`, not visual position.
4. Keep `correct_option_id` only in post-submit outcome data, never in pre-submit render data.
5. Ensure option diagnostics follow canonical `option_id`, not displayed slot.
6. Preserve post-submit diagnostic behavior, including selected-option diagnostics and wrong-option feedback.
7. Keep analytics able to distinguish original answer position from visual display position.

Current frontend dependency summary:

- `frontend/diagnostic-sba/index.html` currently validates render options as exactly `A,B,C,D`.
- It renders `op.option_id` as the visible key.
- Keyboard selection uses visible keys `A/B/C/D`.
- Post-submit correctness compares selected ID directly against `outcome.correct_option_id`.
- Therefore shuffle requires explicit frontend/export contract work and should not be implemented implicitly.

## 8. Changes Applied

Applied:

- Added this report: `docs/PHASE_4A_3_7_39_TARGETED_QA_REMEDIATION_REPORT.md`

Not applied:

- No changes to `frontend/diagnostic-sba/preguntas.json`.
- No changes to Gold Bank drafts.
- No changes to review records.
- No payload regeneration write.
- No option shuffle implementation.
- No replacement.

## 9. Changes Not Applied And Rationale

| Candidate change | Decision | Rationale |
|---|---|---|
| Auto-correct Q515 | Not applied | No unequivocal evidence-backed correction. |
| Change Q515 `review_status` to `requires_review` | Not applied | Would reduce exporter eligibility below 36 with no Gold-A/B replacement available. |
| Replace Q515 | Not applied | No inactive Gold-A/B candidate exists. |
| Replace Q21 | Not applied | Semantically justified, but no inactive Gold-A/B candidate exists. |
| Use Gold-C replacement | Not applied | Would not improve activation quality and violates replacement priority. |
| Use PARTIAL replacement | Not applied | Requires separate source-specific promotion phase. |
| Implement option shuffle | Not applied | Explicitly reserved for separate authorized subphase. |

## 10. Dry-Run Result

Command:

```powershell
python -m tools.question_generation.export_static_demo_questions --dry-run
```

Result:

```text
export_version: static_demo_export_v0
static_demo_only: True
eligible_item_count: 36
source_question_ids: 2, 21, 83, 105, 107, 206, 216, 228, 230, 232, 240, 258, 265, 268, 269, 270, 277, 287, 301, 308, 309, 325, 356, 395, 402, 421, 424, 438, 440, 441, 464, 493, 498, 515, 659, 834
validation_errors: 0
target_path: frontend/diagnostic-sba/preguntas.json
```

## 11. Test Result

Command:

```powershell
python -m unittest discover -s tests -v
```

Result:

```text
Ran 1352 tests in 11.033s

OK (skipped=9)
```

## 12. Final Worktree State

Final `git status --short` remains dirty due to the same classified pre-existing changes plus this phase report.

Phase-owned change:

- `docs/PHASE_4A_3_7_39_TARGETED_QA_REMEDIATION_REPORT.md`

Pre-existing dirty files remain classified as described in Section 1:

- Runtime/local artifacts under `knowledge/nazareth/`, `knowledge/retrieval-sandbox/`, and `knowledge/self-eval/`.
- Gold Bank activation changes under `frontend/diagnostic-sba/`, `knowledge/question-bank/diagnostic_sba/`, `tests/test_static_demo_export*`, and prior Gold Bank docs.

No additional payload, draft, review, governance, Tutor, Retrieval, Self-Eval, Golden, Snapshot, causal-chain, or global Gold Bank mutations were made by this phase.

## 13. Human Review Recommendation

Priority order:

1. **Q515**: human source-specific review required. Treat as `requires_review` semantically, while leaving exporter eligibility untouched until a replacement or repair phase is authorized.
2. **Q21/Q216**: keep Q216; replace or repair Q21 first when a valid Gold-A/B substitute exists.
3. **Option shuffle**: authorize a separate frontend/exporter subphase using the contract above.
4. **Replacement path**: to preserve 36 without Gold-C, run a PARTIAL promotion phase first. High-priority candidates previously identified include Q247, Q253, Q386, Q852, and Q44, but they are not Gold-A/B today and were not used in this phase.

Closure status against criteria:

- Q515: clearly marked for human review in this report.
- Q21/Q216: redundancy resolved as Q21 weaker, Q216 preferred; replacement blocked by no inactive Gold-A/B.
- Position bias: measured and option-shuffle contract documented.
- Active set size: remains 36.
- Exporter dry-run: 36 eligible, 0 validation errors.
- Tests: 1352 run, OK, 9 skipped.
- Governance: no unsafe flag changed or introduced.
