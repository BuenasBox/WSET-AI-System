# Adaptive Session Pedagogical Rules

**Status:** Pedagogical contract for future implementation  
**Scope:** Deterministic adaptive SBA sessions of up to 50 questions  
**Implementation status:** Not implemented by this document

## 1. Central Rule

The system does not measure intelligence.

It estimates only:

- current learner proficiency;
- reasoning maturity;
- RA mastery;
- knowledge stability;
- misconception persistence;
- retention risk;
- need for reinforcement;
- readiness for adaptive progression.

All estimates are provisional, local to the available evidence, and reversible when new observations arrive.

The system must never describe a learner as inherently intelligent, weak, incapable, gifted, slow, or fixed at a level. It may describe a concept or RA as currently fragile, emerging, developing, stable, or robust.

## 2. Separation of Concerns

Three independent dimensions must never be collapsed into one value:

1. **Item confidence:** how reliable and reviewed a question is.
2. **Learner proficiency:** how consistently the learner handles a concept or RA.
3. **Reasoning maturity:** how well the learner distinguishes mechanisms, consequences, and plausible distractors.

A low-confidence item cannot reduce learner proficiency. An incorrect response to a question with uncertain metadata must be treated as an item-review signal, not automatically as a learner weakness.

Likewise, a Gold question does not create mastery by itself. Mastery requires repeated, varied evidence.

## 3. Master Bank Usage Layers

The complete Master Bank is an organized practice universe. “Not Gold” means that an item requires an appropriate context, filter, or review. It does not mean that the item is useless.

### 3.1 `public_lab`

Purpose:

- stable learner-facing experience;
- regression reference;
- conservative cold-start sessions;
- comparison point for new composers.

Current known set: 36 SBA items.

Use:

- eligible for public or stable private sessions;
- may seed initial proficiency observations;
- must retain existing governance and validation.

### 3.2 `private_practice`

Purpose:

- expand practice beyond the 36 published items;
- use the broader SBA universe in controlled private sessions.

Entry requirements:

- structurally valid SBA;
- unique source and item identity;
- valid answer-option relationship;
- governance-clean;
- usable RA/topic/difficulty metadata;
- no unresolved quarantine reason.

Gold status is not required.

Non-Gold items in this layer must carry their confidence and review metadata. Their responses may update learner state only when the item meets the evidence rules in Section 9.

### 3.3 `review_pool`

Purpose:

- hold structurally usable items that need metadata, grounding, distractor, difficulty, or duplication review.

Use:

- internal audit;
- shadow composition;
- reviewer packets;
- coverage analysis.

Items in this layer must not independently lower learner proficiency. They may be presented only in an explicitly labelled private calibration session, and their outcomes must not update mastery until the item is approved for `private_practice`.

### 3.4 `remediation_pool`

Purpose:

- reinforce a known weak concept, misconception node, causal chain, or RA gap.

Entry requirements:

- item is eligible for learner-facing private practice;
- item maps to a specific remediation target;
- distractor diagnostics or topic metadata identify why the item is useful;
- the item is not an immediate duplicate of the triggering question.

This pool may contain Gold and non-Gold items. Selection depends on remediation relevance and item confidence, not Gold status alone.

### 3.5 `generation_training_pool`

Purpose:

- provide reviewed structural examples for future governed question-generation work;
- analyze stems, distractor roles, metadata coverage, and lineage.

Use:

- internal only;
- never learner-facing merely because it is useful as a generation example;
- never used to train or call an external model under current governance.

### 3.6 `quarantine`

Purpose:

- preserve records with structural anomalies, unsafe governance, contradictory answers, missing identity, unresolved duplicates, or invalid lineage.

Use:

- audit and repair only;
- never learner-facing;
- no learner-state updates;
- no silent deletion.

### 3.7 Layer Precedence

If an item belongs to more than one operational category, the most restrictive state wins:

```text
quarantine
> review_pool
> generation_training_pool
> remediation_pool
> private_practice
> public_lab
```

`public_lab` is a publication state, not a claim that the item is pedagogically superior to every private item.

## 4. Session Structure

An adaptive SBA session contains a maximum of 50 questions, organized into five blocks of 10.

