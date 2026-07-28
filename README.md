# AI-assisted extraction of architectural parameters from RISC-V specifications

[![ci](https://github.com/titoatwork/lfx-firstanalysis/actions/workflows/ci.yml/badge.svg)](https://github.com/titoatwork/lfx-firstanalysis/actions/workflows/ci.yml)

Prework for [LFX Fall 2026 Part II](https://mentorship.lfx.linuxfoundation.org/project/22296947-cecb-4a8f-8bcb-4f34710e9f66) · Parameter SIG / [riscv/riscv-unified-db](https://github.com/riscv/riscv-unified-db)

Ibteshamul Haque, [@titoatwork](https://github.com/titoatwork)

**Corpus:** 60 param-bearing chunks of the ISA Manual, ~52,000 lines.
**Gold:** 185-parameter pinned freeze and a 223-parameter live regeneration.
**Runs:** 4 preregistered arms, every arm run twice, multiple models.

---

## Check it without trusting me

```bash
./verify.sh
```

No credentials, no network, no model calls, seconds. It re-derives **every published number in this repository from committed artifacts** and exits non-zero if any figure disagrees with the file it came from. It also runs the fail-closed challenge gate and the evaluation fixtures.

Four claims are reported as **not checkable** rather than passing quietly. `./verify.sh --list` shows the whole claim table and which artifact each number comes from.

---

## Three findings, each of which cost me something

### 1. Recall is not stable across identical runs

Same model, byte-identical prompt, `temperature=0`, run twice thirty minutes apart:

| | run 1 | run 2 |
|---|---:|---:|
| adjusted recall | **33.9%** | **44.6%** |
| `NORM_CSR_RW` | 6/51 | 21/51 |

Prompts match by SHA-256, the scorer is deterministic, and the harness reproduces the published figures exactly, so the variation is in the model and the alignment step amplifies it: run 2 produced *fewer* raw parameters and matched *more* gold.

**Consequence:** every single-run recall figure in this problem space is one sample from a distribution nobody has measured, including mine and including the Spring baseline this project cites. Reported upstream as [#2163](https://github.com/riscv/riscv-unified-db/issues/2163).

**I nearly published the opposite.** After one run, WARL looked like it collapsed without the name catalogue, which is exactly the mechanism I had been arguing publicly. The second run reversed it. The finding was withdrawn, not shipped.

→ [`artifact_c/results/PRIMARY_RESULTS.md`](./riscv-param-extraction/artifact_c/results/PRIMARY_RESULTS.md) · [preregistration](./riscv-param-extraction/artifact_c/PREREGISTRATION.md), committed before any model call

### 2. Published recall measures grounding, not discovery

The Part I prompts inject **all 185 gold parameter names**, a set identical to the ground truth, instructing the model to reuse them exactly:

```
injected list size : 185
gold set size      : 185
identical sets     : True
```

So `72.9%` means *given the catalogue, locate which entries apply and evidence them*. That is the correct design for producing a spreadsheet and tagging spec text. It is not what the number is usually read to mean, and I was citing it that way myself until I read the prompt assembly.

Corrected here, in the claim ledger, and [publicly upstream](https://github.com/riscv/riscv-unified-db/issues/2053) where I had quoted it uncorrected.

### 3. Most of the score is awarded by fuzzy matching, and that is where the noise lives

The scorer credits a gold parameter either by exact name or through one of five inexact passes. Only the totals reach the metrics files, so the split is invisible. Pulling it out of the alignment data:

| | Exact | Inexact | Reported | Exact-name only | Inexact share |
|---|---:|---:|---:|---:|---:|
| gpt-4o-mini, 8 runs | 5–9 | 47–70 | 29.4–44.6% | 2.8–5.1% | **84.5–90.4%** |
| claude-sonnet-4, Part I | 86 | 43 | 72.9% | **48.6%** | 33.3% |

Across the eight runs, exact matches span a range of 4 and inexact matches span 23. The component carrying seven eighths of the score is the component that moves, which is the mechanism behind finding 1.

It also means the two models differ in kind rather than degree. On adjusted recall the published gap reads 72.9% against 32.2%, about 2.3x. On exact-name recall it reads 48.6% against 6.2%, about **7.8x**. The alignment layer compresses a large real difference into a modest-looking one.

Two independent runs on a different harness put the same gap at 9.6x, so the direction is not sensitive to which artifact you use. Read the multiplier as an order of magnitude rather than a precise ratio, since the two sides come from different extraction paths.

Inexact matching is not wrong; a model answering "support for misaligned loads and stores" has found `MISALIGNED_LDST`. The problem is that the credit is mostly heuristic and nothing in the reported number says so. **This one cost me the cleanest comparison I had**, since the headline figure I had been citing turns out to understate the result it was being used to support.

Reproduce with `python artifact_c/scripts/decompose_matches.py`, deterministic and no API key. Not preregistered: it came out of diagnosing finding 1 and is labelled exploratory throughout.

---

## Five-minute path

| # | Open | What it shows |
|---|------|---------------|
| 1 | [`verify.sh`](./verify.sh) | every published number re-derives from a committed artifact |
| 2 | [Artifact C results](./riscv-param-extraction/artifact_c/results/PRIMARY_RESULTS.md) | the variance finding, the match decomposition, and the withdrawn one |
| 3 | [`docs/metrics.md`](./riscv-param-extraction/docs/metrics.md) | all measured tables, each with its condition stated |
| 4 | [Upstream work](#upstream-riscvriscv-unified-db) | 4 PRs with one merged, 6 issues, reviews on four other contributors' PRs |
| 5 | [Challenge pack](./riscv-param-extraction/challenge/) | 4 fail-closed fixtures, 4 hard negatives, 10-model live matrix with its failures reported |
| 6 | [Claim ledger](./application-packet/MEASURED-CLAIM-LEDGER.md) | every claim mapped to a source, plus the claims that are forbidden and why |

---

## Upstream (riscv/riscv-unified-db)

| Item | State |
|------|-------|
| [#2145](https://github.com/riscv/riscv-unified-db/issues/2145) → [PR #2146](https://github.com/riscv/riscv-unified-db/pull/2146) | **Merged** 2026-07-28 as `278d1edc`. `UXLEN`'s description named `SXLEN` as what `mstatus.UXL` changes. Found while triaging a sweep whose other flag was verified **correct** and deliberately not filed |
| [#2137](https://github.com/riscv/riscv-unified-db/issues/2137) → [PR #2138](https://github.com/riscv/riscv-unified-db/pull/2138) | Open, 70 checks green, awaiting re-review. `4095` is not a power of two but sits in both `unsigned_pow2` schema enums. Two rounds of review changes applied: a schema `$id` bump, and reverting a generated v0.1 doc page |
| [#2188](https://github.com/riscv/riscv-unified-db/issues/2188) → [PR #2189](https://github.com/riscv/riscv-unified-db/pull/2189) | Open, 70 checks green, awaiting re-review. `CACHE_BLOCK_SIZE` admitted any integer to 2^64-1 although the CMO spec defines a cache block as a naturally aligned power of two |
| [PR #2164](https://github.com/riscv/riscv-unified-db/pull/2164) | Parameter-extraction evaluation fixtures, invited by the author of #2097. Awaiting a reviewer |
| [PR #2090](https://github.com/riscv/riscv-unified-db/pull/2090) | **Merged.** A [review comment](https://github.com/riscv/riscv-unified-db/pull/2090#issuecomment-5084258197) here identified the MTVEC alignment defect and the maintainer adopted it. **That PR is the maintainer's; the contribution is the review** |
| [PR #2097](https://github.com/riscv/riscv-unified-db/pull/2097) | Five-point review, all five adopted. The author then revised one of them, and rightly: my rule filtered at extraction where the design filters at human review. A [follow-up](https://github.com/riscv/riscv-unified-db/pull/2097#issuecomment-5109644710) measured the recall gap that revision closes, 63 conditional-writability sentences in the manual carrying no `WARL` token against 5 that do, and the class boundary it leaves open |
| [PR #2155](https://github.com/riscv/riscv-unified-db/pull/2155) · [PR #2109](https://github.com/riscv/riscv-unified-db/pull/2109) | Reviews of other contributors' work. The first found the same four edits duplicated in a second open PR; the second verified two removed branches were provably unreachable and flagged the same gaps surviving in a sibling field |
| [#2199](https://github.com/riscv/riscv-unified-db/issues/2199) | The `unsigned_pow2` schema defs cannot be referenced by any parameter: the Z3 constraint path resolves them, the IDL type resolver does not. Found by hitting it in #2189 |
| [#2163](https://github.com/riscv/riscv-unified-db/issues/2163) · [#2158](https://github.com/riscv/riscv-unified-db/issues/2158) · [#1748](https://github.com/riscv/riscv-unified-db/issues/1748) · [#2053](https://github.com/riscv/riscv-unified-db/issues/2053) | Run-to-run variance · fixture placement · a parameter-taxonomy answer · scope discussion |

**One PR merged, three open with checks green, two awaiting re-review.** The first merge also cleared the first-time-contributor workflow gate, so later commits run CI without a maintainer approving each one.

---

## Measured numbers

Every figure below is a **single run**, and single runs on this task are unstable by ~10 points. All are **grounding** scores with the gold name catalogue supplied.

| Item | Value |
|------|------:|
| Part I v2 remeasure (GT 185) | adj **72.9%** · class **88.4%** · WARL **12/24** |
| Same output vs live GT 223 | adj **64.2%** |
| Artifact A, gpt-4o-mini | adj **32.2%** · name Jaccard vs Claude **3.8%** |
| v3 WARL prompt ablation | adj **35.0%** · WARL **2/24**, a null |
| Artifact B export | **83/83** named · **20/20** new, schema-valid |
| Artifact C, arm A | **33.9%** then **44.6%** on identical input |

Authoritative: [`docs/metrics.md`](./riscv-param-extraction/docs/metrics.md). Verify: `./verify.sh`.

---

## Credit

Spring Part I (extract → analyze → spreadsheet) is the work of [@ishaan-arora-1](https://github.com/ishaan-arora-1) on UDB PRs **#1765–#1832**. This repository **reproduces, remeasures and extends** it and claims no authorship of it. The mentee has since noted those PRs are a first version and the working pipeline is internal, so the remeasure here is a public snapshot rather than current state.

---

## Limitations

- Every recall figure is a single run; run-to-run variance on this task is ~10 points.
- All published recall is **grounding** with the name catalogue supplied. Discovery recall is the subject of Artifact C and is not yet complete.
- The nine dual-model "new" candidates are **not** a validated review queue: `IALIGN` and `FLEN` are derived quantities the gate passed at high confidence.
- Artifact A's per-chunk outputs were missing from this repo for three days and were briefly described here as lost. They were not lost. They were sitting uncommitted in a `git stash` on the local UDB clone, and I did not think to look there before writing that they were gone. All 60 chunks, both alignment files and the deduped lists are now committed under [`results/artifact_a/`](./riscv-param-extraction/results/artifact_a/), and every figure they back re-derives: alignment exact is 11 against the published 11, v3 is 10 against 10, and `pipeline/agreement.py` reproduces the exclusive-set counts exactly. Retention is a hard gate on all later runs, enforced by `verify.sh` rather than remembered.
- Artifact A's second model is `gpt-4o-mini`, which underperforms Claude on this corpus.
- The holdout is an **exploratory null** under documented v1.2 prompt limitations, not clean temporal evidence.
- Challenge results on 2 snippets are not comparable to corpus recall.

---

## Layout

```
riscv-param-extraction/
  artifact_c/        preregistered 4-arm experiment, runs, results
  challenge/         coding challenge, CI gate, live matrix, holdout
  docs/metrics.md    measured tables
  scripts/           verify_claims.py
  export/ drafts/    Artifact B
  workflow_slice/    evaluation fixtures, review-envelope slice
application-packet/  essay, nine-week plan, claim ledger
verify.sh            re-derives every published number
```

## License

See [`riscv-param-extraction/LICENSE`](./riscv-param-extraction/LICENSE). Vendored UDB schemas retain upstream BSD-3-Clause-Clear notices.
