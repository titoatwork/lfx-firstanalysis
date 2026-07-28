# Part II application answers — ready to paste

**Date:** 2026-07-26  
**Project:** AI-assisted extraction of architectural parameters from RISC-V specifications – Part II  
**Public prework:** https://github.com/titoatwork/lfx-firstanalysis  
**Metrics:** `riscv-param-extraction/docs/metrics.md`  
**Credit:** Spring Part I — @ishaan-arora-1 / riscv-unified-db PRs #1765–#1832 (reproduction, not authorship)

Replace bracketed contact fields only if the form asks. Numbers below match the measured-claim ledger.

---

## 1. Short project-specific response (~150–200 words)

```text
I am applying to AI-assisted extraction of architectural parameters from RISC-V
specifications – Part II (LFX Fall 2026).

I preregistered an experiment on whether removing the gold name catalogue reduces
extraction recall, and ran each arm twice. The registered question was answered.
The useful result was not registered: the same model, byte-identical prompt,
temperature 0, run twice, scored 33.9% and 44.6%. Prompts match by hash and the
scorer reproduces the published figures exactly, so the variation is the model and
the alignment step amplifies it. Single-run recall here cannot carry the
comparisons it is asked to carry, including my own. Reported upstream as
riscv-unified-db #2163.

I had nearly published the opposite. After one run, WARL looked like it collapsed
without the catalogue, which is the mechanism I had been arguing. The second run
reversed it, so I withdrew the finding.

I also found the pipeline injects all 185 gold parameter names, so every published
recall figure measures grounding rather than discovery. I corrected my own claims.
Under that condition the remeasure is 72.9% on the pinned gold, with WARL worst at
50%, and prompt-only WARL guidance made it worse rather than better.

Upstream: three PRs open, two approved, and a review comment of mine on #2090 was
adopted by the maintainer before that PR merged. I can commit ≥30 hours/week.
```

---

## 2. Longer response (~350–500 words)

```text
I am applying to the Fall 2026 mentorship “AI-assisted extraction of
architectural parameters from RISC-V specifications – Part II.”

Understanding of the work. Part II continues Spring LFX and Parameter SIG work:
extract parameters from privileged and unprivileged ISA material with LLMs;
evaluate against gold sources (Manual chapter YAML, keyword spreadsheets, UDB
param YAML); extend classification; productize reproducible workflows; export
schema-valid UDB YAML; and land reviewed PRs. The public Spring surface is PRs
#1765–#1832 (@ishaan-arora-1), but the Spring mentee has noted the working
pipeline is internal and those PRs were its first version. I treat them as a
superseded snapshot rather than the baseline to build on. That shapes what success
means. Not more candidates against a stale reference, but evaluation that stays
valid while the pipeline underneath it moves.

What I measured. Regenerating ground truth on live UDB gives 223 parameters; the
Part I freeze was 185. Re-scoring the committed Claude-sonnet-4 output: 72.9%
adjusted recall, 88.4% classification accuracy on GT185, 64.2% on live GT223, WARL
worst at 50%. gpt-4o-mini on the same 60 chunks reached 32.2%, sharing only 3.8%
of parameter names with Claude.

Three corrections to my own work, in the order I found them. First, the prompts
inject all 185 gold parameter names, a set identical to the ground truth, so every
figure above is a grounding score against a supplied catalogue rather than
discovery. That is correct design for the Spring deliverables, and it reframes
WARL: the model was never short of the right name, so the failure is
identification, which is why prompt-only guidance made it worse.

Second, I had called nine dual-model candidates a prioritised review queue. A
contributor checked one: IALIGN is derived in globals.isa from whether C is
implemented, not a parameter at all. I verified it and found FLEN is derived too,
so the gate passed at least two non-parameters. I registered his objection as a
hypothesis with a rubric fixed in advance instead of defending the number.

Third, and most consequential, running each arm twice showed adjusted recall
moving 33.9% to 44.6% with nothing changed. Prompts match by hash and the scorer
is deterministic, so it is the model, amplified by the alignment step. Every
single-run figure above, mine and the published baseline alike, is one sample.
Reported upstream as #2163.

What I built. An exporter producing schema-valid draft UDB param YAML (83/83
named, 20/20 new candidates), which is structural conformance only. A challenge
control pack with four fail-closed fixtures, four hard negatives and a ten-model
live matrix that reports its CSR false positives. A temporal holdout harness whose
locked run returned 0/10 in both arms, an exploratory null rather than evidence
for anything.

Upstream. Three PRs open, two approved. #2137/#2138 fixes a non-power-of-two value
in both unsigned_pow2 schema enums and ships a regression test rather than a bare
data edit. #2145/#2146 corrects two parameter descriptions found while triaging an
automated sweep over all 227 param files; the sweep's other flag turned out to be
architecturally correct, so I documented why instead of filing it. #2164
contributes the evaluation fixtures. A review comment of mine on #2090 identified
the MTVEC alignment defect and the maintainer adopted it before merge, though that
PR is his and I claim only the review. My aim upstream is small, testable,
issue-linked work, not volume.

What Part II must do differently. Ground output in CSR context under leakage audit
and preregistered evaluation; run more than once before believing a difference;
treat cross-model agreement as a signal to review rather than truth; keep
provenance; export only reviewed findings.

Prior credibility. Fourth-year CS undergraduate; research attachment at Universiti
Malaya under Prof. Por Lip Yee, owning an end-to-end IoT IDS pipeline with measured
evaluation and a manuscript in preparation.

Logistics. ≥30 hours/week for ~15 Sep–15 Nov 2026; India (IST), flexible for
US-Pacific meetings. Prework: https://github.com/titoatwork/lfx-firstanalysis

Thank you for your consideration.
```

