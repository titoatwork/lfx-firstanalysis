# Scoring rubric — temporal holdout pilot (preregistered)

**Pilot:** `temporal-holdout-artifact-c-v1`  
**Scale:** 10 positives (~4.5% of public 223) + 3 negatives.  
**Report:** case table + raw counts only. Do not report p-values or “beats corpus recall.”

## Units

| Unit | Definition |
|------|------------|
| Case | One holdout case id (P01–P10, N01–N03) under one condition |
| Condition | `baseline` or `treatment` |
| Extraction | Zero or more param docs parsed from model output |

## Metrics (all counted per condition)

### 1. Name-agnostic detection recall (positives only)

Gold case is a **hit** if the model emits ≥1 parameter document that is
schema-shaped (`kind: parameter` or clear name+schema) **and** the predicted
class (if any) is not `NEGATIVE`, **or** the name matches gold/alias, **or**
description/quote clearly targets the same architectural choice (scorer uses
name/alias first; description match is **manual review queue only**, not auto-hit).

**Automated scorer:** hit iff exact/alias name match **or** `detected=true` flag
from optional human JSON override file (default none).  
**Primary automated metric for tables:** exact/alias name recall; name-agnostic
column filled only with overrides or left as review-queue count.

### 2. Exact / alias name recall

Hit if any extracted `name` equals gold `name` or an entry in `aliases`
(case-sensitive UPPER_SNAKE after normalization: strip non `[A-Z0-9_]`, upper).

### 3. Classification accuracy

Among positives with a name hit, predicted class (from output `class` field or
heuristic from description keywords WARL/WLRL/RW) matches gold `class` group:

| Gold | Accept |
|------|--------|
| NORM_CSR_WARL | WARL, NORM_CSR_WARL |
| NORM_CSR_RW | CSR_RW, NORM_CSR_RW, RW |
| NORM_DIRECT | DIRECT, NORM_DIRECT |
| WLRL-related DIRECT | DIRECT or WLRL |

If no class field, classification = `unknown` (not correct).

### 4. WARL recall

Among P01–P05 only: fraction with exact/alias name hit.

### 5. Schema validity

Fraction of extracted documents that parse as YAML mapping with `name` and
`schema.type` (or `schema` with `type`). Invalid docs counted but do not credit recall.

### 6. Quote grounding

If sibling evidence JSON/YAML provides `quote`, require whitespace-normalized
substring of:

- baseline: source.txt only  
- treatment: source.txt + context block  

Missing quote → not grounded (counts against grounding rate, not automatic recall fail).

### 7. Type fidelity

Among name hits with gold `schema.type`, extracted `schema.type` equals gold.

### 8. Negative-control false positives

For N01–N03: any extracted parameter document ⇒ FP. Rate = FP cases / 3.

## Human-review queue

Emit `review_queue.json` listing:

- positives with detection signal but name miss  
- name hits with type mismatch  
- negatives with FP  
- treatment cases where context failed leakage re-check  

## Forbidden post-hoc moves

- Editing model raw text before scoring  
- Dropping failed cases  
- Changing gold after seeing outputs  
- Claiming statistical significance on n=10  
