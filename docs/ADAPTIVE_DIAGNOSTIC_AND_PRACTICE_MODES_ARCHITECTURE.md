# Adaptive Diagnostic & Practice Modes — Architecture
**Date:** 2026-06-05  
**Phase:** 4A.3.8.0  
**Status:** v1 — pedagogical contract; no code, no frontend

---

## Purpose

This document defines the pedagogical architecture for how the WSET-AI-System selects, sequences, and adapts questions from the Master Bank according to each learner's current understanding profile, available time, and practice goal. It covers five distinct practice modes, the signals used to estimate understanding, and the mechanisms that prevent frustration, examiner-authority creep, and official-scoring patterns.

This is a **contract for cognition**, not for infrastructure. It answers: *what should the system think before presenting each question?*

---

## 0. Foundational Constraints

These constraints govern every decision in every mode. They are not negotiable.

**No scoring authority.** The system never assigns marks, percentages, grades, or pass/fail outcomes. It produces understanding signals and learning recommendations — nothing else.

**No IQ or intelligence language.** The system never characterizes a learner as "smart", "weak", "advanced", or any cognitive-ability descriptor. It describes *what has been covered* and *what hasn't*, not the learner's capability.

**No official WSET criteria.** The system does not calibrate against WSET exam passing thresholds, mark schemes, or grade boundaries. All difficulty calibration is internal to the system's own schema.

**Deterministic by default.** Where the system must make a selection, it follows a defined rule. It does not select randomly. Pseudo-random tie-breaking is allowed only when all ranked candidates are strictly equivalent.

**LES is the memory.** All understanding signals live in the Learner Epistemic State. No session logic is stateful in isolation — every decision reads from and writes back to LES.

---

## 1. The Learner Profile — What the System Knows

Before composing any session, the system reads the current LES and constructs a **Learner Profile**. The profile is a derived object — computed at session start, never stored persistently (it is always re-derived from LES).

### 1.1 Per-topic understanding signal

For each WSET L3 topic, the system computes a `topic_signal` from LES data:

| Signal | Meaning | LES evidence |
|---|---|---|
| `unvisited` | No interaction with this topic | No exposure record |
| `introduced` | Seen at least once; low concept coverage detected | `topic_exposure_count ≥ 1`, `concept_gap` non-empty |
| `developing` | Consistent partial coverage; improving over sessions | `topic_exposure_count ≥ 2`, concept gaps decreasing |
| `consolidating` | High concept coverage but causal chain not yet articulated | High `present_concepts` ratio, `causal_gap` set |
| `strong` | High concept coverage + causal chain articulated consistently | No active `concept_gap` or `causal_gap` for this topic |

**How signal is estimated:**
- `concept_gap` flags: presence means a specific term was absent in ≥2 recent responses on this topic
- `causal_gap` flags: presence means the causal chain for this topic was not articulated in ≥2 recent sessions
- `topic_exposure_count`: raw count of sessions where this topic appeared
- `misconception_triggered`: any misconception node that fired in prepass or distractor analysis for this topic

Signal transitions are **conservative** — the system moves a topic from `developing` to `consolidating` only after 2 consistent partial-coverage outcomes, not after 1. This prevents false confidence inflation.

Signal is **never surfaced to the learner as a label or score.** It is internal routing metadata only.

### 1.2 Per-RA mastery signal

Each WSET L3 RA (RA1–RA4) covers multiple topics. RA mastery is a **distribution summary** over the `topic_signal` values within that RA.

| RA Signal | Composition rule |
|---|---|
| `cold_start` | Majority of topics in RA are `unvisited` |
| `partial` | Mixed — some topics `developing` or stronger, some `unvisited` |
| `developing` | Majority of topics at `introduced` or `developing`; few `strong` |
| `consolidating` | Majority at `consolidating`; few `strong`; few `unvisited` |
| `strong` | Majority at `strong`; minimal active gaps |

RA mastery is used for: Focused Practice target selection, RA Focus mode, and Full Diagnostic RA weighting.

### 1.3 Active gap inventory

Three gap types are extracted from LES at session start:

**Concept gaps** — specific terms never or rarely detected in responses:
```
concept_gaps = [concept_name for concept_name where concept_gap[concept_name] = true]
```

**Causal gaps** — causal chain structures not yet articulated:
```
causal_gaps = [chain_id for chain_id where causal_gap[chain_id] = true]
```

**Active misconceptions** — misconception nodes that have fired recently:
```
active_misconceptions = [node_id from misconception_triggered within last N sessions]
```

