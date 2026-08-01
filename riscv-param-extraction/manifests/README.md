# manifests/ — reproducible run records

One file per serious extraction or analysis run. **No API keys. No secrets.**

| Manifest | Status |
|----------|--------|
| [pilot-machine-adoc.md](./pilot-machine-adoc.md) | **COMPLETE_WITH_MODEL_SPLIT** (2026-07-22) |
| [artifact-a-plan.md](./artifact-a-plan.md) | Offline plan + READY gate (2026-07-24) |
| [artifact-a-gpt-4o-mini.md](./artifact-a-gpt-4o-mini.md) | **COMPLETE** (2026-07-24/25). 60 chunks, ~$0.16; worse recall than Claude |
| [stretch-c-v3-warl.md](./stretch-c-v3-warl.md) | **COMPLETE null** (2026-07-25), prompt v3 WARL; WARL 3/24→2/24 |
| Artifact B | validation reports under `../results/export_b_*.json` |
| Artifact C | preregistration + results under `../artifact_c/` |

Suggested fields for new runs:

```text
date:
artifact:          # pilot | A | B | C | other
model_alias:
model_id:
prompt_version:
command:
input_tokens:
output_tokens:
approx_cost_usd:
notes:
```
