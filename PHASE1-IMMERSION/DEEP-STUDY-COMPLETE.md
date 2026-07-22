# Deep Study: LFX AI-Assisted Architectural Parameter Extraction (Part II)

**For:** Ibteshamul Haque (`titoatwork`)  
**Purpose:** Single master reading document — everything relevant to selection  
**Compiled:** 2026-07-21  
**Sources:** Local UDB clone (`lfx-1832`), GitHub issues/PRs, Part I results, SIG RSS, LFX plan, measured local runs  
**Companion pack:** `PHASE1-IMMERSION/` (raw dumps); UDB live tree: `../riscv-unified-db/`

---

## 0. How to use this document

| If you need… | Go to section |
|--------------|---------------|
| What the program wants | §1 |
| What Part I already built | §2–4 |
| Exact metrics & gaps | §5 |
| How the code works | §6 |
| Taxonomy / what a parameter is | §7 |
| UDB repo & contribution rules | §8 |
| SIG / mentors / politics | §9 |
| Your measured work so far | §10 |
| Phase 2 A/B/C plan → objectives | §11 |
| Cover letter numbers later | §12 |
| Risks & etiquette | §13 |
| File map on disk | §14 |

**Selection bar (your definition):** rejection is irrational if the packet shows (1) reproduced Part I, (2) measured multi-model or clear ablation, (3) SIG presence, (4) UDB YAML export path, (5) 9-week plan mapped to 5 objectives, (6) reviewable artifacts.

---

## 1. The target program

| Field | Value |
|-------|--------|
| **Name** | AI-assisted extraction of architectural parameters – **Part II** |
| **LFX URL** | https://mentorship.lfx.linuxfoundation.org/project/22296947-cecb-4a8f-8bcb-4f34710e9f66 |
| **ID** | `22296947-cecb-4a8f-8bcb-4f34710e9f66` |
| **Mentors** | **Allen Baum** (spec/precision/cert mindset), **Ajit Dingankar** (AI-for-V&V, metrics) |
| **Primary repo** | https://github.com/riscv/riscv-unified-db |
| **Apply by** | Official: **2026-08-05** · Plan: submit **Jul 31–Aug 2** (not last day) |
| **Term** | ~Sep 15–Nov 15 · **≥30 h/wk** |
| **Seats** | ~1 paid (RVI first mentee) |
| **Related community** | Parameters SIG (`sig-parameters`), UnifiedDB SIG (`sig-unifieddb`) |

### Official Part II objectives (map everything here)

1. **LLM extract** privileged + unprivileged ISA material; improve against gold standards:  
   (a) Manual chapter YAML · (b) Drive keyword_matches · (c) UDB YAML — **improve recall**
2. **Extend classification scheme**
3. **AI agents/skills**, reproducible workflows
4. **Export → UDB YAML**
5. **Reviewed PR** + merge follow-up

### Mentor psychology (write artifacts to both)

| Mentor | Cares about | Your artifact style |
|--------|-------------|---------------------|
| **Allen Baum** | Spec precision, certification/testability, reviewability | Justification/reasoning fields, provenance per param, no sloppy eagerness, ask before big PRs |
| **Ajit Dingankar** | AI for validation, metrics, baselines, ablations | Numbers tables, v1/v2/model comparisons, honest failures, run manifests |

Ajit also runs Parameters SIG agendas (e.g. 2026-07-17 agenda: James Ball manual extraction + UDB export; Ishaan/Allen Gen-AI pipeline update).

---

## 2. What is an “architectural parameter”?

From Part I taxonomy and v2 system prompt (authoritative for this project):

> An **architectural parameter** is a choice the RISC-V **spec explicitly leaves to the hardware implementer**.  
> It is **not** a fixed “must/shall for all implementations,” **not** pure runtime SW behavior, **not** content only in NOTE/TIP blocks.

**Classes (decision order in LLM prompt):**

