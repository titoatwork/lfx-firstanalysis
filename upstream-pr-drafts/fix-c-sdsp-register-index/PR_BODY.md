# PR body draft — fix(isa): c.sdsp must use its full 5-bit register index

**Issue number placeholder:** `#NNNN` below must be replaced before posting.
**Kept short on purpose.** The analysis lives in the issue; this says what
changed and why.

---

## Title

`fix(isa): c.sdsp must use its full 5-bit register index`

---

## Body

`c.sdsp` is a CSS-format instruction, so its `rs2` is a full 5-bit register specifier, and `c.sdsp.yaml` declares it that way (`location: 6-2`). Both branches then pass that field to `creg2reg`, which takes a 3-bit compressed index and returns `{2'b01, creg_idx}`. Its range is `x8`-`x15`, so on RV64 `c.sdsp x20, 0(sp)` stores from `x12`.

Drop `creg2reg` from both branches. `c.swsp` has the identical CSS field and uses `X[xs2]`; `I/sd.yaml` builds its pair as `{X[xs2 + 1], X[xs2]}`.

Encodings, `definedBy` and the `not:` lists are unchanged and already correct. Three stock configs reach the RV64 line; the RV32 branch is unreachable, since no config implements `Zclsd`.

Closes #NNNN

---

## If a reviewer asks for the detail

- `creg2reg` is declared `arguments Bits<3> creg_idx` at `globals.isa:348-350`.
- The spec draws C.SWSP, C.SDSP, C.FSWSP and C.FSDSP as one CSS group with a
  single 5-bit `rs2` in `images/wavedrom/c-sp-load-store-css.edn`.
- 75 `creg2reg` call sites across 33 files under `spec/std/isa/inst/`;
  72 pass a 3-bit field, and the 3 that do not are all in this file.
- The type checker does not catch it because `Type#convertable_to?`
  (`idlc/lib/idlc/type.rb:291-296`) ignores width for `:bits`.
- No `idlc` run; no Ruby toolchain on this machine.
