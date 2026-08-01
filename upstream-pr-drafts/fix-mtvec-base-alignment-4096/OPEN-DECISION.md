# Decision: do not open a competing PR

**Opened:** 2026-07-27 · **Closed:** 2026-07-27  
**Outcome:** fix landed in the maintainer's PR. Local branch retired unopened.

## What happened

| Item | Status |
|------|--------|
| Maintainer PR [#2090](https://github.com/riscv/riscv-unified-db/pull/2090) | **Merged** 2026-07-27 |
| Review comment on #2090 (26 Jul) | Flagged `0xfff` (4095) in both MTVEC alignment enums against a schema requiring a power of two |
| Maintainer reply | Agreement that the value should be 4096; PR updated accordingly |
| `0xfff` on upstream `main` after merge | **Gone** |
| Local branch `fix/mtvec-base-alignment-4096` | **Retired unopened** |

## Why

Opening a second PR against files already under active maintainer edit would race for credit on a one-token change. A review comment produced the same correction inside the maintainer's PR.

## How to describe it

> Review comment on #2090 identified a non-power-of-two value in both MTVEC alignment enums; the maintainer adopted the correction and #2090 merged with `0x1000`.

Do **not** describe #2090 as an authored merge by titoatwork. It is jordancarlin's PR.

## Related authored work

The same `4095` defect in shared schema enums was fixed in authored PR [#2138](https://github.com/riscv/riscv-unified-db/pull/2138) (`spec/schemas/schema_defs.json` plus a regression test). **Merged.**
