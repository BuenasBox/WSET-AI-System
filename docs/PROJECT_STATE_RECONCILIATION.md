# Project State Reconciliation — Repository Truth

Fecha de conciliación: 2026-06-05  
Repositorio auditado: `C:\Dev\WSET-AI-System-push`  
Principio de esta auditoría: el estado se deriva del Git actual, el código, los datos, las pruebas y los despliegues verificables. Los planes y documentos históricos no se toman como evidencia de implementación.

## Resumen ejecutivo

El repositorio canónico está en `main`, sincronizado con `origin/main`, en el commit `90524ff247e696e0b3b4b16c63f232fc670a6f74`.

El sistema tiene hoy dos superficies de producto muy diferentes:

- **Diagnostic SBA:** 36 preguntas activas en un laboratorio estático publicado y accesible.
- **Open Response:** pipeline, revisión, motor de sesión, runtime y frontend están mergeados, pero la activación sigue en `inactive`, hay 0 preguntas activas y no existe despliegue público.

La suite regular está verde: **1431 pruebas ejecutadas, 9 omitidas, 0 fallos**. Sin embargo, el slow golden actual está rojo: **7 pruebas, 3 pasan y 4 fallan**. Por tanto, el repositorio compila y supera su regresión ordinaria, pero no cumple hoy su propio baseline profundo de calidad Tutor/Retrieval.

La siguiente fase recomendada no es ampliar funcionalidades: es corregir la regresión del slow golden y recuperar una línea base confiable.

## 1. Estado Git

### Rama principal y commit actual

- Rama principal local: `main`.
- Tracking: `main...origin/main`, sin adelanto ni retraso.
- Commit actual: `90524ff247e696e0b3b4b16c63f232fc670a6f74`.
- Fecha del commit: 2026-06-05 17:42:35 -06:00.
- Mensaje: `Merge pull request #2 from BuenasBox/codex/phase-4a3-7-open-response-lab`.
- El árbol de trabajo estaba limpio antes de crear este informe.

### Ramas remotas relevantes

Mergeadas en `main`:

- `origin/codex/phase-4a3-7-32-gold-bank`
- `origin/codex/phase-4a3-7-35-canonical-baseline`
- `origin/codex/phase-4a3-7-open-response-lab`, integrada mediante PR #2 y ya no presente como rama remota separada

No mergeadas según la topología Git:

- `origin/codex/phase-4a3-7-33-remediation-artifacts`
- `origin/gh-pages`

`origin/gh-pages` es un artefacto histórico de publicación, no una rama de
desarrollo pendiente de fusionar ni la fuente activa de producción. La fuente
activa es `BuenasBox/epistemiclab-dashboard`, rama `main`.

La rama `phase-4a3-7-33-remediation-artifacts` contiene dos commits que Git no considera mergeados. Sus tres documentos de remediación ya existen en `main`, aparentemente incorporados por otra línea de commits. Queda una diferencia real de tres líneas en `tests/test_structured_question_bank_adapter.py`, donde cambia la expectativa de validación de `question_type`. Debe resolverse explícitamente antes de eliminar la rama.

### Fases mergeadas

El código actual contiene e integra:

- Núcleo de governance y constantes fail-safe.
- Retrieval determinístico, clasificación, expansión de dominio y causal chains.
- Tutor determinístico, SAT reasoner, misconception pre-pass y snapshots.
- Strategic planner, persistencia de plan, session ledger y resumen CLI.
- Planner query hints y causal-chain injection experimentales.
- Pipeline SBA: adapter, enriquecimiento, revisión humana, exporter estático y option shuffle.
- Gold Bank y export activo de 36 SBA.
- Pipeline Open Response, paquete de revisión, remediaciones, session engine, runtime y frontend privado/inactivo.

### Fases no mergeadas

- La rama técnica `phase-4a3-7-33-remediation-artifacts` no está formalmente mergeada, aunque la mayor parte de sus documentos está ya presente.
- No existe implementación mergeada de un master bank canónico único.
- No existe session composer SBA general.
- No existe pipeline general de generación gobernada de preguntas.

## 2. Diagnostic SBA

### Banco estructurado

- Banco total: **616** registros en `knowledge/question-bank/structured/wset3_questions.json`.
- Composición: **595 theory** y **21 short_answer**.
- Auditados contra corpus: **524** registros en `docs/FULL_BANK_CORPUS_VERIFICATION.json`.
- Dataset post-remediación: **524** registros en `docs/CORPUS_REMEDIATION_DATASET.json`.

### Gold Bank y activación

El término “Gold Bank” se usa para dos cantidades diferentes:

- **41** registros `STRONG` en la clasificación post-remediación del corpus.
- **34** drafts/reviews en los archivos de activación Gold.

La activación Gold añadió 34 elementos a 2 elementos previamente aprobados. El resultado operativo exportado es:

