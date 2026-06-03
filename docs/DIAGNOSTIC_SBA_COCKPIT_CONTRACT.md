# Diagnostic SBA Cockpit — Frontend/Backend Contract

Date: 2026-06-01

Status: Design contract. No backend implementation authorized by this document.
No Supabase connection. No LES writes. No retrieval changes. No cognitive runtime
changes. No snapshot changes.

References:

- `docs/DIAGNOSTIC_SBA_GOVERNANCE_CONTRACT.md` — authority boundaries
- `docs/DIAGNOSTIC_SBA_ITEM_SCHEMA.md` — item schema (diagnostic_sba_item_v1)
- `docs/DIAGNOSTIC_OUTCOME_MODEL.md` — outcome model (diagnostic_outcome_v1)
- `knowledge/enrichment/diagnostic_sba_item.schema.json` — machine-readable item schema
- `knowledge/enrichment/diagnostic_outcome.schema.json` — machine-readable outcome schema
- `frontend/diagnostic-sba/index.html` — current static prototype

---

## 1. Purpose

This document defines the interface contract between the Diagnostic SBA Cockpit
frontend and the future backend that will serve items, receive attempts, and
compute diagnostic outcomes.

The contract is not an implementation plan. It defines:

- What the frontend renders and what data it needs to do so.
- What the frontend sends to the backend on submit.
- What the backend must return to make all diagnostic panels correct.
- The UI state machine.
- The timing, hesitation, and confidence models.
- Governance constraints the frontend must enforce at render time.
- The migration path from static prototype to connected system.
- Risks.

---

## 2. Current State vs Target State

### 2.1 Current (static prototype)

- `frontend/diagnostic-sba/index.html` — static frontend with one same-path fetch
  to `./preguntas.json`; no backend or external HTTP calls.
- `frontend/diagnostic-sba/preguntas.json` keeps pre-submit `items[]` separate
  from post-submit `outcomes_by_item_id`.
- The loader validates minimum item structure, matching outcomes, and fail-closed
  governance flags before activating the loaded data.
- If the JSON is missing or invalid, the private lab shows a clear error state,
  disables answer submission, and does not invent or activate fallback questions.
- The frontend derives correctness, misconception display, and stagger order
  from the static post-submit outcome map only after answer confirmation.
- No backend, no attempt logging, no LES writes.
- Governance disclaimer: visible badge. Timer: client-side. Session state: ephemeral
  in `window` scope.

### 2.2 Target (connected system)

- Frontend fetches items from a local backend endpoint.
- Frontend sends attempt payload on submit.
- Backend computes and returns a `diagnostic_outcome_v1` payload.
- Frontend renders diagnostic panels from the outcome payload only — it does not
  derive or invent any diagnostic conclusion.
- Governance flags in the item and outcome payloads drive frontend rendering
  decisions (disclaimer, mastery label, misconception visibility).
- Session state may be persisted via backend or browser storage.

The frontend must never derive `is_correct`, `diagnosed_error_type`,
`confidence_alignment`, `timing_band`, or `misconception_id` itself. All
diagnostic interpretation belongs to the backend.

---

## 3. Item Payload (Backend → Frontend, Pre-Submission)

The backend serves a **display-ready item payload** that omits fields the
frontend must not see before submission. Specifically, `is_correct` and
`diagnostic_role` per option are stripped from the pre-submission payload.
Revealing correct-answer state before submission would allow the frontend to
contaminate the display or leak answers.

### 3.1 Item render payload structure

```json
{
  "schema_version": "diagnostic_sba_item_v1",
  "item_id": "diag_sba_fml_001",
  "item_version": "1.0.0",
  "curriculum": {
    "ra_id": "RA2",
    "topic": "winemaking",
    "subtopic": "malolactic_fermentation",
    "difficulty": "intermediate",
    "learning_objective": "Identificar el mecanismo bioquímico de la FML y su efecto sobre la acidez percibida y la textura."
  },
  "question": {
    "stem": "¿Cuál de las siguientes afirmaciones describe con mayor precisión el efecto principal de la FML...?",
    "question_type": "single_best_answer",
    "expected_reasoning_type": "process",
    "estimated_time_seconds": 60
  },
  "options": [
    { "option_id": "A", "option_text": "..." },
    { "option_id": "B", "option_text": "..." },
    { "option_id": "C", "option_text": "..." },
    { "option_id": "D", "option_text": "..." }
  ],
  "sat_relevance": ["process_analysis"],
  "display_metadata": {
    "domain_label": "Vinificación — Fermentación Maloláctica",
    "difficulty_display": "INTERMEDIO",
    "sat_skill_label": "Análisis de procesos enológicos"
  },
  "governance": {
    "training_item_only": true,
    "safe_for_examiner": false,
    "official_wset_question": false
  }
}
```

