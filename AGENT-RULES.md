# Agent / session rules (read every new chat)

**Status:** LOCKED until user explicitly replaces  
**Owner:** Ibteshamul Haque  
**Last updated:** 2026-07-22  

Any new agent or chat session **must** load this file together with `PLAN-SOURCE-OF-TRUTH.md`. Do not reinvent process, etiquette, or presentation.

---

## 1. Role and goal

| Rule | Detail |
|------|--------|
| **Role** | Execution only until user changes instructions |
| **Primary goal** | Get selected for LFX Part II param extraction |
| **URL** | https://mentorship.lfx.linuxfoundation.org/project/22296947-cecb-4a8f-8bcb-4f34710e9f66 |
| **Mentors** | Allen Baum, Ajit Dingankar |
| **Upstream** | https://github.com/riscv/riscv-unified-db |
| **Play** | Stop being an applicant → become a **contributor** before Aug 5 |
| **“Guarantee” definition (user)** | Make rejection irrational: reproduce pipeline, measure improvement/multi-model, SIG presence, 9-week plan mapped to 5 official objectives |
| **Do not lead with** | Probability lectures / “no 100% chance” as main content |
| **Competition tier** | **Tier-A** behavior (not fork spam / generic essay) |

---

## 2. Source-of-truth files (load order)

| Order | File | Purpose |
|-------|------|---------|
| 1 | **AGENT-RULES.md** (this file) | Session rules — do not hallucinate process |
| 2 | **PLAN-SOURCE-OF-TRUTH.md** | Full plan (phases, join tiers, INPUT, non-goals) |
| 3 | **PROGRESS.md** | Done vs left checklist |
| 4 | **PHASE1-CLOSEOUT.md** | Phase 1 technical closeout + pilot/community leftovers |
| 5 | **GITHUB-PRESENTATION.md** | How work is shown on GitHub |
| 6 | **PHASE1-IMMERSION/DEEP-STUDY-COMPLETE.md** | Technical deep study (do not re-scrape from zero) |
| 7 | **NEXT-SESSION-PROMPT.md** / **HANDOFF-NEW-SESSION.md** | Kickoff templates |

**Repo on GitHub (SINGLE home — Phase 1 docs + Phase 2 code):** https://github.com/titoatwork/lfx-firstanalysis  
**Phase 2 path in that repo:** `riscv-param-extraction/` (Artifact B from 2026-07-22)  
**Local workspace:** `Desktop\LFX-Mentorship\`  
**Local UDB (not in git):** `riscv-unified-db\` branch `lfx-1832`  

### HARD RULE — GitHub surface (2026-07-22 incident; do not repeat)

| Rule | Detail |
|------|--------|
| **Only public campaign repo** | `titoatwork/lfx-firstanalysis` |
| **Forbidden without explicit user text** | `gh repo create`, new org/repo under any name, second “prototype” GitHub product |
| **If docs say “public repo” / “create repo”** | Mean **folder + commit + push inside lfx-firstanalysis**, unless user names a *new* repo |
| **Before any create/push/delete on GitHub** | Confirm target repo URL with user if there is any ambiguity |
| **Why** | A wrong public repo splits the campaign story, confuses mentors, and can tank selection optics |

---

## 3. Identity (do not ask user to restate every chat)

| Rule | Detail |
|------|--------|
| **Membership / lists email** | `ibteshamulhaque01@gmail.com` |
| **Earlier list attempt** | `ibteshamul.123421@stu.upes.ac.in` (UPES) |
| **Friend Gmail** | Appears in some pasted guides — **never use**; do not nag user to repeat this |
| **GitHub (user)** | `titoatwork` (public prototype later; analysis repo = `lfx-firstanalysis`) |
| **Student employer on RVI form** | UPES, Dehradun |
| **UM** | June research **attachment** only (Prof. Por Lip Yee) — not degree home |

---

## 4. Quality doctrine (user — non-negotiable)

| Rule | Detail |
|------|--------|
| **Code quality** | Exceptional — not generic, not AI-slop |
| **Pace** | Slow when needed: research → design → implement → critique → rewrite (multiple passes) |
| **Domain voice** | UDB / param / WARL / adjusted recall vocabulary — not chatbot starter kits |
| **Evidence** | Manifests, measured tables, provenance; no silent failures |
| **Honesty** | Never invent metrics, merges, or pilot results |

---

## 5. Phase rules

### Phase 1 — Immersion
| Rule | Detail |
|------|--------|
| **Technical** | Treat as **COMPLETE** except pilot — **do not re-clone, re-fetch PRs, or restart deep study** |
| **Pilot** | `machine.adoc` via `extract.py pilot` — needs user API key; runbook: `PHASE1-IMMERSION/06-measured-local/pilot-RUNBOOK.md` |
| **Membership** | Individual submitted; wait approval |
| **Lists** | After approval: sig-parameters + sig-unifieddb from user Gmail |
| **Slack** | `#risc-v-mentorship-questions` — **logistics only**, never technical design |
| **Calendar** | Subscribe; meetings: listen; one-sentence intro only if asked |
| **LFX profile** | Mentee profile OK anytime — **NOT project Apply** |
| **Apply** | Phase 3 only (Jul 31–Aug 2) after A+B |

