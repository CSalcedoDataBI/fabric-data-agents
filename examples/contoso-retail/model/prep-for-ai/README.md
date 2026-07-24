# Prep for AI — versioned source of truth

Power BI's **Prep for AI** (AI instructions, AI data schema, verified answers) is stored *inside*
the model — and the AI-instructions box is a **preview feature saved as a model-level annotation**,
which does not round-trip cleanly into the PBIP/TMDL yet. So the model's AI-prep content is hard to
diff and review in git.

This folder is the fix: the AI-prep content, kept as **plain, version-controlled files** next to the
model. It is the human-readable **source of truth**; the in-model form is applied *from* here.

| File | What it is | Applied in Power BI Desktop via |
|---|---|---|
| [`ai-instructions.md`](ai-instructions.md) | The AI instructions text — **every line verified against real data** | *Prep data for AI → Add AI instructions* → paste → Apply → Save |
| [`ai-data-schema.json`](ai-data-schema.json) | Which tables/columns/measures Copilot sees (Visible/Hidden), in Microsoft's authoritative `copilot/schema` format | *Prep data for AI → Simplify data schema* |

> **Why this matters (the honest part):** these instructions were not written by vibes. Each claim
> was checked against the model structure (TMDL relationships, measure DAX) and the real data
> (queried over the committed Parquet). See the verification table in `ai-instructions.md`.

**Workflow:** edit these files → apply them in Desktop → Save the PBIP → (optionally) rebuild the
`.pbix`. When we can round-trip the annotation reliably, this folder becomes the input we write
directly into the model.
