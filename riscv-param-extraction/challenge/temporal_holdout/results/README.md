# Results — temporal holdout pilot

## Status

| Item | Status |
|------|--------|
| Preregistered manifest / gold / prompts | **Frozen** (before live outputs) |
| Live baseline + treatment (`gpt-4o-mini-2024-07-18`) | **Locked primary** `20260726T164713Z_...` (26/26) — see `PRIMARY_RESULTS.md` |
| Claim level | **Exploratory null / harness demo** — not clean temporal-holdout (v1.2 guidance leakage) |
| Run tree | `runs/<run_id>/` (refuse overwrite) |
| Primary pointer | `PRIMARY_RUN.json` locked once; second primary live run refused |
| Scores | `score_holdout.py` requires validated `RUN_META.json` (not file count alone) |

## Commands

```bash
python challenge/temporal_holdout/scripts/run_live.py --estimate
# pin must match; wrong model exits 2 with no calls
python challenge/temporal_holdout/scripts/run_live.py --live --model gpt-4o-mini-2024-07-18
python challenge/temporal_holdout/scripts/score_holdout.py
# non-primary debug only:
# python challenge/temporal_holdout/scripts/run_live.py --live --debug-run --model gpt-4o-mini-2024-07-18
```

Primary comparison requires 26/26 successful calls, pinned model, prompt version/hash, and exact call set in `RUN_META.json`.
