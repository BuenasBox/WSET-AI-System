# PEDAGOGICAL_STRATEGY_LAYER.md — Contrato Técnico

**Versión:** 1.0.0  
**Fecha:** 2026-05-30  
**Estado:** Implementación feature-flagged OFF — disconnected de la cadena de renderizado  
**Referencia:** `PSL_DESIGN_AND_TESTS_PLAN.md`, `STRATEGIC_PLANNER_CONTRACT.md`, `PLANNER_INFLUENCE_BOUNDARY.md`, `AGENT_BOUNDARIES.md`

---

## 1. Propósito

La **Pedagogical Strategy Layer (PSL)** es un módulo determinístico de estrategia pedagógica que calcula cómo debe comportarse el Tutor Agent en función del estado del aprendiz, el perfil de rol, y señales de contexto de sesión.

La PSL **modula**:
- **Intensidad del feedback** (`feedback_intensity`: low / medium / high) — cuán exigente es el feedback sobre errores o imprecisiones
- **Tipo de pregunta preferido** (`preferred_question_type`: causal / contextual / evaluative / adversarial / narrative / reflective) — qué clase de mini-práctica o andamiaje se genera
- **Profundidad causal requerida** (`causal_depth_required`: minimal / standard / deep) — si el Tutor debe expandir cadenas CAUSA→MECANISMO→EFECTO
- **Nivel de soporte emocional** (`emotional_support_level`: low / medium / high) — qué presencia tiene la función `host` en el output
- **Nivel de desafío adversarial** (`challenge_level`: low / medium / high) — qué presencia tiene `challenger` para probar supuestos del aprendiz
- **Estilo de remediación** (`remediation_style`: analytical / contextual / scaffolded / narrative / direct / challenge)

La PSL existe porque el sistema necesita que el comportamiento pedagógico del Tutor sea ajustable por perfil de aprendiz y condición de sesión **sin modificar el pipeline de retrieval ni las reglas de governance**. La estrategia pedagógica es ortogonal al contenido recuperado: la PSL cambia cómo se presenta el conocimiento, nunca qué conocimiento se recupera ni si ese conocimiento es correcto.

### Estado de implementación actual

El módulo está implementado y con tests pero **completamente desconectado** del `answer_builder.py` y del `session_ledger.py`. El gate `ENABLE_PEDAGOGICAL_STRATEGY_LAYER = False` en `tools/tutor/pedagogical_strategy/strategy_layer.py` hace que todas las llamadas retornen un directive inerte `{"strategy_active": False, "governance": {...}}` sin ningún efecto sobre el output del Tutor.

---

## 2. No objetivos

La PSL **nunca debe**:

1. **Emitir scoring oficial WSET.** La PSL no asigna puntos, bandas, marcas, ni resultados. No tiene autoridad evaluativa. Esto incluye el modo `exam_pressure` — la presión de examen es pedagógica, no oficial.

2. **Reclamar autoridad de examinador.** Ningún perfil, modo, rol visible ni personaje puede presentarse al aprendiz como un examinador de WSET o como representante de evaluación oficial.

3. **Imitar personas reales.** Los personajes visibles (Clara, Marco, Inés, Rafael, Sofía) son personajes ficticios originales. Ningún `display_name`, `role_label`, o `short_description` puede referenciar el nombre, likeness, o biografía de ninguna persona real.

4. **Hacer roleplay.** El `display_name` de un personaje visible es para la UI únicamente. Nunca debe usarse como instrucción de persona (persona instruction) en el system prompt del Tutor Agent.

5. **Hacer llamadas externas.** La PSL no llama a LLMs, APIs, servicios de embeddings, ni bases de datos vectoriales. Es completamente local y determinística.

6. **Modificar retrieval-first.** La PSL opera aguas abajo del retrieval. No influye en scoring de chunks, ranking de resultados, ni selección de nodos causales. Esto está clasificado como `FORBIDDEN` en `PLANNER_INFLUENCE_BOUNDARY.md §2`.

7. **Cambiar governance rules.** La PSL no puede activar ningún invariante de governance. Los campos `safe_for_examiner`, `examiner_scoring_allowed`, `uses_llm`, `uses_api`, `uses_embeddings`, `uses_vector_db` son siempre `False` en todo output de la PSL.

8. **Activar `examiner_scoring_allowed`.** Este campo nunca puede ser `True` en ningún `StrategyDirective`, perfil, modo, ni personaje.

9. **Activar `safe_for_examiner=True`.** Invariante absoluto del sistema. Ver `tools/constants.py`.

