# HANDSOFF.md — hard no-touch (Grok: read every session)

Obey absolutely. If a task requires touching something listed here, **stop and ask**.

Last updated: 2026-07-24

---

## Never without explicit user text

| Target | Why |
|--------|-----|
| `git push` / force-push / tags to any remote | User alone ships |
| `gh repo create` / second public product repo | 2026-07-22 incident; single home = `lfx-firstanalysis` |
| Unsolicited big PRs to `riscv/riscv-unified-db` | Wrong pre-apply strategy; list ask first after A+B |
| Paid OpenAI/API calls (any model) | Budget scarce; need key + scoped go-ahead |
| Re-run pilot `machine.adoc` / `extract.py pilot` | Already COMPLETE_WITH_MODEL_SPLIT |
| Full `extract.py run` / Artifact A corpus | Only after A plan + spend go-ahead |
| Commit / paste API keys, `.env`, secrets | Security |
| Push nested `riscv-unified-db/` | Large local clone; gitignored on purpose |
| Rewrite `PLAN-SOURCE-OF-TRUTH.md` as a new plan | Locked until user explicitly replaces |
| LFX **Apply** to Part II (agent cannot apply for user) | User clicks; Phase 3 only |
| Cold email spam to mentors Baum / Dingankar | Forbidden channel |
| Technical design debate on mentorship Slack | Logistics only |

---

## Do not redo (finished technical work)

- Phase 1 immersion from zero (re-clone, re-fetch all PR dumps, re-scrape issues, invent metrics)
- Artifact B core exporter + 83/83 + 20/20 schema-valid drafts (optional polish only if asked)
- Claiming Part I / Spring work as this user’s authorship
- “Create public prototype repo” as a **new** GitHub repo (use monorepo path instead)

---

## Paths / files — treat as protected

| Path | Rule |
|------|------|
| `riscv-unified-db/` | Local only; never add to this repo’s remote |
| `.env`, `.env.*`, `**/secrets*`, `*.pem` | Never commit |
| `**/slack-notes.md`, `**/private/`, `**/*-PRIVATE.md` | Local / personal — do not push |
| Mentor-facing numbers in `riscv-param-extraction/docs/metrics.md` | Do not “improve” without a real remeasure |
| `LIVE-VERIFY-2026-07-20.md` | Historical snapshot; do not present as current pilot |

---

## Identity — never substitute

- Do **not** use friend Gmail `asquare567@gmail.com` for lists/membership/docs.
- Prefer roster Gmail `ibteshamulhaque01@gmail.com` and GitHub `titoatwork`.
- Do not re-prompt the user to restate identity every turn (see `AGENT-RULES.md`).

---

## When in doubt

1. Leave untracked / local.
2. Ask before GitHub surface, spend, or upstream contact.
3. Log durable new no-touch items **here** in the same session.
