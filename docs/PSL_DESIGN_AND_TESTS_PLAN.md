# PSL Design and Tests-First Plan
## WSET-AI-System — Pedagogical Strategy Layer

**Auditor:** Claude (Cowork)  
**Date:** 2026-05-30  
**Updated:** 2026-05-31 (baseline commit)  
**Status:** Design document — PSL core implemented and gated OFF. Connections C, D, B, E implemented. 4 connections pending (feedback_intensity, preferred_question_type, scaffolding_policy bridge, explanation_priority).  
**Scope:** Full repo audit + tests-first integration plan for the Pedagogical Strategy Layer

---

## 1. Archivos relevantes encontrados

### PSL core — código ya existente

| Archivo | Descripción |
|---------|-------------|
| `tools/tutor/pedagogical_strategy/__init__.py` | Package init |
| `tools/tutor/pedagogical_strategy/strategy_layer.py` | Facade de integración con gate `ENABLE_PEDAGOGICAL_STRATEGY_LAYER = False`. Extrae señales del `context_package`, llama a `mode_selector`, añade `traceability`. Totalmente inerte cuando el gate está apagado. |
| `tools/tutor/pedagogical_strategy/mode_selector.py` | Selector determinístico. Carga perfil base, aplica 8 reglas de ajuste (`exam_imminent`, `exam_approaching`, `low_confidence`, `causal_gap`, `regional_confusion`, `vague_answer`, `memorization_without_reasoning`, `distinction_goal`), normaliza pesos con floor constraints. Retorna `StrategyDirective` completo. |
| `tools/tutor/pedagogical_strategy/profiles.py` | Cargador y validador de perfiles. Define `ALLOWED_FUNCTIONS` (6), `ALLOWED_TUTOR_MODES` (5), `ALLOWED_VISIBLE_ROLES` (5). Validación de governance en carga. Resolución: `visible_role → tutor_mode → default`. |

### Configuración declarativa

| Archivo | Descripción |
|---------|-------------|
| `knowledge/config/pedagogical_profiles.json` | 5 tutor modes (`mentor`, `trainer`, `reviewer`, `distinction`, `exam_pressure`) + 5 visible roles con pesos de funciones y governance blocks. Schema v1.0.0. |
| `knowledge/config/visible_tutor_characters.json` | 5 personajes ficticios (`Clara`, `Marco`, `Inés`, `Rafael`, `Sofía`) con `strategy_profile_id`, `allowed_modes`, governance. Explícitamente sin personas reales ni autoridad examinadora. |
| `knowledge/config/explanation_priority_config.json` | Configuración de prioridad de explicación usada por `explanation_priority.py` |
| `knowledge/enrichment/pedagogical_roles.schema.json` | Schema JSON de roles pedagógicos |
| `knowledge/enrichment/retrieval_priority_matrix.json` | Matriz de prioridad de recuperación |

### Tests existentes

| Archivo | Descripción |
|---------|-------------|
| `tests/test_pedagogical_strategy_layer.py` | Tests del facade: gate off/on, contratos de las 6 funciones, extracción de señales desde `context_package`, determinismo. ~45 tests. |
| `tests/test_pedagogical_mode_selector.py` | Tests del selector: las 8 reglas individualmente, combinaciones compuestas, clamping de floors, normalización de pesos, cold start, señales derivadas. ~75 tests. |
| `tests/test_pedagogical_profiles.py` | Tests de carga y validación de perfiles. |
| `tests/test_visible_tutor_characters.py` | Tests del config de personajes. |
| `tests/test_adaptive_pedagogical_reasoning.py` | Tests de razonamiento pedagógico adaptativo. |

### Capa de orquestación

| Archivo | Descripción |
|---------|-------------|
| `tools/orchestrator/orchestrator.py` | Loop cognitivo local. `_pedagogical_priority_boost()` es el adaptador legacy — actualmente afecta solo `force_deep_explanation` en `answer_builder.py`. El `strategic_plan` está cableado pero inerte (no llega al `context_package`). |
| `tools/orchestrator/strategic_planner.py` | Planificador determinístico. Señales: `review_topics`, `avoid_topics`, `misconception_focus`, `causal_chain_focus`, `sat_drill_needed`, `difficulty_progression`, `planning_confidence`. Completamente inerte en runtime (no consume el context package). |
| `tools/orchestrator/protocols.py` | Interfaces de protocolo tipadas. |
| `tools/orchestrator/session_ledger.py` | Telemetría de sesión (write-only). |
| `tools/orchestrator/learner_state.py` | Defaults y staging del LES. |
| `tools/orchestrator/les_reconciler.py` | Reconcilia feedback de self-eval en LES. |

### Tutor rendering

| Archivo | Descripción |
|---------|-------------|
| `tools/tutor/answer_builder.py` | Construye respuestas determinísticas. Consume `force_deep_explanation` via `_pedagogical_priority_boost()`. Punto de integración futuro para la PSL. |
| `tools/tutor/scaffolding_policy.py` | Política de scaffolding determinística: `direct_correction`, `guided_explanation`, `hint`, `compressed_reinforcement`, `socratic_questioning`. Actualmente **no conectada** a la PSL. |
| `tools/tutor/explanation_priority.py` | Prioridad de explicación según señales de memoria. |
| `tools/tutor/sat_reasoner.py` | Razonador SAT determinístico. |

