# PR body draft — fix(csr): hstateen0h-3h must read through their parent's sw_read

**Status:** HELD until 2026-08-08. Not filed.
**Branch:** `fix/hstateen-high-half-read-mask` off `origin/main` at `4cf908e8`.
**Issue number placeholder:** `#2413` below must be replaced with the filed issue number before posting.

**Kept short on purpose.** ThinkOpenly rewrote #2384's description down to two
sentences on 2026-08-05 and archived the original as a comment, so a long
reviewer-facing body gets replaced rather than read. The analysis lives in
`ISSUE.md`; this says what changed and why.

---

## Title

`fix(csr): hstateen0h-3h must read through their parent's sw_read`

---

## Body

`hstateen0h` through `hstateen3h` read their parent with `$bits(CSR[hstateenN])[63:32]`, which returns raw field storage and never runs the parent's `sw_read()`. That body is where the `mstateen` read-only-zero rule is implemented, so on RV32 the rule is not applied to any bit only the high half can reach. `hstateen1`-`hstateen3` model a single field each at bit 63, so for them nothing is masked at all.

Switch the four to `CSR[hstateenN].sw_read()[63:32]`, the form `henvcfgh` already uses against `henvcfg` (`spec/std/isa/csr/H/henvcfgh.yaml:119-120`). `mstateen0h`-`mstateen3h` keep `$bits()` correctly, because their parents have no `sw_read()` and there the raw value is the software view.

Length and fields are untouched; the field-level `sw_write` blocks already apply the mask. RV64 is unaffected, since all four are `definedBy` `xlen: 32`.

Closes #2413

---

## If a reviewer asks for the detail

Everything below is in `ISSUE.md` and should stay there unless asked:

- `CSR[x]` as an rvalue compiles to `_hw_read()` (`backends/cpp_hart_gen/lib/gen_cpp.rb:1059-1068`), `CSR[x].sw_read()` compiles to `_sw_read()` (`:325-330`), and `_sw_read()` carries the custom body (`templates/csrs_impl.hxx.erb:116-137`). The builtins are declared apart for this reason at `spec/std/isa/isa/builtin_functions.idl:70-87`.
- The rule is `norm:mstateen_lower_priv_roz`, `ext/riscv-isa-manual/src/priv/smstateen.adoc:141`.
- Reachability: `mstateen0` has no field `sw_write`, so clearing a bit there leaves `hstateen0`'s storage alone.
- Scope: of 109 high-half CSRs, exactly four pair a `$bits()` read with a parent that has read logic.
- No `idlc` run; no Ruby toolchain on this machine.
