# PHASE Z.1A — Pedagogical Audit for Distinction

**Date:** 2026-06-10
**Perspective:** Senior WSET L3 educator / examiner trainer / instructional designer / learning scientist
**Scope:** Learning effectiveness only. No code, no architecture, no bank audits.
**Status:** Formative planning document. `safe_for_examiner = false`. Not WSET assessment.

---

## 0. Method and core finding

The audit reviews the complete learner journey (Diagnostic SBA → Adaptive Session → Open Response Lab → Full Simulation → Distinction Coach → Analytics → Weakness Engine) against two models:

- **Command Verb Matrix** (Describe/Explain/Why/How/Discuss/Assess/Evaluate/Compare/Identify-and-Explain/Outline/State/List)
- **Universal Distinction Chain:** Factor → What happens → Impact on vine → Impact on grape → Impact on wine → **Impact on quality**

**Core finding:** the platform is now excellent at *measuring* and *selecting* — it is still weak at *teaching*. Almost every learning event terminates at a verdict (correct/incorrect, concept present/absent, weakness detected) rather than at an explanation, a corrected mental model, or a scheduled re-encounter. The Distinction-critical skills — full causal chains ending in quality, command-verb-conformant production, evaluative judgement — are *checked* in several places but *trained* almost nowhere. Phase Z.1+ should convert verdicts into instruction.

One verified fact anchors this audit: **all 578 deployed SBA items carry only the correct answer key — no explanation and no distractor rationale.** The platform's highest-volume learning event is therefore verification, not learning.

---

## 1. Component-by-component analysis

### 1.1 Diagnostic SBA (578 items)

**Where learning occurs:** at the retrieval attempt itself (testing effect) and at the moment of correctness feedback. This is real but shallow learning.

**Where learning does NOT occur:**

- After an error. Feedback is right/wrong only. The learner who chose "crianza larga" instead of "adición de aguardiente" leaves with the misconception intact — and having just rehearsed a plausible distractor without refutation, which familiarity research suggests can *strengthen* the error.
- After a correct answer. No elaboration ("correct, and the mechanism is..."), so a lucky guess and stable knowledge produce identical learning (none) and identical analytics evidence.
- Across time. An item answered wrong today has no guaranteed re-encounter at day 2 / 7 / 21.

**Feedback insufficiency:** the single largest pedagogical gap on the platform. Elaborated feedback (correct-answer rationale + per-distractor refutation) is the most robust effect in the feedback literature, and it is absent from the highest-volume activity.

**Retrieval practice quality:** recognition only. SBA never demands free recall or production; Distinction is awarded on production.

### 1.2 Adaptive Session

**Where learning occurs:** in question selection — weak areas get more exposure, which raises retrieval opportunities where they matter.

**Where learning does NOT occur:**

- Adaptivity governs *what is asked*, not *what happens after an error*. The instructional response to failure is "another question," i.e. massed practice on the weak topic. Massing feels productive and produces poor retention; the spacing literature is unambiguous here.
- Coach material (`coach_data.js`) exists in the same experience but is passively available reference — it is not injected at the moment of error, which is exactly when a mentor hint has maximal effect.
- SAT Sprint/Practice/Mock modes create production opportunities, but the feedback loop (X.3/X.4/X.5 validators) checks structure and completeness — it does not coach *calibration* (is "good" vs "outstanding" justified by the cited observations?).

**Reinforcement missing:** there is reaction (more of the weak topic now) but no reinforcement schedule (the same concept at expanding intervals).

### 1.3 Open Response Lab (37 items)

**This is the best-designed learning component.** Items carry `expected_concepts`, `common_errors` (failure → correction → example), `hints`, and `optional_causal_chain` — that is genuine instructional scaffolding, not just assessment.

**Remaining gaps:**

- **Chain-completeness feedback is absent.** Concept-coverage checking verifies *presence* of concepts, not whether the answer traversed the full Distinction Chain. A Merit-level answer typically stops at "impact on wine"; the Distinction answer reaches "impact on quality" and commits to a judgement. The system cannot currently say: *"You stopped one link short."* This is the single most Distinction-specific feedback the platform could give, and the causal-chain nodes to power it already exist.
- **No contrastive exemplars.** Learners never see an annotated Pass answer next to an annotated Distinction answer to the same stem. Distinction is a *register* learners must perceive before they can produce it; contrast is how registers are learned.
- **Volume and verb coverage.** 37 items cannot cover 12 command verbs × major domains. Evaluate/Assess/Discuss — the verbs that decide Distinction — are almost certainly under-represented relative to Describe/Explain.
- **No timed planning practice.** Distinction candidates differ from Merit candidates most visibly in the first 90 seconds: skeleton selection by command verb. This is never drilled in isolation.

### 1.4 Full Simulation

**Where learning occurs:** test-taking stamina, time allocation, format familiarity. Legitimate, but a simulation is an *assessment* event; learning happens in the debrief — and there is no structured debrief.

