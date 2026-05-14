# knowledge-map / grape-varieties

## Purpose

Contains structured knowledge records for grape varieties covered in the WSET
Level 3 curriculum.

Each grape variety record encodes its key characteristics, typical style
parameters, principal regions, climate preferences, and common exam question
angles.

## Schema

Grape variety records follow a local schema (to be formalised). Key fields:
- `variety_id`
- `variety_name` (plus synonyms)
- `colour` — `red` / `white` / `rosé`
- `key_characteristics` — acidity, tannin, body, aroma profile
- `climate_preference` — `cool` / `moderate` / `warm` / `hot`
- `principal_regions`
- `exam_question_angles`
- `common_misconceptions`
- `related_concepts`

## Naming convention

`{variety_slug}.json`  — e.g. `chardonnay.json`, `cabernet_sauvignon.json`

## Status

`ingestion_status: empty` — awaiting population. Schema to be finalised.