### 3.2 Fields the frontend requires per panel

| UI zone | Required fields |
|---|---|
| Header RA badge | `curriculum.ra_id` |
| Header domain | `display_metadata.domain_label` |
| Header difficulty | `display_metadata.difficulty_display` |
| Header SAT skill | `display_metadata.sat_skill_label` |
| Question counter | `item_id`, session total from session payload |
| Stem | `question.stem` |
| Options A–D | `options[].option_id`, `options[].option_text` |
| Timer calibration | `question.estimated_time_seconds` (optional; default 60s) |
| Instruments — SAT | `display_metadata.sat_skill_label` |
| Governance badge | `governance.training_item_only`, `governance.official_wset_question` |

### 3.3 Fields stripped from pre-submission payload

These fields from `diagnostic_sba_item_v1` are intentionally absent:

- `options[].is_correct` — not served before submission
- `options[].diagnostic_role` — not served before submission
- `options[].misconception_id` — not served before submission
- `source_support.*` — backend-only, not needed by UI
- `feedback.*` — served via outcome payload, not pre-submission
- `attempt_analytics_placeholders.*` — computed at attempt time

---

## 4. Attempt Payload (Frontend → Backend, On Submit)

The frontend sends this payload when the learner confirms an answer. The
backend uses it to compute `diagnostic_outcome_v1`.

### 4.1 Attempt payload structure

```json
{
  "attempt_id": "att_20260601_143200_diag_sba_fml_001",
  "item_id": "diag_sba_fml_001",
  "session_id": "sess_20260601_143000",
  "selected_option_id": "A",
  "response_time_ms": 38420,
  "answer_changed": true,
  "hesitation_count": 2,
  "confidence_self_report": "medium",
  "client_timestamp_utc": "2026-06-01T14:32:00Z"
}
```

### 4.2 Field derivation rules (frontend responsibility)

| Attempt field | Frontend derivation rule |
|---|---|
| `attempt_id` | `att_` + ISO timestamp + `_` + `item_id`. Generated at question load. |
| `session_id` | `sess_` + ISO timestamp at session start. Generated once per session. |
| `selected_option_id` | Final selected option at time of confirm click. One of A/B/C/D. |
| `response_time_ms` | `Math.floor(Date.now() - t0)` where `t0 = Date.now()` at question load. Integer milliseconds. |
| `answer_changed` | `hesitation_count > 0`. Boolean. |
| `hesitation_count` | Incremented each time the learner selects a different option before confirming. Minimum 0. |
| `confidence_self_report` | Mapped from UI 1–5 scale (see Section 6.3). `not_reported` if learner skips. |
| `client_timestamp_utc` | `new Date().toISOString()` at moment of confirm. |

### 4.3 Current prototype deviation

The current static prototype does not send this payload anywhere. The attempt
data is held in the session state object `S` and used locally to render
diagnostic content. When the backend is connected:

1. Build this payload at confirm time.
2. POST to the session backend endpoint.
3. Await the diagnostic outcome response (Section 5).
4. Render panels from the response only — not from embedded question data.

---

## 5. Diagnostic Outcome Payload (Backend → Frontend, Post-Submit)

The backend returns a `diagnostic_outcome_v1` object extended with a
`display` block containing pre-computed human-readable content for every
UI panel. The frontend renders only from `display`. It must not re-derive
or re-interpret any diagnostic field.

### 5.1 Outcome payload structure

