# FINAL DRAFT — Overmatch Anshul by a mile

**Status:** LOCKED execution blueprint (do not start code until user says **GO**)  
**Date:** 2026-07-26  
**Owner:** Ibteshamul Haque · GitHub `titoatwork`  
**Target rival:** @AnshulPatil2005 · [riscv-param-extraction-challenge](https://github.com/AnshulPatil2005/riscv-param-extraction-challenge) · UDB PRs #1967 (merged), #1968, #2009, #2023  
**Public home (ONLY):** https://github.com/titoatwork/lfx-firstanalysis  
**Never:** second product repo · bulk param dump PR · invent metrics · claim Spring authorship · named 97  

**Companions:** `PLAN-BECOME-NUMBER-ONE.md` · `PLAN-SPINE-AND-SPEAR.md` · `docs/metrics.md` · `application-packet/*` · claim ledger  

**Honesty:** “By a mile” is the **design standard** for every deliverable. Selection is not guaranteed. This draft is the full work order so execution can start without re-planning.

---

## 0. North star

**Mentor 20-minute verdict we want:**

> Anshul has an excellent challenge kit and a real UDB merge.  
> This applicant completed a **strictly stronger challenge product** (more controls, better packaging, CI, multi-model including open-weight), **plus** full-corpus Spring-faithful science he does not have (GT223/185, 60-chunk multi-model, bulk export, null ablation), **plus** **≥1 high-signal upstream contribution** (merge preferred), **plus** a complete on-time application — all in one monorepo, with credit to Spring and zero overclaim.

```text
OVERMATCH = (Anshul every axis, but stronger)  +  (our unique spine, louder)  +  (Apply + presence)
```

---

## 1. What Anshul has (complete inventory — we overmatch ALL of it)

| # | His asset | His bar (what “win” means) |
|---|-----------|----------------------------|
| A1 | Dedicated challenge framing | “LFX coding challenge submission” + task definition |
| A2 | 2 fixed snippets | Priv 19.3.1 CMO + Priv 2.1 CSR |
| A3 | Prompts v1→v2→v3 | Failure-driven iteration documented |
| A4 | Verbatim quote grounding | Mechanical string check |
| A5 | Schema-shaped YAML + vendored UDB schema | param_schema.json |
| A6 | Fail-closed bad fixtures | HALLUCINATED_QUOTE + SCHEMA_INVALID |
| A7 | CI badge + ci_check.sh | Green validate on push |
| A8 | Multi-model (3) | Sonnet + Opus + **GLM open-weight** |
| A9 | CSR = 0 negative control | Documented |
| A10 | Hard negatives | 2 “should” software-advice → zero |
| A11 | Markup robustness | Naive 1/3 vs tag-aware 3/3; #1832 story |
| A12 | n=13 known-param benchmark | 13/13 existence, 69% type fidelity + leak caveat |
| A13 | Scale/cost doc | 147 files, 845 chunks, ~$10.50 estimate |
| A14 | Modeling judgment prose | Split params (#2009 culture), SIG defer, no overclaim vs 36.8% |
| A15 | UDB **merged** PR #1967 | Param defaults restored |
| A16 | UDB open/closed PRs | #2009 PMLEN, #2023 Sorbet, #1968 Zbs closed |
| A17 | CONTRIBUTOR association | Name in UDB history |
| A18 | Repo product polish | Layout, how-to-run, score scripts |

**He does NOT have (we already lead — amplify):** full GT remeasure · 60-chunk multi-model Jaccard · bulk 83+20 export · v3 WARL null · formal apply packet.

---

## 2. Overmatch design principles

| Principle | Meaning |
|-----------|---------|
| **Same exam, higher grade** | Same 2 snippets + optionality task, then **extra layers he has, done denser** |
| **Never only parity** | Every Anshul feature gets a **+1** (more cases, stricter CI, better docs, or linked to corpus) |
| **Spine is the mile** | The distance is **challenge parity + corpus/export he cannot match in one README table** |
| **One monorepo** | `riscv-param-extraction/challenge/` + existing spine; no second GitHub product |
| **Upstream quality > volume** | 1–2 excellent PRs beat 5 cosmetics; target **merge** on at least one |
| **Epistemics first** | No “we beat Spring 72.9%/36.8%” without equal footing; copy his anti-overclaim discipline **and** apply it to our own numbers |
| **Apply on time** | Jul 31 (hard stop Aug 2) even if one stretch slips |

---

## 3. Work packages — Anshul axis → our overmatch

### WP-C — Challenge supersession (beat A1–A14, A18)

**Path:** `riscv-param-extraction/challenge/`

| ID | Deliverable | Anshul bar | **Our overmatch (+1)** | Done when |
|----|-------------|------------|------------------------|-----------|
| C0 | Challenge README | Long, excellent | **Two-path README:** Path A challenge · Path B corpus/export with **side-by-side table** he cannot fill | Mentor sees both in 5 min |
| C1 | Snippets | 2 fixed | Same 2 **from local ISA manual** + provenance (file, section, commit/hash of manual submodule) | Cited sources |
| C2 | Prompts v1–v3 | Failure-driven | Same **plus** v3.1 or explicit mapping: each version ↔ failure **observed in our raw logs** (not copied prose) | 3 prompts + failure log |
| C3 | Quote grounding | validate.py | Same **plus** tag-aware mode as default in validate | Both modes in CI |
| C4 | Schema YAML | Vendored schema | Vendor from UDB **with UPSTREAM-LICENSE** + pin schema commit SHA | Reproducible vendor |
| C5 | Bad fixtures | 2 | **≥4:** hallucinated quote, schema invalid, wrong name pattern, **CSR false-positive fixture** that must fail | 4 red fixtures |
| C6 | Results | 3 models dirs | ≥3 models: e.g. frontier or gpt-4o-mini + second + **open-weight (GLM or free alternative)**; raw + curated | Matrix table |
| C7 | CSR = 0 | Yes | Same **plus** automated test `assert_no_params(csr_snippet)` | Test in CI |
| C8 | Hard negatives | 2 | **≥4** passages (his 2 class + 2 more from manual) | 4/4 zero |
| C9 | Markup robustness | 3 cases, 1/3 vs 3/3 | **≥5** raw cases **or** his 3 + 2 harder; publish naive vs tag-aware table; link Spring #1832 | Table + script |
| C10 | Known-param bench | n=13 | **n≥15** OR n=13 **plus** separate **blind/candidate** slice from dual-new/gaps with **no** existence-100% headline; type-fidelity + leak caveats **louder** | Score script + caveats first in README |
| C11 | Scale/cost | Estimate | **His-style full manual estimate** + **our measured** A/v3 token costs side-by-side | `docs/scale_and_cost.md` |
| C12 | Score / disagreement | score.py | Auto table + **disagreement queue** (Sonnet/Opus-style split OR multi-model name set) | Script + sample output |
| C13 | Extract runner | extract.py | Runner with `--retries 0`, model pin, manifest write | Repro one command |
| C14 | Modeling cards | Prose on CMO split | **One-page** modeling notes: CACHE_* independence, max omit honesty, SIG defer — cite #2009 as **public** precedent not personal | Card in challenge/docs |

**Definition of “mile” for challenge:**  
A mentor who used Anshul’s repo as checklist finds **every box ticked and at least one stricter row** (more negatives, more markup cases, corpus table, louder caveats, more fixtures).

---

### WP-I — CI / product rigor (beat A7)

| ID | Deliverable | Overmatch |
|----|-------------|-----------|
| I1 | `.github/workflows/ci.yml` | challenge validate + bad fixtures must fail + export unit tests + frozen metric fixture optional |
| I2 | Badge on root + challenge README | Green |
| I3 | Secret scan | Fail on keys |
| I4 | `scripts/ci_check.sh` equivalent | One local command = CI |

---

### WP-S — Spine amplification (beat him on what he lacks)

| ID | Deliverable | Why it’s the “mile” |
|----|-------------|---------------------|
| S1 | Root README 5-min mentor path | Challenge → metrics → export → UDB PR → apply packet |
| S2 | `docs/metrics.md` unchanged except real runs | Keep 72.9 / 64.2 / 32.2 / 3.8% / 83+20 / v3 null |
| S3 | **Snippet vs corpus table** (mandatory) | His n=2/n=13 vs our 60-chunk GT — labels pretraining leak |
| S4 | Dual-new **9 review cards** | Full provenance template each name |
| S5 | `docs/REPRODUCE.md` | One path to recompute a published metric |
| S6 | Export polish | Provenance header standard on drafts; still no bulk dump |
| S7 | Manifest index | Pilot + A + v3 + challenge runs listed |

**Table every README must show (template):**

| Track | Scope | Key result | Caveat |
|-------|--------|------------|--------|
| Challenge snippets | 2 | CSR=0; CMO params; multi-model | Demo scale |
| Known-param re-derive | n=k | existence / type fidelity | Pretraining-leaky |
| Corpus multi-model | 60 chunks | mini 32.2% vs Claude 72.9%; Jaccard 3.8% | Second model is mini |
| GT remeasure | GT185/223 | 72.9% / 64.2%; WARL 50% | Credit Spring |
| Export | 83+20 | schema-valid | Not merge approval |
| Ablation | v3 WARL | null (WARL worse) | Need CSR context later |

---

### WP-U — Upstream (beat A15–A17)

**Goal:** Not PR spam. **Clearer param-quality signal than a single small default fix** if possible; at minimum **match merge + add open quality**.

| ID | Deliverable | Overmatch vs #1967 |
|----|-------------|-------------------|
| U0 | Deep-read | #1967, #1968 thread, #2009, #2019, #1048, CONTRIBUTING, param schema |
| U1 | **PR-A (must)** | Small, correct, **testable** fix — param defaults/schema/docs/IDL — quality ≥ #1967 |
| U2 | **PR-B or Issue-B (should)** | Param-modeling or extract-reliability signal (PMLEN-class thinking without copying #2009) |
| U3 | Engage review | Split if asked; respond in <24h; SIG-defer tone |
| U4 | Never | Bulk YAML from B drafts · rate war · cosmetic only |

**#1 upstream outcomes (priority):**

1. **1 merged** + 1 serious open (best)  
2. 1 merged only (parity+ on merge count if quality higher)  
3. 2 open with deep review (acceptable if Apply deadline bites)

**Timebox:** Open PR-A by **Jul 29**; do not block Apply waiting for merge. Chase merge Aug 1–14.

**Candidate themes (verify still valid before coding):**

- Param default/schema consistency (class of #1967)  
- Markup/grounding tooling note or small helper if upstream wants it  
- Documentation: how to validate param YAML against schema  
- One dual-new name as **issue with evidence package** (not dump)  
- Fail-closed validation idea as discussion only if not PR-ready  

---

### WP-A — Apply + presence

| ID | Deliverable | When |
|----|-------------|------|
| A1 | Membership Schedule A | **Today** (user) |
| A2 | Resume PDF personal fields | Jul 26–27 |
| A3 | Essay = overmatch narrative + ledger only | Jul 28–30 |
| A4 | **Apply Part II** | **Jul 31** (hard stop Aug 2) |
| A5 | Lists after membership | sig-parameters + sig-unifieddb |
| A6 | Calendar | Subscribe |
| A7 | List note (optional post-Apply) | 5 bullets + monorepo; calm |

**Essay spine (order):**

1. Who + ≥30 h/wk + timezone  
2. Part II understanding (5 objs)  
3. **Coding challenge completed** (controls, CSR=0, fail-closed, multi-model)  
4. **Beyond challenge:** GT remeasure, 60-chunk multi-model, export, v3 null  
5. **Upstream** link(s)  
6. 9-week plan ↔ 5 objs  
7. Credit @ishaan-arora-1 #1765–#1832  
8. What we refuse (bulk dump, overclaim, second repo)

---

### WP-X — Stretch locks (post-Apply if needed to widen the mile)

| ID | Deliverable |
|----|-------------|
| X1 | Stratified frontier multi-model 15–25 chunks (spend go) |
| X2 | Artifact C CSR-context pre-registered + leakage audit |
| X3 | Interview 60s / 5m / 15m from monorepo only |
| X4 | Second merged UDB PR only if natural |

---

## 4. Monorepo layout (target end state)

```text
titoatwork/lfx-firstanalysis/
├── README.md                          ← 5-min mentor path + overmatch table
├── application-packet/                ← spine apply
├── .github/workflows/ci.yml           ← SPEAR CI
└── riscv-param-extraction/
    ├── docs/
    │   ├── metrics.md                 ← spine truth (locked numbers)
    │   ├── REPRODUCE.md
    │   ├── review-queue-dual-new.md
    │   └── scale_and_cost.md          ← challenge-linked + measured A/v3
    ├── manifests/                     ← all runs
    ├── export/ + drafts/              ← B 83+20
    ├── pipeline/ + tests/
    └── challenge/                     ← SPEAR (Anshul supersession)
        ├── README.md
        ├── snippets/
        ├── prompts/                   ← v1 v2 v3 (+ notes)
        ├── schema/                    ← vendored + license + pin
        ├── scripts/                   ← extract, validate, score, ci_check
        ├── results/<model>/
        ├── tests/bad_examples/        ← ≥4
        ├── negative_controls/         ← ≥4
        ├── robustness/                ← markup modes
        ├── benchmark/                 ← known-param + caveats first
        └── docs/modeling-notes.md
```

Local only (never push): `riscv-unified-db/`

---

## 5. Calendar (execution after GO)

### Wave 0 — Hygiene (hours)

- [ ] Membership doc submitted (user — today)  
- [ ] Key rotated if exposed  
- [ ] LFX portal: challenge text + deadline confirmed  
- [ ] Resume personal fields listed  

### Wave 1 — Challenge MVP → Anshul parity (1–2 days)

- [ ] C1–C5, C7, C13 scaffold  
- [ ] First model results on both snippets  
- [ ] I1–I4 CI green  

**Gate:** CSR=0 + bad fixtures red + good results green.

### Wave 2 — Challenge overmatch (1–2 days)

- [ ] C6 multi-model + open-weight  
- [ ] C8 hard negatives ≥4  
- [ ] C9 markup  
- [ ] C10 benchmark with loud caveats  
- [ ] C0/C11/C12/C14 packaging  
- [ ] S1–S3 monorepo table  

**Gate:** README two-path; mentor checklist exceeds Anshul’s feature list.

### Wave 3 — Upstream (parallel from Wave 1 day 2)

- [ ] U0 read  
- [ ] U1 PR-A opened  
- [ ] U2 optional  
- [ ] U3 engage  

### Wave 4 — Apply freeze

- [ ] A2–A3 essay/resume  
- [ ] **A4 Apply Jul 31**  
- [ ] push only on user **push**  

### Wave 5 — Lock the mile (Aug+)

- [ ] Merge chase  
- [ ] Lists + optional note  
- [ ] X stretch if needed  

---

## 6. Acceptance tests (“overmatched by a mile”)

A neutral reviewer must answer **YES** to all:

| # | Question |
|---|----------|
| 1 | Does this repo complete the **same coding challenge** as Anshul? |
| 2 | Does it have **fail-closed** validation with **more** bad fixtures than his 2? |
| 3 | Is **CI green** with challenge + export tests? |
| 4 | Are there **hard negatives** and **markup robustness** at least as strong? |
| 5 | Is there **≥2 models**, including an **open-weight or clearly cheaper second model**, on snippets? |
| 6 | Is there a **snippet vs full-corpus** table linking to GT185/223 and Jaccard? |
| 7 | Is there **bulk export** evidence (83+20) he lacks? |
| 8 | Is there an **honest null** (v3 WARL) he lacks? |
| 9 | Is there **≥1 UDB PR** (merged preferred) with real review? |
| 10 | Is **Apply submitted** with ledger-safe claims and Spring credit? |
| 11 | Does the README **refuse** bare “we beat Spring recall” overclaim? |

If 1–5 fail → not overmatch.  
If 1–5 pass but 6–8 fail → parity kit, not “by a mile.”  
If 1–11 pass → **mission standard met.**

---

## 7. Spend policy

| Work | Cap posture |
|------|-------------|
| Challenge multi-model + open-weight | Low; key + explicit go; `--retries 0` |
| Full 60 re-run | Forbidden unless reopen |
| Stratified / C | Post-Apply; hard cap |
| CI/docs | $0 |

---

## 8. Forbidden moves (lose the mile)

| Do not | Why |
|--------|-----|
| Second public challenge repo | Splits story; past incident |
| Copy Anshul results YAML as ours | Fraud |
| Bulk B drafts as UDB PR | Mentors reject; anti-strategy |
| Headline n=k 100% as beating Spring | He already framed this as overclaim |
| Claim mini beat Claude | False |
| Claim v3 fixed WARL | False (null) |
| named 97 | False (87/83) |
| Author Spring Part I | Credit ishaan |
| Delay Apply for perfect CI | Dark pool / deadline risk |
| PR rate war with AlgoArtist06 | Wrong game |

---

## 9. Agent execution commands (after this draft)

| User phrase | Starts |
|-------------|--------|
| **`GO OVERMATCH wave1`** | Challenge scaffold + validate + snippets + CI (no full-corpus API) |
| **`GO OVERMATCH wave2`** | Multi-model/negatives/markup/benchmark/README (API if key+cap) |
| **`GO OVERMATCH upstream`** | U0–U1 research + draft PR (open only with confirm if needed) |
| **`GO SPINE apply`** | Essay/resume polish |
| **`push`** | Ship to GitHub |
| **`GO OVERMATCH all`** | Wave1 then wave2 sequentially (still no push; still no spend without key) |

Default until GO: **no code, no push, no API.**

---

## 10. One-page strategy

Anshul’s lead is **challenge product + CI + controls + multi-model + one UDB merge**.  
We overmatch by building a **strictly denser challenge** (more fixtures, negatives, markup cases, louder caveats, open-weight, disagreement routing) **inside the monorepo**, wiring every challenge claim to **corpus science and bulk export he does not have**, landing **careful upstream work**, and **submitting Apply on time** with Spring credit and no overclaim.  
The “mile” is not louder README adjectives — it is **Anshul’s checklist completed better, plus a second checklist only we can fill.**

---

## 11. Immediate next step

1. User: finish **membership document today**; gather resume personal fields.  
2. User: confirm LFX challenge text if visible on portal.  
3. User: read this file once; mark any WP to cut.  
4. User: say **`GO OVERMATCH wave1`** (or `GO OVERMATCH all`) to start implementation.

---

*End final draft. Execution begins only on explicit GO.*
