# WSET-AI-System — Auditoría Técnica Completa
**Fecha:** 2026-05-28  
**Propósito:** Briefing técnico para orientar la planificación de las siguientes fases del proyecto.  
**Audiencia:** Asistente de IA sin contexto previo del proyecto.

---

## 1. ¿Qué es este sistema?

WSET-AI-System es un **tutor inteligente determinista y local** para preparar el examen WSET Level 3 (Wine & Spirit Education Trust). Está siendo construido para un estudiante específico llamado Nazareth.

### Filosofía de diseño

El sistema está construido bajo una premisa inusual y deliberada: **recuperación estructurada primero, generación nunca**. Esto significa:

- No usa LLMs en tiempo de inferencia.
- No usa embeddings ni bases de datos vectoriales.
- No hace llamadas a APIs externas.
- No tiene frontend aún.
- Todo output es reproducible: la misma consulta siempre produce la misma respuesta.

Esta decisión fue tomada porque el sistema es *exam-adjacent*: el riesgo principal no es falta de fluidez, sino **autoridad no respaldada, drift de calibración, overclaim de puntuación y cambios de comportamiento cognitivo imposibles de auditar**. Al ser completamente determinista y basado en recuperación de fuentes explícitas, el sistema es inspeccionable, testeable con snapshots y gobernado.

### Invariantes de gobernanza (NUNCA se pueden cambiar)

```python
safe_for_examiner = False          # el sistema nunca actúa como examinador
examiner_scoring_allowed = False   # nunca puntúa respuestas del estudiante
uses_llm = False
uses_api = False
uses_embeddings = False
uses_vector_db = False
cloud_services_active = False
```

Estos flags están en `tools/constants.py` y se verifican en pruebas de regresión, snapshots y en el self-eval dorado.

---

## 2. Arquitectura del sistema

El sistema tiene cinco capas bien delimitadas:

```
Consulta del estudiante
        │
        ▼
┌─────────────────────┐
│     ORCHESTRATOR    │  tools/orchestrator/orchestrator.py
│  router cognitivo   │  → carga LES → misconception prepass → routing
└────────┬────────────┘
         │
    ┌────┴────────────────────────┐
    │                             │
    ▼                             ▼
┌──────────────┐         ┌───────────────────┐
│  Misconception│         │     RETRIEVAL     │
│   Prepass     │         │  tutor_retrieval  │
│  (20 nodos)   │         │  _sandbox.py      │
└──────┬────────┘         └────────┬──────────┘
       │                           │
       │                    ┌──────┴──────────┐
       │                    │  Scoring Engine  │
       │                    │  5 helpers       │
       │                    │  + 21 pesos JSON │
       │                    └──────┬──────────┘
       │                           │
       └──────────┬────────────────┘
                  ▼
        ┌──────────────────┐
        │   TUTOR / ANSWER │  tools/tutor/answer_builder.py
        │   BUILDER        │  → Markdown determinista
        │   (41 patterns)  │
        └──────────────────┘
                  │
                  ▼
        ┌──────────────────┐
        │   SELF-EVAL /    │  tools/self_eval/
        │   HARNESS CI     │  question_runner + comparator + reporter
        └──────────────────┘
```

### 2.1 Fuentes de conocimiento

El sistema integra tres tipos de corpus:

| Corpus | Ubicación | Descripción |
|--------|-----------|-------------|
| **Wine With Jimmy** | `knowledge/wine-with-jimmy/` | Transcripciones de YouTube procesadas con Whisper + limpieza manual. Chunks JSONL enriquecidos con metadatos WSET. |
| **Official WSET extracted** | `knowledge/official-wset/study-guide/official-chunks/` | Chunks extraídos del WSET L3 Study Guide oficial. Fuente de mayor autoridad. |
| **Golden tutor chunks** | `knowledge/wine-with-jimmy/manual-import/reports/` | Chunks manualmente curados por calidad pedagógica superior. |

### 2.2 Base de conocimiento estructurado (Knowledge Map)

```
knowledge/knowledge-map/
├── causal-chains/      32 nodos JSON (causa→mecanismo→efecto→formulación de examen)
├── misconceptions/     21 nodos JSON (errores cognitivos con señales de detección)
├── concepts/           Conceptos WSET con relaciones semánticas
├── relationships/      Relaciones entre conceptos
├── grape-varieties/    Variedades por región
├── regions/            Regiones vitivinícolas
├── tasting/            Terminología SAT
└── topics/             Mapeo de temas del programa
```

El **diccionario maestro** (`knowledge/enrichment/wset_master_dictionary/consolidated/canonical_terms_master.jsonl`) contiene **424 términos canónicos WSET** con aliases bilingües y categoría.

### 2.3 Configuración externalizada (JSON configs)