```json
{
  "schema_version": "diagnostic_outcome_v1",
  "identity": {
    "outcome_id": "out_20260601_143200_diag_sba_fml_001",
    "item_id": "diag_sba_fml_001",
    "attempt_id": "att_20260601_143200_diag_sba_fml_001",
    "outcome_version": "1.0.0",
    "generated_by": "diagnostic_sba_attempt_analyzer_v1",
    "training_diagnostic_only": true
  },
  "attempt_observation": {
    "selected_option_id": "A",
    "is_correct": false,
    "response_time_ms": 38420,
    "answer_changed": true,
    "confidence_self_report": "medium",
    "hesitation_flag": true
  },
  "diagnostic_classification": {
    "diagnosed_error_type": "keyword_trap",
    "confidence_alignment": "uncertain_wrong"
  },
  "source_trace": {
    "item_source_ids": ["CC_FML_TEXTURE", "MC-FML-TARTARICO"],
    "selected_option_diagnostic_role": "keyword_trap",
    "misconception_id": "MC-FML-TARTARICO",
    "causal_chain_id": "CC_FML_TEXTURE",
    "sat_relevance": ["process_analysis"],
    "topic": "winemaking",
    "subtopic": "malolactic_fermentation",
    "ra_id": "RA2"
  },
  "timing_interpretation": {
    "timing_band": "expected",
    "timing_interpretation": "deliberate_reasoning"
  },
  "remediation_routing": {
    "recommended_next_action": "review_causal_chain",
    "remediation_target_type": "causal_chain",
    "remediation_target_id": "CC_FML_TEXTURE",
    "feedback_priority": "high"
  },
  "learner_state_effect_placeholders": {
    "mastery_signal": null,
    "confidence_signal": null,
    "retention_signal": null,
    "misconception_signal": "MC-FML-TARTARICO",
    "recommended_ledger_event": null
  },
  "governance": {
    "safe_for_examiner": false,
    "examiner_scoring_allowed": false,
    "official_wset_score": false,
    "training_diagnostic_only": true,
    "uses_llm": false,
    "uses_api": false,
    "uses_embeddings": false,
    "uses_vector_db": false,
    "cloud_services_active": false
  },
  "display": {
    "is_correct": false,
    "correct_option_id": "B",
    "timing_label": "DELIBERADA",
    "veredicto": {
      "title": "RESPUESTA INCORRECTA",
      "subtitle": "Opción seleccionada: A · Correcta: B",
      "meta": "Tiempo: 38s · Cambios: 2 · Confianza: NEUTRO"
    },
    "distractor_analysis": {
      "active": true,
      "selected_option_id": "A",
      "diagnostic_role_display": "KEYWORD TRAP",
      "why_attractive": "Menciona correctamente el ácido láctico como producto, activando la asociación parcial con la FML. El error está en el ácido de partida: es el málico, no el tartárico.",
      "error_reasoning": "Confusión entre ácido tartárico y ácido málico como sustrato de la FML."
    },
    "correct_rationale": "La FML convierte ácido málico (diprótico) en ácido láctico (monoprótico), reduciendo la acidez percibida...",
    "misconception": {
      "active": true,
      "id": "MC-FML-TARTARICO",
      "name": "Confusión de sustratos en FML",
      "description": "El aprendiz confunde el ácido tartárico (estable, no fermentado en FML) con el ácido málico (sustrato real)..."
    },
    "causal_chain": {
      "active": true,
      "id": "CC_FML_TEXTURE",
      "causa": "Presencia de ácido málico diprótico tras la fermentación alcohólica",
      "mecanismo": "Bacterias lácticas convierten ácido málico en ácido láctico + CO₂; metabolizan ácido cítrico generando diacetil",
      "efecto": "Descenso de acidez percibida, textura más redonda, notas a mantequilla si diacetil elevado",
      "formulacion_examen": "Identificar FML como proceso que reduce acidez y aporta complejidad láctea; sustrato específico = ácido málico."
    },
    "sat_signal": {
      "level": "weak",
      "level_display": "SEÑAL DÉBIL",
      "skill": "Análisis de procesos enológicos",
      "description": "El aprendiz no ancló el proceso enológico a su mecanismo bioquímico preciso."
    },
    "remediation": {
      "text": "Revisar cadena causal CC_FML_TEXTURE. Énfasis en: (1) ácido málico como único sustrato FML; (2) diferencia diprótico/monoprótico; (3) diacetil desde metabolismo cítrico.",
      "action_type": "review_causal_chain",
      "action_label": "DRILL · Cadena Causal FML → Textura Mantecosa",
      "feedback_priority": "high"
    }
  }
}
```

### 5.2 Frontend rendering rules per outcome field