### Documentos de gobernanza

| Archivo | Descripción |
|---------|-------------|
| `docs/PEDAGOGICAL_CLASSIFICATION_SYSTEM.md` | 9 roles pedagógicos (`foundational`, `reinforcement`, `misconception_correction`, `exam_strategy`, `advanced_enrichment`, `tasting_alignment`, `linkage_training`, `concise_answer_training`, `distinction_training`). Matriz de interacción con retrieval. |
| `docs/AGENT_BOUNDARIES.md` | Especificación de separación Tutor/Examiner. Invariante: la PSL es dominio del Tutor únicamente. |
| `docs/EXAMINER_CALIBRATION_RULES.md` | Reglas del Examiner Agent. La PSL debe ser invisible para este agente. |
| `docs/STRATEGIC_PLANNER_CONTRACT.md` | Contrato semántico entre `strategic_planner` y `_pedagogical_priority_boost()`. Define separación de `answer_depth`, `difficulty_progression`, `pedagogical_mode`. |
| `docs/PLANNER_INFLUENCE_BOUNDARY.md` | Límite de influencia del planner. Clasificación ALLOWED/CONDITIONALLY_ALLOWED/FORBIDDEN para cada señal. |
| `docs/governance_risk_matrix.md` | Matriz de riesgos. Identifica brechas activas: calibration gate sin código, logging ausente, corpus Diploma sin etiqueta. |
| `CLAUDE.md` | Invariantes de gobernanza inmutables. Fuente de verdad para las constantes en `tools/constants.py`. |

### Prompts

| Archivo | Descripción |
|---------|-------------|
| `prompts/tutor-agent.md` | Prompt del Tutor Agent. Define método de enseñanza, restricciones, patrones de output. No referencia la PSL directamente — punto de integración pendiente. |
| `prompts/examiner-agent.md` | Prompt del Examiner Agent (vacío — 1 línea). |
| `prompts/orchestrator.md` | Prompt del Orchestrator (pendiente). |

---

## 2. Arquitectura propuesta — Pedagogical Strategy Layer

### 2.1 Mapa de capas

```
┌─────────────────────────────────────────────────────────────────────┐
│                    RUNTIME VISIBLE TO STUDENT                       │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │  VISIBLE TUTOR ROLES  (what student sees)                    │   │
│  │  Clara · Marco · Inés · Rafael · Sofía                       │   │
│  │  Fictional original characters — no real person, no examiner │   │
│  └──────────────────┬───────────────────────────────────────────┘   │
│                     │ maps to strategy_profile_id                   │
│  ┌──────────────────▼───────────────────────────────────────────┐   │
│  │  TUTOR MODES  (behavioral configurations)                    │   │
│  │  mentor · trainer · reviewer · distinction · exam_pressure   │   │
│  │  Each mode = a named weight vector over internal functions    │   │
│  └──────────────────┬───────────────────────────────────────────┘   │
└─────────────────────┼───────────────────────────────────────────────┘
                      │ resolved by profiles.get_profile()
┌─────────────────────▼───────────────────────────────────────────────┐
│            PEDAGOGICAL STRATEGY LAYER (PSL)                         │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │  INTERNAL FUNCTIONS  (pure cognitive logic — NOT personas)     │  │
│  │                                                                │  │
│  │  cartographer  — spatial/relational orientation                │  │
│  │  scientist     — causal mechanism + evidence chains           │  │
│  │  host          — emotional support + engagement floor         │  │
│  │  storyteller   — narrative + analogy + memory encoding        │  │
│  │  critic        — precision + gap identification               │  │
│  │  challenger    — adversarial probing + assumption testing     │  │
│  │                                                                │  │
│  │  Weight vector = StrategyDirective (deterministic)            │  │
│  └────────────────┬───────────────────────────────────────────────┘  │
│                   │                                                   │
│  ┌────────────────▼───────────────────────────────────────────────┐  │
│  │  ADJUSTMENT RULES  (8 deterministic rules)                     │  │
│  │  exam_imminent · exam_approaching · low_confidence             │  │
│  │  causal_gap · regional_confusion · vague_answer                │  │
│  │  memorization_without_reasoning · distinction_goal             │  │
│  └────────────────┬───────────────────────────────────────────────┘  │
│                   │                                                   │
│  ┌────────────────▼───────────────────────────────────────────────┐  │
│  │  SIGNAL EXTRACTION LAYER                                       │  │
│  │  context_package → LES → scaffolding → planner (advisory)     │  │
│  └────────────────┬───────────────────────────────────────────────┘  │
└────────────────────┼────────────────────────────────────────────────┘
                     │ StrategyDirective (dict, fully auditable)
┌────────────────────▼────────────────────────────────────────────────┐
│            INTEGRATION POINTS  (consume StrategyDirective)          │
│                                                                      │
│  scaffolding_policy.py  ←  emotional_support_level + challenge_level│
│  answer_builder.py      ←  causal_depth_required + feedback_intensity│
│  explanation_priority   ←  preferred_question_type (advisory)       │
│  session_ledger         ←  rules_applied + profile_id (audit log)   │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│            FUTURE AVATARS STUB  (out of scope)                      │
│  Interface defined: avatar_id → visible_role → strategy_profile_id  │
│  No implementation. No AI persona. No roleplay. Slot reserved only. │
└─────────────────────────────────────────────────────────────────────┘
```

