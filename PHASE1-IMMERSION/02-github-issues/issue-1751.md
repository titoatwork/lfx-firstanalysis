# Issue #1751 : LFX - Phase 5: Analyze Results and Compare Across Models & UDB

- State: open
- Author: @ishaan-arora-1
- Created: 2026-03-22T23:44:13Z
- Updated: 2026-07-19T13:23:20Z
- URL: https://github.com/riscv/riscv-unified-db/issues/1751
- Labels: 

## Body

## Objective

Compare LLM extraction results against each other and against UDB ground truth. Produce metrics, categorize discrepancies, and identify hallucinations vs. genuine new parameter discoveries.

## Deliverables

| Deliverable | Description |
|---|---|
| `analyze.py` | Analysis script that deduplicates, aligns, and compares results |
| `comparison.json` | Three-way comparison matrix (Model A x Model B x UDB) |
| `metrics.json` | Precision, recall, classification accuracy, inter-model agreement |
| `discrepancies.csv` | Every disagreement categorized by type |

## Analysis Steps

### Step 5.1 — Deduplicate within each model
Multiple chunks may identify the same parameter (especially with overlap). Deduplicate by:
- Exact parameter name match
- Fuzzy excerpt match (>80% token overlap within the same file)
- Keep the highest-confidence instance

### Step 5.2 — Cross-model alignment
Produce a comparison matrix:

| Parameter | Claude | GPT-4o | UDB |
|---|---|---|---|
| MXLEN | Found, NORM_DIRECT | Found, NORM_DIRECT | Exists |
| (new) XYZ_THING | Found | Not found | Not in UDB |

### Step 5.3 — Compute metrics (per model vs UDB)
- **Recall**: How many of the 185 UDB params did the LLM find? (Target: >70%)
- **Precision**: How many LLM findings are real params? (vs. hallucinations)
- **Classification accuracy**: For matched params, correct class assignment rate
- **Inter-model agreement**: For shared findings, classification agreement rate

### Step 5.4 — Categorize every discrepancy
Each goes into one of:
- **LLM hallucination** — LLM said it's a parameter but it isn't (false positive)
- **UDB gap** — LLM found a real parameter that UDB doesn't have yet (true positive, new)
- **UDB recall miss** — UDB has it, LLM missed it (false negative)
- **Classification disagreement** — Found by both, classified differently
- **Naming mismatch** — Same parameter, different name

## Acceptance Criteria
- [ ] Deduplication produces a clean, unique parameter list per model
- [ ] All discrepancies categorized with type and explanation
- [ ] Recall against UDB >= 70% for at least one model
- [ ] Metrics report is clear and actionable
- [ ] Hallucinations flagged for use as negative examples in Phase 6

