# ENRICHMENT BATCH 1 — Reporte de muestra para aprobación

Lote: **8 ítems** · derivación determinista desde nodos causales CC_/HC_ (umbral: ≥2 trigger keywords, mejor nodo único, capa ES con guard).
Con micro_drill: **8** · fingerprint de entrada: `599dd36d10b7d8d6`

Política v2 (precisión primero): word-boundary, triggers genéricos prohibidos, el nodo debe
explicar la respuesta correcta (hit en stem Y en opción correcta), stems de identificación excluidos.

Rechazos por regla: `{"below_threshold": 141, "identification_stem": 112, "no_correct_option_hit": 11, "no_stem_hit": 4, "no_spanish_layer": 3}`

---

## wset3_4 (sq 4) · RA4 · gold=False

**Pregunta:** ¿Cuál es el sistema tradicional de envejecimiento utilizado en Jerez?
**Correcta (C):** Sistema de soleras y criaderas
**Nodo:** `CC_FRACTIONAL_BLENDING_CONSISTENCY` · score 6 · en stem: envejecimiento, jerez, sistema tradicional · en respuesta correcta: criaderas

- **Causa:** Se establece un sistema de solera: una serie de botas (criaderas) ordenadas por edad, cada una con vino en distinta etapa de maduración.
- **Mecanismo:** Al extraer vino de las botas más viejas (la solera) para embotellar, estas se rellenan parcialmente con vino más joven de la siguiente criadera, y la cascada continúa por todos los niveles.
- **Efecto:** Cada saca contiene una mezcla de añadas; la incorporación constante de vino viejo y joven mantiene una edad media y un estilo estables año tras año.

**Mentor Guía:** La respuesta correcta es C: «Sistema de soleras y criaderas». La clave está en el sistema de solera y criaderas: Al extraer vino de las botas más viejas (la solera) para embotellar, estas se rellenan parcialmente con vino más joven de la siguiente criadera, y la cascada continúa por todos los niveles. Por eso, cada saca contiene una mezcla de añadas; la incorporación constante de vino viejo y joven mantiene una edad media y un estilo estables año tras año.

**Entrenador Técnico:** Concepto técnico (RA4): Tema: fortified wines. Fija el mecanismo del sistema de solera y criaderas: Se establece un sistema de solera: una serie de botas (criaderas) ordenadas por edad, cada una con vino en distinta etapa de maduración. → Al extraer vino de las botas más viejas (la solera) para embotellar, estas se rellenan parcialmente con vino más joven de la siguiente criadera, y la cascada continúa por todos los niveles. En el examen, identifica este patrón causa→mecanismo→efecto antes de mirar las opciones.

**Revisor Estricto:** Exigencia de repaso (RA4): debes poder justificar por qué «Sistema de soleras y criaderas» es correcta y por qué las otras tres opciones no lo son, citando el mecanismo del sistema de solera y criaderas. Si no puedes reconstruir la cadena completa sin ver las opciones, repasa este concepto en tu material WSET L3.

**Micro-drill:** Consolidación: ¿cuál de estas afirmaciones corresponde al sistema de solera y criaderas?
  - A. Adición de aguardiente vínico
  - B. Evitar la extracción de taninos verdes
  - C. Sistema de soleras y criaderas ✅
  - D. Crianza prolongada en botella después de corta crianza en barrica
  - _Explicación:_ «Sistema de soleras y criaderas» corresponde al sistema de solera y criaderas. Las demás afirmaciones son correctas, pero describen otros mecanismos.

---

## wset3_17 (sq 17) · RA1 · gold=False

**Pregunta:** ¿Cuál es el propósito principal del despalillado antes de la fermentación?
**Correcta (B):** Evitar la extracción de taninos verdes
**Nodo:** `CC_DESTEMMING_TANNIN_STRUCTURE` · score 4 · en stem: despalillado · en respuesta correcta: taninos verdes

- **Causa:** Los raspones pueden estar presentes con las uvas antes de la fermentación y aportar taninos verdes y astringentes.
- **Mecanismo:** Si los raspones permanecen durante la fermentación, de ellos se extraen taninos y compuestos fenólicos verdes hacia el mosto.
- **Efecto:** El despalillado elimina esa fuente de taninos verdes, dando taninos más suaves y redondos y una estructura más limpia en boca.

**Mentor Guía:** La respuesta correcta es B: «Evitar la extracción de taninos verdes». La clave está en el despalillado antes de la fermentación: Si los raspones permanecen durante la fermentación, de ellos se extraen taninos y compuestos fenólicos verdes hacia el mosto. Por eso, el despalillado elimina esa fuente de taninos verdes, dando taninos más suaves y redondos y una estructura más limpia en boca.

