# Ablation — raw run captures (evidence)

Verbatim answers from the published Data Agent's MCP endpoint. Kept for
reproducibility behind [`ablation-prep-for-ai.md`](ablation-prep-for-ai.md).
Data is synthetic (Contoso); figures are in MXN.

## Round A — V2 (no Prep-for-AI)

**Q1 — total sales 2024**
> Total sales for 2024 were $10,387,132. The currency is Mexican Peso (MXN).
> ```DAX
> EVALUATE
> SUMMARIZECOLUMNS(
>     'DimDate'[Year],
>     FILTER('DimDate', 'DimDate'[Year] = 2024),
>     "Total Sales 2024", [Total Sales]
> )
> ```

**Q2 — margin % 2024**
> The margin percentage for all sales in 2024 is 19.6%.
> Margin % = DIVIDE([Gross Margin], [Total Sales]) — context filtered to 2024
> (DimDate[Date] within 2024-01-01 to 2024-12-31).

**Q3 — sales by category 2024**
> | Categoría | Ventas Totales 2024 |
> |---|---|
> | Electrodomésticos | $2,085,640 |
> | Electrónica | $3,489,973 |
> | Música, Películas y Medios | $1,882,478 |
> | Videojuegos y Juguetes | $2,929,040 |
> ```DAX
> EVALUATE
> SUMMARIZECOLUMNS(
>     'DimProduct'[Category],
>     FILTER('DimDate', 'DimDate'[Year] = 2024),
>     "Ventas Totales 2024", [Total Sales]
> )
> ORDER BY [Ventas Totales 2024] DESC
> ```
> (⚠️ `'DimProduct'[Category]` is not a real column — the real one is `CategoryName`.)

## Round B — ContosoRetail (with Prep-for-AI)

**Q1 — total sales 2024**
> Total sales in 2024 were $10,387,132 Mexican Pesos (MXN).
> `CALCULATE([Total Sales], YEAR(DimDate[Date]) = 2024)`

**Q2 — margin % 2024**
> The margin percentage for 2024 is 19.6%.
> ```DAX
> EVALUATE
> SUMMARIZECOLUMNS('DimDate'[Year], "Margin %", [Margin %]) WHERE 'DimDate'[Year] = 2024
> ```
> (⚠️ `SUMMARIZECOLUMNS(...) WHERE` is not valid DAX — the "shown" query is an LLM
> reconstruction, not the literal executed query.)

**Q3 — sales by category 2024**
> | Categoría | Total de Ventas |
> |---|---|
> | Electrodomésticos | $2,085,640 |
> | Electrónica | $3,489,973 |
> | Música, Películas y Medios | $1,882,478 |
> | Videojuegos y Juguetes | $2,929,040 |
> ```DAX
> EVALUATE
> SUMMARIZECOLUMNS(
>     DimProduct[CategoryName],
>     FILTER(DimDate, YEAR(DimDate[Date]) = 2024),
>     "Total Sales", [Total Sales]
> )
> ```

## Round C — bare Agent instructions (two separate agents)

Both agents given only: *"You are a retail sales analyst for Contoso. Answer questions
about the ContosoRetail semantic model."* Run against each agent's MCP endpoint.

### C-A — V2 agent (bare, no Prep-for-AI)

**Q1** > Total sales in 2024 were $10,387,132. The currency is Mexican Peso (MXN).
> `CALCULATE([Total Sales], DimDate[Year] = 2024)` *(sample; said it doesn't run DAX directly)*

**Q2** > The margin percentage for 2024 is 19.6%.
> `DIVIDE(SUM('FactSales'[GrossMargin]), SUM('FactSales'[SalesAmount]))` ⚠️ invented column names

**Q3** > Electrodomésticos 2,085,640.04 · Electrónica 3,489,972.79 · Música/Películas 1,882,478.29 · Videojuegos 2,929,040.46
> `SUMMARIZECOLUMNS(DimProduct[Category], FILTER(DimDate,[Year]=2024), "Total Sales 2024", SUM(FactSales[SalesAmount]))` ⚠️ `[Category]` / `[SalesAmount]` do not exist

### C-B — ContosoRetail agent (bare, with Prep-for-AI)

**Q1** > Total sales in 2024 were $10,387,132 MXN.
> `SUMMARIZECOLUMNS('DimDate'[Year], FILTER('DimDate','DimDate'[Year]=2024), "Total Sales",[Total Sales], "Currency", SELECTEDVALUE('DimCurrency'[CurrencyCode]))` ✅ real names

**Q2** > The margin percentage for 2024 is 19.6%. *(declined to show DAX)*

**Q3** > Electrónica $3,489,973 · Videojuegos $2,929,040 · Electrodomésticos $2,085,640 · Música/Películas $1,882,478
> `SUMMARIZECOLUMNS('DimProduct'[CategoryName], FILTER('DimDate',[Year]=2024), "Total Sales 2024",[Total Sales])` ✅ real `CategoryName`

**Round C takeaway:** identical numbers, MXN and Spanish in BOTH even with a bare prompt —
those come from the model (format string / data values / defined measures), not the
instructions. (The DAX schema-name difference seen in the *shown* DAX above was later
RETRACTED — see the corrected verdict in `ablation-prep-for-ai.md`: in the executed query
both agents use `DimProduct[CategoryName]`; the invented name was reconstruction noise.)

## Round D — ambiguous questions, via MCP (production path)

Two bare agents, two ambiguous questions.

| Question | V2 (no Prep) | ContosoRetail (Prep) |
|---|---|---|
| ¿Cuál es el margen total? | El margen total es $3,938,789. | El margen total de la empresa es de $3,938,789 MXN. |
| ¿Cuáles son las ventas del último trimestre? | Las ventas del último trimestre (trimestre 4 de 2024) fueron de $2,653,095. | Las ventas totales del último trimestre disponible (Trimestre 4 de 2024) fueron de $2,653,095. |

Identical + correct via API. **Two-panes note:** the Prep agent's hedge + raw SQL +
*"cópiala y ejecútala en tu entorno"* came from **Build agent with AI** (the authoring
copilot), NOT from **Test data agent**. In **Test data agent** the Prep agent executed
clean DAX — margin returned both `[Gross Margin]` $3,938,789 and `[Margin %]` 19.8% —
matching the API. Evaluate on Test data agent / MCP, never on Build agent with AI.

## Cross-check (direct DAX, ground truth)

- Total Sales 2023 / 2024 = **9,516,546 / 10,387,132 MXN** — matches all rounds.
- Gross Margin (all) = **3,938,789** · Total Sales 2024-Q4 = **2,653,095** — matches Round D.
Verified via Power BI REST `POST /datasets/{modelId}/executeQueries`.
