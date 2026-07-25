# HANDOFF — morning of 2026-07-26

**Wake calendar day: still 2026-07-26** (overnight work ended ~05:00 local; user sleeps then continues **same day**).  
**Do not** treat “next session” as July 27.

**Repo:** [titoatwork/lfx-firstanalysis](https://github.com/titoatwork/lfx-firstanalysis)  
**Public tip:** **`main` / `origin/main` @ `58f91de`**  
**Local workspace:** `Desktop\LFX-Mentorship\`  
**Local UDB (gitignored):** `riscv-unified-db/` @ **`lfx-1832`**

**Canonical short leftover list:** `LEFTOVER-WORK.md`  
**Progress:** `PROGRESS.md`  
**Agent entry:** `AGENTS.md`  
**Overmatch scoreboard:** `OVERMATCH-STATUS.md` (local; may be unpushed)  
**Metrics truth:** `riscv-param-extraction/docs/metrics.md`

Older `HANDOFF-2026-07-26.md` (session-close draft without challenge push) **lags** — prefer **this file**.

---

## Doctrine

```text
GOAL: Erase Anshul on every mentor-visible axis (not "tie challenge", not "#2 is fine")
SPINE  = GT remeasure, multi-model corpus, export, honest nulls, apply packet
SPEAR  = challenge pack + CI + live multi-model + small UDB PR
Apply target: 2026-07-31  |  hard stop: 2026-08-02  |  official ~2026-08-05
```

- Single public monorepo only. No second product repo. No bulk UDB dump.  
- Credit Spring: **@ishaan-arora-1** / PRs **#1765–#1832** (reproduce, not authorship).  
- Named: **87 rows / 83 unique** — never 97.  
- No invent metrics. Curated challenge results ≠ live multi-model.  
- Grok **subscription ≠** free Claude/OpenAI extract; multi-model needs **API keys / free tiers / Ollama**.  
- Agent posture: **unbiased hostile** — force improvement; no fanfic crowning.

---

## DONE (do not redo)

| Item | Facts |
|------|--------|
| Phase 1 immersion | Done |
| GT live | **223** · 100% any / 91% strong |
| Remeasure GT185 | adj **72.9%** · class **88.4%** · WARL **50%** |
| vs GT223 | adj **64.2%** |
| Pilot | COMPLETE_WITH_MODEL_SPLIT · ~$0.05 |
| Artifact A | mini **32.2%** vs Claude **72.9%** · Jaccard **3.8%** · dual-new **9** · ~$0.16 |
| Artifact B | **83/83** + **20/20** schema-valid (recount disk if audit; Grok listed 84/22 once) |
| v3 WARL | **null** (WARL **8.3%** worse) · ~$0.16 |
| Application packet | On main · `application-packet/` |
| **Coding challenge pack** | **Pushed** `58f91de` · `riscv-param-extraction/challenge/` |
| CI | `.github/workflows/ci.yml` + `challenge/scripts/ci_check.py` |
| UDB PR draft | `upstream-pr-drafts/fix-hpm-mcountinhibit-typo/` (not opened) |
| Multi-agent consult | Mostly biased/stale; **best external audit: Grok auditor prompt** (fix: Anshul **does** have UDB merges e.g. **#1967**) |

### Honesty (numbers)

- Spine metrics = measured / on disk.  
- Challenge `results/curated/` = **hand-grounded reference for CI**, not live Sonnet/Opus/GLM.  
- n=15 benchmark extractions = **constructed re-derive mechanics**, not LLM scores — do not sell as model recall.

---

## LEFT

### User (must)

| # | Task | When |
|---|------|------|
| 1 | Membership / Schedule A if not finished | **26 Jul** |
| 2 | Resume personal fields → PDF → LFX profile | **26–27** |
| 3 | Essay vs claim ledger | **27–30** |
| 4 | **Apply Part II** | target **Jul 31** (not “morning of 26”) · hard stop **Aug 2** |
| 5 | Membership → lists + calendar | Parallel |
| 6 | API keys in **shell only** (not chat) if live multi-model | Before multi-model go |

### Agent (only on explicit go)

| Phrase | Work |
|--------|------|
| `GO LIVE MULTI-MODEL` | Both challenge snippets → `results/live/<model>/` · validate · README table · needs key/free/local + spend cap |
| `GO OPEN UDB PR` | Open mcountinhibit typo fix from clean main |
| `GO SPINE apply` | Essay/resume polish only |
| `GO ERASE ANSHUL` | Max path: live multi-model + UDB PR + monorepo tighten |
| `push` | Ship local commits (validate trigger-WARN etc. may be unpushed) |

### Still Anshul leads

- Live multi-model result dirs on exact two snippets  
- Merged UDB PR (#1967 etc.)

### You lead

- Corpus GT / A / cost / Jaccard / dual-new  
- Bulk export 83+20  
- v3 null honesty  
- Challenge pack density offline (fixtures/negatives/CI matrix) — **public**

**Rank (honest):** ~**#3–#5** now · **#1–#2 fight** only after live multi-model + UDB PR + Apply.

---

## Local dirty (not necessarily on remote)

May exist unpushed after overnight session:

- `challenge/scripts/validate.py` (`--check-triggers` / `--strict-triggers`)  
- `AGENTS.md`, `LEFTOVER-WORK.md`, `OVERMATCH-STATUS.md`, plans/handoffs  

Push only on user **`push`**.

---

## Free vs paid multi-model

- **Best erase path:** Sonnet (or similar) **API** + gpt-4o-mini + free open-weight (Groq/Ollama).  
- **$0 path:** Gemini free / Groq / Ollama — weaker name optics, still valid if labeled.  
- Snippet-only cost: usually **cents–few $**.

---

## KICKOFF PROMPT (paste into next chat)

```text
HANDOFF — morning of 2026-07-26 (same calendar day; user slept after ~05:00 work).
NOT July 27. Apply is NOT due this morning — target Jul 31, hard stop Aug 2.

Workspace: Desktop\LFX-Mentorship\
GitHub ONLY: https://github.com/titoatwork/lfx-firstanalysis
Public tip: main @ 58f91de (challenge pack + CI pushed)
Local UDB gitignored: riscv-unified-db/ @ lfx-1832

READ FIRST (order):
1. HANDOFF-2026-07-26-MORNING.md  ← THIS handoff
2. AGENTS.md + AGENT-RULES.md + HANDSOFF.md + RECURRING_MISTAKES.md
3. LEFTOVER-WORK.md + PROGRESS.md
4. OVERMATCH-STATUS.md (if present)
5. riscv-param-extraction/docs/metrics.md
6. application-packet/MEASURED-CLAIM-LEDGER.md when writing claims
Skim: challenge/README.md

ROLE: execution agent. User owns plan. Unbiased hostile — force improvement; no fanfic.
GOAL: Erase Anshul on every mentor-visible axis (live multi-model + UDB ink + Apply still required).

DONE (do not redo): Phase1; pilot; A (32.2% vs Claude 72.9%, Jaccard 3.8%); B 83+20; v3 WARL null; application-packet on main; coding challenge pack + CI on main @ 58f91de; UDB PR draft (mcountinhibit) not opened.
NOT DONE: live multi-model under challenge/results/live/; open/merge UDB PR; Apply click; resume PDF fields; membership/lists as needed.
HONESTY: curated challenge results ≠ live LLM matrix; n=15 extractions are mechanics not model scores; Anshul HAS UDB merge #1967 (do not say neither has merges); named 87/83 never 97; credit @ishaan-arora-1 #1765–#1832.

GAP vs Anshul: CLOSED challenge/CI optics; STILL BEHIND live multi-model + merged UDB PR; AHEAD corpus GT/export/null.
Grok subscription ≠ extract API. Multi-model needs provider keys / free tier / Ollama.

HARD: no push without "push"; no paid API without key+scope+cap; --retries 0; no bulk UDB dump; no second public product repo; no invent metrics.

NOW:
- Confirm state from this handoff + LEFTOVER + metrics + git tip.
- Wait for user go: GO LIVE MULTI-MODEL | GO OPEN UDB PR | GO ERASE ANSHUL | GO SPINE apply | push
- Do not invent roadmap; do not rebuild challenge/CI from zero.
```

---

*End HANDOFF-2026-07-26-MORNING.*
