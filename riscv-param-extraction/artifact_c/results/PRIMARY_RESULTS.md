# Artifact C: primary results

**Preregistered:** [`../PREREGISTRATION.md`](../PREREGISTRATION.md), commit `dfa6b23`, 2026-07-27 13:58:34Z, before any model call.
**Model:** `gpt-4o-mini-2024-07-18`, temperature 0, 60 param-bearing chunks, two independent runs of each arm.
**Scored by:** the Part I corpus's own `analyze.py`, unmodified, at the published denominators (DIRECT 100, CSR_RW 51, WARL 24, SW_RULE 2).

---

## The headline is not the hypothesis I registered

I set out to measure whether removing the gold name catalogue reduces recall (H0), and whether CSR
context helps WARL (H1). The first answer is yes, with a caveat. But the result that matters more is
one I did not register, because I did not think to:

> **Adjusted recall on this task is not stable across identical runs.** The same model, the same
> byte-identical prompt, temperature 0, run twice thirty minutes apart, scored 33.9% and 44.6%. That is
> a 10.7 point swing on the headline metric with nothing changed.

Every single-run recall figure in this problem space, including my own published ones and the Spring
baseline this project cites, is one sample from a distribution nobody has measured.

## Results

| Arm | Names given | Context | Run 1 | Run 2 |
|-----|:-----------:|:-------:|------:|------:|
| **A** control, published condition | yes | no | 33.9% | **44.6%** |
| **B** discovery | no | no | 29.4% | 32.2% |

Per class, found / total:

| | A run1 | A run2 | B run1 | B run2 |
|---|---:|---:|---:|---:|
| DIRECT | 45/100 | 51/100 | 43/100 | 42/100 |
| CSR_RW | 6/51 | **21/51** | 7/51 | 6/51 |
| WARL | 9/24 | 7/24 | 2/24 | **9/24** |

## What is established

**H0 holds in direction, twice.** Arm A beat arm B in both runs (33.9 vs 29.4, and 44.6 vs 32.2). Taking
away the complete answer key costs recall. The *magnitude* is not established: the gap was 4.5 points
in one run and 12.4 in the other.

**The variance is in the model, not the harness.** Three checks:

1. The resolved prompts for each arm are **byte-identical** between runs (SHA-256 match, 175,140 bytes
   for arm A).
2. `analyze.py` is **deterministic**: re-scoring run 1 arm A on identical input reproduces 33.9%,
   6/51, 9/24, 45/100 exactly.
3. The harness reproduces the published Claude figures exactly (72.9%, 88.4%, 12/24, 83/100, 32/51).

**The alignment layer amplifies small output differences into large recall differences.** Run 2 arm A
produced *fewer* raw parameters than run 1 (214 against 228) and yet matched far more gold (79 against
60). Exact-name matches were identical at 9 in both. So the swing came entirely from the alias,
one-to-many and fuzzy alignment passes, not from the model finding more things by name.

That is the mechanism worth flagging: **adjusted recall is dominated by an alignment step that is
highly sensitive to small changes in phrasing**, so it converts modest output variation into large
metric variation.

## What is not established, and was withdrawn

**The WARL result.** Run 1 looked like a clean finding: WARL fell 9/24 to 2/24 when the catalogue was
removed, while DIRECT stayed flat. That is exactly the mechanism I have been arguing, and I nearly
reported it.

Run 2 destroys it. Arm A fell to 7/24, and arm B rose to **9/24**, higher than arm A. The direction
reverses. On a 24-item denominator with this much run-to-run movement, nothing about WARL can be
claimed from this data.

Had I published after one run, I would be retracting a headline finding now.

## Consequences

**For this project.** Single-run comparison is not a sound basis for deciding whether an intervention
helped. The v3 prompt ablation, my Artifact A multi-model comparison, and the Part I baseline are all
single runs. None of them are wrong, but none of them carry the precision their presentation implies.
Any future claim of the form "X improved recall from a to b" on this corpus needs N > 1 and a reported
spread.

**For the metric.** If the goal is measuring extraction quality, an adjusted-recall figure that moves
10 points on identical inputs is measuring the alignment heuristics as much as the extraction. Exact
match was stable across all four runs. That argues for reporting exact and adjusted separately, and for
treating adjusted recall as a range.

## Limitations, stated plainly

- **Two runs per arm.** Enough to demonstrate instability, nowhere near enough to characterise the
  distribution. A spread measured from n=2 is not a confidence interval.
- **One model.** `gpt-4o-mini` only. Whether other models or providers are this unstable is untested
  here. @RAJVEER42 independently reports non-identical output across N=3 runs at temperature 0 on
  different providers, which is corroboration but not measurement.
- **Arms C and D are not yet run**, so H1, H2 and H4 are open.
- **H5 is unrunnable as designed** on this data: agreement requires two models within an arm, and only
  one model has been run. It needs a second model before it can be evaluated at all.
- The registered rule applies: a null here is "not detected under a design built for something else",
  not evidence of absence.

## Reported upstream

Filed as [riscv/riscv-unified-db#2163](https://github.com/riscv/riscv-unified-db/issues/2163), against
[#1750](https://github.com/riscv/riscv-unified-db/issues/1750) (LFX Phase 4, "run it against at least 2
different LLMs"), since single-run comparison between models cannot distinguish a capability difference
from this much run-to-run movement.

Checked for prior art before filing: no existing issue or PR upstream covers evaluation variance,
nondeterminism or reproducibility of recall. The `long_name: TODO` census was **not** filed, because
[#2155](https://github.com/riscv/riscv-unified-db/pull/2155) is already active on that.

## Reproduction

```bash
cd riscv-param-extraction/artifact_c
python scripts/build_context.py --udb-root ../../.udb-corpus --check-only
python scripts/score_arms.py --validate          # harness against published figures
python scripts/compare_runs.py --a runs/<run1> --b runs/<run2> --arm A
```

Every raw response, parsed candidate list, resolved prompt sample and per-call record for all four
runs is committed under `runs/`. The retention gate exists because the earlier Artifact A per-chunk
outputs were not kept, which is why its exclusive sets cannot be audited today.
