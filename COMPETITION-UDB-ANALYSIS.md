# Competition & traffic analysis — `riscv/riscv-unified-db` (AI Part II)

**Researched:** 2026-07-19  
**Repo:** https://github.com/riscv/riscv-unified-db  
**Caveat:** GitHub **does not** publish LFX applicant counts. Traffic views/clones need repo-admin auth (401). Estimates below use **public proxies only**.

---

## 1. Repo snapshot (live)

| Metric | Value |
|--------|--------|
| Full name | `riscv/riscv-unified-db` |
| Created | 2024-07-12 |
| Description | Machine-readable RISC-V spec DB + artifact tools |
| Stars | **194** |
| Forks | **192** (network_count 192) |
| Open issues+PRs | **332** |
| Watchers (subscribers_count) | **8** (API; often undercounts vs stars) |
| Language | Ruby (monorepo; Python also used) |
| Default branch | `main` |
| Homepage | https://riscv.github.io/riscv-unified-db/ |
| Discussions | Enabled |
| Pages | Enabled |
| Last push | 2026-07-19 |
| Size | ~80 MB git |

**Compare (same day context):** `bsc-loca/sargantana` ~146★ / **30** forks / ~25 open — UDB has **~6× forks** and far more open traffic surface.

---

## 2. Traffic (views / clones)

| Endpoint | Result |
|----------|--------|
| `/traffic/views` | **401** Requires authentication |
| `/traffic/clones` | **401** Requires authentication |

**Conclusion:** True unique visitors / clone counts are **not public**. Anyone claiming exact traffic without being a collaborator is guessing.

**Proxies we can use instead:** forks/day, PR/issue creation, commit cadence, contributor list.

---

## 3. Fork timeline (strongest “application season” signal)

Loaded **189/192** forks via API (2 pages).

### Forks by month

| Period | Forks | Notes |
|--------|------:|--------|
| 2024-07 → 2024-12 | ~14 | Early repo life |
| 2025-01 → 2025-06 | ~23 | Steady |
| **2025-07** | **17** | Prior summer spike |
| 2025-08 → 2025-12 | ~23 | |
| **2026-01** | **30** | Large spike (prior term / events?) |
| 2026-02 → 2026-06 | ~41 | Active OSS |
| **2026-07 (month to date)** | **41** | **Highest month in history of this sample** |

### July 2026 by day (application window starts ~Jul 15)

| Date | New forks |
|------|----------:|
| Jul 5–12 | 3 |
| **Jul 13** | **5** |
| **Jul 14** | **4** (RVI mentorships listed ~Jul 14) |
| **Jul 15** | **10** (apps open) |
| **Jul 16** | **8** |
| Jul 17 | 3 |
| **Jul 18** | **7** |
| Jul 19 | 1+ |

**~33 forks in ~Jul 13–18 alone.** That is a **clear surge** correlated with Fall LFX going live—not proof each forker applied to Part II (see §7).

Sample newest fork owners (Jul 14–19):  
shellyco-code, nikhil3495, Qivoxe, AlgoArtist06, Maanvi212006, deepak0x, Adii0906, Aman071106, A-Chronicle, Prat260104, Goyamjain06, khanak0509, rimmie26, Teemooooooooo, Saksham05oct, RajGautam2004, yuvraj-kolkar17, subinita01, RAJVEER42, Purav001, Priya-Sharma25, Shivampal157, krrishverma1805-web, shivamsingh-007, Kayd-06, aruhis10, 2024itb047samata, shrevid03, …

Many Indian student-style handles + some known UDB contributors forking again.

---

## 4. Contribution / commit traffic

### Top contributors (API list, 70 accounts)

| Login | Contributions (approx) | Role guess |
|-------|----------------------:|------------|
| **dhower-qc** | 388 | Core maintainer (Derek Hower / QC) |
| renovate[bot] | 241 | Dep bots |
| jordancarlin | 65 | Active maintainer-level |
| ThinkOpenly | 61 | Paul Clarke (RVI mentor culture) |
| ayosher | 61 | Regular |
| **ishaan-arora-1** | **29** | **Spring LFX param extraction** |
| ShashankVM | 23 | |
| kevbroch | 22 | |
| **adingank-qualcomm** | **10** | Likely **Ajit Dingankar** (mentor) |
| AFOliveira, lucifer4330k, others | … | Generators / tools |
| Many 4–12 commit users | | Student/OSS contributors |

