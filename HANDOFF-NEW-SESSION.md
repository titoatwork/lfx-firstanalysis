# HANDOFF — new session (canonical kickoff)

**Prepared:** 2026-07-23  
**Workspace:** `Desktop\LFX-Mentorship\`  
**Public monorepo (ONLY):** https://github.com/titoatwork/lfx-firstanalysis  

Paste the block under **KICKOFF PROMPT** into a new chat. Also open this file.  
**Do not invent a parallel plan.** Obey locked files.

---

## KICKOFF PROMPT (copy everything below this line)

```text
HANDOFF — new session. Workspace: Desktop\LFX-Mentorship\
GitHub (ONLY public home): https://github.com/titoatwork/lfx-firstanalysis

READ IN ORDER (do not skip; do not invent process):
1. AGENT-RULES.md
2. PLAN-SOURCE-OF-TRUTH.md
3. PROGRESS.md
4. PHASE1-STATUS.md
5. PHASE1-CLOSEOUT.md
6. GITHUB-PRESENTATION.md
Skim as needed: PHASE1-IMMERSION/DEEP-STUDY-COMPLETE.md
Public evidence: riscv-param-extraction/docs/metrics.md + manifests/pilot-machine-adoc.md

Role: execution only until I change instructions.
Quality: exceptional code, not generic/AI-slop; slow; multi-iterate; domain voice (UDB / param / WARL / adjusted recall).
Honesty: never invent metrics, merges, pilot/A results, or Part I authorship.

═══════════════════════════════════════
IDENTITY (do not re-ask; never use friend accounts)
═══════════════════════════════════════
- User: Ibteshamul Haque · GitHub: titoatwork
- Membership / lists email: ibteshamulhaque01@gmail.com
- Earlier list attempt: ibteshamul.123421@stu.upes.ac.in (UPES)
- NEVER use friend Gmail asquare567@gmail.com
- Student employer on RVI form: UPES, Dehradun
- UM: June research attachment only (Prof. Por Lip Yee) — not degree home
- Location: India (IST, UTC+5:30); flexible for US-Pacific meetings
- Primary LFX: Part II only (param extraction) unless user says otherwise
- Mentors: Allen Baum, Ajit Dingankar
- Project: https://mentorship.lfx.linuxfoundation.org/project/22296947-cecb-4a8f-8bcb-4f34710e9f66
- Upstream: https://github.com/riscv/riscv-unified-db

═══════════════════════════════════════
HARD RULES (violations = campaign risk)
═══════════════════════════════════════
1. Plan lock = PLAN-SOURCE-OF-TRUTH.md until user explicitly replaces it.
2. SINGLE public GitHub repo: titoatwork/lfx-firstanalysis.
   - Phase 2 code lives under riscv-param-extraction/ INSIDE this monorepo.
   - NEVER create a second public product repo (2026-07-22 mistake: riscv-param-extraction standalone — do not repeat).
   - If docs say “public repo / create repo” → mean folder + commit + push inside lfx-firstanalysis.
3. GitHub content policy (user):
   - PUSH only mentor-auditable evidence: metrics, manifests, how-to-run, draft code, honest limits.
   - DO NOT push personal notes, Slack dumps, competition strategy, agent diary, pep talks unless user explicitly orders that file.
   - Local-only: riscv-unified-db/ (gitignored), **/slack-notes.md, secrets, .env.
4. NEVER push without explicit user text (“push”). Prefer confirm if ambiguous.
5. NEVER open unsolicited big PRs to riscv/riscv-unified-db. Ask on-list first after A+B + membership.
6. Mentorship Slack #risc-v-mentorship-questions = LOGISTICS ONLY (deadlines/process). No technical design debate there.
7. Technical discussion → sig-parameters / sig-unifieddb AFTER membership roster maps (ibteshamulhaque01@gmail.com).
8. LFX mentee PROFILE ≠ project Apply. Apply only Phase 3 (plan: Jul 31–Aug 2) after A+B evidence preferred.
9. No cold email spam to mentors. No confidential COLIDE links. No CGPA on resume materials.
10. Do NOT restart Phase 1 technical immersion (no re-clone/re-fetch/re-scrape from zero).
11. API budget: treat OpenAI credits as scarce (~$5 historically). No paid calls without user key + explicit scope. No auto-retry loops. Never write keys to disk/git/README/chat echo if avoidable; session env only; unset after.
12. Named param count: measured ~87 rows / 83 unique — NEVER claim 97 without recount.
13. Pilot honesty: COMPLETE_WITH_MODEL_SPLIT — NOT “pure gpt-4o full machine.adoc pilot.”

═══════════════════════════════════════
STATE (fill brackets only if wrong; else keep)
═══════════════════════════════════════
- membership: [pending / submitted Schedule A]
- LFX mentee profile: [YES — completed 2026-07-23]
- Resume on mentee profile: [YES — uploaded 2026-07-23]
- Project Apply to Part II: [NO — not yet]
- Slack logistics channel: [YES — joined]
- calendar: [NO]
- sig-parameters / sig-unifieddb: [blocked until membership approved]
- Phase 1 technical (clone, PRs, GT, metrics, deep study): DONE
- Pilot machine.adoc: DONE — COMPLETE_WITH_MODEL_SPLIT (~$0.05 total)
  - chunk_021: gpt-4o-2024-11-20 — 10115 in + 1152 out, 6 params, ~$0.037
  - chunk_020: gpt-4o-mini-2024-07-18 — 44874 in + 1541 out, 9 params, ~$0.008
  - Why split: gpt-4o org TPM 30k blocked ~44k input on large chunk
  - Public: riscv-param-extraction/manifests/pilot-machine-adoc.md