10. **Escribir al LES directamente.** Solo `tools/orchestrator/les_reconciler.py` tiene autoridad para escribir al Learner Epistemic State.

11. **Influir en el Examiner Agent.** La PSL es dominio exclusivo del Tutor. El `StrategyDirective` nunca debe propagarse al `examiner_corpus` ni ser leído por el Examiner Agent.

---

## 3. Restricciones de governance

| Restricción | Constante / Flag | Enforcement en el codebase |
|-------------|-----------------|---------------------------|
| `safe_for_examiner = False` | `tools/constants.py` | Verificado en retrieval filters, Tutor validation, self-eval, SAT reasoner tests, y snapshot tests. El `answer_builder.py` verifica este flag antes de cualquier renderizado. La PSL hardcodea `False` en cada `StrategyDirective`. |
| `examiner_scoring_allowed = False` | `tools/constants.py` | Hardcodeado en `select_pedagogical_strategy()` (`mode_selector.py` línea 129). Validado en `profiles.py` `_validate_governance_block()` línea 141 — un `True` lanza `ProfileValidationError`. También en `pedagogical_profiles.json` y `visible_tutor_characters.json` `_meta.governance`. |
| No imitación de personas reales | `visible_tutor_characters.json` `governance_rules.no_real_person_names = true` | Todos los personajes tienen `governance_notes` explícitas. `profiles.py` valida governance blocks en carga. Test futuro `TEST-G-09` verificará ausencia de names reales. |
| No scoring oficial | Todos los `governance` blocks en `pedagogical_profiles.json` | `_validate_governance_block()` en `profiles.py` rechaza cualquier `True` en governance keys. El `StrategyDirective` no tiene campos `score`, `marks`, `grade`, `band`, ni `examiner_verdict`. |
| Determinístico-first | `ENABLE_PEDAGOGICAL_STRATEGY_LAYER: bool = False` (gate) | `mode_selector.py` usa únicamente aritmética de pesos, comparadores determinísticos, y normalización iterativa. No hay `random`, `time.time()`, ni fuentes no determinísticas. |
| Retrieval-first | Gate off por defecto; PSL opera aguas abajo | La PSL no importa `tutor_retrieval_sandbox.py`. No tiene acceso al pipeline de retrieval. Clasificado FORBIDDEN en `PLANNER_INFLUENCE_BOUNDARY.md`. |
| Audit trail | `traceability` block en `StrategyDirective` | Cuando el gate está activo, `build_pedagogical_strategy()` añade `traceability` con `profile_source`, `rules_fired_count`, `evidence_required=True`, `official_scoring=False`. Futuro: `psl_trace` en `session_ledger.py`. |

---

## 4. Separación de capas

La PSL tiene cuatro capas con contratos estrictos. Ninguna capa puede substituir a otra ni transferirle autoridad que no le pertenece.

### 4.1 Funciones internas

Son los seis vectores de estrategia cognitiva. Son **lógica pura**, sin nombres de persona, sin roleplay, sin API. Su valor es un peso flotante entre 0.0 y 1.0, normalizado a suma 1.0 en el `StrategyDirective`. Los pesos determinan todos los valores derivados del directive.

No son visibles al estudiante. Son completamente testeables en aislamiento (ver `tests/test_pedagogical_mode_selector.py`).

**Ejemplo:** `{"cartographer": 0.25, "scientist": 0.35, "host": 0.15, "storyteller": 0.10, "critic": 0.10, "challenger": 0.05}` es la representación interna del perfil `investigador_causalidad`. El estudiante ve a "Inés", no estos pesos.

### 4.2 Tutor modes

Son configuraciones de comportamiento nombradas: `mentor`, `trainer`, `reviewer`, `distinction`, `exam_pressure`. Cada modo es un vector de pesos base declarado en `knowledge/config/pedagogical_profiles.json` bajo `tutor_modes`. Los pesos base pueden ser modulados por las 8 reglas de ajuste del `mode_selector.py`.

Los modos no son modos de IA ni instrucciones de roleplay. Son vectores de partida que el selector transforma en un `StrategyDirective` final mediante reglas determinísticas.

**Ejemplo:** El modo `exam_pressure` tiene `critic=0.25, challenger=0.25` como pesos base. Si se dispara la regla `exam_imminent`, `challenger` recibe un delta de `+0.15` antes de la normalización — pero `governance.examiner_scoring_allowed` permanece `False` siempre.

