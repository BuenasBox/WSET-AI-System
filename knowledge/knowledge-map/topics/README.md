# knowledge-map / topics

## Purpose

Contains structured topic records for the WSET Level 3 curriculum.

A **topic** is a curriculum-level grouping of related knowledge — for example
"Sparkling Wine Production", "Bordeaux", or "Wine and Food Pairing". Topics form
the primary navigation layer of the knowledge map.

## Schema

Each file is a JSON object conforming to `schemas/topic.schema.json`.

## Naming convention

`{ra}_{slug}.json`  — e.g. `ra1_malolactic_conversion.json`, `ra2_bordeaux.json`

## Relationships

- Topics contain one or more **concepts** (see `../concepts/`)
- Topics may depend on **prerequisite topics** (declared in the schema)
- Topics are linked to **causal chains** (see `../causal-chains/`)

## Status

`ingestion_status: empty` — awaiting population. See manifest for roadmap.
