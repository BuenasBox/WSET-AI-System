# SBA Batch 1 Report

**Date:** 2026-06-15  
**Phase:** S.1  
**Status:** Backend corpus integration complete; frontend and production untouched.

## Questions Added

- Added: **47 SBA**
- Source IDs: `858`-`904`
- Operational SBA: **578 -> 625**
- Enrichment records: **360 -> 407**
- New enrichment-ready records: **47**
- New micro-drill candidates integrated as micro-drills: **47**

## RA Distribution

| RA | Added | Purpose |
|---|---:|---|
| RA1 | 4 | Icewine/Eiswein concentration process and production risk |
| RA2 | 36 | Canada/Germany Icewine, Sauternes, Tokaji, botrytis, late harvest, drying and sweet-wine style |
| RA5 | 7 | Sweet-wine pairing, service, storage and open-bottle advice |

No generic RA1 expansion was added beyond the four documented
Icewine/Eiswein process items.

## Coverage Gaps Closed

- Icewine/Eiswein moved from missing to repeated causal SBA coverage.
- Cryoconcentration is discriminated from botrytis, drying and late harvest.
- Canada and Germany sweet-wine applications now include vintage risk,
  harvest timing, fermentation difficulty, acidity and cost.
- Sauternes coverage now includes weather sequence, selective harvesting,
  variety roles, botrytis acid metabolism, vintage risk, oak and quality balance.
- Tokaji coverage now includes Aszu berry addition, Furmint acidity,
  Szamorodni, Eszencia, classification limits, botrytis conditions and ageing.
- RA5 now includes applied sweet-wine pairing, service temperature, storage,
  open-bottle preservation and portion advice.

## Enrichment Opportunities

Every new record includes:

- A cause-mechanism-effect causal-chain candidate.
- Correct and distractor feedback.
- A remediation recommendation.
- A micro-drill candidate.
- A linkage to an existing operational misconception node.
- Local source-file provenance.

The integration sidecar contains learner-facing `causal_chain`,
`feedback_by_mode`, `micro_drill`, and `misconception_linkage_candidate`
records for all 47 items.

## Validation

- Batch size and IDs: valid.
- RA mapping: valid.
- Four unique options and one keyed answer per item: valid.
- Identification-only and definition-only stems: none.
- Duplicate stems against the existing corpus: none.
- Duplicate stems within the batch: none.
- Governance flags: all immutable safe values.
- Examiner language, scoring and pass prediction: absent.
- Frontend and production files: unchanged.

## Remaining Gaps

- RA4 breadth remains the next priority.
- RA2 regional breadth outside sweet wines remains under target.
- Applied regional winemaking decisions require Batch 3 expansion.
- Aggregate RA1 remains overrepresented in the inherited corpus; no further
  RA1 growth is planned in this program.

This report is formative project documentation. It does not represent WSET
assessment, examiner evaluation or official scoring.
