# Verification methodology — prove every claim before writing it

The rule: **no instruction is written until it is proven** against the model and its real data. Split
each claim into *structural* (TMDL) or *data* (query the source) and check it.

## Structural claims → check the TMDL (no query needed)

| Claim type | Where to check |
|---|---|
| "X is the primary date, related to Fact[Date]" | `definition/relationships.tmdl` — confirm the relationship exists (and which is active) |
| "Use [Measure] for X" / additivity | `tables/_Measures.tmdl` (or wherever measures live) — read the DAX: `SUM`/`SUMX` ⇒ additive; `DIVIDE`/ratios/% ⇒ non-additive; `DISTINCTCOUNT` ⇒ semi-additive |
| "Break down by Dim[Col]" | the table's `.tmdl` — confirm the column exists |
| "Table Y is disconnected / don't use it to convert" | `relationships.tmdl` — confirm Y has no relationship to the fact |
| Ratio denominators ("state Distinct Customers = N") | the ratio measure's DAX — confirm the denominator measure |

## Data claims → query the source

You must read the real data. The source is usually Parquet/CSV (an M parameter like `DataBaseUrl` +
`Web.Contents`/`File.Contents` in the partitions) or a database. Query it directly — **duckdb** over
Parquet is fast and dependency-light:

```python
import duckdb
con = duckdb.connect()
# reporting period
con.execute("SELECT min(OrderDate), max(OrderDate) FROM 'FactSales.parquet'").fetchall()
# is it really multi-currency? (this is the classic trap)
con.execute("SELECT DISTINCT CurrencyCode FROM 'FactSales.parquet'").fetchall()
# real dimension values (for example values + language)
con.execute("SELECT DISTINCT CategoryName FROM 'DimProduct.parquet' ORDER BY 1").fetchall()
# grain sanity: distinct keys vs row count
con.execute("SELECT count(*), count(DISTINCT OrderKey) FROM 'FactSales.parquet'").fetchall()
```

Claims that MUST be data-verified (these are where drafts go wrong):
- **Reporting period** — MIN/MAX of the date; don't trust the config.
- **Currency** — DISTINCT of the currency column. *A single-currency dataset makes "convert
  currencies / don't mix" instructions false and harmful.* (Real case: a draft told the agent to
  convert with a `DimCurrencyExchange` table; the data was single-currency MXN and that table was
  disconnected → removed.)
- **Dimension values & language** — DISTINCT of key dimension columns (also gives real example values
  and tells you the language of the data, e.g. Spanish categories).
- **Grain** — distinct keys vs row count (e.g. "1 line per order" vs "many lines per order").
- **Channels / categorical enums** you reference as example values.

## Output of verification
A short table: each claim → how verified → confirmed / corrected. Keep it (mirror it into
`prep-for-ai/ai-instructions.md`). The corrections are the highest-value, most credible part —
they prove the instructions are real, not generated.
