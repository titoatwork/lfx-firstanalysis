# Live multi-model results

Live LLM runs on the two challenge snippets (not curated CI gold).

| Dir | Provider | Role |
|-----|----------|------|
| `nemotron-3-ultra-550b-a55b-free/` | OpenRouter free (NVIDIA) | CMO=3, CSR=0 — best free OR model |
| `gemini-3.6-flash/` | Google free tier | CMO=3, CSR=0 |
| `llama-3.3-70b-versatile/` | Groq free tier | CMO=3; CSR 5 false positives (honest) |
| `gpt-4o-mini-2024-07-18/` | OpenAI | CMO under-extract; CSR false positive |
| `gpt-4o-2024-11-20/` | OpenAI | CMO under-extract; CSR=0 |
| `_raw/` | — | unmodified API text (+ usage meta, no keys) |
| `MANIFEST.md` | — | run facts, matrix, honesty |

**Read MANIFEST first.** Curated ≠ live. Keys never committed.
