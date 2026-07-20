# Deep research — AI params Part II (re-done, primary sources)

**Compiled:** 2026-07-19  
**Sources:** LFX project API; `riscv/riscv-unified-db` issues/PRs (#1747–#1832, #1765–#1793, #1790, #1772, #1803); Parameter SIG list; param schema + live YAML; prior shallow STUDY notes superseded for technical depth.

---

## 0. Why the first study pass was “too fast”

The first pass used mostly:

- LFX one-paragraph description  
- README / repo tree skim  
- ~228 param file count  

It **missed** the real artifact trail:

| Missed | Why it matters |
|--------|----------------|
| **Spring 2026 LFX phase issues #1747–#1754** | Full work breakdown written by mentees |
| **Open PRs #1765–#1832** (ishaan-arora-1) | Actual pipeline, metrics, code paths (`param_extraction/`) |
| **Parallel track #1790, #1772, #1803** (ankit-cybertron) | Second mentee / RAG-classifier line |
| **Nothing of that on `main`** | `param_extraction/` **not** in default tree — work lives on **open PRs**, not released main |
| **Parameter SIG** | Organizational home after Spring; ongoing meetings (e.g. 2026-06-26 notes, 2026-07-17 agenda) |
| **V1→V2 metrics** | Concrete recall/accuracy numbers Part II must beat |

This document fixes that.

---

## 1. Project identity (official)

| Field | Value |
|-------|--------|
| Name | AI-assisted extraction of architectural parameters from RISC-V specifications – **Part II** |
| LFX ID | `22296947-cecb-4a8f-8bcb-4f34710e9f66` |
| Org | RISC-V International |
| Mentors | **Allen Baum**, **Ajit Dingankar** |
| Listed skills | Generative AI, ISA specifications, Parameterized modeling |
| Listed repo | https://github.com/riscv/riscv-unified-db |
| Term (API) | 2026-09-15 → 2026-11-15 |
| Apps | 2026-07-15 → 2026-08-05 |

### Official Fall goals (verbatim intent)

1. Keep extracting params with LLMs from **privileged + unprivileged** specs; train/eval on gold from:  
   - (a) ISA Manual per-chapter YAML  
   - (b) Google Drive **keyword_matches** spreadsheet  
   - (c) **UDB yaml** (improve recall)  
2. Extend **classification scheme** as needed  
3. **AI coding agents/skills** for reproducible runs (prompt + context management)  
4. Integrate ISA-Manual tools → export **UDB yaml**  
5. **GitHub PR** of reviewed parameter files + maintainer follow-up  

**Fall framing:** quality + **implementation robustness** (Spring improved steadily but not enough).

---

## 2. Ecosystem: Parameter SIG + UDB + ACT culture

### Parameter SIG

- List: https://lists.riscv.org/g/sig-parameters (~28 members, 46+ topics)  
- Jira/group: RVG-931  
- Recent public topics (2026):  
  - Agenda 2026/07/17  
  - “UDB and Parameters discussion”  
  - Meeting notes 2026/06/26  
  - Chair/Vice-chair self-nominations  
- Historical thread themes (public snippets):  
  - Parameters include **legal values** and **encoding**  
  - UDB is **a** destination, not the only Parameter SIG deliverable  
  - Naming: UPPERCASE_CAMEL for param names and some rule names  

**Implication for mentee:** you are not only “hacking a repo”; you feed a **SIG + UDB + possibly isa-manual tagging** pipeline.

### Mentors

| Mentor | Public signal | Expectation |
|--------|---------------|-------------|
| **Allen Baum** | Decade+ RISC-V; Architecture Test SIG / certification; test format, trap handler, coverpoints | Spec-faithful definitions, testable clarity, low tolerance for hand-wavy “impl-defined” |
| **Ajit Dingankar** | UDB contributor; ~30y Intel/IBM arch; **AI for V&V**, modeling, formal, HLS | Modeling rigor, validation metrics, AI that reduces verification cost |

### UDB role

UDB = machine-readable RISC-V (exts, insts, CSRs, **params**, configs) + generators.  
Params drive configurations, hart generators, constraints (IDL / Z3 paths exist; some anyOf/oneOf still incomplete — see open issues).

Live `main` (~2026-07): **~228** param YAMLs under `spec/std/isa/param/` (Spring docs used **185** non-MOCK — catalog grew).

---

## 3. Spring 2026 LFX — what was actually built

Two public contributor lines on `riscv-unified-db`:

### Track A — ishaan-arora-1 (primary phased LFX)

Phased issues filed ~2026-03-22; implementation PRs ~Mar–May 2026. **All major LFX PRs still OPEN (not merged to main as of this research).**

| Phase | Issue | PR | Core artifact |
|-------|-------|-----|----------------|
| 1 Ground truth | #1747 | **#1765** | Catalog 185 UDB params → `ground_truth.json`, spec mappings, CSV |
| 2 Taxonomy + prompts | #1748 | **#1766** | `taxonomy.md`, system prompt, few-shots, `run_prompt.py` |
| 3 Chunking | — | **#1783** | AsciiDoc-aware `chunker.py` → **78 chunks**, 0 CSR section splits |
| 4 Extract | #1750 | **#1791** | `extract.py`, Claude full run, ~$3.60, 59 chunks |
| 5 Analyze | #1751 | **#1792** | `analyze.py`, metrics, discrepancy taxonomy |
| 6 Refine V2 | — | **#1793** | Prompt v2, large metric gains |
| 7 Spreadsheet | #1753 | **#1831** | `parameters.csv` / xlsx, 330 rows ≥ medium conf |
| 8 Spec tags | #1754 | **#1832** | `[#param:NAME]` into isa-manual (321 tags), patch for upstream |

**Code lives under proposed path:** `param_extraction/` (scripts, data, prompts, results) — **absent from default `main` tree** (confirmed: 0 matching paths on main recursive tree).

### Track B — ankit-cybertron (parallel / complementary)

| Item | State | Focus |
|------|-------|--------|
| #1772 RAG knowledge base | closed PR | Schema recursion, CSR IDL cross-ref, rag vs analysis modes |
| #1790 Spec chunking AsciiDoc+UDB | open PR | Dual chunkers, `chunks_repo.json` |
| #1803 AsciiDoc classifier | open PR | Rules engine; reduced UNKNOWN rate; more non_CSR_parameters |

LinkedIn-style bios reference Ankit as LFX’26 on AI-assisted extraction — consistent with this track.

---

## 4. Technical design (Spring) — deep detail

### 4.1 What is a parameter? (operational)

From taxonomy used in Phase 1–2:

| Class | Meaning | Examples |
|-------|---------|----------|
| **NORM_DIRECT** | Implementation must choose; not a CSR field’s WARL set | `NUM_PMP_ENTRIES`, `PHYS_ADDR_WIDTH`, `MXLEN` |
| **NORM_CSR_WARL** | Set of **legal values** of a WARL CSR field | `MTVEC_MODES`, legal FS values |
| **NORM_CSR_RW** | Whether field/CSR is RO vs RW / mutability | `MTVEC_ACCESS`, `MUTABLE_MISA_C` |
| **SW_RULE** | Looks impl-defined but SW-deterministic if rules followed | `HW_MSTATUS_FS_DIRTY_UPDATE` |
| **NON_ISA** | Platform (reset/NMI vectors, etc.) | |
| **NON_NORM** | NOTE/TIP/WARNING only | |
| **DOC_RULE** | Documentation/reporting, not arch behavior | |
| **UNKNOWN** | Needs human | |

Phase 1 counts (185 UDB non-MOCK):  
NORM_DIRECT 102 (55%), NORM_CSR_RW 55 (30%), NORM_CSR_WARL 26 (14%), SW_RULE 2 (1%).  
Value types: binary 60%, enum 19%, range 6%, …  
CSR cross-refs: 51%. Spec text mapped: 183/185 (98%).

**UDB file shape** (`param_schema.json`):

- Required: `$schema`, `kind: parameter`, `description`, `long_name`, `definedBy`, `schema` (JSON Schema for legal values)  
- Optional: `requirements` (IDL conditions), `$source`  
- Live examples still have many `long_name: TODO` — data quality debt.

### 4.2 Spec corpus

- Spring Phase 1: **74** `.adoc` files, **52,602** lines (isa-manual submodule)  
- Chunking Phase 3: **78** chunks; CSR `====` sections **never split**; target ~2.5–3.5k lines; 30-line overlap  
- Multi-chunk files: `machine.adoc`, `scalar-crypto.adoc`, `v-st-ext.adoc`, `vector-crypto.adoc`  
- Pilot density: **`machine.adoc`** highest parameter density  

### 4.3 Prompt architecture (three layers)

1. **System** (~800 tokens): role, task, condensed taxonomy, JSON schema, anti-hallucination rules  
2. **Few-shot** (~2–3k tokens): positive per class + negatives (NOTE text, non-params, “may” as permission, CSR behavior that is not a param)  
3. **User**: optional UDB name list + **one spec chunk**

Design choices documented in #1766:

- Single-pass extract+classify (preserve context)  
- Mandatory `reasoning` field  
- `skipped_non_parameters` to force boundary awareness  
- Section-boundary-aware chunking  

### 4.4 Extraction output schema (per hit)

```json
{
  "excerpt": "exact clause from spec",
  "line_number": 478,
  "parameter_name": "MSTATUS_XPP_LEGAL_VALUES",
  "existing_udb_name": "null or UDB name",
  "class": "NORM_CSR_WARL",
  "value_type": "set",
  "confidence": "high|medium|low",
  "reasoning": "one sentence"
}
```

Models used/planned: Claude (actual full runs), GPT-4o / Gemini recommended for multi-model comparison.  
`temperature=0`; retry on bad JSON; token cost logging.

### 4.5 Metrics (the numbers Part II must beat)

From Phase 5–6 PR writeups (Claude, UDB gold = 185):

| Metric | V1 | V2 | Notes |
|--------|----|----|--------|
| Deduped unique LLM params | 215 | **346** | |
| Raw recall vs UDB | 60.0% | **69.7%** | |
| Adjusted recall | 62.7% | **72.9%** | after one-to-many / alignment |
| Classification accuracy | 67.9% | **88.4%** | |
| New discoveries (not in UDB) | 153 | **256** | need human review |
| NORM_DIRECT recall | 47% | **83%** | |
| NORM_CSR_RW recall | 41% | **63%** | |
| NORM_CSR_WARL recall | 25% | **50%** | hardest class |

**Acceptance in Phase 5 issue:** recall ≥70% for at least one model — V2 **adjusted** ~73% clears; raw still ~70%. WARL class still weak.

Discrepancy types (Phase 5):

- LLM hallucination (FP)  
- UDB gap (true new param)  
- UDB recall miss (FN)  
- Classification disagreement  
- Naming mismatch  

Alignment tricks: exact, fuzzy, stem/prefix, **curated one-to-many groups** (e.g. 10 `REPORT_VA_IN_MTVAL_ON_*` UDB rows ↔ one spec sentence), concept groups.

### 4.6 Spreadsheet + tagging (Phases 7–8)

- **330** rows confidence ≥ medium  
- 97 already named in UDB, **233 newly discovered** (untrusted until review)  
- Classes: NORM_DIRECT 208, NORM_CSR_RW 63, NORM_CSR_WARL 52, …  
- Phase 8: **321/330** tags inserted as `[#param:NAME]#…#` mirroring `[#norm:…]` convention  
- Fuzzy match on excerpt (don’t trust LLM line numbers)  
- Patch produced for `riscv-isa-manual` submodule; **upstream merge still open problem**

---

## 5. What “Part II” really means (synthesis)

Spring delivered a **research prototype pipeline** + metrics + spreadsheet + draft manual tags — **not** a merged, maintainer-blessed, production UDB integration.

| Fall goal | Spring gap to close |
|-----------|---------------------|
| Quality | Push recall past ~73% adjusted; especially **NORM_CSR_WARL**; reduce hallucinations among 233 “new” |
| Robustness | Code not on main; multi-model; Python/version fragility (3.13 fixes already appeared); rate limits; chunk overlap bugs |
| Classification | Extend taxonomy if WARL/RW/DIRECT still confuses models; Ankit classifier track may merge ideas |
| Agents/skills | UDB has instruction-extract **skill** pattern; parameter pipeline not yet first-class “agent skills” product |
| UDB YAML export | Spreadsheet ≠ valid `param_schema` files with `definedBy` + JSON Schema + IDL requirements |
| PR merge | #1765–#1832 still open; need reviewable, smaller, schema-valid PRs maintainers accept |

**Part II success = not redoing Phase 1 from zero; = productize + evaluate + land.**

Also gold sources (b) spreadsheet / (a) chapter YAMLs may only be fully available **after selection** (Drive access).

---

## 6. Live UDB param system (main branch facts)

- Path: `spec/std/isa/param/*.yaml`  
- Schema: `spec/schemas/param_schema.json`  
- Docs fragment: `doc/docs/schemas/v0.1/param_schema.mdx`  
- Related: `cfgs/*.yaml` consume params; backends (e.g. cpp_hart_gen) generate from architecture  
- Open quality work on main (non-LFX): PMP param overhaul, HPM_COUNTER_EN semantics, Z3 anyOf gaps, ZAWRS params, etc.  
- MOCK fixtures existed in Spring (22 excluded from 185)  

Example complexity: `HPM_EVENTS` is an **array** param with huge `definedBy` anyOf over `HPM_COUNTER_EN[i]` — hard for LLMs and for constraint solvers.

---

## 7. Failure modes (what kills quality)

From Spring design + metrics:

1. **Treating NOTE/informative text as normative params**  
2. **CSR behavior ≠ architectural parameter** (must classify correctly)  
3. **One-to-many**: one sentence defines many UDB names  
4. **Naming mismatch** LLM name ≠ UDB name (recall undercounted without alignment)  
5. **Chunk overlap double-counting** (partially fixed mid-pipeline)  
6. **Line numbers wrong** → tagging must fuzzy-match excerpts  
7. **Hallucinated “new” params** inflate discoveries  
8. **WARL legal-value sets** under-extracted (50% recall class)  
9. **Export gap**: free JSON/CSV ≠ schema-valid UDB YAML with IDL  

---

## 8. Skills a Fall mentee needs (honest)

| Must | Nice | Not central |
|------|------|-------------|
| Python engineering | Multi-LLM APIs | CUDA / COLIDE-style GPU |
| Read ISA AsciiDoc carefully | Ruby/UDB internals | Full RTL |
| Eval design (precision/recall, alignment) | JSON Schema | |
| Git + small reviewable PRs | Agent skill packaging | |
| Spec taxonomy thinking | Z3/IDL constraints | |

---

## 9. How to study this deeply (actionable)

1. **Read open PR descriptions in order:** #1765 → #1766 → #1783 → #1791 → #1792 → #1793 → #1831 → #1832  
2. **Checkout PR branches** (when applying pre-work) — `param_extraction/` only exists there  
3. **Read 10 param YAMLs** + `param_schema.json` on main  
4. **Open `machine.adoc`** in isa-manual submodule; find WARL / “implementation-defined” language  
5. **Skim Parameter SIG** list archive (UDB discussion threads)  
6. **Do not** claim Spring metrics as your work; cite them as baseline to improve  

---

## 10. Smart questions for mentors (Part II)

1. Which Spring artifacts are **canonical handoff** (which PR branch / Drive folder)?  
2. Primary Fall KPI: adjusted recall? WARL-class recall? reduction of false “new” params?  
3. Priority: merge `param_extraction/` tooling, or merge **reviewed UDB YAML**, or **isa-manual param tags** upstream?  
4. Access to gold (a)(b) — timeline after acceptance?  
5. Multi-model required or Claude-class sufficient if metrics clear?  
6. Relationship to Parameter SIG deliverables outside UDB?  

---

## 11. CFI / DFI (pointer only)

Separate LFX projects on `bsc-loca/sargantana`. Not expanded here; see `SARGANTANA-ANALYSIS.md`.

---

## 12. Source index (for re-verification)

| Source | Use |
|--------|-----|
| LFX project API | Official 5 goals |
| UDB issues #1747–#1754, #1765–#1766, #1783, #1791–#1793, #1831–#1832 | Spring design + metrics |
| UDB PRs ishaan-arora-1, ankit-cybertron | Code existence, merge status |
| `spec/std/isa/param/`, `param_schema.json` | Live data model |
| lists.riscv.org/g/sig-parameters | SIG activity |
| AGENTS.md + `.agents/skills/extract-instructions-from-subsection` | Agent culture in UDB |

---

## 13. Bottom line

**Part II is a continuation of a real, documented Spring LFX pipeline** with published V1/V2 metrics (~60%→~73% adjusted recall), open unmerged PRs, dual mentee tracks, Parameter SIG context, and a clear missing step: **robust, reviewable, UDB-schema-valid delivery that maintainers will merge.**

Any pre-work or application essay that shows you **read #1765–#1832 and understand the metric gap** will outclass generic “I like LLMs + RISC-V” applicants.
