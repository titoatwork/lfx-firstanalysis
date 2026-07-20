# LFX Fall 2026 — Project Cards (Live)

**Verified:** 2026-07-18 via `api.mentorship.lfx.linuxfoundation.org` + riscv.org mentorship page + GitHub  
**Re-check before apply:** LFX UI “Accepting Applications” + deadlines

---

## Seats / pay (RVI policy — important)

From [riscv.org/community/mentorship](https://riscv.org/community/mentorship/):

> **The first selected mentee will receive a stipend** from the sponsoring organization based on project criteria.  
> **Additional mentees may be offered** the opportunity to participate **for experience but no stipend**.

| Interpretation | Default assumption |
|---|---|
| **Paid seats per project** | **~1** (first selected) |
| **Unpaid extra seats** | Optional; **not guaranteed** |
| **How to compete** | Fight for the **paid** slot |
| **LFX API field for seat count** | **None published** — policy is RVI-side, not a number on the card |

Stipend (general LFX, if eligible paid track): PPP from **~$1,000 min to ~$6,600 max**, base **$6,000** before PPP (see [LFX mentee stipends](https://docs.linuxfoundation.org/lfx/mentorship/mentee-stipends)). Paid in installments after satisfactory evaluations.

---

## Timeline (Fall 2026)

| Milestone | Date |
|---|---|
| Mentorships available on LFX | ~**14 July 2026** (RVI) |
| Applications open | **15 July – 5 August 2026** |
| Review / decisions / paperwork | ~**6–22 August 2026** (RVI) |
| Decline notifications | ~**8 September 2026** (RVI) |
| **API program term** (all 3 projects) | **15 Sep 2026 → 15 Nov 2026** |
| RVI marketing window | Sep 1 – Nov 30 (use **mentor/LFX term** as authority for work) |
| Hours expectation (RVI) | ~**30 h/week** for 3 months |

**You may apply to max 3 mentorships per term** (LFX rule).

---

## 1. PRIMARY — AI params Part II

| Field | Value |
|---|---|
| **Name** | AI-assisted extraction of architectural parameters from RISC-V specifications – **Part II** |
| **Project ID** | `22296947-cecb-4a8f-8bcb-4f34710e9f66` |
| **LFX URL** | https://mentorship.lfx.linuxfoundation.org/project/22296947-cecb-4a8f-8bcb-4f34710e9f66 |
| **Org** | RISC-V International |
| **acceptApplications** (API 2026-07-18) | **true** |
| **Repo** | https://github.com/riscv/riscv-unified-db |
| **Skills (API)** | Generative AI, ISA specifications, Parameterized modeling |
| **Mentors** | **Allen Baum**, **Ajit Dingankar** |

### Mentor notes (from LFX bios)

- **Allen Baum** — 10+ years RISC-V; Architecture Test SIG (chair/vice/participant); ISA Infrastructure; test format spec.
- **Ajit Dingankar** — ~1 year RISC-V + contributor to `riscv-unified-db`; ~30y Intel-era architecture/modeling; **AI for validation/verification**, formal analysis, HLS.

### Official goals (from LFX description, paraphrased cleanly)

Continues Spring 2026 RVI mentorship + Parameter SIG work. Fall focuses on **quality + robustness**:

1. **Keep extracting architectural parameters with LLMs** from privileged + unprivileged specs; use training examples from:
   - ISA Manual per-chapter params (YAML)
   - Google Drive “keyword_matches” spreadsheet
   - UDB YAML (improve parameter recall)
2. **Extend classification scheme** for parameters as needed  
3. **AI coding agents / skills** for reproducible runs and reusable workflows (prompt + context management)  
4. **Explore integration** so ISA Manual-based flow can export params in **UDB YAML**  
5. **GitHub PR** of final reviewed parameter files + work with maintainers to merge  

### Repo facts (UDB, 2026-07-18)

| | |
|---|---|
| Full name | `riscv/riscv-unified-db` |
| Stars | ~**193** |
| Language | **Ruby** (monorepo; also Python/JS tooling via mise) |
| Open issues | ~**330** |
| Last push | **2026-07-18** (very active) |
| Purpose | Machine-readable RISC-V spec database + artifact generators |
| Key dirs | `spec/`, `backends/`, `cfgs/`, `doc/`, `tools/ruby-gems/` |
| Docs preview | https://riscv.github.io/riscv-unified-db/docs-preview/ |
| Setup | **mise** native; Docker optional for some C++ ISS builds |
| Note | Rapid development; schemas/APIs change; some data WIP |

### Why this is PRIMARY for Ibteshamul

- Pre-work possible in **72h without SystemVerilog**  
- Skills map: Python / LLM APIs / YAML / Git / reading specs  
- Clear Part I → Part II story  
- Still RISC-V / systems-adjacent for resume spine  
- Higher cold-start acceptance odds vs Sargantana RTL scramble  

### Pre-work target (for 72h)

Suggested public repo: `lfx-riscv-param-extraction-prework`

```text
README.md          — project link, goals in own words, plan
notes/udb-overview.md
notes/part-ii-goals.md
examples/          — optional tiny extraction sketch / sample YAML
```

Must show: cloned UDB, read CONTRIBUTING/docs, ran or attempted setup, understood Part II deliverables, 4-week plan, 2–3 smart mentor questions.

---

## 2. BACKUP — CFI on Sargantana

| Field | Value |
|---|---|
| **Name** | Implementation of the RISC-V ISA Extensions for **Control-Flow Integrity** |
| **Project ID** | `846490b5-2092-4645-895a-83c147ba5b68` |
| **LFX URL** | https://mentorship.lfx.linuxfoundation.org/project/846490b5-2092-4645-895a-83c147ba5b68 |
| **acceptApplications** | **true** |
| **Repo** | https://github.com/bsc-loca/sargantana |
| **Skills** | SystemVerilog, Computer Architecture, Linux |
| **Mentors** | **Rubén Salvador**, **Emanuele Parisi** |
| **Collaboration** | **BSC** + **SUSHI** (Inria Rennes / CentraleSupélec) |

### What the mentee does (from description)

1. Study **RISC-V CFI** (shadow stack + landing pads) + **Sargantana** microarch  
2. Produce **architectural plan** of pipeline modifications  
3. Implement **shadow stack** (HW enforcement + access protection)  
4. Implement **landing pads** (validate indirect branch targets, commit-time checks)  
5. Use Sargantana **emulation** for functional correctness + HW overhead study  

### Related public signals (GitHub, mid-July 2026)

- CFI-specific pre-issues filed by applicants (e.g. Zicfilp `auipc x0`, envcfg LPE/SSE bits)  
- Maintainer **@narcisrodas**: CFI enablement **not yet planned to integrate** on public tree until mentorship implementation  
- See **SARGANTANA-ANALYSIS.md** for full competition/workflow  

**Only apply if willing to commit to RTL ramp.**

---

## 3. BACKUP — DFI on Sargantana

| Field | Value |
|---|---|
| **Name** | Implementation of Tightly-Coupled **Data-Flow Integrity** in RISC-V |
| **Project ID** | `dc34ec1a-f0d7-4be4-aa8d-0583e4bf537e` |
| **LFX URL** | https://mentorship.lfx.linuxfoundation.org/project/dc34ec1a-f0d7-4be4-aa8d-0583e4bf537e |
| **acceptApplications** | **true** |
| **Repo** | https://github.com/bsc-loca/sargantana |
| **Skills** | SystemVerilog/RTL, computer architecture, Linux/Git/Make/bash, **LLVM**, **C/C++**, static analysis |
| **Mentors** | **Rubén Salvador**, **Emanuele Parisi** (same pair as CFI) |

### Phases (from description)

| Phase | Focus |
|---|---|
| **1 — Hardware** | Port/optimize preliminary RTL (from SUSHI CVA-6 work) onto **Sargantana** |
| **2 — Software (stretch)** | PoC toolchain; baseline **RVDFI**; SUSHI LLVM guidance for foundational compiler backend |

**Most systems-adjacent of the three open RVI projects**, but **harder cold-start** than AI Part II.

---

## 4. SKIP (default) — Women in Energy (unpaid)

| | |
|---|---|
| Org | LF Energy |
| Status | Unpaid; long window; Spring 2027 card may appear |
| Role | **Skip** unless strategy changes |

---

## Project choice matrix (locked)

| Project | Pros | Cons | Role |
|---|---|---|---|
| **AI Part II** | 72h pre-work w/o RTL; clear Part II; RVI; UDB active | “AI” keyword → more apps; less pure HPC | **PRIMARY** |
| **DFI** | Full-stack HW+LLVM; systems prestige | SV + cold start; Sargantana applicant wave | Backup if RTL committed |
| **CFI** | Clear HW CFI scope; same mentors/lab | Pure HW security; CFI not in public tree yet | Backup #2 if RTL |
| **Unpaid Energy** | Long window | Unpaid; off-theme | Skip |

---

## API noise warning

LFX API often shows stale `acceptApplications: true` ghosts (old Meshery/Jaeger/Electron terms, etc.).  
**Trust:** UI “Accepting Applications” + **Fall 2026** term + RVI careers/jobs list.

---

## Direct links (bookmark)

| What | URL |
|---|---|
| LFX home | https://mentorship.lfx.linuxfoundation.org |
| AI Part II | https://mentorship.lfx.linuxfoundation.org/project/22296947-cecb-4a8f-8bcb-4f34710e9f66 |
| CFI | https://mentorship.lfx.linuxfoundation.org/project/846490b5-2092-4645-895a-83c147ba5b68 |
| DFI | https://mentorship.lfx.linuxfoundation.org/project/dc34ec1a-f0d7-4be4-aa8d-0583e4bf537e |
| UDB | https://github.com/riscv/riscv-unified-db |
| Sargantana | https://github.com/bsc-loca/sargantana |
| core_tile (sim) | https://github.com/bsc-loca/core_tile |
| RVI mentorship | https://riscv.org/community/mentorship/ |
| RVI jobs | https://riscv.org/community/jobs/ |
| Apply how-to | https://docs.linuxfoundation.org/lfx/mentorship/mentees/apply-to-a-project |
| Stipends | https://docs.linuxfoundation.org/lfx/mentorship/mentee-stipends |
