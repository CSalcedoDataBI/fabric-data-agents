[![Lang: English](https://img.shields.io/badge/lang-English-1f6feb?style=flat-square)](03-agent-instructions.md)
[![Idioma: Español](https://img.shields.io/badge/idioma-Espa%C3%B1ol-2da44e?style=flat-square)](03-agent-instructions.es.md)
&nbsp;·&nbsp; [↑ Index](../../README.md)

# 03 · Agent-level instructions

## What it is

Agent-level instructions are the **global rules** that apply to every question, regardless of which
source answers it. They live in the same Data agent instructions field as the identity
([01](01-identity-and-role.md)) — the shared **15,000-character** budget — but where identity says
*who the agent is*, these say *how it must behave*: additivity discipline, disambiguation, null
handling, output shape, and the things it must never do.

Keep them distinct from **source-level** instructions ([04](04-source-instructions-and-fewshots.md)),
which teach the agent how to query *one specific source*. Agent-level rules are source-agnostic
behavior; source-level rules are query craft.

## Why it matters

Most wrong answers from a Data Agent are not translation failures — the SQL or DAX is valid — they are
**behavioral** failures the model would make by default and that only an explicit rule prevents:

- **Additivity.** A model will happily `SUM` a percentage or average a rate across rows. Summing a
  non-additive measure is arithmetically meaningless, and nothing stops it unless you say so.
- **Silent guessing.** Asked to "show spend" with no period or grain, the default is to pick one and
  answer as if it were asked for — hiding the assumption. A disambiguation rule turns that into a
  stated assumption or a one-line clarifying question.
- **Per-capita ratios.** "Sales per customer" is wrong if the denominator is the wrong population. A rule
  that forces the agent to *name the denominator* makes the number auditable.
- **Governance boundaries.** Instructions operate *below* organizational and role-based intent; RLS
  is enforced whether or not you mention it. Stating "you answer under the caller's identity; never
  reason around permissions" sets the expectation honestly rather than implying the agent polices
  access itself.

## How to write it well

- **Make rules testable and imperative.** "Only additive measures may be summed; never total a %, a
  rate, or an average across rows" is checkable; "be accurate" is not.
- **Force disambiguation over guessing.** Require the agent to state the assumption it is making, or
  ask one short clarifying question, when period or grain is missing.
- **Name denominators.** Any per-unit ratio must label its denominator and population.
- **Prefer tables with units** for breakdowns, rankings, and multi-measure answers — prose hides the
  numbers.
- **Encode "never invent."** No measures, dimensions, or values that are not in the source.
- **Give users steering, not a maze.** A small, documented command vocabulary (a help/catalog/validate
  set) is more discoverable than a wall of prose — see the Contoso `>` commands below.
- **Respect the character budget.** Identity + global rules share 15k characters; push
  source-specific query examples down to [04](04-source-instructions-and-fewshots.md).

## Anti-pattern

The **"be helpful and accurate" instruction** — aspirational, unverifiable, and behaviorally empty:
it prevents none of the failures above. Its opposite is the **novella of edge cases** that blows the
character budget and buries the three rules that actually matter. A third anti-pattern is
**instructing around governance** — telling the agent to "show all data" in the hope of bypassing
RLS; it cannot, and the instruction only misleads whoever reads it next.

## The Contoso example

Contoso's [agent instructions](../../examples/contoso-retail/data-agent/instructions.md) are a compact set
of global rules, each targeting a real failure mode:

1. **Use defined measures** — never re-aggregate a raw column when a measure exists.
2. **Respect additivity** — only additive (volume) measures may be summed; never total a %, rate, or
   average across rows.
3. **Report companion measures together** — when a measure declares `ALSO REPORT WITH IT: …`, return
   the companions for the same period and filters, unless the user says "only" / "just".
4. **Per-capita ratios name their denominator** — `[Sales per Customer]` divides by *Distinct
   Customers* (customers who bought in the period); label it ("per customer (Distinct Customers = N)"),
   never imply the total customer base.
5. **Prefer tables**, **6. RLS respected automatically**, **7. Disambiguate before guessing.**

It also ships a small `>` **command vocabulary** (`>help`, `>about`) so users can steer the agent
explicitly — commands begin with `>` rather than `/` precisely because host assistants intercept a
leading slash. These are agent-level because they hold for every question, independent of which
source (here, only one) answers it.

---
_Next: [04 · Source instructions & few-shots →](04-source-instructions-and-fewshots.md)_
