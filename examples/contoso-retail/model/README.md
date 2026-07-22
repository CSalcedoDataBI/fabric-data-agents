[![Lang: English](https://img.shields.io/badge/lang-English-1f6feb?style=flat-square)](README.md)
[![Idioma: Español](https://img.shields.io/badge/idioma-Espa%C3%B1ol-2da44e?style=flat-square)](README.es.md)
&nbsp;·&nbsp; [↑ Example](../README.md)

# Contoso Retail — the semantic model (issue [#5](https://github.com/CSalcedoDataBI/fabric-data-agents/issues/5))

The teaching semantic model built on the [dataset](../data) next door. **This is the model used to
evaluate everything this reference says about a Fabric Data Agent** — the Data Agent config
(issue [#6](https://github.com/CSalcedoDataBI/fabric-data-agents/issues/6)) sits on top of it.

## Two ways to use it

### 1. Just open it — `ContosoRetail.pbix` (data embedded) ← start here
Download and open in Power BI Desktop. The data is **embedded inside the file** (126,524 sales lines):
no refresh, no SQL Server, no internet. Everything loads instantly. This is the **evaluation model** —
open it, explore the star schema, and see the 15 measures compute.

### 2. The source — `ContosoRetail.pbip` (TMDL, refreshable)
The human-readable definition. Tables, relationships and the measures container are plain-text
**TMDL** under `ContosoRetail.SemanticModel/definition/`. Data streams from the committed Parquet in
[`../data`](../data) over **GitHub raw** via the `DataBaseUrl` parameter — so it **refreshes for
anyone once this repo is public**, with no local paths. To refresh offline, point `DataBaseUrl` at a
local folder holding the `.parquet` files.

## The model

- **Star schema:** `FactSales` ↔ 6 dimensions (`DimProduct`, `DimCustomer`, `DimStore`, `DimDate`,
  `DimCurrency`, `DimCurrencyExchange`), joined on their `*Key` columns; the calendar relationship is
  `FactSales[OrderDate] → DimDate[Date]`.
- **Measures container `_Measures`** — a hidden calculated table holding **15 measures** in 5 display
  folders, so measures live in one tidy, categorised home instead of scattered across fact tables:

| Folder | Measures |
|---|---|
| **01 Sales & Revenue** | Total Sales · Total Quantity · Orders · Average Order Value |
| **02 Profitability** | Total Cost · Gross Margin · Margin % |
| **03 Customers** | Distinct Customers · Sales per Customer |
| **04 Pricing & Basket** | Average Selling Price · Units per Order · % of Total Sales |
| **05 Time Intelligence** | Sales YTD · Sales PY · Sales YoY % |

## Gotchas worth knowing (documented here so you don't relive them)

- **The measures table is `_Measures`, not `Measures`.** `Measures` is a **reserved table name** in
  Power BI: a table named exactly `Measures` makes the `.pbip` fail to open with *"Unsupported Table
  name 'Measures' has been found in data model schema"* (a regression since the **Feb 2025** Desktop
  update). The leading underscore also sorts it to the top of the field list.
- **`FactSales.OrderDate` / `DeliveryDate` arrive as text** from the source and are cast to `date`
  in the partition (`Table.TransformColumnTypes(..., type date, "en-US")`) so the `DimDate`
  relationship is valid.

## Verified

`FactSales` **126,524** rows · **Total Sales $19,903,677** · **Distinct Customers 12,000** · all 15
measures compute (queried against the live engine).
