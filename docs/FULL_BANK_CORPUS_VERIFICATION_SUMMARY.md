# Full Bank Corpus Verification Summary

Phase 4A.3.7.31 — full structured SBA bank corpus verification

Method: deterministic, local, exact case-insensitive string search over `knowledge/**/*.md`; no embeddings, vector database, external API, LLM, item edits, or promotion actions. Corpus files were processed one file at a time.

## Totals

- Total structurally-valid SBA items processed: **524**
- Source bank records inspected: **616**
- Valid four-option record excluded to match SBA target: **Q18**
- Markdown corpus files with decoding issues skipped: **0**

## Grounding Distribution

| Grounding | Count | Recommended action |
|---|---:|---|
| STRONG | 57 | eligible for promotion pipeline |
| PARTIAL | 256 | requires human review before promotion |
| WEAK | 10 | downgrade to Tier-3 |
| NOT_FOUND | 201 | quarantine, do not promote |

## Items With DISTRACTOR_CONFLICT

Total: **181**

| Item | RA | Grounding | Correct answer |
|---|---|---|---|
| Q1 | UNKNOWN | STRONG | Protege al vino del oxígeno y desarrolla sabores únicos |
| Q2 | UNKNOWN | STRONG | Adición de aguardiente vínico |
| Q3 | UNKNOWN | STRONG | Estructura potente y necesidad de guarda |
| Q5 | UNKNOWN | STRONG | Envejecimiento exclusivamente oxidativo |
| Q9 | RA4 | PARTIAL | Sercial |
| Q10 | RA4 | PARTIAL | Madeira |
| Q11 | RA1 | STRONG | Clima fresco continental |
| Q12 | UNKNOWN | STRONG | Pendiente del terreno |
| Q13 | UNKNOWN | STRONG | Estructura arenosa |
| Q14 | UNKNOWN | STRONG | Puede aumentar la oxidación |
| Q16 | UNKNOWN | STRONG | Remontado |
| Q17 | UNKNOWN | STRONG | Evitar la extracción de taninos verdes |
| Q21 | RA3 | STRONG | Chenin Blanc |
| Q25 | RA3 | PARTIAL | Iniciar segunda fermentación |
| Q29 | RA3 | NOT_FOUND | Se embotella con levadura natural sin degüelle |
| Q38 | RA1 | PARTIAL | Prevenir oxidación |
| Q40 | RA1 | NOT_FOUND | Exposición sur en el hemisferio norte |
| Q41 | RA1 | PARTIAL | Vino tinto añejo |
| Q83 | RA1 | STRONG | Alta acidez, taninos firmes y buen equilibrio |
| Q94 | RA4 | PARTIAL | Palomino |
| Q95 | RA4 | PARTIAL | Madeira |
| Q97 | RA4 | PARTIAL | Oloroso |
| Q99 | RA4 | NOT_FOUND | Crianza prolongada en botella después de corta crianza en barrica |
| Q100 | RA4 | PARTIAL | Madeira |
| Q105 | RA4 | STRONG | Palo Cortado |
| Q111 | RA3 | STRONG | Brut Nature |
| Q113 | RA3 | PARTIAL | Acidez suficiente |
| Q114 | RA3 | NOT_FOUND | Lombardía |
| Q126 | RA3 | NOT_FOUND | Sudáfrica |
| Q203 | RA3 | STRONG | Pinot Meunier |
| Q204 | RA3 | NOT_FOUND | Ancestral |
| Q206 | RA4 | STRONG | Touriga Nacional |
| Q207 | RA4 | PARTIAL | Notas de frutos secos y color oscuro |
| Q210 | RA4 | PARTIAL | Larga crianza oxidativa en toneles |
| Q211 | RA4 | PARTIAL | Pedro Ximénez |
| Q216 | RA3 | STRONG | Chenin Blanc |
| Q223 | RA3 | PARTIAL | Prosecco |
| Q226 | RA3 | PARTIAL | Robertson |
| Q227 | RA3 | NOT_FOUND | Más carácter tánico y fruta madura |
| Q230 | RA1 | STRONG | Alta acidez, taninos marcados y estructura firme |
| Q232 | RA2 | STRONG | Pinot Noir |
| Q236 | RA2 | NOT_FOUND | Grecia |
| Q237 | RA3 | PARTIAL | Tradicional |
| Q238 | RA3 | NOT_FOUND | Trepat |
| Q239 | RA3 | NOT_FOUND | Lombardía |
| Q243 | RA2 | PARTIAL | Valle del Uco |
| Q244 | RA2 | WEAK | Campo de Borja |
| Q245 | RA2 | PARTIAL | Malbec |
| Q247 | RA2 | STRONG | Pendientes empinadas y clima fresco |
| Q248 | RA2 | PARTIAL | Riesling |
| Q252 | RA2 | PARTIAL | Grenache (Garnacha) |
| Q254 | RA2 | STRONG | Sonoma Coast |
| Q257 | RA2 | NOT_FOUND | Semillón |
| Q258 | RA2 | STRONG | Uco Valley |
| Q263 | RA2 | PARTIAL | Carignan (Mazuelo) |
| Q264 | RA2 | PARTIAL | Carneros |
| Q268 | RA2 | PARTIAL | Florales, taninos firmes, alta acidez |
| Q270 | RA2 | STRONG | Cabernet Franc |
| Q272 | RA2 | NOT_FOUND | Variedad Tannat y estructura potente |
| Q273 | RA2 | WEAK | Tocai Friulano |
| Q277 | RA2 | STRONG | Pinot Noir |
| Q278 | RA2 | PARTIAL | Pomerol |
| Q279 | RA2 | NOT_FOUND | Valdeorras |
| Q286 | RA2 | PARTIAL | Hermitage |
| Q287 | RA2 | STRONG | Taninos altos, acidez alta y notas terciarias con la edad |
| Q288 | RA2 | NOT_FOUND | Influencia marina y nieblas |
| Q291 | RA2 | PARTIAL | Valpolicella |
| Q294 | RA2 | PARTIAL | Malbec |
| Q296 | RA2 | PARTIAL | Casablanca |
| Q298 | RA2 | PARTIAL | Viognier |
| Q301 | RA2 | STRONG | Cabernet Sauvignon |
| Q303 | RA2 | STRONG | Sonoma Coast |
| Q306 | RA2 | PARTIAL | Sangiovese |
| Q308 | RA2 | STRONG | Sauvignon Blanc |
| Q309 | RA2 | STRONG | Botrytis cinerea |
| Q312 | RA2 | PARTIAL | Nerello Mascalese |
| Q325 | RA2 | STRONG | Sauvignon Blanc |
| Q330 | RA1 | PARTIAL | Contaminación por TCA |
| Q338 | RA2 | PARTIAL | Corvina |
| Q343 | RA2 | PARTIAL | Aromas florales, taninos firmes y alta intensidad |
| Q344 | RA2 | PARTIAL | Valpolicella |
| Q350 | RA2 | PARTIAL | Sauternes |
| Q353 | RA2 | STRONG | Mineralidad, acidez marcada y taninos firmes |
| Q354 | RA2 | PARTIAL | Corriente de Humboldt |
| Q356 | RA2 | STRONG | Santa Rita Hills |
| Q361 | RA2 | STRONG | Mount Veeder |
| Q363 | RA2 | PARTIAL | Tannat |
| Q370 | RA2 | NOT_FOUND | Grampians |
| Q371 | RA2 | NOT_FOUND | Gewürztraminer |
| Q373 | RA1 | NOT_FOUND | Maceración prolongada y delestage |
| Q376 | RA2 | NOT_FOUND | Suelos de pizarra y viñedos en ladera |
| Q378 | RA2 | NOT_FOUND | Uruguay |
| Q379 | RA2 | PARTIAL | Bourgogne |
| Q381 | RA2 | PARTIAL | Bourgogne |
| Q382 | RA2 | NOT_FOUND | Uruguay |
| Q387 | RA2 | PARTIAL | Toscana |
| Q394 | RA2 | PARTIAL | Pendiente y exposición solar |
| Q395 | RA2 | STRONG | Alta acidez, aromas a grosella negra, taninos marcados |
| Q397 | RA2 | PARTIAL | Chablis |
| Q398 | RA2 | PARTIAL | Sangiovese |

