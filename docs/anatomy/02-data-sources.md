[![Lang: English](https://img.shields.io/badge/lang-English-1f6feb?style=flat-square)](02-data-sources.md)
[![Idioma: Español](https://img.shields.io/badge/idioma-Espa%C3%B1ol-2da44e?style=flat-square)](02-data-sources.es.md)
&nbsp;·&nbsp; [↑ Index](../../README.md)

# 02 · Data sources

## What it is

A data source is one governed store the agent may query, plus the **selection of tables** within it
that the agent is allowed to see. A single Fabric Data Agent supports **up to five sources in any
combination**, and each source type carries its own natural-language-to-query translator:

| Category | Artifacts | Language | Translator |
|---|---|---|---|
| **SQL** | Lakehouse, Warehouse, SQL Database, Mirrored Database | T-SQL | NL2SQL |
| **Eventhouse** | KQL Database | KQL | NL2KQL |
| **Semantic model** | Power BI semantic model | DAX | NL2DAX |
| **Graph** _(preview)_ | Graph model | GQL | NL2GQL |
| **Ontology** _(preview)_ | Fabric Ontology | ontology-native | — |
| **Azure AI Search** _(preview)_ | Search index | natural language | retrieval |

_Version note (2026): SQL, Eventhouse, and semantic-model sources are generally available; Graph,
Ontology, and Azure AI Search are in preview — confirm current status before relying on them._

The agent executes every query **under the caller's identity**, so Row-Level Security and object
permissions hold automatically. Notably, you only need **Read** on a semantic model to add it; Write
is required only to *modify* the model or configure Prep for AI (see
[04](04-source-instructions-and-fewshots.md)).

## Why it matters

The source you pick decides the query language, the shape of the answer, and where the business logic
lives:

- **Semantic model (DAX)** — answers in the language of *governed measures*. The model already
  encodes additivity, currency, filters, and time intelligence, so the agent inherits correct
  business logic instead of reinventing it in SQL. Best when a curated model exists.
- **SQL (lakehouse / warehouse)** — answers over raw relational or Delta tables. Maximum reach and
  detail, but the agent must assemble joins and aggregations itself, so correctness rests on your
  schema selection and example queries.
- **KQL (Eventhouse)** — time-series and log/event analytics, queried in place with no data movement.
  Encourage time filters to keep it fast.

Selecting **only the relevant tables** is a first-class accuracy lever, not a formality: a bloated
schema is more surface for the translator to misread. Fewer, well-named tables → fewer wrong joins
and fewer ambiguous columns.

## How to write it well

- **Prefer a semantic model when one exists** and the questions are metric-shaped — you get governed
  measures for free and sidestep a whole class of re-aggregation bugs.
- **Trim the table selection** to what the agent's questions actually need. For lakehouses, select
  *tables*, not files — ingest files into tables first.
- **Route by question type, not by convenience** — declare in the agent identity
  ([01](01-identity-and-role.md)) which source owns which kind of question.
- **Combine sources deliberately.** Five sources multiply routing ambiguity; add a source only when a
  class of questions genuinely needs it, and give the router a clear rule for it.
- **Mind the grain per source** and expose it in instructions so the agent doesn't blend
  incompatible grains in one answer.

## Anti-pattern

**Pointing the agent at raw tables when a governed semantic model already encodes the metrics.** The
agent then re-derives "total spend" with a `SUM` over a fact column, silently diverging from the
model's official measure (which may filter, convert currency, or handle nulls). Equally common:
**selecting every table "just in case,"** which floods the translator with lookalike columns and
produces confident wrong joins. And **mixing five sources with no routing rules**, so the same
question resolves against a different source run to run.

## The Contoso example

Contoso uses a **single semantic-model source**, declared in
[`data-sources.yaml`](../../examples/contoso-vendor-spend/data-sources.yaml):

```yaml
sources:
  - type: semantic-model          # NL -> DAX
    name: "Contoso Vendor Spend (SM)"
    id: "<semantic-model-id>"     # placeholder — real value is a GUID
    tables: [factspend, CALENDAR, dimbusinessunit, dimjobfamily,
             dimlocation, dimspendtype, dimsupplier, dimcostcenter]
```

One curated model, eight named tables — not the whole workspace. Because it is a semantic model, the
agent answers in DAX against **defined measures** (`[Total Spend]`, `[Invoiced Workers]`, …) rather
than summing `factspend` columns, so the business logic stays where the modeler put it. The routing
brief is a single line in the identity; a second source (say a lakehouse of raw invoices for
record-level lookups) would earn its own routing rule before being added.

---
_Next: [03 · Agent-level instructions →](03-agent-instructions.md)_
