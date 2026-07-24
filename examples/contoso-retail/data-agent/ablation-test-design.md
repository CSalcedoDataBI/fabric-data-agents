# Reproducible test — make Prep-for-AI's effect *visible*

The first ablation (A/B/C/D) measured a **clean model + literal questions** — the case
where, per Microsoft's own docs, Prep-for-AI has little to add. This is the follow-up
designed to **force** a Prep-for-AI difference, with a precomputed ground truth so the
result is not hand-waving.

## Design

Isolate ONE variable: a single **AI instruction** (Prep-for-AI) with a business definition
the model cannot infer and the LLM cannot guess (deliberately counterintuitive — the
campaign *excludes* December). With Prep the agent is right; without Prep it is wrong with a
**different, visible number**.

- **Treatment model** `ContosoRetail` — add ONE line to *Prep data for AI → AI instructions*,
  then **Publish**:
  > Contoso's 'temporada de rebajas de fin de año' (end-of-year sale season) covers ONLY
  > October and November (DimDate[Month] = 10 or 11); it excludes December.
- **Control model** `ContosoRetail V2` — unchanged (no Prep-for-AI).
- Everything else identical: same data, same bare agent prompt.

## Questions (ask both agents in **Test data agent**)

| # | Question | With Prep (ContosoRetail) | Without Prep (V2) |
|---|---|---|---|
| Control | ¿Cuáles fueron las ventas totales de 2024? | 10,387,132 MXN | 10,387,132 MXN |
| Treatment | ¿Cuánto vendimos en la temporada de rebajas de fin de año de 2024? | **1,844,999** (Oct+Nov) ✅ | asks / guesses Nov+Dec **1,728,113** or Q4 ✗ |

## Ground truth (verified via direct DAX `executeQueries`)

| Window 2024 | Total Sales (MXN) |
|---|---|
| Full year (control) | 10,387,132 |
| **Oct + Nov (defined "temporada")** | **1,844,999** |
| Nov + Dec (the naive guess) | 1,728,113 |

## Protocol

1. Add the AI instruction to `ContosoRetail` Prep-for-AI + **Publish**. Leave `V2` untouched.
   (AI instructions require **Q&A enabled** on the model; Prep changes can take ~15 min to
   propagate.)
2. Ask both questions in **Test data agent** (NOT Build agent with AI). Capture the answer,
   the DAX from *Execution & output*, and the number.
3. **Repeat 3×** per agent — the LLM is non-deterministic; we want consistency, not one lucky
   run. (An MCP-endpoint battery can double-confirm.)
4. Compare against the ground-truth table. With-Prep should hit 1,844,999 consistently;
   without-Prep should not.

## Test 2 — internal segment code (a different mechanism)

Where Test 1 maps jargon → a **time window**, Test 2 maps an **unguessable internal code → a set
of dimension values**. The LLM has zero prior knowledge of "Programa Aurora", so without Prep it
*cannot* answer; with Prep it resolves to two exact categories.

- **Treatment instruction** (Prep-for-AI, `ContosoRetail`):
  > Contoso's 'Programa Aurora' groups ONLY the product categories Electrónica and
  > Electrodomésticos. For questions about Programa Aurora, filter DimProduct[CategoryName] to
  > those two categories and include no others.

| # | Question | With Prep (ContosoRetail) | Without Prep (V2) |
|---|---|---|---|
| Treatment | ¿Cuánto vendió el Programa Aurora en 2024? | **5,575,613** (Electrónica + Electrodomésticos) ✅ | cannot know the code → asks / refuses / hallucinates ✗ |

Ground truth (direct DAX): Electrónica 3,489,973 + Electrodomésticos 2,085,640 = **5,575,613** MXN.

## Gotcha — two levels of propagation (learned live)

Updating the model's Prep-for-AI is **necessary but not sufficient**. There are two hops:

1. **Model → Prep-for-AI** — publish/replace the semantic model (verifiable via
   `getDefinition` on the model: the culture file must contain the instruction).
2. **Data Agent → model snapshot** — the Data Agent does **not** re-read the model's Prep-for-AI
   live per query; it picks it up when you (re-)add/refresh the semantic-model source and **Publish
   the agent**. Changes also take ~15 min to propagate.

Symptom we hit: the model already had the instruction (`getDefinition` = present) yet the agent
still guessed — because the agent's snapshot predated the model change. **Re-sync the source +
Publish the agent, then wait**, before concluding anything.

## Why this is rigorous
- Single variable (the AI instruction); ground truth precomputed and verifiable.
- Unguessable, counterintuitive definition → the failure mode returns a *different* number
  (1,728,113), not an ambiguous tie.
- Exercises the documented "map business jargon → fields/filters" mechanism.

## Harder variant — AI data schema (duplicate measure)

Zero-ambiguity alternative (costs one measure on **both** models):
- Add `Ventas Brutas = SUMX(FactSales, FactSales[Quantity] * FactSales[UnitPrice])` (gross,
  before discount) to both. `Total Sales` stays net.
- Now "ventas" is ambiguous: **net 10,387,132** vs **gross 11,289,599** (both DAX-verified).
- On `ContosoRetail`, exclude `Ventas Brutas` from the AI data schema (or instruct
  `'ventas' = [Total Sales]`). Ask *"¿ventas de 2024?"*: with Prep → net; without Prep → may
  return gross. Two deterministic numbers, nothing to guess.

See the measured baseline in [`ablation-prep-for-ai.md`](ablation-prep-for-ai.md) and why the
clean-model null result matches Microsoft's docs.
