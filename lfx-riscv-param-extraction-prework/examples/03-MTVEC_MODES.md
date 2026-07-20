# Example: `MTVEC_MODES` (NORM_CSR_WARL-style)

**Source:** `spec/std/isa/param/MTVEC_MODES.yaml`  
**Why critical:** This is the **hard class** Spring struggled with (~50% WARL recall in V2).

---

## UDB content (summary)

| Field | Value |
|-------|--------|
| `name` | `MTVEC_MODES` |
| `long_name` | Modes supported by `mtvec.MODE` |
| `definedBy` | `Sm` |
| `schema` | array of integers enum `{0,1}`, minItems 1, maxItems 2, unique |
| Modes | `0` Direct; `1` Vectored (async interrupt → BASE+4×cause) |
| Semantics | If only one mode → `mtvec.MODE` read-only; else read-write |
| `requirements` | If `MTVEC_ACCESS` is `ro` → `MTVEC_MODES` size must be 1 |

---

## Classification intuition

| Class | Fit |
|-------|-----|
| **NORM_CSR_WARL** | Strong — legal mode set for `mtvec.MODE` |
| NORM_CSR_RW | Related via `MTVEC_ACCESS` but modes themselves are the value set |
| NORM_DIRECT | Weaker — tightly coupled to CSR field behavior |

---

## Extraction pitfalls (why models fail)

1. Spec describes Direct vs Vectored behavior **without** listing “parameter MTVEC_MODES”  
2. Models emit runtime behavior (“when interrupt occurs…”) instead of **legal set**  
3. Confuse with `stvec` / VS-mode analogs → wrong name  
4. Miss coupling to `MTVEC_ACCESS` (conditional requirements)  
5. One-to-many: similar sentences for multiple `*TVEC_MODES` params  

---

## Part II leverage

Improving extraction/classification on **WARL legal-value parameters** is high-ROI relative to Spring V2.  
Few-shot examples should include:

- Positive: mode list + RO if singleton  
- Negative: narrative of trap entry that is **not** a new param  
- Negative: NOTE-only commentary  

---

## Export check

Array schema + uniqueItems + link to `MTVEC_ACCESS` requirement must survive round-trip generation.
