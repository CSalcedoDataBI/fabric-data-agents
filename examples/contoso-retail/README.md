[![Lang: English](https://img.shields.io/badge/lang-English-1f6feb?style=flat-square)](README.md)
[![Idioma: Español](https://img.shields.io/badge/idioma-Espa%C3%B1ol-2da44e?style=flat-square)](README.es.md)
&nbsp;·&nbsp; [↑ Index](../../README.md)

# Contoso Retail — a real, reproducible example dataset

This is a **real, generated retail dataset** — not a described schema. It is the second worked
example in this reference (alongside [Contoso Vendor Spend](../contoso-vendor-spend/), which is
VMS/staffing). Where that one teaches the patterns over an *authored* model, this one grounds them in
a dataset you can **regenerate byte-for-byte** and load into Fabric yourself.

The data is produced by **[Contoso Universe Generator (CUG)](https://github.com/CSalcedoDataBI/contoso-universe-gen)**
— a Python-native synthetic-data tool — which itself stands on the shoulders of **SQLBI's**
[Contoso Data Generator V2](https://github.com/sql-bi/Contoso-Data-Generator-V2) (Marco Russo &
Alberto Ferrari). It is **100% synthetic**: Faker-generated names, addresses, and products — no real
person or company.

## Reproduce it (deterministic)

The exact config is committed at [`config/contoso-retail-ref-es.toml`](config/contoso-retail-ref-es.toml).
Same config + same seed = same data, always.

```bash
# with CUG installed (see its repo)
cug generate -c config/contoso-retail-ref-es.toml -o ./output
```

- **Locale:** `es` (Spanish names/categories; currencies incl. MXN/USD/EUR)
- **Seed:** `42` · **Reporting period:** `2023-01-01` → `2024-12-31` (parallels the vendor-spend example)
- **Scale:** ~126k sales lines, 12k customers, 137 products, 25 stores (lean by design — a teaching
  dataset, not a scale test; regenerate at any size by changing `orders_count`)
- **Format:** Parquet (compact, columnar — the natural lakehouse format). Add CSV/DuckDB/Delta with
  `-f csv,duckdb,delta`.

## Schema — a classic retail star

`data/*.parquet`:

| Table | Grain | Key columns |
|---|---|---|
| **FactSales** | one order line | `OrderKey`, `LineNumber`, `OrderDate`, `CustomerKey`, `StoreKey`, `ProductKey`, `Channel`, `Quantity`, `UnitPrice`, `NetPrice`, `UnitCost`, `CurrencyCode` |
| **DimProduct** | product | `ProductKey`, `ProductName`, `Brand`, `Manufacturer`, `CategoryName`, `SubCategoryName`, `Cost`, `Price` |
| **DimCustomer** | customer | `CustomerKey`, `GivenName`, `Surname`, `City`, `State`, `Country`, `Gender`, `Age`, `Occupation` |
| **DimStore** | store / channel | `StoreKey`, `StoreCode`, `CountryName`, `Description`, `Status`, `SquareMeters` |
| **DimDate** | day | `DateKey`, `Date`, `Year`, `Quarter`, `Month`, `MonthName`, `IsHoliday`, `IsWorkingDay` |
| **DimCurrency** | currency | `CurrencyKey`, `CurrencyCode`, `CurrencyName`, `Symbol` |
| **DimCurrencyExchange** | currency × day | `Date`, `FromCurrency`, `ToCurrency`, `Exchange` |

`FactSales` joins to the dimensions on their `*Key` columns; `DimDate` on `OrderDate`/`DeliveryDate`.

## What comes next (this is issue [#4](https://github.com/CSalcedoDataBI/fabric-data-agents/issues/4))

This folder holds the **dataset** only. The teaching semantic model (additive vs. non-additive
measures, companion measures, a per-head ratio with a named denominator, leadership dimensions) and
the Data Agent config (`agent.config.json`, `data-sources.yaml`, `instructions.md`,
`example-queries.json`) are built on top of it in issues #5 and #6 — mirroring the structure of
[`../contoso-vendor-spend/`](../contoso-vendor-spend/) and the anatomy in
[`docs/anatomy/`](../../docs/anatomy/00-overview.md).

## Attribution & license

- Data generator: [CUG](https://github.com/CSalcedoDataBI/contoso-universe-gen) — MIT.
- Original Contoso concept & schema realism: [SQLBI Contoso Data Generator V2](https://github.com/sql-bi/Contoso-Data-Generator-V2).
- See this repo's [SANITIZATION.md](../../SANITIZATION.md): the dataset is synthetic by construction —
  there is no client data to leak.
