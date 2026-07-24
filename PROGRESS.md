# Progress — done vs left

**Last updated:** 2026-07-24 (agent context stack organized for Grok; A still open; user owns plan)  
**Plan lock:** [PLAN-SOURCE-OF-TRUTH.md](./PLAN-SOURCE-OF-TRUTH.md)  
**Grok entry:** [AGENTS.md](./AGENTS.md) · [HANDSOFF.md](./HANDSOFF.md) · [RECURRING_MISTAKES.md](./RECURRING_MISTAKES.md)  
**Session rules:** [AGENT-RULES.md](./AGENT-RULES.md)  
**New chat handoff:** [HANDOFF-NEW-SESSION.md](./HANDOFF-NEW-SESSION.md)  
**Leftover checklist:** [LEFTOVER-WORK.md](./LEFTOVER-WORK.md)  
**Phase 2 A plan:** [PHASE2-PLAN.md](./PHASE2-PLAN.md)  
**Context map:** [.grok/rules/00-context-map.md](./.grok/rules/00-context-map.md)  
**Phase 1 handoff:** [PHASE1-CLOSEOUT.md](./PHASE1-CLOSEOUT.md)  
**This GitHub repo (ONLY public home):** https://github.com/titoatwork/lfx-firstanalysis  
**Phase 2 code path (in this repo):** `riscv-param-extraction/` — first landed **2026-07-22**  
**Local UDB clone (not in git):** `riscv-unified-db/` on branch `lfx-1832`

---

## Snapshot

| Area | State |
|------|--------|
| Study + reproduce + docs | **Done** |
| Community half of Phase 1 | **In progress** (you) |
| Pilot `machine.adoc` | **COMPLETE_WITH_MODEL_SPLIT** (~$0.05) — public: `riscv-param-extraction/manifests/pilot-machine-adoc.md` + `docs/metrics.md` |
| Phase 2 folder in **lfx-firstanalysis** | **`riscv-param-extraction/`** (2026-07-22) |
| Selection weapon **B** | **Done offline** (83+20 schema-valid drafts) |
| Selection weapon **A** | **Done** (gpt-4o-mini 60/60; adj recall 32.2% vs Claude 72.9%; ~$0.16) |
| Grounding / provenance suite | **Not shipped** as public product |
| Stretch **C** WARL | **Not started** |
| Apply to Part II | **Not started** (plan Jul 31–Aug 2) |
| Next plan author | **User** (agent tracks done / executes on go) |

---

## Done so far

### Plan / docs (this repo)

| Item | Path |
|------|------|
| Plan locked | [PLAN-SOURCE-OF-TRUTH.md](./PLAN-SOURCE-OF-TRUTH.md) |
| Phase 1 closeout | [PHASE1-CLOSEOUT.md](./PHASE1-CLOSEOUT.md) |
| Status board | [PHASE1-STATUS.md](./PHASE1-STATUS.md) |
| Leftover list | [LEFTOVER-WORK.md](./LEFTOVER-WORK.md) |
| GitHub presentation rules | [GITHUB-PRESENTATION.md](./GITHUB-PRESENTATION.md) |
| New-session handoff | [HANDOFF-NEW-SESSION.md](./HANDOFF-NEW-SESSION.md) |
| Deep study + evidence pack | [PHASE1-IMMERSION/](./PHASE1-IMMERSION/) |
| Pushed to GitHub | `titoatwork/lfx-firstanalysis` (`main`) — mentor-facing only |

### Phase 1 — technical

| Item | Status | Notes |
|------|--------|--------|
| Clone `riscv-unified-db` | **Done** (local) | Not pushed (`.gitignore`) |
| Fetch PR branches `lfx-1765`…`lfx-1832` | **Done** (local) | Work branch: `lfx-1832` |
| isa-manual submodule | **Done** (local) | 74 `.adoc` files |
| Read plans/code | **Done** | [DEEP-STUDY-COMPLETE.md](./PHASE1-IMMERSION/DEEP-STUDY-COMPLETE.md) |
| Reproduce Phase 1 GT ($0) | **Done** | **223** params |
| Remeasure Part I v2 metrics | **Done** | **72.9%** adj recall, **88.4%** class, WARL **50%** |
| Pilot `machine.adoc` | **Done** | COMPLETE_WITH_MODEL_SPLIT; OpenAI path verified |
| Membership form + Schedule A | **Submitted** | Waiting RVI processing |
| Kendall / list mapping path | **Documented** | `ibteshamulhaque01@gmail.com` |

