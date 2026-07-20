# Example: `PHYS_ADDR_WIDTH` (NORM_DIRECT-style)

**Source file on main:** `spec/std/isa/param/PHYS_ADDR_WIDTH.yaml`  
**Why study it:** Clear **implementation-defined width** with numeric schema + IDL requirements tied to `MXLEN` / `Sv32`.

---

## UDB content (summary)

| Field | Value |
|-------|--------|
| `name` | `PHYS_ADDR_WIDTH` |
| `long_name` | Number of bits in a physical address |
| `definedBy` | extension `Sm` |
| `schema` | integer, min 1, max 64 |
| `description` | Implementation-defined size of the physical address space |
| `requirements` | If `MXLEN==32` → width ≤ 34; without Sv32 → width ≤ 32 (with reasons in YAML) |

---

## Classification intuition

| Class | Fit | Why |
|-------|-----|-----|
| **NORM_DIRECT** | Strong | Implementation must choose a width; not “legal values of one WARL enum field” alone |
| NORM_CSR_WARL | Weak | Not primarily a MODE-style legal set |

---

## Extraction pitfalls

- Spec may discuss **physical addresses**, **Sv32/Sv39**, **PMP**, without always saying `PHYS_ADDR_WIDTH`  
- Model may invent related names (`PA_BITS`, `PADDR_WIDTH`) → **naming mismatch** vs UDB  
- NOTE blocks about platforms must not create fake params  

---

## Eval notes

- Gold hit if aligned to `PHYS_ADDR_WIDTH`  
- Good reasoning cites physical address size as implementation-defined and constraints with XLEN/translation  

---

## Export check (Goal 4)

Any regenerated YAML must keep:

- integer schema bounds  
- `definedBy: Sm` (or correct condition if schema evolves)  
- `requirements` IDL that matches current UDB semantics  

Validate with project schema tooling when available (`./do test:schema` style workflows in UDB).
