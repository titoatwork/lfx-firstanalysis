# Master plan — Uncatchable spine + beat every competitor at their game

**Status:** LOCKED strategy (2026-07-26)  
**Owner:** Ibteshamul Haque · GitHub `titoatwork`  
**Public monorepo (only):** https://github.com/titoatwork/lfx-firstanalysis  
**Upstream arena:** https://github.com/riscv/riscv-unified-db  
**LFX Part II:** https://mentorship.lfx.linuxfoundation.org/project/22296947-cecb-4a8f-8bcb-4f34710e9f66  
**Apply target:** 2026-07-31 · internal hard stop 2026-08-02 · official ~2026-08-05  

**Companions:**  
- Metrics truth: `riscv-param-extraction/docs/metrics.md`  
- Claim ledger: `application-packet/MEASURED-CLAIM-LEDGER.md`  
- Competition map: `COMPETITION-REPORT-2026-07-26.md`  
- Term plan: `application-packet/NINE-WEEK-PLAN.md`  
- Agent law: `AGENT-RULES.md`  

---

## 0. Doctrine (read every session)

### 0.1 Two layers — never invert priority

```text
SPINE  =  What Part II + mentors actually select for
          (uncatchable if we keep deepening it)

SPEAR  =  What competitors are flexing publicly
          (we beat them on their field WITHOUT becoming them)
```

| Rule | Meaning |
|------|---------|
| **Spine first** | If time fights, Apply + gold metrics + export + honesty win |
| **Spear second** | Challenge/CI/PR-optics are weapons, not the identity |
| **One public home** | All spear work lives under `lfx-firstanalysis` — **never** a second product repo |
| **No bulk UDB dump** | Spear for PR-swarm is *smart tiny* contribution, not spam |
| **Credit Spring** | @ishaan-arora-1 / PRs #1765–#1832 — never claim authorship |
| **Honest metrics only** | No invented numbers; every claim → ledger |
| **Coding challenge ≠ required** | Informal applicant pattern; we **supersede** it, we don’t pivot to it |

### 0.2 What “uncatchable spine” already is (protect and extend)

You already own the public Part II–shaped stack most applicants lack:

| Spine asset | Status | Why uncatchable (if maintained) |
|-------------|--------|----------------------------------|
| GT remeasure GT185 / GT223 | Done public | 72.9% / 64.2%, WARL 50% — Spring-faithful |
| Artifact A multi-model | Done public | 60 chunks, mini 32.2% vs Claude 72.9%, Jaccard 3.8% |
| Artifact B export | Done public | 83+20 schema-valid drafts |
| v3 WARL ablation | Done public **null** | Scientific honesty most kits skip |
| Manifests + metrics | Done public | Obj 3 discipline |
| Application packet | Done public | Essay modules + 9-week ↔ 5 objs |
| Correct merge ethics | Done | 0 bulk unsolicited param dump |

**Uncatchable means:** keep this denser, clearer, and more recomputable than anyone else’s story—not abandon it for badges.

### 0.3 Competitor “games” we must also win

| Game | Archetype | Poster children (public) |
|------|-----------|---------------------------|
| **G1 Challenge kit** | 2-snippet prompt+YAML+README | Anshul, Devadarsh, Harsh, Aryansri, Mansha, AYYAPPAN…, Adii, dhruvil, Hitesh, mishti… |
| **G2 CI / validate theater** | Badge, bad fixtures, fail-closed checks | Anshul (strongest) |
| **G3 Multi-frontier model names** | Opus/Sonnet/Gemini on demos | Anshul, Devadarsh, Harsh |
| **G4 Eval harness** | Precision/recall on small gold | Dipak |
| **G5 UDB engineering PRs** | Real upstream tooling/data PRs | **Ashutosh Saxena = @AlgoArtist06**, krrish, Purav, Teemo, RAJVEER… |
| **G6 Soft mentor-facing** | Issue/gist/Slack with mentors | hjaat |
| **G7 Incumbent continuity** | Built Spring | ishaan-arora-1, ankit-cybertron |
| **G8 Dark pool** | Apply only, no GitHub | Unknown |

---

## 1. Competitor-by-competitor: their game → your kill shot

### 1.1 You (baseline to defend)

| Keep doing | Never trade away for spear |
|------------|----------------------------|
| Full-corpus remeasure narrative | Challenge-only identity |
| Multi-model agreement science | Fake “beat Claude” claims |
| Bulk schema export path | Second public repo |
| Honest nulls (v3) | Silent failure hiding |
| 9-week plan ↔ 5 objectives | Generic “I love AI” essay |

