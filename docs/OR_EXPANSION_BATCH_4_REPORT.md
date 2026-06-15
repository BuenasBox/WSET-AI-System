# Open Response Expansion Batch 4 Report

**Date:** 2026-06-15  
**Status:** Implemented locally and integrated into the canonical payload path  
**Authority:** Formative training content only

## Result

Batch 4 adds **32** Open Response items:

- New IDs: `OR_107`-`OR_138`
- Previous bank: 106
- New bank total: **138**
- Duplicate IDs: 0
- Duplicate normalized question texts: 0

## Batch Distribution

| RA | New items |
|---|---:|
| RA1 | 6 |
| RA2 | 12 |
| RA3 | 0 |
| RA4 | 8 |
| RA5 | 6 |
| **Total** | **32** |

Final bank distribution after the batch and three legacy mapping corrections:

| RA | Total items |
|---|---:|
| RA1 | 42 |
| RA2 | 41 |
| RA3 | 15 |
| RA4 | 23 |
| RA5 | 17 |
| **Total** | **138** |

## Verb Distribution

The requested eight verbs are exactly balanced:

| Command verb | Items |
|---|---:|
| Describe | 4 |
| Explain | 4 |
| Compare | 4 |
| Assess | 4 |
| Evaluate | 4 |
| Discuss | 4 |
| Recommend | 4 |
| Identify and Explain | 4 |

## Specification Coverage Added

### RA1

- Icewine/Eiswein natural freezing conditions
- Icewine delayed-harvest risk
- Icewine versus botrytis vineyard comparison
- Sauternes botrytis site suitability
- Tokaji botrytis and climate risk
- Passito ripeness and harvest risk

### RA2

- Icewine fermentation and residual-sugar management
- Tokaji Aszú berry addition, maceration, fermentation, and maturation
- Tokaji versus Sauternes production
- Sauternes lot fermentation, oak use, and style creation
- Passito drying-method choices
- Botrytis versus passito concentration
- Non-fortified sweet-wine fermentation arrest
- Sweetness/acidity balance and ageing

### RA4

- Ruby versus Tawny Port
- LBV versus Vintage Port category decisions
- Fino versus Oloroso production
- Flor and solera management
- Madeira production choices and style categories
- Port versus Sherry fortification timing
- Rutherglen Muscat production

### RA5

- Tokaji and Sauternes service
- Mature Vintage Port storage and decanting
- Icewine and Sauternes food pairing
- Madeira customer advice
- Sherry service sequence
- Expected oxidative character versus wine fault

## Official RA Mapping Correction

Sweetness is not an RA5 classification rule.

- **RA1** is used for growing environment, freezing, botrytis development,
  ripeness, harvest timing, and vineyard risk.
- **RA2** is used for still-wine production, concentration, fermentation,
  residual sugar, maturation, style creation, and production choices.
- **RA3** remains sparkling wine only.
- **RA4** remains fortified wine only.
- **RA5** is reserved for service, storage, faults, food pairing, customer
  advice, health, and safe consumption.

Three legacy items were corrected without changing IDs or question text:

| Item | Previous RA | Corrected RA | Reason |
|---|---|---|---|
| `OR_050` | RA5 | RA2 | Sweet-wine production comparison |
| `OR_081` | RA5 | RA2 | Botrytised sweet-wine maturation |
| `OR_106` | RA5 | RA2 | Tokaji Aszú production and maturation |

Future agents must not map Icewine, Eiswein, Tokaji, Sauternes, botrytis,
passito, or sweet-wine production to RA5 unless the question genuinely concerns
service, storage, faults, pairing, health, safe consumption, or customer advice.

## Integration

The existing OR node shape remains the source of truth. Batch 4 adds the
required `question_id` alias while preserving `item_id`.

`open_response_lab_runtime.py` now provides a normalization adapter from
`open_response_bank.json` into the established runtime candidate contract. It
does not create a parallel bank schema.

The generated `lab_payload.js` now contains:

- 138 learner-visible items
- 138 evaluation/coaching records
- legacy IDs `OR_001`-`OR_106` unchanged
- Batch 4 IDs `OR_107`-`OR_138`
- preserved formative evaluation metadata
- the existing 1/2/4/4 session-size contract
- a four-item Full Simulation pool: `OR_113`, `OR_114`, `OR_115`, `OR_125`
  with RA distribution RA2/RA2/RA2/RA4

A governed `recommend` command-verb definition was added to the knowledge and
frontend coaching contracts.

## Files Changed

- `knowledge/question-bank/open_response/or_batch_04_expansion.json`
- `knowledge/question-bank/open_response/open_response_bank.json`
- `knowledge/command-verbs/recommend.json`
- `tools/question_generation/open_response_lab_runtime.py`
- `frontend/open-response-lab/lab_payload.js`
- `frontend/open-response-lab/command_verbs_loader.js`
- Batch and integration tests
- Batch 4 report and validation report

Production repository touched: **no**.

