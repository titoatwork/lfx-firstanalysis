# Live multi-model matrix

## Status (2026-07-26)

**10 live model dirs** under [`results/live/`](../results/live/) — full table in [`MANIFEST.md`](../results/live/MANIFEST.md).

Headline (do not invent beyond MANIFEST):

| Band | Models | CMO / CSR pattern |
|------|--------|-------------------|
| Strong free | Nemotron Ultra, Ling-3.0 Flash, Gemini 3.6 Flash | CMO **3** · CSR **PASS** |
| Free + caveat | Nemotron Super/Nano | CMO 3 or 1 · CSR empty→0 (PASS*) |
| Open-weight fail CSR | Groq Llama 70B, Laguna S, Gemma-4-26B | CMO 3 or 1 · CSR **FAIL** FP |
| OpenAI | gpt-4o, gpt-4o-mini | CMO **1** · gpt-4o CSR PASS · mini CSR FAIL |

**Not run:** Anthropic Sonnet/Opus (no key). Direct DeepSeek (insufficient balance). Some free OR probes 429/empty (e.g. Gemma-4-31B).

Offline we also ship: curated gold + CSR=0, multi-strategy matrix, denser fail-closed CI.

## One-command dry-run (no spend)

```bash
cd riscv-param-extraction
python challenge/scripts/extract.py --snippet challenge/snippets/cmo_cache_block.txt
python challenge/scripts/extract.py --snippet challenge/snippets/csr_address_mapping.txt
```

## Live (spend go required)

```bash
set OPENAI_API_KEY=...   # user shell only; never commit
python challenge/scripts/extract.py --snippet challenge/snippets/cmo_cache_block.txt --live --model gpt-4o-mini-2024-07-18 --retries 0
```

OpenRouter / Groq / Gemini use their own keys and base URLs (see MANIFEST for models already shipped).

After runs: place YAML + `*.evidence.json` under `results/live/<model>/`, then:

```bash
python challenge/scripts/validate.py --results challenge/results/live/<model>
```

**Campaign rules:** key + spend cap + explicit go; `--retries 0`; never commit secrets.  
**Honesty:** curated ≠ live; live multi-model is snippet-scale only.
