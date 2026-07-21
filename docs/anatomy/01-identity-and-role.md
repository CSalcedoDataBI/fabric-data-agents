[![Lang: English](https://img.shields.io/badge/lang-English-1f6feb?style=flat-square)](01-identity-and-role.md)
[![Idioma: Español](https://img.shields.io/badge/idioma-Espa%C3%B1ol-2da44e?style=flat-square)](01-identity-and-role.es.md)
&nbsp;·&nbsp; [↑ Index](../../README.md)

# 01 · Identity & role

## What it is

The **identity** is the agent-level instruction block that frames *who the agent is* before it looks
at a single row: its domain, its audience, the data it speaks for, and how it should behave. In
Microsoft Fabric this lives in the **Data agent instructions** pane — one plain-language field of up
to **15,000 characters** that the agent's orchestrator reads first, on every turn, ahead of any
source-specific rule.

It is not a system prompt you engineer with jailbreak tricks, and it is not where query syntax
belongs. It is the **role and routing brief**: what the agent is for, what a "row" of its world means,
which source answers which kind of question, and what to do when a request is vague or out of scope.

## Why it matters

The identity is the highest-leverage text you write, because everything downstream inherits its
framing:

- **Scope.** A named role ("vendor-spend analyst for Contoso") tells the agent what is *in* its world
  and, by omission, what is not — so it declines or redirects instead of hallucinating an answer from
  the wrong table.
- **Routing.** With up to five data sources in one agent, the identity is where you say *direct
  financial-metric questions to the semantic model, raw-record questions to the lakehouse, log
  questions to the KQL database*. The orchestrator uses exactly this to pick a source.
- **Defaults.** Tone, output shape (tables over prose), and disambiguation posture are set once here
  and apply everywhere.

It also sits inside a **precedence model**. From highest to lowest: organizational intent (tenant
policy) → role-based intent (workspace governance, RLS) → **developer intent (this identity)** → user
intent (the question). Your identity can shape behavior, but it can never override governance — a
useful thing to know so you don't try to instruct around a permission boundary.

## How to write it well

- **Name the role and the audience** in the first sentence. "You are a *vendor-spend analyst* for
  Contoso" beats "You are a helpful data assistant."
- **State the grain.** Say what one row represents and what dimensions it can be sliced by, so the
  agent orients a vague "break it down" correctly (see [05 · Ontology](05-ontology-and-glossary.md)).
- **Write the routing rules** when the agent has more than one source: one line per source, keyed to
  the *kind* of question, not the table name.
- **Set behavioral defaults**: prefer labeled tables, disambiguate before guessing, never invent
  measures or numbers.
- **Keep query mechanics out.** How to join, which DAX measure, how to filter a date — that is
  source-level instruction, covered in [04](04-source-instructions-and-fewshots.md). Mixing it into
  the identity bloats the 15k budget and couples the persona to one source's schema.

## Anti-pattern

The **blank "helpful assistant"** identity — no domain, no grain, no routing — which makes the agent
treat every source as equally valid for every question and answer confidently from whichever one the
model happened to pick. Its twin is the **overstuffed identity**: pages of DAX and JOIN rules pasted
into the role field, which belong in source instructions and which crowd out the framing that
actually steers routing. A third trap is **promising data the agent cannot see** ("you know our
headcount") when no such source or measure exists — the agent will try, and fabricate.

## The Contoso example

The [Contoso Vendor Spend agent](../../examples/contoso-vendor-spend/instructions.md) opens with a
tight role and an explicit grain, and nothing else masquerading as identity:

> You are a vendor-spend analyst for **Contoso**. You answer questions about contingent-workforce
> spend (staffing suppliers, assignments, invoices) using the **Contoso Vendor Spend (SM)** semantic
> model. […] You never invent numbers, measures, or dimensions that are not in the model.

It then states the grain (`CALENDAR[Date] × Business Unit × Job Family × Country × Spend Type`), the
reporting period, and the default breakdown dimensions — the orientation the router needs — while
leaving *how to write the DAX* to the source-level rules. Because this agent has a single source, its
routing brief is trivial; the same identity over five sources would carry one routing line each.

---
_Next: [02 · Data sources →](02-data-sources.md)_