| UI panel | Source field | Condition |
|---|---|---|
| Veredicto title | `display.veredicto.title` | Always |
| Veredicto subtitle | `display.veredicto.subtitle` | Always |
| Veredicto meta | `display.veredicto.meta` | When `response_time_ms` is not null |
| Options — lock correct | `display.correct_option_id` | Always after submit |
| Options — lock incorrect | `attempt_observation.selected_option_id` + `display.is_correct = false` | When wrong |
| Distractor panel visibility | `display.distractor_analysis.active` | True when wrong |
| Distractor panel label | `display.distractor_analysis.diagnostic_role_display` | When active |
| Distractor why-attractive | `display.distractor_analysis.why_attractive` | When active |
| Distractor error type | `display.distractor_analysis.error_reasoning` | When active |
| Fundamento (when correct) | `display.correct_rationale` | When `display.is_correct = true` |
| Misconception panel | `display.misconception.active` | True only when `!display.is_correct` AND misconception_id is not null |
| Misconception id/name/desc | `display.misconception.*` | When active |
| Causal chain | `display.causal_chain.*` | Always (collapsed by default) |
| SAT level/skill/desc | `display.sat_signal.*` | Always |
| SAT dot color | `display.sat_signal.level` — weak/medium/strong → red/amber/green | Always |
| Remediation text | `display.remediation.text` | Always |
| Next action button label | `display.remediation.action_label` | Always |
| Timing instrument | `timing_interpretation.timing_band` | Post-submit only |

The frontend must not show the misconception panel when the learner answers
correctly, even if the item has a misconception node. Misconception display
is gated on `display.misconception.active`, which the backend sets to `false`
for correct answers.

---

## 6. UI State Machine

Seven states. Transitions are one-directional with reset exception.

```
LOADING → ANSWERING → OPTION_SELECTED → SUBMITTED → DIAGNOSTIC_REVEALED
                ↑_____________________________|          |
                                                         ↓
                                               SESSION_COMPLETE

Any state → ERROR (on network or validation failure)
ERROR → LOADING (on retry)
SESSION_COMPLETE → LOADING (on reset)
```

### 6.1 State definitions

**LOADING**
- Trigger: session start, next-question request, or retry.
- Display: loading indicator in question panel; diagnostic panel shows
  "Cargando pregunta..."; timer paused.
- Transition out: item payload received and rendered → ANSWERING.
- On error: → ERROR.

**ANSWERING**
- Trigger: item rendered.
- Display: stem visible; options clickable; timer running from zero; right panel
  shows instruments only ("Sistema en escucha activa").
- No option is selected. Confirm button hidden. Confidence selector hidden.
- Transition out: learner clicks or keypresses A/B/C/D → OPTION_SELECTED.

**OPTION_SELECTED**
- Trigger: option click or keypress.
- Display: selected option highlighted; confidence selector visible; confirm
  button enabled; keyboard hint visible; hesitation counter updating if changed.
- Re-selecting a different option stays in this state; hesitation_count
  increments.
- Transition out: confirm click or Enter → SUBMITTED.

**SUBMITTED**
- Trigger: confirm action.
- Display: options locked immediately; timer stopped; attempt payload built and
  sent to backend (future: async); loading indicator in diagnostic panel.
- In static prototype: outcome derived locally from embedded data; no actual HTTP.
- Transition out: outcome received (or derived) → DIAGNOSTIC_REVEALED.
- On error: → ERROR.

**DIAGNOSTIC_REVEALED**
- Trigger: outcome payload received.
- Display: diagnostic sections revealed in staggered sequence (~105ms apart):
  veredicto → distractor/fundamento → misconception (if active) → causal chain
  (collapsed) → SAT → remediación → next action.
- Options remain locked. Timer instrument shows final time with timing_band label.
- Next question / session summary button enabled.
- Transition out: next-question click → LOADING (if more questions);
  session-summary click → SESSION_COMPLETE (if last question).

**SESSION_COMPLETE**
- Trigger: learner clicks next/summary after last question in session.
- Display: overlay with session stats (see Section 8).
- Transition out: reset → LOADING (restart from Q1).

**ERROR**
- Trigger: item fetch failure; outcome response failure; malformed payload.
- Display: error message; retry button. No diagnostic content. Timer stopped.
- Must not show partial diagnostic or claim LES was updated.
- Transition out: retry → LOADING.

### 6.2 State variable map (current prototype → target)

