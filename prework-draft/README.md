# LFX Pre-work: AI-assisted architectural parameter extraction (Part II)

**Status:** DRAFT — fill and publish to a **public** GitHub repo before applying.  
**LFX project:** [AI-assisted extraction of architectural parameters from RISC-V specifications – Part II](https://mentorship.lfx.linuxfoundation.org/project/22296947-cecb-4a8f-8bcb-4f34710e9f66)  
**Target codebase:** [riscv/riscv-unified-db](https://github.com/riscv/riscv-unified-db)  
**Applicant:** [YOUR NAME]  
**Date:** [YYYY-MM-DD]

---

## 1. What I understand this mentorship must deliver

*(Rewrite in your own words after reading the LFX page. Draft below — edit heavily.)*

This is **Part II** of work that started in Spring 2026 and continued under the Parameter SIG. The goal is **higher-quality, more robust** extraction of **architectural parameters** from the RISC-V ISA manuals (privileged + unprivileged), not a greenfield chatbot demo.

Concrete goals I read from the project description:

1. Keep using LLMs to find architectural parameters in the specs, using training examples from:
   - ISA Manual per-chapter parameters (YAML)
   - “keyword_matches” spreadsheet material
   - Existing **UDB YAML** parameter data (improve recall)
2. Extend the **classification scheme** for parameters where needed
3. Build **reproducible AI coding agents / skills** (prompt + context management)
4. Explore integrating ISA-Manual-based tools so parameters can be exported as **UDB YAML**
5. Land a **GitHub PR** of reviewed parameter files and work with maintainers toward merge

**Success for me if selected:** reviewable, mergeable artifacts in the appropriate RISC-V / UDB repos by end of term (Sep–Nov 2026), with reproducible runs documented.

---

## 2. What I explored in `riscv-unified-db`

| Item | Notes |
|---|---|
| Clone | `git clone https://github.com/riscv/riscv-unified-db.git` |
| Purpose | Machine-readable RISC-V database: extensions, instructions, CSRs, prose + generators |
| Key dirs | `spec/` (data), `spec/schemas/`, `backends/`, `cfgs/`, `tools/ruby-gems/`, `bin/` |
| Setup | `bin/setup` via [mise](https://mise.jdx.dev) (Ruby/Python/Node, etc.) |
| Docs | https://riscv.github.io/riscv-unified-db/docs-preview/ |
| Contributing | Issues + PRs; tests via `./bin/regress --all`; Code Owners; maintainers include Derek Hower, Paul Clarke |
| Mentors (LFX) | Allen Baum (Architecture Test / specs culture), Ajit Dingankar (UDB + AI for validation background) |

### My exploration log

- [ ] Read LFX project page end-to-end  
- [ ] Cloned UDB  
- [ ] Read README.adoc + CONTRIBUTING.adoc  
- [ ] Browsed `spec/std` structure (what I noticed: …)  
- [ ] Opened docs-preview (what I learned: …)  
- [ ] Tried `bin/setup` → result: **success / partial / blocked** (details: …)

---

## 3. Skills I have / will learn in week 1

| Have | Learning |
|---|---|
| Git, Linux basics | UDB data model / YAML schemas |
| Python | mise + Ruby tooling as needed |
| [LLM APIs / prompting — honest level] | Reproducible agent workflows, parameter classification |
| Academic research writing (UM) | RISC-V privileged/unprivileged spec navigation |

---

## 4. Four-week plan if selected (sketch)

| Week | Focus |
|---|---|
| 1 | Onboarding, UDB setup solid, reproduce prior Part I / Parameter SIG materials, agree metrics with mentors |
| 2 | Parameter extraction experiments; compare recall vs gold lists; log failures systematically |
| 3 | Harden classification + reproducible agent/skills; draft UDB YAML export path |
| 4 | Clean parameter files, PR, address review, document how to re-run |

*(Will adjust with mentor milestones.)*

---

## 5. Questions for mentors

1. Which gold-standard parameter lists should I treat as ground truth first (ISA Manual YAML vs spreadsheet vs UDB)?  
2. Preferred stack for the agent loop (specific models/tools, offline constraints)?  
3. Where should final reviewed YAML live for the PR (exact path/repo convention)?

---

## 6. Availability

I can commit approximately **25–30 hours/week** from mid-September through mid-November 2026 (LFX Fall term), with clear communication if university deadlines conflict.

---

## Links

- LFX project: https://mentorship.lfx.linuxfoundation.org/project/22296947-cecb-4a8f-8bcb-4f34710e9f66  
- UDB: https://github.com/riscv/riscv-unified-db  
- This pre-work repo: [add after publish]
