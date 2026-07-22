# Handoff — next session (pilot under $5 budget)

**Prepared:** 2026-07-22  
**Plan lock:** `PLAN-SOURCE-OF-TRUTH.md` + `AGENT-RULES.md`  
**Do not invent a parallel plan.**

Paste the block below as the next chat kickoff (or open this file first).

---

```text
EXECUTE PLAN-SOURCE-OF-TRUTH.md + AGENT-RULES.md. Do not invent a parallel plan.

## Role
Execution agent for LFX Mentorship Part II prep (AI-assisted RISC-V architectural parameter extraction).
- Quality: exceptional code, slow careful analysis, multi-iterate — no AI-slop.
- Prefer reversible local work.
- NEVER push to GitHub, NEVER open UDB PRs, NEVER commit secrets, unless I explicitly order that later.
- Do not restart finished Phase 1 technical immersion (no re-clone from zero, no re-fetch PRs if present, no re-scrape issues, no invent metrics).
- HARD: only public GitHub home is titoatwork/lfx-firstanalysis — never create a second campaign repo.

## Source of truth (read in order)
1. AGENT-RULES.md
2. PLAN-SOURCE-OF-TRUTH.md
3. GITHUB-PRESENTATION.md
4. PROGRESS.md + PHASE1-STATUS.md + PHASE1-CLOSEOUT.md
5. PHASE1-IMMERSION/06-measured-local/PILOT-READY.md  ← pilot gate
6. PHASE1-IMMERSION/06-measured-local/pilot-RUNBOOK.md
7. PHASE1-IMMERSION/06-measured-local/pilot-manifest.md
8. riscv-param-extraction/ (Artifact B — already built; in this repo)

## Identity
- GitHub: titoatwork
- Membership email: ibteshamulhaque01@gmail.com
- Never use friend Gmail asquare567@gmail.com

## ALREADY DONE (do not redo)
- Phase 1 technical except pilot: UDB lfx-1832, deep study, GT 223, Part I metrics
  72.9% adj recall / 88.4% class acc / WARL 50% vs GT185; 64.2% vs live GT223
- Artifact B in lfx-firstanalysis path riscv-param-extraction/:
  named 83/83 schema-ok; new 20/20; named=yes 87 rows / 83 unique (never claim 97)
- B already on GitHub under lfx-firstanalysis (2026-07-22) — not a second product repo
- Offline pilot setup COMPLETE: openai installed; PILOT-READY.md written; zero API spend so far
- Membership form submitted (wait approval)

## NOT done
1. Pilot machine.adoc (needs API key) — READY offline
2. Artifact A multi-model full/compare (needs API + my explicit yes after pilot)
3. Community clicks: LFX mentee profile ≠ Apply, Slack logistics, calendar, lists after membership
4. Phase 3 Apply Jul 31–Aug 2 after A+B evidence

## PRIMARY OBJECTIVE THIS SESSION
Run pilot with maximum care for money — or finish any remaining offline gate then ask for key.

### Budget law (HARD — ~$5 total OpenAI credits)
- Until I paste the key: ZERO API calls. No test call, no network probe.
- After key: ONE command only first:
  cd …/riscv-unified-db
  $env:OPENAI_API_KEY = "<key>"
  $env:PROMPT_VERSION = "v2"
  python param_extraction\scripts\extract.py pilot --model gpt4o --retries 0 -v
- Pilot = machine.adoc only = 2 chunks (chunk_020, chunk_021) = 2 API calls. Expected ~cents (~$0.10–0.30).
- Forbidden without my explicit yes: extract.py run, --force, re-pilot, multi-model full, Artifact A corpus.
- If spend path looks > ~$0.50 before pilot finishes: STOP and ask me.
- Never write key to disk/commits/README/chat echo. Session env only.
- --retries 0 required (default retries can double spend on parse fail).

### After pilot success
1. Fill pilot-manifest.md with REAL tokens/cost/paths
2. Update PROGRESS.md + PHASE1-STATUS.md
3. STOP. Show me cost. Do not start Artifact A unless I say so.

### On failure
Diagnose offline; no automatic re-spend; ask before second paid attempt.

## Secondary (only if blocked offline, or after pilot + my OK)
- Docs clarity, no fake A numbers
- User community click checklist only
- No git push unless I say push

## Explicit non-goals
- No unsolicited UDB PRs
- No invent metrics
- No second GitHub product repo
- LFX profile ≠ Apply

## Definition of done
A) Key given + pilot once + manifest + status + most of $5 left
OR B) If no key yet: confirm PILOT-READY still green + ask for key with single command

## Start
1. Read locked files + PILOT-READY.md
2. Confirm branch lfx-1832 + openai import + machine chunks
3. If setup green and I have not given key: report READY and ask for key with the single command
4. If I paste key: run pilot once only, then stop
```

---

## Human notes (not for agent paste)

| You should do | Why |
|---------------|-----|
| Delete archived mistake repo `riscv-param-extraction` if still on GitHub | Optics; real work is in lfx-firstanalysis |
| LFX mentee profile / Slack / calendar | Community half of Phase 1 |
| Watch membership approval → lists | sig-parameters / sig-unifieddb |
| Keep $5 for pilot + later A | Full A may need most of the budget |

**Do not paste API key into git or handoff files.**
