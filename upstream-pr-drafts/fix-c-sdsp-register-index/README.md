# c.sdsp maps its 5-bit rs2 through creg2reg

**Status: FILED 2026-08-06.**
Issue: https://github.com/riscv/riscv-unified-db/issues/2418
PR:    https://github.com/riscv/riscv-unified-db/pull/2419

**Commit** `d4d229ce` on `fix/c-sdsp-full-register-index`, branched from
`origin/main` at `7ad0966e`. Two lines, one file. DCO passes.

Found while researching #2282 (`ld` and `sd` for RV32 are broken). ThinkOpenly
posted an endianness analysis there on 2026-08-05 that went unanswered for a
day; surveying the whole Zilsd/Zclsd family to answer it turned this up. The
reply on #2282 is `upstream-pr-drafts/issue-2282-zilsd-endianness/REPLY.md`,
posted as `issuecomment-5199576100`, and it flags this defect so a family
rewrite does not carry it forward. #2418 references #2282, so the
cross-reference appears on that thread automatically.

## The defect in one line

`c.sdsp` is CSS format, so `rs2` is a full 5-bit register specifier, but both
branches pass it to `creg2reg`, whose parameter is `Bits<3>` and whose body is
`return {2'b01, creg_idx}`, giving a range of `x8`-`x15`.

## Why this one is live, not latent

Unlike the Zilsd paths in #2282, the affected RV64 line is generated in stock
configurations. `c.sdsp` is `definedBy: anyOf: [allOf: [xlen: 64, Zca], Zclsd]`,
and three configs implement `Zca` at `MXLEN: 64`. The RV32 branch is
unreachable, which matches the reachability claim I made publicly on #2256.

## Every factual claim, and where it was verified

All checks against `origin/main` at `7ad0966e` (2026-08-06), submodule
`ext/riscv-isa-manual` at `310a1114`. No `idlc` run: no Ruby toolchain here.

| Claim | Verified against | Result |
|---|---|---|
| `xs2` is 5 bits in both encodings | `c.sdsp.yaml:28-30`, `:37-38` (`location: 6-2`) | confirmed, quoted |
| Both branches route it through `creg2reg` | `c.sdsp.yaml:56`, `:62` | confirmed, 3 call sites |
| `creg2reg` takes a 3-bit index | `globals.isa:348-350` | confirmed, read in full |
| Its body is `return {2'b01, creg_idx}` | `globals.isa`, function body | confirmed, quoted |
| So its range is `x8`-`x15` | derived from the concatenation | confirmed |
| The spec gives C.SDSP a 5-bit `rs2` | `images/bytefield/rvc-instr-quad2.edn:103` (`:span 5`) | confirmed, quoted |
| C.SWSP and C.SDSP share one CSS wavedrom | `images/wavedrom/c-sp-load-store-css.edn:7,9` | confirmed, quoted |
| Zclsd form is also 5-bit | `zclsd.adoc`, c.sdsp wavedrom | confirmed, quoted |
| Only the CS pair is restricted to `x8`-`x15` | `zclsd.adoc:15` | confirmed, quoted |
| `c.swsp` has the identical field and no `creg2reg` | `c.swsp.yaml` | confirmed, quoted |
| `c.sw` (CS, genuine 3-bit) correctly uses `creg2reg` | `c.sw.yaml` | confirmed |
| `I/sd.yaml` builds its pair as `{X[xs2 + 1], X[xs2]}` | `sd.yaml` RV32 branch | confirmed |
| 75 `creg2reg` call sites across 33 files | sweep of `spec/std/isa/inst/**` | confirmed by count |
| 72 pass a 3-bit field; the 3 that do not are all here | same sweep, width computed from `location:` | confirmed, enumerated |
| The type checker ignores width for `:bits` | `idlc/lib/idlc/type.rb:291-296` | confirmed, read in full |
| Arguments are checked with `convertable_to?` | `idlc/lib/idlc/ast.rb:7868` | confirmed |
| 3 configs implement `Zca` at `MXLEN: 64` | `rv64-riscv-tests`, `rv64-vector`, `example_rv64_with_overlay` | confirmed, enumerated |
| No config implements `Zclsd` or `Zilsd` | `grep` over `cfgs/` | confirmed, 0 hits |
| No existing upstream report | `gh search issues` for `c.sdsp` and `creg2reg` | confirmed, none |
| The patched file validates | `inst_schema.json` via `jsonschema` 4.26, with a negative control | confirmed, 0 errors |

## The sweep

Parses every instruction YAML under `spec/std/isa/inst/`, collects the names
passed to `creg2reg` in `operation()`, and computes each named variable's bit
width from its `location:` string across both encoding flavours. The script is
untracked, per `.gitignore:76`.

## Deliberately not claimed

- That the two replacement lines compile. No `idlc` available here.
- Anything about the `x0` rule at `zclsd.adoc:13`. Unimplemented here as it is
  in `sd`, and it belongs with the register-pair work under #2282.
- Anything about `c.ld`, `c.sd` or `c.ldsp`, whose `creg2reg` use is correct.
- What the generated C++ does with a `Bits<5>` argument to a `Bits<3>`
  parameter. The claim is about the type checker accepting it, not about
  observed truncation, which keeps this consistent with the non-claim recorded
  in `issue-2282-read-memory/COMMENT.md` on 2026-08-01.
