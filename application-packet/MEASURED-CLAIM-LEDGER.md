# Measured claim ledger — Part II application

**Purpose:** Every public or application claim must map to a source.  
**Primary sources:** `riscv-param-extraction/docs/metrics.md`, manifests, monorepo results JSON  
**Credit:** Spring Part I pipeline and committed Claude results — [@ishaan-arora-1](https://github.com/ishaan-arora-1) / PRs #1765–#1832. This campaign **reproduces and extends**; it does not claim Spring authorship.

---

## Single runs are unstable. Never present a single-run difference as an effect

Measured 2026-07-28: identical model, byte-identical prompt, `temperature=0`, run twice, **33.9%** and **44.6%** adjusted recall. Per class worse: `CSR_RW` 6/51 to 21/51; `WARL` 2/24 to 9/24. Not a harness artefact (prompts SHA-identical, scorer deterministic, harness reproduces published Claude figures).

**Forbidden as a result of this:**

| Do not say | Why |
|------------|-----|
| "v3 improved adjusted recall from 32.2% to 35.0%" | 2.8 points is inside the measured noise. State it as not distinguishable from run-to-run variation |
| "mini scored 32.2% and Claude 72.9%, so Claude is better" | The gap is large enough to survive, but say it is one run each |
| Any per-class comparison from single runs | `WARL` has a 24-item denominator and moved by 7 between identical runs |
| Quoting recall to one decimal as if precise | Report the range, or say single run |

**Allowed:** "one run of each, and run-to-run variation on this task is around 10 points on the headline metric, so treat single-run differences with care."

---

## Mandatory qualifier on every recall number

**All published recall figures were produced with the full gold name list in the prompt.** `extract.py` → `build_user_message()` unconditionally injects all 185 names from `udb_param_names.txt`, which is set-identical to `ground_truth.json`. The accompanying instruction is *"When a parameter you find matches one of these known names, use the exact name."*

Every citation of 72.9%, 64.2%, 32.2%, 35.0%, or any per-class recall **must** state this condition. Acceptable forms:

- "72.9% adjusted recall, with the 185 gold parameter names supplied in the prompt"
- "grounding recall of 72.9% (catalogue supplied); discovery recall is unmeasured"

Never cite these as evidence a model can *find* parameters. They measure locating and evidencing names from a supplied catalogue. That is a legitimate task and the correct design for the spreadsheet and tagging work, but it is not discovery.

Discovery recall is unmeasured and is the subject of `artifact_c/PREREGISTRATION.md`.

---

## Safe claims (approved wording)

| Claim | Exact numbers | Source | Allowed use |
|-------|---------------|--------|-------------|
| Live UDB GT size | **223** params; 100% any / **91%** strong keyword match | metrics §1 | Application, README |
| Part I v2 vs pinned GT185 | adj recall **72.9%**, class acc **88.4%**, WARL **50%** (12/24) | metrics §2; remeasure | Lead numbers |
| Same LLM output vs live GT223 | adj recall **64.2%**, class acc **88.6%**, WARL still **50%** | metrics §2 | Gold drift story |
| named=yes rows | **87** rows / **83** unique names | metrics §4 | Never say 97 |
| Artifact B named export | **83/83** schema-valid; all 83 already in UDB | metrics §7 | Structural validity only |
| Artifact B new export | **20/20** schema-valid drafts; not in UDB | metrics §7 | Candidates, not merges |
| Pilot | **COMPLETE_WITH_MODEL_SPLIT** ~**$0.05**; 021 gpt-4o, 020 gpt-4o-mini | metrics §3; pilot manifest | TPM honesty |
| Artifact A model | **gpt-4o-mini**, PROMPT **v2**, **60/60** chunks | metrics §5; A manifest | Not pure gpt-4o |
| Artifact A vs GT185 | adj **32.2%**, WARL **12.5%** (3/24), ~**$0.16** | metrics §5 | Honest worse-than-Claude |
| Claude Part I baseline (not re-billed) | adj **72.9%**, 346 deduped names | metrics §5 | Comparison baseline |
| Name agreement A | shared **21**, Jaccard **3.8%** | metrics §5.3 | Review-gating story |
| High-conf proposed-new both models | **9** names, of which **at least 2 are not parameters** | metrics §5.4 | **Never call these a validated review queue.** `IALIGN` is derived (`function ialign` in `globals.isa`), `FLEN` follows from which FP extension is implemented, `ILEN` unresolved. Dual-model agreement failed to filter them. Also state the retention gap: the exclusive sets (227 / 209) were not committed and cannot be recomputed. Credit @RAJVEER42 for the IALIGN finding |
| v3 prompt WARL ablation | **60/60**; adj **35.0%**; WARL **8.3%** (2/24); ~**$0.16** | metrics §6; stretch-c manifest | **Null / negative** for WARL |
| Public repo | https://github.com/titoatwork/lfx-firstanalysis | git | Prework link |
| Coding challenge pack | 2 snippets · fail-closed CI · curated + live multi-model under `challenge/` | monorepo | Path A |
| Live multi-model (snippets) | Multiple providers; **best free legs** hit CMO=3 + CSR=0 (e.g. Nemotron Ultra free, Gemini free, Ling free); some models under-extract or CSR false-positive, report honestly | `challenge/results/live/MANIFEST.md` | Not corpus-scale; not Sonnet claim |
| Challenge control density | **4** bad fixtures · **4** hard negatives · **n=15** known-param mechanics · green monorepo CI | `challenge/README.md`; `ci_check.py` | Not “weaker kit”; packaging differs from dedicated-repo kits |
| Known-param n=15 | Existence **15/15**, type fidelity **15/15** on committed pairs | `benchmark/scripts/score_recall.py` | Mechanics only; not live multi-model re-derive; not corpus recall |
| Temporal holdout primary | **26/26**; name **0/10** both arms; WARL **0/5**; exploratory null under v1.2 limits | `temporal_holdout/results/PRIMARY_RESULTS.md`; PR #1 | Not clean temporal proof; neg FP not attributable to treatment |
| Open Spring PRs (context) | #1765–#1832 still the Part I surface | GitHub | “merge/export still open” |
| UDB PRs (when open) | Only original unclaimed fixes; STVAL/HPM already claimed by others | GitHub PR URLs | Never invent merges; comment ≠ PR |
| **Spring PRs are a superseded snapshot** | @ishaan-arora-1 in issue #2053: those PRs were “the first version of the pipeline”; current work “is internal and not uploaded on this repository yet” | [issue #2053](https://github.com/riscv/riscv-unified-db/issues/2053) | State this **before** citing any Part I remeasure; never present #1765–#1832 as current state |
| **Own upstream PRs, merged (5)** | [#2138](https://github.com/riscv/riscv-unified-db/pull/2138) `aee74ee8`, [#2146](https://github.com/riscv/riscv-unified-db/pull/2146) `278d1edc`, [#2189](https://github.com/riscv/riscv-unified-db/pull/2189) `57d70cfa`, [#2215](https://github.com/riscv/riscv-unified-db/pull/2215) `f1669021`, [#2227](https://github.com/riscv/riscv-unified-db/pull/2227) `86e68458`. Each closed an issue I filed first: #2137, #2145, #2188, #2214, #2226 | GitHub API, re-derived 2026-07-30 after #2227 merged | Say **five merged**. Each is a small data or schema correction, not a feature. Do not describe #2146 as a schema fix; it is docs-only |
| **Own upstream PRs, open (3)** | [#2212](https://github.com/riscv/riscv-unified-db/pull/2212) closes #2199, the only Ruby change; [#2227](https://github.com/riscv/riscv-unified-db/pull/2227) closes #2226; [#2164](https://github.com/riscv/riscv-unified-db/pull/2164) fixtures, gated on #2158 | GitHub API | Say **open with checks green**. Never say approved or merged until the API says so |
| **Reviews carried into others' merged PRs (3)** | [#2090](https://github.com/riscv/riscv-unified-db/pull/2090) MTVEC alignment adopted by the maintainer; [#2109](https://github.com/riscv/riscv-unified-db/pull/2109) unreachable-branch verification; [#2197](https://github.com/riscv/riscv-unified-db/pull/2197) `62a97783`, where my review prompted the PR and my later retraction reshaped it | GitHub API | **Those PRs are other people's.** Claim the review only. On #2197 the merged code follows my correction, not my original advice |
| **Sweep false positive (verified)** | `MXLEN` scalar vs `SXLEN`/`UXLEN`/`VSXLEN` array is **correct**: M-mode XLEN is fixed per hart; the others are runtime-switchable sets (`mstatus.SXL`/`UXL`, `hstatus.VSXL`). Flagged by invariant sweep, rejected on domain review, documented in #2145 | `workflow_slice/findings/` | Use as evidence of triage discipline, a machine flag that a human correctly refused to file |
| **Review-adopted upstream fix** | Comment on [#2090](https://github.com/riscv/riscv-unified-db/pull/2090) identified `0xfff` (4095) in both MTVEC alignment enums; maintainer jordancarlin: “I agree that it should be 4096. Updated accordingly.” #2090 merged with the correction | [PR #2090](https://github.com/riscv/riscv-unified-db/pull/2090) | “Review comment identified … maintainer adopted the correction.” **#2090 is jordancarlin’s PR, not ours** |
| **Adversarial review of skill PR** | 5-point review on [#2097](https://github.com/riscv/riscv-unified-db/pull/2097), all five adopted in `9d88fa4`. Eval pack at `workflow_slice/eval_2097/`, v2: **6 positives / 1 candidate / 4 negatives**, 2 of them recall-direction | monorepo; GitHub | Review + fixtures only; the skill is @uditjainstjis’s work |
| **Point 1 of that review was later revised** | The author revised the WARL rule in `72d18f7` and was right to: point 1 asked for a rejection gate where the design filters at human review, and it contradicted point 2 of the same comment. It also tested only over-firing; measured after, 63 conditional-writability sentences in the manual carry no `WARL` token against 5 that do | [follow-up comment](https://github.com/riscv/riscv-unified-db/pull/2097#issuecomment-5109644710); `eval_2097/MANIFEST.yaml` | **Never claim all five still stand.** Say four hold and one was revised, and that the observation survived while the remedy did not |
| **The structural test was proposed upstream, then reproduced mechanically** | The [#2097 follow-up](https://github.com/riscv/riscv-unified-db/pull/2097#issuecomment-5109644710) listed nine parameters that encode a legal-value set directly, read by hand from `param_schema.json`, and predicted the boolean-array counter parameters are mutability parameters under `NORM_CSR_RW`. `scripts/audit_param_schema_shapes.py`, written two days later from a rule stated before that list was consulted, selects the same nine and finds all five counter parameters labelled `NORM_CSR_RW` | [comment 5109644710](https://github.com/riscv/riscv-unified-db/pull/2097#issuecomment-5109644710); `analysis/param_schema_shapes.json`; `analysis/PARAM-SCHEMA-SHAPES.md` | Say **reproduced**, not discovered: the list was public first. The value is the independence of the two derivations, nine for nine and five for five. **These counts are not gated in `verify_claims.py` yet**, so do not call them harness-verified; they re-derive by running the script against a UDB checkout |
| **Taxonomy ambiguity found underneath it** | `taxonomy.md` routes `mstatus.MBE` to `NORM_CSR_WARL` via decision-tree step 4 while its `NORM_CSR_RW` class definition names those exact fields as its own example. UDB settles it: `type()` gates on `M_MODE_ENDIANNESS == "dynamic"` with no `sw_write` at all | [#2200](https://github.com/riscv/riscv-unified-db/issues/2200) | Filed, not merged. It is a documentation defect in an **unmerged** PR (#1766), so do not describe it as a UDB bug |

### The nine dual-model high-conf “new” candidates (not confirmed params)

`FLEN`, `IALIGN`, `ILEN`, `MISELECT_ACCESS`, `NUM_PRIVILEGE_MODES`, `PAUSE_DURATION`, `RNMI_EXCEPTION_TRAP_HANDLER_ADDRESS`, `SEED_CSR_ACCESS_CONTROL`, `SISELECT_MIN_RANGE`

---

## Forbidden or unsafe claims

| Do **not** say | Why |
|----------------|-----|
| Any recall figure without the name-list condition | All published recall is **grounding** recall with the 185 gold names supplied. Omitting that overstates it as discovery |
| “the model found / discovered N parameters” | It located them in a catalogue it was given |
| “discovery recall is X” | **Unmeasured.** Nothing in this repo measures extraction without the name list |
| “I built / authored Spring Part I” | Authorship is @ishaan-arora-1 / Spring PRs |
| “97 named parameters” | Measured **87/83** |
| “Pure gpt-4o full pilot / full multi-model matrix” | Pilot model-split; A is mini |
| “Mini matched or beat Claude” | 32.2% vs 72.9% |
| “v3 improved WARL” | WARL fell 3/24 → 2/24 |
| “9 overlapping names are real parameters” | **At least 2 verifiably are not.** `IALIGN` and `FLEN` are derived quantities |
| “dual-model agreement is a validated review gate” | It passed at least two non-parameters at high confidence |
| “Schema-valid means architecturally correct” | Structural check only |
| “Artifact C (CSR-field context) is done” | **Not run**; only prompt-v3 ablation done |
| Fake merge counts or SIG attendance | Not true |
| “Curated challenge results are live LLM scores” | Curated = CI gold; live = `results/live/` |
| “Holdout proved CSR context fixes WARL / clean temporal holdout success” | Primary is exploratory null under v1.2 limitations |
| “n=15 type fidelity equals live model re-derive” | Committed extraction pairs / mechanics scorer |
| Comparisons against other applicants / “guaranteed selection” | Strategy talk, not evidence. Never name another applicant in public text |
| Applicant counts / admission probability | Unknown; do not invent |

---

## Four red-team checks (apply to every sentence)

1. **Attribution**. Reproduction vs original authorship  
2. **Measurement**. Number in metrics/manifest?  
3. **Scope**. Model, corpus, denominator, prompt version stated?  
4. **Interpretation**. Claim only what the measurement shows?

---

## One-sentence narrative (memorize)

> I reproduced the Spring pipeline, measured where it fails across models and a WARL prompt ablation, built a schema-valid UDB export path, and have a concrete plan to turn generated findings into small human-reviewed upstream contributions.