- Aprobadas para demo estática: **36**.
- Activas en el frontend: **36**.
- `requires_revision`: **2**.
- `preserve_only`: **16**.

En total existen 54 drafts y 54 review records SBA distribuidos entre los paquetes inicial y Gold.

### Exporter

Estado: **funcional**.

La ejecución actual:

```text
python -m tools.question_generation.export_static_demo_questions --dry-run
```

produce:

- `eligible_item_count`: 36
- `validation_errors`: 0
- `export_version`: `static_demo_export_v0`
- target: `frontend/diagnostic-sba/preguntas.json`

El archivo publicado contiene 36 items y conserva los flags de training/static demo sin autoridad oficial.

### Option shuffle

Estado: **activo**.

- Estrategia: `stable_item_id_sha256_v1`.
- El orden es determinístico por `item_id`.
- Se emite `visual_option_id`.
- No cambia la opción correcta ni introduce aleatoriedad no reproducible.

### Deployment

Estado: **publicado y accesible**.

- URL verificada el 2026-06-05: `https://epistemiclab.dpdns.org/diagnostic-sba/`
- Respuesta HTTP: 200.
- `origin/gh-pages` contiene `diagnostic-sba/index.html` y `diagnostic-sba/preguntas.json`.
- Alcance declarado: laboratorio privado/de entrenamiento, aunque técnicamente la URL es públicamente accesible.
- No es examen oficial ni habilita scoring de examinador.

## 3. Open Response

### Inventario y revisión

- Detectadas/normalizadas: **21**.
- Aprobadas por revisión: **20**.
- Rechazadas: **1**.
- Activas: **0**.
- Todos los registros mantienen `activation_status: inactive`.

### Pipeline

Estado: **mergeado y funcional como pipeline determinístico inactivo**.

`tools/question_generation/open_response_pipeline.py` normaliza los registros, aplica governance y produce candidatos. No usa LLM, API, embeddings ni vector DB.

### Session engine

Estado: **mergeado y probado**, pero no equivale a activación.

- Pool configurado: **18** source IDs.
- IDs excluidos explícitamente: `807` y `809`.
- Tamaños de sesión: short 3, standard 5, long 10.
- El pool interno puede componer sesiones aunque todos los candidatos sigan con activación global `inactive`.

### Runtime

Estado: **MVP mergeado, estático e inactivo**.

- Archivo: `tools/question_generation/open_response_lab_runtime.py`.
- `LAB_ACTIVATION_STATUS = "inactive"`.
- Genera un payload estático validado.
- No llama servicios externos.
- El payload frontend actual expone sesiones de hasta 10 items, no la totalidad de los 20 aprobados.

### Frontend

Estado: **existe en `main`, no publicado**.

- Existen `frontend/open-response-lab/index.html` y `lab_payload.js`.
- El payload declara `activation_status: inactive`.
- `origin/gh-pages` no contiene `open-response-lab/`.
- URL verificada: `https://epistemiclab.dpdns.org/open-response-lab/` responde HTTP 404.

## 4. Tutor

### Estado actual

El Tutor determinístico está implementado en `tools/tutor/answer_builder.py` e integrado con:

- Retrieval local.
- Misconception pre-pass.
- SAT reasoner.
- Causal-chain rendering.
- Scaffolding y explanation priority.
- Governance validation.

La regresión de snapshots está verde:

- **35 pruebas** en `tests.test_tutor_snapshot_regression`.
- **25 fixtures de respuesta** congelados.
- Resultado actual: OK.

### Blockers

El blocker principal es el slow golden:

- `shallow_reasoning`: 12 casos.
- `missing_causal_link`: 1 caso.
- `missing_keyword_support`: 17, frente a 5 en el baseline.
- Nueva debilidad: `missing_causal_link_support`.
- Nueva cadena faltante: `cause -> mechanism -> effect`.

### Slow golden

Ejecución actual:

```text
$env:RUN_SLOW_TESTS=1
python -m unittest tests.test_golden_self_eval -v
```

Resultado:

- 7 pruebas ejecutadas.
- 3 pasan.
- 4 fallan.

Pasan governance flags, ausencia de retrieval gaps y ausencia de SAT weaknesses. Fallan los contratos de failure labels, keyword support, causal-chain support y retrieval weaknesses.

### Riesgos

- Los snapshots verdes no detectan la regresión semántica capturada por el slow golden.
- `answer_builder.py` es behavior-dense y cualquier cambio requiere snapshots y golden.
- El self-eval escribe artefactos versionados durante pruebas; esto contamina el worktree si no se restaura.
- No debe afirmarse que Tutor está completamente verde mientras el slow golden falle.

## 5. Retrieval

### Estado actual

Retrieval es determinístico y local. Incluye:

