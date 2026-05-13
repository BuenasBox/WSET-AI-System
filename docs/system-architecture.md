# WSET Level 3 AI Agent Architecture

## Scope

This project designs a professional WSET Level 3 Award in Wines learning and evaluation system for a primary exam date of 08 August 2026.

This phase does not include UI, frontend implementation, backend services, deployment, authentication, payments, or infrastructure. It defines the architecture for three AI agents:

- Tutor Agent
- Examiner Agent
- Orchestrator

The system is not a generic wine chatbot. It is a WSET-focused learning, calibration, deliberate-practice, and official-like evaluation system.

## Core Principle

The system optimizes for structure, linkage, precision, concision, examinable relevance, and conversion of knowledge into marks.

The system does not evaluate how much the student knows. It evaluates how much of that knowledge can be converted into a mark-worthy WSET Level 3 answer.

## Folder Architecture

```text
WSET-AI-System/
  agents/
    tutor-agent/
    examiner-agent/
    orchestrator/
  knowledge/
    official/
    book/
    question-bank/
    wine-with-jimmy/
    nazareth/
    calibration/
  prompts/
    tutor-agent.md
    examiner-agent.md
    orchestrator.md
  schemas/
  docs/
    product-requirements.md
    system-architecture.md
    roadmap.md
  frontend/
  backend/
  tests/
```

Recommended future files, still architecture-only:

```text
schemas/
  source.schema.json
  learning-outcome.schema.json
  evaluation-result.schema.json
  tasting-note.schema.json
  student-progress.schema.json
  practice-recommendation.schema.json

knowledge/calibration/
  official-boundaries.md
  practice-rubrics.md
  benchmark-wines.md
  sat-consistency-rules.md
```

## Source Reliability Hierarchy

Authority is source-dependent and agent-dependent.

### Tier 1: Grading Authority

Used by Examiner Agent as calibration authority:

- Official WSET specification and learning outcomes
- Official SAT structure
- Official sample papers
- Official marking guidance, when available
- Official mock exams and published examiner-style guidance, when available

Tier 1 defines exam calibration. Non-official sources must not alter grading severity.

### Tier 2: Core Learning Authority

Used by Tutor Agent for explanation and training:

- Official WSET documents
- SAT Level 3
- Understanding Wines: Explaining Style and Quality
- Approved course materials and specification-aligned content

Tier 2 may explain and organize knowledge but must not invent official scoring standards.

### Tier 3: Pedagogical Support

Used by Tutor Agent only:

- Wine With Jimmy transcripts
- Teacher notes
- Student mistake history
- Question banks
- Deliberate-practice resources
- Calibration examples built from prior student answers

Tier 3 improves teaching and practice design. It cannot override Tier 1.

### Tier 4: Unverified or External Material

Used only after verification:

- Web articles
- Producer pages
- Commercial tasting notes
- Unofficial forums
- User-provided material

Tier 4 must be clearly labeled as non-authoritative and cannot be used for official-style grading.

## Gold-Standard Calibration Rules

- Official WSET sources define grading authority.
- When an official mark scheme exists, Examiner follows it strictly.
- When no official mark scheme exists, Examiner labels the output as practice calibration, not official scoring.
- Examiner evaluates the answer submitted, not the student's probable knowledge.
- Correct facts earn little or nothing if they are irrelevant, vague, unsupported, or not linked to the question.
- Distinction-level evaluation requires precise cause-effect linkage.
- No credit is awarded for padding, name-dropping, encyclopedic breadth, or unsupported claims.
- Tutor may coach toward stronger answers but may not present unofficial rules as official standards.
- The tasting engine evaluates the wine in the glass and the consistency of the note, not identity guessing.
- Ambiguous SAT ranges such as "medium to medium(+)" are penalized because they avoid commitment.
- BICL conclusions must be justified by evidence present in the SAT note.

## Agent Responsibilities

### Tutor Agent

Purpose:

- Teach, explain, coach, and train
- Build understanding and cause-effect logic
- Convert knowledge into mark-worthy answers
- Create drills, answer frames, benchmark structures, and revision tasks
- Use Examiner feedback to repair weaknesses

Allowed sources:

- Tier 1, Tier 2, and Tier 3 sources
- Student history and prior errors
- Question banks

Must not:

- Override official WSET evaluation standards
- Invent official scoring rules
- Act as final grading authority
- Reward verbosity as a substitute for relevance

Primary outputs:

- Explanations
- Structured answer templates
- Cause-effect chains
- Deliberate-practice drills
- Compressed model answers
- Weakness repair plans

