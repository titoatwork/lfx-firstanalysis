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

### 0. Infrastructure failures (not model metrics)

If a result file is missing, or marked `# INFRA_ERROR:` / `*.status.json` with
`ok: false`, the case is **excluded** from model metrics. It is **not** scored
as a model zero. Report `infra_or_missing` separately.

### 1. Name-agnostic detection recall (positives only)

**Automated hit** if any of:

1. Exact/alias name match (see §2), or  
2. ≥1 document that validates against vendored `param_schema.json` **and**
   shares ≥2 content keywords with gold `description`/`long_name`, or  
3. Schema-valid document with matching `schema.type` and ≥1 shared keyword.

Keywording: alphanumeric tokens length ≥4, stopwords stripped. This is a weak
signal for “something parameter-like about the right concept,” not a claim of
correct naming.

### 2. Exact / alias name recall

Hit if any extracted `name` equals gold `name` or an entry in `aliases`
(after normalization: strip non `[A-Z0-9_]`, upper).

### 3. Classification accuracy

**Denominator = all scored positives** (not only name hits). A name-miss or
missing/unknown class counts as **incorrect**.

Among name hits, predicted `class` must match gold group:

| Gold | Accept |
|------|--------|
| NORM_CSR_WARL | WARL, NORM_CSR_WARL |
| NORM_CSR_RW | CSR_RW, NORM_CSR_RW, RW |
| NORM_DIRECT | DIRECT, NORM_DIRECT, WLRL |

### 4. WARL recall

Among scored P01–P05: fraction with exact/alias name hit.

### 5. Schema validity

Fraction of extracted documents that **validate** against vendored UDB
`challenge/schema/param_schema.json` via jsonschema Draft7 (+ refs). Not a
two-field name/type presence check.

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