### 2.2 Separación conceptual estricta

| Capa | Qué es | Qué NO es |
|------|--------|-----------|
| **Funciones internas** | Lógica pura de estrategia cognitiva. Pesos abstractos sobre dimensiones de enseñanza. Sin nombres de persona, sin roleplay, sin API, sin LLM. | Personas. Agentes. Avatares. Simulaciones de examinador. |
| **Tutor modes** | Configuraciones de comportamiento nombradas. Cada modo = un vector de pesos base que puede ser modulado por reglas de ajuste. | Modos de IA. Prompts de persona. Instrucciones de roleplay. |
| **Visible tutor roles** | Lo que el estudiante ve. Personajes ficticios originales enlazados a `strategy_profile_id`. Sin nombre de persona real, sin autoridad de examinador. | Imitación de personas reales. Examinadores oficiales. |
| **Future avatars** | Slot de interfaz reservado. `avatar_id → visible_role → strategy_profile_id`. Sin implementación, sin IA, sin gráficos generados. | Cualquier cosa con nombre de persona real, likeness, o autoridad WSET. |

### 2.3 Contratos de integración

#### 2.3.1 PSL → `scaffolding_policy.py`

La PSL debe alimentar `select_scaffolding_policy()` con señales derivadas del `StrategyDirective`:

```python
# Mapeo propuesto (no implementar hasta paso 4)
psl_directive = build_pedagogical_strategy(context_package=pkg)

scaffolding_input = {
    "mastery_probability":      _from_les(pkg),
    "cognitive_load":           _derive_load(psl_directive),   # NEW
    "urgency":                  _derive_urgency(psl_directive), # NEW
    "misconception_severity":   _from_prepass(pkg),
}
scaffolding = select_scaffolding_policy(**scaffolding_input)
```

- `cognitive_load` = "high" si `emotional_support_level == "low"` y `feedback_intensity == "high"` (examiner pressure scenario)  
- `urgency` = "high" si `challenge_level == "high"` y `exam_days_remaining ≤ 14`

Ambas derivaciones son **reglas determinísticas**, no LLM.

#### 2.3.2 PSL → `answer_builder.py`

El `StrategyDirective` debe inyectarse en el `context_package` bajo la clave `"psl_directive"` (solo cuando el gate está activo). El `answer_builder` consumirá:

- `causal_depth_required` → reemplaza/complementa la lógica de `force_deep_explanation`
- `feedback_intensity` → modula el nivel de detalle en las secciones de feedback
- `preferred_question_type` → guía el tipo de mini-practice prompt
- `remediation_style` → guía el estilo de las secciones correctivas

**Invariante:** el `answer_builder` debe poder operar SIN `psl_directive` (gate off = comportamiento actual sin cambios).

#### 2.3.3 PSL → `strategic_planner.py` (relación de señales)

La PSL NO lee del planner directamente. El planner es una señal de entrada opcional al `_extract_signals()` de `strategy_layer.py`. Flujo propuesto:

```
strategic_plan.difficulty_progression → "escalate"/"consolidate"/"stable"
                                       ↓
                        _extract_signals() puede leer esto como
                        señal de ajuste de learning_goal
                        (solo si planning_confidence > 0.1)
```

Esta influencia es **advisory-only** y unidireccional. La PSL nunca escribe al planner.

#### 2.3.4 PSL → `session_ledger.py`

Cada invocación del PSL cuando el gate está activo debe añadir un campo `psl_trace` al ledger:

```json
{
  "profile_id": "revisor_respuestas",
  "rules_applied": ["exam_approaching", "vague_answer"],
  "causal_depth_required": "standard",
  "feedback_intensity": "high",
  "challenge_level": "medium"
}
```

Sin texto libre. Sin queries. Sin contenido del estudiante. Solo metadatos de estrategia.

### 2.4 Future avatars — solo la interfaz

```python
# STUB ONLY — no implementation until explicit activation
# File: tools/tutor/pedagogical_strategy/avatar_stub.py

AVATAR_INTERFACE = {
    # avatar_id → visible_role (maps to strategy_profile_id)
    # This table is the only runtime artifact for avatars.
    # Avatars are presentation-layer only. They carry zero cognitive authority.
    # No AI generation. No real-person likenesses. No roleplay personas.
}

def resolve_avatar_to_role(avatar_id: str) -> str | None:
    """Return the visible_role for a given avatar_id, or None if unknown."""
    return AVATAR_INTERFACE.get(avatar_id)
```

**Por qué stub-only:** Los avatares son una capa de presentación que no afecta la lógica pedagógica. La PSL trabaja sobre `strategy_profile_id`. El avatar es solo la ruta de entrada al `profile_id`. Implementar la presentación de avatares antes de tener la PSL activa invierte el orden de dependencias y crea riesgo de roleplay no gobernado.

---

## 3. Riesgos

### R-PSL-01 — Examiner mode leakage a través de tutor mode `exam_pressure`

