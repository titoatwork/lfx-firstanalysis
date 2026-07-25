# AGENTS.md — Grok project entry (auto-loaded)

**Repo:** [titoatwork/lfx-firstanalysis](https://github.com/titoatwork/lfx-firstanalysis)  
**Role:** execution agent for LFX Part II prep (AI-assisted RISC-V param extraction).  
**User owns the plan.** Agent tracks state and executes only on go. Do not invent a parallel roadmap.

**Full agent law:** [`AGENT-RULES.md`](./AGENT-RULES.md).  
**Canonical handoff (wake still 26 Jul morning):** [`HANDOFF-2026-07-26-MORNING.md`](./HANDOFF-2026-07-26-MORNING.md)  
Also: `HANDSOFF.md`, `RECURRING_MISTAKES.md`, `.grok/rules/*`, `LEFTOVER-WORK.md`.

---

## Current work (2026-07-26 pre-sleep → wake same morning)

| Area | State |
|------|--------|
| Branch | **`main` / `origin/main` @ `58f91de`** (challenge + CI) |
| Doctrine | Erase Anshul · unbiased hostile · no fanfic |
| Phase 1 / pilot / A / B / v3 | **DONE** (null WARL on v3) |
| **Coding challenge + CI** | **DONE + pushed** |
| Live multi-model (`results/live/`) | **NOT done** |
| UDB PR | Draft only — not opened |
| Apply Part II | **NOT submitted** — **Jul 31** (not morning of 26) |
| Membership / lists | In progress |
| Agent next | Wait for: `GO LIVE MULTI-MODEL` · `GO OPEN UDB PR` · `GO ERASE ANSHUL` · `push` |

Live leftovers: **`LEFTOVER-WORK.md`**.  
**Do not** rebuild challenge/CI from zero. Grok sub ≠ extract API.

---

## Session start

1. Read **`HANDOFF-2026-07-26-MORNING.md`** → this → `AGENT-RULES.md` → `HANDSOFF.md` → `RECURRING_MISTAKES.md`.  
2. Confirm `PROGRESS.md` + `LEFTOVER-WORK.md` + `docs/metrics.md` + `git rev-parse HEAD` (disk > stale).  
3. Default: confirm state; wait for go.  
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
