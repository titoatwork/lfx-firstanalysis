# HANDOFF — Contributor path (LFX Part II)

**For:** next session / agent  
**Owner:** Ibteshamul Haque  
**Role of agent until user changes it:** **EXECUTE this plan only** — highest outcomes, contributor-grade, not generic applicant coaching  
**User doctrine:** Stop being an applicant. Become a contributor before **Aug 5**.  
**“Guarantee” definition (user):** make rejection irrational — sole applicant who **reproduced pipeline, measured improvement, showed at SIG, mapped 9-week plan to their 5 objectives**.  
**Do not** lead with “no 100% chance” lectures.  
**Date of handoff:** 2026-07-21  

**Workspace:** `C:\Users\Ibteshamul Haque\Desktop\LFX-Mentorship\`  

**Plan lock (current work):** `PLAN-SOURCE-OF-TRUTH.md` — use that as source of truth until user replaces it (identity/emails included).  
**Phase 1 handoff:** `PHASE1-CLOSEOUT.md` — do not restart Phase 1 technical work.

---

## 1. Mission

| Item | Value |
|------|--------|
| **Primary project** | AI-assisted extraction of architectural parameters – **Part II** |
| **LFX** | https://mentorship.lfx.linuxfoundation.org/project/22296947-cecb-4a8f-8bcb-4f34710e9f66 |
| **ID** | `22296947-cecb-4a8f-8bcb-4f34710e9f66` |
| **Mentors** | **Allen Baum** (precision/spec/cert mindset), **Ajit Dingankar** (AI-for-V&V, metrics) |
| **Repo** | https://github.com/riscv/riscv-unified-db |
| **Apply** | through **2026-08-05** — **submit by Aug 2** (plan: Jul 31–Aug 2, not last day) |
| **Term** | ~Sep 15–Nov 15 API · **≥30 h/wk** |
| **Seats** | ~1 paid (RVI first mentee) |
| **Parallel apps** | CFI + DFI on Sargantana (tailored letters); **this project primary** |

**Official Part II objectives (map everything to these):**  
1) LLM extract priv+unpriv; gold (a) Manual chapter YAML (b) Drive keyword_matches (c) UDB YAML — improve recall  
2) Extend classification scheme  
3) AI agents/skills, reproducible workflows  
4) Export → UDB YAML  
5) Reviewed PR + merge follow-up  

---

## 2. User plan — four phases (SOURCE OF TRUTH)

### Phase 1 — Immersion (Jul 20–24)

- Join RISC-V individual/community member (**free**).  
- Join **sig-parameters** list; read **all archived messages** (~50+).  
- Subscribe SIG calendar; attend next meeting (biweekly likely) — one-sentence intro only if asked; else listen.  
- RISC-V Slack **#risc-v-mentorship-questions** — **logistics only**, never technical.  
- Clone UDB + fetch Part I PR branches:

```bash
git clone https://github.com/riscv/riscv-unified-db && cd riscv-unified-db
for n in 1765 1766 1791 1792 1793 1831 1832; do
  git fetch origin pull/$n/head:lfx-$n
