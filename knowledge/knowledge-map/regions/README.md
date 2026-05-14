# knowledge-map / regions

## Purpose

Contains structured knowledge records for wine regions covered in the WSET
Level 3 curriculum (RA2–RA4).

Region records encode climate, soil, key appellations, permitted varieties,
style parameters, wine laws, and principal producers — all at the precision
level required for WSET L3 Pass, Merit, and Distinction responses.

## Schema

Region records follow a local schema (to be formalised). Key fields:
- `region_id`
- `region_name`
- `country`
- `ra` — `RA2` / `RA3` / `RA4`
- `climate_type`
- `key_appellations`
- `permitted_varieties`
- `key_styles`
- `related_wine_laws`
- `exam_question_angles`
- `related_concepts`

## Naming convention

`{country_slug}_{region_slug}.json`  — e.g. `france_bordeaux.json`

## Status

`ingestion_status: empty` — awaiting population.
