# Phase 4A.3.7.53B — Slow Golden Metadata Fix Verification

Fecha: 2026-06-05  
Repositorio canónico verificado: `C:\Dev\WSET-AI-System-push`  
Commit base: `3ab09a2560ca09155e6a9c940cca4a216747f7ba`

## Resultado

La causa principal fue una divergencia entre carpetas de trabajo:

- El fix de metadata estaba aplicado en `C:\Users\esand\OneDrive\Documents\WSET-AI-System`.
- El slow golden rojo se ejecutó y volvió a verificarse en `C:\Dev\WSET-AI-System-push`.
- En `C:\Dev`, Q6–Q11, Q15 y Q19–Q25 todavía conservaban respuestas completas dentro de `expected_keywords`.

El cambio sí tenía efecto. Después de portarlo al repositorio canónico:

- `missing_keyword_support`: 17 → 5.
- `shallow_reasoning`: 12 → 0.
- Fallos slow golden: 4 → 3.

Los tres fallos restantes provenían de un único falso negativo del comparator para Q19. La respuesta contenía una cadena causal explícita basada en `competencia → menor vigor → menor rendimiento → concentración`, pero el vocabulario determinístico de `_has_cause_mechanism_effect()` no reconocía esos términos vitícolas.

Tras la corrección mínima del comparator:

- Suite regular: **1432 OK, 9 skipped**.
- Slow golden: **7/7 OK**.
- Golden baseline: **sin cambios y vigente**.

## Fuente real del slow golden

`tests/test_golden_self_eval.py` llama:

```python
run_self_eval(limit=25)
```

La cadena de carga es:

```text
tests/test_golden_self_eval.py
  -> tools/self_eval/question_runner.py::run_self_eval()
  -> load_questions(limit=25)
  -> _load_structured_questions(knowledge/question-bank/structured/)
  -> _normalize_question()
```

Orden de precedencia real:

1. `knowledge/question-bank/structured/*.json`
2. `knowledge/question-bank/raw/*.xlsx`, sólo si no hay preguntas estructuradas
3. `knowledge/self-eval/sample_questions.json`, sólo si las dos fuentes anteriores están vacías

Por tanto:

- El slow golden **sí lee** `knowledge/question-bank/structured/wset3_questions.json`.
- No usa `sample_questions.json` en el estado actual.
- `question_expectations.json` sólo participa como fallback por campo dentro de `_normalize_question()`.
- Los archivos en `knowledge/self-eval/attempts/` son outputs, no inputs del test.
- `golden_brutal_output.json` aporta únicamente las métricas baseline esperadas.

## Confirmación del fix de metadata

Se confirmó `expected_keywords: []` para:

```text
Q6, Q7, Q8, Q9, Q10, Q11,
Q15,
Q19, Q20, Q21, Q22, Q23, Q24, Q25
```

El cambio estaba inicialmente sólo en OneDrive. Se aplicó el mismo diff a la fuente canónica en `C:\Dev`.

## Comportamiento de `_infer_expectations()`

`_normalize_question()` usa:

```python
_as_list(question.get("expected_keywords")) or inferred["expected_keywords"]
```

Esto significa que una lista vacía permite inferencia. Sin embargo, para las 14 preguntas corregidas ningún patrón actual de `question_expectations.json` coincide con el texto español completo. Sus keywords efectivos permanecen vacíos.

La inferencia no fue la causa de que las métricas siguieran en 17. La causa fue ejecutar el test contra otra copia del repositorio.

## Las 25 preguntas efectivas

Fuente runtime para las 25: `knowledge/question-bank/structured/wset3_questions.json`.

La columna “provenance” conserva el `source_type` del registro original; no indica que el XLSX sea leído durante el slow golden.

