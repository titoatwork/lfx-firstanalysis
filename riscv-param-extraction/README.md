# RISC-V architectural parameter extraction

Code, fixtures, and measured results for extracting **architectural parameters** from RISC-V ISA material and exporting draft UDB param YAML.

**Monorepo:** [titoatwork/lfx-firstanalysis](https://github.com/titoatwork/lfx-firstanalysis) · path `riscv-param-extraction/`  
**Upstream:** [riscv/riscv-unified-db](https://github.com/riscv/riscv-unified-db)  
**Part I credit:** [@ishaan-arora-1](https://github.com/ishaan-arora-1) / UDB PRs #1765–#1832. This package **reproduces and extends** that public surface; it does not claim Spring authorship.

Part I shipped extract → analyze → spreadsheet on open PR branches. This package adds:

| Piece | What it is |
|-------|------------|
| **Artifact A** | Multi-model measurement (gpt-4o-mini vs Claude under identical v2 prompt) |
| **Artifact B** | Spreadsheet rows → draft UDB param YAML + schema validation |
| **Manifests** | Run records (model, prompt hash, cost, checksums) |
| **Artifact C** | Preregistered dual-run / variance experiment |
| **`analysis/`** | Offline audits of gold classification labels and schema shapes |

> **Every published recall figure is a grounding score.** Part I prompts supply the complete list of 185 gold parameter names, set-identical to the ground truth. Discovery without that catalogue is unmeasured here; see [`artifact_c/PREREGISTRATION.md`](artifact_c/PREREGISTRATION.md) and the note at the top of [`docs/metrics.md`](docs/metrics.md).

Per-class rates use small denominators (WARL n=24). One item moves the rate by about four points; the same class moved by 7 between two byte-identical runs.

---

## Measured numbers

| Work | Result |
|------|--------|
| Phase 1 GT (live UDB) | **223** params; 100% any / **91%** strong match |
| Part I v2 remeasure (GT 185) | adj recall **72.9%**, class acc **88.4%**, WARL **12/24** |
| Same LLM output vs live GT 223 | adj recall **64.2%**, class acc **88.6%**, WARL **50%** |
| Pilot machine.adoc | **COMPLETE_WITH_MODEL_SPLIT**. 021 **gpt-4o** (6 params), 020 **gpt-4o-mini** (9 params); total ~**$0.05** |
| **Artifact A** (gpt-4o-mini, 60 chunks, GT185) | adj recall **32.2%**; name Jaccard vs Claude **3.8%**; WARL **3/24**; ~**$0.16** |
| `parameters.csv` named=yes | **87** rows / **83** unique |
| Artifact B named export | **83/83** schema-valid |
| Artifact B new (limit 20) | **20/20** schema-valid |

Full tables: [docs/metrics.md](docs/metrics.md).  
Re-derive from the monorepo root: `../verify.sh`.

### Artifact A — cross-model disagreement

Under the **same** v2 prompt and chunk set:

| Metric | Claude-sonnet-4 | gpt-4o-mini |
|--------|----------------:|------------:|
| Adjusted recall | **72.9%** | **32.2%** |
| WARL recall | **50%** | **12.5%** |
| Deduped params | 346 | 230 |
| Name Jaccard | — | **3.8%** |
| High-conf “new” both models | — | **9** |

High-confidence overlap is not a validated review gate: shared lists have included derived non-parameters (e.g. `IALIGN`). Details: [docs/metrics.md](docs/metrics.md) §5.

### Pilot model-split

| Chunk | Model | In / out tokens | Params | ~USD |
|-------|--------|----------------:|-------:|-----:|
| chunk_021 | gpt-4o-2024-11-20 | 10 115 / 1 152 | 6 | ~0.037 |
| chunk_020 | gpt-4o-mini-2024-07-18 | 44 874 / 1 541 | 9 | ~0.008 |

gpt-4o org TPM **30 000** blocked the large chunk; mini completed it. Not a pure gpt-4o full-manual pilot.

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

Live extraction needs a local `riscv-unified-db` checkout and an API key; see [manifests/pilot-machine-adoc.md](manifests/pilot-machine-adoc.md). This package does not ship keys or full per-chunk JSON dumps.

---

## Limitations

- Named params already exist in UDB; Artifact B is a draft export + validation path, not 83 new architecture parameters.
- Pilot used two OpenAI models for machine.adoc because of TPM limits.
- Artifact A second model is **gpt-4o-mini**, not full gpt-4o; mini underperforms Claude on recall (32.2% vs 72.9%).
- Prompt **v3** WARL ablation: overall adj **35.0%** but WARL worse (8.3% vs 12.5%); honest null (metrics §6).
- Per-chunk extraction JSON stays in the local UDB clone; public surface ships aggregates + manifests.
- Do not merge draft YAML upstream without SIG / mentor review.
- No unsolicited bulk PR into `riscv/riscv-unified-db`.

---

## Layout

```text
riscv-param-extraction/
  docs/metrics.md          # authoritative measured tables
  docs/design.md           # design decisions
  manifests/               # run records
  export/                  # Artifact B (csv → draft YAML)
  drafts/param/            # DRAFT YAML (named)
  drafts/param-new/        # DRAFT YAML (new candidates)
  results/                 # B reports + A agreement samples
  pipeline/               # Artifact A agreement tools
  artifact_c/              # preregistered variance experiment
  analysis/                # gold classification + schema-shape audits
  workflow_slice/          # eval fixtures + review/export path
  data/parameters.csv
  tests/
```

---

## Links

| Resource | URL |
|----------|-----|
| LFX Part II project | https://mentorship.lfx.linuxfoundation.org/project/22296947-cecb-4a8f-8bcb-4f34710e9f66 |
| Upstream UDB | https://github.com/riscv/riscv-unified-db |
| Part I plans | issues #1747, #1751 |
| Part I PRs | #1765–#1832 |
| Monorepo summary | [../docs/](../docs/README.md) |
