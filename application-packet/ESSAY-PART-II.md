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

I studied and reproduced the public Spring Part I work on riscv-unified-db
(credit: @ishaan-arora-1 / PRs #1765–#1832) rather than treating it as a black
box. Against the pinned 185-parameter gold I remeasured 72.9% adjusted recall,
88.4% classification accuracy, and 50% WARL recall; against the live 223-
parameter set, adjusted recall falls to 64.2%, which shows why pinned and
evolving golds both matter.

I then shipped two concrete pre-apply artifacts in
github.com/titoatwork/lfx-firstanalysis: a schema-valid draft UDB YAML exporter
(83 existing named parameters + 20 candidates) and a controlled 60-chunk second-
model run with gpt-4o-mini (PROMPT v2). Mini reached only 32.2% adjusted recall
versus the public Claude baseline of 72.9%, with 3.8% parameter-name Jaccard.
A prompt-only WARL ablation was negative (matched WARL 3/24 → 2/24).

These results motivate grounded CSR context, cross-model/human review gates,
explicit provenance, and small reviewable PRs—not bulk generation. I can commit
≥30 hours/week for the Fall term.
```

---

## 2. Longer response (~350–500 words)

```text
I am applying to the Fall 2026 mentorship “AI-assisted extraction of
architectural parameters from RISC-V specifications – Part II.”

Understanding of the work. I treat Part II as continuation of Spring LFX and
Parameter SIG work: extract architectural parameters from privileged and
unprivileged ISA material with LLMs; evaluate against gold sources (Manual
chapter YAML, keyword spreadsheets, and UDB param YAML); improve classification
where evidence supports it; productize reproducible agent/workflows; export
schema-valid UDB YAML; and land reviewed, maintainable PRs. The Spring pipeline
is public on open PR branches (#1765–#1832, mentee @ishaan-arora-1). As of this
application those PRs remain unmerged—so Fall success is not “extract more
candidates,” but reliability, reviewable artifacts, and mergeable work.

What I reproduced and measured. I cloned UDB on the fullest Part I branch,
regenerated ground truth (223 live parameters; 100% any / 91% strong keyword
match), and remeasured the committed Claude-sonnet-4 v2 results: 72.9% adjusted
recall and 88.4% classification accuracy on the pinned 185-parameter freeze;
64.2% adjusted recall on live 223. WARL-class recall remains 50% (12/24). I
completed a machine.adoc pilot with an honest model split (gpt-4o + gpt-4o-mini)
because org TPM blocked a pure gpt-4o path on the large chunk.

What I built. Artifact B maps parameters.csv rows to draft UDB param YAML and
validates against the UDB param schema: 83/83 named parameters (87 rows / 83
unique; all already present in UDB) and 20/20 new candidates are schema-valid.
“Schema-valid” means structural conformance, not architectural approval or
mentor acceptance. Artifact A ran the same 60 param-bearing chunks and v2 prompt
with gpt-4o-mini (~$0.16): 32.2% adjusted recall versus Claude’s 72.9%, only 21
shared names (Jaccard 3.8%), and nine high-confidence proposed-new names that
appear in both models—still candidates requiring human review, not confirmed
parameters. A prompt-only WARL guidance ablation (v3) slightly raised overall
adjusted recall to 35.0% but reduced matched WARL recall from 3/24 to 2/24: more
confident labeling is not more correct labeling.

What Part II must do differently. Ground model output in CSR/spec context with a
leakage audit; treat cross-model agreement as a review signal, not automatic
truth; keep provenance (spec file, anchor, excerpt, class, confidence, run id);
export only reviewed findings; open small PRs with reproduction commands instead
of another enormous generated dump.

Prior research credibility. I am a 4th-year CS undergraduate. I completed a
faculty research attachment at Universiti Malaya under Prof. Por Lip Yee (on-site
June 2026), owning an end-to-end IoT IDS pipeline with measured evaluation and
manuscript preparation (FGCS target). That habit—baseline, measure, document
limits, ship reviewable artifacts—is what I will bring here.

Logistics. ≥30 hours/week for ~15 Sep–15 Nov 2026; India (IST), flexible for
US-Pacific meetings. Public prework and numbers:
https://github.com/titoatwork/lfx-firstanalysis
(path riscv-param-extraction/; metrics and manifests under docs/ and manifests/).

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
- Reproduced and measured the public Spring parameter-extraction pipeline
  (credit @ishaan-arora-1 / PRs #1765–#1832): 72.9% adjusted recall on GT185;
  64.2% on live GT223; WARL 50%.
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
Week 0: mentor kickoff contract—repos, golds, metrics, first PR shape.
Weeks 1–2: pin SHAs; reproduce baselines; reconcile Manual YAML / spreadsheet /
UDB golds; human-review protocol and error taxonomy.
Week 3: leakage-audited CSR-field context experiment for WARL (only if mentors
want it); publish positive or negative result equally.
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
that both mentors can audit—Baum-style reviewability and Dingankar-style
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
I reproduced the Spring pipeline, measured multi-model and WARL failure modes,
built a schema-valid UDB export path, and plan small human-reviewed upstream
contributions—not bulk generation.
```
