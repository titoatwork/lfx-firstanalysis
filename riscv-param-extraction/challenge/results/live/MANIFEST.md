# Live multi-model run — challenge snippets

**Date:** 2026-07-26  
**Prompt:** `challenge/prompts/v3_schema_constrained.md` (v3)  
**Snippets:** `cmo_cache_block.txt` (Priv 19.3.1) · `csr_address_mapping.txt` (Priv 2.1)  
**Temperature:** 0  
**Raw responses:** `_raw/`  

## Honesty

- Live matrix on the **two challenge snippets**, not the 60-chunk corpus Artifact A.
- **Models chosen freely** (challenge does not fix model names).
- Free-tier **Gemini** + free **Groq** + free **OpenRouter (Nemotron Ultra 550B)** + usage **OpenAI**. **Not** Sonnet/Opus/GLM.
- `definedBy` normalized to schema-valid UDB shape when models emitted free-form strings; names/quotes/descriptions reflect live content.
- Curated `results/curated/` remains CI gold; live dirs are comparative evidence.
- **API keys never committed.**

## Matrix

| Model | Provider | CMO params | CSR negative control | Notes |
|-------|----------|----------:|----------------------|-------|
| **nvidia/nemotron-3-ultra-550b-a55b:free** | OpenRouter free | **3** | **PASS** — zero | Best free OpenRouter model (probed first); CMO full + CSR clean |
| **gemini-3.6-flash** | Google AI (free tier) | **3** | **PASS** — zero | Best free Gemini on key; matches curated count |
| **llama-3.3-70b-versatile** | **Groq free tier** | **3** | **FAIL** — 5 false positives | Strongest free Groq chat; CMO full; CSR over-trigger |
| **gpt-4o-mini-2024-07-18** | OpenAI | **1** (`CACHE_BLOCK_SIZE` only) | **FAIL** — 1 false positive | Under-extract CMO; over-trigger CSR |
| **gpt-4o-2024-11-20** | OpenAI | **1** (`CACHE_BLOCK_SIZE` only) | **PASS** — zero | Under-extract CMO vs curated 3 |
| curated (not live LLM) | — | 3 | PASS | CI gold |

## Comparison to Anshul (challenge axis)

| Axis | Anshul | Us now |
|------|--------|--------|
| Live multi-model dirs | Sonnet / Opus / GLM | **5 live models** (OpenAI×2 + Gemini + Groq + Nemotron free) |
| Provider breadth | Anthropic + Zhipu | **OpenAI + Google + Groq + NVIDIA via OpenRouter** |
| CMO recall (snippet) | Sonnet 3; GLM 1 | **Nemotron/Gemini/Llama = 3**; OpenAI = 1 each |
| CSR precision | all pass | Nemotron + Gemini + gpt-4o pass; **mini + Llama fail honestly** |

Corpus GT / export / WARL null still monorepo Path B (`docs/metrics.md`).

## Validate

```bash
cd riscv-param-extraction
python challenge/scripts/validate.py --results challenge/results/live/nemotron-3-ultra-550b-a55b-free
python challenge/scripts/validate.py --results challenge/results/live/gemini-3.6-flash
python challenge/scripts/validate.py --results challenge/results/live/llama-3.3-70b-versatile
python challenge/scripts/validate.py --results challenge/results/live/gpt-4o-2024-11-20
python challenge/scripts/validate.py --results challenge/results/live/gpt-4o-mini-2024-07-18
```

## Cost

- OpenAI: snippet-scale (cents).
- Gemini / Groq / OpenRouter free: rate limits only (no token charge on free models used).
- OpenRouter pick: `nvidia/nemotron-3-ultra-550b-a55b:free` (best free after live probe).