These three lists form the **gap inventory** used for Review Mistakes mode and gap-targeting in all other modes.

### 1.4 Session history (anti-repeat)

For each question in the bank, the system reads:
- `last_seen_date`: when the question was last presented to this learner
- `times_seen`: how many times the learner has seen this question

A question is **cooling down** if:
- Foundational: seen within the last 7 days
- Intermediate: seen within the last 14 days
- Distinction: seen within the last 21 days

Cooling-down questions are excluded from candidate selection unless the available pool has fewer eligible candidates than the session requires. In that case, cooldown relaxation follows this order: foundational cooldown relaxed first, then intermediate, then distinction.

---

## 2. Proficiency and Difficulty Calibration

### 2.1 Initial difficulty decision

At the start of any session, for each RA or topic targeted, the system selects a **starting difficulty** based on the current `topic_signal`:

| Topic signal | Starting difficulty |
|---|---|
| `unvisited` | foundational |
| `introduced` | foundational |
| `developing` | intermediate |
| `consolidating` | intermediate |
| `strong` | distinction |

Cold start (no LES data at all): start all topics at `foundational`.

This is the **initial calibration point**. It is adjusted dynamically within the session as the learner responds.

### 2.2 In-session difficulty progression

The system maintains a **per-topic difficulty cursor** during a session. The cursor starts at the initial difficulty and moves based on response quality.

**Ramp-up rule** (increase difficulty):
- After 2 consecutive `strong_response` outcomes on the same topic → advance cursor one tier
- `foundational → intermediate → distinction`
- Maximum rate: one tier per 2 questions

**Ramp-down rule** (reduce difficulty):
- After 2 consecutive `weak_response` outcomes on the same topic → retreat cursor one tier
- `distinction → intermediate → foundational`
- Minimum difficulty: foundational (never goes below)

**Hold rule** (no change):
- After 1 `strong_response`: hold — do not ramp up yet; confirm with a second question
- After 1 `weak_response`: hold — do not ramp down yet; present another question at same difficulty on a different subtopic
- After `partial_response` or `incomplete`: hold; same difficulty, same topic or adjacent topic

**Cross-topic transitions:** when switching to a new topic within a session, reset the cursor to the `topic_signal`-derived initial difficulty for that topic. Do not carry the cursor from a previous topic.

### 2.3 Frustration prevention

The system monitors for **frustration patterns** — sequences of responses that suggest the learner is hitting a persistent wall.

**Frustration trigger:**
- 3 or more consecutive `weak_response` or `incomplete` outcomes across any topics in the session

**Response to frustration:**
- Do NOT present another question immediately
- Generate a **Tutor recommendation**: suggest the learner explore the relevant topic in the Tutor before continuing
- Pause the difficulty cursor — do not ramp further down
- When the session resumes (if learner continues), present a foundational question on a *different topic* within the same RA before returning to the frustrating domain

**What does NOT happen when frustration fires:**
- No message of the form "you are struggling"
- No message of the form "this topic seems hard for you"
- No difficulty reduction communicated to the learner
- No score displayed

The system simply changes the question selection and offers a learning resource. It does not editorialize about the learner's state.

### 2.4 Confidence without complacency

When the learner is performing well (3+ consecutive `strong_response`), the system:
- Advances to distinction-level questions
- Introduces adjacent topics not yet covered in this session
- Introduces questions with multi-step causal chains (distinction difficulty, `optional_causal_chain` with 3 nodes)

But the system does NOT:
- Say "excellent work" or any praise that could imply scoring
- Mark the learner as "done" with a topic after a strong session (understanding requires revisitation)

After 3 strong responses on one topic, the cursor is at distinction and stays there for that topic for the rest of the session.

---

## 3. The Five Practice Modes

### Mode 1: Quick Practice — 10 Questions

**Purpose:** Rapid reinforcement of recent gaps. Ideal after a Tutor session or as a daily warmup. Short enough that a learner does not need to commit to a deep engagement.

**Question count:** 10

**Time estimate (internal, not shown to learner):** ~8–12 minutes (SBA average ~45s per question; OR average ~2–3 minutes)

**Composition rules:**
| Difficulty | Target count | Tolerance |
|---|---|---|
| foundational | 3 | ±1 |
| intermediate | 5 | ±1 |
| distinction | 2 | ±1 |

