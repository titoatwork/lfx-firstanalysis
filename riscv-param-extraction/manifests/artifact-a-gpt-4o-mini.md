# Manifest — Artifact A (gpt-4o-mini)

**Status:** `COMPLETE`  
**Date:** 2026-07-24 → 2026-07-25 (IST)  
**Artifact:** A (multi-model vs Claude-sonnet-4 Part I baseline)  
**Repo:** [titoatwork/lfx-firstanalysis](https://github.com/titoatwork/lfx-firstanalysis) · `riscv-param-extraction/`  
**No secrets.**

> **Condition:** both models received the full 185-name gold catalogue in the prompt, so these are grounding scores. The cross-model disagreement (Jaccard 3.8%) is measured under that shared condition.

---

## Claim (honest)

Second-model extraction with **gpt-4o-mini-2024-07-18** and **PROMPT_VERSION=v2** over all **60** Part I param-bearing chunks; metrics vs **GT185**; agreement + hallucination-overlap vs committed Claude v2.  

**gpt-4o-mini adjusted recall 32.2% vs Claude 72.9%**. Worse on all per-class recall rows. Not a pure gpt-4o multi-model matrix.

---

## Run configuration

| Field | Value |
|-------|--------|
| Upstream tree | local `riscv-unified-db`, branch **`lfx-1832`** |
| Monorepo branch | `analysis/artifact-a` |
| Tool | Part I `param_extraction/scripts/extract.py` |
| Model alias | `gpt4o-mini` |
| Model id | `gpt-4o-mini-2024-07-18` |
| Prompt version | **v2** |
| Retries | **0** |
| Force | **no** |
| Chunk set | 60 param-bearing; non-param sources skipped by pipeline |
| Pre-existing skip | `chunk_020` from pilot (not re-billed under `--force`) |

### Command

```powershell
cd <path-to>/riscv-unified-db
$env:PROMPT_VERSION = "v2"
# OPENAI_API_KEY in session or gitignored .env — never committed
python param_extraction\scripts\extract.py run --model gpt4o-mini --retries 0 --delay 1.0
python param_extraction\scripts\extract.py merge --model gpt4o-mini
```

Post-run (offline):

```powershell
cd <monorepo>/riscv-param-extraction
python -m pipeline.stage_for_analyze --model-display gpt-4o-mini --restore-gt185 --udb-root ..\riscv-unified-db
cd ..\riscv-unified-db
python param_extraction\scripts\analyze.py --model gpt-4o-mini all
cd ..\riscv-param-extraction
python -m pipeline.compare_models `
  --a ..\riscv-unified-db\param_extraction\results\v2\deduped_claude-sonnet-4.json `
  --b ..\riscv-unified-db\param_extraction\results\deduped_gpt-4o-mini.json `
  --model-a claude-sonnet-4 --model-b gpt-4o-mini `
  --udb-gt ..\riscv-unified-db\param_extraction\data\ground_truth.json `
  --out results\artifact_a_agreement.json
```

---

## Tokens / cost

| Field | Value |
|------:|
| Input tokens | **868 976** |
| Output tokens | **51 718** |
| Approx cost (USD) | **~$0.16** (list: ~$0.15/M in + ~$0.60/M out) |
| Chunks OK | **60** |
| Chunks errors | **0** |
| Wall clock | ~49 minutes (TPM waits ~60s after large chunks) |

### Skips / errors

| Chunk | Reason |
|-------|--------|
| (none failed) | 0 errors |
| 19 non-param sources | Pipeline skip (same as Part I) |

### Pre-existing (not re-billed at start)

| Chunk | Source |
|-------|--------|
| chunk_020 | pilot 2026-07-22 (gpt-4o-mini); reused |

---

## Analysis outputs

| Artifact | Path |
|----------|------|
| Merged (local UDB) | `param_extraction/results/v2/all_results_gpt-4o-mini.json` |
| Metrics (analyze) | `param_extraction/results/metrics_gpt-4o-mini.json` (also copied under monorepo `results/`) |
| Agreement JSON | `riscv-param-extraction/results/artifact_a_agreement.json` |
| Public tables | `docs/metrics.md` §5 |

### Headline numbers (GT185)

| Metric | gpt-4o-mini |
|--------|------------:|
| Adjusted recall | **32.2%** |
| Class acc (exact only) | 100% (11/11) |
| WARL recall | **12.5%** (3/24) |
| Name Jaccard vs Claude | **3.8%** |
| High-conf new both models | **9** |

---

## Limitations

- Second model is **gpt-4o-mini**, not full gpt-4o.  
- Substantially lower recall than Claude-sonnet-4 under the same v2 pipeline.  
- Class accuracy 100% is on a tiny exact-match set, not a global quality win.  
- Full chunk JSON not published in monorepo (size + noise); manifests + aggregate metrics are public.  