**Entrenador Técnico:** Concepto técnico (RA1): Tema: winemaking. Fija el mecanismo del despalillado antes de la fermentación: Los raspones pueden estar presentes con las uvas antes de la fermentación y aportar taninos verdes y astringentes. → Si los raspones permanecen durante la fermentación, de ellos se extraen taninos y compuestos fenólicos verdes hacia el mosto. En el examen, identifica este patrón causa→mecanismo→efecto antes de mirar las opciones.

**Revisor Estricto:** Exigencia de repaso (RA1): debes poder justificar por qué «Evitar la extracción de taninos verdes» es correcta y por qué las otras tres opciones no lo son, citando el mecanismo del despalillado antes de la fermentación. Si no puedes reconstruir la cadena completa sin ver las opciones, repasa este concepto en tu material WSET L3.

**Micro-drill:** Consolidación: ¿cuál de estas afirmaciones corresponde al despalillado antes de la fermentación?
  - A. Adición de aguardiente vínico
  - B. Evitar la extracción de taninos verdes ✅
  - C. Sistema de soleras y criaderas
  - D. Crianza prolongada en botella después de corta crianza en barrica
  - _Explicación:_ «Evitar la extracción de taninos verdes» corresponde al despalillado antes de la fermentación. Las demás afirmaciones son correctas, pero describen otros mecanismos.

---

## wset3_99 (sq 99) · RA4 · gold=False

**Pregunta:** ¿Qué tipo de crianza se utiliza para un Porto Vintage?
**Correcta (B):** Crianza prolongada en botella después de corta crianza en barrica
**Nodo:** `CC_BOTTLE_AGEING_SEDIMENT` · score 3 · en stem: porto, vintage · en respuesta correcta: botella

- **Causa:** Un tinto con suficiente tanino, pigmento y estructura se cría en botella durante un periodo prolongado (años o décadas).
- **Mecanismo:** Los taninos y los antocianos se polimerizan (se unen en moléculas mayores) y acaban precipitando; la estructura se suaviza a medida que disminuyen los taninos libres.
- **Efecto:** Se forma sedimento en la botella; el vino desarrolla aromas terciarios (cuero, tierra, fruta seca, champiñón, tabaco) y los taninos se integran y suavizan.

**Mentor Guía:** La respuesta correcta es B: «Crianza prolongada en botella después de corta crianza en barrica». La clave está en la crianza prolongada en botella de tintos estructurados: Los taninos y los antocianos se polimerizan (se unen en moléculas mayores) y acaban precipitando; la estructura se suaviza a medida que disminuyen los taninos libres. Por eso, se forma sedimento en la botella; el vino desarrolla aromas terciarios (cuero, tierra, fruta seca, champiñón, tabaco) y los taninos se integran y suavizan.

**Entrenador Técnico:** Concepto técnico (RA4): Fija el mecanismo de la crianza prolongada en botella de tintos estructurados: Un tinto con suficiente tanino, pigmento y estructura se cría en botella durante un periodo prolongado (años o décadas). → Los taninos y los antocianos se polimerizan (se unen en moléculas mayores) y acaban precipitando; la estructura se suaviza a medida que disminuyen los taninos libres. En el examen, identifica este patrón causa→mecanismo→efecto antes de mirar las opciones.

**Revisor Estricto:** Exigencia de repaso (RA4): debes poder justificar por qué «Crianza prolongada en botella después de corta crianza en barrica» es correcta y por qué las otras tres opciones no lo son, citando el mecanismo de la crianza prolongada en botella de tintos estructurados. Si no puedes reconstruir la cadena completa sin ver las opciones, repasa este concepto en tu material WSET L3.

**Micro-drill:** Consolidación: ¿cuál de estas afirmaciones corresponde a la crianza prolongada en botella de tintos estructurados?
  - A. Adición de aguardiente vínico
  - B. Crianza prolongada en botella después de corta crianza en barrica ✅
  - C. Sistema de soleras y criaderas
  - D. Evitar la extracción de taninos verdes
  - _Explicación:_ «Crianza prolongada en botella después de corta crianza en barrica» corresponde a la crianza prolongada en botella de tintos estructurados. Las demás afirmaciones son correctas, pero describen otros mecanismos.

---

## wset3_102 (sq 102) · RA4 · gold=False

**Pregunta:** ¿Qué diferencia un Jerez Fino de un Oloroso?
**Correcta (B):** La crianza biológica vs oxidativa
**Nodo:** `CC_FLOR_BIOLOGICAL_AGEING` · score 3 · en stem: fino, jerez · en respuesta correcta: crianza biologica

