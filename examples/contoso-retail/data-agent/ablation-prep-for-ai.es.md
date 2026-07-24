# Ablation — ¿el Prep-for-AI del modelo cambia las respuestas?

Un A/B controlado sobre el **ContosoRetail Data Agent**: mismo agente, mismas
preguntas, solo cambia la **fuente de datos**. El objetivo es aislar qué aporta
realmente el **Prep-for-AI** del modelo semántico (AI instructions + verified
answers, autoradas sobre el modelo) por encima de las **Agent instructions** del
propio agente.

## Montaje

Dos modelos semánticos publicados en el workspace, con **los mismos datos**:

| Modelo | ¿Prep-for-AI en el modelo? |
|---|---|
| `ContosoRetail` | ✅ sí (AI instructions + verified answers) |
| `ContosoRetail V2` | ❌ no |

Ambos se agregan como fuentes a **un solo** Data Agent, cuyas **Agent instructions**
llevan las guardrails de negocio (moneda, aditividad, valores de dimensión en
español, tablas etiquetadas). Para cada ronda: tildar una sola fuente, **Publish**,
y preguntar contra el agente publicado.

> El endpoint de consumo lee siempre el estado **publicado**, no el draft.
> Tilda la fuente que quieras → Publish → luego pregunta.

## Las tres preguntas (idénticas en ambas rondas)

1. *What were total sales in 2024? State the currency. Then show the exact DAX query you executed.*
2. *What is the margin percentage for 2024? Then show the exact DAX query you executed.*
3. *Show total sales by product category for 2024 as a labeled table. Then show the exact DAX query you executed.*

Q1 prueba la guardrail de **moneda**, Q2 la de **no-aditividad** (una tasa se
recomputa, nunca se suma), Q3 la de **valores en español** + tabla etiquetada — y, en
su DAX, si el agente nombra las columnas **reales**.

## Resultados

| | **A — V2 (sin Prep-for-AI)** | **B — ContosoRetail (con Prep-for-AI)** |
|---|---|---|
| **Q1 total 2024** | `10,387,132 MXN` ✅ | `10,387,132 MXN` ✅ |
| Q1 DAX mostrado | `SUMMARIZECOLUMNS(DimDate[Year], FILTER(…=2024), …, [Total Sales])` | `CALCULATE([Total Sales], YEAR(DimDate[Date]) = 2024)` |
| **Q2 margin %** | `19.6%` ✅ (recomputado, no sumado) | `19.6%` ✅ (recomputado, no sumado) |
| Q2 DAX mostrado | `DIVIDE([Gross Margin], [Total Sales])` filtrado a 2024 | `SUMMARIZECOLUMNS(DimDate[Year], "Margin %", [Margin %]) WHERE …` |
| **Q3 por categoría** | tabla en español ✅ (mismas cifras) | tabla en español ✅ (mismas cifras) |
| Q3 DAX mostrado | `'DimProduct'[Category]` ❌ **columna que no existe** | `DimProduct[CategoryName]` ✅ **columna real exacta** |

Cifras de Q3 (ambas rondas, MXN):

| Categoría | Total de Ventas 2024 |
|---|---:|
| Electrónica | 3,489,973 |
| Videojuegos y Juguetes | 2,929,040 |
| Electrodomésticos | 2,085,640 |
| Música, Películas y Medios | 1,882,478 |

## Hallazgos

1. **Los números son idénticos.** V2 es una copia de los mismos datos, así que el
   Prep-for-AI no cambió nada en los resultados — ni un peso.
2. **Las guardrails se cumplen en AMBAS rondas** — MXN sin conversión, margen
   no-aditivo recomputado, categorías en español, tabla etiquetada. Viven en las
   **Agent instructions**, no en el modelo. → Con instrucciones de agente fuertes, el
   grueso del grounding lo aporta el prompt del agente, no el Prep-for-AI del modelo.
3. **Dónde SÍ se nota el Prep-for-AI: fidelidad de esquema en el DAX.** En Q3, la
   ronda con Prep-for-AI escribió el nombre **real** de la columna
   (`DimProduct[CategoryName]`); la ronda sin Prep-for-AI inventó `[Category]`. Ese es
   el beneficio marginal: **nombra bien columnas y tablas**, que es justo lo que
   reduce errores en las preguntas menos "guiadas" que hará un usuario real.