### Examiner Agent

Purpose:

- Grade, evaluate, score, and calibrate
- Simulate official-style exams
- Assess theory answers
- Assess SAT tasting notes
- Detect weaknesses

Allowed sources:

- Tier 1 only for grading authority
- Tier 1-derived calibration notes
- Practice rubrics only when clearly labeled as non-official

Must:

- Be strict, objective, concise, repeatable, and evidence-based
- Separate correct knowledge from mark-worthy response quality
- Penalize vagueness, irrelevant content, unsupported conclusions, and weak linkage
- Identify what would likely earn marks and what would not

Must not:

- Soften grading to motivate the student
- Use non-official pedagogical material to change severity
- Reward irrelevant information
- Accept vague terminology where precision is expected

Primary outputs:

- Score or practice score
- Mark-worthy points
- Lost-mark analysis
- Error taxonomy labels
- SAT/BICL consistency assessment
- Corrective recommendations routed to Tutor

### Orchestrator

Purpose:

- Route user requests to the correct agent
- Maintain student state and evaluation history
- Connect Examiner feedback to Tutor drills
- Track learning progress
- Recommend next practice actions

Routing examples:

- "Explain Bordeaux" -> Tutor
- "Grade my answer" -> Examiner
- "Help me improve this answer" -> Tutor using Examiner feedback
- "Simulate a mock exam" -> Examiner
- "Create drills for my weak areas" -> Tutor

Must:

- Preserve distinction between teaching and grading
- Store evaluation results in structured form
- Trigger corrective drills after repeated weaknesses
- Maintain source boundaries
- Ask clarifying questions only when routing or grading is impossible

## Shared Architecture

Shared services are conceptual in this phase:

- Source registry: stores source tier, type, provenance, and permitted agent use.
- LO mapper: maps questions, answers, errors, and drills to WSET learning outcomes.
- Calibration registry: stores official rules, official-like examples, and practice-only rubrics.
- Student profile: stores exam date, target grade, attempts, weak areas, and improvement trends.
- Evaluation ledger: stores Examiner outputs, SAT consistency checks, and error taxonomy labels.
- Practice planner: converts weaknesses into targeted Tutor drills.
- Benchmark wine library: stores calibrated wine profiles for SAT practice and comparison.

## Data Architecture

### Source Object

```json
{
  "source_id": "official-specification-2026",
  "title": "WSET Level 3 Specification",
  "tier": 1,
  "type": "official",
  "allowed_agents": ["tutor", "examiner", "orchestrator"],
  "grading_authority": true,
  "pedagogy_only": false,
  "provenance": "official",
  "last_verified": "YYYY-MM-DD"
}
```

### Learning Outcome Object

```json
{
  "lo_id": "LO-x",
  "topic": "climate and grape growing",
  "exam_relevance": "high",
  "required_skills": ["explain", "link", "justify"],
  "common_errors": ["fact_without_consequence", "generic_claim"],
  "benchmark_tasks": ["short_answer", "structured_explanation"]
}
```

### Evaluation Result Object

```json
{
  "evaluation_id": "eval-001",
  "student_id": "primary",
  "agent": "examiner",
  "mode": "practice_calibration",
  "question_type": "theory",
  "learning_outcomes": ["LO-x"],
  "score": {
    "awarded": 0,
    "available": 0,
    "official": false,
    "note": "No official mark scheme supplied; practice calibration only."
  },
  "mark_worthy_points": [],
  "lost_marks": [],
  "error_taxonomy": [],
  "next_actions": []
}
```

### Tasting Note Object

```json
{
  "appearance": {},
  "nose": {},
  "palate": {},
  "conclusions": {
    "quality": "",
    "readiness": "",
    "identity_guess_optional": ""
  },
  "sat_commitment_flags": [],
  "bicl_consistency": {
    "balanced": null,
    "intensity": null,
    "complexity": null,
    "length": null,
    "supported_by_note": false
  }
}
```

### Student Progress Object

```json
{
  "student_id": "primary",
  "exam_date": "2026-08-08",
  "target": "Distinction",
  "weak_areas": [],
  "strengths": [],
  "error_trends": {},
  "sat_trends": {},
  "recommended_practice": []
}
```

## Prompt Architecture

Each prompt has five layers:

1. Role and boundary: defines agent purpose and forbidden behavior.
2. Source policy: defines which source tiers may be used and how.
3. Task logic: defines how the agent processes the request.
4. Output contract: defines concise, repeatable response structures.
5. Escalation rules: defines when to route to another agent or label uncertainty.

