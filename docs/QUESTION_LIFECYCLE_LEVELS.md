# Question Lifecycle Levels
**Date:** 2026-06-05  
**Phase:** Parallel Track B — Pedagogical Brain  
**Status:** v1 — approved for reference; not yet enforced by tooling

---

## Purpose

Defines the 5 review levels a question passes through from initial generation to active lab use. These levels apply across all question banks (Open Response, SBA, future Master Bank and Generated Bank). Each level has strict entry criteria, an exit gate, and explicit demotion rules.

---

## The 5 Levels

```
generated_candidate
       ↓
corpus_supported
       ↓
human_reviewed
       ↓
gold_candidate
       ↓
active_lab
```

Progress is **sequential and non-skippable**. A question cannot jump from `generated_candidate` to `human_reviewed`. Demotion (going backward) is always allowed and sometimes required.

---

## Level 1: `generated_candidate`

### What it is
A question that has been produced (by a human, by the system, or by a generation pipeline) but has not yet been verified against the corpus or reviewed for pedagogical quality.

### Entry criteria
- Exists as a structured record with at minimum: `stem`, `question_type`, `RA` field (even if tentative), `governance_flags` (all false)
- Has not yet been checked for corpus support

### What is NOT required yet
- Corpus evidence chunks
- Validated causal chain
- Expected concepts list
- Human review

### Exit gate (to reach `corpus_supported`)
All of the following must be true:
1. `corpus_support.status = "supported"` — minimum 2 official chunks with matched terms
2. `optional_causal_chain` is not null, OR explicit documented waiver for foundational questions
3. `expected_concepts` is non-empty, contains no full sentences, has 8–20 terms
4. `RA` field is set to a valid WSET L3 RA code (RA1–RA4)
5. All governance flags are `false`

### Demotion triggers
- If the stem is found to contain forbidden language → remains `generated_candidate`
- If corpus evidence cannot be found after search → demote to a "rejected" terminal state (do not discard — keep with `review_status: "rejected"` and reason documented)

---

## Level 2: `corpus_supported`

### What it is
A question that has been verified to be grounded in the official WSET corpus. It is structurally complete but has not yet been reviewed by a human for pedagogical quality, difficulty calibration, or feedback design.

### What it contains
- Complete `corpus_support` object with ≥2 evidence chunks
- Validated `expected_concepts` list
- `optional_causal_chain` set or explicitly waived
- Clean governance flags

### What is NOT required yet
- Human review of the stem for clarity, difficulty calibration, or bias
- An operational feedback rubric (beyond the placeholder)
- Activation approval

### Exit gate (to reach `human_reviewed`)
A human reviewer must explicitly confirm all of the following in a review record:
1. `ra_checked: true` — RA mapping is correct for the stem content
2. `causal_metadata_checked: true` — causal chain is accurate and testable
3. `corpus_support_checked: true` — evidence chunks genuinely support the stem
4. `sba_residue_removed: true` — no SBA fields leaked into open response record
5. `official_scoring_absent: true` — no scoring language anywhere in the record
6. `governance_checked: true` — all governance flags confirmed false
7. Stem passes the "forbidden verb" check from `GOVERNED_GENERATION_CONTRACT.md §3`
8. Difficulty calibration confirmed (foundational/intermediate/distinction criteria met)