### 4.3 Visible tutor roles

Son lo que el estudiante ve: `mentor_fundamentos`, `entrenador_sensorial`, `investigador_causalidad`, `revisor_respuestas`, `entrenador_distinction`. Tienen un `strategy_profile_id` que los conecta a un perfil en `pedagogical_profiles.json`. Son la capa de presentación únicamente.

Los personajes asociados (Clara, Marco, Inés, Rafael, Sofía) viven en `knowledge/config/visible_tutor_characters.json`. Su `display_name` y `role_label` son para la UI. El único campo que fluye hacia la PSL es `strategy_profile_id`. El nombre del personaje **nunca aparece en el system prompt del Tutor como instrucción de comportamiento**.

**Ejemplo:** Clara (`id: "clara_mapas"`) tiene `strategy_profile_id: "mentor_fundamentos"`. La PSL recibe `tutor_role="mentor_fundamentos"`, no el string "Clara". La resolución en `profiles.get_profile()` usa `tutor_role` para cargar los pesos correspondientes.

### 4.4 Future avatars

Fuera del alcance de esta implementación. La interfaz está reservada como stub únicamente:

```python
# tools/tutor/pedagogical_strategy/avatar_stub.py (pendiente de crear)
AVATAR_INTERFACE = {
    # avatar_id → visible_role (maps to strategy_profile_id)
    # Presentation-layer only. Zero cognitive authority.
    # No AI generation. No real-person likenesses. No roleplay personas.
}

def resolve_avatar_to_role(avatar_id: str) -> str | None:
    """Return the visible_role for a given avatar_id, or None if unknown."""
    return AVATAR_INTERFACE.get(avatar_id)
```

El stub debe ser creado antes de cualquier implementación de avatar para bloquear rutas no gobernadas. `resolve_avatar_to_role()` solo puede retornar un string de `ALLOWED_VISIBLE_ROLES` o `None` — nunca texto libre.

---

## 5. Funciones internas

### 5.1 `cartographer`

**Descripción pedagógica:** Orienta al aprendiz en el espacio conceptual. Construye mapas de regiones, variedades, estilos de vino, y relaciones entre conceptos. Especialidad: ayudar a un aprendiz a saber dónde está en el espacio del conocimiento WSET.

**Efecto en feedback:** El feedback señala explícitamente la cobertura geográfica y conceptual de la respuesta. Si el aprendiz confunde una región o un varietal, `cartographer` activo produce feedback de orientación, no de penalización.

**Efecto en tipo de pregunta:** Produce `preferred_question_type = "contextual"` cuando es la función dominante. Las mini-prácticas piden al aprendiz situar un concepto en su contexto regional o tipológico.

**Efecto en profundidad causal:** Contribuye ligeramente a `causal_depth_required` a través del peso de `scientist`. No determina causal depth directamente.

**Restricciones específicas:** No puede afirmar que una respuesta tiene "cobertura completa" en sentido oficial. El feedback de cobertura es pedagógico, no evaluativo.

**Archivo de implementación:** `tools/tutor/pedagogical_strategy/mode_selector.py` (weights y reglas `regional_confusion` delta `+0.20`). Config: `knowledge/config/pedagogical_profiles.json`.

---

### 5.2 `scientist`

**Descripción pedagógica:** Expone mecanismos causales. Construye cadenas CAUSA→MECANISMO→EFECTO. Explica por qué los fenómenos ocurren (fermentación maloláctica, oxidación, extracción de taninos, etc.), no solo que ocurren.

**Efecto en feedback:** El feedback identifica si el aprendiz describió el efecto sin el mecanismo. A mayor peso de `scientist`, mayor demanda de explicación causal en la respuesta.

**Efecto en tipo de pregunta:** Produce `preferred_question_type = "causal"` cuando es dominante. Las mini-prácticas piden explicar el mecanismo detrás de un fenómeno.

**Efecto en profundidad causal:** Es el determinante directo de `causal_depth_required`:
- `scientist >= 0.35` → `"deep"` (cadenas causales completas, FORMULACIÓN DE EXAMEN)
- `scientist >= 0.20` → `"standard"`
- `scientist < 0.20` → `"minimal"`

**Restricciones específicas:** Las cadenas causales deben estar respaldadas por conocimiento recuperado. `scientist` no autoriza al Tutor a inventar mecanismos no presentes en las fuentes.

**Archivo de implementación:** `mode_selector.py` función `_causal_depth_required()` líneas 258–264. Perfiles con scientist dominante: `investigador_causalidad` (0.35), `entrenador_sensorial` (0.30).