The system must not precommit all 50 selections before observing the learner. It composes:

1. Block 1 from prior learner evidence or cold-start rules.
2. Blocks 2–5 after evaluating the immediately preceding block.

Each block is deterministic for the same:

- Master Bank version;
- learner-state snapshot;
- prior-session history;
- filters;
- item eligibility state;
- session identifier.

Random selection is not allowed. Option shuffle may remain deterministic under the existing strategy.

The session may stop before 50 questions when the frustration safeguards in Section 11 are triggered. A shorter session is not a failure.

## 5. Observable Evidence

Only observable signals may influence adaptive decisions:

- selected option and correctness against the internal training key;
- RA, topic, difficulty, expected concepts, and causal metadata;
- distractor diagnostic role;
- misconception ID, when explicitly mapped;
- learner confidence self-report;
- response-time band, not raw speed as an ability measure;
- whether the learner changed the answer;
- repeated performance across different items;
- performance across different sessions;
- retention after time has passed;
- success on transfer items with different wording or context;
- current mastery probability;
- recent failures;
- misconception hits;
- retention risk;
- confidence trend;
- overload patterns.

The following must not influence learner estimates:

- item publication status by itself;
- Gold status by itself;
- raw number of questions available in an RA;
- response speed without accuracy and confidence context;
- a single answer;
- demographic, identity, or inferred personality traits;
- official examination assumptions or pass thresholds.

## 6. Initial Proficiency Estimate

### 6.1 Existing Learner State

When prior evidence exists, the initial session plan uses:

- concept mastery probability;
- RA-level evidence aggregation;
- retention risks;
- recurrent misconceptions;
- difficult causal chains;
- confidence trend;
- time since last observation;
- prior overload patterns.

Existing system thresholds remain authoritative:

| Signal | Contract threshold |
|---|---:|
| Low mastery concept | mastery probability `< 0.45` |
| Mastered concept candidate | mastery probability `>= 0.82` |
| Retention review | retention risk `>= 0.55` |
| Persistent misconception | persistence `>= 0.40` |
| Difficult causal chain | retention risk `>= 0.50` |

These thresholds are internal routing thresholds, not grades.

### 6.2 Cold Start

A cold start exists when there are no usable mastery, retention, misconception, causal-chain, or RA observations.

Cold-start Block 1 must:

- contain 10 questions;
- sample all RAs represented by eligible learner-facing items;
- allocate at least one item to each represented RA before assigning a second item to any RA;
- prefer `public_lab`, then approved `private_practice`;
- use foundational and intermediate items;
- contain no distinction item unless fewer than 10 eligible lower-difficulty items exist;
- avoid conceptual duplicates;
- avoid two items mapped to the same misconception node;
- use no `review_pool` or `quarantine` items.

Cold-start results establish provisional observations only. No RA may be classified as stable or robust from Block 1 alone.

### 6.3 Proficiency Bands

These labels describe current evidence:

| Band | Required evidence |
|---|---|
| `insufficient_evidence` | Fewer than 3 independent observations |
| `emerging` | At least 3 observations and mastery probability `< 0.45` |
| `developing` | At least 3 observations and mastery probability `0.45–0.64` |
| `stable` | At least 4 observations, mastery probability `0.65–0.81`, and no persistent misconception in the last two relevant observations |
| `robust` | Mastery probability `>= 0.82`, at least 4 observations across at least 2 sessions, and at least 1 successful transfer or delayed-retention observation |

An observation is independent when it comes from a different `master_item_id`. Repeating the same item does not increase the independent-observation count.

## 7. RA Mastery

RA mastery must be inferred from concept-level evidence, not from a simple percentage of correct answers.

For each RA, maintain:

- observed concept count;
- eligible independent attempts;
- concept mastery distribution;
- retention-risk count;
- persistent misconception count;
- difficulty coverage;
- confidence-alignment pattern;
- transfer evidence.

### 7.1 RA Band Rules

An RA is:

- `insufficient_evidence` when fewer than 5 independent items or fewer than 3 distinct concepts have been observed;
- `emerging` when at least half of observed concepts are below `0.45`, or a persistent misconception affects a core concept;
- `developing` when evidence is mixed and neither emerging nor stable criteria are met;
- `stable` when at least 70% of observed concepts are `stable` or `robust`, with no more than one active retention risk;
- `robust` when at least 80% of observed concepts are `robust`, at least two difficulty levels have been observed, and delayed or transfer evidence exists.