---

### 1.2 Challenge-kit cohort (G1)

**Players:** AnshulPatil2005, devadarshnair, singhharsh1708, aryansri05, ManshaAgarwal716, AYYAPPANAYYANAN, Adii0906, dhruvil-codes, Hiteshsai007, mishtiagrawal02-cloud, GiGiKoneti (older), others.

**Their game:** Two ISA snippets → prompts v1–v3 → LLM → YAML → long README on hallucinations. Often titled “LFX coding challenge.” **Not verified as official LFX attachment.**

**Their ceiling:** Snippet scale; weak Spring gold story; weak bulk export.

**Your kill shot (spear that still serves spine):**

| Deliverable | Location | Beats them because |
|-------------|----------|-------------------|
| Challenge supersession pack | `riscv-param-extraction/challenge/` | Same demo **plus** link to full-corpus A/B/v3 |
| v1→v2→v3 prompts + raw/curated results | `challenge/prompts/`, `challenge/results/` | Match craft |
| Empty CSR negative control | Documented | Match Devadarsh/Harsh/Anshul |
| Side-by-side table | Challenge README | **Snippet metrics vs GT185/223/A** — they cannot match |
| Explicit FAQ | “Is coding challenge required?” → No; this pack exceeds it | Ends confusion |

**Do not:** make challenge the center of the monorepo.

---

### 1.3 AnshulPatil2005 (G1+G2+G3+G9 elite)

**Repo:** `AnshulPatil2005/riscv-param-extraction-challenge`  
**Game:** Best-in-class challenge engineering — multi-model (Sonnet/Opus/GLM), schema vendored from UDB, quote grounding, CI, bad fixtures, n=13 “recall”, markup robustness, hard negatives, scale/cost doc, UDB review culture citations.

**Kill shots:**

| His flex | Your overmatch |
|----------|----------------|
| CI badge | Monorepo CI: export tests + challenge validate + secret scan + frozen metric fixture |
| Quote grounding | Same + **AsciiDoc markup-aware** grounding mode (extend his robustness idea) |
| n=13 known-param recall | Keep honesty: that test is pretraining-leaky; **your** 60-chunk vs GT185 is the real bar; optionally run n=13 **as secondary** with his caveats stated louder |
| Multi-frontier on snippets | Snippet multi-model **and** stratified corpus multi-model |
| Cost doc | Cost doc for **full corpus** using your measured A/v3 tokens |
| Review culture refs | You already have Part I remeasure + dual-new review queue of 9 |

**Spine protection:** Never replace GT185 tables with n=13 as headline.

---

### 1.4 Devadarsh A Nair (G1 strong science)

**Repo:** `devadarshnair/RISCV-Parameter-Extraction`  
**Game:** Opus+Haiku, inspectable raw outputs, validate.py, UDB-shaped params, empty list discipline, BITS identity on README.

**Kill shots:**

| Flex | Overmatch |
|------|-----------|
| Dual-model consistency | Your Jaccard 3.8% on **60 chunks** is stronger science than 2-snippet agreement |
| Raw outputs kept | Already true in local UDB; publish **sample** + manifests (not full dump) |
| Empty-result discipline | Challenge pack CSR control + full-corpus “no invent” metrics |
| Brand | Irrelevant if metrics denser |

---

### 1.5 Harsh (@singhharsh1708) (G1 + taxonomy)

**Repo:** `singhharsh1708/param-extraction`  
**Game:** Strong parameter definition, WARL/WLRL triggers, Opus run, provenance, rejected_snippets.

**Kill shots:**

| Flex | Overmatch |
|------|-----------|
| Taxonomy prose | Your taxonomy is Spring-aligned (Part I) + **measured** WARL 50% scar + v3 null |
| Provenance fields | B drafts + dual-new review cards with provenance block |
| Single strong model | Multi-model disagreement as product insight |

---

### 1.6 Dipak (@dipak0000812) (G4 eval harness)

**Repo:** `riscv-spec-parameter-extractor`  
**Game:** Precision/recall/F1 harness, gold YAML for HPM counters, mock backend offline, clean methodology docs.

**Kill shots:**

| Flex | Overmatch |
|------|-----------|
| Eval harness UX | Document one-command remeasure of **Part I analyze.py** metrics (spine) |
| Offline mock | Already $0 GT path; advertise it |
| Scoped honesty | Keep full-manual ambition; optionally add **HPM section micro-eval** as nested demo under spine |

---

