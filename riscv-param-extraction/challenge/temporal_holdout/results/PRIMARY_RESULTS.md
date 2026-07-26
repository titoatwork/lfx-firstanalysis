# Primary holdout results (frozen run — do not replace)

**Run id:** `20260726T164713Z_gpt-4o-mini-2024-07-18`  
**Model pin:** `gpt-4o-mini-2024-07-18` · temperature 0 · prompt **`holdout-v1.2`**  
**Calls:** **26/26** successful · primary pointer locked  
**Raw:** `runs/20260726T164713Z_gpt-4o-mini-2024-07-18/raw/`  
**Scores:** `scored/scores.json` · review queue: `scored/review_queue.json`

This primary run is **immutable**. A cleaner prompt generation (e.g. v1.3) must be published as a **separate** experiment, not by overwriting this tree or `PRIMARY_RUN.json`.

## Compact table (raw counts only; n=10 positives + 3 negatives)

| condition | name recall | name-agnostic detect | WARL | class | schema (all docs) | quote ground | neg FP |
|-----------|-------------|----------------------|------|-------|-------------------|--------------|--------|
| baseline  | **0/10**    | **0/10**             | 0/5  | 0/10  | 11/11             | 10/11        | **1/3** |
| treatment | **0/10**    | **0/10**             | 0/5  | 0/10  | 4/4               | 4/4          | **2/3** |

## Defensible claim (use this wording)

The locked v1.2 run completed 26/26 calls and produced **0/10** exact/alias recall and **0/5** WARL recall in both arms. **No improvement was observed.** Because v1.2 contained case-specific guidance and label-revealing negatives, treat this as a **reproducible harness demonstration and exploratory null** — **not** clean temporal-holdout evidence. The negative FP arm difference (**1/3 vs 2/3**) is **not attributable to treatment**, because those negative prompts were **byte-identical** across arms (model nondeterminism).

## Limitations (v1.2 — why this is not clean temporal-holdout evidence)

1. **Semantic leakage in prompts (v1.2)**  
   - Negative prompts included guidance such as “Expect ZERO parameters.”  
   - Negative sources reveal their control class (fixed encoding / shall-only / software advice).  
   - Positive prompts included **case-specific definedBy guidance** adjacent to gold modeling choices.  
   CSR context leak_scan can pass while these label/guidance channels remain.

2. **Identical prompts across arms (invalidates FP attribution)**  
   Verified: `N01`, `N02`, `N03` baseline and treatment built prompts are **byte-identical** (no CSR context ids).  
   `P07` (TRAP_ON_ILLEGAL_WLRL) is also **identical** across arms (`csr_context_ids: []`).  
   Therefore baseline **1/3** vs treatment **2/3** negative FP is **not** evidence that CSR context made negatives worse.

3. **Sent-byte hash not recorded**  
   `RUN_META.json` stores **expected** prompt hashes (`prompt_sha256_expected`) but **does not** record the hash of the exact bytes sent to the API. A future run should write `prompt_sha256_sent` per call; this primary run is left unchanged.

## What the numbers still support

- Harness completed a locked 26/26 run with pinned model and reproducible scoring.  
- On this exploratory setup, **name/WARL recall stayed at zero** under both arms — no support for “context fixes WARL naming on mini” as a positive claim.  
- Schema-valid extractions with **wrong names** appear in the review queue (naming failure mode, not infrastructure failure).

## What they do **not** support

- Clean temporal separation with leakage-free prompts.  
- Causal claim that treatment improved or harmed negative-control precision.  
- Any claim that this pilot beats challenge-kit multi-model tables.

## Reproduce (score only; do not re-run primary)

```bash
cd riscv-param-extraction
python challenge/temporal_holdout/scripts/score_holdout.py
# Live re-run of primary is blocked while PRIMARY_RUN.json is locked.
```

Do not hand-edit raw model outputs.
