# How we present work on GitHub

**Status:** LOCKED with plan until user replaces it  
**Plan lock:** `PLAN-SOURCE-OF-TRUTH.md`  
**Do not invent a different presentation strategy later.**

---

## 1. Where work lives

| Rule | Detail |
|------|--------|
| **Home** | **`titoatwork/lfx-firstanalysis`** (single repo). Phase 2 code under `riscv-param-extraction/`. Do not invent a second public repo unless user asks. |
| **Not first** | Giant unsolicited PR into `riscv/riscv-unified-db` |
| **Credit** | Link Part I issues/PRs (#1747–#1832, #1765–#1832); never claim Spring as ours |
| **Identity** | User’s GitHub/email only — see `PLAN-SOURCE-OF-TRUTH.md` |

---

## 2. Repo shape (canonical)

```text
<your-repo>/
  README.md                 # 5-minute path: problem → numbers → how to run
  docs/
    design.md               # decisions, non-goals, relation to Part I
    metrics.md              # tables only (remeasure + A vs Claude + B validation)
  manifests/                # one file per run (model, tokens, cost, commit, cmd)
  pipeline/                 # thin, domain-named code (not generic “AI app”)
  export/                   # Artifact B: csv → draft YAML
  results/                  # small samples committed; large dumps gitignored
  drafts/param/             # generated YAML, clearly DRAFT
  LICENSE
```

Names/layout: **UDB / params / recall / WARL** vocabulary — not chatbot-starter cosplay.

---

## 3. README order (do not reorder into fluff)

1. One paragraph — Part I exists; gap = multi-model + UDB export (Obj 1/4).  
2. **Measured numbers tables** — remeasure (72.9% / 88.4% / WARL 50%), then A, then B.  
3. Exact **reproduce** commands.  
4. **Limitations** (honest).  
5. Links — Part I PRs, later list post.  
6. **No** emoji walls, “my journey,” fake certainty.

**Pass test:** Baum can audit one param draft provenance; Dingankar can recompute a metric.

---

## 4. What each artifact looks like on GitHub

| Artifact | On GitHub |
|----------|-----------|
| Reproduce Part I | `docs/metrics.md` + notes/scripts; credit upstream |
| **A** multi-model | Tables + manifests; agreement + hallucination-overlap |
| **B** exporter | Code + `drafts/param/*.yaml` + schema validation log |
| **Obj 3** | `manifests/*` every serious run |
| **C** WARL | Only if real lift; separate section |

---

## 5. Commits & hygiene

- Small commits, domain-specific messages  
- No API keys; no huge binary dumps in git  
- Pin model ids / prompt version in manifests  
- `DRAFT` in paths or headers for unmerged YAML  
- Update README when numbers change  

---

## 6. Presentation stack (order)

```text
1. GitHub public repo (always — main stage)
2. After membership + A/B: short sig-parameters email (link + 5 bullets)
3. Optional: one calm UDB issue comment (same link)
4. Phase 3: LFX application points at repo (not a substitute)
5. If invited: draft UDB PR (subset) — never unsolicited megadiff
```

### Explicit non-goals on GitHub

| Avoid | Why |
|-------|-----|
| Empty UDB fork as portfolio | Tier C |
| Claiming Part I authorship | Dishonest |
| Many cosmetic UDB PRs for “GSoC optics” | Wrong filter for this project |
| Private-only “trust me” results | Not auditible |
| Generic AI README template | User quality bar |

---

## 7. One-line standard

**Present so a mentor clones once, runs one command, and sees the same table you claim.**

---

## 8. When Phase 2 starts (first GitHub steps)

1. Work **in** `titoatwork/lfx-firstanalysis` (already exists) — path `riscv-param-extraction/`  
2. Folder README + `docs/metrics.md` with **already measured** 72.9% numbers  
3. Implement A then B to fill tables for real  
4. Manifests on every run  
5. Date new work clearly (e.g. `docs/WORKLOG-YYYY-MM-DD.md`) so it is not confused with Phase 1 commits  

Do **not** invent a different repo or layout without updating this file and `PLAN-SOURCE-OF-TRUTH.md`.

---

*Locked 2026-07-21. Agent must re-read this before scaffolding the public repo.*
