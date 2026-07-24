# Contoso Retail — Verified Answers (paste-ready)

**Verified Answers** pin a natural-language question to a specific, human-approved DAX query. For a
**semantic-model source**, this is where few-shots actually influence the Data Agent — an
`example-queries.json` set at the *agent* level is ignored for NL2DAX, so the Q→DAX pairs below are
seeded on the **model** instead. See
[04 · Source instructions & few-shots](../../../docs/anatomy/04-source-instructions-and-fewshots.md).

## How to apply

Power BI Desktop → open **ContosoRetail** → **Home → Prep data for AI** → **Verified answers** →
**+ Add** → paste the **question** and its **DAX**, run it to confirm the shape, then **Save**.
Repeat for each of the five below. (Verified Answers are stored at the report layer, so this step is
manual in Desktop and confirmed with a live run — it is not written into TMDL.)

> Every query uses only measures and columns that exist in the model (verified against
> `_Measures.tmdl` and the dimension tables). The **result values** are computed live by the model
> when you run each query — confirm the returned shape below, don't hardcode numbers.

---

### 1. Sales by product category

**Question:** `Sales by product category`

```dax
EVALUATE
SUMMARIZECOLUMNS(
    DimProduct[CategoryName],
    "Total Sales", [Total Sales],
    "% of Total Sales", [% of Total Sales]
)
ORDER BY [Total Sales] DESC
```

**Returns:** one row per category (4 rows — the categories are in Spanish: Electrónica,
Electrodomésticos, "Música, Películas y Medios", "Videojuegos y Juguetes"), with revenue and its
share of the total. `[% of Total Sales]` is recomputed per row, never summed.

---

### 2. Margin % by store country

**Question:** `Margin % by store country`

```dax
EVALUATE
SUMMARIZECOLUMNS(
    DimStore[CountryName],
    "Gross Margin", [Gross Margin],
    "Margin %", [Margin %]
)
ORDER BY [Gross Margin] DESC
```

**Returns:** one row per store country, with absolute `[Gross Margin]` and the `[Margin %]` rate.
The rate is non-additive — it is recomputed per country and must never be summed across the column.

---

### 3. Monthly sales trend for 2024 with year-over-year change

**Question:** `Monthly sales trend for 2024 with year over year change`

```dax
EVALUATE
SUMMARIZECOLUMNS(
    DimDate[YearMonth],
    DimDate[MonthName],
    FILTER(ALL(DimDate[Year]), DimDate[Year] = 2024),
    "Total Sales", [Total Sales],
    "Sales PY", [Sales PY],
    "Sales YoY %", [Sales YoY %]
)
ORDER BY DimDate[YearMonth]
```

**Returns:** 12 rows (2024 months), each with the month's sales, the same month one year earlier
(`[Sales PY]`, from 2023), and the growth rate `[Sales YoY %]`. Time analysis runs over
`DimDate[Date]` (related to `FactSales[OrderDate]`), never `DeliveryDate`.

---

### 4. Top 10 products by sales

**Question:** `Top 10 products by sales`

```dax
EVALUATE
TOPN(
    10,
    SUMMARIZECOLUMNS(DimProduct[ProductName], "Total Sales", [Total Sales]),
    [Total Sales], DESC
)
ORDER BY [Total Sales] DESC
```

**Returns:** the 10 highest-revenue products, ranked descending. A ranking → a labeled table with
the measure column named.

---

### 5. Online vs Store split of total sales

**Question:** `Online vs Store split of total sales`

```dax
EVALUATE
SUMMARIZECOLUMNS(
    FactSales[Channel],
    "Total Sales", [Total Sales],
    "Orders", [Orders],
    "% of Total Sales", [% of Total Sales]
)
ORDER BY [Total Sales] DESC
```

**Returns:** two rows (`Online`, `Store`), with revenue, order count, and each channel's share of
total sales. `[Orders]` is a distinct count — do not sum it across periods.

---

> **Why these five.** Each one exercises a rule the agent must respect: a mix % that can't be summed
> (1, 5), a non-additive rate (2), a time-intelligence comparison (3), and a ranking (4). Seeding
> them as Verified Answers gives the NL2DAX generator a governed, tested pattern to match — the
> counterpart to the AI instructions in [`../model/prep-for-ai/`](../model/prep-for-ai/).