```
knowledge/config/
├── retrieval_config.json          21 pesos de scoring + PRIORITY_BOOSTS calibrados
├── domain_expansions.json         Expansiones de dominio por query intent
├── explanation_priority_config.json  SEVERITY_WEIGHT + DEPTH_TO_STYLE
└── sat_observation_aliases.json   Aliases para observaciones SAT (balance, intensidad, etc.)
```

---

## 3. Descripción de cada módulo

### 3.1 Orchestrator (`tools/orchestrator/orchestrator.py`, 373 líneas)

Router cognitivo local. Flujo:
1. `ensure_learner_files()` — garantiza que existan los archivos de estado del estudiante
2. `load_learner_state()` — carga el LES (Learner Epistemic State)
3. `load_misconception_nodes()` + `detect_misconception()` — prepass de 21 nodos
4. Si hay misconception detectada → ruta de intervención. Si no → ruta normal.
5. `run_retrieval_sandbox()` — recuperación determinista
6. Construye paquete de contexto (context package) con chunks recuperados + causal chains forzadas
7. `write_session_staging()` — persiste el staging de la sesión

El orchestrator es actualmente un **router**, no un planificador estratégico. No tiene memoria de sesiones anteriores más allá del LES.

### 3.2 Retrieval Engine (`tools/retrieval/tutor_retrieval_sandbox.py`, 1192 líneas)

Motor de recuperación determinista. Pasos principales:

1. **Clasificación de query** en 13 intents (`sat_coaching`, `cause_effect_explanation`, `viticulture`, `vinification`, etc.)
2. **Matching de términos** contra el diccionario de 424 términos canónicos
3. **Expansión de query** vía `domain_expansions.json` + SAT expansions
4. **Scoring** de chunks con 5 helpers nombrados:
   - `_score_lexical_overlap()` — solapamiento de tokens entre query y chunk
   - `_score_term_and_concept_matches()` — matching contra diccionario + knowledge graph
   - `_score_boost_signals()` — boosts: golden chunk, official source, priority, reasoning alignment, SAT
   - `_aggregate_chunk_score()` — suma ponderada de todos los componentes (clamped 0–1)
   - `_build_score_breakdown()` — breakdowns auditables por componente (4 decimales)
5. **Source diversity selection** — garantiza variedad de fuentes en top-K
6. **Governance filter** — excluye chunks con `safe_for_examiner=True`
7. **Causal chain extraction** — detecta y extrae los 32 nodos de causal chains relevantes

### 3.3 Misconception Prepass (`tools/orchestrator/misconception_prepass.py`, 247 líneas)

- Carga 21 nodos de misconceptions desde `knowledge/knowledge-map/misconceptions/`
- Cada nodo tiene: `detection_keywords`, señales de detección ponderadas, directivas de intervención
- Aplica guardas para distinguir preguntas genuinamente exploratorias de errores conceptuales
- Retorna directivas deterministas de intervención (qué enfatizar, qué corregir)
- Las misconceptions son **objetos cognitivos**, no snippets recuperados

### 3.4 Answer Builder (`tools/tutor/answer_builder.py`, 996 líneas)

Renderiza Markdown determinista del Tutor a partir del paquete de contexto. Componentes:

- **5 funciones de dispatch data-driven** que leen `knowledge/answer_patterns.json` (41 entradas bilingües):
  - `_normal_direct_answer()` — respuesta directa basada en patrón de topic
  - `_cause_effect_line()` — línea de causa-efecto del topic
  - `_exam_line()` — formulación de examen WSET-register
  - `_mini_practice()` — prompt de mini-práctica para el estudiante
  - `_official_idea_from_text()` — idea oficial extraída del texto recuperado
- **Renderizado de causal chains** — bloques CAUSA/MECANISMO/EFECTO/FORMULACIÓN DE EXAMEN
- **SAT quality section** — sección especial para preguntas de cata (balance, intensidad, complejidad, longitud)
- **Registros de headings y disclaimers** — anti-duplicación
- **Validación de gobernanza** — verifica flags antes de emitir respuesta

### 3.5 SAT Reasoner (`tools/tutor/sat_reasoner.py`, 260 líneas)

Sistema de razonamiento para el SAT (Systematic Approach to Tasting) de WSET:
- Detecta si una query es sobre cata
- Extrae observaciones SAT (balance, intensidad, complejidad, finish)
- Puntúa hipótesis de calidad (high/medium)
- Formula observaciones en registro WSET
- Usa alias bilingüe desde `sat_observation_aliases.json`

### 3.6 Learner Model

**LES (Learner Epistemic State)** — `knowledge/nazareth/epistemic_state.json`:
- Mastery por topic
- Risk flags de retención
- Misconceptions recurrentes
- Historial de sesiones

**Knowledge Tracing** — `tools/learner_model/knowledge_tracing.py`:
- Mastery score por topic
- Retention risk (curva de olvido simplificada)
- Learning velocity
- Recurring misconception tracking

