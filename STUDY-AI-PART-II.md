# Study notes — AI params Part II (primary LFX)

**Project:** AI-assisted extraction of architectural parameters from RISC-V specifications – Part II  
**LFX:** https://mentorship.lfx.linuxfoundation.org/project/22296947-cecb-4a8f-8bcb-4f34710e9f66  
**Repo:** https://github.com/riscv/riscv-unified-db  
**Mentors:** Allen Baum, Ajit Dingankar  
**Term:** ~15 Sep – 15 Nov 2026 · **≥30 h/week** · apps through **5 Aug 2026**

---

## 1. One-sentence mission

Take the **RISC-V ISA manuals** (unprivileged + privileged), use **LLMs + tooling** to find **architectural parameters**, classify them, measure **recall/quality** against gold lists, make the pipeline **reproducible**, and land **reviewed parameter files** (ideally **UDB YAML**) via **GitHub PR**.

This is **Part II**: Spring 2026 + Parameter SIG already started; Fall is **quality + robustness**, not inventing the idea from zero.

---

## 2. Official deliverables (the five numbered goals)

| # | Deliverable | In plain English |
|---|-------------|------------------|
| **1** | Extract params with LLMs from priv + unpriv specs | Read specs → find implementation-defined knobs (widths, options, modes…) |
| **1a–c** | Train/eval against three gold sources | (a) per-chapter YAML from ISA Manual work (b) keyword_matches spreadsheet (c) existing UDB params — **recreate full lists**, improve **recall** |
| **2** | Extend **classification scheme** | Types/categories of parameters; when scheme is incomplete, improve it |
| **3** | **AI coding agents + skills** | Reusable, reproducible workflows (prompt/context management), not one-off ChatGPT sessions |
| **4** | Export to **UDB YAML** | Bridge ISA-Manual extraction → `spec/std/isa/param/*.yaml` style |
| **5** | **GitHub PR** + maintainer follow-up | Reviewed parameter files merged into the right repo |

**Definition of done for the term:** better extraction quality, robust runnable workflow, classification updates if needed, UDB-shaped outputs, PR in flight/merged.

---

## 3. What is an “architectural parameter”?

Not an instruction mnemonic. A **parameter** is a **configurable property** of a RISC-V implementation implied by the specs, e.g.:

- How many **ASID** bits are implemented? (`ASID_WIDTH`)
- Cache block size? (`CACHE_BLOCK_SIZE`)
- Which HPM counters exist? (`HPM_COUNTER_EN`, `HPM_EVENTS`)
- Vector `ELEN`? Mode options for traps? Endianness options?

In UDB today there are **~228** standard param files under:

```text
spec/std/isa/param/<NAME>.yaml
```

### Example (real file shape)

`ASID_WIDTH.yaml` (simplified idea):

```yaml
$schema: param_schema.json#
kind: parameter
name: ASID_WIDTH
description: Number of implemented ASID bits...
long_name: ...
schema:
  type: integer
  minimum: 0
  maximum: 16
definedBy:
  extension:
    name: S
requirements:
  idl(): |
    MXLEN == 32 -> ASID_WIDTH <= 9;
```

Schema requires roughly: `$schema`, `kind`, `description`, `long_name`, `definedBy`, `schema` (JSON-schema for allowed values).

**Your job in spirit:** discover more params from prose, fill/align fields, avoid junk (false positives), measure how many gold params you recover (**recall**).

---

## 4. Three “gold” sources (evaluation anchors)

| Source | Role |
|--------|------|
| **(a) ISA Manual per-chapter YAML** | Human/manual param lists tied to chapters |
| **(b) Google Drive keyword_matches spreadsheet** | Keyword → match lists (mentor/SIG-held; you’ll get access if selected) |
| **(c) UDB YAML** (`spec/std/isa/param/`) | Live open gold (~228 params); enhance **parameter recall** against this |

Part II = use subsets as **training/examples**, try to **recreate full lists**, improve quality vs Spring.

---

## 5. Mentors (what they optimize for)

| Mentor | Background | Implies for you |
|--------|------------|-----------------|
| **Allen Baum** | 10+ years RISC-V; Architecture Test / certification culture; specs review | Correctness, spec fidelity, testable/clear definitions |
| **Ajit Dingankar** | UDB contributor; Intel/IBM arch + **AI for V&V** | Modeling, validation mindset, AI that is useful not flashy |

They will not be impressed by “I used GPT-4.” They will be impressed by **metrics, logs, reproducible commands, clean YAML, honest misses**.

---

## 6. Repo map (`riscv-unified-db`)