---

## 3. Why this project?

```text
Because Part II sits at ISA specifications, structured evaluation, and
LLM-in-pipeline discipline with clear public baselines and open merge debt. The
Spring trail makes success criteria concrete (recall, taxonomy, export, PR), and
my prework already measures multi-model failure modes and a schema-valid export
path rather than a generic “I like AI and RISC-V” essay.
```

---

## 4. Relevant experience

```text
- Reproduced and measured the public Spring parameter-extraction snapshot
  (credit @ishaan-arora-1 / PRs #1765–#1832): 72.9% adjusted recall on GT185;
  64.2% on live GT223; WARL 50%.
- Upstream riscv-unified-db: opened #2138 (+ issue #2137) fixing a non-power-of-
  two value in the unsigned_pow2 schema enums, with a regression test; a review
  comment on #2090 identified the same defect in the MTVEC alignment enums and
  the maintainer adopted the correction before merge; published an adversarial
  eval pack and five-point review against the extraction-skill PR #2097.
- Built a CSV→draft UDB YAML exporter with schema validation (83 named + 20
  candidate drafts).
- Ran a controlled 60-chunk gpt-4o-mini vs Claude comparison (32.2% vs 72.9% adj
  recall; 3.8% name Jaccard) and a negative prompt-only WARL ablation (3/24→2/24).
- Research attachment at Universiti Malaya (Prof. Por Lip Yee): end-to-end IoT
  IDS, GPU inference, on-device LLM explainability, reproducible evaluation;
  manuscript in preparation.
- Strong habits: Python tooling, Git, YAML/structured configs, manifests, honest
  limitations; treating LLMs as instrumented pipeline stages, not ad-hoc chat.
```

---

## 5. Technical approach (term)

```text
Week 0: mentor kickoff contract. Establish which pipeline is actually live (the
internal one, not the Spring PR snapshot), plus repos, golds, metrics, and the
shape of the first PR.
Weeks 1–2: build the evaluation harness before touching extraction. Pin SHAs;
reconcile Manual YAML / spreadsheet / UDB golds into one versioned reference;
per-class recall, negative controls, cross-model agreement, human-review protocol
and error taxonomy. Recall that cannot be measured cannot be improved, and a
harness keeps its value while the pipeline underneath it changes, which, given the
Spring history, it will.
Week 3: leakage-audited CSR-field context experiment for WARL, the worst class at
50% and the one prompt-only guidance already failed to fix; publish a positive or
negative result equally.
Weeks 4–5: fix dominant error classes; optional cross-model gating for review
efficiency; package reproducible workflows with manifests and tests (Obj 3).
Week 6: export only reviewed findings to UDB YAML with provenance; schema tests.
Weeks 7–8: small mentor-approved PRs (tooling and/or reviewed data), not bulk
dumps; full suite green; fast review response.
Week 9: merge follow-up, final metrics, handoff backlog.
Success = reproducible measurements and small mergeable artifacts, not maximum
generated YAML count.
```

---

## 6. Expected mentorship outcomes

```text
Ability to land machine-readable ISA parameter artifacts maintainers trust;
deeper RISC-V spec literacy (especially WARL and classification boundaries);
experience shipping under RVI mentorship standards with provenance and metrics
that both mentors can audit: Baum-style reviewability and Dingankar-style
baselines/ablations.
```

---

## 7. Availability and timezone

```text
≥30 hours/week for the Fall term (~15 September–15 November 2026). Location:
India (IST, UTC+5:30). Flexible for US-Pacific mentor meetings. LFX mentee
profile and resume already on the platform; primary application is this Part II
project only.
```

---

## 8. Public prework / repository link

```text
https://github.com/titoatwork/lfx-firstanalysis

Upstream (riscv/riscv-unified-db):
- PR #2138 + issue #2137: unsigned_pow2 schema enums, with regression test
- PR #2146 + issue #2145: SXLEN/UXLEN description corrections
- PR #2090: review comment identified the MTVEC alignment defect; the maintainer
  adopted the correction before merge (that PR is the maintainer's, not mine)
- PR #2097: five-point review + adversarial eval pack for the extraction skill
- Issue #2053: measured WARL/cross-model findings contributed to scope discussion

Start with:
- riscv-param-extraction/docs/metrics.md
- riscv-param-extraction/manifests/artifact-a-gpt-4o-mini.md
- riscv-param-extraction/manifests/stretch-c-v3-warl.md
- riscv-param-extraction/manifests/pilot-machine-adoc.md
- riscv-param-extraction/export/ and drafts/
```

---

## One-sentence summary (form field if present)

```text
I measured where parameter extraction actually fails (WARL worst at 50%, 3.8%
cross-model name agreement, a failed prompt-only WARL fix), built a schema-valid
UDB export path, and have started contributing small issue-linked fixes and
review upstream rather than bulk generation.
```
