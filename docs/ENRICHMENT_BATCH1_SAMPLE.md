# ENRICHMENT BATCH 1 — Reporte de muestra para aprobación

Lote: **235 ítems** · derivación determinista desde nodos causales CC_/HC_ (umbral: ≥2 trigger keywords, mejor nodo único, capa ES con guard).
Con micro_drill: **179** · fingerprint de entrada: `07e789300d2e49d4`

Política v2 (precisión primero): word-boundary, triggers genéricos prohibidos, el nodo debe
explicar la respuesta correcta (hit en stem Y en opción correcta), stems de identificación excluidos.

Rechazos por regla: `{"below_threshold": 95, "identification_stem": 112, "no_stem_hit": 2, "negative_polarity_stem": 24, "no_correct_option_hit": 3}`

---

## wset3_287 (sq 287) · RA2 · gold=True

**Pregunta:** ¿Qué define el estilo clásico de un vino tinto de la DOCG Barolo?
**Correcta (B):** Taninos altos, acidez alta y notas terciarias con la edad
**Nodo:** `HC_BAROLO_TERTIARY_EVOLUTION` · score 5 · en stem: barolo, vino tinto de la docg barolo · en respuesta correcta: acidez alta, notas terciarias con la edad, taninos altos

- **Causa:** El Barolo de Nebbiolo parte de taninos altos y acidez alta, que aportan una estructura considerable para la guarda.
- **Mecanismo:** Durante la crianza en botella los taninos se polimerizan y suavizan, mientras los aromas primarios evolucionan gradualmente hacia compuestos terciarios.
- **Efecto:** El Barolo maduro conserva acidez y estructura y desarrolla notas terciarias como flores secas, cuero, tierra y alquitrán.

**Mentor Guía:** La respuesta correcta es B: «Taninos altos, acidez alta y notas terciarias con la edad». La clave está en la evolución en botella del Barolo: Durante la crianza en botella los taninos se polimerizan y suavizan, mientras los aromas primarios evolucionan gradualmente hacia compuestos terciarios. Por eso, el Barolo maduro conserva acidez y estructura y desarrolla notas terciarias como flores secas, cuero, tierra y alquitrán.

**Entrenador Técnico:** Concepto técnico (RA2): Tema: still wines. Fija el mecanismo de la evolución en botella del Barolo: El Barolo de Nebbiolo parte de taninos altos y acidez alta, que aportan una estructura considerable para la guarda. → Durante la crianza en botella los taninos se polimerizan y suavizan, mientras los aromas primarios evolucionan gradualmente hacia compuestos terciarios. En el examen, identifica este patrón causa→mecanismo→efecto antes de mirar las opciones.

**Revisor Estricto:** Exigencia de repaso (RA2): debes poder justificar por qué «Taninos altos, acidez alta y notas terciarias con la edad» es correcta y por qué las otras tres opciones no lo son, citando el mecanismo de la evolución en botella del Barolo. Si no puedes reconstruir la cadena completa sin ver las opciones, repasa este concepto en tu material WSET L3.

**Micro-drill:** Consolidación: ¿cuál de estas afirmaciones corresponde a la evolución en botella del Barolo?
  - A. Taninos altos, acidez alta y notas terciarias con la edad ✅
  - B. Protege al vino del oxígeno y desarrolla sabores únicos
  - C. Adición de aguardiente vínico
  - D. Estructura potente y necesidad de guarda
  - _Explicación:_ «Taninos altos, acidez alta y notas terciarias con la edad» corresponde a la evolución en botella del Barolo. Las demás afirmaciones son correctas, pero describen otros mecanismos.

---

## wset3_464 (sq 464) · RA2 · gold=True

**Pregunta:** ¿Qué efecto tiene el despalillado previo a la fermentación?
**Correcta (A):** Reduce el tanino verde
**Nodo:** `HC_DESTEMMING_GREEN_TANNIN_REDUCTION` · score 2 · en stem: despalillado previo a la fermentacion · en respuesta correcta: reduce el tanino verde

- **Causa:** Los raspones se separan de los racimos antes de la fermentación alcohólica.
- **Mecanismo:** Al retirar los raspones se evita que sus compuestos fenólicos se extraigan hacia el mosto en fermentación.
- **Efecto:** El vino tiene menos probabilidad de adquirir taninos verdes y ásperos de los raspones, aunque todavía puede extraer tanino de hollejos y pepitas.

**Mentor Guía:** La respuesta correcta es A: «Reduce el tanino verde». La clave está en el despalillado previo a la fermentación: Al retirar los raspones se evita que sus compuestos fenólicos se extraigan hacia el mosto en fermentación. Por eso, el vino tiene menos probabilidad de adquirir taninos verdes y ásperos de los raspones, aunque todavía puede extraer tanino de hollejos y pepitas.

**Entrenador Técnico:** Concepto técnico (RA2): Tema: winemaking. Fija el mecanismo del despalillado previo a la fermentación: Los raspones se separan de los racimos antes de la fermentación alcohólica. → Al retirar los raspones se evita que sus compuestos fenólicos se extraigan hacia el mosto en fermentación. En el examen, identifica este patrón causa→mecanismo→efecto antes de mirar las opciones.

**Revisor Estricto:** Exigencia de repaso (RA2): debes poder justificar por qué «Reduce el tanino verde» es correcta y por qué las otras tres opciones no lo son, citando el mecanismo del despalillado previo a la fermentación. Si no puedes reconstruir la cadena completa sin ver las opciones, repasa este concepto en tu material WSET L3.

**Micro-drill:** Consolidación: ¿cuál de estas afirmaciones corresponde al despalillado previo a la fermentación?
  - A. Protege al vino del oxígeno y desarrolla sabores únicos
  - B. Adición de aguardiente vínico
  - C. Reduce el tanino verde ✅
  - D. Estructura potente y necesidad de guarda
  - _Explicación:_ «Reduce el tanino verde» corresponde al despalillado previo a la fermentación. Las demás afirmaciones son correctas, pero describen otros mecanismos.

---

## wset3_498 (sq 498) · RA2 · gold=True

**Pregunta:** ¿Cuál es una práctica común para evitar enfermedades fúngicas en climas húmedos?
**Correcta (B):** Canopy management
**Nodo:** `HC_CANOPY_AIRFLOW_FUNGAL_RISK` · score 2 · en stem: enfermedades fungicas en climas humedos · en respuesta correcta: canopy management

- **Causa:** Un follaje denso alrededor de los racimos restringe el flujo de aire y conserva humedad después de la lluvia o el rocío.
- **Mecanismo:** Abrir el dosel mediante posicionamiento de brotes o deshoje mejora la ventilación y acelera el secado de los racimos.
- **Efecto:** Las condiciones son menos favorables para Botrytis y otros hongos; un dosel excesivamente denso aumenta la presión de enfermedad.

**Mentor Guía:** La respuesta correcta es B: «Canopy management». La clave está en la ventilación del dosel y el riesgo de enfermedades fúngicas: Abrir el dosel mediante posicionamiento de brotes o deshoje mejora la ventilación y acelera el secado de los racimos. Por eso, las condiciones son menos favorables para Botrytis y otros hongos; un dosel excesivamente denso aumenta la presión de enfermedad.

**Entrenador Técnico:** Concepto técnico (RA2): Tema: viticulture. Fija el mecanismo de la ventilación del dosel y el riesgo de enfermedades fúngicas: Un follaje denso alrededor de los racimos restringe el flujo de aire y conserva humedad después de la lluvia o el rocío. → Abrir el dosel mediante posicionamiento de brotes o deshoje mejora la ventilación y acelera el secado de los racimos. En el examen, identifica este patrón causa→mecanismo→efecto antes de mirar las opciones.

**Revisor Estricto:** Exigencia de repaso (RA2): debes poder justificar por qué «Canopy management» es correcta y por qué las otras tres opciones no lo son, citando el mecanismo de la ventilación del dosel y el riesgo de enfermedades fúngicas. Si no puedes reconstruir la cadena completa sin ver las opciones, repasa este concepto en tu material WSET L3.

**Micro-drill:** no derivado (sin patrón claro) — etapa ENTRENAR se salta para este ítem.

---

## wset3_440 (sq 440) · RA1 · gold=True

**Pregunta:** ¿Qué práctica en bodega es común en Chablis para mantener el perfil fresco del vino?
**Correcta (C):** Evitar la fermentación maloláctica
**Nodo:** `HC_MLF_BLOCKING_FRESHNESS` · score 3 · en stem: mantener el perfil fresco, perfil fresco · en respuesta correcta: evitar la fermentacion malolactica

- **Causa:** El elaborador busca mantener la acidez punzante y la fruta primaria de un vino blanco fresco.
- **Mecanismo:** Al bloquear la fermentación maloláctica se evita que las bacterias conviertan el ácido málico, más punzante, en ácido láctico, más suave.
- **Efecto:** El vino conserva más acidez málica y frescura, con un perfil más crujiente y lineal y sin el carácter cremoso que puede acompañar a la FML.

**Mentor Guía:** La respuesta correcta es C: «Evitar la fermentación maloláctica». La clave está en el bloqueo de la fermentación maloláctica para conservar frescura: Al bloquear la fermentación maloláctica se evita que las bacterias conviertan el ácido málico, más punzante, en ácido láctico, más suave. Por eso, el vino conserva más acidez málica y frescura, con un perfil más crujiente y lineal y sin el carácter cremoso que puede acompañar a la FML.

**Entrenador Técnico:** Concepto técnico (RA1): Tema: winemaking. Fija el mecanismo del bloqueo de la fermentación maloláctica para conservar frescura: El elaborador busca mantener la acidez punzante y la fruta primaria de un vino blanco fresco. → Al bloquear la fermentación maloláctica se evita que las bacterias conviertan el ácido málico, más punzante, en ácido láctico, más suave. En el examen, identifica este patrón causa→mecanismo→efecto antes de mirar las opciones.

**Revisor Estricto:** Exigencia de repaso (RA1): debes poder justificar por qué «Evitar la fermentación maloláctica» es correcta y por qué las otras tres opciones no lo son, citando el mecanismo del bloqueo de la fermentación maloláctica para conservar frescura. Si no puedes reconstruir la cadena completa sin ver las opciones, repasa este concepto en tu material WSET L3.

**Micro-drill:** Consolidación: ¿cuál de estas afirmaciones corresponde al bloqueo de la fermentación maloláctica para conservar frescura?
  - A. Protege al vino del oxígeno y desarrolla sabores únicos
  - B. Adición de aguardiente vínico
  - C. Estructura potente y necesidad de guarda
  - D. Evitar la fermentación maloláctica ✅
  - _Explicación:_ «Evitar la fermentación maloláctica» corresponde al bloqueo de la fermentación maloláctica para conservar frescura. Las demás afirmaciones son correctas, pero describen otros mecanismos.

---

## wset3_240 (sq 240) · RA3 · gold=True

**Pregunta:** ¿Qué define al método Charmat usado en Prosecco?
**Correcta (B):** Fermentación en tanques presurizados
**Nodo:** `HC_TANK_METHOD_FRUIT_RETENTION` · score 2 · en stem: metodo charmat · en respuesta correcta: fermentacion en tanques presurizados

- **Causa:** La segunda fermentación se realiza en un tanque cerrado resistente a la presión en lugar de cada botella final.
- **Mecanismo:** El acero inoxidable con temperatura controlada y un contacto relativamente corto con las lías limitan la oxidación y el desarrollo autolítico mientras retienen el CO₂ bajo presión.
- **Efecto:** El espumoso conserva aromas primarios frescos, frutales y florales y puede producirse con mayor rapidez y menor coste.

**Mentor Guía:** La respuesta correcta es B: «Fermentación en tanques presurizados». La clave está en el método de tanque y la conservación de la fruta primaria: El acero inoxidable con temperatura controlada y un contacto relativamente corto con las lías limitan la oxidación y el desarrollo autolítico mientras retienen el CO₂ bajo presión. Por eso, el espumoso conserva aromas primarios frescos, frutales y florales y puede producirse con mayor rapidez y menor coste.

**Entrenador Técnico:** Concepto técnico (RA3): Tema: sparkling wines. Fija el mecanismo del método de tanque y la conservación de la fruta primaria: La segunda fermentación se realiza en un tanque cerrado resistente a la presión en lugar de cada botella final. → El acero inoxidable con temperatura controlada y un contacto relativamente corto con las lías limitan la oxidación y el desarrollo autolítico mientras retienen el CO₂ bajo presión. En el examen, identifica este patrón causa→mecanismo→efecto antes de mirar las opciones.

**Revisor Estricto:** Exigencia de repaso (RA3): debes poder justificar por qué «Fermentación en tanques presurizados» es correcta y por qué las otras tres opciones no lo son, citando el mecanismo del método de tanque y la conservación de la fruta primaria. Si no puedes reconstruir la cadena completa sin ver las opciones, repasa este concepto en tu material WSET L3.

**Micro-drill:** Consolidación: ¿cuál de estas afirmaciones corresponde al método de tanque y la conservación de la fruta primaria?
  - A. Protege al vino del oxígeno y desarrolla sabores únicos
  - B. Fermentación en tanques presurizados ✅
  - C. Adición de aguardiente vínico
  - D. Estructura potente y necesidad de guarda
  - _Explicación:_ «Fermentación en tanques presurizados» corresponde al método de tanque y la conservación de la fruta primaria. Las demás afirmaciones son correctas, pero describen otros mecanismos.

---

## wset3_493 (sq 493) · RA1 · gold=True

**Pregunta:** ¿Cuál es el principal riesgo de una vendimia muy tardía?
**Correcta (B):** Exposición a heladas
**Nodo:** `HC_LATE_HARVEST_FROST_EXPOSURE` · score 2 · en stem: vendimia muy tardia · en respuesta correcta: exposicion a heladas

- **Causa:** Las uvas permanecen en la vid hasta muy avanzado el otoño para ganar madurez o concentración.
- **Mecanismo:** El tiempo adicional de permanencia coincide con noches más frías y una probabilidad creciente de heladas.
- **Efecto:** Una helada puede dañar o congelar la fruta antes de la cosecha, amenazando el rendimiento y el estilo previsto.

**Mentor Guía:** La respuesta correcta es B: «Exposición a heladas». La clave está en la vendimia muy tardía y la exposición a heladas: El tiempo adicional de permanencia coincide con noches más frías y una probabilidad creciente de heladas. Por eso, una helada puede dañar o congelar la fruta antes de la cosecha, amenazando el rendimiento y el estilo previsto.

**Entrenador Técnico:** Concepto técnico (RA1): Tema: viticulture. Fija el mecanismo de la vendimia muy tardía y la exposición a heladas: Las uvas permanecen en la vid hasta muy avanzado el otoño para ganar madurez o concentración. → El tiempo adicional de permanencia coincide con noches más frías y una probabilidad creciente de heladas. En el examen, identifica este patrón causa→mecanismo→efecto antes de mirar las opciones.

**Revisor Estricto:** Exigencia de repaso (RA1): debes poder justificar por qué «Exposición a heladas» es correcta y por qué las otras tres opciones no lo son, citando el mecanismo de la vendimia muy tardía y la exposición a heladas. Si no puedes reconstruir la cadena completa sin ver las opciones, repasa este concepto en tu material WSET L3.

**Micro-drill:** Consolidación: ¿cuál de estas afirmaciones corresponde a la vendimia muy tardía y la exposición a heladas?
  - A. Protege al vino del oxígeno y desarrolla sabores únicos
  - B. Adición de aguardiente vínico
  - C. Estructura potente y necesidad de guarda
  - D. Exposición a heladas ✅
  - _Explicación:_ «Exposición a heladas» corresponde a la vendimia muy tardía y la exposición a heladas. Las demás afirmaciones son correctas, pero describen otros mecanismos.

---

## wset3_372 (sq 372) · RA2 · gold=False

