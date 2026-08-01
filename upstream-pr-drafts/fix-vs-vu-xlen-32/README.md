# VSXLEN / VUXLEN parent-child 32 support

| | |
|--|--|
| **Outcome** | **Open** |
| Issue | [#2254](https://github.com/riscv/riscv-unified-db/issues/2254) |
| PR | [#2255](https://github.com/riscv/riscv-unified-db/pull/2255) |

`VSXLEN` and `VUXLEN` previously constrained only the upper bound, so a child mode could be configured wider than a parent that can still select RV32. Mirrors the existing `UXLEN` vs `SXLEN` pattern.

See [`PR_BODY.md`](./PR_BODY.md).
