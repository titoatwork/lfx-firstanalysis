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

Everything else in `coding-challenge/` is the author's own work and is covered
by the repository [LICENSE](../../LICENSE).
