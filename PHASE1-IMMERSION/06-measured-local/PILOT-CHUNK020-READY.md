# READY — chunk_020 completion (gpt-4o-mini only)

**Status:** READY for key · **zero** new API spend while writing this  
**Goal:** Complete large machine.adoc chunk only · **no** rebill of chunk_021  
**Date:** 2026-07-22  

---

## Why not gpt-4o again

| Fact | Value |
|------|--------|
| Prior failure | org TPM **30 000** for gpt-4o; chunk_020 request **~44 373** |
| Retry gpt-4o | Will fail the same way — **forbidden** as default path |
| Chosen model | **`gpt4o-mini`** → `gpt-4o-mini-2024-07-18` |

## Code changes (local UDB only, not pushed)

In `param_extraction/scripts/extract.py`:

1. Alias **`gpt4o-mini`** added  
2. **`--chunk CHUNK_ID`** (repeatable) on pilot/run — filters to those ids only  

## How chunk_021 is protected from rebill

| Risk | Mitigation |
|------|------------|
| `pilot --model gpt4o-mini` alone would process **both** machine chunks under a new result dir | **Must** pass `--chunk chunk_020` |
| `skip_done` only skips within **same** model display name | Does **not** protect 021 across models — hence `--chunk` is mandatory |
| `--force` | **Never** use |
| Re-run gpt-4o pilot without force | Would skip 021 (success) but **retry 020** and fail TPM again — do not |

## Exact paid command (one call)

```powershell
cd "C:\Users\Ibteshamul Haque\Desktop\LFX-Mentorship\riscv-unified-db"
$env:OPENAI_API_KEY = "<PASTE_ROTATED_KEY>"
$env:PROMPT_VERSION = "v2"
python param_extraction\scripts\extract.py pilot --model gpt4o-mini --chunk chunk_020 --retries 0 -v
# then: Remove-Item Env:OPENAI_API_KEY
```

| Flag | Value |
|------|--------|
| model | `gpt4o-mini` only |
| chunk | **`chunk_020` only** |
| PROMPT_VERSION | **v2** |
| retries | **0** |
| force | **no** |
| Expected paid calls | **1** |

## Results path (after success)

```text
param_extraction/results/v2/gpt-4o-mini/chunk_020.json
```

Existing (leave untouched):

```text
param_extraction/results/v2/gpt-4o/chunk_021.json   # success
param_extraction/results/v2/gpt-4o/chunk_020.json   # failed TPM record
```

## Cost class

- Input ~40k tokens (chunk + v2 system prompt)  
- gpt-4o-mini list-ish pricing is much lower than 4o  
- **Estimate: well under $0.10** for one call; abort if path looks **> ~$0.50**  

## Abort / no auto

- 429 / size / auth → diagnose offline, **no** auto-retry, **no** model hop without user OK  
- Do not start Artifact A  

## After success (agent)

1. Update `pilot-manifest.md` → `COMPLETE_WITH_MODEL_SPLIT`  
2. Update PROGRESS / PHASE1-STATUS  
3. Honest claim: 021 = gpt-4o; 020 = gpt-4o-mini (TPM)  
4. Unset key · STOP  

---

**API key please — one large-chunk attempt only** (`gpt4o-mini` + `--chunk chunk_020`).  
Prefer a **rotated** key if the previous one was pasted in chat.
