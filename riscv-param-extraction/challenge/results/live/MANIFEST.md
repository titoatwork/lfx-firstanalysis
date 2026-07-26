# Live multi-model run — challenge snippets

**Date:** 2026-07-26  
**Prompt:** `challenge/prompts/v3_schema_constrained.md` (v3)  
**Snippets:** `cmo_cache_block.txt` (Priv 19.3.1) · `csr_address_mapping.txt` (Priv 2.1)  
**API:** OpenAI Chat Completions · `temperature=0` · `--retries 0`  
**Runner:** `challenge/scripts/extract.py --live`  
**Raw responses:** `_raw/`  

## Honesty

- This is a **live** matrix on the **two challenge snippets**, not the 60-chunk corpus Artifact A.
- Only **OpenAI** models were available for this run (single provider key). **Not** Sonnet/Opus/GLM.
- `definedBy` extension gating was normalized to schema-valid UDB shape when the model emitted a free-form string; parameter **names/quotes/descriptions** reflect live model content.
- Curated `results/curated/` remains the CI reference; live dirs are comparative evidence.

## Matrix

| Model | CMO params emitted | CSR negative control | Notes |
|-------|-------------------:|----------------------|-------|
| **gpt-4o-mini-2024-07-18** | **1** (`CACHE_BLOCK_SIZE` only) | **FAIL** — false positive `CSR_ACCESSIBILITY_ENCODING` | Under-extract on CMO; over-trigger on CSR |
| **gpt-4o-2024-11-20** | **1** (`CACHE_BLOCK_SIZE` only) | **PASS** — zero params | Under-extract on CMO vs curated 3; correct CSR=0 |
| curated (reference, not live LLM) | 3 | PASS (zero file) | CI gold |

## Comparison to Anshul (challenge axis)

Anshul publishes Sonnet/Opus/GLM dirs. We now publish **live** OpenAI dual-model dirs with:
- mechanical validate on schema+quote where YAML exists
- **honest** mini CSR false positive (do not hide)
- raw API text retained under `_raw/`

Still weaker on **model-family breadth** (no Anthropic/open-weight leg yet). Stronger on **corpus science** outside this pack (see monorepo `docs/metrics.md`).

## Validate commands

```bash
cd riscv-param-extraction
python challenge/scripts/validate.py --results challenge/results/live/gpt-4o-2024-11-20
python challenge/scripts/validate.py --results challenge/results/live/gpt-4o-mini-2024-07-18
```

## Cost

Snippet-scale only (4 completion calls: 2 models × 2 snippets). On the order of **cents**.