Only first 100 shown; see JSON for all 181 conflict flags.

## Top 20 NOT_FOUND Items

| Item | RA | Topic | Correct answer | Key terms |
|---|---|---|---|---|
| Q7 | RA4 | RA4 / Bloque 8 | Desarrolla aromas a nuez, caramelo y umami | Desarrolla aromas a nuez, caramelo y umami, Desarrolla aromas nuez, aromas nuez caramelo, nuez caramelo umami |
| Q26 | RA3 | RA3 / Bloque 10 | Mover sedimentos al cuello de la botella | Mover sedimentos cuello, sedimentos cuello botella, Mover sedimentos, sedimentos cuello, cuello botella |
| Q29 | RA3 | RA3 / Bloque 9 | Se embotella con levadura natural sin degüelle | embotella levadura natural, levadura natural degüelle, embotella levadura, levadura natural, natural degüelle |
| Q30 | RA3 | RA3 / Bloque 9 | Notas de autólisis como pan y brioche | Notas autólisis como, autólisis como pan, como pan brioche, Notas autólisis, autólisis como |
| Q33 | RA1 | RA1 | Aumenta el rendimiento sin diluir calidad | Aumenta rendimiento diluir, rendimiento diluir calidad, Aumenta rendimiento, rendimiento diluir, diluir calidad |
| Q40 | RA1 | RA1 | Exposición sur en el hemisferio norte | Exposición sur hemisferio, sur hemisferio norte, Exposición sur, sur hemisferio, hemisferio norte |
| Q43 | RA1 | RA1 | Puede hacer que el vino se perciba más amargo o ácido | Puede hacer perciba, hacer perciba amargo, perciba amargo ácido, Puede hacer, hacer perciba |
| Q46 | RA1 | RA1 | Enfriador de botellas con hielo y agua | Enfriador botellas hielo, botellas hielo agua, Enfriador botellas, botellas hielo, hielo agua |
| Q47 | RA1 | RA1 | Maridarlo con alimentos grasos o proteicos | Maridarlo alimentos grasos, alimentos grasos proteicos, Maridarlo alimentos, alimentos grasos, grasos proteicos |
| Q48 | RA1 | RA1 | Aroma a cartón mojado y sabor apagado | Aroma cartón mojado, cartón mojado sabor, mojado sabor apagado, Aroma cartón, cartón mojado |
| Q49 | RA1 | RA1 | 10–13 °C | 10–13 °C |
| Q50 | RA1 | RA1 | Temperatura estable, oscuridad y humedad moderada | Temperatura estable, oscuridad y humedad moderada, Temperatura estable oscuridad, estable oscuridad humedad, oscuridad humedad moderada |
| Q51 | RA1 | RA1 | Limpiar las copas con detergentes perfumados | Limpiar copas detergentes, copas detergentes perfumados, Limpiar copas, copas detergentes, detergentes perfumados |
| Q53 | RA5 | RA5 | Minimizar la evaporación y evolución prematura | Minimizar evaporación evolución, evaporación evolución prematura, Minimizar evaporación, evaporación evolución, evolución prematura |
| Q56 | RA1 | RA1 | Lo intensifica | Lo intensifica, intensifica |
| Q58 | RA1 | RA1 | Bomba de vacío | Bomba de vacío, Bomba vacío, Bomba, vacío |
| Q60 | RA1 | RA1 | Problemas hepáticos y dependencia | Problemas hepáticos y dependencia, Problemas hepáticos dependencia, Problemas hepáticos, hepáticos dependencia, Problemas |
| Q61 | RA1 | RA1 | Incluir sugerencias de maridaje, precios y estilos explicados claramente | Incluir sugerencias de maridaje, Incluir sugerencias maridaje, sugerencias maridaje precios, maridaje precios estilos, precios estilos explicados |
| Q62 | RA1 | RA1 | Hace que el vino se perciba más amargo, ácido y menos frutal | ácido y menos frutal, perciba amargo ácido, amargo ácido menos, ácido menos frutal, perciba amargo |
| Q63 | RA1 | RA1 | Enfriado y decantado si es necesario | Enfriado decantado necesario, Enfriado decantado, decantado necesario, Enfriado, decantado |

## Coverage Gaps By RA

| RA | Total items | NOT_FOUND | NOT_FOUND % |
|---|---:|---:|---:|
| RA1 | 176 | 88 | 50.0% |
| RA2 | 209 | 59 | 28.2% |
| RA3 | 64 | 23 | 35.9% |
| RA4 | 27 | 7 | 25.9% |
| RA5 | 38 | 24 | 63.2% |
| UNKNOWN | 10 | 0 | 0.0% |

## Recommended Action By Grounding

- **STRONG:** eligible for promotion pipeline, subject to normal human review and governance checks.
- **PARTIAL:** requires human review before promotion; claim may be inferential or only partly stated in corpus.
- **WEAK:** downgrade to Tier-3; keep out of active diagnostic use until rewritten or better grounded.
- **NOT_FOUND:** quarantine; do not promote unless corpus support is added or the item is removed.

## Notes

- The score is a deterministic lexical-support audit, not examiner authority and not official WSET scoring.
- `DISTRACTOR_CONFLICT` means at least one wrong option has strong exact-string corpus support under the same local search heuristic; it is a review flag, not a final ambiguity ruling.
- `core_claim` is generated from the correct answer text plus stem context because the audit is prohibited from using LLM rewriting.
