# Phase 2 — param export prototype (Artifact B)

**Lives in:** [titoatwork/lfx-firstanalysis](https://github.com/titoatwork/lfx-firstanalysis) under `riscv-param-extraction/`  
**First committed here:** **2026-07-22** (Phase 2 code — not Phase 1 study)  
**Do not confuse with:** Phase 1 immersion pack at repo root / `PHASE1-IMMERSION/` (earlier commits)

This folder is the Phase 2 public-selection work for [LFX Part II — architectural parameter extraction](https://mentorship.lfx.linuxfoundation.org/project/22296947-cecb-4a8f-8bcb-4f34710e9f66).

Part I already shipped extract → analyze → spreadsheet on PR branches of [riscv/riscv-unified-db](https://github.com/riscv/riscv-unified-db) (#1765–#1832, mentee [@ishaan-arora-1](https://github.com/ishaan-arora-1)). Gaps addressed here: **export spreadsheet → draft UDB param YAML** (Artifact B, this folder) and later **multi-model measurement** (Artifact A, needs API).

Does **not** claim Part I authorship. Not an unsolicited bulk PR into UDB.

### Work log (this folder)

| Date | What landed |
|------|-------------|
| **2026-07-22** | Artifact B: CSV→draft UDB YAML exporter, 83 named + 20 new schema-valid drafts, metrics tables, tests. Pilot + Artifact A still pending API. |

---

## Measured numbers (reproduction)

| Work | Result |
|------|--------|
| Phase 1 GT on live UDB | **223** params; 100% any / **91%** strong spec match |
| Part I v2 remeasure (GT 185) | adjusted recall **72.9%**, class acc **88.4%**, WARL **50%** |
| Same LLM output vs live GT 223 | adjusted recall **64.2%**, class acc **88.6%**, WARL **50%** |
| `parameters.csv` `named=yes` | **87** rows / **83** unique (all already present in UDB on this freeze) |
| Artifact B named export | **83/83** schema-valid drafts (`results/export_b_named.json`) |
| Artifact B new candidates | **20/20** schema-valid drafts not in UDB (`results/export_b_new.json`) |
| Artifact A multi-model | **Not run** (API key) |

Full tables: [docs/metrics.md](docs/metrics.md). Design: [docs/design.md](docs/design.md). Session log: [docs/WORKLOG-2026-07-22.md](docs/WORKLOG-2026-07-22.md).

---

## Artifact B — CSV → draft UDB YAML (runs offline)

From this directory:

```text
pip install -r requirements.txt

python -m export.csv_to_param_yaml ^
  --csv data/parameters.csv ^
  --out drafts/param ^
  --mode named ^
  --udb-root ..\riscv-unified-db ^
  --clean

python -m export.csv_to_param_yaml ^
  --mode new --limit 20 ^
  --udb-root ..\riscv-unified-db ^
  --out drafts/param-new
```

- Drafts under `drafts/param/` (or `--out`). Every file is marked **DRAFT**.  
- Report: `results/export_b_*.json`  
- Schemas: `export/schemas/param_schema.json`

```text
python -m unittest discover -s tests -v
```

---

## Artifact A — multi-model (needs API key)

Not run yet. When a key is available:

1. Pilot on `machine.adoc` in local UDB (`extract.py pilot`) — see `../PHASE1-IMMERSION/06-measured-local/pilot-RUNBOOK.md`  
2. Full second-model run + agreement vs committed `claude-sonnet-4`  
3. Manifest under `manifests/`  

Scaffold: [pipeline/README.md](pipeline/README.md).

---

## Limitations (honest)

- Named params already exist in UDB; B is a **draft export + validation path**, not 83 new architecture parameters.  
- `value_type` alone does not recover enum members or range bounds — drafts leave TODOs.  
- Prefer `--udb-root` for `definedBy` copy.  
- No multi-model metrics until a real second-model run.  
- Do not merge these drafts upstream without SIG / mentor review.

---

## Layout

```text
riscv-param-extraction/   # this folder inside lfx-firstanalysis
  README.md
  docs/metrics.md
  docs/design.md
  docs/WORKLOG-2026-07-22.md
  export/                  # Artifact B
  pipeline/                # Artifact A (scaffold)
  manifests/
  drafts/param/
  drafts/param-new/
  results/
  data/parameters.csv
  tests/
```

Parent repo home: https://github.com/titoatwork/lfx-firstanalysis  
