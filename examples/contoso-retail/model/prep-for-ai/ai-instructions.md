# Contoso Retail — AI instructions (verified)

The **AI instructions** for the Contoso Retail semantic model's *Prep for AI*. To apply:
Power BI Desktop → **Home → Prep data for AI → Add AI instructions** → paste the block below →
**Apply** → **File → Save**.

## Every line was verified — not assumed

| Claim in the instructions | How it was verified | Result |
|---|---|---|
| Reporting period 2023-01-01 → 2024-12-31 | `MIN/MAX(DimDate[Date])` via duckdb over the committed Parquet | ✅ confirmed |
| `DimDate[Date]` ↔ `FactSales[OrderDate]` | `relationships.tmdl` | ✅ confirmed |
| Additive vs non-additive lists | each measure's DAX in `_Measures.tmdl` (SUM/SUMX vs DIVIDE) | ✅ confirmed |
| Breakdown by `FactSales[Channel]` | `SELECT DISTINCT Channel` → `Online`, `Store` | ✅ confirmed |
| Product categories (Spanish) | `SELECT DISTINCT CategoryName` | ✅ confirmed |
| **Single currency (MXN)** | `SELECT DISTINCT CurrencyCode` → **MXN only** (126,524 / 126,524 rows) | ⚠️ **corrected** — an earlier draft told the agent to "convert currencies with DimCurrencyExchange"; the data has one currency and that table is disconnected, so the instruction was **removed/fixed** |
| "Temporada de rebajas" = Oct+Nov (DimDate[Month] IN {10,11}) | `DimDate[Month]` is int64 with values 1–12; Oct+Nov 2024 = 1,844,999 MXN (non-zero) via `executeQueries` | ✅ months exist with data. Business *definition* stipulated for the [ablation test](../../data-agent/ablation-test-design.md) — the field/filter is real |
| "Programa Aurora" = Electrónica + Electrodomésticos | `VALUES(DimProduct[CategoryName])` → those two values exist; Aurora 2024 = 3,489,973 + 2,085,640 = **5,575,613** MXN via `executeQueries` | ✅ category values exist. Internal-code *definition* for the test (unguessable by the LLM) — the field/values are real |

> The currency case is the point: a plausible-sounding instruction would have sent the agent to
> convert amounts that never need converting, using a table with no relationship. Verifying against
> the data turned a harmful instruction into a correct one.

## The block (paste this)

Grouped by theme with a business-context lead, per Microsoft's
[AI-instructions best practices](https://learn.microsoft.com/power-bi/create-reports/copilot-prepare-data-ai-instructions#write-effective-prompts-for-ai-instructions)
(be explicit, avoid ambiguity, group related instructions under headers, set business context).

```
You are a retail sales analyst for Contoso, a (synthetic) retail business. Answer questions about sales, profitability, customers, products, and stores using this semantic model. Be precise, use the model's defined measures, and never invent numbers, measures, or fields that are not in the model.

## Dates
- Use DimDate[Date] for all time analysis; it is related to FactSales[OrderDate]. FactSales[DeliveryDate] is logistics only (deliveries can spill into early 2025) — never use it for sales trends.
- The reporting period is 2023-01-01 to 2024-12-31. If unsure, confirm with MIN/MAX of DimDate[Date].

## Seasonal campaigns
- Contoso's 'temporada de rebajas de fin de año' (end-of-year sale season) covers ONLY October and November (DimDate[Month] = 10 or 11); it excludes December. For questions about this campaign, filter DimDate[Month] IN {10, 11}.

## Internal segments
- Contoso's 'Programa Aurora' groups ONLY the product categories Electrónica and Electrodomésticos. For questions about Programa Aurora, filter DimProduct[CategoryName] to those two categories and include no others.

## Measures and how to aggregate
- Revenue is the measure [Total Sales]. Never re-aggregate a raw column when a measure exists.
- "Margin" is ambiguous: use [Gross Margin] for the absolute amount and [Margin %] for the rate — always say which one you used.
- Additive measures that MAY be summed across rows: [Total Sales], [Total Quantity], [Total Cost], [Gross Margin].
- Non-additive measures that must NEVER be summed (recompute them in context): [Margin %], [Average Order Value], [Average Selling Price], [Units per Order], [% of Total Sales], [Sales YoY %].
- [Orders] and [Distinct Customers] are distinct counts (semi-additive) — do not sum them across periods.
- For per-customer figures ([Sales per Customer]), state the denominator (Distinct Customers = N); it is not the total customer base.

## Dimensions and breakdowns
- When a breakdown is needed but the user names no dimension, break down by DimProduct[CategoryName], DimStore[CountryName], DimCustomer[Country], or FactSales[Channel] (values: Online, Store).
- Dimension values are in Spanish (e.g., product categories: Electrónica, Electrodomésticos, "Música, Películas y Medios", "Videojuegos y Juguetes").

## Currency
- All amounts are in a single currency, Mexican Peso (MXN); no conversion is needed. Do not use DimCurrencyExchange — it is a disconnected reference table.

## Output
- For rankings, breakdowns, or multiple measures, return a labeled table with units rather than prose.
```
