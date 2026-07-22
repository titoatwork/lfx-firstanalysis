# Handoff — new chat session

**Date prepared:** 2026-07-22  
**Why:** Prior chat is heavy; all critical state is on disk + GitHub.  
**GitHub mirror:** https://github.com/titoatwork/lfx-firstanalysis  

---

## For the human (you)

### Before or at start of new chat
1. Optional but good: finish Slack, calendar, LFX mentee profile (not Apply).  
2. Note membership: pending / approved.  
3. If you have an API key, say provider only (`claude` / `gpt4o` / `gemini`) — do not paste the key.  
4. Paste the **kickoff prompt** in §3 below.

### Do not re-explain
- Full plan, friend email drama, PR philosophy, or Phase 1 research — agents must **read the files**.

---

## For the agent (load these first)

| # | File | Must |
|---|------|------|
| 1 | `AGENT-RULES.md` | All session rules |
| 2 | `PLAN-SOURCE-OF-TRUTH.md` | Locked plan |
| 3 | `PROGRESS.md` | Done vs left |
| 4 | `PHASE1-CLOSEOUT.md` | Phase 1 state + pilot |
| 5 | `GITHUB-PRESENTATION.md` | Public repo presentation |
| 6 | `PHASE1-IMMERSION/DEEP-STUDY-COMPLETE.md` | Technical context (skim as needed) |

**Local code:** `riscv-unified-db` on `lfx-1832` with `lfx-*` branches (gitignored from this docs repo).

**Do not:** re-clone UDB, re-fetch all PRs, re-scrape all issues, or invent a parallel plan.

---

## §3 — Kickoff prompt (copy into new chat)

```text
HANDOFF — new session. Workspace: Desktop\LFX-Mentorship\
GitHub docs: https://github.com/titoatwork/lfx-firstanalysis

READ IN ORDER (do not skip; do not invent process):
1. AGENT-RULES.md
2. PLAN-SOURCE-OF-TRUTH.md
3. PROGRESS.md
4. PHASE1-CLOSEOUT.md
5. GITHUB-PRESENTATION.md
Skim as needed: PHASE1-IMMERSION/DEEP-STUDY-COMPLETE.md

Role: execution only until I change instructions.
Quality: exceptional code, not generic/AI-slop; slow; multi-iterate.

State (fill brackets if wrong, else keep):
- membership: [pending]
- LFX mentee profile (not Apply): [no]
- Slack logistics channel: [no]
- calendar: [no]
- sig-parameters / sig-unifieddb: [blocked until membership]
- Phase 1 technical (clone, PRs, GT, metrics, deep study): DONE — do not restart
- pilot machine.adoc: not yet
- A / B: not yet
- API: [none]
- Public prototype GitHub: [titoatwork — repo not created yet]
- Analysis repo: titoatwork/lfx-firstanalysis (docs already pushed)

Continue highest-outcome next steps per locked plan only.
First technical priority when API available: pilot (pilot-RUNBOOK.md), then Phase 2 public repo + A then B.
```

---

## §4 — One-screen state for the agent

### Done
- Plan lock, agent rules, progress, presentation, closeout docs  
- Clone + Part I PR branches + isa-manual (local)  
- GT reproduce: **223** params  
- Metrics remeasure: **72.9% / 88.4% / WARL 50%**  
- Full immersion pack + deep study  
- Membership application submitted  
- Docs pushed to `lfx-firstanalysis`

### Not done
- Community: profile, Slack, calendar, list join after membership  
- Pilot extract  
- Public A/B prototype repo  
- Application packet  
- Any UDB PR (correct — not required pre-apply)

### Immediate next (priority order)
1. User community TODOs (parallel, non-blocking for pilot if API exists)  
2. Pilot `machine.adoc`  
3. Scaffold public prototype per GITHUB-PRESENTATION.md  
4. Artifact A → B  

---

## §5 — After handoff works

Update `PROGRESS.md` when pilot/A/B/membership flip.  
Push docs to `lfx-firstanalysis` when major docs change.

---

*End handoff package.*
