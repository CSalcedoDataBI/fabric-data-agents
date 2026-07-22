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

> The currency case is the point: a plausible-sounding instruction would have sent the agent to
> convert amounts that never need converting, using a table with no relationship. Verifying against
> the data turned a harmful instruction into a correct one.

## The block (paste this)

```
* Primary date: use DimDate[Date] for all time analysis; it is related to FactSales[OrderDate]. FactSales[DeliveryDate] is logistics only (deliveries can spill into early 2025) — do not use it for sales trends.
* Reporting period is 2023-01-01 through 2024-12-31 (verified against MIN/MAX of DimDate[Date]).
* Revenue is the measure [Total Sales]. Never re-aggregate a raw column when a measure exists.
* "Margin" is ambiguous: use [Gross Margin] for the absolute amount and [Margin %] for the rate — state which you used.
* Additive measures that may be summed: [Total Sales], [Total Quantity], [Total Cost], [Gross Margin]. NEVER sum non-additive measures (ratios/percentages): [Margin %], [Average Order Value], [Average Selling Price], [Units per Order], [% of Total Sales], [Sales YoY %].
* [Orders] and [Distinct Customers] are distinct counts (semi-additive) — do not sum them across periods.
* For per-customer figures ([Sales per Customer]), state the denominator (Distinct Customers = N); it is not the total customer base.
* When a breakdown is needed but no dimension is named, break down by DimProduct[CategoryName], DimStore[CountryName], DimCustomer[Country], or FactSales[Channel] (values: Online, Store).
* All amounts are in a single currency — Mexican Peso (MXN); no conversion is needed. Do not use DimCurrencyExchange (it is a disconnected reference table).
* Dimension values are in Spanish (e.g., product categories: Electrónica, Electrodomésticos, "Música, Películas y Medios", "Videojuegos y Juguetes").
* Prefer labeled tables with units for rankings, breakdowns, or multiple measures.
```
