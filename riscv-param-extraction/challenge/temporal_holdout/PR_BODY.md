# feat(eval): add temporal holdout and leakage-audited CSR context pilot

## Hypothesis

Under temporal separation from a fixed model snapshot, **leakage-audited CSR/field context** improves WARL-related extraction versus source-excerpt-only baseline — addressing the failure mode that prompt-only v3 guidance did not fix on corpus WARL recall.

## Scope (defensible “5%”)

- **10 / 223** public UDB parameters (**~4.5%**) + **3** hard negatives  
- **Not** 5% of mentors’ current internal pipeline ([#2053 scope note](https://github.com/riscv/riscv-unified-db/issues/2053#issuecomment-5060711204))

| Strata | Cases |
|--------|--------|
| WARL | P01–P05 |
| CSR_RW / WLRL | P06–P07 |
| DIRECT | P08–P10 (includes post-2026-02 first-adds) |
| Negatives | fixed encoding · shall-only · software may/should |

## Pins (preregistered before outputs)

| Pin | Value |
|-----|--------|
| Model | `gpt-4o-mini-2024-07-18` (release 2024-07-18) |
| UDB | `5b7eccde` |
| ISA manual | `7fc198f1` |
| Temperature | 0 |
| Prompt | `holdout-v1.2` (case-correct `definedBy` guidance) |

Temporal rule: each positive’s UDB param first-add date is **after** model release.

## Design

```
source → scrubbed CSR context → fail-closed leak_scan → baseline|treatment prompt
  → extract → score vs frozen gold → review_queue
```

Treatment context forbids exact/normalized gold parameter names and GT YAML bodies. Prompt/context hashes under `prompts/built/PROMPT_HASHES.json`.

## Status (honest)

| Item | State |
|------|--------|
| Offline harness + leak gate + unit tests | Implemented (CI green) |
| Live baseline vs treatment (26 calls) | **Pending** — not claimed until raw/scores committed |
| Null / negative treatment result | Acceptable if published honestly |

**Draft PR:** live measurements are **not** included yet. Do not treat CI green as experimental result.

## Pre-live integrity gates

- UDB param YAML: **no `class` field**; class + quote in eval metadata JSON only  
- Schema validity: **untouched** docs (no `$schema`/`kind` injection); totals include **all** extracted docs (positives **and** negatives)  
- Grounding: **per extracted param**; missing quote = fail (in denominator)  
- Model pin mismatch: **fail-closed** (exit before calls)  
- `definedBy`: **case-correct guidance** (e.g. `Zvl32b` for SEW_MIN; not hard-coded `Sm` everywhere)  
- Runs under `results/runs/<id>/` with **no overwrite**  
- **PRIMARY_RUN.json** written once only; a second complete run cannot replace it (use `--debug-run` for non-primary)  
- Primary score requires adjacent **RUN_META.json** validating: pinned model, prompt version/hash, **26 unique successful (case, condition) pairs**, zero failures, `primary_comparison_eligible`  
- File presence alone is **not** enough for a primary claim  

## Reproduce (CI / local, no API)

```bash
cd riscv-param-extraction
pip install -r requirements.txt
python challenge/temporal_holdout/tests/test_holdout.py -v
python challenge/temporal_holdout/scripts/leak_scan.py
python challenge/scripts/ci_check.py
```

Live (only with local key; never commit secrets):

```bash
python challenge/temporal_holdout/scripts/run_live.py --estimate
python challenge/temporal_holdout/scripts/run_live.py --live --model gpt-4o-mini-2024-07-18
python challenge/temporal_holdout/scripts/score_holdout.py
```

## Honesty

Case table + raw counts only (n=10). No claim of statistical significance or “beats Anshul.”
Credit: Spring Part I — [@ishaan-arora-1](https://github.com/ishaan-arora-1) / #1765–#1832.
