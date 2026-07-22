[![Lang: English](https://img.shields.io/badge/lang-English-1f6feb?style=flat-square)](README.md)
[![Idioma: Español](https://img.shields.io/badge/idioma-Espa%C3%B1ol-2da44e?style=flat-square)](README.es.md)
&nbsp;·&nbsp; [↑ Example](../README.md)

# Contoso Retail — the semantic model (issue [#5](https://github.com/CSalcedoDataBI/fabric-data-agents/issues/5))

The teaching semantic model built on the [dataset](../data) next door. **This is the model used to
evaluate everything this reference says about a Fabric Data Agent** — the Data Agent config
(issue [#6](https://github.com/CSalcedoDataBI/fabric-data-agents/issues/6)) sits on top of it.

## Two ways to use it — pick by who you are

A Power BI Project (PBIP) is the right format for *building* a model, but a rough *download* for
someone who just wants to look: it means reconnecting data, clearing credential/privacy prompts, and
refreshing — friction that makes many people quit. So we ship both formats and **lead with the one
that just works**.

### For almost everyone — `ContosoRetail.pbix` (data embedded) ← start here
Download, open in Power BI Desktop, done. The data is **baked into the file** (126,524 sales lines):
no refresh, no data to download, no reconnecting, no internet. It also carries the model's
**AI-readiness** (field descriptions, AI instructions, AI data schema), so you can open *Prep data for
AI* and see exactly how it's set up for a Data Agent — configuring nothing. This is the model the
Fabric Data Agent is evaluated against. **This is the file to hand people.**

### For builders — `ContosoRetail.pbip` (TMDL source)
The human-readable, version-controlled definition (plain-text **TMDL** under
`ContosoRetail.SemanticModel/definition/`). Use it to read the code, contribute, or **do / redo Prep
for AI** — that work is authored here, on the connected PBIP, then baked into the `.pbix` above (which
is regenerated from this source). Data streams from the committed Parquet in [`../data`](../data) over
**GitHub raw** via the `DataBaseUrl` parameter, so it refreshes for anyone once this repo is public
(the first refresh asks once for anonymous access). To work fully offline, point `DataBaseUrl` at a
local folder holding the `.parquet` files.

> **We don't publish the PBIP as the thing you "run".** The PBIP is the *source*; connecting data and
> Prep-for-AI are builder steps. The artifact a user downloads and opens is the **`.pbix`**.

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
