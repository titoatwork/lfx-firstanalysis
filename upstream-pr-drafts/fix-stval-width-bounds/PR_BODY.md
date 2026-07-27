# PR: fix(param): STVAL_WIDTH bounds match MTVAL_WIDTH

**Target:** `riscv/riscv-unified-db`  
**Branch:** `fix/stval-width-bounds` (local commit `f62eacd0` on clone)  
**Closes:** #2102  
**Author:** Ibteshamul Haque · `titoatwork`

## Summary

`STVAL_WIDTH` is the number of implemented bits in `stval` (a bit-width), but
its schema used `maximum: 2^64-1` with **no minimum**. The byte-size idiom
used for parameters like `CACHE_BLOCK_SIZE`, not for CSR widths.

Bring it to parity with the M-mode twin `MTVAL_WIDTH`:

| Field | Was | Now |
|-------|-----|-----|
| `minimum` | *(missing)* | `0` |
| `maximum` | `18446744073709551615` | `64` |
| `long_name` | `TODO` | `Width of the stval CSR` |

Spec: `stval` is an SXLEN-bit register (SXLEN ∈ {32,64}); a width of 2^64−1
bits is not representable.

## Diff scope

- **1 file:** `spec/std/isa/param/STVAL_WIDTH.yaml`
- No schema language change; no bulk param dump

## Test plan

- [ ] Visual parity with `MTVAL_WIDTH.yaml` bounds
- [ ] `./do test:schema` (or project equivalent) still passes
- [ ] No other files changed

## Suggested title

```
fix(param): STVAL_WIDTH bounds match MTVAL_WIDTH (#2102)
```
