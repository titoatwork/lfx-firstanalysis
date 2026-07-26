# Live multi-model results

Live LLM runs on the two challenge snippets (not curated CI gold).

| Dir | Provider | Role |
|-----|----------|------|
| `gemini-3.6-flash/` | Google free tier | best free model on key; CMO=3, CSR=0 |
| `gpt-4o-mini-2024-07-18/` | OpenAI | cheap leg; CSR false positive (honest) |
| `gpt-4o-2024-11-20/` | OpenAI | stronger OpenAI; CSR=0, CMO under-extract |
| `_raw/` | — | unmodified API text (+ usage meta, no keys) |
| `MANIFEST.md` | — | run facts, matrix, honesty |

**Read MANIFEST first.** Curated ≠ live. Keys never committed.
