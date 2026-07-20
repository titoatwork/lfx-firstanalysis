# LFX Mentorship + Year-4 Master Plan — Full Handoff

**Created:** 2026-07-18  
**Last deep refresh:** 2026-07-18 (evening) — re-pulled LFX API project cards, RVI mentorship policy, GitHub (sargantana + UDB), stipend docs  
**Purpose:** Complete handoff so a new chat/session can continue without re-deriving a long thread.  
**Owner:** Ibteshamul Haque  
**Folder:** `Desktop\LFX-Mentorship\`

### Companion files (read as needed)

| File | Contents |
|---|---|
| [README.md](./README.md) | Index + quick start |
| [PROJECTS.md](./PROJECTS.md) | Full Fall 2026 project cards, seats, mentors, UDB notes |
| [SARGANTANA-ANALYSIS.md](./SARGANTANA-ANALYSIS.md) | Deep CFI/DFI repo analysis (issues/PRs/workflow) |

---

## 0. How to use this file

1. Read **§1 Identity** and **§2 Decisions locked** first.  
2. For LFX execution, jump to **§8–§12** + **PROJECTS.md**.  
3. For full year strategy, read **§3–§7**.  
4. At kickoff (**19 July 2026**), follow **§11 72-hour plan** and fill **§11.6 kickoff template**.  
5. Do **not** re-open settled debates unless facts change (deadlines, project list, mentor reply).  
6. Before apply: re-check LFX UI still **Accepting** + deadline still **5 Aug 2026**.

---

## 1. Who the candidate is

| Field | Detail |
|---|---|
| **Name** | Ibteshamul Haque (confirm exact spelling on legal docs) |
| **Stage** | Just finished **3rd year** undergrad; entering **4th / final year** |
| **Home university** | **UPES** (India, self-described tier-3) |
| **CGPA** | **~7.5/10** (75% converted by uni); target by graduation **~7.9** |
| **Work capacity** | High — willing to put in heavy hours; risk is **overcommitment**, not laziness |
| **Brand constraint** | College name does not open doors; **public artifacts + research** must |
| **Technical ambition** | HPC / systems / parallel computing; eventual **GSoC 2027** with **HPX** (STE\|\|AR) |
| **Research already done** | Attachment at **Universiti Malaya (UM)** under **Prof. Por Lip Yee** |
| **UM paper status** | **Development work finished**; now **paper writing only** |
| **UM writing help** | A **PhD student is already assigned** to help write the UM paper |
| **UM venue target** | **FGCS** (*Future Generation Computer Systems*, Elsevier) — stretch Q1-style systems journal; reviews often take months |
| **Por Lip Yee (context)** | UM professor; ML/AI, cybersecurity, intelligent systems / healthcare AI (not pure HPC). Primary research mentor for UM paper. |
| **Home uni resources** | UPES has an **HPC lab with H100s** (user reports); wants a **separate UPES paper** as a challenge |
| **UPES project time** | Can work on home-uni project **during school hours** |
| **Free time split** | Evenings/weekends: **GATE + self-study + LFX and/or HPX** |
| **LinkedIn / GitHub** | Self-assessed as **not strong** — fix in 72h pack to “acceptable + pre-work,” not “impressive” |
| **CGPA on LFX resume** | **Omit by default** (not important for OSS/LFX) |

### What “success” looks like

> International research (UM) → journal pipeline → optional **LFX** credential → **GATE** → research-oriented Indian MS → optional **GSoC 2027 (HPX)**

Commitment is shown by **finished deliverables + LoRs + continuous spine**, not by doing only one thing forever.

### Feasibility judgment (can this candidate do LFX?)

| Question | Judgment |
|---|---|
| **Complete the term if accepted?** | **Yes** — high capacity; AI Part II is learnable (Python/LLM/YAML/specs), not pure silicon cold-start |
| **Get accepted?** | **Possible, not automatic** — competitive (~1 paid seat); needs **pre-work + complete prereqs + specific essay** |
| **Without pre-work?** | Effectively **no** — becomes noise vs prepared applicants |
| **CFI/DFI from zero RTL?** | **Much harder** than AI Part II; only if committed to RTL ramp + Sargantana competition |

---

## 2. Decisions locked (as of last refresh)

| Decision | Status |
|---|---|
| **Primary formal near-term credential** | **LFX Fall 2026 first** |
| **HPX deep work** | **Not ASAP** — start roughly **from December 2026** for **GSoC 2027** |
| **GSoC target org theme** | **HPX / STE\|\|AR** (simd / par_unseq / parallel algorithms) — later |
| **LFX primary project** | **AI-assisted extraction of architectural parameters from RISC-V specifications – Part II** |
| **LFX backups** | RISC-V **CFI** or **DFI** only if willing to learn RTL; else skip |
| **Unpaid Women in Energy** | Not default |
| **Hard timeline collisions** | **Avoid two full-intensity bosses** (e.g. full LFX + max GATE peak) |
| **Soft overlaps** | OK (paper + GATE foundation; school-hours UPES + evening LFX) |
| **GSoC + MS same summer** | Prefer **not** both full-burn; GSoC then MS join, or MS then GSoC next year |
| **UM paper** | Write/submit with PhD student help — **do not start a second UM research project** |
| **UPES paper** | Optional **scoped** challenge during school hours |
| **72h LFX campaign start** | **19 July 2026** (July, not June) |
| **CGPA on LFX resume** | **Omit** |
| **GSR / other distractions** | Out of scope unless user re-opens |

---

## 3. Overall year-4 strategy (Aug 2026 → graduation ~2027)

### 3.1 Spines and ribs

| Role | Track | Notes |
|---|---|---|
| **Spine A — Research** | UM → FGCS write/submit/revise | Dev done; writing with PhD student |
| **Spine B — Academic gate** | **GATE CS 2027** (~Feb 2027) → MS apps | Peak Jan–mid Feb |
| **Rib — Home project** | UPES H100 / FYP / optional paper | **School hours** |
| **Rib — LFX** | Fall 2026 Sep–Nov | **Primary free-time job** if accepted |
| **Rib — HPX** | From ~Dec 2026 | For GSoC Mar 2027 proposal |
| **Crown** | GSoC 2027 **or** MS join intensity | One summer flagship |

### 3.2 Sequencing (user-approved)

```text
NOW → mid-Aug 2026
  - 72h LFX apply pack starting 19 July
  - UM paper writing (PhD student)
  - UPES school hours
  - Light GATE foundation

