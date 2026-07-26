# Results — temporal holdout pilot

## Status

| Item | Status |
|------|--------|
| Preregistered manifest / gold / prompts | **Frozen** (before live outputs) |
| Live baseline + treatment (`gpt-4o-mini-2024-07-18`) | **Pending** local `OPENAI_API_KEY` after pre-live gates |
| Run tree | `runs/<run_id>/` (refuse overwrite) |
| Primary pointer | `PRIMARY_RUN.json` only if **26/26** complete |
| Scores | `scored/` after `score_holdout.py` (refuses incomplete primary) |

## Commands

```bash
python challenge/temporal_holdout/scripts/run_live.py --estimate
# pin must match; wrong model exits 2 with no calls
python challenge/temporal_holdout/scripts/run_live.py --live --model gpt-4o-mini-2024-07-18
python challenge/temporal_holdout/scripts/score_holdout.py
```

Primary comparison requires 26/26 successful calls. Incomplete runs keep `failed_attempts/` but are not claimed as the experiment.