**LES Reconciler** — `tools/orchestrator/les_reconciler.py`:
- Reconcilia feedback del self-eval en el LES
- Actualiza mastery, risk flags y pedagogical memory

### 3.7 Self-Eval Harness

Pipeline completo de autoevaluación:

| Módulo | Función |
|--------|---------|
| `question_runner.py` | Corre 25 preguntas → orchestrator → retrieval → Tutor |
| `answer_comparator.py` | Labels diagnósticos deterministas (sin LLM) |
| `evaluation_reporter.py` | Escribe summaries, feedback, pedagogical memory |

**Baseline dorado** (`knowledge/self-eval/golden_brutal_output.json`):
```json
{
  "failure_labels": {},
  "retrieval_weaknesses": {"missing_keyword_support": 5},
  "sat_weakness_question_ids": [],
  "retrieval_gap_question_ids": []
}
```
→ 25 preguntas, 0 failure labels, 0 gaps SAT, 5 debilidades de keyword (toleradas como baseline).

---

## 4. Estado actual del sistema

### 4.1 Suite de pruebas

| Categoría | Archivos de test | Tests |
|-----------|-----------------|-------|
| Retrieval engine | `test_tutor_retrieval_sandbox.py`, `test_retrieval_config.py`, `test_score_components.py`, `test_domain_expansions.py`, `test_official_corpus_retrieval.py` | ~80 |
| Tutor / Answer builder | `test_tutor_answer_builder.py`, `test_tutor_snapshot_regression.py`, `test_answer_patterns_schema.py`, `test_answer_builder_sat_integration.py` | ~60 |
| SAT reasoning | `test_sat_reasoner.py`, `test_sat_causal_chains.py`, `test_sat_observation_aliases.py`, `test_retrieval_sat_integration.py`, `test_comparator_sat_strengths.py` | ~50 |
| Orchestrator | `test_minimal_brain_orchestrator.py`, `test_milestone_1_3.py`, `test_adaptive_pedagogical_reasoning.py` | ~30 |
| Learner model | `test_learner_knowledge_tracing.py` | ~15 |
| Self-eval / CI | `test_self_eval_loop.py`, `test_question_runner_expectations.py`, `test_regression_r4a.py`, `test_golden_self_eval.py` (slow) | ~30 |
| Constants / Config | `test_constants.py`, `test_explanation_priority_config.py`, `test_evaluation_reporter_import.py` | ~15 |
| Dictionary pipeline | `test_wset_dictionary_pipeline.py`, `test_wset_dictionary_consolidation.py`, `test_golden_tutor_chunks.py`, `test_manual_srt_import.py` | ~20 |
| **TOTAL** | **29 archivos** | **298 (291 + 7 slow)** |

**Estado:** ✅ 291 tests pasan en el suite regular. 7 tests slow (golden self-eval) pasan con `RUN_SLOW_TESTS=1`. 25 snapshots Tutor congelados y verdes.

### 4.2 Hitos completados

| Batch | Items | Resultado |
|-------|-------|-----------|
| A | Config extraction: sample questions + expectations JSON | 236 → 238 tests |
| B | SAT constants, retrieval config JSON, protocols, tokenizer unificado | 238 tests |
| C | Data-driven dispatch (41 patrones), score helpers descompuestos | 238 → 246 tests |
| D | Regression tests R4A, golden CI baseline, slow golden suite | 246 → 262 tests |
| E | Unit tests score helpers (36 tests, fixture corregida) | 262 → 298 tests |

### 4.3 Lo que el sistema YA puede hacer

- Recibir una consulta en español o inglés sobre WSET L3
- Clasificarla en 13 intents diferentes
- Detectar si hay una misconception cognitiva activa
- Recuperar los chunks más relevantes de tres corpus (Wine With Jimmy, Official WSET, Golden)
- Puntuar chunks usando 21 señales de relevancia calibradas
- Extraer las causal chains de conocimiento relevantes (de 32 disponibles)
- Renderizar una respuesta Tutor en Markdown con: respuesta directa, causa-efecto, formulación de examen WSET, mini-práctica, fuentes
- Razonar sobre preguntas de cata SAT y formular observaciones en registro WSET
- Auto-evaluarse con 25 preguntas sin fallar ninguna
- Persistir el estado epistémico del estudiante Nazareth

### 4.4 Limitaciones conocidas

- **Sin frontend**: no hay interfaz de usuario. El sistema solo corre desde Python.
- **Sin sesión conversacional**: cada query es independiente. No hay memoria intra-sesión (solo el LES entre sesiones).
- **5 debilidades de keyword_support**: algunos topics no tienen suficientes keywords en el diccionario para trigger robusto.
- **Banco de preguntas pequeño**: solo 25 preguntas para self-eval (5 en `sample_questions.json`, resto en la suite de snapshots).
- **Corpus limitado**: los chunks de Wine With Jimmy y WSET official cubren el programa pero no exhaustivamente.
- **Orchestrator es un router, no un planificador**: no tiene estrategia de sesión, no adapta secuencia de temas.

