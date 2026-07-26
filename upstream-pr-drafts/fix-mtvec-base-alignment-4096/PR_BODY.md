## Summary

`MTVEC_BASE_ALIGNMENT_DIRECT` and `MTVEC_BASE_ALIGNMENT_VECTORED` declare an unsigned **power of 2** ≥ 4, but both enums list **`4095`** (`0xfff` = 2¹²−1) instead of **`4096`** (`0x1000` = 2¹²).

That value is the only non–power-of-two entry in each enum (off-by-one / copy-paste). The analogous STVEC-side size uses **`0x1000`**.

Also fixes `long_name` typo: `Minumum` → `Minimum`.

## Change

| Field | Before | After |
|-------|--------|-------|
| enum entry | `4095` | `4096` |
| `long_name` | `Minumum alignment…` | `Minimum alignment…` |

**Files:**
- `spec/std/isa/param/MTVEC_BASE_ALIGNMENT_DIRECT.yaml`
- `spec/std/isa/param/MTVEC_BASE_ALIGNMENT_VECTORED.yaml`
- `tools/ruby-gems/udb/test/test_mtvec_base_alignment_pow2.rb`
- `tools/ruby-gems/udb/test/run.rb` (load test)
- `tools/test/regress-tests.yaml` (CI matrix entry `mtvec_base_alignment_pow2`)

## Why this is deterministic

- `schema.description` requires a power of two.
- Every other enum value is `2^k` for `k ≥ 2`.
- `4095` cannot be a legal alignment power of two.

## Related

- Raised on maintainer PR #2090: MTVEC enums use `0xfff` while power-of-two is required.
- This PR is a **minimal data + regression** fix only (no tvec unification / IDL rewrite). Happy to close or rework if #2090 already lands the same correction.

## Test plan

- [ ] `./bin/ruby tools/ruby-gems/udb/test/test_mtvec_base_alignment_pow2.rb`
- [ ] Confirm `4095` absent and `4096` present in both enums
- [ ] Confirm all enum values are positive powers of two
- [ ] CI matrix includes `mtvec_base_alignment_pow2` under `regress-udb-unit-test`