| Class | Meaning | Example |
|-------|---------|---------|
| `NON_NORM` | Inside NOTE/TIP/WARNING — do not extract | — |
| `NON_ISA` | Platform/physical, outside ISA | reset vector |
| `DOC_RULE` | Documentation/reporting requirement, not arch behavior | — |
| `NORM_CSR_WARL` | Parameter **is** the set of **legal values** of a WARL CSR field | `MTVEC_MODES`, `SATP_MODE_BARE` |
| `NORM_CSR_RW` | Whether a CSR/field is RO vs RW | `MUTABLE_MISA_C`, counter-inhibit bits |
| `SW_RULE` | Looks impl-defined but SW can force outcome | `HW_MSTATUS_FS_DIRTY_UPDATE` |
| `NORM_DIRECT` | Design-time choice, not CSR-controlled | `MXLEN`, `NUM_PMP_ENTRIES`, `PHYS_ADDR_WIDTH` |
| `UNKNOWN` | Cannot classify | — |

**Value types:** `binary` · `enum` · `range` · `set` · `bitmask` · `value` · (GT also uses `conditional`)

**Critical false-positive traps (from prompt):**
- “may” as *permission to software* ≠ parameter  
- “when field X = Y” behavior description ≠ parameter (the parameter is which X values are legal)  
- Fixed requirements applying to all implementations ≠ parameter  

Full text: `04-pipeline-docs/taxonomy.md`, `04-pipeline-docs/system_prompt-v2.txt`

---

## 3. Spring Part I — full phase map

**Mentee:** @ishaan-arora-1  
**Parallel contributor context:** @ankit-cybertron (separate activity; do not spam either)  
**Code location:** **not on `main`** — live on PR branches / local `lfx-*`  
**Fullest local checkout:** `lfx-1832`

### Issues (plans) — complete set