The percentages apply only after minimum evidence requirements are met.

### 7.2 Weighting Weak RAs

Weak RAs receive more questions, but no session may become a single-RA loop unless the learner explicitly requests focused practice.

For each new 10-question block:

- 4 positions target the weakest evidenced RA;
- 2 positions target the second-weakest RA;
- 2 positions maintain stronger or unobserved RAs;
- 1 position targets retention risk;
- 1 position is a transfer or confidence-calibration item.

Positions may overlap in purpose, but the block must still contain 10 distinct items.

If there is insufficient evidence to rank RAs, use balanced coverage instead.

No RA should receive more than 50% of a general adaptive session. Focused practice may exceed this limit only when explicitly selected by the learner.

## 8. Reasoning Maturity

Reasoning maturity is separate from factual recall and must not be inferred from correctness alone.

The system tracks these observable dimensions:

1. **Concept discrimination:** distinguishes plausible distractors from the correct mechanism.
2. **Causal coherence:** connects cause, mechanism, and effect where metadata supports that expectation.
3. **Context transfer:** applies a concept in a differently worded region, variety, production, or style context.
4. **Confidence calibration:** confidence generally aligns with demonstrated knowledge.
5. **Revision behavior:** answer changes improve or degrade the final response over repeated observations.

Reasoning maturity bands:

| Band | Evidence |
|---|---|
| `insufficient_evidence` | Fewer than 3 diagnostic observations |
| `literal` | Correct mainly on direct recall; transfer or distractor discrimination remains fragile |
| `connected` | Repeatedly distinguishes related concepts and recognizes mechanism/consequence relationships |
| `analytical` | Handles transfer, calibrated confidence, and higher-difficulty distractors across at least 2 sessions |

The system must not infer `analytical` from response speed, vocabulary complexity, or one distinction item.

## 9. Real Mastery vs Casual Success

A correct response is not sufficient evidence of mastery.

### 9.1 Casual-Success Indicators

Treat a correct answer as weak evidence when one or more apply:

- first observation of the concept;
- very low learner confidence;
- answer changed from a diagnostically stronger option without a stable pattern;
- correct selection on an item with incomplete or review-pool metadata;
- success is not reproduced on a different item;
- the same item was recently repeated;
- the item exposes lexical clues that duplicate the expected keyword.

Weak evidence may increase familiarity but must not promote a concept to `stable` or `robust`.

### 9.2 Mastery Confirmation

Mastery requires:

- at least 3 successful independent observations;
- evidence across at least 2 sessions;
- no repeated selection of the same misconception distractor;
- at least one transfer or delayed-retention success;
- confidence that is not repeatedly high on wrong answers;
- item confidence sufficient for learner-state updates.

Two consecutive correct answers in one block may justify maintaining or gently increasing difficulty. They do not establish robust mastery.

### 9.3 Item Eligibility for Learner-State Updates

Full learner-state updates are allowed for:

- `public_lab`;
- approved `private_practice`;
- approved `remediation_pool`.

Provisional, non-persistent observations only:

- explicitly labelled calibration items from `review_pool`.

No learner-state updates:

- `generation_training_pool`;
- `quarantine`;
- items with governance violations;
- items with contradictory or missing answer keys.

## 10. Difficulty Progression

Difficulty changes happen between blocks, never mid-question.

### 10.1 Increase Difficulty

Increase one level for a target concept or RA only when the latest block shows:

- at least 3 independent relevant observations;
- at least 2 successful relevant observations;
- no high-confidence misconception response;
- no active overload safeguard;
- current concept or RA band is at least `developing`;
- at least one success is from a non-identical context.

Difficulty moves one step only:

```text
foundational -> intermediate -> distinction
```

No direct foundational-to-distinction jump is allowed.

### 10.2 Maintain Difficulty

Maintain when:

- evidence is mixed;
- fewer than 3 relevant observations exist;
- success is accompanied by low confidence;
- the learner is correct on recall but not yet on transfer;
- item confidence is insufficient to justify progression.

