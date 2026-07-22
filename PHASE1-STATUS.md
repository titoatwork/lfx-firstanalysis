# Phase 1 Immersion — Status

**Last updated:** 2026-07-22  
**Plan lock:** `PLAN-SOURCE-OF-TRUTH.md`  
**Full handoff:** `PHASE1-CLOSEOUT.md`  
**Identity / emails:** see `PLAN-SOURCE-OF-TRUTH.md` only (do not re-prompt every session)  
**Phase 2 code:** `riscv-param-extraction/` inside https://github.com/titoatwork/lfx-firstanalysis (2026-07-22)

---

## Summary

| Track | Status |
|-------|--------|
| Technical immersion | **DONE** (except pilot) |
| Community immersion | **IN PROGRESS** |
| Pilot `machine.adoc` | **COMPLETE_WITH_MODEL_SPLIT**: 021=gpt-4o; 020=gpt-4o-mini (TPM workaround); ~$0.05 total |
| Phase 2 public scaffold | **DONE** locally |
| Phase 2 Artifact B | **DONE** offline (schema-valid drafts) |
| Phase 2 Artifact A | **NOT STARTED** (API) |

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
| Pilot extract | **DONE (model split)** — see pilot-manifest.md |
| Public prototype layout | **DONE** → `riscv-param-extraction\` |
| Artifact B exporter | **DONE** (83 named + 20 new, 103/103 schema-ok) |

### Community
| Item | Status |
|------|--------|
| Individual membership + Schedule A | **SUBMITTED** (wait ≤1 week) |
| Kendall mapping email | **SENT** |
| Membership approved | pending |
| sig-parameters | blocked on membership |
| sig-unifieddb | blocked on membership |
| Full archives read | partial (RSS only) |
| SIG calendar | **USER TODO** |
| Slack logistics channel | **JOINED** (2026-07-22) — `#risc-v-mentorship-questions` only; Allen Baum posted “see answer under risc-v-mentorship-questions” (paste full answer when available) |
| LFX mentee profile (not Apply) | **USER TODO** |

---

## User-measured numbers (do not invent)

- GT live: **223** params; match 100% / strong 91%  
- Part I v2 vs GT185: **72.9%** adj recall, **88.4%** class acc, WARL **50%**  
- vs GT223: **64.2%** adj recall  
- `named=yes` in parameters.csv: **87** rows / **83** unique (not uncritically “97”)  
- Artifact B: **83/83** named + **20/20** new schema-valid (local)

---

## Remaining Phase 1 “fully done” per plan text

1. User: calendar + Slack + LFX profile  
2. Wait: membership approve → join lists → read archives  
3. API: pilot on machine.adoc + save manifest  

Then complete Artifact A; push public repo when user approves.

---

## Next session priority

1. **Artifact A** only if user authorizes spend (most of ~$5 still left)  
2. User: community (lists after membership, calendar, LFX mentee profile ≠ Apply)  
3. Single GitHub home = `titoatwork/lfx-firstanalysis`  
4. Do not re-pilot without user OK  
5. Do not restart Phase 1 technical study  