**Pregunta:** ¿Cuál es el efecto de la botrytis en los vinos de Tokaj?
**Correcta (C):** Aumenta la concentración de azúcar y acidez
**Nodo:** `HC_BOTRYTIS_CONCENTRATION` · score 3 · en stem: botrytis · en respuesta correcta: aumenta la concentracion, concentracion de azucar

- **Causa:** La Botrytis cinerea beneficiosa infecta uvas maduras cuando periodos húmedos o con niebla van seguidos de condiciones cálidas y secas.
- **Mecanismo:** El hongo perfora la piel de la baya y permite que el agua se evapore durante los periodos secos. Esta pérdida de agua concentra directamente los azúcares y los compuestos de sabor; al mismo tiempo, la Botrytis metaboliza parte de los ácidos de la uva.
- **Efecto:** La fruta adquiere mayor concentración de azúcar y sabor, una textura rica y aromas característicos de podredumbre noble. La acidez neta depende del equilibrio entre concentración y metabolismo de ácidos, por lo que no debe interpretarse como una regla simple de aumento de acidez.

**Mentor Guía:** La respuesta correcta es C: «Aumenta la concentración de azúcar y acidez». La clave está en la podredumbre noble y la concentración de la uva: El hongo perfora la piel de la baya y permite que el agua se evapore durante los periodos secos. Esta pérdida de agua concentra directamente los azúcares y los compuestos de sabor; al mismo tiempo, la Botrytis metaboliza parte de los ácidos de la uva. Por eso, la fruta adquiere mayor concentración de azúcar y sabor, una textura rica y aromas característicos de podredumbre noble. La acidez neta depende del equilibrio entre concentración y metabolismo de ácidos, por lo que no debe interpretarse como una regla simple de aumento de acidez.

**Entrenador Técnico:** Concepto técnico (RA2): Fija el mecanismo de la podredumbre noble y la concentración de la uva: La Botrytis cinerea beneficiosa infecta uvas maduras cuando periodos húmedos o con niebla van seguidos de condiciones cálidas y secas. → El hongo perfora la piel de la baya y permite que el agua se evapore durante los periodos secos. Esta pérdida de agua concentra directamente los azúcares y los compuestos de sabor; al mismo tiempo, la Botrytis metaboliza parte de los ácidos de la uva. En el examen, identifica este patrón causa→mecanismo→efecto antes de mirar las opciones.

**Revisor Estricto:** Exigencia de repaso (RA2): debes poder justificar por qué «Aumenta la concentración de azúcar y acidez» es correcta y por qué las otras tres opciones no lo son, citando el mecanismo de la podredumbre noble y la concentración de la uva. Si no puedes reconstruir la cadena completa sin ver las opciones, repasa este concepto en tu material WSET L3.

**Micro-drill:** Consolidación: ¿cuál de estas afirmaciones corresponde a la podredumbre noble y la concentración de la uva?
  - A. Aumenta la concentración de azúcar y acidez ✅
  - B. Protege al vino del oxígeno y desarrolla sabores únicos
  - C. Adición de aguardiente vínico
  - D. Estructura potente y necesidad de guarda
  - _Explicación:_ «Aumenta la concentración de azúcar y acidez» corresponde a la podredumbre noble y la concentración de la uva. Las demás afirmaciones son correctas, pero describen otros mecanismos.

---

## wset3_385 (sq 385) · RA2 · gold=False

**Pregunta:** ¿Cuál es una característica típica de un vino tinto Grand Cru Classé del Médoc?
**Correcta (C):** Alta intensidad, taninos firmes y capacidad de envejecimiento
**Nodo:** `HC_RED_WINE_AGEABILITY_STRUCTURE` · score 3 · en stem: grand cru classe del medoc · en respuesta correcta: capacidad de envejecimiento, taninos firmes

- **Causa:** Un tinto concentrado parte de taninos, acidez y fruta abundantes y, en estilos fortificados, también de alcohol y azúcar.
- **Mecanismo:** La acidez y otros componentes estables ralentizan el deterioro, mientras los taninos se polimerizan y el perfil concentrado evoluciona con el tiempo.
- **Efecto:** El vino tiene capacidad estructural para una guarda prolongada, durante la cual los taninos pueden integrarse y surgir complejidad terciaria; esa estructura permite la evolución, pero no garantiza mejora si el almacenamiento es deficiente.

**Mentor Guía:** La respuesta correcta es C: «Alta intensidad, taninos firmes y capacidad de envejecimiento». La clave está en la estructura que permite la guarda prolongada de un vino tinto: La acidez y otros componentes estables ralentizan el deterioro, mientras los taninos se polimerizan y el perfil concentrado evoluciona con el tiempo. Por eso, el vino tiene capacidad estructural para una guarda prolongada, durante la cual los taninos pueden integrarse y surgir complejidad terciaria; esa estructura permite la evolución, pero no garantiza mejora si el almacenamiento es deficiente.

**Entrenador Técnico:** Concepto técnico (RA2): Fija el mecanismo de la estructura que permite la guarda prolongada de un vino tinto: Un tinto concentrado parte de taninos, acidez y fruta abundantes y, en estilos fortificados, también de alcohol y azúcar. → La acidez y otros componentes estables ralentizan el deterioro, mientras los taninos se polimerizan y el perfil concentrado evoluciona con el tiempo. En el examen, identifica este patrón causa→mecanismo→efecto antes de mirar las opciones.

**Revisor Estricto:** Exigencia de repaso (RA2): debes poder justificar por qué «Alta intensidad, taninos firmes y capacidad de envejecimiento» es correcta y por qué las otras tres opciones no lo son, citando el mecanismo de la estructura que permite la guarda prolongada de un vino tinto. Si no puedes reconstruir la cadena completa sin ver las opciones, repasa este concepto en tu material WSET L3.

**Micro-drill:** Consolidación: ¿cuál de estas afirmaciones corresponde a la estructura que permite la guarda prolongada de un vino tinto?
  - A. Alta intensidad, taninos firmes y capacidad de envejecimiento ✅
  - B. Protege al vino del oxígeno y desarrolla sabores únicos
  - C. Adición de aguardiente vínico
  - D. Sistema de soleras y criaderas
  - _Explicación:_ «Alta intensidad, taninos firmes y capacidad de envejecimiento» corresponde a la estructura que permite la guarda prolongada de un vino tinto. Las demás afirmaciones son correctas, pero describen otros mecanismos.

---

## wset3_436 (sq 436) · RA2 · gold=False

**Pregunta:** ¿Qué se busca con el manejo del dosel (canopy management)?
**Correcta (B):** Incrementar la exposición solar
**Nodo:** `HC_CANOPY_VIGOUR_EXPOSURE` · score 3 · en stem: manejo del dosel, que se busca con el manejo del dosel · en respuesta correcta: incrementar la exposicion solar

- **Causa:** Se gestionan brotes y hojas durante la temporada mediante poda en verde y otras operaciones de dosel.
- **Mecanismo:** Retirar o posicionar crecimiento limita la densidad vegetal y mejora la entrada de luz y la ventilación alrededor de los racimos.
- **Efecto:** Se controla el vigor y se equilibran la exposición de los racimos y sus condiciones de maduración.

**Mentor Guía:** La respuesta correcta es B: «Incrementar la exposición solar». La clave está en el manejo del dosel, el vigor y la exposición de los racimos: Retirar o posicionar crecimiento limita la densidad vegetal y mejora la entrada de luz y la ventilación alrededor de los racimos. Por eso, se controla el vigor y se equilibran la exposición de los racimos y sus condiciones de maduración.

**Entrenador Técnico:** Concepto técnico (RA2): Fija el mecanismo del manejo del dosel, el vigor y la exposición de los racimos: Se gestionan brotes y hojas durante la temporada mediante poda en verde y otras operaciones de dosel. → Retirar o posicionar crecimiento limita la densidad vegetal y mejora la entrada de luz y la ventilación alrededor de los racimos. En el examen, identifica este patrón causa→mecanismo→efecto antes de mirar las opciones.

**Revisor Estricto:** Exigencia de repaso (RA2): debes poder justificar por qué «Incrementar la exposición solar» es correcta y por qué las otras tres opciones no lo son, citando el mecanismo del manejo del dosel, el vigor y la exposición de los racimos. Si no puedes reconstruir la cadena completa sin ver las opciones, repasa este concepto en tu material WSET L3.

**Micro-drill:** Consolidación: ¿cuál de estas afirmaciones corresponde al manejo del dosel, el vigor y la exposición de los racimos?
  - A. Incrementar la exposición solar ✅
  - B. Protege al vino del oxígeno y desarrolla sabores únicos
  - C. Adición de aguardiente vínico
  - D. Estructura potente y necesidad de guarda
  - _Explicación:_ «Incrementar la exposición solar» corresponde al manejo del dosel, el vigor y la exposición de los racimos. Las demás afirmaciones son correctas, pero describen otros mecanismos.

---

## wset3_483 (sq 483) · RA2 · gold=False

**Pregunta:** ¿Cuál de los siguientes factores contribuye a una mayor concentración fenólica en la uva?
**Correcta (C):** Estrés hídrico moderado
**Nodo:** `HC_MODERATE_WATER_STRESS_PHENOLICS` · score 3 · en stem: factores contribuye a una mayor concentracion fenolica, mayor concentracion fenolica · en respuesta correcta: estres hidrico moderado

- **Causa:** La vid sufre un déficit de agua moderado, no severo, durante el desarrollo y la maduración de las bayas.
- **Mecanismo:** Se limita el crecimiento de los brotes y las bayas permanecen más pequeñas, aumentando la proporción de hollejo rico en fenoles respecto al jugo.
- **Efecto:** Puede aumentar la concentración fenólica, incluido el potencial de color y tanino; un estrés severo, en cambio, detendría la fotosíntesis y la maduración.

**Mentor Guía:** La respuesta correcta es C: «Estrés hídrico moderado». La clave está en el estrés hídrico moderado y la concentración fenólica: Se limita el crecimiento de los brotes y las bayas permanecen más pequeñas, aumentando la proporción de hollejo rico en fenoles respecto al jugo. Por eso, puede aumentar la concentración fenólica, incluido el potencial de color y tanino; un estrés severo, en cambio, detendría la fotosíntesis y la maduración.

**Entrenador Técnico:** Concepto técnico (RA2): Fija el mecanismo del estrés hídrico moderado y la concentración fenólica: La vid sufre un déficit de agua moderado, no severo, durante el desarrollo y la maduración de las bayas. → Se limita el crecimiento de los brotes y las bayas permanecen más pequeñas, aumentando la proporción de hollejo rico en fenoles respecto al jugo. En el examen, identifica este patrón causa→mecanismo→efecto antes de mirar las opciones.

**Revisor Estricto:** Exigencia de repaso (RA2): debes poder justificar por qué «Estrés hídrico moderado» es correcta y por qué las otras tres opciones no lo son, citando el mecanismo del estrés hídrico moderado y la concentración fenólica. Si no puedes reconstruir la cadena completa sin ver las opciones, repasa este concepto en tu material WSET L3.

**Micro-drill:** Consolidación: ¿cuál de estas afirmaciones corresponde al estrés hídrico moderado y la concentración fenólica?
  - A. Protege al vino del oxígeno y desarrolla sabores únicos
  - B. Adición de aguardiente vínico
  - C. Estructura potente y necesidad de guarda
  - D. Estrés hídrico moderado ✅
  - _Explicación:_ «Estrés hídrico moderado» corresponde al estrés hídrico moderado y la concentración fenólica. Las demás afirmaciones son correctas, pero describen otros mecanismos.

---

## wset3_513 (sq 513) · RA2 · gold=False

**Pregunta:** ¿Qué característica se espera de un vino tinto elaborado con vendimia tardía?
**Correcta (D):** Cuerpo alto y sabores maduros
**Nodo:** `HC_LATE_HARVEST_RIPENESS_BODY` · score 3 · en stem: vendimia tardia, vino tinto elaborado con vendimia tardia · en respuesta correcta: cuerpo alto y sabores maduros

- **Causa:** Uvas tintas sanas permanecen más tiempo en la vid antes de cosecharse mientras las condiciones todavía permiten madurar.
- **Mecanismo:** El tiempo adicional suele permitir más acumulación de azúcar y desarrollo de sabores y puede reducir el agua de la baya, mientras la acidez tiende a disminuir.
- **Efecto:** Tras la fermentación, el vino puede mostrar fruta más madura, alcohol más alto y mayor cuerpo, pero el resultado depende de la sanidad, el clima, el rendimiento, la extracción y la vinificación.

**Mentor Guía:** La respuesta correcta es D: «Cuerpo alto y sabores maduros». La clave está en la vendimia tardía, la madurez y el cuerpo del vino: El tiempo adicional suele permitir más acumulación de azúcar y desarrollo de sabores y puede reducir el agua de la baya, mientras la acidez tiende a disminuir. Por eso, tras la fermentación, el vino puede mostrar fruta más madura, alcohol más alto y mayor cuerpo, pero el resultado depende de la sanidad, el clima, el rendimiento, la extracción y la vinificación.

**Entrenador Técnico:** Concepto técnico (RA2): Fija el mecanismo de la vendimia tardía, la madurez y el cuerpo del vino: Uvas tintas sanas permanecen más tiempo en la vid antes de cosecharse mientras las condiciones todavía permiten madurar. → El tiempo adicional suele permitir más acumulación de azúcar y desarrollo de sabores y puede reducir el agua de la baya, mientras la acidez tiende a disminuir. En el examen, identifica este patrón causa→mecanismo→efecto antes de mirar las opciones.

**Revisor Estricto:** Exigencia de repaso (RA2): debes poder justificar por qué «Cuerpo alto y sabores maduros» es correcta y por qué las otras tres opciones no lo son, citando el mecanismo de la vendimia tardía, la madurez y el cuerpo del vino. Si no puedes reconstruir la cadena completa sin ver las opciones, repasa este concepto en tu material WSET L3.

**Micro-drill:** Consolidación: ¿cuál de estas afirmaciones corresponde a la vendimia tardía, la madurez y el cuerpo del vino?
  - A. Protege al vino del oxígeno y desarrolla sabores únicos
  - B. Adición de aguardiente vínico
  - C. Estructura potente y necesidad de guarda
  - D. Cuerpo alto y sabores maduros ✅
  - _Explicación:_ «Cuerpo alto y sabores maduros» corresponde a la vendimia tardía, la madurez y el cuerpo del vino. Las demás afirmaciones son correctas, pero describen otros mecanismos.

---

## wset3_671 (sq 671) · RA2 · gold=False

**Pregunta:** ¿Cuál de las siguientes afirmaciones sobre los viñedos del Mosel es CORRECTA?
**Correcta (A):** Las pendientes pronunciadas del Mosel favorecen la maduración del Riesling al maximizar la insolación.
**Nodo:** `HC_STEEP_SLOPE_SOLAR_RIPENING` · score 3 · en stem: afirmaciones sobre los vinedos del mosel · en respuesta correcta: maximizar la insolacion, pendientes pronunciadas del mosel favorecen la maduracion del riesling

- **Causa:** Las vides crecen en una pendiente pronunciada cuya orientación recibe sol favorable en una región fresca.
- **Mecanismo:** El ángulo y la orientación de la ladera mejoran la intercepción de radiación directa, elevan la temperatura del dosel y de los racimos y sostienen la fotosíntesis en condiciones de maduración marginales.
- **Efecto:** La uva puede madurar con mayor fiabilidad y alcanzar más desarrollo de sabor y azúcar que en un sitio mal expuesto; la pendiente por sí sola no garantiza ese efecto.