| ID | Question text | Expected keywords efectivos | Expected topics efectivos | Expected causal links efectivos | Provenance |
|---|---|---|---|---|---|
| 1 | ¿Qué rol juega la 'flor' en la crianza biológica del Jerez? | flor; crianza biológica; oxígeno; acetaldehído | flor; jerez; biological ageing | flor → oxygen protection → biological ageing | structured_question_bank |
| 2 | ¿Qué método se usa para detener la fermentación en el vino de Oporto? | aguardiente; fortificación; fermentación; azúcar residual | port; fortification; fermentation | fortification → yeast stops → residual sugar | structured_question_bank |
| 3 | ¿Cuál es una característica clave de los vinos de Porto Vintage? | Vintage Port; botella; tanino; sedimento | vintage port; bottle ageing | structure → bottle ageing → sediment | structured_question_bank |
| 4 | ¿Cuál es el sistema tradicional de envejecimiento utilizado en Jerez? | solera; criaderas; mezcla; consistencia | jerez; solera | fractional blending → consistency | structured_question_bank |
| 5 | ¿Qué diferencia al Oloroso del Amontillado en términos de crianza? | flor; oxidativa; biológica; fortificación | oloroso; amontillado; sherry ageing | flor dies → oxidative ageing; no flor → oxidative ageing | structured_question_bank |
| 6 | ¿Cuál es una característica clave del vino de Jerez Fino? | — | RA4 / Bloque 9 | — | WSET3_RA4...xlsx / Sheet1 |
| 7 | ¿Qué influencia tiene el envejecimiento oxidativo en los vinos generosos? | — | RA4 / Bloque 8 | — | WSET3_RA4...xlsx / Sheet1 |
| 8 | ¿Qué práctica específica distingue al Tokaji Aszú? | — | RA2 / Bloque 8 | — | WSET3_RA4...xlsx / Sheet1 |
| 9 | ¿Qué variedad se asocia comúnmente con los vinos de Madeira? | — | RA4 / Bloque 8 | — | WSET3_RA4...xlsx / Sheet1 |
| 10 | ¿Cuál de los siguientes es un vino generoso portugués reconocido? | — | RA4 / Bloque 8 | — | WSET3_RA4...xlsx / Sheet1 |
| 11 | ¿Cuál de los siguientes climas se asocia comúnmente con una alta acidez en los vinos blancos? | — | RA1 | — | WSET3_RA1...xlsx / Sheet1 |
| 12 | ¿Qué factor natural tiene mayor influencia en el riesgo de heladas primaverales? | topografía; aire frío; heladas primaverales; drenaje del aire frío | heladas primaverales; topografía; viticultura | aire frío → puntos bajos → riesgo de heladas primaverales | structured_question_bank |
| 13 | ¿Qué elemento del suelo influye más directamente en el drenaje del viñedo? | textura del suelo; drenaje; raíces; concentración | textura del suelo; drenaje; vigor de la vid | textura del suelo → retención de agua → vigor de la vid | structured_question_bank |
| 14 | ¿Cuál es el principal efecto de la vendimia mecánica sobre el estilo del vino? | vendimia mecánica; rotura de la baya; oxígeno; frescura aromática | vendimia mecánica; oxidación; frescura aromática | vendimia mecánica → rotura de la baya → frescura aromática | structured_question_bank |
| 15 | ¿Cuál de los siguientes factores humanos tiene un impacto directo en el precio de producción del vino? | — | RA1 | — | WSET3_RA1...xlsx / Sheet1 |
| 16 | ¿Qué práctica enológica se utiliza para aumentar la extracción de color y taninos en tintos? | extracción; color; taninos; estructura | extracción; taninos | — | structured_question_bank |
| 17 | ¿Cuál es el propósito principal del despalillado antes de la fermentación? | despalillado; raspones; taninos verdes; astringencia | despalillado; fermentación; estructura tánica | raspones → taninos verdes → estructura | structured_question_bank |
| 18 | ¿Cuál es una consecuencia del uso excesivo de sulfitos? | sulfitos; SO₂; aromas reductivos; dióxido de azufre | sulfitos; SO₂; carácter del vino | — | structured_question_bank |
| 19 | ¿Qué efecto tiene una densidad de plantación alta? | — | RA1 | — | WSET3_RA1...xlsx / Sheet1 |
| 20 | ¿Qué variable de vinificación afecta más directamente el cuerpo del vino? | — | RA1 | — | WSET3_RA1...xlsx / Sheet1 |
| 21 | ¿Cuál es una variedad comúnmente utilizada en el espumoso Crémant de Loire? | — | RA3 / Bloque 10 | — | WSET3_RA3...xlsx / Sheet1 |
| 22 | ¿Qué región chilena es reconocida por espumosos de calidad debido a su clima fresco? | — | RA3 / Bloque 10 | — | WSET3_RA3...xlsx / Sheet1 |
| 23 | ¿Cuál es el efecto de una presión menor a 3 atmósferas en un espumoso? | — | RA3 / Bloque 10 | — | WSET3_RA3...xlsx / Sheet1 |
| 24 | ¿Cuál es una diferencia técnica entre Cava y Champagne? | — | RA3 / Bloque 10 | — | WSET3_RA3...xlsx / Sheet1 |
| 25 | ¿Cuál es el propósito del licor de tiraje? | — | RA3 / Bloque 10 | — | WSET3_RA3...xlsx / Sheet1 |

