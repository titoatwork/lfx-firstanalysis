# fix(param): correct 4095 typo in MTVEC_BASE_ALIGNMENT power-of-two enums

**Local branch:** `fix/mtvec-base-alignment-4096` @ `616a0c98`  
**Target:** `riscv/riscv-unified-db` `main`  
**Files:** 2 param YAML + 1 minitest regression

## Summary

`MTVEC_BASE_ALIGNMENT_DIRECT` and `MTVEC_BASE_ALIGNMENT_VECTORED` declare:

> An unsigned **power of 2** greater than or equal to 4 …

but both enums listed **`4095`** (`2^12 − 1`) instead of **`4096`** (`2^12`). That value is not a power of two and is the only non-power-of-two entry in each enum (copy-paste off-by-one).

## Change

| Field | Before | After |
|-------|--------|-------|
| enum entry | `4095` | `4096` |
| `long_name` | `Minumum alignment…` | `Minimum alignment…` |

## Why this is not modeling judgment

- Schema `description` explicitly requires power-of-two.  
- Every other enum value is `2^k` for k≥2.  
- Deterministic and reproducible; no open issue/PR found for this typo.

## Regression test

`tools/ruby-gems/udb/test/test_mtvec_base_alignment_pow2.rb` asserts:

- every enum entry is a positive power of two  
- `4096` present, `4095` absent  

## Test plan

- [ ] `ruby tools/ruby-gems/udb/test/test_mtvec_base_alignment_pow2.rb` (or suite equivalent)  
- [ ] YAML still schema-valid  
- [ ] No other files changed (except the two params + test)

## Suggested title

```
fix(param): correct 4095 typo in MTVEC_BASE_ALIGNMENT power-of-two enums
```
