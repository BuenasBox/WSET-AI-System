# knowledge-map / causal-chains

## Purpose

Contains causal chain records — structured, multi-step cause-and-effect sequences
that explain how one wine factor leads to another through traceable intermediate
steps.

Causal reasoning is central to WSET L3 Distinction performance. Examiners reward
answers that do not merely state facts but explain *why* and *how*.

## Schema

Each file is a JSON object conforming to `schemas/causal_chain.schema.json`.

## Naming convention

`cc_{starting_factor_slug}.json`  — e.g. `cc_cool_climate.json`

## Example structure

```
cool_climate
  → slower ripening
  → higher malic acid retained
  → lower sugar at harvest
  → lower potential alcohol
  → higher natural acidity in finished wine
```

## Usage

- Tutor Agent uses causal chains to construct step-by-step explanations
- Weak-area tracker identifies which steps in a chain a learner misses
- Causal chains support adaptive questioning (ask about step N if N-1 is mastered)

## Status

`ingestion_status: seeded` — initial chains present for core concepts.
