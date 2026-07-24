# Manifest — recovered screenshots (all 25)

Recovered from the session transcript and saved to `raw/`. Nothing was lost.
✅ = identity visually confirmed by Claude · ⚠️ = best-guess from conversation position (verify on request).

| File (raw/) | Approx. content | Blog use |
|---|---|---|
| `img_01_line060.png` | ✅ ContosoRetail model published in workspace, ready to create the Data Agent | context / intro |
| `img_02_line399.png` | ⚠️ Agent working — the first "must-have" answer capture | intro proof |
| `img_03_line429.png` | ⚠️ Agent instructions (full guardrails) | anatomy |
| `img_04_line429.png` | ⚠️ About panel | anatomy |
| `img_05_line429.png` | ⚠️ Publishing panel | anatomy |
| `img_06_line429.png` | ⚠️ MCP endpoint panel | anatomy |
| `img_07_line452.png` | ⚠️ Prep-for-AI flow (1) | Prep-for-AI |
| `img_08_line452.png` | ⚠️ Prep-for-AI flow (2) | Prep-for-AI |
| `img_09_line452.png` | ⚠️ Prep-for-AI flow (3) | Prep-for-AI |
| `img_10_line452.png` | ⚠️ Prep-for-AI flow (4) | Prep-for-AI |
| `img_11_line452.png` | ⚠️ Prep-for-AI flow (5) | Prep-for-AI |
| `img_12_line452.png` | ⚠️ (DUPLICATE of a Prep-for-AI shot) | skip |
| `img_13_line530.png` | ⚠️ V2 published / bare instructions | Round C |
| `img_14_line567.png` | ⚠️ Explorer with BOTH sources (ContosoRetail + V2), full instructions | A/B setup |
| `img_15_line801.png` | ⚠️ Published toggle — V2 active | A/B |
| `img_16_line801.png` | ⚠️ Published toggle — ContosoRetail (Prep) active | A/B |
| `img_17_line863.png` | ✅ **Build agent with AI** — "¿margen?" → hedges + SQL, no execute | **01 (annotated)** |
| `img_18_line863.png` | ⚠️ Build-with-AI / V2 test — ambiguous batch | Round D |
| `img_19_line863.png` | ⚠️ ambiguous batch (SQL "último trimestre") | Round D |
| `img_20_line863.png` | ⚠️ ambiguous batch | Round D |
| `img_21_line863.png` | ⚠️ ambiguous batch | Round D |
| `img_22_line863.png` | ⚠️ ambiguous batch (V2 executes last-quarter) | Round D |
| `img_23_line863.png` | ⚠️ ambiguous batch (V2 output 2024-Q4) | Round D |
| `img_24_line910.png` | ✅ **Test data agent** — "¿margen?" → executes $3,938,789 \| 19.8% | **02 (annotated)** |
| `img_25_line910.png` | ⚠️ Test data agent — último trimestre (2024-Q4 $2,653,095) | 03 |

## Annotated so far (`annotated/`)
- `01-buildwithai-hedges.png` — the wrong pane (authoring copilot, no execution).
- `02-testdataagent-margin.png` — the right pane (runtime, executes real measures).

Annotate the rest with `scratchpad/annotate.py` + a JSON spec (see `anno_spec.json`).

> **How recovery works:** pasted images live as base64 inside the session transcript
> (`~/.claude/projects/<proj>/<session>.jsonl`). `scratchpad/extract_images.py` walks it and
> writes every image to disk — so nothing pasted is ever truly lost while the transcript exists.
