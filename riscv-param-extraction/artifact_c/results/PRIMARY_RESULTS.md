# Artifact C: primary results

**Preregistered:** [`../PREREGISTRATION.md`](../PREREGISTRATION.md), commit `dfa6b23`, 2026-07-27 13:58:34Z, before any model call.
**Model:** `gpt-4o-mini-2024-07-18`, temperature 0, the 60 param-bearing chunks.
**Design:** 4 arms, **every arm run twice**, 480 calls.
**Scored by:** the Part I `analyze.py`, unmodified, at the published denominators.

---

## The result, in two parts

**The registered hypotheses are unresolved: the noise floor is larger than every effect the design was built to detect.**

**The unregistered finding is the substantive one:** 85% to 90% of the score this corpus reports is awarded by fuzzy matching rather than by the model naming the parameter, and that heuristic layer is where essentially all of the run-to-run instability lives. That was found while diagnosing the variance, not predicted in advance, and it is labelled exploratory throughout.

| Arm | Condition | run 1 | run 2 | spread | mean |
|-----|-----------|------:|------:|-------:|-----:|
| **A** | names, no context | 33.9% | 44.6% | **10.7** | 39.2% |
| **B** | no names, no context | 29.4% | 32.2% | 2.8 | 30.8% |
| **C** | names + context | 32.8% | 39.5% | 6.7 | 36.1% |
| **D** | no names + context | 35.0% | 31.1% | 3.9 | 33.0% |

Across all eight runs adjusted recall spans **29.4% to 44.6%**, a range of 15.2 points. The largest spread *within a single arm, on identical input*, is **10.7 points**.

Now put the effects beside that:

| Hypothesis | Contrast | Mean effect | Direction across runs |
|------------|----------|------------:|-----------------------|
| H0 name list helps | A − B | **+8.4** | consistent (+4.5, +12.4) |
| H0 name list helps | C − D | +3.1 | **sign flips** (−2.2, +8.4) |
| H1 context helps | C − A | −3.1 | consistent (−1.1, −5.1) |
| H4 context substitutes | D − B | +2.2 | **sign flips** (+5.6, −1.1) |

**The largest effect (8.4) is smaller than the largest within-arm spread (10.7).** Two of the four contrasts change sign between runs. At n=2 per cell this design cannot separate any of them from noise.

## What can still be said

**H0 is suggestive, not established.** Removing the name catalogue lowered recall in both runs of the no-context pair, by 4.5 and 12.4 points. That is the most consistent signal in the data. But the same contrast flips sign once context is added, so even H0 is conditional on the other factor.

**H1 is not supported, and leans the wrong way.** Adding CSR context while the name catalogue is present lowered recall in both runs (−1.1, −5.1). Small, but the only other contrast whose direction held.

**H2 cannot be evaluated.** The per-class figures are dominated by noise. `NORM_CSR_WARL` across the eight runs reads 9, 7, 2, 9, 9, 8, 8, 7 with a denominator of 24. There is no gradient to test.

**H5 remains unrunnable here.** Agreement requires two models within an arm; this file covers one model.

## One structural observation

`NORM_CSR_RW` is **bimodal** across the eight runs, with a denominator of 51:

```
arm A: 6, 21     arm B: 7, 6
arm C: 5, 21     arm D: 7, 6
```

Six runs land at 5–7. Two land at 21. Nothing between. Whatever produces the jump is not a gradual response to a changed condition, since it appears in both a names-only arm and a names-plus-context arm. It looks like a threshold in the alias and fuzzy alignment passes rather than a change in what the model found, which is consistent with the amplification described below.

## Where the score actually comes from

`analyze.py` credits a gold parameter through one of seven passes: an exact name match, or one of five inexact ones (`one_to_many`, `explicit_group`, `concept_group`, `stem`, `fuzzy_name`), with `none` for unmatched. Only the totals reach the metrics file, so the composition of a score is invisible in normal use. Recovering it changes what these numbers mean.

Across the eight runs, decomposed by [`scripts/decompose_matches.py`](../scripts/decompose_matches.py):

