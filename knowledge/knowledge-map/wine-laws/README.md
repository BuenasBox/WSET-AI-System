# knowledge-map / wine-laws

## Purpose

Contains structured records for wine classification systems and appellation laws
covered in the WSET Level 3 curriculum (primarily RA2 and RA5).

Wine law records encode the regulatory hierarchy, quality tiers, labelling
requirements, and their relationship to style and quality expectations.

## Schema

Wine law records follow a local schema (to be formalised). Key fields:
- `law_id`
- `law_name`
- `country` / `region`
- `ra` — `RA2` / `RA5`
- `classification_tiers` — ordered list from base to highest
- `key_requirements` — yield limits, variety restrictions, ageing rules
- `labelling_implications`
- `related_regions`
- `exam_question_angles`

## Naming convention

`{country_slug}_{law_slug}.json`  — e.g. `france_aoc_system.json`

## Status

`ingestion_status: empty` — awaiting population.
