# Contributing

Thanks for your interest. This repo is a **reference**, so contributions are held to a reference's bar.

## Ground rules

1. **Never commit a client identifier.** No real names, IDs, GUIDs, or endpoints — ever. The
   sanitization guard ([`scripts/sanitize-check.sh`](scripts/sanitize-check.sh)) runs in CI and will
   fail your PR; run it locally first: `bash scripts/sanitize-check.sh`. See [SANITIZATION.md](SANITIZATION.md).
2. **Keep the two languages in sync.** Every page is a pair: `X.md` (English) and `X.es.md`
   (Spanish). If you edit one, edit its pair, and keep the language-switch badges at the top.
3. **Every section follows the same shape.** *What it is · Why it matters · How to write it well ·
   Anti-pattern · The Contoso example.* Consistency is the point.
4. **Date your claims.** The Fabric Data Agent surface moves fast (preview features, API sunsets).
   Anything version-sensitive gets a date and a source link (prefer Microsoft Learn).
5. **The example is authored clean.** Extend the [Contoso](examples/contoso-vendor-spend/) model;
   don't paste from a real agent and rename.

## Workflow

Fork → branch → run the guard locally → open a PR describing what part of the anatomy you touched
and why. Small, focused PRs review best.
