# WSET Level 3 Master Dictionary Extraction Report

Controlled vocabulary extraction only. No embeddings, retrieval indexes, semantic graph linking, transcript mutation, question-bank mutation, or official PDF mutation were performed.

## Official Sources
- 1. `specification`: `knowledge\official-wset\specification\WSET_L3_Specification_Official_2026.pdf`
- 2. `sat`: `knowledge\official-wset\sat\WSET_L3_SAT_Official_2016.pdf`
- 3. `study-guide`: `knowledge\official-wset\study-guide\WSET_L3_Study_Guide_Official_2026.pdf`

## Category Counts

- `appellation`: 175
- `climate`: 18
- `grape_variety`: 202
- `region`: 72
- `sat_term`: 44
- `vinification`: 44
- `viticulture`: 38
- `wine_law`: 87

## Quality Flags

- `duplicate_term`: 511
- `ambiguous_category`: 2
- `low_confidence_extraction`: 0
- `possible_ocr_issue`: 58

## Method

The extractor uses a conservative seeded vocabulary drawn from official WSET specification lists, the official study-guide index, and official SAT vocabulary. A candidate is emitted only when it is found in the local official PDFs. SAT rows are emitted only from the standalone official SAT sheet or the official SAT chapter/table in the study guide.

Canonical terms preserve official WSET capitalization/spelling from the seeded official term. Aliases are emitted only for observed accent, capitalization, OCR, or ASR variants such as `Rhone` for `Rhône` and `carbonicm aceration` for `carbonic maceration`.

## First 20 Extracted Terms

- Aglianico del Vulture | appellation | specification | high
- Aglianico del Vulture | appellation | study-guide | high
- Alsace Grand Cru | appellation | specification | high
- Alsace Grand Cru | appellation | study-guide | high
- Amarone della Valpolicella | appellation | specification | high
- Amarone della Valpolicella | appellation | study-guide | high
- Anjou | appellation | specification | high
- Anjou | appellation | study-guide | high
- Asti | appellation | specification | high
- Asti | appellation | study-guide | high
- Bandol | appellation | specification | high
- Bandol | appellation | study-guide | high
- Barbaresco | appellation | specification | high
- Barbaresco | appellation | study-guide | high
- Barbera d’Asti | appellation | specification | high
- Barbera d’Asti | appellation | study-guide | medium
- Barolo | appellation | specification | high
- Barolo | appellation | study-guide | high
- Barsac | appellation | specification | high
- Barsac | appellation | study-guide | high