---

### 5.3 `host`

**Descripción pedagógica:** Mantiene el vínculo emocional con el aprendiz. Garantiza que el feedback no sea punitivo. Función de engagement, confianza, y seguridad psicológica. Es el piso emocional del sistema.

**Efecto en feedback:** A mayor peso de `host`, el feedback adopta un tono más cálido, más orientado al proceso que al resultado, más orientado a lo que el aprendiz hizo bien antes de señalar lo que falta.

**Efecto en tipo de pregunta:** Produce `preferred_question_type = "reflective"` cuando es dominante. Las mini-prácticas invitan a la reflexión propia antes de la corrección.

**Efecto en profundidad causal:** Reducido en perfiles donde `host` es elevado, ya que corresponden a aprendices en etapas fundacionales.

**Restricciones específicas:** `host` **nunca puede ser eliminado completamente de ningún perfil**. El floor constraint `HOST_MIN_WEIGHT = 0.08` en `mode_selector.py` garantiza que después de cualquier combinación de reglas de ajuste, `host` permanezca al menos en 0.08. El perfil `exam_pressure` tiene `host=0.15` base — incluso bajo `exam_imminent` (delta `-0.05`), el floor impide que baje de 0.08.

**Archivo de implementación:** `mode_selector.py` constante `HOST_MIN_WEIGHT = 0.08` (línea 8), función `_clamp_and_normalise()` (líneas 173–216), función `_emotional_support_level()` (líneas 267–273).

---

### 5.4 `storyteller`

**Descripción pedagógica:** Usa narrativa, analogías, y metáforas para anclar el conocimiento en la memoria del aprendiz. Especialidad: hacer que un concepto abstracto (ej. madurez fenólica) sea recordable mediante una imagen o historia que el aprendiz pueda recuperar en el examen.

**Efecto en feedback:** El feedback incluye analogías o marcos narrativos que conectan el error con un ejemplo memorable. Menor demanda de precisión terminológica, mayor énfasis en comprensión conceptual.

**Efecto en tipo de pregunta:** Produce `preferred_question_type = "narrative"` cuando es dominante. Las mini-prácticas piden al aprendiz reformular un concepto con sus propias palabras o mediante una analogía.

**Efecto en profundidad causal:** `storyteller` elevado generalmente coexiste con `causal_depth_required = "minimal"` o `"standard"` — los perfiles narrativos son para aprendices en etapas tempranas donde la narrativa es más útil que la cadena causal completa.

**Restricciones específicas:** Las analogías y narrativas deben estar **ancladas en conocimiento recuperado**. El Tutor no puede usar `storyteller` como pretexto para inventar explicaciones no respaldadas por las fuentes. `entrenador_sensorial` tiene `storyteller=0.25` con esta restricción explícita en `governance_notes`.

**Archivo de implementación:** `mode_selector.py` función `_preferred_question_type()` (líneas 231–243). Perfiles con storyteller elevado: `mentor_fundamentos` (0.15), `entrenador_sensorial` (0.25).

---

### 5.5 `critic`

**Descripción pedagógica:** Identifica y señala imprecisiones, vaguedades, y afirmaciones sin soporte. Demanda precisión terminológica. Función de calibración — reduce la tolerancia del sistema hacia respuestas correctas-pero-imprecisas.

**Efecto en feedback:** El feedback señala explícitamente qué partes de la respuesta del aprendiz son imprecisas, vagas, o insuficientemente respaldadas. A mayor `critic`, el feedback es más granular y menos tolerante con formulaciones aproximadas.

**Efecto en tipo de pregunta:** Produce `preferred_question_type = "evaluative"` cuando es dominante. Las mini-prácticas piden al aprendiz evaluar o comparar afirmaciones — identificar cuál es más precisa o por qué una es insuficiente.

**Efecto en profundidad causal:** `critic` elevado coexiste frecuentemente con `scientist` elevado (ej. `revisor_respuestas`, `entrenador_distinction`), empujando `causal_depth_required` hacia "standard" o "deep".

**Restricciones específicas:** `critic` no puede emitir juicios de valor ("tu respuesta es mala"). El feedback es descriptivo y orientado a brechas específicas ("falta el mecanismo que explica X", "el término Y no es el registro WSET correcto para esta observación"). No hay scoring implícito ni explicit en el feedback de `critic`.

