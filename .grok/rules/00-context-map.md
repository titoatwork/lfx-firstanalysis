# Context map — what to load (token discipline)

Grok auto-loads `AGENTS.md` + this rules dir. **Do not** load every root `*.md` by default.

## Always on (already loaded or read first)

1. `AGENTS.md` — short ops + current work  
2. **`AGENT-RULES.md`** — **full agent law** (the detailed rules file)  
3. `HANDSOFF.md` — no-touch  
4. `RECURRING_MISTAKES.md` — known failure modes  
5. This file + sibling rules under `.grok/rules/`

## Default state files (read when starting real work)

| File | Why |
|------|-----|
| `PROGRESS.md` | Done vs left snapshot |
| `LEFTOVER-WORK.md` | **Canonical** live leftover list |
| `PHASE1-STATUS.md` | Short status board |

## Locked process (read when changing process or on full kickoff)

| File | Why |
|------|-----|
| **`AGENT-RULES.md`** | **Full agent rules / session law** — required |
| `PLAN-SOURCE-OF-TRUTH.md` | Plan lock |
| `GITHUB-PRESENTATION.md` | Public surface rules |
| `Prompt.md` | Master execution steps (A done; use for apply / stretch) |

## Other knowledge stores (not handoffs only)

| Store | Why |
|-------|-----|
| `riscv-param-extraction/docs/metrics.md` + `manifests/` | Mentor-facing measured truth |
| `PHASE1-IMMERSION/` | Issues, PRs, deep study, measured Phase 1 |
| `lfx-riscv-param-extraction-prework/` | Essay / profile / concept notes |
| Local `riscv-unified-db/param_extraction/` | Live extract results (v2/v3) — never push |
| `APPLICATION-PLAN.md`, `RESUME-DRAFT.md` | Apply phase |
| `COMPETITION-UDB-ANALYSIS.md` | Rival context (optional) |

## Kickoff templates

| File | Use |
|------|-----|
| `HANDOFF-NEW-SESSION.md` | **Canonical** long kickoff paste |
| `NEXT-SESSION-PROMPT.md` | Short pointer + short paste |
| `HANDOFF-NEXT-SESSION.md` | **Archived** pilot-budget handoff (pilot already done) |
| `HANDOFF-CONTRIBUTOR.md` | Older contributor path (pre-monorepo polish) |
| `HANDOFF.md` | Year/master plan (large) — only if user asks year strategy |

## Phase / tech

| File / path | Use |
|-------------|-----|
| `PHASE2-PLAN.md` | Artifact A execution plan |
| `PHASE1-CLOSEOUT.md` | Historical Phase 1 bridge |
| `LEFT-TODO.md` | Personal checklist mirror (prefer `LEFTOVER-WORK.md` for agents) |
| `riscv-param-extraction/` | Prototype code + public metrics |
| `PHASE1-IMMERSION/` | Evidence pack — do not re-scrape |
| `LIVE-VERIFY-2026-07-20.md` | Historical live-verify snapshot only |

## Usually skip unless user asks

| File | Reason |
|------|--------|
| `APPLICATION-PLAN.md`, `RESUME-DRAFT.md` | Apply-phase materials |
| `COMPETITION-UDB-ANALYSIS.md`, `SARGANTANA-ANALYSIS.md` | Side research |
| `STUDY-AI-PART-II.md`, `DEEP-STUDY-AI-PART-II.md` | Study essays |
| `PROJECTS.md`, `72H-CHECKLIST.md` | Broader LFX / early checklist |
| `lfx-riscv-param-extraction-prework/` | Older prework tree |

## Load budgets (guidance)

| Session type | Max intentional reads beyond auto-load |
|--------------|----------------------------------------|
| Status / “what’s left” | PROGRESS + LEFTOVER-WORK |
| Execute Artifact A | PHASE2-PLAN + riscv-param-extraction/* + pilot manifest |
| Export / B change | `riscv-param-extraction/AGENTS.md` + design.md + tests |
| Full new chat kickoff | HANDOFF-NEW-SESSION prompt + AGENT-RULES + PLAN |
