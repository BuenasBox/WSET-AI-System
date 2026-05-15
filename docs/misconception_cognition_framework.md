# Misconception Cognition Framework
## WSET-AI-System — Cognitive Architecture Design Series

**Author:** Claude (Cowork) — Cognitive Architecture Designer Role
**Date:** 2026-05-15
**Series position:** 3 of 8 — Depends on LES (Document 1); directs Orchestrator planning (Document 2)
**Status:** Design specification — requires engineering implementation

---

## Why Misconceptions Deserve Their Own Framework

Most educational AI systems treat misconceptions as errors. An error is something the student got wrong; the correction is to tell them what is right. This is the wrong model.

A misconception is not an error. It is a coherent, internally consistent false belief that the student holds with confidence. The student is not confused — they are wrong in a structured way. The distinction matters enormously for tutoring, because the correction strategy for a confused student (more explanation) is exactly the wrong strategy for a misconceiving student (more explanation may actually reinforce the misconception by providing more material for the student to reinterpret through their false belief).

WSET L3 is particularly vulnerable to the wrong correction strategy because wine is a domain with high everyday familiarity. Students arrive with pre-existing mental models of what wine quality means, what "acidity" feels like, what "tannic" means colloquially — and these lay models are frequently inverted from or incompatible with the technical WSET model. The student is not building understanding from zero; they are rebuilding understanding from wrong.

This framework specifies how the system should model, detect, classify, prioritize, and correct misconceptions as first-class cognitive objects.

---

## Misconception Classification Taxonomy

Not all misconceptions are the same. The intervention strategy must match the misconception type. The system distinguishes five types:

### Type 1 — Causal Inversion

The student has the right concepts but has the causal direction reversed.

**Example:** "High acidity causes wines to feel harsh and aggressive" — the student has linked acidity to unpleasant sensation correctly (as an observation) but has made a quality judgment from it that inverts the role of acidity in wine quality and ageability.

**Example:** "Tannin comes from the barrel, not the grape" — tannin source inverted (most tannin is grape-derived; barrel contribution is secondary and texturally different).

**Exam impact:** Catastrophic. A causal inversion will produce structurally wrong SAT conclusions and wrong causal explanations. Marking schemes penalize unsupported causal claims — an inverted causal claim with confidence is worse than a hedged correct statement.

**Correction strategy:** Causal chain walkthrough. Do not correct the conclusion directly; trace the mechanism from the cause. The goal is to make the student see where the inversion occurs in the chain, not just to hear the right answer.

### Type 2 — Scope Error

The student has a correct belief that is applied at the wrong scope — too broad, too narrow, or to the wrong domain.

**Example:** "Cool climate always means green, underripe wines" — the statement is true at the extreme end of a cool spectrum but false as a general rule. The belief is correct in scope (cool climates do tend toward higher acidity, lower alcohol, more primary fruit) but the student has overapplied it.

**Example:** "MLF is used in all red wines" — MLF is common in red winemaking but is a winemaker choice, not a universal.

**Exam impact:** Medium. Scope errors produce answers that are directionally correct but imprecise, which markers penalize with "lacks precision" feedback. They do not produce catastrophically wrong answers but will not achieve Distinction marks.

**Correction strategy:** Boundary clarification. Acknowledge the correct core ("You're right that cool climates tend to produce wines with...") then explicitly define the scope boundary ("...but this is not universal — here's what determines whether a cool climate wine achieves full ripeness").

### Type 3 — Vocabulary Confusion

The student is using the right word with the wrong meaning, or conflating two distinct WSET technical terms.

**Example:** Confusing "balance" (WSET SAT structural term) with personal preference for a wine that feels "balanced" or harmonious.

**Example:** Confusing "complexity" (number and range of aromas/flavours present, WSET SAT definition) with "impressive" or "difficult to understand."

**Example:** Using "finish" to mean "aftertaste" rather than the duration of perceived flavour after swallowing.

**Exam impact:** High for SAT specifically. WSET markers read vocabulary precisely. A student who uses "complex" to mean "sophisticated" rather than "offering multiple distinct aroma/flavour layers" will score incorrectly on SAT quality assessment even if their sensory perception is accurate.

**Correction strategy:** Definition anchoring. Provide the exact WSET technical definition, contrast it explicitly with the lay usage, give a test example, then ask the student to apply the correct definition to a new case.

### Type 4 — False Prerequisite

The student believes that X must precede Y — that a feature, condition, or process is a prerequisite for something that it is not.

**Example:** "A wine must be oaked to be Distinction-level quality" — false prerequisite linking production method to quality tier.

**Example:** "High alcohol wines cannot have high acidity" — false mutual exclusivity built from real correlation (warm climates → lower acidity + higher potential alcohol) overapplied as a rule.

