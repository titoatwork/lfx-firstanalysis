# Source and attribution

The two files in this directory are excerpts from the **RISC-V Instruction Set
Manual, Volume II: Privileged Architecture**, reproduced verbatim as supplied in
the LFX Fall 2026 Part II coding challenge.

| File | Section |
|------|---------|
| `priv_19.3.1_cmo_cache_blocks.txt` | Privileged Spec 19.3.1, cache maintenance operations |
| `priv_2.1_csr_address_mapping.txt` | Privileged Spec 2.1, conventional R/W accessibility of CSRs by address mapping |

**Copyright:** 2017-2025 Contributors to the RISC-V ISA Manual,
<https://github.com/riscv/riscv-isa-manual>

**License:** [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/)

`SPDX-License-Identifier: CC-BY-4.0`

The attribution above follows the convention `riscv/riscv-unified-db` uses in its
own `REUSE.toml` for imported ISA Manual text.

## Why these files carry no header

They are byte-faithful to the text as given in the challenge, so that any
comparison against the source passes exactly. Adding a licence header inside
them would break that, so the attribution lives here instead.

## Both section labels above are the challenge's, and one of them is wrong

Recorded 2026-08-12, checked against `riscv-isa-manual` at two revisions:
`310a111`, pinned by `riscv/riscv-unified-db` main, and `b2e69ab2`, pinned by the
branch behind PR #2164. The passage sits at the same path and the same lines in
both, so nothing below depends on which one you look at.

**`priv_19.3.1_cmo_cache_blocks.txt` is not Privileged 19.3.1.** The passage
appears exactly once in the manual, in `src/unpriv/cmo.adoc` lines 86-93, in the
*Unprivileged* volume, under Background > Memory and Caches. `src/cmo.adoc` does
not exist. The volume is wrong under any reading; the text is verbatim apart from
"(or NAPOT)", where the manual reads "(NAPOT)".

The section number depends on which rendering you read, so it is worth being
exact. `modules/unpriv/nav.adoc` labels `cmo.adoc` "Chapter 19. \"CMO\"
Extensions for Base Cache Management Operation ISA", and under that page
numbering the heading nesting in the file puts the passage at 19.2.1, with
19.3.1 being "Memory Ordering". That is the rendering in which a citation of the
form 19.3.1 refers to CMO at all, and the challenge's label is wrong within it.
In the monolithic build there is no `leveloffset` on the include chain
(`riscv-spec.adoc` to `unpriv/unpriv.adoc` to `unpriv/zi.adoc` to `cmo.adoc`), so
`cmo.adoc` is a section inside the "Scalar Integer Extensions" chapter and the
numbers differ entirely.

**`priv_2.1_csr_address_mapping.txt` is correctly labelled**, at
`src/priv/csrs.adoc`: chapter 2, "Control and Status Registers (CSRs)", section
2.1, "CSR Address Mapping Conventions". Its text is truncated rather than
mislabelled: the challenge omits the closing clause the manual carries,
"with the pattern `10` representing hypervisor CSRs". That clause contains none
of the words the challenge names as parameter indicators, so the snippet remains
a zero-parameter negative control.

The filenames and the result files keep the challenge's labels as identifiers,
because renaming them would break the link to what was submitted. This note is
the correction; the archive stays as supplied.

Everything else in `coding-challenge/` is the author's own work and is covered
by the repository [LICENSE](../../LICENSE).