- Clasificación de query.
- Expansión de dominio.
- Scoring léxico y conceptual.
- Selección con diversidad de fuentes.
- Filtros de governance.
- Detección y extracción de causal chains.
- Compatibilidad con observaciones SAT.

El código está mergeado y la suite regular pasa, pero las métricas del slow golden muestran deterioro real en soporte de keywords y enlaces causales.

### Planner integration

El strategic planner está integrado en el orchestrator como señal observable:

- Genera `strategic_plan`.
- Se persiste en staging.
- Alimenta el session ledger.
- No controla hoy el ranking normal de retrieval.

Existen parsers y adaptadores para hints `causal_chain:<id>`, pero su influencia permanece experimental.

### Gates activos

Los siguientes gates están **desactivados**:

- `ENABLE_PLANNER_QUERY_EXPANSION = False`
- `ENABLE_PLANNER_CAUSAL_CHAIN_INJECTION = False`
- `ENABLE_PEDAGOGICAL_STRATEGY_LAYER = False`

Por tanto, el planner está integrado para observación y telemetría, pero no modifica activamente la consulta, el ranking o la estrategia pedagógica del runtime normal.

## 6. Governance

### Invariantes actuales

En `tools/constants.py`:

```text
SAFE_FOR_EXAMINER = False
EXAMINER_SCORING_ALLOWED = False
USES_LLM = False
USES_API = False
USES_EMBEDDINGS = False
USES_VECTOR_DB = False
CLOUD_SERVICES_ACTIVE = False
```

### Enforcement

Los invariantes se propagan y validan en:

- Orchestrator y learner state.
- Retrieval.
- Tutor y SAT reasoner.
- Self-eval.
- SBA adapter, validator y exporter.
- Open Response pipeline, session engine y runtime.
- Snapshots, pruebas unitarias y golden.

No se encontró una ruta activa que habilite autoridad de examinador, scoring oficial, LLM, API, embeddings o vector DB.

### Riesgos

- El Diagnostic SBA se describe como “private training lab”, pero su URL es públicamente accesible. La privacidad es semántica/de alcance, no control de acceso.
- El dashboard contiene estado desactualizado de pruebas y commit.
- Hay artefactos históricos de learner state y self-eval versionados aunque las reglas actuales indican que deben ser machine-local.
- La suite golden deja archivos runtime modificados en el árbol de trabajo.
- Los corpus locales ignorados por Git pueden hacer que un clon limpio no reproduzca todos los resultados sin un proceso separado de provisión de datos.

## 7. Tests

### Suite regular

Comando:

```text
python -m unittest discover -s tests -v
```

Resultado real actual:

- **1431 pruebas ejecutadas**
- **9 skipped**
- **0 fallos**
- Estado: **OK**

### Suites focalizadas

- Tutor snapshot regression: 35/35 OK.
- Static exporter dry-run: 36 elegibles, 0 errores.
- Slow golden: 3/7 OK, 4/7 fallan.

### Blockers

- El slow golden impide declarar el sistema completamente verde.
- La suite genera cambios en archivos versionados de self-eval y learner feedback.
- `frontend/architecture-dashboard/system_state.json` reporta 1363 pruebas y commit `f0b5d84`; ambos están obsoletos frente al estado actual.

## 8. Despliegues

### Publicado

Fuente de producción: `BuenasBox/epistemiclab-dashboard`, rama `main`.
Dominio operativo: `https://epistemiclab.dpdns.org/`.

No usar `WSET-AI-System/origin/gh-pages` para determinar el estado publicado,
salvo que exista una decisión posterior que lo reactive explícitamente.

- Cockpit/dashboard raíz: `https://epistemiclab.dpdns.org/` — HTTP 200.
- Diagnostic SBA: `https://epistemiclab.dpdns.org/diagnostic-sba/` — HTTP 200.
- Payload SBA de 36 preguntas.
- `robots.txt`, `CNAME` y `system_state.json`.

### No publicado

- Open Response Lab: HTTP 404 y ausente de `gh-pages`.
- Tutor interactivo.
- Orchestrator.
- Retrieval runtime.
- Ledger y learner-state tools.
- Master bank canónico.
- Cualquier backend o API.

### Sigue privado/local

- Estado epistémico del learner.
- Session staging y pedagogical memory.
- Self-eval attempts y reports dinámicos.
- Outputs de retrieval sandbox.
- Corpus fuente ignorado por Git.
- Runtime Open Response, aunque su frontend está versionado en `main`.

## 9. Roadmap real

### COMPLETADO

