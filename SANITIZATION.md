# Sanitization policy

The material in this repository is distilled from Microsoft Fabric Data Agents that were built
for **real clients**. The engineering *patterns* are reusable and worth sharing; the client's
**data, identifiers, schema, and endpoints are not** — and never appear here.

This document is the public contract for how that separation is guaranteed. It deliberately does
**not** reproduce any private token: naming the thing you're scrubbing would itself be a leak.

## What is replaced (by category)

| Private category | Public representation |
|---|---|
| Client / product / program names | The fictional company **Contoso** and its partners (Fabrikam, Northwind Traders, Adventure Works — Microsoft's standard fictional brands) |
| The client's *verbatim* semantic model (its exact measure & dimension set) | **Contoso Retail** — a fully **synthetic**, generated retail sales model that reuses the *shape* (companion measures, additivity, declared breakdown defaults) but shares no schema with any client |
| Fabric resource IDs (workspace, item, semantic model, agent) | Placeholders: `<workspace-id>`, `<agent-id>`, `<semantic-model-id>` |
| Live application / endpoint URLs | Placeholders: `https://<your-validator-app>.example` |
| Internal sample values (customers, stores, products, etc.) | Generated synthetic values |

## The example is representative, not extracted

The [Contoso Retail Agent](examples/contoso-retail/) is **authored fresh** to teach the
patterns. It is not a client agent with names swapped out. This is stronger than find-and-replace:
there is no original to leak because the public artifact was built clean from the start.

The underlying data is stronger still: it is **generated synthetic data**, not a masked extract, and
it is published openly at
[`CSalcedoDataBI/SampleDataSets/contoso-retail`](https://github.com/CSalcedoDataBI/SampleDataSets/tree/main/contoso-retail).
Anyone can rebuild the model and reproduce every claim in this repository — which is only possible
because there is nothing private in it.

## The guard

[`scripts/sanitize-check.sh`](scripts/sanitize-check.sh) fails the build if the public tree contains:

- any **GUID** (`xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`) — real Fabric IDs are GUIDs; the repo uses
  named placeholders instead, so a GUID means a real ID slipped in. **Scope:** the check skips the
  machine-generated PBIP model source (`*.SemanticModel/` and `*.Report/`), which is inherently full
  of *synthetic* object GUIDs (lineageTag, nodeLineageTag, logicalId, relationship names) that are
  not Fabric resource IDs. It stays fully active where a real ID would actually be pasted — agent
  config, docs, and `model/prep-for-ai/`;
- any real **`*.fabricapps.net` / `*.webapp.*`** deployed-app hostname;
- leftover **`TODO-SANITIZE`** markers.

### Where it runs (free + safe)

While this repo is **private**, GitHub Actions minutes are billed, so the guard is **not** spent in
CI: the [`sanitize.yml`](.github/workflows/sanitize.yml) job is gated with
`if: github.event.repository.private == false`, so it is **skipped** (0 billable minutes) until the
repo goes public — at which point Actions is free and the job **auto-arms** as the unbypassable
backstop, with no manual flip. During the private phase the same guard is enforced **locally** by a
`pre-push` git hook ([`.githooks/pre-push`](.githooks/pre-push)) — free, and it blocks a push before
anything leaves the machine.

Enable the hook once per clone:

```bash
git config core.hooksPath .githooks
```

A second, **private** denylist of the actual client tokens lives in the source (private) repository
and is run there *before* anything is copied out. The public guard is the backstop; the private
denylist is the front line. Nothing reaches this repo without passing both.

## Found something?

If you believe any identifier slipped through, please open an issue (do **not** paste the suspected
value into a public issue — describe the file and line, and it will be scrubbed and force-removed
from history).
