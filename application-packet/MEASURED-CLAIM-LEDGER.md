# Measured claim ledger — Part II application

**Purpose:** Every public or application claim must map to a source.  
**Primary sources:** `riscv-param-extraction/docs/metrics.md`, manifests, monorepo results JSON  
**Credit:** Spring Part I pipeline and committed Claude results — [@ishaan-arora-1](https://github.com/ishaan-arora-1) / PRs #1765–#1832. This campaign **reproduces and extends**; it does not claim Spring authorship.

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
| High-conf proposed-new both models | **9** names | metrics §5.4 | Candidates needing review. **State the retention gap:** the model-exclusive sets (227 / 209) were not committed and cannot be recomputed. Do not present the 9 as a validated review queue; an open prediction (H5, credited to @RAJVEER42) is that dual-model agreement selects for *easy* candidates. Unresolved until Artifact C |
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
| **Own upstream PR** | [#2138](https://github.com/riscv/riscv-unified-db/pull/2138) **OPEN**, `schema_defs.json` `4095`→`4096` in both `unsigned_pow2` enums + regression test in `run.rb`; filed with issue [#2137](https://github.com/riscv/riscv-unified-db/issues/2137) | GitHub | “**Opened**” only. Awaiting first-time-contributor workflow approval — **not merged** |
| **Own upstream PR (2)** | [#2146](https://github.com/riscv/riscv-unified-db/pull/2146) **OPEN** + issue [#2145](https://github.com/riscv/riscv-unified-db/issues/2145), `UXLEN` description named `SXLEN` as what `mstatus.UXL` changes; `SXLEN` option list used scalars against its array schema. Docs-only, +3/−3 | GitHub | “**Opened**” only — **not merged**. Docs correction; do not inflate to a schema fix |
| **Sweep false positive (verified)** | `MXLEN` scalar vs `SXLEN`/`UXLEN`/`VSXLEN` array is **correct**: M-mode XLEN is fixed per hart; the others are runtime-switchable sets (`mstatus.SXL`/`UXL`, `hstatus.VSXL`). Flagged by invariant sweep, rejected on domain review, documented in #2145 | `workflow_slice/findings/` | Use as evidence of triage discipline, a machine flag that a human correctly refused to file |
| **Review-adopted upstream fix** | Comment on [#2090](https://github.com/riscv/riscv-unified-db/pull/2090) identified `0xfff` (4095) in both MTVEC alignment enums; maintainer jordancarlin: “I agree that it should be 4096. Updated accordingly.” #2090 merged with the correction | [PR #2090](https://github.com/riscv/riscv-unified-db/pull/2090) | “Review comment identified … maintainer adopted the correction.” **#2090 is jordancarlin’s PR, not ours** |
| **Adversarial review of skill PR** | 5-point review on [#2097](https://github.com/riscv/riscv-unified-db/pull/2097) + frozen eval pack (5 positives / 4 negatives) at `workflow_slice/eval_2097/` | monorepo; GitHub | Review + fixtures only; the skill is @uditjainstjis’s work |

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
| “9 overlapping names are real parameters” | Candidates only |
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
