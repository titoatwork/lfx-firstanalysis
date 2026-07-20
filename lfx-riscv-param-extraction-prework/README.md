# Pre-work: AI-assisted extraction of architectural parameters (Part II)

**Applicant:** Ibteshamul Haque  
**LFX project:** [AI-assisted extraction of architectural parameters from RISC-V specifications – Part II](https://mentorship.lfx.linuxfoundation.org/project/22296947-cecb-4a8f-8bcb-4f34710e9f66)  
**Org:** RISC-V International · **Term:** Fall 2026 (API: 2026-09-15 → 2026-11-15)  
**Mentors:** Allen Baum, Ajit Dingankar  
**Primary codebase:** [riscv/riscv-unified-db](https://github.com/riscv/riscv-unified-db)  
**Status:** Pre-application study pack (public-ready). Deep personal study of PR branches continues offline.  
**Availability:** ≥ **30 hours/week** for the full term.

---

## 1. What I understand this mentorship must deliver

This is **Part II** of work started in **Spring 2026 RVI LFX** and continued under the **Parameter SIG**. Fall is not a greenfield chatbot demo. Official goals:

| # | Goal | My reading of “done” |
|---|------|----------------------|
| **1** | LLM extraction on **privileged + unprivileged** specs; train/eval against gold | Higher **quality** than Spring V2; recreate full lists from gold subsets |
| **1a** | ISA Manual per-chapter params (YAML) | Chapter-level gold as train/eval |
| **1b** | Google Drive `keyword_matches` spreadsheet | Second gold (access likely post-selection) |
| **1c** | **UDB YAML** params | Improve **parameter recall** vs `spec/std/isa/param/` |
| **2** | Extend **classification scheme** | Taxonomy updates only where evidence demands |
| **3** | **AI agents/skills**, reproducible workflows | Same inputs → logged, re-runnable pipeline (prompt + context mgmt) |
| **4** | Export Manual-side flow → **UDB YAML** | Schema-valid files under param_schema, not only CSV |
| **5** | **GitHub PR** + maintainer follow-up | **Reviewed** params/tooling **merged**, not PR tourism |

**Problem statement in one line:**  
Find implementation-defined architectural parameters in ISA prose, classify them, measure against gold, productize the pipeline, emit UDB-shaped YAML, land merges.

---

## 2. Spring baseline I am building on (public trail)

I am **not** claiming Spring work as mine. I studied the public phase issues/PRs on `riscv-unified-db` (primarily @ishaan-arora-1 phases; parallel track @ankit-cybertron).

### Pipeline (as documented on open PRs)

```text
UDB param YAML (gold, ~185 non-MOCK in Spring; ~228 files on main mid-2026)
 + riscv-isa-manual AsciiDoc
        → ground truth map + taxonomy + prompts
        → CSR-atomic AsciiDoc chunks
        → LLM extract (JSON: excerpt, class, confidence, reasoning)
        → dedupe + align to UDB
        → metrics (recall / precision / hallucinations / UDB gaps)
        → spreadsheet
        → optional [#param:NAME] tags in isa-manual
        → ⚠ still weak: schema-valid UDB YAML on main + merged tooling
```

### Metrics to beat (from Phase 5–6 PR writeups; Claude vs 185 UDB gold)

| Metric | V1 | V2 |
|--------|----|----|
| Adjusted recall | ~62.7% | **~72.9%** |
| Raw recall | ~60% | **~69.7%** |
| Classification accuracy | ~67.9% | **~88.4%** |
| NORM_DIRECT recall | ~47% | **~83%** |
| **NORM_CSR_WARL recall** | ~25% | **~50%** ← priority gap |
| “New” discoveries (need review) | ~153 | **~256** ← FP risk |

### Critical repo fact

`param_extraction/` and the phase deliverables appear on **open PRs**, not as a finished tree on default **`main`**. That matches Fall language: **quality + implementation robustness** and **merge**.

Details: [`notes/spring-baseline.md`](notes/spring-baseline.md)

---

## 3. What is an architectural parameter? (operational)

Not an instruction mnemonic. A **parameter** is a configurable property of a RISC-V implementation implied by the ISA (widths, legal value sets, mutability, options), with:

- A stable **name** (e.g. `PHYS_ADDR_WIDTH`, `NUM_PMP_ENTRIES`, `MTVEC_MODES`)
- **description** / **long_name**
- **definedBy** (extension / conditions)
- **schema** (JSON Schema for legal values: integer range, enum, array, …)
- optional **requirements** (IDL / conditional constraints)

Live location: `spec/std/isa/param/<NAME>.yaml`  
Schema: `spec/schemas/param_schema.json`

**Taxonomy (Spring):** `NORM_DIRECT`, `NORM_CSR_WARL`, `NORM_CSR_RW`, `SW_RULE`, plus `NON_ISA` / `NON_NORM` / `DOC_RULE` / `UNKNOWN`.

Worked examples: [`examples/`](examples/) · notes: [`notes/what-is-a-parameter.md`](notes/what-is-a-parameter.md)

---

## 4. Skills / evidence I bring (honest)

| Have | Transfer to Part II |
|------|---------------------|
| End-to-end research pipeline under faculty mentor (UM, Prof. Por Lip Yee) | Own multi-stage work to paper-facing state |
| Controlled use of LLMs as **pipeline stages** + measurement mindset | Agents/skills, not ad-hoc chat |
| Reproducible evaluation culture (multi-run honesty, baselines, limits) | Recall/precision vs gold |
| Python, Git, Linux, structured configs/YAML | Day-to-day mentee stack |
| Technical writing for coauthors/reviewers | PR descriptions, taxonomy docs |

**Learning in week 1:** UDB Ruby/mise workflow as needed; full Spring branch checkout; gold (a)(b) access with mentors; WARL-class error analysis.

**Not claiming:** SystemVerilog expertise; authorship of Spring UDB phases.

---

## 5. Four-week plan if selected (scaffold; mentor-adjusted)

| Week | Focus | Maps to goals |
|------|--------|----------------|
| **1** | Handoff: reproduce Spring eval on agreed branch; freeze gold versions; metric dashboard | 1, 3 |
| **2** | Quality: WARL + naming mismatch + false “new” params; taxonomy tweaks if justified | 1, 2 |
| **3** | Robustness: agents/skills, prompt versioning, CI-friendly re-run, context/chunk policy | 3 |
| **4** | Export schema-valid UDB YAML for a reviewed subset; open PR(s); maintainer loop | 4, 5 |

Stretch: multi-model comparison; Parameter SIG alignment; isa-manual tag hygiene only if mentors prioritize.

Full plan: [`notes/four-week-plan.md`](notes/four-week-plan.md)

---

## 6. Questions for mentors

See [`notes/questions-for-mentors.md`](notes/questions-for-mentors.md).

Top three:

1. Primary Fall KPI (adjusted recall? WARL-class? reduction of false discoveries? merge count?)  
2. Canonical Spring handoff branch / Drive gold (a)(b) access timeline  
3. Priority order: tooling on main vs reviewed `param/*.yaml` vs isa-manual tags  

---

## 7. Application materials (local)

| File | Purpose |
|------|---------|
| [`application/essay-part-ii.md`](application/essay-part-ii.md) | Project-specific application text |
| [`application/interview-cheatsheet.md`](application/interview-cheatsheet.md) | Call prep |
| [`application/profile-introduction.md`](application/profile-introduction.md) | Shared LFX profile intro (multi-project safe) |

---

## 8. How to verify this pack

```text
notes/fall-goals.md          — official 1–5 decoded
notes/spring-baseline.md     — phases, metrics, PR numbers
notes/what-is-a-parameter.md — UDB model + taxonomy
examples/*.md                — real param walkthroughs
```

---

## 9. License / intent

Study and application pre-work only. Spring metrics and designs attributed to public UDB issues/PRs and their authors. No confidential third-party code included.
