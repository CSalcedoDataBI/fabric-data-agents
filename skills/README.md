# Skills

Agent Skills published alongside this reference. They are the tools that produced the material in
this repository — not illustrations of it.

| Skill | What it does |
|---|---|
| [`verified-ai-instructions`](verified-ai-instructions/) | Authors Microsoft-format, **data-verified** *Prep for AI* instructions for a Power BI / Fabric semantic model and writes them into the model's TMDL. Every claim is proven against the model's structure and its real data before it is written. |

See [`docs/tooling.md`](../docs/tooling.md) for the full tooling page, including Microsoft's own
`skills-for-fabric` plugin.

## Install

A skill is a folder containing `SKILL.md`. Copy the one you want into your skills directory:

```bash
# global (available in every project)
cp -r skills/verified-ai-instructions ~/.claude/skills/

# or scoped to a single project
cp -r skills/verified-ai-instructions <your-repo>/.claude/skills/
```

Then start a new session — skills are loaded at startup.

## Why these ship here

`verified-ai-instructions` wrote the instructions in
[`examples/contoso-retail/model/prep-for-ai/ai-instructions.md`](../examples/contoso-retail/model/prep-for-ai/ai-instructions.md),
including the correction that makes the case for the whole method: a draft told the agent to convert
currencies with `DimCurrencyExchange`, which sounded reasonable and was false — all 126,524 fact rows
are `MXN` and that table is disconnected. Verifying against the data turned a harmful instruction
into a correct one.

Licensed under this repository's [MIT license](../LICENSE).
