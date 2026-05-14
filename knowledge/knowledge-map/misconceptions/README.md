# knowledge-map / misconceptions

## Purpose

Contains misconception records — documented incorrect beliefs that learners
frequently hold about WSET L3 concepts.

Misconceptions are distinct from simply wrong answers. They represent systematic
cognitive errors: patterns of misunderstanding that repeat across learners and
that, if uncorrected, cause reliable exam failure.

## Schema

Each file is a JSON object conforming to `schemas/misconception.schema.json`.

## Naming convention

`mc_{concept_slug}_{n}.json`  — e.g. `mc_tannin_01.json`

## Key fields

- `severity` — `low` / `medium` / `high` / `critical`
- `frequency` — estimated prevalence among learners
- `distinction_relevance` — whether correcting this is required for Distinction

## Usage

- Tutor Agent uses misconception records to proactively correct errors
- Orchestrator flags recurring misconceptions in a learner's session history
- Misconceptions must not influence Examiner Agent scoring criteria

## Status

`ingestion_status: seeded` — examples present for core concepts.
