# Fall 2026 official goals → execution checklist

**Source:** LFX project description (AI-assisted extraction of architectural parameters – Part II), verified accepting as of pre-work pack build.  
**Mentors:** Allen Baum, Ajit Dingankar  
**Repo listed:** https://github.com/riscv/riscv-unified-db

---

## Framing paragraph (official)

> Extends effort already underway… Spring 2026 RVI Mentorship… continued under Parameter SIG… results improved steadily… need further improvement in **quality** and **implementation robustness**.

| Phrase | Operational meaning |
|--------|---------------------|
| Already underway | Do not restart from zero; inherit Spring + SIG |
| Quality | Metrics, fewer hallucinations, better hard classes |
| Implementation robustness | Re-runnable, versioned, mergeable, less brittle |

---

## Goal 1 — Continue LLM extraction (priv + unpriv)

**Official:** Find architectural parameters with LLMs in privileged and unprivileged specs; use subsets of manually created lists as training examples; **try to recreate the full lists** from:

| ID | Gold source | Status for applicant pre-selection |
|----|-------------|--------------------------------------|
| **1a** | ISA Manual per-chapter params (YAML) | Likely mentor/SIG materials |
| **1b** | Google Drive `keyword_matches` spreadsheet | Likely post-accept access |
| **1c** | UDB YAML | **Public now:** `spec/std/isa/param/*.yaml` |

### Deliverables I associate with Goal 1

- [ ] Extraction runs over full agreed corpus (unpriv + priv AsciiDoc)  
- [ ] Train/few-shot from **subsets**; eval on **held-out full gold**  
- [ ] Metrics: precision, recall (raw + adjusted), per-class recall  
- [ ] Error taxonomy: hallucination, UDB gap, recall miss, naming mismatch, class disagreement  
- [ ] Comparison table vs Spring V2 baseline (~72.9% adjusted recall; WARL ~50%)  

### Done when

Mentors can re-run (or read logs of) an evaluation that **beats or clearly diagnoses** Spring V2 on agreed gold, with honest failure cases.

---

## Goal 2 — Extend classification scheme

**Official:** Extend current classification as needed.

### Current scheme (Spring public taxonomy)

| Class | Definition (compressed) |
|-------|-------------------------|
| `NORM_DIRECT` | Impl must choose; not CSR WARL value-set |
| `NORM_CSR_WARL` | Legal values of a WARL CSR field |
| `NORM_CSR_RW` | RO vs RW / mutability of CSR/field |
| `SW_RULE` | Appears free; SW-deterministic if rules followed |
| `NON_ISA` | Platform-level |
| `NON_NORM` | NOTE/TIP/WARNING only |
| `DOC_RULE` | Documentation/reporting, not arch behavior |
| `UNKNOWN` | Needs human |

### Deliverables

- [ ] Written taxonomy doc (diff vs Spring)  
- [ ] Updated few-shot set for weak classes (esp. WARL)  
- [ ] Evidence: class accuracy / confusion matrix before vs after  

### Done when

Classification changes are **justified by errors**, not taxonomy cosplay.

---

## Goal 3 — AI coding agents and skills (reproducible)

**Official:** Develop AI coding agents and skills for reproducible runs and reusable workflows; extend prompt and context management in the current flow.

### Deliverables

- [ ] Versioned prompts (`v1`/`v2`/… ) with changelog  
- [ ] Chunk/context policy documented (CSR atomicity, overlap rules)  
- [ ] One-command or skill-style entrypoint (`run extract`, `run eval`)  
- [ ] Logs: model, git SHA, prompt hash, token usage, temperature  
- [ ] Alignment with UDB agent culture (`AGENTS.md`, `.agents/skills/` patterns)  

### Done when

A third person (or mentor) can re-run without private tribal knowledge.

---

## Goal 4 — Export to UDB YAML

**Official:** Explore integration of ISA Manual–based tools (1.a flow) to export parameters in **UDB yaml format**.

### Target shape

```yaml
$schema: param_schema.json#
kind: parameter
name: EXAMPLE
long_name: ...
description: ...
definedBy: ...
schema: { type: ... }
# optional requirements: idl() / if-then
```

Validate against `spec/schemas/param_schema.json`.

### Deliverables

- [ ] Mapper: reviewed row → draft `param/*.yaml`  
- [ ] Schema validation in CI or script  
- [ ] Sample export set (high-confidence, human-reviewed only)  

### Done when

At least a **reviewed subset** is schema-valid and ready for PR—not only `parameters.csv`.

---

## Goal 5 — GitHub PR + merge follow-up

**Official:** Create a GitHub PR to publish final **reviewed** parameter files; follow up with maintainers on merging.

### Deliverables

- [ ] Small, reviewable PR(s) (tooling and/or data)  
- [ ] Clear PR description: gold, metrics, review process  
- [ ] Maintainer feedback loop until merge or explicit next step  

### Done when

Merge (or maintainer-accepted path into next release)—not “PR opened for optics.”

---

## Dependency graph

```text
Goal 1 (extract+eval) ──┬──► Goal 2 (taxonomy) 
                        │
                        ├──► Goal 3 (agents/skills)
                        │
                        └──► Goal 4 (UDB YAML export) ──► Goal 5 (PR+merge)
```

Goals 2–3 feed quality of 1; 4–5 are the **shipping** end of Fall.

---

## Out of scope (unless mentors expand)

- Full formal verification of all constraints  
- Replacing Parameter SIG governance  
- Unrelated UDB backend generators  
- Claiming unaudited “hundreds of new params” as truth  