**Mentor Guía:** La respuesta correcta es A: «Las pendientes pronunciadas del Mosel favorecen la maduración del Riesling al maximizar la insolación.». La clave está en las pendientes bien orientadas y la maduración en clima fresco: El ángulo y la orientación de la ladera mejoran la intercepción de radiación directa, elevan la temperatura del dosel y de los racimos y sostienen la fotosíntesis en condiciones de maduración marginales. Por eso, la uva puede madurar con mayor fiabilidad y alcanzar más desarrollo de sabor y azúcar que en un sitio mal expuesto; la pendiente por sí sola no garantiza ese efecto.

**Entrenador Técnico:** Concepto técnico (RA2): Fija el mecanismo de las pendientes bien orientadas y la maduración en clima fresco: Las vides crecen en una pendiente pronunciada cuya orientación recibe sol favorable en una región fresca. → El ángulo y la orientación de la ladera mejoran la intercepción de radiación directa, elevan la temperatura del dosel y de los racimos y sostienen la fotosíntesis en condiciones de maduración marginales. En el examen, identifica este patrón causa→mecanismo→efecto antes de mirar las opciones.

**Revisor Estricto:** Exigencia de repaso (RA2): debes poder justificar por qué «Las pendientes pronunciadas del Mosel favorecen la maduración del Riesling al maximizar la insolación.» es correcta y por qué las otras tres opciones no lo son, citando el mecanismo de las pendientes bien orientadas y la maduración en clima fresco. Si no puedes reconstruir la cadena completa sin ver las opciones, repasa este concepto en tu material WSET L3.

**Micro-drill:** Consolidación: ¿cuál de estas afirmaciones corresponde a las pendientes bien orientadas y la maduración en clima fresco?
  - A. Las pendientes pronunciadas del Mosel favorecen la maduración del Riesling al maximizar la insolación. ✅
  - B. Protege al vino del oxígeno y desarrolla sabores únicos
  - C. Adición de aguardiente vínico
  - D. Estructura potente y necesidad de guarda
  - _Explicación:_ «Las pendientes pronunciadas del Mosel favorecen la maduración del Riesling al maximizar la insolación.» corresponde a las pendientes bien orientadas y la maduración en clima fresco. Las demás afirmaciones son correctas, pero describen otros mecanismos.

---

## wset3_339 (sq 339) · RA2 · gold=False

**Pregunta:** ¿Qué práctica de vinificación se emplea para producir Amarone della Valpolicella?
**Correcta (C):** Secado parcial de uvas antes de la fermentación
**Nodo:** `manual_review_v1` · score 0 · en stem:  · en respuesta correcta: Secado parcial de uvas antes de la fermentación

- **Causa:** Uvas maduras y sanas se secan después de la vendimia antes de iniciar la fermentación alcohólica.
- **Mecanismo:** La evaporación de agua concentra azúcares, ácidos, compuestos de sabor y fenoles en las bayas.
- **Efecto:** El vino puede alcanzar alcohol potencial alto, cuerpo considerable y sabores concentrados de fruta madura o desecada; la sanidad y el control del secado siguen siendo esenciales.

**Mentor Guía:** La respuesta correcta es C: «Secado parcial de uvas antes de la fermentación». La clave está en el secado parcial de uvas antes de la fermentación: La evaporación de agua concentra azúcares, ácidos, compuestos de sabor y fenoles en las bayas. Por eso, el vino puede alcanzar alcohol potencial alto, cuerpo considerable y sabores concentrados de fruta madura o desecada; la sanidad y el control del secado siguen siendo esenciales. Matiz: El secado debe controlarse para evitar podredumbre no deseada y no es equivalente a añadir azúcar.

**Entrenador Técnico:** Concepto técnico (RA2): Fija el mecanismo del secado parcial de uvas antes de la fermentación: Uvas maduras y sanas se secan después de la vendimia antes de iniciar la fermentación alcohólica. → La evaporación de agua concentra azúcares, ácidos, compuestos de sabor y fenoles en las bayas. En el examen, identifica este patrón causa→mecanismo→efecto antes de mirar las opciones. Matiz: El secado debe controlarse para evitar podredumbre no deseada y no es equivalente a añadir azúcar.

**Revisor Estricto:** Exigencia de repaso (RA2): debes poder justificar por qué «Secado parcial de uvas antes de la fermentación» es correcta y por qué las otras tres opciones no lo son, citando el mecanismo del secado parcial de uvas antes de la fermentación. Si no puedes reconstruir la cadena completa sin ver las opciones, repasa este concepto en tu material WSET L3. Matiz: El secado debe controlarse para evitar podredumbre no deseada y no es equivalente a añadir azúcar.

**Micro-drill:** Consolidación: ¿cuál de estas afirmaciones corresponde al secado parcial de uvas antes de la fermentación?
  - A. Protege al vino del oxígeno y desarrolla sabores únicos
  - B. Adición de aguardiente vínico
  - C. Estructura potente y necesidad de guarda
  - D. Secado parcial de uvas antes de la fermentación ✅
  - _Explicación:_ «Secado parcial de uvas antes de la fermentación» corresponde al secado parcial de uvas antes de la fermentación. Las demás afirmaciones son correctas, pero describen otros mecanismos.

---

## wset3_354 (sq 354) · RA2 · gold=False

**Pregunta:** ¿Qué factor permite que los vinos del Valle de Casablanca tengan acidez elevada y frescura aromática?
**Correcta (C):** Corriente de Humboldt
**Nodo:** `HC_HUMBOLDT_CURRENT_FRESHNESS` · score 2 · en stem: vinos del valle de casablanca tengan acidez elevada y frescura aromatica · en respuesta correcta: corriente de humboldt

- **Causa:** La corriente fría de Humboldt enfría el Pacífico cercano y favorece aire fresco y nieblas en el Valle de Casablanca.
- **Mecanismo:** Las temperaturas de cultivo más bajas ralentizan la maduración y reducen la pérdida respiratoria de ácidos.
- **Efecto:** La uva conserva acidez elevada y frescura aromática a pesar de la latitud chilena.

**Mentor Guía:** La respuesta correcta es C: «Corriente de Humboldt». La clave está en la corriente de Humboldt y la frescura del Valle de Casablanca: Las temperaturas de cultivo más bajas ralentizan la maduración y reducen la pérdida respiratoria de ácidos. Por eso, la uva conserva acidez elevada y frescura aromática a pesar de la latitud chilena.

**Entrenador Técnico:** Concepto técnico (RA2): Fija el mecanismo de la corriente de Humboldt y la frescura del Valle de Casablanca: La corriente fría de Humboldt enfría el Pacífico cercano y favorece aire fresco y nieblas en el Valle de Casablanca. → Las temperaturas de cultivo más bajas ralentizan la maduración y reducen la pérdida respiratoria de ácidos. En el examen, identifica este patrón causa→mecanismo→efecto antes de mirar las opciones.

**Revisor Estricto:** Exigencia de repaso (RA2): debes poder justificar por qué «Corriente de Humboldt» es correcta y por qué las otras tres opciones no lo son, citando el mecanismo de la corriente de Humboldt y la frescura del Valle de Casablanca. Si no puedes reconstruir la cadena completa sin ver las opciones, repasa este concepto en tu material WSET L3.

**Micro-drill:** Consolidación: ¿cuál de estas afirmaciones corresponde a la corriente de Humboldt y la frescura del Valle de Casablanca?
  - A. Protege al vino del oxígeno y desarrolla sabores únicos
  - B. Corriente de Humboldt ✅
  - C. Adición de aguardiente vínico
  - D. Estructura potente y necesidad de guarda
  - _Explicación:_ «Corriente de Humboldt» corresponde a la corriente de Humboldt y la frescura del Valle de Casablanca. Las demás afirmaciones son correctas, pero describen otros mecanismos.

---

## wset3_365 (sq 365) · RA2 · gold=False

**Pregunta:** ¿Qué efecto tiene la altitud en los vinos del Valle de Uco, Mendoza?
**Correcta (C):** Aumenta la acidez y retención de aromas
**Nodo:** `HC_ALTITUDE_SLOW_RIPENING_FRESHNESS` · score 2 · en stem: efecto tiene la altitud en los vinos del valle de uco · en respuesta correcta: aumenta la acidez y retencion de aromas

- **Causa:** El viñedo se encuentra a gran altitud, donde las temperaturas ambientales, sobre todo nocturnas, son más bajas.
- **Mecanismo:** Las condiciones más frescas ralentizan la maduración y reducen la pérdida respiratoria de ácidos de la uva, a la vez que prolongan el desarrollo aromático.
- **Efecto:** La fruta de altura puede conservar más acidez y frescura aromática y madurar más lentamente que fruta comparable de menor altitud.

**Mentor Guía:** La respuesta correcta es C: «Aumenta la acidez y retención de aromas». La clave está en la altitud elevada, la maduración lenta y la frescura: Las condiciones más frescas ralentizan la maduración y reducen la pérdida respiratoria de ácidos de la uva, a la vez que prolongan el desarrollo aromático. Por eso, la fruta de altura puede conservar más acidez y frescura aromática y madurar más lentamente que fruta comparable de menor altitud.

**Entrenador Técnico:** Concepto técnico (RA2): Fija el mecanismo de la altitud elevada, la maduración lenta y la frescura: El viñedo se encuentra a gran altitud, donde las temperaturas ambientales, sobre todo nocturnas, son más bajas. → Las condiciones más frescas ralentizan la maduración y reducen la pérdida respiratoria de ácidos de la uva, a la vez que prolongan el desarrollo aromático. En el examen, identifica este patrón causa→mecanismo→efecto antes de mirar las opciones.

**Revisor Estricto:** Exigencia de repaso (RA2): debes poder justificar por qué «Aumenta la acidez y retención de aromas» es correcta y por qué las otras tres opciones no lo son, citando el mecanismo de la altitud elevada, la maduración lenta y la frescura. Si no puedes reconstruir la cadena completa sin ver las opciones, repasa este concepto en tu material WSET L3.

**Micro-drill:** Consolidación: ¿cuál de estas afirmaciones corresponde a la altitud elevada, la maduración lenta y la frescura?
  - A. Protege al vino del oxígeno y desarrolla sabores únicos
  - B. Adición de aguardiente vínico
  - C. Aumenta la acidez y retención de aromas ✅
  - D. Estructura potente y necesidad de guarda
  - _Explicación:_ «Aumenta la acidez y retención de aromas» corresponde a la altitud elevada, la maduración lenta y la frescura. Las demás afirmaciones son correctas, pero describen otros mecanismos.

---

## wset3_380 (sq 380) · RA2 · gold=False

**Pregunta:** ¿Qué permite el clima continental en Ribera del Duero?
**Correcta (C):** Alta oscilación térmica y concentración
**Nodo:** `HC_DIURNAL_RANGE_FRESHNESS` · score 2 · en stem: clima continental · en respuesta correcta: oscilacion termica

- **Causa:** Las regiones con gran amplitud térmica —donde los días cálidos favorecen la acumulación de azúcar pero las noches frescas frenan la respiración— generan un patrón de maduración característico.
- **Mecanismo:** El calor diurno permite que la fotosíntesis y el desarrollo de azúcar avancen, mientras que las noches frescas frenan la degradación respiratoria del ácido tartárico y málico, conservando la acidez.
- **Efecto:** Los vinos de gran amplitud térmica retienen más acidez, muestran un carácter aromático marcado y preciso, y suelen exhibir una frescura o vibración que los distingue de los de clima más cálido y uniforme.

**Mentor Guía:** La respuesta correcta es C: «Alta oscilación térmica y concentración». La clave está en la amplitud térmica entre el día y la noche: El calor diurno permite que la fotosíntesis y el desarrollo de azúcar avancen, mientras que las noches frescas frenan la degradación respiratoria del ácido tartárico y málico, conservando la acidez. Por eso, los vinos de gran amplitud térmica retienen más acidez, muestran un carácter aromático marcado y preciso, y suelen exhibir una frescura o vibración que los distingue de los de clima más cálido y uniforme.

**Entrenador Técnico:** Concepto técnico (RA2): Fija el mecanismo de la amplitud térmica entre el día y la noche: Las regiones con gran amplitud térmica —donde los días cálidos favorecen la acumulación de azúcar pero las noches frescas frenan la respiración— generan un patrón de maduración característico. → El calor diurno permite que la fotosíntesis y el desarrollo de azúcar avancen, mientras que las noches frescas frenan la degradación respiratoria del ácido tartárico y málico, conservando la acidez. En el examen, identifica este patrón causa→mecanismo→efecto antes de mirar las opciones.

**Revisor Estricto:** Exigencia de repaso (RA2): debes poder justificar por qué «Alta oscilación térmica y concentración» es correcta y por qué las otras tres opciones no lo son, citando el mecanismo de la amplitud térmica entre el día y la noche. Si no puedes reconstruir la cadena completa sin ver las opciones, repasa este concepto en tu material WSET L3.

**Micro-drill:** Consolidación: ¿cuál de estas afirmaciones corresponde a la amplitud térmica entre el día y la noche?
  - A. Protege al vino del oxígeno y desarrolla sabores únicos
  - B. Adición de aguardiente vínico
  - C. Estructura potente y necesidad de guarda
  - D. Alta oscilación térmica y concentración ✅
  - _Explicación:_ «Alta oscilación térmica y concentración» corresponde a la amplitud térmica entre el día y la noche. Las demás afirmaciones son correctas, pero describen otros mecanismos.

---

## wset3_388 (sq 388) · RA2 · gold=False

**Pregunta:** ¿Qué influencia tiene el clima marítimo en la región de Bordeaux?
**Correcta (C):** Modera el clima y reduce el riesgo de heladas
**Nodo:** `HC_MARITIME_MODERATION` · score 2 · en stem: clima maritimo · en respuesta correcta: modera el clima y reduce el riesgo de heladas

- **Causa:** Un clima marítimo u oceánico se da en regiones próximas al mar o al océano, cuya gran masa térmica se calienta y se enfría lentamente a lo largo del año.
- **Mecanismo:** El agua cercana modera los extremos de temperatura: mantiene veranos más frescos e inviernos más suaves que los sitios de interior a la misma latitud, reduce el riesgo de heladas y de calor excesivo y alarga la temporada, aunque puede traer lluvia y humedad.
- **Efecto:** Los vinos de clima marítimo tienden a una maduración moderada y uniforme, con acidez conservada y elegancia; la temporada más larga y suave favorece estilos equilibrados, siendo la lluvia de la añada un riesgo clave.

**Mentor Guía:** La respuesta correcta es C: «Modera el clima y reduce el riesgo de heladas». La clave está en la influencia marítima u oceánica: El agua cercana modera los extremos de temperatura: mantiene veranos más frescos e inviernos más suaves que los sitios de interior a la misma latitud, reduce el riesgo de heladas y de calor excesivo y alarga la temporada, aunque puede traer lluvia y humedad. Por eso, los vinos de clima marítimo tienden a una maduración moderada y uniforme, con acidez conservada y elegancia; la temporada más larga y suave favorece estilos equilibrados, siendo la lluvia de la añada un riesgo clave.

**Entrenador Técnico:** Concepto técnico (RA2): Fija el mecanismo de la influencia marítima u oceánica: Un clima marítimo u oceánico se da en regiones próximas al mar o al océano, cuya gran masa térmica se calienta y se enfría lentamente a lo largo del año. → El agua cercana modera los extremos de temperatura: mantiene veranos más frescos e inviernos más suaves que los sitios de interior a la misma latitud, reduce el riesgo de heladas y de calor excesivo y alarga la temporada, aunque puede traer lluvia y humedad. En el examen, identifica este patrón causa→mecanismo→efecto antes de mirar las opciones.

**Revisor Estricto:** Exigencia de repaso (RA2): debes poder justificar por qué «Modera el clima y reduce el riesgo de heladas» es correcta y por qué las otras tres opciones no lo son, citando el mecanismo de la influencia marítima u oceánica. Si no puedes reconstruir la cadena completa sin ver las opciones, repasa este concepto en tu material WSET L3.