**Topic selection:**
1. Priority 1 — topics with active `concept_gap` or `causal_gap` (up to 4 questions)
2. Priority 2 — topics at `introduced` signal not seen in last 7 days (up to 4 questions)
3. Priority 3 — topics at `developing` signal (fill remaining slots)
4. No topic may appear more than 2 times in the session

**RA balance:** no more than 4 questions from any single RA.

**Format mix:** primarily SBA (8 questions), up to 2 Open Response if Open Response is enabled and the learner has ≥1 prior OR session. If OR is not yet enabled: 10 SBA.

**Adaptive behavior:** cursor active, but with a gentler ramp (requires 3 consecutive strong responses to advance, 3 consecutive weak to retreat — one extra confirmation step vs default).

**LES update:** writes `topic_exposure_count`, `concept_gap` updates, `causal_gap` updates per question outcome. Does NOT write a session-level "score" or "performance summary".

---

### Mode 2: Focused Practice — 25 Questions

**Purpose:** Sustained reinforcement of the learner's weakest RA. Designed for a dedicated study session targeting a specific curriculum area.

**Question count:** 25

**Target RA selection:**
- If learner specifies an RA → use that RA
- If learner does not specify → use the RA with the weakest `RA_mastery_signal` (in order: `cold_start` > `partial` > `developing`)
- If all RAs are equal → use the RA with the largest active `concept_gap` inventory

**Composition rules:**
| Difficulty | Target count | Tolerance |
|---|---|---|
| foundational | 5 | ±1 |
| intermediate | 13 | ±2 |
| distinction | 7 | ±1 |

**Topic selection within target RA:**
- Every topic in the target RA must be represented at least once if the question pool allows
- Topics with active gaps are presented before gap-free topics at the same difficulty
- Topics at `unvisited` are presented at foundational first regardless of cursor position

**Misconception targeting:** if active misconceptions exist within the target RA, the session must include at least 2 questions whose topic directly maps to those misconceptions. These questions are selected from the misconception-distractor bank in SBA format.

**Format mix:** 3:1 SBA:OR ratio (≈19 SBA, ≈6 OR) when OR is enabled. When OR is not enabled: 25 SBA.

**Adaptive behavior:** full cursor with default ramp rules (see §2.2).

**Frustration handling:** after 3 consecutive weak responses within the target RA → recommend Tutor on the specific topic, then pivot to a *different topic within the same RA* before returning.

**LES update:** full per-question write-back + an RA-level summary entry in pedagogical_memory noting which topics were covered and the dominant gap pattern detected.

---

### Mode 3: Full Diagnostic — 50 Questions

**Purpose:** A comprehensive, cross-curriculum diagnostic sweep. Produces the most complete LES refresh. Appropriate at the start of a study period or when returning after a break.

**Question count:** 50

**RA blueprint:**
The 50 questions must follow a curriculum-proportional distribution. Until a formal WSET L3 blueprint is defined in the system, use this default:

| RA | Description | Target questions | Tolerance |
|---|---|---|---|
| RA1 | Wine production factors | 20 | ±3 |
| RA2 | Wines of the world | 16 | ±3 |
| RA3 | Sparkling & fortified | 8 | ±2 |
| RA4 | SAT & quality assessment | 6 | ±2 |

*(Blueprint constants should be extracted to `knowledge/config/diagnostic_blueprint.json` — see Codex contract §7)*

**Composition rules:**
| Difficulty | Target % | Approx count |
|---|---|---|
| foundational | 20% | 10 |
| intermediate | 50% | 25 |
| distinction | 30% | 15 |

**Ordering logic:**
- Within each RA block, questions are ordered: foundational first, then intermediate, then distinction
- RA blocks are interleaved, not presented as contiguous blocks (to reduce topic-fatigue)
- Interleaving pattern: RA1-question, RA2-question, RA3-question, RA4-question, repeat

**Topic coverage within each RA:**
- Aim for ≥70% of topics in each RA to have at least 1 question
- Prioritize `unvisited` and `introduced` topics over `strong` topics
- Topics at `strong` signal may be skipped or represented at distinction level only (to avoid redundancy)

**Gap targeting:** all questions targeting active `concept_gap` or `causal_gap` entries are included in the selection pool at higher priority than their difficulty tier alone would suggest.

**Format mix:** 2:1 SBA:OR (≈34 SBA, ≈16 OR) when OR is fully enabled. Default fallback when OR not enabled: 50 SBA.

**Adaptive behavior:** full cursor active per topic; RA-level difficulty progression is independent (performing well on RA1 does not advance the RA2 cursor).

