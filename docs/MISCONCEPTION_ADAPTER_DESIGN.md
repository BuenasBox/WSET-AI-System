# Misconception Adapter Design

**Date:** 2026-06-15  
**Decision:** Normalize existing misconception nodes at runtime.

## Constraints

- Keep all 20 node schemas unchanged.
- Do not create a parallel misconception schema or catalog.
- Keep existing IDs and Y.2/Y.3 consumer contracts working.
- Use deterministic local logic only.
- Treat confidence as evidence frequency, never probability or prediction.

## Adapter Boundary

`tools/learner_model/misconception_adapter.py` will load nodes through the
existing pre-pass loader and return a derived view. The view may contain:

- source identity and original pedagogical fields
- normalized detection phrases
- weakness relationships from related topics and concepts
- recommendation targets from existing remediation lookup and related topics
- coaching fields derived verbatim or by fixed framing from source fields
- evidence count, session count, source types, and confidence label

The adapter must not write node files or mutate caller-provided dictionaries.

## Evidence Contract

Each accepted event records:

- `misconception_id`
- `source_type`: `sba`, `open_response`, `sat`, `weakness_profile`, or `tutor`
- `session_id`
- optional `item_id`
- `timestamp`
- `outcome`: `observed` or `corrected`
- matched source phrases when text detection is used

Explicit node IDs remain valid for backward compatibility. Text inference is
used only when direct misconception wording or a node detection signal meets
the existing deterministic threshold. Generic weakness topics cannot create a
hit without an explicit misconception trend ID.

## Confidence Labels

- `low`: one unresolved observed event
- `medium`: two unresolved observed events
- `high`: three or more unresolved observed events across at least two sessions

A corrected event records improvement evidence and resolves the active insight
without deleting its history.

## Consumer Views

The adapter supplies:

- detection result for SBA, Open Response, SAT, and explicit weakness events
- LES evidence summary
- adaptive recommendation target
- formative coaching:
  - why it matters
  - what is being confused
  - triggering evidence
  - what to practice next
  - what improvement evidence reduces confidence
- student presentation model without technical IDs
- simulation-scoped model filtered by `session_id`

## Compatibility

Existing functions such as `process_sba_outcome`, pre-pass detection, adaptive
signal consumption, and WWJ remediation remain callable. New behavior is
introduced through adapters and additive runtime fields. Legacy nodes must
continue to load byte-for-byte and old callers that provide `mc_id` must retain
their previous signals.