**Exam impact:** Medium. False prerequisites produce hedged, imprecise answers — students qualify claims in ways that reveal the false belief to a knowledgeable marker.

**Correction strategy:** Exception drilling. Present a counter-example that violates the false prerequisite, then explain the underlying principle. The counter-example must be vivid and memorable (e.g., Mosel Riesling — a wine with very high acidity AND high quality AND no oak).

### Type 5 — Authority Substitution

The student substitutes personal taste preference or received opinion ("my wine teacher says," "a well-known wine writer thinks") for technical WSET assessment criteria.

**Example:** "Obviously Burgundy is better than Bordeaux" — a preference claim substituted for a technical quality assessment framework.

**Example:** "Natural wine is inherently higher quality because it's authentic" — a philosophical value claim substituted for the WSET quality definition (showing expected characteristics for type and price point, with positive attributes outweighing faults).

**Exam impact:** High for SAT quality conclusions. WSET markers explicitly expect candidates to apply the defined quality framework, not personal preference. An authority substitution in a quality conclusion will score poorly even if the candidate clearly knows a lot about wine.

**Correction strategy:** Framework installation. Do not argue with the preference; validate it as a legitimate personal response, then clearly separate it from the WSET examination framework. Install the correct framework explicitly: "In a WSET examination context, quality means specifically..."

---

## Detection System

### Primary Detection — Examiner Error Taxonomy

The Examiner Agent's 14-label error taxonomy is the primary detection mechanism. After every Examiner session, the Orchestrator maps error labels to misconception types:

| Examiner error label | Likely misconception type | LES action |
|---|---|---|
| `missing_causal_link` | Type 1 (Causal Inversion) | Check for active causal inversion misconceptions; if absent, create new entry |
| `unsupported_conclusion` | Type 1 or Type 2 | Check if conclusion is inverted or merely out-of-scope |
| `vague_claim` | Type 3 (Vocabulary Confusion) | Flag relevant vocabulary terms for definition anchoring |
| `sat_non_commitment` | Type 5 (Authority Substitution) or SAT-specific | Check SAT epistemic state; escalate SAT cognitive module |
| `bicl_not_supported` | Type 4 (False Prerequisite) or SAT-specific | Check BICL understanding in SAT epistemic state |
| `fact_without_consequence` | Type 1 (causal direction absent) | Pattern: student knows output but not mechanism |

### Secondary Detection — Soft Signals in Tutor Sessions

Not every misconception surfaces through formal Examiner sessions. The Tutor Agent can detect soft signals during explanation sessions:

- Student asks a question that presupposes a false belief: "But doesn't high tannin mean the wine is better quality?" (presupposes tannin = quality)
- Student uses vocabulary inconsistently with WSET definition: "The wine has good complexity — I mean it tastes sophisticated"
- Student expresses resistance to a correction: "My uncle always says..." (authority substitution signal)

Soft signals do not trigger LES writes directly. They are logged as `soft_detection_signals` in the staging file. Three soft signals for the same misconception without Examiner confirmation → `suspected_active` status → next session includes Examiner evaluation of that concept.

### Tertiary Detection — Query Pattern Analysis

Certain query patterns are statistically predictive of underlying misconceptions:

- Repeated queries about the same concept after explanations → fragile understanding, possibly misconception-anchored
- Queries phrased as "why does X *always*..." → scope error risk
- Queries seeking external authority validation → authority substitution risk
- Avoidance of certain topics across multiple sessions → suspected misconception-induced avoidance

The Orchestrator can detect these patterns from the LES session history without any new student input.

---

## Intervention Sequencing

The intervention strategy is selected based on misconception type AND severity AND hardening risk:

### Low hardening risk (first detection, no reactivation history)

Intervention: `inline_correction`
- Brief acknowledgment of the misconception within an ongoing explanation
- Correction delivered without breaking the pedagogical flow
- No forced retrieval; Tutor uses knowledge from retrieved content
- LES update: `corrected_provisional`, hardening_risk remains `low`

### Medium hardening risk (2–3 detections OR one reactivation)

Intervention: `causal_chain_walkthrough` (for Type 1) or `definition_anchoring` (for Type 3)
- Dedicated pedagogical act, not inline
- Forced retrieval of the relevant misconception node
- Structured step-by-step correction using the chain or definition
- Comprehension check before proceeding
- LES update: if check passed → `corrected_provisional`; if failed → `hardening_risk` increments

### High hardening risk (4+ detections OR multiple reactivations)

Intervention: `challenge_and_reconstruct`
- Full session dedicated to this misconception
- Strategy: challenge the misconception using a vivid counter-example that the student cannot ignore
- Then rebuild the correct model from first principles
- Examiner evaluation of the target concept in the same session
- LES update only after Examiner confirms correction

### SAT-context reactivation (misconception stable in theory but active in SAT)

