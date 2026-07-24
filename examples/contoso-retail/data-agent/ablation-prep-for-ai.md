# Ablation — does the model's Prep-for-AI change the answers?

A controlled A/B on the **ContosoRetail Data Agent**: same agent, same questions,
only the **data source** swapped. The goal is to isolate what the semantic model's
**Prep-for-AI** (AI instructions + verified answers, authored on the model) actually
contributes on top of the agent's own **Agent instructions**.

## Setup

Two semantic models published to the workspace, holding the **same data**:

| Model | Prep-for-AI on the model? |
|---|---|
| `ContosoRetail` | ✅ yes (AI instructions + verified answers) |
| `ContosoRetail V2` | ❌ no |

Both are added as data sources to **one** Data Agent whose **Agent instructions**
carry the business guardrails (currency, additivity, Spanish dimension values,
labeled tables). To run each round, tick a single source, **Publish**, then ask the
questions against the published agent.

> The consumption endpoint always reads the **published** state, not the draft.
> Tick the source you want → Publish → then ask.

## The three questions (identical for both rounds)

1. *What were total sales in 2024? State the currency. Then show the exact DAX query you executed.*
2. *What is the margin percentage for 2024? Then show the exact DAX query you executed.*
3. *Show total sales by product category for 2024 as a labeled table. Then show the exact DAX query you executed.*

Q1 probes the **currency** guardrail, Q2 the **non-additive** guardrail (a rate must
be recomputed, never summed), Q3 the **Spanish dimension values** + labeled-table
guardrail — and, in its DAX, whether the agent names the **real** columns.

## Results

| | **A — V2 (no Prep-for-AI)** | **B — ContosoRetail (with Prep-for-AI)** |
|---|---|---|
| **Q1 total 2024** | `10,387,132 MXN` ✅ | `10,387,132 MXN` ✅ |
| Q1 DAX shown | `SUMMARIZECOLUMNS(DimDate[Year], FILTER(…=2024), …, [Total Sales])` | `CALCULATE([Total Sales], YEAR(DimDate[Date]) = 2024)` |
| **Q2 margin %** | `19.6%` ✅ (recomputed, not summed) | `19.6%` ✅ (recomputed, not summed) |
| Q2 DAX shown | `DIVIDE([Gross Margin], [Total Sales])` filtered to 2024 | `SUMMARIZECOLUMNS(DimDate[Year], "Margin %", [Margin %]) WHERE …` |
| **Q3 by category** | Spanish table ✅ (same figures) | Spanish table ✅ (same figures) |
| Q3 DAX shown | `'DimProduct'[Category]` ❌ **column does not exist** | `DimProduct[CategoryName]` ✅ **exact real column** |

Q3 figures (both rounds, MXN):

| Categoría | Total de Ventas 2024 |
|---|---:|
| Electrónica | 3,489,973 |
| Videojuegos y Juguetes | 2,929,040 |
| Electrodomésticos | 2,085,640 |
| Música, Películas y Medios | 1,882,478 |

## Findings

1. **The numbers are identical.** V2 is a copy of the same data, so Prep-for-AI
   changed nothing in the results — not a single peso.
2. **The guardrails hold in BOTH rounds** — MXN without conversion, non-additive
   margin recomputed, Spanish categories, labeled table. They live in the **Agent
   instructions**, not on the model. → With strong agent instructions, most of the
   grounding comes from the agent prompt, not from the model's Prep-for-AI.
3. **Where Prep-for-AI does show up: schema fidelity in the DAX.** In Q3 the
   Prep-for-AI round wrote the **real** column name (`DimProduct[CategoryName]`);
   the no-Prep round invented `[Category]`. That is the marginal benefit — it names
   columns and tables correctly, which is exactly what curbs errors on the less
   "guided" questions a real user will ask.

## Honest caveat

The *"exact DAX executed"* the agent prints is **not guaranteed to be the literal
query** — it is the LLM's reconstruction. Evidence: round B's Q2 shows
`SUMMARIZECOLUMNS(...) WHERE ...`, which is **not valid DAX**. What is trustworthy
are the **numbers** (cross-checked against a direct DAX `executeQueries` run) and the
**column names** the model chooses. To capture the *literal* query you would need an
XMLA trace on the Fabric semantic model (heavier; out of scope here).

## Reproduce it manually

1. Publish two semantic models with the **same data** — one with Prep-for-AI, one
   without (`… V2`).
2. Create one Data Agent; **Add data** → add both models.
3. Paste the **Agent instructions** (see [`instructions.md`](instructions.md)).
4. Round A: tick **only V2** → **Publish** → in **Test data agent**, ask the three
   questions; copy each answer + the DAX it shows.
5. Round B: untick V2, tick the **Prep-for-AI** model → **Publish** → ask the same
   three questions; copy answer + DAX.
6. Compare. You should see identical figures, guardrails honored in both, and the
   Prep-for-AI round using the exact column names.

## Round C — the isolation run (bare Agent instructions)

Rounds A/B still carried the guardrails in the Agent instructions, so to isolate the
variable we stripped them. Two **separate** agents (to rule out caching), each wired to
one model, both given the same bare prompt:

> `You are a retail sales analyst for Contoso. Answer questions about the ContosoRetail semantic model.`