Sep → Nov 2026   (if LFX accepted)
  - LFX = PRIMARY free time (~60–70%)
  - GATE maintenance (~25–30%)
  - HPX ≈ pause
  - UM = revisions only
  - UPES = school hours

Dec 2026
  - GATE rising (~50–55%)
  - HPX bootstrap (~30–35%)
  - Papers as needed

Jan → mid-Feb 2027
  - GATE PEAK (~85–90%)
  - HPX minimal / off

Late Feb → Apr 2027
  - MS applications + interviews
  - HPX sprint + GSoC proposal if trail exists
  - Paper review responses

May → Aug 2027
  - ONE primary: GSoC OR MS join (not both full-burn)
```

### 3.3 Why LFX-before-HPX is OK for GSoC 2027

- GSoC 2027 contributor apps typically **~March 2027**.  
- Deep HPX from **Dec → Mar** (with GATE pause Jan–Feb) is **enough** for a serious proposal if focused.  
- No need to hop on HPX in July 2026.

### 3.4 Avoid hard collisions

**Avoid simultaneous full intensity of:**

- LFX (~30 h/week) + peak GATE (Jan–Feb)  
- Full GSoC + brutal first MS semester  
- New heavy research + LFX + max GATE  

**OK:**

- School-hours UPES + evening LFX  
- UM writing help from PhD student + LFX  
- Light GATE during LFX season  
- GSoC ending mid-Aug + MS starting late Aug (if dates barely touch)

---

## 4. UM paper (Por Lip Yee)

| Item | Detail |
|---|---|
| Status | **Implementation/dev done** |
| Remaining | **Paper writing**, coauthor process, submit |
| Help | **PhD student assigned** for writing support |
| Target | **FGCS** (confirm with Por; backup venue if he says so) |
| FGCS reality | Strong Elsevier venue; review can take **months**; do not block GATE on acceptance |
| Resume language until accepted | “Manuscript in preparation / under review” — **never fake published** |
| Priority vs LFX 72h | During 19–21 July: only **quick replies** if Por/PhD student need you |

After submit → **maintenance mode** (review responses when they arrive).

---

## 5. UPES home-uni paper / H100 lab

| Item | Detail |
|---|---|
| Intent | Separate home-uni paper as a challenge |
| Resources | HPC lab with **H100s** (verify faculty access) |
| Time box | Prefer **school hours** during LFX season |
| Scope | Tight: one problem, baselines, numbers — not a second multi-year arc |
| Faculty | Need UPES guide who will **supervise and coauthor** |

---

## 6. GATE and MS (context for later)

### 6.1 GATE 2027 (verify on official portal)

- Registration often **Aug–Oct 2026**  
- Exam often **early–mid February 2027**  

### 6.2 Score targets (GATE score /1000, Gen CS — approximate)

| Goal | Target |
|---|---|
| Research MS shortlist hope | **~700+** floor; **~780–800+** safer |
| Stronger options | **850+** |
| IISc **course** M.Tech CSE style cutoffs | Often very high; plan **900+** if that is the goal |

### 6.3 IISc paths (do not confuse)

| Programme | Admission |
|---|---|
| **M.Tech CSE (course)** | Mostly GATE via COAP — very high cutoffs |
| **M.Tech (Research)** | GATE shortlist + **interview**; portfolio (UM, papers, systems) matters |
| CFTI 8.0 GATE waiver | **Not available** (tier-3, CGPA &lt; 8.0 from CFTI) |

### 6.4 Money order of magnitude (if successful)

| Source | Rough scale |
|---|---|
| Year 4 lab/paper | Usually **₹0** |
| LFX stipend | **~$1,000–$6,600** PPP (if paid track + evaluations) |
| GSoC India | Often cited ~₹60k–₹2.5L+ (size/PPP) |
| MS GATE scholarship | ~₹12.4k/mo × 24 if rules apply |

Path funds **study/credentials**, not FAANG intern cash.

---

## 7. HPX / GSoC 2027 (deferred)

### 7.1 Ground truth (do not re-derive blindly from old “Tito” notes)

- Repo: `github.com/TheHPXProject/hpx` (LF; old STEllAR-GROUP redirects)  
- **#2271** open, GSoC-labeled, pinned (par_unseq / vectorization lineage)  
- Two tracks (hkaiser): **`simd`/`par_simd`** (explicit datapar) vs **`unseq`/`par_unseq`** (compiler auto-vec)  
- **#6018 merged (2023)** — unseq infrastructure exists  
- **#2333** closed (not an open scoreboard)  
- Contested lane; GSoC needs prior merged work + proposal + presence  

### 7.2 When to start HPX

- **Not** during LFX 72h apply  
- **Not deep** during LFX Sep–Nov  
- **Dec 2026:** bootstrap  
- **Jan–mid Feb:** near-pause for GATE  
- **Late Feb–Mar:** sprint for GSoC proposal  

### 7.3 Old plan file (historical only)

`C:\Users\Ibteshamul Haque\Downloads\message (1).txt` — useful historically; **must not** be executed blindly.

---

## 8. LFX Mentorship — program facts

| Item | Detail |
|---|---|
| Platform | https://mentorship.lfx.linuxfoundation.org |
| Org model | Mentorship (mentee + mentor + project), **not** LF employment |
| Apply docs | https://docs.linuxfoundation.org/lfx/mentorship/mentees/apply-to-a-project |
| Profile docs | https://docs.linuxfoundation.org/lfx/mentorship/mentees/create-a-mentee-profile |
| Status docs | https://docs.linuxfoundation.org/lfx/mentorship/mentees/view-status-of-your-application |
| Stipends doc | https://docs.linuxfoundation.org/lfx/mentorship/mentee-stipends |
| Stipend amount | PPP; **base $6,000**, **min ~$1,000**, **max ~$6,600**; installments after evaluations |
| Max apps per term | **3** |
| Navigation | **Become a Mentee** = profile; **Mentorships → Accepting Applications** = apply; **My Projects** = status |
| Interviews | **Not always required**; mentors may do informal call / async questions |
| Selection | **Not random** — resume, text, prereqs, pre-work, fit |
| Quiet GitHub on project repos | **Not** a reliable “low competition” signal |

### 8.1 Is LFX reputed?

**Yes, in open-source / systems / LF ecosystems.** Not a diploma mill.

| Audience | Perception |
|---|---|
| OSS / RISC-V / systems people | Strong positive if you **finish** + show public work |
| Research MS interviews | Supporting evidence of commitment/skill (with UM) |
| Generic campus HR | Mixed name recognition — spell out “Linux Foundation Mentorship” |
| vs GSoC | GSoC more famous globally; LFX is peer-class OSS mentorship |
| vs big-tech intern | **Not equivalent** by default |

**Reputation is conditional:** graduated + public artifacts ≫ “selected only.”  
RVI-sponsored Fall projects are **serious** (industry-funded mentorships).

### 8.2 Seats (RVI policy — verified 2026-07-18)

From [riscv.org/community/mentorship](https://riscv.org/community/mentorship/):

> **First selected mentee** receives a **stipend**.  
> **Additional mentees may** join **unpaid** for experience.

| Assumption for planning | Value |
|---|---|
| Paid seats per project | **~1** |
| Unpaid extras | Optional / not guaranteed |
| How to compete | Fight for the **paid** seat |
| LFX API seat field | **None** — policy is RVI-side |

### 8.3 Application status codes

- **Pending** — received; may still need prereqs  
- **Accepted** — follow email instructions  
- **Declined** — rejected  
- **Withdrawn** — you withdrew  
- **Graduated** — completed  

Incomplete prerequisites → stuck Pending / not really competing.

### 8.4 RVI Fall 2026 timeline (marketing + API)

| Milestone | Date |
|---|---|
| Mentorships on LFX | ~14 July 2026 |
| Applications | **15 July – 5 August 2026** |
| Review / decisions / HR | ~6–22 August 2026 |
| Decline notifications | ~8 September 2026 |
| **API term (all 3 RVI projects)** | **15 Sep – 15 Nov 2026** |
| RVI page also says | Sep 1 – Nov 30 — use mentor/LFX term as work authority |
| Hours | ~**30 h/week** |

---

## 9. Live project landscape (re-verified 2026-07-18)

**Full cards:** see **[PROJECTS.md](./PROJECTS.md)**. Summary below.

### 9.1 Projects that matter

| # | Project | Mentors | Repo | Role |
|---|---|---|---|---|
| 1 | **AI params Part II** | Allen Baum, Ajit Dingankar | [riscv-unified-db](https://github.com/riscv/riscv-unified-db) | **PRIMARY** |
| 2 | **CFI** (shadow stack + landing pads) | Rubén Salvador, Emanuele Parisi | [sargantana](https://github.com/bsc-loca/sargantana) | Backup if RTL |
| 3 | **DFI** (tightly-coupled; HW then LLVM PoC) | Same as CFI | sargantana | Backup if RTL |
| 4 | Women in Energy (unpaid) | LF Energy | — | **Skip** |

All three RVI: `acceptApplications: true`, app end **2026-08-05**, term **2026-09-15 → 2026-11-15**.

| Project | LFX ID | Direct link |
|---|---|---|
| AI Part II | `22296947-cecb-4a8f-8bcb-4f34710e9f66` | https://mentorship.lfx.linuxfoundation.org/project/22296947-cecb-4a8f-8bcb-4f34710e9f66 |
| CFI | `846490b5-2092-4645-895a-83c147ba5b68` | https://mentorship.lfx.linuxfoundation.org/project/846490b5-2092-4645-895a-83c147ba5b68 |
| DFI | `dc34ec1a-f0d7-4be4-aa8d-0583e4bf537e` | https://mentorship.lfx.linuxfoundation.org/project/dc34ec1a-f0d7-4be4-aa8d-0583e4bf537e |

### 9.2 AI Part II — goals (official, condensed)

Continue Spring 2026 + Parameter SIG work; improve **quality + robustness**:

1. LLM extraction of architectural parameters from priv + unpriv specs (training examples: ISA Manual YAML, keyword_matches sheet, UDB YAML)  
2. Extend parameter classification  
3. AI coding agents/skills for reproducible workflows  
4. Explore export to **UDB YAML**  
5. GitHub PR of reviewed parameter files + maintainer follow-up  

**UDB (2026-07-18):** ~193★, Ruby monorepo, very active (push same day), ~330 open issues, setup via **mise**, docs preview at riscv.github.io/riscv-unified-db.

### 9.3 CFI / DFI one-liners

- **CFI:** Implement ratified RISC-V CFI (shadow stack + landing pads) on **Sargantana**; plan → RTL → emulate → overhead. BSC + SUSHI (Inria).  
- **DFI:** Tightly-coupled DFI on Sargantana; Phase 1 HW (port from SUSHI CVA-6 prelim); Phase 2 PoC toolchain/LLVM (stretch).  

**Deep repo analysis:** **[SARGANTANA-ANALYSIS.md](./SARGANTANA-ANALYSIS.md)**  
Key facts: public GH is **release mirror** (internal port of PRs); mid-July applicant flood; CFI enablement **not** integrated publicly yet; sim via **core_tile**.

### 9.4 Project choice rationale (locked)

| Project | Pros | Cons | Role |
|---|---|---|---|
| **AI Part II** | Pre-work in 72h without RTL; clear Part II; RVI | “AI” → more applicants; less pure HPC | **PRIMARY** |
| **DFI** | Systems/full-stack adjacent; BSC prestige | SystemVerilog + cold start | Backup if RTL |
| **CFI** | Clear HW security scope | Pure HW; public CFI deferred | Backup #2 if RTL |
| **Unpaid Energy** | Long window | Unpaid; off-theme | Skip |

### 9.5 API noise

Ignore stale `acceptApplications: true` ghosts (old Meshery/Jaeger/Electron, etc.).  
**Trust UI + Fall 2026 term + RVI jobs list.**

---

## 10. How to maximize LFX acceptance

### 10.1 What moves the needle (ranked)

1. **Pre-work** on *their* problem/repo (public)  
2. **Project-specific** application text  
3. Complete profile + **all prerequisites**  
4. Honest skills + clear **25–30 h/week** Sep–Nov  
5. Resume with **UM research** bullets  
6. Basic non-broken GitHub/LinkedIn  
7. Fast reply if mentors message (24–48h)  

**Low impact for LFX:** CGPA, college tier, LinkedIn polish beyond basic.

### 10.2 Interviews

- Not guaranteed.  
- Prep: project goal in own words, pre-work demo, hours, timezone, 2 smart questions, honest gaps + ramp plan.

### 10.3 Common failure modes

- Incomplete prereqs  
- Empty GitHub + generic essay  
- Apply to 3 unrelated domains  
- Overclaim skills  
- Miss mentor email  
- Last-day apply with no pre-work  

### 10.4 Max 3 applications — recommended use

1. **AI Part II** (primary)  
2. Optional second only if fully prepared (CFI or DFI)  
3. Rarely a third  

---

## 11. 72-hour campaign (starts 19 July 2026)

### 11.1 Mission

In 72 hours produce:

- [ ] Complete LFX **mentee profile**  
- [ ] Acceptable **GitHub** (README + pre-work repo)  
- [ ] Acceptable **LinkedIn** (photo, headline, UM, education)  
- [ ] **1-page resume PDF** (**no CGPA** unless form forces)  
- [ ] Public **pre-work** for primary project  
- [ ] **Application submitted** for Fall 2026 + all prereqs  

### 11.2 Hour blocks

| Hours | Focus |
|---|---|
| **0–24** | Accounts, profile, GitHub/LinkedIn, resume v1, clone repo, read description |
| **24–48** | Pre-work public repo end-to-end |
| **48–72** | Application essay, resume v2, Apply + prereqs, interview cheat-sheet |

### 11.3 Pre-work repo (AI Part II)

Suggested name: `lfx-riscv-param-extraction-prework`

```text
README.md
  - LFX project link
  - What I understand the mentee must deliver
  - What I explored in riscv-unified-db
  - What I ran / tried
  - Skills have / learning
  - 4-week plan if selected (Sep–Nov)
  - 2–3 smart questions for mentors