| Path | Why it matters |
|------|----------------|
| `spec/std/isa/param/` | **Target shape** of parameters (~228 YAML) |
| `spec/schemas/param_schema.json` | Validation rules for params |
| `spec/std/isa/` | Extensions, instructions, CSRs (context for `definedBy`) |
| `ext/` | Submodules incl. **riscv-isa-manual** (AsciiDoc sources of the specs) |
| `backends/` | Generators (docs, sim, etc.) — less Day-1 for mentee |
| `bin/setup`, `bin/doctor` | Environment |
| `./bin/regress`, `./do test:schema` | Don’t break the repo |
| `AGENTS.md` | How gen-AI agents should work in this repo |
| `.agents/skills/...` | Example **skill**: extract instructions from AsciiDoc subsection → YAML |

### Already exists: agent skill pattern

`.agents/skills/extract-instructions-from-subsection/SKILL.md`  
→ recipe to extract **instruction names** from ISA manual AsciiDoc into YAML.  

Part II wants **similar discipline for parameters**: skills/agents, reproducible, not ad-hoc chat.

---

## 7. Mental model of the pipeline (what you’ll build/improve)

```text
  RISC-V ISA Manual (AsciiDoc / PDF prose)
           │
           ▼
  Chunk + context management (which chapter/section?)
           │
           ▼
  LLM extraction (candidate parameters + metadata)
           │
           ▼
  Classification (type / category scheme)
           │
           ▼
  Normalize → UDB-like YAML (name, description, schema, definedBy, …)
           │
           ▼
  Score vs gold (a/b/c): precision, recall, false positives
           │
           ▼
  Human review → PR into appropriate repo
```

**Robustness** = same inputs → same outputs; logged prompts; versioned configs; failures recorded.

---

## 8. How this maps to you (COLIDE → this mentorship)

| COLIDE habit | Part II use |
|--------------|-------------|
| LLM as **pipeline stage** (measured, not chat-only) | Agents/skills + overhead/quality metrics |
| Multi-session **evaluation** vs baselines | Recall/precision vs gold lists |
| Structured artifacts + honest limits | YAML + docs + PR |
| Mentor-facing finish | Baum/Dingankar + UDB maintainers |
| Python + research discipline | Day-to-day mentee stack |

You do **not** need CUDA here. You need **spec literacy + extraction eval + software hygiene**.

---

## 9. Stack you’ll actually touch

| Layer | Tools (likely) |
|-------|----------------|
| Specs | `ext/riscv-isa-manual` AsciiDoc; priv/unpriv manuals |
| Data | YAML, JSON Schema |
| UDB | Ruby/mise ecosystem for repo; Python often for AI glue |
| AI | LLM APIs or local models; prompt/context mgmt; agent skills |
| Eng | Git, PRs, logging, maybe small eval harness |

---

## 10. Study path (no resume required)

**Session A — concepts (1–2 h)**  
Re-read this file + LFX description until you can explain the 5 goals without notes.

**Session B — UDB params (1–2 h)**  
```bash
git clone https://github.com/riscv/riscv-unified-db.git
# open several files under spec/std/isa/param/
# open spec/schemas/param_schema.json
```
Write 10 lines: “A parameter is … Fields are …”

**Session C — ISA manual source (1 h)**  
Browse `ext/` / docs; open one chapter of unpriv or priv prose; list 3 sentences that *sound* like implementation-defined parameters.

**Session D — agents (30 min)**  
Read `AGENTS.md` + `.agents/skills/extract-instructions-from-subsection/SKILL.md`.  
Note: same pattern could exist for **parameters**.

**Session E (optional)**  
`bin/setup` if machine allows; run `bin/doctor` or smoke tests; log success/fail for pre-work later.

---

## 11. Questions smart mentees ask mentors (save for interview/app)

1. Which gold list is the **primary** scoreboard for Fall (UDB vs chapter YAML vs spreadsheet)?  
2. Where should Spring 2026 / Parameter SIG **code and prompts** live for handoff?  
3. Preferred model stack (API vs local) and **license/data** constraints?  
4. Target PR repo/path for reviewed params (`spec/std/isa/param/` vs separate staging)?  
5. Definition of “good enough” recall/precision for graduation?

---

## 12. CFI / DFI (backups only — one paragraph each)

**CFI:** Implement RISC-V **control-flow integrity** (shadow stack + landing pads) on **Sargantana** (SystemVerilog): study specs + microarch → plan → RTL → emulate → overhead. Mentors: Rubén Salvador, Emanuele Parisi. Repo: `bsc-loca/sargantana` (+ `core_tile` for sim).  

**DFI:** Tightly coupled **data-flow integrity** on Sargantana: Phase 1 HW (port from SUSHI/CVA-6 prelim), Phase 2 PoC toolchain/LLVM. Same mentors. Harder cold-start (RTL + compilers).

Primary study now = **this file + UDB**. CFI/DFI only if you open a second application later.

---

## 13. Resume status

Paused on purpose. Return when ready. Understanding first is correct for this block of the 72h.
