# PLAN — Source of Truth (until replaced)

**Status:** LOCKED for current work  
**Owner:** Ibteshamul Haque (tito / GitHub as confirmed separately — not friend accounts)  
**Last locked:** 2026-07-21 · **Rules companion:** `AGENT-RULES.md` · **New chat:** `HANDOFF-NEW-SESSION.md`  
**Replace only when user sends a new plan explicitly**

---

## Email / identity rules (hard)

| Rule | Detail |
|------|--------|
| **Do NOT use** | `asquare567@gmail.com` or any variant — **friend’s Gmail only**, ignore wherever it appears in pasted guides |
| **Membership / lists** | Use **user’s** roster email: `ibteshamulhaque01@gmail.com` (Individual membership Schedule A) |
| **Earlier list attempt** | `ibteshamul.123421@stu.upes.ac.in` (UPES) — map via Kendall; prefer Gmail after membership active |
| **GitHub** | User: work under **user’s** GitHub (`titoatwork` unless user renames). Treat “Asquare” in chat as **friend handle / noise** unless user confirms their own org/repo name |
| **Student employer form** | UPES, Dehradun (UM = June research attachment only) |

---

## The play

Stop being an applicant. Become a **contributor** before **Aug 5**.

**“Guarantee” definition (user):** make rejection irrational — sole (or clearest) applicant who:

1. Reproduced the pipeline  
2. Measured an improvement (or honest multi-model ablation)  
3. Showed up at the SIG  
4. Mapped a **9-week plan** to their **5 official objectives**

That is the max lever that exists. Execute for **Tier-A** packet quality. Do not lead sessions with probability lectures.

**Primary selection goal:**  
https://mentorship.lfx.linuxfoundation.org/project/22296947-cecb-4a8f-8bcb-4f34710e9f66  

**Repo:** https://github.com/riscv/riscv-unified-db  
**Mentors:** Allen Baum, Ajit Dingankar  

**Quality doctrine (user):** exceptional code — not generic / AI-slop; slow analysis; multiple iteration passes over code.

**GitHub presentation (locked):** `GITHUB-PRESENTATION.md` — how public work is shown; do not invent a different strategy.

---

## Phase 1 — Immersion (July 20–24)

- Join RISC-V as individual/community member (free).  
- Join **sig-parameters** list; read **all** archived messages (~50+).  
- Subscribe SIG calendar; attend next meeting (biweekly likely) — one-sentence intro only if asked; else listen.  
- RISC-V Slack **#risc-v-mentorship-questions** — **logistics only**, never technical.  
- Clone UDB + fetch Part I PR branches:

```bash
git clone https://github.com/riscv/riscv-unified-db && cd riscv-unified-db
for n in 1765 1766 1791 1792 1793 1831 1832; do
  git fetch origin pull/$n/head:lfx-$n
done
```

- Read order: issues **#1747 / #1751** (plans) → `taxonomy.md` → `extract.py` → `analyze.py`.  
- Read UDB CONTRIBUTING, param YAML schema, sample `spec/std/isa/param/*.yaml`. Skim isa-manual AsciiDoc layout.  
- **Reproduce Phase 1 ground truth** locally (pure Python, $0 API).  
- **Reproduce one extraction pilot** on `machine.adoc` (~cents).  

**Local progress (2026-07-21 session closeout):**
- Technical Phase 1 **DONE** except pilot (see `PHASE1-CLOSEOUT.md`).
- Membership submitted; list blocked on roster.
- Slack / calendar / LFX mentee profile: user TODO.
- Pilot: ready when API key available.
- **Next session entry:** `PHASE1-CLOSEOUT.md` then this file.

---

## Phase 2 — Prototype (July 24–31)

Own **public repo** (user’s GitHub). Two required artifacts:

| ID | Artifact | Maps to |
|----|----------|---------|
| **A** | **Multi-model run + agreement analysis** — exact Part I pipeline on **2nd model** (GPT/Gemini; full run ~$5–10). Deliver: per-class recall vs claude-sonnet-4, inter-model agreement, hallucination-overlap. Honest numbers if worse. | Obj 1 + unfinished multi-model |
| **B** | **UDB YAML exporter** — `parameters.csv` → draft `param/*.yaml` valid vs UDB JSON schema + tooling. Start with **already-named** params (verify count on current CSV; do not invent 97 if measured differs — use measured), then 10–20 new as drafts. | Obj 4 → 5 |
| **C stretch** | **WARL recall attack** — UDB CSR-field YAML as aux context; target NORM_CSR_WARL (~50%). Only if A+B done. | Obj 1–2 quality |

- **Run manifests** (model, version, seeds, tokens, cost) = Obj **3** demonstrated.  

**Etiquette:**
- Live in **user’s** repo.  
- Short summary + link to **sig-parameters** after A+B.  
- Optional one comment on relevant UDB issue.  
- **No unsolicited big PRs** — ask on-list if draft PR welcome.  
- Baum-quality: no sloppy eagerness.  

**Presentation details (repo layout, README order, manifests, non-goals):** see **`GITHUB-PRESENTATION.md`**.

---

## Phase 3 — Application (July 31 – Aug 2, not Aug 5)

**Cover letter weapon:**

