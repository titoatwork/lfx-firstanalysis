# Timeline — Spine + Spear (Part II campaign)

**As of:** 2026-07-26  
**Plan lock:** [PLAN-SPINE-AND-SPEAR.md](./PLAN-SPINE-AND-SPEAR.md)  
**Public monorepo:** https://github.com/titoatwork/lfx-firstanalysis  
**Apply target:** **2026-07-31** · internal hard stop **2026-08-02** · official ~**2026-08-05**  
**Term (if selected):** ~**2026-09-15 → 2026-11-15** · ≥30 h/week  

**Legend:** 🔴 critical · 🟠 high · 🟢 normal · ⬜ deferred · **S** = spine · **P** = spear  

---

## At a glance

```text
Jul 26          Jul 31        Aug 2     Aug 5        Sep 15              Nov 15
  |---- PHASE 1 ----|  buffer  |  late   |---- warm / spear ----|---- TERM ----|
  spine+spear pre   APPLY      hard stop official    lists, polish      9-week plan
```

| Phase | Dates | Goal |
|-------|--------|------|
| **0** Done / immediate | Jul 26 | Hygiene + start Phase 1 |
| **1** Pre-apply | **Jul 26–31** | Apply + spear challenge/CI without abandoning spine |
| **2** Buffer | Aug 1–2 | Fix only; submit if not done |
| **3** Emergency | Aug 3–5 | Contingency only |
| **4** Post-apply spear | Aug 6 – Sep 14 | Robustness, multi-model, community, smart UDB |
| **5** Term | Sep 15 – Nov 15 | Official Part II execution |

---

## PHASE 0 — Today (2026-07-26)

| When | Who | S/P | Task | Done? |
|------|-----|-----|------|-------|
| Morning | **You** | S | 🔴 Rotate OpenAI API key (was pasted in chat) | [ ] |
| Morning | **You** | S | 🔴 LFX dashboard: still Accepting? Deadline still Aug 5? | [ ] |
| Anytime | **You** | S | 🔴 Check membership approval email | [ ] |
| Anytime | **You** | S | 🟠 Subscribe RISC-V tech / SIG calendar | [ ] |
| Anytime | Agent | S | Plan docs already: `PLAN-SPINE-AND-SPEAR.md`, packet on `main` | [x] |

---

## PHASE 1 — Pre-apply spine + spear (Jul 26–31)

**Non-negotiable outcome by Jul 31:** **Part II application submitted.**  
Spear is built only if it does not delay Apply.

### Day-by-day

#### Sat 26 Jul

| Block | S/P | Task |
|-------|-----|------|
| You | S | Personal resume fields (city, phone, email, uni, grad date) |
| You | S | Read `application-packet/ESSAY-PART-II.md` + claim ledger; mark edits |
| Agent (on go) | S | README 5-minute mentor path polish |
| Agent (on go) | P | Scaffold `riscv-param-extraction/challenge/` (layout + README stub) |

#### Sun 27 Jul

| Block | S/P | Task |
|-------|-----|------|
| Agent (on go) | P | Challenge: snippets + prompts v1–v3 + validate skeleton + bad fixtures |
| Agent (on go) | P | CI: export unit tests + challenge validate |
| You / Agent | S | Dual-new-9 review-queue draft (offline) |
| You | S | Export resume → **1-page PDF** → re-upload LFX profile |

#### Mon 28 Jul

| Block | S/P | Task |
|-------|-----|------|
| Agent (on go) | P | Challenge multi-model **snippet-only** runs (low $; only with key + go) |
| Agent (on go) | S | `docs/REPRODUCE.md` one-command metric path |
| You | S | Final essay length fit for LFX form fields |
| You | S | Dry-run Apply form (fill, **do not submit** if still polishing) |

#### Tue 29 Jul

| Block | S/P | Task |
|-------|-----|------|
| You + Agent | S | 🔴 Red-team essay (attribution, metrics, schema-valid ≠ correct, v3 null) |
| You | S | Confirm every public GitHub link works signed-out |
| Agent (on go) | S/P | Push only if you type **push** |
| You | S | Optional: membership bump if &gt; ~1 week pending (logistics email only) |

#### Wed 30 Jul

| Block | S/P | Task |
|-------|-----|------|
| You | S | 🔴 Form fully filled; resume PDF final; prereqs checked |
| You | S | Sleep on it; only factual fixes |

#### Thu 31 Jul — **APPLY DAY**

| Block | S/P | Task |
|-------|-----|------|
| You | S | 🔴 **Submit Part II application** |
| You | S | 🔴 Screenshot status (Pending/Submitted) + date |
| You | S | Save final pasted answers locally |
| — | — | ⬜ No new experiments today |

### Phase 1 checklist (summary)

| # | Item | S/P | Status |
|---|------|-----|--------|
| 1 | Key rotated | S | [ ] |
| 2 | Resume PDF uploaded | S | [ ] |
| 3 | Essay final | S | [ ] |
| 4 | **Apply submitted** | S | [ ] |
| 5 | README mentor path | S | [ ] |
| 6 | Challenge pack scaffold | P | [ ] |
| 7 | CI green | P | [ ] |
| 8 | Dual-new review queue doc | S | [ ] |
| 9 | Push spear to `main` (optional) | — | only on **push** |

---

## PHASE 2 — Internal buffer (Aug 1–2)

**Allowed:** fix broken links, factual errors, resume, form prereqs, submit if missed Jul 31.  
**Forbidden:** full rewrite, new corpus runs, second repo, bulk UDB PR.

| Date | Task |
|------|------|
| **Aug 1** | If not applied: submit today. If applied: only link/prereq fixes. |
| **Aug 2** | 🔴 **Internal hard stop** — application must be in. |