### 10.3 Reduce or Consolidate

Move one level down, or remain at foundational with added scaffolding, when:

- two relevant errors occur within the latest 3 observations;
- the same misconception distractor is selected twice;
- a high-confidence wrong answer occurs on an approved diagnostic item;
- retention risk is `>= 0.55`;
- overload safeguards activate.

Reducing difficulty is adaptive consolidation, not regression or failure.

## 11. Frustration and Cognitive Load Safeguards

The session must protect continuity of learning.

Activate a consolidation block when any condition occurs:

- 3 consecutive incorrect responses;
- 4 incorrect responses within the latest 5;
- 2 high-confidence wrong responses linked to the same misconception;
- response-time band rises substantially while accuracy falls across 3 observations;
- repeated answer changes degrade outcomes;
- learner explicitly requests a pause, easier questions, or explanation.

A consolidation block must:

- lower difficulty by one level;
- include at least 2 previously stable concepts;
- include no more than 2 questions targeting the same misconception;
- avoid immediate repetition of the failed item;
- use a different stem/context for remediation;
- restore RA breadth after the first 3 questions.

Stop the session before 50 when:

- two consolidation blocks fail to restore stable engagement;
- the learner requests to stop;
- fewer than 5 eligible non-duplicate items remain;
- item confidence would require using `review_pool` or `quarantine` items as normal practice.

The system must never use punitive wording or describe early stopping as failure.

## 12. Misconception Nodes

An incorrect answer updates a misconception node only when the selected option has an explicit `misconception_id` or a deterministic diagnostic role mapped to one node.

### 12.1 Reinforcement Rules

- One mapped selection creates a tentative misconception observation.
- Two mapped selections on different items create a recurrent signal.
- Persistence `>= 0.40` makes the misconception eligible for session focus.
- A high-confidence wrong response increases priority, not severity language shown to the learner.
- An unmapped wrong answer updates topic uncertainty but must not invent a misconception ID.

### 12.2 Remediation Selection

When a misconception becomes recurrent:

- select a different item from `remediation_pool`;
- prefer the same concept in a different context;
- lower difficulty if the misconception concerns a foundational mechanism;
- include one contrast item that distinguishes the misconception from the correct principle;
- do not repeat the original distractor wording immediately.

### 12.3 Resolution

A misconception is not resolved by one correct answer.

Resolution requires:

- two successful independent contrast observations;
- no repeat hit in the following relevant observation;
- at least one success with medium or high confidence;
- one delayed or later-session confirmation before removing persistent status.

Historical hits remain auditable even after the active signal is cleared.

## 13. Confidence Alignment

Confidence is diagnostic context, not a score.

Allowed internal classifications:

- `calibrated_correct`;
- `uncertain_correct`;
- `calibrated_incorrect`;
- `overconfident_wrong`;
- `insufficient_confidence_data`.

Rules:

- `uncertain_correct` calls for confirmation, not immediate escalation.
- `overconfident_wrong` prioritizes misconception contrast and explanation.
- repeated `calibrated_correct` observations support progression.
- confidence alone never changes mastery without response evidence.

The learner may decline to provide confidence. Missing confidence must not be penalized.

## 14. Deciding the Next Block

After every block of 10, the composer must execute this decision order:

1. Remove ineligible, used, quarantined, and immediate conceptual duplicates.
2. Check frustration safeguards.
3. Identify persistent misconceptions.
4. Identify retention risks.
5. Rank RAs by evidence-adjusted need.
6. Determine difficulty direction per target RA: consolidate, stable, or escalate.
7. Reserve maintenance coverage for stronger and unobserved RAs.
8. Reserve one transfer/confidence-calibration item.
9. Select items from the highest permitted confidence layer.
10. Record why each item was selected.

Selection reason codes must be structured:

```text
cold_start_coverage
weak_ra_reinforcement
second_weak_ra_reinforcement
retention_review
misconception_contrast
difficulty_progression
mastery_confirmation
transfer_check
confidence_calibration
strong_ra_maintenance
unobserved_ra_coverage
```

Free-form hidden reasoning must not control selection.

## 15. Deciding the Next Session