### Phase 2 — Prototype
| Rule | Detail |
|------|--------|
| **Home** | User’s **public** repo (presentation per `GITHUB-PRESENTATION.md`) |
| **A** | Multi-model run + agreement vs claude-sonnet-4; honest if worse |
| **B** | parameters.csv → draft param YAML + schema validation |
| **named=yes count** | Use **measured ~87** on current CSV; do not blindly claim 97 |
| **C** | WARL stretch **only if A+B done** |
| **Manifests** | Every serious run = Obj 3 |
| **List post** | After A+B + list access: short summary + link |
| **UDB PRs** | **No unsolicited big PRs**; ask on-list if draft welcome |

### Phase 3 — Application
| Rule | Detail |
|------|--------|
| **Cover letter** | Who + research; 3 lines measured Part I; A/B links; 9-week ↔ 5 objectives; 30 h/wk; UTC+8 |
| **Resume** | 1 page; no CGPA; no confidential COLIDE link |
| **Mentors** | Baum = precision/provenance; Dingankar = metrics/baselines/ablations |
| **Parallel apps** | CFI/DFI separate letters; Part II primary |

### Phase 4 — Warm
| Rule | Detail |
|------|--------|
| Keep SIG presence; iterate public work; interview = walkthrough of seen work |

---

## 6. PR / open-source competition rules

| Rule | Detail |
|------|--------|
| **Pre-apply UDB merges required** | **0** |
| **GSoC-style PR spam** | **Not** the strategy for this project |
| **Relevant invited draft PR** | Optional bonus after A+B + list OK |
| **If selected (Obj 5)** | Reviewed PR path with mentors — quality over count |
| **Credit Part I** | @ishaan-arora-1 / public PRs — never claim as user’s authorship |
| **Empty UDB fork as portfolio** | Avoid (Tier C) |

---

## 7. Channel rules

| Channel | Allowed |
|---------|---------|
| **Mentorship Slack** | Logistics only (deadlines, process) |
| **sig-parameters / sig-unifieddb** | Technical after membership; calm contributor tone |
| **Cold email mentors** | **No** application spam |
| **Kendall / info@riscv.org** | Membership/list mapping only |
| **mentorships@riscv.org** | Program logistics |

---

## 8. Content / privacy rules

| Rule | Detail |
|------|--------|
| **COLIDE** | Describe if needed; **no public confidential link** |
| **API keys** | Never commit; never paste into git; user says provider only |
| **Secrets** | No `.env` in repo |
| **Do not push** | Local `riscv-unified-db/` clone (gitignored) |

---

## 9. Measured facts (use these; do not invent)

```
GT regenerate (live UDB):     223 params; 100% any / 91% strong match
Part I v2 remeasure (GT185):  adjusted recall 72.9%, class acc 88.4%, WARL 50%
vs live GT223:                adjusted recall 64.2%, class acc 88.6%, WARL 50%
parameters.csv named=yes:      ~87
Local branches:               lfx-1765 … lfx-1832; work on lfx-1832
Analysis GitHub:              github.com/titoatwork/lfx-firstanalysis
```

---

## 10. What not to do (hallucination guardrails)

1. Do **not** invent a new roadmap that overrides the plan lock.  
2. Do **not** restart Phase 1 technical from zero.  
3. Do **not** invent pilot/A/B results without runs.  
4. Do **not** open big unsolicited UDB PRs.  
5. Do **not** put technical discussion on mentorship Slack.  
6. Do **not** treat LFX profile as Apply.  
7. Do **not** use friend accounts or re-prompt identity every turn.  
8. Do **not** ship generic AI-slop code or emoji README portfolios.  
9. Do **not** claim Part I / Spring work as the user’s.  
10. Do **not** push the nested UDB clone to GitHub.  

---

## 11. Official Part II objectives (map all work)

1. LLM extract priv+unpriv; improve recall vs gold (manual YAML / keyword_matches / UDB YAML)  
2. Extend classification scheme  
3. AI agents/skills + reproducible workflows (manifests)  
4. Export → UDB YAML  
5. Reviewed PR + merge follow-up  

---

## 12. When user says “start” / next work order

1. Read this file + plan lock + PROGRESS.md  
2. If API ready → pilot  
3. Then public prototype repo per GITHUB-PRESENTATION.md  
4. Then A → B → manifests  
5. Community: only guide user; they click Slack/calendar/lists  
6. Application only after A+B evidence  

---

*End agent rules. Prefer quoting these files over inventing process.*
