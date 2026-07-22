# All LFX-titled issues/PRs on riscv-unified-db

Total: 16

## #1747 — LFX - Phase 1: Build the Ground Truth Map from UDB Parameters
- State: open | @ishaan-arora-1 | https://github.com/riscv/riscv-unified-db/issues/1747
- Updated: 2026-03-22T23:53:30Z

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

---

## #1748 — LFX - Phase 2: Design Parameter Taxonomy & LLM Prompts
- State: open | @ishaan-arora-1 | https://github.com/riscv/riscv-unified-db/issues/1748
- Updated: 2026-03-22T23:53:52Z

## Objective

Formalize the parameter classification taxonomy into a precise, documented reference, and design the LLM prompt architecture that will drive parameter extraction from the RISC-V specification text.

## Deliverables

| Deliverable | Description |
|---|---|
| `taxonomy.md` | Formal taxonomy document defining all parameter classes and value types with clear definitions, rules, and examples |
| `system_prompt.txt` | System prompt template (~800 tokens) defining the LLM's role and task |
| `examples.json` | 5-6 positive + 3-4 negative few-shot examples with full JSON structure |
| `run_prompt.py` | Prompt assembler script that combines system prompt + examples + parameter name list + spec chunk into a complete prompt |

## Taxonomy Design

Formalize and document these classification categories (refined from Phase 1 heuristics):

| Class | Definition | Example |
|---|---|---|
| `NORM_DIRECT` | Normative, directly configurable — implementation must choose, not controlled by any CSR field | `NUM_PMP_ENTRIES`, `PHYS_ADDR_WIDTH`, `MXLEN` |
| `NORM_CSR_WARL` | Normative, CSR WARL-controlled — the parameter is the set of legal values for a WARL CSR field | `MTVEC_MODES`, `MSTATUS_FS_LEGAL_VALUES` |
| `NORM_CSR_RW` | Normative, CSR read-write behavior — whether a CSR or field is read-only vs read-write | `MTVEC_ACCESS`, `MUTABLE_MISA_C` |
| `SW_RULE` | Software-deterministic — appears impl-defined, but outcome is determinate if SW follows spec rules | `HW_MSTATUS_FS_DIRTY_UPDATE` |
| `NON_ISA` | Non-ISA / platform — platform-level, not architectural | Reset vector, NMI vector |
| `NON_NORM` | Non-normative — in NOTE or informative block | — |
| `DOC_RULE` | Documentation rule — describes reporting, not architectural behavior | — |
| `UNKNOWN` | Cannot be confidently classified | — |

## Prompt Architecture — Three-Layer Design