**Archivo de implementación:** `mode_selector.py` función `_feedback_intensity()` (líneas 223–229) — usa `critic + challenger` combinados para determinar intensidad. Regla `vague_answer` delta `critic +0.15`. Perfil `revisor_respuestas` tiene `critic=0.35`.

---

### 5.6 `challenger`

**Descripción pedagógica:** Prueba supuestos del aprendiz de forma adversarial. Hace preguntas que el aprendiz no anticipó. Expone los límites del conocimiento cuando el aprendiz cree que sabe más de lo que sabe. Especialidad: la transición de "memorizar" a "razonar".

**Efecto en feedback:** El feedback incluye preguntas o afirmaciones que contradicen o complican la respuesta del aprendiz. No para desmotivar, sino para revelar qué parte del conocimiento es frágil bajo presión.

**Efecto en tipo de pregunta:** Produce `preferred_question_type = "adversarial"` cuando es dominante. Las mini-prácticas presentan un caso límite o una objeción que el aprendiz debe refutar o conciliar.

**Efecto en profundidad causal:** `challenger` elevado generalmente empuja hacia mayor profundidad — un desafío adversarial requiere que el aprendiz explique el mecanismo, no solo el efecto.

**Restricciones específicas:** `challenge_level = "high"` en el `StrategyDirective` **nunca activa `examiner_scoring_allowed`**. El modo `exam_pressure` tiene `challenger=0.25` con `examiner_scoring_allowed=False` hardcodeado. El desafío es pedagógico — no es una simulación oficial de examen WSET. El floor constraint `FUNCTION_MIN_WEIGHT = 0.02` impide que `challenger` llegue a cero (aunque en perfiles de baja presión como `mentor_fundamentos`, permanece en 0.05 o cerca del floor).

**Archivo de implementación:** `mode_selector.py` función `_challenge_level()` (líneas 276–282), constante `FUNCTION_MIN_WEIGHT = 0.02` (línea 7). Regla `exam_imminent` delta `challenger +0.15`. Perfil `exam_pressure` tiene `challenger=0.25`.

---

## 6. Reglas del sistema

Las siguientes reglas son invariantes formales. Cualquier implementación, test, o extensión de la PSL debe garantizar que ninguna de estas reglas se viola.

1. **Ninguna función interna puede reclamar autoridad oficial WSET.** El output de `cartographer`, `scientist`, `host`, `storyteller`, `critic`, o `challenger` es pedagogía, no evaluación acreditada.

2. **Ninguna función interna puede emitir scoring oficial.** El `StrategyDirective` no puede contener campos `score`, `marks`, `grade`, `band`, `examiner_verdict`, ni `official_result`. Esto se verificará en `TEST-G-03`.

3. **Ninguna función interna puede imitar personas reales.** Los nombres de los personajes visibles (Clara, Marco, Inés, Rafael, Sofía) son fictios. No pueden aparecer como instrucciones de comportamiento en ningún prompt de agente.

4. **Todo feedback modulado por la PSL debe seguir retrieval-first.** La PSL ajusta cómo se presenta el conocimiento. El conocimiento mismo proviene del pipeline de retrieval. La PSL no puede reemplazar retrieval ni inventar contenido.

5. **Todo comportamiento de la PSL debe ser testeable en aislamiento.** Cada función interna, regla de ajuste, y derivación de señal tiene una interfaz determinística que puede ser testeada sin dependencias del orchestrator, retrieval, ni answer_builder.

6. **`host` nunca puede ser eliminado completamente de ningún perfil.** Floor constraint: `HOST_MIN_WEIGHT = 0.08`. Verificado en `_clamp_and_normalise()` en `mode_selector.py`. Aplica incluso bajo la peor combinación de reglas de ajuste.

7. **`exam_pressure` nunca activa `examiner_scoring_allowed`.** El modo de mayor presión del sistema tiene `examiner_scoring_allowed=False` hardcodeado y validado en carga de perfiles. La presión es pedagógica. Verificado en `TEST-G-10`.

8. **Todos los `StrategyDirective` emitidos cuando el gate está activo deben ser auditables en `session_ledger`.** El campo `psl_trace` debe incluir `profile_id`, `rules_applied`, y señales derivadas — sin texto libre del estudiante, sin queries, sin contenido de respuestas. Ver §2.3.4 de `PSL_DESIGN_AND_TESTS_PLAN.md`.

---

## 7. Riesgos conocidos

