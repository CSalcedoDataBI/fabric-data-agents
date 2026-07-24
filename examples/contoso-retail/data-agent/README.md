[![Lang: English](https://img.shields.io/badge/lang-English-1f6feb?style=flat-square)](README.md)
[![Idioma: Español](https://img.shields.io/badge/idioma-Espa%C3%B1ol-2da44e?style=flat-square)](README.es.md)

# Contoso Retail — Data Agent (worked example)

A complete, **sanitized** Fabric Data Agent over the [Contoso Retail semantic model](../model/),
used throughout [Anatomy of a Fabric Data Agent](../../../README.md). It is authored clean (not
extracted from a client) — see [SANITIZATION.md](../../../SANITIZATION.md).

## The scenario

**Contoso** runs a retail business. Every order line lands in a Power BI semantic model,
**ContosoRetail** (sales, cost, margin, customers, products, stores, channels). Business users want
to ask, in plain language: *"Sales by category?"*, *"Margin % by country?"*, *"Online vs Store
split?"*, *"What drove the change year over year?"* — without writing DAX.

## What goes where (the key lesson)

A Fabric Data Agent has an **agent layer** and a **source layer**. For a **semantic-model** source,
the NL2DAX generator relies **solely** on the model's metadata + **Prep-for-AI** — so the DAX-shaping
substance is configured on the **model**, and only routing/tone/steering lives on the agent.

| What you author | Where it lives | File |
|---|---|---|
| Identity + Fabric resource IDs | Agent | [`agent.config.json`](agent.config.json) |
| The semantic-model source (NL2DAX) | Agent | [`data-sources.yaml`](data-sources.yaml) |
| Role, scope, tone, output shape, `::` commands | Agent | [`instructions.md`](instructions.md) |
| Additivity, measure semantics, breakdown & currency rules | **Model** (Prep-for-AI) | [`../model/prep-for-ai/ai-instructions.md`](../model/prep-for-ai/ai-instructions.md) |
| Table/column/measure visibility + synonyms | **Model** (Prep-for-AI) | [`../model/prep-for-ai/ai-data-schema.json`](../model/prep-for-ai/ai-data-schema.json) |
| Governed, tested Q→DAX few-shots | **Model** (Verified Answers) | [`verified-answers.md`](verified-answers.md) · mirror in [`example-queries.json`](example-queries.json) |

> This is the correction that distinguishes this example: **data-source instructions and example
> queries set at the *agent* level are ignored** for a semantic-model source. Put that substance on
> the model, where the generator actually reads it. See
> [04 · Source instructions & few-shots](../../../docs/anatomy/04-source-instructions-and-fewshots.md).

> **Nuance — measured, not assumed.** The top-level **Agent instructions** (the system prompt) are a
> different thing from per-source *data-source instructions*, and they **do** shape the answer — the
> orchestrator reads them and can reformulate the question before the DAX generator ever sees it. In a
> controlled A/B ([`ablation-prep-for-ai.md`](ablation-prep-for-ai.md)), the same agent hitting a
> model **without** Prep-for-AI still honored currency, non-additivity and Spanish values — because
> those guardrails were in the Agent instructions and in the model itself. On these clean, literal
> questions there was **no reproducible Prep-for-AI difference**: numbers, currency, language and the
> *executed* DAX were identical. Prep-for-AI earns its keep on terms the model cannot infer — business
> jargon, internal codes, duplicate measures — see
> [`prep-for-ai-reference.md`](prep-for-ai-reference.md).

## Patterns this example demonstrates

- **Additive vs non-additive discipline** — *Total Sales* / *Gross Margin* can be summed; *Margin %*,
  *Average Order Value*, *% of Total Sales*, *Sales YoY %* cannot, ever.
- **Distinct-count semi-additivity** — *Orders* and *Distinct Customers* are not summed across periods.
- **Per-customer-ratio denominator caveat** — *Sales per Customer* always names its denominator.
- **Single-currency rule (verified)** — all amounts are MXN; *DimCurrencyExchange* is disconnected and
  must not be used. A plausible-sounding "convert currencies" instruction was removed after checking
  the data — the point of the whole example.
- **Spanish dimension values** — categories and other labels are in Spanish; the agent is told so.
- **`::` steering commands** — `::about`, `::catalog`, `::improve`, `::validate`, `::drivers`.

## The model at a glance

- **Fact:** `FactSales` (grain: one order line; Date × Category × Country × Channel)
- **Measures (15):** Total Sales, Total Quantity, Total Cost, Gross Margin, Orders, Distinct
  Customers, Margin %, Average Order Value, Average Selling Price, Units per Order, Sales per
  Customer, % of Total Sales, Sales YTD, Sales PY, Sales YoY %
- **Default breakdown dims:** Product Category, Store Country, Customer Country, Channel
- **Period:** 2023-01-01 → 2024-12-31 · **Currency:** MXN only · **Channels:** Online, Store

> Every ID in `agent.config.json` and `data-sources.yaml` is a `<placeholder>`. Fill them with your
> own Fabric workspace/model/agent GUIDs when you provision — see
> [07 · Provisioning](../../../docs/anatomy/07-provisioning.md). The published model is named
> `ContosoRetail` in your workspace.
