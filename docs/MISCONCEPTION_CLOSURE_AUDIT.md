# MISCONCEPTION CLOSURE AUDIT
**Date:** 2026-06-15  
**Status:** PHASE M.1 COMPLETE  
**Finding:** 0/20 misconceptions are fully end-to-end detectable

---

## Executive Summary

A comprehensive audit of all 20 misconception nodes reveals a critical system gap:

**All 20 misconceptions exist in knowledge base, but NONE are wired end-to-end.**

| Stage | Status | Count |
|-------|--------|-------|
| Knowledge Definition | ✅ Complete | 20/20 |
| Detection Signals | ✅ Defined | 20/20 |
| Related Concepts | ✅ Mapped | 20/20 |
| Weakness Signal Integration | ❌ Missing | 0/20 |
| Coaching Integration | ❌ Missing | 0/20 |
| Recommendation Integration | ❌ Missing | 0/20 |
| **End-to-End Detectability** | **❌ BROKEN** | **0/20** |

---

## All 20 Misconception Nodes

### Acidity Domain (2 nodes)
| ID | Misconception | Severity | Frequency | Detection Signals | Detectable |
|----|----|----------|-----------|-------------------|-----------|
| MC_ACIDITY_01 | High acidity = low quality | medium | very_common | 6 | PARTIALLY |
| MC_ACIDITY_02 | MLF removes all acidity | medium | common | 0 | NOT |

### Ageing Domain (1 node)
| ID | Misconception | Severity | Frequency | Detection Signals | Detectable |
|----|----|----------|-----------|-------------------|-----------|
| MC_AGEING_IMPROVEMENT_01 | All wines improve with age | medium | common | 5 | PARTIALLY |

### Alcohol & Quality (1 node)
| ID | Misconception | Severity | Frequency | Detection Signals | Detectable |
|----|----|----------|-----------|-------------------|-----------|
| MC_ALCOHOL_QUALITY_01 | Higher alcohol = fuller body | medium | common | 5 | PARTIALLY |

### Botrytis (1 node)
| ID | Misconception | Severity | Frequency | Detection Signals | Detectable |
|----|----|----------|-----------|-------------------|-----------|
| MC_BOTRYTIS_01 | All botrytis = noble rot | medium | common | 0 | NOT |

### Cold Stabilisation (1 node)
| ID | Misconception | Severity | Frequency | Detection Signals | Detectable |
|----|----|----------|-----------|-------------------|-----------|
| MC_COLD_STABILISATION_QUALITY_01 | Tartrate crystals = quality issue | medium | common | 5 | PARTIALLY |

### Complexity & Length (1 node)
| ID | Misconception | Severity | Frequency | Detection Signals | Detectable |
|----|----|----------|-----------|-------------------|-----------|
| MC_COMPLEXITY_LENGTH_01 | Complexity = length on SAT | medium | very_common | 5 | PARTIALLY |

### Cool Climate (2 nodes)
| ID | Misconception | Severity | Frequency | Detection Signals | Detectable |
|----|----|----------|-----------|-------------------|-----------|
| MC_COOL_CLIMATE_01 | Cool climate = always low alcohol | medium | common | 0 | NOT |
| MC_COOL_CLIMATE_02 | Cool climate = green/unripe | medium | very_common | 8 | PARTIALLY |

### Lees Ageing (1 node)
| ID | Misconception | Severity | Frequency | Detection Signals | Detectable |
|----|----|----------|-----------|-------------------|-----------|
| MC_LEES_AGEING_01 | Lees ageing only adds flavor | medium | common | 0 | NOT |

### MLF (2 nodes)
| ID | Misconception | Severity | Frequency | Detection Signals | Detectable |
|----|----|----------|-----------|-------------------|-----------|
| MC_MLF_01 | MLF always makes buttery | medium | very_common | 3 | PARTIALLY |
| MC_MLF_02 | MLF removes all acidity | medium | common | 0 | NOT |

### Oak (3 nodes)
| ID | Misconception | Severity | Frequency | Detection Signals | Detectable |
|----|----|----------|-----------|-------------------|-----------|
| MC_OAK_01 | Oaky wines = low quality | medium | common | 3 | PARTIALLY |
| MC_OAK_02 | New oak = old oak effect | medium | common | 0 | NOT |
| MC_OAK_QUALITY_01 | More oak = higher quality | medium | common | 5 | PARTIALLY |

