[![Lang: English](https://img.shields.io/badge/lang-English-1f6feb?style=flat-square)](00-overview.md)
[![Idioma: Español](https://img.shields.io/badge/idioma-Espa%C3%B1ol-2da44e?style=flat-square)](00-overview.es.md)
&nbsp;·&nbsp; [↑ Index](../../README.md)

# 00 · Overview

## What a Fabric Data Agent is

A **Microsoft Fabric Data Agent** is a governed natural-language interface over your data. A user
asks a question in plain language; the agent picks a data source, generates a query in that source's
language — **SQL** (lakehouse/warehouse), **DAX** (Power BI semantic model), **KQL** (Eventhouse), or
**GQL** (graph, preview) — executes it **under the caller's own identity** (so Row-Level Security and
permissions hold), and returns a data-grounded answer.

It is *not* a chatbot with data pasted into a prompt, and it is *not* a fine-tuned model. It is a
**query-generation-and-execution** layer whose accuracy you control through configuration, not training.

## The mental model: four parts you author

Everything you can influence about an agent's behavior lives in four authored parts. This whole
reference is organized around them:

```
                ┌─────────────────────────────────────────────┐
   user asks ──▶│  IDENTITY & ROLE        (01)  who am I       │
                │  DATA SOURCES           (02)  what can I see │──▶ SQL / DAX / KQL / GQL
                │  AGENT INSTRUCTIONS     (03)  how I behave   │──▶ executed as the caller
                │  SOURCE INSTRUCTIONS +  (04)  how I query    │──▶ grounded answer
                │  FEW-SHOTS                   each source     │
                └─────────────────────────────────────────────┘
```

- **[01 · Identity & role](01-identity-and-role.md)** frames *who the agent is* and what it's for.
- **[02 · Data sources](02-data-sources.md)** decides *what it can see* and in which query language.
- **[03 · Agent instructions](03-agent-instructions.md)** are the *global rules* (additivity, RLS,
  disambiguation) that keep answers correct.
- **[04 · Source instructions & few-shots](04-source-instructions-and-fewshots.md)** teach it *how to
  query each source well* — the single biggest lever on accuracy.

Three more parts surround them: **[05 · Ontology & glossary](05-ontology-and-glossary.md)** (business
language → model fields), **[06 · Direct vs. orchestrator](06-direct-vs-orchestrator.md)** (one agent
or a router over many), and the operational bookends **[07 · Provisioning](07-provisioning.md)** and
**[08 · Lifecycle & the 2026 sunset](08-lifecycle-and-sunset.md)**.

## Why this reference exists

Most material stops at "click Create and pick a lakehouse." The hard, undocumented part is making the
agent answer *correctly and consistently*: not summing a percentage, defaulting a vague "break it
down" to the right dimensions, naming the denominator of a per-head ratio, disambiguating instead of
guessing. Those behaviors come from the parts above, and this guide shows exactly how to write them —
grounded in the **[Contoso Vendor Spend](../../examples/contoso-vendor-spend/)** example.

## How to read it

Each section is self-contained and follows the same shape:

> **What it is · Why it matters · How to write it well · Anti-pattern · The Contoso example**

Read straight through for a full mental model, or jump to the one part you're authoring right now.
Version-sensitive facts are dated; preview features and the 2026 API sunset are flagged where they bite.

## Prerequisites (the short version)

| Requirement | Detail |
|---|---|
| Fabric capacity | Paid F2+ SKU (or Power BI Premium P1+ with Fabric enabled) |
| Tenant settings | *Fabric data agent* + cross-geo processing/storing for AI enabled |
| Data access | At least Read on the target lakehouse / warehouse / semantic model / KQL DB |
| Semantic-model sources | XMLA endpoints enabled; **Prep for AI configured on the model** (see 04) |

Full provisioning detail is in **[07 · Provisioning](07-provisioning.md)**.

---
_Next: [01 · Identity & role →](01-identity-and-role.md)_