~**70** listed contributors; bots inflate activity.

### Weekly commit participation (52 weeks, `stats/participation`)

- **Sum ~625 commits** over 52 weeks (all contributors)  
- Recent burst: last weeks include **34** and **68** commit weeks (heavy bot + human)  
- Last 12 weeks sum **~143** — healthy ongoing project  

Recent `main` commits: heavy **renovate[bot]**, plus humans: krrishverma1805-web, jordancarlin, Teemooooooooo (param), AnshulPatil2005, lucifer4330k, Felix-Gong, …

---

## 5. Issues / PRs volume

| Signal | Value |
|--------|--------|
| Open issues+PRs | **332** |
| Search `LFX` in repo | **29** items (almost all **ishaan-arora-1** phase issues/PRs) |
| Open PRs (first page 50) | **28 unique authors** on that page alone |
| PRs created **2026-07-14 → 07-20** | **47** total (many renovate) |
| Human PR authors in that window | krrishverma…, Maanvi212006, AnshulPatil2005, AlgoArtist06, Goyamjain06, khanak0509, Teemooooooooo, RAJVEER42, jordancarlin, … |

### Param / LFX-related open PRs (examples)

| # | Author | Topic |
|---|--------|--------|
| 1765–1832 | **ishaan-arora-1** | Full Spring LFX param pipeline (still open) |
| 1790, 1803 | **ankit-cybertron** | Chunking / classifier (parallel Spring track) |
| 1991 | RAJVEER42 | HPM_COUNTER_EN param semantics |
| 1994 | Teemooooooooo | ZAWRS_NTO_IS_NOP param |
| 1995 | jordancarlin | PMP parameters overhaul |
| 2019 | AlgoArtist06 | Z3 anyOf for parameters |
| 1963 | davidharrishmc | Parameters for interrupts |

**Interpretation:** Repo is busy for **many reasons** (UDB data quality, generators, bots). Param work is a **subset**. LFX-titled work is **dominated by Spring mentees**, not a flood of new “LFX Part II” issues yet (as of research date).

---

## 6. Named people (competition-relevant)

### Already embedded in param-extraction history

| Person | Signal | Competition meaning |
|--------|--------|---------------------|
| **ishaan-arora-1** | 16 LFX-titled items; 9 open param PRs; 29 contributions | Spring primary pipeline author — may re-apply, mentor-side, or hand off |
| **ankit-cybertron** | Parallel RAG/chunk/classifier PRs; LinkedIn LFX’26 extraction | Spring co-track; same for Part II risk |
| **adingank-qualcomm** | UDB commits; mentor Ajit Dingankar | **Mentor**, not competitor |
| **ThinkOpenly** | Paul Clarke | Mentor-adjacent RVI culture |
| **dhower-qc / jordancarlin** | Maintainers | Gatekeepers for merge |

### July wave (active OSS on UDB, not necessarily Part II applicants)

High-visibility recent humans: **krrishverma1805-web**, **Maanvi212006**, **AnshulPatil2005**, **AlgoArtist06**, **deepak0x**, **Goyamjain06**, **khanak0509**, **RAJVEER42**, **Teemooooooooo**, **Saksham05oct** (also seen on Sargantana), **AdeshDeshmukh** (Sargantana LFX-adjacent), …

Some of these may be:

- General UDB contributors  
- Applying to **other** RVI LFX projects but using UDB  
- Applying to **Part II** with pre-work  
- Drive-by / resume activity  

**Cannot map fork → LFX application 1:1.**

---

## 7. How many people are “probably competing” for Part II?

### Hard facts

| Fact | Value |
|------|--------|
| Published applicant count | **None** |
| Paid seats (RVI policy) | **~1** first mentee; optional unpaid extras |
| Max apps per person | 3 projects |
| Apps window | 15 Jul – 5 Aug 2026 |

