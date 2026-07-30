# The same question, asked of the schema instead of the IDL

`taxonomy.md:43` defines `NORM_CSR_WARL` as the case where "The parameter IS the set
of legal values." That is a statement about a parameter's **shape**, and UnifiedDB
already records the shape, in the JSON schema attached to every parameter. So the
class can be checked without running a model and without reading a line of IDL.

This is a deliberate second route to the question that
[`GOLD-CLASSIFICATION-AUDIT.md`](./GOLD-CLASSIFICATION-AUDIT.md) asks. That audit
asks how the IDL **consumes** a parameter. This one asks what the parameter **is**.
The two share no code, no inputs beyond the gold, and no logic.

```bash
python scripts/audit_param_schema_shapes.py
```

## Method

Only an array can be "the set of legal values", so the scan is exhaustive over the
array-typed parameters and reports the total it drew from. **227 parameters scanned,
15 array-valued.** All 15 fall into three shapes, with nothing left over:

| Shape | Test | Meaning |
|---|---|---|
| `set_enum` | array, enumerated `items`, bounded, `uniqueItems` | a set of legal values from a named domain |
| `set_integer` | array, `items.type: integer` | a set of legal values from an integer range |
| `bitmask` | array, `items.type: boolean`, `minItems == maxItems` | one flag per bit position |

The `bitmask` distinction is the one no keyword or name can make. Every one of these
is "an array attached to a CSR field". Only `items` separates a set of legal values
from a per-bit writability mask, and the two carry opposite classes.

## Result

| Shape | Params | In gold | Gold's labels | Verdict |
|---|---:|---:|---|---|
| `bitmask` | 5 | 5 | `NORM_CSR_RW` x5 | consistent |
| `set_integer` | 1 | 1 | `NORM_CSR_WARL` x1 | consistent |
| `set_enum` | 9 | 7 | `NORM_CSR_WARL` x3, `NORM_DIRECT` x4 | **split on one shape** |

Two of the three shapes are labelled perfectly consistently, 6 entries for 6. The
gold gets the hard case right: `HPM_EVENTS` is an array of integers and is a legal
value set, while `COUNTINHIBIT_EN` and its four siblings are 32-entry boolean masks
and are not. Nothing about the names says that. The schema does, and the gold follows
it.

**One shape carries two labels.** Nine parameters share an identical structure, and
the seven of them present in the gold are split three against four:

```
NORM_CSR_WARL   MSTATUS_FS_LEGAL_VALUES  MSTATUS_VS_LEGAL_VALUES  MTVEC_MODES
NORM_DIRECT     SXLEN  UXLEN  VSXLEN  VUXLEN
not in gold     STVEC_MODES  VSTVEC_MODES
```

## Why this is the finding

The four dissenting parameters are **exactly** the four that the IDL-consumption
audit flagged independently:

```
IDL-consumption method flags : SXLEN  UXLEN  VSXLEN  VUXLEN
schema-shape method flags    : SXLEN  UXLEN  VSXLEN  VUXLEN
identical                    : yes
```

Two routes that disagreed would mean one was wrong. Two routes that agree, sharing
no logic, on the same four names out of 227 candidates, is the evidence. The first
audit showed these four are **consumed** as legal-value sets, by CSR fields whose
`type()` computes read-only against read-write from the parameter's cardinality. This
one shows they **are** legal-value sets, structurally indistinguishable from the three
the gold labels correctly.

The two entries absent from the gold, `STVEC_MODES` and `VSTVEC_MODES`, are the
parameters PR [#2090](https://github.com/riscv/riscv-unified-db/pull/2090) introduced
when it removed the four that the other audit found stale. Same commit, both ends of
the same change.

## Honest limits

- **This method cannot adjudicate a non-array parameter at all.** The gold's 26
  `NORM_CSR_WARL` entries include 9 booleans and 5 integers. A boolean is not a set,
  so under a literal reading of `taxonomy.md:43` none of them can "be" the set of
  legal values. This scan does not claim they are misclassified. It reports that they
  are outside what it can decide, which is the same undecidable region the IDL audit
  measured at 18 of 26.
- The shape test is a **sufficient** condition for being a legal-value set, not a
  necessary one, for the same reason given in the other audit.
- `uniqueItems` is load-bearing in the `set_enum` test. Dropping it would still
  select the same 9 here, but the test is stated as it is checked.
- Counts are re-derived from a UnifiedDB checkout, which is not committed to this
  repository. The gold is pinned by digest in the artifact's `provenance` block.
  Running against `main` and against a topic branch produced identical output.
