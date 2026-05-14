# knowledge-map / concepts

## Purpose

Contains atomic concept records. A **concept** is the smallest independently
teachable unit of WSET L3 knowledge — for example "tartaric acid", "autolysis",
or "phenolic ripeness".

Concepts are the primary nodes in the knowledge graph. All relationships,
misconceptions, and causal chains reference concepts by their `concept_id`.

## Schema

Each file is a JSON object conforming to `schemas/concept.schema.json`.

## Naming convention

`{concept_slug}.json`  — e.g. `acidity.json`, `tannin_polymerisation.json`

## Key fields

- `tutor_allowed` — whether the Tutor Agent may draw on this concept
- `examiner_allowed` — whether the Examiner Agent may reference this concept
- `common_misconceptions` — links to `../misconceptions/`
- `cause_effect_links` — links to `../causal-chains/`

## Status

`ingestion_status: seeded` — initial examples present. Full population pending.