| Issue | Title | Role |
|-------|--------|------|
| [#1747](https://github.com/riscv/riscv-unified-db/issues/1747) | Phase 1: Ground truth map from UDB | GT export + spec map + classify |
| [#1748](https://github.com/riscv/riscv-unified-db/issues/1748) | Phase 2: Taxonomy & LLM prompts | `taxonomy.md`, prompts, few-shots |
| [#1749](https://github.com/riscv/riscv-unified-db/issues/1749) | Phase 3: Spec chunking | `chunker.py`, CSR-atomic chunks |
| [#1750](https://github.com/riscv/riscv-unified-db/issues/1750) | Phase 4: LLM extraction pipeline | multi-model extract, pilot machine.adoc |
| [#1751](https://github.com/riscv/riscv-unified-db/issues/1751) | Phase 5: Analyze across models & UDB | metrics, multi-model matrix |
| [#1752](https://github.com/riscv/riscv-unified-db/issues/1752) | Phase 6: Iterative prompt refinement | v2/v3, target recall >80% |
| [#1753](https://github.com/riscv/riscv-unified-db/issues/1753) | Phase 7: Final spreadsheet | `parameters.csv` / xlsx |
| [#1754](https://github.com/riscv/riscv-unified-db/issues/1754) | Phase 8: Insert `[#param:…]` tags | isa-manual tagging PR path |

Raw bodies: `02-github-issues/all-lfx-issues-bodies.md`

### PRs (implementation) — all still **open** as of study date

| PR | Title | Local branch |
|----|--------|--------------|
| [#1765](https://github.com/riscv/riscv-unified-db/pull/1765) | Phase 1 ground truth | `lfx-1765` |
| [#1766](https://github.com/riscv/riscv-unified-db/pull/1766) | Phase 2 taxonomy + prompts | `lfx-1766` |
| [#1791](https://github.com/riscv/riscv-unified-db/pull/1791) | Phase 4 extraction pipeline | `lfx-1791` |
| [#1792](https://github.com/riscv/riscv-unified-db/pull/1792) | Phase 5 analysis & metrics | `lfx-1792` |
| [#1793](https://github.com/riscv/riscv-unified-db/pull/1793) | Phase 6 v2 prompts + results | `lfx-1793` |
| [#1831](https://github.com/riscv/riscv-unified-db/pull/1831) | Phase 7 spreadsheet | `lfx-1831` |
| [#1832](https://github.com/riscv/riscv-unified-db/pull/1832) | Phase 8 param tags | `lfx-1832` |

**Important:** PRs are large (hundreds of files) because they carry `param_extraction/` + chunk/results data. They are **not merged to main**; study via branches.

---

## 4. Part I pipeline architecture (end-to-end)

```
spec/std/isa/param/*.yaml  ──export_udb_params──► ground_truth.json
                                                      │
ext/riscv-isa-manual/src/*.adoc ──map_params_to_spec──► spec_mappings.json
                                                      │
                                              generate_report ──► phase1_report.txt
                                                                  parameters_catalog.csv
                                                                  udb_param_names.txt

isa-manual .adoc ──chunker──► chunks/ (79 chunks, 74 files)
         │
         ▼
prompts/v{1,2}/ + extract.py ──LLM──► results/{v2/}claude-sonnet-4/chunk_*.json
         │
         merge ──► all_results_*.json
         │
         analyze.py ──► deduped, alignment, metrics, discrepancies
         │
         generate_spreadsheet ──► parameters.csv / .xlsx
         │
         insert_tags.py ──► [#param:NAME] in adoc + patch for isa-manual upstream
```

### Scripts inventory (`param_extraction/scripts/`)

| Script | Role |
|--------|------|
| `export_udb_params.py` | Phase 1.1 — YAML → `ground_truth.json` |
| `map_params_to_spec.py` | Phase 1.2 — keyword map to adoc |
| `generate_report.py` | Phase 1 final report + catalog CSV |
| `chunker.py` | Phase 3 — semantic chunks, CSR-atomic |
| `run_prompt.py` / `validate_prompt.py` | Phase 2 prompt assembly / validation |
| `extract.py` | Phase 4 — pilot / run / merge / status |
| `analyze.py` | Phase 5 — dedup, align, metrics, discrepancies |
| `generate_spreadsheet.py` | Phase 7 |
| `insert_tags.py` | Phase 8 |

Heads of all scripts: `04-pipeline-docs/scripts-heads.md`

### Chunking rules (issue #1749 → implemented)

- **Never split mid-CSR section** (WARL needs full field context)  
- Split at `===` / `====` headings  
- Target ~2.5k–3.5k lines; small files whole  
- Overlap from previous section for context  
- **Actual manifest (lfx-1832):** `total_chunks=79`, `total_files=74`, `total_lines=53006`  
- **Pilot file:** `machine.adoc` (highest parameter density)

### Extraction models wired in `extract.py`

| Alias | Provider | Model ID | Display |
|-------|----------|----------|---------|
| `claude` | anthropic | `claude-sonnet-4-20250514` | `claude-sonnet-4` |
| `gpt4o` | openai | `gpt-4o-2024-11-20` | `gpt-4o` |
| `gemini` | google | `gemini-2.5-pro` | `gemini-2.5-pro` |

CLI: `extract.py pilot|run|merge|status --model {claude,gpt4o,gemini}`  
Issue #1750: temperature 0, pilot first, log tokens, estimate **~$5–15 per full model run**.

### JSON schema per extracted param

```json
{
  "excerpt": "exact sentence",
  "line_number": 478,
  "parameter_name": "SUGGESTED_NAME",
  "existing_udb_name": "UDB_NAME_or_null",
  "class": "NORM_CSR_WARL",
  "value_type": "set",
  "confidence": "high|medium|low",
  "reasoning": "one sentence"
}
```

**Baum-relevant:** mandatory `reasoning` / justification culture.

### Analysis (`analyze.py`) — what “recall” means

- **Dedup:** same name across chunks → keep highest confidence; prefer content region over overlap  
- **Align to UDB:** exact, fuzzy, stem, concept groups, curated **one-to-many** groups (`one_to_many_groups.json`)  
- **Debug exclusion:** params with prefixes `DBG_`, `DCSR_`, `TRIGGER_`, `TDATA_`, `MCONTEXT_`, `HCONTEXT_`, `SCONTEXT_` excluded from **adjusted** recall (debug spec not in extraction corpus)  
- **Adjusted recall** = matched non-debug UDB / non-debug UDB total  
- **Classification accuracy** = among exact-ish matches, class agreement  
- **Discrepancy types** (observed in v2 CSV):  
  `LLM_NEW_HIGH_CONF`, `LLM_NEW_MEDIUM_CONF`, `UDB_RECALL_MISS`, `UDB_RECALL_MISS_DEBUG`, `CLASS_DISAGREEMENT`, `NAMING_MISMATCH`, (+ ONE_TO_MANY in code)

### Phase 8 tagging (#1832)

- Introduces **`[#param:NAME]`** namespace (parallel to existing `[#norm:…]`)  
- **321 tags** inserted (97.3% of medium+ rows); 9 unmatched  
- Fuzzy match: **do not trust LLM line numbers** as exact  
- Output: patch for follow-on PR to `riscv/riscv-isa-manual`  
- Future work stated in PR: add **new** params as UDB YAML under `spec/std/isa/param/` — this is **Part II / your Artifact B** territory

---

## 5. Part I metrics (the numbers that matter)

### V1 → V2 (from PR #1793 writeup)

| Metric | V1 | V2 | Delta |
|--------|----|----|-------|
| Deduped unique params | 215 | **346** | +61% |
| Raw recall | 60.0% | **69.7%** | +9.7 pp |
| **Adjusted recall** | 62.7% | **72.9%** | +10.2 pp |
| Classification accuracy | 67.9% | **88.4%** | +20.5 pp |
| New params discovered | 153 | **256** | +67% |
| NORM_DIRECT recall | 47% | **83%** | +36 pp |
| NORM_CSR_RW recall | 41% | **63%** | +22 pp |
| **NORM_CSR_WARL recall** | 25% | **50%** | +25 pp |

V2 wins: classification disambiguation + “commonly missed patterns” in prompt; analysis lift (one-to-many groups + stem) made recall honest for multi-variant UDB names.

### Committed v2 metrics file (local)

```
total_udb_params: 185
debug_spec_params: 8
total_llm_params_deduped: 346
adjusted_recall: 72.9%
classification_accuracy: 88.4%
WARL: 12/24 (50%)
CSR_RW: 32/51
DIRECT: 83/100
new_params_total: 256
```

### Token usage (v2 full run, claude-sonnet-4)

| | |
|--|--|
| Chunks with results in merge | 60 (of 79 planned; some chunks may be empty/skipped) |
| Total parameters (pre-dedup stream) | 361 |
| Input tokens | **1,030,983** |
| Output tokens | **83,189** |
| Errors | 0 |

### Discrepancy CSV counts (v2)

| Type | Count |
|------|------:|
| LLM_NEW_HIGH_CONF | 233 |
| LLM_NEW_MEDIUM_CONF | 23 |
| UDB_RECALL_MISS | 48 |
| UDB_RECALL_MISS_DEBUG | 8 |
| CLASS_DISAGREEMENT | 10 |
| NAMING_MISMATCH | 3 |

### Spreadsheet (`parameters.csv`)

| | |
|--|--:|
| Rows | 346 |
| `named=yes` | **87** (handoff said ~97 — use **measured 87** or re-verify naming rules; don’t invent 97) |
| Classes (all rows) | DIRECT 205 · CSR_RW 87 · WARL 38 · DOC_RULE 9 · NON_ISA 5 · SW_RULE 2 |

### Unfinished Part I goals (your openings)

| Planned (issues) | Reality |
|------------------|---------|
| ≥2 LLMs full extraction (#1750) | Pipeline supports 3 models; **public results dominated by Claude v2** |
| Three-way Claude × GPT-4o × UDB matrix (#1751) | **Not delivered as headline artifact** → **Artifact A** |
| Convergence recall >80% (#1752) | Stopped at **72.9%** adjusted |
| WARL strong | Still **~50%** → stretch **Artifact C** |
| New params → UDB YAML files | Called out as **future work** in #1832 → **Artifact B** |
| Multi-model agreement metrics | Explicit in #1751 deliverables → **A** |

---

## 6. Deep code notes (for reproduction & A/B)

### `export_udb_params.py`
- Reads `spec/std/isa/param/*.yaml`, skips `MOCK_*`  
- Derives value types from JSON Schema (`boolean`→binary, min/max→range, oneOf+when→conditional, …)  
- Cross-links CSR IDL references  
- Heuristic classification → GT  
- **Our regen (2026-07-21):** **223** params (UDB grew since 185 freeze)

### `map_params_to_spec.py`
- Multi-strategy keyword search over 74 adoc files  
- Scores candidates; notes normative vs NOTE blocks  
- Our regen: 100% any match, 91% strong (≥5)

### `extract.py`
- Rate limiter for Anthropic TPM  
- Providers: Anthropic, OpenAI, Google  
- `PROMPT_VERSION` env (v1/v2 dirs)  
- `pilot` = machine.adoc path  
- `run` = all chunks; `merge` = all_results; `status` = progress  

### `analyze.py` path caveat
- Default `RESULTS_DIR = results/` (v1 layout)  
- Part I headline numbers live in **`results/v2/`**  
- For multi-model A: store as `results/v2/` or parallel model dirs + point analysis correctly  

### No reverse YAML exporter in Part I scripts
- `export_udb_params` is **UDB YAML → JSON GT**, not CSV → YAML  
- **Artifact B is new work:** `parameters.csv` → draft `param/*.yaml` validating against `param_schema.json`

### `param_schema.json` (required fields)

```
$schema: "param_schema.json#"   (const)
kind: "parameter"               (const)
name, long_name, description, definedBy, schema
optional: requirements, $source
additionalProperties: false
```

Samples on disk: `05-schemas-samples/param-yaml/{PHYS_ADDR_WIDTH,NUM_PMP_ENTRIES,MTVEC_MODES,MXLEN,ASID_WIDTH,ARCH_ID_VALUE}.yaml`

---

## 7. UDB repository (what you’re joining)

| | |
|--|--|
| **Repo** | https://github.com/riscv/riscv-unified-db |
| **Stars / forks** (approx at study) | ~196 ★ / ~198 forks |
| **Purpose** | Machine-readable RISC-V data (extensions, instructions, CSRs, params, prose) + generators |
| **Languages** | Ruby-heavy tooling, C++ backends, Python tools, schemas in JSON |
| **Key tree** | `spec/std/isa/param/`, `spec/schemas/`, `backends/`, `ext/riscv-isa-manual` submodule |
| **Docs** | https://riscv.github.io/riscv-unified-db/docs-preview (WIP) |
| **UDB SIG** | Coordinates with RVI; public discussion also on lists |

### Contribution rules (from CONTRIBUTING.adoc)

- Issues for bugs/features; PRs for fixes/data  
- Link “Closes #N”  
- Must pass `./bin/regress` (heavy)  
- Squash merge; Conventional Commits preferred  
- ≥1 Code Owner approval (`.github/CODEOWNERS`)  
- Default license BSD-3-Clear; **no copyleft**  
- REUSE/SPDX hygiene  

### Etiquette for *you* (playbook — critical)

1. Prototype in **your** public GitHub (`titoatwork`), not drive-by giant UDB PRs  
2. After A+B: short note + link on **sig-parameters** (“reproduced Part I, multi-model, draft export — feedback welcome”)  
3. Optional: one comment on relevant UDB issue  
4. **Ask on-list** before opening a large draft PR  
5. Slack `#risc-v-mentorship-questions` = **logistics only**, never technical design  

---

## 8. Parameters SIG & parallel ecosystem

### Lists
| List | URL / subscribe |
|------|-----------------|
| Parameters SIG | https://lists.riscv.org/g/sig-parameters · `sig-parameters+subscribe@lists.riscv.org` |
| UnifiedDB SIG | https://lists.riscv.org/g/sig-unifieddb |
| Portal | https://lists.riscv.org (membership required to post) |

### Recent public archive themes (RSS digest — not full 50+)

1. **2026-07-17 agenda (Ajit):** James Ball — manual parameter extraction + export to UDB; Ishaan + Allen — Gen-AI pipeline update; M-mode params for RVM profile  
2. **2026-06-29 UDB↔Parameters discussion (James Ball et al.):**  
   - Per-chapter hand-written `params.yaml` (friendlier than UDB YAML)  
   - Tools → `params.json` + **export to individual UDB YAML** + HTML  
   - Sync needed between manual SIG work and **AI extraction**  
   - Generators / clear static vs generated file layout in UDB  
3. Meeting notes, chair self-noms (Ajit), mentorship status reports (May)

**Strategic read for Artifact B:** mentors already care about **params → UDB YAML export**. Align B with that conversation; don’t invent a competing schema casually — target `param_schema.json` and mention James Ball’s chapter-params direction as context when you post.

### Calendar / Slack (still to do same day)
- Tech calendar: https://tech.riscv.org/calendar/  
- Slack invite (from RVI site): join → `#risc-v-mentorship-questions` only for process  

### Membership status (you)
- Individual Schedule A **submitted** (processing ≤1 week)  
- Email: `ibteshamulhaque01@gmail.com`  
- Student mail used earlier: `ibteshamul.123421@stu.upes.ac.in`  
- Kendall Perez notified; list join after roster maps  
- Employer on form: **UPES** (UM = June attachment only)

---

## 9. Part II objectives ↔ your Phase 2 artifacts

| Obj | Meaning | Your artifact |
|-----|---------|----------------|
| **1** Improve LLM extract + recall | Second model + honest metrics vs Claude 72.9% baseline | **A** multi-model run + agreement |
| **2** Extend classification | Document confusion (esp WARL/RW/DIRECT); optional schema notes | A class tables + taxonomy notes; later C |
| **3** Agents/skills, reproducible workflows | Run manifests: model, version, seeds, tokens, $ | Every run folder + README |
| **4** Export → UDB YAML | CSV/named set → draft YAML + schema validation | **B** exporter |
| **5** Reviewed PR + merge follow-up | Only after list OK / mentor invite | Draft PR *later*, not unsolicited dump |

### Artifact A (required) — detail

- Run **their** pipeline (`extract.py` v2 prompts preferred) on **gpt4o or gemini**  
- Cost: issue estimate ~$5–15; plan says ~$5–10  
- Deliver:  
  - Per-class recall table vs **claude-sonnet-4**  
  - Inter-model agreement  
  - Hallucination-overlap (both invent vs one finds)  
  - **Honest numbers if worse** — evaluation discipline is the brand  
- This closes the **#1751 multi-model gap**

### Artifact B (required) — detail

- Input: `parameters.csv`  
- Start with **`named=yes`** rows (~87 measured) — verify against existing `spec/std/isa/param/*.yaml` as built-in GT  
- Then 10–20 **new** candidates as **drafts**  
- Validate against `param_schema.json` (+ UDB tooling if available)  
- Maps Obj 4 → feeds Obj 5  

### Stretch C (only if A+B done)

- WARL recall attack: inject CSR-field YAML context into chunks  
- Target lift on NORM_CSR_WARL from ~50% (even +10 pp is headline)

---

## 10. What *you* have already measured (local)

| Work | Result |
|------|--------|
| Clone + fetch PRs `lfx-1765`…`1832` | Done |
| isa-manual submodule | Done (74 adoc) |
| Phase 1 GT regen | **223** params; DIRECT 140 · CSR_RW 55 · WARL 26 · SW_RULE 2 |
| Spec map | 100% any / 91% strong |
| Re-run analyze on v2 Claude vs committed GT185 | **72.9% / 88.4% exact match to Part I** |
| Same vs live GT223 | Adjusted recall **64.2%** (UDB grew; WARL still 50%) |
| Pilot extract | **Not done** (API key) |
| Public A/B repo | Not started |

**Cover-letter-ready three lines (after pilot + A, extend):**
1. Reproduced Phase 1 GT pipeline (export→map→report); current tree 223 params vs Part I freeze 185.  
2. Remeasured Part I v2 Claude results: **72.9% adjusted recall, 88.4% class accuracy, WARL 50%**.  
3. (Pending) Second-model comparison + YAML export prototypes — links.

Files: `06-measured-local/metrics_summary.json`, `phase1_report-regenerated.txt`

---

## 11. Phase calendar (your plan)

| Phase | Dates | Focus |
|-------|-------|--------|
| **1 Immersion** | Jul 20–24 | Membership, list, calendar, Slack logistics, clone, read, GT, pilot |
| **2 Prototype** | Jul 24–31 | Public repo: **A** then **B** (+C stretch) |
| **3 Application** | Jul 31–Aug 2 | Cover letter weapon + 1-page resume; submit |
| **4 Warm** | Aug 2–Sep | SIG meetings, iterate public, interview = walkthrough |

### Cover letter skeleton (Phase 3)

1. Who + research (IoT IDS, on-device LLM, **Prof. Por Lip Yee**, UM **June attachment**; degree home **UPES**)  
2. “I reproduced Part I” — 3 lines with **your** numbers  
3. “I built X” — A/B links + tables  
4. **9-week plan** 1:1 to 5 objectives, fortnight milestones, explicit metrics (e.g. 72.9%→85%+; WARL 50%→75%; N YAML drafts)  
5. 30 h/wk credible; UTC+8 flexible for US-Pacific; honest limitations  

### Parallel apps
- CFI/DFI on Sargantana etc. with **separate** letters; Part II primary  

---

## 12. Competitive / political landscape (compressed)

| Factor | Note |
|--------|------|
| Part I PRs still open | Merges may lag; your work should not depend on merge |
| James Ball manual pipeline | Parallel human gold path; export-to-UDB already in SIG discussion |
| Fork spike after LFX listing | Competition proxies only — no public applicant count |
| ~1 paid seat | Quality of reviewable artifacts > volume of emails |
| Outreach Ankit/Ishaan | Already sent per handoff — **wait**, don’t spam |

---

## 13. Risks, non-goals, discipline

| Do | Don’t |
|----|-------|
| Measure honestly | Fake multi-model or inflated recall |
| Manifest every run | Silent one-off demos |
| List first for big PR | Unsolicited megadiff on UDB |
| Logistics on mentorship Slack | Technical design on mentorship Slack |
| Keep COLIDE confidential | Link private COLIDE |
| Personal Gmail for lists post-membership | Confuse work vs membership email |

---

## 14. On-disk map (everything collected)

### Master pack
`Desktop\LFX-Mentorship\PHASE1-IMMERSION\`

| Path | Content |
|------|---------|
| **`DEEP-STUDY-COMPLETE.md`** | **This file** |
| `INDEX.md` | Pack index |
| `01-lfx-project/` | Project card |
| `02-github-issues/` | #1747, #1751, **all LFX issue bodies**, related search |
| `03-part1-prs/` | PR 1765–1832 bodies, file lists, discussions |
| `04-pipeline-docs/` | taxonomy, v2 prompt, script heads, STUDY-DIGEST |
| `05-schemas-samples/` | param_schema + sample YAMLs |
| `06-measured-local/` | Your metrics & phase1 report |
| `07-sig-parameters/` | RSS + digest |
| `08-udb-docs/` | CONTRIBUTING, README, isa-manual index |
| `09-pointers/` | Clone, membership, playbook |

### Live code (not duplicated)
`Desktop\LFX-Mentorship\riscv-unified-db\` · branch **`lfx-1832`** · branches `lfx-1765`…`lfx-1832` · `ext/riscv-isa-manual`

### Older notes (seed only)
`lfx-riscv-param-extraction-prework/`, `DEEP-STUDY-AI-PART-II.md`, `COMPETITION-UDB-ANALYSIS.md`, `HANDOFF-CONTRIBUTOR.md`, `PHASE1-STATUS.md`

---

## 15. Immediate next actions (priority)

1. **Read this file fully once**  
2. **Calendar + Slack** (same day — logistics only on Slack)  
3. **Pilot:** `extract.py pilot --model claude` (or gpt4o) when API key ready — machine.adoc  
4. **Scaffold public repo** for A then B  
5. Membership/list when Kendall/RVI completes  
6. Application packet only after measured A+B  

### Pilot command (when ready)

```powershell
cd "C:\Users\Ibteshamul Haque\Desktop\LFX-Mentorship\riscv-unified-db"
# set ANTHROPIC_API_KEY or OPENAI_API_KEY or Gemini creds
python param_extraction\scripts\extract.py pilot --model claude
```

### Reproduce GT anytime ($0)

```powershell
python param_extraction\scripts\export_udb_params.py
python param_extraction\scripts\map_params_to_spec.py
python param_extraction\scripts\generate_report.py
```

---

## 16. One-page mental model

```
ISA AsciiDoc ──chunk──► LLM(v2 taxonomy) ──► params + class + reasoning
                              │
                     align to UDB GT (185 freeze / 223 live)
                              │
              metrics: recall 72.9% · class 88.4% · WARL 50%
                              │
         Part II: +second model (A) + YAML export (B) + SIG presence
                              │
                    9-week plan ↔ 5 LFX objectives → application
```

You are not applying as a generic student. You are applying as someone who **runs the same evaluation loop mentors already defined in #1747–#1754**, with **public, reviewable deltas**.

---

*End of deep study. Raw evidence under `PHASE1-IMMERSION/`; code under `riscv-unified-db/`.*
