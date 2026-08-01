# pipeline/ — Artifact A (multi-model, offline analysis)

Thin, domain-named tools. **No LLM calls here.**

| Module | Role |
|--------|------|
| `load_results.py` | Load merged or deduped Part I JSON; UDB name sets |
| `agreement.py` | Name agreement + high-conf proposed-new overlap |
| `compare_models.py` | CLI → markdown tables + JSON summary |
| `stage_for_analyze.py` | Stage extract results for `analyze.py`; optional GT185 restore |

## Plan

See [../manifests/artifact-a-plan.md](../manifests/artifact-a-plan.md).

## Offline self-check (Claude vs Claude)

```powershell
cd riscv-param-extraction
python -m pipeline.compare_models `
  --a ..\riscv-unified-db\param_extraction\results\v2\deduped_claude-sonnet-4.json `
  --b ..\riscv-unified-db\param_extraction\results\v2\deduped_claude-sonnet-4.json `
  --model-a claude-sonnet-4 --model-b claude-sonnet-4 `
  --udb-param-dir ..\riscv-unified-db\spec\std\isa\param
```

Expect Jaccard **100%** and full class agreement on shared names.

## After a second-model run

1. `extract.py merge --model gpt4o-mini` (with `PROMPT_VERSION=v2`)
2. `python -m pipeline.stage_for_analyze --model-display gpt-4o-mini --restore-gt185`
3. `analyze.py all --model gpt-4o-mini`
4. `python -m pipeline.compare_models --a <claude deduped> --b <mini deduped> ...`
5. Update `docs/metrics.md` §5 + `manifests/artifact-a-gpt-4o-mini.md`

Do not invent multi-model metrics without a real second-model run.
