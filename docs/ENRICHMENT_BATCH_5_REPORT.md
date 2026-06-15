# SBA Enrichment Batch 5 Report

## Result

- Previous enriched count: **235**
- New enriched count: **260**
- Delta: **+25**
- Remaining fallback: **318**
- Generated micro-drills: **196**
- Batch policy: deterministic manual-review promotion layered after matcher v2
- Matcher v2 changed: **no**

## Items Added

`wset3_28`, `wset3_49`, `wset3_67`, `wset3_76`, `wset3_212`,
`wset3_227`, `wset3_247`, `wset3_262`, `wset3_322`, `wset3_323`,
`wset3_329`, `wset3_347`, `wset3_358`, `wset3_367`, `wset3_386`,
`wset3_389`, `wset3_390`, `wset3_393`, `wset3_396`, `wset3_413`,
`wset3_701`, `wset3_715`, `wset3_723`, `wset3_726`, `wset3_738`.

## Domains Covered

- Sparkling dosage, tank-method fruit retention and service temperature
- Service temperatures for light whites, oaked whites, reds and Amontillado
- Saignee rose extraction
- Mosel climate, slopes, acidity, residual sugar and alcohol
- Warm-climate ripeness, fruit profile and alcohol potential
- Cool and maritime climate moderation
- Frost risk and shoot damage
- Oak origin, oak ageing and maturation vessel size
- Long maceration and large-cask maturation
- Oxidation in white wine
- Food sweetness and wine balance

## Nodes Created

- `HC_OAKED_WHITE_SERVICE_TEMPERATURE`
- `HC_SPARKLING_SERVICE_TEMPERATURE`
- `HC_LIGHT_WHITE_SERVICE_TEMPERATURE`
- `HC_AMONTILLADO_SERVICE_TEMPERATURE`
- `HC_SAIGNEE_ROSE_EXTRACTION`
- `HC_MOSEL_COOL_SLOPE_ACIDITY`
- `HC_WARM_CLIMATE_RIPE_FRUIT_ALCOHOL`
- `HC_MOSEL_RESIDUAL_SUGAR_LOW_ALCOHOL`
- `HC_LONG_MACERATION_LARGE_CASK`

## Nodes Extended

No existing causal node was broadened. Existing nodes were reused only where
their established mechanism directly explained the keyed answer.

## Rejected Items

- Negative-polarity and deliberately false keyed answers: rejected.
- Pure region, variety or terminology identification: rejected as trivia-only.
- Climate or soil claims without a bounded, site-specific mechanism: rejected.
- Service-temperature questions with no defensible balance between aroma,
  structure and freshness: rejected.
- Items where oak, climate or vessel choice explained only the topic rather
  than the correct option: rejected.
- Absolute regional claims that could not be made safe with a short caveat:
  rejected.

`wset3_396` was retained only through manual review. Matcher v2 still returns no
match, preserving the old substring false-positive guard. Its enrichment is
explicitly linked to maritime moderation and warns that continental influence
increases eastward and that the Loire is not climatically uniform.

## Caveats Added

Every promoted item includes a Spanish learner-facing `Matiz:` and a
provenance-level `learner_caveat`. Caveats cover regional and vintage
variation, service-temperature ranges, producer choices, oak variability,
limits of climate generalizations, and the distinction between correlation
and direct mechanism.

## Tests Run

Passed:

- Batch 5 promotion tests: **6/6**
- Strong-signal and false-positive regression tests: **9/9**
- Determinism tests: **1/1**
- Spanish and enrichment-integrity tests: **7/7**
- HC node schema/governance and manifest tests: **47/47**
- Structured enrichment contract tests: **12/12**
- Structured enrichment behavior tests: **16/16**
- Post-regeneration Batch 5 verification: **6/6**
- Post-regeneration integrity, false-positive and Spanish tests: **13/13**

Timed out:

- Combined expansion/structured-enrichment run exceeded 300 seconds.
- `tests.test_sba_enrichment_expansion` exceeded 360 seconds when isolated.
- No focused test failure was observed. The two structured suites from the
  combined command passed independently, so the timeout did not block the
  batch under the requested policy.

## Artifacts

- `knowledge/question-bank/enrichment/sba_enrichment_v1.json` regenerated
  with 260 enriched items and 196 micro-drills.
- `docs/ENRICHMENT_BATCH1_SAMPLE.md` regenerated.
- Frontend and production payload mirrors were not touched.

## Files Changed

- `tools/question_generation/sba_enrichment_deriver.py`
- `tests/test_sba_enrichment_batch5.py`
- `tests/test_sba_enrichment_deriver.py`
- Nine new `HC_*` causal node files
- `knowledge/question-bank/enrichment/sba_enrichment_v1.json`
- `docs/ENRICHMENT_BATCH1_SAMPLE.md`
- This report

## Delivery

- Implementation commit: `da83705`
- Implementation push: **success**, `origin/main`
- Report commit: recorded in the subsequent documentation commit
- Production touched: **no**
- Frontend touched: **no**
- Governance flags changed: **no**
- LLM/API/embedding/vector DB/cloud usage added: **no**

This is formative enrichment only. It does not represent official WSET
assessment or examiner scoring.
