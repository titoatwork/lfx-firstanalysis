# Artifact A — offline plan (Obj 1 + 3)

**Status:** READY for paid gate (STEP 3)  
**Date planned:** 2026-07-24  
**Branch (monorepo):** `analysis/artifact-a`  
**UDB clone:** `riscv-unified-db/` · branch **`lfx-1832`** (local, gitignored)  
**No secrets in this file.**

---

## Goal (locked)

Second-model extraction with **gpt-4o-mini** (`PROMPT_VERSION=v2`) over the Part I **param-bearing** chunk set, then:

1. Per-class recall / class accuracy vs **GT185** (Part I freeze) via `analyze.py`  
2. Inter-model **agreement** vs committed **claude-sonnet-4** v2 results  
3. **Hallucination-overlap** (high-conf proposed-new both vs one)  
4. Manifest with tokens, cost, command, skips  

Honest numbers if mini is worse than Claude. **Not** a pure gpt-4o multi-model matrix.

---

## Verified ground state (this machine)

| Check | Result |
|-------|--------|
| UDB on `lfx-1832` | Yes |
| `extract.py` / `analyze.py` | Present; `--help` OK |
| `gpt4o-mini` alias + `--chunk` | Present (local extract.py) |
| Chunks | 79 total · **60** param-bearing (Claude complete) |
| Claude v2 baseline | `results/v2/all_results_claude-sonnet-4.json` + deduped + metrics **72.9%** |
| GT live working tree | **223** (dirty remeasure) — **do not** use for headline A vs Part I |
| GT at `HEAD` on lfx-1832 | **185** (restore before analyze) |
| Pilot mini | `v2/gpt-4o-mini/chunk_020.json` only (will be **skipped** without `--force`) |
| Pilot gpt-4o | chunk_021 OK; chunk_020 error (TPM) — irrelevant to mini A path |

### Token inventory (content estimate ≈ chars/3.8)

| Item | Value |
|------|------:|
| Param-bearing chunks | 60 |
| Content-only est. tokens (sum) | ~469k |
| Claude v2 actual (status) | **1,030,983** in · **83,189** out |
| TPM-risky for **gpt-4o** (≥~28k content) | chunk_015, **020**, 055, 058 |
| Default A model | **gpt-4o-mini** (cleared ~44k pilot input) |

Full list: `results/artifact_a_chunk_inventory.json`.

---

## Cost estimate (pre-run; not a claim of spend)

Using Claude-scale token totals as the best available proxy and **list** gpt-4o-mini rates  
(~**$0.15 / 1M input**, ~**$0.60 / 1M output** — verify at run time):

| Item | Estimate |
|------|----------|
| Input ~1.03M | ~$0.15 |
| Output ~83k | ~$0.05 |
| **Full-ish mini total** | **~$0.20–0.35** (buffer for prompt drift / retries-off) |
| Already paid (chunk_020 pilot) | ~$0.008 — skipped on re-run |
| Cap to request | **$4.50** hard stop (leave buffer under ~$5 campaign budget) |

If burn rate after first **5** new chunks implies total **>$4.50**, **STOP and ask**.

---

## Exact commands (paid — only after key + cap)

```powershell
cd <workspace>\riscv-unified-db
# Key: put OPENAI_API_KEY in .env (gitignored) OR set in session — never commit/echo
git check-ignore .env   # must print .env if using file
$env:PROMPT_VERSION = "v2"
# $env:OPENAI_API_KEY = "<session only>"

python param_extraction\scripts\extract.py status
python param_extraction\scripts\extract.py run --model gpt4o-mini --retries 0 -v
# Optional first batch (measure burn):
# python param_extraction\scripts\extract.py run --model gpt4o-mini --retries 0 --chunk chunk_001 --chunk chunk_002 -v

python param_extraction\scripts\extract.py merge --model gpt4o-mini
```

### Post-run (offline)

```powershell
cd <workspace>\riscv-param-extraction

# Stage v2 merge where analyze.py expects it; restore GT185
python -m pipeline.stage_for_analyze --model-display gpt-4o-mini --restore-gt185 --udb-root ..\riscv-unified-db

cd ..\riscv-unified-db
python param_extraction\scripts\analyze.py all --model gpt-4o-mini -v

cd ..\riscv-param-extraction
# Prefer GT185 freeze for "new" filter when available; else live yaml dir
python -m pipeline.compare_models `
  --a ..\riscv-unified-db\param_extraction\results\v2\deduped_claude-sonnet-4.json `
  --b ..\riscv-unified-db\param_extraction\results\deduped_gpt-4o-mini.json `
  --model-a claude-sonnet-4 --model-b gpt-4o-mini `
  --udb-gt ..\riscv-unified-db\param_extraction\data\ground_truth.json `
  --out results\artifact_a_agreement.json `
  --md-out results\artifact_a_tables.md
```

Note: after `analyze.py`, deduped/metrics land under `param_extraction/results/` (not `v2/`). Claude baseline for agreement stays the **v2** committed deduped file.

---

## Abort / skip rules

| Event | Action |
|-------|--------|
| Auth error | Stop; re-check key load (never print key) |
| TPM / limit on mini | Skip chunk; record in manifest; do **not** switch to gpt-4o without new gate |
| Parse failure | Diagnose offline; **no** auto re-spend |
| Projected total > cap | Stop and ask |
| Urge to re-pilot / re-Claude | **Forbidden** |

---

## Offline scaffold delivered (this step)

| Path | Role |
|------|------|
| `pipeline/agreement.py` | Name agreement + hallucination-overlap |
| `pipeline/compare_models.py` | CLI → markdown + JSON |
| `pipeline/stage_for_analyze.py` | v2 → analyze.py path + GT185 restore |
| `pipeline/load_results.py` | Load merged/deduped |
| `tests/test_agreement.py` | Unit tests ($0) |
| `manifests/artifact-a-gpt-4o-mini.md` | Run manifest template |
| `results/artifact_a_chunk_inventory.json` | Chunk sizes |

---

## READY gate summary

| Item | Value |
|------|--------|
| Chunks to extract (param) | 60 (1 already done → **59** new if skip_done) |
| Model | `gpt4o-mini` → `gpt-4o-mini-2024-07-18` |
| Prompt | `PROMPT_VERSION=v2` |
| Retries | **0** |
| Force | **no** |
| Est. cost | **~$0.20–0.35** |
| Requested cap | **$4.50** |
| Command | `extract.py run --model gpt4o-mini --retries 0 -v` |

**Next:** STEP 3 — need user API key + explicit spend approval (see session ask block).