**Missing:**

- **Post-mortem error taxonomy.** Every simulation error should be classified: (a) knowledge gap, (b) command-verb misread (explained when asked to describe; described when asked to evaluate), (c) incomplete causal chain, (d) structure/ordering failure, (e) time mismanagement. These five failure modes have five different remedies; without the taxonomy, the learner only learns "I got 62%."
- **No closed loop.** Simulation errors do not visibly seed the Weakness Engine's next two weeks of practice. The most diagnostic data the platform ever collects is currently its least exploited.

### 1.5 Distinction Coach

**Where learning occurs:** marginally. The command-verb content (definitions, do/do-not, mentor hints) is accurate and well-written — but it is *reference material*, and reference material is read once, nodded at, and not encoded.

**Missing — this is knowledge that must become training:**

- **Verb-identification drills:** show a stem, learner names the verb's demanded structure in <10 seconds. (Maps directly onto the Command Verb Matrix.)
- **Transformation drills:** same content, different verb — "Describe MLF" vs "Explain how MLF affects style" vs "Evaluate the decision to use MLF in a cool-climate Chardonnay." Nothing teaches verb sensitivity faster.
- **Contextual injection:** when a learner's open response fails on verb conformity, the relevant coach card should appear *at that moment*, not live in a separate tab.

### 1.6 Performance Analytics

**Where learning occurs:** indirectly, via self-regulation — if the learner reads dashboards correctly.

**Missing:**

- **Prescription.** Analytics says "fortified_wines is fragile"; it does not say "re-study Chapter 24 §Oloroso, then take this 5-item drill, then re-test Friday." Measurement without prescription transfers the instructional-design burden to the learner — precisely the skill a struggling learner lacks. Chapter recommendations are entirely missing from the journey.
- **Calibration data.** Without confidence ratings at answer time, analytics cannot distinguish confident error (misconception — dangerous) from unconfident error (gap — benign), nor lucky guess from mastery. This contaminates every downstream estimate the Weakness Engine consumes, and forfeits the hypercorrection effect (high-confidence errors, once corrected, are the *best*-retained corrections).

### 1.7 Adaptive Weakness Engine

**Where learning occurs:** in directing effort toward weakness — necessary but not sufficient.

**Missing:**

