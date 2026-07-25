# Overmatch status vs Anshul (living)

**Updated:** 2026-07-26 ~05:00 (pre-sleep; **wake still morning of 26 Jul**)  
**Public tip:** `58f91de` · **Standard:** erase Anshul on every mentor axis (not soft #2).

| Axis | Anshul | Us now | Mile? | Blocker |
|------|--------|--------|-------|---------|
| Challenge pack exists | Public repo | **Public monorepo** `58f91de` | **Yes** | Confirm Actions green |
| Fail-closed fixtures | 2 | **4** | **Yes** | — |
| Hard negatives | 2 | **4** | **Yes** | — |
| Markup robustness | 3 cases | **3** + tag-aware | **Match+** | — |
| Trigger relevance WARN | no | **`--check-triggers`** (local; not all pushed yet) | **Partial** | optional push |
| CI | Yes | **GHA public** | **Yes** | Actions tab |
| Multi-strategy controls | weak | **score_strategies.py** | **Yes** | — |
| Known-param bench | n=13 | **n=15** + caveats | **Yes** | — |
| Scale/cost + measured corpus $ | estimate | estimate + **A/v3 measured** | **Yes** | — |
| Live 3-model LLM matrix | **Yes** | **Not yet** | **NO** | **API keys + go** |
| Merged UDB PR | **#1967** | Draft only | **NO** | **`GO OPEN UDB PR`** |
| Corpus GT / multi-model / export / null | weak/none | **Lead** | **Yes** | defend |
| Single monorepo story | challenge-only | challenge+corpus+export | **Yes** | — |

## What closes the last two “his lead” cells

1. **Live multi-model:** set keys → run `challenge/docs/LIVE_MULTI_MODEL.md` → commit `results/live/`.  
2. **UDB PR:** open draft fix (`mhmpcountinhibit` → `mcountinhibit`) from clean `main` → respond to review → merge.

Until both land, do **not** claim “mile on everything.” Claim: **mile on offline challenge engineering + science; two public axes still open.**
