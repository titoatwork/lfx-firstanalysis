# Metrics

Tables only. Numbers are **user-measured** unless marked pending. Do not invent pilot/A results.

Credit: Part I pipeline and committed results — [@ishaan-arora-1](https://github.com/ishaan-arora-1) / [riscv/riscv-unified-db](https://github.com/riscv/riscv-unified-db) PRs #1765–#1832. Remeasure and pilot here are independent reproduction, **not** Part I authorship.

---

## 1. Phase 1 ground truth (regenerated on live UDB)

| Metric | Value |
|--------|------:|
| Real parameters | **223** (Part I freeze was 185; +38) |
| Spec files / lines | 74 / ~52 878 |
| Any keyword match / strong | 100% / 91% |
| Classes | DIRECT 140 · CSR_RW 55 · WARL 26 · SW_RULE 2 |

Source: local `export_udb_params` → `map_params_to_spec` → `generate_report` (2026-07-21).

---

## 2. Part I v2 remeasure (Claude Sonnet 4, committed GT 185)

| Metric | Value |
|--------|------:|
| Adjusted recall | **72.9%** |
| Classification accuracy | **88.4%** |
| WARL recall (`NORM_CSR_WARL`) | **50%** (12/24) |
| Deduped LLM params | 346 |

| Class | Found | Total |
|-------|------:|------:|
| NORM_DIRECT | 83 | 100 |
| NORM_CSR_RW | 32 | 51 |
| NORM_CSR_WARL | 12 | 24 |
| SW_RULE | 2 | 2 |

Against **live GT 223** (same LLM output): adjusted recall **64.2%**, class acc **88.6%**, WARL still **50%**.

---

## 3. Pilot — machine.adoc (2026-07-22)

**Status:** `COMPLETE_WITH_MODEL_SPLIT`  
**Manifest:** [manifests/pilot-machine-adoc.md](../manifests/pilot-machine-adoc.md)

| Chunk | Model | In | Out | Params | ~USD |
|-------|--------|---:|----:|-------:|-----:|
| chunk_021 | gpt-4o-2024-11-20 | 10 115 | 1 152 | **6** | ~0.037 |
| chunk_020 | gpt-4o-mini-2024-07-18 | 44 874 | 1 541 | **9** | ~0.008 |
| **Total** | model split | **54 989** | **2 693** | **15** | **~0.05** |

| Limitation | Detail |
|------------|--------|
| Why not pure gpt-4o | Org TPM **30 000** for gpt-4o; chunk_020 needed ~**44 373** input tokens |
| Artifact A | **Done** — full gpt-4o-mini corpus (see §5); not pure gpt-4o |
| Full corpus extract (mini) | **Done** 2026-07-24/25 |

---

## 4. Spreadsheet baseline (Artifact B input)

| Metric | Value |
|--------|------:|
| `parameters.csv` rows | 346 |
| `named=yes` rows | **87** |
| Unique `named=yes` names | **83** |
| Overlap with UDB `spec/std/isa/param/*.yaml` | **83 / 83** |
| Unique names not in UDB | **257** (`named=no`) |

Do **not** claim 97 named params without re-counting the CSV in use.

---

## 5. Artifact A — multi-model (gpt-4o-mini vs Claude Part I)

**Status:** `COMPLETE` (2026-07-24 → 2026-07-25)  
**Manifest:** [manifests/artifact-a-gpt-4o-mini.md](../manifests/artifact-a-gpt-4o-mini.md)  
**Agreement JSON:** [results/artifact_a_agreement.json](../results/artifact_a_agreement.json)

Second model: **gpt-4o-mini-2024-07-18**, `PROMPT_VERSION=v2`, **60/60** param-bearing chunks, **0** errors.  
Headline metrics vs **GT 185** (Part I freeze). Claude baseline = committed Part I v2 (not re-billed).

### 5.0 What this run establishes

1. **Cross-model name agreement is near zero under an identical prompt.** Claude-sonnet-4 and gpt-4o-mini extracted **346** and **230** unique parameter names on the same 60 chunks with the same v2 prompt; only **21** names were shared (Jaccard **3.8%**). Pipeline and source text were held constant, so the disagreement is attributable to the model, not the extract/analyze path.

2. **Single-model “discoveries” are mostly model-private and cannot be trusted individually.** High-confidence proposed-new counts were Claude **236** and mini **218**, with only **9** proposed by both. Those **9** form a prioritized human-review queue; the remaining model-private proposals (~**440** combined exclusive) are not evidence of real parameters until reviewed. That is a measured argument for a review protocol, not an opinion.

3. **The cost/quality curve is steep and now quantified.** On the same 60 chunks, mini reached **32.2%** adjusted recall against the Claude baseline **72.9%**, with tokens (**868 976** in / **51 718** out) and cost (**~$0.16**) published alongside. Mini is not competitive with Claude on this task; the gap is measured, not speculated.

These three findings are why a Fall plan should put **cross-model gating** and a **human-review rubric** ahead of chasing raw single-model recall.

### 5.1 Run cost (gpt-4o-mini)

| Field | Value |
|------:|
| Chunks OK / errors | **60 / 0** |
| Raw params (pre-dedup) | 239 |
| Input tokens | **868 976** |
| Output tokens | **51 718** |
| Approx cost (USD, list rates ~$0.15/M in · $0.60/M out) | **~$0.16** |

### 5.2 Per-model metrics vs GT 185

| Metric | Claude-sonnet-4 (Part I v2) | gpt-4o-mini (this run) |
|--------|----------------------------:|-----------------------:|
| Deduped LLM params | 346 | **230** |
| Adjusted recall | **72.9%** | **32.2%** |
| Classification accuracy (exact matches only) | **88.4%** (76/86) | **100%** (11/11)† |
| WARL recall | **50%** (12/24) | **12.5%** (3/24) |
| Matched non-debug UDB | 129 | **57** |

† Mini class-acc denominator is small (only **11** exact name matches). Do **not** read this as “better than Claude overall.”

| Class | Claude found/total | Mini found/total |
|-------|-------------------:|-----------------:|
| NORM_DIRECT | 83/100 | **48/100** |
| NORM_CSR_RW | 32/51 | **6/51** |
| NORM_CSR_WARL | 12/24 | **3/24** |
| SW_RULE | 2/2 | **0/2** |

**Honest summary:** gpt-4o-mini is **substantially worse** than Claude-sonnet-4 on adjusted recall and every per-class recall row under this pipeline. Useful as a multi-model ablation / cost baseline, not as a replacement for Claude-quality extract.

### 5.3 Inter-model agreement (parameter names)

| Metric | Value |
|--------|------:|
| Unique Claude | 346 |
| Unique mini | 230 |
| Shared names | **21** |
| Only Claude | 325 |
| Only mini | 209 |
| Jaccard (name) | **3.8%** |
| Match rate vs Claude | 6.1% |
| Match rate vs mini | 9.1% |
| Class agreement on shared | **81.0%** (17/21) |

Shared-name sample: `CACHE_BLOCK_SIZE`, `ELEN`, `VLEN`, `MTVEC_MODES`, `NUM_PMP_ENTRIES`, `XLEN`, …

### 5.4 Hallucination-overlap (high-conf proposed-new)

Proposed-new = name **not** in GT185 UDB set and no trusted `existing_udb_name` hit; **confidence=high** only.

| Metric | Value |
|--------|------:|
| Proposed-new Claude | 236 |
| Proposed-new mini | 218 |
| Both models | **9** |
| Only Claude | 227 |
| Only mini | 209 |
| Overlap rate vs Claude | 3.8% |
| Overlap rate vs mini | 4.1% |

Low both-model overlap on “new” names → most proposed-new are model-private (higher hallucination risk); the **9** both-model hits are higher-priority review candidates.

### 5.5 Limitations (A)

- Second model is **gpt-4o-mini**, not full gpt-4o corpus (TPM + budget).  
- Org TPM forced ~60s waits between large chunks; run ~49 min wall clock.  
- `analyze.py --model` must precede the subcommand (`--model gpt-4o-mini all`).  
- Full per-chunk JSON stays local under UDB clone (not shipped in this monorepo).  
- Do not claim mini “matched or beat Claude.”

---

## 6. Stretch C ablation — prompt v3 WARL guidance (gpt-4o-mini)

**Status:** `COMPLETE` (2026-07-25) — **honest null / negative for WARL**  
**Manifest:** [manifests/stretch-c-v3-warl.md](../manifests/stretch-c-v3-warl.md)  
**Metrics JSON:** [results/metrics_gpt-4o-mini.v3.json](../results/metrics_gpt-4o-mini.v3.json)

Same model (**gpt-4o-mini**), same 60 param-bearing chunks, **PROMPT_VERSION=v3** (v2 + structural WARL recognition section only; no GT name leakage). Compared to Artifact A mini under **v2**.

### 6.0 Headline

| Metric | A mini (v2) | v3 mini | Δ |
|--------|------------:|--------:|--:|
| Adjusted recall (GT185) | **32.2%** | **35.0%** | +2.8 pp |
| WARL recall (`NORM_CSR_WARL`) | **12.5%** (3/24) | **8.3%** (2/24) | **−4.2 pp** |
| NORM_DIRECT | 48/100 | 53/100 | +5 |
| NORM_CSR_RW | 6/51 | 7/51 | +1 |
| Deduped LLM params | 230 | 204 | −26 |
| Class acc (exact only) | 100% (11/11) | 80% (8/10) | small n |

**Honest claim:** Adding WARL-focused prompt text **did not improve** gold WARL recall; it **worsened** it. Overall adjusted recall ticked up slightly (mostly DIRECT). Raw extraction tagged more rows as WARL (**59** raw class labels vs **~36** on v2), but those did **not** translate into more GT WARL hits — over-labeling without better name/alignment quality.

**Do not** present v3 as a successful Stretch C WARL attack. Treat as a measured **prompt ablation null result** (useful for the Fall plan: need CSR-field aux context or different strategy, not prompt-only WARL essay).

### 6.1 Run cost (v3 full corpus)

| Field | Value |
|------:|
| Chunks OK / errors | **60 / 0** |
| Input tokens | **901 796** |
| Output tokens | **48 731** |
| Approx cost (USD) | **~$0.16** |
| Resume note | Mid-run 401 (dead key) then completed with rotated key; good chunks not re-billed |

### 6.2 Limitations (v3)

- Still **gpt-4o-mini**, not Claude-quality extract.  
- WARL “lift” target failed; report as null.  
- Per-chunk JSON stays local under UDB `results/v3/`.  

---

## 7. Artifact B — export validation (2026-07-22)

Reports: `results/export_b_named.json`, `results/export_b_new.json`.

### Mode `named` (named=yes unique)

| Metric | Value |
|--------|------:|
| Drafts written | **83** |
| Schema-valid | **83 / 83** |
| UDB name overlap | **83 / 83** |
| `definedBy` source | **udb_copy** (all) |

| Class | Count |
|-------|------:|
| NORM_DIRECT | 38 |
| NORM_CSR_RW | 32 |
| NORM_CSR_WARL | 11 |
| SW_RULE | 2 |

### Mode `new` (limit 20, not in UDB)

| Metric | Value |
|--------|------:|
| Drafts written | **20** |
| Schema-valid | **20 / 20** |
| UDB name overlap | **0** |
| `definedBy` source | **adoc_map** |

| Class | Count |
|-------|------:|
| NORM_DIRECT | 16 |
| NORM_CSR_RW | 4 |

Schema fragments for enum/range/set still need human domain fill (CSV does not encode members/bounds).
