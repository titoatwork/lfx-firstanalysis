# misa gating ignores MISA_CSR_IMPLEMENTED in 139 of 292 sites

**Status: FILED 2026-08-07, extended 2026-08-10 after review.**
Issue: https://github.com/riscv/riscv-unified-db/issues/2434
PR:    https://github.com/riscv/riscv-unified-db/pull/2435

**Two commits** on `fix/misa-csr-implemented-guard`, branched from `origin/main`
at `e909b6c9`. Net 130 files, +278/-314.

| Commit | Change | Diff |
|---|---|---|
| `95f69b24` | add the `MISA_CSR_IMPLEMENTED` guard at 139 sites | 130 files, +139/-139 |
| `6fd5a21e` | replace the direct `raise` with `reserved_instruction($encoding)` at the same 139 | 130 files, +139/-175 |

The second commit answers ThinkOpenly's review on 2026-08-10 (comment
`5245035942`): the guard alone left the 139 raising `IllegalInstruction`
directly, while the 153 already-correct sites routed through
`reserved_instruction()`, which is what consults
`TRAP_ON_UNIMPLEMENTED_INSTRUCTION` and therefore what lets `Ssstrict` govern
these traps. After it, all 292 match. Reply archived in `REPLY-2435.md`.

The `-175` on the second commit is 139 `raise` lines plus 36 lines of comment
about reporting `mode()` rather than `effective_ldst_mode()`, which the 18
`Zalrsc` sites carried and which `reserved_instruction()` makes redundant.

## Posted

| File | Where |
|---|---|
| `PR_BODY.md` | PR #2435 body |
| `REPLY-2435.md` | `issuecomment-5246384873`, 2026-08-10 21:44 UTC |
| `REPLY-2435-ci-fixed.md` | `issuecomment-5248517389`, 2026-08-11 03:04 UTC |

`REPLY-2435.md` closes by saying CI would stay red "until the `prek` issue is
sorted". Calling it a prek issue was a mislabel carried over from the wrong root
cause posted on #2419; the actual cause was a node `devEngines` mismatch, fixed
by #2455 at 2026-08-11 01:53 UTC. `REPLY-2435-ci-fixed.md` is that correction.
The full account is in
[`../fix-c-sdsp-full-register-index/README.md`](../fix-c-sdsp-full-register-index/README.md).

Found by sweeping the pattern behind ThinkOpenly's #1175 (`MISA extension bits
mean "supported" and "maybe?"`). #1175 itself is stalled on an unresolved design
question — dhower-qc proposed a `STRICT_MISA_EXTENSION_BITS` parameter,
ThinkOpenly asked how much granularity is needed, and nobody answered. This PR
deliberately does **not** touch that question. It fixes a separate, settled
defect that the sweep turned up on the way: whether a misa bit should be
consulted at all when `misa` is not implemented. The repo already answers that
in 153 places.

## The defect in one line

`if (implemented?(ExtensionName::B) && (CSR[misa].B == 1'b0)) { raise ... }` reads
a `misa` bit without checking `MISA_CSR_IMPLEMENTED`, so on a hart where `misa`
is read-only-0 the check traps an instruction the hart supports.

## Why this one is latent, not live

Stated plainly in the issue. All 7 `fully configured` configs set
`MISA_CSR_IMPLEMENTED: true`, so `X && true ≡ X` and no generated output changes.
The other 6 configs are `unconfigured` or `partially configured` and pin no value.
This is the opposite of #2418/#2419 (c.sdsp), which was live in 3 stock configs.

## Why the fix is safe to take now

- No behavior change on any config in the tree.
- No new parameter dependency: instruction IDL already references
  `MISA_CSR_IMPLEMENTED` in 153 places, so the 139 new references reach a
  parameter that is already in scope wherever these instructions are.
- No golden file changes: `tests/golden/*.h` and `*.svh` carry parameter
  `#define`s only, and `all_instructions.golden.adoc` does not embed
  `operation()` bodies (0 occurrences of `CSR[misa]`).

## Every factual claim, and where it was verified

All checks against `origin/main` at `e909b6c9` (2026-08-07). No `idlc` run: no
Ruby toolchain on this machine, so the IDL type check and layout regeneration are
left to CI.

| Claim | Verified against | Result |
|---|---|---|
| 292 misa-gated illegal-instruction checks exist | `git grep` over `spec/**/inst/**`, `sweep_misa.py` | confirmed |
| 153 of them guard on `MISA_CSR_IMPLEMENTED` | same sweep | confirmed: Zaamo 81, Zabha 72 |
| 139 do not | same sweep | confirmed: 132 std + 7 custom |
| All 153 guarded sites gate `misa.A` | sweep, grouped by bit | confirmed |
| `Zalrsc` gates `misa.A` unguarded, 18 sites | sweep | confirmed — same bit, both spellings in tree |
| `mstatus.yaml` uses the guard in both polarities | `mstatus.yaml:426,429,443,449,498,501,510,516` | confirmed, 7 lines quoted |
| `MISA_CSR_IMPLEMENTED: false` means read-only-0 | `param/MISA_CSR_IMPLEMENTED.yaml` description | confirmed, quoted |
| `misa.yaml` never references the parameter | `grep -c` in `csr/misa.yaml` | confirmed: 0, and no CSR-level `sw_read()` |
| No backend/Ruby code reads the parameter | repo-wide `git grep` over `*.rb *.erb *.py *.hpp *.h` | confirmed: only a generated golden `#define` |
| All 7 fully configured configs set it `true` | `cfgs/*.yaml`, `type:` + value per file | confirmed, table in issue |
| The other 6 pin no value | same | confirmed: unconfigured / partially configured |
| Only `Zalrsc` is generated | `auto-generated` header probe on all 139 | confirmed: 2 `.layout` + 16 generated, 121 hand-written |
| Layout edit == regeneration output | layout line and generated line compared after edit | confirmed identical; inserted text has no ERB |
| Replacement string is unambiguous | 139 occurrences of `" && (CSR[misa]."` under `inst/`, all gate shape | confirmed, 0 non-gate matches |
| Change is +1/-1 per site | `git diff -U0`, normalized | confirmed: 139 hunks, 139 `+`, 139 `-`, one shape each |
| No non-`inst/` file touched | `git diff --name-only` | confirmed: none |
| All changed YAML still parses | `yaml.safe_load` over the 128 changed `.yaml` | confirmed: 0 failures |

## What this does NOT claim

- **Not** that any shipped config misbehaves today. It does not; all 7 set the
  parameter `true`.
- **Not** that a zero misa bit on an implemented `misa` should stop raising
  `IllegalInstruction`. That is #1175's open question and is untouched here.
- **Not** that the generated C++ was inspected. No Ruby toolchain locally; the
  no-op argument is `X && true ≡ X` on the IDL, not an observed diff of generated
  output.

## The follow-up that is deliberately not in this PR

`misa.yaml` does not implement its own parameter: setting
`MISA_CSR_IMPLEMENTED: false` leaves every field resetting to
`implemented?(ExtensionName::X) ? 1 : 0`, so `misa` does not actually read
read-only-0. Raised as an observation at the end of #2434, with the ordering
argument — that fix needs this one to land first, or the 139 latent sites become
live in exactly the configuration it is meant to enable. Offered to file
separately rather than filed unprompted.

## Scope note left for the maintainer

7 of the 139 sites are in `spec/custom/isa/qc_iu/inst/Xqccmp/`, a vendor
extension. They carry the identical defect and got the identical edit. Called out
explicitly in the issue table so a maintainer can ask for them to be dropped if
custom extensions are meant to be out of scope.
