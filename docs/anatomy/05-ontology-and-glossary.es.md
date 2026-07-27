[![Lang: English](https://img.shields.io/badge/lang-English-1f6feb?style=flat-square)](05-ontology-and-glossary.md)
[![Idioma: Español](https://img.shields.io/badge/idioma-Espa%C3%B1ol-2da44e?style=flat-square)](05-ontology-and-glossary.es.md)
&nbsp;·&nbsp; [↑ Índice](../../README.es.md)

# 05 · Ontología y glosario

## Qué es

La ontología es el **mapa de las palabras que dicen los usuarios a los campos que tiene el modelo**.
Los usuarios preguntan por "clientes", "churn", "el Norte", "el último trimestre"; el modelo tiene
`DimCustomer[Country]`, `[Distinct Customers]`, `DimDate[Date]`. El glosario cierra esa brecha:
sinónimos, definiciones de negocio, agrupaciones por defecto y el campo canónico detrás de cada
término ambiguo.

No es un artefacto separado que despliegas — está **distribuido entre las partes que ya escribes**:
metadata del modelo (descripciones de tabla/columna/medida), AI Instructions de Prep for AI,
definiciones a nivel agente y Verified Answers. (Fabric también tiene un tipo de fuente *Ontología* de
primera clase, en preview, para modelos de dominio estilo grafo — algo distinto del glosario de
negocio que se discute aquí.)

## Por qué importa

La ambigüedad es donde un Data Agent se equivoca calladamente. "Muéstrame el rendimiento por
territorio" se resuelve a una columna `Territory` de la tabla de productos cuando el usuario quería
decir regiones de venta — consulta válida, respuesta equivocada. Un glosario elimina la adivinanza:

- **Sinónimos → un campo.** "Clientes", "compradores", "consumidores" aquí significan todos *Distinct
  Customers*, y decirlo evita que el agente invente una segunda población.
- **Las definiciones fijan la semántica.** "Margen = `[Gross Margin]` para el importe, `[Margin %]`
  para la tasa" vuelve la convención de la casa el default en vez de un volado entre medidas parecidas.
- **Las agrupaciones por defecto** responden la parte no dicha de una pregunta. "Desglosa el gasto"
  sin dimensión nombrada debería caer a las *dimensiones de liderazgo*, no a una columna al azar.
- **El lenguaje de tiempo** ("último trimestre", "temporada alta") necesita una definición explícita o
  el agente elige un calendario que no le pidieron.

## Cómo escribirla bien

- **Describe cada objeto en lenguaje de negocio.** Las descripciones en tablas, columnas y medidas son
  el primer diccionario del agente — `Sales Region`, no `DIM_GEO_01`.
- **Lista sinónimos reales** que los usuarios de verdad tipean, mapeados al único campo canónico.
- **Define los términos cargados** — las métricas cuyo significado se disputa (rentabilidad, activo,
  churned, margen) — y nombra la medida exacta a la que cada uno se resuelve.
- **Declara los desgloses por defecto** para que un "desglósalo" sin dimensión sea determinista.
- **Usa Verified Answers para las preguntas ambiguas recurrentes** — 5–7 formulaciones de disparo cada
  una — para que los casos comunes cortocircuiten a una estructura conocida-buena.
- **Mantén una sola fuente de verdad.** Prefiere la metadata del modelo + Prep for AI; usa
  definiciones a nivel agente solo para terminología entre fuentes.

## Anti-patrón

**Confiar en los nombres de columna como glosario** — confiar en que `Territory` obviamente significa
lo que el usuario quiere, cuando el modelo tiene tres hogares plausibles para la palabra. **Métricas
cargadas sin definir**, donde "rentabilidad" se resuelve calladamente a la medida de margen que ordene
primero. **Sinónimos solo en la cabeza del modelador**, así que "compradores" nunca llega a *Distinct
Customers*. Y **definiciones contradictorias** regadas entre metadata del modelo, instrucciones del
agente y Verified Answers que no concuerdan — el agente hereda el conflicto.

## El ejemplo Contoso

Contoso codifica su glosario dentro de las
[instrucciones](../../examples/contoso-retail/data-agent/instructions.md) y del modelo, no como archivo
aparte:

- **El término del denominador está fijado.** "Clientes" aquí significa exactamente una cosa —
  **`[Distinct Customers]`** (clientes que compraron en el periodo, no las filas de `DimCustomer`) — y
  las reglas obligan a que todo ratio per cápita lo nombre, así que "ventas por cliente" no puede
  adoptar en silencio otra población.
- **El desglose por defecto está declarado.** Cuando una pregunta necesita un desglose y no nombra
  dimensión, el agente cae a un juego declarado (`DimProduct[CategoryName]`, `DimStore[CountryName]`,
  `DimCustomer[Country]`, `FactSales[Channel]`) — la agrupación no dicha hecha explícita.
- **Los valores se ilustran, no se adivinan.** `FactSales[Channel]` es `Online` o `Store`; los valores
  de categoría están **en español** (`Electrónica`, `Electrodomésticos`) — decirlo evita que el agente
  filtre por `Electronics` y devuelva vacío.
- **`>about`** expone este glosario a los usuarios bajo demanda, volviendo la ontología
  una funcionalidad descubrible en vez de configuración escondida.

---
_Siguiente: [06 · Directo vs. orquestador →](06-direct-vs-orchestrator.es.md)_