### Soft estimates (order of magnitude)

| Cohort | Estimate | Basis |
|--------|----------|--------|
| **Serious Part II competitors** (read Spring PRs, pre-work, fit essay) | **~15–40** | July fork surge diluted across whole UDB; param domain is niche; AI keyword widens net |
| **Total LFX applications to this project** (including weak/generic) | **~40–120** | AI + remote + paid attracts more than pure RTL; still not CNCF-scale |
| **Effective shortlist mentors read carefully** | **~8–20** | Pre-work + resume + specificity |
| **Seats** | **1 paid** (+ maybe 0–2 unpaid) | RVI rules |

**Calibrated guess for “people who could beat a weak app”:** dozens.  
**Calibrated guess for “people who did real pre-work on param extraction”:** low tens or fewer.  
**You only need to be #1 of the paid seat**, not beat every forker.

### Why not “192 competitors”

- 192 = **lifetime forks**, years of history  
- Many forks never apply  
- Many July forks are for **general UDB contribution** culture (repo is famously contribution-friendly)  
- Sargantana-style applicants sometimes multi-apply and fork both repos  

### Why not “only 2 people”

- Spring already had **2** strong extraction tracks  
- July surge is real  
- “AI-assisted” title broadens applicant pool beyond pure ISA nerds  

---

## 8. What competition looks like on GitHub (quality tiers)

| Tier | Behavior | Threat level |
|------|----------|--------------|
| **A** | Read #1765–#1832; reproduce metrics; pre-work repo with eval notes; knows WARL gap | **High** |
| **B** | Clone UDB; fix small param/data bugs; generic LLM interest essay | Medium |
| **C** | Fork only; empty; “I love AI and RISC-V” | Low |
| **Incumbent** | ishaan / ankit re-applying or referred | **High** if they apply again |
| **Maintainer-sponsored** | Internal / known SIG student | Unknown; rare but decisive |

Most July forks look **Tier B/C** until proven otherwise. Your edge is **Tier A** behavior without claiming Spring’s work as yours.

---

## 9. Activity that is *not* Part II competition

- renovate[bot] flood  
- General CSR/instruction data PRs  
- Generator backends (QEMU, GAS, …)  
- Sorbet/Ruby infra fixes  
- Z3 constraint work (adjacent to params but different goal)  

Busy repo ≠ every contributor wants this mentorship.

---

## 10. Strategic implications for you

1. **Repo is high-traffic OSS**, not a dead quiet corner — expect many **applications**, fewer **serious** ones.  
2. **Do not compete by raw issue spam** on main the way Sargantana CFI wave did; Part II is judged more on **understanding Spring pipeline + pre-work quality**.  
3. **Cite Spring metrics** as baseline to improve; don’t open 8 fake “Phase 9” issues.  
4. **Public pre-work** on *your* repo (notes + tiny eval sketch) beats silent fork.  
5. **~1 seat** → quality over volume.  
6. Watch whether **ishaan-arora-1 / ankit-cybertron** stay active into Fall applications (incumbent risk).

---

## 11. Data limits (honesty)

| Cannot know from outside | Why |
|--------------------------|-----|
| Exact LFX applicant count | Private to LFX |
| Views/clones | Admin-only traffic API |
| How many unpaid seats mentors take | Mentor decision |
| Who applied without GitHub noise | Silent majority |

---

## 12. Bottom line

| Question | Answer |
|----------|--------|
| How busy is UDB? | **Very** — 194★, 192 forks, 332 open, daily commits, July PR flood |
| Application-season traffic? | **Clear** — **41 forks in July**, ~**33 in ~6 days** after LFX listing |
| How many competing for Part II? | **Unknown exact**; **likely tens of apps**, **~15–40 serious**, **1 paid seat** |
| Is it “easy”? | **No** — AI title + active repo + Spring bar |
| Is it “hopeless”? | **No** — most forks ≠ prepared Part II candidates; Spring work is **open for you to study and extend** |

Re-check before apply: fork counts, new LFX-titled issues, activity from ishaan/ankit.