**Descripción:** El modo `exam_pressure` tiene `critic=0.25` y `challenger=0.25`. Si la señal `safe_for_examiner` o `examiner_scoring_allowed` se filtra desde este modo hacia el `answer_builder`, el Tutor podría actuar como examinador.

**Severidad:** Alta  
**Mitigación:** El `StrategyDirective` siempre tiene `safe_for_examiner=False` y `examiner_scoring_allowed=False` hardcodeados. Los tests de governance deben verificar esto para CADA modo y CADA combinación de reglas. El `answer_builder` debe verificar estos flags antes de cualquier renderizado PSL.

---

### R-PSL-02 — Snapshot drift al activar el gate

**Descripción:** Cuando `ENABLE_PEDAGOGICAL_STRATEGY_LAYER = True`, el `StrategyDirective` fluye al `answer_builder`. Cualquier cambio en `causal_depth_required` o `feedback_intensity` puede alterar los 25 snapshots congelados.

**Severidad:** Alta  
**Mitigación:** El gate debe permanecer `False` en producción hasta que los snapshots sean regenerados deliberadamente. Todo test de integración PSL↔answer_builder debe usar snapshots separados o usar el gate local. **Nunca activar el gate globalmente sin regeneración explícita y revisada de snapshots.**

---

### R-PSL-03 — Roleplay por nombre de personaje visible

**Descripción:** Los personajes (Clara, Marco, Inés, etc.) podrían ser usados como system prompt personas en un LLM futuro. Si el `display_name` o `role_label` llega al prompt del Tutor como instrucción de roleplay, se violaría la separación función/persona.

**Severidad:** Alta  
**Mitigación:** Los personajes son **presentation-layer only**. Su `display_name` nunca debe aparecer en el system prompt del Tutor Agent como instrucción de comportamiento. El `strategy_profile_id` es el único campo que fluye hacia la PSL. El `display_name` es para la UI únicamente.

---

### R-PSL-04 — Inflación de señales desde `_extract_signals()`

**Descripción:** `_extract_signals()` actualmente lee solo `mastery` y `learning_goal` del LES. Si en el futuro se añaden más señales (e.g., `exam_days_remaining` desde el LES), puede haber conflicto con señales explícitas pasadas vía `extra_context`.

**Severidad:** Media  
**Mitigación:** La regla actual de precedencia (`extra_context` wins) debe preservarse. Cualquier nueva señal en `_extract_signals()` debe tener un test explícito de que `extra_context` la sobreescribe.

---

### R-PSL-05 — Deriva semántica entre `ADJUSTMENT_RULES` y perfiles base

**Descripción:** Si se añaden nuevos perfiles a `pedagogical_profiles.json` con pesos base que ya tienen `challenger` alto, las reglas `exam_imminent` pueden empujar `challenger` más allá de lo intencionado antes del clamping.

**Severidad:** Media  
**Mitigación:** El floor constraint (`FUNCTION_MIN_WEIGHT=0.02`, `HOST_MIN_WEIGHT=0.08`) protege el piso pero no el techo. Cualquier perfil nuevo debe tener un test de que bajo las peores combinaciones de reglas, `safe_for_examiner` permanece `False` y `host >= HOST_MIN_WEIGHT`.

---

### R-PSL-06 — PSL como fuente de autoridad de scoring indirecta

**Descripción:** `feedback_intensity="high"` en la PSL podría ser interpretado por el `answer_builder` como autorización para dar feedback de tipo "scoring". La distinción entre feedback pedagógico de alta intensidad y scoring oficial es semántica, no estructural.

**Severidad:** Alta  
**Mitigación:** El `answer_builder` nunca debe usar `feedback_intensity` como señal para activar lenguaje de scoring ("tu respuesta ganaría X puntos"). El test de governance debe verificar que ningún output del PSL contiene campos `score`, `marks`, `grade`, o `band`.

---

### R-PSL-07 — Conexión prematura PSL → retrieval

**Descripción:** El `PLANNER_INFLUENCE_BOUNDARY.md` clasifica como `FORBIDDEN` cualquier influencia de la PSL sobre retrieval scoring o ranking. Si la PSL se conecta a retrieval antes de que la infraestructura de trazabilidad esté lista, se introducen decisiones no auditables.

**Severidad:** Alta  
**Mitigación:** La PSL **no debe tener influencia sobre retrieval en ninguna fase de este plan**. La ruta PSL→retrieval es dominio del `strategic_planner` y requiere un plan separado. La PSL opera aguas abajo del retrieval, no aguas arriba.

---

### R-PSL-08 — Avatar stub sin contrato de activación

**Descripción:** Si el stub de avatares se extiende sin una especificación de activación, puede crearse una ruta donde `avatar_id` llega al prompt del Tutor y genera comportamiento de roleplay.

**Severidad:** Media  
**Mitigación:** El stub debe incluir un test explícito de que `resolve_avatar_to_role()` solo retorna `None` o un string de `ALLOWED_VISIBLE_ROLES` — nunca texto libre, nunca un nombre de persona.

---

## 4. Tests necesarios (tests-first)

