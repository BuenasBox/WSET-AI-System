# knowledge-map / relationships

## Purpose

Contains directed relationship records between concepts. Relationships are the
edges of the knowledge graph. They encode how concepts interact causally,
structurally, or pedagogically.

A relationship record always has a `source_concept`, a `target_concept`, and a
typed `relationship_type` (e.g. `causes`, `increases`, `contrasts_with`).

## Schema

Each file is a JSON object conforming to `schemas/relationship.schema.json`.

## Naming convention

`{source_slug}__{relationship_type}__{target_slug}.json`
e.g. `cool_climate__increases__acidity.json`

## Relationship types (partial list)

`causes` · `influences` · `increases` · `decreases` · `requires`
`contrasts_with` · `often_confused_with` · `prerequisite_for`
`improves` · `reduces`

## Usage

The Tutor Agent uses relationships to construct causal explanations.
The Orchestrator uses relationships to detect weak-area clusters.
Relationships must never be used by the Examiner Agent for scoring.

## Status

`ingestion_status: seeded` — initial examples present.
