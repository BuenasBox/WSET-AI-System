# WSET Level 3 Canonical Dictionary Consolidation Report

Phase 2 consolidation only. No official PDFs, transcript files, question-bank files, raw extraction rows, embeddings, vector DBs, or agents were modified or created.

## Summary

- Raw term count: 680
- Consolidated canonical term count: 424
- Duplicates merged: 256
- Raw extraction files untouched: true

## Counts By Category

- `appellation`: 89
- `climate`: 18
- `grape_variety`: 102
- `region`: 45
- `sat_term`: 42
- `vinification`: 43
- `viticulture`: 37
- `wine_law`: 48

## Ambiguous Category Terms

- whole bunch fermentation: vinification, viticulture

## Alias Collision Terms

- Semillon
- Sémillon
- whole bunch fermentation

## Top 30 Canonical Terms By Source Count

- Joven | wine_law | sources: 3 | sat, specification, study-guide
- Aconcagua Region | region | sources: 2 | specification, study-guide
- Agiorgitiko | grape_variety | sources: 2 | specification, study-guide
- Aglianico | grape_variety | sources: 2 | specification, study-guide
- Aglianico del Vulture | appellation | sources: 2 | specification, study-guide
- Airén | grape_variety | sources: 2 | specification, study-guide
- Albariño | grape_variety | sources: 2 | specification, study-guide
- Alcohol | sat_term | sources: 2 | sat, study-guide
- Alfrocheiro | grape_variety | sources: 2 | specification, study-guide
- Alicante Bouschet | grape_variety | sources: 2 | specification, study-guide
- Alsace | region | sources: 2 | specification, study-guide
- Alsace Grand Cru | appellation | sources: 2 | specification, study-guide
- Alvarinho | grape_variety | sources: 2 | specification, study-guide
- Amarone della Valpolicella | appellation | sources: 2 | specification, study-guide
- Anjou | appellation | sources: 2 | specification, study-guide
- Arinto | grape_variety | sources: 2 | specification, study-guide
- Assyrtiko | grape_variety | sources: 2 | specification, study-guide
- Asti | appellation | sources: 2 | specification, study-guide
- Australia | region | sources: 2 | specification, study-guide
- Austria | region | sources: 2 | specification, study-guide
- AVA | wine_law | sources: 2 | specification, study-guide
- Baden | region | sources: 2 | specification, study-guide
- Baga | grape_variety | sources: 2 | specification, study-guide
- Bandol | appellation | sources: 2 | specification, study-guide
- Barbaresco | appellation | sources: 2 | specification, study-guide
- Barbera | grape_variety | sources: 2 | specification, study-guide
- Barbera d’Asti | appellation | sources: 2 | specification, study-guide
- Barolo | appellation | sources: 2 | specification, study-guide
- Barossa | region | sources: 2 | specification, study-guide
- Barsac | appellation | sources: 2 | specification, study-guide

## Recommended Human Review Priorities

- Barbera d’Asti | appellation | conflicting_confidence; needs_human_review; possible_ocr_issue
- Bordeaux Supérieur | appellation | conflicting_confidence; needs_human_review; possible_ocr_issue
- Châteauneuf-du-Pape | appellation | conflicting_confidence; needs_human_review; possible_ocr_issue
- Crémant de Bourgogne | appellation | conflicting_confidence; needs_human_review; possible_ocr_issue
- Crémant de Loire | appellation | conflicting_confidence; needs_human_review; possible_ocr_issue
- Crémant d’Alsace | appellation | conflicting_confidence; needs_human_review; possible_ocr_issue
- Côte Rôtie | appellation | conflicting_confidence; needs_human_review; possible_ocr_issue
- Côtes de Bordeaux | appellation | conflicting_confidence; needs_human_review; possible_ocr_issue
- Côtes de Gascogne | appellation | conflicting_confidence; needs_human_review; possible_ocr_issue
- Côtes du Rhône | appellation | conflicting_confidence; needs_human_review; possible_ocr_issue
- Côtes du Rhône Villages | appellation | conflicting_confidence; needs_human_review; possible_ocr_issue
- Côtes du Roussillon | appellation | conflicting_confidence; needs_human_review; possible_ocr_issue
- Côtes du Roussillon Villages | appellation | conflicting_confidence; needs_human_review; possible_ocr_issue
- Dolcetto d’Alba | appellation | conflicting_confidence; needs_human_review; possible_ocr_issue
- IGP Pays d’Oc | appellation | duplicate_alias; needs_human_review; possible_ocr_issue
- Médoc | appellation | conflicting_confidence; needs_human_review; possible_ocr_issue
- Pessac-Léognan | appellation | conflicting_confidence; needs_human_review; possible_ocr_issue
- Pouilly-Fumé | appellation | conflicting_confidence; needs_human_review; possible_ocr_issue
- Saint-Estèphe | appellation | conflicting_confidence; needs_human_review; possible_ocr_issue
- Saint-Émilion | appellation | conflicting_confidence; needs_human_review; possible_ocr_issue
- Savennières | appellation | conflicting_confidence; needs_human_review; possible_ocr_issue
- altitude | climate | conflicting_confidence; needs_human_review
- climate | climate | conflicting_confidence; needs_human_review
- continental climate | climate | conflicting_confidence; needs_human_review
- continentality | climate | conflicting_confidence; needs_human_review
- cool climate | climate | conflicting_confidence; needs_human_review
- diurnal range | climate | conflicting_confidence; needs_human_review
- fog | climate | conflicting_confidence; needs_human_review
- hot climate | climate | conflicting_confidence; needs_human_review
- latitude | climate | conflicting_confidence; needs_human_review

## Validation

- JSONL is valid.
- CSV row count matches JSONL row count.
- Every record has `canonical_term`, `category`, and `source_documents`.
- `safe_for_examiner` is `false` on every consolidated record.
- Raw rows categorized as `sat_term` remain category `sat_term` after consolidation.
