# Issue #1747 : LFX - Phase 1: Build the Ground Truth Map from UDB Parameters

- State: open
- Author: @ishaan-arora-1
- Created: 2026-03-22T23:42:56Z
- Updated: 2026-03-22T23:53:30Z
- URL: https://github.com/riscv/riscv-unified-db/issues/1747
- Labels: 

## Body

## Objective

Create a machine-readable catalog of all 185 existing UDB architectural parameters, enriched with schema analysis, CSR cross-references, heuristic classifications, and candidate spec text locations. This catalog serves as both the training data for LLM prompts and the validation benchmark for evaluating LLM extraction accuracy.

## Deliverables

| Deliverable | Description |
|---|---|
| `ground_truth.json` | Full structured data for all 185 parameters: name, description, value type analysis, definedBy conditions, CSR cross-references, classification with confidence and reasoning |
| `spec_mappings.json` | For each parameter, the top candidate locations in the spec `.adoc` files with relevance scores, line numbers, and text context |
| `parameters_catalog.csv` | Spreadsheet-ready catalog (19 columns) for review |
| `phase1_report.txt` | Human-readable report with statistics and per-parameter breakdown |
| `udb_param_names.txt` | Flat list of 185 parameter names for inclusion in LLM prompts |

## Approach

### Step 1.1 — Export UDB parameters to structured JSON
- Read all `spec/std/isa/param/*.yaml` files (excluding MOCK fixtures)
- Derive value type programmatically from JSON Schema (boolean -> binary, integer+enum -> enum, integer+min/max -> range, array -> set/bitmask, oneOf+when -> conditional)
- Parse complex `definedBy` structures (allOf, anyOf, parameter conditions)
- Cross-reference all CSR YAML files to find IDL code (`sw_write()`, `type()`, `reset_value()`, `legal?()`) that references each parameter

### Step 1.2 — Map parameters to spec text locations
- Search all 74 `.adoc` files (52,602 lines) using multi-strategy keyword matching
- Search strategies: exact parameter name, CSR name in backticks, description keywords, WARL+CSR proximity patterns, name segment matching
- Score and rank candidate lines; extract surrounding context
- Exclude non-normative content (NOTE/TIP/WARNING blocks)

### Step 1.3 — Classify every UDB parameter
Heuristic classification into:
- **NORM_DIRECT** — Directly configurable, not CSR-controlled (e.g., `MXLEN`, `NUM_PMP_ENTRIES`)
- **NORM_CSR_WARL** — Legal values of a WARL CSR field (e.g., `MTVEC_MODES`, `SATP_MODE_BARE`)
- **NORM_CSR_RW** — Controls whether a CSR field is RO/RW (e.g., `MUTABLE_MISA_C`, `M_MODE_ENDIANNESS`)
- **SW_RULE** — Software-deterministic with correct fencing (e.g., `HW_MSTATUS_FS_DIRTY_UPDATE`)

## Acceptance Criteria
- [ ] All 185 non-MOCK parameters exported with complete metadata
- [ ] Value types verified against actual YAML schemas (100% match)
- [ ] CSR cross-references verified against actual CSR YAML files
- [ ] >= 95% of parameters have at least one spec text candidate match
- [ ] Classification confidence breakdown: >= 75% high confidence
- [ ] CSV catalog produced and ready for review

