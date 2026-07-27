# Nine-week mentorship plan ↔ 5 official objectives

**Applicant:** Ibteshamul Haque  
**Project:** AI-assisted architectural parameter extraction – Part II  
**Term (last verified):** ~2026-09-15 → 2026-11-15 · ≥30 h/week  
**Hours:** India (IST); flexible for US-Pacific  
**Prework repo:** https://github.com/titoatwork/lfx-firstanalysis  

**Official objectives**

1. LLM extract priv+unpriv; improve recall vs gold (Manual YAML / keyword_matches / UDB YAML)  
2. Extend classification scheme (only with evidence)  
3. AI agents/skills + reproducible workflows (manifests)  
4. Export → UDB YAML  
5. Reviewed PR + merge follow-up  

**On the baseline these targets move from.** The published 72.9% and 50% WARL are **grounding** scores: the Part I prompts supply all 185 gold parameter names and instruct the model to reuse them. Discovery recall, without that catalogue, is measured pre-apply in [`artifact_c/`](../riscv-param-extraction/artifact_c/PREREGISTRATION.md). Which number the term should optimise is a Week 0 decision with the mentors, because they are different tasks and only one of them is what "extraction" usually means.

**Targets, stated as commitments I control.** Improve recall against the mentor-pinned gold **under a stated condition**, with the condition named every time the number is; close the WARL gap or report why it does not close; ship N small schema-valid reviewed param files in mentor-approved PRs. I am not promising a specific percentage before knowing which task is being scored, and a target hit by quietly changing the condition is not a result.

**Non-goals:** unsolicited bulk PRs; claiming Spring authorship; treating schema-valid as architecturally correct; reporting a recall figure without the condition attached.

---

## Week 0 — Pre-start coordination (after selection)

| Work | Obj | Deliverable |
|------|-----|-------------|
| Channels, cadence, access to Manual YAML + keyword spreadsheet | 1,5 | Kickoff contract (1 page) |
| Confirm canonical UDB branch + first reviewable upstream target | 5 | Written success criteria |
| Agree recall / precision / WARL / merge readiness definition | 1,2 | Mentor-signed KPI paragraph |

**Exit:** Shared definition of success and inputs.

---

## Week 1 — Sep 15–21: Pinned reproduction

| Work | Obj | Deliverable |
|------|-----|-------------|
| Pin UDB, ISA Manual, Spring PR SHAs, prompts, golds | 1,3 | Environment lock + SHAs |
| Reproduce Part I end-to-end; verify GT185 / live GT223 | 1 | Baseline metrics report |
| Record commands, model IDs, prompt hashes, costs | 3 | Reproduction manifest |

**Exit:** Every reported baseline recreatable; mismatches explained.

---

## Week 2 — Sep 22–28: Reconcile golds + review semantics

| Work | Obj | Deliverable |
|------|-----|-------------|
| Crosswalk Manual YAML / spreadsheet / UDB YAML | 1,2 | Gold comparison table |
| Separate exact, alias, one-to-many, new candidates | 1,2 | Annotation guide |
| Human-review protocol; error taxonomy | 1,2 | Error book + rubric |
| Precision-oriented metrics, not recall alone | 1 | Metric definitions |

**Exit:** Mentors agree what counts as TP / one-to-many / new candidate.

---

## Week 3 — Sep 29–Oct 5: Grounded WARL experiment (Artifact C if approved)

| Work | Obj | Deliverable |
|------|-----|-------------|
| Extend the pre-apply four-arm result to the mentor-pinned gold | 1,2 | Replication or divergence report |
| Whichever of the four arms the pre-apply run says is worth pursuing | 1 | Follow-on ablation |
| Manual WARL case study on the cases the harness gets wrong | 1,2 | Recommendation adopt/reject |

**Exit:** Context intervention adopted with evidence **or** rejected with a second honest null.

**This week is narrower than it was, because the experiment now runs pre-apply.** The leakage-audited context builder, the fail-closed gold-name scan, the four arms and the preregistration are already built and public. Prompt-only v3 failed (WARL 3/24 → 2/24) and is not re-run. What is left for the term is extending the result to the mentors' own gold and acting on whichever arm wins, not building the apparatus.

---

## Week 4 — Oct 6–12: Extraction / classification candidate

| Work | Obj | Deliverable |
|------|-----|-------------|
| Attack dominant error classes from Weeks 2–3 | 1,2 | Candidate config |
| Cross-model gating **only if** it survives the pre-apply failure, see note | 1,3 | Gate design note |
| Taxonomy extension **only** with multiple reviewed cases + mentor OK | 2 | Proposal or “no change” |
| Freeze before held-out eval | 1 | Held-out plan |

