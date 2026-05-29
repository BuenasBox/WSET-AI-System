# Phase 3A.8 — Planner Causal-Chain Activation Readiness Review

Date: 2026-05-29

## Recommendation

**Keep experimental behind gates; do not activate globally.**

`ENABLE_PLANNER_QUERY_EXPANSION` should remain `False`.
`ENABLE_PLANNER_CAUSAL_CHAIN_INJECTION` should remain `False`.

The causal-chain hint path is now safer after the Phase 3A.7 semantic
compatibility gate, but the evidence does not yet justify default runtime
activation. The main remaining question is incremental value: once retrieval
requires semantic compatibility, many useful cases are already matched
organically by the clean query.

## Evidence Reviewed

### Phase 3A.4 — Controlled A/B Retrieval Comparison

Phase 3A.4 created a test-only A/B harness:

- Baseline: planner expansion OFF, causal-chain injection OFF.
- Experimental: both gates enabled inside test scope only.
- Captured top result IDs, rank deltas, hint IDs, causal signal visibility,
  and governance safety.

Observed result:

- Valid hints could be parsed and exposed.
- Injected hints could become visible in native `matched_causal_chains`.
- Causal-chain signal was inspectable.
- Ranking did not move in the controlled positive fixtures.
- Defaults remained OFF.

Interpretation:

The path was observable and deterministic, but Phase 3A.4 did not prove useful
ranking improvement.

### Phase 3A.5 — Score Delta Measurement

Phase 3A.5 measured score impact rather than ranking impact.

Positive fixtures showed:

- `score_delta` approximately `+0.18`.
- `causal_score_delta` approximately `+0.08`.
- `rank_delta = 0`.

Negative fixtures in the final suite stayed bounded.

Important calibration finding:

- At least one adversarial wrong-hint case promoted an incorrect causal-chain
  chunk, demonstrating that raw injection was not safe.

Interpretation:

Planner hints could materially change scores, even when ranking did not move.
That score movement was large enough to become dangerous under adversarial
conditions.

### Phase 3A.6 — Adversarial Negative Expansion

Phase 3A.6 deliberately tried to break the mechanism.

Observed failures before semantic compatibility:

- Wrong hints could add approximately `+0.18` total score.
- Wrong hints could add approximately `+0.08` causal score.
- Wrong chunks could move to rank 1.
- SAT/quality/balance-style hints could create material score gains in
  unrelated contexts.
- Contradictory hints and maximum-hint stress produced near-failures.

Interpretation:

Phase 3A.6 established clear activation blockers. Planner causal-chain focus
cannot be treated as sufficient evidence. Retrieval must verify planner hints
locally before allowing any scoring influence.

### Phase 3A.7 — Semantic Compatibility Gate

Phase 3A.7 added a fail-closed semantic compatibility gate:

- Retrieval uses the clean query after hint-token parsing.
- Candidate chain metadata is inspected deterministically.
- Generic terms are excluded.
- A hinted chain is injected only when the clean query shares enough meaningful
  chain terms.
- No LLM, embeddings, vector DB, cloud loop, or new scoring weights are used.

Observed after gating:

- Former adversarial failures were mitigated in the test harness.
- Wrong-hint `score_delta` dropped to `0.0`.
- Wrong-hint `causal_score_delta` dropped to `0.0`.
- Wrong-hint `rank_delta` dropped to `0`.
- Compatible positive fixtures still showed causal signal.
- Defaults remained OFF.

Interpretation:

The gate substantially reduces known false positives. It also changes the value
proposition: when the query contains enough meaningful overlap to pass the
gate, retrieval often already has enough evidence to match the causal chain
organically.

## Activation Questions

### 1. What value does causal-chain hint injection add after semantic compatibility gating?

The remaining value appears narrow.

After compatibility gating, planner hints can still help when:

