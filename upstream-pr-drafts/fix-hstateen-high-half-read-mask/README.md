# hstateen0h-hstateen3h read around their parent's mstateen mask

**Status: FILED 2026-08-06.**
Issue: https://github.com/riscv/riscv-unified-db/issues/2413
PR:    https://github.com/riscv/riscv-unified-db/pull/2414

**Commit** `02c2bda9` on `fix/hstateen-high-half-read-mask`, rebased onto
`origin/main` at `7ad0966e`. Four lines, four files. DCO passes.

Released ahead of the 08-08 window deliberately. On 2026-08-04 ThinkOpenly called
[#2377](https://github.com/riscv/riscv-unified-db/issues/2377) "the tip of the
iceberg for replacing aliases with code across the project" on
[#781](https://github.com/riscv/riscv-unified-db/issues/781), and RAJVEER42 is
mid-inventory on that same surface. Filing into a live design discussion is worth
more than filing into a quiet one.

**Identity:** this is the first PR signed as
`Ibteshamul Haque <ibteshamulhaque01@gmail.com>`. Global `git config user.name`
moved from `titoatwork` to the real name on 2026-08-05 so the author line and the
sign-off match exactly, which is what DCO inspects. The 12 earlier PRs sign as
`titoatwork`; that is deliberate and not being rewritten.

## The defect in one line

`hstateen0h`-`hstateen3h` read their parent with `$bits(CSR[hstateenN])[63:32]`,
which returns raw field storage and never runs the parent's `sw_read()`, where
the `mstateen` read-only-zero rule is implemented.

## Filing checklist (done 2026-08-06)

1. Re-fetch `origin/main` and re-run the sweep below; the pin will have moved.
2. File the issue from `ISSUE.md` (body only, from the `## Body` heading down).
3. **Replace `#2413` in the commit message** with the issue number:
   `git commit --amend` on `fix/hstateen-high-half-read-mask`. The placeholder
   is deliberately invalid so an unamended push is obvious.
4. Push to `fork`, open the PR with `PR_BODY.md`, replacing `#2413` there too.
5. Sign-off belongs in the commit only. `PR_BODY.md` and `ISSUE.md` have zero
   occurrences and must keep it that way.

## Every factual claim, and where it was verified

All checks re-run against `origin/main` at `7ad0966e` (2026-08-06), submodule
`ext/riscv-isa-manual` pinned at `310a1114`. No `idlc` run: there is no Ruby
toolchain on this machine, and `bin/` needs one.

| Claim | Verified against | Result |
|---|---|---|
| The four high halves use the `$bits()` form | `hstateen0h.yaml:159`, `hstateen1h.yaml:47`, `hstateen2h.yaml:47`, `hstateen3h.yaml:47` | confirmed, quoted |
| Each parent masks against its `mstateen` | `hstateen0.yaml:214`, `hstateen1-3.yaml:64` | confirmed, quoted |
| `CSR[x]` rvalue compiles to `_hw_read()` | `backends/cpp_hart_gen/lib/gen_cpp.rb:1059-1068` | confirmed, read in full |
| `CSR[x].sw_read()` compiles to `_sw_read()` | `backends/cpp_hart_gen/lib/gen_cpp.rb:325-330` | confirmed, read in full |
| `_sw_read()` runs the custom body, else falls back to `_hw_read()` | `backends/cpp_hart_gen/templates/csrs_impl.hxx.erb:116-137` | confirmed, read in full |
| `_hw_read()` composes from raw field storage | `backends/cpp_hart_gen/templates/csrs.hxx.erb:302-314` | confirmed |
| `$bits()` is a width cast and does not change the read | `BitsCastAst`, `tools/ruby-gems/idlc/lib/idlc/ast.rb:4418` | confirmed, `type`/`value` read in full |
| The two builtins are declared apart | `spec/std/isa/isa/builtin_functions.idl:70-87` | confirmed, quoted both descriptions |
| A Zicsr read arrives via `csr_sw_read` | `spec/std/isa/inst/Zicsr/csrrs.yaml:74`, `csrrw.yaml:66` | confirmed |
| `norm:mstateen_lower_priv_roz` says the bit is RO-zero | `ext/riscv-isa-manual/src/priv/smstateen.adoc:141` | confirmed, quoted |
| The high halves are an access path, not separate registers | same file line 65, `norm:stateen_rv32_upper_bits_csrs` | confirmed, quoted |
| The rule is registered in this repo | `ext/riscv-isa-manual/normative_rule_defs/smstateen.yaml:62` | confirmed |
| `mstateen0` has no field `sw_write` | 0 occurrences in `spec/std/isa/csr/mstateen0.yaml` | confirmed by count |
| The write path already masks | `hstateen0h.yaml:55-60` and the other 6 fields | confirmed, quoted |
| The CTR description states the rule | `hstateen0h.yaml:155-156` | confirmed, quoted |
| 7 of `hstateen0`'s 10 fields are in bits 63:32 | SE0 63, ENVCFG 62, CSRIND 60, AIA 59, IMSIC 58, CONTEXT 57, CTR 54; JVT 2, FCSR 1, C 0 | confirmed, enumerated |
| `hstateen1-3` model only `SE0` at bit 63 | `hstateen1-3.yaml` | confirmed, enumerated |
| RV64 is unaffected | all four are `definedBy` `xlen: 32` | confirmed |
| Exactly 4 registers are in the defect class | sweep of every `*h` CSR with an existing base, testing the `sw_read()` form against whether the parent has one | confirmed, 4 of 109 |
| `mstateen0h`-`3h` are correctly left alone | same sweep: `$bits()` form, parents have no `sw_read()` | confirmed |
| `henvcfgh` is the correct-idiom sibling | `henvcfg.yaml:342-364` masks 5 bits, 3 in the high half; `henvcfgh.yaml:119-120` uses `.sw_read()` | confirmed, quoted |
| Shapes match for the fix | `hstateen0` `length: 64`, `hstateen0h` `length: 32`, same as `henvcfg`/`henvcfgh` | confirmed |
| The parent exists wherever the high half does | `hstateen0h.definedBy` = `hstateen0`'s condition plus `xlen: 32` | confirmed, both read in full |
| No existing upstream issue | `gh search issues --repo riscv/riscv-unified-db "stateen" --include-prs` returns #2394/#2395 (mine), #781, #592, #782, #1793 | confirmed |
| The four patched files still validate | `csr_schema.json` via `jsonschema` 4.26, with a negative control (`length: 999` rejected) | confirmed, 0 errors |

## The sweep

Enumerates every CSR under `spec/std/isa/csr/` whose name ends in `h` and whose
base register also exists, classifies each `sw_read()` body by how it reaches
the parent, and checks that against whether the parent has a `sw_read()` of its
own. The script lives beside this file as `scripts/sweep_high_half.py`; it is
untracked, because `.gitignore:76` excludes `upstream-pr-drafts/**/*.py`.

Result at `7ad0966e`, before the fix: 109 high-half CSRs with an existing base.

| Form of the high half's `sw_read()` | Count |
|---|---|
| no parent reference (counters, `cycleh`, `timeh`) | 62 |
| no `sw_read()` at all | 36 |
| `$bits(CSR[parent])` | 8 |
| other parent reference (`minstreth`, `htimedeltah`) | 2 |
| `CSR[parent].sw_read()` | 1 |

Four of the eight `$bits()` users have a parent with read logic, and they are
`hstateen0h`-`hstateen3h`. The other four are `mstateen0h`-`mstateen3h`, whose
parents have no `sw_read()`, so the raw value is the software view and `$bits()`
is right. The single `.sw_read()` user is `henvcfgh`. `mhpmcounterNh` reaches
the right value through `read_hpm_counter(N)[63:32]` rather than the parent CSR,
which is why the counters land in the first row.

After the fix the `$bits()` row drops to 4 and the `.sw_read()` row rises to 5,
and the defect class is empty.

## Publication

Held untracked until the issue was filed, since publishing a defect report in
the public portfolio repo before the maintainers have been told about it is the
wrong order. Filed 2026-08-06 as #2413 and #2414, and committed here the same
day alongside the census refresh. `ISSUE.md` and `scripts/*.py` stay ignored,
per `.gitignore:71-76`.

## Deliberately not claimed

- That the four replacement bodies compile. No `idlc` available here.
- Anything about `reset_value: UNDEFINED_LEGAL` on these fields against
  `norm:mstateen_zero_initialization`. Not analysed.
- That `alias:` should be carrying the forwarding. That is #781's question, and
  `CsrField#alias` builds an `Alias` object without forwarding either direction.
- Any claim about the `sstateen` VS-mode masking branch, which is separate.

## Provenance

Found on 2026-08-05 while re-validating the review posted on PR #2378
(`issuecomment-5187345151`), which mentions it in passing as deserving its own
issue. This is that issue.
