# Review queue: dual-model high-confidence “new” names

**Source:** Artifact A multi-model (gpt-4o-mini vs Claude Part I v2), metrics §5.4  
**Rule:** These are **candidates**, not confirmed architectural parameters.  
**Credit:** Spring pipeline [@ishaan-arora-1](https://github.com/ishaan-arora-1) / PRs #1765–#1832.

High-confidence proposed-new names appearing in **both** models (n=9):

| Name | Status |
|------|--------|
| FLEN | candidate; note: often follows from implemented FP extension (derived) |
| IALIGN | candidate; note: derived by `function ialign` in `globals.isa` (non-parameter) |
| ILEN | candidate |
| MISELECT_ACCESS | candidate |
| NUM_PRIVILEGE_MODES | candidate |
| PAUSE_DURATION | candidate |
| RNMI_EXCEPTION_TRAP_HANDLER_ADDRESS | candidate |
| SEED_CSR_ACCESS_CONTROL | candidate |
| SISELECT_MIN_RANGE | candidate |

Agreement alone is **not** a validated review gate: at least `IALIGN` and `FLEN` are derived non-parameters.

## Review card template (fill per name before any upstream PR)

```text
Name:
Spec file / section / quote:
Why implementation-defined (trigger phrase):
Proposed schema type / bounds:
definedBy / extension gate:
Conflict with existing UDB params?:
Decision: accept-as-draft | reject | defer-to-SIG
```

Do **not** bulk-open UDB PRs for this list.