**Micro-drill:** Consolidación: ¿cuál de estas afirmaciones corresponde a la influencia marítima u oceánica?
  - A. Protege al vino del oxígeno y desarrolla sabores únicos
  - B. Modera el clima y reduce el riesgo de heladas ✅
  - C. Adición de aguardiente vínico
  - D. Estructura potente y necesidad de guarda
  - _Explicación:_ «Modera el clima y reduce el riesgo de heladas» corresponde a la influencia marítima u oceánica. Las demás afirmaciones son correctas, pero describen otros mecanismos.

---

## wset3_400 (sq 400) · RA2 · gold=False

**Pregunta:** ¿Qué factor natural permite a Salta producir vinos aromáticos a pesar de su latitud?
**Correcta (C):** Altitud elevada
**Nodo:** `HC_ALTITUDE_SLOW_RIPENING_FRESHNESS` · score 2 · en stem: factor natural permite a salta producir vinos aromaticos · en respuesta correcta: altitud elevada

- **Causa:** El viñedo se encuentra a gran altitud, donde las temperaturas ambientales, sobre todo nocturnas, son más bajas.
- **Mecanismo:** Las condiciones más frescas ralentizan la maduración y reducen la pérdida respiratoria de ácidos de la uva, a la vez que prolongan el desarrollo aromático.
- **Efecto:** La fruta de altura puede conservar más acidez y frescura aromática y madurar más lentamente que fruta comparable de menor altitud.

**Mentor Guía:** La respuesta correcta es C: «Altitud elevada». La clave está en la altitud elevada, la maduración lenta y la frescura: Las condiciones más frescas ralentizan la maduración y reducen la pérdida respiratoria de ácidos de la uva, a la vez que prolongan el desarrollo aromático. Por eso, la fruta de altura puede conservar más acidez y frescura aromática y madurar más lentamente que fruta comparable de menor altitud.

**Entrenador Técnico:** Concepto técnico (RA2): Fija el mecanismo de la altitud elevada, la maduración lenta y la frescura: El viñedo se encuentra a gran altitud, donde las temperaturas ambientales, sobre todo nocturnas, son más bajas. → Las condiciones más frescas ralentizan la maduración y reducen la pérdida respiratoria de ácidos de la uva, a la vez que prolongan el desarrollo aromático. En el examen, identifica este patrón causa→mecanismo→efecto antes de mirar las opciones.

**Revisor Estricto:** Exigencia de repaso (RA2): debes poder justificar por qué «Altitud elevada» es correcta y por qué las otras tres opciones no lo son, citando el mecanismo de la altitud elevada, la maduración lenta y la frescura. Si no puedes reconstruir la cadena completa sin ver las opciones, repasa este concepto en tu material WSET L3.

**Micro-drill:** no derivado (sin patrón claro) — etapa ENTRENAR se salta para este ítem.

---

## wset3_408 (sq 408) · RA2 · gold=False

**Pregunta:** ¿Qué característica del clima de Alsacia contribuye a la concentración de azúcares en las uvas?
**Correcta (C):** Sol intenso y escasa lluvia
**Nodo:** `HC_ALSACE_SUN_DRY_RIPENING` · score 2 · en stem: clima de alsacia contribuye a la concentracion de azucares · en respuesta correcta: sol intenso y escasa lluvia

- **Causa:** Alsacia recibe abundante insolación y lluvia relativamente escasa por el efecto de sombra pluviométrica de los Vosgos.
- **Mecanismo:** Cuando la vid dispone de agua suficiente, las condiciones soleadas y relativamente secas sostienen la fotosíntesis y una maduración larga y sana, y limitan la dilución causada por lluvia.
- **Efecto:** La uva puede alcanzar alta madurez de azúcares y concentración de sabor; un estrés hídrico severo, en cambio, frenaría la fotosíntesis y la maduración.

**Mentor Guía:** La respuesta correcta es C: «Sol intenso y escasa lluvia». La clave está en el sol, la escasa lluvia y la maduración de azúcares en Alsacia: Cuando la vid dispone de agua suficiente, las condiciones soleadas y relativamente secas sostienen la fotosíntesis y una maduración larga y sana, y limitan la dilución causada por lluvia. Por eso, la uva puede alcanzar alta madurez de azúcares y concentración de sabor; un estrés hídrico severo, en cambio, frenaría la fotosíntesis y la maduración.

**Entrenador Técnico:** Concepto técnico (RA2): Fija el mecanismo del sol, la escasa lluvia y la maduración de azúcares en Alsacia: Alsacia recibe abundante insolación y lluvia relativamente escasa por el efecto de sombra pluviométrica de los Vosgos. → Cuando la vid dispone de agua suficiente, las condiciones soleadas y relativamente secas sostienen la fotosíntesis y una maduración larga y sana, y limitan la dilución causada por lluvia. En el examen, identifica este patrón causa→mecanismo→efecto antes de mirar las opciones.

**Revisor Estricto:** Exigencia de repaso (RA2): debes poder justificar por qué «Sol intenso y escasa lluvia» es correcta y por qué las otras tres opciones no lo son, citando el mecanismo del sol, la escasa lluvia y la maduración de azúcares en Alsacia. Si no puedes reconstruir la cadena completa sin ver las opciones, repasa este concepto en tu material WSET L3.

**Micro-drill:** Consolidación: ¿cuál de estas afirmaciones corresponde al sol, la escasa lluvia y la maduración de azúcares en Alsacia?
  - A. Protege al vino del oxígeno y desarrolla sabores únicos
  - B. Adición de aguardiente vínico
  - C. Sol intenso y escasa lluvia ✅
  - D. Estructura potente y necesidad de guarda
  - _Explicación:_ «Sol intenso y escasa lluvia» corresponde al sol, la escasa lluvia y la maduración de azúcares en Alsacia. Las demás afirmaciones son correctas, pero describen otros mecanismos.

---

## wset3_417 (sq 417) · RA2 · gold=False

**Pregunta:** ¿Qué técnica en la viña es esencial en Sancerre para controlar el vigor?
**Correcta (D):** Manejo del dosel
**Nodo:** `HC_CANOPY_VIGOUR_EXPOSURE` · score 2 · en stem: tecnica en la vina es esencial en sancerre para controlar el vigor · en respuesta correcta: manejo del dosel

- **Causa:** Se gestionan brotes y hojas durante la temporada mediante poda en verde y otras operaciones de dosel.
- **Mecanismo:** Retirar o posicionar crecimiento limita la densidad vegetal y mejora la entrada de luz y la ventilación alrededor de los racimos.
- **Efecto:** Se controla el vigor y se equilibran la exposición de los racimos y sus condiciones de maduración.

**Mentor Guía:** La respuesta correcta es D: «Manejo del dosel». La clave está en el manejo del dosel, el vigor y la exposición de los racimos: Retirar o posicionar crecimiento limita la densidad vegetal y mejora la entrada de luz y la ventilación alrededor de los racimos. Por eso, se controla el vigor y se equilibran la exposición de los racimos y sus condiciones de maduración.

**Entrenador Técnico:** Concepto técnico (RA2): Fija el mecanismo del manejo del dosel, el vigor y la exposición de los racimos: Se gestionan brotes y hojas durante la temporada mediante poda en verde y otras operaciones de dosel. → Retirar o posicionar crecimiento limita la densidad vegetal y mejora la entrada de luz y la ventilación alrededor de los racimos. En el examen, identifica este patrón causa→mecanismo→efecto antes de mirar las opciones.

**Revisor Estricto:** Exigencia de repaso (RA2): debes poder justificar por qué «Manejo del dosel» es correcta y por qué las otras tres opciones no lo son, citando el mecanismo del manejo del dosel, el vigor y la exposición de los racimos. Si no puedes reconstruir la cadena completa sin ver las opciones, repasa este concepto en tu material WSET L3.

**Micro-drill:** no derivado (sin patrón claro) — etapa ENTRENAR se salta para este ítem.

---

## wset3_428 (sq 428) · RA2 · gold=False

**Pregunta:** ¿Qué puede causar una vendimia demasiado temprana?
**Correcta (B):** Aromas herbáceos
**Nodo:** `HC_UNDERRIPE_HARVEST_GREEN_AROMAS` · score 2 · en stem: que puede causar una vendimia demasiado temprana · en respuesta correcta: aromas herbaceos

- **Causa:** Las uvas se cosechan demasiado pronto, antes de alcanzar una madurez aromática y fenólica adecuada.
- **Mecanismo:** Los compuestos verdes y herbáceos siguen siendo prominentes porque la maduración no los ha reducido ni equilibrado con caracteres de fruta madura.
- **Efecto:** El vino puede mostrar aromas herbáceos o inmaduros, acidez más marcada y menor expresión de fruta madura.

**Mentor Guía:** La respuesta correcta es B: «Aromas herbáceos». La clave está en la vendimia antes de la madurez aromática suficiente: Los compuestos verdes y herbáceos siguen siendo prominentes porque la maduración no los ha reducido ni equilibrado con caracteres de fruta madura. Por eso, el vino puede mostrar aromas herbáceos o inmaduros, acidez más marcada y menor expresión de fruta madura.

**Entrenador Técnico:** Concepto técnico (RA2): Fija el mecanismo de la vendimia antes de la madurez aromática suficiente: Las uvas se cosechan demasiado pronto, antes de alcanzar una madurez aromática y fenólica adecuada. → Los compuestos verdes y herbáceos siguen siendo prominentes porque la maduración no los ha reducido ni equilibrado con caracteres de fruta madura. En el examen, identifica este patrón causa→mecanismo→efecto antes de mirar las opciones.

**Revisor Estricto:** Exigencia de repaso (RA2): debes poder justificar por qué «Aromas herbáceos» es correcta y por qué las otras tres opciones no lo son, citando el mecanismo de la vendimia antes de la madurez aromática suficiente. Si no puedes reconstruir la cadena completa sin ver las opciones, repasa este concepto en tu material WSET L3.

**Micro-drill:** no derivado (sin patrón claro) — etapa ENTRENAR se salta para este ítem.

---

## wset3_442 (sq 442) · RA2 · gold=False

**Pregunta:** ¿Qué clima favorece los aromas de pirazina en variedades como Cabernet Sauvignon?
**Correcta (B):** Climas frescos
**Nodo:** `HC_COOL_CLIMATE_STYLE` · score 2 · en stem: clima favorece los aromas de pirazina en variedades como cabernet sauvignon · en respuesta correcta: climas frescos

- **Causa:** En las regiones de clima fresco, las temperaturas medias del periodo de maduración son lo bastante bajas como para que la uva madure despacio, a veces de forma incompleta, en una temporada más corta.
- **Mecanismo:** La maduración lenta y fresca preserva el ácido málico y tartárico de la uva, porque las noches no aceleran lo suficiente la respiración de los ácidos, y la acumulación de azúcar es más limitada.
- **Efecto:** Los vinos de clima fresco suelen presentar acidez alta, menor alcohol, cuerpo más ligero y aromas primarios que tienden a manzana verde, cítricos y notas herbáceas.

**Mentor Guía:** La respuesta correcta es B: «Climas frescos». La clave está en el clima fresco y su estilo de vino: La maduración lenta y fresca preserva el ácido málico y tartárico de la uva, porque las noches no aceleran lo suficiente la respiración de los ácidos, y la acumulación de azúcar es más limitada. Por eso, los vinos de clima fresco suelen presentar acidez alta, menor alcohol, cuerpo más ligero y aromas primarios que tienden a manzana verde, cítricos y notas herbáceas.

**Entrenador Técnico:** Concepto técnico (RA2): Fija el mecanismo del clima fresco y su estilo de vino: En las regiones de clima fresco, las temperaturas medias del periodo de maduración son lo bastante bajas como para que la uva madure despacio, a veces de forma incompleta, en una temporada más corta. → La maduración lenta y fresca preserva el ácido málico y tartárico de la uva, porque las noches no aceleran lo suficiente la respiración de los ácidos, y la acumulación de azúcar es más limitada. En el examen, identifica este patrón causa→mecanismo→efecto antes de mirar las opciones.

**Revisor Estricto:** Exigencia de repaso (RA2): debes poder justificar por qué «Climas frescos» es correcta y por qué las otras tres opciones no lo son, citando el mecanismo del clima fresco y su estilo de vino. Si no puedes reconstruir la cadena completa sin ver las opciones, repasa este concepto en tu material WSET L3.

**Micro-drill:** no derivado (sin patrón claro) — etapa ENTRENAR se salta para este ítem.

---

## wset3_457 (sq 457) · RA2 · gold=False

**Pregunta:** ¿Cuál es el objetivo principal de la vendimia manual selectiva?
**Correcta (C):** Eliminar racimos dañados
**Nodo:** `HC_SELECTIVE_HAND_HARVEST_QUALITY` · score 2 · en stem: vendimia manual selectiva · en respuesta correcta: eliminar racimos danados

- **Causa:** Los vendimiadores inspeccionan y seleccionan los racimos individualmente durante la cosecha.
- **Mecanismo:** Los racimos dañados, enfermos, inmaduros o inadecuados pueden rechazarse antes de entrar en bodega.
- **Efecto:** La bodega recibe una selección de fruta más sana y uniforme, favoreciendo sabores limpios y el nivel de calidad buscado.

**Mentor Guía:** La respuesta correcta es C: «Eliminar racimos dañados». La clave está en la vendimia manual selectiva: Los racimos dañados, enfermos, inmaduros o inadecuados pueden rechazarse antes de entrar en bodega. Por eso, la bodega recibe una selección de fruta más sana y uniforme, favoreciendo sabores limpios y el nivel de calidad buscado.

**Entrenador Técnico:** Concepto técnico (RA2): Fija el mecanismo de la vendimia manual selectiva: Los vendimiadores inspeccionan y seleccionan los racimos individualmente durante la cosecha. → Los racimos dañados, enfermos, inmaduros o inadecuados pueden rechazarse antes de entrar en bodega. En el examen, identifica este patrón causa→mecanismo→efecto antes de mirar las opciones.

**Revisor Estricto:** Exigencia de repaso (RA2): debes poder justificar por qué «Eliminar racimos dañados» es correcta y por qué las otras tres opciones no lo son, citando el mecanismo de la vendimia manual selectiva. Si no puedes reconstruir la cadena completa sin ver las opciones, repasa este concepto en tu material WSET L3.

**Micro-drill:** Consolidación: ¿cuál de estas afirmaciones corresponde a la vendimia manual selectiva?
  - A. Protege al vino del oxígeno y desarrolla sabores únicos
  - B. Eliminar racimos dañados ✅
  - C. Adición de aguardiente vínico
  - D. Estructura potente y necesidad de guarda
  - _Explicación:_ «Eliminar racimos dañados» corresponde a la vendimia manual selectiva. Las demás afirmaciones son correctas, pero describen otros mecanismos.

---

## wset3_459 (sq 459) · RA2 · gold=False

**Pregunta:** ¿Qué efecto tiene la fermentación a baja temperatura?
**Correcta (B):** Aromas delicados
**Nodo:** `HC_COOL_FERMENTATION_AROMA_RETENTION` · score 2 · en stem: fermentacion a baja temperatura · en respuesta correcta: aromas delicados

- **Causa:** Un mosto blanco o aromático fermenta a una temperatura relativamente baja y controlada.
- **Mecanismo:** La temperatura baja ralentiza la actividad de la levadura y reduce la volatilización y transformación rápida de compuestos aromáticos delicados.
- **Efecto:** El vino terminado conserva más aromas frescos y delicados de fruta y flores.

**Mentor Guía:** La respuesta correcta es B: «Aromas delicados». La clave está en la fermentación a baja temperatura y la retención aromática: La temperatura baja ralentiza la actividad de la levadura y reduce la volatilización y transformación rápida de compuestos aromáticos delicados. Por eso, el vino terminado conserva más aromas frescos y delicados de fruta y flores.

