# Results — temporal holdout pilot

## Status

| Item | Status |
|------|--------|
| Preregistered manifest / gold / prompts | **Frozen** (before live outputs) |
| Live baseline + treatment (`gpt-4o-mini-2024-07-18`) | **Pending** local `OPENAI_API_KEY` + spend decision |
| Parsed outputs | `parsed/{baseline,treatment}/` after live run |
| Raw API text (including failures) | `raw/` |
| Scores + review queue | `scored/` after `score_holdout.py` |

**Infra vs model:** files marked `# INFRA_ERROR:` or `*.status.json` with `ok: false` are **excluded** from model metrics (not scored as empty extractions).

## Commands

```bash
python challenge/temporal_holdout/scripts/run_live.py --estimate
python challenge/temporal_holdout/scripts/run_live.py --live --model gpt-4o-mini-2024-07-18
python challenge/temporal_holdout/scripts/score_holdout.py
```

Do not hand-edit model outputs. Null treatment results are publishable.