### 1.7 Lighter challenge clones (G1 long tail)

**Players:** aryansri05, Mansha, AYYAPPAN…, Adii, dhruvil, Hitesh, mishti, etc. (many repos updated mid–late July 2026).

**Game:** Same 2-snippet pattern, thinner docs.

**Kill shot:** One monorepo page “Landscape” is optional; better: **challenge pack + full corpus** so the long tail looks redundant. Do not 1:1 chase each clone.

---

### 1.8 Ashutosh Saxena = @AlgoArtist06 (G5 UDB engineer)

**Profile:** https://github.com/AlgoArtist06 · IIITDM Jabalpur · name Ashutosh Saxena  

**Recent UDB PRs (examples):**

| PR | Title | When |
|----|--------|------|
| #2115 | fix(idlc): short-circuit && and \|\| | 2026-07-25 |
| #2114 | test(udb-gen): orphaned cfg-header goldens | 2026-07-25 |
| #2112 | fix(generators): fail loudly on exception codes | 2026-07-25 |
| #2110 | feat(udb-gen): cfg-gdb-xml generator | 2026-07-25 |
| #2019 | fix(z3): anyOf for integer/boolean/string **parameters** | 2026-07-18 |

**His game:** High-volume **real UDB engineering** (IDL, generators, tests, Z3 param typing)—not a public extract challenge pack. Also active on other OSS (Rocket.Chat, cal.com, etc.).

**Why he matters:** Mentors who open UDB **see his name** in the PR firehose. Optics of “already contributing.”

**Kill shots (without becoming PR spam):**

| Do | Don’t |
|----|--------|
| **One** high-signal, correct, small PR or issue tied to **param quality / schema / extract reliability** after you understand the codepath | Open 5 cosmetic PRs in a day to match volume |
| In essay: distinguish **UDB engineering skill** (valuable) from **Part II selection evidence** (extract metrics + export + plan) | Imply PR count = Part II readiness |
| Optional: review #2019 carefully; cite as “parameter schema tooling still evolving” in plan | Compete on generator features you don’t need pre-apply |
| Membership → list note linking **your** metrics | Cold “please select me” |

**Spine protection:** His lane is Obj5-adjacent tooling; your lane is Obj1–4 prework. You win selection by **packet**, not by matching PR rate.

---

### 1.9 UDB PR swarm (G5 volume)

**Players:** krrishverma1805-web, Purav001, Teemooooooooo, RAJVEER42, Maanvi212006, etc.

**Game:** Many small UDB PRs / forks during application season.

**Kill shot:** Essay + README line:

> Pre-apply merges required: 0 bulk dumps. Selection for Part II is measured extraction quality and reviewable export, not PR volume.

Optional: **one** good first contribution post-apply or after list norms.

---

### 1.10 hjaat (G6 soft mentor-facing)

**Signal:** UDB issue #2053 (Spring work location) + gist on WARL/CSR misclassification + Slack with Baum.

**Game:** Thoughtful questions, mentor-visible, incomplete public packet.

**Kill shot:**

| Do | Don’t |
|----|--------|
| Deeper **published** WARL analysis (v3 null + planned C) | Only ask questions without artifacts |
| Dual-new 9 as review protocol demo | Duplicate his issue |
| After lists: technical substance note | Mentorship Slack design debate |

---

### 1.11 Incumbents ishaan / ankit (G7)

**Game:** Built Spring extraction (and parallel tracks).

**Kill shot (narrative only pre-apply):**

> I reproduced and stress-tested the public Spring system, measured multi-model disagreement and failed prompt-only WARL, and built the export/review path Part II needs for mergeable work—not a rewrite of Part I authorship.

If they re-apply: compete on **Part II delta**, not who wrote `extract.py`.

---

### 1.12 Dark pool (G8)

**Game:** Invisible.

**Kill shot:** Earliest complete **public** density + **submitted** application + recompute path. No other defense.

---

## 2. Architecture of work (where files go)

```text
titoatwork/lfx-firstanalysis/          ← ONLY public product home
├── README.md                          ← 5-min mentor path + two-path UX
├── application-packet/                ← SPINE apply
├── riscv-param-extraction/
│   ├── docs/metrics.md                ← SPINE truth
│   ├── manifests/                     ← SPINE Obj3
│   ├── export/ + drafts/              ← SPINE Obj4
│   ├── pipeline/                      ← SPINE agreement tools
│   ├── challenge/                     ← SPEAR G1–G3 (NEW)
│   │   ├── snippets/
│   │   ├── prompts/
│   │   ├── scripts/validate.py
│   │   ├── results/
│   │   └── README.md                  ← links UP to metrics §5–7
│   └── docs/robustness.md             ← SPEAR G2/G9 (NEW)
├── .github/workflows/ci.yml           ← SPEAR G2 (NEW)
└── riscv-unified-db/                  ← LOCAL ONLY (gitignore)
```