Prompt files:

- `prompts/tutor-agent.md`: teaching, drills, linkage, compression, repair.
- `prompts/examiner-agent.md`: grading, SAT evaluation, BICL consistency, official calibration.
- `prompts/orchestrator.md`: routing, memory, progress tracking, next-action selection.

## Error Taxonomy

Core error labels:

- `irrelevant_content`: correct or incorrect material that does not answer the question.
- `vague_claim`: imprecise wording that cannot reliably earn marks.
- `fact_without_consequence`: fact stated without explaining why it matters.
- `missing_causal_link`: answer lacks cause-effect linkage.
- `unsupported_conclusion`: conclusion not justified by evidence.
- `overbreadth`: too much generic knowledge, not enough exam relevance.
- `underdeveloped_point`: relevant idea present but not developed enough.
- `wrong_direction`: causal relationship is reversed or misleading.
- `sat_non_commitment`: ambiguous range such as "medium to medium(+)".
- `sat_internal_inconsistency`: descriptors conflict across appearance, nose, palate, or conclusions.
- `bicl_not_supported`: BICL conclusion not supported by SAT evidence.
- `quality_without_justification`: quality stated without balance, intensity, complexity, or length support.
- `identity_overfocus`: tasting answer prioritizes guessing identity over wine-in-glass evidence.
- `structure_failure`: answer is hard to mark because it lacks organization.
- `missed_command_word`: answer does not match explain, describe, compare, assess, or justify.

## Learning Outcome Mapping

Every question, evaluation, drill, and weakness should be tagged to learning outcomes.

Mapping dimensions:

- Topic: region, grape, climate, winemaking, maturation, style, quality, business, tasting.
- Skill: describe, explain, compare, justify, assess, evaluate.
- Mark conversion: fact, consequence, example, conclusion.
- Risk level: high-frequency, high-difficulty, repeated weakness.

The LO mapper should support:

- Examiner: identify whether the student answered the tested outcome.
- Tutor: create drills for the exact outcome and skill gap.
- Orchestrator: aggregate weak areas and prioritize practice.

## Cause-Effect Evaluation Logic

A mark-worthy WSET Level 3 theory answer usually requires a chain:

```text
Cause -> Mechanism -> Effect on grape/wine -> Exam-relevant conclusion
```

Example structure:

```text
Warm climate -> faster sugar accumulation and lower acid retention -> fuller body, higher alcohol, lower acidity -> riper style profile.
```

Evaluation checks:

- Is the cause specific?
- Is the mechanism correct?
- Is the wine-style or quality effect stated?
- Is the conclusion relevant to the question?
- Is the answer concise enough to be markable?

Distinction-level answers require more than isolated facts. They need linked reasoning under exam constraints.

## SAT Tasting Evaluation Logic

The tasting engine evaluates SAT discipline and internal consistency.

Core checks:

- Uses official SAT categories and vocabulary.
- Commits to one valid level where required.
- Avoids ambiguous ranges such as "medium to medium(+)".
- Separates aroma/flavour descriptors from structural conclusions.
- Ensures palate evidence supports conclusions.
- Evaluates wine in the glass rather than identity guessing.
- Flags contradictions such as high acidity with descriptors that imply low freshness unless justified.

SAT assessment output:

- Valid observations
- Invalid or vague descriptors
- Missing required SAT fields
- Internal consistency flags
- BICL support assessment
- Priority correction drill

## BICL Consistency Logic

BICL means balance, intensity, complexity, and length.

Quality conclusions must be justified by the note:

- Balance: structure components work together; no unsupported harshness, flatness, heat, or sweetness imbalance.
- Intensity: nose and palate intensity support the stated quality.
- Complexity: range and development of aromas/flavours support the stated complexity.
- Length: finish length supports the conclusion.

The system should reject conclusions such as "very good" or "outstanding" when the note does not provide enough BICL evidence.

## Internal Consistency Checks

Theory:

- Command word answered
- Scope controlled
- Cause-effect links present
- Examples relevant
- No contradiction between claims
- No unsupported conclusions

Tasting:

- SAT structure complete
- Descriptor levels committed
- Nose, palate, and conclusion aligned
- Quality conclusion supported by BICL
- Readiness conclusion supported by fruit, structure, development, and balance

Agent:

- Examiner does not use Tier 3 to grade.
- Tutor does not claim unofficial rubrics are official.
- Orchestrator routes grading to Examiner and coaching to Tutor.

## Benchmark Wine Architecture

