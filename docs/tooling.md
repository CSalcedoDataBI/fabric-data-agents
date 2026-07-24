[![Lang: English](https://img.shields.io/badge/lang-English-1f6feb?style=flat-square)](tooling.md)
[![Idioma: Español](https://img.shields.io/badge/idioma-Espa%C3%B1ol-2da44e?style=flat-square)](tooling.es.md)

# Tooling — what to install before you author

This reference tells you *what* to write. This page lists the tooling that helps you *write it
well*. It is deliberately limited to **authoring aids** — things that help you produce better
instructions and verify them. Provisioning, CI and orchestration automation are out of scope here;
they belong to [07 · Provisioning](anatomy/07-provisioning.md).

Nothing here is required to read this repository. It is required only if you want to *do* the work
with assistance.

---

## Official — Microsoft

### `microsoft/skills-for-fabric`

Microsoft's own collection of Agent Skills and MCP servers for operating Microsoft Fabric from a
CLI, VS Code or Claude. It ships profiles for **semantic-model review**, **Fabric apps** and
**data agents** — the last one is directly relevant to everything in this repository.

| | |
|---|---|
| Repo | <https://github.com/microsoft/skills-for-fabric> |
| Publisher | Microsoft (official) |
| License | MIT |
| Kind | Claude Code plugin (marketplace) |

```bash
claude plugin marketplace add microsoft/skills-for-fabric
```

Use it for the operational surface: exploring workspaces, inspecting semantic models, running the
Fabric CLI, and driving a Data Agent from your editor.

---

## Authoring aids — writing better instructions

The single highest-leverage thing you can improve is the text you give the agent and the model. The
discipline that matters is **verification**: an instruction that sounds plausible but is false is
worse than no instruction at all, because it actively steers the agent wrong.

That claim is not theoretical here. While authoring the Contoso Retail instructions, a draft told
the agent to *"convert currencies using `DimCurrencyExchange`"* — reasonable-sounding, and **false**:
every one of the 126,524 fact rows is `MXN` and that table is disconnected. Checking it against the
data turned a harmful instruction into a correct one. See
[`examples/contoso-retail/model/prep-for-ai/ai-instructions.md`](../examples/contoso-retail/model/prep-for-ai/ai-instructions.md),
which records how **every** line was verified.

### `verified-ai-instructions` *(ours — not yet published)*

Authors Microsoft-format, **data-verified** *Prep for AI* instructions for a Power BI / Fabric
semantic model and writes them straight into the model's on-disk TMDL. Every claim is proven against
the model's structure and its real data *before* it is written.

What it contains:

- the Microsoft authoring format (business-context lead, themed sections, explicit `Table[Column]`
  naming, the 10,000-character limit);
- a verification protocol that splits each claim into **structural** (checkable against TMDL) and
  **data** (needs a query), and requires both to pass;
- `apply-instructions.py`, which writes the text into the `CustomInstructions` JSON string inside
  `definition/cultures/<culture>.tmdl`, escaping it correctly and re-parsing to validate. Hand-editing
  that value is the number-one way to corrupt the file — a single raw newline instead of `\n` makes
  the JSON invalid and Power BI silently drops the instructions.

> **Status: authored, not published.** This skill currently lives only in its author's local
> `~/.claude/skills/`. There is no install command yet. It is listed here because it is the tool that
> produced the verified instructions in this repository — and because the *method* it encodes is
> reproducible by hand from
> [`examples/contoso-retail/model/prep-for-ai/ai-instructions.md`](../examples/contoso-retail/model/prep-for-ai/ai-instructions.md),
> whose verification table shows exactly what was checked and how.

---

## Deliberately not listed yet

Automation — provisioning agents over REST, CI/CD for agent config, evaluation batteries against the
MCP endpoint — is real and used in this project, but it is a different kind of tool with different
failure modes, and it is not what makes an agent answer correctly. It will be documented separately
once it is stable enough to recommend. The measurement method those batteries implement is already
written up in
[`examples/contoso-retail/data-agent/ablation-test-design.md`](../examples/contoso-retail/data-agent/ablation-test-design.md),
so you can reproduce the evaluation by hand today.