---

## PHASE 3 — Emergency only (Aug 3–5)

| Date | Task |
|------|------|
| Aug 3–4 | Official deadline buffer only |
| **Aug 5** | 🔴 Official last day (reconfirm on dashboard) |
| Any day | If form/deadline broken → LFX/RVI support, not new features |

---

## PHASE 4 — Post-apply spear + community (Aug 6 – Sep 14)

Spine status: **applied**. Now free to gap competitors harder.

### Week of Aug 6–12

| S/P | Task |
|-----|------|
| P | Finish challenge pack results + README “snippet vs corpus” table |
| P | Robustness: markup-aware grounding + hard negatives |
| P | Full-manual scale/cost doc (offline measure + list prices) |
| S | Membership follow-up; join **sig-parameters** + **sig-unifieddb** when approved |
| S | Read recent list archives before posting |

### Week of Aug 13–19

| S/P | Task |
|-----|------|
| S | Short list note: monorepo link + 5 bullets (remeasure, A, B, v3 null, export question) |
| P/S | Optional **stratified** multi-model (15–25 chunks) — **spend go required** |
| U | Optional **one** smart UDB PR/issue (param-adjacent quality) — not PR race vs AlgoArtist06 |

### Week of Aug 20–26

| S/P | Task |
|-----|------|
| S | Optional Artifact **C** (CSR-context), pre-registered + leakage audit — spend go |
| S | Interview walkthrough rehearsal (60s / 5 min / 15 min) |
| S | Attend SIG/calendar meetings (listen) |

### Week of Aug 27 – Sep 14

| S/P | Task |
|-----|------|
| S | Polish public surface from any new metrics |
| S | Week-0 kickoff notes ready if selected |
| — | No bulk unsolicited param dump |

---

## PHASE 5 — Term (if selected) · Sep 15 – Nov 15

Full detail: [application-packet/NINE-WEEK-PLAN.md](./application-packet/NINE-WEEK-PLAN.md)

| Window | Focus | Objs |
|--------|--------|------|
| **Week 0** (pre-start) | Kickoff contract, golds, success criteria | 1,5 |
| **Sep 15–21** | Pinned reproduction | 1,3 |
| **Sep 22–28** | Gold crosswalk + review protocol | 1,2 |
| **Sep 29–Oct 5** | Grounded WARL / C if mentors want | 1,2 |
| **Oct 6–12** | Extraction/classification candidate freeze | 1,2 |
| **Oct 13–19** | Workflow packaging, manifests, tests | 3 |
| **Oct 20–26** | Reviewed export → UDB YAML | 4 |
| **Oct 27–Nov 2** | Review queue + PR shaping | 4,5 |
| **Nov 3–9** | Small upstream PR(s) + review | 5 |
| **Nov 10–15** | Merge follow-up + handoff | 5 |

---

## Milestone map

| Milestone | Date | Definition of done |
|-----------|------|--------------------|
| M0 Hygiene | Jul 26 | Key rotated; LFX status known |
| M1 Public spear MVP | Jul 28–30 | Challenge scaffold + CI local/PR |
| **M2 Apply** | **Jul 31** | Part II **submitted** |
| M3 Hard stop | Aug 2 | App in no matter what |
| M4 Official close | Aug 5 | Dashboard confirmed |
| M5 Lists live | When membership OK | Joined params + unifieddb |
| M6 List signal | ~Aug 13–19 | One calm technical note |
| M7 Science optional | Aug 20–Sep | Stratified multi-model and/or C published |
| M8 Term start | Sep 15 | Kickoff with mentors |
| M9 Term end | Nov 15 | Reviewed PRs + handoff |

---

## Parallel tracks (who does what)

```text
YOU (must click / personal)
  key · LFX form · Apply · membership · calendar · lists · resume fields · screenshots

AGENT (on explicit go)
  README · challenge/ · CI · review-queue docs · metrics/manifests · optional paid runs

BOTH
  essay red-team · push decision · list note wording
```

---

## Spend timeline (API)

| Window | Allowed paid work |
|--------|-------------------|
| Pre-apply (→ Jul 31) | Snippet-only multi-model for challenge pack (optional, low $) |
| Pre-apply | **No** full 60-chunk re-run unless you explicitly reopen |
| Post-apply | Stratified multi-model; optional Artifact C |
| Term | Mentor-approved runs only |

---

## Risk triggers

| If this happens | Do this |
|-----------------|---------|
| Spear not done by Jul 29 | **Drop spear; submit Apply** |
| Membership still pending at Apply | **Apply anyway** |
| AlgoArtist06-style PR flood FOMO | Stick to ≤1 smart UDB action post-apply |
| Form asks for coding challenge | Point at monorepo `challenge/` (build ASAP) |
| Deadline changes on dashboard | Replan same week; trust UI over this file |

---

## Daily “what do I do today?” (cheat sheet)

| Today is… | Do this |
|-----------|---------|
| **Jul 26–27** | Hygiene + resume + essay + start spear scaffold |
| **Jul 28–29** | Red-team + form dry-run + finish CI/challenge if time |
| **Jul 30** | Final freeze |
| **Jul 31** | **SUBMIT** |
| **Aug 1–2** | Buffer / late submit only |
| **After apply** | Lists + spear depth + optional science |
| **Sep 15+** | Nine-week term plan |

---

## One line

**Through July 31: ship the application and only enough spear (challenge/CI) to not look weaker than kit applicants; after apply: outbuild them and show up on lists—without ever abandoning Spring-scale metrics, export, and honest science.**

---

*Update checkboxes as you complete items. Prefer this file + PLAN-SPINE-AND-SPEAR.md for sequencing.*
