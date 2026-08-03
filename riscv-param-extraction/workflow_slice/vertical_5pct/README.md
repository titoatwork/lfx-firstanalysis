# 5% vertical slice

End-to-end path for five frozen candidates:

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
- Reject has no `param.yaml` by design.
- Claims limited to fixture contents + validator exit codes.
