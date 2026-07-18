[![Lang: English](https://img.shields.io/badge/lang-English-1f6feb?style=flat-square)](README.md)
[![Idioma: Español](https://img.shields.io/badge/idioma-Espa%C3%B1ol-2da44e?style=flat-square)](README.es.md)

# Contoso Vendor Spend — worked example

A complete, **sanitized** Fabric Data Agent used throughout [Anatomy of a Fabric Data Agent](../../README.md).
It is authored clean (not extracted from a client) — see [SANITIZATION.md](../../SANITIZATION.md).

## The scenario

**Contoso** runs a contingent workforce: it hires temporary staff through staffing suppliers. Every
invoice line lands in a Power BI semantic model, **Contoso Vendor Spend (SM)**. Business users want
to ask, in plain language: *"Top 5 suppliers by spend last year?"*, *"SOW vs Staff Augmentation
split?"*, *"What drove the jump in spend?"* — without writing DAX.

## The files (the four parts you author)

| File | Anatomy part | What it holds |
|---|---|---|
| [`agent.config.json`](agent.config.json) | 01, 07 | Identity + Fabric resource IDs (placeholders) |
| [`data-sources.yaml`](data-sources.yaml) | 02 | The semantic-model source (NL2DAX) |
| [`instructions.md`](instructions.md) | 03 | Role, additivity rules, companion-measure rule, `::` commands |
| [`example-queries.json`](example-queries.json) | 04 | Few-shots that pin down measure/period/grain/breakdown |

## Patterns this example demonstrates

- **Companion measures reported together** — ask for *Total Spend* and you also get *Invoiced Workers*
  and *Assignments*, unless you say "only".
- **Additive vs. non-additive discipline** — *Total Spend* can be summed; *Average Invoice* and
  *% of Total Spend* cannot, ever.
- **Leadership-dimension defaults** — an unqualified "break it down" defaults to Business Unit /
  Job Family / Country / Spend Type.
- **Per-head-ratio denominator caveat** — *Spend per Invoiced Worker* always names its denominator,
  so nobody mistakes it for spend per active employee.
- **`::` steering commands** — `::about`, `::catalog`, `::improve`, `::validate`, `::drivers` let a
  user drive the agent instead of re-typing long prompts.

## The model at a glance

- **Fact:** `factspend` (grain: Date × Business Unit × Job Family × Country × Spend Type)
- **Measures:** Total Spend, Invoiced Workers, Suppliers with Spend, Assignments, Average Invoice,
  Spend per Invoiced Worker, % of Total Spend
- **Leadership dims:** Business Unit, Job Family, Country, Spend Type
- **Period:** 2023–2024 · **Suppliers (examples):** Fabrikam, Northwind Traders, Adventure Works

> Every ID in `agent.config.json` and `data-sources.yaml` is a `<placeholder>`. Fill them with your
> own Fabric workspace/model/agent GUIDs when you provision — see
> [07 · Provisioning](../../docs/anatomy/07-provisioning.md).
