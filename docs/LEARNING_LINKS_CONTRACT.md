# Learning Links Contract

> **STATUS: CANONICAL**
>
> **LAST RECONCILED: 2026-06-06**

## Purpose

`learning_links` connects a Master Bank item to already governed cognitive
objects. It allows an observed answer to target misconception repair or
causal-chain reinforcement without inferring IDs from prose.

The contract is additive. It does not change question eligibility, answer keys,
publication state, difficulty, RA classification, or Open Response suitability.

## Current Coverage

At reconciliation time:

```text
Master Bank records: 616
Records with learning_links: 0
```

Topic, RA, difficulty, and exposure adaptation therefore work immediately.
Misconception and causal-chain item targeting becomes active only for records
that later receive reviewed links.

## Shape

```json
{
  "learning_links": {
    "causal_chain_id": "CC_EXAMPLE",
    "options": {
      "A": {
        "diagnostic_role": "misconception",
        "misconception_id": "MC_EXAMPLE",
        "causal_chain_id": "CC_EXAMPLE"
      }
    }
  }
}
```

`causal_chain_id` at the top level describes the principal chain tested by the
item. Option-level links describe the diagnostic meaning of selecting a
specific option.

## Rules

- Every referenced ID must already exist in a governed repository artifact.
- Links must be based on question semantics and distractor intent, not lexical
  similarity alone.
- The correct option must not be assigned a misconception.
- Missing links remain missing; runtimes must not invent or guess IDs.
- Unknown IDs must not influence adaptive ranking.
- Duplicate option links must resolve to the same governed object.
- Adding links must not alter the question stem, options, answer key,
  eligibility, publication state, or source lineage.
- Open Response records may use the top-level causal-chain link only when a
  separate Open Response phase authorizes consumption.

## Runtime Consumption

The Learning Event Runtime reads:

- top-level `causal_chain_id`;
- selected-option `diagnostic_role`;
- selected-option `misconception_id`;
- selected-option `causal_chain_id`.

The adaptive Master Bank Composer may prioritize linked SBA items when
`next_session_signals` contains a matching misconception or causal-chain ID.
This is ranking influence only. It does not bypass eligibility, RA filters,
mode constraints, topic caps, exposure avoidance, or governance.

## Review Requirements

Future population work must provide:

- source item ID;
- option letter;
- proposed governed ID;
- evidence for the semantic relationship;
- reviewer decision;
- deterministic validation for referenced IDs;
- before/after confirmation that eligibility counts and answer content are
  unchanged.

Bulk automatic link generation is not authorized by this contract.
