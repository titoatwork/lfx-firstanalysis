# Manifest — machine.adoc pilot (Obj 3)

**Status:** `COMPLETE_WITH_MODEL_SPLIT`  
**Date:** 2026-07-22  
**Repo:** [titoatwork/lfx-firstanalysis](https://github.com/titoatwork/lfx-firstanalysis) · folder `riscv-param-extraction/`  
**No secrets.** API keys never stored in this file.

---

## Claim (honest)

machine.adoc pilot completed with a **model split**:

| Chunk | Model | Why |
|-------|--------|-----|
| `chunk_021` | **gpt-4o** (`gpt-4o-2024-11-20`) | Succeeded first |
| `chunk_020` | **gpt-4o-mini** (`gpt-4o-mini-2024-07-18`) | gpt-4o org **TPM 30 000** rejected ~**44 373** input tokens |

Do **not** claim a pure gpt-4o full machine.adoc pilot. Pipeline + OpenAI path verified; total pilot spend ~**$0.05**.

---

## Run configuration

| Field | Value |
|-------|--------|
| Upstream tree | local `riscv-unified-db` checkout, branch **`lfx-1832`** |
| Tool | Part I `param_extraction/scripts/extract.py` |
| Prompt | **`PROMPT_VERSION=v2`** |
| Retries | **0** |
| Force | **no** |
| chunk_021 rebill on mini run | **no** (`--chunk chunk_020` only) |

### Commands (reproduce with your own key)

```powershell
cd <path-to>/riscv-unified-db
$env:PROMPT_VERSION = "v2"
$env:OPENAI_API_KEY = "<your key, not committed>"

# chunk_021 (gpt-4o) — historical command form
python param_extraction\scripts\extract.py pilot --model gpt4o --retries 0 -v
# (machine.adoc both chunks; 020 failed TPM, 021 succeeded)

# chunk_020 only (gpt-4o-mini) — completion
python param_extraction\scripts\extract.py pilot --model gpt4o-mini --chunk chunk_020 --retries 0 -v
```

Local code note: `gpt4o-mini` alias + `--chunk` filter were added on the local UDB tree for the completion run (not an upstream merge).

---

## Results

### chunk_021 — gpt-4o

| Field | Value |
|-------|------:|
| Status | OK |
| Input tokens | 10 115 |
| Output tokens | 1 152 |
| Params found | **6** |
| Approx cost (USD) | ~0.037 |
| Result pattern | `param_extraction/results/v2/gpt-4o/chunk_021.json` |

Parameters: `PMP_GRANULARITY`, `PMP_HARDWIRED_PRIVILEGES`, `PMP_CHECKS_ON_M_MODE`, `NUM_PMP_ENTRIES`, `PMPADDR_WIDTH`, `PMP_REGION_GRAIN`

### chunk_020 — gpt-4o-mini

| Field | Value |
|-------|------:|
| Status | OK |
| Input tokens | 44 874 |
| Output tokens | 1 541 |
| Params found | **9** |
| Approx cost (USD) | ~0.008 |
| Result pattern | `param_extraction/results/v2/gpt-4o-mini/chunk_020.json` |

Parameters: `MISA_EXTENSIONS`, `COUNTINHIBIT_EN`, `MTVEC_MODES`, `M_MODE_ENDIANNESS`, `REPORT_ENCODING_IN_MTVAL_ON_ILLEGAL_INSTRUCTION`, `MCONFIGPTR_OPTIONAL`, `MIMPID_IMPLEMENTED`, `MHARTID_IMPLEMENTED`, `MSTATUS_MIE_MPRV_RESET`

### Totals

| Field | Value |
|-------|------:|
| Successful paid calls | 2 |
| Failed gpt-4o attempt on 020 (earlier) | 1 (TPM; ~$0 generation) |
| Total input tokens (success) | 54 989 |
| Total output tokens (success) | 2 693 |
| Approx total pilot USD | **~0.05** |

Compact name list: [results/pilot/param-names-summary.json](../results/pilot/param-names-summary.json)

---

## Limitations

- Not multi-model **Artifact A** (full corpus vs Claude).  
- Not full-corpus `extract.py run`.  
- Result JSON remains on the local UDB tree (large); this repo keeps **names + tokens + cost** only.  
- Cost figures are approximate from published list-style rates, not a billing CSV.  