Los tests existentes (`test_pedagogical_strategy_layer.py`, `test_pedagogical_mode_selector.py`) cubren bien la lógica interna de la PSL. Los tests faltantes se organizan a continuación por nuevo módulo de test.

---

### 4.1 Tests unitarios

#### `tests/test_psl_scaffolding_integration.py`

**TEST-U-01: `test_high_challenge_maps_to_high_urgency`**
- Verifica: `challenge_level="high"` en PSL → `urgency="high"` en scaffolding input
- Input: `StrategyDirective(challenge_level="high", exam_days_remaining=7)`
- Expected: `scaffolding_input["urgency"] == "high"`
- Constraint: deterministic-first

**TEST-U-02: `test_low_emotional_support_maps_to_high_cognitive_load`**
- Verifica: `emotional_support_level="low"` + `feedback_intensity="high"` → `cognitive_load="high"` en scaffolding
- Input: directive de `exam_pressure` mode
- Expected: `scaffolding_input["cognitive_load"] == "high"`
- Constraint: deterministic-first

**TEST-U-03: `test_scaffolding_policy_remains_governance_clean_via_psl`**
- Verifica: el resultado de `select_scaffolding_policy()` alimentado por PSL nunca tiene `safe_for_examiner=True` ni `examiner_scoring_allowed=True`
- Input: todos los modos posibles
- Expected: governance flags = False en todos los casos
- Constraint: governance-first

**TEST-U-04: `test_scaffolding_policy_noop_when_gate_off`**
- Verifica: cuando `ENABLE_PEDAGOGICAL_STRATEGY_LAYER=False`, el scaffolding se calcula igual que antes (no cambia por PSL)
- Input: context_package con mastery="medium"
- Expected: output idéntico al baseline sin PSL
- Constraint: deterministic-first

**TEST-U-05: `test_host_dominant_produces_scaffolded_act`**
- Verifica: perfil `mentor_fundamentos` (host=0.35) → acto de scaffolding no adversarial
- Input: PSL gate on, tutor_role="mentor_fundamentos", mastery_probability=0.3
- Expected: `scaffolding_act in {"guided_explanation", "hint"}` (no "direct_correction")
- Constraint: consistencia semántica función/comportamiento

**TEST-U-06: `test_critic_dominant_produces_direct_correction_or_socratic`**
- Verifica: perfil `revisor_respuestas` (critic=0.35) con `recent_error_type="vague_answer"` → acto de scaffolding de alta precisión
- Input: mastery_probability=0.6
- Expected: `scaffolding_act in {"direct_correction", "socratic_questioning"}`
- Constraint: consistencia semántica

---

#### `tests/test_psl_signal_extraction_extended.py`

**TEST-U-07: `test_extra_context_wins_over_les_mastery`**
- Verifica: si el LES dice `mastery="low"` pero `extra_context={"learner_confidence": "high"}`, la confianza es "high"
- Expected: `"low_confidence"` NOT in `rules_applied`
- Constraint: precedencia de señales explícitas

**TEST-U-08: `test_strategic_plan_difficulty_read_as_advisory`**
- Verifica: cuando `strategic_plan.difficulty_progression="escalate"` se pasa como señal, el PSL puede (no debe obligatoriamente) ajustar el learning_goal
- Input: extra_context={"strategic_plan_difficulty": "escalate"}, planning_confidence=0.5
- Expected: NO exception; governance clean; output determinístico
- Constraint: advisory-only, no mandatory

**TEST-U-09: `test_signal_extraction_does_not_mutate_context_package`**
- Verifica: `_extract_signals()` nunca modifica el `context_package` original
- Input: context_package complejo con LES y memory
- Expected: `context_package == original_copy` después de llamada
- Constraint: no side effects

**TEST-U-10: `test_none_signals_produce_cold_start_default`**
- Verifica: ninguna señal → perfil default, rules_applied=[], governance clean
- Input: `build_pedagogical_strategy()` sin argumentos, gate on
- Expected: `profile_id="default"`, `rules_applied=[]`, todas las governance flags False
- Constraint: deterministic-first, cold-start safe

---

#### `tests/test_avatar_stub.py`

**TEST-U-11: `test_avatar_resolve_returns_allowed_role_or_none`**
- Verifica: `resolve_avatar_to_role(avatar_id)` retorna solo strings de `ALLOWED_VISIBLE_ROLES` o `None`
- Input: todos los avatar_ids conocidos + un id desconocido
- Expected: retorno en `ALLOWED_VISIBLE_ROLES | {None}` siempre
- Constraint: no roleplay, no free text

**TEST-U-12: `test_avatar_stub_never_returns_real_person_name`**
- Verifica: ningún valor en `AVATAR_INTERFACE` contiene nombres en `FORBIDDEN_REAL_NAMES` (hardcoded set de nombres reales conocidos)
- Expected: assertion sobre todos los valores del dict
- Constraint: no real-person imitation

**TEST-U-13: `test_avatar_stub_maps_to_strategy_profile_id`**
- Verifica: el `strategy_profile_id` resultante de un avatar_id existe en `pedagogical_profiles.json`
- Input: todos los avatar_ids
- Expected: profile_id encontrado en config
- Constraint: consistency

---

### 4.2 Tests de integración

#### `tests/test_psl_answer_builder_integration.py`

