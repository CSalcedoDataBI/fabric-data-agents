[![Lang: English](https://img.shields.io/badge/lang-English-1f6feb?style=flat-square)](05-ontology-and-glossary.md)
[![Idioma: Español](https://img.shields.io/badge/idioma-Espa%C3%B1ol-2da44e?style=flat-square)](05-ontology-and-glossary.es.md)
&nbsp;·&nbsp; [↑ Index](../../README.md)

# 05 · Ontology & glossary

## What it is

The ontology is the **map from the words users say to the fields the model has**. Users ask about
"customers," "churn," "the North," "last quarter"; the model has `DimCustomer[Country]`,
`[Distinct Customers]`, `DimDate[Date]`. The glossary closes that gap: synonyms, business definitions,
default groupings, and the canonical field behind each ambiguous term.

This is not a separate artifact you deploy — it is **distributed across the parts you already write**:
model metadata (table/column/measure descriptions), Prep-for-AI AI Instructions, agent-level
definitions, and Verified Answers. (Fabric also has a first-class *Ontology* source type, in preview,
for graph-style domain models — a different thing from the business glossary discussed here.)

## Why it matters

Ambiguity is where a Data Agent quietly goes wrong. "Show me performance by territory" resolves to a
`Territory` column in the product table when the user meant sales regions — valid query, wrong answer.
A glossary removes the guess:

- **Synonyms → one field.** "Customers," "buyers," "shoppers" all mean *Distinct Customers* here, and
  saying so stops the agent from inventing a second population.
- **Definitions pin semantics.** "Margin = `[Gross Margin]` for the amount, `[Margin %]` for the rate"
  makes the house convention the default instead of a coin flip among look-alike measures.
- **Default groupings** answer the unspoken part of a question. "Break down sales" with no dimension
  named should fall back to a *declared* set, not a random column.
- **Time language** ("last quarter," "peak season") needs an explicit definition or the agent picks a
  calendar it wasn't asked for.

## How to write it well

- **Describe every object in business language.** Descriptions on tables, columns, and measures are
  the agent's first dictionary — `Sales Region`, not `DIM_GEO_01`.
- **List real synonyms** users actually type, mapped to the one canonical field.
- **Define the loaded terms** — the metrics whose meaning is contested (profitability, active,
  churned, margin) — and name the exact measure each resolves to.
- **State default breakdowns** so a dimension-less "break it down" is deterministic.
- **Use Verified Answers for the recurring ambiguous questions** — 5–7 trigger phrasings each — so the
  common cases short-circuit to a known-good structure.
- **Keep one source of truth.** Prefer the model's metadata + Prep for AI; use agent-level definitions
  only for cross-source terminology.

## Anti-pattern

**Relying on column names as the glossary** — trusting that `Territory` obviously means what the user
means, when the model has three plausible homes for the word. **Undefined loaded metrics**, where
"profitability" silently resolves to whichever margin measure sorts first. **Synonyms only in the
modeler's head**, so "shoppers" never reaches *Distinct Customers*. And **contradictory definitions**
scattered across model metadata, agent instructions, and Verified Answers that disagree — the agent
inherits the conflict.

## The Contoso example

Contoso encodes its glossary inside the [instructions](../../examples/contoso-retail/data-agent/instructions.md)
and the model, not as a separate file:

- **The denominator term is pinned.** "Customers" here means exactly one thing — **`[Distinct Customers]`**
  (customers who bought in the period, not the rows of `DimCustomer`) — and the rules force any
  per-capita ratio to name it, so "sales per customer" can't silently adopt a different population.
- **Default breakdown is declared.** When a question needs a breakdown and names no dimension, the
  agent falls back to a declared set (`DimProduct[CategoryName]`, `DimStore[CountryName]`,
  `DimCustomer[Country]`, `FactSales[Channel]`) — the unspoken grouping made explicit.
- **Values are illustrated, not guessed.** `FactSales[Channel]` is `Online` or `Store`; category
  values are **in Spanish** (`Electrónica`, `Electrodomésticos`) — stating this stops the agent from
  filtering on `Electronics` and returning an empty result.
- **`::about` / `::catalog`** surface this glossary to users on demand, turning the ontology into a
  discoverable feature rather than hidden configuration.

---
_Next: [06 · Direct vs. orchestrator →](06-direct-vs-orchestrator.md)_
