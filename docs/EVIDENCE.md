# Evidence and measurements

**Author:** Ibteshamul Haque ([@titoatwork](https://github.com/titoatwork))  
**Project:** [LFX Fall 2026 Part II](https://mentorship.lfx.linuxfoundation.org/project/22296947-cecb-4a8f-8bcb-4f34710e9f66)  
**Repository:** https://github.com/titoatwork/lfx-firstanalysis  
**Upstream census:** 2026-08-12 (GitHub API on [riscv/riscv-unified-db](https://github.com/riscv/riscv-unified-db); **9** merged / **9** open authored PRs / **19** authored issues; **54** unique issues+PRs involving `@titoatwork`; **0** PRs closed unmerged). Every figure here is produced by a command in [§2.6](#26-how-to-re-check-the-census).

This page records **what was measured** and **what was contributed upstream**, with links. Spring Part I pipeline and committed Claude results are by [@ishaan-arora-1](https://github.com/ishaan-arora-1) (PRs #1765-#1832); this repository **reproduces and extends** that public surface and does not claim Spring authorship.

Primary metric tables (including **§8 upstream-thread measurements**): [`docs/metrics.md`](../riscv-param-extraction/docs/metrics.md). Re-check numbers with [`./verify.sh`](../verify.sh).
---

## 1. Measurement notes (eval honesty)

### 1.1 Gold names are supplied in the prompt

On the Part I branches, every extraction prompt is assembled by `build_user_message()`, which injects all **185** names from `udb_param_names.txt` (set-identical to the pinned ground truth). The instruction is to reuse known names exactly when they match.

So published recall figures measure **grounding** (locate and evidence catalogue entries for a passage), not **discovery** of names without a list. That design fits the Spring spreadsheet/tagging goals. It is not evidence that a model can invent parameters unaided. Discovery under a sealed catalogue is unmeasured here; see `artifact_c/PREREGISTRATION.md`.

When citing 72.9%, 64.2%, 32.2%, or class rates, the name-list condition should be stated.

### 1.2 Single-run differences are noisy

On identical model, byte-identical prompt, `temperature=0`, two runs of the same arm scored **33.9%** and **44.6%** adjusted recall (2026-07-28). Per-class movement is large on small denominators (e.g. WARL 2/24 vs 9/24 across runs). Prompts match by hash; the scorer is deterministic and reproduces the published Claude figures. Treat single-run deltas of a few points as inside noise unless repeated.

Filed and discussed upstream: [#2163](https://github.com/riscv/riscv-unified-db/issues/2163).

### 1.3 Selected measured figures

| Measurement | Result | Source |
|-------------|--------|--------|
| UDB parameter count at corpus pin `c184e313` (regenerated gold) | **223** | metrics |
| Part I Claude output vs pinned GT185 | adj recall **72.9%**, class acc **88.4%**, WARL **12/24** | metrics; remeasure |
| Same output vs GT223 (corpus pin, not main) | adj recall **64.2%** | metrics |
| gpt-4o-mini Artifact A vs GT185 | adj recall **32.2%** (name list supplied) | metrics |
| Cross-model name Jaccard (same chunks/prompt) | **3.8%** | metrics |
| Schema-valid export (named / new drafts) | **83/83** and **20/20** structural only | metrics |
| Dual-run noise (headline) | **33.9%** vs **44.6%** | #2163 / local dual runs |

Full tables and caveats remain in [`docs/metrics.md`](../riscv-param-extraction/docs/metrics.md). Dual-model "new" high-confidence lists include derived non-parameters (e.g. `IALIGN`); agreement is not a validated review gate.

### 1.4 Spring public surface vs live work

Issue [#2053](https://github.com/riscv/riscv-unified-db/issues/2053) records that Spring PRs #1765-#1832 were an early public version and that later pipeline work may be internal. Public remeasures of those PRs describe a **snapshot**, not necessarily the current internal system.

---

## 2. Upstream contributions on riscv-unified-db

All links are under https://github.com/riscv/riscv-unified-db unless noted.

### 2.1 Merged pull requests authored by titoatwork (9)

| PR | Merged | Summary | Closes |
|----|--------|---------|--------|
| [#2138](https://github.com/riscv/riscv-unified-db/pull/2138) | 2026-07-29 | `unsigned_pow2` schema enums: 4095 -> 4096 | [#2137](https://github.com/riscv/riscv-unified-db/issues/2137) |
| [#2146](https://github.com/riscv/riscv-unified-db/pull/2146) | 2026-07-28 | SXLEN/UXLEN description corrections (docs) | [#2145](https://github.com/riscv/riscv-unified-db/issues/2145) |
| [#2189](https://github.com/riscv/riscv-unified-db/pull/2189) | 2026-07-29 | CACHE_BLOCK_SIZE constrained to powers of two | [#2188](https://github.com/riscv/riscv-unified-db/issues/2188) |
| [#2215](https://github.com/riscv/riscv-unified-db/pull/2215) | 2026-07-29 | SV32_VSMODE_TRANSLATION requirement concludes SV32, not SV39 | [#2214](https://github.com/riscv/riscv-unified-db/issues/2214) |
| [#2227](https://github.com/riscv/riscv-unified-db/pull/2227) | 2026-07-30 | vstval/vstvec `priv_mode` S -> VS | [#2226](https://github.com/riscv/riscv-unified-db/issues/2226) |
| [#2256](https://github.com/riscv/riscv-unified-db/pull/2256) | 2026-07-31 | Document `read_memory` return type / MXLEN width | [#2253](https://github.com/riscv/riscv-unified-db/issues/2253) (filed by ThinkOpenly) |
| [#2266](https://github.com/riscv/riscv-unified-db/pull/2266) | 2026-07-31 | Counter-enable parameters enforce description rules | [#2265](https://github.com/riscv/riscv-unified-db/issues/2265) |
| [#2362](https://github.com/riscv/riscv-unified-db/pull/2362) | 2026-08-04 | Supervisor and VS-mode trap CSRs take `length: SXLEN`/`VSXLEN`, not 64 | [#2361](https://github.com/riscv/riscv-unified-db/issues/2361) |
| [#2384](https://github.com/riscv/riscv-unified-db/pull/2384) | 2026-08-05 | `senvcfg` takes `length: SXLEN`, not 64 | [#2364](https://github.com/riscv/riscv-unified-db/issues/2364), opened at the maintainer's request on [#2361](https://github.com/riscv/riscv-unified-db/issues/2361) |

### 2.2 Open pull requests authored by titoatwork (9)

| PR | Summary | Relates |
|----|---------|---------|
| [#2289](https://github.com/riscv/riscv-unified-db/pull/2289) | Smoke check: string-enum params vs IDL string literals | [#2285](https://github.com/riscv/riscv-unified-db/issues/2285); data instance fixed earlier in [#2271](https://github.com/riscv/riscv-unified-db/pull/2271) |
| [#2255](https://github.com/riscv/riscv-unified-db/pull/2255) | VSXLEN/VUXLEN must support 32 when the parent mode can | [#2254](https://github.com/riscv/riscv-unified-db/issues/2254) |
| [#2212](https://github.com/riscv/riscv-unified-db/pull/2212) | idlc resolves `unsigned_pow2` schema $refs | [#2199](https://github.com/riscv/riscv-unified-db/issues/2199) |
| [#2164](https://github.com/riscv/riscv-unified-db/pull/2164) | Parameter-extraction evaluation fixtures | [#2158](https://github.com/riscv/riscv-unified-db/issues/2158), [#2097](https://github.com/riscv/riscv-unified-db/pull/2097) |
| [#2395](https://github.com/riscv/riscv-unified-db/pull/2395) | `sstateen0`-`sstateen3` take `length: SXLEN`, not MXLEN | [#2394](https://github.com/riscv/riscv-unified-db/issues/2394) |
| [#2414](https://github.com/riscv/riscv-unified-db/pull/2414) | `hstateen0h`-`hstateen3h` read through their parent's `sw_read` | [#2413](https://github.com/riscv/riscv-unified-db/issues/2413) |
| [#2419](https://github.com/riscv/riscv-unified-db/pull/2419) | `c.sdsp` uses its full 5-bit register index | [#2418](https://github.com/riscv/riscv-unified-db/issues/2418) |
| [#2435](https://github.com/riscv/riscv-unified-db/pull/2435) | misa-gated illegal-instruction checks consult `MISA_CSR_IMPLEMENTED` and route through `reserved_instruction()` | [#2434](https://github.com/riscv/riscv-unified-db/issues/2434) |
| [#2459](https://github.com/riscv/riscv-unified-db/pull/2459) | Instruction descriptions name the operands their own `assembly:` line declares (`xs1`/`xd`, and the RVC primes) | [#2458](https://github.com/riscv/riscv-unified-db/issues/2458) |

### 2.3 Issues filed by titoatwork (19)

| Issue | State | Topic |
|-------|-------|--------|
| [#2137](https://github.com/riscv/riscv-unified-db/issues/2137) | closed | schema_defs non-power-of-two 4095 |
| [#2145](https://github.com/riscv/riscv-unified-db/issues/2145) | closed | UXLEN/SXLEN description defects |
| [#2158](https://github.com/riscv/riscv-unified-db/issues/2158) | open | Where evaluation fixtures should live |
| [#2163](https://github.com/riscv/riscv-unified-db/issues/2163) | open | Run-to-run recall variance |
| [#2188](https://github.com/riscv/riscv-unified-db/issues/2188) | closed | CACHE_BLOCK_SIZE domain |
| [#2199](https://github.com/riscv/riscv-unified-db/issues/2199) | open | unsigned_pow2 $ref unhandled in idlc |
| [#2200](https://github.com/riscv/riscv-unified-db/issues/2200) | open | Taxonomy NORM_CSR_WARL vs NORM_CSR_RW (on unmerged #1766 surface) |
| [#2214](https://github.com/riscv/riscv-unified-db/issues/2214) | closed | SV32_VSMODE_TRANSLATION concludes wrong param |
| [#2226](https://github.com/riscv/riscv-unified-db/issues/2226) | closed | vstval/vstvec priv_mode |
| [#2254](https://github.com/riscv/riscv-unified-db/issues/2254) | open | VSXLEN/VUXLEN parent-child 32 support |
| [#2265](https://github.com/riscv/riscv-unified-db/issues/2265) | closed | Counter-enable requirements incomplete |
| [#2361](https://github.com/riscv/riscv-unified-db/issues/2361) | closed | Supervisor/VS trap CSRs carry `length: 64` instead of SXLEN/VSXLEN |
| [#2364](https://github.com/riscv/riscv-unified-db/issues/2364) | closed | `senvcfg` carries `length: 64` instead of SXLEN, closed by [#2384](https://github.com/riscv/riscv-unified-db/pull/2384) |
| [#2394](https://github.com/riscv/riscv-unified-db/issues/2394) | open | `sstateen0`-`sstateen3` carry `length: MXLEN` instead of SXLEN |
| [#2413](https://github.com/riscv/riscv-unified-db/issues/2413) | open | `hstateen0h`-`hstateen3h` read around the `mstateen` mask their parent applies |
| [#2418](https://github.com/riscv/riscv-unified-db/issues/2418) | open | `c.sdsp` maps its 5-bit `rs2` through `creg2reg`, so it stores from the wrong register |
| [#2434](https://github.com/riscv/riscv-unified-db/issues/2434) | open | misa-gated illegal-instruction checks do not honor `MISA_CSR_IMPLEMENTED` |
| [#2458](https://github.com/riscv/riscv-unified-db/issues/2458) | open | Instruction descriptions name operands the instruction does not declare. 33 files in six groups: **18** mechanical (fixed in [#2459](https://github.com/riscv/riscv-unified-db/pull/2459)), **3** correct as written, **1** already fixed by [#2419](https://github.com/riscv/riscv-unified-db/pull/2419), **11** needing a maintainer decision |
| [#2463](https://github.com/riscv/riscv-unified-db/issues/2463) | open | CSR length is computed without U or VU mode, and `max_length` raises on a core without the M extension |

### 2.4 Reviews and technical comments on other contributors' PRs and issues

These threads are **not** authored by titoatwork. Comments verify or refine the author's change, or
the thread exists because of an earlier comment. One row is a **mention** by another contributor
rather than a comment and is marked as such: `gh search --involves` counts mentions, so omitting it
would leave this table disagreeing with the command that produces the headline count.

| Thread | Author | Status | Comment / review |
|----|--------|--------|------------------|
| [#2090](https://github.com/riscv/riscv-unified-db/pull/2090) | jordancarlin | merged | Flagged non-power-of-two `0xfff` in MTVEC alignment enums ([comment](https://github.com/riscv/riscv-unified-db/pull/2090#issuecomment-5084258197)) |
| [#2109](https://github.com/riscv/riscv-unified-db/pull/2109) | krrishverma1805-web | merged | Review of unreachable `array_size == 0` branches |
| [#2197](https://github.com/riscv/riscv-unified-db/pull/2197) | krrishverma1805-web | merged | Follow-up correcting earlier FS-guard feedback ([comment](https://github.com/riscv/riscv-unified-db/pull/2197#issuecomment-5110068008)) |
| [#2103](https://github.com/riscv/riscv-unified-db/pull/2103) | uditjainstjis | merged | Corroboration of STVAL_WIDTH bounds ([comment](https://github.com/riscv/riscv-unified-db/pull/2103#issuecomment-5118523007)) |
| [#2245](https://github.com/riscv/riscv-unified-db/pull/2245) | Hiteshsai007 | merged | Independent check of three FP description fixes ([comment](https://github.com/riscv/riscv-unified-db/pull/2245#issuecomment-5142526646)) |
| [#2284](https://github.com/riscv/riscv-unified-db/pull/2284) | lntutor | merged | Verified Zilsd vs Zclsd for RV32 `sd` ([comment](https://github.com/riscv/riscv-unified-db/pull/2284#issuecomment-5146172752)) |
| [#2192](https://github.com/riscv/riscv-unified-db/pull/2192) | Hiteshsai007 | open | Review connecting emitter/validator to extraction fixtures ([comment](https://github.com/riscv/riscv-unified-db/pull/2192#issuecomment-5125684081)) |
| [#2155](https://github.com/riscv/riscv-unified-db/pull/2155) | Bhupesh-081 | open | Review of `long_name` replacements |
| [#2097](https://github.com/riscv/riscv-unified-db/pull/2097) | uditjainstjis | open | Design review of parameter-extraction skill; fixtures; later WARL reframe ([thread](https://github.com/riscv/riscv-unified-db/pull/2097)) |
| [#2282](https://github.com/riscv/riscv-unified-db/issues/2282) | ThinkOpenly | open | Withdrew my own `read_memory` return-type proposal from #2256 once henrikg-qc clarified the interface, and located the actual defect in the `ld`/`sd` IDL ([comment](https://github.com/riscv/riscv-unified-db/issues/2282#issuecomment-5162446049)) |
| [#2283](https://github.com/riscv/riscv-unified-db/issues/2283) | ThinkOpenly | closed | Filed by the maintainer from my #2256 comment: `sd` (RV32) checks `Zilcd` where it should check `Zilsd` |
| [#2285](https://github.com/riscv/riscv-unified-db/issues/2285) | ThinkOpenly | open | Took assignment for the enum-conditional validation this issue asks for; #2289 is that work ([comment](https://github.com/riscv/riscv-unified-db/issues/2285#issuecomment-5155460381)) |
| [#2317](https://github.com/riscv/riscv-unified-db/issues/2317) | Princess0407 | open | Showed the named blocker on the `MTVAL_WIDTH` TODO is already gone (**44** of **227** params carry requirements referencing another param), and that `SXLEN` being an array stops the M-mode form porting to S-mode ([comment](https://github.com/riscv/riscv-unified-db/issues/2317#issuecomment-5173500696)) |
| [#2171](https://github.com/riscv/riscv-unified-db/pull/2171) | Hiteshsai007 | merged | **Mention, not a comment.** The author cites the power-of-two test from #2138 as what actually catches this defect class, hex notation being readability only ([comment](https://github.com/riscv/riscv-unified-db/pull/2171#issuecomment-5106864830)) |

### 2.5 Mentorship and design discussion threads (measurements on the tracker)

These threads carry **numbers**, not only opinions. Full figure list: [`metrics.md` §8](../riscv-param-extraction/docs/metrics.md).

| Thread | Role | Measured contribution (summary) |
|--------|------|----------------------------------|
| [#2053](https://github.com/riscv/riscv-unified-db/issues/2053) | Participant | Grounding vs discovery; dual-model limits (e.g. `IALIGN`); claim corrections. [correction example](https://github.com/riscv/riscv-unified-db/issues/2053#issuecomment-5117676758) |
| [#2163](https://github.com/riscv/riscv-unified-db/issues/2163) | Author | **33.9% / 44.6%** dual-run; exact vs inexact tables (**72.9%** vs **32.2%** adjusted; exact-name **48.6%** vs **6.2%**) |
| [#2200](https://github.com/riscv/riscv-unified-db/issues/2200) | Author | WARL gold **26** = **4** decidable + **4** stale + **18** undecidable; IDL self-correction notes |
| [#2251](https://github.com/riscv/riscv-unified-db/issues/2251) | Participant (not proposal owner) | **9** closed-set schema params; WARL file-token vs gold-label unit split |
| [#1748](https://github.com/riscv/riscv-unified-db/issues/1748) | Participant | Taxonomy / parameter class examples |

#2251 is a Fall design discussion thread; contributions there are technical comments, not ownership of that proposal.

### 2.6 How to re-check the census

```bash
# authored: 9 merged, 9 open, 0 closed unmerged, 19 issues
gh pr list --repo riscv/riscv-unified-db --author titoatwork --state merged
gh pr list --repo riscv/riscv-unified-db --author titoatwork --state open
gh pr list --repo riscv/riscv-unified-db --author titoatwork --state closed   # merged ones re-listed; 0 others
gh issue list --repo riscv/riscv-unified-db --author titoatwork --state all

# unique threads involving the author (author OR assignee OR commenter OR mentioned): 54
{ gh search issues --involves=titoatwork --repo=riscv/riscv-unified-db --limit 200 --json number --jq '.[].number'
  gh search prs    --involves=titoatwork --repo=riscv/riscv-unified-db --limit 200 --json number --jq '.[].number'
} | sort -un | wc -l
```

The last command is the definition of the unique-thread figure, not a check on it. Until 2026-08-05
this page carried **41**, which was reached by hand and matched nothing: the API returned 43, and the
tables in §2.1-§2.5 then enumerated 38 distinct threads (40 rows, with #2163 and #2200 each listed
twice). The five it was missing are #2171, #2282, #2283, #2285 and #2317, now added to §2.4. With
those in place the tables enumerate exactly the threads the command returns, so the two can be
diffed instead of trusted.

The figure only moves when a new thread opens, so it goes stale silently. `check_census.py`
(offline) holds the headline, the README census row and the §2.1-§2.5 tables to one number;
`check_census.py --online` diffs that number against the API and names any thread listed nowhere.
That is what caught #2434 and #2435 missing on 2026-08-11, when the page still said 49 and the API
said **51**. Run the `--online` form before publishing the figure anywhere outside this repository.

---

## 3. Artifacts in this repository

| Path | Role |
|------|------|
| [`docs/metrics.md`](../riscv-param-extraction/docs/metrics.md) | Measured tables |
| [`artifact_c/`](../riscv-param-extraction/artifact_c/) | Preregistration / dual-run variance experiments |
| [`export/`](../riscv-param-extraction/export/) | Spreadsheet → draft UDB param YAML |
| [`workflow_slice/`](../riscv-param-extraction/workflow_slice/) | Eval fixtures + review/export path |
| [`./verify.sh`](../verify.sh) | Re-derive published figures from committed files |

---

## 4. One-line summary

Reproduction of the public Spring extraction surface with stated measurement limits; schema-valid export tooling; small linked fixes and reviews on [riscv-unified-db](https://github.com/riscv/riscv-unified-db); technical discussion on related design issues.
