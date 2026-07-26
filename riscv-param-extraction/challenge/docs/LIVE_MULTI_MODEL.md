# Live multi-model matrix

## Status (2026-07-26)

**Live OpenAI dual-model run is committed** under `results/live/`:

| Model | CMO | CSR |
|-------|-----|-----|
| `gpt-4o-mini-2024-07-18` | 1 (under-extract) | false positive |
| `gpt-4o-2024-11-20` | 1 (under-extract) | zero (correct) |

See [`../results/live/MANIFEST.md`](../results/live/MANIFEST.md).  
**Not yet:** Anthropic Sonnet/Opus or open-weight (GLM/Ollama) legs — Anshul still leads model-family breadth.

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

Recommended full matrix (match/beat Anshul breadth):

| Leg | Model | Role | Status |
|-----|--------|------|--------|
| 1 | gpt-4o-mini | primary cheap | **Done** |
| 2 | gpt-4o (or Sonnet) | stronger / disagreement | **gpt-4o done**; Sonnet needs `ANTHROPIC_API_KEY` |
| 3 | open-weight (GLM / Groq / Ollama) | omission vs hallucination | **Not run** |

After runs: place YAML + `*.evidence.json` under `results/live/<model>/`, then:

```bash
python challenge/scripts/validate.py --results challenge/results/live/<model>
```

**Campaign rules:** key + spend cap + explicit go; `--retries 0`; never commit secrets.
