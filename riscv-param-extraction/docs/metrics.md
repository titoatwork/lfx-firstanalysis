# Metrics

Tables only. Numbers are **user-measured** unless marked pending. Do not invent pilot/A results.

---

## Every recall figure here is a single run, and single runs are unstable

**Measured 2026-07-28.** The same model, the same byte-identical prompt, `temperature=0`, run twice thirty minutes apart, scored **33.9%** and **44.6%** adjusted recall on the same 60 chunks. Per class it moved further: `NORM_CSR_RW` went 6/51 to 21/51, and `NORM_CSR_WARL` went 2/24 to 9/24 in the other arm.

Verified not to be a harness artefact: prompts byte-identical by SHA-256, `analyze.py` deterministic on re-scoring, and the harness reproduces the published Claude figures exactly. The variance is in the model, and the alias / one-to-many / fuzzy alignment passes amplify it, since run 2 produced *fewer* raw parameters yet matched *more* gold.

**Consequence for everything below.** Every figure in this file is one sample. The numbers are correctly measured and correctly reported, and they do not carry the precision a single decimal place implies. Do not present a difference between two single runs as an improvement or a regression.

Full write-up and committed artifacts: [`artifact_c/results/PRIMARY_RESULTS.md`](../artifact_c/results/PRIMARY_RESULTS.md). Reported upstream as [riscv-unified-db#2163](https://github.com/riscv/riscv-unified-db/issues/2163).

---

## Most of a recall figure here is awarded by fuzzy matching, not by naming the parameter

**Measured 2026-07-28.** `analyze.py` credits a gold parameter through an exact name match or through one of five inexact passes (`one_to_many`, `explicit_group`, `concept_group`, `stem`, `fuzzy_name`). Only the totals reach the metrics files, so the split is invisible unless you go looking. Recovering it across eight complete runs:

| Run set | Exact | Inexact | Reported | Exact-name only | Inexact share |
|---------|------:|--------:|---------:|----------------:|--------------:|
| gpt-4o-mini, 8 runs | 5–9 | 47–70 | 29.4–44.6% | 2.8–5.1% | **84.5–90.4%** |
| claude-sonnet-4, Part I | 86 | 43 | 72.9% | 48.6% | 33.3% |
| gpt-4o-mini, published † | 11 | 46 | 32.2% | 6.2% | 80.7% |
| gpt-4o-mini, v3 prompt † | 10 | 52 | 35.0% | 5.6% | 83.9% |

**† Aggregate-only, and not auditable.** These two runs predate the artefact-retention rule. Their per-chunk outputs and alignment files were not kept, so `Exact` here is `exact_matches_evaluated` read from the metrics file, which is a **lower bound**: `analyze.py:510` counts only exact matches that also carried a comparable class. It cannot be cross-checked against an alignment tally, and it never will be without re-running the model. Where both artefacts do survive, on the Claude row, the field equals the alignment tally exactly (86 against 86), so these figures are probably correct. Probably correct is not the same as verifiable. The top two rows re-derive from committed alignment files and are the ones to cite.

Two consequences.

**The instability is concentrated in the heuristic layer.** Across the eight runs exact matches span a range of 4 while inexact matches span 23. The component carrying roughly seven eighths of the score is the component that moves.

**The published cross-model gap is understated.** On reported adjusted recall it reads 72.9% against 32.2%, about 2.3x. On exact-name recall it is far wider. The reproducible comparison is **48.6% against 5.1%, about 9.6x**, taking gpt-4o-mini from the two complete arm A runs whose alignment files are committed and which agree exactly at 9 exact matches each. The aggregate-only published run gives 6.2% and 7.8x; that figure was cited here until 2026-07-28 and is superseded because its alignment was never retained.

Both comparisons cross an extraction-harness boundary, since the Claude baseline ran through the Part I `extract.py` and the arm A runs through `run_arms.py`. Read the multiplier as an order of magnitude rather than a precise ratio. The direction is not in doubt: one model names the parameter, the other is scored on description similarity.

Inexact matching is not wrong; a model answering "support for misaligned loads and stores" has found `MISALIGNED_LDST`. The point is that the credit is mostly heuristic, that is where the noise lives, and neither fact is visible in the headline number.

Reproduce with `python artifact_c/scripts/decompose_matches.py` — deterministic, no API key needed. This analysis was **not preregistered**; it came out of diagnosing the variance above and is reported as exploratory.

---

## Read this before citing any recall number

**Every recall figure below was produced with the complete list of gold parameter names supplied in the prompt.**

`extract.py` builds each prompt through `build_user_message()`, which unconditionally injects `format_param_names_section(load_udb_param_names())`. That list is read from `param_extraction/data/udb_param_names.txt`, which is **set-identical** to the 185 parameters in `ground_truth.json`:

```
injected list size : 185
gold set size      : 185
identical sets     : True
```

The instruction accompanying it reads: *"When a parameter you find matches one of these known names, use the exact name."*

**What this means.** These numbers measure **grounding**, not discovery: given the catalogue of 185 names, locate which apply to a passage and cite evidence. For the Spring work that produced the parameter spreadsheet and tagged spec text, supplying the catalogue is the correct design, because mapping to a catalogue requires the catalogue.

**What it does not mean.** None of these figures show whether a model can find architectural parameters *without* being given the answer key. That number is not measured anywhere in this repository or, as far as I can tell, anywhere public. Measuring it is the subject of [`artifact_c/PREREGISTRATION.md`](../artifact_c/PREREGISTRATION.md).

Do not present any figure below as discovery recall. State the name-list condition whenever these numbers are cited.

*Added 2026-07-27 on discovering the condition while building Artifact C. The figures themselves are unchanged and remain correctly measured for what they measure.*

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

> **Condition: gold name list supplied.** All 185 gold names were in the prompt. This is grounding recall, not discovery recall. See the note at the top of this file.

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
| Artifact A | **Done**. Full gpt-4o-mini corpus (see §5); not pure gpt-4o |
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

> **Condition: gold name list supplied to both models.** The cross-model comparison is therefore between two models doing the *same grounding task* with the same catalogue. The 3.8% name Jaccard is measured under that condition, which makes the disagreement more striking rather than less: both models had the identical list of 185 names available and still shared only 21.

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

> **At least two of the nine are not missed parameters. Recorded 2026-07-28.** Labelling the nine dual-model candidates against UDB: `IALIGN` is **derived**, not a parameter, via `function ialign` in `spec/std/isa/isa/globals.isa` (returns 16 or 32 depending on `C` and `misa.C`); no parameter file exists. Found by [@RAJVEER42](https://github.com/riscv/riscv-unified-db/issues/2053). `FLEN` is also derived, from which of `F`/`D`/`Q` is implemented, though without an explicit derivation function. `ILEN` is unresolved: no parameter, no function, only a prose constraint in `Ziccif.yaml`. So dual-model agreement at high confidence failed to filter at least two non-parameters. **The nine must not be described as a validated review queue.**
>
> **Retention gap, recorded 2026-07-28.** The per-chunk gpt-4o-mini outputs behind this section were kept local rather than committed, and the working clone has since moved branches. The aggregate counts below stand, and the nine dual-model names are listed in the claim ledger. The **model-exclusive sets are no longer on disk**, so the 227 Claude-only and 209 mini-only candidates cannot be recomputed or audited. Treat the counts as reported-but-unauditable until the Artifact C run regenerates them. Retention is a hard gate on that run (`artifact_c/PREREGISTRATION.md` §6b).

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

> **Condition: gold name list supplied in both arms.** The v3 WARL guidance was therefore added *on top of* an already-supplied catalogue of names. That the model labelled more items WARL without matching more gold WARL entries is a failure of identification, not of vocabulary, since it already had every correct name in front of it.

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

**Honest claim:** Adding WARL-focused prompt text **did not improve** gold WARL recall; it **worsened** it. Overall adjusted recall ticked up slightly (mostly DIRECT). Raw extraction tagged more rows as WARL (**59** raw class labels vs **~36** on v2), but those did **not** translate into more GT WARL hits, over-labeling without better name/alignment quality.

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

---

## 8. Challenge pack controls (Path A)

| Control | Value |
|---------|------:|
| Snippets | 2 (CMO + CSR zero) |
| Fail-closed bad fixtures | **4** |
| Hard negatives | **4** |
| Markup robustness cases | **3** (naive vs tag-aware) |
| Known-param bench | **n=15** |
| Existence (committed extraction pairs) | **15/15** |
| Type fidelity (same pairs) | **15/15** |
| Live multi-model dirs | **10** |

**Known-param note:** n=15 scores **mechanics** of paired ground_truth.yaml + extraction.yaml under the scorer. It is **not** a live multi-model re-derive table and **not** equal to Spring corpus adjusted recall. Pretraining leakage applies to any known-param public UDB set.

Source: python challenge/benchmark/scripts/score_recall.py; live matrix challenge/results/live/MANIFEST.md.

---

## 9. Temporal holdout pilot (exploratory primary)

**Status:** locked primary 20260726T164713Z_gpt-4o-mini-2024-07-18 · **26/26** calls  
**Write-up:** [challenge/temporal_holdout/results/PRIMARY_RESULTS.md](../challenge/temporal_holdout/results/PRIMARY_RESULTS.md)  
**PR:** https://github.com/titoatwork/lfx-firstanalysis/pull/1

| Condition | Name recall | Detect | WARL | Schema docs | Ground | Neg FP |
|-----------|------------:|-------:|-----:|------------:|-------:|-------:|
| baseline | **0/10** | 0/10 | 0/5 | 11/11 | 10/11 | 1/3 |
| treatment | **0/10** | 0/10 | 0/5 | 4/4 | 4/4 | 2/3 |

**Claim level:** reproducible harness demonstration + **exploratory null** under prompt **v1.2**.  
**Not:** clean temporal-holdout evidence (v1.2 had case-specific guidance / label-revealing negatives).  
**Not:** treatment caused worse negative FPs (N01–N03 prompts byte-identical across arms).

