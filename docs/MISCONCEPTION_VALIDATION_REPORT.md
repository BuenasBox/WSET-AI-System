# Misconception Validation Report

**Date:** 2026-06-15
**Scope:** Corrected M.1-M.6 implementation

## Misconception Gates

| Validation | Result |
|---|---|
| 20 legacy nodes load without migration | PASS |
| Legacy nodes remain unmodified by normalization | PASS |
| All 20 canonical statements detect through the adapter | PASS |
| Candidate-ID constrained detection | PASS |
| Explicit-ID backward compatibility | PASS |
| Generic weakness does not create direct evidence | PASS |
| SBA distractor inference | PASS |
| Open Response direct evidence | PASS |
| Missing causal chain does not imply misconception | PASS |
| SAT text evidence | PASS |
| Low/medium/high evidence accumulation | PASS |
| Correction reduces active confidence | PASS |
| Duplicate evidence is idempotent | PASS |
| Recommendation generation for all 20 nodes | PASS |
| Coaching generation for all 20 nodes | PASS |
| Profile rendering without IDs or percentages | PASS |
| Simulation-scoped evidence trace | PASS |
| Governance flags remain false | PASS |

## Commands Executed

Backend focused gate:

```text
python -m unittest tests.test_misconception_adapter
  tests.test_learning_event_runtime_integration
  tests.test_runtime_consumers
  tests.test_adaptive_loop_wireup -v
```

Result: 146/146 passed after correcting the diagnostic assertion.

LES rollback regression:

```text
python -m unittest
  tests.test_learning_event_runtime.LesAdapterTests.test_les_change_set_reverses_update
  tests.test_misconception_adapter
  tests.test_learning_event_runtime_integration -v
```

Result: 62/62 passed.

Additional backend chunks:

| Chunk | Result |
|---|---|
| `test_[q-r]*.py` | 211 passed, 2 skipped |
| SAT modules | 215 passed |
| score/self/session/strategic/structured modules | 278 passed |
| static modules | 93 passed |
| SBA session composer | 11 passed |
| `test_[t-z]*.py` | 104 passed |

Dashboard:

```text
node tests/test_misconception_visibility.js
node --test tests/full-simulation-gate.test.js tests/test_or_integration_106.js
node --test <all *.test.js files>
```

Results:

- misconception visibility: PASS
- Full Simulation gate plus OR integration: 55/55 passed
- complete `*.test.js` set: 160 passed, 1 pre-existing failure

## Broader Baseline Failures

The complete backend discovery could not be reported as green:

- stale master-bank assertions expect 589 SBA items and 27 OR candidates;
  current data has 578 SBA items and 38 OR candidates
- older Open Response expansion and suitability artifacts expect the prior
  26/27-item state
- `test_sba_enrichment_batch3_botrytis.py` and related derivation modules exceed
  five minutes during setup, causing monolithic discovery timeouts

These failures do not touch misconception closure files.

The complete dashboard `*.test.js` set has one pre-existing failure:

- `student-profile.test.js` expects no `learner_intelligence.js` import, while
  the current Profile page already imports it for Y.2/Y.3 panels

## Governance

The implemented misconception path maintains:

```text
safe_for_examiner=false
examiner_scoring_allowed=false
uses_llm=false
uses_embeddings=false
uses_vector_db=false
cloud_services_active=false
```

No pass, merit, distinction, readiness, examiner authority, or probability is
introduced in the new learner-facing misconception views.

## Conclusion

All misconception-specific validation gates pass. Broader suite limitations are
documented and are not hidden as successful runs.