- the clean query contains enough chain-specific evidence to pass the gate;
- organic matching fails due to wording, casing, or metadata gaps;
- the hinted chain has terms that retrieval can use for `causal_chain_match`.

However, the current evidence suggests that many compatible positives are
already matched organically. The hint path may be more useful as an explicit
audit signal than as a ranking influence.

### 2. Did adversarial risk remain mitigated?

Yes for the known Phase 3A.6 adversarial fixtures.

The semantic gate mitigated the observed failures:

- semantic opposition;
- near-neighbor confusion;
- SAT contamination;
- keyword overlap traps;
- maximum hint stress;
- contradictory hints.

This is not proof of general safety. It is evidence that the known blockers
were addressed for the current deterministic fixtures.

### 3. Do compatible hints still provide measurable incremental value?

Not enough evidence yet.

Compatible hints still preserve causal-chain visibility, but after the gate the
incremental score value is often no longer separable from organic matching. A
future activation review should measure cases where:

- organic retrieval misses a chain;
- the compatibility gate passes;
- injection improves recall without promoting unrelated chunks.

### 4. Are many positives already matched organically?

Yes.

Once queries include enough meaningful terms to pass semantic compatibility,
they frequently also contain enough information for organic causal-chain
matching. That reduces the practical upside of activating injection globally.

### 5. Should `ENABLE_PLANNER_QUERY_EXPANSION` remain `False`?

Yes.

The query expansion gate is the upstream source of planner hint tokens. It
should remain OFF until activation criteria are met and reviewed.

### 6. Should `ENABLE_PLANNER_CAUSAL_CHAIN_INJECTION` remain `False`?

Yes.

The injection path should remain OFF. The compatibility gate is a necessary
safety layer, not a sufficient reason for activation.

### 7. What exact criteria would justify future activation?

Future activation would require all of the following:

1. A larger fixture suite with representative WSET3 learner queries.
2. Clear positive incremental value after compatibility gating:
   - measurable score or recall improvement in cases organic retrieval misses;
   - no material score gain for wrong hints.
3. Adversarial negatives remain bounded:
   - wrong-hint `score_delta < 0.05`;
   - wrong-hint `causal_score_delta = 0.0` or demonstrably negligible;
   - no wrong chunk promoted above the relevant target.
4. Contradictory and max-hint scenarios remain deterministic and bounded.
5. Snapshot suite remains unchanged with defaults OFF.
6. Governance fields remain absent.
7. No scoring weights are changed to compensate for hint behavior.
8. Activation plan includes rollback instructions and an explicit audit report.

### 8. What tests must pass before activation?

At minimum:

```bash
python -m unittest tests.test_planner_query_expansion_gate -v
python -m unittest tests.test_retrieval_planner_query_hints -v
python -m unittest tests.test_retrieval_planner_causal_chain_injection -v
python -m unittest tests.test_retrieval_planner_ab_comparison -v
python -m unittest tests.test_retrieval_planner_score_delta -v
python -m unittest tests.test_retrieval_planner_adversarial_negatives -v
python -m unittest tests.test_retrieval_planner_semantic_compatibility -v
python -m unittest discover -s tests -v
python -m unittest tests.test_tutor_snapshot_regression -v
```

Before any default activation, an additional activation-specific test suite
should run with the proposed flags enabled in test scope and verify:

- no snapshot drift for default OFF behavior;
- bounded deltas for wrong hints;
- useful deltas for organic-miss compatible positives;
- no ranking corruption;
- no governance field introduction;
- no full causal-chain prose injection.

## Decision

Do not activate now.

Keep the influence path experimental and gated:

- `ENABLE_PLANNER_QUERY_EXPANSION = False`
- `ENABLE_PLANNER_CAUSAL_CHAIN_INJECTION = False`

Proceed only to an activation readiness review after additional evidence shows
that the gated hint path adds value beyond organic retrieval without reopening
the adversarial risks discovered in Phase 3A.6.
