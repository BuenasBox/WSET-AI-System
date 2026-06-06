# Phase 4A.3.8.5.7 - Master Bank Review & Inactive Resolution

## Scope

Recovery-first resolution of the 68 operational Review records and 24
operational Inactive records. Only repository evidence was used. No frontend,
deployment, Tutor, Retrieval, Self-Eval, Golden, snapshot, governance, or public
activation behavior was changed.

## Initial State

| Pool | Count |
|---|---:|
| Master Bank | 616 |
| SBA operational | 506 |
| Open Response candidate | 21 |
| Review | 68 |
| Inactive | 24 |
| Public Lab | 36 |

## Final State

| Pool | Count |
|---|---:|
| Master Bank | 616 |
| SBA operational | 589 |
| Open Response candidate | 27 |
| Review | 0 |
| Inactive eligibility backlog | 0 |
| Quarantine | 0 |
| Public Lab | 36 |

The canonical Master Bank `inactive` collection remains an activation-state
boundary for private records. It does not mean operationally ineligible.
Operational eligibility is defined by the eligibility layer, where the
Inactive backlog is now zero.

## Transitions

| Transition | Count |
|---|---:|
| Review -> SBA | 68 |
| Review -> Open Response | 0 |
| Review -> Quarantine | 0 |
| Inactive -> SBA | 18 |
| Inactive -> Open Response | 6 |
| Inactive -> Quarantine | 0 |

### Review -> SBA

`7, 19, 23, 24, 29, 33, 43, 56, 59, 60, 62, 75, 81, 85, 102, 116, 128, 218, 225, 267, 284, 296, 316, 318, 335, 337, 341, 346, 349, 356, 362, 364, 365, 368, 372, 384, 388, 390, 394, 421, 426, 435, 451, 454, 459, 464, 473, 479, 480, 490, 491, 496, 500, 509, 511, 670, 712, 713, 724, 727, 731, 746, 785, 826, 827, 842, 846, 847`

All 68 have valid stems, four options, traceable answers, clean governance, and
minimum metadata. Their explanation/comparison wording alone did not establish
a sufficiently bounded free-response answer. They were therefore finalized as
SBA rather than converted speculatively.

The public records `356`, `421`, and `464` remain in the unchanged 36-item
Public Lab and retain explicit SBA eligibility.

### Inactive -> SBA

`1, 4, 5, 12, 13, 15, 17, 20, 30, 44, 50, 78, 87, 108, 247, 253, 386, 510`

These records already had structurally valid SBA content. Existing enrichment
drafts supplied traceable RA, topic, subtopic, and difficulty metadata. Prior
inactive/revision states represented activation or review decisions, not
irrecoverable data defects.

### Inactive -> Open Response

`18, 853, 854, 855, 856, 857`

- `18`: recovered using the existing sulphites preservation causal-chain
  artifact and RA1 metadata. SBA residue was removed from the normalized
  candidate.
- `853`: converted to an explanation of vintage labelling, supported by the
  existing structured bank.
- `854`: converted to an explanation of the DOP/IGP regulatory distinction,
  supported by the existing structured bank.
- `855`: converted to an explanation of Spanish Reserva ageing requirements,
  supported by the existing structured bank.
- `856`: converted to a Kabinett/Trockenbeerenauslese comparison, supported by
  the official WSET Germany corpus already present in the repository.
- `857`: converted to an on-trade/off-trade comparison, supported by the
  existing structured bank.

The original structured records were not deleted or rewritten. A versioned
resolution artifact applies normalized overrides and preserves evidence paths.
Open Response remains inactive at runtime and requires explicit private opt-in
in the existing session composer.

## Architecture

- `master_bank_review_inactive_resolution.json` records one final decision for
  every affected ID, including source pool, destination, repairs, evidence, and
  quarantine analysis.
- `master_bank_resolution.py` loads and applies only explicit source-view
  overrides.
- The canonical importer consumes the resolution layer and records its lineage.
- The Open Response pipeline consumes the same resolution layer, removes SBA
  residue, attaches repository support, and regenerates 26 approved normalized
  records.
- Suitability treats resolved decisions as authoritative, while Q14 remains the
  existing suitability-derived candidate. This produces 27 operational Open
  Response candidates.
- Eligibility and Dashboard data are derived from the updated suitability
  artifact. No frontend was modified.

## Repairs

- Finalized 68 ambiguous suitability reviews as evidence-backed SBA.
- Restored 18 valid SBA records and applied existing draft metadata.
- Added RA/topic/causal/support metadata to Q18.
- Reframed Q853-Q857 as repository-grounded short-answer prompts.
- Removed True/False and A-D residue from normalized Q853-Q857 candidates.
- Preserved source lineage, resolution lineage, governance defaults, and all
  616 source records.

## Verification

- Full suite: `1553 OK`, `9 skipped`.
- SBA export dry-run: 36 eligible, 0 validation errors.
- Slow Golden: `7/7 OK`.
- Public Lab: 36, unchanged.
- Suitability: 589 SBA-only, 27 Open Response candidates, 0 Review, 0 Inactive.
- Eligibility: 589 SBA operational, 27 Open Response candidates, 0 Review,
  0 Inactive.
- Governance flags remain false and training-only.

## Remaining Risks

- The 27 Open Response candidates are structurally approved but not publicly
  activated and do not imply official scoring authority.
- Difficulty labels remain inherited repository metadata; this phase does not
  perform difficulty calibration.
- Q853-Q857 retain their original source statements as lineage evidence while
  their normalized Open Response prompts are applied through the resolution
  layer.
- Quarantine is empty. Future evidence conflicts must fail closed rather than
  silently changing these decisions.

This phase does not represent WSET assessment, examiner marking, or official
evaluation.