| State variable | Current prototype | Target |
|---|---|---|
| Question data | `QS[S.idx]` embedded | Fetched from backend per item_id |
| Correct answer | `q.correcta` embedded | `display.correct_option_id` from outcome |
| Is correct | `S.sel === q.correcta` — frontend derived | `display.is_correct` from outcome |
| Diagnostic content | Embedded in `q.diag.*` | `display.*` from outcome |
| Session state | `S` object in closure | `S` object + optional backend session |
| Attempt payload | Not sent anywhere | POSTed to `/api/attempt` |
| LES write | None (ephemeral) | Backend responsibility; not frontend |

---

## 7. Governance Requirements (Frontend Enforcement)

The frontend is the last line of defence against authority leakage. Even if the
backend returns a compliant payload, the frontend must enforce these rules
independently.

### 7.1 What the frontend must always render

- The `proto-badge` must visibly retain the training/non-official disclaimer and
  state that the cockpit is a private lab with no examiner authority.
  must be visible in the header while any item governance flag reads
  `training_item_only: true` or `official_wset_question: false`.
  This badge must never be removed by any item or session configuration.

- The footer mastery label must include the qualifier `· Entrenamiento`.
  It must never read "Examen", "Puntuación oficial", or any variant implying
  official assessment.

### 7.2 What the frontend must never render

| Forbidden string category | Examples of forbidden text |
|---|---|
| Official score | "Puntuación: X/Y", "Nota oficial", "Score" |
| Examiner marks | "Aprobado", "Suspendido", "Resultado WSET" |
| Certification claims | "Apto para el examen", "Preparado para certificación" |
| False LES claims | "LES actualizado", "Historial guardado en LES" |
| Official readiness | "Nivel L3 confirmado", "Listo para el examen" |
| Grade prediction | "Probabilidad de aprobado", "Nivel estimado" |

The current prototype correctly uses:
- "Señales Registradas Localmente" (not "LES Actualizado")
- "Señal de Maestría · Entrenamiento" (not "Puntuación")
- "Fundamento confirmado · Sin misconception activa" (not a score)

These must remain the reference labels when the backend is connected.

### 7.3 Governance gate at render time

Before rendering any outcome content, the frontend must check:

```javascript
if (outcome.governance.safe_for_examiner === true) {
  // MUST NOT render. Show error state instead.
  showError('Governance violation: safe_for_examiner must be false.');
  return;
}
if (outcome.governance.official_wset_score === true) {
  showError('Governance violation: official_wset_score must be false.');
  return;
}
if (outcome.governance.training_diagnostic_only !== true) {
  showError('Governance violation: training_diagnostic_only must be true.');
  return;
}
```

This gate applies to the outcome payload. An equivalent gate applies to the
item payload on load:

```javascript
if (item.governance.official_wset_question === true) {
  showError('Item governance violation: official_wset_question must be false.');
  return;
}
```

---

## 8. Timing Model

### 8.1 Frontend measurement

```
t0 = Date.now()  // set at question load (LOADING → ANSWERING transition)
tConfirm = Date.now()  // captured at confirmAnswer()
response_time_ms = tConfirm - t0  // integer, always >= 0
```

The current prototype uses seconds (`Math.floor(.../ 1000)`). When the backend
is connected, the frontend must send milliseconds as required by
`diagnostic_outcome_v1.attempt_observation.response_time_ms`.

### 8.2 Timing bands (backend computation)

The backend computes the timing band and interpretation from `response_time_ms`.
These are not computed by the frontend. Reference values:

| Band | Threshold | Backend interpretation |
|---|---|---|
| `fast` | < 15 000 ms | `fluent_recall` or `likely_guess` |
| `expected` | 15 000 – 60 000 ms | `deliberate_reasoning` |
| `slow` | 60 000 – 120 000 ms | `uncertainty_signal` or `hesitation` |
| `very_slow` | > 120 000 ms | `uncertainty_signal` |
| `not_measured` | null response_time_ms | `not_measured` |

The frontend timer color states (blue/amber/red) are visual guides only.
They are keyed to 30s and 60s thresholds for UX reasons and do not need to
align exactly with backend bands.

### 8.3 Hesitation model

```
hesitation_count: int  // number of option changes before confirm
answer_changed: bool = hesitation_count > 0
hesitation_flag: bool = hesitation_count > 0  // matches outcome schema
```

Hesitation is a diagnostic signal, not a penalty. A learner who changed from
C → B (correct final) may have self-corrected. The backend must not penalize
hesitation; it must use it probabilistically in `confidence_alignment`.

### 8.4 Confidence mapping

