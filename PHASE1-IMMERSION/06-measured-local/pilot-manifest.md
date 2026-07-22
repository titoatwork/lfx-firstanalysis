# Pilot manifest — COMPLETE_WITH_MODEL_SPLIT (2026-07-22)

**Canonical public copy (mentor-facing):**  
[`riscv-param-extraction/manifests/pilot-machine-adoc.md`](../../riscv-param-extraction/manifests/pilot-machine-adoc.md)  
Metrics tables: [`riscv-param-extraction/docs/metrics.md`](../../riscv-param-extraction/docs/metrics.md)

**Status:** machine.adoc pilot coverage complete via **honest model split**  
**No secrets in this file.** Key was session env only; unset after runs. Rotate if exposed in chat.

## Honest claim (use this language)

> Ran Part I `extract.py` pilot on `machine.adoc` with `PROMPT_VERSION=v2`.  
> - **chunk_021** → **gpt-4o** (`gpt-4o-2024-11-20`): success (6 params).  
> - **chunk_020** → **gpt-4o-mini** (`gpt-4o-mini-2024-07-18`): success (9 params), because org **gpt-4o TPM 30k** rejected the ~44k request.  
> Do **not** claim a pure gpt-4o full machine.adoc pilot.

```text
date: 2026-07-22
status: COMPLETE_WITH_MODEL_SPLIT
prompt_version: v2
branch: lfx-1832
retries_flag: 0
force: no

--- chunk_021 (earlier same day) ---
model_alias: gpt4o
model_id: gpt-4o-2024-11-20
status: OK
input_tokens: 10115
output_tokens: 1152
params_found: 6
approx_cost_usd: ~0.037
path: param_extraction/results/v2/gpt-4o/chunk_021.json
parameter_names:
  - PMP_GRANULARITY
  - PMP_HARDWIRED_PRIVILEGES
  - PMP_CHECKS_ON_M_MODE
  - NUM_PMP_ENTRIES
  - PMPADDR_WIDTH
  - PMP_REGION_GRAIN

--- chunk_020 (completion run) ---
model_alias: gpt4o-mini
model_id: gpt-4o-mini-2024-07-18
status: OK
command: python param_extraction\scripts\extract.py pilot --model gpt4o-mini --chunk chunk_020 --retries 0 -v
input_tokens: 44874
output_tokens: 1541
params_found: 9
approx_cost_usd: ~0.008  (gpt-4o-mini list-style ~$0.15/1M in + $0.60/1M out)
path: param_extraction/results/v2/gpt-4o-mini/chunk_020.json
parameter_names:
  - MISA_EXTENSIONS
  - COUNTINHIBIT_EN
  - MTVEC_MODES
  - M_MODE_ENDIANNESS
  - REPORT_ENCODING_IN_MTVAL_ON_ILLEGAL_INSTRUCTION
  - MCONFIGPTR_OPTIONAL
  - MIMPID_IMPLEMENTED
  - MHARTID_IMPLEMENTED
  - MSTATUS_MIE_MPRV_RESET
why_not_gpt4o: org TPM Limit 30000 for gpt-4o; Requested ~44373

--- totals (pilot machine.adoc, both models) ---
total_paid_calls: 2 successful + 1 failed gpt-4o attempt on 020 earlier
total_input_tokens_success: 54989
total_output_tokens_success: 2693
approx_total_pilot_usd: ~0.05
chunk_021_rebilled: no
full_corpus_run: no
artifact_A: not started

local_code_note: extract.py gained gpt4o-mini alias + --chunk filter (UDB local only; not pushed)
```
