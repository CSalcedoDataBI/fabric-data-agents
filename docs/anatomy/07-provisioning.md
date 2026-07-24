[![Lang: English](https://img.shields.io/badge/lang-English-1f6feb?style=flat-square)](07-provisioning.md)
[![Idioma: Español](https://img.shields.io/badge/idioma-Espa%C3%B1ol-2da44e?style=flat-square)](07-provisioning.es.md)
&nbsp;·&nbsp; [↑ Index](../../README.md)

# 07 · Provisioning

## What it is

Provisioning is how the agent gets **created, configured, versioned, and published** — the operational
seam around the content the earlier sections author. There are three surfaces:

- **Portal** — the authoring UI in Fabric. Best for design and iteration: add sources, pick tables,
  write instructions, test, publish.
- **Config-as-code (Git integration)** — the agent's configuration serialized to files, so it lives in
  source control and moves through ALM like any Fabric item.
- **SDK / REST** — the Fabric Data Agent Python SDK (`fabric-data-agent-sdk`) for building, evaluating,
  and automating agents in notebooks, plus REST for CI/CD pipelines.

Prerequisites are the same across all three: a **paid F2+ capacity** (or Power BI Premium P1+ with
Fabric enabled), the **cross-geo processing/storing for AI** tenant settings enabled, and **Read** on
at least one data source.

## Why it matters

The portal is where an agent is *born*, but config-as-code is where it becomes a **maintainable
product**. Serializing the configuration turns the agent into a reviewable, diffable, deployable
artifact — the difference between "someone clicked this together in prod" and "this change went through
a PR." The Git layout makes the review meaningful because it maps one-to-one to the anatomy:

| File / folder | Holds | Anatomy section |
|---|---|---|
| `stage_config.json` → `aiInstructions` | Agent-level instructions | [01](01-identity-and-role.md) · [03](03-agent-instructions.md) |
| `<source>/datasource.json` | `dataSourceInstructions`, `displayName`, `elements` (schema map) | [02](02-data-sources.md) · [04](04-source-instructions-and-fewshots.md) |
| `<source>/fewshots.json` | Example query pairs (SQL/KQL sources) | [04](04-source-instructions-and-fewshots.md) |

Source folders are prefixed by type (`lakehouse-tables-…`, `warehouse-tables-…`, `kusto-…`,
`semantic-model-…`, `ontology-…`), and there are separate **draft** and **published** folders — the
draft/publish boundary is explicit in the tree. A semantic-model source has **no `fewshots.json`**,
because its examples live in Prep for AI on the model (see [04](04-source-instructions-and-fewshots.md)) —
the file layout itself encodes that asymmetry.

## How to write it well

- **Author in the portal, govern in Git.** Iterate visually, then commit the serialized config so
  every subsequent change is a diff, not a mystery.
- **Review the config against the anatomy.** A PR that changes `aiInstructions` is an
  identity/behavior change; a change to `datasource.json.elements` is a schema-selection change — read
  them as such.
- **Publish deliberately.** Draft is where you iterate; only a *published* agent exposes the endpoint
  that consumers and orchestrators ([06](06-direct-vs-orchestrator.md)) use.
- **Automate evaluation, not just deployment.** Use the SDK's evaluation harness (a ground-truth set
  of question→expected-answer pairs) as a quality gate before publish — provisioning without a
  regression check ships silent accuracy drops.
- **Don't duplicate secrets or IDs into the repo.** Workspace, item, and semantic-model identifiers
  are environment-specific GUIDs — keep them as parameters/placeholders, never hard-coded
  (see [SANITIZATION.md](../../SANITIZATION.md)).

## Anti-pattern

**Portal-only, prod-only** — every change made by hand in the published agent, with no version
history, no review, and no way to roll back. Its mirror image is **automating deployment without
evaluation**, so a config change ships fast *and* silently regresses answer quality. And
**hard-coding environment GUIDs** into committed config, which both leaks identifiers and breaks the
moment the agent is promoted to another workspace.

## The Contoso example

This repository *is* the config-as-code view of the Contoso agent, kept vendor-neutral:

- [`agent.config.json`](../../examples/contoso-retail/data-agent/agent.config.json) carries the
  Fabric identifiers as **placeholders** — `<workspace-id>`, `<agent-id>`, `<semantic-model-id>` —
  never real GUIDs (the sanitization guard fails the build if a GUID appears).
- [`data-sources.yaml`](../../examples/contoso-retail/data-agent/data-sources.yaml) is the readable analog
  of `datasource.json` — the one semantic-model source and its eight selected tables — and, being a
  semantic model, it deliberately carries **no `fewshots.json`**.
- [`instructions.md`](../../examples/contoso-retail/data-agent/instructions.md) is the `aiInstructions`
  payload in human form.

Read together they show the shape a real agent's Git folder takes — the same files a reviewer would
diff in a PR — with every environment-specific value parameterized out.

---
_Next: [08 · Lifecycle & the 2026 sunset →](08-lifecycle-and-sunset.md)_
