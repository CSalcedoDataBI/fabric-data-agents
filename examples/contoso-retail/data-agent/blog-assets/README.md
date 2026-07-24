# Blog assets — ablation screenshots (catalog + annotation plan)

Screenshots for the blog companion of the ablation. **Workflow:**
1. Save each raw capture into `blog-assets/raw/` (gitignored — may contain the workspace
   name / account) with the filename in the table below.
2. Claude reads each, redacts the sensitive bits, adds arrows/boxes/labels, and writes the
   sanitized version into `blog-assets/annotated/` (safe to commit).
3. Tool: `scratchpad/annotate.py` (OpenCV) driven by a JSON spec.

**Redaction targets in every Data Agent capture** (blur these):
- Left-nav **workspace-name** sliver (the dark left margin, partial text like "…-Ray").
- Top-right **account avatar / name**.
- (No GUIDs appear in the UI; the tool name `DataAgent_ContosoRetail_Data_Agent` is safe.)

## The shots that carry the story

| # | Filename (save as) | What it proves | Highlight (arrow/box) |
|---|---|---|---|
| 1 | `01-buildwithai-hedges.png` | **Wrong pane.** "Build agent with AI" (Prep agent), "¿cuál es el margen?" → hedges, proposes raw **SQL**, "no puedo ejecutar, cópiala a tu entorno". Never runs. | box the **"Build agent with AI"** tab; box the SQL block; label "authoring copilot — does NOT execute" |
| 2 | `02-testdataagent-margin.png` | **Right pane.** "Test data agent" (Prep agent), same question → **executes** DAX `ROW([Gross Margin],[Margin %])` → **$3,938,789 \| 19.8% MXN**. | arrow to **"Test data agent"** tab; arrow to the `[Gross Margin]`/`[Margin %]` measures; box the Output row |
| 3 | `03-testdataagent-lastquarter.png` | Same right pane, "ventas del último trimestre" → **2024-Q4 $2,653,095**, DAX resolves last quarter *with data*. | box "Analyzed ContosoRetail SemanticModel"; box Output `2024 \| 4 \| $2,653,095` |
| 4 | `04-v2-testpane-margin.png` | V2 (no Prep) in Test data agent → same `$3,938,789`. Numbers don't depend on Prep. | box Output; label "V2 — no Prep-for-AI, same number" |
| 5 | `05-bare-instructions.png` | The stripped Agent instructions (the Round C control prompt). | box the one-line prompt |
| 6 | `06-schema-fidelity.png` *(optional, compose)* | DAX naming: Prep → `DimProduct[CategoryName]` ✅ vs no-Prep → `[Category]`/`FactSales[SalesAmount]` ❌. May be a side-by-side we compose from two captures. | two boxes, green ✅ / red ❌ |

## The one-line takeaways to caption

- **Evaluate on "Test data agent" or the MCP API — never on "Build agent with AI."**
- **Prep-for-AI moved only DAX schema-name fidelity; numbers/MXN/Spanish come from the model.**

See the full write-up in [`ablation-prep-for-ai.md`](../ablation-prep-for-ai.md) (ES: [`.es.md`](../ablation-prep-for-ai.es.md)).
