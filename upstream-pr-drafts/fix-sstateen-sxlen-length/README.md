# sstateen0-3 carry the wrong length

**Status: FILED 2026-08-05, revised 2026-08-11 after review.**
Issue: https://github.com/riscv/riscv-unified-db/issues/2394
PR:    https://github.com/riscv/riscv-unified-db/pull/2395

**Two commits** on `fix/sstateen-sxlen-length`, branched from `origin/main` at
`bac3bf6d`. Net 4 files, +7/-10.

| Commit | Change | Diff |
|---|---|---|
| `59af35af` | `length: MXLEN` -> `length: SXLEN` on all four | 4 files, +4/-4 |
| `688d575d` | `length: SXLEN` -> `length: 64`, and `DATA` on `sstateen1`-`sstateen3` collapsed to `location: 31-0` | 4 files, +7/-10 |

## How the conclusion changed

The original argument was that `sstateen*` are supervisor CSRs and the
privileged spec sizes them by S-mode, so `MXLEN` takes the width from the wrong
mode. ThinkOpenly approved at 2026-08-10 15:35 UTC, then reversed ten minutes
later at 15:45 UTC and requested `length: 64` instead, to match `mstateen*` and
`hstateen*`, with four inline `suggestion` blocks.

Applying those four as-is would have left `location_rv32: 31-0` on the `DATA`
field of `sstateen1`-`sstateen3` inside a register fixed at 64 bits. That was
raised at 20:27 UTC with a direct question, and answered at 2026-08-11 00:47 UTC:

> Let's go with `location: 31-0`. Undefined bits are read-only-0, which is fine
> here. The CSRs in your list are all well-defined with length `SXLEN`.
> `sstateen*` are weird.

`688d575d` is that, both halves together.

## Every factual claim, and where it was verified

All checks at `59af35af` (the state before the second commit) unless noted. No
`idlc` run: no Ruby toolchain on this machine, so the IDL type check is left to
CI. The type-system claims below are read off the compiler source, not observed.

| Claim | Verified against | Result |
|---|---|---|
| `hstateen0`-`hstateen3` are `priv_mode: S` at fixed `length: 64` | `spec/std/isa/csr/hstateen*.yaml` | confirmed |
| 8 `priv_mode: S` CSRs use a fixed `length: 64` | sweep of all CSRs under `spec/std/isa/csr/` | confirmed: hedeleg, henvcfg, hstateen0-3, htimedelta, sctrctl |
| No `sstateen0h`-`sstateen3h` exist | `ls spec/std/isa/csr/` | confirmed: 8 `h` registers for m/h, none for s |
| 461 CSRs under `spec/` | parse of every `kind: csr` YAML | confirmed |
| 288 of them have a fixed integer `length` | same sweep | confirmed (169/292 after this change) |
| 137 carry an XLEN-dependent field location | same sweep | confirmed, and **all 137 have a symbolic length** |
| 0 fixed-integer-length CSRs carry one | same sweep | confirmed before and after |
| 291 fields are a range narrower than their fixed-width register | same sweep | confirmed, e.g. `mhpmevent10` `EVENT: 57-0` in `length: 64` |
| `31-0` matches the description already in the file | `sstateen1.yaml` description text | confirmed: "4 * 32 = 128 bits for supervisor level" |
| Narrowing `DATA` needs no IDL change | `idlc/lib/idlc/ast.rb` `BinaryExpressionAst#type` and `#type_check` | confirmed: bitwise ops take `max(lhs, rhs)` width and do not require equal widths |
| `sw_write` return width is field-independent | `udb/lib/udb/obj/csr_field.rb:533` | confirmed: compiled with `return_type: Bits<128>` |
| All four still schema-valid | `csr_schema.json` via `jsonschema` | confirmed: 0 errors |

## A correction posted to the thread

The 20:27 UTC comment said "none of the **112** with a fixed integer `length`".
The real figure is **288** of 461. The claim itself holds and is stronger than
stated, since zero of those 288 carry an XLEN-dependent field location, but the
count was wrong. Corrected in the 2026-08-11 02:42 UTC reply rather than left in
the thread. What 112 measured is unknown; it was not the stated quantity.

## What this does NOT claim

- **Not** that any config in `cfgs/` observes the difference. None sets `SXLEN`
  different from `MXLEN`, so this corrects the model rather than a live output.
- **Not** that the generated C++ was inspected. No Ruby toolchain locally.

## Posted

| File | Where |
|---|---|
| `PR_BODY-v2.md` | PR #2395 body, replacing the original ~500-word body |
| `REPLY-2395.md` | `issuecomment-5245573852`, 2026-08-10 20:27 UTC |
| `REPLY-2395-length64.md` | `issuecomment-5248396412`, 2026-08-11 02:42 UTC |

Title also changed, since the conclusion moved rather than the wording:
`fix(csr): sstateen0-3 length should be SXLEN, not MXLEN` ->
`fix(csr): sstateen0-3 take the stateen family's fixed length of 64`
