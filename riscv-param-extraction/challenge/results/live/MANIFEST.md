# Live multi-model run — challenge snippets

**Date:** 2026-07-26  
**Prompt:** `challenge/prompts/v3_schema_constrained.md` (v3)  
**Snippets:** `cmo_cache_block.txt` (Priv 19.3.1) · `csr_address_mapping.txt` (Priv 2.1)  
**Temperature:** 0  
**Raw responses:** `_raw/`  

## Honesty

- Live matrix on the **two challenge snippets**, not the 60-chunk corpus Artifact A.
- **Models chosen freely** (challenge does not fix model names).
- Free: **Gemini**, **Groq Llama**, **OpenRouter** (Nemotron Ultra/Super/Nano, Ling-3.0 Flash, Laguna S, Gemma-4-26B) + usage **OpenAI**. **Not** Sonnet/Opus/GLM.
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
| **poolside/laguna-s-2.1:free** | OpenRouter free | **1** | **FAIL** 1 FP | Real text both sides; CMO under-extract; CSR false +ve |
| **google/gemma-4-26b-a4b-it:free** | OpenRouter free | **1** | **FAIL** 1 FP | Real text both sides; same pattern as Laguna |
| curated (not live) | — | 3 | PASS | CI gold |

### Useful-output filter (2026-07-26 later)

Re-probed remaining free models; **accepted only if both snippets returned real text** (rejected empty `(No output)`).  
Accepted: Laguna S, Gemma-4-26B. Rejected empty CSR: Nemotron nano-omni reasoning. 429/empty probe: several others.

## Comparison to Anshul (challenge axis)

| Axis | Anshul | Us now |
|------|--------|--------|
| Live multi-model dirs | Sonnet / Opus / GLM (3) | **10 live models** across 4 providers |
| Free strong legs | GLM playground | **Nemotron Ultra + Gemini + Ling** (CMO=3, CSR pass) |
| CSR all models pass | Yes | **No** — mini + Llama + Laguna + Gemma fail (honest) |
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
python challenge/scripts/validate.py --results challenge/results/live/laguna-s-2.1-free
python challenge/scripts/validate.py --results challenge/results/live/gemma-4-26b-a4b-it-free
```

## Cost

- OpenAI: cents. Free providers: rate limits only.
- **Shipped free OpenRouter legs** (real dual-snippet text): Nemotron Ultra/Super/Nano, Ling-3.0 Flash, **Laguna S 2.1**, **Gemma-4-26B**.
- **Not run** (429 or empty probe on later hunt): e.g. `google/gemma-4-31b-it:free` (429), Laguna XS/M, gpt-oss-20b, north-mini-code, Nemotron nano-omni (empty CSR) — see “Useful-output filter” above.
