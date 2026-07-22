# Study digest — Part I plans + local measurements

Generated for Phase 1 immersion. Facts only from issues/PRs/local runs.

## Read order (from playbook)
1. Issues #1747 (Phase 1 GT), #1751 (Phase 5 analysis) — full text in `02-github-issues/`
2. `04-pipeline-docs/taxonomy.md`
3. Scripts under `riscv-unified-db/param_extraction/scripts/` (heads in `04-pipeline-docs/scripts-heads.md`)
4. `08-udb-docs/CONTRIBUTING.adoc`, `05-schemas-samples/param_schema.json`
5. Sample YAML in `05-schemas-samples/param-yaml/`
6. Isa-manual index `08-udb-docs/isa-manual-src-index.md`

## Part I phase map (Ishaan PRs — still open, code on branches)

| Phase | Issue / PR | Focus |
|-------|------------|--------|
| 1 | #1747 / PR #1765 | Ground truth from UDB params |
| 2 | PR #1766 | Taxonomy + LLM prompt architecture |
| 4 | PR #1791 | LLM extraction pipeline |
| 5 | #1751 / PR #1792 | Analyze, align, metrics |
| 6 | PR #1793 | Prompt refinement + V2 results |
| 7 | PR #1831 | Final parameter spreadsheet |
| 8 | PR #1832 | Insert `[#param:...]` tags into isa-manual |

Local: checkout `lfx-1832` has the fullest tree.

## Issue #1747 — Ground truth (what we reproduced)
- Goal: machine-readable catalog of UDB params as LLM training + validation benchmark
- Deliverables: ground_truth.json, spec_mappings.json, parameters_catalog.csv, phase1_report.txt, udb_param_names.txt
- Classes: NORM_DIRECT, NORM_CSR_WARL, NORM_CSR_RW, SW_RULE
- Acceptance: 185 params at freeze; >=95% spec candidates; etc.

### Our run (2026-07-21)
- Params: **223** (UDB grew; +38 vs Part I freeze 185)
- Spec files: 74, lines ~52878
- Any match 100%, strong match 91%
- Commands: export_udb_params.py → map_params_to_spec.py → generate_report.py

## Issue #1751 — Analysis (Part II multi-model lives here)
- Goal: compare models vs UDB; metrics; discrepancy types
- Planned models in issue: Claude, GPT-4o, UDB three-way matrix
- Metrics: recall (target >70%), precision, class accuracy, inter-model agreement
- Discrepancy types: hallucination, UDB gap, recall miss, class disagreement, naming mismatch
- **Part I delivered metrics mainly for claude-sonnet-4 v2**; multi-model matrix is unfinished → **your Artifact A**

### Our remeasure (v2 Claude results)
| Against | Adjusted recall | Class acc | WARL |
|---------|-----------------|-----------|------|
| Committed GT 185 | **72.9%** | **88.4%** | 50% (12/24) |
| Regenerated GT 223 | 64.2% | 88.6% | 50% (12/24) |

Exact match to published 72.9% on GT185 → pipeline reproduced.

## Taxonomy (classes) — see full file
- NORM_DIRECT: design-time, not CSR-controlled
- NORM_CSR_WARL: legal values of WARL field (hardest recall ~50%)
- NORM_CSR_RW: RO vs RW mutability
- SW_RULE: software-deterministic with correct SW
- Value types: binary, enum, range, set, bitmask, conditional, value

## param_schema essentials
Required: ``, `kind: parameter`, `description`, `long_name`, `definedBy`, `schema`
`` const: `param_schema.json#`
See `05-schemas-samples/param_schema.json` + sample YAML.

## Artifact A hook (from #1751)
Issue explicitly wants cross-model matrix (Claude x GPT-4o x UDB). Part I left multi-model unfinished. Your Phase 2 A = run second model + agreement analysis.

## Artifact B hook
parameters.csv (346 rows, named=yes ~87) → draft param YAML validated vs param_schema + existing YAML as GT for named set.
Obj 4 → 5 on Part II project card.

## Etiquette (playbook)
- Public work in **your** repo first
- List summary after A/B, no unsolicited big UDB PRs
- Slack mentorship channel = logistics only
