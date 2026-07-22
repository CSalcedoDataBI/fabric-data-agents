[![Lang: English](https://img.shields.io/badge/lang-English-1f6feb?style=flat-square)](README.md)
[![Idioma: Español](https://img.shields.io/badge/idioma-Espa%C3%B1ol-2da44e?style=flat-square)](README.es.md)
&nbsp;·&nbsp; [↑ Ejemplo](../README.es.md)

# Contoso Retail — el modelo semántico (issue [#5](https://github.com/CSalcedoDataBI/fabric-data-agents/issues/5))

El modelo semántico de enseñanza construido sobre el [dataset](../data) de al lado. **Este es el
modelo que usamos para evaluar todo lo que esta referencia afirma sobre un Fabric Data Agent** — la
config del Data Agent (issue [#6](https://github.com/CSalcedoDataBI/fabric-data-agents/issues/6)) se
apoya en él.

## Dos formas de usarlo

### 1. Solo ábrelo — `ContosoRetail.pbix` (datos embebidos) ← empieza aquí
Descárgalo y ábrelo en Power BI Desktop. Los datos están **embebidos dentro del archivo** (126,524
líneas de venta): sin refresh, sin SQL Server, sin internet. Todo carga al instante. Este es el
**modelo de evaluación** — ábrelo, explora el esquema estrella y ve las 15 medidas calculando.

### 2. La fuente — `ContosoRetail.pbip` (TMDL, refrescable)
La definición legible. Tablas, relaciones y el contenedor de medidas son **TMDL** en texto plano bajo
`ContosoRetail.SemanticModel/definition/`. Los datos se transmiten desde los Parquet commiteados en
[`../data`](../data) por **GitHub raw** vía el parámetro `DataBaseUrl` — así **refresca para
cualquiera en cuanto el repo sea público**, sin rutas locales. Para refrescar offline, apunta
`DataBaseUrl` a una carpeta local con los `.parquet`.

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
