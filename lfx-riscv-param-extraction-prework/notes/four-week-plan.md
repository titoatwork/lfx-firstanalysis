# Four-week plan (Fall term scaffold)

**Hours:** ≥30 h/week  
**Assumes:** mentor-approved gold pins; access to Spring handoff branch + (a)(b) when available  
**Adjust:** first meeting with Baum / Dingankar overrides this

---

## Week 1 — Reproduce & freeze baseline

| Task | Output |
|------|--------|
| Checkout agreed Spring PR branch(es) / handoff archive | `ENVIRONMENT.md` with SHAs |
| Reproduce extract+eval on pinned gold (UDB 1c; subsets of a/b) | Metric table vs published V2 |
| Document gaps (WARL, naming, false new) | `error_book.md` top 20 failures |
| Agree Fall KPI with mentors | Written KPI (1 paragraph) |

**Goals hit:** 1 (partial), 3 (start logging)

**Exit criteria:** Can re-run eval; numbers within noise of Spring or explained.

---

## Week 2 — Quality push

| Task | Output |
|------|--------|
| Targeted few-shots / rules for WARL + naming | Prompt `v3` changelog |
| Alignment improvements (one-to-many groups review) | Updated alignment config |
| Human review protocol for “new” params | Rubric: accept / reject / defer |
| Taxonomy tweak only if confusion matrix demands | `taxonomy_diff.md` |

**Goals hit:** 1, 2

**Exit criteria:** Measurable lift on WARL recall and/or precision; fewer unchecked discoveries.

---

## Week 3 — Robustness & agents/skills

| Task | Output |
|------|--------|
| Package pipeline as skill/agent-style workflow | README + entrypoint |
| Prompt/context versioning + config | `prompts/v3/`, hash in logs |
| Chunk policy tests (CSR atomicity, overlap) | Automated checks |
| Optional second model smoke compare | Cost + agreement notes |

**Goals hit:** 3, supports 1

**Exit criteria:** Clean re-run by mentor instructions alone.

---

## Week 4 — UDB YAML export + PR

| Task | Output |
|------|--------|
| Mapper reviewed rows → `param_schema` YAML | Generator + samples |
| Schema validation | CI or script green |
| Small PR(s): data and/or tooling | GitHub PR |
| Maintainer follow-up | Response log |

**Goals hit:** 4, 5

**Exit criteria:** Reviewed subset PR open with schema-valid files; merge path clear.

---

## Parallel hygiene (all weeks)

- Weekly status to mentors (metrics + blockers)  
- No bulk unaudited merges  
- Pin dependency versions for reproducibility  
- Keep Parameter SIG-aware naming/docs  

---

## Risk register

| Risk | Mitigation |
|------|------------|
| Gold (a)(b) delayed | Start on UDB 1c + public adoc; expand when Drive arrives |
| Spring branch bitrot | Early freeze + mentor-owned archive |
| Over-focus on new params | Cap discovery; prioritize gold recall |
| PR too large | Split tooling vs data; tiny reviewed batches |
| API cost | Pilot `machine.adoc`; cache; temperature 0 |
