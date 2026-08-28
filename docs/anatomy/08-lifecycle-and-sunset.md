[![Lang: English](https://img.shields.io/badge/lang-English-1f6feb?style=flat-square)](08-lifecycle-and-sunset.md)
[![Idioma: Español](https://img.shields.io/badge/idioma-Espa%C3%B1ol-2da44e?style=flat-square)](08-lifecycle-and-sunset.es.md)
&nbsp;·&nbsp; [↑ Index](../../README.md)

# 08 · Lifecycle & the 2026 sunset

> **Updated 2026-08-27 — this date is now in the past.** The retirement date announced for
> the Assistants API, 2026-08-26, has passed. This page was written before it and is kept
> updated on purpose: a reference that names a deadline and then lets it slip by in the
> future tense is worth less than one that never named it.
>
> What is verified here is the calendar. Whether a particular client still receives a
> response is a thing to check, not to assume — retirements are announced precisely, and
> executed on their own schedule.

## What it is

An agent is not shipped once; it is **maintained** — and one of its dependencies has a hard expiry
date. Two moving parts define its lifecycle:

- **Runtime.** Every Data Agent runs on a runtime that carries its orchestration, routing, and
  query-generation logic. **Standard** is the GA runtime (stable, infrequent updates); **Preview** is
  where new routing/query-gen behavior lands before graduating. Runtime choice does **not** change
  which LLM the agent uses — model upgrades apply to both.
- **The consumption surface**, which is where the deadline lives. Historically, external clients
  consumed a published Data Agent through the **OpenAI Assistants API** (`beta.assistants`,
  `beta.threads`, `beta.threads.runs`). **OpenAI announced 2026-08-26 as the
  retirement date for the Assistants API, and that date has passed.** Code built on it worked up to then; whether a given client still gets an answer today is something to verify.

## Why it matters — the evergreen advantage

This is the section that dates the fastest, which is exactly why it earns its place in a reference
meant to be cited: **the deadline was real, dated, and most material ignored it — and it has now arrived.** Which is the test of a dated claim: not whether it was right when written, but whether it was updated when the date came.

- **What breaks:** anything consuming a Data Agent through the Assistants-API pattern — the older
  external-client and notebook samples that call `beta.threads.runs`.
- **What does *not* break:** the Data Agent itself, its sources, its instructions, its published
  endpoint. The agent is fine; the *client protocol* is what sunsets.
- **The migration targets:**
  - **MCP endpoint** — Microsoft's recommended replacement for programmatic consumption (the Data
    Agent exposed as a Model Context Protocol server). This is the evergreen path.
  - **Foundry Agent Service** — consume the agent as a `FabricTool` under On-Behalf-Of identity, for
    orchestrated/multi-agent scenarios ([06](06-direct-vs-orchestrator.md)).
  - **Responses API** — where you were using the OpenAI Assistants API directly, its successor for
    stateful, tool-calling workflows.

Naming the date and the exits turns a latent outage into a planned migration — the difference between
a reference and a blog post that rots.

## How to write it well

- **Date every version-sensitive claim.** "As of 2026, Graph and Ontology sources are preview" ages
  gracefully; "Graph is preview" does not.
- **Choose Standard runtime for production**, Preview only to trial upcoming behavior — and pin which
  you rely on, so a routing change doesn't surprise you.
- **Audit consumption code for the Assistants API today.** If any client still calls
  `beta.assistants` / `beta.threads`, it is past the 2026-08-26 date: the migration to MCP /
  Foundry / Responses is overdue rather than planned. Start by confirming what those calls
  actually return now — "it still works" and "nobody has run it since" look identical from
  a dashboard.
- **Re-run your evaluation set after any runtime, model, or migration change** — lifecycle events are
  precisely when silent accuracy regressions appear.
- **Keep the config in Git** ([07](07-provisioning.md)) so a migration is a reviewable diff with a
  rollback, not a rebuild.

## Anti-pattern

**Building consumption on the Assistants API in 2026 with no migration plan** — shipping straight onto
a surface with a published shutdown date. **Undated version claims** that quietly become false as
preview features graduate and deadlines pass. **Living on the Preview runtime in production**, then
being surprised when routing behavior shifts under you. And **migrating the client without
re-validating answers**, assuming a protocol swap is behavior-neutral when a lifecycle change is the
likeliest moment for quality to move.

## The Contoso example

The Contoso [instructions](../../examples/contoso-retail/data-agent/instructions.md) close with an explicit
**lifecycle note** rather than leaving the deadline implicit:

> If this agent is consumed programmatically through the OpenAI Assistants API, that surface **shuts
> down 2026-08-26** — migrate to the Responses API / Azure AI Foundry OBO.

The agent's *authored* parts — identity, sources, instructions, glossary — are protocol-independent
and carry forward untouched; only the consumption client is dated. That is the whole point of building
the anatomy well: when the surface changes, you re-point the client at the MCP endpoint or Foundry and
the agent keeps answering. Everything that made it *correct* outlives the API that happened to carry
its answers.

---
_This is the last section. Back to the [Index](../../README.md) · see the full
[Contoso Retail example](../../examples/contoso-retail/)._
