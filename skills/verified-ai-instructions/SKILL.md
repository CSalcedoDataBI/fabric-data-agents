---
name: verified-ai-instructions
description: >
  Author Microsoft-format, DATA-VERIFIED AI instructions ("Prep for AI") for a Power BI / Fabric
  semantic model and write them straight into the model's on-disk definition. Use this whenever the
  user wants to prepare a semantic model for a Fabric Data Agent or Copilot, write or edit "AI
  instructions" / "Prep for AI" custom instructions, improve NL2DAX / natural-language answer quality,
  reduce ambiguity for an analytics agent, or asks how to make a model "AI-ready" — even if they don't
  say the words "AI instructions". Every instruction is verified against the model's TMDL and its real
  data before it is written, so no claim goes in unchecked.
---

# Verified AI Instructions (Prep for AI)

Write the **AI instructions** that a Fabric Data Agent / Power BI Copilot reads to interpret a
semantic model — but never on vibes. The whole point of this skill is a discipline:

> **A plausible-sounding instruction that is false is worse than no instruction** — it actively
> steers the agent wrong. So every claim is proven against the model's structure (TMDL) and its real
> data before it is written into the model.

For a **Power BI semantic model** source, this is where the quality lives: the DAX-generation tool
"relies solely on the semantic model's metadata and Prep-for-AI configurations" and **ignores**
per-source *data-source instructions* set at the Data Agent level. So the instructions must live on
the model, and they must be correct.

> **Measured nuance.** That documented behavior describes the *last* step only. A Data Agent reads a
> question in **two layers**: the **orchestrator** reads the question plus the agent's top-level
> (system) instructions and can reformulate it — resolving business jargon before the generator ever
> sees it — and only then does the **DAX-generation tool** read the reformulated question plus the
> model's metadata and Prep-for-AI. So agent-level instructions *can* still change the answer. The
> practical rule that follows: **define any business term in exactly one layer**. When both layers
> define the same term differently there is no clean precedence, and the collision produces
> confidently wrong answers. Evidence and the full "what goes where" table:
> [`prep-for-ai-reference.md`](../../examples/contoso-retail/data-agent/prep-for-ai-reference.md).

## When Q&A/Prep-for-AI hasn't been touched yet

The `CustomInstructions` slot only exists after **Q&A is enabled** and the culture file has been
generated. If `definition/cultures/<culture>.tmdl` does not exist:

1. Set `"qnaEnabled": true` in `<Name>.SemanticModel/definition.pbism` (safe, code-first).
2. Ask the user to open the model in Power BI Desktop → **Home → Prep data for AI**, then **File →
   Save** once. Enabling Q&A generates `definition/cultures/<culture>.tmdl` (the linguistic schema)
   and adds `CopilotTooling` to `PBI_ProTooling` in `model.tmdl`. After that one-time seed, this
   skill edits everything in code.

## Workflow

### 1. Locate the model
Find the PBIP: `<Name>.SemanticModel/definition/`. Note the `culture` (from `model.tmdl`, e.g.
`es-ES`), and the data source (M parameter / partition M in `expressions.tmdl` + `tables/*.tmdl`).

### 2. Draft in Microsoft's format
Load [references/ms-format.md](references/ms-format.md). Write instructions with a **business-context
lead** then **themed sections** (Dates / Measures & aggregation / Dimensions & breakdowns / Currency
& units / Output). Be explicit, name exact `Table[Column]` / `[Measure]`, define ambiguous terms, and
say what NOT to do. Keep it focused (≤10,000 characters — hard limit).

### 3. VERIFY every claim (the core of this skill)
Load [references/verify.md](references/verify.md). Split each claim into **structural** (checkable
against TMDL) or **data** (needs a query against the source), and check them all. Never write a claim
you have not proven. Correct anything the data contradicts, and note what changed (that correction is
the most valuable output — and great blog/PR material).

### 4. Write it into the model
The AI instructions are stored as the **`CustomInstructions`** string inside the `linguisticMetadata`
JSON (`contentType: json`) in `definition/cultures/<culture>.tmdl` — a **single, often multi-hundred-KB
line**. Hand-editing that value is the #1 way to corrupt the file.

**Do NOT hand-escape it.** Author the instructions in the plain-text mirror
`<model>/prep-for-ai/ai-instructions.md` (real newlines, human-readable), then push them in with the
helper — it JSON-escapes correctly (`\n`, `\"`), keeps accents raw, preserves the BOM, and
re-validates by parsing the value back:

```bash
# write the exact box text to a temp file (from the mirror's block), then:
python scripts/apply-instructions.py <model>/definition/cultures/<culture>.tmdl instructions.txt
python scripts/apply-instructions.py <culture>.tmdl instructions.txt --check   # validate only
```

> **Why (learned the hard way):** a single **raw** newline instead of `\n` makes the JSON invalid and
> Power BI silently drops or rejects the instructions. The value must be a valid JSON string. The
> script guarantees it; manual splicing does not.

- If the `CustomInstructions` key is absent (Q&A on but instructions never entered), do the one-time
  seed in "When Q&A/Prep-for-AI hasn't been touched yet", then run the script.
- Do NOT edit the culture file while the model is open in Power BI Desktop — Desktop will overwrite on
  its next save. Have the user close it (or reopen after).

The **plain-text mirror** at `<model>/prep-for-ai/ai-instructions.md` is the version-controlled,
human-readable source of truth (the in-model form is a large JSON blob). Keep the two in sync — the
mirror is what the script reads from.

> **On-disk ≠ published.** Writing the culture file does not update the **published** Fabric model that
> a Data Agent / Copilot reads. To activate, the user opens the model in Desktop (confirms the text in
> *Prep data for AI → AI instructions*) and **Publishes**, or the model is re-deployed to the workspace.

### 5. Test (optional but recommended)
In Power BI Desktop, open the Copilot pane → skill picker → **Answers questions about the data** →
ask questions that exercise the instructions (a non-additive measure, an ambiguous term, the default
breakdown) and confirm the agent behaves. Iterate.

## What this skill does NOT do
- **Descriptions** on tables/columns/measures — those are TMDL `///` metadata, a separate (also
  valuable) layer. Do them first as the foundation.
- **AI data schema** (which fields Copilot sees) — a separate artifact (Microsoft's
  `copilot/schema` format / the culture linguistic schema). Related but distinct from instructions.
- **Verified Answers** — report-layer, authored in Desktop, not editable from files.

## Gotchas
- The "Add AI instructions" box is **empty until you paste** — an empty box + a generated culture file
  means Q&A ran but instructions were never entered. Grep the culture file for a distinctive phrase to
  confirm they actually landed.
- Instructions are unstructured guidance; the LLM interprets them and may not follow exactly. For
  non-negotiable behavior, fix the model (a measure, a relationship), not the prompt.
- The culture file is large (hundreds of KB, Desktop-generated). That's expected — it is the real
  Q&A linguistic schema; `CustomInstructions` is one field inside it.