The next session plan is based on the completed session, not only the final block.

Priority order:

1. persistent misconception requiring contrast;
2. high retention risk;
3. RA with `emerging` proficiency and sufficient trusted items;
4. RA with insufficient evidence;
5. mastery confirmation for recently `stable` concepts;
6. transfer checks for `robust` candidates;
7. broader curriculum coverage.

### 15.1 Next Session Modes

The planner emits one mode:

- `balanced_diagnostic`: insufficient evidence across multiple RAs;
- `targeted_reinforcement`: one or two RAs dominate current need;
- `misconception_repair`: recurrent misconception is the highest-priority signal;
- `retention_review`: previously learned concepts are becoming fragile;
- `difficulty_progression`: evidence supports one-level escalation;
- `mastery_confirmation`: stable concepts need transfer or delayed verification.

### 15.2 Spacing

Do not repeat the same item in consecutive sessions unless:

- the learner explicitly requests it; or
- the purpose is answer-review rather than mastery evidence.

Repeated items do not count as independent mastery confirmation.

## 16. Fifty-Question Session Composition Contract

Across the complete session, when sufficient eligible inventory exists:

- all represented RAs receive at least one observation;
- no general session assigns more than 25 questions to one RA;
- at least 5 questions test retention, transfer, or mastery confirmation;
- no more than 10 questions target one misconception node;
- no immediate conceptual duplicates appear in the same block;
- distinction items appear only after evidence supports them;
- the final block contains confirmation and transfer, not only unresolved weaknesses.

The composer must report:

- questions requested and delivered;
- item layer used;
- RA distribution;
- difficulty distribution;
- selection reason per item;
- concepts observed;
- misconception targets;
- items deferred as duplicates;
- items excluded by confidence/governance;
- early-stop reason, when applicable.

These are pedagogical telemetry fields, not assessment results.

## 17. Governance

Immutable requirements:

```text
safe_for_examiner = False
examiner_scoring_allowed = False
uses_llm = False
uses_api = False
uses_embeddings = False
uses_vector_db = False
cloud_services_active = False
```

The adaptive system must not:

- issue an official score;
- calculate or display pass/fail;
- predict certification readiness;
- claim examiner authority;
- map proficiency bands to WSET marks;
- present an internal mastery probability as an official result;
- use response speed as an intelligence proxy;
- expose learner-state or misconception history publicly;
- activate Open Response through the SBA composer;
- silently promote a review or quarantined item into learner-facing practice.

Allowed learner-facing language:

- “This topic appears to need more reinforcement.”
- “Your recent responses show stable understanding in this area.”
- “The next block will revisit this mechanism in a different context.”
- “Your confidence and response pattern suggest that a confirmation item would be useful.”

Forbidden learner-facing language:

- “You passed/failed this RA.”
- “You are intelligent/not intelligent.”
- “You are at examiner level.”
- “This would earn X marks.”
- “You are ready/not ready to pass WSET.”

## 18. Implementation Acceptance Criteria

A future implementation conforms to this contract only if tests demonstrate:

- deterministic composition from identical inputs;
- 50-question maximum and 10-question adaptive blocks;
- cold-start coverage rules;
- RA weighting rules;
- one-step difficulty changes;
- conceptual duplicate deferral;
- distinction between item confidence and learner proficiency;
- no mastery promotion from one answer;
- misconception reinforcement only from mapped evidence;
- frustration safeguards and early stopping;
- use of non-Gold `private_practice` items when eligible;
- exclusion of `review_pool` from persistent mastery updates;
- complete quarantine exclusion;
- preservation of the 36-item public lab;
- Open Response remains separate and inactive;
- all governance invariants remain false;
- no official scoring, pass/fail, or examiner-authority output.

## 19. Non-Goals

This contract does not:

- define official WSET assessment criteria;
- generate new questions;
- perform semantic review of Open Response;
- activate any frontend;
- alter the current 36-item public lab;
- claim that all 595 SBA are equally ready for learner-facing use;
- discard non-Gold questions;
- authorize cloud, API, LLM, embeddings, or vector database use.

Its purpose is to convert the full bank into a governed adaptive progression system where every record has an explicit role and every learner inference has observable evidence.