notes/
  - udb-overview.md
  - part-ii-goals.md

(optional) examples/
  - tiny extraction sketch or YAML sample
```

### 11.4 Application essay skeleton

```text
I'm a 4th-year CS student at UPES. I completed a research attachment at
Universiti Malaya under Prof. Por Lip Yee and am preparing that work for
publication. I'm applying to [PROJECT] for LFX Fall 2026.

I read the project description and explored [REPO]. My understanding is
that the core goal is [1–2 sentences]. Pre-work: [LINK].

Relevant background: [UM in 1 line], [Python/Git/Linux/etc.].
Gaps for week 1: [honest].

I can commit ~25–30 hours/week September–November and aim to finish with
reviewable, merged work.

Thank you for considering my application.
```

### 11.5 Rules during 72h

- No deep HPX  
- No GATE marathon (≤30 min/day OK)  
- UM paper only if PhD/Por need a quick reply  
- Sleep; don’t submit half-prereq applications  

### 11.6 Kickoff message template (paste into new chat on 19 July)

```text
LFX 72H START — local date/time:

1. Full name:
2. Email:
3. GitHub URL:
4. LinkedIn URL (or none yet):
5. City / country:
6. Phone (optional):
7. CGPA on resume? NO (default)
8. UM project bullets (3–5):
9. Skills honest (Python/C++/Git/Linux/LLM APIs):
10. Hours free per day next 3 days:
11. Primary project: AI params Part II YES/NO
12. If NO, which project?
```

After this, the agent should return: README text, LinkedIn text, full resume, pre-work commands, final essay, and checklist until Pending+complete.

---

## 12. Free-time split after acceptance / rejection

### If LFX **accepted** (Sep–Nov)

| Track | Share of free time |
|---|---|
| LFX | 60–70% |
| GATE | 25–30% |
| Paper revisions | as needed |
| HPX | ~0% |
| UPES | school hours only |

### If LFX **rejected**

| Track | Share |
|---|---|
| GATE | 50–60% rising to peak |
| UM/UPES papers | remaining focused slots |
| HPX | start earlier (Sep–Oct light, Dec stronger) |

### Dec onwards

As in §3.2.

---

## 13. Resume / LinkedIn / GitHub guidance (LFX pack)

### Resume

- **1 page**  
- **No CGPA** for LFX  
- Lead with **UM research**  
- Include pre-work link  
- Skills ordered for **target project first**  

### LinkedIn (minimum bar)

- Clear photo  
- Headline: `CS @ UPES | Research @ Universiti Malaya | Open Source`  
- About 4–5 lines  
- Education + UM experience  
- GitHub link  

### GitHub (minimum bar)

- Profile README  
- No junk empty repos pinned  
- Public pre-work repo  
- Recent activity  

**Does weak GitHub kill LFX?** Not automatically. **Weak GitHub + no pre-work + generic essay does.**

---

## 14. Commitment / colliding timelines

- Certificates alone do not prove commitment.  
- **Finished hard things + LoRs + continuous spine** do.  
- Rule: **avoid dangerous collisions; soft overlaps OK.**

---

## 15. What the next agent must NOT do

1. Restart full HPX archaeology as if LFX weren’t first.  
2. Tell user to put CGPA on LFX resume as mandatory.  
3. Guarantee LFX acceptance.  
4. Apply for the user (cannot) — only drive materials and checklists.  
5. Encourage 3 unrelated LFX apps.  
6. Treat stale API projects as real Fall 2026 targets without UI verification.  
7. Start a second multi-year research project instead of writing UM paper.  
8. Schedule full HPX + full LFX + peak GATE in the same weeks.  
9. Treat Sargantana public PRs as “merged” success metric (internal port model).  
10. Spam CFI enablement PRs maintainers already deferred.

---

## 16. What the next agent MUST do on 19 July

1. Confirm Fall projects still accepting (UI + deadline).  
2. Collect kickoff fields (§11.6).  
3. Produce complete apply pack for **AI Part II** (or user override).  
4. Drive pre-work on `riscv-unified-db` / project goals.  
5. Ensure prereqs uploaded before calling application “done.”  
6. Keep HANDOFF/PROJECTS updated if project text or deadlines change.

---

## 17. One-page operating card

```text
WHO:     Ibteshamul Haque — UPES 4th year, UM research done (writing), CGPA ~7.5 omit on LFX
PRIMARY: LFX Fall 2026 — AI params Part II (UDB)
BACKUPS: CFI / DFI on Sargantana only if RTL committed
SEATS:   ~1 paid per RVI project; unpaid extras optional
APPLY:   15 Jul – 5 Aug 2026 | TERM API: 15 Sep – 15 Nov 2026
72H:     Starts 19 July — profile + resume + pre-work + apply
THEN:    LFX Sep–Nov → HPX Dec → GATE Feb → GSoC/MS 2027
SKIP:    CGPA on LFX resume; deep HPX until Dec; hard collisions
MONEY:   LFX ~$1k–$6.6k PPP if paid+pass evals; MS ~12.4k INR/mo later
SUCCESS: Finished LFX + UM submitted + GATE solid + optional GSoC + MS path
REPUTE:  LFX is real OSS credential if graduated + public work
```

---

## 18. Related files / paths

| Path | What |
|---|---|
| `Desktop\LFX-Mentorship\HANDOFF.md` | This file |
| `Desktop\LFX-Mentorship\PROJECTS.md` | Project cards |
| `Desktop\LFX-Mentorship\SARGANTANA-ANALYSIS.md` | CFI/DFI repo deep dive |
| `Desktop\LFX-Mentorship\README.md` | Index |
| `Downloads\message (1).txt` | Old Tito/HPX master plan (historical) |

---

## 19. Changelog (handoff)

| When | What |
|---|---|
| 2026-07-18 | Initial handoff from long strategy thread |
| 2026-07-18 (refresh) | Re-fetched LFX API (full descriptions, mentors, dates); RVI seat policy; stipend PPP bounds; UDB live stats; Sargantana analysis extracted to companion file; reputation + feasibility sections; README/PROJECTS added |
