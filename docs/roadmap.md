# Roadmap

## Phase 1: Agent Architecture

Status: current phase.

Deliverables:

- Define folder architecture.
- Define data architecture.
- Define prompt architecture.
- Define Tutor, Examiner, and Orchestrator responsibilities.
- Define shared source, calibration, evaluation, and progress concepts.
- Create initial prompt files.

## Phase 2: Schemas and Calibration Files

Deliverables:

- JSON schemas for sources, learning outcomes, evaluations, tasting notes, student progress, and practice recommendations.
- Official-source registry template.
- Calibration registry template.
- Error taxonomy file.
- Benchmark wine file structure.

## Phase 3: Knowledge Preparation

Deliverables:

- Organize official documents in `knowledge/official`.
- Organize book-aligned notes in `knowledge/book`.
- Organize question banks in `knowledge/question-bank`.
- Organize teaching transcripts in `knowledge/wine-with-jimmy`.
- Organize calibration assets in `knowledge/calibration`.
- Tag sources by reliability tier.

## Phase 4: Agent Prompt Refinement

Deliverables:

- Tutor prompt tested against explanation and drill tasks.
- Examiner prompt tested against grading and SAT tasks.
- Orchestrator prompt tested against routing and progress tracking tasks.
- Adversarial tests for prompt injection and calibration drift.

## Phase 5: Evaluation Workflows

Deliverables:

- Theory answer evaluation workflow.
- SAT tasting evaluation workflow.
- BICL consistency workflow.
- Weak-area analytics workflow.
- Practice recommendation workflow.

## Phase 6: Implementation Planning

Deliverables:

- Decide backend architecture.
- Decide storage architecture.
- Decide retrieval architecture.
- Decide frontend requirements.

Implementation begins only after the agent architecture and calibration files are stable.