- **Causa:** La levadura de flor (un velo de cepas de Saccharomyces cerevisiae) se forma en la superficie del vino en botas parcialmente llenas.
- **Mecanismo:** El velo protege al vino del oxígeno; la levadura metaboliza etanol y glicerol produciendo acetaldehído, y su autólisis aporta aminoácidos.
- **Efecto:** El vino desarrolla carácter de crianza biológica: notas de almendra, masa de pan y levadura, color pálido, tanino bajo y protección frente a la oxidación pese a la crianza en bota.

**Mentor Guía:** La respuesta correcta es B: «La crianza biológica vs oxidativa». La clave está en la crianza biológica bajo velo de flor: El velo protege al vino del oxígeno; la levadura metaboliza etanol y glicerol produciendo acetaldehído, y su autólisis aporta aminoácidos. Por eso, el vino desarrolla carácter de crianza biológica: notas de almendra, masa de pan y levadura, color pálido, tanino bajo y protección frente a la oxidación pese a la crianza en bota.

**Entrenador Técnico:** Concepto técnico (RA4): Fija el mecanismo de la crianza biológica bajo velo de flor: La levadura de flor (un velo de cepas de Saccharomyces cerevisiae) se forma en la superficie del vino en botas parcialmente llenas. → El velo protege al vino del oxígeno; la levadura metaboliza etanol y glicerol produciendo acetaldehído, y su autólisis aporta aminoácidos. En el examen, identifica este patrón causa→mecanismo→efecto antes de mirar las opciones.

**Revisor Estricto:** Exigencia de repaso (RA4): debes poder justificar por qué «La crianza biológica vs oxidativa» es correcta y por qué las otras tres opciones no lo son, citando el mecanismo de la crianza biológica bajo velo de flor. Si no puedes reconstruir la cadena completa sin ver las opciones, repasa este concepto en tu material WSET L3.

**Micro-drill:** Consolidación: ¿cuál de estas afirmaciones corresponde a la crianza biológica bajo velo de flor?
  - A. Adición de aguardiente vínico
  - B. Sistema de soleras y criaderas
  - C. La crianza biológica vs oxidativa ✅
  - D. Evitar la extracción de taninos verdes
  - _Explicación:_ «La crianza biológica vs oxidativa» corresponde a la crianza biológica bajo velo de flor. Las demás afirmaciones son correctas, pero describen otros mecanismos.

---

## wset3_209 (sq 209) · RA4 · gold=False

**Pregunta:** ¿Qué sistema de envejecimiento se utiliza en Jerez?
**Correcta (C):** Sistema de soleras y criaderas
**Nodo:** `CC_FRACTIONAL_BLENDING_CONSISTENCY` · score 3 · en stem: envejecimiento, jerez · en respuesta correcta: criaderas

- **Causa:** Se establece un sistema de solera: una serie de botas (criaderas) ordenadas por edad, cada una con vino en distinta etapa de maduración.
- **Mecanismo:** Al extraer vino de las botas más viejas (la solera) para embotellar, estas se rellenan parcialmente con vino más joven de la siguiente criadera, y la cascada continúa por todos los niveles.
- **Efecto:** Cada saca contiene una mezcla de añadas; la incorporación constante de vino viejo y joven mantiene una edad media y un estilo estables año tras año.

**Mentor Guía:** La respuesta correcta es C: «Sistema de soleras y criaderas». La clave está en el sistema de solera y criaderas: Al extraer vino de las botas más viejas (la solera) para embotellar, estas se rellenan parcialmente con vino más joven de la siguiente criadera, y la cascada continúa por todos los niveles. Por eso, cada saca contiene una mezcla de añadas; la incorporación constante de vino viejo y joven mantiene una edad media y un estilo estables año tras año.

**Entrenador Técnico:** Concepto técnico (RA4): Fija el mecanismo del sistema de solera y criaderas: Se establece un sistema de solera: una serie de botas (criaderas) ordenadas por edad, cada una con vino en distinta etapa de maduración. → Al extraer vino de las botas más viejas (la solera) para embotellar, estas se rellenan parcialmente con vino más joven de la siguiente criadera, y la cascada continúa por todos los niveles. En el examen, identifica este patrón causa→mecanismo→efecto antes de mirar las opciones.

**Revisor Estricto:** Exigencia de repaso (RA4): debes poder justificar por qué «Sistema de soleras y criaderas» es correcta y por qué las otras tres opciones no lo son, citando el mecanismo del sistema de solera y criaderas. Si no puedes reconstruir la cadena completa sin ver las opciones, repasa este concepto en tu material WSET L3.

