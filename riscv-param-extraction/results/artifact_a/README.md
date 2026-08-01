# Artifact A raw outputs, recovered 2026-07-28

The gpt-4o-mini runs behind `metrics.md` section 5 and section 6. Committed here so the
aggregate figures can be audited rather than trusted.

## Why this directory exists

These files were written on 2026-07-25 by the Part I `extract.py`, whose output lands in a
**gitignored** working tree. Only the aggregate `metrics_gpt-4o-mini.json` was ever copied into this
repository. For three days `metrics.md` and the README described the per-chunk outputs and alignment
files as lost, and `verify_claims.py` carried `artifactA.exclusive_sets` as UNVERIFIABLE on that basis.

They were not lost. They were sitting uncommitted in a `git stash` on the local UDB clone, on branch
`lfx-1832`, in the stash's untracked-files parent. They were recovered from a local `git stash` on the UDB clone (`lfx-1832`).

Retention rule: if a number is published, the artifact that produced it is committed here.

## What is here

```
v2/   Artifact A, PROMPT_VERSION=v2, the published cross-model comparison
v3/   the v3 prompt ablation from metrics.md section 6
```

Each contains `alignment_*.json`, `all_results_*.json`, `deduped_*.json`, `metrics_*.json`, the run
log, and `chunks/` with all 60 per-chunk responses.

## Verification on recovery

Every published figure these back was re-derived before committing:

| Check | Published | Recovered | |
|---|---:|---:|---|
| v2 alignment exact matches | 11 | 11 | match |
| v3 alignment exact matches | 10 | 10 | match |
| v2 deduped unique params | 230 | 230 | match |
| chunk files | 60 | 60 | match |
| exclusive sets via `pipeline/agreement.py` | 236 / 218 / 9 / 227 / 209 | 236 / 218 / 9 / 227 / 209 | match |

`exact_matches_evaluated` in the metrics files is a **lower bound**, since `analyze.py:510` counts
only exact matches that also carried a comparable class. That is why the alignment tally matters and
why it was worth recovering: it is the only thing that can confirm the published 11 and 10. Both
confirm.

## Reproduce

```bash
python scripts/verify_claims.py --tag artifactA     # gated claims, including the alignment cross-checks
python scripts/verify_claims.py --tag recovered     # the checks added on recovery
```
