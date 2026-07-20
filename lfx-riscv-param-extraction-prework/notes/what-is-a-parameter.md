# What is an architectural parameter? (UDB-centric)

---

## 1. Definition (working)

An **architectural parameter** is an implementation-defined quantity or choice that:

1. Is **implied or constrained by RISC-V ISA specifications** (privileged and/or unprivileged), and  
2. Must be **fixed (or constrained) by a concrete hart/platform implementation**, and  
3. Can be represented as structured data: **name + value domain + defining conditions**.

It is **not**:

- An instruction opcode/mnemonic alone (`ADD`, `JAL`)  
- Arbitrary microarchitectural performance trivia with no ISA wording  
- Text that appears **only** in non-normative NOTE blocks (unless taxonomy marks `NON_NORM`)  
- A full CSR field **value at runtime** (that is state); parameters often describe **which values are legal** or **whether a field exists / is writable**

---

## 2. UDB representation

**Path:** `spec/std/isa/param/<NAME>.yaml`  
**Schema:** `spec/schemas/param_schema.json`

### Required-style fields (schema)

| Field | Role |
|-------|------|
| `$schema` | `param_schema.json#` |
| `kind` | `parameter` |
| `name` | Stable id, e.g. `PHYS_ADDR_WIDTH` |
| `long_name` | Short human title (many still `TODO` on main—data debt) |
| `description` | Spec-facing explanation + valid values narrative |
| `definedBy` | When the parameter exists (extension / conditions) |
| `schema` | JSON Schema for the parameter’s **value type** |

### Optional

| Field | Role |
|-------|------|
| `requirements` | Extra constraints (`idl()`, if/then on other params) |
| `$source` | Provenance |

---

## 3. Value shapes (from Spring analysis + live files)

| Shape | JSON Schema pattern | Example |
|-------|---------------------|---------|
| Binary / flag | boolean or 0/1 enum | many `*_EN` style |
| Range integer | `type: integer` + min/max | `PHYS_ADDR_WIDTH` 1..64 |
| Enum integer | `enum: [0, 16, 64]` | `NUM_PMP_ENTRIES` |
| Set / list | `type: array` + item enums | `MTVEC_MODES` ∈ {[0],[1],[0,1]} |
| Complex conditional | `requirements` + `definedBy` allOf/anyOf | `HPM_EVENTS` tied to counters |

---

## 4. Taxonomy classes (Spring) — decision guide

| Class | Ask | Example |
|-------|-----|---------|
| **NORM_DIRECT** | Must the implementation pick this even when no CSR field encodes the choice as WARL set? | `NUM_PMP_ENTRIES`, `PHYS_ADDR_WIDTH` |
| **NORM_CSR_WARL** | Is this the **set of legal values** of a WARL field? | `MTVEC_MODES` |
| **NORM_CSR_RW** | Is this about **read-only vs read-write** / mutability? | access-style params |
| **SW_RULE** | If software follows the rules, is the outcome determined? | dirty-bit update policies |
| **NON_ISA** | Platform reset vectors, etc. | outside pure ISA param set |
| **NON_NORM** | Only in NOTE/TIP? | exclude from normative gold |
| **DOC_RULE** | Reporting/documentation only? | |
| **UNKNOWN** | Needs human | |

**Hard class:** `NORM_CSR_WARL` — Spring V2 recall only ~**50%**. Legal-value sets are easy for models to miss or confuse with runtime behavior.

---

## 5. Extraction output (Spring JSON shape)

Useful as intermediate form **before** UDB YAML:

```json
{
  "excerpt": "exact clause from spec",
  "line_number": 478,
  "parameter_name": "MTVEC_MODES",
  "existing_udb_name": "MTVEC_MODES",
  "class": "NORM_CSR_WARL",
  "value_type": "set",
  "confidence": "high",
  "reasoning": "one sentence"
}
```

Eval must align names to UDB (exact / fuzzy / one-to-many groups).

---

## 6. Evaluation vocabulary

| Term | Meaning |
|------|---------|
| **Recall** | Of gold params, what fraction did we find? |
| **Adjusted recall** | After legitimate one-to-many / alignment rules |
| **Precision** | Of predicted params, what fraction are real? |
| **Hallucination** | Predicted, not real |
| **UDB gap** | Real param missing from UDB gold |
| **Naming mismatch** | Same concept, different string |

Part II Goal 1c explicitly: enhance **parameter recall** vs UDB YAML.

---

## 7. From row → UDB YAML (Goal 4 sketch)

```text
reviewed extraction row
  → normalize NAME
  → draft description from excerpt + surrounding context (human edit)
  → set definedBy from extension/CSR context
  → build JSON Schema for legal values
  → add requirements if IDL/conditions known
  → validate param_schema.json
  → PR under spec/std/isa/param/
```

Never bulk-PR unaudited model output.

---

## 8. Related UDB pieces (context)

| Path | Why |
|------|-----|
| `spec/std/isa/csr/` | CSR fields; WARL; IDL references to params |
| `spec/std/isa/ext/` | Extensions for `definedBy` |
| `cfgs/*.yaml` | Configurations consuming params |
| `backends/` | Generators (secondary for Day 1) |
| `ext/riscv-isa-manual` | Prose source for extraction |
| `AGENTS.md` | How automated agents should work in-repo |
