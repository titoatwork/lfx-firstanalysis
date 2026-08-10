A `misa` that reads zero means `misa` is not implemented, not that no extensions are. `MISA_CSR_IMPLEMENTED` models that, and its description says `false` makes `misa` read-only-0.

Of the 292 misa-gated illegal-instruction checks, 139 consulted a `misa` bit without first checking that `misa` exists, and raised `IllegalInstruction` directly instead of calling `reserved_instruction()`. The 153 in `Zaamo` and `Zabha` already do both, and `mstatus.yaml` uses the same guard in both polarities. This brings the 139 into line. `reserved_instruction()` is documented for exactly this case, "called when an instruction is architecturally defined but has been disabled at runtime (e.g., by clearing misa.A)", and it honors `TRAP_ON_UNIMPLEMENTED_INSTRUCTION`, which `Ssstrict` requires to be true, so routing through it is what lets `Ssstrict` govern these traps.

No behavior change in the tree: every config that pins `MISA_CSR_IMPLEMENTED` or `TRAP_ON_UNIMPLEMENTED_INSTRUCTION` sets it true. Only `misa.A`, `.B`, `.C`, `.D`, `.F` and `.M` are affected; the 23 `misa.S` and `misa.H` sites test `== 1` to select behavior rather than to trap, so they are a separate question. `Zalrsc` is the only generated directory involved, and its 2 `.layout` templates and 16 generated files got the identical edit.

Closes #2434