## Caveat honesto

El *"exact DAX executed"* que imprime el agente **no es necesariamente el query
literal** — es una reconstrucción del LLM. Prueba: el Q2 de la ronda B muestra
`SUMMARIZECOLUMNS(...) WHERE ...`, que **no es DAX válido**. Lo fiable son los
**números** (contrastados contra un `executeQueries` en DAX directo) y los **nombres
de columna** que elige el modelo. Para capturar el query *literal* haría falta una
traza XMLA sobre el modelo semántico en Fabric (más pesado; fuera de alcance aquí).

## Reprodúcelo manualmente

1. Publica dos modelos semánticos con **los mismos datos** — uno con Prep-for-AI y
   otro sin él (`… V2`).
2. Crea un Data Agent; **Add data** → agrega ambos modelos.
3. Pega las **Agent instructions** (ver [`instructions.md`](instructions.md)).
4. Ronda A: tilda **solo V2** → **Publish** → en **Test data agent**, haz las tres
   preguntas; copia cada respuesta + el DAX que muestra.
5. Ronda B: destilda V2, tilda el modelo **con Prep-for-AI** → **Publish** → repite
   las mismas tres preguntas; copia respuesta + DAX.
6. Compara. Deberías ver cifras idénticas, guardrails respetadas en ambas, y la ronda
   con Prep-for-AI usando los nombres de columna exactos.

## Round C — la corrida de aislamiento (Agent instructions peladas)

Las rondas A/B todavía llevaban las guardrails en las Agent instructions, así que para
aislar la variable las quitamos. Dos agentes **separados** (para descartar caché), cada
uno cableado a un modelo, ambos con el mismo prompt pelado:

> `You are a retail sales analyst for Contoso. Answer questions about the ContosoRetail semantic model.`

| | **C-A · V2 (pelado, sin Prep)** | **C-B · ContosoRetail (pelado, con Prep)** |
|---|---|---|
| Q1 total 2024 | `10,387,132` **MXN** ✅ | `10,387,132` **MXN** ✅ |
| Q2 margin % | `19.6%` ✅ (no sumado) | `19.6%` ✅ (no sumado) |
| Q3 por categoría | español ✅, cifras correctas | español ✅, cifras correctas |
| DAX nombres de columna | `FactSales[SalesAmount]`, `FactSales[GrossMargin]`, `DimProduct[Category]` ❌ inventados | `[Total Sales]`, `DimProduct[CategoryName]`, `DimCurrency[CurrencyCode]` ✅ reales |

**La sorpresa:** con prompt pelado, ambos agentes *igual* dieron el número correcto,
`MXN` y las categorías en español. Esas tres cosas nunca vinieron de las instrucciones —
están horneadas en el **modelo**:

- **MXN** → el *format string* de las medidas / `DimCurrency` (metadata del modelo).
- **Español** → son los **valores reales de los datos** (la categoría *se llama* "Electrónica").
- **Margen no-aditivo** → la medida `[Margin %]` ya está definida; el agente la usa y
  sale bien sola.

## El cuadro completo — cuatro combos, mismas preguntas

| Combo | Números | MXN | Español | **DAX nombres reales** |
|---|:--:|:--:|:--:|:--:|
| A · instrucciones full + sin Prep | ✅ | ✅ | ✅ | ❌ |
| B · instrucciones full + Prep | ✅ | ✅ | ✅ | ✅ |
| C-A · pelado + sin Prep | ✅ | ✅ | ✅ | ❌ |
| C-B · pelado + Prep | ✅ | ✅ | ✅ | ✅ |

**Solo se mueve la última columna — y se mueve con el Prep-for-AI, no con las Agent instructions.**

- **Agent instructions (full vs pelado):** en estas preguntas, efecto medible ≈ 0.
- **Prep-for-AI (con vs sin):** el *único* delta medible es la **fidelidad de nombres de
  tabla/columna en el DAX generado** (`DimProduct[CategoryName]` vs el inventado
  `[Category]` / `FactSales[SalesAmount]`).

