# Manifest — Stretch C ablation (prompt v3 WARL)

**Status:** `COMPLETE` (honest **null / negative** for WARL recall)  
**Date:** 2026-07-25 (IST)  
**Artifact:** Stretch C-adjacent, prompt-only WARL guidance (not CSR-field aux context)  
**Repo:** [titoatwork/lfx-firstanalysis](https://github.com/titoatwork/lfx-firstanalysis) · `riscv-param-extraction/`  
**No secrets.**

---

## Claim (honest)

Full Part I param-bearing corpus on **gpt-4o-mini** with **PROMPT_VERSION=v3** (v2 system prompt + structural WARL recognition section; no ground-truth parameter names injected).  

Compared to Artifact A mini under **v2**:

| Metric | v2 (A) | v3 | Note |
|--------|-------:|---:|------|
| Adj recall GT185 | 32.2% | **35.0%** | slight overall lift |
| WARL recall | **12.5%** (3/24) | **8.3%** (2/24) | **worse**. Null Stretch C |

**Not** a successful WARL recall attack. **Not** full gpt-4o. **Not** CSR-field YAML aux context (that path remains untested).

---

## Run configuration

| Field | Value |
|-------|--------|
| Upstream tree | local `riscv-unified-db`, branch **`lfx-1832`** |
| Tool | Part I `param_extraction/scripts/extract.py` |
| Model alias | `gpt4o-mini` |
| Model id | `gpt-4o-mini-2024-07-18` |
| Prompt version | **v3** |
| Retries | **0** |
| Force | **no** (error stubs retried; good chunks skipped) |
| Chunk set | 60 param-bearing |

### Commands

```powershell
cd <path-to>/riscv-unified-db
$env:PROMPT_VERSION = "v3"
# OPENAI_API_KEY session-only
python param_extraction\scripts\extract.py run --model gpt4o-mini --retries 0 --delay 1.0
python param_extraction\scripts\extract.py merge --model gpt4o-mini
# offline stage + analyze vs GT185
Copy-Item param_extraction\results\v3\all_results_gpt-4o-mini.json param_extraction\results\
git checkout HEAD -- param_extraction/data/ground_truth.json
python param_extraction\scripts\analyze.py --model gpt-4o-mini all
```

---

## Tokens / cost

| Field | Value |
|------:|
| Input tokens | **901 796** |
| Output tokens | **48 731** |
| Approx cost (USD) | **~$0.16** |
| Chunks OK | **60** |
| Chunks errors | **0** (after resume) |

### Ops notes

- First pass died mid-run on **401 invalid API key** (~21 then residual errors).  
- Resume skipped done chunks; completed 60/60.  
- Do not run two `extract.py` processes in parallel (race on result JSON).

---

## Analysis outputs

| Artifact | Path |
|----------|------|
| Merged (local UDB) | `param_extraction/results/v3/all_results_gpt-4o-mini.json` |
| Metrics | monorepo `results/metrics_gpt-4o-mini.v3.json` |
| Public tables | `docs/metrics.md` §6 |

---

## Limitations

- Prompt-only WARL essay is **insufficient** for Stretch C on this model.  
- Next WARL work should try CSR-field aux context or stronger model, only with user spend OK.  
- Class accuracy denominators remain small (exact name matches).  
