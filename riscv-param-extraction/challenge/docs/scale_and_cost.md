# Scale and cost (challenge context)

## Full ISA manual (order-of-magnitude)

Public challenge kits often cite full-manual scale for Anthropic frontier models.
Anshul-class estimate (for comparison only; re-measure before quoting as ours):

| Quantity | Typical cited ballpark |
|----------|------------------------|
| Manual `.adoc` files | ~147 |
| Words | ~2.8e5 |
| Section-sized chunks | ~845 |
| Dual frontier full pass | on the order of **$10–15** with caching |

**Takeaway shared with elite kits:** API spend is usually not the binding
constraint — grounding, schema fidelity, markup robustness, and review are.

## Measured costs in *this* monorepo (corpus science)

Authoritative tables: [`../docs/metrics.md`](../docs/metrics.md)

| Run | Scope | ~USD |
|-----|--------|-----:|
| Pilot machine.adoc | model-split 2 chunks | ~0.05 |
| Artifact A gpt-4o-mini | 60 param-bearing chunks | ~0.16 |
| v3 WARL ablation mini | 60 chunks | ~0.16 |

These are **measured corpus runs**, not challenge-snippet estimates. Use them
when comparing cost/quality of full extract vs 2-snippet demos.
