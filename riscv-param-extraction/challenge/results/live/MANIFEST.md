# Live multi-model run — challenge snippets

**Date:** 2026-07-26  
**Prompt:** `challenge/prompts/v3_schema_constrained.md` (v3)  
**Snippets:** `cmo_cache_block.txt` (Priv 19.3.1) · `csr_address_mapping.txt` (Priv 2.1)  
**Temperature:** 0  
**Raw responses:** `_raw/`  

## Honesty

- Live matrix on the **two challenge snippets**, not the 60-chunk corpus Artifact A.
- **Models chosen freely** (challenge does not fix model names).
- Free: **Gemini**, **Groq Llama**, **OpenRouter** (Nemotron Ultra/Super/Nano, Ling-3.0 Flash) + usage **OpenAI**. **Not** Sonnet/Opus/GLM.
- `definedBy` normalized to schema-valid UDB shape when models emitted free-form strings.
- Curated `results/curated/` remains CI gold; live dirs are comparative evidence.
- **API keys never committed.**
- Some free models returned literal `(No output)` on CSR; documented and treated as zero with caveat.

## Matrix

| Model | Provider | CMO | CSR negative control | Notes |
|-------|----------|----:|----------------------|-------|
| **nvidia/nemotron-3-ultra-550b-a55b:free** | OpenRouter free | **3** | **PASS** | Best free OR; full CMO + clean CSR |
| **nvidia/nemotron-3-super-120b-a12b:free** | OpenRouter free | **3** | **PASS*** | *CSR API returned `(No output)`; treated as zero |
| **inclusionai/ling-3.0-flash:free** | OpenRouter free | **3** | **PASS** | Explicit empty list / no-params |
| **nvidia/nemotron-3-nano-30b-a3b:free** | OpenRouter free | **1** | **PASS*** | Under-extract CMO; CSR `(no output)` |
| **gemini-3.6-flash** | Google free | **3** | **PASS** | Strong free Google |
| **llama-3.3-70b-versatile** | Groq free | **3** | **FAIL** 5 FP | Open-weight precision fail |
| **gpt-4o-2024-11-20** | OpenAI | **1** | **PASS** | Under-extract CMO |
| **gpt-4o-mini-2024-07-18** | OpenAI | **1** | **FAIL** 1 FP | Under-extract + CSR fail |
| curated (not live) | — | 3 | PASS | CI gold |

## Comparison to Anshul (challenge axis)

| Axis | Anshul | Us now |
|------|--------|--------|
| Live multi-model dirs | Sonnet / Opus / GLM (3) | **8 live models** across 4 providers |
| Free strong legs | GLM playground | **Nemotron Ultra + Gemini + Ling** (CMO=3, CSR pass) |
| CSR all models pass | Yes | **No** — mini + Llama fail (honest) |
| Merged UDB PR | #1967 | Still draft only |

Corpus GT / export / WARL null: monorepo Path B (`docs/metrics.md`).

## Validate

```bash
cd riscv-param-extraction
python challenge/scripts/validate.py --results challenge/results/live/nemotron-3-ultra-550b-a55b-free
python challenge/scripts/validate.py --results challenge/results/live/nemotron-3-super-120b-a12b-free
python challenge/scripts/validate.py --results challenge/results/live/ling-3.0-flash-free
python challenge/scripts/validate.py --results challenge/results/live/nemotron-3-nano-30b-a3b-free
python challenge/scripts/validate.py --results challenge/results/live/gemini-3.6-flash
python challenge/scripts/validate.py --results challenge/results/live/llama-3.3-70b-versatile
python challenge/scripts/validate.py --results challenge/results/live/gpt-4o-2024-11-20
python challenge/scripts/validate.py --results challenge/results/live/gpt-4o-mini-2024-07-18
```

## Cost

- OpenAI: cents. Free providers: rate limits only.
- Laguna S / Gemma free were **429 rate-limited** at probe time — not run.