The frontend confidence UI uses a 1–5 scale. The backend and outcome schema
use `low / medium / high / not_reported`.

| UI label | UI value | Backend value |
|---|---|---|
| INSEG | 1 | `low` |
| POCO | 2 | `low` |
| NEUTRO | 3 | `medium` |
| SEGURO | 4 | `high` |
| MUY SEG | 5 | `high` |
| (not selected) | — | `not_reported` |

The mapping is applied in the frontend before building the attempt payload:

```javascript
function mapConfidence(n) {
  if (!n) return 'not_reported';
  if (n <= 2) return 'low';
  if (n === 3) return 'medium';
  return 'high';
}
```

---

## 9. Panel Field Requirements

### 9.1 Veredicto panel

| Field | Source | Notes |
|---|---|---|
| Correct/incorrect icon | `display.is_correct` | ✓ green / ✗ red |
| Title | `display.veredicto.title` | "RESPUESTA CORRECTA" / "RESPUESTA INCORRECTA" |
| Subtitle | `display.veredicto.subtitle` | Option selected + correct option when wrong |
| Meta line | `display.veredicto.meta` | Time, changes, confidence — shown when data available |
| Timing label | `display.timing_label` | "RÁPIDA / DELIBERADA / LENTA / MUY LENTA" |

The veredicto must never use words implying official scoring. "RESPUESTA
CORRECTA" is acceptable; "APROBADO" or "NOTA: 1" are not.

### 9.2 Distractor / fundamento panel

Rendered when `display.distractor_analysis.active = true` (wrong answer).
Relabelled to "Fundamento de la Respuesta Correcta" when `display.is_correct = true`.

| Field | Source |
|---|---|
| Panel label (wrong) | "Análisis del Distractor" |
| Panel label (correct) | "Fundamento de la Respuesta Correcta" |
| Diagnostic role tag | `display.distractor_analysis.diagnostic_role_display` |
| Why attractive | `display.distractor_analysis.why_attractive` |
| Error reasoning | `display.distractor_analysis.error_reasoning` |
| Correct rationale (correct) | `display.correct_rationale` |

### 9.3 Misconception panel

Rendered only when `display.misconception.active = true`. The backend sets
`active = false` whenever the learner answered correctly, regardless of whether
a misconception node exists for the item. The frontend must not override this.

| Field | Source |
|---|---|
| Panel label | "Misconception Detectada" |
| Misconception ID tag | `display.misconception.id` |
| Misconception name | `display.misconception.name` |
| Misconception description | `display.misconception.description` |

### 9.4 Causal chain panel

Always rendered (collapsed by default). All fields from the outcome `display.causal_chain`.

| Field | Source |
|---|---|
| ID tag | `display.causal_chain.id` |
| Causa | `display.causal_chain.causa` |
| Mecanismo | `display.causal_chain.mecanismo` |
| Efecto | `display.causal_chain.efecto` |
| Formulación de examen | `display.causal_chain.formulacion_examen` |

If `display.causal_chain.active = false` (item has no causal chain), the panel
should be hidden.

### 9.5 SAT panel

Always rendered.

| Field | Source |
|---|---|
| Signal level dot | `display.sat_signal.level` — weak=red / medium=amber / strong=green |
| Level label | `display.sat_signal.level_display` — "SEÑAL DÉBIL / MEDIA / FUERTE" |
| Skill label | `display.sat_signal.skill` |
| Description | `display.sat_signal.description` |

### 9.6 Remediación panel

Always rendered.

| Field | Source |
|---|---|
| Remediation text | `display.remediation.text` |
| Action type | `display.remediation.action_type` (internal, not shown) |
| Action label | `display.remediation.action_label` (shown as next-action tag) |
| Priority indicator | `display.remediation.feedback_priority` — optional visual badge |

Remediation text must be training-only language. Any phrase implying official
exam preparation ("para que apruebes el examen") is outside the governance
boundary and must be scrubbed by the backend before it enters this field.

### 9.7 Session summary overlay

| Field | Source |
|---|---|
| Correct count | Local: `results.filter(r => r.ok).length` / `total` |
| Mastery signal | Local: `correct / total * 100` — labelled "Señal de Maestría · Entrenamiento" |
| Average time | Local: mean of `results[].t` |
| Average hesitations | Local: mean of `results[].hesit` |
| Weak domains | Local: domains of incorrect answers |
| Session notice | "Señales Registradas Localmente" — NEVER "LES Actualizado" |
| LES integration note | Backend responsibility; future phase; not implied in current UI |

