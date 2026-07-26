# Known-parameter mechanics benchmark (n=15)

## What this is

Fifteen parameters that already exist in public UDB, each paired with source prose and a committed `extraction.yaml`. The scorer checks:

1. **Existence** — extraction claims a parameter  
2. **Type fidelity** — `schema.type` matches ground truth when present  
3. **Name match** — stricter optional check  

```bash
cd riscv-param-extraction
python challenge/benchmark/scripts/score_recall.py
```

Latest local run (committed extractions):

| Metric | Value |
|--------|------:|
| Existence | **15/15** |
| Type fidelity | **15/15** |
| Strict name match | **15/15** |

## What this is **not**

- **Not** a blind generalization estimate  
- **Not** equal to Spring corpus adjusted recall (72.9% / 36.8%-class numbers)  
- **Not** a live multi-model re-derive table (some public kits run a frontier model live on n≈13; this pack scores **pipeline mechanics** on frozen pairs)  

All cases are public UDB parameters — **pretraining leakage** is possible. The scorer prints that caveat first.

## Why ship it

Proves end-to-end mechanics (source → extract shape → type) under fail-closed packaging, with an explicit honesty frame so it cannot be misread as beating corpus recall.