| Arm | Run | Exact | Inexact | Reported | **Exact-name only** | Inexact share |
|-----|-----|------:|--------:|---------:|--------------------:|--------------:|
| A | 1 | 9 | 51 | 33.9% | 5.1% | 85.0% |
| B | 1 | 5 | 47 | 29.4% | 2.8% | 90.4% |
| A | 2 | 9 | 70 | 44.6% | 5.1% | 88.6% |
| B | 2 | 7 | 50 | 32.2% | 4.0% | 87.7% |
| C | 1 | 9 | 49 | 32.8% | 5.1% | 84.5% |
| D | 1 | 7 | 55 | 35.0% | 4.0% | 88.7% |
| C | 2 | 8 | 62 | 39.5% | 4.5% | 88.6% |
| D | 2 | 7 | 48 | 31.1% | 4.0% | 87.3% |

**Between 84.5% and 90.4% of every score above is awarded by inexact matching.** On exact names alone the model recovers 2.8% to 5.1% of the gold set, against a reported 29.4% to 44.6%.

**This is also where all the instability lives.** Exact matches range 5 to 9, a spread of 4. Inexact matches range 47 to 70, a spread of 23. The unstable component is the heuristic one, and it is carrying roughly seven eighths of the score.

Output volume does not explain it. Two runs produced **identical** deduplicated parameter counts of 214 and scored 35.0% and 39.5%. The run with the second-lowest output volume (202) scored the highest of all eight (44.6%).

### The same decomposition on the published baselines

| Run | Matched | Exact | Inexact | Reported | **Exact-name only** | Inexact share |
|-----|--------:|------:|--------:|---------:|--------------------:|--------------:|
| claude-sonnet-4 (Part I) | 129 | 86 | 43 | 72.9% | **48.6%** | 33.3% |
| gpt-4o-mini (published) | 57 | 11 | 46 | 32.2% | 6.2% | 80.7% |
| gpt-4o-mini v3 prompt | 62 | 10 | 52 | 35.0% | 5.6% | 83.9% |

`Exact` is `exact_matches_evaluated`, which `analyze.py:510` filters by `class_match is not None` and is therefore a lower bound rather than the exact-match count. All three rows have been cross-checked against their own alignment tallies and agree: 86, 11, 10. The mini and v3 alignment files were recovered on 2026-07-28 from an uncommitted `git stash` on the local UDB clone, having been described as lost for three days, and are committed under [`../../results/artifact_a/`](../../results/artifact_a/).

The two models differ in kind, not just in degree. Claude names the parameter two thirds of the time; gpt-4o-mini almost never does and is scored mostly on description similarity.

This changes how the headline comparison reads. On reported adjusted recall the gap is 72.9% against 32.2%, about 2.3x. On exact-name recall it is **48.6% against 6.2%, about 7.8x**. Both sides ran through the same Part I `extract.py`, so that is the like-for-like comparison.

The two complete arm A runs put the same gap at 9.6x from a different extraction harness, agreeing with each other exactly at 9 exact matches. Two independent paths, same direction, same order of magnitude, which is stronger than either figure alone. Treat the multiplier as an order of magnitude, not a precise ratio. The alignment layer compresses a large real difference into a modest-looking one, and it does so by being generous to the weaker model.

It also predicts the variance asymmetry, which is testable: a model scored mostly on exact names should be far more stable run to run than one scored mostly on fuzzy matching. The Part I Claude run has n=1, so this remains a prediction, not a result.

None of this makes inexact matching wrong. A model that answers "support for misaligned loads and stores" has found `MISALIGNED_LDST` and should be credited. The finding is that the credit is **mostly** heuristic, that the heuristic is **where the noise is**, and that neither fact is visible in the metric as published.

## The variance is not an artefact of the harness

Three checks:

1. Resolved prompts are **byte-identical** between runs, SHA-256 verified.
2. `analyze.py` is **deterministic**: re-scoring identical input reproduces 33.9%, 6/51, 9/24, 45/100 exactly.
3. The same scoring path reproduces the published Claude figures exactly: 72.9%, 88.4%, 12/24, 83/100, 32/51.

