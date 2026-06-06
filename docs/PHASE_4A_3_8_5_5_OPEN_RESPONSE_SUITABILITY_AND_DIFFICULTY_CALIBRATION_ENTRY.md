# Phase 4A.3.8.5.5 - Open Response Suitability and Difficulty Calibration Entry

## Status

Implemented as a shadow classification layer.

This phase does not activate new Open Response questions, modify the Master
Bank, alter the public 36-item SBA lab, change Open Response Runtime, or assign
official WSET marks or grade equivalence.

## Purpose

The complete Master Bank must not be divided into SBA and Open Response using
an arbitrary numeric target. Suitability is derived from cognitive demand:

- explanation;
- cause, mechanism and effect;
- comparison;
- justification;
- inability to resolve the learning task through option recognition alone.

The result becomes an input to Difficulty Calibration. It is not itself a
difficulty label.

## Implementation

`tools/question_generation/open_response_suitability.py` classifies all 616
canonical records into:

| Classification | Meaning |
|---|---|
| `open_response_candidate` | Strong suitability evidence or existing approved Open Response review |
| `human_review_required` | Plausible explanatory demand, but insufficient metadata or answer boundary |
| `sba_only` | Recognition is sufficient under current evidence |
| `inactive` | Master Bank eligibility prevents learner-facing use |

The deterministic artifact is:

`knowledge/question-bank/open_response/suitability/master_bank_open_response_suitability.json`

Each record contains:

```json
{
  "open_response_candidate": false,
  "sba_only": false,
  "human_review_required": true,
  "signals": {
    "requires_explanation": true,
    "requires_causal_chain": false,
    "requires_comparison": false,
    "requires_justification": false,
    "recognition_only_sufficient": false,
    "recognition_framing_detected": false,
    "answer_boundary_support": false
  },
  "confidence": "low",
  "evidence": [],
  "review_status": "shadow_classified",
  "activation_status": "inactive"
}
```

`quota_target` is explicitly `null`. The validator rejects a fixed quota.

## Shadow Results

| Classification | Count |
|---|---:|
| `open_response_candidate` | 21 |
| `human_review_required` | 68 |
| `sba_only` | 503 |
| `inactive` | 24 |
| Total | 616 |

The 21 strong candidates consist of:

- 20 existing `approved_open_response` records;
- 1 newly discovered SBA-derived candidate: source question `14`.

Q14 asks for the principal effect of mechanical harvesting and carries the
causal metadata:

```text
mechanical harvesting -> berry breakage -> aromatic freshness
```

It therefore has explanation demand, causal support and a usable response
boundary. Its RA metadata remains `unknown`, so it is suitable for the future
calibration set but is not runtime-ready.

The 68 review records contain potentially useful prompts such as effects,
comparisons and justifications, but their current metadata is too sparse for
automatic promotion. They require human confirmation of:

1. whether the prompt can stand without options;
2. the expected concept boundary;
3. the causal or comparative structure;
4. RA and topic metadata;
5. whether the resulting answer can be interpreted deterministically.

## Difficulty Calibration Integration

The next phase must preserve three separate axes.

### 1. Item Difficulty

Internal complexity of the task:

- `easy`;
- `intermediate`;
- `advanced`.

This axis is used by Quick Practice, Full Diagnostic, RA Focus and future
adaptive composition.

### 2. Response Depth Target

What cognition the item asks the learner to demonstrate:

- `recall`;
- `explanation`;
- `causal_reasoning`;
- `comparative_justification`;
- `integrated_evaluation`.

The suitability signals from this phase seed this axis.

### 3. Aspirational Response Standard

How complete and well-structured a learner response is:

- concept coverage;
- factual precision;
- cause-mechanism-effect clarity;
- comparison quality;
- justification quality;
- balance and conclusion;
- appropriate WSET register.

The internal value may be named `distinction_oriented`, but it must remain:

- pedagogical and aspirational;
- non-authoritative;
- non-predictive;
- without marks, percentage, pass/fail or official grade equivalence.

It may guide the learner toward the characteristics of a maximally complete
response. It may not claim that WSET would award a Distinction.

## Proposed Calibration Record

```json
{
  "master_item_id": "wset3_14",
  "item_difficulty": {
    "level": "intermediate",
    "confidence": "pending",
    "dimension_scores": {}
  },
  "response_depth_target": "causal_reasoning",
  "open_response_suitability": {
    "classification": "open_response_candidate",
    "confidence": "high"
  },
  "aspirational_response_standard": {
    "profile": "distinction_oriented",
    "official_grade_prediction": false
  },
  "review_status": "calibration_pending"
}
```

## Activation Order

1. Use the 21 strong candidates plus a stratified sample from the 68 review
   records to build the human Gold Calibration Set.
2. Calibrate `item_difficulty` independently from response format.
3. Calibrate `response_depth_target` using this phase's signals.
4. Define response-quality dimensions for Open Response interpretation.
5. Run all 616 records in shadow mode.
6. Review all low-confidence records, public-lab records and proposed advanced
   records.
7. Expose metrics to Dashboard data only.
8. Enable private composers behind a feature gate.
9. Enable future adaptive selection last.

The existing `difficulty` field remains unchanged until the new calibration
artifact is reviewed and versioned.

## Governance

All records remain inactive and enforce:

```json
{
  "safe_for_examiner": false,
  "examiner_scoring_allowed": false,
  "uses_llm": false,
  "uses_api": false,
  "uses_embeddings": false,
  "uses_vector_db": false,
  "cloud_services_active": false
}
```

No runtime, frontend, deployment, Tutor, Retrieval, golden baseline or snapshot
change is part of this phase.

## Verification

```powershell
python -m unittest discover -s tests -v
python -m tools.question_generation.export_static_demo_questions --dry-run
$env:RUN_SLOW_TESTS=1; python -m unittest tests.test_golden_self_eval -v
```

Results:

- full suite: 1536 tests, 9 skipped, 0 failures;
- suitability tests: 14/14 OK;
- SBA export: 36 eligible items, 0 validation errors;
- Slow Golden: 7/7 OK;
- Tutor snapshots: unchanged.
