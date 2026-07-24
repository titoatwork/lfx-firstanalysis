# Phase 1 Immersion — Status

**Last updated:** 2026-07-23  
**Plan lock:** `PLAN-SOURCE-OF-TRUTH.md`  
**Full handoff:** `PHASE1-CLOSEOUT.md` (historical; pilot/community superseded by PROGRESS)  
**Leftovers:** `LEFTOVER-WORK.md`  
**Identity / emails:** see `PLAN-SOURCE-OF-TRUTH.md` only  
**Phase 2 code:** `riscv-param-extraction/` inside https://github.com/titoatwork/lfx-firstanalysis  

---

## Summary

| Track | Status |
|-------|--------|
| Technical immersion | **DONE** |
| Community immersion | **IN PROGRESS** |
| Pilot `machine.adoc` | **COMPLETE_WITH_MODEL_SPLIT** + public evidence |
| Phase 2 public scaffold | **DONE** |
| Phase 2 Artifact B | **DONE** (schema-valid drafts) |
| Phase 2 Artifact A | **NOT STARTED** (API) |
| User plan ownership | User designs; agent tracks/executes on go |

---

## Checklist

### Technical
| Item | Status |
|------|--------|
| Clone UDB | **DONE** → `riscv-unified-db\` |
| PR branches lfx-1765…1832 | **DONE** |
| Branch for work | `lfx-1832` |
| isa-manual submodule | **DONE** (74 adoc) |
| Deep study pack | **DONE** → `PHASE1-IMMERSION\` |
| Phase 1 GT reproduce | **DONE** (223 params) |
| Metrics remeasure | **DONE** (72.9% / 88.4%) |
| Pilot extract | **DONE (model split)** |
| Public prototype layout | **DONE** → `riscv-param-extraction\` |
| Artifact B exporter | **DONE** (83 named + 20 new) |

### Community
| Item | Status |
|------|--------|
| Individual membership + Schedule A | **SUBMITTED** (pending approval) |
| Kendall mapping email | **SENT** |
| Membership approved | pending |
| sig-parameters | blocked on membership |
| sig-unifieddb | blocked on membership |
| Full archives read | partial (RSS only) |
| SIG calendar | **USER TODO** |
| Slack logistics channel | **JOINED** (2026-07-22) |
| LFX mentee profile (not Apply) | **DONE** (2026-07-23) |

---

## User-measured numbers (do not invent)

- GT live: **223** params; match 100% / strong 91%  
- Part I v2 vs GT185: **72.9%** adj recall, **88.4%** class acc, WARL **50%**  
- vs GT223: **64.2%** adj recall  
- `named=yes`: **87** rows / **83** unique  
- Artifact B: **83/83** named + **20/20** new schema-valid  
- Pilot: **~$0.05** COMPLETE_WITH_MODEL_SPLIT  

---

## Remaining (see LEFTOVER-WORK.md)

1. User: calendar + membership → lists  
2. Technical: Artifact A (+ grounding/surface); optional B polish; C after A+B  
3. Phase 3: cover letter + Apply Jul 31–Aug 2  
4. Do not re-pilot / restart Phase 1 without user OK  

---

## Next session

1. Load **AGENTS.md** (Grok auto) + **HANDOFF-NEW-SESSION.md** kickoff  
2. Confirm state via **PROGRESS.md** + **LEFTOVER-WORK.md**; **wait for user’s plan**  
3. Single GitHub home = `titoatwork/lfx-firstanalysis`  
4. Artifact A plan when go: **PHASE2-PLAN.md**  