| | **C-A · V2 (bare, no Prep)** | **C-B · ContosoRetail (bare, with Prep)** |
|---|---|---|
| Q1 total 2024 | `10,387,132` **MXN** ✅ | `10,387,132` **MXN** ✅ |
| Q2 margin % | `19.6%` ✅ (not summed) | `19.6%` ✅ (not summed) |
| Q3 by category | Spanish ✅, right figures | Spanish ✅, right figures |
| DAX column names | `FactSales[SalesAmount]`, `FactSales[GrossMargin]`, `DimProduct[Category]` ❌ invented | `[Total Sales]`, `DimProduct[CategoryName]`, `DimCurrency[CurrencyCode]` ✅ real |

**The surprise:** with a bare prompt, both agents *still* returned the right number,
`MXN`, and Spanish categories. Those three never came from the instructions — they are
baked into the **model** itself:

- **MXN** → the measures' format string / `DimCurrency` (model metadata).
- **Spanish** → the actual **data values** (the category *is* named "Electrónica").
- **Non-additive margin** → the `[Margin %]` measure is already defined; the agent uses
  it and gets it right on its own.

## The full picture — four combos, same questions

| Combo | Numbers | MXN | Spanish | **DAX real names** |
|---|:--:|:--:|:--:|:--:|
| A · full instructions + no Prep | ✅ | ✅ | ✅ | ❌ |
| B · full instructions + Prep | ✅ | ✅ | ✅ | ✅ |
| C-A · bare + no Prep | ✅ | ✅ | ✅ | ❌ |
| C-B · bare + Prep | ✅ | ✅ | ✅ | ✅ |

**Only the last column moves — and it tracks Prep-for-AI, not the Agent instructions.**

- **Agent instructions (full vs bare):** on these questions, measurable effect ≈ 0.
- **Prep-for-AI (with vs without):** the *only* measurable delta is **schema-name
  fidelity in the generated DAX** (`DimProduct[CategoryName]` vs the invented
  `[Category]` / `FactSales[SalesAmount]`).

Currency, language and non-additivity were properties of the **model** all along, not of
either instruction layer. Prep-for-AI's (and the agent prompt's) real value would show
on **ambiguous** questions or logic not baked into the model — which measure to pick,
avoiding the disconnected `DimCurrencyExchange`, synonyms. Round D tests exactly that.

## Round D — ambiguous questions (and a Test-pane trap)

Both bare agents asked two deliberately ambiguous questions:

1. *"¿Cuál es el margen total?"* — absolute vs percentage is undefined.
2. *"¿Cuáles son las ventas del último trimestre?"* — the data ends 2024-12-31, so
   "last quarter" relative to today has no data.

**Via the MCP endpoint (the production path) both agents answered identically and
correctly** — verified against direct DAX:

| Question | V2 (no Prep) | ContosoRetail (Prep) | Ground truth |
|---|---|---|---|
| margen total | `$3,938,789` | `$3,938,789 MXN` | `3,938,789` (Gross Margin) ✅ |
| último trimestre | `2024-Q4 $2,653,095` | `2024-Q4 $2,653,095` | `2,653,095` ✅ |

Both correctly resolved "last quarter" to **the last quarter with data (2024-Q4)**, not a
quarter relative to today — good behavior, from both.

**The two-panes trap (the real lesson).** Fabric shows two similar-looking chat surfaces
and they behave very differently:

- **Build agent with AI** — the *authoring copilot*. It helps you configure the agent; it
  chats, proposes SQL/DAX illustratively, asks clarifying questions, and **may not execute
  against the model**.
- **Test data agent** — the *agent runtime*. It calls the query tool, executes DAX, and
  shows *"N step completed · Analyzed ContosoRetail SemanticModel · Execution and output"*.

Our first ambiguous-question captures came from **Build agent with AI**: there the Prep
agent hedged, proposed raw **SQL** (`SUM(Quantity*NetPrice)…`) and said *"no puedo
ejecutar, cópiala y ejecútala en tu entorno"* — never running anything. Re-run in **Test
data agent**, the same Prep agent executed clean DAX and answered — margin returned **both**
`[Gross Margin]` = $3,938,789 **and** `[Margin %]` = 19.8% using the real measures, labeled
in Spanish with MXN. That matches the MCP/API exactly.

**Lesson (matters for anyone evaluating a Data Agent):** evaluate in **Test data agent**
or against the **MCP endpoint** — never in **Build agent with AI**, which is a build-time
assistant, not the runtime. Judging an agent by the authoring copilot is how you get a
false "it can't answer" verdict.

## Overall verdict (A · B · C · D) — corrected

> **Correction (2026-07-23):** an earlier version of this doc claimed the *one* reproducible
> Prep-for-AI delta was DAX schema-name fidelity (with Prep → `DimProduct[CategoryName]`,
> without → invented `[Category]`). That was **retracted**: manual **Test data agent** runs
> show BOTH agents (with and without Prep) generate the correct `DimProduct[CategoryName]` in
> the **executed** query. The invented name only ever appeared in the chat's *reconstructed*
> DAX, not the executed one — non-determinism, not a Prep effect.

- **Numbers, currency (MXN), language (Spanish), and the executed DAX:** identical across
  every combination and both real channels (Test data agent + API) → they come from the
  **model**, not from instructions or Prep-for-AI.
- **No reproducible difference** between with-Prep and without-Prep was found on these
  questions. They were too "clean" to exercise Prep-for-AI (whose value should show on
  ambiguous questions, synonyms, disconnected-table avoidance — a future round).
- **Lessons that hold:** (1) evaluate on **Test data agent** / the **MCP API**, never on
  **Build agent with AI**; (2) the DAX a Data Agent *shows* is a reconstruction — trust the
  **executed** query (Execution & output) and verify numbers against direct DAX.