**LES update:** full per-question write-back. Additionally, writes a `full_diagnostic_run` entry to `pedagogical_memory` with: timestamp, RA coverage achieved, dominant gaps per RA, misconceptions encountered, and any frustration events.

**Duration note (internal):** ~40–60 minutes. The session should be designed to be completable in segments — if interrupted, the system should preserve per-question state so the session can be resumed.

---

### Mode 4: RA Focus Mode

**Purpose:** Deep practice within a single RA. The learner explicitly selects which RA to target. This mode does not attempt full curriculum coverage — it goes deep on one area.

**Question count:** configurable (default 15; learner or system can specify 10–30).

**Target RA:** always learner-specified or explicit. The system never selects the RA for this mode — the learner must own the choice.

**Composition:**
Calibrated to detected mastery within the target RA:

| RA mastery signal | Foundational | Intermediate | Distinction |
|---|---|---|---|
| `cold_start` | 40% | 50% | 10% |
| `partial` | 25% | 50% | 25% |
| `developing` | 15% | 50% | 35% |
| `consolidating` | 10% | 40% | 50% |
| `strong` | 5% | 35% | 60% |

**Topic coverage:** every topic within the target RA with a non-`strong` signal must receive at least 1 question.

**Misconception priority:** any misconception nodes mapped to the target RA are presented early in the session (first 5 questions).

**Format mix:** 1:1 SBA:OR when OR is enabled and the learner has prior OR experience. The deeper engagement of OR is particularly valuable in RA Focus because the learner is deliberately committing time to one area.

**Adaptive behavior:** full cursor. In RA Focus, the cursor can advance aggressively — if a learner is at `strong` on a topic, the system immediately presents distinction questions and may introduce adjacent topics at the edges of the RA.

**Session extension:** if the learner completes the default 15 questions with all `strong_response` outcomes (no gaps detected), the system may offer to extend by 5 questions targeting distinction-level material in the RA. This is an invitation, not an automatic extension.

---

### Mode 5: Review Mistakes Mode

**Purpose:** Targeted remediation based on what the system has observed across prior sessions. Addresses concept gaps, causal gaps, and active misconceptions directly.

**Question count:** variable; minimum 5, maximum 20. The count is determined by the size of the active gap inventory, not by a fixed target.

**Candidate pool construction:**
The system assembles the candidate pool in three layers:

Layer A — direct concept gap questions:
- Questions whose `expected_concepts` contains ≥1 term from the active `concept_gaps` list
- All difficulties; no difficulty filter at this stage

Layer B — causal gap questions:
- Questions whose `optional_causal_chain` matches an active `causal_gap` chain ID
- Prefer intermediate and foundational

Layer C — misconception-targeted questions:
- Questions whose topic maps to an `active_misconception` node
- Include the corresponding misconception-distractor SBA question if available

**Selection order within the session:**
1. Present Layer A questions at foundational difficulty first (concept grounding before causal structure)
2. Advance to Layer B questions (causal chain engagement)
3. Close with Layer C questions (misconception confrontation)

**Difficulty calibration in this mode:**
- Start at `foundational` regardless of general proficiency signal
- This is deliberate: the learner is revisiting areas of difficulty; starting gentle prevents compounding frustration
- Ramp up only after 2 consecutive `strong_response` per concept area

**Format:** primarily SBA (faster feedback loop for misconception correction). Open Response may be included for Layer B (causal gap) questions — a causal gap is best addressed by having the learner articulate the chain in their own words.

**What this mode does NOT do:**
- It does not tell the learner "you got this wrong before"
- It does not reference prior sessions, scores, or performance history
- The learner simply receives questions in a relevant domain; the system does not narrate why those questions were chosen

**LES update:** same as other modes. Additionally, when a concept gap is successfully addressed (gap-related concept now detected in response), the gap flag is cleared.

---

## 4. SBA and Open Response Integration

The two question formats serve different pedagogical functions and are deliberately interleaved rather than segregated.

### 4.1 Functional difference

| Format | Primary function | Feedback speed | Causal depth |
|---|---|---|---|
| SBA | Concept detection from distractor choice; misconception confrontation | Immediate | Surface (correct/incorrect option signals concept presence) |
| Open Response | Causal chain articulation; deeper concept coverage; misconception via absence | Slow (requires processing) | Deep (causal chain in free text) |

### 4.2 Interleaving rules

**Default ratios by mode (when OR is enabled):**

