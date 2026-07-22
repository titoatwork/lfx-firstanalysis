# Pilot manifest (fill AFTER real run only)

Do not invent numbers. Leave blank until pilot succeeds.

```text
date:
model_alias: gpt4o
model_id: gpt-4o-2024-11-20
prompt_version: v2
command: python param_extraction\scripts\extract.py pilot --model gpt4o --retries 0 -v
env: PROMPT_VERSION=v2  OPENAI_API_KEY=(session env only)

chunks_processed:
  - chunk_020:
      input_tokens:
      output_tokens:
      params_found:
      path: param_extraction/results/v2/gpt-4o/chunk_020.json
  - chunk_021:
      input_tokens:
      output_tokens:
      params_found:
      path: param_extraction/results/v2/gpt-4o/chunk_021.json

total_input_tokens:
total_output_tokens:
approx_cost_usd:
latency_notes:
errors:
budget_remaining_note: ($5 OpenAI credits minus this pilot; do not start A without user OK)
notes:
```
