[![Lang: English](https://img.shields.io/badge/lang-English-1f6feb?style=flat-square)](README.md)
[![Idioma: Español](https://img.shields.io/badge/idioma-Espa%C3%B1ol-2da44e?style=flat-square)](README.es.md)
&nbsp;·&nbsp; [↑ Ejemplo](../README.es.md)

# Contoso Retail — el modelo semántico (issue [#5](https://github.com/CSalcedoDataBI/fabric-data-agents/issues/5))

El modelo semántico de enseñanza construido sobre el [dataset](../data) de al lado. **Este es el
modelo que usamos para evaluar todo lo que esta referencia afirma sobre un Fabric Data Agent** — la
config del Data Agent (issue [#6](https://github.com/CSalcedoDataBI/fabric-data-agents/issues/6)) se
apoya en él.

## Dos formas de usarlo — elige según quién seas

Un Power BI Project (PBIP) es el formato ideal para *construir* un modelo, pero una *descarga* incómoda
para quien solo quiere mirar: implica reconectar datos, pasar diálogos de credenciales/privacidad y
refrescar — fricción que hace que mucha gente abandone. Por eso publicamos ambos formatos y
**priorizamos el que simplemente funciona**.

### Para casi todos — `ContosoRetail.pbix` (datos embebidos) ← empieza aquí
Descarga, abre en Power BI Desktop, listo. Los datos están **horneados en el archivo** (126,524 líneas
de venta): sin refresh, sin datos que bajar, sin reconectar, sin internet. Además lleva la
**preparación para IA** del modelo (descripciones de campos, AI instructions, AI data schema), así que
puedes abrir *Prep data for AI* y ver exactamente cómo está configurado para un Data Agent — sin
configurar nada. Es el modelo contra el que se evalúa el Fabric Data Agent. **Este es el archivo que le
pasas a la gente.**

### Para constructores — `ContosoRetail.pbip` (fuente TMDL)
La definición legible y versionada (**TMDL** en texto plano bajo
`ContosoRetail.SemanticModel/definition/`). Úsala para leer el código, contribuir, o **hacer / rehacer
Prep for AI** — ese trabajo se autora aquí, sobre el PBIP conectado, y luego se hornea en el `.pbix` de
arriba (que se regenera desde esta fuente). Los datos se transmiten desde los Parquet commiteados en
[`../data`](../data) por **GitHub raw** vía el parámetro `DataBaseUrl`, así refresca para cualquiera en
cuanto el repo sea público (el primer refresh pide una vez acceso anónimo). Para trabajar 100% offline,
apunta `DataBaseUrl` a una carpeta local con los `.parquet`.

> **No publicamos el PBIP como "lo que se ejecuta".** El PBIP es la *fuente*; conectar datos y
> Prep-for-AI son pasos de constructor. El artefacto que un usuario descarga y abre es el **`.pbix`**.

## El modelo

- **Esquema estrella:** `FactSales` ↔ 6 dimensiones (`DimProduct`, `DimCustomer`, `DimStore`,
  `DimDate`, `DimCurrency`, `DimCurrencyExchange`), unidas por sus columnas `*Key`; la relación de
  calendario es `FactSales[OrderDate] → DimDate[Date]`.
- **Contenedor de medidas `_Measures`** — una tabla calculada oculta con **15 medidas** en 5 carpetas
  de visualización, para que las medidas vivan en un solo hogar ordenado y categórico en vez de
  dispersas por las tablas de hechos:

| Carpeta | Medidas |
|---|---|
| **01 Sales & Revenue** | Total Sales · Total Quantity · Orders · Average Order Value |
| **02 Profitability** | Total Cost · Gross Margin · Margin % |
| **03 Customers** | Distinct Customers · Sales per Customer |
| **04 Pricing & Basket** | Average Selling Price · Units per Order · % of Total Sales |
| **05 Time Intelligence** | Sales YTD · Sales PY · Sales YoY % |

## Gotchas que conviene saber (documentados aquí para que no los revivas)

- **La tabla de medidas es `_Measures`, no `Measures`.** `Measures` es un **nombre de tabla
  reservado** en Power BI: una tabla llamada exactamente `Measures` hace que el `.pbip` **falle al
  abrir** con *"Unsupported Table name 'Measures' has been found in data model schema"* (regresión
  desde la actualización de Desktop de **feb-2025**). El guion bajo inicial además la ordena arriba.
- **`FactSales.OrderDate` / `DeliveryDate` llegan como texto** desde la fuente y se castean a `date`
  en la partición (`Table.TransformColumnTypes(..., type date, "en-US")`) para que la relación con
  `DimDate` sea válida.

## Verificado

`FactSales` **126,524** filas · **Total Sales $19,903,677** · **Distinct Customers 12,000** · las 15
medidas calculan (consultado contra el motor en vivo).
