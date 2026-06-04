# Open Response Lab Contract

Date: 2026-06-04

Status: private foundation only. Not active. Not public. No frontend.

## Purpose

The Open Response Lab is a private, training-only practice layer for WSET Level 3 open-response reasoning. Its first scope is RA1 formative practice using reviewed diagnostic open-response candidates.

The lab exists to help a learner notice concept coverage, missing concepts, weak causal links, and possible revision targets. It is not an assessment authority and must not be presented as WSET marking, examiner feedback, certification readiness, or official grading.

## Scope

Initial scope:

- Private RA1 open-response practice only.
- Deterministic session selection from an approved inactive pool.
- Deterministic formative feedback boundaries.
- No publication, deployment, public URL, dashboard exposure, or frontend activation.

Out of scope:

- Official WSET question publication.
- Examiner-style scoring.
- Pass/fail decisions.
- Certification readiness decisions.
- Open-response frontend.
- Public learner-facing activation.
- Tutor, Retrieval, Self-Eval, Golden, Snapshot, Dashboard, SBA frontend, or Open Response frontend changes.

## Governance

The lab inherits the project governance invariants:

```python
safe_for_examiner = False
examiner_scoring_allowed = False
uses_llm = False
uses_api = False
uses_embeddings = False
uses_vector_db = False
cloud_services_active = False
```

Additional lab-layer defaults:

```python
official_wset_question = False
training_item_only = True
public_frontend_active = False
open_response_lab_active = False
```

Any truthy violation must fail safe. No lab component may call external services, LLMs, APIs, embeddings, vector databases, cloud services, or hidden runtime systems.

## Active Pool Boundary

The initial private lab pool contains only candidates classified as `READY` or `READY_WITH_MINOR_GAPS` in Phase 4A.3.7.50.

Included source IDs:

```text
798, 799, 800, 801, 802, 803, 804, 805, 806, 808, 810, 811, 812, 813, 814, 815, 816, 817
```

Excluded source IDs:

```text
807, 809
```

IDs 807 and 809 remain excluded because Phase 4A.3.7.50 classified them as `NEEDS_REVIEW`.

## Session Selection

Session selection must be deterministic and reproducible.

Allowed inputs:

- `RA`
- `topic`
- `difficulty`
- `session_size`

Allowed session sizes:

- short: 3 questions
- standard: 5 questions
- long: 10 questions

Selection must not use randomness, LLMs, APIs, embeddings, vector databases, cloud services, or mutable learner-facing activation state.

## Feedback Allowed

The lab may provide only formative guidance:

- Concepts present.
- Concepts absent.
- Missing causal links.
- Suggestions for review.
- Orientative answer model.

The orientative answer model is a learning scaffold, not an official model answer and not an examiner key.

## Feedback Prohibited

The lab must not provide:

- Mark.
- Score.
- Percentage.
- Pass/fail result.
- WSET equivalence.
- Official grade.
- Examiner judgement.
- Certification-readiness claim.
- Any claim that feedback predicts an official WSET result.

## No Scoring, Grading, Or Examiner Authority

The lab must not contain official scoring, grading, pass/fail classification, percentage output, examiner authority, or equivalence to WSET assessment bands.

The only permitted result class is formative training guidance. The learner may be told what concepts or causal links appear to be present or absent, but not how many marks the answer would receive or whether it would pass.

## Activation Rule

This contract does not activate the Open Response Lab.

Activation requires a later explicit phase that changes only the intended private-lab layer after separate review. Until then, all candidates and lab sessions remain inactive and private.
