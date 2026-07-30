# Upstream defect candidates: what was checked, and what happened

Every candidate defect found during prework is recorded here with its outcome, including the ones that never became a PR. Four of the six did not, because someone else already owned the fix or a maintainer landed it first. That check is the point of this directory.

**Rule:** a candidate is only filed after it reproduces on current `origin/main`, no open PR touches it, no issue comment claims it, and the fix is small enough to review.

## Filed

| Candidate | Issue | PR | State |
|-----------|-------|----|-------|
| `4095` in both `unsigned_pow2` schema enums, with a regression test in the Ruby runner | [#2137](https://github.com/riscv/riscv-unified-db/issues/2137) | [#2138](https://github.com/riscv/riscv-unified-db/pull/2138) | **Merged** `aee74ee8` |
| `UXLEN` description named `SXLEN` as what `mstatus.UXL` changes; `SXLEN` option list used scalars against its own array schema | [#2145](https://github.com/riscv/riscv-unified-db/issues/2145) | [#2146](https://github.com/riscv/riscv-unified-db/pull/2146) | **Merged** `278d1edc` |

## Not filed, and why

| Candidate | Outcome |
|-----------|---------|
| `fix-mtvec-base-alignment-4096/` | **Resolved by review instead.** A comment on [#2090](https://github.com/riscv/riscv-unified-db/pull/2090) flagged `0xfff` in both MTVEC alignment enums against a schema requiring a power of two. The maintainer agreed and corrected it, and #2090 merged carrying the fix. Opening a competing PR against files under active maintainer edit would have been a race for credit on a one-token change. See [`OPEN-DECISION.md`](./fix-mtvec-base-alignment-4096/OPEN-DECISION.md). |
| `fix-stval-width-bounds/` | Already owned. [#2103](https://github.com/riscv/riscv-unified-db/pull/2103) covers [#2102](https://github.com/riscv/riscv-unified-db/issues/2102). |
| `fix-hpm-events-dup-index/` | Already owned. [#2047](https://github.com/riscv/riscv-unified-db/pull/2047) and [#1991](https://github.com/riscv/riscv-unified-db/pull/1991) both address the duplicate `HPM_COUNTER_EN` index in [#2046](https://github.com/riscv/riscv-unified-db/issues/2046), and the issue was claimed in-thread. |
| `fix-hpm-mcountinhibit-typo/` | Subsumed by the HPM_EVENTS candidate above, which covers the same file. Filing it separately would have been noise. |

The draft YAML and PR bodies are kept as-is so the reasoning stays auditable. They are **not** pending work.

This directory covers only the candidates drafted here before filing. The complete
upstream record, four merged PRs, three open, nine issues and the reviews carried
into other people's merged work, is in the [root README](../README.md#upstream-riscvriscv-unified-db).

## Related

A machine sweep over all 227 files in `spec/std/isa/param` plus the JSON schemas runs from [`workflow_slice/scripts/sweep_invariants.py`](../riscv-param-extraction/workflow_slice/scripts/sweep_invariants.py). It reports known and already-reviewed findings without presenting them as new work. One finding it flags, the `MXLEN` scalar against its `SXLEN`/`UXLEN`/`VSXLEN` array siblings, was reviewed and is **not** a defect; the reasoning is recorded in [#2145](https://github.com/riscv/riscv-unified-db/issues/2145) and encoded in the checker.
