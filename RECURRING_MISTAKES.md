# RECURRING_MISTAKES.md — do not repeat

Living lesson catalog for agents on this campaign repo. Read at session start; append when a failure mode is real.

Last updated: 2026-07-24

---

## Campaign / GitHub

| Mistake | Correct behavior |
|---------|------------------|
| Creating a **second** public repo named like the product (`riscv-param-extraction` standalone) | All public work stays in `titoatwork/lfx-firstanalysis` under `riscv-param-extraction/` |
| Treating “create public repo” in old docs as `gh repo create` | Mean **folder + commit inside monorepo** unless user names a new repo |
| Pushing personal strategy, Slack dumps, agent diaries | Push only mentor-auditable evidence (metrics, manifests, how-to-run, drafts, honest limits) |
| Pushing without explicit “push” | Never push by default |
| Empty UDB fork as portfolio | Avoid (Tier-C optics) |

---

## Metrics & claims

| Mistake | Correct behavior |
|---------|------------------|
| Claiming **97** named params | Measured **87** rows / **83** unique — recount before changing |
| Inventing pilot / A / B results | Only cite runs that exist on disk + manifests |
| “Pure gpt-4o full machine.adoc pilot” | **COMPLETE_WITH_MODEL_SPLIT** — 021 gpt-4o, 020 gpt-4o-mini; TPM 30k blocked large chunk |
| Claiming Part I authorship | Credit @ishaan-arora-1 / PRs #1765–#1832 |
| Quietly editing public metrics to look better | Remeasure, manifest, then update tables |

---

## Process / plan

| Mistake | Correct behavior |
|---------|------------------|
| Inventing a parallel roadmap | `PLAN-SOURCE-OF-TRUTH.md` + user plan; agent executes on go |
| Restarting Phase 1 immersion | Technical Phase 1 done; use `PHASE1-IMMERSION/` evidence |
| Re-piloting “to be sure” | Costs money; already complete unless user reopens |
| Treating LFX mentee **profile** as **Apply** | Profile OK; Apply is Phase 3 only |
| Leading with probability lectures | Execute Tier-A packet quality; user definition of “guarantee” is evidence density |

---

## API / money

| Mistake | Correct behavior |
|---------|------------------|
| Test API call before key + scope | Zero calls until user pastes key and scopes work |
| Default retries doubling spend | `--retries 0` for paid extract paths |
| Full gpt-4o corpus on ~$5 budget | Pilot proved TPM + cost risk; default A path is **gpt-4o-mini** (see `PHASE2-PLAN.md`) |
| Writing key to README / handoff / commit | Session env only; unset after |
| Auto re-spend on parse failure | Diagnose offline; ask before second paid attempt |

---

## Channels & identity

| Mistake | Correct behavior |
|---------|------------------|
| Technical design on mentorship Slack | Logistics only; technical → sig lists after membership |
| Cold mentor application spam | Forbidden |
| Using friend Gmail `asquare567@gmail.com` | Use `ibteshamulhaque01@gmail.com` / `titoatwork` only |
| Re-asking identity every chat | Load from locked files |

---

## Engineering quality

| Mistake | Correct behavior |
|---------|------------------|
| Generic AI-slop README / emoji portfolio | Domain voice; numbers first; honest limitations |
| Shipping workarounds that hide bugs | Fix root cause; no muted checks |
| Silent failures in export/extract | Manifests, non-zero exits, measured tables |

---

## How to append

When a review, CI, or session finds a durable failure mode: add one row under the right section with **Mistake → Correct behavior**. Do not wait for the user to ask.
