# Spring 2026 baseline (public UDB trail)

**Purpose:** Accurate handoff map for Part II applicants.  
**Attribution:** Designs, metrics, and PR text from public `riscv/riscv-unified-db` issues/PRs. Primary phased track: **@ishaan-arora-1**. Parallel track: **@ankit-cybertron**.  
**Research date for this pack:** 2026-07-19. Re-verify PR merge state before apply.

---

## 1. Why this baseline matters

Fall description says results “improved steadily” but need **quality** and **implementation robustness**.  
Spring public numbers and open PRs **are** that baseline. Part II success = improve and **land**, not re-discover the problem.

---

## 2. Phased track A — ishaan-arora-1

| Phase | Issue | PR | Core output |
|------:|-------|-----|-------------|
| 1 Ground truth | #1747 | **#1765** | Catalog UDB params → JSON/CSV; map to `.adoc` |
| 2 Taxonomy + prompts | #1748 | **#1766** | `taxonomy.md`, system prompt, few-shots, `run_prompt.py` |
| 3 Chunking | #1749 | **#1783** | AsciiDoc-aware chunks; CSR sections atomic |
| 4 Extract | #1750 | **#1791** | `extract.py`; full Claude run |
| 5 Analyze | #1751 | **#1792** | `analyze.py`; metrics; discrepancies |
| 6 Refine | #1752 | **#1793** | Prompt v2; large metric gains |
| 7 Spreadsheet | #1753 | **#1831** | Final parameter spreadsheet |
| 8 Spec tags | #1754 | **#1832** | `[#param:NAME]` into isa-manual |

**As of 2026-07-19 research:** these LFX phase PRs were still **open** (not merged to `main`).  
**Implication:** `param_extraction/` path may exist only on PR branches—not on a clean `main` clone.

---

## 3. Phase 1 — ground truth (numbers from PR #1765 text)

| Metric | Value |
|--------|------:|
| UDB parameters cataloged (non-MOCK) | **185** |
| MOCK fixtures excluded | 22 |
| NORM_DIRECT | 102 (55%) |
| NORM_CSR_RW | 55 (30%) |
| NORM_CSR_WARL | 26 (14%) |
| SW_RULE | 2 (1%) |
| High-confidence classifications | 150 (81%) |
| Value type binary | 111 (60%) |
| Params with CSR cross-refs | 94 (51%) |
| Mapped to some spec text | 183/185 (98%) |
| Spec corpus | 74 `.adoc` files, 52,602 lines |

Scripts described: `export_udb_params.py`, `map_params_to_spec.py`, `generate_report.py`.

**Note:** On `main` mid-2026, file count under `spec/std/isa/param/` was **~228** YAML files—catalog grew after Spring counts. Always pin gold by **git SHA**.

---

## 4. Phase 2 — taxonomy & prompts (#1766)

### Classes (formalized)

- `NORM_DIRECT` — e.g. `NUM_PMP_ENTRIES`, `PHYS_ADDR_WIDTH`, `MXLEN`  
- `NORM_CSR_WARL` — e.g. `MTVEC_MODES`, legal FS sets  
- `NORM_CSR_RW` — e.g. mutability / access  
- `SW_RULE` — e.g. dirty-bit update rules  
- `NON_ISA`, `NON_NORM`, `DOC_RULE`, `UNKNOWN`

### Prompt architecture

1. System (~800 tokens): role, task, taxonomy, JSON schema, rules  
2. Few-shots (~2–3k tokens): positive + negative examples  
3. User: optional UDB name list + **one chunk**

Design choices: single-pass extract+classify; mandatory `reasoning`; `skipped_non_parameters`; section-boundary chunking.

---

## 5. Phase 3 — chunking (#1783)

| Metric | Value |
|--------|------:|
| Total chunks | **78** |
| CSR section splits | **0** |
| Target size | ~2,500–3,500 lines |
| Overlap | 30 lines |
| Multi-chunk files | `machine.adoc`, `scalar-crypto.adoc`, `v-st-ext.adoc`, `vector-crypto.adoc` |

**Rule:** Never split mid-CSR `====` section.  
**Pilot density:** `machine.adoc` called out as highest parameter density.

---

## 6. Phase 4 — extract (#1791)

- `extract.py`: pilot / run / merge / status  
- Rate limiting, retries, skip list for boilerplate adoc  
- V1 results: Claude across chunks; example cost cited ~**$3.60** full run  
- Output per hit: excerpt, line_number, parameter_name, existing_udb_name, class, value_type, confidence, reasoning  
- Overlap fix: do not re-extract params whose defining sentence lives only in overlap region  