One caveat found while building the decomposition, recorded because it would otherwise trip the next person: `exact_matches_evaluated` in the metrics file counts exact matches *that also carried a comparable class* ([`analyze.py:510`](https://github.com/riscv/riscv-unified-db/blob/99f9dad81c7d58e7dcb43739c0828bc396ed2d86/param_extraction/scripts/analyze.py#L510)), so it is a lower bound rather than the exact-match count. It happens to equal the true count in all eleven runs checked here, but the figures above are taken from the alignment file's own tally, which is the right source. Symmetrically, the alignment file lists one entry per LLM parameter, so its sum can exceed the gold-side `matched_udb_count` when several outputs land on one gold parameter; it does on the Claude run, 133 against 129. The script reports gold-side counts and flags any disagreement.

## A finding that was withdrawn

After run 1, WARL looked like it collapsed when the catalogue was removed: 9/24 in arm A against 2/24 in arm B, while DIRECT stayed flat. That is precisely the mechanism argued in [#2053](https://github.com/riscv/riscv-unified-db/issues/2053), and it was one decision away from being published.

Run 2 reversed it. Arm A fell to 7/24 and arm B rose to 9/24, higher than arm A. The finding was withdrawn.

## What this means beyond this experiment

Any claim of the form *"intervention X improved recall from a to b"* on this corpus needs **N > 1 and a reported spread**, or it is unfalsifiable. That applies to the v3 prompt ablation (+2.8), to the Artifact A cross-model comparison, and to the Spring baseline this project cites. None of those numbers are wrong. None of them carry the precision a single decimal implies.

Exact match was stable across all eight runs while adjusted recall was not, which argues for reporting both and treating adjusted recall as a range.

Reported upstream as [#2163](https://github.com/riscv/riscv-unified-db/issues/2163), filed against [#1750](https://github.com/riscv/riscv-unified-db/issues/1750) whose stated deliverable is comparing two or more LLMs.

## Limitations

- **n=2 per arm.** Enough to show the design is underpowered, not enough to characterise the distribution. A spread from two samples is not a confidence interval.
- **The decomposition was not preregistered.** It came out of diagnosing the variance. It is a measurement of committed artifacts rather than a test of a hypothesis, and it is reported as exploratory. It is fully reproducible without an API key, since scoring is deterministic.
- **Cross-provider replication did not complete. Both providers impose a daily request quota, and one of them is measurable.**

  | Provider | Arm | Returned | Refused by provider | Local network |
  |---|---|---:|---|---:|
  | `gemini-3.6-flash` | A | 21/60 | 39 × `429 RESOURCE_EXHAUSTED` (daily quota) | 0 |
  | `gemini-3.6-flash` | B | 0/60 | 7 × `429 RESOURCE_EXHAUSTED` | **53** |
  | `nemotron-3-ultra-550b-a55b:free` | A | 50/60 | 9 × `429 Rate limit exceeded` (+1 timeout) | 0 |
  | `nemotron-3-ultra-550b-a55b:free` | B | 0/60 | 60 × `429 Rate limit exceeded` | 0 |

  The Gemini arm B failures are evidence about this machine's connectivity, not about Google's limits, and are not cited as a quota result.

  **The two quotas differ in whether they can be measured, and only one can.** Gemini's 429 body is truncated before the quota identifier, so the artifact records the refusal but never the allowance; the widely quoted 20 requests per day is vendor documentation rather than something observed here. OpenRouter states its limit in the response: every one of the 69 rate-limit errors carries `'X-RateLimit-Limit': '50'`, and the run returned **exactly 50** successful calls before the first refusal. Stated limit and observed ceiling agree exactly, which makes 50 requests per day a measurement rather than a citation.

  **The OpenRouter cap is account-wide, not per-model.** Attempting a different free model on the same account after the quota was spent returned the identical `free-models-per-day` refusal with `X-RateLimit-Remaining: 0`, so rotating models is not a workaround. The reset is a fixed daily boundary rather than a rolling window: `X-RateLimit-Reset` points at 00:00Z.

  A single arm needs 60 responses, so **50 per day cannot produce even one complete arm**, let alone the two same-model runs a variance estimate requires. No cross-provider variance estimate exists, and **H5 remains untested** because it requires two models within one arm. All partial runs are committed and excluded from every table by the 60-chunk gate, which prints what it dropped.

  The generalisable point is not that one vendor was stingy. It is that **the free tiers of two independent providers cap daily requests below the size of a single arm**, which is a concrete planning constraint for [#1750](https://github.com/riscv/riscv-unified-db/issues/1750), whose deliverable is comparing two or more LLMs. Paid inference is not a convenience here; it is the difference between the experiment being possible and not.
- The registered rule applies: these nulls mean **not detected under this design**, not evidence of absence.
- Context reaches only 32 of 60 chunks, so arms C and D are identical to A and B on the other 28. Registered in advance in section 4b.

## Reproduction

```bash
./verify.sh                                   # every number here re-derives
python scripts/score_arms.py --validate       # harness against published figures
python scripts/compare_runs.py --a runs/<r1> --b runs/<r2> --arm A
```

Every raw response, parsed candidate list, resolved prompt and per-call record for all eight runs is committed under `runs/`.