---

## 10. Mock-to-Real Migration Plan

Four phases. Each phase is independently shippable.

### Phase 1 — Current (static prototype, complete)

- `frontend/diagnostic-sba/index.html` — self-contained.
- `QS` array: embedded question objects with all diagnostic content inline.
- No HTTP. No backend. No session persistence.
- All content (correct answer, misconception, causal chain, remediation) pre-baked.
- Use: prototype testing, UX validation, Nazareth's first session.

### Phase 2 — Static JSON file (next step after Phase 1 validation)

Replace the embedded `QS` array with a `fetch('./preguntas.json')` call.

```javascript
// Replace the embedded QS array with:
fetch('./preguntas.json')
  .then(function(r) { return r.json(); })
  .then(function(data) {
    QS = data.questions;
    loadQ(0);
  })
  .catch(function(err) { showError('No se pudo cargar las preguntas.'); });
```

`preguntas.json` format:
```json
{
  "schema_version": "preguntas_demo_v1",
  "session_label": "Sesión Diagnóstica · Demo",
  "governance": { "training_item_only": true, "safe_for_examiner": false },
  "questions": [ /* array of item render payloads (Section 3.1) */ ]
}
```

The internal `QS` array format and the frontend rendering logic remain
unchanged. Only the data source changes.

**Prerequisite:** Items must be validated against `diagnostic_sba_item_v1`
before entering `preguntas.json`. Unvalidated items must not enter.

### Phase 3 — Local HTTP endpoint

A minimal local server (FastAPI, Flask, or similar) provides:

```
GET  /api/session          → session_id, item list
GET  /api/item/{item_id}   → item render payload (Section 3.1)
POST /api/attempt          → attempt payload (Section 4.1) → outcome payload (Section 5.1)
```

Frontend changes:
1. Replace `fetch('./preguntas.json')` with `GET /api/session` + per-item fetches.
2. Add `postAttempt(attemptPayload)` function called from `confirmAnswer()`.
3. Replace local outcome derivation with `await postAttempt()` response rendering.
4. Add ERROR state handling (Section 6).
5. Add governance gate (Section 7.3).

The `QS` array is removed. The embedded diagnostic content is removed. The
frontend renders exclusively from server responses.

**Prerequisite:** Phase 4A.7 Attempt Analyzer must exist before Phase 3 can
return genuine diagnostic outcomes.

### Phase 4 — Supabase session persistence (future, separate decision)

Add session persistence for attempt history, LES signal routing, and
cross-session mastery tracking. This requires:

- A Supabase schema for attempts and session records.
- Backend writes on each attempt (not frontend writes).
- Frontend shows backend-confirmed session status, not locally derived mastery.
- LES update claims become backend-driven and explicit ("Señal enviada al LES"),
  never frontend-asserted.

This phase requires its own governance review before implementation.

---

## 11. Risks

### 11.1 Frontend inventing diagnosis

**Risk:** The current static prototype embeds distractor analysis, misconception
descriptions, and SAT signals in the `QS` array. When the backend is connected,
the embedded content could persist and conflict with or override backend-returned
content.

**Mitigation:** In Phase 3, remove all `q.diag.*` fields from the embedded
data entirely. The frontend must have no diagnostic content to fall back on.
If the backend fails, show ERROR state — do not fall back to embedded content.

### 11.2 Official WSET authority leakage

**Risk:** Option text, question stems, or feedback text could inadvertently
replicate protected WSET wording or imply official question authority.

**Mitigation:** Backend-side text safety check (governance contract Section 13
text patterns). Frontend governance gate (Section 7.3). The `official_wset_question`
flag must be `false` on every item; the frontend refuses to render items where
this flag is `true`.

### 11.3 False LES update claims

**Risk:** The frontend session overlay previously said "LES Actualizado" — a
false claim since no backend write occurred. This has been corrected in the
current prototype.

**Mitigation:** The string "LES Actualizado" is permanently forbidden in the
frontend. Any text claiming a real LES write must be sourced from a confirmed
backend response field, not frontend-generated. The approved string is
"Señales Registradas Localmente" in Phase 1 and 2, transitioning to a
backend-confirmed message in Phase 3.

### 11.4 Mastery signal overclaim

