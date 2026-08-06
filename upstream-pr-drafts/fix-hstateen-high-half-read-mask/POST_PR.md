`hstateen0h` through `hstateen3h` read their parent with `$bits(CSR[hstateenN])[63:32]`, which returns raw field storage and never runs the parent's `sw_read()`. That body is where the `mstateen` read-only-zero rule is implemented, so on RV32 the rule is not applied to any bit only the high half can reach. `hstateen1`-`hstateen3` model a single field each at bit 63, so for them nothing is masked at all.

Switch the four to `CSR[hstateenN].sw_read()[63:32]`, the form `henvcfgh` already uses against `henvcfg` (`spec/std/isa/csr/H/henvcfgh.yaml:119-120`). `mstateen0h`-`mstateen3h` keep `$bits()` correctly, because their parents have no `sw_read()` and there the raw value is the software view.

Length and fields are untouched; the field-level `sw_write` blocks already apply the mask. RV64 is unaffected, since all four are `definedBy` `xlen: 32`.

Closes #2413
