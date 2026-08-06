On RV32, `hstateen0h` through `hstateen3h` return the stored contents of bits 63:32 of the matching `hstateen` register without applying the read-only-zero masking that the parent's own `sw_read()` implements. For `hstateen1`, `hstateen2` and `hstateen3` this means the mask has no effect at all on RV32, because their only modelled field sits at bit 63.

## What the specification requires

`ext/riscv-isa-manual/src/priv/smstateen.adoc:141` (`norm:mstateen_lower_priv_roz`, at the submodule commit this repository pins, `310a1114`):

> For every bit in an `mstateen` CSR that is zero (whether read-only zero or set to zero), the same bit appears as read-only zero in the matching `hstateen` and `sstateen` CSRs.

The rule is about the architectural register, and the high-half CSRs are an access path to that same register rather than a register of their own. `norm:stateen_rv32_upper_bits_csrs` at line 65 of the same file:

> For RV32, there are CSR addresses for **accessing the upper 32 bits of corresponding machine-level and hypervisor CSRs**: `mstateen0h`, `mstateen1h`, `mstateen2h`, `mstateen3h`, `hstateen0h`, `hstateen1h`, `hstateen2h`, and `hstateen3h`.

So bit 30 of `hstateen0h` is bit 62 of `hstateen0`, and reading it must observe the same read-only-zero rule. The rule is registered in this repository as `mstateen_lower_priv_roz` in `ext/riscv-isa-manual/normative_rule_defs/smstateen.yaml:62`.

## What the model does

`spec/std/isa/csr/hstateen0.yaml:214` implements the rule:

```
sw_read(): |
  # for every bit in an mstateen CSR that is zero, the same bit
  # appears as read-only zero in the matching hstateen CSR

  Bits<64> mstateen0_mask = $bits(CSR[mstateen0]);
  Bits<64> hstateen0_value = $bits(CSR[hstateen0]) & mstateen0_mask;
  return hstateen0_value;
```

`hstateen1.yaml:64`, `hstateen2.yaml:64` and `hstateen3.yaml:64` carry the same body against their own `mstateen`.

The four high halves do not go through it. `spec/std/isa/csr/hstateen0h.yaml:159`:

```
sw_read(): return $bits(CSR[hstateen0])[63:32];
```

`hstateen1h.yaml:47`, `hstateen2h.yaml:47` and `hstateen3h.yaml:47` are the same line against their own parent.

`$bits(CSR[x])` is not `CSR[x].sw_read()`. The two compile to different functions:

- `CsrReadExpressionAst#gen_cpp` (`backends/cpp_hart_gen/lib/gen_cpp.rb:1059-1068`) emits `__UDB_CSR_BY_NAME(x)._hw_read()`.
- `CsrFunctionCallAst#gen_cpp` (`backends/cpp_hart_gen/lib/gen_cpp.rb:325-330`) emits `__UDB_CSR_BY_NAME(x)._sw_read()` for `sw_read`.
- `_sw_read()` (`backends/cpp_hart_gen/templates/csrs_impl.hxx.erb:116-137`) emits the custom body when the CSR has one and falls back to `_hw_read()` when it does not.
- `_hw_read()` (`backends/cpp_hart_gen/templates/csrs.hxx.erb:302-314`) composes the value from raw field storage.

`$bits(...)` itself is a width cast over whatever the inner expression produced (`BitsCastAst`, `tools/ruby-gems/idlc/lib/idlc/ast.rb:4418`), so it does not change which read is called. The builtin declarations in `spec/std/isa/isa/builtin_functions.idl:70-87` name the distinction directly: `csr_hw_read` "Returns the raw value of csr", `csr_sw_read` "Returns the result of `CSR[csr].sw_read()`; i.e., the software view of the register".

A Zicsr read reaches this through `csr_sw_read` (`spec/std/isa/inst/Zicsr/csrrs.yaml:74`, `csrrw.yaml:66`), which dispatches to `hstateen0h`'s own custom body, which then calls `_hw_read()` on the parent. The parent's mask is never evaluated on that path.

## Why the stale bit is reachable

`mstateen0` has no field `sw_write` (0 occurrences in `spec/std/isa/csr/mstateen0.yaml`), so clearing a bit there has no side effect on `hstateen0`'s storage. That leaves an ordinary sequence:

1. RV32 hart with `H`, `Smstateen` and `Ssstateen`.
2. M-mode sets `mstateen0.ENVCFG` to 1.
3. Software writes `hstateen0h.ENVCFG` to 1. The field's `sw_write` at `hstateen0h.yaml:55-60` sees `mstateen0.ENVCFG == 1`, forwards to `CSR[hstateen0].ENVCFG` and returns 1.
4. M-mode clears `mstateen0.ENVCFG` to 0.
5. Reading `hstateen0h` returns bit 30 set, where the specification requires read-only zero.

