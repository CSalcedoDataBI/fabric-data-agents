[![Lang: English](https://img.shields.io/badge/lang-English-1f6feb?style=flat-square)](04-source-instructions-and-fewshots.md)
[![Idioma: Español](https://img.shields.io/badge/idioma-Espa%C3%B1ol-2da44e?style=flat-square)](04-source-instructions-and-fewshots.es.md)
&nbsp;·&nbsp; [↑ Índice](../../README.es.md)

# 04 · Instrucciones de fuente y few-shots

## Qué es

El contexto a nivel de fuente le enseña al agente **cómo consultar bien una fuente específica**. Tiene
dos partes:

1. **Instrucciones de fuente** — reglas acotadas a una sola fuente (sus rarezas de esquema, claves de
   join, convenciones de filtro, columnas preferidas).
2. **Few-shots** — pares *pregunta → consulta* ya resueltos que el traductor empareja en tiempo de
   ejecución. Esto es few-shot learning clásico, y es **la mayor palanca sobre la precisión**.

Dónde autoras esto depende del tipo de fuente — una asimetría que casi a todos les hace tropezar:

- **Lakehouse / Warehouse / KQL:** autoras consultas de ejemplo e instrucciones de fuente **en el
  propio Data Agent** (el panel *Example queries*). Solo se usan las consultas con sintaxis válida que
  coinciden con el esquema seleccionado; las inválidas se ignoran en silencio.
- **Modelo semántico de Power BI:** el panel de example-queries del Data Agent **no acepta pares**. En
  su lugar, este contexto vive en el **modelo**, vía **Prep for AI** — *AI Data Schema* (qué
  tablas/columnas/medidas ve la IA), *AI Instructions* (reglas de negocio **y** DAX de ejemplo), y
  *Verified Answers* (mapeos aprobados pregunta→visual, 5–7 formulaciones de disparo cada uno). El
  Data Agent los honra todos; simplemente no los configuras en el agente.

## Por qué importa

Las instrucciones le dicen al agente las reglas; los few-shots se las *muestran* — y mostrar
generaliza donde decir no lo hace. Un puñado de ejemplos correctos arregla clases enteras de error:
joins malos, formato de filtro equivocado, la medida "ventas" errónea entre cinco parecidas, las
columnas por defecto equivocadas.

Para modelos semánticos, la división de Prep for AI importa porque es donde la precisión se gana de
verdad. Las Verified Answers cortocircuitan preguntas ambiguas hacia una estructura de consulta
conocida-buena *antes* de que el modelo adivine; el AI Data Schema retira medidas parecidas de la
vista para que "las ventas del último trimestre" no se resuelvan a Bruto cuando el estándar de la casa
es Neto. La higiene del modelo lo potencia: un modelo esbelto, bien descrito y con DAX eficiente corre
más rápido y le da al generador de DAX menos ruido que malinterpretar.

## Cómo escribirla bien

- **Autora los ejemplos donde el tipo de fuente lo exige** — panel del agente para SQL/KQL, Prep for
  AI para modelos semánticos. Poner pares DAX en el panel del agente para un modelo semántico no hace
  nada.
- **Haz los few-shots diversos, no numerosos.** Cubre los *tipos* de pregunta (ranking, desglose,
  ratio, delta), no muchas reformulaciones de una.
- **Valida cada ejemplo.** Para SQL/KQL, la sintaxis inválida se descarta en silencio. Para DAX,
  verifícalo en DAX Query View antes de pegarlo en las AI Instructions.
- **Describe todo** en un modelo semántico — las descripciones de tabla, columna y medida son lo que
  el generador de DAX lee para interpretar una pregunta.
- **Usa nombres amigables al negocio.** `Total Revenue`, no `TR_AMT`; la metadata del modelo *es* el
  vocabulario del agente.
- **Incluye objetos dependientes** en el AI Data Schema — una medida que referencia otras medidas
  necesita esas (y sus columnas) también seleccionadas.

## Anti-patrón

**Esperar que el panel de example-queries del Data Agent enseñe a un modelo semántico** — el panel no
tomará los pares, y la autoría no tiene efecto en silencio. **Un ejemplo gigante para todo** que
intenta demostrar cada join a la vez, del que el agente no puede generalizar. **Ejemplos sin validar**
— descartados (SQL/KQL) o, peor para DAX, pegados mal y copiados fielmente. Y un **modelo inflado con
nombres crípticos**, donde ninguna cantidad de instrucción supera una metadata que el generador no
puede leer.

## El ejemplo Contoso

El [`example-queries.json`](../../examples/contoso-retail/data-agent/example-queries.json) de Contoso es un
**artefacto didáctico** para este repositorio — hace visible en la página el DAX pretendido. En el
producto real, como la fuente es un **modelo semántico**, estos pares se autorarían como DAX de
ejemplo dentro de **Prep for AI › AI Instructions** en el modelo, no en el panel de example-queries
del agente. El conjunto es deliberadamente diverso — uno por patrón:

- **Medidas compañeras** — `EVALUATE ROW("Total Sales", [Total Sales], "Orders", [Orders], "Distinct Customers", [Distinct Customers])`
  muestra la regla de reporte en acción.
- **Ranking** — `TOPN(5, …, [Total Sales], DESC)` → una tabla etiquetada.
- **Ratio per cápita** — `[Sales per Customer]` devuelto *con* `[Distinct Customers]`, para que
  el denominador sea visible y nunca se sume.
- **Desglose por dimensión nombrada** — canal `Online` vs `Store` vía `[% of Total Sales]`.
- **Descomposición de drivers** — el split del delta interanual sobre `DimProduct[CategoryName]`.

Cada ejemplo codifica una regla de [03](03-agent-instructions.es.md) como un patrón concreto que el
traductor puede imitar — la esencia del diseño de few-shots.

---
_Siguiente: [05 · Ontología y glosario →](05-ontology-and-glossary.es.md)_
