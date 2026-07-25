# AGENTS.md — Grok project entry (auto-loaded)

**Repo:** [titoatwork/lfx-firstanalysis](https://github.com/titoatwork/lfx-firstanalysis)  
**Role:** execution agent for LFX Part II prep (AI-assisted RISC-V param extraction).  
**User owns the plan.** Agent tracks state and executes only on go. Do not invent a parallel roadmap.

**Full agent law:** [`AGENT-RULES.md`](./AGENT-RULES.md) (read this — it is the detailed rules file).  
Also: `PLAN-SOURCE-OF-TRUTH.md`, `HANDSOFF.md`, `RECURRING_MISTAKES.md`, `.grok/rules/*`.

---

## Current work (2026-07-26)

| Area | State |
|------|--------|
| Branch | `application/packet-2026-07-26` (local) · `main`/`origin/main` at `499ee96` until user says push |
| Phase 1 technical | **DONE** — do not restart immersion |
| Pilot `machine.adoc` | **COMPLETE_WITH_MODEL_SPLIT** (~$0.05) — do not re-pilot without user OK |
| Artifact **B** (CSV → draft YAML) | **DONE** — 83 named + 20 new, schema-valid |
| Artifact **A** (multi-model, v2 prompt) | **DONE** — gpt-4o-mini 60/60; adj 32.2% vs Claude 72.9%; Jaccard 3.8%; ~$0.16 · **public on main** |
| Prompt v3 WARL ablation | **DONE — null for WARL** (adj 35.0%; WARL 8.3%) · public metrics §6 |
| Original Artifact C (CSR-field context) | **Deferred** until after apply (not run) |
| Apply Part II | **Packet drafted locally** (`application-packet/`) — user submits Jul 31–Aug 2 |
| Membership / lists | Submitted; lists blocked on approval |
| Next focus | Application review + submit; no new broad experiments |

Live leftovers: **`LEFTOVER-WORK.md`**. Done vs left: **`PROGRESS.md`**.  
Knowledge map (all doc stores, not just handoffs): **`.grok/rules/00-context-map.md`**.

---

## Session start (when user says start / continue)

1. Read this file → **`AGENT-RULES.md`** → **`HANDSOFF.md`** → **`RECURRING_MISTAKES.md`**.
2. Confirm state against `PROGRESS.md` + `LEFTOVER-WORK.md` + disk (`docs/metrics.md`, UDB results). Prefer **disk + metrics** over stale handoffs.
3. State the next concrete step **or wait** if the user has not given a plan/go.
4. Never push / never paid API / never second public repo without explicit user text.

---

## Hard constraints (summary)

| Rule | Detail |
|------|--------|
| **Single public home** | Only `titoatwork/lfx-firstanalysis`. Phase 2 code = `riscv-param-extraction/` **inside** this monorepo. Never `gh repo create` a second product repo. |
| **Never push** | Default: no `git push` without explicit user **push**. |
| **No unsolicited UDB PRs** | No big PRs to `riscv/riscv-unified-db` without list ask + user OK. |
| **No invented metrics** | Use measured tables only (`docs/metrics.md` + manifests). |
| **API spend** | Zero paid calls without user key **and** explicit scope. `--retries 0`. Keys: session env only; never commit / paste into docs. Prefer user sets key in shell (chat paste = rotate after). |
| **Pilot honesty** | Claim **model split** (gpt-4o + gpt-4o-mini), not pure gpt-4o full pilot. |
| **Named count** | **87** rows / **83** unique — never claim 97 without recount. |
| **Part I credit** | @ishaan-arora-1 / PRs #1765–#1832 — never claim as user authorship. |
| **LFX profile ≠ Apply** | Apply only Phase 3 after evidence preferred. |
| **Slack** | `#risc-v-mentorship-questions` = logistics only. Technical → lists after membership. |
| **Identity** | GitHub `titoatwork`. Lists: `ibteshamulhaque01@gmail.com`. **Never** use friend Gmail `asquare567@gmail.com`. |

Full tables: **`AGENT-RULES.md`**, `PLAN-SOURCE-OF-TRUTH.md`, `GITHUB-PRESENTATION.md`.

---

## Measured facts (do not invent)

```
GT live UDB:                 223 params; 100% any / 91% strong match
Part I v2 vs GT185:          adj recall 72.9%, class acc 88.4%, WARL 50%
Part I v2 vs live GT223:     adj recall 64.2%, class acc 88.6%, WARL 50%
parameters.csv named=yes:     87 rows / 83 unique
Artifact B:                  83/83 named + 20/20 schema-valid
Pilot spend:                 ~$0.05 COMPLETE_WITH_MODEL_SPLIT
Artifact A (v2, mini, 60/60): adj 32.2% vs Claude 72.9%; WARL 12.5%; Jaccard 3.8%;
                             high-conf new both models 9; ~$0.16
v3 WARL ablation (mini):     COMPLETE null: adj 35.0%; WARL 8.3% (2/24) — worse WARL than A
```

Public tables: `riscv-param-extraction/docs/metrics.md`  
Pilot manifest: `riscv-param-extraction/manifests/pilot-machine-adoc.md`  
Artifact A manifest: `riscv-param-extraction/manifests/artifact-a-gpt-4o-mini.md`

---

## What to load (task → files)

| Task | Read (in order) |
|------|-----------------|
| **Any new session** | `AGENTS.md` → **`AGENT-RULES.md`** → `HANDSOFF.md` → `RECURRING_MISTAKES.md` → `PROGRESS.md` → `LEFTOVER-WORK.md` |
| **Full process law** | `AGENT-RULES.md` + `PLAN-SOURCE-OF-TRUTH.md` |
| **Kickoff paste** | `HANDOFF-NEW-SESSION.md` (may lag; prefer PROGRESS) · short: `NEXT-SESSION-PROMPT.md` |
| **Phase 2 / A** | `PHASE2-PLAN.md` (historical A path) + `docs/metrics.md` §5 |
| **Stretch C / v3** | Local UDB `prompts/v3/` + `results/v3/` — document only after complete run |
| **Public presentation** | `GITHUB-PRESENTATION.md` + root `README.md` + `riscv-param-extraction/README.md` |
| **Export / B code** | `riscv-param-extraction/AGENTS.md` + `docs/design.md` |
| **Phase 1 evidence** | `PHASE1-IMMERSION/` (do not re-scrape from zero) |
| **Deep study** | `PHASE1-IMMERSION/DEEP-STUDY-COMPLETE.md` only if needed |
| **Apply packet** | `Prompt.md` STEP 7–8, `lfx-riscv-param-extraction-prework/application/`, `RESUME-DRAFT.md` |
| **Year strategy** | `HANDOFF.md`, `PROJECTS.md` — only if user asks |

Full map: `.grok/rules/00-context-map.md`.

---

## Paths

| Path | Role |
|------|------|
| `riscv-param-extraction/` | Mentor-facing prototype (metrics, A, B, manifests) |
| `PHASE1-IMMERSION/` | Phase 1 evidence pack |
| `lfx-riscv-param-extraction-prework/` | Early apply notes / essay drafts |
| `riscv-unified-db/` | Local UDB clone only — **gitignored**, never push |
| Workspace | `Desktop\LFX-Mentorship\` |

---

## Quality

- Exceptional code; multi-iterate; domain voice (UDB / param / WARL / adjusted recall).
- Prefer reversible local work; small diffs; match existing style.
- Fix root causes; no workarounds that mute checks.
- When blocked: say so and wait — do not invent a bypass plan.
- Prefer **metrics.md + results JSON + PROGRESS** over stale handoff prose.

---

## Update this file when

- Branch / current objective changes  
- Artifact A / v3 / Apply status flips  
- A durable hard rule is added (also write `AGENT-RULES.md` / `HANDSOFF.md` / `RECURRING_MISTAKES.md`)

*Prefer quoting locked files over inventing process.*
