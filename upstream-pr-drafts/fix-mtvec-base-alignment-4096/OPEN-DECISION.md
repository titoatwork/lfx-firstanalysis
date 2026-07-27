# Decision — RESOLVED: do **not** open. Superseded upstream.

**Opened:** 2026-07-27 · **Closed:** 2026-07-27  
**Outcome:** the fix landed in the maintainer's PR. This branch is retired unopened.

## What happened

| Item | Status |
|------|--------|
| Maintainer PR [#2090](https://github.com/riscv/riscv-unified-db/pull/2090) | **MERGED** 2026-07-27 |
| Our comment on #2090 (26 Jul) | Flagged `0xfff` (4095) in both MTVEC alignment enums against a schema requiring a power of two |
| Maintainer reply | jordancarlin: *"Looks like this was an issue in the old decimal version too … I agree that it should be 4096. Updated accordingly."* |
| `0xfff` on upstream `main` | **Gone**. Verified after merge |
| Our branch `fix/mtvec-base-alignment-4096` | **Retired unopened** |

## Why this was the right call

Opening a competing PR against files already under active maintainer edit would have been a visible race for credit on a one-token fix. Raising it as a review comment got the same defect corrected, in the maintainer's own PR, in under 12 hours.

## How to describe it

> Review comment on #2090 identified a non-power-of-two value in both MTVEC alignment enums; the maintainer adopted the correction and #2090 merged with `0x1000`.

Do **not** describe #2090 as our merged PR. It is jordancarlin's.

## Related, still open

The same `4095` defect exists in the shared schema enums and is fixed by our own PR
[**#2138**](https://github.com/riscv/riscv-unified-db/pull/2138), `spec/schemas/schema_defs.json` plus a regression test. That one is ours and is awaiting review.