The benchmark wine library supports tasting calibration and style recognition without turning tasting into identity guessing.

Benchmark object:

```json
{
  "benchmark_id": "benchmark-001",
  "category": "high-acid-aromatic-white",
  "style_markers": [],
  "sat_expected_ranges": {},
  "bicl_expectations": {},
  "common_student_errors": [],
  "training_drills": []
}
```

Use cases:

- Tutor compares student note to style benchmarks.
- Examiner evaluates whether the note is plausible and internally consistent.
- Orchestrator identifies recurring SAT weaknesses.

The benchmark must not imply that blind tasting marks depend primarily on guessing the wine.

## Student Progress Tracking

Track:

- Exam date: 08 August 2026
- Target: Distinction
- Attempts by topic and question type
- Examiner scores and practice scores
- Error taxonomy frequency
- Learning outcome coverage
- SAT field-level weaknesses
- BICL support quality
- Answer compression performance
- Linkage quality trend

Progress indicators:

- Mark conversion rate
- Linkage success rate
- Concision score
- SAT commitment rate
- BICL support rate
- Repeated error decay
- Readiness by learning outcome

## Distinction-Level Coaching Logic

Tutor coaching should train:

- Answer the command word first.
- Select only examinable facts.
- Convert each fact into consequence.
- Use specific mechanisms.
- Avoid vague claims.
- Compress without losing causality.
- Practice under time limits.
- Repair recurring error labels.

Distinction training prompt:

```text
Give me the shortest answer that preserves the causal chain and would be easiest for an examiner to mark.
```

## Compression and Concise-Answer Training

Compression sequence:

1. Full explanation
2. Mark-worthy bullet answer
3. Exam-length answer
4. One-sentence causal chain
5. Examiner check: what earns marks, what is filler

Compression score:

- Keeps cause
- Keeps mechanism
- Keeps effect
- Keeps conclusion
- Removes padding
- Preserves WSET vocabulary

## Linkage Detection

Linkage detector checks for:

- Cause words: because, due to, leads to, results in, therefore.
- Mechanism words: ripening, acid retention, sugar accumulation, tannin extraction, oxidation, malolactic conversion.
- Outcome words: acidity, alcohol, body, tannin, aroma, flavour, quality, style, ageing potential.
- Specificity: named factor and named consequence.

Weak linkage pattern:

```text
X is important for quality.
```

Strong linkage pattern:

```text
X changes Y, which affects Z in the wine, so it is relevant to the question.
```

## Weak-Area Analytics

Weak areas should be computed from repeated evidence, not single failures.

Signals:

- Same error taxonomy label appears repeatedly.
- Same learning outcome remains below target.
- Same SAT category shows inconsistency.
- Same command word is mishandled.
- Student writes correct facts but fails to convert them into marks.

Priority formula:

```text
priority = exam_relevance + recurrence + severity + proximity_to_exam - recent_improvement
```

## Practice Recommendation Engine

Recommendation types:

- Tutor explanation
- Cause-effect drill
- Examiner regrade
- SAT calibration drill
- BICL justification drill
- Compression drill
- Timed short-answer set
- Mock exam
- Error repair session

Recommendation logic:

- If answer lacks linkage -> Tutor cause-effect drill.
- If answer is verbose but correct -> Tutor compression drill.
- If answer seems strong but score is low -> Examiner lost-mark analysis, then Tutor repair.
- If SAT ranges are ambiguous -> SAT commitment drill.
- If BICL unsupported -> BICL evidence drill.
- If repeated LO weakness -> targeted micro-cycle: teach, drill, grade, repair.

## Verification and Adversarial Quality Control

The system may use legal adversarial testing techniques to improve reliability:

- Prompt-injection tests against source boundaries.
- Calibration drift tests between Examiner runs.
- Hallucinated-mark-scheme detection.
- Source authority conflict tests.
- Contradictory SAT note tests.
- Ambiguous answer tests.
- Relevance traps with true but non-mark-worthy facts.

The system must not use unauthorized access, scraping behind access controls, credential bypass, or any illegal acquisition of materials.

## End-to-End Workflow

1. User submits request.
2. Orchestrator classifies intent.
3. Orchestrator routes to Tutor or Examiner.
4. Agent responds under source and role constraints.
5. If Examiner evaluates, result is stored in evaluation ledger.
6. Orchestrator maps errors to learning outcomes.
7. Orchestrator triggers Tutor drills for repeated or high-severity weaknesses.
8. Student completes practice.
9. Examiner re-evaluates.
10. Progress state updates toward Distinction readiness.