**Risk:** The session summary shows a mastery percentage based on
(correct / total) which jumps dramatically with small sample sizes (4 questions).
This could be read as an official readiness signal.

**Mitigation:** Label always reads "Señal de Maestría · Entrenamiento". Add
a note under the percentage when sample size is below a meaningful threshold
(e.g., N < 10): "Señal preliminar — muestra insuficiente para calibración". The
backend mastery signal (from learner model, future phase) supersedes this local
calculation.

### 11.5 Hesitation and timing as ability judgments

**Risk:** Displaying response time and change count prominently could be
interpreted by the learner as a performance penalty or moral judgment.

**Mitigation:** These fields appear in the veredicto meta line as neutral
observations: "Tiempo: Xs · Cambios: N". The timing band label ("DELIBERADA")
is non-evaluative. The backend interpretation ("deliberate_reasoning") is
internal and not surfaced in the UI. No text must imply that slower = worse.

### 11.6 Unsupported distractor analysis

**Risk:** In Phase 1/2, distractor analysis text is hand-authored and not
source-grounded. A learner could treat it as authoritative WSET content.

**Mitigation:** The prototype badge ("PROTOTIPO · ENTRENAMIENTO") is always
visible. In Phase 3, distractor analysis text must pass backend source-grounding
validation before serving. Items failing validation must not enter the question
pool.

### 11.7 Confidence alignment display

**Risk:** Displaying `confidence_alignment = "overconfident_wrong"` to the
learner without careful framing could feel judgmental.

**Mitigation:** The `confidence_alignment` enum value is internal to the
backend and outcome schema. The frontend in Phase 3 should only render a
softened human-readable version if explicitly provided in `display.veredicto.meta`
by the backend. The frontend must not map the enum directly to a displayed
string without a display map reviewed for tone.

---

## 12. Fields the Frontend Requires From Backend (Summary)

### From item payload

```
item_id, item_version, schema_version
curriculum.ra_id, topic, subtopic, difficulty, learning_objective
question.stem, question_type, expected_reasoning_type, estimated_time_seconds
options[].option_id, options[].option_text
sat_relevance[]
display_metadata.domain_label, difficulty_display, sat_skill_label
governance.training_item_only, safe_for_examiner, official_wset_question
```

### From outcome payload

```
identity.outcome_id, item_id, attempt_id
attempt_observation.selected_option_id, is_correct, response_time_ms
attempt_observation.answer_changed, confidence_self_report, hesitation_flag
diagnostic_classification.diagnosed_error_type, confidence_alignment
source_trace.selected_option_diagnostic_role, misconception_id, causal_chain_id
timing_interpretation.timing_band, timing_interpretation
remediation_routing.recommended_next_action, remediation_target_type, feedback_priority
governance.safe_for_examiner, official_wset_score, training_diagnostic_only
display.is_correct, correct_option_id, timing_label
display.veredicto.title, subtitle, meta
display.distractor_analysis.active, diagnostic_role_display, why_attractive, error_reasoning
display.correct_rationale
display.misconception.active, id, name, description
display.causal_chain.active, id, causa, mecanismo, efecto, formulacion_examen
display.sat_signal.level, level_display, skill, description
display.remediation.text, action_type, action_label, feedback_priority
```

---

## 13. Next Frontend Step

**Phase 2 readiness check (when at least 5 validated items exist):**

1. Create `frontend/diagnostic-sba/preguntas.json` with items validated against
   `diagnostic_sba_item_v1`.
2. Replace `var QS = [...]` with `fetch('./preguntas.json')` call in the prototype.
3. Add loading state and error state to the UI state machine.
4. Verify governance gate logic fires for any item with `official_wset_question: true`.
5. Confirm `ds-misc` remains hidden for all correct answers.

**The following must be true before Phase 3 (local HTTP):**

- Phase 4A.7 Attempt Analyzer implemented and tested.
- At least one validated item can produce a real `diagnostic_outcome_v1` payload.
- Backend governance gate rejects items with unsafe governance flags.
- Frontend governance gate (Section 7.3) is implemented.
- The embedded `q.diag.*` fallback path is fully removed.

---

*This document is a design contract. It does not authorize backend implementation,
schema changes, retrieval changes, or LES writes. Those require separate phase
instructions. The governance invariants defined in `docs/DIAGNOSTIC_SBA_GOVERNANCE_CONTRACT.md`
supersede anything in this document if there is a conflict.*