1. **System prompt** (~800 tokens): Role definition, task definition, output format, condensed taxonomy
2. **Few-shot examples** (~2,000-3,000 tokens): Positive examples (one per class) + negative examples (non-normative text, CSR behavior that isn't a parameter, "may" used as permission not optionality, behavior controlled by a CSR field)
3. **Spec chunk** (variable, up to ~40K tokens): The actual specification text to analyze

### Key Design Decisions
- Single-pass extraction + classification (not two separate passes) to preserve context
- Mandatory `reasoning` field in output to reduce hallucinations and aid review
- Known UDB parameter names included in prompt for name matching
- Structured JSON output with enforced schema

## Acceptance Criteria
- [ ] Taxonomy document is complete with clear definitions, disambiguation rules, and examples for every class
- [ ] System prompt produces valid, parseable JSON output on test input
- [ ] Few-shot examples cover every classification category
- [ ] Negative examples cover the key false-positive patterns (NOTE blocks, CSR field behavior, permission "may")
- [ ] Prompt assembler correctly combines all layers and respects context window limits

---

## #1749 — LFX - Phase 3: Implement Spec Text Chunking Strategy
- State: open | @ishaan-arora-1 | https://github.com/riscv/riscv-unified-db/issues/1749
- Updated: 2026-03-22T23:48:59Z

## Objective

Split the 52,602-line RISC-V specification into semantically coherent chunks that fit within LLM context windows while preserving the context needed for parameter identification.

## Deliverables

| Deliverable | Description |
|---|---|
| `chunker.py` | Script that parses AsciiDoc section structure and produces chunks with metadata |
| `chunks/` directory | Numbered chunk files with source file, line range, and section headings |

## Chunking Rules

1. **Never split within a CSR section** — each CSR description (from `====` heading to next `====`) is atomic, since WARL parameter identification requires the full field description + bytefield + behavioral paragraphs together
2. **Split at `===` (3rd-level) or `====` (4th-level) AsciiDoc headings** — natural semantic boundaries
3. **Target chunk size: ~2,500-3,500 lines** (~35K-45K tokens), leaving room for prompt layers within a 128K context window
4. **Include overlap** — the previous section's heading and first paragraph as context
5. **Small files go whole** — any file under 2,000 lines is processed as a single chunk

### Spec File Sizes (actual line counts)

| File | Lines | Est. Chunks |
|---|---|---|
| `scalar-crypto.adoc` | 5,590 | 2-3 (low parameter density — mostly instruction descriptions) |
| `v-st-ext.adoc` | 5,396 | 2-3 |
| `vector-crypto.adoc` | 4,966 | 2 (low parameter density) |
| `machine.adoc` | 3,629 | 2 (highest parameter density) |
| `b-st-ext.adoc` | 3,375 | 1-2 (low parameter density) |
| `hypervisor.adoc` | 2,932 | 1-2 |
| `supervisor.adoc` | 2,630 | 1-2 |
| `zc.adoc` | 2,587 | 1-2 |
| Remaining 66 files | <2,000 each | 1 each |

**Total estimated: ~50-60 chunks across 74 files.**

## Acceptance Criteria
- [ ] No chunk splits within a CSR section
- [ ] All chunks respect the target size range (+/- 20%)
- [ ] Overlap context is included at chunk boundaries
- [ ] Chunk metadata (source file, line range, section headings) is complete
- [ ] All 74 spec `.adoc` files are covered

---

## #1750 — LFX - Phase 4: Build and Run the LLM Extraction Pipeline
- State: open | @ishaan-arora-1 | https://github.com/riscv/riscv-unified-db/issues/1750
- Updated: 2026-06-14T14:04:04Z

## Objective

Build the extraction pipeline and run it against at least 2 different LLMs to collect structured parameter identification results from across the full RISC-V specification.

## Deliverables

| Deliverable | Description |
|---|---|
| `extract.py` | Extraction script that assembles prompts, calls LLM APIs, and parses structured JSON responses |
| `results/{model}/` | Per-chunk JSON results for each LLM |
| `all_results_{model}.json` | Merged results per model |

## LLM Selection (at least 2, recommend 3)

| Model | Rationale |
|---|---|
| **Claude** (Anthropic) | Strong structured reasoning, large context (200K), excellent taxonomy adherence |
| **GPT-4o** (OpenAI) | Different training data, strong JSON extraction, good baseline comparison |
| **Gemini 2.5 Pro** (Google) | 1M+ context allows processing entire files without chunking — useful cross-check |

## Pipeline Design

For each spec chunk:
1. Assemble the full prompt: system + examples + UDB parameter name list + chunk text
2. Call LLM API with `temperature=0` for deterministic extraction
3. Parse JSON response and validate against expected schema
4. Annotate each result with source chunk metadata (file, line offset)
5. Store raw response + parsed results

### Expected Output Per Extracted Parameter
```json
{
  "excerpt": "The exact sentence or clause from the spec",
  "line_number": 478,
  "parameter_name": "MSTATUS_XPP_LEGAL_VALUES",
  "existing_udb_name": "null or matching UDB param name",
  "class": "NORM_CSR_WARL",
  "value_type": "set",
  "confidence": "high|medium|low",
  "reasoning": "One sentence explaining why"
}
```

### Execution Strategy
- Pilot on `machine.adoc` first (highest parameter density) to validate prompts before full run
- Sequential chunk processing with configurable delays for rate limiting
- Retry logic: if JSON parsing fails, retry once with format-correction follow-up
- Log token usage per call for cost tracking
- Estimated cost: ~$5-15 per full run per model

## Acceptance Criteria
- [ ] Pipeline successfully processes all chunks for at least 2 LLMs
- [ ] All results are valid, parseable JSON matching the expected schema
- [ ] Pilot run on `machine.adoc` reviewed before scaling to full spec
- [ ] Token usage and cost logged per call
- [ ] Raw API responses preserved for debugging

---

## #1751 — LFX - Phase 5: Analyze Results and Compare Across Models & UDB
- State: open | @ishaan-arora-1 | https://github.com/riscv/riscv-unified-db/issues/1751
- Updated: 2026-07-19T13:23:20Z

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

---

## #1752 — LFX - Phase 6: Iteratively Refine Prompts Based on Analysis
- State: open | @ishaan-arora-1 | https://github.com/riscv/riscv-unified-db/issues/1752
- Updated: 2026-03-22T23:44:27Z

## Objective

Use the discrepancies and metrics from Phase 5 to systematically improve the LLM prompts, then re-run extraction and re-analyze. Repeat until convergence.

## Deliverables

| Deliverable | Description |
|---|---|
| `prompts/v2/`, `prompts/v3/` | Versioned prompt files with changelogs |
| Updated `results/` and `analysis/` | Re-run results and metrics for each iteration |

## Refinement Strategy

### Iteration 1 -> 2
- Add 3-5 **hallucination examples** as negative few-shot examples (from Phase 5 false positives — things that don't fit any valid category or fall into the wrong one)
- Add 3-5 **missed UDB parameters** as additional positive examples to improve recall
- If a specific classification is consistently wrong (e.g., LLMs confuse `NORM_CSR_WARL` with `NORM_DIRECT`), add a disambiguation paragraph to the system prompt
- If hallucinations cluster at the end of long chunks (context-size-dependent errors), reduce chunk size

### Iteration 2 -> 3
- Fine-tune taxonomy if certain categories are consistently ambiguous
- If one model is clearly better, weight its results more heavily in the merged output
- Add any remaining missed parameters as examples

## Convergence Criteria

Stop iterating when:
- Recall against UDB > 80%
- Inter-model agreement on classification > 85%
- New hallucinations per iteration < 5%

## Acceptance Criteria
- [ ] At least 2 refinement iterations completed
- [ ] Each iteration has versioned prompts with documented changes
- [ ] Metrics improve monotonically across iterations
- [ ] Final recall > 80% against UDB
- [ ] Convergence criteria met or clearly justified why not

---

## #1753 — LFX - Phase 7: Generate the Final Parameter Spreadsheet
- State: open | @ishaan-arora-1 | https://github.com/riscv/riscv-unified-db/issues/1753
- Updated: 2026-03-22T23:54:07Z

## Objective

Produce the final deliverable spreadsheet consolidating all confirmed parameters — both existing UDB parameters and newly discovered ones — with the classification, spec location, and metadata.

## Deliverables

| Deliverable | Description |
|---|---|
| `generate_spreadsheet.py` | Script that merges refined results into the final spreadsheet |
| `parameters.csv` | CSV format for programmatic use |
| `parameters.xlsx` | Excel format for presentation and review |

## Spreadsheet Columns

| Column | Description | Source |
|---|---|---|
| `adoc_file` | The `.adoc` file containing the parameter | From chunk/spec metadata |
| `line_number` | Line number of the excerpt | From LLM output, adjusted by chunk offset |
| `excerpt` | Verbatim spec text excerpt that mentions the parameter | From LLM output |
| `parameter_name` | UDB name if it exists, else a new name following UDB conventions | Matched against `udb_param_names.txt` |
| `named` | Whether this parameter already has a name in UDB (yes/no) | Cross-referenced against Phase 1 ground truth |
| `class` | Classification of the parameter (see taxonomy below) | From LLM + inter-model agreement |
| `value_type` | Type of the parameter value (see types below) | From LLM output |
| `confidence` | Confidence level from LLM + inter-model agreement | high/medium/low |
| `notes` | Reviewer notes (blank initially) | — |

### Classification Taxonomy

| Class ID | Definition |
|---|---|
| `NORM_DIRECT` | Normative, directly configurable — implementation must choose a value; not controlled by any CSR field |
| `NORM_CSR_WARL` | Normative, CSR WARL-controlled — the parameter is the set of legal values for a WARL CSR field |
| `NORM_CSR_RW` | Normative, CSR read-write behavior — whether a CSR field is read-only vs read-write |
| `SW_RULE` | Software-deterministic — appears impl-defined, but outcome is determinate if SW follows spec rules |
| `NON_ISA` | Non-ISA / platform — platform-level, not architectural |
| `NON_NORM` | Non-normative — in a NOTE or informative block |
| `DOC_RULE` | Documentation rule — describes how something should be documented/reported |
| `UNKNOWN` | Cannot be confidently classified |

### Value Types

| Type | Definition |
|---|---|
| `binary` | Exactly 2 choices (boolean or 2-value enum) |
| `enum` | Finite set of 3+ discrete values |
| `range` | Continuous integer range with min/max bounds |
| `set` | Subset selection from a fixed universe of values |
| `bitmask` | Fixed-length boolean array (one bit per feature) |
| `value` | Single unconstrained value |

## Naming Convention for New (Unnamed) Parameters

Follow UDB's existing `ALL_CAPS_WITH_UNDERSCORES` style:
- Prefix with CSR name for CSR-controlled params (e.g., `MTVEC_BASE_ALIGNMENT`)
- Prefix with `TRAP_ON_` for trap behavior params
- Prefix with `REPORT_` for reporting behavior params
- Use descriptive suffixes that capture the implementation choice

## Acceptance Criteria
- [ ] All confirmed parameters from refined extraction included
- [ ] Columns cover: file, line, excerpt, name, named, class, value type, confidence
- [ ] New parameter names follow UDB naming conventions
- [ ] Both CSV and XLSX formats generated
- [ ] Spreadsheet reviewed before proceeding to tagging

---

## #1754 — LFX - Phase 8: Insert Parameter Tags into Spec & Create PR
- State: open | @ishaan-arora-1 | https://github.com/riscv/riscv-unified-db/issues/1754
- Updated: 2026-03-22T23:54:22Z

## Objective

Insert `[#param:...]` tags into the `riscv-isa-manual` specification AsciiDoc files for every confirmed parameter from the final spreadsheet, and create a GitHub Pull Request for review.

## Deliverables

| Deliverable | Description |
|---|---|
| `insert_tags.py` | Script that reads the spreadsheet and inserts tags into `.adoc` files |
| Modified `.adoc` files | Spec files with `[#param:NAME]#excerpt#` tags inserted |
| GitHub PR | Pull request to `riscv-isa-manual` with all tagged parameters |

## Tag Format

Following the existing `[#norm:...]` convention already used in the spec (~1,361 normative tags across 31 files). Example of the existing format:

```
[#norm:misa_acc]#The `misa` CSR is a *WARL* read-write register#
```

New parameter tags will follow the same pattern:

```
[#param:MTVEC_MODES]#An implementation can choose to subset the delegatable traps#
```

For newly discovered parameters with new names:
```
[#param:MSTATUS_FS_RDONLY_WHEN_NO_F]#FS may optionally be read-only zero.#
```

**Note**: Zero `[#param:...]` tags currently exist in the spec — this PR will introduce them for the first time.

## Implementation

1. Read the final spreadsheet (only rows with `confidence >= medium`)
2. For each parameter, locate the exact line in the `.adoc` file
3. Wrap the excerpt with `[#param:NAME]#...#`
4. Handle edge cases:
   - Excerpt already has a `[#norm:...]` tag -> place adjacent per spec convention
   - Excerpt spans multiple lines -> tag only the key sentence
   - Multiple parameters on the same line -> multiple tags
5. Validate all modified files with `asciidoctor` to ensure no AsciiDoc breakage

## PR Structure

- Branch: `param-tags-v1`
- PR description includes:
  - Methodology summary
  - Statistics (N parameters tagged, M new, K existing)
  - Link to the spreadsheet
  - Classification breakdown

## Future Work

Adding newly discovered parameters as YAML files in `spec/std/isa/param/` is a natural follow-on after this PR is reviewed and the parameter list is confirmed. This phase focuses on spec tagging; UDB integration will be a subsequent effort.

## Acceptance Criteria
- [ ] All confirmed parameters tagged in the correct `.adoc` files
- [ ] Tag format follows the existing `[#norm:...]` convention
- [ ] No AsciiDoc rendering errors introduced
- [ ] PR description is comprehensive and links to all supporting artifacts
- [ ] PR reviewed and approved before merge

---

## #1765 — LFX Phase 1: Ground truth map for architectural parameter extraction
- State: open | @ishaan-arora-1 | https://github.com/riscv/riscv-unified-db/pull/1765
- Updated: 2026-05-25T21:52:06Z

## Summary

- Adds scripts and data that catalog all 185 UDB architectural parameters with schema analysis, CSR cross-references, heuristic classifications, and candidate spec text locations
- This is the foundation for LLM-based parameter extraction from the RISC-V privileged and unprivileged specifications (see #1747)
- Part of the LFX project to systematically identify and tag architectural parameters in the spec

## What's included

### Scripts (`param_extraction/scripts/`)

| Script | Purpose |
|---|---|
| `export_udb_params.py` | Reads all 185 `spec/std/isa/param/*.yaml` files (excluding 22 MOCK fixtures), analyzes JSON Schema structure, cross-references CSR IDL code for `sw_write()`/`type()`/`reset_value()` references, and classifies each parameter |
| `map_params_to_spec.py` | Searches all 74 spec `.adoc` files (52,602 lines) for text related to each parameter using multi-strategy keyword matching (exact name, CSR backtick refs, description keywords, WARL proximity patterns) |
| `generate_report.py` | Produces the CSV catalog, text report, and flat parameter name list |

### Data outputs (`param_extraction/data/`)

| File | Description |
|---|---|
| `ground_truth.json` | Full structured data for all 185 parameters: name, description, value type, definedBy, CSR cross-references, classification with confidence and reasoning |
| `spec_mappings.json` | Top candidate spec text locations per parameter with relevance scores, line numbers, and context |
| `parameters_catalog.csv` | 19-column spreadsheet-ready catalog |
| `phase1_report.txt` | Human-readable report with statistics and per-parameter breakdown |
| `udb_param_names.txt` | Flat list of 185 parameter names (for inclusion in LLM prompts in later phases) |

## Key results

| Metric | Value |
|---|---|
| Parameters cataloged | 185 (22 MOCK fixtures excluded) |
| Classification: NORM_DIRECT | 102 (55%) — directly configurable, not CSR-controlled |
| Classification: NORM_CSR_RW | 55 (30%) — controls RO/RW behavior of CSR fields |
| Classification: NORM_CSR_WARL | 26 (14%) — legal values of WARL CSR fields |
| Classification: SW_RULE | 2 (1%) — software-deterministic with correct fencing |
| High-confidence classifications | 150 (81%) |
| Value type: binary | 111 (60%), enum: 36 (19%), range: 12 (6%) |
| Parameters with CSR cross-references | 94 (51%) |
| Parameters mapped to spec text | 183/185 (98%) |
| Strong spec matches (score >= 5) | 161 (87%) |

## How to run

```bash
# Requires PyYAML (pip install pyyaml)
# Requires ext/riscv-isa-manual submodule to be initialized

python3 param_extraction/scripts/export_udb_params.py
python3 param_extraction/scripts/map_params_to_spec.py
python3 param_extraction/scripts/generate_report.py
```

## Test plan

- [x] All 185 non-MOCK parameters exported with complete metadata
- [x] Value types verified against actual YAML schemas (100% match)
- [x] CSR cross-references verified against actual CSR YAML files
- [x] 98% of parameters have at least one spec text candidate match
- [x] 81% high-confidence classifications (target was >= 75%)
- [x] CSV catalog and JSON outputs are consistent (all 185 rows match)
- [x] No duplicate parameter names
- [x] All source YAML files exist on disk
- [x] Scripts run cleanly end-to-end with no errors

Closes #1747

---

## Update — review tweaks applied

Went back through the review and pushed the two small `generate_report.py` cleanups:

- Added `encoding="utf-8"` to the `open(names_path, "w")` call so the names file is written with an explicit text encoding instead of relying on the platform default.
- Added an `if not rows: return` guard before the CSV write so we don't blow up on `rows[0].keys()` if there's nothing to write.

No data regen for this phase — the catalog files are byte-identical for any non-empty dataset (UTF-8 is already the default on Linux/macOS and `rows` is never empty for real input).


---

## #1766 — LFX Phase 2: Parameter taxonomy and LLM prompt architecture
- State: open | @ishaan-arora-1 | https://github.com/riscv/riscv-unified-db/pull/1766
- Updated: 2026-05-25T21:53:26Z

## Summary

Design and implement the formal parameter classification taxonomy and LLM prompt architecture for extracting architectural parameters from the RISC-V specification. Builds on Phase 1 (#1765).

- **Formal taxonomy** (`taxonomy.md`): 8 parameter classes with precise definitions, disambiguation rules, and a decision tree
- **System prompt** (`system_prompt.txt`): ~940 token prompt defining role, task, condensed taxonomy, critical rules, and strict JSON output schema
- **Few-shot examples** (`examples.json`): 6 positive + 4 negative examples from real spec text covering all normative classification classes and key false-positive patterns
- **Prompt assembler** (`run_prompt.py`): CLI tool with 3 modes — `assemble`, `chunk`, and `estimate` — for building context-aware prompts across different LLM models
- **Validation suite** (`validate_prompt.py`): 175-check automated verification covering taxonomy completeness, example accuracy, schema consistency, assembly correctness, and chunking integrity

## Key Design Decisions

| Decision | Rationale |
|---|---|
| Single-pass extraction + classification | Preserves context for classification; avoids two-pass token cost |
| Mandatory `reasoning` field in output | Reduces hallucinations and aids human review |
| `skipped_non_parameters` in output | Forces LLM to demonstrate understanding of boundaries |
| Section-boundary-aware chunking | Prevents splitting mid-paragraph; configurable overlap for context continuity |
| Three-layer prompt (system + examples + chunk) | Each layer has clear token budget; examples/param-names can be toggled off for small-context models |

## Parameter Classes

| Class | Count in Phase 1 | Description |
|---|---|---|
| `NORM_DIRECT` | 102 | Direct implementation choice, not CSR-controlled |
| `NORM_CSR_RW` | 55 | Controls whether a CSR field is RO/RW |
| `NORM_CSR_WARL` | 26 | Legal values of a WARL CSR field |
| `SW_RULE` | 2 | Deterministic with correct software |
| `NON_ISA` | — | Platform-level, outside ISA scope |
| `NON_NORM` | — | Inside NOTE/TIP/WARNING blocks |
| `DOC_RULE` | — | Documentation requirements |
| `UNKNOWN` | — | Needs further analysis |

## Token Budget

```
System prompt:           940 tokens
Few-shot examples:     1,691 tokens
UDB param names:       1,401 tokens
System overhead:         200 tokens
Reserved for output:   4,096 tokens
────────────────────────────────────
Fixed overhead:        4,232 tokens

Available for spec chunk:
  gpt-4o/gpt-4-turbo:   ~119K tokens
  claude-3.5-sonnet:     ~191K tokens
  gemini-1.5-pro:        ~991K tokens
```

## How to Run

```bash
# Estimate token budgets
python3 param_extraction/scripts/run_prompt.py estimate

# Chunk a spec file
python3 param_extraction/scripts/run_prompt.py chunk \
    ext/riscv-isa-manual/src/machine.adoc --max-tokens 40000

# Assemble a prompt for a specific chunk
python3 param_extraction/scripts/run_prompt.py assemble \
    ext/riscv-isa-manual/src/machine.adoc \
    --start-line 1209 --end-line 1270 --output-json

# Run validation suite
cd param_extraction/scripts && python3 validate_prompt.py
```

## Test Plan

- [x] `validate_prompt.py` passes 175/175 checks (0 failures)
- [x] All 8 parameter classes defined consistently across taxonomy, system prompt, and examples
- [x] All 6 value types defined consistently across taxonomy, system prompt, and examples
- [x] Decision tree ordering in taxonomy matches system prompt ordering
- [x] All example UDB parameter names verified in `ground_truth.json`
- [x] All example classifications match Phase 1 classifications
- [x] All example line numbers verified against actual spec files
- [x] Example output schema fields match system prompt schema
- [x] All 74 spec files chunk successfully with no gaps
- [x] Chunking handles edge cases: empty files, no headers, very small chunk limits
- [x] Context overflow correctly raises `ValueError` for small-context models
- [x] Examples/param-names correctly omit when disabled
- [x] No unuse

---

## #1783 — LFX Phase 3: AsciiDoc-aware spec chunking
- State: open | @ishaan-arora-1 | https://github.com/riscv/riscv-unified-db/pull/1783
- Updated: 2026-05-25T21:56:56Z

## Summary

Split the 52,602-line RISC-V specification into 78 semantically coherent chunks that preserve CSR section integrity for LLM-based parameter extraction. Builds on Phase 1 (#1765) and Phase 2 (#1766).

- **`chunker.py`**: AsciiDoc-aware chunking script with `run`, `info`, and `verify` CLI commands
- **`chunks/`**: 78 numbered chunk files with metadata headers + `manifest.json`

## Chunking Rules

1. **CSR section atomicity**: Never splits within a `====` section — each CSR description (heading, bytefield, behavioral paragraphs) stays together
2. **Section boundaries**: Splits at `===` or `====` AsciiDoc heading boundaries
3. **Target size**: 2,500–3,500 lines (~35K–45K tokens), leaving room for prompt layers within 128K context
4. **Overlap**: 30 lines of overlap context at chunk boundaries
5. **Small files**: Files under 2,000 lines are processed as single chunks

## Results

| Metric | Value |
|---|---|
| Total chunks | 78 |
| Total files | 74 |
| Multi-chunk files | 4 (machine.adoc, scalar-crypto.adoc, v-st-ext.adoc, vector-crypto.adoc) |
| CSR section splits | 0 |
| Line coverage | 100% on all multi-chunk files |
| Chunk size range | 2–3,448 lines |

### Multi-Chunk File Details

| File | Chunks | Sizes |
|---|---|---|
| machine.adoc (3,629 lines) | 2 | 3,334 + 325 |
| scalar-crypto.adoc (5,590 lines) | 2 | 3,448 + 2,172 |
| v-st-ext.adoc (5,396 lines) | 2 | 3,393 + 2,011 |
| vector-crypto.adoc (4,966 lines) | 2 | 3,340 + 1,656 |

## How to Run

```bash
# Chunk all spec files
python3 param_extraction/scripts/chunker.py run

# Show chunking for a specific file
python3 param_extraction/scripts/chunker.py info ext/riscv-isa-manual/src/machine.adoc

# Verify chunking output
python3 param_extraction/scripts/chunker.py verify
```

## Test Plan

- [x] `chunker.py verify` passes: 74/74 files, 0 CSR splits, 0 gaps
- [x] All 78 chunk files exist with correct metadata headers
- [x] manifest.json is consistent with chunk files
- [x] 100% line coverage on all 4 multi-chunk files
- [x] Overlap regions present in all non-first chunks of multi-chunk files
- [x] content_start_line correctly distinguishes overlap from new content
- [x] No debug artifacts or unused imports

Closes #1749

---

## Update — review change + re-chunk

Rewrote `merge_tiny_blocks` so it's bidirectional. The old version only checked the current block: if it was small, it got absorbed into the previous one. That meant a tiny leading block could never be merged forward because there was no "previous" yet when it was added. The new version handles both directions — if the previous block in the merged list is too small we absorb the current one into it, and if the current block is too small we extend the previous one to include it.

After that I re-ran the chunker against the current `riscv-isa-manual` submodule. The chunk layout shifted slightly:

|                    | Before | After  |
|--------------------|--------|--------|
| Total chunks       | 78     | **79** |
| Total lines coved  | 52,700 | 53,006 |

All 79 chunk files and `manifest.json` are refreshed in this PR.


---

## #1791 — LFX - Phase 4: LLM Extraction Pipeline
- State: open | @ishaan-arora-1 | https://github.com/riscv/riscv-unified-db/pull/1791
- Updated: 2026-05-25T21:57:11Z

## Summary

- Add `extract.py` — automated LLM extraction pipeline for identifying architectural parameters in the RISC-V specification
- Features token-aware rate limiting, exponential backoff for API throttling, source file skipping for non-parameter content (19 files), and pilot/run/merge/status CLI modes
- Includes v1 extraction results from Anthropic Claude across 59 spec chunks (208 unique parameters, ~$3.60 API cost)

### Key capabilities
- **Pilot mode**: Test extraction on `machine.adoc` chunks only (prompt validation)
- **Run mode**: Full extraction across all spec chunks with configurable delay and retry
- **Rate limiter**: Token-bucket algorithm tracking usage over 60s windows with 0.75 safety factor (stays within Anthropic's 30K input tokens/min tier)
- **Skip list**: 19 boilerplate `.adoc` files (bibliography, index, rationale, etc.) automatically excluded

### Results structure
- Per-chunk JSON results in `results/claude-sonnet-4/chunk_NNN.json`
- Merged `all_results_claude-sonnet-4.json` with all extracted parameters
- Each result includes: parameters found, confidence scores, classifications, token usage, and latency

## Test plan
- [x] Pilot run on `machine.adoc` chunks validates prompt quality
- [x] Full extraction completes all 59 chunks without errors
- [x] Rate limiter prevents 429 errors during sustained extraction
- [x] Merge produces valid combined results file
- [x] Status command reports accurate progress
- [x] Pre-commit hooks pass (ruff, SPDX headers)

---

## Update — review change + v1 re-run

Pushed the prompt change in `extract.py` — added a line right above the existing "include line numbers" instruction telling the model to treat lines before `content_start_line` as overlap context only and not re-extract a parameter whose defining sentence lives entirely in that overlap region.

While I was re-running the full v1 extraction I had to land three small infra fixes on `extract.py` in a separate commit (`fix(phase4): make extract.py runnable on Python 3.13 and tunable`):

- `from datetime import UTC, datetime` — the script was calling `datetime.now(datetime.UTC)` which only works as a chained attribute in a different import pattern. On Python 3.13 with the existing `from datetime import datetime`, it raises `AttributeError`. Switched to importing `UTC` explicitly.
- Made `RATE_LIMIT_TOKENS_PER_MIN` configurable via a `RATE_LIMIT_TPM` env var (default unchanged at 30,000). I bumped it to 200,000 for the re-run so the full extraction took ~20 minutes instead of ~2 hours.
- Made `max_tokens` configurable via a `MAX_OUTPUT_TOKENS` env var (default unchanged at 8,192). One large CSR-heavy chunk (the first machine.adoc chunk) was getting its JSON response truncated; 16,384 fixed it.

All three are env-driven with the original values as defaults, so nothing changes for the existing usage.

**V1 re-run results (claude-sonnet-4):**

| Metric                | Value |
|-----------------------|-------|
| Chunks processed      | 60    |
| Errors                | 0     |
| Raw parameters found  | 225   |
| Input tokens          | ~919K |
| Output tokens         | ~62K  |

Per-chunk JSON results and the merged `all_results_claude-sonnet-4.json` are refreshed.


---

## #1792 — LFX - Phase 5: Analysis, Alignment & Metrics
- State: open | @ishaan-arora-1 | https://github.com/riscv/riscv-unified-db/pull/1792
- Updated: 2026-05-26T17:47:48Z

## Summary

- Add `analyze.py` — comprehensive analysis pipeline for evaluating LLM extraction results against UDB ground truth
- Implements deduplication (handling cross-chunk duplicates with confidence-based selection), multi-strategy alignment (exact match, one-to-many mappings, concept groups, fuzzy name matching), and detailed metrics computation
- Generates discrepancy reports categorizing differences as naming mismatches, class disagreements, recall misses, new discoveries, and hallucination suspects

### V1 Evaluation Results
| Metric | Value |
|--------|-------|
| UDB parameters | 185 |
| LLM params (deduped) | 215 |
| Raw recall | **60.0%** |
| Adjusted recall | **62.7%** |
| Classification accuracy | 67.9% |
| New params discovered | 153 |

### Key analysis capabilities
- **Deduplication**: Cross-chunk parameter deduplication preferring in-content-region matches over overlap-region duplicates
- **Curated one-to-many groups**: Hand-reviewed allowlist (`data/one_to_many_groups.json`) of UDB parameter groups where many per-exception / per-register / per-extension variants are defined by a single spec sentence (e.g. `REPORT_VA_IN_MTVAL_ON_*` has 10 UDB members but is defined once in the spec). Every group carries a `justification` field pointing at the text it covers, so the matching is reviewable rather than algorithmic.
- **Stem / prefix matching**: Catches close-but-not-exact pairs that share a long common token stem (e.g. LLM `REPORT_ENCODING_IN_MTVAL_ON_X` vs UDB `REPORT_ENCODING_IN_VSTVAL_ON_X`), which strict Jaccard would miss.
- **Concept groups**: Single-member shared-concept groups for recall calculation.
- **Per-class recall**: Breakdown of recall by parameter classification (NORM_DIRECT, NORM_CSR_WARL, etc.)
- **Confusion matrix**: Classification accuracy analysis across all parameter classes

## Test plan
- [x] Deduplication correctly resolves cross-chunk duplicates
- [x] Alignment matches UDB parameters via exact, fuzzy, stem, concept-group, and curated one-to-many strategies
- [x] Metrics computation produces valid recall and accuracy figures
- [x] Discrepancy CSV categorizes all differences correctly
- [x] Pre-commit hooks pass (ruff, SPDX headers)

---

## Update — review changes + analyze re-run

Pushed two changes to `analyze.py`:

1. Restricted concept-group alignment to groups with exactly one UDB member (`len(group_members) == 1`). The old code marked **every** member of a multi-member group as aligned whenever any LLM finding matched the group's keywords, which inflated recall by claiming alignment for parameters the LLM never actually produced.
2. Broadened the `already_aligned_llm` filter from `match_type in ("exact",)` to `match_type != "none"`, so LLM findings already matched via fuzzy / one-to-many / concept-group don't get re-considered for fuzzy matching.

Re-ran the analysis on the refreshed v1 extraction. With the strict fix in place, raw recall measured 36.8% — the honest number after removing the inflated multi-member matches.

---

## Update 2 — curated one-to-many groups + stem matching

After the strict concept-group fix, a lot of legitimate alignments were being dropped: the spec describes things like "mtval reports the faulting virtual address on these exceptions" **once**, but UDB splits that across 10 separate `REPORT_VA_IN_MTVAL_ON_*` parameters. With the strict fix, finding the concept counted as zero hits; with the old loose code, any keyword overlap counted as 10 hits. Neither was right.

I added a curated allowlist (`param_extraction/data/one_to_many_groups.json`) of these multi-variant groups. Each entry has:
- the UDB prefix it covers,
- the keywords that signal the concept,
- a per-group minimum match score,
- and a written `justification` pointing at the spec text the group represents.

When the LLM's name + excerpt clearly match the concept, every group member is counted as aligned. There are currently 8 such groups, all reviewed by hand:

- `REPORT_VA_IN_MTVAL_ON_*` / 

---

## #1793 — LFX - Phase 6: Prompt Refinement & V2 Results
- State: open | @ishaan-arora-1 | https://github.com/riscv/riscv-unified-db/pull/1793
- Updated: 2026-05-26T17:47:10Z

## Summary

- Refine LLM prompts based on Phase 5 gap analysis, targeting 49 recoverable UDB recall misses
- Add v2 system prompt with classification disambiguation rules and 7 commonly missed parameter pattern categories (counter/HPM, VM modes, tval reporting, alignment, implementation values, conditional SC failure, stateen control)
- Add 4 new positive few-shot examples targeting previously missed parameter types
- Implement prompt versioning support (`PROMPT_VERSION` env var) in `run_prompt.py` and `extract.py` for side-by-side v1/v2 comparison

### V1 vs V2 Comparison (final, after analysis improvements)

| Metric                  | V1     | V2       | Delta     |
|-------------------------|--------|----------|-----------|
| Parameters found        | 225    | **361**  | +60%      |
| Deduped unique          | 215    | **346**  | +61%      |
| Raw recall              | 60.0%  | **69.7%** | +9.7 pp  |
| Adjusted recall         | 62.7%  | **72.9%** | +10.2 pp |
| Classification accuracy | 67.9%  | **88.4%** | +20.5 pp |
| New params discovered   | 153    | **256**  | +67%      |
| Per-class NORM_DIRECT recall | 47%  | **83%**  | +36 pp |
| Per-class NORM_CSR_RW recall | 41%  | **63%**  | +22 pp |
| Per-class NORM_CSR_WARL recall | 25%  | **50%**  | +25 pp |

### What changed in v2 prompts
- **System prompt additions**: Classification disambiguation section clarifying NORM_CSR_WARL vs NORM_CSR_RW vs NORM_DIRECT boundaries; "Commonly Missed Parameter Patterns" section with 7 specific categories and indicators
- **New examples**: `COUNTINHIBIT_EN` (counter inhibit), `GSTAGE_MODE_BARE` (VM mode support), `REPORT_ENCODING_IN_MTVAL_ON_ILLEGAL_INSTRUCTION` (tval reporting), `LRSC_FAIL_ON_NON_EXACT_LRSC` (LR/SC conditional failure)
- **Versioning**: Results stored in `results/v2/` directory, prompts in `prompts/v2/`

## Test plan
- [x] V2 extraction completes all chunks without errors
- [x] Classification accuracy improves over v1 (88.4% vs 67.9%)
- [x] Prompt versioning correctly isolates v1 and v2 results
- [x] Pre-commit hooks pass (ruff, SPDX headers, formatting)

---

## Update — review change + v2 re-run

Mirrored the Phase 4 prompt change in the v2 pipeline by adding the overlap-context instruction to `run_prompt.py`:

```
Use overlap text only as context; avoid re-extracting a parameter when
its defining sentence appears entirely in a previous chunk.
```

Then re-ran the v2 extraction end-to-end and the analysis on top of it.

---

## Update 2 — analysis lift (curated one-to-many + stem matching)

Carried forward the Phase 5 changes: a curated one-to-many group allowlist (`param_extraction/data/one_to_many_groups.json`) plus stem/prefix matching in `analyze.py`. The previous v2 recall numbers were undercounting any case where the spec described many UDB variants in a single sentence (e.g. mtval/stval/vstval VA reporting, transformed-instruction reporting, ECALL-per-mode). With curated groups, each such sentence now legitimately aligns to the full set of UDB variants it describes.

**V2 metrics, before vs after the analysis lift:**

| Metric | Strict-only | With curated groups + stem |
|---|---|---|
| Raw recall | 46.5% | **69.7%** |
| Adjusted recall | 48.6% | **72.9%** |
| Classification accuracy | 88.4% | 88.4% |
| Deduped LLM params | 346 | 346 |
| Per-class NORM_DIRECT | 42% | **83%** |

None of the LLM extractions changed — only the alignment recognises real semantic equivalence between a spec sentence and its UDB variants. Classification accuracy is unchanged because nothing in the underlying class assignments moved.

The v2 prompt's "Classification Disambiguation" section and "Commonly Missed Parameter Patterns" remain the headline win for accuracy (88.4% vs 67.9%). The lift here just makes the recall number an honest reflection of what the v2 extraction actually covers.

---

## #1831 — LFX - Phase 7: Final Parameter Spreadsheet
- State: open | @ishaan-arora-1 | https://github.com/riscv/riscv-unified-db/pull/1831
- Updated: 2026-05-26T17:46:46Z

## Summary

- Add `generate_spreadsheet.py` — consolidates the V2 deduplicated LLM extraction (Phase 6, #1793) with the UDB ground truth (Phase 1, #1765) and the LLM↔UDB alignment (Phase 5/6, #1792, #1793) into a single authoritative spreadsheet of every confirmed architectural parameter
- Produces `parameters.csv` (programmatic use) and `parameters.xlsx` (presentation / review) with the 9 columns specified in #1753, plus a human-readable `parameters_stats.txt` summary
- Adds `openpyxl` as a project dependency for XLSX output

Closes #1753. Builds on #1765, #1766, #1783, #1791, #1792, #1793.

## Columns

| Column | Source |
|---|---|
| `adoc_file` | LLM result `_source_file` |
| `line_number` | LLM result `line_number` |
| `excerpt` | Verbatim spec text |
| `parameter_name` | UDB name when aligned, else normalized ALL_CAPS_WITH_UNDERSCORES |
| `named` | `yes` if already in UDB, `no` otherwise |
| `class` | LLM classification (`NORM_DIRECT`, `NORM_CSR_WARL`, `NORM_CSR_RW`, `SW_RULE`, `NON_ISA`, …) |
| `value_type` | `binary`, `enum`, `range`, `set`, `bitmask`, `value` |
| `confidence` | `high` / `medium` (low filtered out per Phase 8 plan) |
| `notes` | Reviewer notes (seeded with alignment path for non-exact matches) |

## Resolution Rules

For each deduplicated V2 result row:
1. `existing_udb_name` set & in `udb_param_names.txt` → use UDB name, `named=yes`
2. Alignment exact match → UDB name, `named=yes`
3. Alignment `one_to_many` / `concept_group` / `fuzzy_name` → UDB name, `named=yes`, `notes` seeded with the alignment path for reviewer context
4. Otherwise → normalized LLM name, `named=no`, `notes='newly discovered'`

## Results

| Metric | Value |
|---|---|
| Total rows (confidence ≥ medium) | **330** |
| Already named in UDB | 97 |
| Newly discovered | 233 |
| Spec files touched | 43 |

### Classification breakdown

| Class | Count |
|---|---|
| `NORM_DIRECT` | 208 |
| `NORM_CSR_RW` | 63 |
| `NORM_CSR_WARL` | 52 |
| `NON_ISA` | 5 |
| `SW_RULE` | 2 |

### Value type breakdown

| Type | Count |
|---|---|
| `binary` | 170 |
| `enum` | 59 |
| `set` | 36 |
| `value` | 30 |
| `bitmask` | 21 |
| `range` | 14 |

### Confidence breakdown

| Confidence | Count |
|---|---|
| `high` | 291 |
| `medium` | 39 |

### Top spec files

| File | Params |
|---|---|
| `machine.adoc` | 39 |
| `supervisor.adoc` | 38 |
| `scalar-crypto.adoc` | 34 |
| `unpriv-cfi.adoc` | 24 |
| `v-st-ext.adoc` | 22 |
| `smstateen.adoc` | 21 |
| `hypervisor.adoc` | 17 |

## Naming Convention for New Parameters

Newly discovered (unnamed) parameters follow UDB's existing `ALL_CAPS_WITH_UNDERSCORES` style. The normalizer:
- Strips backticks/quotes
- Replaces non-identifier separators with `_`
- Collapses repeated underscores
- Upper-cases the result

The LLM, primed by Phase 2's few-shot examples, already produces names in this style for the vast majority of new parameters (e.g. `BF16_SUBNORMAL_SUPPORT`, `VFNCVTBF16_SEW_SUPPORT`, `MTVEC_BASE_ALIGNMENT`, `LRSC_FAIL_ON_NON_EXACT_LRSC`).

## How to Run

```bash
uv run python param_extraction/scripts/generate_spreadsheet.py
# defaults to V2 inputs; --min-confidence low|medium|high to adjust
```

## Test Plan

- [x] CSV emits all 9 columns in the order specified by #1753
- [x] XLSX renders with styled header, wrapped excerpts, frozen header row, and autofilter
- [x] 100% of UDB-aligned rows resolve to a real UDB name (`udb_param_names.txt` cross-check)
- [x] New-parameter names follow `ALL_CAPS_WITH_UNDERSCORES`
- [x] Pre-commit hooks pass (ruff, SPDX sidecars)
- [x] Reviewable size (330 rows) — ready for Phase 8 tagging

---

## Update — review change + spreadsheet rebuild

Rewrote the alignment lookup in `generate_spreadsheet.py` to handle ambiguous LLM names properly:

- `build_alignment_lookup` now returns `dict[str, list[dict]]` so all alignment entries for an LLM name are kept. The old version silently overwrote with the last entry whenever an LLM name had multiple alignments — so if the LLM produced one finding th

---

## #1832 — LFX - Phase 8: Insert [#param:...] tags into riscv-isa-manual
- State: open | @ishaan-arora-1 | https://github.com/riscv/riscv-unified-db/pull/1832
- Updated: 2026-05-26T17:46:13Z

## Summary

- Add `insert_tags.py` — locates every confirmed parameter excerpt from the Phase 7 spreadsheet (#1831) in its matching `.adoc` file and wraps it with `[#param:NAME]#excerpt#`, mirroring the existing `[#norm:NAME]#text#` convention (~1,361 occurrences across 31 files)
- Introduces the `[#param:...]` namespace **for the first time** in `riscv-isa-manual`, so UDB can mechanically track architectural parameters in the spec text itself
- Captures the full submodule diff as `riscv-isa-manual-param-tags.patch` (2.5K lines) ready for a follow-on PR against `riscv/riscv-isa-manual`

Closes #1754. Builds on #1765, #1766, #1783, #1791, #1792, #1793, #1831.

## Match Statistics

Run against `parameters.csv` (330 rows at confidence ≥ medium):

| Metric | Value |
|---|---|
| **Tags inserted** | **321 (97.3%)** |
| Inline wraps `[#param:NAME]#text#` | 102 |
| Bare anchors `[#param:NAME]##` (inside existing norm tags) | 219 |
| Unmatched rows (manual review) | 9 |
| `.adoc` files modified | **43** |
| AsciiDoc validation (asciidoctor --failure-level=ERROR) | **0 errors** |

The 9 unmatched rows are written to `tagging_unmatched.csv` for manual review — all are cases where the LLM excerpt drifted slightly from the spec wording (paraphrasing, punctuation, sentence boundaries).

## Matcher Design

- **Whitespace-normalized fuzzy locator** across the whole file. The LLM-reported line number is used only as a proximity tiebreaker — LLMs notoriously mis-count lines, so we never trust them as exact positions.
- **Inline-tag pre-stripping**: existing `[#prefix:NAME]#` openers / matching `#` closers are skipped over during normalization, so an excerpt buried inside a multi-line `[#norm:…]#…#` block still matches.
- **AsciiDoc attribute refs** (`{ge}`, `{le}`, `{ne}`, …) are collapsed to whitespace — matches the LLM's rendered-text form (`≥`, `≤`, `≠`) to the source's attribute-ref form.
- **Unicode normalization**: en/em dashes, backticks, asterisks, underscores, arrow chars all collapse to whitespace on both sides.
- **Overlap detection** uses a whole-file scan of inline tag spans — when a match lands inside an existing `[#norm:…]#…#` block, we emit a zero-width param anchor `[#param:NAME]##` placed immediately before the enclosing norm tag's opener, so paragraph flow is preserved and the anchor still attaches to the same prose.

### Tag forms

**Plain wrap** (no overlap):
``[#param:LRSC_FAIL_ON_VA_SYNONYM]#Following this model, in systems with memory translation, an SC is allowed to succeed if the earlier LR reserved the same location using an alias with a different virtual address, but is also allowed to fail if the virtual address is different.#``

**Adjacent anchor** (excerpt is already inside a `[#norm:...]#...#` block):
``[#param:LRSC_MISALIGNED_BEHAVIOR]##[#norm:lr_sc_alignment]#For LR and SC, the Zalrsc extension requires that the address held in `rs1` be naturally aligned to the size of the operand…#``

## Deliverables

**UDB side (this PR):**

| File | Description |
|---|---|
| `param_extraction/scripts/insert_tags.py` | Tagger with `run` / `dry-run` / `verify` modes |
| `param_extraction/data/tagging_report.txt` | Per-file statistics + failure log |
| `param_extraction/data/tagging_unmatched.csv` | 9 rows for manual review |
| `param_extraction/data/riscv-isa-manual-param-tags.patch` | Full diff (2.5K lines) of all 43 modified `.adoc` files, ready to apply on a fork of `riscv/riscv-isa-manual` |

**riscv-isa-manual side (follow-on upstream PR):**

The patch under `param_extraction/data/riscv-isa-manual-param-tags.patch` applies cleanly against the submodule pinned by this repo. Procedure to open the upstream PR:

```bash
# in a fork of riscv-isa-manual, on the pinned commit:
git apply /path/to/riscv-unified-db/param_extraction/data/riscv-isa-manual-param-tags.patch
git checkout -b param-tags-v1
git add src/ && git commit -m \"feat(tags): introduce [#param:...] namespace for architectural parameters\"
git push origin param-tags

---