**Exit:** No taxonomy change from LLM invention alone.

**Note on cross-model gating.** I proposed dual-model agreement as a review gate pre-apply. It does not work as claimed: of nine candidates both models proposed at high confidence, `IALIGN` is derived by `function ialign` in `globals.isa` and `FLEN` follows from which FP extension is implemented. The gate passed at least two non-parameters. It is carried into this week as a hypothesis to be re-tested at scale, not as a technique to be applied.

---

## Week 5 — Oct 13–19: Reproducible pipeline / workflow packaging

| Work | Obj | Deliverable |
|------|-----|-------------|
| Stage extract → analyze → compare → review → export | 3 | CLI/workflow |
| Manifests: SHA, prompt hash, model, chunks, tokens, cost, checksums | 3 | Manifest schema |
| Tests for chunking, normalization, alignment, manifests | 3 | Unit tests |
| Offline vs paid stages documented | 3 | Contributor runbook |

**Exit:** Maintainer can reproduce without hidden local state; paid path not accidental.

---

## Week 6 — Oct 20–26: UDB export integration

| Work | Obj | Deliverable |
|------|-----|-------------|
| Align exporter with SIG manual-side params.yaml direction | 4 | Design note |
| Export **only reviewed** findings; full provenance | 4 | Provenance format |
| Schema validation + fixtures | 4 | Green validation |
| Separate structural validity vs architectural approval | 4 | Docs |

**Exit:** Each draft YAML traces to spec evidence + human decision.

---

## Week 7 — Oct 27–Nov 2: Review queue + PR shaping

| Work | Obj | Deliverable |
|------|-----|-------------|
| Mentor-approved subset review queue | 4,5 | Reviewed set |
| PR boundaries: workflow vs exporter vs data | 5 | PR plan |
| Reviewer checklist + draft patches | 5 | Checklist |

**Exit:** Batch small enough and justified for upstream review.

---

## Week 8 — Nov 3–9: Upstream contribution

| Work | Obj | Deliverable |
|------|-----|-------------|
| Open agreed small PR(s) **only with mentor/list OK** | 5 | PR link(s) |
| Full suite green; fast review response | 5 | CI + response log |
| Split if maintainers request | 5 | Revision log |

**Exit:** Reviewers need not read entire experimental history.

---

## Week 9 — Nov 10–15: Merge follow-up + handoff

| Work | Obj | Deliverable |
|------|-----|-------------|
| Merge path or documented external blocker | 5 | Final status |
| Final pinned metrics; accepted/rejected approaches | 1,3 | Final report |
| Backlog + reproducibility package | 3,5 | Handoff |

**Success definition:** reproducible measurements + small mergeable artifacts, not maximum generated YAML count.

---

## Fortnight view (for short form fields)

| Fortnight | Focus | Objectives |
|-----------|--------|------------|
| 1 (W1–2) | Reproduce + gold crosswalk + review protocol | 1, 2, 3 |
| 2 (W3–4) | Grounded WARL + candidate pipeline freeze | 1, 2 |
| 3 (W5–6) | Workflow packaging + reviewed export | 3, 4 |
| 4 (W7–9) | Small PRs + merge follow-up + handoff | 4, 5 |

---

## Risks

| Risk | Mitigation |
|------|------------|
| Gold (a)(b) delayed | Start on UDB + public adoc; expand when Drive access arrives |
| Context leakage in WARL experiment | Fail-closed gold-name scan before any API call. Built and passing pre-apply |
| **Recall is measured against an incomplete gold** | A parameter that should exist but is absent cannot be scored as a miss. `Smpmpmt` carries implementation-defined language and declares no parameters ([@RAJVEER42](https://github.com/riscv/riscv-unified-db/issues/2053)). Recall is a regression signal, not a coverage measure, and Week 2 metric definitions must say so |
| **Reporting grounding recall as discovery recall** | State the name-list condition on every figure. This already went wrong pre-apply and was corrected publicly |
| **Losing the evidence behind a number** | Artifact A's per-chunk outputs were kept local and are gone, so its exclusive sets cannot be audited. Retention is a hard gate from Week 1: if a number is reported, the file it came from is committed |
| PR too large | Split tooling vs data; tiny reviewed batches |
| Over-focus on “new” params | Cap discovery; prioritize gold recall + precision |
| API cost | Cache; retries 0; mentor-approved spend only |
