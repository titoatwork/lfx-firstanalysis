# Entire LFX Application Plan

**Candidate:** Ibteshamul Haque  
**Goal:** Get selected for LFX Fall 2026 (paid seat)  
**Last updated:** 2026-07-21  
**Workspace:** `Desktop\LFX-Mentorship\`

---

## 1. Target projects

| Priority | Project | Action |
|----------|---------|--------|
| **PRIMARY** | **AI-assisted extraction of architectural parameters from RISC-V specifications – Part II** | **Apply (must)** |
| Backup (optional) | CFI on Sargantana | Only if willing to do RTL and fully prepared |
| Backup (optional) | DFI on Sargantana | Same; harder cold-start |
| Skip | Women in Energy (unpaid) | Default skip |

**LFX Part II:**  
https://mentorship.lfx.linuxfoundation.org/project/22296947-cecb-4a8f-8bcb-4f34710e9f66  

**Repo:** https://github.com/riscv/riscv-unified-db  

**Mentors:** Allen Baum, Ajit Dingankar  

**Apply window:** 2026-07-15 → **2026-08-05**  

**Term (API):** 2026-09-15 → 2026-11-15 (~30 h/week)  

**Seats:** ~**1 paid** (RVI: first mentee paid; unpaid extras optional)  

**Max apps per term:** **3** — recommended: Part II only, or Part II + at most one RTL backup if serious.

---

## 2. Strategy in one paragraph

Compete as a **Tier-A** applicant: prove you understand **Spring baseline + official Fall goals 1–5**, ship **public pre-work**, submit a **project-specific essay**, show **faculty research ownership** (UM / COLIDE without confidential link), commit **≥30 h/week**. Do **not** compete on fork spam or generic “I love AI + RISC-V.” Contact past mentees for intel (already done); convert intel into better essay/pre-work, not name-dropping.

---

## 3. What “application package” means

| Piece | Required? | Where it lives | Source file |
|-------|-----------|----------------|-------------|
| LFX mentee **profile** | Yes | LFX platform | `lfx-riscv-param-extraction-prework/application/profile-introduction.md` |
| **Resume PDF** (1 page) | Yes | Upload to LFX | `RESUME-DRAFT.md` → export PDF |
| **Project application essay** | Yes | Apply form for Part II | `.../application/essay-part-ii.md` |
| **Public pre-work repo** | Strongly recommended | GitHub public | `lfx-riscv-param-extraction-prework/` |
| GitHub / LinkedIn links | Yes if form asks | Profile + resume | `github.com/titoatwork` |
| Prereqs (enrollment etc.) | If form lists them | Upload completely | Platform-dependent |
| Interview | Maybe | If shortlisted | `.../application/interview-cheatsheet.md` |

**Editable later:** mentee profile (My Account → Edit).  
**Treat as more final:** project Apply submission.

---

## 4. Content rules (locked)

| Rule | Detail |
|------|--------|
| Hours | Always **≥30 hours/week** for the term |
| CGPA | **Omit** on resume |
| COLIDE | Describe work; **no public repo link** if confidential/private |
| College name | Optional on resume; profile intro can say “4th-year CS undergrad” only |
| Spring UDB | Cite as **public trail you studied**, never as your authorship |
| Paper | “Manuscript in preparation” / FGCS target — never fake published |
| Tone | Specific, technical, human — no generic open-source love letter |

---

## 5. Understanding you must have before Apply

### Official Fall goals (Part II)

1. LLM extraction on **priv + unpriv** specs; recreate full lists using gold:  
   - (a) ISA Manual per-chapter YAML  
   - (b) Google Drive `keyword_matches`  
   - (c) **UDB YAML** (`spec/std/isa/param/`) — improve **recall**  
2. Extend **classification scheme** as needed  
3. **AI agents/skills** — reproducible runs, prompt/context management  
4. Export Manual-side tools → **UDB YAML** format  
5. **GitHub PR** of reviewed files + maintainer merge follow-up  

### Spring baseline (public)

- Pipeline: ground truth → taxonomy → CSR-safe chunking → extract → metrics → v2 prompts → spreadsheet → `[#param:]` tags  
- V2 metrics (approx., from public PRs): adjusted recall **~73%**, class acc **~88%**, **WARL ~50%**  
- Much of `param_extraction` still on **open PRs**, not fully on `main`  
- Study notes: `spring-baseline.md`, `DEEP-STUDY-AI-PART-II.md`

### What you would do if selected (4-week sketch)

| Week | Focus |
|------|--------|
| 1 | Reproduce eval, pin gold SHAs, error book |
| 2 | Quality (WARL, false “new”, taxonomy if needed) |
| 3 | Agents/skills + robustness |
| 4 | Schema-valid UDB YAML + small reviewed PRs |

Full: `notes/four-week-plan.md`

---

## 6. Step-by-step application execution

### Phase A — Study (before or during materials)

1. Read `fall-goals.md` + LFX project page  
2. Read `spring-baseline.md` + PRs #1765, #1791–#1793  
3. Clone UDB; open param schema + example YAMLs  
4. Run self-test in `TONIGHT-DEEP-STUDY.md`  
5. Optional: `COMPETITION-UDB-ANALYSIS.md` (context only)

### Phase B — Materials

6. Build **resume PDF** from `RESUME-DRAFT.md`  
7. Complete **LFX mentee profile** + paste introduction + upload resume  
8. Minimum **LinkedIn** (photo, headline, UM, GitHub)  
9. **Publish** `lfx-riscv-param-extraction-prework` as public GitHub repo  
10. Finalize **essay** with pre-work URL (`essay-part-ii.md`)

### Phase C — Submit

11. LFX → Part II → **Apply**  
12. Paste project-specific essay  
13. Complete **all prerequisites**  
14. Confirm **My Projects** status (Pending + complete is OK)  
15. Screenshot/save confirmation  

### Phase D — After submit

16. Check email daily (mentors / LFX)  
17. If Ankit/Ishaan reply → fold advice into pre-work or interview prep  
18. **One** outreach bump only after 5–7 days silence  
19. If shortlisted → `interview-cheatsheet.md`  
20. Do not spam UDB issues for fake activity  

---

## 7. Outreach plan (support, not substitute)

| Person | Channel | Status / plan |
|--------|---------|----------------|
| **Ankit** (Spring parallel track) | LinkedIn + email | Messaged — **wait** |
| **Ishaan** (Spring main phases) | Email sent; LinkedIn connect pending | **Wait**; do **not** withdraw connect |
| Mentors | Only if they open contact / after selection | No cold spam |

Outreach = intel. **Selection = pre-work + essay + fit.**

---

## 8. Competition reality (planning assumptions)

| Assumption | Value |
|------------|--------|
| Exact applicant count | Unknown |
| Paid seats | ~1 |
| Serious competitors | Likely tens, not hundreds prepared |
| July UDB fork spike | Many lookers; few Tier-A |
| Your edge | Spring literacy + public pre-work + research finish record |

---

## 9. What NOT to do

- Generic multi-project copy-paste essay  
- Apply last day with empty pre-work  
- CGPA flex / college shame narrative  
- COLIDE confidential link  
- “I will merge 200 new params in week 1”  
- Withdraw LinkedIn connect to “fix” note  
- Triple-message mentees  
- Full CFI/DFI app without RTL commitment  
- Hard collision: ignore ≥30h reality  

---

## 10. Timeline (execution)

| When | What |
|------|------|
| **Already done** | Strategy lock; deep research; pre-work pack written; Ankit/Ishaan outreach; COLIDE private decision |
| **Now → before 5 Aug** | Study internalization → resume → profile → publish pre-work → **Apply** |
| **Ideal** | Application in **well before 5 Aug** (not last day) |
| **Sep–Nov 2026** | If accepted: LFX primary free time (~60–70%); GATE maintenance |
| **If rejected** | GATE + papers + earlier HPX per `HANDOFF.md` |

---

## 11. File checklist (open these)

```text
Desktop\LFX-Mentorship\
  APPLICATION-PLAN.md              ← this file
  RESUME-DRAFT.md
  72H-CHECKLIST.md
  HANDOFF.md
  PROJECTS.md
  lfx-riscv-param-extraction-prework\
    INDEX.md
    README.md
    notes\fall-goals.md
    notes\spring-baseline.md
    notes\what-is-a-parameter.md
    notes\four-week-plan.md
    notes\TONIGHT-DEEP-STUDY.md
    notes\questions-for-mentors.md
    examples\01-03-*.md
    application\essay-part-ii.md
    application\profile-introduction.md
    application\interview-cheatsheet.md
```

---

## 12. Success definition

| Outcome | Meaning |
|---------|---------|
| **Win** | Accepted (+ paid track if offered) → execute Fall plan, graduate |
| **Strong attempt** | Complete app + public pre-work + informed essay before deadline |
| **Fail mode** | Incomplete prereqs, generic essay, no pre-work, last-day rush |

---

## 13. One-line plan

**Study Spring + UDB params → 1-page resume → LFX profile → public pre-work → Part II essay with link → Apply complete prereqs → wait on mentees/mentors → interview from cheatsheet if called.**

---

*End of application plan.*