1. One line: who + research (IoT IDS, on-device LLM, **Prof. Por Lip Yee**).  
2. “I reproduced Part I”: **3 lines with numbers YOU measured**.  
3. “I built X”: prototype links + comparison/export table.  
4. **9-week plan** 1:1 to their **5 objectives**, fortnight milestones, explicit metrics (e.g. adjusted recall 72.9%→85%+; WARL 50%→75%; N param files merged).  
5. Style: **30 h/wk** credible; **UTC+8** flexible for US-Pacific; honest ranges/limitations.  

**Resume:** 1 page; LLM/ISA-relevant; keywords: Generative AI, ISA specifications, Parameterized modeling; GitHub + pinned prototype. **No CGPA. No confidential COLIDE link.**  

**Mentor psychology:** Baum → reviewable artifacts, justification/provenance. Dingankar → metrics, baselines, ablations.  

**Parallel:** apply CFI/DFI with **separate** letters; Part II primary. LFX ~3 apps/term.

---

## Phase 4 — Aug 2 – Sep (warm)

- Keep SIG meetings, public prototype iteration, on-list replies.  
- Interview = walk through work they’ve already seen.  

---

## Official Part II objectives (map everything)

1. LLM extract priv+unpriv; gold (a) Manual chapter YAML (b) Drive keyword_matches (c) UDB YAML — improve recall  
2. Extend classification scheme  
3. AI agents/skills, reproducible workflows  
4. Export → UDB YAML  
5. Reviewed PR + merge follow-up  

---

## Join list — priority (from guide; emails = USER only)

### Tier 1 — project-critical

| Item | How |
|------|-----|
| **sig-parameters** | After membership: `sig-parameters+subscribe@lists.riscv.org` or https://lists.riscv.org/g/sig-parameters — from **user Gmail on roster** |
| **sig-unifieddb** | `sig-unifieddb+subscribe@lists.riscv.org` — https://lists.riscv.org/g/sig-unifieddb |
| **RISC-V Slack** | Official invite from riscv.org / plan invite; channel **#risc-v-mentorship-questions** logistics only |
| **LFX Mentorship account** | https://mentorship.lfx.linuxfoundation.org/ — LF account, profile + resume |
| **RISC-V membership** | Individual submitted; wait processing; Kendall map Gmail |

Jira context: Parameters SIG RVG-931.

### Tier 2 — backup mentorships (after Tier 1; Part II primary)

- sig-control-flow-integrity  
- sig-runtime-integrity  
- sig-ai-ml / sig-ml-ai-apps  

(Same `listname+subscribe@lists.riscv.org` pattern; membership required to post.)

### Tier 3 — optional soft signal

- Unofficial community Discords — optional only; not official RVI.  
- **Do not** treat friend Discord DMs as official channels.

### Contacts

- `mentorships@riscv.org` — program logistics  
- Mentors via **sig-parameters** (not cold spam)  
- Kendall Perez (`kendall@riscv.org`) — membership/list mapping only  

---

## Candidate INPUT (for letters / profile — user)

Name: tito / Ibteshamul Haque  

4th-year CS undergrad; architecture-adjacent systems; specs → implementations → reproducible eval under research mentorship.

Main research under **Prof. Por Lip Yee** at **Universiti Malaya** (June on-site attachment): IoT IDS pipeline — neural detection, C/C++ GPU inference, on-device air-gapped LLM for explainability. Manuscript prep (FGCS target). Degree home: **UPES**.

Habits/keywords for LFX: ISA/spec corpora; generative AI + structured outputs; reproducible evaluation; pipeline thinking; security/integrity mindset; Linux/Git/C++; mentor-facing delivery.

Applying where center of gravity is RISC-V param extraction and/or CFI/DFI-on-core; Part II primary.

---

## Related local paths

| Path | Role |
|------|------|
| `GITHUB-PRESENTATION.md` | **How work is presented on GitHub** (layout, README, stack, non-goals) |
| `HANDOFF-CONTRIBUTOR.md` | Agent handoff (aligned; this file supersedes for “current plan lock”) |
| `PHASE1-CLOSEOUT.md` | Phase 1 session bridge for next agents |
| `PHASE1-STATUS.md` | Phase 1 status board |
| `PHASE1-IMMERSION/` | Collected issues/PRs/metrics/deep study |
| `PHASE1-IMMERSION/DEEP-STUDY-COMPLETE.md` | Technical deep study |
| `riscv-unified-db/` | Clone, branch `lfx-1832`, local `lfx-*` PR branches |
| `APPLICATION-PLAN.md` | Package/tiers context (Tier-A); do not let older soft plans override Phase 2 A/B priority |
| `COMPETITION-UDB-ANALYSIS.md` | Tier A/B/C competition framing |

---

## Explicit non-goals for agent

- Using friend’s Gmail (`asquare567@gmail.com`) or friend’s accounts  
- Generic “how to apply” pep talks as main content  
- Probability disclaimer essays as main content  
- Unsolicited big UDB PRs  
- Technical discussion on mentorship Slack  
- Publishing confidential COLIDE  
- Spamming mentees/mentors  

---

## Kickoff prompt template

```text
EXECUTE PLAN-SOURCE-OF-TRUTH.md
Role: execution only until I change instructions.
Current phase: [1 / 2 / 3 / 4]
Status: membership=…; list=…; clone=…; pilot=…; A=…; B=…
Continue highest-outcome next steps per locked plan only.
```

**User does not need to restate identity rules each chat.** Agents must load this file and honor the Email / identity section (including never using the friend Gmail).

---

*End source of truth. Do not invent a parallel plan.*
