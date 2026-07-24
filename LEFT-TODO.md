# What’s left — personal todo list

**Updated:** 2026-07-22 (Phase 2 start)  
**Plan lock:** `PLAN-SOURCE-OF-TRUTH.md`  
**Phase 2 plan:** `PHASE2-PLAN.md`  
**Pilot status:** `COMPLETE_WITH_MODEL_SPLIT` (do not re-spend on pilot unless reopened)

**For agents:** prefer canonical **[LEFTOVER-WORK.md](./LEFTOVER-WORK.md)** + **[AGENTS.md](./AGENTS.md)**.  
This file is a personal checkbox mirror; keep both in sync when you flip items.

Use this as your working checklist. Mark items `[x]` when done.

---

## Done (do not redo)

- [x] Phase 1 study / deep immersion pack
- [x] UDB clone + Part I branches + GT remeasure + metrics (72.9% / 88.4% / WARL 50%)
- [x] Artifact **B** — CSV → draft UDB YAML (83 named + 20 new, schema OK)
- [x] Public monorepo path for B (`titoatwork/lfx-firstanalysis` → `riscv-param-extraction/`)
- [x] Pilot **COMPLETE_WITH_MODEL_SPLIT**
  - chunk_021 → gpt-4o (~$0.04, 6 params)
  - chunk_020 → gpt-4o-mini (~$0.008, 9 params)
  - total pilot ~$0.05; honest model-split claim only
- [x] Membership form + Schedule A **submitted**
- [x] Kendall mapping email **sent**

---

## NOW — free / you (no API)

### Security
- [ ] **Rotate OpenAI API key** (old key was pasted in chat)

### Community presence
- [ ] **LFX mentee profile** filled (resume + intro) — **not** project Apply
- [ ] Join **RISC-V Slack** → `#risc-v-mentorship-questions` only (logistics)
- [ ] Subscribe **SIG / tech calendar** — https://tech.riscv.org/calendar/
- [ ] **Membership approved** (wait / bump Kendall if &gt; ~1 week)
- [ ] Join **sig-parameters** (from `ibteshamulhaque01@gmail.com` after roster active)
- [ ] Join **sig-unifieddb**
- [ ] Read **sig-parameters archives** (beyond RSS digest)

---

## PHASE 2 — now

See **`PHASE2-PLAN.md`**.

### Offline first ($0)
- [ ] Confirm machine has `riscv-unified-db` @ `lfx-1832` + Claude Part I results
- [ ] Confirm prototype `riscv-param-extraction/` (B) present
- [ ] Inventory chunks / TPM-unsafe sizes
- [ ] Ensure `gpt4o-mini` alias works for full `run`
- [ ] Scaffold agreement analysis vs Claude v2 (no API)
- [ ] READY gate + exact A commands documented

### Paid — Artifact A (only when you say go)

Budget: ~**$5** OpenAI. Recommended: **gpt-4o-mini full/near-full run** (not gpt-4o).

- [ ] Explicit **spend go-ahead** + rotated key
- [ ] `extract.py run` (mini) + merge + analyze
- [ ] Per-class recall vs GT + vs Claude Part I
- [ ] Inter-model agreement + hallucination-overlap (honest if worse)
- [ ] Run **manifests** (model, tokens, cost, cmd)
- [ ] Update `docs/metrics.md` + README
- [ ] Local commit; push only if ordered

### Stretch (only if A+B solid and budget allows)
- [ ] **C** WARL recall attack (optional)

---

## THEN — publish & apply

### Git / GitHub
- [ ] Decide what local commits to **push** (status/pilot docs, monorepo updates) — only when you order push
- [ ] README / metrics reflect: B done + pilot model-split + A when ready
- [ ] No unsolicited big UDB PRs

### Soft signal (after A is real)
- [ ] Short **sig-parameters** note: link + ~5 bullets
- [ ] Optional calm comment on relevant UDB issue

### Phase 3 application (target ~Jul 31–Aug 2, not last-minute Aug 5)
- [ ] 1-page **resume PDF** (no CGPA, no confidential COLIDE)
- [ ] Cover letter: research line + **your** measured numbers + B/A links + 9-week plan → 5 objectives
- [ ] **Apply** Part II on LFX
- [ ] Complete prereqs; confirm Pending
- [ ] Optional: CFI/DFI apps with **separate** letters (Part II primary; max ~3 apps)

---

## Phase 4 (after apply)

- [ ] Keep attending SIG meetings
- [ ] Iterate public prototype if needed
- [ ] On-list replies when useful
- [ ] Interview = walk through work already public

---

## Quick “what do I do today?”

1. Rotate OpenAI key  
2. LFX mentee profile  
3. Slack + calendar  
4. Wait for membership → join lists  

**Do not** spend API money until you start Artifact A on purpose.

---

## Honest claims cheat-sheet

| Topic | Say this |
|--------|----------|
| Pilot | machine.adoc complete with **model split** (4o + 4o-mini) due to gpt-4o TPM |
| Named params | **83** unique (`named=yes` rows **87**) — not 97 |
| Metrics | Part I remeasure **72.9%** adj recall, **88.4%** class acc, WARL **50%** (GT185) |
| B | Schema-valid draft YAML export offline |
| A | Only after you run it |

---

*End leftover todo list.*
