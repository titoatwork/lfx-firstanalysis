# PR body (not filed) — STVAL_WIDTH bounds

**Outcome:** not filed. Covered by [#2103](https://github.com/riscv/riscv-unified-db/pull/2103) for [#2102](https://github.com/riscv/riscv-unified-db/issues/2102).

Draft below is historical.

---

## Summary

`STVAL_WIDTH` is the number of implemented bits in `stval` (a bit-width), but its schema used `maximum: 2^64-1` with **no minimum**. That is the byte-size idiom used for parameters like `CACHE_BLOCK_SIZE`, not for CSR widths.

Bring it to parity with the M-mode twin `MTVAL_WIDTH`:

| Field | Was | Now |
|-------|-----|-----|
| `minimum` | *(missing)* | `0` |
| `maximum` | `18446744073709551615` | `64` |
| `long_name` | `TODO` | `Width of the stval CSR` |

Spec: `stval` is an SXLEN-bit register (SXLEN ∈ {32,64}); a width of 2^64−1 bits is not representable.

## Diff scope

- **1 file:** `spec/std/isa/param/STVAL_WIDTH.yaml`
- No schema language change; no bulk param dump

## Test plan

- Visual parity with `MTVAL_WIDTH.yaml` bounds
- Schema validation still passes
- No other files changed