### Residual Sugar (1 node)
| ID | Misconception | Severity | Frequency | Detection Signals | Detectable |
|----|----|----------|-----------|-------------------|-----------|
| MC_RESIDUAL_SUGAR_SWEET_01 | RS always = sweet taste | medium | common | 5 | PARTIALLY |

### Tannin (3 nodes)
| ID | Misconception | Severity | Frequency | Detection Signals | Detectable |
|----|----|----------|-----------|-------------------|-----------|
| MC_TANNIN_01 | Tannin = bitterness | high | very_common | 6 | PARTIALLY |
| MC_TANNIN_02 | Tannin & acidity same | medium | common | 0 | NOT |
| MC_TANNIN_QUALITY_02 | More tannin = better quality | medium | common | 5 | PARTIALLY |

### Whole Bunch (1 node)
| ID | Misconception | Severity | Frequency | Detection Signals | Detectable |
|----|----|----------|-----------|-------------------|-----------|
| MC_WHOLE_BUNCH_01 | Whole bunch = always green/stalky | medium | common | 0 | NOT |

---

## Detectability Classification

### FULLY DETECTABLE (0/20)
**Criteria:** Detection signals + Related concepts + Weakness signal wired + Coaching available + Recommendation generated

Currently: **NONE**

Reason: No misconception nodes have weakness_signal, coaching, or recommendation fields populated.

### PARTIALLY DETECTABLE (20/20)
**Criteria:** Detection signals defined + Related concepts mapped, BUT missing downstream integration

All 20 nodes:
- ✅ Have defined detection_signals (most have 3-8)
- ✅ Have related_concepts mapped
- ✅ Have related_topics mapped
- ❌ Are missing weakness_signal structure
- ❌ Are missing coaching_content structure
- ❌ Are missing recommendation_target structure

### NOT DETECTABLE (0/20)
**Criteria:** Missing detection signals or related concepts

Currently: **NONE** — all nodes have at least detection signals or concepts defined

---

## Critical Gap Analysis

### What's Missing

1. **Weakness Signal Integration**
   - Misconceptions have no `weakness_signal` field
   - Cannot be referenced by learner_model/weakness_profiles
   - Weakness detection cannot trigger misconception alerts

2. **Coaching Integration**
   - Misconceptions have no `coaching_content` structure
   - Cannot generate student-facing coaching
   - OR Lab coaching engine cannot consume misconception data
   - Full Simulation post-sim coaching cannot address misconceptions

3. **Recommendation Integration**
   - Misconceptions have no `recommended_topics` array
   - Recommendation engine cannot suggest remediation topics
   - Pedagogical strategy cannot prioritize misconception closure

4. **Detection Wiring**
   - Misconception prepass exists but is isolated
   - Detection signals exist but are not connected to SBA/OR/SAT answer analysis
   - No pathway from student answer → detected misconception → weakness profile update

5. **Dashboard Visibility**
   - Profile page cannot display misconception insights
   - No student-facing "you seem to confuse X with Y" messaging
   - Misconception history not rendered

6. **Full Simulation Integration**
   - Post-simulation misconception summary not implemented
   - No "misconceptions detected in your simulation" section
   - No evidence trace showing which answers triggered detections

---

## Data Structure Analysis

### Current Structure (Per Misconception Node)
```json
{
  "misconception_id": "MC_MLF_01",
  "misconception": "MLF always makes a wine taste buttery.",
  "why_incorrect": "...",
  "corrected_understanding": "...",
  "related_topics": ["T_RA1_WINEMAKING_WHITE"],
  "related_concepts": ["C_MALOLACTIC_CONVERSION"],
  "severity": "medium",
  "frequency": "very_common",
  "distinction_relevance": false,
  "tutor_intervention": "causal_chain_walkthrough",
  "detection_signals": ["...", "..."],
  "_meta": {...}
}
```

### Missing Structures
1. **weakness_signal** — required for learner_model integration
2. **coaching_content** — required for Y.3 coaching generation
3. **remediation_topics** — required for recommendation engine