---

## 3. Workstreams (exhaustive)

### WS-S — Spine fortification (always on)

| ID | Task | Deliverable | API $ | When |
|----|------|-------------|------:|------|
| S0 | Key rotate + LFX deadline verify | User checklist | 0 | Immediate |
| S1 | Resume PDF with A/B/v3 bullets | Upload LFX profile | 0 | Immediate |
| S2 | Essay final from claim ledger | Form-ready text | 0 | Immediate |
| S3 | **Apply Part II** | Submitted/Pending | 0 | **Jul 31** |
| S4 | README mentor path ruthlessly clear | Root + package README | 0 | Pre-apply |
| S5 | One-command “recompute metric X” doc | `docs/REPRODUCE.md` | 0 | Pre-apply |
| S6 | Dual-new 9 review cards | `docs/review-queue-dual-new.md` | 0 | Pre/post apply |
| S7 | B provenance header standard | Export/docs | 0 | Post-apply OK |
| S8 | Membership → lists → calendar | Community | 0 | Parallel |
| S9 | List note (5 bullets + link) | After membership | 0 | Post-membership |
| S10 | Stratified frontier multi-model | metrics + manifest | $$ | Post-apply preferred |
| S11 | Artifact C CSR-context (pre-registered, leakage audit) | metrics + null-or-lift | $$ | Post-apply |
| S12 | Term: nine-week plan execution | If selected | — | Sep–Nov |

### WS-P — Spear: challenge supersession (G1)

| ID | Task | Beats | When |
|----|------|-------|------|
| P1 | Scaffold `challenge/` layout | All kits | Phase 1 |
| P2 | Snippets + v1–v3 prompts | All kits | Phase 1 |
| P3 | Runner + multi-model snippet results | G3 | Phase 1–2 |
| P4 | `validate.py` + bad_examples | G2 | Phase 1 |
| P5 | README: challenge **and** corpus table | Everyone | Phase 1 |
| P6 | FAQ: challenge not required | Confusion | Phase 1 |

### WS-C — Spear: CI / product rigor (G2)

| ID | Task | Beats | When |
|----|------|-------|------|
| C1 | GHA: unittest export | Anshul badge | Phase 1 |
| C2 | GHA: challenge validate + bad fixtures | Anshul | Phase 1 |
| C3 | Secret scan fail | Hygiene | Phase 1 |
| C4 | Optional frozen metrics unit check | Dingankar | Phase 2 |

### WS-R — Spear: robustness (Anshul G9)

| ID | Task | When |
|----|------|------|
| R1 | Markup-aware grounding modes | Phase 2 |
| R2 | Hard negatives (“should” ≠ param) | Phase 2 |
| R3 | Full-manual scale + cost doc | Phase 2 |

### WS-U — Spear: UDB visibility without spam (G5)

| ID | Task | Target | When |
|----|------|--------|------|
| U1 | Deep-read AlgoArtist06 #2019 / generators path | Understand parameter tooling | Parallel |
| U2 | **At most one** small, correct PR **or** high-quality issue | Optics + skill | After Apply or with list norms |
| U3 | Never match PR rate of AlgoArtist06 | Avoid wrong objective | Always |

### WS-M — Mentor/community (G6–G7)

| ID | Task | When |
|----|------|------|
| M1 | Calendar subscribe | Now |
| M2 | Lists after membership | When approved |
| M3 | Essay incumbent framing | Apply |
| M4 | Interview sheet (already drafted) | Polish |

---

## 4. Phased calendar

### Phase 0 — Immediate (hours)

- [ ] Rotate OpenAI key  
- [ ] Verify LFX Accepting + deadline  
- [ ] Resume PDF (personal fields)  
- [ ] Final essay pass vs claim ledger  

### Phase 1 — Pre-apply spine+spear (through Jul 31)

**Spine (must):** S1–S4, Apply S3  
**Spear (should):** P1–P6, C1–C3, S5–S6  

**Explicitly defer to post-apply:** S10–S11 full frontier / C experiment, R1–R3 if time-crunched, U2.

### Phase 2 — Post-apply buffer (Aug 1–14)