- Artifact B: DONE — 83/83 named + 20/20 new schema-valid drafts in monorepo
- Artifact A multi-model: [NOT STARTED]
- Stretch C WARL: [NOT STARTED]
- Cover letter / formal Apply: [NOT STARTED]
- Public monorepo: titoatwork/lfx-firstanalysis (mentor evidence pushed; personal notes NOT pushed)
- Local UDB: riscv-unified-db/ branch lfx-1832 (not in git)
- Local extract.py note: gpt4o-mini alias + --chunk filter added for pilot completion (local UDB only; not upstream merge)

═══════════════════════════════════════
MEASURED FACTS (use these; do not invent)
═══════════════════════════════════════
Phase 1 GT (live UDB):     223 params; 100% any / 91% strong match
Part I v2 remeasure GT185: adjusted recall 72.9%, class acc 88.4%, WARL 50%
vs live GT223:             adjusted recall 64.2%, class acc 88.6%, WARL 50%
parameters.csv named=yes:   87 rows / 83 unique
Pilot total spend:         ~$0.05
Part I credit:             @ishaan-arora-1 / PRs #1765–#1832 — never claim as user’s authorship

═══════════════════════════════════════
OFFICIAL PART II OBJECTIVES (map work)
═══════════════════════════════════════
1. LLM extract priv+unpriv; improve recall vs gold
2. Extend classification scheme
3. AI agents/skills + reproducible workflows (manifests)
4. Export → UDB YAML
5. Reviewed PR + merge follow-up

═══════════════════════════════════════
WHAT IS DONE (do not redo)
═══════════════════════════════════════
- Plan lock, agent rules, immersion pack, deep study
- Clone UDB + lfx-1765…1832, GT regenerate, Part I metrics remeasure
- Artifact B exporter + drafts + tests + public metrics
- Pilot COMPLETE_WITH_MODEL_SPLIT + public pilot manifest
- Mentor-facing README / metrics surface on GitHub
- Membership form submitted; Slack joined; LFX profile + resume on profile
- Identity / presentation / “single repo” rules documented after 2026-07-22 incident

═══════════════════════════════════════
WHAT IS LEFT (priority order)
═══════════════════════════════════════
USER CLICKS / WAIT:
1. Membership approval email → join sig-parameters + sig-unifieddb from Gmail on roster
2. SIG/tech calendar subscribe; meetings: listen; one-sentence intro only if asked
3. Read list archives after join

TECHNICAL (highest selection gap):
1. Artifact A — multi-model run + agreement / hallucination-overlap vs claude-sonnet-4
   - Needs user API authorization + budget discipline
   - Honest numbers if worse
   - Manifest every run (Obj 3)
2. Optional offline B polish (enum/range domain fill) — not required for A
3. Stretch C WARL only if A+B done

PHASE 3 APPLY (plan Jul 31–Aug 2, not last day Aug 5):
1. Cover letter: who + research; measured Part I remeasure; A/B links; 9-week ↔ 5 objectives; 30 h/wk; IST
2. Resume refresh on profile if A ships new numbers
3. Apply to Part II only (unless user changes max-3 strategy)
4. Optional CFI/DFI only with separate letters

PHASE 4: SIG presence; iterate public repo; interview = walkthrough of visible work

═══════════════════════════════════════
GITHUB / PRESENTATION RULES
═══════════════════════════════════════
- Layout & README order: GITHUB-PRESENTATION.md
- Public path: riscv-param-extraction/ (metrics, manifests, export, drafts)
- Pass test: Baum can audit param draft provenance; Dingankar can recompute a metric
- No emoji walls, no “my journey,” no fake certainty
- Push: only on user order; only mentor-facing files; never UDB clone; never secrets

═══════════════════════════════════════
CHANNEL RULES
═══════════════════════════════════════
- Slack mentorship channel: logistics only
- Lists: technical after membership; calm contributor tone
- No cold mentor spam
- Kendall / info@riscv.org: membership/list mapping only
- mentorships@riscv.org: program logistics

═══════════════════════════════════════
COMPETITION / ETIQUETTE NOTES
═══════════════════════════════════════
- Competitor signal observed (e.g. hjaat gist / Slack technical Q): do not match with Slack essay spam. Win with measured public artifacts.
- Pre-apply UDB merges required: 0. No GSoC-style PR spam.
- Optional invited draft PR only after A+B + list OK.

═══════════════════════════════════════
THIS SESSION DEFAULT
═══════════════════════════════════════
Continue highest-outcome next steps per locked plan only.
Highest technical gap: Artifact A when user authorizes spend.
Otherwise: offline polish, status accuracy, Apply package drafting when user asks — no fake A numbers.
Community: guide user only; they click Slack/calendar/lists.
Do not restart Phase 1 technical study.
Do not re-run pilot unless user reopens scope.
Ask before any git push or paid API work.

Start: read AGENT-RULES + PLAN + PROGRESS, confirm state table above, propose next action and wait for my go.
```

---

## After the new chat starts

Agent should confirm:

1. Files loaded  
2. State table matches disk  
3. Next action (usually **Artifact A design/run** only if user authorizes API spend, or **Apply package** near Jul 31)

## Local-only reminders (not for GitHub)

- Personal notes / slack-notes stay local  
- Keys never committed  
- `riscv-unified-db/` never pushed  

## Related files

| File | Role |
|------|------|
| `AGENT-RULES.md` | Full session law |
| `PLAN-SOURCE-OF-TRUTH.md` | Plan lock |
| `PROGRESS.md` | Done vs left |
| `GITHUB-PRESENTATION.md` | Public presentation |
| `riscv-param-extraction/` | Mentor-facing prototype |

*End handoff. Prefer quoting these files over inventing process.*
