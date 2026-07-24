# RISC-V architectural parameter extraction (pre-apply)

Public selection surface for [LFX Mentorship Part II — AI-assisted extraction of architectural parameters](https://mentorship.lfx.linuxfoundation.org/project/22296947-cecb-4a8f-8bcb-4f34710e9f66).

**Home:** [titoatwork/lfx-firstanalysis](https://github.com/titoatwork/lfx-firstanalysis) · path `riscv-param-extraction/`  
**Not a second product repo.** Credit Part I to [@ishaan-arora-1](https://github.com/ishaan-arora-1) / [riscv/riscv-unified-db](https://github.com/riscv/riscv-unified-db) PRs #1765–#1832 — this work **reproduces and extends**, it does not claim Spring authorship.

Part I already shipped extract → analyze → spreadsheet on open PR branches. This folder adds: **multi-model measurement** (Artifact A), **export of spreadsheet rows to draft UDB param YAML** (Artifact B), and **run manifests** (Obj 3).

---

## Measured numbers

| Work | Result |
|------|--------|
| Phase 1 GT (live UDB) | **223** params; 100% any / **91%** strong match |
| Part I v2 remeasure (GT 185) | adj recall **72.9%**, class acc **88.4%**, WARL **50%** |
| Same LLM output vs live GT 223 | adj recall **64.2%**, class acc **88.6%**, WARL **50%** |
| Pilot machine.adoc | **COMPLETE_WITH_MODEL_SPLIT** — 021 **gpt-4o** (6 params), 020 **gpt-4o-mini** (9 params); total ~**$0.05** |
| **Artifact A** (gpt-4o-mini, 60 chunks, GT185) | adj recall **32.2%**, WARL **12.5%**, name Jaccard vs Claude **3.8%** — **worse than Claude (honest)**; ~**$0.16** |
| `parameters.csv` named=yes | **87** rows / **83** unique (not 97) |
| Artifact B named export | **83/83** schema-valid |
| Artifact B new (limit 20) | **20/20** schema-valid |

Full tables: [docs/metrics.md](docs/metrics.md).  
Pilot manifest: [manifests/pilot-machine-adoc.md](manifests/pilot-machine-adoc.md).  
Artifact A manifest: [manifests/artifact-a-gpt-4o-mini.md](manifests/artifact-a-gpt-4o-mini.md).  
Design notes: [docs/design.md](docs/design.md).

### Pilot model-split (detail)

| Chunk | Model | In / out tokens | Params | ~USD |
|-------|--------|----------------:|-------:|-----:|
| chunk_021 | gpt-4o-2024-11-20 | 10 115 / 1 152 | 6 | ~0.037 |
| chunk_020 | gpt-4o-mini-2024-07-18 | 44 874 / 1 541 | 9 | ~0.008 |

gpt-4o org TPM **30 000** blocked the large chunk (~**44 373** input); mini completed it. **Not** a pure gpt-4o full machine.adoc pilot.

### Artifact A vs Claude (GT185) — summary

| Metric | Claude-sonnet-4 | gpt-4o-mini |
|--------|----------------:|------------:|
| Adjusted recall | **72.9%** | **32.2%** |
| WARL recall | **50%** | **12.5%** |
| Deduped params | 346 | 230 |
| Name Jaccard | — | **3.8%** |
| High-conf “new” both models | — | **9** |

---

## How to run Artifact B (offline, $0)

```text
cd riscv-param-extraction
pip install -r requirements.txt

python -m export.csv_to_param_yaml --csv data/parameters.csv --out drafts/param --mode named --udb-root ../riscv-unified-db --clean
python -m export.csv_to_param_yaml --mode new --limit 20 --udb-root ../riscv-unified-db --out drafts/param-new --clean
python -m unittest discover -s tests -v
```

- Drafts: `drafts/param/`, `drafts/param-new/` (all marked **DRAFT**)  
- Reports: `results/export_b_*.json`  
- Schema: `export/schemas/param_schema.json`

Pilot extraction needs a local `riscv-unified-db` on `lfx-1832` and **your own** API key — see [manifests/pilot-machine-adoc.md](manifests/pilot-machine-adoc.md). This repo does not ship keys or full chunk JSON dumps.

---

## Limitations

- Named params already exist in UDB; B is a **draft export + validation** path, not 83 new architecture parameters.  
- Pilot used **two OpenAI models** for machine.adoc because of TPM limits.  
- Artifact A second model is **gpt-4o-mini** (budget/TPM), **not** full gpt-4o; mini **underperforms** Claude on recall (32.2% vs 72.9%).  
- Per-chunk extraction JSON stays in the local UDB clone; public surface ships aggregates + manifests.  
- Do not merge draft YAML upstream without SIG / mentor review.  
- No unsolicited bulk PR into `riscv/riscv-unified-db`.

---

## Links

| Resource | URL |
|----------|-----|
| Part II LFX project | https://mentorship.lfx.linuxfoundation.org/project/22296947-cecb-4a8f-8bcb-4f34710e9f66 |
| Upstream UDB | https://github.com/riscv/riscv-unified-db |
| Part I plans | issues #1747, #1751 |
| Part I PRs | #1765–#1832 |
| This monorepo | https://github.com/titoatwork/lfx-firstanalysis |

---

## Layout

```text
riscv-param-extraction/
  README.md
  docs/metrics.md          # remeasure + pilot + A + B tables
  docs/design.md
  manifests/               # Obj 3 run records
  export/                  # Artifact B
  drafts/param/            # DRAFT YAML (named)
  drafts/param-new/        # DRAFT YAML (new candidates)
  results/                 # B reports + A agreement/metrics samples
  pipeline/                # Artifact A agreement tools
  data/parameters.csv
  tests/
```
