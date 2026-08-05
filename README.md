# Architectural parameter extraction for RISC-V

[![ci](https://github.com/titoatwork/lfx-firstanalysis/actions/workflows/ci.yml/badge.svg)](https://github.com/titoatwork/lfx-firstanalysis/actions/workflows/ci.yml)

Measurement, export tooling, evaluation fixtures, and merged upstream fixes for extracting **architectural parameters** from RISC-V ISA material into [riscv/riscv-unified-db](https://github.com/riscv/riscv-unified-db).

**Author:** Ibteshamul Haque ([@titoatwork](https://github.com/titoatwork))
**Context:** [LFX Fall 2026 Part II](https://mentorship.lfx.linuxfoundation.org/project/22296947-cecb-4a8f-8bcb-4f34710e9f66), Parameter SIG
**Spring Part I credit:** [@ishaan-arora-1](https://github.com/ishaan-arora-1) / UDB PRs #1765-#1832. This repository reproduces and extends that public surface and claims no Spring authorship.

---

## Reviewer summary

| Question | Answer |
|---|---|
| **What was investigated** | Whether the published Part I extraction figures measure what they are read as measuring, and whether the UDB parameter data they are scored against is itself self-consistent |
| **What was contributed** | **8 merged** upstream PRs, **6** open, **14** issues filed, review comments adopted into other contributors' merged code. Zero PRs rejected |
| **What was learned** | The headline recall number measures **grounding, not discovery**; most of it is awarded by fuzzy matching; and it moves ~10 points between byte-identical runs |
| **How to check it** | `./verify.sh` re-derives each registered figure from the artifact it came from, and reports anything it cannot check rather than passing it. **109/109** checkable claims pass, offline, no API key |
| **What comes next** | [`docs/TERM-PLAN.md`](./docs/TERM-PLAN.md), nine weeks mapped to the five official Part II objectives |

---

## Verify in one command

```bash
git clone https://github.com/titoatwork/lfx-firstanalysis
cd lfx-firstanalysis
pip install -r riscv-param-extraction/requirements.txt   # PyYAML, jsonschema
./verify.sh
```

Two dependencies, both pure data handling. No credentials, no network model calls, no API key, no model SDK. Every failure prints which artifact disagreed with which published number. `./verify.sh --list` prints the claim table without running the checks.

CI runs this exact path on every push, so the badge above tracks the same command a reviewer would type.

Windows, from the repository root:

```powershell
$env:PYTHONPATH = "riscv-param-extraction"
python riscv-param-extraction/scripts/verify_claims.py
```

---

## Proof table

Every row is checkable without trusting this page.

| Claim | Artifact | Proof |
|---|---|---|
| Published recall is **grounding**, not discovery | [`metrics.md`](./riscv-param-extraction/docs/metrics.md) grounding note | Prompt injects all **185** gold names, set-identical to the pinned ground truth. Corrected in public on [#2053](https://github.com/riscv/riscv-unified-db/issues/2053) |
| Single-run recall is unstable | [`PRIMARY_RESULTS.md`](./riscv-param-extraction/artifact_c/results/PRIMARY_RESULTS.md) | **33.9%** then **44.6%**, same model, byte-identical prompt, `temperature=0`. Filed as [#2163](https://github.com/riscv/riscv-unified-db/issues/2163) |
| The cross-model gap is wider than headline recall shows | [`metrics.md` §5](./riscv-param-extraction/docs/metrics.md) | Adjusted recall 72.9% vs 32.2% (2.3x); **exact-name 48.6% vs 6.2%** (7.8x) |
| Gold WARL labels are largely undecidable from syntax | [`GOLD-CLASSIFICATION-AUDIT.md`](./riscv-param-extraction/analysis/GOLD-CLASSIFICATION-AUDIT.md) | Of **26** gold WARL labels: **4** decidable, **4** stale, **18** undecidable. Posted on [#2200](https://github.com/riscv/riscv-unified-db/issues/2200) |
| Two independent audits converge on the same four names | [`PARAM-SCHEMA-SHAPES.md`](./riscv-param-extraction/analysis/PARAM-SCHEMA-SHAPES.md) | Schema-shape scan and IDL scan both dissent on `SXLEN`, `UXLEN`, `VSXLEN`, `VUXLEN`. The equality is gated as an invariant in `verify_claims.py` |
| Export produces schema-valid UDB YAML | [`export/`](./riscv-param-extraction/export/) | **83/83** named, **20/20** new drafts. Structural validity only, not architectural approval |
| Findings became merged upstream fixes | [`docs/EVIDENCE.md`](./docs/EVIDENCE.md) | 8 merged PRs; 7 closed an issue filed from this measurement work, the eighth took up a maintainer's open request |
| The extraction task itself found a real defect | [`coding-challenge/`](./coding-challenge/) | The Part II challenge snippet describes a cache block as a power of two. UDB's own parameter did not enforce it, until [#2189](https://github.com/riscv/riscv-unified-db/pull/2189) |

---

## The correction that matters most

Part I prompts build every request through `build_user_message()`, which unconditionally injects the complete list of **185** gold parameter names, with the instruction *"When a parameter you find matches one of these known names, use the exact name."* That list is set-identical to the pinned ground truth.

So the published 72.9% and 32.2% figures measure **grounding**: given the catalogue, locate which entries apply to a passage and cite evidence. They do not measure whether a model can find architectural parameters without being handed the answer key. That second number is not measured in this repository, or anywhere public that I could find.

The figures are correctly measured and unchanged. What changed is the claim attached to them. I found this while building the variance experiment, corrected it in public on [#2053](https://github.com/riscv/riscv-unified-db/issues/2053), and every recall figure in this repository now carries the condition.

The same discipline retired a second claim of my own: a run-1 result suggesting WARL collapsed when the catalogue was removed reversed direction in run 2, so what stands is the narrower statement that the contrast sits inside run-to-run noise at N = 1.

---

## Upstream contribution record

Census **2026-08-05**, re-derived from the GitHub API. Full index with links: [`docs/EVIDENCE.md`](./docs/EVIDENCE.md).

A dated snapshot rather than a live count. [#2384](https://github.com/riscv/riscv-unified-db/pull/2384) is listed below as open and merged later the same day; the figures are left as the API returned them, since patching a census by hand between refreshes is how the last one went wrong. Next refresh 2026-08-08.

| Kind | Count |
|---|---:|
| Merged PRs authored | **8** |
| Open PRs authored | **6** |
| Issues authored | **14** |
| Unique issues and PRs involving this author | **45** |
| PRs rejected | **0** |

**Merged:** [#2138](https://github.com/riscv/riscv-unified-db/pull/2138) · [#2146](https://github.com/riscv/riscv-unified-db/pull/2146) · [#2189](https://github.com/riscv/riscv-unified-db/pull/2189) · [#2215](https://github.com/riscv/riscv-unified-db/pull/2215) · [#2227](https://github.com/riscv/riscv-unified-db/pull/2227) · [#2256](https://github.com/riscv/riscv-unified-db/pull/2256) · [#2266](https://github.com/riscv/riscv-unified-db/pull/2266) · [#2362](https://github.com/riscv/riscv-unified-db/pull/2362)

**Open:** [#2289](https://github.com/riscv/riscv-unified-db/pull/2289) (draft, under review) · [#2255](https://github.com/riscv/riscv-unified-db/pull/2255) · [#2212](https://github.com/riscv/riscv-unified-db/pull/2212) · [#2164](https://github.com/riscv/riscv-unified-db/pull/2164) · [#2384](https://github.com/riscv/riscv-unified-db/pull/2384) · [#2395](https://github.com/riscv/riscv-unified-db/pull/2395)

**Review comments carried into other people's merged PRs:** [#2090](https://github.com/riscv/riscv-unified-db/pull/2090) (alignment defect adopted by the maintainer) · [#2109](https://github.com/riscv/riscv-unified-db/pull/2109) · [#2197](https://github.com/riscv/riscv-unified-db/pull/2197) (own earlier advice corrected after the author had built on it; the merged code follows the correction) · [#2245](https://github.com/riscv/riscv-unified-db/pull/2245) · [#2284](https://github.com/riscv/riscv-unified-db/pull/2284)

**Measurement threads:** [#2053](https://github.com/riscv/riscv-unified-db/issues/2053) · [#2163](https://github.com/riscv/riscv-unified-db/issues/2163) · [#2200](https://github.com/riscv/riscv-unified-db/issues/2200) · [#2251](https://github.com/riscv/riscv-unified-db/issues/2251). These carry numbers, not only opinions; indexed in [`metrics.md` §8](./riscv-param-extraction/docs/metrics.md).

---

## Repository layout

```text
riscv-param-extraction/
  docs/metrics.md      authoritative measured tables (§8 indexes upstream threads)
  artifact_c/          preregistered dual-run variance experiment and results
  analysis/            gold classification and schema-shape audits
  export/              spreadsheet rows to draft UDB param YAML
  manifests/           reproducible run records
  workflow_slice/      evaluation fixtures and the review/export path
  scripts/             claim verifier and audit scripts
docs/
  EVIDENCE.md          measurement limits and the upstream contribution index
  FAQ.md               how to read the numbers
  TERM-PLAN.md         nine-week plan mapped to the official objectives
coding-challenge/      Part II challenge submission: prompts, ten-model matrix, results
upstream-pr-drafts/    local drafts for filed and not-filed defects (historical archive)
verify.sh              offline verification entrypoint
```

---

## Limitations, stated deliberately

- Single-run recall is noisy. Treat any single figure as one sample, not a point estimate.
- Published recall is grounding, measured with the gold name list supplied in the prompt.
- Schema-valid export is **structural** validity. It is not a claim that a parameter is architecturally correct.
- Most of the adjusted score is awarded by inexact alignment passes, and that is where the run-to-run variance concentrates.
- Recall is a regression signal, not a coverage measure. A parameter that should exist but is absent from the gold cannot score as a miss.
- No Ruby toolchain on the development machine, so CI is the only validator for `.rb` changes and for whether `idlc` accepts new IDL. Nothing in this repository needs Ruby; the limitation applies to the UnifiedDB changes filed from it.

Fuller treatment: [`docs/EVIDENCE.md`](./docs/EVIDENCE.md) and [`docs/FAQ.md`](./docs/FAQ.md).

---

## Proposed term continuation

[`docs/TERM-PLAN.md`](./docs/TERM-PLAN.md) maps nine weeks to the five official Part II objectives, with a Week 0 decision on which figure the term optimizes. A target hit by quietly changing the scoring condition is not a result.

---

## AI assistance

This repository was developed with an AI coding assistant. Prefer the technical artifacts and `./verify.sh` over commit trailers when judging the work. Judgement calls, what to file, what to correct, and what not to file, are the author's.

---

## License

See [LICENSE](./LICENSE) and package-level licenses under `riscv-param-extraction/`.
