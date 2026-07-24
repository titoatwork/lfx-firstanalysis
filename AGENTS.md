# AGENTS.md — Grok project entry (auto-loaded)

**Repo:** [titoatwork/lfx-firstanalysis](https://github.com/titoatwork/lfx-firstanalysis)  
**Role:** execution agent for LFX Part II prep (AI-assisted RISC-V param extraction).  
**User owns the plan.** Agent tracks state and executes only on go. Do not invent a parallel roadmap.

Deeper law lives in `AGENT-RULES.md` + `PLAN-SOURCE-OF-TRUTH.md`. This file is the **short always-on** layer for Grok.

---

## Current work (2026-07-24)

| Area | State |
|------|--------|
| Branch | `main` (local may be ahead of `origin/main` after analysis merge) |
| Phase 1 technical | **DONE** — do not restart immersion |
| Pilot `machine.adoc` | **COMPLETE_WITH_MODEL_SPLIT** (~$0.05) — do not re-pilot without user OK |
| Artifact **B** (CSV → draft YAML) | **DONE** — 83 named + 20 new, schema-valid |
| Artifact **A** (multi-model) | **NOT STARTED** — needs user API + spend go-ahead |
| Stretch **C** WARL | Not started (only after A+B) |
| Apply Part II | Not started (plan Jul 31–Aug 2; deadline Aug 5) |
| Membership / lists | Submitted; lists blocked on approval |
| Next plan author | **User** |

Live leftovers: **`LEFTOVER-WORK.md`**. Done vs left: **`PROGRESS.md`**. Phase 2 A path: **`PHASE2-PLAN.md`**.

---

## Session start (when user says start / continue)

1. Read this file, then **`HANDSOFF.md`**, then **`RECURRING_MISTAKES.md`**.
2. Confirm state against `PROGRESS.md` + `LEFTOVER-WORK.md` (do not invent).
3. State the next concrete step **or wait** if the user has not given a plan/go.
4. Never push / never paid API / never second public repo without explicit user text.

---

## Hard constraints (summary)

| Rule | Detail |
|------|--------|
| **Single public home** | Only `titoatwork/lfx-firstanalysis`. Phase 2 code = `riscv-param-extraction/` **inside** this monorepo. Never `gh repo create` a second product repo. |
| **Never push** | Default: no `git push`. User alone ships. |
| **No unsolicited UDB PRs** | No big PRs to `riscv/riscv-unified-db` without list ask + user OK. |
| **No invented metrics** | Use measured tables only (see below / `docs/metrics.md`). |
| **API spend** | Zero paid calls without user key **and** explicit scope. No auto-retry spend loops. Keys: session env only; never commit / paste into docs. |
| **Pilot honesty** | Claim **model split** (gpt-4o + gpt-4o-mini), not pure gpt-4o full pilot. |
| **Named count** | **87** rows / **83** unique — never claim 97 without recount. |
| **Part I credit** | @ishaan-arora-1 / PRs #1765–#1832 — never claim as user authorship. |
| **LFX profile ≠ Apply** | Apply only Phase 3 after evidence preferred. |
| **Slack** | `#risc-v-mentorship-questions` = logistics only. Technical → lists after membership. |
| **Identity** | GitHub `titoatwork`. Lists: `ibteshamulhaque01@gmail.com`. **Never** use friend Gmail `asquare567@gmail.com`. |

Full tables: `AGENT-RULES.md`, `PLAN-SOURCE-OF-TRUTH.md`, `GITHUB-PRESENTATION.md`.

---

## Measured facts (do not invent)

```
GT live UDB:                 223 params; 100% any / 91% strong match
Part I v2 vs GT185:          adj recall 72.9%, class acc 88.4%, WARL 50%
Part I v2 vs live GT223:     adj recall 64.2%, class acc 88.6%, WARL 50%
parameters.csv named=yes:     87 rows / 83 unique
Artifact B:                  83/83 named + 20/20 new schema-valid
Pilot spend:                 ~$0.05 COMPLETE_WITH_MODEL_SPLIT
Artifact A:                  not run
```

Public tables: `riscv-param-extraction/docs/metrics.md`  
Pilot manifest: `riscv-param-extraction/manifests/pilot-machine-adoc.md`

---

## What to load (task → files)

| Task | Read (in order) |
|------|-----------------|
| **Any new session** | `AGENTS.md` → `HANDSOFF.md` → `RECURRING_MISTAKES.md` → `PROGRESS.md` → `LEFTOVER-WORK.md` |
| **Full process law** | `AGENT-RULES.md` + `PLAN-SOURCE-OF-TRUTH.md` |
| **Kickoff paste** | `HANDOFF-NEW-SESSION.md` (canonical) · short: `NEXT-SESSION-PROMPT.md` |
| **Phase 2 Artifact A** | `PHASE2-PLAN.md` + pilot constraints in `AGENT-RULES.md` |
| **Public presentation** | `GITHUB-PRESENTATION.md` + root `README.md` |
| **Export / B code** | `riscv-param-extraction/AGENTS.md` + `docs/design.md` |
| **Phase 1 evidence** | `PHASE1-IMMERSION/` (do not re-scrape from zero) |
| **Deep study** | `PHASE1-IMMERSION/DEEP-STUDY-COMPLETE.md` only if needed |
| **Historical / year plan** | `HANDOFF.md`, `PROJECTS.md` — **not** default session load |
| **Archived pilot-budget handoff** | `HANDOFF-NEXT-SESSION.md` — superseded by pilot complete |

Full map: `.grok/rules/00-context-map.md`.

---

## Paths

| Path | Role |
|------|------|
| `riscv-param-extraction/` | Mentor-facing prototype (metrics, B, pilot manifest) |
| `PHASE1-IMMERSION/` | Phase 1 evidence pack |
| `riscv-unified-db/` | Local UDB clone only — **gitignored**, never push |
| Workspace (this machine) | `…/2026_projects/lfx-firstanalysis` |

---

## Quality

- Exceptional code; multi-iterate; domain voice (UDB / param / WARL / adjusted recall).
- Prefer reversible local work; small diffs; match existing style.
- Fix root causes; no workarounds that mute checks.
- When blocked: say so and wait — do not invent a bypass plan.

---

## Update this file when

- Branch / current objective changes  
- Artifact A starts or finishes  
- Apply status flips  
- A durable hard rule is added (also write `HANDSOFF.md` / `RECURRING_MISTAKES.md`)

*Prefer quoting locked files over inventing process.*
