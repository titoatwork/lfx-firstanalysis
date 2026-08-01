# Upstream contribution drafts

Defect candidates against [riscv/riscv-unified-db](https://github.com/riscv/riscv-unified-db): what was filed, what was not, and why.

Live issue/PR state is on GitHub. Full census: [`docs/EVIDENCE.md`](../docs/EVIDENCE.md).

**Author:** [@titoatwork](https://github.com/titoatwork)

---

## Filed

| Directory | Defect | Issue | PR | Outcome |
|-----------|--------|-------|-----|---------|
| [`fix-counteren-en-constraints/`](./fix-counteren-en-constraints/) | Counter-enable params missing `requirements` already stated in descriptions | [#2265](https://github.com/riscv/riscv-unified-db/issues/2265) | [#2266](https://github.com/riscv/riscv-unified-db/pull/2266) | **Merged** |
| [`fix-vs-vu-xlen-32/`](./fix-vs-vu-xlen-32/) | `VSXLEN` / `VUXLEN` must support 32 when parent mode can | [#2254](https://github.com/riscv/riscv-unified-db/issues/2254) | [#2255](https://github.com/riscv/riscv-unified-db/pull/2255) | **Open** |
| [`issue-2285-enum-validation/`](./issue-2285-enum-validation/) | Smoke check: string-enum params vs IDL string literals | [#2285](https://github.com/riscv/riscv-unified-db/issues/2285) | [#2289](https://github.com/riscv/riscv-unified-db/pull/2289) | **Open** |

Also authored (bodies not under `fix-*` here; see EVIDENCE):

| | |
|--|--|
| Merged | [#2138](https://github.com/riscv/riscv-unified-db/pull/2138), [#2146](https://github.com/riscv/riscv-unified-db/pull/2146), [#2189](https://github.com/riscv/riscv-unified-db/pull/2189), [#2215](https://github.com/riscv/riscv-unified-db/pull/2215), [#2227](https://github.com/riscv/riscv-unified-db/pull/2227), [#2256](https://github.com/riscv/riscv-unified-db/pull/2256) |
| Open | [#2212](https://github.com/riscv/riscv-unified-db/pull/2212), [#2164](https://github.com/riscv/riscv-unified-db/pull/2164) |

---

## Checked and not filed

| Directory | Outcome |
|-----------|---------|
| [`fix-mtvec-base-alignment-4096/`](./fix-mtvec-base-alignment-4096/) | Fixed via review on [#2090](https://github.com/riscv/riscv-unified-db/pull/2090) (maintainer PR). See [`OPEN-DECISION.md`](./fix-mtvec-base-alignment-4096/OPEN-DECISION.md). |
| [`fix-stval-width-bounds/`](./fix-stval-width-bounds/) | Owned by [#2103](https://github.com/riscv/riscv-unified-db/pull/2103) / [#2102](https://github.com/riscv/riscv-unified-db/issues/2102). |
| [`fix-hpm-events-dup-index/`](./fix-hpm-events-dup-index/) | Owned by [#2047](https://github.com/riscv/riscv-unified-db/pull/2047) / [#1991](https://github.com/riscv/riscv-unified-db/pull/1991) for [#2046](https://github.com/riscv/riscv-unified-db/issues/2046). |
| [`fix-hpm-mcountinhibit-typo/`](./fix-hpm-mcountinhibit-typo/) | Same file / class as the HPM_EVENTS candidate above. |

---

## Related

Invariant sweep over param YAML + schemas:

```bash
cd riscv-param-extraction
python workflow_slice/scripts/sweep_invariants.py --git-ref origin/main
```

`MXLEN` scalar vs `SXLEN`/`UXLEN`/`VSXLEN` array siblings is intentional, not a defect ([#2145](https://github.com/riscv/riscv-unified-db/issues/2145)).