### R-PSL-01 — Examiner mode leakage a través de `exam_pressure`
**Severidad:** Alta  
**Descripción:** El modo `exam_pressure` tiene `critic=0.25` y `challenger=0.25`. Si los flags `safe_for_examiner` o `examiner_scoring_allowed` llegaran al `answer_builder` como `True` desde este modo, el Tutor podría actuar como examinador.  
**Mitigación:** `StrategyDirective` hardcodea `safe_for_examiner=False` y `examiner_scoring_allowed=False` en todas las rutas de `select_pedagogical_strategy()`. `profiles._validate_governance_block()` rechaza en carga cualquier perfil con `True` en estos campos. `TEST-G-01` y `TEST-G-10` verifican esto para todos los modos y la combinación adversarial `exam_pressure + exam_imminent + distinction_goal`.

---

### R-PSL-02 — Snapshot drift al activar el gate
**Severidad:** Alta  
**Descripción:** Cuando `ENABLE_PEDAGOGICAL_STRATEGY_LAYER = True`, el `StrategyDirective` puede fluir al `answer_builder`. Cualquier cambio en `causal_depth_required` o `feedback_intensity` puede alterar los 25 snapshots congelados en `tests/fixtures/tutor_snapshots/`.  
**Mitigación:** El gate permanece `False` en producción hasta que los snapshots sean regenerados deliberadamente y revisados. `TEST-G-04` y `TEST-I-06` verifican snapshot invariance con gate off. Nunca activar el gate globalmente sin regeneración explícita y aprobada.

---

### R-PSL-03 — Roleplay por nombre de personaje visible
**Severidad:** Alta  
**Descripción:** Los personajes (Clara, Marco, Inés, Rafael, Sofía) podrían ser inyectados en el system prompt como personas de LLM. Si `display_name` llega al prompt del Tutor como instrucción de comportamiento, se violaría la separación función/persona.  
**Mitigación:** Los personajes son presentation-layer only. `strategy_profile_id` es el único campo de `visible_tutor_characters.json` que fluye a la PSL. `TEST-G-09` verifica que ningún personaje tiene `safe_for_examiner=True` y que los `governance_notes` están presentes.

---

### R-PSL-04 — Inflación de señales desde `_extract_signals()`
**Severidad:** Media  
**Descripción:** Si en el futuro se añaden más señales a `_extract_signals()` (e.g., `exam_days_remaining` desde el LES), puede haber conflicto con señales pasadas vía `extra_context`.  
**Mitigación:** La regla de precedencia `extra_context wins` está implementada en `strategy_layer.py` líneas 97–102. `TEST-U-07` verifica que `extra_context` sobreescribe señales del LES. Cualquier nueva señal en `_extract_signals()` requiere un test explícito de esta precedencia.

---

### R-PSL-05 — Deriva semántica entre `ADJUSTMENT_RULES` y perfiles base
**Severidad:** Media  
**Descripción:** Si se añaden nuevos perfiles con `challenger` base alto, las reglas `exam_imminent` pueden empujar `challenger` por encima de lo intencionado antes del clamping.  
**Mitigación:** El floor constraint protege el piso. Cualquier perfil nuevo debe tener un test que verifique que bajo la peor combinación de reglas, `safe_for_examiner=False` y `host >= HOST_MIN_WEIGHT`.

---

### R-PSL-06 — PSL como fuente de autoridad de scoring indirecta
**Severidad:** Alta  
**Descripción:** `feedback_intensity="high"` podría ser interpretado por el `answer_builder` como autorización para usar lenguaje de scoring ("tu respuesta ganaría X puntos").  
**Mitigación:** `TEST-G-03` verifica que el `StrategyDirective` no tiene campos de scoring. `TEST-I-05` verifica que `feedback_intensity="high"` no produce campos prohibidos en el output del `answer_builder`.

---

### R-PSL-07 — Conexión prematura PSL → retrieval
**Severidad:** Alta  
**Descripción:** La PSL podría ser conectada al pipeline de retrieval antes de que la infraestructura de trazabilidad esté lista, introduciendo decisiones no auditables.  
**Mitigación:** `PLANNER_INFLUENCE_BOUNDARY.md §2` clasifica la influencia PSL→retrieval como `FORBIDDEN`. La PSL no importa `tutor_retrieval_sandbox.py`. Esta restricción es permanente para la PSL (a diferencia del strategic_planner, donde está condicionalmente permitida bajo gates).

---