### Demotion triggers
- Reviewer identifies stem language that implies scoring → demote to `generated_candidate` for revision
- Corpus chunks found to be mismatched (terms matched but chunks don't actually support the concept) → demote to `generated_candidate`
- RA mapping found to be incorrect → demote to `generated_candidate`

---

## Level 3: `human_reviewed`

### What it is
A question that has passed a full human review. It is considered pedagogically valid, corpus-grounded, and governance-clean. It has not yet been selected for a Lab session or had its operational rubric finalized.

### What it contains
- All fields from `corpus_supported` level
- A completed review record with reviewer ID, date, and all checklist items confirmed
- `review_status: "approved"`

### What is NOT yet required
- An operational feedback rubric (beyond placeholder)
- Activation status `active`
- Assignment to a Lab session

### Exit gate (to reach `gold_candidate`)
A `gold_candidate` designation requires:
1. An **operational feedback rubric** defined — specifying:
   - Concept coverage threshold for this specific question (e.g., "at least 4 of the 12 expected concepts")
   - How the causal chain is detected (keywords? structural markers?)
   - At least 3 formative feedback templates for: (a) good coverage, (b) partial coverage, (c) missing causal link
   - A remediation map: which Tutor topics to surface for each feedback gap
2. At least 1 **test response** has been drafted (a model response demonstrating what full concept coverage looks like)
3. The question has been reviewed for the **pilot set** — confirmed non-duplicate in the session it would appear in
4. The `feedback_rubric` field in the question record has been upgraded from placeholder to operational

### Demotion triggers
- If during rubric design it becomes clear the question cannot be evaluated formatively without scoring → demote to `human_reviewed`, redesign stem
- If a near-duplicate is found in the same proposed session → hold at `human_reviewed` until session composition is resolved

---

## Level 4: `gold_candidate`

### What it is
A question fully prepared for Lab use. It has corpus grounding, human review, an operational rubric, a model response, and a session assignment. It is awaiting activation.

### What it contains
- All fields from `human_reviewed` level
- Operational feedback rubric (not a placeholder)
- Model response (internal only — never shown to learners)
- Session assignment record (which Lab session this question will appear in)
- Remediation map (which Tutor topics to surface per gap)
- `activation_status: "inactive"` (still not live)

### Exit gate (to reach `active_lab`)
1. The session composer has confirmed session balance (difficulty mix, topic distribution, no duplicates)
2. The feedback engine has been implemented and tested with the question's rubric
3. The model response has been validated against the rubric (full concept coverage confirmed)
4. Governance confirmation performed: no new fields introduced that could imply scoring
5. The activation flag for this question's session has been explicitly set in the deployment configuration
6. Human sign-off on the full session before going live

### Demotion triggers
- If feedback engine testing reveals rubric is unworkable → demote to `human_reviewed` for rubric redesign
- If session balance is violated by a new question entering the same session → hold at `gold_candidate`

---

## Level 5: `active_lab`

### What it is
A question that is live in a private Lab session. Learners are actively engaging with it and formative feedback is being generated.

### What it contains
- All fields from `gold_candidate` level
- `activation_status: "active"`
- A live session ID it is associated with
- Response collection active (if telemetry is enabled)

### Ongoing constraints
- No changes to the stem while active (stem freeze)
- Rubric changes allowed only between sessions, not mid-session
- Governance flags must remain false at all times
- `review_status` stays `"approved"` — it does not change to "active" (that is the `activation_status`'s job)

### Retirement triggers
- Question is retired from active pool when: (a) a duplicate or superior question enters the bank, (b) the curriculum it maps to changes, or (c) response data reveals systematic misconception in the question design itself (confusing stem)
- Retired questions go to `activation_status: "retired"` and are preserved in the archive (never deleted)

---

## Status Field Summary

| Level | `review_status` | `activation_status` |
|---|---|---|
| generated_candidate | `"pending"` | `"inactive"` |
| corpus_supported | `"pending"` | `"inactive"` |
| human_reviewed | `"approved"` | `"inactive"` |
| gold_candidate | `"approved"` | `"inactive"` |
| active_lab | `"approved"` | `"active"` |
| Rejected (any level) | `"rejected"` | `"inactive"` |
| Retired | `"approved"` | `"retired"` |

**Note:** The existing `diagnostic_open_response_candidates.json` pool currently maps to `human_reviewed` level (structural review complete, operational rubrics not yet defined). The transition from `human_reviewed` to `gold_candidate` is the primary bottleneck before any Lab activation.

---

## Current State Map (Open Response Pool)

| ID | Current level | Blocker to next level |
|---|---|---|
| 18 | generated_candidate | Missing corpus, RA, causal metadata; SBA residue |
| 798–806, 810–817 | human_reviewed | No operational rubric; feedback engine not built |
| 807 | human_reviewed | Compound-response design decision required |
| 809 | human_reviewed | Deduplication vs 803; 4-axis rubric risk |

**All pool questions need operational rubrics before any `gold_candidate` promotion can occur.**

---

*This document does not constitute WSET assessment criteria. Levels are internal system governance constructs only.*
