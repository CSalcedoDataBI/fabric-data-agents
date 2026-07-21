[![Lang: English](https://img.shields.io/badge/lang-English-1f6feb?style=flat-square)](06-direct-vs-orchestrator.md)
[![Idioma: Español](https://img.shields.io/badge/idioma-Espa%C3%B1ol-2da44e?style=flat-square)](06-direct-vs-orchestrator.es.md)
&nbsp;·&nbsp; [↑ Index](../../README.md)

# 06 · Direct vs. orchestrator

## What it is

Two architectures answer a question with a Data Agent:

- **Direct** — the user (or app) talks to **one Fabric Data Agent**, which internally routes across its
  own (up to five) sources and returns a data-grounded answer. The routing between sources is the
  agent's *own* orchestration/planning logic, set by its **runtime** (Standard = GA, Preview = latest
  routing/query-gen changes).
- **Orchestrator** — an **external agent** (Foundry Agent Service, Microsoft 365 Copilot, Copilot
  Studio, Teams, a custom multi-agent app) treats the Fabric Data Agent as **one tool among many**.
  The outer agent decides *when* to call it, then blends its result with other tools and its own
  reasoning. Authorization flows **On-Behalf-Of (OBO)**: the data agent still runs under the end
  user's identity, so RLS holds across the hop.

A key seam: in the orchestrator pattern the outer model does the *routing and phrasing*, but it **does
not change the model the Data Agent uses for NL2SQL/DAX/KQL** — the two are independent.

## Why it matters

The choice sets the boundary of responsibility and the failure modes you inherit:

- **Direct** is the tighter contract. One artifact, one set of instructions, one place to test and
  govern. It is the right default when the questions live entirely within your Fabric data, and it is
  the surface this whole reference optimizes.
- **Orchestrator** buys reach — combine governed Fabric data with unstructured knowledge, external
  APIs, or actions — at the cost of a second layer that can *re-interpret* the agent's output. Under
  Microsoft 365 Copilot, for instance, the host orchestrator reasons over the returned data and may
  summarize or rephrase it; you can dampen that with the publishing description
  (`description_for_model`) but not eliminate it.
- **Governance is preserved either way** — OBO means the data agent never exceeds the caller's
  permissions, whichever architecture wraps it — but the *outer* layer's compliance boundary and data
  handling become yours to account for once results leave Fabric.

## How to write it well

- **Default to direct** while the questions are Fabric-shaped; reach for an orchestrator only when a
  real class of questions needs tools the Data Agent doesn't have.
- **Keep the Data Agent read-only and single-purpose** — a clean tool for an orchestrator to call is a
  well-scoped one, not a do-everything agent.
- **Write the outer agent a crisp tool description** — "for vendor-spend and staffing-invoice
  questions, use the Fabric tool" — and consider `tool_choice` / forced invocation when the tool must
  always run.
- **Publish before you integrate.** Only a *published* Data Agent exposes the endpoint
  (`.../groups/<workspace-id>/aiskills/<artifact-id>`) an orchestrator connects to.
- **Test the seam, not just the agent** — verify the orchestrator doesn't distort correct numbers, and
  add an "emit as-is" instruction where fidelity matters.

## Anti-pattern

**Reaching for a multi-agent orchestrator when a single direct agent would answer everything** — you
add a re-interpretation layer, a second compliance boundary, and more moving parts for no coverage
gain. The inverse: **cramming unrelated domains into one Data Agent** to avoid an orchestrator, until
its five sources and routing rules collide. And **letting the host silently reword governed
numbers** — shipping a Copilot integration without checking whether the orchestrator summarizes the
figures into something subtly wrong.

## The Contoso example

The Contoso agent is authored **direct**: one semantic-model source, one instruction set, testable in
isolation — the simplest contract that answers vendor-spend questions correctly. Its design also makes
it a *good orchestrator tool* the day that's needed: it is read-only, single-domain, and its role
("vendor-spend analyst … staffing suppliers, assignments, invoices") reads almost verbatim as the
tool description an outer Foundry or Copilot agent would use to decide when to call it. Nothing about
the direct build has to be undone to promote it into an orchestrated workflow — publish it, hand the
endpoint to the outer agent, and the OBO identity flow keeps RLS intact.

---
_Next: [07 · Provisioning →](07-provisioning.md)_
