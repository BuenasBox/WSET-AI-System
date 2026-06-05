# Phase 4A.3.7.52 Open Response Lab Runtime MVP

Date: 2026-06-04

Status: runtime MVP created. Private only. Inactive. Not published. Not connected to Dashboard, Tutor, Retrieval, Self-Eval, Golden, snapshots, or SBA frontend.

## Scope

Created a local Open Response Lab runtime under:

```text
frontend/open-response-lab/
```

The runtime supports:

- short session: 3 questions
- standard session: 5 questions
- long session: 10 questions
- free-text answer capture
- local-only answer persistence through browser localStorage
- formative feedback display
- next question, finish session, and restart session actions

## Engine And Pipeline Use

The source-of-truth runtime adapter is:

```text
tools/question_generation/open_response_lab_runtime.py
```

It builds the static lab payload from the existing Open Response Session Engine:

```text
tools/question_generation/open_response_session_engine.py
```

It also exposes `build_formative_feedback()`, which delegates answer evaluation to the existing Open Response Pipeline:

```text
tools/question_generation/open_response_pipeline.py
```

The static browser runtime uses the generated payload:

```text
frontend/open-response-lab/lab_payload.js
```

No backend is introduced. No external service is called.

## Question Display Boundary

The UI shows only:

- stem
- topic
- RA

The render item payload exposes only:

```text
item_id
source_question_id
stem
topic
RA
```

The UI does not render expected concepts, feedback rubric, grounding evidence, or causal-chain metadata before answer review.

## Feedback Boundary

The UI displays only formative categories:

- conceptos detectados
- conceptos ausentes
- razonamiento causal faltante
- sugerencias de mejora

The runtime does not display official result language, marks, percentages, pass/fail, WSET equivalence, or examiner judgement.

## Governance

Verified runtime defaults:

```python
safe_for_examiner = False
examiner_scoring_allowed = False
uses_llm = False
uses_api = False
uses_embeddings = False
uses_vector_db = False
cloud_services_active = False
public_frontend_active = False
open_response_lab_active = False
```

The lab remains inactive and private.

## Tests

Added:

```text
tests/test_open_response_lab_runtime_mvp.py
```

Coverage includes:

- session selection matches the existing Session Engine
- answer submission uses a textarea and localStorage only
- feedback sections render only allowed formative categories
- formative feedback wrapper delegates to the existing pipeline shape
- governance flags remain false
- session completion controls are present
- no Dashboard integration
- no backend, analytics, or external API references

## Risks

- The browser-side evaluator mirrors the deterministic formative logic for local static use. The Python adapter remains the source of truth for direct calls into the existing pipeline.
- Hidden evaluation metadata is present in the local payload so a static no-backend page can evaluate arbitrary answers. It is not rendered as question-facing content.
- The pool is still RA1-only and inactive; this must not be presented as full WSET Level 3 coverage or public learner activation.
- Future activation would need a separate review of UI copy, metadata exposure, accessibility, and payload boundaries.
