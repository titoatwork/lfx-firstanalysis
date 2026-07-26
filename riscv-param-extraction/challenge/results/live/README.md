# Live multi-model results

Live LLM runs on the two challenge snippets (not curated CI gold).

| Dir | Provider | Role |
|-----|----------|------|
| `nemotron-3-ultra-550b-a55b-free/` | OpenRouter free | CMO=3, CSR=0 — best free OR |
| `nemotron-3-super-120b-a12b-free/` | OpenRouter free | CMO=3, CSR empty→0 |
| `ling-3.0-flash-free/` | OpenRouter free | CMO=3, CSR=0 |
| `nemotron-3-nano-30b-a3b-free/` | OpenRouter free | CMO=1 under-extract |
| `gemini-3.6-flash/` | Google free | CMO=3, CSR=0 |
| `llama-3.3-70b-versatile/` | Groq free | CMO=3; CSR 5 FP |
| `gpt-4o-mini-2024-07-18/` | OpenAI | CMO=1; CSR FP |
| `gpt-4o-2024-11-20/` | OpenAI | CMO=1; CSR=0 |
| `_raw/` | — | unmodified API text (+ usage meta, no keys) |
| `MANIFEST.md` | — | run facts, matrix, honesty |

**Read MANIFEST first.** Curated ≠ live. Keys never committed.