**TEST-I-01: `test_psl_directive_injected_in_context_package_when_gate_on`**
- Verifica: cuando gate activo, `context_package["psl_directive"]` está presente y tiene todos los campos requeridos
- Input: run_orchestrator con `ENABLE_PEDAGOGICAL_STRATEGY_LAYER=True` (local override)
- Expected: `"psl_directive"` in context_package, governance flags False
- Constraint: governance-first

**TEST-I-02: `test_psl_directive_absent_from_context_package_when_gate_off`**
- Verifica: gate off → `"psl_directive"` NO está en `context_package`
- Expected: `"psl_directive"` NOT in context_package
- Constraint: zero side effects when gate off

**TEST-I-03: `test_answer_builder_unchanged_when_psl_absent`**
- Verifica: output del answer_builder con y sin `psl_directive` en context_package es idéntico cuando el builder no consume PSL aún
- Input: mismo context_package, con y sin `psl_directive`
- Expected: outputs iguales
- Constraint: backward compatibility, snapshot safety

**TEST-I-04: `test_causal_depth_required_deep_activates_deep_explanation`**
- Verifica: `psl_directive["causal_depth_required"] == "deep"` → answer_builder usa modo deep
- Input: PSL gate on, tutor_role="investigador_causalidad", recent_error_type="causal_gap"
- Expected: `_determine_explanation_depth()` retorna "deep"
- Constraint: deterministic-first (no LLM decision)

**TEST-I-05: `test_feedback_intensity_high_does_not_activate_scoring_language`**
- Verifica: `feedback_intensity="high"` nunca produce campos `score`, `marks`, `grade`, `band`, o `examiner_verdict` en el output del answer_builder
- Input: tutor_role="revisor_respuestas", recent_error_type="vague_answer"
- Expected: ninguno de los campos prohibidos en el output
- Constraint: no official scoring, governance-first

**TEST-I-06: `test_psl_integration_snapshot_invariance`**
- Verifica: con gate off (default), los 25 snapshots no cambian
- Input: run completo con retrieval → answer_builder para todos los fixtures
- Expected: todos los snapshots igual que antes
- Constraint: snapshot-tested cognition

---

### 4.3 Tests de gobernanza y seguridad

#### `tests/test_psl_governance.py`

**TEST-G-01: `test_governance_flags_always_false_all_modes`**
- Verifica: para todos los tutor modes y visible roles, `safe_for_examiner=False` y `examiner_scoring_allowed=False`
- Input: todos los valores de `ALLOWED_TUTOR_MODES` y `ALLOWED_VISIBLE_ROLES`, con y sin señales de contexto
- Expected: governance flags False en TODOS los casos
- Constraint: invariante absoluto

**TEST-G-02: `test_governance_flags_always_false_all_rule_combinations`**
- Verifica: para todas las combinaciones posibles de reglas disparadas simultáneamente, governance flags permanecen False
- Input: combinaciones de las 8 reglas (subset representativo)
- Expected: governance flags False en todos
- Constraint: invariante absoluto

**TEST-G-03: `test_no_score_marks_grade_fields_in_directive`**
- Verifica: el `StrategyDirective` no contiene ningún campo de scoring en ningún caso
- Input: todos los modos y roles
- Expected: `{"score", "marks", "grade", "band", "examiner_verdict", "official_result"}` ∩ directive.keys() == ∅
- Constraint: no official scoring

**TEST-G-04: `test_psl_does_not_modify_snapshots_silently`**
- Verifica: activar y desactivar el gate no produce diferencias en los snapshots congelados
- Input: gate on y off sobre los 25 fixtures
- Expected: snapshots idénticos independientemente del gate
- Constraint: snapshot protection (mientras el answer_builder no consuma PSL)

**TEST-G-05: `test_psl_uses_no_llm_no_api_no_embeddings`**
- Verifica: la PSL no importa ningún módulo que haga llamadas externas
- Expected: `{"openai", "anthropic", "requests", "httpx", "aiohttp", "sklearn", "faiss", "chromadb"}` ∩ all_imports == ∅
- Constraint: no LLM/API/cloud, no embeddings, no vector DB

**TEST-G-06: `test_psl_is_stateless_same_input_same_output`**
- Verifica: llamar a `build_pedagogical_strategy` dos veces con los mismos inputs produce exactamente el mismo output
- Input: combinación compleja de señales
- Expected: output_1 == output_2 (dict equality)
- Constraint: deterministic-first

**TEST-G-07: `test_psl_traceability_block_present_and_complete`**
- Verifica: con gate on, el `StrategyDirective` incluye `traceability` con `evidence_required=True` y `official_scoring=False`
- Input: cualquier invocación con gate on
- Expected: `traceability["evidence_required"] == True`, `traceability["official_scoring"] == False`
- Constraint: governance-first, auditability

**TEST-G-08: `test_psl_ledger_trace_governance_clean`**
- Verifica: el `psl_trace` escrito al session_ledger no contiene campos de scoring ni texto libre del estudiante
- Input: invocación PSL + write al ledger
- Expected: trace contiene solo `profile_id`, `rules_applied`, y señales derivadas (sin queries, sin content)
- Constraint: governance-first, no learner data exposure

