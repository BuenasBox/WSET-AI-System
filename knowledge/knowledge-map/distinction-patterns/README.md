# knowledge-map / distinction-patterns

## Purpose

Contains patterns of reasoning and knowledge depth that characterise
Distinction-level WSET L3 responses.

A **distinction pattern** is not just a correct answer — it is a documented
cognitive or structural quality that separates a Merit or Pass response from a
Distinction response for a given topic or concept.

## Schema

Distinction patterns are stored as structured JSON. Fields include:
- `topic_id` — the topic this pattern applies to
- `pattern_type` — `causal_depth` / `precision` / `exception_handling` / `integration`
- `pass_response_example` — what a Pass-level answer looks like
- `distinction_response_example` — what a Distinction-level answer adds
- `key_differentiator` — the single most important quality upgrade

## Naming convention

`dp_{topic_slug}.json`  — e.g. `dp_acidity_in_cool_climates.json`

## Usage

- Tutor Agent uses these patterns to coach learners toward Distinction
- Examiner Agent must NOT use these patterns for scoring (pedagogical content)
- Orchestrator uses distinction patterns to generate targeted study prompts

## Status

`ingestion_status: empty` — awaiting expert curation.
