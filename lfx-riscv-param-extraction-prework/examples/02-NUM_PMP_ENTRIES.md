# Example: `NUM_PMP_ENTRIES` (NORM_DIRECT + enum)

**Source:** `spec/std/isa/param/NUM_PMP_ENTRIES.yaml`

---

## UDB content (summary)

| Field | Value |
|-------|--------|
| `name` | `NUM_PMP_ENTRIES` |
| `schema` | integer **enum: [0, 16, 64]** (architecture appearance constraint) |
| `definedBy` | `Sm` |
| `description` | Number of implemented PMP entries; ties to which `pmpaddr*` / `pmpcfg` exist; distinguishes usable entries via related params |

Note in description: odd `pmpcfgN` never exists when XLEN==64; implemented entry may still be read-only zero.

`long_name` on main may still be `TODO` — example of **data quality debt** Part II-style work can help when exporting/reviewing.

---

## Classification intuition

**NORM_DIRECT** — implementation chooses how many PMP entries appear (0/16/64), which then determines CSR presence.

---

## Extraction pitfalls

- Prose discusses PMP regions, locking, matching modes — easy to over-extract adjacent concepts  
- Confusing **NUM_PMP_ENTRIES** vs **NUM_USABLE_PMP_ENTRIES** (related but distinct)  
- Hallucinating enum values outside {0,16,64}  

---

## Why it matters for Part II

Good test of:

1. Distinct param identity (vs neighbors)  
2. Enum-valued schema export  
3. Cross-links to CSR existence rules in description/IDL elsewhere  