**Entrenador Técnico:** Concepto técnico (RA2): Fija el mecanismo de la fermentación a baja temperatura y la retención aromática: Un mosto blanco o aromático fermenta a una temperatura relativamente baja y controlada. → La temperatura baja ralentiza la actividad de la levadura y reduce la volatilización y transformación rápida de compuestos aromáticos delicados. En el examen, identifica este patrón causa→mecanismo→efecto antes de mirar las opciones.

**Revisor Estricto:** Exigencia de repaso (RA2): debes poder justificar por qué «Aromas delicados» es correcta y por qué las otras tres opciones no lo son, citando el mecanismo de la fermentación a baja temperatura y la retención aromática. Si no puedes reconstruir la cadena completa sin ver las opciones, repasa este concepto en tu material WSET L3.

**Micro-drill:** no derivado (sin patrón claro) — etapa ENTRENAR se salta para este ítem.

---

## wset3_467 (sq 467) · RA2 · gold=False

**Pregunta:** ¿Qué resultado produce la maceración carbónica en vinos tintos jóvenes?
**Correcta (B):** Aromas de frutas frescas y poco tanino
**Nodo:** `HC_CARBONIC_MACERATION_FRUIT_LOW_TANNIN` · score 2 · en stem: maceracion carbonica en vinos tintos jovenes · en respuesta correcta: aromas de frutas frescas y poco tanino

- **Causa:** Racimos enteros y bayas intactas permanecen en un depósito rico en dióxido de carbono.
- **Mecanismo:** La fermentación intracelular genera ésteres frutales característicos y la escasa rotura y extracción limita la incorporación de taninos.
- **Efecto:** El tinto joven muestra fruta fresca intensa, poco tanino y una textura accesible.

**Mentor Guía:** La respuesta correcta es B: «Aromas de frutas frescas y poco tanino». La clave está en la maceración carbónica en tintos jóvenes: La fermentación intracelular genera ésteres frutales característicos y la escasa rotura y extracción limita la incorporación de taninos. Por eso, el tinto joven muestra fruta fresca intensa, poco tanino y una textura accesible.

**Entrenador Técnico:** Concepto técnico (RA2): Fija el mecanismo de la maceración carbónica en tintos jóvenes: Racimos enteros y bayas intactas permanecen en un depósito rico en dióxido de carbono. → La fermentación intracelular genera ésteres frutales característicos y la escasa rotura y extracción limita la incorporación de taninos. En el examen, identifica este patrón causa→mecanismo→efecto antes de mirar las opciones.

**Revisor Estricto:** Exigencia de repaso (RA2): debes poder justificar por qué «Aromas de frutas frescas y poco tanino» es correcta y por qué las otras tres opciones no lo son, citando el mecanismo de la maceración carbónica en tintos jóvenes. Si no puedes reconstruir la cadena completa sin ver las opciones, repasa este concepto en tu material WSET L3.

**Micro-drill:** Consolidación: ¿cuál de estas afirmaciones corresponde a la maceración carbónica en tintos jóvenes?
  - A. Protege al vino del oxígeno y desarrolla sabores únicos
  - B. Adición de aguardiente vínico
  - C. Estructura potente y necesidad de guarda
  - D. Aromas de frutas frescas y poco tanino ✅
  - _Explicación:_ «Aromas de frutas frescas y poco tanino» corresponde a la maceración carbónica en tintos jóvenes. Las demás afirmaciones son correctas, pero describen otros mecanismos.

---

## wset3_470 (sq 470) · RA2 · gold=False

**Pregunta:** ¿Qué beneficio aporta el uso de hormigón en fermentadores?
**Correcta (B):** Mantiene temperatura de forma natural
**Nodo:** `HC_CONCRETE_THERMAL_INERTIA` · score 2 · en stem: uso de hormigon en fermentadores · en respuesta correcta: mantiene temperatura de forma natural

- **Causa:** Los recipientes de hormigón tienen paredes gruesas y una masa térmica elevada.
- **Mecanismo:** Esa masa absorbe y libera calor lentamente, amortiguando cambios rápidos de temperatura durante la fermentación.
- **Efecto:** La temperatura puede mantenerse más estable de forma natural, aunque todavía puede requerirse refrigeración activa.

**Mentor Guía:** La respuesta correcta es B: «Mantiene temperatura de forma natural». La clave está en la inercia térmica de los fermentadores de hormigón: Esa masa absorbe y libera calor lentamente, amortiguando cambios rápidos de temperatura durante la fermentación. Por eso, la temperatura puede mantenerse más estable de forma natural, aunque todavía puede requerirse refrigeración activa.

**Entrenador Técnico:** Concepto técnico (RA2): Fija el mecanismo de la inercia térmica de los fermentadores de hormigón: Los recipientes de hormigón tienen paredes gruesas y una masa térmica elevada. → Esa masa absorbe y libera calor lentamente, amortiguando cambios rápidos de temperatura durante la fermentación. En el examen, identifica este patrón causa→mecanismo→efecto antes de mirar las opciones.

**Revisor Estricto:** Exigencia de repaso (RA2): debes poder justificar por qué «Mantiene temperatura de forma natural» es correcta y por qué las otras tres opciones no lo son, citando el mecanismo de la inercia térmica de los fermentadores de hormigón. Si no puedes reconstruir la cadena completa sin ver las opciones, repasa este concepto en tu material WSET L3.

**Micro-drill:** Consolidación: ¿cuál de estas afirmaciones corresponde a la inercia térmica de los fermentadores de hormigón?
  - A. Protege al vino del oxígeno y desarrolla sabores únicos
  - B. Adición de aguardiente vínico
  - C. Estructura potente y necesidad de guarda
  - D. Mantiene temperatura de forma natural ✅
  - _Explicación:_ «Mantiene temperatura de forma natural» corresponde a la inercia térmica de los fermentadores de hormigón. Las demás afirmaciones son correctas, pero describen otros mecanismos.

---

## wset3_489 (sq 489) · RA2 · gold=False

**Pregunta:** ¿Cuál de las siguientes prácticas reduce el riesgo de botrytis en climas húmedos?
**Correcta (C):** Canopy abierto
**Nodo:** `HC_CANOPY_AIRFLOW_FUNGAL_RISK` · score 2 · en stem: reduce el riesgo de botrytis · en respuesta correcta: canopy abierto

- **Causa:** Un follaje denso alrededor de los racimos restringe el flujo de aire y conserva humedad después de la lluvia o el rocío.
- **Mecanismo:** Abrir el dosel mediante posicionamiento de brotes o deshoje mejora la ventilación y acelera el secado de los racimos.
- **Efecto:** Las condiciones son menos favorables para Botrytis y otros hongos; un dosel excesivamente denso aumenta la presión de enfermedad.

**Mentor Guía:** La respuesta correcta es C: «Canopy abierto». La clave está en la ventilación del dosel y el riesgo de enfermedades fúngicas: Abrir el dosel mediante posicionamiento de brotes o deshoje mejora la ventilación y acelera el secado de los racimos. Por eso, las condiciones son menos favorables para Botrytis y otros hongos; un dosel excesivamente denso aumenta la presión de enfermedad.

**Entrenador Técnico:** Concepto técnico (RA2): Fija el mecanismo de la ventilación del dosel y el riesgo de enfermedades fúngicas: Un follaje denso alrededor de los racimos restringe el flujo de aire y conserva humedad después de la lluvia o el rocío. → Abrir el dosel mediante posicionamiento de brotes o deshoje mejora la ventilación y acelera el secado de los racimos. En el examen, identifica este patrón causa→mecanismo→efecto antes de mirar las opciones.

**Revisor Estricto:** Exigencia de repaso (RA2): debes poder justificar por qué «Canopy abierto» es correcta y por qué las otras tres opciones no lo son, citando el mecanismo de la ventilación del dosel y el riesgo de enfermedades fúngicas. Si no puedes reconstruir la cadena completa sin ver las opciones, repasa este concepto en tu material WSET L3.

**Micro-drill:** no derivado (sin patrón claro) — etapa ENTRENAR se salta para este ítem.

---

## wset3_495 (sq 495) · RA2 · gold=False

**Pregunta:** ¿Qué tipo de clima favorece vinos con menor acidez natural?
**Correcta (B):** Clima cálido
**Nodo:** `HC_WARM_CLIMATE_ACID_LOSS` · score 2 · en stem: clima favorece vinos con menor acidez natural · en respuesta correcta: clima calido

- **Causa:** Las uvas maduran bajo temperaturas cálidas de forma sostenida.
- **Mecanismo:** El calor acelera la respiración, especialmente el consumo de ácido málico, a medida que avanza la maduración.
- **Efecto:** La acidez natural de la uva tiende a ser menor que en condiciones comparables más frescas.

**Mentor Guía:** La respuesta correcta es B: «Clima cálido». La clave está en el clima cálido y la pérdida de acidez natural: El calor acelera la respiración, especialmente el consumo de ácido málico, a medida que avanza la maduración. Por eso, la acidez natural de la uva tiende a ser menor que en condiciones comparables más frescas.

**Entrenador Técnico:** Concepto técnico (RA2): Fija el mecanismo del clima cálido y la pérdida de acidez natural: Las uvas maduran bajo temperaturas cálidas de forma sostenida. → El calor acelera la respiración, especialmente el consumo de ácido málico, a medida que avanza la maduración. En el examen, identifica este patrón causa→mecanismo→efecto antes de mirar las opciones.

**Revisor Estricto:** Exigencia de repaso (RA2): debes poder justificar por qué «Clima cálido» es correcta y por qué las otras tres opciones no lo son, citando el mecanismo del clima cálido y la pérdida de acidez natural. Si no puedes reconstruir la cadena completa sin ver las opciones, repasa este concepto en tu material WSET L3.

**Micro-drill:** no derivado (sin patrón claro) — etapa ENTRENAR se salta para este ítem.

---

## wset3_516 (sq 516) · RA2 · gold=False

**Pregunta:** ¿Qué práctica agrícola puede reducir el vigor en un suelo fértil?
**Correcta (C):** Poda severa
**Nodo:** `HC_CANOPY_VIGOUR_EXPOSURE` · score 2 · en stem: reducir el vigor · en respuesta correcta: poda severa

- **Causa:** Se gestionan brotes y hojas durante la temporada mediante poda en verde y otras operaciones de dosel.
- **Mecanismo:** Retirar o posicionar crecimiento limita la densidad vegetal y mejora la entrada de luz y la ventilación alrededor de los racimos.
- **Efecto:** Se controla el vigor y se equilibran la exposición de los racimos y sus condiciones de maduración.

**Mentor Guía:** La respuesta correcta es C: «Poda severa». La clave está en el manejo del dosel, el vigor y la exposición de los racimos: Retirar o posicionar crecimiento limita la densidad vegetal y mejora la entrada de luz y la ventilación alrededor de los racimos. Por eso, se controla el vigor y se equilibran la exposición de los racimos y sus condiciones de maduración.

**Entrenador Técnico:** Concepto técnico (RA2): Fija el mecanismo del manejo del dosel, el vigor y la exposición de los racimos: Se gestionan brotes y hojas durante la temporada mediante poda en verde y otras operaciones de dosel. → Retirar o posicionar crecimiento limita la densidad vegetal y mejora la entrada de luz y la ventilación alrededor de los racimos. En el examen, identifica este patrón causa→mecanismo→efecto antes de mirar las opciones.

**Revisor Estricto:** Exigencia de repaso (RA2): debes poder justificar por qué «Poda severa» es correcta y por qué las otras tres opciones no lo son, citando el mecanismo del manejo del dosel, el vigor y la exposición de los racimos. Si no puedes reconstruir la cadena completa sin ver las opciones, repasa este concepto en tu material WSET L3.

**Micro-drill:** no derivado (sin patrón claro) — etapa ENTRENAR se salta para este ítem.

---

## wset3_518 (sq 518) · RA2 · gold=False

**Pregunta:** ¿Qué factor natural tiende a aumentar la acidez en la uva?
**Correcta (B):** Altitud elevada
**Nodo:** `HC_ALTITUDE_GRAPE_ACIDITY` · score 2 · en stem: factor natural tiende a aumentar la acidez en la uva · en respuesta correcta: altitud elevada

- **Causa:** El viñedo se sitúa a mayor altitud, donde las temperaturas suelen ser más bajas, sobre todo de noche.
- **Mecanismo:** La maduración más fresca ralentiza la respiración y reduce la pérdida de ácidos de la uva.
- **Efecto:** La fruta tiende a conservar más acidez natural que fruta comparable de una cota inferior y más cálida.

**Mentor Guía:** La respuesta correcta es B: «Altitud elevada». La clave está en la altitud y la retención de acidez en la uva: La maduración más fresca ralentiza la respiración y reduce la pérdida de ácidos de la uva. Por eso, la fruta tiende a conservar más acidez natural que fruta comparable de una cota inferior y más cálida.

**Entrenador Técnico:** Concepto técnico (RA2): Fija el mecanismo de la altitud y la retención de acidez en la uva: El viñedo se sitúa a mayor altitud, donde las temperaturas suelen ser más bajas, sobre todo de noche. → La maduración más fresca ralentiza la respiración y reduce la pérdida de ácidos de la uva. En el examen, identifica este patrón causa→mecanismo→efecto antes de mirar las opciones.

**Revisor Estricto:** Exigencia de repaso (RA2): debes poder justificar por qué «Altitud elevada» es correcta y por qué las otras tres opciones no lo son, citando el mecanismo de la altitud y la retención de acidez en la uva. Si no puedes reconstruir la cadena completa sin ver las opciones, repasa este concepto en tu material WSET L3.

**Micro-drill:** no derivado (sin patrón claro) — etapa ENTRENAR se salta para este ítem.

---

## wset3_668 (sq 668) · RA2 · gold=False

**Pregunta:** ¿Cuál de las siguientes afirmaciones sobre la influencia de la altitud en Mendoza es CORRECTA?
**Correcta (A):** La altitud contribuye a preservar la acidez natural en los vinos de Mendoza.
**Nodo:** `HC_ALTITUDE_GRAPE_ACIDITY` · score 2 · en stem: afirmaciones sobre la influencia de la altitud en mendoza · en respuesta correcta: altitud contribuye a preservar la acidez natural en los vinos de mendoza

- **Causa:** El viñedo se sitúa a mayor altitud, donde las temperaturas suelen ser más bajas, sobre todo de noche.
- **Mecanismo:** La maduración más fresca ralentiza la respiración y reduce la pérdida de ácidos de la uva.
- **Efecto:** La fruta tiende a conservar más acidez natural que fruta comparable de una cota inferior y más cálida.

**Mentor Guía:** La respuesta correcta es A: «La altitud contribuye a preservar la acidez natural en los vinos de Mendoza.». La clave está en la altitud y la retención de acidez en la uva: La maduración más fresca ralentiza la respiración y reduce la pérdida de ácidos de la uva. Por eso, la fruta tiende a conservar más acidez natural que fruta comparable de una cota inferior y más cálida.

**Entrenador Técnico:** Concepto técnico (RA2): Fija el mecanismo de la altitud y la retención de acidez en la uva: El viñedo se sitúa a mayor altitud, donde las temperaturas suelen ser más bajas, sobre todo de noche. → La maduración más fresca ralentiza la respiración y reduce la pérdida de ácidos de la uva. En el examen, identifica este patrón causa→mecanismo→efecto antes de mirar las opciones.

**Revisor Estricto:** Exigencia de repaso (RA2): debes poder justificar por qué «La altitud contribuye a preservar la acidez natural en los vinos de Mendoza.» es correcta y por qué las otras tres opciones no lo son, citando el mecanismo de la altitud y la retención de acidez en la uva. Si no puedes reconstruir la cadena completa sin ver las opciones, repasa este concepto en tu material WSET L3.

