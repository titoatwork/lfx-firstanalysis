# Progress — done vs left

**Last updated:** 2026-07-22  
**Plan lock:** [PLAN-SOURCE-OF-TRUTH.md](./PLAN-SOURCE-OF-TRUTH.md)  
**Phase 1 handoff:** [PHASE1-CLOSEOUT.md](./PHASE1-CLOSEOUT.md)  
**This GitHub repo:** https://github.com/titoatwork/lfx-firstanalysis  
**Local UDB clone (not in git):** `riscv-unified-db/` on branch `lfx-1832`

---

## Snapshot

| Area | State |
|------|--------|
| Study + reproduce + docs | **Done** |
| Community half of Phase 1 | **In progress** (you) |
| Pilot `machine.adoc` | **Next session** (API key) |
| Selection weapons A / B | **Not started** |
| Apply to Part II | **After A/B** (Jul 31–Aug 2) |

---

## Done so far

### Plan / docs (this repo)

| Item | Path |
|------|------|
| Plan locked | [PLAN-SOURCE-OF-TRUTH.md](./PLAN-SOURCE-OF-TRUTH.md) |
| Phase 1 closeout / next-session bridge | [PHASE1-CLOSEOUT.md](./PHASE1-CLOSEOUT.md) |
| Status board | [PHASE1-STATUS.md](./PHASE1-STATUS.md) |
| GitHub presentation rules | [GITHUB-PRESENTATION.md](./GITHUB-PRESENTATION.md) |
| Next kickoff prompt | [NEXT-SESSION-PROMPT.md](./NEXT-SESSION-PROMPT.md) |
| Deep study + evidence pack | [PHASE1-IMMERSION/](./PHASE1-IMMERSION/) |
| Pilot runbook | [PHASE1-IMMERSION/06-measured-local/pilot-RUNBOOK.md](./PHASE1-IMMERSION/06-measured-local/pilot-RUNBOOK.md) |
| Identity / emails | In plan lock only (user Gmail for membership/lists) |
| Pushed to GitHub | `titoatwork/lfx-firstanalysis` (`main`) |

### Phase 1 — technical

| Item | Status | Notes |
|------|--------|--------|
| Clone `riscv-unified-db` | **Done** (local) | Not pushed (too large; `.gitignore`) |
| Fetch PR branches `lfx-1765`…`lfx-1832` | **Done** (local) | Work branch: `lfx-1832` |
| isa-manual submodule | **Done** (local) | 74 `.adoc` files |
| Read plans/code (#1747–#1754, taxonomy, schema, pipeline) | **Done** | Pack on disk + [DEEP-STUDY-COMPLETE.md](./PHASE1-IMMERSION/DEEP-STUDY-COMPLETE.md) |
| Reproduce Phase 1 GT ($0) | **Done** | **223** params on current tree |
| Remeasure Part I v2 metrics | **Done** | **72.9%** adj recall, **88.4%** class acc, WARL **50%** |
| Membership form + Schedule A | **Submitted** | Waiting RVI processing |
| Kendall / list mapping path | **Documented** | Membership email: `ibteshamulhaque01@gmail.com` |

### Measured numbers (do not invent)

```
Phase 1 GT (live UDB):     223 params; 100% any / 91% strong spec match
Part I v2 vs GT185:        adjusted recall 72.9%, class acc 88.4%, WARL 50%
Part I v2 vs live GT223:   adjusted recall 64.2%, class acc 88.6%, WARL 50%
parameters.csv named=yes:   ~87 (verify before claiming 97)
```

Source: [PHASE1-IMMERSION/06-measured-local/metrics_summary.json](./PHASE1-IMMERSION/06-measured-local/metrics_summary.json)

### Phase 2 / 3 / 4

| Item | Status |
|------|--------|
| Public prototype repo (A/B home) | **Not started** (separate from this analysis repo) |
| Artifact A multi-model | **Not started** |
| Artifact B YAML exporter | **Not started** |
| Stretch C WARL | **Not started** |
| Application / cover letter / resume submit | **Not started** |
| SIG warm period | **Not started** |

---

## Left to do

### You (before / around next coding session)

| # | Task | Done? |
|---|------|-------|
| 1 | LFX **mentee profile** only (not Apply) | [ ] |
| 2 | Slack → `#risc-v-mentorship-questions` (logistics only) | [ ] |
| 3 | SIG/tech **calendar** | [ ] |
| 4 | Watch membership approval on **your** Gmail | [ ] |
| 5 | If approved: join **sig-parameters** + **sig-unifieddb** | [ ] |
| 6 | Read list archives (full after join) | [ ] |
| 7 | Optional: API key ready for pilot | [ ] |

### Next coding session(s)

| # | Task | Done? |
|---|------|-------|
| 1 | **Pilot** `machine.adoc` ([pilot-RUNBOOK.md](./PHASE1-IMMERSION/06-measured-local/pilot-RUNBOOK.md)) | [ ] |
| 2 | Public GitHub repo per [GITHUB-PRESENTATION.md](./GITHUB-PRESENTATION.md) | [ ] |
| 3 | **Artifact A** — multi-model + agreement tables | [ ] |
| 4 | **Artifact B** — CSV → draft UDB YAML + schema validate | [ ] |
| 5 | Manifests every run (Obj 3) | [ ] |
| 6 | Stretch **C** (WARL) only if A+B done | [ ] |
| 7 | Short **sig-parameters** note after A+B (when on list) | [ ] |
| 8 | **No** big unsolicited UDB PR (ask on-list first) | — |

### Phase 3 (Jul 31–Aug 2)

| # | Task | Done? |
|---|------|-------|
| 1 | Cover letter (measured numbers + A/B links + 9-week plan) | [ ] |
| 2 | 1-page resume | [ ] |
| 3 | **Apply** to Part II | [ ] |
| 4 | Optional parallel CFI/DFI apps (separate letters) | [ ] |

### Phase 4 (after apply)

| # | Task | Done? |
|---|------|-------|
| 1 | SIG meetings, iterate public repo | [ ] |
| 2 | Interview = walk through work already visible | [ ] |
| 3 | If selected: Obj 5 reviewed PR path with mentors | [ ] |

---

## Guarantee bar (selection packet)

| Requirement | Progress |
|-------------|----------|
| Reproduced pipeline | **Yes** |
| Measured multi-model / improvement | **No** (needs A) |
| Showed up at SIG | **No** (membership/list/meeting) |
| 9-week plan ↔ 5 objectives | **Not written** (Phase 3) |
| Reviewable A+B artifacts | **No** |

---

## Next chat

Paste [NEXT-SESSION-PROMPT.md](./NEXT-SESSION-PROMPT.md) with status brackets filled.

---

*Update this file when major checkboxes flip (pilot done, A done, membership approved, etc.).*
