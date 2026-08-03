# PR body (filed): string-enum param literal smoke check

**Outcome:** open as [#2289](https://github.com/riscv/riscv-unified-db/pull/2289) · closes [#2285](https://github.com/riscv/riscv-unified-db/issues/2285)

---

String-enum parameters list legal values under `schema.enum`, but IDL comparisons in CSR `type()` and similar sites are free text. A typo such as `"always_zero"` where the enum only has `"always zero"` is never rejected by schema validation and changes the meaning of the condition.

A full scan of `spec/std/isa/{csr,isa,inst,param}` found 156 `PARAM ==/!= "..."` comparisons against string-enum parameters; exactly two were invalid, both `TINST_VALUE_ON_STORE_AMO_ACCESS_FAULT != "always_zero"` in `htinst` and `mtinst` (the case called out on #2271). Those two lines are corrected here so the tree is clean.

Also adds `tools/scripts/check_param_enum_literals.py` and a smoke CI job so any later invalid literal fails the PR. Unit tests cover a valid compare, an invalid typo, and ignoring non-parameter identifiers.

Closes #2285

Note: the two-line data fix overlaps #2271. Happy to drop those lines and rebase if that PR lands first; the validation is the lasting piece.