**Micro-drill:** Consolidación: ¿cuál de estas afirmaciones corresponde a la altitud y la retención de acidez en la uva?
  - A. Protege al vino del oxígeno y desarrolla sabores únicos
  - B. Adición de aguardiente vínico
  - C. Estructura potente y necesidad de guarda
  - D. La altitud contribuye a preservar la acidez natural en los vinos de Mendoza. ✅
  - _Explicación:_ «La altitud contribuye a preservar la acidez natural en los vinos de Mendoza.» corresponde a la altitud y la retención de acidez en la uva. Las demás afirmaciones son correctas, pero describen otros mecanismos.

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
  - A. Protege al vino del oxígeno y desarrolla sabores únicos
  - B. Adición de aguardiente vínico
  - C. Sistema de soleras y criaderas ✅
  - D. Estructura potente y necesidad de guarda
  - _Explicación:_ «Sistema de soleras y criaderas» corresponde al sistema de solera y criaderas. Las demás afirmaciones son correctas, pero describen otros mecanismos.

---

## wset3_12 (sq 12) · RA1 · gold=False

**Pregunta:** ¿Qué factor natural tiene mayor influencia en el riesgo de heladas primaverales?
**Correcta (C):** Pendiente del terreno
**Nodo:** `HC_FROST_SLOPE_AIR_DRAINAGE` · score 6 · en stem: factor natural, riesgo de heladas primaverales · en respuesta correcta: pendiente del terreno

- **Causa:** En noches despejadas de primavera se forma aire frío que desciende por ser más denso que el aire cálido.
- **Mecanismo:** Las laderas permiten que el aire frío se aleje, mientras los valles y depresiones lo acumulan alrededor de las vides.
- **Efecto:** La pendiente y la topografía condicionan mucho la exposición: las laderas con buen drenaje de aire suelen sufrir menos que las zonas bajas.

**Mentor Guía:** La respuesta correcta es C: «Pendiente del terreno». La clave está en la pendiente, el drenaje de aire frío y el riesgo de helada: Las laderas permiten que el aire frío se aleje, mientras los valles y depresiones lo acumulan alrededor de las vides. Por eso, la pendiente y la topografía condicionan mucho la exposición: las laderas con buen drenaje de aire suelen sufrir menos que las zonas bajas.

**Entrenador Técnico:** Concepto técnico (RA1): Tema: viticulture. Fija el mecanismo de la pendiente, el drenaje de aire frío y el riesgo de helada: En noches despejadas de primavera se forma aire frío que desciende por ser más denso que el aire cálido. → Las laderas permiten que el aire frío se aleje, mientras los valles y depresiones lo acumulan alrededor de las vides. En el examen, identifica este patrón causa→mecanismo→efecto antes de mirar las opciones.

**Revisor Estricto:** Exigencia de repaso (RA1): debes poder justificar por qué «Pendiente del terreno» es correcta y por qué las otras tres opciones no lo son, citando el mecanismo de la pendiente, el drenaje de aire frío y el riesgo de helada. Si no puedes reconstruir la cadena completa sin ver las opciones, repasa este concepto en tu material WSET L3.

**Micro-drill:** Consolidación: ¿cuál de estas afirmaciones corresponde a la pendiente, el drenaje de aire frío y el riesgo de helada?
  - A. Protege al vino del oxígeno y desarrolla sabores únicos
  - B. Adición de aguardiente vínico
  - C. Pendiente del terreno ✅
  - D. Estructura potente y necesidad de guarda
  - _Explicación:_ «Pendiente del terreno» corresponde a la pendiente, el drenaje de aire frío y el riesgo de helada. Las demás afirmaciones son correctas, pero describen otros mecanismos.

---

## wset3_13 (sq 13) · RA1 · gold=False

**Pregunta:** ¿Qué elemento del suelo influye más directamente en el drenaje del viñedo?
**Correcta (C):** Estructura arenosa
**Nodo:** `HC_SANDY_SOIL_DRAINAGE` · score 6 · en stem: drenaje, elemento del suelo influye mas directamente en el drenaje del vinedo · en respuesta correcta: estructura arenosa

- **Causa:** El suelo del viñedo contiene una proporción elevada de partículas de arena relativamente grandes.
- **Mecanismo:** Los poros mayores entre partículas permiten que el agua atraviese el suelo con más rapidez que en una estructura arcillosa fina y compacta.
- **Efecto:** La estructura arenosa favorece el drenaje libre y reduce la retención de agua, condicionando la disponibilidad hídrica de las raíces y el vigor.

**Mentor Guía:** La respuesta correcta es C: «Estructura arenosa». La clave está en la estructura arenosa del suelo y el drenaje: Los poros mayores entre partículas permiten que el agua atraviese el suelo con más rapidez que en una estructura arcillosa fina y compacta. Por eso, la estructura arenosa favorece el drenaje libre y reduce la retención de agua, condicionando la disponibilidad hídrica de las raíces y el vigor.

**Entrenador Técnico:** Concepto técnico (RA1): Tema: viticulture. Fija el mecanismo de la estructura arenosa del suelo y el drenaje: El suelo del viñedo contiene una proporción elevada de partículas de arena relativamente grandes. → Los poros mayores entre partículas permiten que el agua atraviese el suelo con más rapidez que en una estructura arcillosa fina y compacta. En el examen, identifica este patrón causa→mecanismo→efecto antes de mirar las opciones.

**Revisor Estricto:** Exigencia de repaso (RA1): debes poder justificar por qué «Estructura arenosa» es correcta y por qué las otras tres opciones no lo son, citando el mecanismo de la estructura arenosa del suelo y el drenaje. Si no puedes reconstruir la cadena completa sin ver las opciones, repasa este concepto en tu material WSET L3.

**Micro-drill:** no derivado (sin patrón claro) — etapa ENTRENAR se salta para este ítem.

---

## wset3_3 (sq 3) · unknown · gold=False

**Pregunta:** ¿Cuál es una característica clave de los vinos de Porto Vintage?
**Correcta (C):** Estructura potente y necesidad de guarda
**Nodo:** `HC_RED_WINE_AGEABILITY_STRUCTURE` · score 5 · en stem: porto vintage, vinos de porto vintage · en respuesta correcta: estructura potente, estructura potente y necesidad de guarda, necesidad de guarda

- **Causa:** Un tinto concentrado parte de taninos, acidez y fruta abundantes y, en estilos fortificados, también de alcohol y azúcar.
- **Mecanismo:** La acidez y otros componentes estables ralentizan el deterioro, mientras los taninos se polimerizan y el perfil concentrado evoluciona con el tiempo.
- **Efecto:** El vino tiene capacidad estructural para una guarda prolongada, durante la cual los taninos pueden integrarse y surgir complejidad terciaria; esa estructura permite la evolución, pero no garantiza mejora si el almacenamiento es deficiente.

**Mentor Guía:** La respuesta correcta es C: «Estructura potente y necesidad de guarda». La clave está en la estructura que permite la guarda prolongada de un vino tinto: La acidez y otros componentes estables ralentizan el deterioro, mientras los taninos se polimerizan y el perfil concentrado evoluciona con el tiempo. Por eso, el vino tiene capacidad estructural para una guarda prolongada, durante la cual los taninos pueden integrarse y surgir complejidad terciaria; esa estructura permite la evolución, pero no garantiza mejora si el almacenamiento es deficiente.

**Entrenador Técnico:** Concepto técnico (unknown): Tema: vintage port. Fija el mecanismo de la estructura que permite la guarda prolongada de un vino tinto: Un tinto concentrado parte de taninos, acidez y fruta abundantes y, en estilos fortificados, también de alcohol y azúcar. → La acidez y otros componentes estables ralentizan el deterioro, mientras los taninos se polimerizan y el perfil concentrado evoluciona con el tiempo. En el examen, identifica este patrón causa→mecanismo→efecto antes de mirar las opciones.

**Revisor Estricto:** Exigencia de repaso (unknown): debes poder justificar por qué «Estructura potente y necesidad de guarda» es correcta y por qué las otras tres opciones no lo son, citando el mecanismo de la estructura que permite la guarda prolongada de un vino tinto. Si no puedes reconstruir la cadena completa sin ver las opciones, repasa este concepto en tu material WSET L3.

**Micro-drill:** Consolidación: ¿cuál de estas afirmaciones corresponde a la estructura que permite la guarda prolongada de un vino tinto?
  - A. Estructura potente y necesidad de guarda ✅
  - B. Protege al vino del oxígeno y desarrolla sabores únicos
  - C. Adición de aguardiente vínico
  - D. Sistema de soleras y criaderas
  - _Explicación:_ «Estructura potente y necesidad de guarda» corresponde a la estructura que permite la guarda prolongada de un vino tinto. Las demás afirmaciones son correctas, pero describen otros mecanismos.

---

## wset3_30 (sq 30) · RA3 · gold=False

**Pregunta:** ¿Qué característica es más probable encontrar en un espumoso elaborado con método tradicional y envejecido durante más de 24 meses?
**Correcta (C):** Notas de autólisis como pan y brioche
**Nodo:** `HC_SPARKLING_AUTOLYTIC_AROMAS` · score 5 · en stem: mas de 24 meses · en respuesta correcta: autolisis, brioche, notas de autolisis, pan y brioche

- **Causa:** Un vino espumoso de método tradicional permanece durante un periodo prolongado sobre las lías de la segunda fermentación.
- **Mecanismo:** Las células de levadura muertas sufren autólisis y liberan aminoácidos, péptidos, manoproteínas y otros compuestos que evolucionan con el tiempo.
- **Efecto:** El vino desarrolla complejidad autolítica con aromas de pan, galleta, tostado, brioche y pastelería.

**Mentor Guía:** La respuesta correcta es C: «Notas de autólisis como pan y brioche». La clave está en la autólisis durante la crianza sobre lías de un espumoso: Las células de levadura muertas sufren autólisis y liberan aminoácidos, péptidos, manoproteínas y otros compuestos que evolucionan con el tiempo. Por eso, el vino desarrolla complejidad autolítica con aromas de pan, galleta, tostado, brioche y pastelería.

**Entrenador Técnico:** Concepto técnico (RA3): Tema: sparkling wines. Fija el mecanismo de la autólisis durante la crianza sobre lías de un espumoso: Un vino espumoso de método tradicional permanece durante un periodo prolongado sobre las lías de la segunda fermentación. → Las células de levadura muertas sufren autólisis y liberan aminoácidos, péptidos, manoproteínas y otros compuestos que evolucionan con el tiempo. En el examen, identifica este patrón causa→mecanismo→efecto antes de mirar las opciones.

**Revisor Estricto:** Exigencia de repaso (RA3): debes poder justificar por qué «Notas de autólisis como pan y brioche» es correcta y por qué las otras tres opciones no lo son, citando el mecanismo de la autólisis durante la crianza sobre lías de un espumoso. Si no puedes reconstruir la cadena completa sin ver las opciones, repasa este concepto en tu material WSET L3.

**Micro-drill:** Consolidación: ¿cuál de estas afirmaciones corresponde a la autólisis durante la crianza sobre lías de un espumoso?
  - A. Protege al vino del oxígeno y desarrolla sabores únicos
  - B. Adición de aguardiente vínico
  - C. Notas de autólisis como pan y brioche ✅
  - D. Estructura potente y necesidad de guarda
  - _Explicación:_ «Notas de autólisis como pan y brioche» corresponde a la autólisis durante la crianza sobre lías de un espumoso. Las demás afirmaciones son correctas, pero describen otros mecanismos.

---

## wset3_1 (sq 1) · RA4 · gold=False

**Pregunta:** ¿Qué rol juega la 'flor' en la crianza biológica del Jerez?
**Correcta (C):** Protege al vino del oxígeno y desarrolla sabores únicos
**Nodo:** `CC_FLOR_BIOLOGICAL_AGEING` · score 4 · en stem: crianza biologica, flor, jerez · en respuesta correcta: protege al vino del oxigeno y desarrolla sabores unicos

- **Causa:** La levadura de flor (un velo de cepas de Saccharomyces cerevisiae) se forma en la superficie del vino en botas parcialmente llenas.
- **Mecanismo:** El velo protege al vino del oxígeno; la levadura metaboliza etanol y glicerol produciendo acetaldehído, y su autólisis aporta aminoácidos.
- **Efecto:** El vino desarrolla carácter de crianza biológica: notas de almendra, masa de pan y levadura, color pálido, tanino bajo y protección frente a la oxidación pese a la crianza en bota.

**Mentor Guía:** La respuesta correcta es C: «Protege al vino del oxígeno y desarrolla sabores únicos». La clave está en la crianza biológica bajo velo de flor: El velo protege al vino del oxígeno; la levadura metaboliza etanol y glicerol produciendo acetaldehído, y su autólisis aporta aminoácidos. Por eso, el vino desarrolla carácter de crianza biológica: notas de almendra, masa de pan y levadura, color pálido, tanino bajo y protección frente a la oxidación pese a la crianza en bota.

**Entrenador Técnico:** Concepto técnico (RA4): Tema: fortified wines. Fija el mecanismo de la crianza biológica bajo velo de flor: La levadura de flor (un velo de cepas de Saccharomyces cerevisiae) se forma en la superficie del vino en botas parcialmente llenas. → El velo protege al vino del oxígeno; la levadura metaboliza etanol y glicerol produciendo acetaldehído, y su autólisis aporta aminoácidos. En el examen, identifica este patrón causa→mecanismo→efecto antes de mirar las opciones.

**Revisor Estricto:** Exigencia de repaso (RA4): debes poder justificar por qué «Protege al vino del oxígeno y desarrolla sabores únicos» es correcta y por qué las otras tres opciones no lo son, citando el mecanismo de la crianza biológica bajo velo de flor. Si no puedes reconstruir la cadena completa sin ver las opciones, repasa este concepto en tu material WSET L3.

**Micro-drill:** Consolidación: ¿cuál de estas afirmaciones corresponde a la crianza biológica bajo velo de flor?
  - A. Protege al vino del oxígeno y desarrolla sabores únicos ✅
  - B. Adición de aguardiente vínico
  - C. Estructura potente y necesidad de guarda
  - D. Sistema de soleras y criaderas
  - _Explicación:_ «Protege al vino del oxígeno y desarrolla sabores únicos» corresponde a la crianza biológica bajo velo de flor. Las demás afirmaciones son correctas, pero describen otros mecanismos.

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
  - A. Protege al vino del oxígeno y desarrolla sabores únicos
  - B. Evitar la extracción de taninos verdes ✅
  - C. Adición de aguardiente vínico
  - D. Estructura potente y necesidad de guarda
  - _Explicación:_ «Evitar la extracción de taninos verdes» corresponde al despalillado antes de la fermentación. Las demás afirmaciones son correctas, pero describen otros mecanismos.

---

## wset3_81 (sq 81) · RA1 · gold=False

**Pregunta:** ¿Cuál es una consecuencia probable de almacenar vino a temperaturas muy altas durante periodos prolongados?
**Correcta (B):** Evolución prematura y pérdida de frescura
**Nodo:** `HC_HEAT_PREMATURE_BOTTLE_AGEING` · score 4 · en stem: periodos prolongados, temperaturas muy altas · en respuesta correcta: evolucion prematura, perdida de frescura

- **Causa:** El vino embotellado queda expuesto a temperaturas excesivas durante un periodo prolongado.
- **Mecanismo:** El calor acelera la oxidación y otras reacciones químicas y también puede aumentar la expansión y la presión dentro de la botella.
- **Efecto:** El vino evoluciona prematuramente, pierde fruta fresca y puede desarrollar sabores cocidos u oxidados.

**Mentor Guía:** La respuesta correcta es B: «Evolución prematura y pérdida de frescura». La clave está en el efecto del calor excesivo sobre el vino embotellado: El calor acelera la oxidación y otras reacciones químicas y también puede aumentar la expansión y la presión dentro de la botella. Por eso, el vino evoluciona prematuramente, pierde fruta fresca y puede desarrollar sabores cocidos u oxidados.

