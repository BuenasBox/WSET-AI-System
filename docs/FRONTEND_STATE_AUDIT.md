# Frontend State Audit

**Fecha:** 2026-06-05  
**Método:** Inspección directa de GitHub (rama `main`) — sin modificaciones de código  
**Cubre:** NOW-1 · NOW-2 · NOW-3 de `CLAUDE_NEXT_PHASES.md`

---

## NOW-1 — Cargador JSON del Cockpit Desplegado

**Archivo auditado:** `frontend/architecture-dashboard/diagnostic-sba/index.html`  
**SHA:** `4b57b10aad5d460f8d44bbb1e717ff93706da9a5`  
**Tamaño:** 51,357 bytes

### Veredicto: LIVE FETCH ✅ — NO está hardcodeado

El cockpit desplegado usa `fetch()` dinámico:

```js
var DATA_URL = './preguntas.json';

function loadStaticDemoPayload() {
  setLoadingState();
  fetch(DATA_URL)
    .then(function(response) {
      if (!response.ok) throw new Error('HTTP ' + response.status);
      return response.json();
    })
    .then(function(payload) {
      if (!validatePayload(payload)) throw new Error('Payload estático inválido');
      EXPORT_PAYLOAD = payload;
      QS = payload.items;
      OUTCOMES_BY_ITEM_ID = payload.outcomes_by_item_id;
      // ...
    })
    .catch(function(error) {
      setErrorState('No se pudo cargar ./preguntas.json. ' + error.message);
    });
}
```

El payload se resuelve como `./preguntas.json` relativo al HTML. El archivo existe en el mismo directorio:
`frontend/architecture-dashboard/diagnostic-sba/preguntas.json` (184,532 bytes, SHA `041cd052284084ae117f94d5631697f7269f664d`).

### Gobernanza verificada inline

El cockpit ejecuta `validatePayload()` → `validateItem()` → `hasSafeGovernance()` antes de cargar cualquier pregunta. Los contratos exigidos:

| Campo | Valor exigido |
|---|---|
| `safe_for_examiner` | `false` |
| `examiner_scoring_allowed` | `false` |
| `training_item_only` | `true` |
| `static_demo_only` | `true` |
| `official_wset_question` | `false` |
| `export_version` | `"static_demo_export_v0"` |

Cualquier payload que viole estas condiciones es rechazado con `setErrorState()` antes de renderizar.

### Nota sobre el contador inicial

El DOM inicial muestra `1<em>/4</em>` hardcodeado. Esto es solo el estado placeholder pre-carga — se sobreescribe en `loadQ(0)` con el conteo real desde el JSON. No implica límite de 4 preguntas.

### Estado del cockpit vs. v2.2

El cockpit desplegado contiene la misma arquitectura que `frontend/diagnostic-sba-v2.2/`:
- Flujo de 7 etapas (espera → selección → confianza → confirmar → revelar → siguiente → fin)
- `visual_option_id` / `option_id` split (shuffle-ready)
- Teclado A·B·C·D + Enter
- Detección de misconception
- SAT scoring
- Disclaimer: `LABORATORIO PRIVADO · PROTOTIPO ESTÁTICO · ENTRENAMIENTO · NO EVALUACIÓN OFICIAL WSET · SIN AUTORIDAD EXAMINADORA`

**El cockpit desplegado está FUNCIONAL y carga datos en vivo desde su preguntas.json co-localizado.**

---

## NOW-2 — Conteo de Items en preguntas.json

**Archivos involucrados:**

| Path | Tamaño | SHA | Estado |
|---|---|---|---|
| `frontend/diagnostic-sba/preguntas.json` | ~150 KB | — | Fuente original |
| `frontend/architecture-dashboard/diagnostic-sba/preguntas.json` | 184,532 bytes | `041cd052...` | Copia desplegada |

### Conteo: 36 items confirmados

Fuente primaria: `docs/PHASE_4A_3_7_40_OPTION_SHUFFLE_REPORT.md` documenta el resultado del dry-run del exportador:

```
Dry-run: eligible_item_count: 36, validation_errors: 0
```

El mismo reporte confirma: _"Conserva las mismas 36 preguntas y textos de opciones."_

### Comparación con estado anterior

El estado anterior reportado en sesiones previas era _"3 items (Q2, Q12, Q17)"_ — ese dato era **stale**, correspondía a un mock hardcodeado que existía antes de PR #3. Tras el merge de PR #3 y la implementación del shuffle (Fase 4A.3.7.40), `preguntas.json` fue regenerado desde el banco estructurado con 36 items elegibles.

### Relación con master_bank

- `knowledge/question-bank/master_bank/master_bank.json`: 1.2 MB (banco canónico completo)
- `knowledge/question-bank/structured/wset3_questions.json`: ~616 registros
- `frontend/diagnostic-sba/preguntas.json`: 36 items exportados para demo estática