| Mode | SBA | Open Response |
|---|---|---|
| Quick Practice | 8 | 2 |
| Focused Practice | 19 | 6 |
| Full Diagnostic | 34 | 16 |
| RA Focus | 1:1 (7–8 each for 15q) | — |
| Review Mistakes | 3:1 SBA:OR | — |

**Placement rules within a session:**
- Open Response questions should not be the first question in a session (SBA provides faster initial calibration)
- Open Response questions should not be consecutive unless the session explicitly targets deep causal engagement (RA Focus mode at `strong` mastery)
- After an OR question, always follow with ≥1 SBA question before the next OR question
- Never present an OR question on a topic the learner has not encountered in this session or LES (OR requires prior activation of the concept)

### 4.3 LES signal integration

SBA outcome → writes to LES via:
- Distractor selection → infers concept presence or absence
- Misconception-distractor selection → fires `misconception_triggered` flag
- `strong_response` → `topic_exposure_count++`

OR outcome → writes to LES via:
- `present_concepts` → clears matching `concept_gap` entries
- `chain_class` → updates `causal_gap` flag
- `promotion_class` → informs `topic_signal` update

The signals are additive, not competing. An SBA `strong_response` on topic X and an OR `strong_response` on topic X in the same session both contribute to the `topic_signal` update. The signal update is conservative: both must be `strong_response` in the same session to advance from `developing` to `consolidating`.

---

## 5. Master Bank Usage — Beyond the Gold Bank

The Gold Bank (questions at `gold_candidate` or `active_lab` level) is the most reliable pool: every question has an operational rubric, a human review, and corpus grounding. But restricting all modes to the Gold Bank would severely limit coverage, especially in under-represented RAs.

### 5.1 Pool eligibility by mode

| Mode | Eligible question levels |
|---|---|
| Quick Practice | `gold_candidate`, `active_lab` |
| Focused Practice | `gold_candidate`, `active_lab`, `human_reviewed` (corpus verified) |
| Full Diagnostic | `gold_candidate`, `active_lab`, `human_reviewed` |
| RA Focus | `gold_candidate`, `active_lab`, `human_reviewed`, `corpus_supported` (gap-fill only) |
| Review Mistakes | `gold_candidate`, `active_lab` only (requires operational rubric for accurate gap feedback) |

**Rationale for progressive unlocking:**
- Quick Practice and Review Mistakes require accurate gap detection → need operational rubric → Gold Bank only
- Focused Practice and Full Diagnostic can tolerate less-refined feedback for non-gap questions → `human_reviewed` acceptable
- RA Focus can accept `corpus_supported` questions as gap-fill when Gold Bank coverage for a specific RA topic is thin — but these questions deliver no operational rubric feedback, only basic concept exposure

### 5.2 `corpus_supported` questions in RA Focus — handling without operational rubric

When a `corpus_supported` question appears in RA Focus:
- Present as SBA only (no OR format, since OR requires an operational rubric to evaluate)
- For SBA without operational rubric: present the stem + options, record which option was selected, update `topic_exposure_count` only
- Do NOT attempt feedback that depends on expected_concepts matching (the list may not be validated)
- Mark the question as "minimally processed" in the session record

This ensures the full breadth of the Master Bank contributes to coverage, while the integrity of feedback is maintained.

### 5.3 `generated_candidate` questions — never presented

Questions at `generated_candidate` level are never presented to learners in any mode. They are in a pre-verification state and carry no reliability guarantees.

---

## 6. Question Selection Algorithm — Summary

For any mode, question selection follows this decision tree:

```
1. Build candidate pool (by mode eligibility level, RA target, topic target)
2. Remove cooling-down questions (anti-repeat rules)
3. Remove questions already presented in this session
4. Apply gap priority filter:
   - Elevate candidates whose expected_concepts or causal_chain match active gaps
5. Apply difficulty filter:
   - Restrict to candidates at or near the current difficulty cursor for each topic
6. Apply RA balance constraint (mode-specific)
7. Apply format balance constraint (SBA:OR ratio by mode)
8. Apply topic deduplication constraint (max 2 questions per topic per session)
9. Rank remaining candidates:
   - Primary sort: gap-targeted questions first
   - Secondary sort: `unvisited` topics before `introduced` before `developing`
   - Tertiary sort: alphabetical by question_id (deterministic tie-breaking)
10. Select top N candidates for the session
```

---

## 7. LES Update Contract — No Grades, No Scores

Every session writes back to LES. The contract for what CAN and CANNOT be written is absolute.