### R-PSL-08 — Avatar stub sin contrato de activación
**Severidad:** Media  
**Descripción:** Si el stub de avatares se extiende sin especificación de activación, puede crearse una ruta donde `avatar_id` llega al prompt del Tutor.  
**Mitigación:** El stub debe incluir `TEST-U-11` y `TEST-U-12` verificando que `resolve_avatar_to_role()` solo retorna strings de `ALLOWED_VISIBLE_ROLES` o `None` — nunca texto libre, nunca nombres de personas reales.

---

## 8. Tests futuros requeridos

Los tests existentes (`test_pedagogical_strategy_layer.py` ~45 tests, `test_pedagogical_mode_selector.py` ~75 tests, `test_pedagogical_profiles.py`, `test_visible_tutor_characters.py`, `test_adaptive_pedagogical_reasoning.py`) cubren la lógica interna de la PSL. Los **30 tests adicionales** requeridos están especificados en `PSL_DESIGN_AND_TESTS_PLAN.md §4` y se organizan así:

### Tests unitarios (13 tests) — `tests/test_psl_scaffolding_integration.py` y `tests/test_psl_signal_extraction_extended.py` y `tests/test_avatar_stub.py`

`test_psl_scaffolding_integration.py` (6 tests): TEST-U-01 a TEST-U-06. Verifican el mapeo PSL → scaffolding_policy: urgencia, carga cognitiva, governance limpia via PSL, noop cuando gate off, consistencia semántica host-dominante con actos scaffolded, critic-dominante con direct_correction/socratic.

`test_psl_signal_extraction_extended.py` (4 tests): TEST-U-07 a TEST-U-10. Verifican precedencia de `extra_context`, señal de planner como advisory, no-mutación del `context_package`, cold-start sin señales.

`test_avatar_stub.py` (3 tests): TEST-U-11 a TEST-U-13. Verifican que `resolve_avatar_to_role()` retorna solo `ALLOWED_VISIBLE_ROLES | {None}`, que no hay nombres de personas reales en `AVATAR_INTERFACE`, y que cada avatar_id mapea a un `strategy_profile_id` válido en `pedagogical_profiles.json`.

### Tests de integración (6 tests) — `tests/test_psl_answer_builder_integration.py`

TEST-I-01 a TEST-I-06: Verifican inyección del `psl_directive` en el `context_package` cuando el gate está activo, ausencia cuando gate off, backward compatibility del `answer_builder` sin PSL, activación de `causal_depth_required="deep"` desde el perfil `investigador_causalidad`, ausencia de campos de scoring cuando `feedback_intensity="high"`, y snapshot invariance completa (25 fixtures) con gate off.

### Tests de governance y seguridad (10 tests) — `tests/test_psl_governance.py`

TEST-G-01 a TEST-G-10: Cubren governance flags `False` para todos los modos y roles (G-01), governance `False` para todas las combinaciones de reglas (G-02), ausencia de campos de scoring en el directive (G-03), no-modificación de snapshots al activar/desactivar el gate (G-04), ausencia de imports LLM/API/embeddings (G-05), determinismo estricto same-input/same-output (G-06), presencia del bloque `traceability` con `official_scoring=False` (G-07), `psl_trace` en ledger sin datos del estudiante (G-08), personajes visibles sin `safe_for_examiner=True` y con `governance_notes` presentes (G-09), y `exam_pressure + exam_imminent + distinction_goal` sin scoring ni flags activados (G-10).

---

## 9. Estado actual de implementación

### Lo que está construido