- **A forgetting model.** The engine is reactive (weak now → practice now), not prospective (correct now → re-test at day 2, 7, 21). Without expanding-interval scheduling, "remediated" topics silently decay and the learner discovers this in the Full Simulation, the worst possible place.
- **Misconception re-verification.** The backend treats misconceptions as cognitive objects (correct), but a corrected misconception is never deliberately re-tested after a delay. One-shot correction of a strong misconception has a high relapse rate; the correction must be confirmed twice, spaced.
- **Interleaving discipline.** Weakness-driven selection tends to block by topic. Discrimination between confusable regions/styles (Distinction's bread and butter: Mosel vs Alsace Riesling, Fino vs Oloroso logic) is built by *interleaved* practice.

---

## 2. Gap matrix (requested dimensions)

| Dimension | Current state | Severity for Distinction |
|---|---|---|
| Feedback sufficiency | SBA: verdict-only (no explanations on any of 578 items). OR Lab: good. SAT: structural only | **Critical** |
| Retrieval practice | Recognition-heavy; free recall / production under-used | High |
| Reinforcement | Reactive repetition, no schedule | High |
| Spaced repetition | Absent everywhere | **Critical** |
| Command-verb coaching | Good reference content, zero drilling, no contextual injection | High |
| SAT coaching | Structure/readiness/ordering validated; calibration & justification quality uncoached | High |
| Chapter recommendations | Absent | Medium-High |
| Misconception correction | Detected and intervened once; never re-verified after delay | High |
| Causal-chain training | Chains are *shown* to the learner (CAUSA/MECANISMO/EFECTO), never *built by* the learner | **Critical** |
| Distinction-specific guidance | No contrastive exemplars; no chain-completeness feedback; no judgement-commitment coaching | **Critical** |
| Interleaving | Not deliberately engineered | Medium |
| Calibration / metacognition | No confidence capture; no calibration feedback | Medium-High |

---

## 3. Question 1 — What is missing for Pass → Merit?

Pass → Merit is a *knowledge consolidation* problem: more facts, retained longer, retrieved more reliably. The missing pieces:

1. **Elaborated SBA feedback** — every error must end in a corrected mental model, not a red X. Per-distractor refutation converts 578 assessment items into 578 micro-lessons.
2. **Spaced re-exposure** — failed items/concepts return at expanding intervals automatically.
3. **Chapter prescriptions** — weakness → named study unit → drill → re-test, as an explicit loop.
4. **Free-recall moments** — e.g. "answer in your head / one written line *before* options reveal." Cheap, and converts recognition practice into recall practice.
5. **Misconception delayed re-test** — corrected once ≠ corrected.

A learner using the current platform intensively will reach Merit mostly through volume. These five make the path reliable instead of effortful.

## 4. Question 2 — What is missing for Merit → Distinction?

Merit → Distinction is a *production and judgement* problem, not a knowledge problem. The Merit candidate knows the facts; the Distinction candidate organizes them into complete causal chains, in the structure the command verb demands, ending in a committed quality judgement. Missing:

1. **Causal-chain construction practice (generation).** Today the system renders chains *to* the learner. The generation effect requires the reverse: present "Factor: high diurnal range" and demand the learner build vine → grape → wine → quality. Fill-the-missing-link, order-the-shuffled-chain, and complete-the-final-link exercises — all generatable from the existing 14 CC_*/HC_* nodes with zero new content authoring.
2. **Chain-completeness feedback in open responses.** Explicitly flag "you reached impact-on-wine; Distinction requires impact-on-quality." This names the precise behavioral difference between Merit and Distinction scripts.
3. **Contrastive exemplars.** Annotated Pass vs Merit vs Distinction answers to identical stems. Until the learner can *see* the difference, they cannot produce it.
4. **Command-verb production drills** (identification + transformation, §1.5). The classic Distinction-loss pattern is answering a different verb than the one asked.
5. **Evaluative-judgement training.** Have the learner *mark sample answers* against `expected_concepts` and the chain model, then compare with system labels. Learning to see like a marker is the fastest route to writing like a Distinction candidate, and the platform already owns all required assets.
6. **SAT calibration coaching.** Beyond structure: does the cited evidence *entitle* the quality level chosen? Train the acceptable/good/very good/outstanding boundary with commitment language.

## 5. Question 3 — The 10 highest-impact pedagogical improvements

| # | Improvement | Primary mechanism | Impact | Content effort |
|---|---|---|---|---|
| 1 | Elaborated feedback on all 578 SBA items (rationale + per-distractor refutation, written in Factor→Consequence register) | Elaborated feedback; misconception refutation | Very high | High (content-only, batchable, top-failure items first) |
| 2 | Chain-completeness feedback in OR Lab + SAT ("one link short of quality") | Distinction-defining discrimination | Very high | Low — chains and expected_concepts already exist |
| 3 | Causal-chain construction exercises from existing CC_*/HC_* nodes | Generation effect | Very high | Low-Medium |
| 4 | Command-verb micro-drills (identify, skeleton-select, transform) from existing coach_data | Transfer-appropriate processing | High | Low |
| 5 | Spaced repetition layer in Weakness Engine (expanding intervals; misconception re-verification) | Spacing; hypercorrection follow-up | Very high | Medium |
| 6 | Contrastive exemplar library (Pass/Merit/Distinction annotated answers, start with 10 stems) | Perceptual contrast; register acquisition | High | Medium |
| 7 | Confidence ratings on SBA + calibration feedback | Metacognition; analytics de-noising | Medium-High | Low |
| 8 | Structured Full Simulation debrief with 5-way error taxonomy feeding the Weakness Engine | Deliberate practice loop closure | High | Medium |
| 9 | Chapter/study-unit prescriptions from analytics (weakness → reading → drill → re-test) | Self-regulated learning support | Medium-High | Medium |
| 10 | OR bank expansion to ~80 items on a deliberate verb × domain coverage matrix (Evaluate/Assess/Discuss prioritized) | Production volume on Distinction verbs | High | High |

## 6. Questions 4 & 5 — Sequencing and gain-per-effort

**Highest learning gain per unit of effort** (leverage existing assets, content-light):

1. **#2 chain-completeness feedback** — the platform already knows the chains; it only needs to say "incomplete."
2. **#4 verb micro-drills** — coach_data.js already contains the curriculum.
3. **#7 confidence ratings** — one extra click per item; improves every downstream estimate.
4. **#3 chain construction** — 14 existing nodes become a full exercise type.

**Recommended order:**

- **Wave 1 (immediately):** #2, #4, #7. All reuse existing assets; all visible to Nazareth within days of effort.
- **Wave 2 (core Distinction engine):** #3, #6, and begin #1 with the 50 highest-failure-rate SBA items (analytics already knows which ones).
- **Wave 3 (retention infrastructure):** #5, #8 — these compound everything above; without #5, gains from Waves 1–2 decay.
- **Wave 4 (volume):** complete #1 across the bank; #9; #10.

**Single most important sentence of this audit:** before authoring any new item, give the existing 578-item SBA bank explanations and the existing OR/SAT pipeline chain-completeness feedback — the platform already contains nearly all the knowledge needed for Distinction; what it lacks is the moment where that knowledge is handed to the learner *as instruction, at the moment of error, with a scheduled return visit*.

---

*Formative planning document. No examiner authority. safe_for_examiner = false.*
