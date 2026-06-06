# Open Response Pool Audit
**Date:** 2026-06-05  
**Phase:** Parallel Track B — Pedagogical Brain  
**Status:** Complete — audit only, no data modified

---

## 1. Pool Summary

| Category | Count | IDs |
|---|---|---|
| Total candidates | 20 | 18, 798–817 |
| Rejected (structural) | 1 | 18 |
| Approved + held | 2 | 807, 809 |
| Active pool | 18 | 798–806, 810–817 (minus 807/809) |
| All activation_status | inactive | — |

All 20 entries carry clean governance flags (`safe_for_examiner=False`, `examiner_scoring_allowed=False`, `training_item_only=True`).

---

## 2. Rejected Question — ID 18

**Stem:** "¿Cuál es una consecuencia del uso excesivo de sulfitos?"  
**Rejection reasons (from review record):**
- Missing RA metadata
- Missing causal metadata
- Missing corpus chunk support (`corpus_support.status: "missing"`)
- SBA source carried answer/options residue (structural anomaly)

**Status:** Hold indefinitely. Do not include in any pool or activation plan until all 4 issues are resolved via a new review cycle. The source question (`wset3_questions.json` ID 18) appears to be an MCQ repurposed without normalization — the stem is too short/narrow for open response and its knowledge domain (SO₂ excess) has weak causal chain coverage in the current corpus.

**Recommendation:** This question should be reclassified as a short-answer MCQ adjunct, not a full open response. If retained, it needs: (a) RA1 verification, (b) causal link "sulfitos → SO₂ → aromas reductivos" mapped to a causal chain node, (c) at least 2 corpus chunks with direct evidence, (d) explicit SBA residue removal.

---

## 3. Held Questions — 807 and 809

These passed structural review (all checklist items ✓) but are pedagogically risky for the first Open Response Lab.

### ID 807 — Riego + manejo del dosel en sequía/calor extremo

**Stem:** "Explique cómo el riego y el manejo del dosel pueden reducir los efectos de la sequía o del calor extremo sobre la maduración de la uva."  
**Difficulty:** distinction  
**Pedagogical risk:**
- Compound question requiring simultaneous integration of two management strategies. Learner can give a valid partial answer (only irrigation, or only canopy management) that is technically correct but incomplete.
- A formative feedback engine must handle partial coverage gracefully without implying "you scored 1 out of 2 points" — which approaches examiner scoring territory.
- The stem's phrase "reducir los efectos" creates an implicit outcome-evaluation expectation that is harder to satisfy with formative feedback than a purely explanatory question.

**Verdict:** HOLD until the feedback engine has been designed to handle compound-coverage gracefully. Do not promote before `feedback_engine_v1` is defined and the partial-coverage response class is explicitly handled in the rubric.

### ID 809 — Levaduras seleccionadas vs autóctonas (compare)

**Stem:** "Compare el uso de levaduras seleccionadas y levaduras autóctonas en fermentación, considerando control, consistencia, complejidad potencial y riesgos."  
**Difficulty:** distinction  
**Pedagogical risks:**
1. **Near-duplicate:** ID 803 ("Explique la influencia de la elección de levaduras en el perfil sensorial del vino") is already in the pool and covers the same domain. Two yeast questions in the same lab session would over-represent this topic.
2. **Four-axis comparative format** (control / consistencia / complejidad / riesgos): Any feedback system must address all 4 axes. If the system marks coverage on each axis, it functions as a scoring rubric — which is examiner scoring in disguise.
3. **Examiner authority creep risk:** A learner who mentions 2 of 4 axes would receive implicit partial-credit feedback. Without a governing design decision about how many axes are "enough," feedback drift is likely.

**Verdict:** HOLD. Resolve the deduplication issue with ID 803 first. If both are retained, they must appear in different sessions. Revise the stem to remove the explicit 4-axis structure before activation — or redesign the rubric as formative guidance rather than axis coverage.

---

## 4. Active Pool — 18 Questions (798–806, 810–817)

### 4.1 Pool Inventory

| ID | Stem (short) | RA | Difficulty | Causal chain | Lab candidate tier |
|---|---|---|---|---|---|
| 798 | Prácticas sostenibles → costes → diferenciación | RA1 | distinction | sostenibilidad → coste → precio | Tier 1 |
| 799 | FML en vinos blancos → calidad | RA1 | distinction | maloláctica → acidez → textura | Tier 1 |
| 800 | Altitud → estilo de tinto | RA1 | intermediate | altitud → temperatura → maduración | Tier 1 |
| 801 | Orientación + pendiente → maduración | RA1 | intermediate | orientación → exposición → maduración | Tier 1 |
| 802 | Oxidación en vinos blancos (prácticas bodega) | RA1 | intermediate | oxígeno → oxidación → aromas | Tier 1 |
| 803 | Elección de levaduras → perfil sensorial | RA1 | intermediate | levadura → fermentación → aromas | Tier 1 |
| 804 | Drenaje del suelo → vigor → estilo | RA1 | intermediate | suelo → drenaje → vigor | Tier 1 |
| 805 | Roble americano vs francés → aromas + tanino | RA1 | distinction | roble americano → vainilla → perfil | Tier 1 |
| 806 | Manejo del dosel (2 técnicas) → beneficios | RA1 | intermediate | deshojado → exposición → maduración | Tier 1 |
| 810 | Estrés hídrico moderado → rendimiento → coste | RA1 | distinction | estrés hídrico → baya → concentración | Tier 2 |
| 811 | Latitud + altitud → estilo (clima cálido) | RA1 | intermediate | latitud → temperatura → maduración | Tier 2 |
| 812 | Estrés hídrico moderado → vigor → concentración | RA1 | intermediate | estrés hídrico → vigor → concentración | Tier 2 |
| 813 | Riesgo enológico de levaduras autóctonas | RA1 | foundational | levaduras autóctonas → riesgo | Tier 1 |
| 814 | Poda de invierno — justificación | RA1 | foundational | poda → yemas → rendimiento | Tier 1 |
| 815 | Beneficio técnico de fermentación en acero inox | RA1 | foundational | acero inoxidable → temperatura → aromas | Tier 1 |
| 816 | Maceración prolongada → estilo y calidad en tinto | RA1 | distinction | maceración → extracción → tanino | Tier 1 |
| 817 | Suelos arenosos vs arcillosos → agua, vigor, estilo | RA1 | intermediate | arena → drenaje → vigor | Tier 2 |

