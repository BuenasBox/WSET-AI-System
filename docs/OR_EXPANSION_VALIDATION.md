# Open Response Expansion Batch 4 Validation

**Date:** 2026-06-15  
**Scope:** `OR_107`-`OR_138`, canonical bank, generated lab payload, Full
Simulation Part 2 contract, Y.3 coaching metadata, and governance.

## Validation Results

| Gate | Result |
|---|---|
| Batch size is 32 | PASS |
| IDs are contiguous `OR_107`-`OR_138` | PASS |
| Bank total is 138 | PASS |
| No duplicate IDs | PASS |
| No duplicate normalized question text | PASS |
| Required Batch 4 fields present | PASS |
| RA distribution is 6/12/0/8/6 | PASS |
| Eight verbs appear four times each | PASS |
| Causal-chain references resolve | PASS |
| Sweet-wine taxonomy follows official RA scope | PASS |
| Legacy RA5 sweet-production labels corrected | PASS |
| Governance flags remain false | PASS |
| Runtime adapter loads 138 nodes | PASS |
| Payload generation succeeds | PASS |
| Payload contains 138 items and 138 coaching records | PASS |
| Legacy IDs remain stable | PASS |
| Full Simulation four-item sampling succeeds | PASS |
| Y.3 feedback and causal metadata available | PASS |
| Recommend coaching definition available | PASS |

## Commands Executed

Focused Batch 4 and integration gate:

```text
python -m unittest tests.test_or_batch_04
  tests.test_or_batch_04_integration
  tests.test_open_response_session_engine
  tests.test_open_response_lab_runtime_mvp
  tests.test_open_response_evaluator_p2
  tests.test_open_response_p2_3_integration
  tests.test_open_response_p2_4_expansion -v
```

Result: **109/109 passed**.

Historical append-only batch gates:

```text
$env:PYTHONUTF8='1'
python tests/test_or_batch_01.py
python tests/test_or_batch_02.py
python tests/test_or_batch_03.py
```

Result: **PASS/PASS/PASS** after replacing hard-coded final-bank totals with
append-only minimums and bounding each test to its historical ID range.

Broader Open Response discovery:

```text
python -m unittest discover -s tests -p 'test_*open_response*.py' -v
```

Result: **159 passed, 5 failed**. The failures are outside the Batch 4 bank and
runtime path:

- older grounding artifacts expect 26 normalized candidates while current
  master-bank derivation produces 37
- older suitability assertions expect 27 candidates and no review pool while
  current derivation produces 38 candidates and 2 review records
- the persisted suitability report no longer matches the current generated
  master-bank report

Batch 4 does not modify the master bank, normalized grounding candidates, or
suitability report. The focused 109-test integration gate covering the files
changed by this sprint is green.

Payload generation:

```text
from tools.question_generation.open_response_lab_runtime import
write_lab_payload_js
write_lab_payload_js()
```

Result: generated `frontend/open-response-lab/lab_payload.js` successfully.

## Verified Counts

```text
Canonical bank: 138
Payload items: 138
Evaluation/coaching records: 138
Batch 4: 32
Batch RA distribution: RA1=6, RA2=12, RA4=8, RA5=6
Final RA distribution: RA1=42, RA2=41, RA3=15, RA4=23, RA5=17
```

Full Simulation Part 2 deterministic sample:

```text
OR_113  RA2
OR_114  RA2
OR_115  RA2
OR_125  RA4
```

## Governance

The batch and generated payload maintain:

```text
safe_for_examiner=false
examiner_scoring_allowed=false
uses_llm=false
uses_api=false
uses_embeddings=false
uses_vector_db=false
cloud_services_active=false
```

No pass, merit, distinction, official scoring, examiner-authority, or outcome
prediction behavior was introduced.

## Boundary

The local canonical development payload was regenerated. The separate
production dashboard repository and operational deployment were not modified or
published by this sprint.
