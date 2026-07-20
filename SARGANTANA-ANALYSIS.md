# Deep Analysis — `bsc-loca/sargantana`

**Repo:** https://github.com/bsc-loca/sargantana  
**Why it exists in this folder:** Target core for LFX **CFI** and **DFI** (Fall 2026).  
**Analysis dates:** 2026-07-18 (initial deep pass + re-verify same day)  
**Status of mainline:** last push **2026-06-08** (v3.1); public issues/PRs flooded **13–18 July 2026** by LFX applicants.

---

## 1. Identity

| Field | Value |
|---|---|
| Org | **BSC LOCA** — Barcelona Supercomputing Center, Laboratory for Open Computer Architecture |
| Org URL | https://github.com/bsc-loca |
| Core | **Sargantana** — 64-bit RISC-V (README: RV64GB) |
| Microarch | 7-stage pipeline: **OoO write-back**, **register renaming**, non-blocking memory |
| Silicon claim | 1.26 GHz typical / 1.69 GHz fast, **22 nm FD-SOI** |
| Language | ~**81% SystemVerilog** |
| Stars / forks / watchers | **146** / **29** / **8** |
| Open items | **24** (issues + PRs combined on API) |
| Commits on main | **~1,347** |
| License | Solderpad Hardware License **v2.1** |
| Default branch | `main` |
| Latest release | **v3.1** (2026-06-08); also v3.0, v2.1, v2.0 |
| Official MARCHID | **51** (v3.1 notes) |

**Paper vs code:** 2022 Euromicro paper title says *“in-order”*; live README describes renaming + OoO write-back. Core has **evolved past the paper**. Use paper for background only.

**Citation (README):**  
Soria-Pardos et al., “Sargantana: A 1 GHz+ in-order RISC-V processor with SIMD vector extensions in 22nm FD-SOI,” Euromicro 2022.

---

## 2. Critical contribution workflow (read this first)

Public GitHub is a **release mirror**, not a normal continuous-merge OSS project. Internal work is on BSC GitLab.

