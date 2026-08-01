# Measured claim ledger  -  Part II application

**Purpose:** Every public or application claim must map to a source.  
**Primary sources:** `riscv-param-extraction/docs/metrics.md`, manifests, monorepo results JSON  
**Last upstream census:** 2026-08-01 (live GitHub API).
**Credit:** Spring Part I pipeline and committed Claude results  -  [@ishaan-arora-1](https://github.com/ishaan-arora-1) / PRs #1765-#1832. This campaign **reproduces and extends**; it does not claim Spring authorship.

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
| Challenge control density | **4** bad fixtures · **4** hard negatives · **n=15** known-param mechanics · green monorepo CI | `challenge/README.md`; `ci_check.py` | Not "weaker kit"; packaging differs from dedicated-repo kits |
| Known-param n=15 | Existence **15/15**, type fidelity **15/15** on committed pairs | `benchmark/scripts/score_recall.py` | Mechanics only; not live multi-model re-derive; not corpus recall |
| Temporal holdout primary | **26/26**; name **0/10** both arms; WARL **0/5**; exploratory null under v1.2 limits | `temporal_holdout/results/PRIMARY_RESULTS.md`; PR #1 | Not clean temporal proof; neg FP not attributable to treatment |
| Open Spring PRs (context) | #1765-#1832 still the Part I surface | GitHub | "merge/export still open" |
| UDB PRs (when open) | Only original unclaimed fixes; STVAL/HPM already claimed by others | GitHub PR URLs | Never invent merges; comment ≠ PR |
| **Spring PRs are a superseded snapshot** | @ishaan-arora-1 in issue #2053: those PRs were "the first version of the pipeline"; current work "is internal and not uploaded on this repository yet" | [issue #2053](https://github.com/riscv/riscv-unified-db/issues/2053) | State this **before** citing any Part I remeasure; never present #1765-#1832 as current state |
| **Own upstream PRs, merged (7)** | #2138 #2146 #2189 #2215 #2227 #2256 #2266  -  full table in Upstream evidence trail | GitHub API census 2026-08-01 | Say **seven merged**. #2146 is docs-only. #2256 closes maintainer issue #2253. |
| **Own upstream PRs, open (4)** | #2289 #2255 #2212 #2164  -  full table in Upstream evidence trail | GitHub API 2026-08-01 | Say **four open**. Never say merged until the API says so |
| **Reviews/comments on others' PRs (see trail)** | [#2090](https://github.com/riscv/riscv-unified-db/pull/2090) MTVEC alignment adopted by the maintainer; [#2109](https://github.com/riscv/riscv-unified-db/pull/2109) unreachable-branch verification; [#2197](https://github.com/riscv/riscv-unified-db/pull/2197) `62a97783`, where my review prompted the PR and my later retraction reshaped it | GitHub API | **Those PRs are other people's.** Claim the review only. On #2197 the merged code follows my correction, not my original advice |
| **Sweep false positive (verified)** | `MXLEN` scalar vs `SXLEN`/`UXLEN`/`VSXLEN` array is **correct**: M-mode XLEN is fixed per hart; the others are runtime-switchable sets (`mstatus.SXL`/`UXL`, `hstatus.VSXL`). Flagged by invariant sweep, rejected on domain review, documented in #2145 | `workflow_slice/findings/` | Use as evidence of triage discipline, a machine flag that a human correctly refused to file |
| **Review-adopted upstream fix** | Comment on [#2090](https://github.com/riscv/riscv-unified-db/pull/2090) identified `0xfff` (4095) in both MTVEC alignment enums; maintainer jordancarlin: "I agree that it should be 4096. Updated accordingly." #2090 merged with the correction | [PR #2090](https://github.com/riscv/riscv-unified-db/pull/2090) | "Review comment identified … maintainer adopted the correction." **#2090 is jordancarlin's PR, not ours** |
| **Adversarial review of skill PR** | 5-point review on [#2097](https://github.com/riscv/riscv-unified-db/pull/2097), all five adopted in `9d88fa4`. Eval pack at `workflow_slice/eval_2097/`, v2: **6 positives / 1 candidate / 4 negatives**, 2 of them recall-direction | monorepo; GitHub | Review + fixtures only; the skill is @uditjainstjis's work |
| **Point 1 of that review was later revised** | The author revised the WARL rule in `72d18f7` and was right to: point 1 asked for a rejection gate where the design filters at human review, and it contradicted point 2 of the same comment. It also tested only over-firing; measured after, 63 conditional-writability sentences in the manual carry no `WARL` token against 5 that do | [follow-up comment](https://github.com/riscv/riscv-unified-db/pull/2097#issuecomment-5109644710); `eval_2097/MANIFEST.yaml` | **Never claim all five still stand.** Say four hold and one was revised, and that the observation survived while the remedy did not |
| **The structural test was proposed upstream, then reproduced mechanically** | The [#2097 follow-up](https://github.com/riscv/riscv-unified-db/pull/2097#issuecomment-5109644710) listed nine parameters that encode a legal-value set directly, read by hand from `param_schema.json`, and predicted the boolean-array counter parameters are mutability parameters under `NORM_CSR_RW`. `scripts/audit_param_schema_shapes.py`, written two days later from a rule stated before that list was consulted, selects the same nine and finds all five counter parameters labelled `NORM_CSR_RW` | [comment 5109644710](https://github.com/riscv/riscv-unified-db/pull/2097#issuecomment-5109644710); `analysis/param_schema_shapes.json`; `analysis/PARAM-SCHEMA-SHAPES.md` | Say **reproduced**, not discovered: the list was public first. The value is the independence of the two derivations, nine for nine and five for five. Gated in `verify_claims.py` under the `schema_shapes` tag, including the convergence as an invariant, so the agreement between the two audits fails loudly if a future edit breaks it |
| **Taxonomy ambiguity found underneath it** | `taxonomy.md` routes `mstatus.MBE` to `NORM_CSR_WARL` via decision-tree step 4 while its `NORM_CSR_RW` class definition names those exact fields as its own example. UDB settles it: `type()` gates on `M_MODE_ENDIANNESS == "dynamic"` with no `sw_write` at all | [#2200](https://github.com/riscv/riscv-unified-db/issues/2200) | Filed, not merged. It is a documentation defect in an **unmerged** PR (#1766), so do not describe it as a UDB bug |

### The nine dual-model high-conf "new" candidates (not confirmed params)

`FLEN`, `IALIGN`, `ILEN`, `MISELECT_ACCESS`, `NUM_PRIVILEGE_MODES`, `PAUSE_DURATION`, `RNMI_EXCEPTION_TRAP_HANDLER_ADDRESS`, `SEED_CSR_ACCESS_CONTROL`, `SISELECT_MIN_RANGE`


## Upstream evidence trail (census 2026-08-01)

**Repo:** [riscv/riscv-unified-db](https://github.com/riscv/riscv-unified-db)  
**Account:** [@titoatwork](https://github.com/titoatwork)  
**Method:** `gh pr list --author titoatwork`, `gh issue list --author titoatwork`, `gh api search/issues commenter:titoatwork`, per-thread comment/review dump.  
**Rule:** claim only what the API shows. Other people's PRs are never "yours" even if your comment landed in the merge.

### Headline counts (use these in essay)

| Kind | Count | Notes |
|------|------:|-------|
| Merged PRs authored | **7** | All closed with merge |
| Open PRs authored | **4** | Not merged as of census |
| Issues authored | **11** | 6 closed, 5 open |
| Distinct non-own PRs titoatwork commented or reviewed | **≥9** | #2090 #2109 #2197 #2103 #2245 #2284 #2192 #2155 #2097 |
| Distinct non-own issues with substantial titoatwork comments | **≥3** | #2053 #2251 #1748 (plus authored #2163 #2200) |

---

### A. Merged PRs authored by titoatwork (7)

| PR | Merged (UTC) | Title | Closes | One-line substance |
|----|--------------|-------|--------|-------------------|
| [#2138](https://github.com/riscv/riscv-unified-db/pull/2138) | 2026-07-29 | fix(schema): replace non-power-of-two 4095 with 4096 in unsigned_pow2 enums | [#2137](https://github.com/riscv/riscv-unified-db/issues/2137) | Schema enum power-of-two fix |
| [#2146](https://github.com/riscv/riscv-unified-db/pull/2146) | 2026-07-28 | docs(param): correct SXLEN and UXLEN parameter descriptions | [#2145](https://github.com/riscv/riscv-unified-db/issues/2145) | Docs-only; UXLEN prose named SXLEN; SXLEN examples scalar vs array |
| [#2189](https://github.com/riscv/riscv-unified-db/pull/2189) | 2026-07-29 | fix(param): constrain CACHE_BLOCK_SIZE to a power of two | [#2188](https://github.com/riscv/riscv-unified-db/issues/2188) | CMO block size domain; filed #2199 for $ref gap |
| [#2215](https://github.com/riscv/riscv-unified-db/pull/2215) | 2026-07-29 | fix(param): typo SV32_VSMODE_TRANSLATION should require SV32, not SV39 | [#2214](https://github.com/riscv/riscv-unified-db/issues/2214) | Requirement concluded wrong parameter |
| [#2227](https://github.com/riscv/riscv-unified-db/pull/2227) | 2026-07-30 | fix(csr): set priv_mode VS on vstval and vstvec | [#2226](https://github.com/riscv/riscv-unified-db/issues/2226) | VS CSRs wrongly priv_mode S |
| [#2256](https://github.com/riscv/riscv-unified-db/pull/2256) | 2026-07-31 | docs(idl): state what read_memory returns, and that the width is MXLEN | [#2253](https://github.com/riscv/riscv-unified-db/issues/2253) | Issue filed by **ThinkOpenly**; shipped the docs fix |
| [#2266](https://github.com/riscv/riscv-unified-db/pull/2266) | 2026-07-31 | fix(param): enforce counter-enable rules descriptions already state | [#2265](https://github.com/riscv/riscv-unified-db/issues/2265) | MCOUNTENABLE_EN / HCOUNTENABLE_EN requirements |

**Allowed:** "seven merged PRs on riscv-unified-db" with links.  
**Forbidden:** inventing more merges; calling #2146 a schema change; claiming #2253 as your issue.

---

### B. Open PRs authored by titoatwork (4)

| PR | Created | Title | Closes / relates | Note |
|----|---------|-------|------------------|------|
| [#2289](https://github.com/riscv/riscv-unified-db/pull/2289) | 2026-07-31 | fix(data): validate parameter enum string literals in IDL compares | [#2285](https://github.com/riscv/riscv-unified-db/issues/2285) | CI green at last check; instance typos already on main via #2271 |
| [#2255](https://github.com/riscv/riscv-unified-db/pull/2255) | 2026-07-30 | fix(param): require VSXLEN and VUXLEN to support 32 when parent can | [#2254](https://github.com/riscv/riscv-unified-db/issues/2254) | Open |
| [#2212](https://github.com/riscv/riscv-unified-db/pull/2212) | 2026-07-29 | fix(idlc): resolve unsigned_pow2 refs in IDL type resolver | [#2199](https://github.com/riscv/riscv-unified-db/issues/2199) | Open; only Ruby/idlc change among yours |
| [#2164](https://github.com/riscv/riscv-unified-db/pull/2164) | 2026-07-28 | test(param-eval): add parameter-extraction evaluation fixtures | Relates [#2158](https://github.com/riscv/riscv-unified-db/issues/2158), [#2097](https://github.com/riscv/riscv-unified-db/pull/2097) | Open |

---

### C. Issues authored by titoatwork (11)

| Issue | State | Title | Linked fix |
|-------|-------|-------|------------|
| [#2137](https://github.com/riscv/riscv-unified-db/issues/2137) | CLOSED | schema_defs unsigned_pow2 4095 | #2138 merged |
| [#2145](https://github.com/riscv/riscv-unified-db/issues/2145) | CLOSED | UXLEN/SXLEN description defects | #2146 merged |
| [#2158](https://github.com/riscv/riscv-unified-db/issues/2158) | OPEN | Convention: evaluation fixtures placement | #2164 open |
| [#2163](https://github.com/riscv/riscv-unified-db/issues/2163) | OPEN | Extraction recall varies ~10 pts identical runs | Author + exact/inexact follow-up |
| [#2188](https://github.com/riscv/riscv-unified-db/issues/2188) | CLOSED | CACHE_BLOCK_SIZE non-power-of-two domain | #2189 merged |
| [#2199](https://github.com/riscv/riscv-unified-db/issues/2199) | OPEN | param schemas cannot use unsigned_pow2 $defs | #2212 open |
| [#2200](https://github.com/riscv/riscv-unified-db/issues/2200) | OPEN | taxonomy NORM_CSR_WARL vs NORM_CSR_RW | Measurement follow-up (4/4/18) |
| [#2214](https://github.com/riscv/riscv-unified-db/issues/2214) | CLOSED | SV32_VSMODE_TRANSLATION concludes SV39 | #2215 merged |
| [#2226](https://github.com/riscv/riscv-unified-db/issues/2226) | CLOSED | vstval/vstvec priv_mode S | #2227 merged |
| [#2254](https://github.com/riscv/riscv-unified-db/issues/2254) | OPEN | VSXLEN/VUXLEN upper-only bounds | #2255 open |
| [#2265](https://github.com/riscv/riscv-unified-db/issues/2265) | CLOSED | counter-enable requirements missing | #2266 merged |

**Maintainer issues implemented against:** [#2253](https://github.com/riscv/riscv-unified-db/issues/2253) (ThinkOpenly) → #2256; [#2285](https://github.com/riscv/riscv-unified-db/issues/2285) (ThinkOpenly) → #2289 (checker; data instance was #2271 by jordancarlin).

---

### D. Comments / reviews on other people's PRs

Claim form only: "I reviewed / verified / corrected feedback on X; the PR remains AUTHOR's."

| Their PR | Author | State | Contribution | Evidence |
|----------|--------|-------|-------------------|----------|
| [#2090](https://github.com/riscv/riscv-unified-db/pull/2090) | jordancarlin | **MERGED** | Flagged `0xfff` (4095) in MTVEC alignment enums | [comment](https://github.com/riscv/riscv-unified-db/pull/2090#issuecomment-5084258197) |
| [#2109](https://github.com/riscv/riscv-unified-db/pull/2109) | krrishverma1805-web | **MERGED** | Review: unreachable array_size==0 branches safe vs schema | GitHub review COMMENTED |
| [#2197](https://github.com/riscv/riscv-unified-db/pull/2197) | krrishverma1805-web | **MERGED** | Retracted earlier FS-guard advice (cannot fire under definedBy F\|S) | [comment](https://github.com/riscv/riscv-unified-db/pull/2197#issuecomment-5110068008) |
| [#2103](https://github.com/riscv/riscv-unified-db/pull/2103) | uditjainstjis | **MERGED** | Corroborated STVAL_WIDTH bounds from WIDTH census | [comment](https://github.com/riscv/riscv-unified-db/pull/2103#issuecomment-5118523007) |
| [#2245](https://github.com/riscv/riscv-unified-db/pull/2245) | Hiteshsai007 | **MERGED** | Independent verification of three FP description fixes | [comment](https://github.com/riscv/riscv-unified-db/pull/2245#issuecomment-5142526646) |
| [#2284](https://github.com/riscv/riscv-unified-db/pull/2284) | lntutor | OPEN | Verified Zilsd vs Zclsd for RV32 sd | [comment](https://github.com/riscv/riscv-unified-db/pull/2284#issuecomment-5146172752) |
| [#2192](https://github.com/riscv/riscv-unified-db/pull/2192) | Hiteshsai007 | OPEN | Review linking emitter to #2164 fixtures | [comment](https://github.com/riscv/riscv-unified-db/pull/2192#issuecomment-5125684081) |
| [#2155](https://github.com/riscv/riscv-unified-db/pull/2155) | Bhupesh-081 | OPEN | Review of long_name replacements | GitHub review COMMENTED |
| [#2097](https://github.com/riscv/riscv-unified-db/pull/2097) | uditjainstjis | OPEN | Multi-comment design review + fixtures + WARL reframe; revised own point 1 | [5084907776](https://github.com/riscv/riscv-unified-db/pull/2097#issuecomment-5084907776) … [5109644710](https://github.com/riscv/riscv-unified-db/pull/2097#issuecomment-5109644710) |

**Safest "helped their merge" lines:**

1. **#2090**  -  identified concrete enum defect; PR later merged with power-of-two alignment path. **Not your PR.**  
2. **#2103**  -  bounds corroboration before merge. **Not your PR.**  
3. **#2245**  -  independent check; author thanked; merged. **Not your PR.**  
4. **#2197**  -  withdrew bad advice so merged fix matches corrected model. **Not your PR.**

Never: "I got their PR merged."

---

### E. Issue threads (including mentorship)  -  expanded census 2026-08-01

**Method:** every issue where `@titoatwork` is author or commenter on `riscv/riscv-unified-db` (API). Pure PRs excluded.

#### E1. Mentorship / LFX threads (highest weight for Part II story)

| Issue | Author | State | Comments by titoatwork | Chars (titoatwork) | Contribution |
|-------|--------|-------|--------------:|------------:|----------------------|
| [#2053](https://github.com/riscv/riscv-unified-db/issues/2053) | hjaat | OPEN | **10** / 27 total | **~28k** | Spring scope honesty: public #1765-#1832 is a snapshot not live pipeline; gold-name catalogue in prompts (grounding vs discovery); Smpmpmt / capacity / IALIGN corrections; dual-run instability; withdraw single-run WARL class claim; exact vs inexact alignment |
| [#2251](https://github.com/riscv/riscv-unified-db/issues/2251) | KhanRayyan3622 | OPEN | **3** / 10 total | **~6k** | Fall WARL Layer 2 proposal: accept metric corrections; three-way + schema-shape from #2097; pin gold units (185 params vs prose files); mentor-facing decidable definition after Allen |
| [#1748](https://github.com/riscv/riscv-unified-db/issues/1748) | ishaan-arora-1 | OPEN | **1** / 3 total | **~3k** | Taxonomy ordering: MTVEC_MODES vs MTVEC_ACCESS as defining examples of different NORM classes |

**#2053  -  thread map (the 10 titoatwork comments, chronological):**

1. Public Part I is a **snapshot** if pipeline is internal ([5091343921](https://github.com/riscv/riscv-unified-db/issues/2053#issuecomment-5091343921))
2. **Catalogue injection**: every prompt gets all 185 gold names ([5092372573](https://github.com/riscv/riscv-unified-db/issues/2053#issuecomment-5092372573))
3. Generalising non-parameter cases (e.g. Smpmpmt) ([5095661270](https://github.com/riscv/riscv-unified-db/issues/2053#issuecomment-5095661270))
4. Capacity / cache case: correct excerpt still wrong justification ([5095957882](https://github.com/riscv/riscv-unified-db/issues/2053#issuecomment-5095957882))
5. **IALIGN** not a parameter  -  dual-model high-conf false positive ([5096124587](https://github.com/riscv/riscv-unified-db/issues/2053#issuecomment-5096124587))
6. Registered evidence-type / baiting rules before run ([5098706651](https://github.com/riscv/riscv-unified-db/issues/2053#issuecomment-5098706651))
7. Reproducibility: exclusive sets recovered; counts match ([5104713439](https://github.com/riscv/riscv-unified-db/issues/2053#issuecomment-5104713439))
8. Byte-identical prompts, raw response hash: almost no exact model replay ([5106898104](https://github.com/riscv/riscv-unified-db/issues/2053#issuecomment-5106898104))
9. Exact vs alignment layer; multi-model side ([5111139448](https://github.com/riscv/riscv-unified-db/issues/2053#issuecomment-5111139448))
10. **Withdraw** single-run "WARL worst class" / related overclaims ([5117676758](https://github.com/riscv/riscv-unified-db/issues/2053#issuecomment-5117676758))

**Allowed essay line for #2053:** multi-comment technical participation correcting your own metrics and clarifying Spring baseline; not "I own the issue."

**#2251  -  not your issue.** Author is another Fall applicant. Three titoatwork comments:

1. Ground Layer 2 in #2097 three-way + 26/4/4/18 measurement ([5133411956](https://github.com/riscv/riscv-unified-db/issues/2251#issuecomment-5133411956))
2. Pin units: NORM_CSR_WARL lives in gold/#1766, not UDB tree; 48/34/116 prose units differ ([5136611535](https://github.com/riscv/riscv-unified-db/issues/2251#issuecomment-5136611535))
3. Mentor-facing: decidable = closed array+items.enum used via includes/size; hgatp multi-boolean; jvt mutability ([5147443108](https://github.com/riscv/riscv-unified-db/issues/2251#issuecomment-5147443108))

**Allowed:** shaped Fall discussion with tree-backed measurements.  
**Forbidden:** "my Fall WARL project" / naming the other applicant in public application text.

**#1748:** taxonomy class examples already separate NORM_CSR_WARL vs NORM_CSR_RW ([5099729964](https://github.com/riscv/riscv-unified-db/issues/1748#issuecomment-5099729964)).

---

#### E2. Issues authored by titoatwork that carry discussion (not only ticket+PR)

| Issue | State | Extra discussion | Substance |
|-------|-------|------------------|-----------|
| [#2163](https://github.com/riscv/riscv-unified-db/issues/2163) | OPEN | Body + [follow-up](https://github.com/riscv/riscv-unified-db/issues/2163#issuecomment-5103703438) (~3k) | ~10-point run variance; exact vs inexact match share; model-kind gap |
| [#2200](https://github.com/riscv/riscv-unified-db/issues/2200) | OPEN | Body + [measurement](https://github.com/riscv/riscv-unified-db/issues/2200#issuecomment-5126765953) (~3k) | Taxonomy vs IDL; membership/cardinality idioms; 4/4/18; NORM_DIRECT on *XLEN |
| [#2158](https://github.com/riscv/riscv-unified-db/issues/2158) | OPEN | Body only (0 replies yet) | Where evaluation fixtures should live; gates #2164 |
| [#2199](https://github.com/riscv/riscv-unified-db/issues/2199) | OPEN | Body only | unsigned_pow2 $ref unhandled in idlc; #2212 |
| [#2254](https://github.com/riscv/riscv-unified-db/issues/2254) | OPEN | Body only | VSXLEN/VUXLEN parent-child 32 support; #2255 |

Closed ticket-style (issue + merged PR, little/no thread): #2137, #2145, #2188, #2214, #2226, #2265.

---

#### E3. Issue-thread volume (for "lots of discussion" honesty)

| Thread | titoatwork comment count | Approx. titoatwork text |
|--------|-------------------:|------------------:|
| #2053 | 10 | ~28,000 chars |
| #2251 | 3 | ~6,100 chars |
| #2163 | 1 (+ issue body) | ~3,100 chars comment |
| #2200 | 1 (+ issue body) | ~3,100 chars comment |
| #1748 | 1 | ~2,900 chars |
| **Mentorship-weighted (#2053+#2251+#1748)** | **14 comments** | **~37k chars** |

Plus 11 issue bodies authored by titoatwork.

---

#### E4. Forbidden issue-thread wordings

| Do not say | Why |
|------------|-----|
| "I lead the Fall WARL mentorship thread" | #2251 is another applicant's issue |
| "Mentors endorsed my proposal on #2251" | Allen posted observations; no formal endorsement of you |
| "I closed Spring #2053" | Still open; you participated |
| Inflate comment counts without links | Use tables above |

### F. Essay theme map

| Theme | Primary evidence |
|-------|------------------|
| Schema / param domain | #2138 #2189 #2215 #2266 #2255 |
| CSR / IDL | #2227 #2256 |
| Eval honesty / mentorship discussion | #2163 #2053 #2251 #2200 #1748 prework |
| WARL / taxonomy judgment | #2200 #2097 #2251 |
| Tooling / fixtures / guards | #2164 #2212 #2289 |
| Collaborative review | #2090 #2103 #2245 #2197 #2284 |

---

### G. Forbidden upstream wordings

| Do not say | Why |
|------------|-----|
| "Five merged PRs" | Stale; **seven** as of 2026-08-01 |
| "I merged #2090 / #2245 / #2103" | Wrong author |
| "I own #2251 Fall WARL project" | Another applicant filed it |
| "All my reviews became merges" | Several open |
| "I fixed always_zero in #2289" | Instance was **#2271**; #2289 is the checker |
| "Approved by mentor" | No formal approval claimed |

---

### H. Re-derive

```bash
gh pr list --repo riscv/riscv-unified-db --author titoatwork --state merged
gh pr list --repo riscv/riscv-unified-db --author titoatwork --state open
gh issue list --repo riscv/riscv-unified-db --author titoatwork --state all
```

Census date: **2026-08-01**. Re-run before freeze if more merges land.

## Forbidden or unsafe claims

| Do **not** say | Why |
|----------------|-----|
| Any recall figure without the name-list condition | All published recall is **grounding** recall with the 185 gold names supplied. Omitting that overstates it as discovery |
| "the model found / discovered N parameters" | It located them in a catalogue it was given |
| "discovery recall is X" | **Unmeasured.** Nothing in this repo measures extraction without the name list |
| "I built / authored Spring Part I" | Authorship is @ishaan-arora-1 / Spring PRs |
| "97 named parameters" | Measured **87/83** |
| "Pure gpt-4o full pilot / full multi-model matrix" | Pilot model-split; A is mini |
| "Mini matched or beat Claude" | 32.2% vs 72.9% |
| "v3 improved WARL" | WARL fell 3/24 → 2/24 |
| "9 overlapping names are real parameters" | **At least 2 verifiably are not.** `IALIGN` and `FLEN` are derived quantities |
| "dual-model agreement is a validated review gate" | It passed at least two non-parameters at high confidence |
| "Schema-valid means architecturally correct" | Structural check only |
| "Artifact C (CSR-field context) is done" | **Not run**; only prompt-v3 ablation done |
| Fake merge counts or SIG attendance | Not true |
| "Curated challenge results are live LLM scores" | Curated = CI gold; live = `results/live/` |
| "Holdout proved CSR context fixes WARL / clean temporal holdout success" | Primary is exploratory null under v1.2 limitations |
| "n=15 type fidelity equals live model re-derive" | Committed extraction pairs / mechanics scorer |
| Comparisons against other applicants / "guaranteed selection" | Strategy talk, not evidence. Never name another applicant in public text |
| Applicant counts / admission probability | Unknown; do not invent |

---

## Four red-team checks (apply to every sentence)

1. **Attribution**. Reproduction vs original authorship  
2. **Measurement**. Number in metrics/manifest?  
3. **Scope**. Model, corpus, denominator, prompt version stated?  
4. **Interpretation**. Claim only what the measurement shows?

---

## One-sentence narrative (memorize)

> I reproduced the Spring pipeline, measured where it fails across models and a WARL prompt ablation, built a schema-valid UDB export path, and landed seven merged riscv-unified-db PRs plus technical comments on mentorship threads (#2053, #2251) and on other contributors' merged work.