**Note:** ID 806 is included in pool (approved) despite topical overlap with held ID 807. 806 asks for 2 techniques + benefits (explanatory) while 807 asks specifically how they mitigate drought/heat (problem-solving/compound). They are distinguishable.

### 4.2 Deduplication Risks

Three near-overlap pairs exist:

| Pair | IDs | Overlap domain | Resolution |
|---|---|---|---|
| Estrés hídrico | 810 vs 812 | Mismo mecanismo (estrés hídrico → concentración), different angle (rendimiento+coste vs vigor) | Separate sessions; do not co-present |
| Levaduras | 803 vs held 809 | Domain identical | If 809 is ever unblocked, retire 803 first |
| Suelo | 804 vs 817 | Both on soil → water → vigor, different emphasis (drainage vs soil type) | Acceptable if different sessions |

### 4.3 Coverage by Difficulty

| Difficulty | Count | % |
|---|---|---|
| foundational | 3 | 17% |
| intermediate | 8 | 44% |
| distinction | 6 | 33% |

Pool is intermediate-heavy. For a Lab entry point, foundational is underrepresented. The three foundational questions (813, 814, 815) are ideal first-Lab candidates.

### 4.4 Coverage by Topic Domain

| Domain | IDs |
|---|---|
| Viticulture / vineyard | 800, 801, 804, 806, 811, 812, 814, 817 |
| Winemaking / bodega | 799, 802, 803, 810, 813, 815, 816 |
| Sustainability / commercial | 798, 808 (held) |
| Oak / maturation | 805 |

Coverage is strongly vineyard+winemaking (RA1 focus). No SAT, no fortified, no sparkling winemaking represented. This is appropriate for a first Lab but limits future breadth.

---

## 5. First Open Response Lab — Recommended Pilot Set

For a first private Lab activation (MVP, not public deployment), recommend 5–6 questions covering:
- 2 foundational (easy entry point for learner confidence)
- 2 intermediate
- 1 distinction (stretch goal)
- No near-duplicate pairs in the same session

**Recommended Tier 1 first pilot set:**

| Priority | ID | Stem (short) | Why |
|---|---|---|---|
| 1 | 814 | Poda de invierno | Foundational, single causal chain, clear expected answer, high corpus confidence |
| 2 | 815 | Fermentación en acero inox | Foundational, concrete, unambiguous concepts |
| 3 | 813 | Riesgo de levaduras autóctonas | Foundational, triggers causal reasoning without comparative complexity |
| 4 | 800 | Altitud → estilo de tinto | Intermediate, well-covered by corpus (3 diverse chunks), clean causal chain |
| 5 | 802 | Oxidación en vinos blancos | Intermediate, practical domain, strong corpus support, good for misconception detection |
| 6 (stretch) | 799 | FML en vinos blancos | Distinction, rich causal chain, tests whether learner links acid → texture mechanistically |

Questions to reserve for Lab v2: 805 (oak comparison), 816 (prolonged maceration), 798 (sustainability), 811/812 (altitude/water stress variants).

---

## 6. Rubric Quality Assessment

All 18 pool questions share the same `feedback_rubric` object:
```json
{
  "concept_coverage": "expected_concept_presence",
  "causal_link": "formative_causal_link_presence",
  "formative_feedback": "training_guidance_only",
  "needs_review": "derived_from_missing_or_partial_concepts"
}
```

This is a **placeholder rubric** — a governance type declaration, not an operational rubric. It declares *that* concept coverage and causal link presence will be checked, but does not define:
- What constitutes acceptable concept coverage (threshold? any 3 of 10?)
- How the causal link is detected (substring? semantic match?)
- What formative feedback text to generate for each gap
- What remediation path to trigger for `needs_review`

This is the primary gap between current state and Open Response Lab readiness. See `docs/PEDAGOGICAL_FLOW_ARCHITECTURE.md` for the operational rubric design.

---

## 7. What Needs to Happen Before Lab Activation

1. **Feedback engine design** (see `docs/PEDAGOGICAL_FLOW_ARCHITECTURE.md`)
2. **Operational rubric per question** — specify the concept coverage threshold for each pilot question
3. **Causal detection logic** — define how the system detects presence of the causal chain in a free-text response
4. **Formative feedback templates** — per gap type (missing concept, missing causal link, partial coverage)
5. **Remediation map** — which Tutor topics to surface for each detected gap
6. **Resolve 807/809** — design decisions documented before touching those questions

---

*Governance: no code modified, no scoring added, no data altered. Audit only.*