- Governance fail-safe y constantes centrales.
- Retrieval determinístico base.
- Tutor determinístico, SAT, misconceptions y causal chains.
- Orchestrator y strategic planner observable.
- Session ledger y reporting.
- Banco estructurado de 616 registros.
- Auditoría/remediación de 524 registros.
- Pipeline SBA de adapter, drafts, revisión y export.
- Gold activation y frontend SBA de 36 items.
- Option shuffle determinístico.
- Publicación del cockpit y Diagnostic SBA.
- Pipeline, revisión, session engine, runtime y frontend inactivo de Open Response.

### EN PROGRESO

- Calidad Tutor/Retrieval: suite regular verde, slow golden rojo.
- Open Response: implementación mergeada, activación 0 y sin despliegue.
- Consolidación del SBA master bank.
- Evidencia para activar influencia del planner.
- Limpieza de ramas y artefactos de pruebas.
- Reconciliación entre dashboard, Git y conteos reales.

### NO INICIADO

- Archivo canónico `knowledge/question-bank/master_bank.json`.
- Session composer SBA general.
- Pipeline general de governed question generation.
- Despliegue de Open Response.
- Autenticación/control de acceso para laboratorios llamados privados.
- Backend público, API, cloud runtime o Tutor público, todos además fuera del alcance de governance actual.

## 10. Próximas 10 fases

Estas fases se derivan de fallos, archivos ausentes y trabajo mergeado pero inactivo:

1. **Recuperar el slow golden.** Investigar y corregir los 12 `shallow_reasoning`, el causal link faltante y el salto de keyword support de 5 a 17.
2. **Aislar efectos secundarios de las pruebas.** Ejecutar self-eval/golden contra directorios temporales para no modificar artefactos versionados.
3. **Resolver la rama de remediación pendiente.** Decidir la expectativa correcta de `question_type`, integrar sólo el delta válido y retirar ramas obsoletas.
4. **Actualizar la verdad operacional del dashboard.** Sincronizar commit, 1431 tests, 9 skipped, fase Open Response mergeada y estado golden rojo.
5. **Crear el contrato y artefacto canónico del SBA Master Bank.** Hoy el archivo no existe y los datos están repartidos entre banco, auditoría, drafts, reviews y export.
6. **Migrar el Gold Bank al master bank.** Consolidar los 41 STRONG, los 36 activos y su lineage sin perder approval scope ni governance.
7. **Convertir auditoría/remediación en pipeline repetible.** Los datasets existen; falta una ejecución canónica reproducible y verificable.
8. **Implementar el SBA session composer.** Composición determinística por RA, dificultad y cobertura usando exclusivamente items aprobados.
9. **Cerrar readiness de Open Response.** Resolver los IDs 807/809, verificar cobertura y feedback rubric, y definir criterios explícitos de activación.
10. **Desplegar Open Response de forma privada y gobernada.** Sólo después de golden verde, activación deliberada, pruebas de frontend y un mecanismo real de acceso privado.

## Contradicciones encontradas

1. El dashboard declara **1363 tests**, pero la suite real ejecuta **1431**.
2. El dashboard declara `latest_commit: f0b5d84`, pero `main` está en `90524ff`.
3. El dashboard no refleja que Open Response ya fue mergeado el 2026-06-05.
4. La memoria histórica afirma que todas las pruebas están verdes, pero el slow golden actual falla 4 de 7.
5. El término “Gold Bank” se usa como 41 registros STRONG, 34 activaciones Gold y 36 items activos; son métricas distintas.
6. Open Response tiene 20 aprobadas y un pool de sesión de 18, pero 0 activas.
7. Open Response tiene frontend en `main`, pero no está en la rama de despliegue.
8. Diagnostic SBA se denomina privado, pero está disponible en una URL pública sin control de acceso.
9. Las políticas dicen que self-eval/learner artifacts son locales, pero existen artefactos históricos rastreados por Git y las pruebas los modifican.
10. Una rama de remediación aparece no mergeada aunque sus documentos ya están en `main`; queda al menos un delta de prueba no resuelto.

## Estado real

El proyecto es hoy un sistema determinístico local con una superficie SBA estática publicada y una superficie Open Response mergeada pero desactivada. La arquitectura central existe, está ampliamente cubierta por pruebas y mantiene sus invariantes de governance.

No está completamente estable: el golden profundo revela una regresión de calidad que la suite regular y los snapshots no detectan. Tampoco existe todavía el master bank canónico ni un pipeline general de generación/composición SBA. Open Response no está activo ni desplegado.

## Siguiente fase recomendada

**Phase: Slow Golden Recovery and Test Isolation.**

Prioridad inmediata:

1. Reproducir y localizar el origen de los 4 fallos golden.
2. Recuperar el baseline sin relajar expectativas ni governance.
3. Evitar que las pruebas escriban en artefactos versionados.
4. Volver a ejecutar las 1431 pruebas, los 35 snapshot tests y los 7 slow golden tests.

No se recomienda activar Open Response, habilitar gates del planner ni ampliar el banco publicado antes de completar esta fase.
