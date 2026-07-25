# AGENTS.md — `riscv-param-extraction/`

Scoped rules for the public prototype package. Root `AGENTS.md` + `HANDSOFF.md` + `AGENT-RULES.md` still apply.

## Purpose

Mentor-auditable selection surface for LFX Part II:

- Remeasure + pilot evidence (`docs/metrics.md`, `manifests/`)
- Artifact **B**: CSV → draft UDB param YAML + schema validate (**done**)
- Artifact **A**: multi-model agreement vs Claude (**done** — gpt-4o-mini v2)
- Prompt **v3** WARL ablation (**done** — honest null for WARL)

This directory is **not** a separate GitHub product. Home is monorepo `titoatwork/lfx-firstanalysis`.

## Layout

| Path | Role |
|------|------|
| `docs/metrics.md` | Public measured tables only |
| `docs/design.md` | Decisions / non-goals |
| `manifests/` | One file per serious run (Obj 3) |
| `export/` | Artifact B exporter + schemas |
| `drafts/param/`, `drafts/param-new/` | DRAFT YAML only |
| `data/parameters.csv` | Source spreadsheet rows |
| `results/` | Small reports; large dumps stay out |
| `pipeline/` | Artifact A agreement tools |
| `tests/` | Offline unit tests for export |

## Commands (offline B)

```text
pip install -r requirements.txt
python -m export.csv_to_param_yaml --csv data/parameters.csv --out drafts/param --mode named --udb-root ../riscv-unified-db --clean
python -m export.csv_to_param_yaml --mode new --limit 20 --udb-root ../riscv-unified-db --out drafts/param-new --clean
python -m unittest discover -s tests -v
```

`--udb-root` expects a **local** UDB checkout (sibling `../riscv-unified-db` or path user provides). Do not vendor UDB into this monorepo.

## When editing here

- Keep drafts marked **DRAFT**; no unsolicited upstream merge claims
- Every serious paid/offline selection run → update or add a **manifest**
- Update `docs/metrics.md` only with real numbers
- Match domain vocabulary (param / WARL / adjusted recall), not generic chatbot packaging
- Prefer small, tested changes to `export/`; run `unittest` before claiming green

## Do not

- Re-pilot or re-run full multi-model extract without root plan + user spend go-ahead
- Commit API keys or full chunk JSON dumps
- Invent tables; claim named count 97 (use 87 rows / 83 unique)
- Claim v3 “fixed WARL” or mini beat Claude
- Run original CSR-field Artifact C without leakage audit + user spend go

## Presentation order

Follow root `GITHUB-PRESENTATION.md`: numbers → how to run → limitations.  
Pass test: Baum can audit one draft’s provenance; Dingankar can recompute a metric.