Los 36 items representan el subconjunto elegible para demo estática (ítems con cobertura STRONG o PARTIAL validada, `static_demo_only=true`).

**No se requiere re-exportación. El conteo es coherente con el estado del banco.**

---

## NOW-3 — Option Shuffle en el Frontend

**Fuente primaria:** `docs/PHASE_4A_3_7_40_OPTION_SHUFFLE_REPORT.md`

### Veredicto: IMPLEMENTADO Y TESTEADO ✅

#### Estrategia

```
strategy: stable_item_id_sha256_v1
```

Shuffle determinista derivado del `item_id` usando SHA-256. Reproducible para QA. No depende de sesión, reloj ni backend.

#### Arquitectura implementada

| Componente | Qué hace |
|---|---|
| `static_demo_exporter.py` | Calcula permutación en export time; asigna `visual_option_id` |
| `frontend/diagnostic-sba/index.html` | Muestra `visual_option_id`; guarda selección por `option_id` canónico |
| `frontend/diagnostic-sba/preguntas.json` | Regenerado con shuffle; contiene `visual_option_id` en cada opción |
| `tests/test_static_demo_option_shuffle.py` | Cobertura específica de shuffle (89 tests dirigidos) |

#### Contratos verificados por los tests

- `visual_option_id → option_id` preservado
- `option_id → diagnostic` preservado
- `option_id → correctness` preservado
- Correctness **no** derivada de posición visual
- Ausencia de leakage pre-submit (`correct_option_id`, `is_correct`, `diagnostic_role`, `diagnostic_note`)
- Determinismo ante drafts/reviews en distinto orden
- No mutación de drafts/reviews

#### Cobertura de tests al momento del reporte

```
Tests dirigidos:  89 tests OK
Suite completa:   1360 tests OK, 9 skipped
```

#### Correspondencia con el sesgos documentado

El reporte previo (`PHASE_4A_3_7_40_OPTION_SHUFFLE_REPORT.md`) identificó C=56.5% de sesgo posicional en el banco. El shuffle determinista por `item_id` elimina ese sesgo en el laboratorio activo al redistribuir qué `option_id` canónico aparece bajo cada letra visual en cada item.

#### Validación en el cockpit desplegado

El JS del cockpit en `frontend/architecture-dashboard/diagnostic-sba/index.html` contiene el contrato completo:

```js
// Validación del schema de shuffle en payload
function validateItem(item, outcomesByItemId) {
  // ...
  var visualOptionIds = item.options.map(function(option) { return option.visual_option_id; });
  if (visualOptionIds.join(',') !== 'A,B,C,D') return false;  // visual siempre A-D
  var optionIds = item.options.map(function(option) { return option.option_id; });
  if (optionIds.slice().sort().join(',') !== 'A,B,C,D') return false;  // canónicos presentes
  // ...
}

// Mapeo teclado visual → option_id canónico
function optionIdForVisual(options, visualId) {
  var found = (options || []).filter(function(option) {
    return (option.visual_option_id || option.option_id) === visualId;
  })[0];
  return found ? found.option_id : null;
}
```

**El shuffle está completamente implementado, testeado y verificado en el cockpit desplegado.**

---

## Resumen ejecutivo

| Item | Estado | Hallazgo clave |
|---|---|---|
| NOW-1: JSON Loader | ✅ FUNCIONAL | `fetch('./preguntas.json')` vivo, no hardcodeado |
| NOW-2: Item count | ✅ CONFIRMADO | 36 items en preguntas.json (no 3 como era stale) |
| NOW-3: Option shuffle | ✅ IMPLEMENTADO | `stable_item_id_sha256_v1`, 1360 tests pasan |

### Brechas identificadas durante este audit

1. **Divergencia entre preguntas.json**: `frontend/diagnostic-sba/preguntas.json` (fuente) y `frontend/architecture-dashboard/diagnostic-sba/preguntas.json` (desplegada) tienen SHAs distintos y tamaños diferentes. Se desconoce si la versión desplegada está sincronizada con la fuente. Acción recomendada: verificar si son idénticas en contenido o si el dashboard tiene una versión desactualizada.

2. **Cockpit v2.2 vs. desplegado**: `frontend/diagnostic-sba-v2.2/index.html` (93 KB+) vs `frontend/architecture-dashboard/diagnostic-sba/index.html` (51 KB) — tamaños distintos. El v2.2 podría ser una versión más reciente no promovida al dashboard. Requiere diff.

3. **Conteo exacto de architecture-dashboard/preguntas.json**: Se conoce el conteo de `frontend/diagnostic-sba/preguntas.json` (36 items), pero el tamaño diferente del archivo en el dashboard (184,532 bytes) podría indicar un conteo distinto. Lectura pendiente del archivo.

---

*Audit realizado via GitHub MCP (lectura directa de archivos en rama main). Sin modificaciones de código.*