- R1–R3 robustness  
- S10 stratified multi-model if budget  
- S8–S9 community  
- U1–U2 smart UDB signal  
- Optional S11 Artifact C  

### Phase 3 — Warm period (Aug 15 – term)

- Iterate public monorepo  
- SIG presence  
- No unsolicited megadiff  

### Phase 4 — Term (if selected)

- Execute `application-packet/NINE-WEEK-PLAN.md`  
- Obj5 small reviewed PRs  
- Mentors redefine priorities  

---

## 5. Success criteria (“gapped them”)

### 5.1 Mentor 10-minute test (spine)

A mentor who only reads your monorepo can answer:

1. What Spring measured (with credit)?  
2. What you measured on mini vs Claude?  
3. What export path exists?  
4. What failed (v3)?  
5. What is the 9-week plan ↔ 5 objs?  

### 5.2 Challenge-kit 10-minute test (spear)

A skimmer comparing you to Anshul sees:

1. You have a challenge path **and** CI  
2. You **also** have full-corpus metrics they lack  
3. Your validate fails closed on bad fixtures  

### 5.3 UDB skimmer test (G5)

A skimmer comparing you to AlgoArtist06 sees:

1. He has more tooling PRs (conceded)  
2. You have the **selection packet for Part II** he doesn’t (publicly)  
3. Optionally you have **one** high-quality param-adjacent contribution  

### 5.4 Anti-criteria (failure modes)

| Failure | Avoid |
|---------|--------|
| Apply late while polishing CI | Phase 1 order |
| Second repo | Forbidden |
| Bulk param PR | Forbidden |
| Headline n=13 over GT185 | Forbidden |
| PR race with AlgoArtist06 | Forbidden |

---

## 6. Spend policy

| Work | Budget posture |
|------|----------------|
| Challenge snippet multi-model | Low (cents–$1) |
| Stratified corpus frontier | Medium; post-apply; hard cap user-set |
| Full 60 frontier | High; only with explicit go |
| Artifact C | ~A-scale; pre-register; post-apply |
| CI / docs / validate | $0 |

**Standing:** zero paid API without key + scoped go. `--retries 0`.

---

## 7. Scoreboard (target public position)

| Field | Target rank after plan |
|-------|------------------------|
| Spring remeasure + corpus multi-model | **#1** (defend) |
| Bulk schema export | **#1** (defend) |
| Honest ablation series | **#1** (defend) |
| Challenge kit + CI + validate | **#1 or #1-tied with Anshul** (attack) |
| Robustness suite | **#1-tied** (attack) |
| UDB PR volume | **Not competing** (refuse race) |
| UDB smart signal | **Visible once** (optional) |
| Community lists | **Present** after membership |
| Application packet | **#1 density** (defend + submit) |
| Incumbent authorship | **N/A** — win on Part II delta |
| Dark pool | **Mitigated** by early submit + public density |

---

## 8. Execution commands (for agents / future you)

| Command | Meaning |
|---------|---------|
| `GO SPINE apply` | Resume + essay polish + README mentor path; no spear expansion |
| `GO SPEAR challenge` | Build `challenge/` + validate + bad fixtures |
| `GO SPEAR ci` | GitHub Actions |
| `GO SPINE+SPEAR phase1` | README + challenge + CI + dual-new review cards; no full-corpus API |
| `GO SPINE science` | Stratified multi-model or C (needs spend go) |
| `push` | Only user word ships to GitHub |

**Default agent posture:** spine primary, spear secondary; no push/API without go.

---

## 9. One-paragraph strategy

We keep deepening the **uncatchable Part II spine**—Spring-faithful remeasurement, multi-model corpus science, schema-valid export, manifests, honest null results, and a 9-week plan mapped to the five official objectives—and we **also** beat challenge-kit and CI rivals by hosting a **superior challenge supersession pack and fail-closed automation inside the same monorepo**, while treating high-volume UDB engineers (e.g. Ashutosh Saxena / AlgoArtist06) as an **optics lane** answered with at most one excellent contribution and a clearer selection narrative, never a PR-rate war. Apply on time so the dark pool cannot beat an unfinished legend.

---

## 10. Immediate next step (recommended)

**`GO SPINE+SPEAR phase1`** after you confirm:

1. Key rotated (or accepted risk)  
2. Personal resume fields available or deferred  
3. No full-corpus API in phase1  

Then: implement challenge scaffold + CI + README path; you click Apply Jul 31.

---

*End master plan. Update when a major competitor archetype or official LFX requirement changes.*
