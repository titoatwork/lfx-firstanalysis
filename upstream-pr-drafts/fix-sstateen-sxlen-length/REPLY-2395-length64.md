Done, pushed. All four take `length: 64`, and `DATA` on `sstateen1`-`sstateen3` collapses to `location: 31-0`. Net diff is 4 files, +7/-10. Title and body updated to match, since the conclusion changed rather than the wording.

One correction to my previous comment: I wrote "none of the 112 with a fixed integer `length`". The real figure is **288** of 461, not 112. The claim itself holds and is stronger than I stated, since zero of those 288 carry an XLEN-dependent field location, but the count was wrong and I would rather flag it than leave it in the thread.

`31-0` also lands where the description in these files already points: "4 * 32 = 128 bits for supervisor level", and the upper 32 bits of an `mstateen` CSR control state "inherently inaccessible to user level, so no corresponding enable bits in the supervisor-level `sstateen` CSR are applicable".

No IDL change was needed. `csr_value.DATA` narrows to `Bits<32>`, but `BinaryExpressionAst#type` gives a bitwise operator the wider of its operands, so `csr_value.DATA & mstateen1_mask` stays `Bits<64>`, and the field `sw_write` is compiled with a 128-bit return type independent of field width.

CI will be red on `regress-pre-commit` until the `prek` issue is sorted. It has been failing repo-wide since 2026-08-10 09:47 UTC, unrelated to this change.