`norm:hstateen_sstateen_zero_initialization` at line 154 anticipates step 4 exactly, and makes re-initialising `hstateen` a software responsibility. The read-only-zero rule is a hardware property that has to hold whether or not software does that.

## The file already contradicts itself

Each field's `sw_write` in these four files applies the mask. `hstateen0h.yaml:55-60`:

```
sw_write(csr_value): |
  if (CSR[mstateen0].ENVCFG == 1'b0){
    return 0;
  }
  CSR[hstateen0].ENVCFG = csr_value.ENVCFG;
  return csr_value.ENVCFG;
```

So a write of 1 is refused while `mstateen0.ENVCFG` is zero, but a 1 written earlier, while it was one, still reads back. And the CTR field's own description at `hstateen0h.yaml:155-156` states the rule the file does not implement on the read path:

> `hstateen0.CTR` is read-only 0 when `mstateen0.CTR=0`.

## How much is actually masked on RV32

`hstateen0` has ten modelled fields. Seven of them (`SE0` 63, `ENVCFG` 62, `CSRIND` 60, `AIA` 59, `IMSIC` 58, `CONTEXT` 57, `CTR` 54) are in the high half and reachable on RV32 only through `hstateen0h`. Three (`JVT` 2, `FCSR` 1, `C` 0) are in the low half. So the mask reaches three of the ten.

`hstateen1`, `hstateen2` and `hstateen3` model a single field each, `SE0` at bit 63. On RV32 their `sw_read()` masks a half with nothing in it, and the only path to the bit that exists is the high-half CSR that skips the mask.

On RV64 there is no defect: `hstateen0h`-`hstateen3h` are `definedBy` `xlen: 32`, so every read goes through the parent.

## Scope

I enumerated all 109 CSRs under `spec/std/isa/csr/` whose name ends in `h` and whose base register also exists, then checked each one's `sw_read()` body for the `$bits(CSR[parent])` form against whether that parent has a `sw_read()` of its own. Eight use `$bits()`, one uses `.sw_read()`, 36 have no `sw_read()` at all, 62 have one that never mentions the parent, and 2 read a field of it instead (`minstreth` via `CSR[minstret].COUNT[63:32]`, `htimedeltah` via `CSR[htimedelta].DELTA[63:32]`, both against parents with no `sw_read()`). Of the eight, exactly four have a parent with read logic, and they are these four.

The other four are `mstateen0h`-`mstateen3h`, which use the same `$bits()` form and are correct, because `mstateen0`-`mstateen3` have no `sw_read()` and the raw value is the software view. The counter high halves land outside this entirely: `mhpmcounterNh` reaches its value through `read_hpm_counter(N)[63:32]` rather than the parent CSR.

## How this sits against #781

Narrower than the alias question #781 is tracking, and it lands inside the part of it that has already been measured.

The inventory in [#781](https://github.com/riscv/riscv-unified-db/issues/781) splits the 104 high-half CSRs carrying `alias:` into 71 that already have a CSR-level `sw_read()` and 33 that do not, with [#2377](https://github.com/riscv/riscv-unified-db/issues/2377) among the 33. I reproduce that split exactly on `7ad0966e`: 148 CSRs carry an alias, 104 of them are high halves, 71 have a CSR-level `sw_read()` and 33 do not.

These four are in the 71. That split measures whether a `sw_read()` exists, which is the right question for #2377, and for these four it is not sufficient: the body is present and reads the wrong thing. So this is not another instance of the 33, and fixing the 33 would not reach it.

`henvcfgh` is the counterexample in the other direction and is the sibling case: `henvcfg.yaml:342-364` masks five bits against `menvcfg`, three of them (`STCE` 63, `PBMTE` 62, `ADUE` 61) in the high half, and `henvcfgh.yaml:119-120` is

```
sw_read(): |
  return CSR[henvcfg].sw_read()[63:32];
```

which keeps the mask. Same privilege level, same 64-bit parent with a 32-bit high half, opposite idiom.

## Suggested fix

Change the four lines to the form `henvcfgh` already uses:

```
sw_read(): return CSR[hstateen0].sw_read()[63:32];
```

`hstateen0` is `length: 64` and `hstateen0h` is `length: 32`, the same shapes as `henvcfg` and `henvcfgh`. `hstateen0h`'s `definedBy` is `hstateen0`'s condition (`H` and `Smstateen` and `Ssstateen`) plus `xlen: 32`, so the parent exists wherever the high half does. No field changes; the `sw_write` blocks are already correct.

## What I am not claiming

I have not run `idlc` (no Ruby toolchain here), so the four replacement bodies are worth an actual build. I am not claiming anything about the `reset_value: UNDEFINED_LEGAL` on these fields against `norm:mstateen_zero_initialization`, which I have not analysed, nor about whether the `alias:` annotations should be carrying this forwarding; that is #781's question, and `CsrField#alias` builds an `Alias` object without forwarding reads or writes today.