Maintainer **@narcisrodas** (issue #3, July 2026):

> We agree with the fix, you can open a PR… We will **port your commit to our internal version**, and once it passes all checks… it will be included in the **next release**. The PR will **remain open until the next release**; then we close it as the commit is already present.

**Implications for LFX applicants:**

- Expect **few/no classic “Merged” green PRs** for outsiders  
- Value = **issue quality + correct patch + mentor interaction + tests**  
- Do not measure success only by GitHub merge count  

---

## 3. Design map

### Pipeline modules (`rtl/datapath/rtl/`)

```text
if_stage_1   — fetch, branch predictor, return_address_stack
if_stage_2
id_stage     — decoder.sv (CFI decode hooks land here)
ir_stage     — rename
rr_stage
exe_stage    — ALU, branch_unit, LSQ, store_buffer, SIMD, FPU
wb_stage
interface_csr
```

Also: `control_unit/`, `top_drac.sv` (HPM map), `csr/` + `mmu/` submodules.

### Submodules (`.gitmodules`)

| Path | URL | Fork-friendly? |
|---|---|---|
| `rtl/csr` | relative `../csr.git` | **No** — breaks on personal forks |
| `rtl/mmu` | relative `../mmu.git` | **No** |
| `rtl/common_cells` | pulp-platform absolute | Yes |
| FPU (cvfpu) | OpenHW absolute | Yes |

**Workaround (issue #25):**

```bash
git config submodule.rtl/csr.url https://github.com/bsc-loca/csr.git
git config submodule.rtl/mmu.url https://github.com/bsc-loca/mmu.git
git submodule update --init --recursive
```

### Simulation is NOT in this repo

Use **[bsc-loca/core_tile](https://github.com/bsc-loca/core_tile)** (~18★): Sargantana + iCache + HPDcache + MMU.

Needs roughly: gcc ≥10.5, riscv64-unknown-elf-gcc ≥12, Verilator ≥5.004 or Questa ≥2021.3; optional gtkwave, Konata.  
Ubuntu 22 x86/arm64 reported working (issue #1).

### Ecosystem (bsc-loca)

Notable siblings: `core_tile`, `csr`, `mmu`, `reptiles` (OpenPiton + Sargantana), `sauria` (systolic AI), caches, peripherals.

---

## 4. Releases (capability snapshot)

| Tag | Date | Highlights |
|---|---|---|
| **v2.0** | 2025-05 | RVV mostly 1.0 (no LMUL>1 / no vec FP yet); vector rename; Debug; Sscofpmf; B (Zba/Zbb/Zbs); OpenPiton multi-core Linux |
| **v2.1** | 2025-08 | Bugfixes; unified RF modules |
| **v3.0** | 2026-06-08 | Vec FP (CVFPU); **Hypervisor H**; Zvbb; CMOs (Zicbom/Zicbop/Zicboz); Zicond |
| **v3.1** | 2026-06-08 | Zfhmin, Zvfhmin, Zfa, Smcntrpmf; MARCHID=51 |

**Still incomplete (their notes):** full RVV 1.0 with **LMUL>1**.  
**No public CFI extensions** (Zicfilp/Zicfiss) integrated yet — deferred to mentorship.

Recent internal authors before silence: narcisrodas, marc-marcos, OmarAlym, theOfficeCat.

---

## 5. Issues / PRs wave (LFX applicants)

### Stats (2026-07-18)

| | Count |
|---|---|
| Pure issues | ~20 (many open) |
| PRs | ~15 (**0 with merged_at** on public) |
| Pre-July activity | Almost only #1 (sim help, 2025) + PR #2 (2025) |

### Open pure issues (re-verified open list)

| # | Topic | Author |
|---|---|---|
| 3 | SIMD/FP free_list empty not stalling IQ | AdeshDeshmukh |
| 7 | EXTERNAL_HPM_EVENT_NUM validation | tejassinghbhati |
| 9 | LSQ TLB store perm on read prefetches | AdeshDeshmukh |
| 10 | Re-enable rename/free-list asserts | Saksham05oct |
| 15 | Makefile docs incomplete | Shivam-Shukla0 |
| 19 | vf7_wrapper SELRANGE lint | Saksham05oct |
| 20 | Store-buffer false collisions (perf) | anushkagupta200615-jpg |
| 22 | make lint fails (missing packages) | Shivam-Shukla0 |
| 25 | Fork recursive clone / relative submodules | Shivam-Shukla0 |
| 26 | Package width mismatches | Shivam-Shukla0 |
| 30 | RAS pop-then-push wrong slot | tejassinghbhati |
| 32 | lmul never assigned at RR | Saksham05oct |
| 33 | free_list reset hardcodes 32 | Shivam-Shukla0 |

### Mentor decisions (high signal)

| Event | Lesson |
|---|---|
| #3 free_list — narcis **agreed**, ask for PR | Real TODO fixes welcome |
| #9 LSQ prefetch — **@Dar0k** agreed + write-prefetch nuance | Read decoder carefully |
| #7 HPM enforce configs — **rejected** RTL; docs OK | Don’t force policy they don’t want |
| #4 Zicfilp / csr envcfg CFI — **not planned yet** | Don’t spam CFI PRs pre-term |
| #13 LR/SC timeout — closed as **max_cycles**, not deadlock | Don’t misreport sim limits |
| #18 BTB / #23 JAL misalign — peer-debunked false bugs | Quality bar is high among applicants |

### Open PRs (snapshot)

| # | Author | Topic |
|---|---|---|
| 2 | davymillion | Cache line param (old, 2025) |
| 5 | AdeshDeshmukh | free_list empty → stall |
| 8 | tejassinghbhati | HPM docs 40–50 |
| 14 | Saksham05oct | Rename asserts |
| 17 | Shivam-Shukla0 | Makefile docs |
| 21 | anushka | Store-buffer PPN (peer-contested safety) |
| 24 | Shivam-Shukla0 | veri_lint packages |
| 27 | Shivam-Shukla0 | pkg width mismatches |
| 28 | AdeshDeshmukh | LSQ prefetch TLB |
| 29 | Saksham05oct | vf7 SELRANGE |
| 31 | tejassinghbhati | RAS fix + **unit testbench** |

### Active applicant ranking (public signal only)

| Rank | User | Signal |
|---|---|---|
| 1 | **Shivam-Shukla0** | High volume infra + peer reviews |
| 2 | **Saksham05oct** | Deep RTL finds; debunked false bugs |
| 3 | **tejassinghbhati** | RAS + unit TB; mentor-steered HPM docs |
| 4 | **AdeshDeshmukh** | Real TODOs; mentor agreements |
| 5 | anushkagupta… | Aggressive bugs; some contested |
| 6 | skypank-coder | **Only explicit CFI** pre-work (deferred by mentors) |

**Repo is not “untouched.”** Strong competition mid-July 2026.

---

## 6. People map

| Handle | Role |
|---|---|
| **@narcisrodas** (Narcís Rodas) | Primary public gatekeeper; top committer; paper co-author; releases |
| **@Dar0k** (David Roche) | Technical replies (e.g. LSQ) |
| **@emanueleparisi** (Emanuele Parisi, BSC) | LFX CFI/DFI mentor; extensions in cores |
| **@Rubén Salvador** | LFX CFI/DFI mentor (Inria / CentraleSupélec SUSHI) |
| **@OmarAlym** | CSR submodule work |

Historical authors: many BSC emails in `CONTRIBUTORS.md` (Soria-Pardos, Doblas, Moretó, etc.).

---

## 7. CFI / DFI implications for applicants

| Fact | Meaning |
|---|---|
| CFI not in public tree | Mentors closed premature CFI enablement issues |
| Mentorship will implement shadow stack + landing pads | Official LFX CFI description |
| DFI = HW first, LLVM PoC stretch | Full-stack but phased |
| Public pre-work should prove **RTL competence** | Not force unsolicited CFI PRs |
| Sim path = **core_tile** | Setup is a differentiator |

**Good pre-work if applying CFI/DFI:**

1. core_tile sim + ISA tests green  
2. Short microarch notes (pipeline stages, rename, LSQ)  
3. CFI/DFI design note (where hooks would go) without fighting “not planned yet”  
4. Optional: 1 accepted non-CFI bugfix with mentor agreement  

---

## 8. Onboarding checklist

1. Read README + paper (background)  
2. Fix submodule URLs if forking  
3. Clone **core_tile**; install Verilator + riscv toolchain  
4. Read `drac_pkg.sv`, `decoder.sv`, `datapath.sv`, branch/RAS, LSQ  
5. Try `make lint` (may fail until package fixes — see #22/#24)  
6. Watch maintainer comment style before opening PRs  

---

## 9. Bottom line

| Question | Answer |
|---|---|
| Serious core? | **Yes** — silicon path, multi-release, Linux/OpenPiton |
| Easy LFX because quiet stars? | **No** — quiet until LFX listing; then strong applicant scrum |
| Prove contrib via merges? | **Hard** — internal port model |
| Primary LFX for this candidate? | **No** — AI Part II is primary; this is **RTL backup** |
| Gatekeeper | **@narcisrodas**; mentors **Emanuele Parisi + Rubén Salvador** |

Full narrative of competition/quality also lives in chat history; this file is the durable summary.
