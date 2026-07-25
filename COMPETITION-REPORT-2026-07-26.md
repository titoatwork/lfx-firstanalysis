# Competitive landscape report — LFX Part II (param extraction)

**Date:** 2026-07-26  
**Target project:** AI-assisted extraction of architectural parameters from RISC-V specifications – Part II  
**Upstream arena:** [riscv/riscv-unified-db](https://github.com/riscv/riscv-unified-db)  
**Your public home:** [titoatwork/lfx-firstanalysis](https://github.com/titoatwork/lfx-firstanalysis)  

**Honesty first:** LFX applications are **private**. Nobody outside mentors/LFX can see who applied or how strong private essays are. This report ranks **public prework signals** only. The “hidden competitor” section is about **dark-pool risk**, not named people.

---

## 1. Target repo snapshot (live API, 2026-07-26)

| Metric | Value |
|--------|------:|
| Stars | **198** |
| Forks | **211** |
| Open issues+PRs | **381** |
| Watchers (API) | 8 |
| Last push | 2026-07-25 |
| Language | Ruby monorepo (+ Python param_extraction on PR branches) |

**Interpretation:** High-traffic OSS. July application season still shows forks/PRs. **Most activity is not Part II prework** (data fixes, generators, renovate, general UDB).

**Spring Part I surface (still open PRs #1765–#1832):** authored primarily by **@ishaan-arora-1**. That is the bar to understand, not the person you “beat on GitHub spam.”

---

## 2. How to read competition (scoring rubric)

Mentors (Baum / Dingankar) care about different things. Public proxies map roughly as:

| Dimension | Weight for *selection* | What “strong” looks like |
|-----------|------------------------|---------------------------|
| **D1** Understand Spring pipeline | High | Cite PRs #1765–#1832; taxonomy; adjusted recall; WARL scar |
| **D2** Reproduce metrics on real gold | High | GT185 / live gold numbers with methodology |
| **D3** Multi-model / ablation discipline | High | Same corpus, honest worse results, agreement |
| **D4** UDB-shaped export / schema | High | Real `param_schema`, draft YAML, validation |
| **D5** Challenge-kit craft (2-snippet) | Medium | Many applicants ship this; polished ≠ full pipeline |
| **D6** Upstream UDB PRs | Medium–low pre-apply | Small data PRs help optics; bulk spam hurts |
| **D7** Community (lists/SIG/Slack) | Medium | Hard to see publicly until you post |
| **D8** Essay / 9-week plan | High (private) | Invisible until apply |

**Score scale used below:** 1–5 per dimension (public evidence only). **Overall** is not a seat probability.

---

## 3. Cohort map

```text
                    ┌─────────────────────────────┐
                    │  Dark pool (private apps)   │  ← unknown size
                    └─────────────┬───────────────┘
                                  │
     ┌────────────────────────────┼────────────────────────────┐
     ▼                            ▼                            ▼
 Challenge-kit only         Full-corpus / UDB path        Upstream PR swarm
 (2 snippets)               (Spring-scale work)           (UDB data PRs)
     │                            │                            │
  many public repos          YOU + few others            krrish, Purav, …
```

---

## 4. Competitor dossiers (public)

### Tier 0 — Incumbents / mentors (not “competitors,” but shape the field)

#### @ishaan-arora-1 (Spring mentee)
| | |
|--|--|
| **Signal** | Full LFX phase issues #1747–#1754; open PRs #1765–#1832; ground truth, extract, analyze, spreadsheet |
| **Strength** | Built the system Part II extends; deepest domain continuity |
| **Weakness as applicant** | Unknown if re-applying; if yes, highest domain continuity risk |
| **vs you** | You **must credit** them; you cannot out-Spring them on authorship. You can out-them on **independent multi-model ablation + export packaging + honest null** if they do not re-apply with new work. |
| **Public Part II prework score** | N/A (Spring author) |

#### @ankit-cybertron (Spring parallel track)
| | |
|--|--|
| **Signal** | Parallel chunk/classifier-style UDB work; fork of UDB |
| **Strength** | Already inside param-extraction engineering culture |
| **Risk** | If re-applying, high |
| **vs you** | Same as ishaan: credit / don’t claim their work |

#### Mentors / maintainers (dhower-qc, jordancarlin, adingank-qualcomm, …)
Not competitors. They judge merge quality and may prefer **small reviewable PRs** over huge generated dumps.

---

### Tier A — Strong *public* Part II–aligned prework

#### You — Ibteshamul Haque (@titoatwork)
| | |
|--|--|
| **Repo** | https://github.com/titoatwork/lfx-firstanalysis |
| **What shipped** | Phase 1 immersion; GT remeasure **72.9% / 64.2% / WARL 50%**; pilot model-split; Artifact A gpt-4o-mini 60 chunks (**32.2%** vs Claude **72.9%**, Jaccard **3.8%**); Artifact B **83+20** schema-valid drafts; v3 WARL prompt ablation **null** (3/24→2/24); application packet + 9-week plan |
| **Strengths** | Closest public match to **official Part II objectives** (repro, multi-model, export, manifests, honest science). Single monorepo narrative. Credit to Spring. |
| **Weaknesses** | Limited **upstream** UDB merge history; membership/SIG not yet visible; original CSR-context C not run; resume personal fields still incomplete until you finish PDF |
| **D1–D5 scores** | D1:5 D2:5 D3:5 D4:5 D5:3 (pilot/challenge not the main product) D6:2 D7:2 → **public prework ~ strongest observed** |

#### @AnshulPatil2005 — `riscv-param-extraction-challenge`
| | |
|--|--|
| **Repo** | https://github.com/AnshulPatil2005/riscv-param-extraction-challenge |
| **What shipped** | Extremely polished **coding-challenge** kit: v1–v3 prompts, multi-model (Sonnet/Opus/GLM), mechanical quote grounding + schema validate + CI, n=13 “recall” benchmark, markup robustness tests, hard negatives, scale/cost doc, UDB PR cultural references (#2009, etc.) |
| **Strengths** | Best **engineering polish** among challenge kits; mentor-readable anti-hallucination story; understands UDB review culture; multi-model **on challenge scale** |
| **Weaknesses** | Center of gravity is **2-snippet + n=13 known params**, not full Spring 60-chunk corpus remeasure; self-notes that n=13 is **not blind** (pretraining leakage risk); does not replace full-pipeline reproduction metrics like yours |
| **Threat** | **Highest among pure challenge kits** — essay could be excellent; mentors who overweight challenge craft may prefer this |
| **Scores** | D1:4 D2:3 D3:4 D4:4 D5:**5** D6:2–3 → **Tier A challenge specialist** |

#### @devadarshnair — `RISCV-Parameter-Extraction`
| | |
|--|--|
| **Repo** | https://github.com/devadarshnair/RISCV-Parameter-Extraction |
| **What shipped** | Challenge submission: Opus + Haiku, v1→v3 prompts, raw outputs kept, validate.py, UDB-shaped params, empty-result discipline on CSR snippet, BITS Pilani identity on README |
| **Strengths** | Clean scientific writeup; dual-model consistency; evidence quotes; knows empty answer is valid |
| **Weaknesses** | Snippet-scale only; no public full-corpus remeasure; no large exporter suite like your B |
| **Threat** | High among challenge tier; strong essay risk |
| **Scores** | D1:3–4 D2:2 D3:3–4 D4:3–4 D5:**5** |

#### @singhharsh1708 — `param-extraction`
| | |
|--|--|
| **Repo** | https://github.com/singhharsh1708/param-extraction |
| **What shipped** | Claude Opus 4.8 challenge kit; strong taxonomy (WARL/WLRL triggers); v1–v3 prompts; live_run.yaml; negative control on CSR snippet |
| **Strengths** | Domain language quality; reproducible runner; confidence/provenance fields |
| **Weaknesses** | Snippet-scale; less multi-model breadth than Anshul; less full-pipeline than you |
| **Threat** | High challenge tier |
| **Scores** | D1:3–4 D2:2 D3:2–3 D4:3 D5:**5** |

#### @dipak0000812 — `riscv-spec-parameter-extractor`
| | |
|--|--|
| **Repo** | https://github.com/dipak0000812/riscv-spec-parameter-extractor |
| **What shipped** | **Different angle:** evaluation harness + gold YAML for HPM counters §3.1.10–12; mock/gemini/openai backends; precision/recall/F1; offline runnable |
| **Strengths** | Metrics mindset (Dingankar-friendly); gold construction docs; scoped honestly |
| **Weaknesses** | Narrow section scope (8 params), not full Spring pipeline or multi-model corpus story |
| **Threat** | Medium–high if mentors love eval harnesses; less “I own Part II stack” narrative than you |
| **Scores** | D1:3 D2:4 (local gold) D3:2 D4:2 D5:3 |

---

### Tier B — Visible challenge / lighter kits

| Handle | Repo | Notes | Threat |
|--------|------|-------|--------|
| **@aryansri05** | `riscv-parameter-extraction-challenge` + LFX-named repo | Gemini 2.5 Flash-Lite; solid prompt evolution; short; snippet-only | Medium |
| **@ManshaAgarwal716** | `riscv-architectural-parameter-extractor` | Llama 3.3 70B via Groq; clean student project structure; weaker UDB depth | Medium–low |
| **@GiGiKoneti** | `riscv-param-agent` | Older (Feb 2026) challenge framing | Low–medium |
| **@lucifer4073** | `riscv_parameter_extraction` | Larger size historically; less clear Fall 2026 positioning | Low–medium |
| **@DEEP-600**, **@saurabh12nxf**, **@ShashankShenoy** | similarly named repos | Mostly challenge-era or thin | Low |

---

### Tier C — UDB PR swarm / optics (often *wrong arena*)

These people are **active on UDB** but public signal is **general contribution**, not full Part II measurement packets:

| Handle | Signal | Part II threat |
|--------|--------|----------------|
| **krrishverma1805-web** | Frequent UDB PRs | Low–medium unless they also have private strong app |
| **Purav001**, **AlgoArtist06**, **RAJVEER42**, **Teemooooooooo** | Param-related or data PRs | Low–medium for *this* seat (wrong objective function if only PR spam) |
| **Maanvi212006** | UDB fork + CVA6; comment activity | Medium if dual-track; not clearly full extract packet |
| **hjaat** | Issue [#2053](https://github.com/riscv/riscv-unified-db/issues/2053) + gist on WARL misclassification; Slack with Baum | **Interesting medium** — thoughtful, mentor-facing questions, may have strong private writeup |

**Honest rule:** Do **not** treat PR count as Part II ranking. Your plan correctly parks “UDB swarm.”

---

### Hidden / dark-pool competitors (real, not listable)

| Type | Why dangerous | What you can do |
|------|---------------|-----------------|
| **Silent strong applicants** | Applied with excellent essay, no public repo | Your public repo is the antidote |
| **Industry/internals** | Qualcomm-adjacent students, SIG regulars | Quality + realism of 9-week plan |
| **Spring re-applicants** | Continuity advantage | Credit Spring; show Part II delta (A/B/v3) |
| **Challenge-only stars with killer essays** | Anshul/Devadarsh-class + private polish | Your full-corpus + export story must be crystal clear in **LFX form** |
| **Applicants who never forked UDB** | Invisible on GitHub | Inevitable; don’t invent counts |

**Calibrated guess (not a fact):** tens of applications; **~10–25** serious enough to shortlist; **1 paid seat**.

---

## 5. Head-to-head: You vs strongest public rivals

| Capability | **You** | **Anshul (challenge elite)** | **Devadarsh / Harsh** | **Dipak (eval harness)** |
|------------|---------|------------------------------|------------------------|---------------------------|
| Full Spring pipeline remeasure | **Yes (72.9/64.2)** | Partial / cultural | No | Section-scoped |
| 60-chunk multi-model | **Yes (mini vs Claude)** | 3 models on **snippets** | 2 models on snippets | Optional backends, small scope |
| Honest negative ablation | **Yes (v3 WARL)** | Yes (model splits, overclaim warnings) | Yes (empty CSR) | N/A |
| Schema-valid bulk export | **83+20** | Per-param YAML + schema | UDB-shaped few params | Gold-focused, not bulk export |
| Challenge-kit polish / CI | Medium | **Best-in-class** | Strong | Strong tooling |
| Upstream UDB PR history | Low | Some cultural refs | Low | Low |
| Application packet public | **Yes** | Challenge README ≈ packet | Challenge README | Docs/methodology |

**Bottom line of matchup:**  
- Against **challenge kits**, you win **scale + Spring fidelity + export path**.  
- Against **Anshul**, you must not look “less rigorous”; your metrics/manifests must stay as clean as their validate/CI story.  
- Against **incumbents**, public prework cannot neutralize continuity if they re-apply hard—your essay must still be impeccable.

---

## 6. Ranking tables

### 6A. Ranking by *public Part II prework fitness* (what I can see)

| Rank | Who | Why |
|-----:|-----|-----|
| **1** | **You (@titoatwork)** | Only public packet that clearly combines Spring remeasure + full-corpus multi-model + schema export + honest WARL null + apply docs |
| **2** | **@AnshulPatil2005** | Best challenge engineering; multi-model; UDB culture literacy; strongest rival *if* mentors overweight challenge kits |
| **3** | **@devadarshnair** | Clean dual-model challenge science |
| **4** | **@singhharsh1708** | Strong domain prompt + Opus run |
| **5** | **@dipak0000812** | Eval-harness / metrics discipline |
| **6** | **@aryansri05** | Competent lighter challenge |
| **7** | **@hjaat** | Soft signal (issue+gist+mentor Slack); incomplete public packet |
| **8–N** | UDB PR swarm / thin challenge clones | Wrong objective or shallow |

### 6B. Ranking by *challenge-kit craft only*

| Rank | Who |
|-----:|-----|
| 1 | Anshul |
| 2 | Devadarsh ≈ Harsh |
| 3 | Aryansri / Mansha / others |
| — | You (not competing primarily in this lane) |

### 6C. Ranking by *upstream UDB contribution volume*

| Rank | Who |
|-----:|-----|
| 1–3 | Active UDB PR authors (krrish, AlgoArtist, Teemo, …) |
| — | You / most challenge kits (low) |

**Do not optimize for 6C pre-apply.**

### 6D. Seat probability ranking

**Not published. Not rankable honestly.** Anyone claiming “you are #1 for the seat” is guessing.

---

## 7. Strategic implications (honest)

### What you already have
- Correct **objective function** for Part II (not PR spam).  
- Public **numbers mentors can recompute**.  
- A story that includes **failure** (mini worse; v3 null)—signals maturity.

### Where you can still lose
1. **Essay weaker than Anshul’s README** (if form favors challenge narrative).  
2. **Incumbent re-application**.  
3. **Dark-pool** applicant with private Claude full-run + SIG presence.  
4. **Not applying on time** / incomplete resume.  
5. **Membership silence** misread as low engagement (mitigate with calendar + apply anyway).

### What not to do
- Chase UDB PR count.  
- Re-run more models for optics.  
- Attack competitors publicly.  
- Claim 97 named params or Spring authorship.

### Highest-leverage next moves (still)
1. Submit strong application (Jul 31).  
2. Resume PDF with A/B/v3 bullets.  
3. Membership → lists when approved.  
4. Optional: one calm technical list note after lists.  
5. Defer CSR-context C until after submit.

---

## 8. One-sentence competitive position

> **Among publicly visible Fall 2026 Part II prework, your monorepo is the most complete Spring-faithful measurement and export packet; the main open risk is polished challenge-kit applicants (especially Anshul) plus an unknowable private dark pool—not the UDB PR swarm.**

---

## 9. Sources (public)

- GitHub API / repo pages for UDB and competitor repos (2026-07-26)  
- Competitor READMEs (Anshul, Devadarsh, Harsh, Mansha, Dipak, Aryansri)  
- UDB issue #2053 (hjaat)  
- Local prior analysis: `COMPETITION-UDB-ANALYSIS.md` (2026-07-19)  
- Your metrics: `riscv-param-extraction/docs/metrics.md`

*This file is competition strategy — keep local unless you explicitly want it on GitHub.*