**Entrenador Técnico:** Concepto técnico (RA1): Fija el mecanismo del efecto del calor excesivo sobre el vino embotellado: El vino embotellado queda expuesto a temperaturas excesivas durante un periodo prolongado. → El calor acelera la oxidación y otras reacciones químicas y también puede aumentar la expansión y la presión dentro de la botella. En el examen, identifica este patrón causa→mecanismo→efecto antes de mirar las opciones.

**Revisor Estricto:** Exigencia de repaso (RA1): debes poder justificar por qué «Evolución prematura y pérdida de frescura» es correcta y por qué las otras tres opciones no lo son, citando el mecanismo del efecto del calor excesivo sobre el vino embotellado. Si no puedes reconstruir la cadena completa sin ver las opciones, repasa este concepto en tu material WSET L3.

**Micro-drill:** Consolidación: ¿cuál de estas afirmaciones corresponde al efecto del calor excesivo sobre el vino embotellado?
  - A. Protege al vino del oxígeno y desarrolla sabores únicos
  - B. Adición de aguardiente vínico
  - C. Evolución prematura y pérdida de frescura ✅
  - D. Estructura potente y necesidad de guarda
  - _Explicación:_ «Evolución prematura y pérdida de frescura» corresponde al efecto del calor excesivo sobre el vino embotellado. Las demás afirmaciones son correctas, pero describen otros mecanismos.

---

## wset3_128 (sq 128) · RA3 · gold=False

**Pregunta:** ¿Qué impacto tiene un periodo largo de crianza sobre lías en un vino espumoso?
**Correcta (C):** Aporta complejidad, textura cremosa y notas de levadura
**Nodo:** `HC_SPARKLING_LEES_TEXTURE` · score 4 · en stem: crianza sobre lias en un vino espumoso, periodo largo de crianza sobre lias · en respuesta correcta: notas de levadura, textura cremosa

- **Causa:** Un espumoso de método tradicional pasa un periodo prolongado en contacto con las lías de la segunda fermentación.
- **Mecanismo:** La autólisis libera manoproteínas y polisacáridos que aumentan el peso en boca y ayudan a estabilizar las burbujas de CO₂; otros compuestos de levadura aportan aroma.
- **Efecto:** El espumoso gana textura cremosa, una espuma más fina y persistente y mayor complejidad con notas derivadas de la levadura.

**Mentor Guía:** La respuesta correcta es C: «Aporta complejidad, textura cremosa y notas de levadura». La clave está en la crianza prolongada sobre lías en vinos espumosos: La autólisis libera manoproteínas y polisacáridos que aumentan el peso en boca y ayudan a estabilizar las burbujas de CO₂; otros compuestos de levadura aportan aroma. Por eso, el espumoso gana textura cremosa, una espuma más fina y persistente y mayor complejidad con notas derivadas de la levadura.

**Entrenador Técnico:** Concepto técnico (RA3): Fija el mecanismo de la crianza prolongada sobre lías en vinos espumosos: Un espumoso de método tradicional pasa un periodo prolongado en contacto con las lías de la segunda fermentación. → La autólisis libera manoproteínas y polisacáridos que aumentan el peso en boca y ayudan a estabilizar las burbujas de CO₂; otros compuestos de levadura aportan aroma. En el examen, identifica este patrón causa→mecanismo→efecto antes de mirar las opciones.

**Revisor Estricto:** Exigencia de repaso (RA3): debes poder justificar por qué «Aporta complejidad, textura cremosa y notas de levadura» es correcta y por qué las otras tres opciones no lo son, citando el mecanismo de la crianza prolongada sobre lías en vinos espumosos. Si no puedes reconstruir la cadena completa sin ver las opciones, repasa este concepto en tu material WSET L3.

**Micro-drill:** Consolidación: ¿cuál de estas afirmaciones corresponde a la crianza prolongada sobre lías en vinos espumosos?
  - A. Protege al vino del oxígeno y desarrolla sabores únicos
  - B. Adición de aguardiente vínico
  - C. Estructura potente y necesidad de guarda
  - D. Aporta complejidad, textura cremosa y notas de levadura ✅
  - _Explicación:_ «Aporta complejidad, textura cremosa y notas de levadura» corresponde a la crianza prolongada sobre lías en vinos espumosos. Las demás afirmaciones son correctas, pero describen otros mecanismos.

---

## wset3_201 (sq 201) · RA3 · gold=False

**Pregunta:** ¿Qué proceso implica girar lentamente las botellas para que los sedimentos se acumulen en el cuello?
**Correcta (B):** Removido (remuage)
**Nodo:** `HC_RIDDLING_SEDIMENT_COLLECTION` · score 4 · en stem: girar lentamente las botellas, sedimentos se acumulen en el cuello · en respuesta correcta: removido, remuage

- **Causa:** Tras la segunda fermentación y la crianza, el sedimento de lías queda distribuido por el lateral de la botella.
- **Mecanismo:** El removido gira e inclina gradualmente la botella desde la posición horizontal hasta una posición vertical invertida.
- **Efecto:** El sedimento se desliza hasta el cuello, donde puede eliminarse de forma eficaz durante el degüelle.

**Mentor Guía:** La respuesta correcta es B: «Removido (remuage)». La clave está en el removido y la acumulación del sedimento en el cuello: El removido gira e inclina gradualmente la botella desde la posición horizontal hasta una posición vertical invertida. Por eso, el sedimento se desliza hasta el cuello, donde puede eliminarse de forma eficaz durante el degüelle.

**Entrenador Técnico:** Concepto técnico (RA3): Fija el mecanismo del removido y la acumulación del sedimento en el cuello: Tras la segunda fermentación y la crianza, el sedimento de lías queda distribuido por el lateral de la botella. → El removido gira e inclina gradualmente la botella desde la posición horizontal hasta una posición vertical invertida. En el examen, identifica este patrón causa→mecanismo→efecto antes de mirar las opciones.

**Revisor Estricto:** Exigencia de repaso (RA3): debes poder justificar por qué «Removido (remuage)» es correcta y por qué las otras tres opciones no lo son, citando el mecanismo del removido y la acumulación del sedimento en el cuello. Si no puedes reconstruir la cadena completa sin ver las opciones, repasa este concepto en tu material WSET L3.

**Micro-drill:** no derivado (sin patrón claro) — etapa ENTRENAR se salta para este ítem.

---

## wset3_480 (sq 480) · RA1 · gold=False

**Pregunta:** ¿Qué efecto tiene la fermentación a temperaturas más altas en vinos tintos?
**Correcta (B):** Favorece la extracción de taninos y color
**Nodo:** `HC_RED_FERMENTATION_EXTRACTION` · score 4 · en stem: fermentacion a temperaturas mas altas, temperaturas mas altas en vinos tintos · en respuesta correcta: favorece la extraccion de taninos y color, taninos y color

- **Causa:** El mosto tinto fermenta con los hollejos mientras se gestiona el sombrero y la temperatura es suficientemente cálida.
- **Mecanismo:** El remontado renueva el contacto entre líquido y hollejos; el calor y el alcohol creciente favorecen la extracción de compuestos fenólicos.
- **Efecto:** Pasan al vino más color y tanino, aumentando su profundidad y estructura.

**Mentor Guía:** La respuesta correcta es B: «Favorece la extracción de taninos y color». La clave está en la extracción durante la fermentación de tintos: El remontado renueva el contacto entre líquido y hollejos; el calor y el alcohol creciente favorecen la extracción de compuestos fenólicos. Por eso, pasan al vino más color y tanino, aumentando su profundidad y estructura.

**Entrenador Técnico:** Concepto técnico (RA1): Fija el mecanismo de la extracción durante la fermentación de tintos: El mosto tinto fermenta con los hollejos mientras se gestiona el sombrero y la temperatura es suficientemente cálida. → El remontado renueva el contacto entre líquido y hollejos; el calor y el alcohol creciente favorecen la extracción de compuestos fenólicos. En el examen, identifica este patrón causa→mecanismo→efecto antes de mirar las opciones.

**Revisor Estricto:** Exigencia de repaso (RA1): debes poder justificar por qué «Favorece la extracción de taninos y color» es correcta y por qué las otras tres opciones no lo son, citando el mecanismo de la extracción durante la fermentación de tintos. Si no puedes reconstruir la cadena completa sin ver las opciones, repasa este concepto en tu material WSET L3.

**Micro-drill:** Consolidación: ¿cuál de estas afirmaciones corresponde a la extracción durante la fermentación de tintos?
  - A. Protege al vino del oxígeno y desarrolla sabores únicos
  - B. Adición de aguardiente vínico
  - C. Favorece la extracción de taninos y color ✅
  - D. Estructura potente y necesidad de guarda
  - _Explicación:_ «Favorece la extracción de taninos y color» corresponde a la extracción durante la fermentación de tintos. Las demás afirmaciones son correctas, pero describen otros mecanismos.

---

## wset3_504 (sq 504) · RA1 · gold=False

**Pregunta:** ¿Cuál es un riesgo de plantar en zonas con alto índice de lluvias durante la floración?
**Correcta (C):** Pobre cuajado
**Nodo:** `HC_FLOWERING_RAIN_FRUIT_SET` · score 4 · en stem: alto indice de lluvias durante la floracion, lluvias durante la floracion · en respuesta correcta: cuajado, pobre cuajado

- **Causa:** La lluvia y un tiempo fresco e inestable coinciden con la floración de la vid.
- **Mecanismo:** La humedad interfiere con la polinización y la fecundación y puede hacer que las flores fallen o se desprendan.
- **Efecto:** El cuajado es pobre, se forman menos bayas y disminuye el rendimiento potencial.

**Mentor Guía:** La respuesta correcta es C: «Pobre cuajado». La clave está en la lluvia durante la floración y el cuajado: La humedad interfiere con la polinización y la fecundación y puede hacer que las flores fallen o se desprendan. Por eso, el cuajado es pobre, se forman menos bayas y disminuye el rendimiento potencial.

**Entrenador Técnico:** Concepto técnico (RA1): Fija el mecanismo de la lluvia durante la floración y el cuajado: La lluvia y un tiempo fresco e inestable coinciden con la floración de la vid. → La humedad interfiere con la polinización y la fecundación y puede hacer que las flores fallen o se desprendan. En el examen, identifica este patrón causa→mecanismo→efecto antes de mirar las opciones.

**Revisor Estricto:** Exigencia de repaso (RA1): debes poder justificar por qué «Pobre cuajado» es correcta y por qué las otras tres opciones no lo son, citando el mecanismo de la lluvia durante la floración y el cuajado. Si no puedes reconstruir la cadena completa sin ver las opciones, repasa este concepto en tu material WSET L3.

**Micro-drill:** no derivado (sin patrón claro) — etapa ENTRENAR se salta para este ítem.

---

## wset3_672 (sq 672) · RA1 · gold=False

**Pregunta:** ¿Cuál de las siguientes afirmaciones sobre el control de la filoxera es CORRECTA?
**Correcta (A):** Injertar la vid en portainjertos resistentes es el método principal para combatir la filoxera.
**Nodo:** `HC_PHYLLOXERA_RESISTANT_ROOTSTOCK` · score 4 · en stem: control de la filoxera · en respuesta correcta: injertar la vid, metodo principal para combatir la filoxera, portainjertos resistentes

- **Causa:** La filoxera ataca y daña las raíces de las vides Vitis vinifera susceptibles.
- **Mecanismo:** La variedad vinífera deseada se injerta sobre un portainjerto de vid americana resistente que tolera o limita el daño radicular del insecto.
- **Efecto:** La parte aérea produce la uva prevista mientras las raíces resistentes aportan la principal defensa duradera frente a la filoxera.

**Mentor Guía:** La respuesta correcta es A: «Injertar la vid en portainjertos resistentes es el método principal para combatir la filoxera.». La clave está en el control de la filoxera mediante portainjertos resistentes: La variedad vinífera deseada se injerta sobre un portainjerto de vid americana resistente que tolera o limita el daño radicular del insecto. Por eso, la parte aérea produce la uva prevista mientras las raíces resistentes aportan la principal defensa duradera frente a la filoxera.

**Entrenador Técnico:** Concepto técnico (RA1): Fija el mecanismo del control de la filoxera mediante portainjertos resistentes: La filoxera ataca y daña las raíces de las vides Vitis vinifera susceptibles. → La variedad vinífera deseada se injerta sobre un portainjerto de vid americana resistente que tolera o limita el daño radicular del insecto. En el examen, identifica este patrón causa→mecanismo→efecto antes de mirar las opciones.

**Revisor Estricto:** Exigencia de repaso (RA1): debes poder justificar por qué «Injertar la vid en portainjertos resistentes es el método principal para combatir la filoxera.» es correcta y por qué las otras tres opciones no lo son, citando el mecanismo del control de la filoxera mediante portainjertos resistentes. Si no puedes reconstruir la cadena completa sin ver las opciones, repasa este concepto en tu material WSET L3.

**Micro-drill:** Consolidación: ¿cuál de estas afirmaciones corresponde al control de la filoxera mediante portainjertos resistentes?
  - A. Injertar la vid en portainjertos resistentes es el método principal para combatir la filoxera. ✅
  - B. Protege al vino del oxígeno y desarrolla sabores únicos
  - C. Adición de aguardiente vínico
  - D. Estructura potente y necesidad de guarda
  - _Explicación:_ «Injertar la vid en portainjertos resistentes es el método principal para combatir la filoxera.» corresponde al control de la filoxera mediante portainjertos resistentes. Las demás afirmaciones son correctas, pero describen otros mecanismos.

---

## wset3_679 (sq 679) · RA1 · gold=False

**Pregunta:** ¿Cuál de las siguientes afirmaciones sobre la selección clonal es CORRECTA?
**Correcta (A):** La selección clonal permite elegir plantas con características específicas para influir en el estilo del vino.
**Nodo:** `HC_CLONAL_SELECTION_STYLE_INFLUENCE` · score 4 · en stem: afirmaciones sobre la seleccion clonal, seleccion clonal · en respuesta correcta: influir en el estilo del vino, seleccion clonal, seleccion clonal permite elegir plantas con caracteristicas especificas

- **Causa:** El viticultor propaga un clon de vid seleccionado por características heredables concretas.
- **Mecanismo:** La propagación vegetativa conserva los rasgos genéticos del clon, que pueden influir en el rendimiento, el tamaño de racimos o bayas, el momento de maduración, la susceptibilidad a enfermedades y la composición de la uva.
- **Efecto:** Elegir clones adecuados puede orientar la composición de la uva y, por tanto, el estilo del vino, aunque el sitio, la añada, la viticultura y la vinificación siguen siendo determinantes.

**Mentor Guía:** La respuesta correcta es A: «La selección clonal permite elegir plantas con características específicas para influir en el estilo del vino.». La clave está en la selección clonal y su influencia en el estilo: La propagación vegetativa conserva los rasgos genéticos del clon, que pueden influir en el rendimiento, el tamaño de racimos o bayas, el momento de maduración, la susceptibilidad a enfermedades y la composición de la uva. Por eso, elegir clones adecuados puede orientar la composición de la uva y, por tanto, el estilo del vino, aunque el sitio, la añada, la viticultura y la vinificación siguen siendo determinantes.

**Entrenador Técnico:** Concepto técnico (RA1): Fija el mecanismo de la selección clonal y su influencia en el estilo: El viticultor propaga un clon de vid seleccionado por características heredables concretas. → La propagación vegetativa conserva los rasgos genéticos del clon, que pueden influir en el rendimiento, el tamaño de racimos o bayas, el momento de maduración, la susceptibilidad a enfermedades y la composición de la uva. En el examen, identifica este patrón causa→mecanismo→efecto antes de mirar las opciones.