done
```

- Read order: issues **#1747 / #1751** (plans) → `taxonomy.md` → `extract.py` → `analyze.py` (on PR branches).  
- Read UDB CONTRIBUTING, `param_schema`, sample `spec/std/isa/param/*.yaml`. Skim isa-manual AsciiDoc layout.  
- **Reproduce Phase 1 ground truth locally** (pure Python, $0 API).  
- **Reproduce one extraction pilot** on `machine.adoc` (~cents).  

### Phase 2 — Prototype (Jul 24–31)

Own **public repo**. Two required artifacts:

| ID | Artifact | Maps to |
|----|----------|---------|
| **A** | **Multi-model run + agreement analysis** — their pipeline on **2nd model** (GPT/Gemini; full run ~$5–10). Deliver: per-class recall vs claude-sonnet-4, inter-model agreement, hallucination-overlap. Honest numbers if worse. | Obj 1 + unfinished multi-model |
| **B** | **UDB YAML exporter** — `parameters.csv` → draft `param/*.yaml` valid vs UDB JSON schema + UDB tooling. Start **97 already-named** (verify vs existing YAML), then 10–20 new as drafts. | Obj 4 → 5 |
| **C stretch** | **WARL recall attack** — inject UDB CSR-field YAML as aux context; target NORM_CSR_WARL (~50%). Even +10 pp = headline. Only if A+B done. | Obj 1–2 quality |

- **Run manifests** (model, version, seeds, tokens, cost) = Obj **3** demonstrated.  
- **Etiquette:** live in **user’s** repo. Short summary + link to **sig-parameters** list. Optional one comment on relevant UDB issue. **No unsolicited big PRs** — ask on-list if draft PR welcome. Baum-quality: no sloppy eagerness.  

### Phase 3 — Application (Jul 31 – Aug 2)

**Cover letter weapon:**

1. One line: who + research (IoT IDS, on-device LLM, **Prof. Por Lip Yee**).  
2. “I reproduced Part I”: **3 lines with numbers YOU measured**.  
3. “I built X”: prototype links + comparison/export table.  
4. **9-week plan** 1:1 to their **5 objectives**, fortnight milestones, explicit metrics (e.g. adjusted recall 72.9%→85%+; WARL 50%→75%; N param files merged).  
5. Style: **30 h/wk** credible vs coursework; **UTC+8** flexible for US-Pacific; honest ranges/limitations.  

**Resume:** 1 page; lead LLM/ISA-relevant; keywords: Generative AI, ISA specifications, Parameterized modeling; GitHub + pinned prototype + research READMEs (arch, metrics, repro steps). **No CGPA. No confidential COLIDE link.**  

**Mentor psychology:** Baum → reviewable artifacts, justification/provenance. Dingankar → metrics, baselines, ablations.  

**Parallel:** apply CFI/DFI with **separate** letters; Part II primary.  

### Phase 4 — Aug 2 – Sep (warm)

- Keep SIG meetings, public prototype iteration, on-list replies.  
- Interview = walk through work they’ve already seen.  

---

## 3. Valuable prior context (compressed — do not re-dump)

### Candidate
- 4th-year CS undergrad; **UM** research with **Prof. Por Lip Yee** (on-site **June**); COLIDE-class IoT IDS + CUDA + on-device LLM; manuscript prep (FGCS target).  
- GitHub: `titoatwork` · COLIDE **private/confidential** — describe work, **no link**.  
- Capacity high; LFX Fall first; HPX ~Dec; GATE later.  

### Research facts agents already verified
- Spring Part I: **@ishaan-arora-1** phases #1747–#1832 / PRs #1765–#1832; parallel **@ankit-cybertron**.  
- Metrics (public PR writeups): V2 adjusted recall **~72.9%**, class acc **~88.4%**, WARL **~50%**; ~330 spreadsheet rows; tags ~321.  
- `param_extraction/` largely **not on main** — fetch **PR branches**.  
- UDB ~194★ / ~192 forks; July fork spike after LFX listing; competition proxies only (no public applicant count).  
- RVI: ~1 paid seat.  

### Outreach status
- **Ankit:** LinkedIn + email **sent** — wait (bump only 5–7d).  
- **Ishaan:** email **sent**; LinkedIn connect **pending** — **do not withdraw**; wait.  

### Existing local artifacts (reuse / upgrade, don’t restart from zero)
| Path | Use |
|------|-----|
| `lfx-riscv-param-extraction-prework/` | Seed notes/essay/examples — **upgrade into real A+B prototype repo** |
| `DEEP-STUDY-AI-PART-II.md` | Background only |
| `COMPETITION-UDB-ANALYSIS.md` | Context |
| `RESUME-DRAFT.md` | Seed for Phase 3 resume |
| `APPLICATION-PLAN.md` | **Superseded** by this contributor plan for execution priority |
| `HANDOFF.md` | Year-4 life context if needed |

---

## 4. Execution order for next agent (highest outcome)

Until Phase dates say otherwise, **default next work = Phase 1 immersion + local reproduce**, then Phase 2 A/B.

1. Confirm RISC-V membership + sig-parameters subscribe status with user.  
2. Clone UDB + fetch PR branches `lfx-1765` … `lfx-1832`.  
3. Locate `taxonomy.md`, `extract.py`, `analyze.py`, Phase 1 scripts on those branches.  
4. Reproduce Phase 1 ground truth ($0).  
5. Pilot extract on `machine.adoc` (cheap).  
6. Scaffold public prototype repo for **A** then **B**.  
7. Only then SIG post + application materials with **measured** numbers.  

**Etiquette hard rules:** no big unsolicited UDB PRs; list first; logistics-only on mentorship Slack; technical on SIG/repo.  

---

## 5. Cover letter / resume gates (Phase 3)

Do **not** submit application until:

- [ ] Part I reproduce done with **user-measured** numbers written  
- [ ] Artifact **A** and **B** public with READMEs + manifests  
- [ ] 9-week plan drafted against objectives 1–5  
- [ ] Resume 1-pager + cover letter as structured above  
- [ ] Target submit **Jul 31–Aug 2**  

---

## 6. Explicit non-goals for agent

- Generic “how to apply” pep talks  
- Probability disclaimers as main content  
- Replacing user’s phase plan with softer applicant plan  
- Publishing confidential COLIDE  
- Spamming mentees/mentors  

---

## 7. Kickoff prompt for next session

```text
EXECUTE HANDOFF-CONTRIBUTOR.md
Role: execution only until I change instructions.
Current phase: [1 Immersion / 2 Prototype / 3 Application / 4 Warm]
Status of membership, list, clone, PRs fetched, A, B:
[fill]
Continue highest-outcome next steps.
```

---

## 8. Success bar (user definition)

Rejection is irrational if the packet shows:

1. Reproduced Part I pipeline  
2. Measured multi-model (or clear improvement/ablation)  
3. SIG presence  
4. UDB YAML export path  
5. 9-week plan mapped to their 5 objectives  
6. Reviewable, Baum/Dingankar-grade artifacts  

---

*End handoff. Execute the plan above.*