**Micro-drill:** Consolidación: ¿cuál de estas afirmaciones corresponde al sistema de solera y criaderas?
  - A. Adición de aguardiente vínico
  - B. Sistema de soleras y criaderas ✅
  - C. Evitar la extracción de taninos verdes
  - D. Crianza prolongada en botella después de corta crianza en barrica
  - _Explicación:_ «Sistema de soleras y criaderas» corresponde al sistema de solera y criaderas. Las demás afirmaciones son correctas, pero describen otros mecanismos.

---

## wset3_373 (sq 373) · RA1 · gold=False

**Pregunta:** ¿Cuál es una técnica en bodega utilizada para aumentar la extracción en vinos tintos de guarda?
**Correcta (C):** Maceración prolongada y delestage
**Nodo:** `CC_MACERATION_EXTRACTION` · score 3 · en stem: extraccion · en respuesta correcta: delestage, maceracion

- **Causa:** En la vinificación en tinto, el color y los taninos se extraen principalmente de los hollejos durante el contacto entre el mosto en fermentación y las partes sólidas.
- **Mecanismo:** La maceración y las técnicas de manejo del sombrero (remontado, bazuqueo, délestage) aumentan el contacto entre el líquido y los hollejos, permitiendo que pasen más color y taninos al vino.
- **Efecto:** Una mayor extracción produce tintos de color más profundo, mayor estructura tánica y una impresión más completa en boca.

**Mentor Guía:** La respuesta correcta es C: «Maceración prolongada y delestage». La clave está en la maceración y la gestión del sombrero en tintos: La maceración y las técnicas de manejo del sombrero (remontado, bazuqueo, délestage) aumentan el contacto entre el líquido y los hollejos, permitiendo que pasen más color y taninos al vino. Por eso, una mayor extracción produce tintos de color más profundo, mayor estructura tánica y una impresión más completa en boca.

**Entrenador Técnico:** Concepto técnico (RA1): Fija el mecanismo de la maceración y la gestión del sombrero en tintos: En la vinificación en tinto, el color y los taninos se extraen principalmente de los hollejos durante el contacto entre el mosto en fermentación y las partes sólidas. → La maceración y las técnicas de manejo del sombrero (remontado, bazuqueo, délestage) aumentan el contacto entre el líquido y los hollejos, permitiendo que pasen más color y taninos al vino. En el examen, identifica este patrón causa→mecanismo→efecto antes de mirar las opciones.

**Revisor Estricto:** Exigencia de repaso (RA1): debes poder justificar por qué «Maceración prolongada y delestage» es correcta y por qué las otras tres opciones no lo son, citando el mecanismo de la maceración y la gestión del sombrero en tintos. Si no puedes reconstruir la cadena completa sin ver las opciones, repasa este concepto en tu material WSET L3.

**Micro-drill:** Consolidación: ¿cuál de estas afirmaciones corresponde a la maceración y la gestión del sombrero en tintos?
  - A. Adición de aguardiente vínico
  - B. Maceración prolongada y delestage ✅
  - C. Sistema de soleras y criaderas
  - D. Evitar la extracción de taninos verdes
  - _Explicación:_ «Maceración prolongada y delestage» corresponde a la maceración y la gestión del sombrero en tintos. Las demás afirmaciones son correctas, pero describen otros mecanismos.

---

## wset3_2 (sq 2) · RA4 · gold=False

**Pregunta:** ¿Qué método se usa para detener la fermentación en el vino de Oporto?
**Correcta (C):** Adición de aguardiente vínico
**Nodo:** `CC_FORTIFICATION_RESIDUAL_SUGAR` · score 2 · en stem: oporto · en respuesta correcta: aguardiente

- **Causa:** Se añade aguardiente vínico (alcohol neutro de alta graduación) a un mosto o vino parcialmente fermentado.
- **Mecanismo:** La adición eleva el alcohol hasta un nivel (típicamente 15–18% vol.) en el que la levadura no sobrevive: la fermentación se detiene y queda azúcar sin fermentar en el vino.
- **Efecto:** El vino terminado conserva azúcar residual del mosto sin fermentar, dando un estilo dulce o semidulce.

**Mentor Guía:** La respuesta correcta es C: «Adición de aguardiente vínico». La clave está en la fortificación durante la fermentación: La adición eleva el alcohol hasta un nivel (típicamente 15–18% vol.) en el que la levadura no sobrevive: la fermentación se detiene y queda azúcar sin fermentar en el vino. Por eso, el vino terminado conserva azúcar residual del mosto sin fermentar, dando un estilo dulce o semidulce.