This is the most dangerous pattern. The student has "corrected" the misconception in isolation but reactivates it under SAT performance pressure. The correction strategy:

1. Separate the theory session from the SAT session explicitly
2. In the SAT context, install a "commitment prompt": before writing the quality conclusion, force the student to state their BICL evidence first, then commit to the quality claim based on it
3. The Orchestrator monitors whether the misconception reactivates in SAT context specifically

---

## The Hardening Model

Misconception hardening is a time-dependent process. A misconception that is detected once and immediately corrected may never harden. A misconception detected at session 1, mentioned in the Tutor explanation at session 1, not followed up in sessions 2–4, and re-detected at session 5 has hardened significantly.

Hardening has two consequences:
1. The incorrect belief has been reinforced through additional use in subsequent sessions (the student has built correct knowledge on top of the incorrect foundation, making the foundation more load-bearing)
2. The student has had time to build confidence in the wrong belief — correction now requires not just providing correct information but dissolving the student's confidence in a belief they hold firmly

Hardening risk score formula:

```
hardening_risk_score = 
  (detection_count × 0.30)
  + (sessions_since_first_detection × 0.25)
  + (reactivation_count × 0.30)
  + (exam_destructive × 0.15)
```

Where:
- `detection_count`: number of sessions in which this misconception has been detected
- `sessions_since_first_detection`: total sessions elapsed since first detection
- `reactivation_count`: number of times the misconception reappeared after a provisional correction
- `exam_destructive`: binary (1 if this misconception would produce a wrong answer in the exam, 0 if it merely reduces mark quality)

Thresholds:
- 0.0–0.3: `low` hardening risk
- 0.3–0.6: `medium` hardening risk
- 0.6–0.8: `high` hardening risk
- >0.8: `critical` — Orchestrator must dedicate a full session to correction; cannot proceed with new content until resolved

---

## The 10 Most Exam-Destructive Misconceptions for WSET L3

These misconceptions are the highest-priority targets for this specific learner and this specific exam. If a tutoring system corrects only these 10 before the exam, it has done more for Nazareth's score than expanding knowledge into 5 new regions.

1. **Tannin = quality** — High tannin is a structural feature, not a quality indicator in isolation. A wine with high tannin and insufficient fruit weight has structural imbalance.

2. **Acidity = unpleasant / harsh** — Acidity is a structural component supporting freshness, food pairing, and ageability. A wine with high acidity can be beautifully balanced.

3. **Cool climate = underripe always** — Cool climate is a spectrum. A cool climate with a good vintage and a late-ripening site can produce fully ripe fruit with high acidity.

4. **More complex = higher quality (vocabulary confusion)** — "Complex" in WSET SAT means a wine showing many different, distinct aromas/flavours. It is a feature descriptor, not a quality judgment in itself.

5. **Oak = quality enhancement** — Oak is a production tool. Poorly judged oak can dominate and reduce wine quality. An unoaked wine can achieve outstanding quality.

6. **MLF is always performed** — MLF is a winemaker choice. White wines often avoid MLF to preserve freshness and acidity.

7. **Terroir means soil type** — Terroir is the complete growing environment: soil, subsoil, slope, aspect, mesoclimate, drainage. Soil type is one component.

8. **Sweet wines are low quality** — Some of the most celebrated and expensive wines in the world are sweet (Sauternes, TBA Riesling, Tokaji Aszú). Sweetness is a style dimension, not a quality indicator.

9. **Finish = aftertaste (vocabulary confusion)** — "Finish" in WSET SAT means the length of time flavour persists after swallowing, not the qualitative character of what remains.

10. **A well-made wine is automatically good quality** — Technical correctness (no faults) is a necessary but not sufficient condition for quality. A technically faultless wine that lacks complexity or typicality is not high quality in WSET terms.

---

## Implementation Notes

Misconception nodes in the knowledge graph (`MC_` prefix) already contain:
- `detection_signals`: array of strings that match student input patterns
- `severity`: as-designed scale
- `intervention_type`: pre-specified per node
- `corrected_understanding`: the target belief state after correction

The implementation requires:
1. A pre-pass function that runs before every Tutor response, matching student input against all `detection_signals` arrays
2. The Orchestrator using the pre-pass result to redirect the session plan when a match is found
3. The LES misconception registry tracking detection history and hardening risk
4. A forced retrieval path that bypasses scoring when a misconception node is flagged

The pre-pass is string matching, not vector search. It is fast and deterministic. The cost of a false positive (matching a misconception signal that wasn't a real misconception) is low — the student receives a brief correction and then proceeds. The cost of a false negative (missing a misconception) is high — the student's wrong belief remains active. The detection threshold should be set to high recall.

---

*Generated: 2026-05-15 | Cognitive Architecture Design Series | Document 3 of 8*
*Not an official WSET document. Not for learner-facing use.*