## Por qué `missing_keyword_support` seguía en 17

Antes de portar el fix, la ejecución en `C:\Dev` veía:

- 14 preguntas con respuestas completas de opción múltiple como expected keywords.
- 5 debilidades legítimas/preexistentes en Q1, Q2, Q4, Q5 y Q16.
- No todas las 14 contaminadas producían necesariamente un weakness adicional, pero el agregado final era 17.

La copia OneDrive ya corregida mostraba en sus resultados:

- Q6–Q11, Q15 y Q19–Q25 con keywords efectivos vacíos.
- `missing_keyword_support` únicamente en Q1, Q2, Q4, Q5 y Q16.
- Total: 5, exactamente el baseline.

Esto demuestra que no había cache de preguntas ni uso oculto de `sample_questions.json`. Se estaban comparando ejecuciones hechas desde árboles distintos.

## Causa residual Q19

Después del fix de metadata quedó:

```text
missing_causal_link: 1
missing_causal_link_support: 1
cause -> mechanism -> effect: 1
```

Pregunta:

```text
Q19 — ¿Qué efecto tiene una densidad de plantación alta?
```

La respuesta producida incluía:

```text
alta densidad
→ competencia por agua y nutrientes
→ menor vigor
→ menor rendimiento
→ mayor concentración
```

También contenía conectores como `porque`, `por tanto`, `conduce` y `→`.

El comparator exigía estructura causal para preguntas `theory`, pero su lista cerrada de términos de mecanismo/efecto no incluía:

- `competencia`
- `vigor`
- `concentración`

Era un falso negativo determinístico y reproducible. No fue necesario modificar Tutor, Retrieval, inferencia ni baseline.

## Cambios aplicados

### Metadata

`knowledge/question-bank/structured/wset3_questions.json`

- Se limpiaron las 14 listas contaminadas de `expected_keywords`.

### Comparator

`tools/self_eval/answer_comparator.py`

- Se añadieron `competencia` y `vigor` como términos de mecanismo.
- Se añadió `concentración` como término de efecto.
- No se cambió ningún threshold.
- No se eliminó ninguna assertion.
- No se cambió el requisito causal para preguntas theory.

### Regresión

`tests/test_self_eval_loop.py`

- Se añadió `test_viticulture_competition_chain_is_recognized`.
- La prueba confirma que una cadena causal vitícola completa no recibe `missing_causal_link` ni `shallow_reasoning`.

## Métricas antes y después

| Métrica | Antes | Metadata en carpeta correcta | Resultado final |
|---|---:|---:|---:|
| Regular tests | 1431 OK | 1431 OK | 1432 OK |
| Regular skipped | 9 | 9 | 9 |
| Slow golden pass/fail | 3/4 | 4/3 | 7/0 |
| missing_keyword_support | 17 | 5 | 5 |
| shallow_reasoning | 12 | 0 | 0 |
| missing_causal_link | 1 | 1 | 0 |
| missing_causal_link_support | 1 | 1 | 0 |
| cause → mechanism → effect | 1 | 1 | 0 |

El incremento 1431 → 1432 corresponde exclusivamente a la nueva prueba de regresión.

## Pruebas ejecutadas

```text
python -m unittest tests.test_self_eval_loop -v
16 tests — OK
```

```text
python -m unittest discover -s tests -v
1432 tests — OK
9 skipped
```

```text
$env:RUN_SLOW_TESTS='1'
python -m unittest tests.test_golden_self_eval -v
7 tests — OK
```

Los outputs runtime generados por self-eval fueron restaurados después de la verificación. No forman parte del cambio.

## Baseline

`knowledge/self-eval/golden_brutal_output.json` no fue modificado.

El baseline sigue vigente:

```text
failure_labels: {}
retrieval_weaknesses:
  missing_keyword_support: 5
causal_chains_missing: {}
sat_weakness_question_ids: []
retrieval_gap_question_ids: []
```

## Conclusión

El fix anterior no cambió la ejecución reportada porque fue aplicado en OneDrive mientras el test rojo se ejecutaba en `C:\Dev`. Una vez aplicado en el repositorio canónico, eliminó exactamente la contaminación esperada.

El único residual era un falso negativo claramente aislado del comparator frente a vocabulario causal vitícola. La corrección fue mínima, está cubierta por una prueba nueva y no modifica Tutor, Retrieval, SBA runtime, Open Response, assertions ni golden baseline.

Estado final: **slow golden verde y baseline vigente**.
