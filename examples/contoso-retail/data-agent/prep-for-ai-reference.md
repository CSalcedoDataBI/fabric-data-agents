[![Lang: English](https://img.shields.io/badge/lang-English-1f6feb?style=flat-square)](prep-for-ai-reference.md)

# Prep-for-AI — the measured reference (Contoso Retail Data Agent)

Canonical, AI-readable consolidation of everything the **ablation runs** actually
proved about how a Fabric **Data Agent** over a **Power BI semantic model** uses the
model's **Prep-for-AI** (AI instructions, AI data schema, verified answers) versus the
agent's own instructions. Every claim here is backed by the evidence files linked at the
bottom; nothing is asserted that was not either run against the live agent or verified
with a direct DAX `executeQueries` on the model.

> **Scope & provenance.** Data is **synthetic** (Contoso Retail), single currency
> **MXN**, reporting period **2023-01-01 → 2024-12-31**. Ground-truth numbers were
> computed with Power BI REST `POST /datasets/{modelId}/executeQueries`. Agent answers
> were captured from the **Test data agent** pane and the published **MCP endpoint** —
> never from *Build agent with AI* (see [Evaluation traps](#evaluation-traps-read-before-you-judge-an-agent)).

---

## TL;DR (the measured bottom line)

1. **On clean, literal questions, Prep-for-AI changes nothing you can measure.** Numbers,
   currency (MXN), language (Spanish), and the *executed* DAX were **identical** with and
   without Prep-for-AI, across four instruction combos and both real channels (Test data
   agent + MCP API). Those properties come from the **model** — format strings, actual
   data values, and defined measures — not from any instruction layer.
2. **Prep-for-AI earns its keep on terms the LLM cannot guess.** A business definition the
   model cannot infer (a jargon phrase, an internal code) is resolved *correctly* only when
   it is written into the model's Prep-for-AI. Without it, the agent guesses a different,
   wrong number — or refuses. See [Ground truth](#ground-truth-verified-answers).
3. **Two layers read the question, and they read different things.** The **orchestrator**
   reads the question + the **agent (system) instructions** and can reformulate/route it;
   the **DAX-generation tool** reads only the reformulated question + **model metadata +
   Prep-for-AI**, and ignores per-source *data-source* instructions. This is why agent
   instructions still shape answers even though Microsoft documents that the generator
   relies solely on the model. See [The two layers](#the-two-layers-what-reads-what).
4. **One term, one place.** Define any business term in exactly one layer. When the agent
   instructions and the model's Prep-for-AI define the same term differently, there is no
   clean precedence — the collision is non-deterministic and produces confidently wrong
   answers. See [What goes where](#what-goes-where).
5. **Updating the model is necessary but not sufficient.** There are **two propagation
   hops** (model → Prep-for-AI, and Data Agent → model snapshot). Re-sync the source,
   **Publish the agent**, and wait (~15 min). See [Propagation & caching](#propagation--caching-the-two-hops).
6. **Evaluate on the runtime, not the authoring copilot**, and trust the **executed** DAX,
   not the DAX the chat *prints*. See [Evaluation traps](#evaluation-traps-read-before-you-judge-an-agent).

---

## The two layers (what reads what)

A Data Agent answering over a semantic-model source runs the question through two distinct
readers. Keeping them separate resolves an apparent contradiction in the docs — that the
generator "relies solely on the model," yet agent instructions still change answers.

| Layer | Reads | Can it change the final answer? |
|---|---|---|
| **Orchestrator** (agent runtime / planner) | the user's question **+ agent (system) instructions** | **Yes** — it can reformulate, expand, disambiguate and route the question (e.g. resolve business jargon) *before* handing it down. |
| **DAX-generation tool** (NL2DAX) | the **already-reformulated** question **+ model metadata + Prep-for-AI** (AI instructions, AI data schema, verified answers) | **Yes** — it writes the DAX. It does **not** read per-source *data-source instructions* set at the agent level (Microsoft's documented behavior). |

**Consequences that were measured:**

- With **strong agent (system) instructions**, most grounding comes from the agent prompt:
  a model **without** Prep-for-AI still honored currency (MXN), non-additivity (recomputed
  margin), and Spanish dimension values — because those guardrails were in the agent
  instructions and/or baked into the model, and the orchestrator carried them through.
- With a **bare** agent prompt, the agent *still* returned the right number, MXN, and
  Spanish categories — proving those three were properties of the **model** all along
  (format string / `DimCurrency`, the literal data values, the defined `[Margin %]`
  measure), not of any instruction layer.
- The layer that the **model's Prep-for-AI** uniquely controls is the **DAX-generation
  tool's** view: which fields it sees (AI data schema), what business terms map to
  (AI instructions), and which governed Q→DAX patterns it can match (verified answers).

> **Documented vs. observed.** Microsoft documents only that the NL2DAX generator, for a
> semantic-model source, reads the model's metadata + Prep-for-AI and that per-source
> *example queries / data-source instructions* set on the agent are ignored. The
> orchestrator-reformulation path — how top-level **agent instructions** still influence the
> answer — is under-documented; treat it as the reconciling mechanism, and always **test the
> seam** rather than assume precedence.

---

## What goes where

Author each kind of substance in exactly the layer that reads it. This table is the
decision rule; the file-by-file "what you author / where it lives" map is in the
[example README](README.md).

| Substance | Author it on | Read by | Notes |
|---|---|---|---|
| Role, scope, tone, output shape, routing, `>` steering commands | **Agent instructions** (system prompt) | Orchestrator | Also carries global guardrails (currency, additivity, language) that the orchestrator propagates. 15,000-char budget. |
| Business-term → field/filter mappings, jargon, internal codes, additivity rules, measure semantics, breakdown defaults, currency rule | **Model → Prep-for-AI → AI instructions** | DAX-generation tool | The only place the generator reads business logic. 10,000-char limit. Requires Q&A enabled on the model. |
| Which tables/columns/measures the AI can see (Visible/Hidden) + synonyms | **Model → Prep-for-AI → AI data schema** | DAX-generation tool | Hide look-alike measures so "sales" cannot resolve to the wrong one. Include dependent objects a measure references. |
| Governed, tested question → DAX few-shots | **Model → Verified Answers** | DAX-generation tool | For a semantic-model source, few-shots authored on the **agent** (`example-queries.json`) are **ignored**; seed them on the model. |

### The rule: one term, one place

Define any given business term in **exactly one** layer. If the agent instructions say
"Programa Aurora = Videojuegos" and the model's Prep-for-AI says "Programa Aurora =
Electrónica + Electrodomésticos," the two readers disagree and **there is no clean
precedence**. The observed failure mode is non-deterministic: across repeated runs the same
conflicted question can return a confidently **mislabeled** answer, an **empty** result
(both contradictory filters applied at once → no rows), or a **different** number each time.
A term defined once, in the layer that the generator actually reads (Prep-for-AI), is the
only configuration that answers consistently.

---

## Ground truth (verified answers)

All figures verified via direct DAX `executeQueries` on the model. These are the values a
correctly configured agent must return.

### Baselines

| Window | Measure | Value (MXN) |
|---|---|---:|
| Full year 2023 | Total Sales | 9,516,546 |
| Full year 2024 | Total Sales | 10,387,132 |
| 2024 | Margin % | 19.6% |
| All periods | Gross Margin | 3,938,789 |
| 2024-Q4 | Total Sales | 2,653,095 |

### 2024 sales by product category (Spanish dimension values)

| Categoría | Total Sales 2024 (MXN) |
|---|---:|
| Electrónica | 3,489,973 |
| Videojuegos y Juguetes | 2,929,040 |
| Electrodomésticos | 2,085,640 |
| Música, Películas y Medios | 1,882,478 |

### The jargon cases — where Prep-for-AI is decisive

These are terms the model cannot infer and the LLM cannot guess. Each is a single AI
instruction whose ground truth is precomputed, so the failure mode is a *different, visible*
number, not an ambiguous tie.

| Business term (as defined in Prep-for-AI) | Resolves to | Correct answer 2024 (MXN) | Without Prep-for-AI |
|---|---|---:|---|
| `temporada de rebajas de fin de año` (end-of-year sale season) | `DimDate[Month] IN {10, 11}` (Oct+Nov; **excludes December** — counterintuitive on purpose) | **1,844,999** | naive Nov+Dec guess = **1,728,113** (wrong, different number) |
| `Programa Aurora` (internal segment code) | `DimProduct[CategoryName]` ∈ {Electrónica, Electrodomésticos} | **5,575,613** (3,489,973 + 2,085,640) | the LLM has no prior for the code → asks / refuses / hallucinates |

> Every one of these mappings was checked against the real model before being written:
> `DimDate[Month]` is int64 1–12 with data in Oct+Nov; both category values exist in
> `VALUES(DimProduct[CategoryName])`. A *verified* instruction, not a plausible-sounding one
> — see the verification table in [`../model/prep-for-ai/ai-instructions.md`](../model/prep-for-ai/ai-instructions.md).
> The same discipline turned a **harmful** draft instruction ("convert currencies with
> `DimCurrencyExchange`") into a correct one once the data showed a single currency and a
> disconnected table.

---

## What Prep-for-AI does and does NOT change

Measured across four instruction combos (full agent instructions ± Prep; bare prompt ±
Prep), same questions, both real channels:

| Property | With Prep | Without Prep | Where it actually comes from |
|---|:--:|:--:|---|
| The number | ✅ identical | ✅ identical | the **model** (data + defined measures) |
| Currency (MXN) | ✅ | ✅ | measure format string / `DimCurrency` metadata |
| Language (Spanish) | ✅ | ✅ | the literal **data values** ("Electrónica" *is* the value) |
| Non-additive margin recomputed | ✅ | ✅ | the `[Margin %]` measure is already defined |
| **The executed DAX (column/measure names)** | ✅ real names | ✅ real names | the **model** — *both* generate `DimProduct[CategoryName]` |
| **Unguessable jargon resolved correctly** | ✅ | ❌ | **Prep-for-AI** — the only layer that carries the mapping |

> **Retraction (2026-07-23), carried forward.** An earlier ablation draft claimed the one
> reproducible Prep-for-AI delta on clean questions was DAX **schema-name fidelity** (with
> Prep → `DimProduct[CategoryName]`; without → invented `[Category]`). That was **retracted**:
> in the **executed** query, both agents (with and without Prep) use the real
> `DimProduct[CategoryName]`. The invented name appeared only in the chat's **reconstructed**
> DAX — non-determinism, not a Prep effect. On genuinely clean questions there is **no
> reproducible difference**; Prep-for-AI's measurable value shows on the **jargon** cases
> above, which matches Microsoft's own guidance that Prep adds little to a clean model + a
> literal question.

---

## Propagation & caching (the two hops)

Updating the model's Prep-for-AI is **necessary but not sufficient**. Two hops must both
complete before a query reflects a change:

1. **Model → Prep-for-AI.** Publish/replace the semantic model. Verifiable: `getDefinition`
   on the model — the culture file must contain the instruction.
2. **Data Agent → model snapshot.** The Data Agent does **not** re-read the model's
   Prep-for-AI live per query. It picks up the change only when you **(re-)add / refresh the
   semantic-model source** and **Publish the agent**. Changes also take **~15 min** to
   propagate.

**Symptom observed live:** the model already had the instruction (`getDefinition` = present)
yet the agent kept guessing — because the agent's snapshot predated the model change.
**Re-sync the source + Publish the agent, then wait**, before concluding anything.

Prerequisite: **AI instructions require Q&A enabled** on the model (the *Prep data for AI*
tabs are disabled otherwise). The consumption endpoint always reads the **published** state,
never the draft.

---

## Evaluation traps (read before you judge an agent)

- **Two chat surfaces, very different behavior.**
  - **Build agent with AI** — the *authoring copilot*. It helps you configure the agent;
    it chats, proposes SQL/DAX illustratively, asks clarifying questions, and **may not
    execute** against the model. It once hedged, proposed raw SQL, and said "copy it and run
    it in your environment" — running nothing.
  - **Test data agent** — the *runtime*. It calls the query tool, executes DAX, and shows
    "*N step completed · Analyzed … SemanticModel · Execution and output*". Re-run there, the
    same agent executed clean DAX and answered correctly.
  - **Lesson:** evaluate only in **Test data agent** or against the **MCP endpoint**. Judging
    an agent by the authoring copilot is how you get a false "it can't answer" verdict.
- **The DAX the chat prints is a reconstruction, not the executed query.** Evidence: a
  captured answer showed `SUMMARIZECOLUMNS(...) WHERE ...`, which is **not valid DAX**. Trust
  the **numbers** (cross-checked against direct DAX) and the **Execution & output** panel;
  to capture the *literal* query, take an XMLA trace on the model (heavier; out of scope).
- **Verify numbers against direct DAX** (`executeQueries`) — that is the ground-truth channel
  used throughout this reference.

---

## Character limits & prerequisites (quick reference)

| Item | Limit / requirement | Source |
|---|---|---|
| Agent (system) instructions | 15,000 characters (shared identity + rules budget) | repo `docs/anatomy/01`, `03` |
| Model AI instructions (Prep-for-AI) | 10,000 characters | [MS Learn — AI instructions, considerations](https://learn.microsoft.com/power-bi/create-reports/copilot-prepare-data-ai-instructions#considerations-and-limitations) |
| AI instructions require | **Q&A enabled** on the model | [MS Learn — AI instructions, prerequisites](https://learn.microsoft.com/power-bi/create-reports/copilot-prepare-data-ai-instructions) |
| Copilot outputs | **non-deterministic** — set expectations, repeat runs | [MS Learn — Prep for AI tutorial](https://learn.microsoft.com/power-bi/create-reports/tutorial-copilot-power-bi-prepare-model) |

---

## Evidence & references

**Measured evidence (this example):**

- [`ablation-prep-for-ai.md`](ablation-prep-for-ai.md) — the A/B/C/D ablation and the
  corrected verdict ([ES](ablation-prep-for-ai.es.md)).
- [`ablation-raw-runs.md`](ablation-raw-runs.md) — verbatim run captures (rounds A–D) + the
  direct-DAX cross-check.
- [`ablation-test-design.md`](ablation-test-design.md) — the follow-up design that forces a
  Prep-for-AI difference (temporada / Programa Aurora) with precomputed ground truth.
- [`../model/prep-for-ai/ai-instructions.md`](../model/prep-for-ai/ai-instructions.md) — the
  verified AI-instructions block (every line checked against data).
- [`verified-answers.md`](verified-answers.md) · [`instructions.md`](instructions.md) — the
  agent-level contract and the seeded Q→DAX few-shots.

**Microsoft Learn:**

- [Prepare your data for AI — AI instructions](https://learn.microsoft.com/power-bi/create-reports/copilot-prepare-data-ai-instructions)
  (best practices, prerequisites, 10,000-char limit).
- [Write effective prompts for AI instructions](https://learn.microsoft.com/power-bi/create-reports/copilot-prepare-data-ai-instructions#write-effective-prompts-for-ai-instructions).
- [Prepare your data for AI (overview)](https://learn.microsoft.com/power-bi/create-reports/copilot-prepare-data-ai).

**Repo anatomy docs:** [04 · Source instructions & few-shots](../../../docs/anatomy/04-source-instructions-and-fewshots.md) ·
[06 · Direct vs. orchestrator](../../../docs/anatomy/06-direct-vs-orchestrator.md) ·
[03 · Agent-level instructions](../../../docs/anatomy/03-agent-instructions.md).
