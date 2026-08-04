# 5% vertical slice

End-to-end path for eight frozen candidates:

```
spec evidence → candidate → duplicate decision → human-review record
             → validated UDB YAML (if approved) → PR-ready package shape
```

## Candidates

| ID | Class | Decision | Point of the case |
|----|-------|----------|-------------------|
| C01 | NORM_DIRECT | approve_export | CACHE_BLOCK_SIZE, multi-ext `definedBy` |
| C02 | NORM_DIRECT | approve_export | NUM_PMP_ENTRIES |
| C03 | NORM_CSR_WARL | approve_export | true WARL legal-set parameter |
| C04 | NORM_CSR_WARL | approve_export | ASIDLEN → ASID_WIDTH rename/dedup |
| C05 | CSR_FIELD_NOT_PARAM | **reject** | MODE encoding table ≠ parameter |
| C06 | DERIVED_NOT_PARAM | **reject** | `IALIGN`, derived by `function ialign` |
| C07 | DERIVED_NOT_PARAM | **reject** | `FLEN`, same verdict at both pins, different evidence |
| C08 | UNRESOLVED | **needs_more_evidence** | `ILEN`, used everywhere, defined nowhere |

C06 to C08 were added 2026-08-05. All three are candidates that two models
proposed as new parameters at high confidence and agreed on, so they are real
failures of dual-model agreement rather than fixtures written to be failed.

**C07 is the case worth reading.** `FLEN` is derived at the corpus pin and on
`main`, so the disposition never moves. The *evidence* moves: `U32 FLEN = 64;`
with the derivation in a comment at the pin, a config-dependent global on `main`
after [#1813](https://github.com/riscv/riscv-unified-db/pull/1813). This project
published the corpus-pin reading as a fact about UDB. An evidence type is a
claim about a tree, so it is not checkable unless the tree is named, and the
validator now rejects an `evidence_type` that arrives without its pin.

**C08 is the one that should not be resolved.** A rubric that never returns
"unresolved" on a real candidate is not being applied honestly. `ILEN` was left
open on 2026-07-28 and is still open after re-checking both revisions under a
corrected search, so the abstention has survived a deliberate attempt to close
it. `needs_more_evidence` cases must list what evidence would settle them,
which is what separates an abstention from a way of never deciding.

## Layout per candidate

- `source.txt`, exact excerpt context + source pin
- `review_envelope.yaml`, evidence, classification, duplicate decision, reviewer
- `param.yaml`: **only** if `approve_export`; UDB-schema-valid; no review keys

## Reproduce

```bash
python workflow_slice/vertical_5pct/scripts/validate_slice.py
# or full package:
python workflow_slice/scripts/ci_slice_check.py
```

## Rules

- No bulk upstream parameter PR from this tree.
- Reject has no `param.yaml` by design, and neither does `needs_more_evidence`.
- Every `evidence_type` carries the commit it was determined against.
- Claims limited to fixture contents + validator exit codes.