**Entrenador Técnico:** Concepto técnico (RA4): Tema: fortified wines. Fija el mecanismo de la fortificación durante la fermentación: Se añade aguardiente vínico (alcohol neutro de alta graduación) a un mosto o vino parcialmente fermentado. → La adición eleva el alcohol hasta un nivel (típicamente 15–18% vol.) en el que la levadura no sobrevive: la fermentación se detiene y queda azúcar sin fermentar en el vino. En el examen, identifica este patrón causa→mecanismo→efecto antes de mirar las opciones.

**Revisor Estricto:** Exigencia de repaso (RA4): debes poder justificar por qué «Adición de aguardiente vínico» es correcta y por qué las otras tres opciones no lo son, citando el mecanismo de la fortificación durante la fermentación. Si no puedes reconstruir la cadena completa sin ver las opciones, repasa este concepto en tu material WSET L3.

**Micro-drill:** Consolidación: ¿cuál de estas afirmaciones corresponde a la fortificación durante la fermentación?
  - A. Sistema de soleras y criaderas
  - B. Adición de aguardiente vínico ✅
  - C. Evitar la extracción de taninos verdes
  - D. Crianza prolongada en botella después de corta crianza en barrica
  - _Explicación:_ «Adición de aguardiente vínico» corresponde a la fortificación durante la fermentación. Las demás afirmaciones son correctas, pero describen otros mecanismos.

---

## wset3_705 (sq 705) · RA1 · gold=False

**Pregunta:** ¿Cuál de las siguientes afirmaciones sobre el roble americano es CORRECTA?
**Correcta (A):** El roble americano tiende a aportar notas más pronunciadas de vainilla y coco que el francés.
**Nodo:** `HC_OAK_AGEING_COMPLEXITY` · score 2 · en stem: roble · en respuesta correcta: roble, vainilla

- **Causa:** El vino criado en barrica de roble recibe pequeñas cantidades continuas de oxígeno a través de los poros de la madera y absorbe compuestos de la propia madera, como vainillina y lactonas.
- **Mecanismo:** La microoxigenación lenta suaviza los taninos por polimerización y redondea la estructura; a la vez, los compuestos de la madera aportan vainilla, especias, tostado y humo.
- **Efecto:** Los vinos criados en roble nuevo suelen mostrar taninos más suaves, mayor complejidad y aromas secundarios (vainilla, tostado, cedro, especias) sobre la fruta primaria.

**Mentor Guía:** La respuesta correcta es A: «El roble americano tiende a aportar notas más pronunciadas de vainilla y coco que el francés.». La clave está en la crianza en barrica de roble: La microoxigenación lenta suaviza los taninos por polimerización y redondea la estructura; a la vez, los compuestos de la madera aportan vainilla, especias, tostado y humo. Por eso, los vinos criados en roble nuevo suelen mostrar taninos más suaves, mayor complejidad y aromas secundarios (vainilla, tostado, cedro, especias) sobre la fruta primaria.

**Entrenador Técnico:** Concepto técnico (RA1): Fija el mecanismo de la crianza en barrica de roble: El vino criado en barrica de roble recibe pequeñas cantidades continuas de oxígeno a través de los poros de la madera y absorbe compuestos de la propia madera, como vainillina y lactonas. → La microoxigenación lenta suaviza los taninos por polimerización y redondea la estructura; a la vez, los compuestos de la madera aportan vainilla, especias, tostado y humo. En el examen, identifica este patrón causa→mecanismo→efecto antes de mirar las opciones.

**Revisor Estricto:** Exigencia de repaso (RA1): debes poder justificar por qué «El roble americano tiende a aportar notas más pronunciadas de vainilla y coco que el francés.» es correcta y por qué las otras tres opciones no lo son, citando el mecanismo de la crianza en barrica de roble. Si no puedes reconstruir la cadena completa sin ver las opciones, repasa este concepto en tu material WSET L3.

**Micro-drill:** Consolidación: ¿cuál de estas afirmaciones corresponde a la crianza en barrica de roble?
  - A. Adición de aguardiente vínico
  - B. Sistema de soleras y criaderas
  - C. El roble americano tiende a aportar notas más pronunciadas de vainilla y coco que el francés. ✅
  - D. Evitar la extracción de taninos verdes
  - _Explicación:_ «El roble americano tiende a aportar notas más pronunciadas de vainilla y coco que el francés.» corresponde a la crianza en barrica de roble. Las demás afirmaciones son correctas, pero describen otros mecanismos.

---


*Documento formativo. Sin autoridad de examinador. safe_for_examiner: false.*
