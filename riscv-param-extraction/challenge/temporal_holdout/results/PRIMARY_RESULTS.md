# Primary holdout results (frozen run)

**Run id:** `20260726T164713Z_gpt-4o-mini-2024-07-18`  
**Model pin:** `gpt-4o-mini-2024-07-18` · temperature 0 · prompt `holdout-v1.2`  
**Calls:** **26/26** successful · **primary_comparison=true**  
**Raw:** `runs/20260726T164713Z_gpt-4o-mini-2024-07-18/raw/`  
**Scores:** `scored/scores.json` · review queue: `scored/review_queue.json`

## Compact table (raw counts only; n=10 positives + 3 negatives)

| condition | name recall | name-agnostic detect | WARL | class | schema (all docs) | quote ground | neg FP |
|-----------|-------------|----------------------|------|-------|-------------------|--------------|--------|
| baseline  | **0/10**    | **0/10**             | 0/5  | 0/10  | 11/11             | 10/11        | **1/3** |
| treatment | **0/10**    | **0/10**             | 0/5  | 0/10  | 4/4               | 4/4          | **2/3** |

## Interpretation (honest)

- **Null on exact/alias name recall** under both conditions for this fixed mini snapshot.
- Model often emitted **schema-valid** parameters with **wrong or invented names** (e.g. `MTVC_MODE_OPTIONALITY` vs gold `MTVEC_MODES`; many FS-related names on P02).
- **Name-agnostic detection also 0/10** under the automated keyword/type rule — extractions did not meet the preregistered detection criteria either.
- **Treatment did not improve name recall** vs baseline (both 0/10). Treatment produced **fewer** extracted docs (4 vs 11) with perfect schema/grounding on those few — not a WARL win.
- **Negative controls:** baseline 1/3 FP; treatment **2/3** FP (worse on CSR-context legs for software-advice / convention cases).
- This is a **defensible null / negative result** for “CSR context fixes WARL naming on mini”: harness held; hypothesis not supported on this pilot.

## Reproduce

```bash
cd riscv-param-extraction
python challenge/temporal_holdout/scripts/score_holdout.py
# re-run live blocked: PRIMARY_RUN.json already locked
```

Do not hand-edit raw model outputs.
