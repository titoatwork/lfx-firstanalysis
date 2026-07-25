# AGENTS.md — Grok project entry (auto-loaded)

**Repo:** [titoatwork/lfx-firstanalysis](https://github.com/titoatwork/lfx-firstanalysis)  
**Role:** execution agent for LFX Part II prep (AI-assisted RISC-V param extraction).  
**User owns the plan.** Agent tracks state and executes only on go. Do not invent a parallel roadmap.

**Full agent law:** [`AGENT-RULES.md`](./AGENT-RULES.md).  
**Canonical dated handoff:** [`HANDOFF-2026-07-26.md`](./HANDOFF-2026-07-26.md)  
Also: `HANDSOFF.md`, `RECURRING_MISTAKES.md`, `.grok/rules/*`, `PLAN-SPINE-AND-SPEAR.md`, `TIMELINE-SPINE-SPEAR.md`.

---

## Current work (2026-07-26 close)

| Area | State |
|------|--------|
| Branch | **`main` / `origin/main` @ `ca70796`** (packet + metrics pushed) |
| Doctrine | **Spine first, spear second** — see `PLAN-SPINE-AND-SPEAR.md` |
| Phase 1 technical | **DONE** |
| Pilot | **COMPLETE_WITH_MODEL_SPLIT** (~$0.05) |
| Artifact **B** | **DONE** — 83+20 schema-valid |
| Artifact **A** | **DONE** — mini 32.2% vs Claude 72.9%; Jaccard 3.8%; ~$0.16 |
| v3 WARL ablation | **DONE — null** (WARL 8.3%) |
| Original Artifact C | **Deferred** post-apply |
| Application packet | **On main** — `application-packet/` |
| Apply Part II | **NOT submitted** — target **Jul 31** (hard stop Aug 2) |
| Membership / lists | Submitted; lists blocked |
| Next | User: resume PDF + Apply · Agent: wait for go / apply polish / `GO SPINE+SPEAR phase1` |

Live leftovers: **`LEFTOVER-WORK.md`**. Progress: **`PROGRESS.md`**.  
**New chat:** paste kickoff from **`HANDOFF-2026-07-26.md`**.

---

## Session start

1. Read **`HANDOFF-2026-07-26.md`** if present, else this file → `AGENT-RULES.md` → `HANDSOFF.md` → `RECURRING_MISTAKES.md`.  
2. Confirm `PROGRESS.md` + `LEFTOVER-WORK.md` + `docs/metrics.md` (disk > stale handoffs).  
3. Default: help Apply path or wait for go. Spine wins over spear if time is short.  
4. Never push / paid API / second public repo without explicit user text.

---

## Hard constraints (summary)

| Rule | Detail |
|------|--------|
| **Single public home** | Only `titoatwork/lfx-firstanalysis` → `riscv-param-extraction/` |
| **Never push** | Without explicit **push** |
| **No bulk UDB dump PR** | Standing |
| **No invented metrics** | `docs/metrics.md` + manifests only |
| **API** | Key + scope; `--retries 0`; rotate if pasted in chat |
| **Pilot** | Model split, not pure gpt-4o |
| **Named count** | 87 rows / 83 unique — never 97 |
| **Part I credit** | @ishaan-arora-1 / PRs #1765–#1832 |
| **Identity** | `ibteshamulhaque01@gmail.com` · never `asquare567@gmail.com` |
| **Coding challenge** | Not official LFX requirement; spear pack optional |

---

## Measured facts (do not invent)

```
GT223: 100% any / 91% strong
Claude v2 GT185: 72.9% adj / 88.4% class / WARL 50%
vs GT223: 64.2% adj
B: 83/83 + 20/20 schema-valid · named 87/83
Pilot: ~$0.05 model-split
A mini: 32.2% adj / Jaccard 3.8% / WARL 12.5% / ~$0.16
v3: 35.0% adj / WARL 8.3% null / ~$0.16
```

---

## What to load

| Task | Files |
|------|--------|
| **New session** | `HANDOFF-2026-07-26.md` → this → rules → PROGRESS → LEFTOVER |
| **Apply** | `application-packet/*` + claim ledger |
| **Spear/challenge** | `PLAN-SPINE-AND-SPEAR.md` + timeline |
| **Metrics** | `riscv-param-extraction/docs/metrics.md` |
| **Competition** | `COMPETITION-REPORT-2026-07-26.md` (local) |

---

## Update this file when

Branch tip changes · Apply submitted · spear phase1 lands · C starts · durable new rule

*Prefer quoting locked files over inventing process.*