| Componente | Archivo | Estado |
|-----------|---------|--------|
| Facade con gate | `tools/tutor/pedagogical_strategy/strategy_layer.py` | ✅ Implementado, gate OFF |
| Selector activo | `tools/tutor/pedagogical_strategy/mode_selector.py` | ✅ Implementado (8 reglas, 6 derivaciones) |
| Selector legacy (archivado) | `tools/tutor/pedagogical_strategy/strategy_selector.py` | ⚠️ Archivado — no importar desde producción |
| Cargador/validador de perfiles | `tools/tutor/pedagogical_strategy/profiles.py` | ✅ Implementado con validación governance |
| Validador de config PSL (colector de errores) | `tools/tutor/pedagogical_strategy/psl_profile_validator.py` | ✅ Implementado, errores estructurados |
| Resolvedor de personajes | `tools/tutor/pedagogical_strategy/character_resolver.py` | ✅ Implementado con `_FORBIDDEN_REAL_NAMES` |
| Avatar stub | `tools/tutor/pedagogical_strategy/avatar_stub.py` | ✅ Stub puro — `is_avatar_implemented()` siempre False |
| Perfiles declarativos | `knowledge/config/pedagogical_profiles.json` | ✅ 5 modos + 5 visible roles + default |
| Personajes visibles | `knowledge/config/visible_tutor_characters.json` | ✅ 5 personajes ficticios, governance-clean |
| Connection C — orquestador | `tools/orchestrator/orchestrator.py` líneas 194–202 | ✅ Gateado OFF |
| Connection D — ledger trace | `tools/orchestrator/session_ledger.py` líneas 156–163 | ✅ Gateado OFF |
| Connection B — scaffolding hints | `tools/tutor/answer_builder.py` líneas 639–646 | ✅ Gateado OFF |
| Connection E — causal depth | `tools/tutor/answer_builder.py` líneas 618–625 | ✅ Gateado OFF |
| Tests internos PSL | `tests/test_pedagogical_strategy_layer.py` | ✅ ~45 tests |
| Tests mode selector | `tests/test_pedagogical_mode_selector.py` | ✅ ~75 tests |
| Tests strategy_selector (archivado) | `tests/test_psl_strategy_selector.py` | ✅ Tests del selector legacy |
| Tests perfiles | `tests/test_pedagogical_profiles.py`, `tests/test_psl_profile_config.py` | ✅ |
| Tests personajes | `tests/test_visible_tutor_characters.py`, `tests/test_psl_visible_tutor_characters.py` | ✅ |
| Tests feedback integration | `tests/test_psl_feedback_integration.py` | ✅ |
| Tests razonamiento adaptativo | `tests/test_adaptive_pedagogical_reasoning.py` | ✅ |

### Estado de conexiones (actualizado 2026-05-31)

Las siguientes conexiones están **implementadas y gatekeadas** — son no-ops cuando `ENABLE_PEDAGOGICAL_STRATEGY_LAYER = False`:

| Conexión | Archivo | Estado |
|---------|---------|--------|
| **Connection C** — PSL → `context_package` | `tools/orchestrator/orchestrator.py` líneas 194–202 | ✅ Implementado, gate OFF |
| **Connection D** — PSL → `session_ledger.py` (`psl_trace`) | `tools/orchestrator/session_ledger.py` líneas 156–163 | ✅ Implementado, gate OFF |
| **Connection B** — PSL → `answer_builder.py` (scaffolding hints: `emotional_support_level`, `challenge_level`) | `tools/tutor/answer_builder.py` líneas 639–646 | ✅ Implementado, gate OFF |
| **Connection E** — PSL → `answer_builder.py` (`causal_depth_required`) | `tools/tutor/answer_builder.py` líneas 618–625 | ✅ Implementado, gate OFF |
| **Avatar stub** | `tools/tutor/pedagogical_strategy/avatar_stub.py` | ✅ Implementado como stub puro |

Las siguientes conexiones **siguen pendientes** (aún no implementadas):

1. **PSL → `answer_builder.py` (`feedback_intensity`)** — `answer_builder.py` no consume `feedback_intensity` directamente. Pendiente en Paso 7 del plan.

2. **PSL → `answer_builder.py` (`preferred_question_type`)** — El tipo de mini-practice prompt no está guiado por la PSL. Pendiente en Paso 7.

3. **PSL → `scaffolding_policy.py` (función `_psl_to_scaffolding_hints()`)** — La función puente no existe; las conexiones B y E en `answer_builder` son directas, no via `scaffolding_policy`. Pendiente en Paso 4.

4. **PSL → `explanation_priority.py`** — `explanation_priority.py` no recibe señales del `StrategyDirective`. Conexión advisory pendiente (Paso 4 o posterior).

### Criterios para activar el gate globalmente

El gate `ENABLE_PEDAGOGICAL_STRATEGY_LAYER = True` **no debe activarse globalmente** hasta que todos los siguientes criterios sean verdaderos:

- `python -m unittest discover -s tests -v` → 660+ passing, zero errors
- Todos los 30 tests del §4 de `PSL_DESIGN_AND_TESTS_PLAN.md` verdes
- Brutal self-eval → zero failure labels
- Snapshots regenerados deliberadamente y revisados (no actualizados silenciosamente)
- `psl_trace` visible en ledger para al menos 10 sesiones reales de prueba
- Ningún snapshot cambió inesperadamente al conectar el `answer_builder`

---

*Este documento es un contrato técnico de arquitectura. No representa implementación activa, evaluación oficial de WSET, ni autoridad de examinador.*  
*Generado: 2026-05-30 | Requiere revisión humana antes de actuar sobre las recomendaciones.*