**TEST-G-09: `test_visible_role_characters_no_real_person`**
- Verifica: ningún personaje en `visible_tutor_characters.json` tiene `governance.safe_for_examiner=True` o contiene texto que impersone una persona real
- Input: todos los 5 personajes
- Expected: governance flags False, `governance_notes` field presente en cada uno
- Constraint: no real-person imitation, no examiner authority

**TEST-G-10: `test_exam_pressure_mode_never_claims_official_scoring`**
- Verifica: el modo `exam_pressure` con `exam_imminent` + `distinction_goal` no produce ninguna indicación de scoring oficial
- Input: tutor_mode="exam_pressure", exam_days_remaining=7, learning_goal="distinction"
- Expected: governance flags False, no score fields
- Constraint: governance-first (caso más adversarial)

---

## 5. Orden de implementación recomendado

### Paso 1 — Escribir los tests antes de cualquier código
**Qué:** Crear los archivos de test vacíos con las especificaciones del §4 como docstrings. Marcar todos como `@unittest.skip("Not implemented yet")`.  
**Por qué:** Tests-first significa que la especificación existe antes que la implementación. Los tests son el contrato.  
**Tests que desbloquea:** TEST-G-01 a TEST-G-10 (governance baseline).

---

### Paso 2 — Implementar el `avatar_stub.py`
**Qué:** Crear `tools/tutor/pedagogical_strategy/avatar_stub.py` con el dict `AVATAR_INTERFACE` y la función `resolve_avatar_to_role()`.  
**Por qué:** Es el cambio de menor blast radius. No afecta ningún componente existente. Desbloquea el contrato de interfaz de avatares.  
**Tests que desbloquea:** TEST-U-11, TEST-U-12, TEST-U-13. Eliminar `@skip` de esos tests.  
**Verificación:** `python -m unittest tests.test_avatar_stub -v` → verde. Suite completa sin regresión.

---

### Paso 3 — Extender `_extract_signals()` en `strategy_layer.py`
**Qué:** Añadir extracción de señales desde `strategic_plan.difficulty_progression` (advisory, con guard de `planning_confidence`). Añadir test de no-mutación.  
**Por qué:** Conectar PSL con el planner de forma advisory-only es el primer puente inter-capas de bajo riesgo.  
**Tests que desbloquea:** TEST-U-07 a TEST-U-10. Eliminar `@skip`.  
**Verificación:** suite completa verde. Snapshots sin cambio (gate off).

---

### Paso 4 — Implementar la derivación PSL → scaffolding_policy
**Qué:** Crear la función `_psl_to_scaffolding_hints(directive) -> dict` en `strategy_layer.py` que traduce `emotional_support_level` + `challenge_level` → `{"cognitive_load": ..., "urgency": ...}`.  
**Por qué:** La scaffolding_policy es la integración más segura — no afecta retrieval, no afecta snapshots, no modifica el `context_package`.  
**Tests que desbloquea:** TEST-U-01 a TEST-U-06. Eliminar `@skip`.  
**Verificación:** suite completa verde. Snapshots sin cambio.

---

### Paso 5 — Inyectar `psl_directive` en `context_package` (solo observacional)
**Qué:** Cuando `ENABLE_PEDAGOGICAL_STRATEGY_LAYER=True`, añadir `psl_directive` al `context_package` en el orchestrator. El `answer_builder` lo ignora completamente (no consume aún).  
**Por qué:** Hace el directive visible para inspección y logging sin cambiar ningún comportamiento de rendering.  
**Tests que desbloquea:** TEST-I-01, TEST-I-02, TEST-I-03. Eliminar `@skip`.  
**Verificación:** suite completa verde. **Snapshots sin cambio (crítico — el answer_builder no consume aún).**

---

### Paso 6 — Escribir al `session_ledger` el `psl_trace`
**Qué:** Extender `append_to_ledger()` con campo opcional `psl_trace` cuando `psl_directive` está presente.  
**Por qué:** Establece el trail de auditoría antes de que la PSL tenga influencia real. Se puede auditar qué estrategia se habría seleccionado.  
**Tests que desbloquea:** TEST-G-08. Eliminar `@skip`.  
**Verificación:** `test_session_ledger.py` y suite completa verdes. Snapshots sin cambio.

---

### Paso 7 — Conectar PSL → `answer_builder.py` (causal_depth y feedback_intensity)
**Qué:** En `answer_builder._determine_explanation_depth()`, si `context_package["psl_directive"]` existe y el gate está activo, usar `causal_depth_required` como señal adicional (junto con la existente de `force_deep_explanation`).  
**Por qué:** Este es el primer cambio de comportamiento real. Debe estar precedido por todos los pasos anteriores y los tests de integración verdes.  
**Prerequisito obligatorio:** Todos los tests TEST-I-01 a TEST-I-05 verdes con `@skip` removido antes de codificar.  
**Tests que desbloquea:** TEST-I-04, TEST-I-05. Eliminar `@skip`.  
**Verificación:** suite completa verde. **Correr snapshot regression ANTES y DESPUÉS. Si algún snapshot cambia, revisar manualmente, justificar, y regenerar explícitamente — nunca actualizar silenciosamente.**

---

