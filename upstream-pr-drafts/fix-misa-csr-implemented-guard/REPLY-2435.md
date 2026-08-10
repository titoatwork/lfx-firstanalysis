Thanks both, that was the right catch and the tree already had the missing piece.

@ThinkOpenly on the `Ssstrict` condition: UDB spells it `TRAP_ON_UNIMPLEMENTED_INSTRUCTION`, `Ssstrict.yaml` requires that parameter to be true, and the mechanism that consults it is `reserved_instruction()` in `globals.isa`. Its docstring describes these sites exactly: "called when an instruction is architecturally defined but has been disabled at runtime (_e.g._, by clearing misa.A)".

The two families had diverged in two places, not one:

| | guard | action on `misa.X == 0` |
|---|---|---|
| `Zaamo`/`Zabha` (153) | `MISA_CSR_IMPLEMENTED` | `reserved_instruction($encoding)` |
| everything else (139) | none | `raise(ExceptionCode::IllegalInstruction, ...)` |

I have pushed the second half, so all 292 now match. Your condition 4 holds by construction rather than by assertion, and it is still a no-op in tree since every config that pins `TRAP_ON_UNIMPLEMENTED_INSTRUCTION` sets it true. The 18 `Zalrsc` sites also lose a comment about reporting `mode()` rather than `effective_ldst_mode()`, since `reserved_instruction()` uses `mode()` internally and the `Zaamo`/`Zabha` memory operations carry no such note.

CI will be red on this until the `prek` issue is sorted. `regress-pre-commit` has been failing repo-wide since 2026-08-10 09:47 UTC, unrelated to this change.

@jordancarlin I agree with the spec reading, but I do not think this PR is where that gets settled. `misa.yaml` already commits to a policy for all six bits touched here: `type()` is RW only when `implemented?(X) && MUTABLE_MISA_X`, `reset_value()` is 1 when implemented, and the field description states under `[when,"MUTABLE_MISA_B == true"]` that writing 0 raises `IllegalInstruction`. So `misa.B == 0` with B implemented is only reachable when a config opts into `MUTABLE_MISA_B`, and this change does not move that in either direction. All 38 `MUTABLE_MISA_*` assignments in `cfgs/` are `false` today, so none of it is reachable. If the policy is wrong against the text you quoted, the fix belongs in `misa.yaml` and the `MUTABLE_MISA_*` params, and I would rather raise that separately than fold it in here.
