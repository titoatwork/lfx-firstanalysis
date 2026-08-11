# Scale and cost

## Point of the section

Snippet demos are cheap. Full-manual and full-corpus extract is where cost and
quality trade off. This monorepo publishes **measured** corpus costs, not only
order-of-magnitude estimates.

## Challenge snippets (this pack)

| Call | Scope | Approx tokens | Approx USD |
|------|--------|---------------|------------|
| One snippet × gpt-4o-mini | v3 prompt + snippet | ~0.6–1k in + small out | **≪ $0.01** |
| Prestige frontier × 2 snippets | Sonnet-class CMO+CSR | ~1.3k in + ~1–3k out | **~$0.02–0.10** |
| Dual frontier (Sonnet+Opus) × 2 | optional dual-provider matrix | ~2× above | **~$0.15–0.50** |

Full ISA dual-frontier one-pass estimates cited by public kits are often on the
order of **$10–15** with caching, re-measure before quoting as ours.

**Takeaway:** API spend is not the binding constraint for the shared challenge.
Grounding, schema fidelity, markup robustness, negatives, and review are.

## Measured corpus costs (this monorepo)

Authoritative tables: [`../../docs/metrics.md`](../../docs/metrics.md)

| Run | Scope | ~USD |
|-----|--------|-----:|
| Pilot `machine.adoc` | model-split 2 chunks | **~0.05** |
| Artifact A gpt-4o-mini | **60** param-bearing chunks | **~0.16** |
| v3 WARL ablation mini | **60** chunks | **~0.16** |
| Temporal holdout primary | **26** calls mini | **≪ $0.05** |

These are **measured** full-corpus / pilot / holdout spends. Challenge-only kits
usually only estimate full-manual frontier cost; they do not ship 60-chunk
multi-model agreement tables.

## Design implication

Cost is low enough that further work should optimize for **reliability and review**,
not for squeezing another free model into the matrix. The expensive failure mode
is unreviewed bulk YAML, not API invoices.
