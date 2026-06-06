# Project State Reconciliation - Canonical Repository State

Fecha de reconciliacion: 2026-06-06

## Decision documental

Este archivo es el estado canonico actual del repositorio. No es un snapshot
historico ni un roadmap. Las afirmaciones se derivan de Git, artefactos
versionados y verificaciones ejecutables.

Cuando este documento contradiga codigo, datos, tests o Git, prevalece la
evidencia ejecutable y este archivo debe actualizarse.

## Estado ejecutivo

`origin/main` esta en:

```text
7a0caefe67f201e0e6a5de1e0b772711f03f825b
Merge pull request #5 from BuenasBox/codex/phase-4a3-9-learning-event-runtime
```

Phase 4A.3.9.0 esta mergeada. El sistema convierte intentos SBA en eventos
formativos, actualiza el mapa cognitivo y LES existentes, y emite senales para
la siguiente sesion. No crea scoring oficial, porcentaje, pass/fail ni
exam-readiness.

Estado global:

- Master Bank canonico y operativo: 616 registros.
- SBA operational pool: 589.
- Open Response candidate pool: 27.
- Review backlog: 0.
- Inactive eligibility backlog: 0.
- Quarantine: 0.
- Public Lab: 36.
- Slow Golden: 7/7 OK.
- Dashboard: operativo.
- Open Response: no activado ni desplegado.
- Governance: intacta.

## Git y fases integradas

Los siguientes commits son ancestros de `origin/main`:

- `8738ca0` - resolucion del backlog Review/Inactive.
- `82445f2` - Cognitive Map Learning Event Runtime.
- `b886f95` - reconciliacion de elegibilidad canonica 589/27.

El merge de PR #5 integra Phase 4A.3.9.0 y sus prerequisitos Phase 4A.3.8 que
aun no estaban presentes en `main`.

## Master Bank y elegibilidad

La fuente operativa es:

- `knowledge/question-bank/master_bank/master_bank.json`
- `knowledge/question-bank/open_response/suitability/master_bank_open_response_suitability.json`
- `knowledge/question-bank/reviews/master_bank_review_inactive_resolution.json`
- `tools/question_generation/master_bank_eligibility.py`

Conteos derivados por `build_eligibility_index()`:

| Pool | Conteo |
|---|---:|
| Master Bank | 616 |
| SBA operativo | 589 |
| Open Response candidates | 27 |
| Review | 0 |
| Inactive | 0 |
| Quarantine | 0 |
| Public Lab | 36 |

La resolucion es versionada y trazable. No se reabre clasificacion ni se
infieren decisiones de contenido desde este documento.

## Learning Event Runtime

`tools/learner_model/learning_event_runtime.py` implementa el flujo:

```text
Question Attempt
  -> Diagnostic Outcome
  -> Formative Event
  -> Cognitive Map Update
  -> LES Update
  -> Next Session Signals
```

Reutiliza:

- `pedagogical_memory_v1` como mapa cognitivo;
- `minimal_brain_v2` como LES;
- `diagnostic_outcome_v1`;
- exposure, topic y RA observations;
- misconception y causal-chain runtimes;
- metadata del Master Bank.

Produce senales de refuerzo, progresion, misconception repair, causal-chain
reinforcement, exposure avoidance y modo recomendado. El Session Composer
adaptativo completo sigue fuera de alcance.

## Verificacion

Verificacion de Phase 4A.3.9.0 antes del merge:

```text
Full suite: 1633 tests, 9 skipped, 0 failures
SBA export dry-run: 36 eligible, 0 validation errors
Slow Golden: 7/7 OK
```

Verificacion post-merge ejecutada sobre `origin/main`:

```text
SBA export dry-run: 36 eligible, 0 validation errors
Slow Golden: 7/7 OK
```

Los snapshots, Tutor, Retrieval y Golden baseline no fueron modificados por
Phase 4A.3.9.0.

## Dashboard

El Dashboard esta operativo y el Diagnostic SBA Public Lab mantiene 36 items.

Fuente de producción: `BuenasBox/epistemiclab-dashboard`, rama `main`.
Dominio operativo: `https://epistemiclab.dpdns.org/`.

No usar `WSET-AI-System/origin/gh-pages` para determinar el estado publicado,
salvo que exista una decision posterior que lo reactive explicitamente.

El archivo local `frontend/architecture-dashboard/system_state.json` es una
proyeccion versionada y puede quedar por detras del estado canonico entre
actualizaciones. Esa posible deriva de metadata no implica que el Dashboard
este inoperativo y no cambia los conteos ejecutables del Master Bank.

## Open Response

El pool canonico contiene 27 candidatos Open Response. Esto no significa
activacion publica.

- Open Response frontend: sin cambios en Phase 4A.3.9.0.
- Open Response evaluator: sin cambios en Phase 4A.3.9.0.
- Activation: off.
- Deployment: no realizado.
- Scoring oficial: no permitido.

## Governance

Se mantienen los invariantes:

```text
safe_for_examiner = False
examiner_scoring_allowed = False
uses_llm = False
uses_api = False
uses_embeddings = False
uses_vector_db = False
cloud_services_active = False
```

El Learning Event Runtime es formativo y privado. No representa evaluacion
WSET, autoridad de examinador ni resultado oficial.

## Pendientes reales

- Hacer que el Session Composer consuma las nuevas next-session signals en una
  fase separada.
- Completar `learning_links` gobernados para distractores, misconceptions y
  causal chains donde falten.
- Mantener sincronizada la metadata versionada del Dashboard con el estado
  ejecutable.
- Definir persistencia atomica coordinada para actualizaciones de memory y LES.

No hay una discrepancia pendiente de elegibilidad. El estado canonico es
589/27.
