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

Recorded 2026-08-12, checked against `riscv-isa-manual` at revision `310a111`,
the revision `riscv/riscv-unified-db` pins.

**`priv_19.3.1_cmo_cache_blocks.txt` is not Privileged 19.3.1.** The passage
appears exactly once in the manual, in `src/unpriv/cmo.adoc` lines 86-92, in the
*Unprivileged* volume, under Background > Memory and Caches within Chapter 19,
"CMO Extensions for Base Cache Management Operation ISA". By the heading nesting
in that file the section is 19.2.1; 19.3.1 is "Memory Ordering". `src/cmo.adoc`
does not exist. So the label names the wrong volume and the wrong subsection, and
only the chapter number is right. The text itself is verbatim apart from
"(or NAPOT)", where the manual reads "(NAPOT)".

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
