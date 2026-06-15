# EpistemicLab Specification Balance Analysis

**Audit date:** 2026-06-15  
**Specification source:** WSET Level 3 Wines Specification, Issue 2.0.1, August 2023, as extracted in `knowledge/assessment-framework/`.

## 1. Official weighting baseline

Unit 1 Part 1 contains 50 MCQ:

| RA | Official MCQ allocation | Official share |
|---|---:|---:|
| RA1 | 8 | 16% |
| RA2 | 28 | 56% |
| RA3 | 5 | 10% |
| RA4 | 5 | 10% |
| RA5 | 4 | 8% |

Unit 1 Part 2 contains four short-answer questions:

- RA1 is foundational in all four questions.
- RA2 accounts for approximately 70 of 100 allocated content marks.
- RA3 and RA4 together account for approximately 20.
- RA5 Block 1 accounts for approximately 10.

SAT is a separate unit and should not be used to compensate for theory-domain gaps.

## 2. SBA balance

Production SBA distribution:

| RA | Actual items | Actual share | Official share | Delta | Balance |
|---|---:|---:|---:|---:|---|
| RA1 | 225 | 38.9% | 16% | +22.9 pp | OVERREPRESENTED |
| RA2 | 217 | 37.5% | 56% | -18.5 pp | UNDERREPRESENTED |
| RA3 | 64 | 11.1% | 10% | +1.1 pp | PROPORTIONATE |
| RA4 | 31 | 5.4% | 10% | -4.6 pp | UNDERREPRESENTED |
| RA5 | 39 | 6.7% | 8% | -1.3 pp | SLIGHTLY UNDERREPRESENTED |
| Unknown | 2 | 0.3% | 0% | +0.3 pp | REQUIRES MAPPING |

The largest imbalance is not a lack of total questions. It is the substitution of RA1 volume for RA2 regional application and RA4 fortified-wine coverage.

## 3. Open Response balance

The committed deployed OR baseline has **31 items**:

| RA | OR items | Share |
|---|---:|---:|
| RA1 | 21 | 67.7% |
| RA2 | 10 | 32.3% |
| RA3 | 0 | 0% |
| RA4 | 0 | 0% |
| RA5 | 0 | 0% |

This is materially misaligned with the official short-answer structure.

- RA1 is foundational, but the bank treats it as the dominant standalone OR domain.
- RA2, which carries most short-answer content weight, has only 10 items.
- RA3, RA4, and RA5 have no committed deployed OR coverage.

The separate expansion work was excluded from this baseline because it was not part of the frozen 31-item corpus at the audit cutoff. Two expansion batches were committed later while verification was still running.

## 4. SAT balance

The SAT bank contains six prompts:

- 2 complex whites
- 1 simple white
- 1 complex red
- 1 simple red
- 1 sweet white

Strengths:

- Every prompt supports appearance, nose, palate, quality, and readiness.
- Simple versus complex wine logic is represented.
- Oak, lees, tertiary development, sweetness, and structural balance appear.

Weaknesses:

- Only two prompts are explicitly used by the lexical audit for quality-justification language.
- There is no rose archetype.
- There is no clearly faulty wine archetype.
- There is no clearly too-young or too-old calibration case.
- Readiness scale values exist, but readiness discrimination is not diversified across enough edge cases.
- SAT prompts are generic archetypes and do not repair RA2 regional undercoverage.

## 5. Misconception balance

Misconception nodes are concentrated in:

- acidity
- tannin
- oak
- MLF
- cool climate
- ageing
- SAT quality concepts

Domains with no misconception pathway include:

- yield
- canopy
- irrigation
- harvest timing
- most soils reasoning
- sparkling methods and dosage
- fortification
- Port and Sherry styles
- Madeira
- Icewine/passito
- regional law and hierarchy
- service, faults, and food pairing

No RA has fully linked misconception detection because all 20 nodes lack SBA distractor linkage.

## 6. Coaching balance

Coaching is strongest for:

- SAT structure
- SAT quality/readiness
- command verbs
- generic short-answer structure

Coaching is weakest for:

- region-specific causal reasoning
- sparkling method comparisons
- fortified-wine production decisions
- sweet-wine method discrimination
- service/fault/pairing misconceptions

The current coaching estate is a cross-cutting skills layer, not a complete domain-remediation layer.

## 7. Overrepresentation and underrepresentation

### Overrepresented

1. RA1 SBA volume.
2. Climate, fermentation, oak, tannin, and broad palate language.
3. Spain, Italy, and Chile/Argentina within RA2.
4. Sherry within RA4.
5. Recognition tasks relative to free-response production.

### Underrepresented

1. RA2 overall against its 56% official MCQ share.
2. RA4 overall against its 10% official MCQ share.
3. RA3, RA4, and RA5 Open Response.
4. Regional causal chains for USA/Canada, South Africa, Portugal, and Southern France.
5. Sweet-wine method discrimination, especially Icewine/Eiswein.
6. Misconception coverage outside acidity/tannin/oak/MLF.
7. Coaching pathways tied to named content weaknesses.

## 8. Mathematical alignment scenarios

### Current-total deficit floor

Applying official MCQ shares to the current 578-item bank gives approximate targets:

| RA | Current | Target at 578 | Deficit |
|---|---:|---:|---:|
| RA1 | 225 | 92 | 0 |
| RA2 | 217 | 324 | 107 |
| RA3 | 64 | 58 | 0 |
| RA4 | 31 | 58 | 27 |
| RA5 | 39 | 46 | 7 |

Minimum additions to fill current absolute deficits: **141 SBA**.

This does **not** produce exact proportional alignment because RA1 remains overrepresented.

### Strict add-only proportional alignment

If no existing item can be removed, retagged, or down-weighted, RA1's 225 items must equal approximately 16% of the final bank. The smallest practical final bank is about **1,407 items**:

| RA | Approximate final target | Current | Additions |
|---|---:|---:|---:|
| RA1 | 225 | 225 | 0 |
| RA2 | 788 | 217 | 571 |
| RA3 | 141 | 64 | 77 |
| RA4 | 141 | 31 | 110 |
| RA5 | 112 | 39 | 73 |
| **Total** | **1,407** | **576 classified** | **831** |

Strict add-only alignment therefore requires approximately **831 additional SBA**. This is mathematically correct but pedagogically inefficient. A future balancing policy should use selection weights and domain caps rather than attempting to solve all imbalance through content volume.

## 9. Conclusion

The corpus is not proportionally aligned with the official specification.

- RA1 is overbuilt.
- RA2 and RA4 are the primary theory deficits.
- Open Response is the most severe format imbalance.
- SAT is structurally capable but archetypically narrow.
- Misconception and coaching coverage are concentrated in a small set of concepts.
