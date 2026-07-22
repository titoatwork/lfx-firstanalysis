# Pilot manifest — ACCEPTED PARTIAL (2026-07-22)

**Decision (user):** Option 3 — accept partial pilot; do **not** re-spend to force `chunk_020`. Save remaining OpenAI credits for Artifact A later.

Key: session env only for the run; **not** stored here. Rotate key if it was exposed in chat.

```text
date: 2026-07-22
status: ACCEPTED_PARTIAL
decision: option_3_no_retry_chunk_020
model_alias: gpt4o
model_id: gpt-4o-2024-11-20
prompt_version: v2
command: python param_extraction\scripts\extract.py pilot --model gpt4o --retries 0 -v
branch: lfx-1832
retries_flag: 0
force: no

chunks:
  - chunk_020:
      status: FAILED_ACCEPTED
      error: 429 rate_limit_exceeded — org TPM Limit 30000, Requested ~44373 for gpt-4o-2024-11-20
      input_tokens: 0
      output_tokens: 0
      params_found: 0
      path: param_extraction/results/v2/gpt-4o/chunk_020.json
  - chunk_021:
      status: OK
      input_tokens: 10115
      output_tokens: 1152
      params_found: 6
      path: param_extraction/results/v2/gpt-4o/chunk_021.json
      parameter_names:
        - PMP_GRANULARITY
        - PMP_HARDWIRED_PRIVILEGES
        - PMP_CHECKS_ON_M_MODE
        - NUM_PMP_ENTRIES
        - PMPADDR_WIDTH
        - PMP_REGION_GRAIN

total_input_tokens: 10115
total_output_tokens: 1152
approx_cost_usd: ~0.037
budget_note: most of ~$5 OpenAI credits remain for later Artifact A (user-authorized only)

honest_claim_for_application:
  "Ran Part I extract.py pilot on machine.adoc with gpt-4o (v2 prompts).
   Smaller chunk (chunk_021) succeeded (6 params; 10115+1152 tokens; ~$0.04).
   Larger chunk (chunk_020) blocked by OpenAI org TPM tier (30k limit vs ~44k request)
   — documented, not silently ignored. Pipeline + OpenAI path verified; full machine.adoc
   coverage deferred pending tier upgrade or re-chunk (not done this session)."

non_claims:
  - Do NOT claim full machine.adoc pilot complete
  - Do NOT invent params for chunk_020
  - Do NOT claim multi-model Artifact A done
```
