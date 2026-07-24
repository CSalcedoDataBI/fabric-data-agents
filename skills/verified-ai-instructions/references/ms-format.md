# Microsoft AI-instructions format & best practices

Distilled from Microsoft Learn: *Prepare your data for AI: AI instructions*
(`copilot-prepare-data-ai-instructions`). Follow this so a Data Agent / Copilot responds better.

## Structure

Write **prompt-engineered** instructions, not a flat dump. Two content types Microsoft calls out:

1. **General business context & interpretation** — industry, goals, terminology, operational logic.
   - "Busy season is October to February."
   - "When a user mentions *ABCD*, they mean the **total invoice** field."
   - "A lower attrition percent is more positive."
2. **Analysis rules** — how to slice/prioritize.
   - "Always analyze sales on a quarterly basis."
   - "Use the `sales_fact` table as the primary source for all sales questions."
   - "When a user asks about product sales, always ask for clarification on location."

## The seven best practices (apply all)

1. **Be explicit and specific.** Assume the agent knows nothing about your model or business. Lead
   with a role + context line: *"You are a retail sales analyst for Contoso… use the model's defined
   measures, never invent fields."*
2. **Use descriptive language / examples.** Give example values: *"product categories: Electrónica,
   Electrodomésticos, …"*; *"Channel values: Online, Store."*
3. **Avoid ambiguity.** Say what to emphasize AND what to avoid: *"For margin use [Gross Margin]
   (absolute) or [Margin %] (rate); do not sum [Margin %]."*
4. **Group related instructions** under headers/sections by theme (dates, metrics, dimensions,
   currency, output). Structure helps the LLM.
5. **Mind instruction order** — earlier lines carry weight; put the role/context and the highest-value
   rules first.
6. **Break complex rules into steps** — "define *top customers* by first looking at revenue, then
   returning the highest order values."
7. **Keep it focused.** Fewer sharp instructions beat many broad ones; conflicts confuse LLMs. Hard
   limit **10,000 characters**.

## A good skeleton

```
You are a <role> for <business/context>. Answer questions about <domains> using this semantic model.
Be precise, use the model's defined measures, and never invent numbers, measures, or fields.

## Dates
- Primary date is <DimDate[Date]>, related to <Fact[Date]>. <OtherDate> is <purpose> only.
- Reporting period is <min>–<max>.

## Measures and how to aggregate
- <Metric term> = the measure [<Measure>]. Never re-aggregate a raw column when a measure exists.
- Additive (may be summed): [...]. Non-additive (never sum; recompute): [...].
- Distinct counts are semi-additive — do not sum across periods.

## Dimensions and breakdowns
- Default breakdown when none named: <Dim[Col]>, <Dim[Col]>, ...
- Example values / language notes.

## Currency and units
- <single currency / conversion rule>.

## Output
- Prefer labeled tables with units for rankings/breakdowns.
```

## Limits & caveats to tell the user
- Unstructured guidance — the LLM interprets it; no guarantee it's followed exactly. For hard rules,
  fix the model instead.
- Model-level only (not per-report, not per-persona). End users can't see or disable them.
- 10,000-character cap. You currently can't upload/import into the Desktop dialog (paste manually) —
  which is why this skill writes the on-disk `CustomInstructions` directly.
