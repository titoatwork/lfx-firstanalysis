# Live multi-model run — challenge snippets

**Date:** 2026-07-26  
**Prompt:** `challenge/prompts/v3_schema_constrained.md` (v3)  
**Snippets:** `cmo_cache_block.txt` (Priv 19.3.1) · `csr_address_mapping.txt` (Priv 2.1)  
**Temperature:** 0  
**Raw responses:** `_raw/`  

## Honesty

- Live matrix on the **two challenge snippets**, not the 60-chunk corpus Artifact A.
- **Models chosen freely** (challenge does not fix model names).
- Free-tier **Gemini** + free **Groq** (Llama 3.3 70B) + usage **OpenAI**. **Not** Sonnet/Opus/GLM.
- `definedBy` normalized to schema-valid UDB shape when models emitted free-form strings; names/quotes/descriptions reflect live content.
- Curated `results/curated/` remains CI gold; live dirs are comparative evidence.
- **API keys never committed.**

## Matrix

| Model | Provider | CMO params | CSR negative control | Notes |
|-------|----------|----------:|----------------------|-------|
| **gemini-3.6-flash** | Google AI (free tier) | **3** (block + capacity + organization) | **PASS** — zero | Best free Gemini on key; matches curated count |
| **llama-3.3-70b-versatile** | **Groq free tier** | **3** | **FAIL** — 5 false positives | Strongest free chat model on account; CMO full; CSR over-trigger |
| **gpt-4o-mini-2024-07-18** | OpenAI | **1** (`CACHE_BLOCK_SIZE` only) | **FAIL** — 1 false positive | Under-extract CMO; over-trigger CSR |
| **gpt-4o-2024-11-20** | OpenAI | **1** (`CACHE_BLOCK_SIZE` only) | **PASS** — zero | Under-extract CMO vs curated 3 |
| curated (not live LLM) | — | 3 | PASS | CI gold |

## Comparison to Anshul (challenge axis)

| Axis | Anshul | Us now |
|------|--------|--------|
| Live multi-model dirs | Sonnet / Opus / GLM | **Gemini + Groq Llama 70B + OpenAI mini/gpt-4o** |
| Provider breadth | Anthropic + Zhipu | **Google + Groq open-weight + OpenAI** (not a copy of his brands) |
| CMO recall (snippet) | Sonnet 3; GLM 1 | **Gemini 3; Llama 3; OpenAI 1 each** |
| CSR precision | all pass | Gemini + gpt-4o pass; **mini + Llama fail honestly** |

Corpus GT / export / WARL null still monorepo Path B (`docs/metrics.md`).

## Validate

```bash
cd riscv-param-extraction
python challenge/scripts/validate.py --results challenge/results/live/gemini-3.6-flash
python challenge/scripts/validate.py --results challenge/results/live/llama-3.3-70b-versatile
python challenge/scripts/validate.py --results challenge/results/live/gpt-4o-2024-11-20
python challenge/scripts/validate.py --results challenge/results/live/gpt-4o-mini-2024-07-18
```

## Cost

- OpenAI: snippet-scale (cents).
- Gemini: free-tier quota (`gemini-3.6-flash`).
- Groq: free-tier rate limits only (`llama-3.3-70b-versatile` — best free chat model available on the key).