### Measured numbers (do not invent)

```
Phase 1 GT (live UDB):     223 params; 100% any / 91% strong spec match
Part I v2 vs GT185:        adjusted recall 72.9%, class acc 88.4%, WARL 50%
Part I v2 vs live GT223:   adjusted recall 64.2%, class acc 88.6%, WARL 50%
parameters.csv named=yes:   87 rows / 83 unique
Pilot total spend:         ~$0.05
```

Source: [PHASE1-IMMERSION/06-measured-local/metrics_summary.json](./PHASE1-IMMERSION/06-measured-local/metrics_summary.json)  
Public tables: [riscv-param-extraction/docs/metrics.md](./riscv-param-extraction/docs/metrics.md)

### Phase 2 / 3 / 4

| Item | Status |
|------|--------|
| Phase 2 A/B home | **Inside this repo** — `riscv-param-extraction/` (not a second product repo) |
| Artifact A multi-model | **Not started** (API) |
| Artifact B YAML exporter | **Done offline** — 83 named + 20 new, all schema-valid |
| Stretch C WARL | **Not started** |
| Application / cover letter | **Not started** |
| SIG warm period | **Not started** |

### Session 2026-07-23 notes (state tracking)

- Confirmed OpenAI pilot key **worked** (docs/manifests); TPM 30k on gpt-4o large chunk  
- Artifact A **still not started**; can use existing OpenAI path when user authorizes  
- Public rival scan (Tier-1 packets: Anshul, Devadarsh, Harsh; UDB swarm ≠ seat race)  
- Coding challenge = shared applicant pattern; **not** seen as LFX file attachment  
- User: **makes plan**; agent: **tracks done + executes on go**

---

## Left to do

Canonical short list: **[LEFTOVER-WORK.md](./LEFTOVER-WORK.md)**

### You (community)

| # | Task | Done? |
|---|------|-------|
| 1 | LFX **mentee profile** only (not Apply) | [x] 2026-07-23 |
| 2 | Slack `#risc-v-mentorship-questions` (logistics only) | [x] 2026-07-22 |
| 3 | SIG/tech **calendar** | [ ] |
| 4 | Membership approval on Gmail | [ ] |
| 5 | Join **sig-parameters** + **sig-unifieddb** | [ ] blocked |
| 6 | Read list archives | [ ] |

### Technical

| # | Task | Done? |
|---|------|-------|
| 1 | Pilot `machine.adoc` | [x] COMPLETE_WITH_MODEL_SPLIT |
| 2 | Phase 2 path in lfx-firstanalysis | [x] `riscv-param-extraction/` |
| 3 | **Artifact A** multi-model + agreement | [ ] API |
| 4 | Artifact B exporter | [x] 83+20 (optional domain polish later) |
| 5 | Grounding/provenance public suite | [ ] with A preferred |
| 6 | Manifests every serious run | [~] pilot yes; A no |
| 7 | Stretch **C** WARL only if A+B done | [ ] |
| 8 | Short list note after A+B (when on list) | [ ] |
| 9 | No big unsolicited UDB PR | standing rule |

### Phase 3 (Jul 31–Aug 2)

| # | Task | Done? |
|---|------|-------|
| 1 | Cover letter | [ ] |
| 2 | Resume on profile | [~] uploaded; refresh if A ships |
| 3 | **Apply** to Part II | [ ] |
| 4 | Optional CFI/DFI | [ ] |

### Phase 4 (after apply)

| # | Task | Done? |
|---|------|-------|
| 1 | SIG meetings, iterate public repo | [ ] |
| 2 | Interview = walkthrough of visible work | [ ] |
| 3 | If selected: Obj 5 reviewed PR path | [ ] |

---

## Guarantee bar (selection packet)

| Requirement | Progress |
|-------------|----------|
| Reproduced pipeline | **Yes** |
| Measured multi-model / improvement | **No** (needs A + API) |
| Showed up at SIG | **No** (membership/list/meeting) |
| 9-week plan ↔ 5 objectives | **Not written** (Phase 3) |
| Reviewable A+B artifacts | **B yes (public)**; pilot yes; **A no** |

---

## Next chat

Paste the kickoff block in **[HANDOFF-NEW-SESSION.md](./HANDOFF-NEW-SESSION.md)**.  
Also open **[LEFTOVER-WORK.md](./LEFTOVER-WORK.md)**.

---

*Update this file when major checkboxes flip (A done, membership approved, Apply submitted, etc.).*
