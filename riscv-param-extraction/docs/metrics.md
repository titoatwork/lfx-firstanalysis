# Metrics

Tables only. Numbers are **user-measured** on the local `riscv-unified-db` checkout (`lfx-1832`) unless marked pending. Do not invent pilot/A results.

Credit: Part I pipeline and committed results — [@ishaan-arora-1](https://github.com/ishaan-arora-1) / [riscv/riscv-unified-db](https://github.com/riscv/riscv-unified-db) PRs #1765–#1832. Remeasure here is independent reproduction, not authorship of Part I.

---

## 1. Phase 1 ground truth (regenerated on live UDB)

| Metric | Value |
|--------|------:|
| Real parameters | **223** (Part I freeze was 185; +38) |
| Spec files / lines | 74 / ~52 878 |
| Any keyword match / strong | 100% / 91% |
| Classes | DIRECT 140 · CSR_RW 55 · WARL 26 · SW_RULE 2 |

Source: local `export_udb_params` → `map_params_to_spec` → `generate_report` (2026-07-21 session).

---

## 2. Part I v2 remeasure (Claude Sonnet 4, committed GT 185)

| Metric | Value |
|--------|------:|
| Adjusted recall | **72.9%** |
| Classification accuracy | **88.4%** |
| WARL recall (`NORM_CSR_WARL`) | **50%** (12/24) |
| Deduped LLM params | 346 |

| Class | Found | Total |
|-------|------:|------:|
| NORM_DIRECT | 83 | 100 |
| NORM_CSR_RW | 32 | 51 |
| NORM_CSR_WARL | 12 | 24 |
| SW_RULE | 2 | 2 |

Against **live GT 223** (same LLM output): adjusted recall **64.2%**, class acc **88.6%**, WARL still **50%**.

---

## 3. Spreadsheet baseline (Artifact B input)

| Metric | Value |
|--------|------:|
| `parameters.csv` rows | 346 |
| `named=yes` rows | **87** |
| Unique `named=yes` names | **83** |
| Overlap with UDB `spec/std/isa/param/*.yaml` | **83 / 83** (all named already in UDB on this freeze) |
| Unique names not in UDB (candidates) | **257** (all `named=no`) |

Do **not** claim 97 named params without re-counting the CSV in use.

---

## 4. Artifact A — multi-model (pending API)

| Metric | Status |
|--------|--------|
| Second model full run | **Not run** |
| Per-class recall vs claude-sonnet-4 | — |
| Inter-model agreement | — |
| Hallucination-overlap | — |

---

## 5. Artifact B — export validation (2026-07-22)

Reports: `results/export_b_named.json`, `results/export_b_new.json`.

### Mode `named` (named=yes unique)

| Metric | Value |
|--------|------:|
| Drafts written | **83** |
| Schema-valid | **83 / 83** |
| UDB name overlap | **83 / 83** |
| `definedBy` source | **udb_copy** (all) |

| Class | Count |
|-------|------:|
| NORM_DIRECT | 38 |
| NORM_CSR_RW | 32 |
| NORM_CSR_WARL | 11 |
| SW_RULE | 2 |

### Mode `new` (limit 20, not in UDB)

| Metric | Value |
|--------|------:|
| Drafts written | **20** |
| Schema-valid | **20 / 20** |
| UDB name overlap | **0** |
| `definedBy` source | **adoc_map** |

| Class | Count |
|-------|------:|
| NORM_DIRECT | 16 |
| NORM_CSR_RW | 4 |

Schema fragments for enum/range/set still need human domain fill (CSV does not encode members/bounds).
