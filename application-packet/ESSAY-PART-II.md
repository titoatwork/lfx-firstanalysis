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

While reproducing the Spring pipeline I found that its prompts inject the complete
list of 185 gold parameter names, set-identical to the ground truth, instructing
the model to use those exact names. Every published recall figure, including ones
I had been citing myself, therefore measures grounding against a supplied
catalogue rather than discovery. That is the right design for building a
spreadsheet and tagging spec text, but it is not what the numbers are usually read
to mean. I have corrected my own claims and documented the condition. Discovery
recall appears unmeasured anywhere public, and I have preregistered the experiment
that measures it.

Under that condition the remeasure gives 72.9% adjusted recall on the pinned gold
and 64.2% against live UDB, with WARL worst at 50%. A prompt-only WARL
intervention made WARL worse, 12.5% to 8.3%, so the failure is identification
rather than vocabulary: the model already had every correct name in front of it.
Two models given that identical catalogue still shared only 3.8% of parameter
names. I also built a schema-valid UDB export path (83/83 named, 20/20
candidates).

The Spring PRs (#1765–#1832, credit @ishaan-arora-1) are a superseded snapshot.
The mentee has noted that the working pipeline is internal, so I present my
remeasure as a public baseline rather than as current state.

Upstream, I opened riscv-unified-db #2138: a non-power-of-two value in the
unsigned_pow2 schema enums, with a regression test. A review comment of mine on
#2090 identified the same defect in the MTVEC alignment enums, and the maintainer
adopted the correction before that PR merged.

I can commit ≥30 hours/week for the Fall term.
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

What I measured, and a correction. Regenerating ground truth on live UDB gives 223
parameters; the Part I freeze was 185. Re-scoring the committed Claude-sonnet-4
output: 72.9% adjusted recall and 88.4% classification accuracy on GT185, 64.2% on
live GT223, WARL worst at 50% (12/24). Running the same 60 chunks and v2 prompt
through gpt-4o-mini (~$0.16) gave 32.2% adjusted recall, only 21 shared names
(Jaccard 3.8%), and nine high-confidence proposed-new names common to both models.
A contributor on the upstream scope thread has since predicted those nine will be
the *easy* cases, since agreement should concentrate on well-known quantities and
disagreement on genuinely underspecified ones. Four of the nine are textbook
quantities, so he may be right. I registered his prediction as a hypothesis in the
experiment below rather than defending the number. A prompt-only WARL ablation
raised overall recall to 35.0% while cutting WARL recall from 3/24 to 2/24.

The correction matters more than any of those numbers. Building the next
experiment, I traced the prompt assembly and found that every run injects all 185
gold parameter names, a set identical to the ground truth, with the instruction to
reuse them exactly. So these are grounding scores against a supplied catalogue,
not discovery scores. For the Spring deliverables, a spreadsheet and tagged spec
text, that is the correct design. But it reframes the WARL result: the model was
never short of the right name, so the failure is identification, and it explains
why adding prompt guidance made things worse rather than better. I updated
metrics.md, the claim ledger and this essay rather than leaving the ambiguity in
place, and preregistered the measurement of discovery recall before running it.

What I built. An exporter mapping parameters.csv to draft UDB param YAML,
schema-valid at 83/83 named (87 rows / 83 unique) and 20/20 new candidates. That
is structural conformance only, not architectural approval. A challenge control
pack (four fail-closed fixtures, four hard negatives, n=15 known-param mechanics
under a pretraining caveat, a ten-model live matrix including honest CSR false
positives, green CI). A temporal holdout harness whose locked primary run returned
0/10 name recall in both arms, an exploratory null under documented v1.2
limitations rather than evidence that context fixes WARL.

Upstream. I opened riscv-unified-db #2138 with linked issue #2137: both
unsigned_pow2 schema enums list 4095, not a power of two, fixed with a regression
test wired into the Ruby test runner rather than a bare data edit. A review
comment of mine on #2090 identified the same defect in the MTVEC alignment enums,
and the maintainer agreed and corrected it before merge. That PR is his, and I
claim only the review. I also published an adversarial eval pack (five positives,
four negatives) against the extraction-skill PR #2097, including the sharpest
case: WARL vocabulary whose legal value set is ISA-fixed, leaving no
implementation choice. A second pair, #2145/#2146, corrects two parameter
descriptions found while triaging an automated invariant sweep over all 227 param
files. The sweep's other flag, an MXLEN/SXLEN type asymmetry, turned out to be
architecturally correct, so I documented why instead of filing it. My aim upstream
is small, testable, issue-linked work and useful review, not volume.

What Part II must do differently. Ground output in CSR/spec context under leakage
audit and preregistered evaluation; treat cross-model agreement as a review
signal, not truth; keep provenance (file, anchor, excerpt, class, confidence, run
id); export only reviewed findings; open small issue-linked PRs, not generated
dumps.

Prior credibility. Fourth-year CS undergraduate; research attachment at Universiti
Malaya under Prof. Por Lip Yee (on-site June 2026), owning an end-to-end IoT IDS
pipeline with measured evaluation and a manuscript in preparation. Baseline,
measure, document limits, ship reviewable artifacts.

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
