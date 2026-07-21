[![Lang: English](https://img.shields.io/badge/lang-English-1f6feb?style=flat-square)](05-ontology-and-glossary.md)
[![Idioma: Español](https://img.shields.io/badge/idioma-Espa%C3%B1ol-2da44e?style=flat-square)](05-ontology-and-glossary.es.md)
&nbsp;·&nbsp; [↑ Index](../../README.md)

# 05 · Ontology & glossary

## What it is

The ontology is the **map from the words users say to the fields the model has**. Users ask about
"headcount," "churn," "the Northeast," "last quarter"; the model has `dimlocation[State]`,
`[Invoiced Workers]`, `CALENDAR[Date]`. The glossary closes that gap: synonyms, business definitions,
default groupings, and the canonical field behind each ambiguous term.

This is not a separate artifact you deploy — it is **distributed across the parts you already write**:
model metadata (table/column/measure descriptions), Prep-for-AI AI Instructions, agent-level
definitions, and Verified Answers. (Fabric also has a first-class *Ontology* source type, in preview,
for graph-style domain models — a different thing from the business glossary discussed here.)

## Why it matters

Ambiguity is where a Data Agent quietly goes wrong. "Show me performance by territory" resolves to a
`Territory` column in the product table when the user meant sales regions — valid query, wrong answer.
A glossary removes the guess:

- **Synonyms → one field.** "Headcount," "workers," "staff" all mean *Invoiced Workers* here, and
  saying so stops the agent from inventing a second population.
- **Definitions pin semantics.** "Profitability = Contribution Margin, not Gross Profit" makes the
  house convention the default instead of a coin flip among look-alike measures.
- **Default groupings** answer the unspoken part of a question. "Break down spend" with no dimension
  named should fall back to the *leadership dimensions*, not a random column.
- **Time language** ("last quarter," "peak season") needs an explicit definition or the agent picks a
  calendar it wasn't asked for.

## How to write it well

- **Describe every object in business language.** Descriptions on tables, columns, and measures are
  the agent's first dictionary — `Sales Region`, not `DIM_GEO_01`.
- **List real synonyms** users actually type, mapped to the one canonical field.
- **Define the loaded terms** — the metrics whose meaning is contested (profitability, active,
  churned, headcount) — and name the exact measure each resolves to.
- **State default breakdowns** so a dimension-less "break it down" is deterministic.
- **Use Verified Answers for the recurring ambiguous questions** — 5–7 trigger phrasings each — so the
  common cases short-circuit to a known-good structure.
- **Keep one source of truth.** Prefer the model's metadata + Prep for AI; use agent-level definitions
  only for cross-source terminology.

## Anti-pattern

**Relying on column names as the glossary** — trusting that `Territory` obviously means what the user
means, when the model has three plausible homes for the word. **Undefined loaded metrics**, where
"profitability" silently resolves to whichever margin measure sorts first. **Synonyms only in the
modeler's head**, so "headcount" never reaches *Invoiced Workers*. And **contradictory definitions**
scattered across model metadata, agent instructions, and Verified Answers that disagree — the agent
inherits the conflict.

## The Contoso example

Contoso encodes its glossary inside the [instructions](../../examples/contoso-vendor-spend/instructions.md)
and the model, not as a separate file:

- **The denominator term is pinned.** "Headcount" here means exactly one thing — **Invoiced Workers**
  (distinct workers with an invoice) — and the rules force any per-head ratio to name it, so "spend
  per worker" can't silently adopt a different population.
- **Default breakdown is declared.** When a question needs a breakdown and names no dimension, the
  agent falls back to the **leadership dimensions** (`Business Unit`, `Job Family`, `Country`,
  `Spend Type`) — the unspoken grouping made explicit.
- **Values are illustrated, not guessed.** `Spend Type` is `SOW` or `Staff Augmentation`; example
  suppliers are `Fabrikam`, `Northwind Traders`, `Adventure Works` — enough for the agent to
  recognize the vocabulary without pretending the list is exhaustive.
- **`::about` / `::catalog`** surface this glossary to users on demand, turning the ontology into a
  discoverable feature rather than hidden configuration.

---
_Next: [06 · Direct vs. orchestrator →](06-direct-vs-orchestrator.md)_
