[![Lang: English](https://img.shields.io/badge/lang-English-1f6feb?style=flat-square)](README.md)
[![Idioma: Español](https://img.shields.io/badge/idioma-Espa%C3%B1ol-2da44e?style=flat-square)](README.es.md)
&nbsp;·&nbsp; [↑ Índice](../../README.es.md)

# Contoso Retail — un dataset de ejemplo real y reproducible

Este es un **dataset retail real y generado** — no un esquema descrito. Es el segundo ejemplo trabajado
de esta referencia (junto a [Contoso Vendor Spend](../contoso-vendor-spend/README.es.md), que es
VMS/staffing). Donde aquel enseña los patrones sobre un modelo *autorado*, este los ancla en un dataset
que puedes **regenerar idéntico** y cargar en Fabric tú mismo.

Los datos los produce **[Contoso Universe Generator (CUG)](https://github.com/CSalcedoDataBI/contoso-universe-gen)**
— una herramienta de datos sintéticos nativa de Python — que a su vez se apoya en el
[Contoso Data Generator V2](https://github.com/sql-bi/Contoso-Data-Generator-V2) de **SQLBI** (Marco
Russo y Alberto Ferrari). Es **100% sintético**: nombres, direcciones y productos generados por Faker
— ninguna persona ni empresa real.

## Reprodúcelo (determinista)

La config exacta está commiteada en [`config/contoso-retail-ref-es.toml`](config/contoso-retail-ref-es.toml).
Misma config + misma seed = mismos datos, siempre.

```bash
# con CUG instalado (ver su repo)
cug generate -c config/contoso-retail-ref-es.toml -o ./output
```

- **Locale:** `es` (nombres/categorías en español; monedas incl. MXN/USD/EUR)
- **Seed:** `42` · **Periodo:** `2023-01-01` → `2024-12-31` (paralelo al ejemplo vendor-spend)
- **Escala:** ~126k líneas de venta, 12k clientes, 137 productos, 25 tiendas (liviano a propósito — un
  dataset de enseñanza, no una prueba de escala; regenera a cualquier tamaño cambiando `orders_count`)
- **Formato:** Parquet (compacto, columnar — el formato natural de lakehouse). Añade CSV/DuckDB/Delta
  con `-f csv,duckdb,delta`.

## Esquema — un star retail clásico

`data/*.parquet`:

| Tabla | Grano | Columnas clave |
|---|---|---|
| **FactSales** | una línea de orden | `OrderKey`, `LineNumber`, `OrderDate`, `CustomerKey`, `StoreKey`, `ProductKey`, `Channel`, `Quantity`, `UnitPrice`, `NetPrice`, `UnitCost`, `CurrencyCode` |
| **DimProduct** | producto | `ProductKey`, `ProductName`, `Brand`, `Manufacturer`, `CategoryName`, `SubCategoryName`, `Cost`, `Price` |
| **DimCustomer** | cliente | `CustomerKey`, `GivenName`, `Surname`, `City`, `State`, `Country`, `Gender`, `Age`, `Occupation` |
| **DimStore** | tienda / canal | `StoreKey`, `StoreCode`, `CountryName`, `Description`, `Status`, `SquareMeters` |
| **DimDate** | día | `DateKey`, `Date`, `Year`, `Quarter`, `Month`, `MonthName`, `IsHoliday`, `IsWorkingDay` |
| **DimCurrency** | moneda | `CurrencyKey`, `CurrencyCode`, `CurrencyName`, `Symbol` |
| **DimCurrencyExchange** | moneda × día | `Date`, `FromCurrency`, `ToCurrency`, `Exchange` |

`FactSales` une con las dimensiones por sus columnas `*Key`; `DimDate` por `OrderDate`/`DeliveryDate`.

## El modelo, y qué sigue

Esta carpeta contiene el **dataset** (issue [#4](https://github.com/CSalcedoDataBI/fabric-data-agents/issues/4)).
El modelo semántico de enseñanza **ya está construido** encima, en [`model/`](model/README.es.md) — una
estrella retail con un contenedor `_Measures` categórico (issue [#5](https://github.com/CSalcedoDataBI/fabric-data-agents/issues/5)).
**Abre [`model/ContosoRetail.pbix`](model/) para verlo con los datos embebidos** (sin configurar nada);
este es el modelo que usamos para **evaluar** todo lo que la referencia afirma sobre un Fabric Data Agent.

La **config del Data Agent ya está construida** sobre este modelo en
[`data-agent/`](data-agent/README.es.md) (issue
[#6](https://github.com/CSalcedoDataBI/fabric-data-agents/issues/6)) — `agent.config.json`,
`data-sources.yaml`, `instructions.md`, `example-queries.json`, más un
[`verified-answers.md`](data-agent/verified-answers.md) listo para copiar-pegar. Refleja
[`../contoso-vendor-spend/`](../contoso-vendor-spend/README.es.md) pero muestra el **placement
corregido** para una fuente semantic-model: la sustancia que da forma al DAX (aditividad, semántica
de medidas, regla de moneda) se configura en el **Prep-for-AI del modelo**
([`model/prep-for-ai/`](model/prep-for-ai/)), no en el agente — ver la anatomía en
[`docs/anatomy/`](../../docs/anatomy/00-overview.es.md).

## Atribución y licencia

- Generador de datos: [CUG](https://github.com/CSalcedoDataBI/contoso-universe-gen) — MIT.
- Concepto Contoso original y realismo del esquema: [SQLBI Contoso Data Generator V2](https://github.com/sql-bi/Contoso-Data-Generator-V2).
- Ver [SANITIZATION.md](../../SANITIZATION.md) de este repo: el dataset es sintético por construcción —
  no hay datos de cliente que filtrar.
