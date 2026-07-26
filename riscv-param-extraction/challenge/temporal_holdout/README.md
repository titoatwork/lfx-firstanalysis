# Temporal holdout + leakage-audited CSR context (Artifact C pilot)

**Pilot id:** `temporal-holdout-artifact-c-v1`  
**Hypothesis:** Under temporal separation from a fixed model snapshot, leakage-audited CSR/field context improves WARL-related extraction vs source-only baseline.

This is a **vertical 4.5% slice** (10 of 223 public UDB parameters) plus **3 hard negatives** — not “5% of the mentors’ internal pipeline” (see [UDB #2053](https://github.com/riscv/riscv-unified-db/issues/2053) scope clarification).

## What is frozen (preregistered)

| Artifact | Path |
|----------|------|
| Case manifest + pins | `manifests/holdout_cases.yaml` |
| Scoring rubric | `manifests/scoring_rubric.md` |
| Gold (name/class/type only) | `gold/` |
| Source excerpts | `cases/positives/`, `cases/negatives/` |
| Scrubbed CSR contexts | `contexts/` |
| Prompt template | `prompts/holdout_v1.md` |
| Built prompts + hashes | `prompts/built/` |

**Pins:** model `gpt-4o-mini-2024-07-18` (release 2024-07-18) · UDB `5b7eccde` · ISA manual `7fc198f1`.

Temporal rule: each positive’s UDB param YAML first-add date is **after** the model release date. Stronger first-adds: `NUM_USABLE_PMP_ENTRIES` (2026-07-17), `SEW_MIN` (2026-02-02), `MCOUNTINHIBIT_IMPLEMENTED` (2026-04-29).

## Pipeline

```
spec source → CSR/field context (scrubbed) → leakage gate → extract
  → schema/evidence checks → score vs frozen gold → review queue
```

Conditions (same model, same cases):

1. **baseline** — source only  
2. **treatment** — source + leakage-audited CSR context  

## Reproduce (no API)

```bash
cd riscv-param-extraction

# unit tests + fail-closed leakage
python -m unittest challenge/temporal_holdout/tests/test_holdout.py -v
python challenge/temporal_holdout/scripts/leak_scan.py

# rebuild prompts/hashes (offline)
python challenge/temporal_holdout/scripts/build_prompts.py

# score committed/parsed results (if present)
python challenge/temporal_holdout/scripts/score_holdout.py
```

Rebuild contexts from a UDB checkout (optional; committed contexts already scrubbed):

```bash
python challenge/temporal_holdout/scripts/build_context.py \
  --udb-root /path/to/riscv-unified-db
python challenge/temporal_holdout/scripts/leak_scan.py
```

## Live run (paid; requires key + spend approval)

```bash
python challenge/temporal_holdout/scripts/run_live.py --estimate
# only with explicit spend approval and OPENAI_API_KEY:
python challenge/temporal_holdout/scripts/run_live.py --live \
  --model gpt-4o-mini-2024-07-18
python challenge/temporal_holdout/scripts/score_holdout.py
```

Est. cost: on the order of **~$0.02–0.05** for 13×2 calls on gpt-4o-mini (see `--estimate`).

Raw responses: `results/raw/`. Scores: `results/scored/`. Failures are preserved — no hand-repair.

## Leakage gate

Treatment context must not contain:

- exact gold parameter name  
- normalized gold parameter name  
- ground-truth YAML body fragments  

Intentional fixture `fixtures/leaked/contains_param_name.txt` must fail `leak_scan.py --expect-fail`.

## Honesty

- n=10: publish **case table + raw counts**, not significance claims.  
- Curated challenge pack elsewhere ≠ this pilot.  
- Null treatment result is acceptable if the harness is sound.  
- Credit: Spring Part I — [@ishaan-arora-1](https://github.com/ishaan-arora-1) / #1765–#1832.
