[![Lang: English](https://img.shields.io/badge/lang-English-1f6feb?style=for-the-badge)](README.md)
[![Idioma: Español](https://img.shields.io/badge/idioma-Espa%C3%B1ol-2da44e?style=for-the-badge)](README.es.md)
&nbsp;·&nbsp; [![License: MIT](https://img.shields.io/badge/license-MIT-black?style=for-the-badge)](LICENSE)

# Anatomy of a Fabric Data Agent

**A reference-grade, vendor-neutral guide to *how a Microsoft Fabric Data Agent actually works* — and how to instruct one well.**

A Fabric Data Agent turns plain-language questions into governed queries (SQL / DAX / KQL / GQL) over your lakehouse, warehouse, Power BI semantic model, KQL database, or graph — and answers under the caller's own identity. Getting one to answer *correctly and consistently* is less about clicking "Create" and more about the parts you write: its **role**, its **data sources**, its **instructions**, and its **example queries**.

This repository dissects each of those parts. Every section follows the same shape — **What it is · Why it matters · How to write it well · Anti-pattern · The Contoso example** — and every part is illustrated end-to-end with one worked example: the **[Contoso Retail Agent](examples/contoso-retail/)**.

> This is not a "getting started" click-through. It is the reference you keep open *while* you author the agent, distilled from real, in-production Data Agent work (sanitized — see [SANITIZATION.md](SANITIZATION.md)).
> The companion article — field experience, measured questions, and the *why* behind each authoring decision — is at **[Anatomía de un Fabric Data Agent](https://csalcedodatabi.com/blog/anatomia-fabric-data-agent/)**.

## The anatomy

| # | Part | What you'll learn |
|---|------|-------------------|
| 00 | [Overview](docs/anatomy/00-overview.md) | What a Data Agent is, the mental model, and how the parts fit together |
| 01 | [Identity & role](docs/anatomy/01-identity-and-role.md) | The system context that frames everything the agent does |
| 02 | [Data sources](docs/anatomy/02-data-sources.md) | SQL · KQL · Semantic Model (NL2DAX) · Graph (NL2GQL) — which to pick, and why |
| 03 | [Agent-level instructions](docs/anatomy/03-agent-instructions.md) | RLS, nulls, disambiguation, additivity — the rules that prevent wrong answers |
| 04 | [Source instructions & few-shots](docs/anatomy/04-source-instructions-and-fewshots.md) | The single biggest accuracy multiplier |
| 05 | [Ontology & business glossary](docs/anatomy/05-ontology-and-glossary.md) | Mapping business language to model fields |
| 06 | [Direct vs. orchestrator](docs/anatomy/06-direct-vs-orchestrator.md) | One agent or many? Evidence from real tests |
| 07 | [Provisioning](docs/anatomy/07-provisioning.md) | Portal · REST · PowerShell — the automation seam |
| 08 | [Lifecycle & the 2026 sunset](docs/anatomy/08-lifecycle-and-sunset.md) | The Assistants API shuts down **2026-08-26** — plan your migration |

## Tooling

What to install before you author — Microsoft's official Fabric skills, and the authoring aids that
help you write instructions that are **verified**, not merely plausible.

→ [`docs/tooling.md`](docs/tooling.md)

## The worked example — Contoso Retail

A complete Data Agent over **Contoso Retail** — a synthetic retail sales model (~126k order lines in MXN; 8 tables: `FactSales`, `DimDate`, `DimProduct`, `DimStore`, `DimCustomer`, …). It shows real patterns you rarely see spelled out: **companion measures reported together**, **additive-vs-non-additive discipline**, **declared breakdown defaults**, a **per-capita-ratio denominator caveat**, and **`>` steering commands**. The dataset is [public](https://github.com/CSalcedoDataBI/SampleDataSets/tree/main/contoso-retail), so every claim here is reproducible.

→ [`examples/contoso-retail/`](examples/contoso-retail/)

## Who this is for

BI/analytics engineers building Data Agents on Microsoft Fabric, and anyone (human or AI assistant) who needs a precise, current reference on the moving parts. Everything is dated; parts in preview or with a known sunset are flagged.

## Provenance & sanitization

The patterns here come from Data Agents that shipped for real clients. **No client data, names, IDs, or endpoints appear anywhere in this repo.** How that is guaranteed — the replacement map and the automated guard — is documented in **[SANITIZATION.md](SANITIZATION.md)** and enforced by [`scripts/sanitize-check.sh`](scripts/sanitize-check.sh) in CI.

## License

[MIT](LICENSE) © 2026 Cristóbal Salcedo ([CSalcedoDataBI](https://github.com/CSalcedoDataBI)). Contributions welcome — see [CONTRIBUTING.md](CONTRIBUTING.md).