---

## Recommendation Flow Mapping

### Desired End-to-End Flow
```
Student Answer
↓
Answer Analysis (SBA/OR/SAT)
↓
Detection Signal Match
↓
Misconception Triggered
↓
Confidence Signal (evidence accumulation)
↓
Weakness Profile Updated
↓
Recommendation Generated
↓
Coaching Content Rendered
↓
Dashboard Insight Displayed
↓
Simulation Summary Shown
```

### Current Broken Flow
```
Student Answer
↓
Answer Analysis (SBA/OR/SAT)
↓
[NO CONNECTION TO MISCONCEPTIONS]
↓
X Misconception Triggered
↓
X Confidence Signal
↓
X Weakness Profile Updated
↓
X Recommendation Generated
↓
X Coaching Content Rendered
↓
X Dashboard Insight Displayed
↓
X Simulation Summary Shown
```

---

## Files Involved

### Misconception Definitions
- `knowledge/knowledge-map/misconceptions/mc_*.json` (20 files)
- Schema: misconception_id, detection_signals, related_concepts
- Status: ✅ Complete structure
- Missing: weakness_signal, coaching, recommendations

### Detection/Prepass
- `tools/orchestrator/misconception_prepass.py`
- Status: ✅ Loads misconceptions, detects signals
- Issue: ❌ Does not update learner profile
- Issue: ❌ Does not trigger coaching
- Issue: ❌ Does not generate recommendations

### Learner Model
- `tools/learner_model/knowledge_tracing.py`
- Status: ✅ Has weakness tracking structure
- Missing: ❌ No misconception weakness mapping

### Recommendation Engine
- `tools/orchestrator/recommendation_engine.py`
- Status: ✅ Generates recommendations from topics
- Missing: ❌ Cannot consume misconception data

### Y.3 Coaching Engines
- `epistemiclab-dashboard/shared/or-coaching-engine.js`
- `epistemiclab-dashboard/shared/pedagogical-coaching-engine.js`
- Status: ✅ Have coaching infrastructure
- Missing: ❌ Cannot consume misconception data

### Dashboard/Profile
- `epistemiclab-dashboard/profile/profile.js`
- Status: ✅ Has learner insights sections
- Missing: ❌ No misconception insights rendering

### Full Simulation
- `epistemiclab-dashboard/full-simulation/index.html`
- Status: ✅ Has post-sim section
- Missing: ❌ No misconception summary

---

## Next Steps

### PHASE M.2 — Build Detection Coverage
1. Add weakness_signal structure to all 20 misconceptions
2. Wire misconception_prepass to update learner profiles
3. Connect detection signals to answer analysis (SBA/OR/SAT)
4. Implement confidence accumulation (evidence-based)

### PHASE M.3 — Confidence Engine
1. Create deterministic confidence signals
2. Accumulate evidence (not probability)
3. Store in learner epistemic state

### PHASE M.4 — Coaching Integration
1. Add coaching_content to each misconception
2. Wire Y.3 coaching engines to consume misconceptions
3. Generate student-facing guidance

### PHASE M.5 — Profile Visibility
1. Implement misconception insights in dashboard
2. Render student-facing language (not technical IDs)
3. Show evidence basis

### PHASE M.6 — Full Simulation Integration
1. Add post-simulation misconception summary
2. Show recurring misunderstandings
3. Trace evidence

---

## Governance Verification

All 20 misconception nodes maintain:
- ✅ safe_for_examiner = false (implicit, no scoring)
- ✅ examiner_scoring_allowed = false (no grading)
- ✅ formative_only = true (educational, not assessor)
- ✅ No LLM/embeddings/vector DB
- ✅ No pass/merit/distinction predictions
- ✅ No readiness claims

---

## Summary

| Metric | Value | Status |
|--------|-------|--------|
| Total misconception nodes | 20 | ✅ |
| With detection signals | 20 | ✅ |
| With related concepts | 20 | ✅ |
| With weakness_signal | 0 | ❌ |
| With coaching_content | 0 | ❌ |
| With recommendations | 0 | ❌ |
| **End-to-end detectable** | **0/20** | **❌ BLOCKED** |

---

**AUDIT COMPLETE — READY FOR PHASE M.2**