### Paso 8 — Activación gradual del gate con registro de observaciones
**Qué:** Mantener `ENABLE_PEDAGOGICAL_STRATEGY_LAYER = False` globalmente. Activar solo en tests de integración mediante override local. Documentar en `CLAUDE.md` los criterios de activación global.  
**Por qué:** La activación global requiere: (1) todos los tests del §4 verdes, (2) regeneración explícita de snapshots aprobada, (3) brutal self-eval sin regression.  
**Criterios de activación global (NO activar hasta que todos sean True):**  
- [ ] `python -m unittest discover -s tests -v` → 660+ passing, zero errors  
- [ ] Todos los tests PSL en §4 verdes  
- [ ] Brutal self-eval → zero failure labels  
- [ ] Snapshots regenerados deliberadamente y revisados  
- [ ] `psl_trace` visible en ledger para al menos 10 sesiones reales de prueba  
- [ ] Ningún snapshot cambió inesperadamente en el paso 7

---

## 6. Cambios que NO deben hacerse

### 6.1 Violaciones de governance

| Cambio prohibido | Razón |
|-----------------|-------|
| `safe_for_examiner = True` en cualquier perfil, modo, o personaje | Invariante absoluto. Violación de governance. |
| `examiner_scoring_allowed = True` en cualquier perfil | Invariante absoluto. |
| Añadir campos `score`, `marks`, `grade`, `band`, o `examiner_verdict` al `StrategyDirective` | La PSL no tiene autoridad de scoring. |
| Hacer que `exam_pressure` mode se presente al estudiante como "modo examinador" | El modo es pedagógico, no evaluativo. |
| Usar el `display_name` de un personaje en el system prompt del Tutor como instrucción de roleplay | Los personajes son presentation-layer; no deben ser personas en el prompt. |
| Imitación de cualquier persona real en los personajes visibles | Violación de governance de personajes. |

### 6.2 Violaciones de determinismo y arquitectura

| Cambio prohibido | Razón |
|-----------------|-------|
| Añadir llamadas a LLM, API, o embeddings dentro de la PSL | El PSL es determinístico por diseño. Cualquier dependencia de LLM rompe la auditabilidad. |
| Hacer que la PSL influya en retrieval scoring o ranking | `PLANNER_INFLUENCE_BOUNDARY.md` §2 clasifica esto como FORBIDDEN. |
| Inyectar nodos de retrieval forzados desde la PSL | Dominio exclusivo del `misconception_prepass`. |
| Añadir `random` o `time.time()` como inputs al `mode_selector` | Rompe el determinismo. |
| Hacer que `build_pedagogical_strategy()` tenga side effects | Es una función pura. No debe escribir a ningún archivo, memoria, o estado externo. |

### 6.3 Violaciones de snapshot safety

| Cambio prohibido | Razón |
|-----------------|-------|
| Activar `ENABLE_PEDAGOGICAL_STRATEGY_LAYER = True` globalmente sin regenerar snapshots | Los snapshots son el test de regresión más importante del sistema. |
| Modificar los snapshots congelados sin justificación documentada | Cada cambio de snapshot debe ser un cambio deliberado y revisado. |
| Conectar la PSL al `answer_builder` sin ejecutar `test_tutor_snapshot_regression` antes y después | La PSL puede cambiar `causal_depth_required`, lo que afecta el rendering. |

### 6.4 Violaciones de separación de capas

| Cambio prohibido | Razón |
|-----------------|-------|
| Hacer que el `StrategyDirective` se propague al `examiner_corpus` | La PSL es dominio del Tutor únicamente. |
| Leer señales del Examiner Agent en la PSL | Viola la separación Tutor/Examiner de `AGENT_BOUNDARIES.md`. |
| Usar el `StrategyDirective` para modificar el LES directamente | Solo `les_reconciler.py` escribe al LES. |
| Hacer que el planner lea de la PSL o viceversa en forma circular | La PSL lee señales del planner (advisory). El planner no lee de la PSL. |
| Añadir lógica de `pedagogical_mode` (exploration/reinforcement/remediation) a la PSL antes de definirla en el `strategic_planner` | `STRATEGIC_PLANNER_CONTRACT.md` §3 lo asigna al planner como Phase 2 target. |

### 6.5 Violaciones de gobernanza de personajes / avatares

| Cambio prohibido | Razón |
|-----------------|-------|
| Activar `AVATAR_INTERFACE` con personajes fuera de `ALLOWED_VISIBLE_ROLES` | Los avatares solo pueden mapear a roles válidos. |
| Añadir `avatar_id` como field al `StrategyDirective` | Los avatares son presentation-layer; no pertenecen al cognitive layer. |
| Implementar avatares generativos (AI-generated images o voices) antes de tener la PSL estable | Invierte el orden de dependencias. Los avatares dependen de la PSL, no al revés. |
| Usar el nombre de un personaje como instrucción en el prompt de cualquier agente | El nombre es UI. La estrategia es la PSL. No mezclar. |

---

*Este documento es un plan de arquitectura y tests. No representa implementación, evaluación oficial de WSET, ni autoridad de examinador.*  
*Generado: 2026-05-30 | Claude (Cowork) — Audit Role | Requiere revisión humana antes de actuar sobre las recomendaciones.*
