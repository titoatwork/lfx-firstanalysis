# PR body (not filed): MTVEC alignment 4095 → 4096

**Outcome:** not opened. Same defect fixed via review on [#2090](https://github.com/riscv/riscv-unified-db/pull/2090). See [`OPEN-DECISION.md`](./OPEN-DECISION.md).

Body below is the draft that would have been used.

---

## Summary

`MTVEC_BASE_ALIGNMENT_DIRECT` and `MTVEC_BASE_ALIGNMENT_VECTORED` declare an unsigned **power of 2** ≥ 4, but both enums list **`4095`** (`0xfff` = 2¹²−1) instead of **`4096`** (`0x1000` = 2¹²).

That value is the only non-power-of-two entry in each enum (off-by-one / copy-paste). The analogous STVEC-side size uses **`0x1000`**.

Also fixes `long_name` typo: `Minumum` → `Minimum`.

## Change

| Field | Before | After |
|-------|--------|-------|
| enum entry | `4095` | `4096` |
| `long_name` | `Minumum alignment…` | `Minimum alignment…` |

**Files (would have been):**

- `spec/std/isa/param/MTVEC_BASE_ALIGNMENT_DIRECT.yaml`
- `spec/std/isa/param/MTVEC_BASE_ALIGNMENT_VECTORED.yaml`
- plus a small unit/regression test

## Why deterministic

- Schema description requires a power of two.
- Every other enum value is `2^k` for `k ≥ 2`.
- `4095` cannot be a legal alignment power of two.

## Related

Raised on maintainer PR #2090: MTVEC enums use `0xfff` while power-of-two is required. Prefer landing in that PR over a competing one.
