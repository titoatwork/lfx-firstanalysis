# Results — temporal holdout pilot

## Status

| Item | Status |
|------|--------|
| Preregistered manifest / gold / prompts | **Frozen** (before live outputs) |
| Live baseline + treatment (`gpt-4o-mini-2024-07-18`) | **Pending** `OPENAI_API_KEY` + explicit spend go |
| Parsed outputs | `parsed/{baseline,treatment}/` after live run |
| Raw API text (including failures) | `raw/` |
| Scores + review queue | `scored/` after `score_holdout.py` |

## Commands

```bash
python challenge/temporal_holdout/scripts/run_live.py --estimate
python challenge/temporal_holdout/scripts/run_live.py --live --model gpt-4o-mini-2024-07-18
python challenge/temporal_holdout/scripts/score_holdout.py
```

Do not hand-edit model outputs. Null treatment results are publishable.