Models recommended in phase issues: Claude, GPT-4o, Gemini (multi-model for robustness).

---

## 7. Phase 5–6 — metrics (#1792, #1793)

### Alignment strategies

- Exact name  
- Fuzzy / stem / prefix  
- **Curated one-to-many groups** (one spec sentence → many UDB names)  
- Concept groups  

### Discrepancy types

| Type | Meaning |
|------|---------|
| LLM hallucination | FP — not a real param |
| UDB gap | True new param candidate |
| UDB recall miss | FN — gold missed |
| Classification disagreement | Found, wrong class |
| Naming mismatch | Same idea, different name |

### V1 vs V2 (from PR writeups)

| Metric | V1 | V2 | Δ |
|--------|----|----|---|
| Deduped unique | 215 | **346** | +61% |
| Raw recall | 60.0% | **69.7%** | +9.7 pp |
| Adjusted recall | 62.7% | **72.9%** | +10.2 pp |
| Class accuracy | 67.9% | **88.4%** | +20.5 pp |
| New discoveries | 153 | **256** | review burden |
| NORM_DIRECT recall | 47% | **83%** | |
| NORM_CSR_RW recall | 41% | **63%** | |
| NORM_CSR_WARL recall | 25% | **50%** | **still weak** |

Phase 5 acceptance mentioned recall ≥70% for at least one model—V2 **adjusted** clears; raw ~70%; WARL class does not.

V2 prompt adds: class disambiguation; “commonly missed patterns” (HPM/counters, VM modes, tval reporting, alignment, impl values, LR/SC failure, stateen, …).

---

## 8. Phase 7–8 — spreadsheet & tags (#1831, #1832)

| Item | Value |
|------|------:|
| Spreadsheet rows (conf ≥ medium) | **330** |
| Already in UDB (named) | 97 |
| Newly discovered | **233** |
| Tags inserted | **321 / 330 (97.3%)** |
| Unmatched (manual) | 9 |
| Tag form | `[#param:NAME]#excerpt#` (and bare anchors inside norm tags) |

**Matcher lesson:** Do **not** trust LLM line numbers; fuzzy-match excerpts; strip existing AsciiDoc tags when matching.

---

## 9. Parallel track B — ankit-cybertron

| Item | Focus |
|------|--------|
| #1772 (closed PR) | Param knowledge base / schema recursion / CSR IDL cross-ref; rag vs analysis modes |
| #1790 (open) | Dual chunkers: AsciiDoc + UDB YAML → unified chunk schema |
| #1803 (open) | AsciiDoc classifier rules; reduced UNKNOWN rate; more non_CSR_parameter; less false promote |

Part II may need to **unify or choose** LLM-full-pipeline vs rules/RAG-assisted paths under mentor direction.

---

## 10. Organizational context — Parameter SIG

- List: `sig-parameters@lists.riscv.org`  
- Public themes: parameters include **legal values** and **encoding**; UDB is **a** destination, not only deliverable  
- Fall work should stay **mergeable and SIG-legible**, not a private notebook  

---

## 11. Failure modes (study these)

1. NOTE/informative text treated as normative params  
2. CSR runtime behavior mislabeled as architectural parameter  
3. One-to-many UDB expansion undercounted without alignment groups  
4. Naming mismatch → false low recall  
5. Chunk overlap double counts  
6. Line-number errors break tagging  
7. Inflated “new params” without human review  
8. CSV/spreadsheet ≠ `param_schema` YAML with `definedBy` + IDL  
9. Tooling never merges → robustness unproven  

---

## 12. What Part II should prioritize (synthesis)

| Priority | Why |
|----------|-----|
| WARL-class recall + precision | Largest structural gap |
| Reduce false discoveries among ~233 “new” | Quality |
| Pin gold by git SHA; multi-run eval | Robustness |
| Agent/skill packaging | Goal 3; UDB culture |
| Schema-valid UDB YAML export | Goal 4 |
| Small reviewed PRs that maintainers merge | Goal 5; Spring PR debt |

---

## 13. How to re-verify before apply week

```text
1. Open https://github.com/riscv/riscv-unified-db/pull/1765 … #1832 — still open?
2. Count param YAML on main: spec/std/isa/param/*.yaml
3. Search issues: LFX, parameter extraction
4. Check mentor/project description unchanged on LFX
```