### 7.1 Allowed LES writes

```
topic_exposure_count[topic] += 1           # for each topic seen in session
concept_gap[concept_name] = true/false     # set true if absent; clear if now present
causal_gap[chain_id] = true/false          # set true if absent; clear if articulated
misconception_triggered[node_id] += 1     # increment when misconception fires
full_diagnostic_run[timestamp] = {summary} # Full Diagnostic mode only
```

### 7.2 Prohibited LES writes

The following patterns are explicitly forbidden. If an implementation attempt uses any of these, it violates the governance contract:

```
FORBIDDEN: learner_score = X
FORBIDDEN: ra_mastery_percentage = X%
FORBIDDEN: pass_status = "pass" | "fail"
FORBIDDEN: overall_proficiency = X
FORBIDDEN: exam_readiness = "ready" | "not ready"
FORBIDDEN: "performed_well_on" = [list of topics]
FORBIDDEN: any numeric aggregation of question outcomes
```

These are not fields that need to be set to null — they must not exist in the schema at all.

### 7.3 `topic_signal` derivation

`topic_signal` (introduced, developing, consolidating, strong) is **always computed at read time**, not stored. It is derived from the raw LES fields listed in §1.1. This is deliberate: if the derivation logic is updated, all historical signals update automatically. There is no persistent "score" to migrate or invalidate.

---

## 8. Mode Selection — How the Learner Chooses

The learner selects a mode explicitly. The system does not automatically assign a mode. Mode selection is not based on the learner's signal — it is based on the learner's stated goal and time.

**Suggested mode guidance (shown to learner, non-prescriptive):**

| Learner context | Suggested mode |
|---|---|
| "I have 10 minutes" | Quick Practice |
| "I want to focus on a weak area" | Focused Practice or RA Focus |
| "I'm starting a new study cycle" | Full Diagnostic |
| "I keep getting a specific type of question wrong" | Review Mistakes |
| "I want to go deep on Bordeaux/Champagne/etc." | RA Focus on the relevant RA |

**The system never says "you should do X mode" in prescriptive terms.** It surfaces suggestions framed as options, not instructions.

---

## 9. Design Gaps — Open Items Before Implementation

The following decisions remain unresolved and must be documented before Codex implements:

1. **Formal WSET L3 RA blueprint** — exact topic-to-RA mapping and question count proportions. Currently using a default estimate (20/16/8/6). Needs verification against the WSET L3 curriculum structure.

2. **`diagnostic_blueprint.json`** — the RA distribution constants should be extracted from code into `knowledge/config/diagnostic_blueprint.json`. Schema design needed.

3. **`question_exposure_log` schema** — how to store `last_seen_date` and `times_seen` per learner per question. This is a new LES sub-object. Schema change requires Codex + Claude alignment.

4. **`topic_signal` derivation logic** — the exact formula for upgrading from `developing` to `consolidating` (e.g., "2 consecutive sessions with ≥60% concept coverage and ≤1 causal gap") needs to be formally specified.

5. **Session interruption and resume** — the Full Diagnostic specifically needs a session-state persistence mechanism. Whether this lives in `session_staging.json` or a new file needs a design decision.

6. **`generated_candidate` in RA Focus edge case** — if an RA has very thin Gold Bank coverage (e.g., RA3 fortified wines), the system may still not have enough `corpus_supported` questions to fill a 15-question RA Focus session. Define the minimum pool size threshold and the fallback behavior.

7. **OR not yet enabled** — the architecture assumes a boolean "OR enabled" flag per learner. Where does this live in LES? What triggers it being set to true?

8. **"Minimally processed" question tracking** — `corpus_supported` questions used in RA Focus without an operational rubric need a usage flag so they don't re-enter as if they had full feedback capability.

---

## 10. What Codex Must NOT Build

| Prohibited | Why |
|---|---|
| A "difficulty level" shown to the learner | Implies scoring / ranking |
| A "session score" or "accuracy rate" | Examiner authority |
| An "exam readiness meter" or progress bar toward exam | Implied official assessment |
| Automatic mode assignment based on signal | System should surface options, not prescribe paths |
| A "streak" or "XP" gamification layer | Not appropriate for exam-adjacent system |
| Comparison of two learners' signals | Not a competitive tool |
| "You are ready for the exam" messaging | Examiner authority — absolutely forbidden |

---

*This document defines pedagogical intent and system behavior contracts. No official WSET assessment authority is claimed. The system is a formative learning tool, not an examination platform.*
