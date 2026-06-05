# Phase 4A.3.7.51 Open Response Lab Foundation

Date: 2026-06-04

Status: foundation created. Private only. Inactive. No frontend. No publication.

## Contract

Created `docs/OPEN_RESPONSE_LAB_CONTRACT.md`.

The contract defines the Open Response Lab as a private RA1 formative practice layer. It explicitly prohibits official scoring, grading, pass/fail, WSET equivalence, examiner judgement, certification-readiness claims, public activation, frontend exposure, and external runtime services.

Governance remains:

```python
safe_for_examiner = False
examiner_scoring_allowed = False
uses_llm = False
uses_api = False
uses_embeddings = False
uses_vector_db = False
cloud_services_active = False
```

Lab-layer defaults are also inactive:

```python
official_wset_question = False
training_item_only = True
public_frontend_active = False
open_response_lab_active = False
```

## Engine

Created `tools/question_generation/open_response_session_engine.py`.

The engine is isolated from Tutor, Retrieval, Self-Eval, Golden baselines, snapshots, Dashboard, SBA frontend, and Open Response frontend. It performs deterministic session selection only.

Supported inputs:

- `ra`
- `topic`
- `difficulty`
- `session_size`

Supported outputs:

- deterministic source question ID list
- inactive session descriptor
- pool manifest
- feedback boundary metadata
- safe governance flags

The engine does not evaluate answers, activate candidates, publish files, write frontend payloads, or call any external runtime.

## Active Pool

The initial private lab pool is the Phase 4A.3.7.50 `READY` plus `READY_WITH_MINOR_GAPS` set, excluding `NEEDS_REVIEW` items 807 and 809.

Included IDs:

```text
798, 799, 800, 801, 802, 803, 804, 805, 806, 808, 810, 811, 812, 813, 814, 815, 816, 817
```

READY:

```text
800, 801, 802, 804, 805, 806, 812, 813, 814, 815
```

READY_WITH_MINOR_GAPS:

```text
798, 799, 803, 808, 810, 811, 816, 817
```

Excluded:

```text
807, 809
```

## Session Sizes

The engine supports:

- short: 3 questions
- standard: 5 questions
- long: 10 questions

Selection is source-order deterministic after filtering. Redundant pairs `804/817` and `810/812` are deferred when alternatives exist, but no item is permanently removed from the pool.

## Feedback Limits

Allowed feedback categories:

- present concepts
- missing concepts
- missing causal links
- revision suggestions
- orientative answer model

Prohibited feedback categories:

- mark
- score
- percentage
- pass/fail
- WSET equivalence
- examiner judgement
- official grade

## Risks

- The pool is RA1-only and must not imply full WSET Level 3 coverage.
- Several `READY_WITH_MINOR_GAPS` items need careful wording in future feedback layers.
- Concept-presence feedback can still reward term listing unless future rubric work distinguishes causal explanation from vocabulary recall.
- Price, quality, and premium language must remain conditional and formative.
- The lab must remain private until a separate activation phase reviews UI copy, payload boundaries, and feedback rendering.

## Tests

Added `tests/test_open_response_session_engine.py`.

Coverage includes:

- deterministic selection
- exclusion of 807 and 809
- safe governance flags
- reproducibility
- short, standard, and long session sizes
- RA, topic, and difficulty filters
- feedback allowed/prohibited boundaries
- no mutation of input candidates

## Recommended Next Phase

Phase 4A.3.7.52 should add a private dry-run fixture for one inactive session and define question-specific formative feedback expectations for the `READY_WITH_MINOR_GAPS` items. It should still avoid frontend work, publication, scoring, grading, pass/fail, WSET equivalence, and examiner authority.
