# Progress — done vs left

**Last updated:** 2026-07-26 ~05:00 (pre-sleep; **wake still morning of 26 Jul**)  
**Canonical handoff:** [HANDOFF-2026-07-26-MORNING.md](./HANDOFF-2026-07-26-MORNING.md)  
**Leftovers:** [LEFTOVER-WORK.md](./LEFTOVER-WORK.md)  
**GitHub ONLY:** https://github.com/titoatwork/lfx-firstanalysis · **`main` @ 58f91de**  
**Local UDB:** `riscv-unified-db/` · `lfx-1832` (gitignored)

---

## Snapshot

| Area | State |
|------|--------|
| Study + Phase 1 technical | **Done** |
| Pilot model-split | **Done** (~$0.05) |
| Artifact A multi-model (corpus) | **Done** (mini 32.2% vs Claude 72.9%; Jaccard 3.8%) |
| Artifact B export | **Done** (83+20 schema-valid) |
| v3 WARL ablation | **Done — null** |
| Application packet | **On main** |
| Coding challenge + CI | **Done + pushed** (`58f91de`) |
| Live multi-model on challenge snippets | **Not done** |
| UDB PR opened/merged | **Draft only** (not opened) |
| Apply Part II | **NOT submitted** — target **Jul 31** (hard stop Aug 2) |
| Community (membership/lists) | In progress |
| vs Anshul | Challenge/CI gap **mostly closed**; still behind live multi-model + merge; lead corpus/export/null |

---

## Measured facts (do not invent)

```
GT223: 100% any / 91% strong
Claude v2 GT185: 72.9% adj / 88.4% class / WARL 50%
vs GT223: 64.2% adj
named=yes: 87 rows / 83 unique
B: 83/83 + 20/20 schema-valid
Pilot: ~$0.05 model-split
A mini: 32.2% adj / Jaccard 3.8% / WARL 12.5% / ~$0.16
v3: 35.0% adj / WARL 8.3% null / ~$0.16
```

Public tables: `riscv-param-extraction/docs/metrics.md`  
Credit: @ishaan-arora-1 / PRs #1765–#1832

---

## Next (morning of 26 Jul — same day)

**User:** membership/resume as needed; essay path; prepare keys for multi-model if going that route.  
**Agent on go:** `GO LIVE MULTI-MODEL` · `GO OPEN UDB PR` · `GO ERASE ANSHUL` · `GO SPINE apply` · `push`  
**Apply:** still **Jul 31**, not morning of 26.

---

*Update when Apply submitted, multi-model lands, or UDB PR opens.*
