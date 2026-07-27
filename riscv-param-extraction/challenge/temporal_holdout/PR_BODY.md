# feat(eval): temporal holdout harness and exploratory v1.2 run

## Status

| Item | State |
|------|--------|
| Harness, tests, leak_scan, CI | Green |
| Locked live run | Done, `20260726T164713Z_gpt-4o-mini-2024-07-18` · **26/26** |
| Claim level | **Exploratory null / harness demo**, not clean temporal-holdout evidence |
| PR | Ready for review (self-audited limitations documented) |

## Hypothesis (tested exploratorily)

Leakage-audited CSR/field context improves WARL-related extraction vs source-only baseline under temporal case selection.

## Scope

- 10 / 223 public UDB parameters (~4.5%) + 3 hard negatives
- Not 5% of mentors internal pipeline (UDB issue #2053 scope note)

## Pins

| Pin | Value |
|-----|--------|
| Model | `gpt-4o-mini-2024-07-18` |
| Prompt | `holdout-v1.2` |
| Temperature | 0 |
| UDB / ISA | `5b7eccde` / `7fc198f1` |

## Locked primary results (raw counts)

| condition | name recall | detect | WARL | schema | ground | neg FP |
|-----------|-------------|--------|------|--------|--------|--------|
| baseline  | **0/10**    | 0/10   | 0/5  | 11/11  | 10/11  | 1/3    |
| treatment | **0/10**    | 0/10   | 0/5  | 4/4    | 4/4    | 2/3    |

### Defensible claim

The locked v1.2 run completed 26/26 calls and produced **0/10** exact/alias recall and **0/5** WARL recall in both arms. **No improvement was observed.** Because v1.2 contained case-specific guidance and label-revealing negatives, treat this as a **reproducible harness demonstration and exploratory null** — **not** clean temporal-holdout evidence. The negative FP arm difference (**1/3 vs 2/3**) is **not attributable to treatment** because those prompts were **byte-identical** across arms (model nondeterminism). P07 was also identical across arms.

Full write-up: [`results/PRIMARY_RESULTS.md`](./results/PRIMARY_RESULTS.md)

## Design (harness)

```
source -> scrubbed CSR context -> fail-closed leak_scan -> baseline|treatment prompt
  -> extract -> score vs frozen gold -> review_queue
```

- No `class` on UDB param YAML; eval metadata JSON for class/quote
- Untouched schema validation; primary score requires `RUN_META` (26 pairs, pin, prompt version)
- `PRIMARY_RUN.json` locked once; this primary run is **not** replaced by later experiments

## Known gaps (optional later experiment only — not this PR)

1. Remove label-revealing negative framing and gold-adjacent positive guidance
2. Ensure treatment differs from baseline only by CSR context (including P07 if context is intentional)
3. Record `prompt_sha256_sent` (actual bytes) per call, not only expected hashes

A cleaner prompt generation would be a **separate** experiment, not a replacement of this locked primary.

## Reproduce

```bash
cd riscv-param-extraction
pip install -r requirements.txt
python challenge/temporal_holdout/tests/test_holdout.py -v
python challenge/temporal_holdout/scripts/leak_scan.py
python challenge/scripts/ci_check.py
python challenge/temporal_holdout/scripts/score_holdout.py
```

## Honesty

- Case table + raw counts only (n=10). No significance claims.
- Credit Spring Part I: [@ishaan-arora-1](https://github.com/ishaan-arora-1) / UDB PRs #1765–#1832.