La moneda, el idioma y la no-aditividad eran propiedades del **modelo** desde el
principio, no de ninguna capa de instrucciones. El valor real del Prep-for-AI (y del
prompt del agente) aparecería en preguntas **ambiguas** o con lógica no horneada en el
modelo — qué medida elegir, evitar la `DimCurrencyExchange` desconectada, sinónimos.
Round D prueba exactamente eso.

## Round D — preguntas ambiguas (y la trampa del Test pane)

A ambos agentes pelados se les hicieron dos preguntas deliberadamente ambiguas:

1. *"¿Cuál es el margen total?"* — no define absoluto vs porcentaje.
2. *"¿Cuáles son las ventas del último trimestre?"* — los datos terminan en 2024-12-31,
   así que "último trimestre" respecto a hoy no tiene datos.

**Por el endpoint MCP (el camino de producción) ambos agentes respondieron idéntico y
correcto** — verificado contra DAX directo:

| Pregunta | V2 (sin Prep) | ContosoRetail (Prep) | Ground truth |
|---|---|---|---|
| margen total | `$3,938,789` | `$3,938,789 MXN` | `3,938,789` (Gross Margin) ✅ |
| último trimestre | `2024-Q4 $2,653,095` | `2024-Q4 $2,653,095` | `2,653,095` ✅ |

Ambos resolvieron bien "último trimestre" = **el último trimestre con datos (2024-Q4)**,
no un trimestre relativo a hoy.

**La trampa de los dos paneles (la lección de verdad).** Fabric muestra dos superficies de
chat parecidas que se comportan muy distinto:

- **Build agent with AI** — el *copiloto de autoría*. Te ayuda a configurar el agente;
  chatea, propone SQL/DAX de forma ilustrativa, pide precisiones y **puede no ejecutar**
  contra el modelo.
- **Test data agent** — el *runtime del agente*. Llama a la herramienta de query, ejecuta
  DAX y muestra *"N step completed · Analyzed ContosoRetail SemanticModel · Execution and
  output"*.

Las primeras capturas de preguntas ambiguas venían de **Build agent with AI**: ahí el
agente con Prep dudó, propuso **SQL** crudo (`SUM(Quantity*NetPrice)…`) y dijo *"no puedo
ejecutar, cópiala y ejecútala en tu entorno"* — sin correr nada. Repetido en **Test data
agent**, el mismo agente con Prep ejecutó DAX limpio y respondió — el margen devolvió
**tanto** `[Gross Margin]` = $3,938,789 **como** `[Margin %]` = 19.8% usando las medidas
reales, etiquetado en español con MXN. Coincide exacto con MCP/API.

**Lección (importa para cualquiera que evalúe un Data Agent):** evalúa en **Test data
agent** o contra el **endpoint MCP** — nunca en **Build agent with AI**, que es un
asistente de construcción, no el runtime. Juzgar al agente por el copiloto de autoría es
como sacas un veredicto falso de "no sabe responder".

## Veredicto general (A · B · C · D) — corregido

> **Corrección (2026-07-23):** una versión previa afirmaba que el *único* delta reproducible
> del Prep-for-AI era la fidelidad de nombres en el DAX (con Prep → `DimProduct[CategoryName]`,
> sin Prep → inventar `[Category]`). Se **retracta**: las corridas manuales en **Test data
> agent** muestran que AMBOS agentes (con y sin Prep) generan el nombre correcto
> `DimProduct[CategoryName]` en el query **ejecutado**. El nombre inventado solo aparecía en el
> DAX que el chat *reconstruye*, no en el ejecutado — no-determinismo, no efecto del Prep.

- **Números, moneda (MXN), idioma (español) y el DAX ejecutado:** idénticos en cada
  combinación y por ambos canales reales (Test data agent + API) → vienen del **modelo**, no
  de las instrucciones ni del Prep-for-AI.
- **No se encontró diferencia reproducible** entre con-Prep y sin-Prep en estas preguntas.
  Eran demasiado "limpias" para exigirle al Prep-for-AI (su valor debería verse en preguntas
  ambiguas, sinónimos, evitar tablas desconectadas — ronda futura).
- **Lecciones que quedan:** (1) evalúa en **Test data agent** / la **API MCP**, nunca en
  **Build agent with AI**; (2) el DAX que un Data Agent *muestra* es una reconstrucción —
  vale el query **ejecutado** (Execution & output) y verificar números contra DAX directo.