---

## 5. Lo que está explícitamente diferido (deuda técnica documentada)

Estos items están en el audit original pero fueron clasificados como no-bloqueantes para la siguiente fase:

| ID | Descripción | Razón de diferimiento |
|----|-------------|----------------------|
| A-09 | Renombrar umbrales de balance en comparator | Cosmético, funciona bien |
| A-23–A-25 | Externalizar números mágicos en scaffolding_policy | Calibrados y estables |
| A-28 | Externalizar priors de knowledge tracing | Calibrados y estables |
| B-06 | Externalizar signal terms del comparator | Bajo riesgo de coupling |
| B-07 | Refactorizar path resolution en misconception_prepass | Cosmético |
| C-06–C-08 | Longitud de funciones en answer_builder y comparator | Siguen naturalmente de R3 |
| G-01–G-03 | Monitoreo activo de governance flags | Gobernanza limpia, monitoring only |
| P-04 | Cache lru_cache en misconception_prepass | Nice-to-have post-frontend |

---

## 6. Árbol de dependencias del sistema

```
tools/constants.py                     ← base, sin dependencias internas
    ↑
tools/retrieval/tutor_retrieval_sandbox.py
    ↑
tools/tutor/answer_builder.py
    ↑
tools/orchestrator/orchestrator.py    ← leaf, coordina todo
    ↑
tools/self_eval/question_runner.py    ← solo para CI/autoevaluación
```

**Regla de gobernanza de imports:** Los módulos hoja (retrieval, tutor, learner_model) NO deben importar `tools.orchestrator`. El orchestrator importa de todos los demás, no al revés.

---

## 7. Preguntas abiertas que definen las siguientes fases

Las siguientes son las decisiones arquitectónicas pendientes que deben tomarse antes de diseñar el roadmap de las próximas fases:

### 7.1 Frontend
- ¿Qué tipo de interfaz? ¿CLI interactiva? ¿Web app local? ¿App de escritorio?
- ¿El frontend es solo lectura (muestra respuestas) o bidireccional (recibe input del estudiante para actualizar LES)?
- ¿Dónde corre el frontend? ¿Local (Electron/Streamlit)? ¿Vercel (existe config pero no se ha activado)?

### 7.2 Conversación y memoria de sesión
- ¿Debe el sistema mantener contexto entre turnos de la misma sesión?
- ¿Cómo se acumula el historial de una sesión sin romper el determinismo?
- ¿Se agrega un módulo de "session memory" sobre el LES existente?

### 7.3 Estrategia pedagógica
- ¿El orchestrator debe volverse un planificador, no solo un router?
- ¿Debe haber secuenciación de temas (e.g., "no preguntar sobre madurez antes de cubrir taninos")?
- ¿Se integra un spaced repetition system para el LES?

### 7.4 Corpus
- ¿Se expande el banco de preguntas de 25 a cientos de preguntas?
- ¿Se añaden más fuentes de chunks (otros instructores WSET, libros adicionales)?
- ¿Se añaden chunks de mock exams oficiales?

### 7.5 Input del estudiante
- ¿El estudiante puede escribir respuestas libres para que el sistema las evalúe?
- Si sí, ¿cómo se evalúa sin un LLM? ¿Solo keywords + causal chain coverage?
- ¿O se permite un LLM controlado para evaluation only (con governance explícita)?

---

## 8. Resumen ejecutivo para el arquitecto externo

**Lo que tenemos:** Un substrate de ITS/RAG neuro-simbólico determinista y completamente testeado para WSET L3. La capa de recuperación, la capa de razonamiento pedagógico y la capa de respuesta están operativas y tienen 298 tests verdes. El sistema funciona end-to-end para un estudiante específico (Nazareth), auto-evaluándose sin fallos en 25 preguntas.

**Lo que no tenemos:** Interfaz de usuario, conversación multi-turno, estrategia de sesión activa, corpus expandido, evaluación de respuestas del estudiante, y cualquier cosa conectada a internet o a un LLM externo.

**El invariante de diseño más importante:** Todo lo que se construya sobre este sistema debe preservar la auditabilidad y el determinismo. El sistema no puede derivar hacia "el LLM lo dirá" como backstop. Cada respuesta debe ser trazable a una fuente explícita.

**Stack técnico:** Python puro, sin frameworks web todavía. JSON para configuración. JSONL para chunks. unittest para tests. Git para CI. Vercel está en el repo pero sin activar.

---

*Este documento es un artefacto de planificación técnica. No representa evaluación oficial WSET ni autoridad examinadora.*