**Revisor Estricto:** Exigencia de repaso (RA1): debes poder justificar por qué «La selección clonal permite elegir plantas con características específicas para influir en el estilo del vino.» es correcta y por qué las otras tres opciones no lo son, citando el mecanismo de la selección clonal y su influencia en el estilo. Si no puedes reconstruir la cadena completa sin ver las opciones, repasa este concepto en tu material WSET L3.

**Micro-drill:** Consolidación: ¿cuál de estas afirmaciones corresponde a la selección clonal y su influencia en el estilo?
  - A. Protege al vino del oxígeno y desarrolla sabores únicos
  - B. Adición de aguardiente vínico
  - C. Estructura potente y necesidad de guarda
  - D. La selección clonal permite elegir plantas con características específicas para influir en el estilo del vino. ✅
  - _Explicación:_ «La selección clonal permite elegir plantas con características específicas para influir en el estilo del vino.» corresponde a la selección clonal y su influencia en el estilo. Las demás afirmaciones son correctas, pero describen otros mecanismos.

---

## wset3_703 (sq 703) · RA1 · gold=False

**Pregunta:** ¿Cuál de las siguientes afirmaciones sobre el batonnage en vinos blancos es CORRECTA?
**Correcta (A):** El batonnage puede aumentar la complejidad aromática y aportar textura al vino blanco.
**Nodo:** `HC_BATONNAGE_TEXTURE_COMPLEXITY` · score 4 · en stem: batonnage · en respuesta correcta: aportar textura, aumentar la complejidad, batonnage, complejidad aromatica

- **Causa:** Tras la fermentación, las lías finas se depositan y pueden mantenerse en contacto con un vino blanco.
- **Mecanismo:** El bâtonnage remueve y resuspende las lías, aumentando el contacto del vino con manoproteínas, polisacáridos y compuestos de sabor procedentes de las levaduras.
- **Efecto:** El vino puede ganar textura cremosa, mayor peso en boca y más complejidad aromática.

**Mentor Guía:** La respuesta correcta es A: «El batonnage puede aumentar la complejidad aromática y aportar textura al vino blanco.». La clave está en el bâtonnage y el contacto con las lías finas: El bâtonnage remueve y resuspende las lías, aumentando el contacto del vino con manoproteínas, polisacáridos y compuestos de sabor procedentes de las levaduras. Por eso, el vino puede ganar textura cremosa, mayor peso en boca y más complejidad aromática.

**Entrenador Técnico:** Concepto técnico (RA1): Fija el mecanismo del bâtonnage y el contacto con las lías finas: Tras la fermentación, las lías finas se depositan y pueden mantenerse en contacto con un vino blanco. → El bâtonnage remueve y resuspende las lías, aumentando el contacto del vino con manoproteínas, polisacáridos y compuestos de sabor procedentes de las levaduras. En el examen, identifica este patrón causa→mecanismo→efecto antes de mirar las opciones.

**Revisor Estricto:** Exigencia de repaso (RA1): debes poder justificar por qué «El batonnage puede aumentar la complejidad aromática y aportar textura al vino blanco.» es correcta y por qué las otras tres opciones no lo son, citando el mecanismo del bâtonnage y el contacto con las lías finas. Si no puedes reconstruir la cadena completa sin ver las opciones, repasa este concepto en tu material WSET L3.

**Micro-drill:** Consolidación: ¿cuál de estas afirmaciones corresponde al bâtonnage y el contacto con las lías finas?
  - A. Protege al vino del oxígeno y desarrolla sabores únicos
  - B. Adición de aguardiente vínico
  - C. El batonnage puede aumentar la complejidad aromática y aportar textura al vino blanco. ✅
  - D. Estructura potente y necesidad de guarda
  - _Explicación:_ «El batonnage puede aumentar la complejidad aromática y aportar textura al vino blanco.» corresponde al bâtonnage y el contacto con las lías finas. Las demás afirmaciones son correctas, pero describen otros mecanismos.

---

## wset3_704 (sq 704) · RA1 · gold=False

**Pregunta:** ¿Cuál de las siguientes afirmaciones sobre la fermentación maloláctica es CORRECTA?
**Correcta (A):** La fermentación maloláctica convierte el ácido málico en láctico, disminuyendo la acidez.
**Nodo:** `HC_MLF_ACID_CONVERSION` · score 4 · en stem: fermentacion malolactica · en respuesta correcta: acido malico, disminuyendo la acidez, fermentacion malolactica

- **Causa:** Tras la fermentación alcohólica, las bacterias lácticas pueden realizar la fermentación maloláctica.
- **Mecanismo:** Las bacterias convierten el ácido málico, más punzante y con dos protones ácidos, en ácido láctico, más suave y con uno; liberan CO₂, pero no transforman el ácido tartárico.
- **Efecto:** La acidez titulable disminuye y el pH sube ligeramente, por lo que el vino resulta más suave y redondo sin perder la fracción de acidez tartárica.

**Mentor Guía:** La respuesta correcta es A: «La fermentación maloláctica convierte el ácido málico en láctico, disminuyendo la acidez.». La clave está en la conversión de ácido málico en ácido láctico durante la FML: Las bacterias convierten el ácido málico, más punzante y con dos protones ácidos, en ácido láctico, más suave y con uno; liberan CO₂, pero no transforman el ácido tartárico. Por eso, la acidez titulable disminuye y el pH sube ligeramente, por lo que el vino resulta más suave y redondo sin perder la fracción de acidez tartárica.

**Entrenador Técnico:** Concepto técnico (RA1): Fija el mecanismo de la conversión de ácido málico en ácido láctico durante la FML: Tras la fermentación alcohólica, las bacterias lácticas pueden realizar la fermentación maloláctica. → Las bacterias convierten el ácido málico, más punzante y con dos protones ácidos, en ácido láctico, más suave y con uno; liberan CO₂, pero no transforman el ácido tartárico. En el examen, identifica este patrón causa→mecanismo→efecto antes de mirar las opciones.

**Revisor Estricto:** Exigencia de repaso (RA1): debes poder justificar por qué «La fermentación maloláctica convierte el ácido málico en láctico, disminuyendo la acidez.» es correcta y por qué las otras tres opciones no lo son, citando el mecanismo de la conversión de ácido málico en ácido láctico durante la FML. Si no puedes reconstruir la cadena completa sin ver las opciones, repasa este concepto en tu material WSET L3.

**Micro-drill:** Consolidación: ¿cuál de estas afirmaciones corresponde a la conversión de ácido málico en ácido láctico durante la FML?
  - A. Protege al vino del oxígeno y desarrolla sabores únicos
  - B. Adición de aguardiente vínico
  - C. Estructura potente y necesidad de guarda
  - D. La fermentación maloláctica convierte el ácido málico en láctico, disminuyendo la acidez. ✅
  - _Explicación:_ «La fermentación maloláctica convierte el ácido málico en láctico, disminuyendo la acidez.» corresponde a la conversión de ácido málico en ácido láctico durante la FML. Las demás afirmaciones son correctas, pero describen otros mecanismos.

---

## wset3_707 (sq 707) · RA1 · gold=False

**Pregunta:** ¿Cuál de las siguientes afirmaciones sobre el riego por goteo es CORRECTA?
**Correcta (A):** El riego por goteo permite suministrar agua de forma controlada directamente a la zona radicular.
**Nodo:** `HC_DRIP_IRRIGATION_PRECISION` · score 4 · en stem: goteo, riego por goteo · en respuesta correcta: goteo, riego por goteo, suministrar agua de forma controlada, zona radicular

- **Causa:** Las vides de una región seca necesitan agua suplementaria aplicada con eficiencia.
- **Mecanismo:** Las líneas de goteo liberan cantidades medidas de agua lenta y directamente en la zona radicular de cada vid.
- **Efecto:** El aporte de agua puede controlarse con precisión y con menos evaporación y escorrentía que una aplicación superficial amplia.

**Mentor Guía:** La respuesta correcta es A: «El riego por goteo permite suministrar agua de forma controlada directamente a la zona radicular.». La clave está en la precisión del riego por goteo: Las líneas de goteo liberan cantidades medidas de agua lenta y directamente en la zona radicular de cada vid. Por eso, el aporte de agua puede controlarse con precisión y con menos evaporación y escorrentía que una aplicación superficial amplia.

**Entrenador Técnico:** Concepto técnico (RA1): Fija el mecanismo de la precisión del riego por goteo: Las vides de una región seca necesitan agua suplementaria aplicada con eficiencia. → Las líneas de goteo liberan cantidades medidas de agua lenta y directamente en la zona radicular de cada vid. En el examen, identifica este patrón causa→mecanismo→efecto antes de mirar las opciones.

**Revisor Estricto:** Exigencia de repaso (RA1): debes poder justificar por qué «El riego por goteo permite suministrar agua de forma controlada directamente a la zona radicular.» es correcta y por qué las otras tres opciones no lo son, citando el mecanismo de la precisión del riego por goteo. Si no puedes reconstruir la cadena completa sin ver las opciones, repasa este concepto en tu material WSET L3.

**Micro-drill:** Consolidación: ¿cuál de estas afirmaciones corresponde a la precisión del riego por goteo?
  - A. El riego por goteo permite suministrar agua de forma controlada directamente a la zona radicular. ✅
  - B. Protege al vino del oxígeno y desarrolla sabores únicos
  - C. Adición de aguardiente vínico
  - D. Estructura potente y necesidad de guarda
  - _Explicación:_ «El riego por goteo permite suministrar agua de forma controlada directamente a la zona radicular.» corresponde a la precisión del riego por goteo. Las demás afirmaciones son correctas, pero describen otros mecanismos.

---

## wset3_852 (sq 852) · RA5 · gold=False

**Pregunta:** ¿Cuál es la ventaja principal del formato magnum (1,5 litros) respecto a la botella estándar (0,75 litros) para vinos de guarda?
**Correcta (B):** Contiene más vino en relación al oxígeno que penetra por el cierre, favoreciendo un envejecimiento más lento y complejo
**Nodo:** `HC_MAGNUM_SLOW_AGEING` · score 4 · en stem: botella estandar, formato magnum · en respuesta correcta: envejecimiento mas lento, mas vino en relacion al oxigeno

- **Causa:** Una magnum contiene el doble de vino que una botella estándar, pero utiliza un cierre y un espacio de cabeza de escala parecida.
- **Mecanismo:** Cada unidad de vino queda expuesta a una proporción menor del oxígeno presente en el espacio de cabeza o transmitido a través del cierre.
- **Efecto:** La evolución oxidativa suele ser más lenta, permitiendo que los vinos aptos para guarda evolucionen gradualmente y conserven frescura durante más tiempo.

**Mentor Guía:** La respuesta correcta es B: «Contiene más vino en relación al oxígeno que penetra por el cierre, favoreciendo un envejecimiento más lento y complejo». La clave está en el envejecimiento más lento en formato magnum: Cada unidad de vino queda expuesta a una proporción menor del oxígeno presente en el espacio de cabeza o transmitido a través del cierre. Por eso, la evolución oxidativa suele ser más lenta, permitiendo que los vinos aptos para guarda evolucionen gradualmente y conserven frescura durante más tiempo.

**Entrenador Técnico:** Concepto técnico (RA5): Fija el mecanismo del envejecimiento más lento en formato magnum: Una magnum contiene el doble de vino que una botella estándar, pero utiliza un cierre y un espacio de cabeza de escala parecida. → Cada unidad de vino queda expuesta a una proporción menor del oxígeno presente en el espacio de cabeza o transmitido a través del cierre. En el examen, identifica este patrón causa→mecanismo→efecto antes de mirar las opciones.

**Revisor Estricto:** Exigencia de repaso (RA5): debes poder justificar por qué «Contiene más vino en relación al oxígeno que penetra por el cierre, favoreciendo un envejecimiento más lento y complejo» es correcta y por qué las otras tres opciones no lo son, citando el mecanismo del envejecimiento más lento en formato magnum. Si no puedes reconstruir la cadena completa sin ver las opciones, repasa este concepto en tu material WSET L3.

**Micro-drill:** Consolidación: ¿cuál de estas afirmaciones corresponde al envejecimiento más lento en formato magnum?
  - A. Contiene más vino en relación al oxígeno que penetra por el cierre, favoreciendo un envejecimiento más lento y complejo ✅
  - B. Protege al vino del oxígeno y desarrolla sabores únicos
  - C. Adición de aguardiente vínico
  - D. Estructura potente y necesidad de guarda
  - _Explicación:_ «Contiene más vino en relación al oxígeno que penetra por el cierre, favoreciendo un envejecimiento más lento y complejo» corresponde al envejecimiento más lento en formato magnum. Las demás afirmaciones son correctas, pero describen otros mecanismos.

---

## wset3_5 (sq 5) · RA4 · gold=False

**Pregunta:** ¿Qué diferencia al Oloroso del Amontillado en términos de crianza?
**Correcta (C):** Envejecimiento exclusivamente oxidativo
**Nodo:** `HC_OLOROSO_AMONTILLADO_AGEING_PATH` · score 3 · en stem: diferencia al oloroso del amontillado en terminos de crianza, oloroso del amontillado · en respuesta correcta: envejecimiento exclusivamente oxidativo

- **Causa:** El Oloroso se fortifica a un nivel que impide mantener un velo de flor estable, mientras el Amontillado comienza como vino de crianza biológica bajo flor antes de perder esa protección.
- **Mecanismo:** Sin la protección de la flor, el Oloroso permanece expuesto de forma controlada al oxígeno durante toda la maduración; el Amontillado primero desarrolla carácter biológico y después pasa a crianza oxidativa.
- **Efecto:** El Oloroso sigue una ruta de crianza exclusivamente oxidativa, mientras el Amontillado combina una fase biológica inicial con desarrollo oxidativo posterior.

**Mentor Guía:** La respuesta correcta es C: «Envejecimiento exclusivamente oxidativo». La clave está en las rutas de crianza de Oloroso y Amontillado: Sin la protección de la flor, el Oloroso permanece expuesto de forma controlada al oxígeno durante toda la maduración; el Amontillado primero desarrolla carácter biológico y después pasa a crianza oxidativa. Por eso, el Oloroso sigue una ruta de crianza exclusivamente oxidativa, mientras el Amontillado combina una fase biológica inicial con desarrollo oxidativo posterior.

**Entrenador Técnico:** Concepto técnico (RA4): Tema: fortified wines. Fija el mecanismo de las rutas de crianza de Oloroso y Amontillado: El Oloroso se fortifica a un nivel que impide mantener un velo de flor estable, mientras el Amontillado comienza como vino de crianza biológica bajo flor antes de perder esa protección. → Sin la protección de la flor, el Oloroso permanece expuesto de forma controlada al oxígeno durante toda la maduración; el Amontillado primero desarrolla carácter biológico y después pasa a crianza oxidativa. En el examen, identifica este patrón causa→mecanismo→efecto antes de mirar las opciones.

**Revisor Estricto:** Exigencia de repaso (RA4): debes poder justificar por qué «Envejecimiento exclusivamente oxidativo» es correcta y por qué las otras tres opciones no lo son, citando el mecanismo de las rutas de crianza de Oloroso y Amontillado. Si no puedes reconstruir la cadena completa sin ver las opciones, repasa este concepto en tu material WSET L3.

**Micro-drill:** Consolidación: ¿cuál de estas afirmaciones corresponde a las rutas de crianza de Oloroso y Amontillado?
  - A. Protege al vino del oxígeno y desarrolla sabores únicos
  - B. Adición de aguardiente vínico
  - C. Envejecimiento exclusivamente oxidativo ✅
  - D. Estructura potente y necesidad de guarda
  - _Explicación:_ «Envejecimiento exclusivamente oxidativo» corresponde a las rutas de crianza de Oloroso y Amontillado. Las demás afirmaciones son correctas, pero describen otros mecanismos.

---


*Documento formativo. Sin autoridad de examinador. safe_for_examiner: false.*
