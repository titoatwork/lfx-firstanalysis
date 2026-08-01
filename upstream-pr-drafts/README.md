# Upstream contribution drafts

Working archive of defect candidates against [riscv/riscv-unified-db](https://github.com/riscv/riscv-unified-db).

**Live state is always on GitHub.** This directory records what was checked, what was filed, and what was deliberately not filed, so the process is auditable.

| Resource | Link |
|----------|------|
| Full contribution census | [`docs/EVIDENCE.md`](../docs/EVIDENCE.md) |
| Upstream repo | https://github.com/riscv/riscv-unified-db |
| Author | [@titoatwork](https://github.com/titoatwork) |

**Filing rule:** reproduce on current `origin/main`, confirm no open PR or issue claim owns it, keep the fix small enough to review.

---

## Layout

| Path | Meaning |
|------|---------|
| `fix-*/` | Candidate defect + `PR_BODY.md` (and draft YAML when useful) |
| `fix-*/OPEN-DECISION.md` | Explicit decision **not** to open a competing PR |
| Local-only (gitignored) | `COMMENT.md`, `ISSUE.md`, `REPLY.md` under other subdirs — working text, not the public surface |

---

## Filed from this tree

| Directory | Defect (short) | Issue | PR | Outcome |
|-----------|----------------|-------|-----|---------|
| [`fix-counteren-en-constraints/`](./fix-counteren-en-constraints/) | Counter-enable params missing `requirements` already stated in descriptions | [#2265](https://github.com/riscv/riscv-unified-db/issues/2265) | [#2266](https://github.com/riscv/riscv-unified-db/pull/2266) | **Merged** |
| [`fix-vs-vu-xlen-32/`](./fix-vs-vu-xlen-32/) | `VSXLEN` / `VUXLEN` must support 32 when parent mode can | [#2254](https://github.com/riscv/riscv-unified-db/issues/2254) | [#2255](https://github.com/riscv/riscv-unified-db/pull/2255) | **Open** |
| [`issue-2285-enum-validation/`](./issue-2285-enum-validation/) | Smoke check: string-enum params vs IDL string literals | [#2285](https://github.com/riscv/riscv-unified-db/issues/2285) | [#2289](https://github.com/riscv/riscv-unified-db/pull/2289) | **Open** |

The schema `4095` → `4096` fix for shared `unsigned_pow2` enums was authored as [#2138](https://github.com/riscv/riscv-unified-db/pull/2138) (closes [#2137](https://github.com/riscv/riscv-unified-db/issues/2137), **merged**). Draft material for that PR was prepared outside this tree; see EVIDENCE.

Other authored merges not drafted under `fix-*` here (bodies prepared alongside work):  
[#2146](https://github.com/riscv/riscv-unified-db/pull/2146), [#2189](https://github.com/riscv/riscv-unified-db/pull/2189), [#2215](https://github.com/riscv/riscv-unified-db/pull/2215), [#2227](https://github.com/riscv/riscv-unified-db/pull/2227), [#2256](https://github.com/riscv/riscv-unified-db/pull/2256).  
Open tooling PRs: [#2212](https://github.com/riscv/riscv-unified-db/pull/2212), [#2164](https://github.com/riscv/riscv-unified-db/pull/2164). Full list: EVIDENCE.

---

## Not filed (and why)

| Directory | Outcome |
|-----------|---------|
| [`fix-mtvec-base-alignment-4096/`](./fix-mtvec-base-alignment-4096/) | **Resolved by review.** Comment on [#2090](https://github.com/riscv/riscv-unified-db/pull/2090) flagged `0xfff` in MTVEC alignment enums; maintainer fixed it in that PR. See [`OPEN-DECISION.md`](./fix-mtvec-base-alignment-4096/OPEN-DECISION.md). |
| [`fix-stval-width-bounds/`](./fix-stval-width-bounds/) | Already owned by [#2103](https://github.com/riscv/riscv-unified-db/pull/2103) / [#2102](https://github.com/riscv/riscv-unified-db/issues/2102). Draft body kept for audit. |
| [`fix-hpm-events-dup-index/`](./fix-hpm-events-dup-index/) | Already owned by [#2047](https://github.com/riscv/riscv-unified-db/pull/2047) / [#1991](https://github.com/riscv/riscv-unified-db/pull/1991) for [#2046](https://github.com/riscv/riscv-unified-db/issues/2046). |
| [`fix-hpm-mcountinhibit-typo/`](./fix-hpm-mcountinhibit-typo/) | Subsumed by the HPM_EVENTS candidate (same file / same quality class). |

These folders are **not** pending work. They document triage discipline: do not race, do not re-file.

---

## What is not in the public tree

Subdirectories named `issue-*`, `review-*`, `pr-*`, and `slack-*` may exist **locally** with comment drafts. Those paths use gitignored filenames (`COMMENT.md`, `ISSUE.md`, `REPLY.md`) so they do not ship as the public portfolio surface. Posted comments on GitHub are the source of truth.

---

## Related tooling

Machine sweep over param YAML + schemas:

```bash
cd riscv-param-extraction
python workflow_slice/scripts/sweep_invariants.py --git-ref origin/main
```

One finding it flags (`MXLEN` scalar vs `SXLEN`/`UXLEN`/`VSXLEN` array siblings) was reviewed and is **not** a defect; reasoning is in [#2145](https://github.com/riscv/riscv-unified-db/issues/2145).
