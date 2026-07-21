[![Lang: English](https://img.shields.io/badge/lang-English-1f6feb?style=flat-square)](04-source-instructions-and-fewshots.md)
[![Idioma: Español](https://img.shields.io/badge/idioma-Espa%C3%B1ol-2da44e?style=flat-square)](04-source-instructions-and-fewshots.es.md)
&nbsp;·&nbsp; [↑ Index](../../README.md)

# 04 · Source instructions & few-shots

## What it is

Source-level context teaches the agent **how to query one specific source well**. It has two parts:

1. **Source instructions** — rules scoped to a single source (its schema quirks, join keys, filter
   conventions, preferred columns).
2. **Few-shots** — worked *question → query* pairs the translator matches against at run time. This is
   classic few-shot learning, and it is **the single biggest lever on accuracy**.

Where you author these depends on the source type — an asymmetry that trips up almost everyone:

- **Lakehouse / Warehouse / KQL:** author example queries and source instructions **on the Data
  Agent itself** (the *Example queries* pane). Only queries with valid syntax that match the selected
  schema are used; invalid ones are silently ignored.
- **Power BI semantic model:** the Data Agent's example-queries pane **does not accept pairs**.
  Instead, this context lives on the **model**, via **Prep for AI** — *AI Data Schema* (which
  tables/columns/measures the AI sees), *AI Instructions* (business rules **and** example DAX), and
  *Verified Answers* (approved question→visual mappings, 5–7 trigger phrasings each). The Data Agent
  honors all of them; you just don't configure them in the agent.

## Why it matters

Instructions tell the agent the rules; few-shots *show* it the pattern — and showing generalizes
where telling does not. A handful of correct examples fixes whole classes of error: bad joins, wrong
filter formatting, the wrong "sales" measure among five look-alikes, the wrong default columns.

For semantic models, the Prep-for-AI split matters because it is where accuracy is actually won.
Verified Answers short-circuit ambiguous questions to a known-good query structure *before* the model
guesses; AI Data Schema removes look-alike measures from view so "last quarter's sales" can't resolve
to Gross when the house standard is Net. Model hygiene compounds it: a lean, well-described model with
efficient DAX both runs faster and gives the DAX generator less noise to misread.

## How to write it well

- **Author examples where the source type requires** — agent pane for SQL/KQL, Prep for AI for
  semantic models. Putting DAX pairs in the agent pane for a semantic model does nothing.
- **Make few-shots diverse, not numerous.** Cover the *kinds* of questions (ranking, breakdown,
  ratio, delta), not many rewordings of one.
- **Validate every example.** For SQL/KQL, invalid syntax is dropped silently. For DAX, verify in DAX
  Query View before pasting it into AI Instructions.
- **Describe everything** on a semantic model — table, column, and measure descriptions are what the
  DAX generator reads to interpret a question.
- **Use business-friendly names.** `Total Revenue`, not `TR_AMT`; the model's metadata *is* the
  agent's vocabulary.
- **Include dependent objects** in the AI Data Schema — a measure that references other measures needs
  those (and their columns) selected too.

## Anti-pattern

**Expecting the Data Agent's example-queries pane to teach a semantic model** — the pane won't take
the pairs, and the authoring silently has no effect. **One giant catch-all example** that tries to
demonstrate every join at once, which the agent can't generalize from. **Unvalidated examples** —
dropped (SQL/KQL) or, worse for DAX, pasted in wrong and copied faithfully. And a **bloated model with
cryptic names**, where no amount of instruction overcomes metadata the generator can't read.

## The Contoso example

Contoso's [`example-queries.json`](../../examples/contoso-vendor-spend/example-queries.json) is a
**teaching artifact** for this repository — it makes the intended DAX visible on the page. In the real
product, because the source is a **semantic model**, these pairs would be authored as example DAX
inside **Prep for AI › AI Instructions** on the model, not in the agent's example-queries pane. The
set is deliberately diverse — one per pattern:

- **Companion measures** — `EVALUATE ROW("Total Spend", [Total Spend], "Invoiced Workers", …)` shows
  the reporting rule in action.
- **Ranking** — `TOPN(5, …, [Total Spend], DESC)` → a labeled table.
- **Per-head ratio** — `[Spend per Invoiced Worker]` returned *with* `[Invoiced Workers]`, so the
  denominator is visible and never summed.
- **Named-dimension breakdown** — SOW vs Staff Augmentation via `[% of Total Spend]`.
- **Driver decomposition** — the `::drivers` delta split across a leadership dimension.

Each example encodes a rule from [03](03-agent-instructions.md) as a concrete pattern the translator
can imitate — the essence of few-shot design.

---
_Next: [05 · Ontology & glossary →](05-ontology-and-glossary.md)_
