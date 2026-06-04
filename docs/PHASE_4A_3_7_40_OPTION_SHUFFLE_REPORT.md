# Phase 4A.3.7.40 Option Shuffle Report

## Estrategia elegida

Se implemento shuffle visual determinista derivado de `item_id`.

Estrategia: `stable_item_id_sha256_v1`.

Razon:
- Mantiene reproducibilidad para QA y regresion.
- No depende de estado de navegador, reloj, sesion ni backend.
- No modifica el banco canonico.
- Evita calcular correctness por posicion visual.

Cada item conserva sus `option_id` canonicos (`A`, `B`, `C`, `D`) y el outcome conserva `correct_option_id` y `option_diagnostics` por `option_id`. El render pre-submit agrega `visual_option_id` (`A`, `B`, `C`, `D`) y permuta que `option_id` canonico aparece bajo cada letra visual.

## Archivos modificados

- `tools/question_generation/static_demo_exporter.py`
  - Agrega shuffle visual determinista.
  - Agrega `visual_option_id` en opciones renderizadas.
  - Mantiene `option_id`, `correct_option_id` y `option_diagnostics` canonicos.
  - Endurece validacion de payload para exigir:
    - `visual_option_id` en orden visual `A-D`.
    - `option_id` canonicos `A-D` exactamente una vez.
    - ausencia de campos diagnosticos/correctness en render pre-submit.

- `frontend/diagnostic-sba/index.html`
  - Muestra `visual_option_id`.
  - Guarda y selecciona internamente por `option_id`.
  - Mapea teclado `A-D` desde letra visual hacia `option_id`.
  - Evalua correctness por `option_id`, no por posicion visual.
  - Muestra letras visuales en el resultado post-submit.

- `frontend/diagnostic-sba/preguntas.json`
  - Regenerado desde el exportador.
  - Conserva las mismas 36 preguntas y textos de opciones.
  - Agrega `visual_option_id` y permuta solo el orden visual.

- `tests/test_static_demo_option_shuffle.py`
  - Nueva cobertura especifica de shuffle.

- `tests/test_diagnostic_sba_cockpit_json_loader.py`
  - Actualiza contrato del loader para `visual_option_id`.

- `tests/test_diagnostic_sba_loader_failure_recovery_qa.py`
  - Actualiza escenario de opciones faltantes para verificar letras visuales.

## Pruebas agregadas

`tests/test_static_demo_option_shuffle.py` cubre:
- Estrategia documentada en metadata.
- `visual_option_id -> option_id` preservado.
- `option_id -> diagnostic` preservado.
- `option_id -> correctness` preservado.
- Correctness no derivada de posicion visual.
- Ausencia de leakage pre-submit (`correct_option_id`, `is_correct`, `diagnostic_role`, `diagnostic_note`).
- Determinismo ante drafts/reviews en distinto orden.
- No mutacion de drafts/reviews.

## Riesgos

- El payload render pre-submit cambia de esquema al agregar `visual_option_id`; se mitigo actualizando validador Python, loader HTML y tests de loader.
- Una permutacion determinista no cambia entre sesiones para un mismo item. Esto es intencional para estabilidad de QA; el sesgo de posicion fija del banco queda eliminado en el laboratorio activo.
- Si consumidores externos asumian `option_id` en orden visual `A-D`, deben usar `visual_option_id` para UI y `option_id` para diagnostico/correctness.

## Brechas pendientes

- No se implemento shuffle aleatorio por sesion. Queda descartado para esta fase porque haria QA menos reproducible.
- No se agrego persistencia de respuesta por `visual_option_id`; el sistema conserva la seleccion interna por `option_id`, que es el identificador trazable correcto.

## Validacion final

Comandos ejecutados:

```bash
python -m tools.question_generation.export_static_demo_questions --dry-run
python -m unittest tests.test_static_demo_option_shuffle tests.test_static_demo_exporter tests.test_static_demo_export_file tests.test_static_demo_export_dry_run tests.test_diagnostic_sba_cockpit_json_loader tests.test_diagnostic_sba_loader_failure_recovery_qa -v
python -m unittest discover -s tests -v
```

Resultado:
- Dry-run: `eligible_item_count: 36`, `validation_errors: 0`.
- Tests dirigidos: 89 tests OK.
- Suite completa: 1360 tests OK, 9 skipped.
