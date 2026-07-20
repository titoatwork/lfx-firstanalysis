# Application essay — AI params Part II only

**Use when applying to this project on LFX.**  
Do **not** paste the multi-project profile intro here unchanged—this is project-specific.  
Replace bracketed bits. Keep honest.

---

## Short version (~150–200 words)

```text
I’m applying to AI-assisted extraction of architectural parameters from RISC-V
specifications – Part II for LFX Fall 2026.

I’ve read the project goals and studied the public Spring trail on
riscv-unified-db: ground-truth cataloging of UDB parameters, the classification
taxonomy (NORM_DIRECT / NORM_CSR_WARL / NORM_CSR_RW / …), CSR-safe AsciiDoc
chunking, the extract–analyze loop, and the V1→V2 metrics (adjusted recall into
the low ~70s, classification accuracy much higher, WARL-class recall still ~50%).
I also noted that much of param_extraction still lives on open PRs rather than
main, and that spreadsheet/tags are ahead of schema-valid UDB YAML merges—so
Fall’s focus on quality, robustness, UDB export, and actually landing PRs reads
as a concrete next step, not a rebrand.

I’m a 4th-year CS undergrad. I completed a faculty research attachment at
Universiti Malaya (Prof. Por Lip Yee)—June on-site—owning an end-to-end
systems/ML pipeline with serious measurement and write-up discipline
(manuscript in preparation). I’m used to baselines, failure modes, and finishing
under a mentor.

I can commit at least 30 hours/week for the term. Pre-work notes:
[link to this public pre-work repo when published].

Thank you for your consideration.
```

---

## Longer version (if form allows)

```text
I’m applying to the Fall 2026 mentorship “AI-assisted extraction of architectural
parameters from RISC-V specifications – Part II.”

Understanding of the work
I treat Part II as continuation of Spring 2026 LFX + Parameter SIG work: use LLMs
to find architectural parameters in privileged and unprivileged ISA material,
evaluate against gold lists (per-chapter Manual YAML, keyword_matches spreadsheet,
and UDB param YAML), improve classification, productize reproducible
agent/skills-style workflows, export schema-valid UDB YAML, and land reviewed
PRs with maintainers.

From the public Spring trail on riscv-unified-db I studied the phased pipeline
(ground truth → taxonomy/prompts → CSR-atomic chunking → extraction → alignment
metrics → prompt v2 → spreadsheet → [#param:] tagging). Published V1→V2 numbers
show real gains (adjusted recall ~62.7%→~72.9%, classification accuracy
~67.9%→~88.4%) but leave clear gaps—especially NORM_CSR_WARL recall (~50%) and
a large set of “new” discoveries that need human review. The fact that
param_extraction is not fully merged to main matches the Fall emphasis on
implementation robustness and mergeable artifacts.

What I would prioritize
Week 1: reproduce eval on a mentor-pinned baseline. Then quality (WARL, naming
mismatch, false discoveries), then agent/skills packaging, then export of
reviewed rows to param_schema-valid YAML and small PRs—not bulk unaudited dumps.

Background
4th-year CS undergrad. Research attachment at Universiti Malaya under Prof. Por
Lip Yee (on-site June; major implementation before/after). I owned a multi-stage
systems/ML pipeline with careful evaluation and am now in manuscript preparation.
That habit—baseline, measure, document limits, ship reviewable artifacts—is what
I intend to bring here. Comfortable with Python, Git, Linux, structured data/YAML,
and using LLMs as controlled pipeline stages rather than ad-hoc chat.

Logistics
At least 30 hours/week for the Fall term. Pre-work:
[public repo link].

Thank you for your time.
```

---

## Cover-letter Q&A (if form splits questions)

### Why this project?

Because it sits at specs + structured data + LLM pipelines + evaluation—the same research hygiene I already practice—and the Spring public trail makes success criteria (recall, taxonomy, merge) concrete.

### Relevant skills?

Python tooling, experimental evaluation, LLM-in-pipeline discipline, YAML/structured configs, technical writing under a research mentor; rapid ramp on ISA parameter semantics and UDB schemas.

### What do you hope to get?

Ability to land machine-readable ISA parameter artifacts maintainers trust; deeper RISC-V spec literacy; experience shipping under RVI mentorship standards.

### Gaps?

Not a Spring mentee—will spend week 1 on handoff reproduction. Not claiming RTL expertise. Will learn UDB Ruby/mise workflows as needed.
