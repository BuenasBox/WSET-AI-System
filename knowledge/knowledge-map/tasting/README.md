# knowledge-map / tasting

## Purpose

Contains knowledge records related to the WSET Systematic Approach to Tasting
Wine® (SAT), covered in RA1 of the WSET Level 3 curriculum.

Tasting records encode the vocabulary, attribute ranges, assessment criteria,
and cause-and-effect links between wine components and their sensory expression.

## Schema

Tasting records follow a local schema (to be formalised). Key fields:
- `attribute_id`
- `attribute_name` (e.g. `acidity`, `tannin`, `body`)
- `sat_category` — `appearance` / `nose` / `palate` / `conclusions`
- `descriptors` — accepted vocabulary at each level (low / medium(-) / medium / medium(+) / high)
- `cause_links` — what winemaking or viticultural factors drive this attribute
- `distinction_notes` — what Distinction-level tasting notes add beyond the descriptor
- `common_errors`

## Naming convention

`sat_{attribute_slug}.json`  — e.g. `sat_acidity.json`, `sat_tannin.json`

## Usage

- Tutor Agent uses tasting records to coach SAT vocabulary and reasoning
- Examiner Agent may reference SAT attribute definitions from official-wset/sat/
  — NOT from this folder (these are pedagogical interpretations)

## Status

`ingestion_status: empty` — awaiting population.
