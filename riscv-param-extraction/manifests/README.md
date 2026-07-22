# manifests/ — Obj 3 (reproducible runs)

One file per serious extraction or analysis run. **No API keys. No secrets.**

| Manifest | Status |
|----------|--------|
| [pilot-machine-adoc.md](./pilot-machine-adoc.md) | **COMPLETE_WITH_MODEL_SPLIT** (2026-07-22) |
| Artifact A | not run yet |
| Artifact B | validation reports under `../results/export_b_*.json` |

Suggested fields for new runs:

```text
date:
artifact:          # pilot | A | B | other
model_alias:
model_id:
prompt_version:
command:
input_tokens:
output_tokens:
approx_cost_usd:
notes:
```
