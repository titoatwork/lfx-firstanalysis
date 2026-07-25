# Plan — Become #1 for LFX Part II (param extraction)

**Status:** ACTIVE strategy (2026-07-26)  
**Owner:** Ibteshamul Haque · GitHub `titoatwork`  
**Goal:** Be the applicant mentors cannot rationally rank below anyone else — including **@AnshulPatil2005**.  
**Public home (only):** https://github.com/titoatwork/lfx-firstanalysis  
**Upstream:** https://github.com/riscv/riscv-unified-db  
**LFX:** Part II · Apply target **Jul 31** · hard stop **Aug 2** · official ~**Aug 5**

**Companions:** `PLAN-SPINE-AND-SPEAR.md` · `TIMELINE-SPINE-SPEAR.md` · `docs/metrics.md` · `application-packet/*` · `AGENT-RULES.md`

**Honesty clause:** No plan can *guarantee* #1 (dark pool, incumbents, mentor taste). This plan maximizes the probability that **public + apply evidence** puts you first. If time forces a trade: **Apply on time with a complete package beats a perfect package submitted late.**

---

## 0. What “#1” means (definition of done)

You are #1 when a mentor who spends **20 minutes** on the field concludes:

1. **You completed the shared coding challenge** at least as rigorously as Anshul (controls, grounding, fail-closed validation, multi-model).  
2. **You own Part II science** no challenge-only applicant has (GT remeasure, 60-chunk multi-model, export, honest nulls).  
3. **You have real upstream ink** (merged preferred; high-signal open PR acceptable if review is serious).  
4. **Your application is in** with essay/resume that credit Spring correctly and never overclaim.  
5. **You are present** on the right lists / calendar (not silent GitHub-only).

**#1 is not:** most commits · most PRs · loudest README · bare highest recall number.

---

## 1. Current baseline (facts — do not soft-pedal)

| You have (real) | Anshul has (real) | Gap |
|-----------------|-------------------|-----|
| GT223 + GT185 remeasure (72.9% / 64.2%, WARL 50%) | Snippet + n=13 (leaky; he admits it) | **You lead science** |
| Artifact A: mini 32.2% vs Claude 72.9%, Jaccard 3.8%, dual-new 9 | Multi-model on snippets + GLM insight | Different scale; both real |
| Artifact B: 83+20 schema-valid export | No bulk export path | **You lead Obj4 path** |
| v3 WARL null (honest) | Elite epistemics on overclaim | Tie on honesty culture |
| Application packet drafted | Challenge-first identity | Packet ready; Apply not in |
| **No** challenge pack | **Elite** challenge + CI | **Critical gap** |
| **No** UDB PR | **1 merged** (#1967) + open param PRs | **Critical gap** |
| Lists blocked / membership pending | Contributor association on UDB | Community gap |

**Current public rank:** ~**#7**.  
**After weak 4-gap close:** ~#3–#5.  
**This plan targets #1**, not “top five.”

---

## 2. Doctrine for #1 (overrides soft “challenge optional”)

```text
#1 = SPINE at full density  +  SPEAR at Anshul-parity or better  +  UPSTREAM signal  +  APPLY  +  PRESENCE
```

| Rule | #1 meaning |
|------|------------|
| **Spine non-negotiable** | Keep GT / A / B / v3 / manifests / claim ledger. Never trade them away. |
| **Challenge non-negotiable** | For #1, challenge is **required**, not optional spear. |
| **Upstream non-negotiable** | At least **one** high-signal UDB PR (merge preferred). Quality > count. |
| **One monorepo** | Challenge lives under `riscv-param-extraction/challenge/`. No second public product repo. |
| **No bulk dump** | Never open a 50-file param spam PR. |
| **No overclaim** | Never “beat Spring 36.8% / 72.9%” without equal footing. Anshul already framed that as amateur. |
| **Credit Spring** | @ishaan-arora-1 / #1765–#1832 always. |
| **Apply beats polish** | Jul 31 submit even if one stretch item slips; hard stop Aug 2. |
| **named** | 87 rows / 83 unique — never 97. |

---

## 3. How you become #1 vs Anshul (kill matrix)

Anshul wins today on: **challenge depth · CI · open-weight · 1 merge · param PR literacy**.

| His axis | Your overmatch (must ship) |
|----------|----------------------------|
| Challenge 2-snippet kit | **Same bar +** link every claim up to **60-chunk GT metrics** (table he cannot match) |
| n=13 existence 13/13 | Do **not** race 13/13 as headline. Optional secondary with **pretraining caveat louder than his**. Headlines: GT185/223 + agreement. |
| Markup robustness | Ship tag-aware grounding (Spring #1832 scar) — match or beat naive vs tag-aware demo |
| Hard negatives | Ship ≥2 “should ≠ param” controls |
| Fail-closed CI | Monorepo CI: challenge validate + export unit tests + bad fixtures |
| Open-weight GLM | ≥1 non-frontier model on snippets (mini already known; optional second open model if free/cheap) |
| Merged #1967 | **One** correct param-quality PR of your own (see §6) — small, reviewed, defensible |
| Epistemics | Keep v3 null + dual-new review queue; essay tone = “controls and limits first” |
| No bulk export | **You already have B** — make it the first thing after challenge in README |

**#1 narrative (one sentence mentors should remember):**

> He completed the shared challenge with fail-closed rigor *and* independently remeasured the Spring pipeline at full-corpus scale, shipped schema-valid export, published honest multi-model disagreement and a failed WARL prompt ablation, and landed a careful upstream param fix — with credit to Spring and no overclaim.

---

## 4. Workstreams (exhaustive)

### WS-1 — Challenge supersession (must = Anshul parity)

**Location:** `riscv-param-extraction/challenge/`

| ID | Deliverable | Acceptance criteria |
|----|-------------|---------------------|
| C1 | Snippets | Priv **19.3.1** CMO + Priv **2.1** CSR; sourced from local ISA manual; cite sections |
| C2 | Prompts v1→v2→v3 | Each version fixes a **measured** prior failure; v3 = schema + zero-ok + quotes |
| C3 | Results YAML + evidence | Schema-shaped params; sibling evidence/quotes; CSR snippet → **0** params |
| C4 | `validate.py` | Quote ⊆ source (ws-normalized); schema check; exit non-zero on fail |
| C5 | Bad fixtures | `HALLUCINATED_QUOTE` + `SCHEMA_INVALID` both **fail** |
| C6 | Multi-model | ≥2 models on both snippets (reuse OpenAI path if keys; document IDs/cost) |
| C7 | Hard negatives | ≥2 passages with “should/may” that correctly return **zero** |
| C8 | Markup robustness | ≥1 raw AsciiDoc case: naive fail / tag-aware pass (or document both) |
| C9 | Challenge README | Task, models, prompts, results, **snippet vs corpus table**, FAQ, Spring credit |
| C10 | Optional n=k | Thin known-param sanity **only** with pretraining-leak disclaimer; never headline |

**Done when:** stranger can clone monorepo, run validate, see green on good results + red on bad fixtures, and understand CSR=0.

### WS-2 — CI / product rigor (must)

| ID | Deliverable | Acceptance |
|----|-------------|------------|
| I1 | `.github/workflows/ci.yml` | On PR/push: export unit tests + challenge validate |
| I2 | Badge | README shows green CI |
| I3 | Secret scan | Fail if `.env` / key patterns committed |

### WS-3 — Spine fortification (must — already mostly done)

| ID | Deliverable | Acceptance |
|----|-------------|------------|
| S1 | Metrics stay honest | `docs/metrics.md` unchanged except real new runs |
| S2 | Mentor path README | 5-minute path: challenge → metrics → export → apply packet |
| S3 | Dual-new review cards | `docs/review-queue-dual-new.md` for the 9 names |
| S4 | REPRODUCE.md | One-command or short path to recompute a published metric |
| S5 | Essay + resume | Claim ledger only; Anshul-aware (controls first); personal fields filled |

### WS-4 — Upstream signal (must for #1)

| ID | Deliverable | Acceptance |
|----|-------------|------------|
| U0 | Read before write | Read #1967, #2009 thread, #2019 (AlgoArtist06), CONTRIBUTING, param schema |
| U1 | Pick **one** target | Param default/schema/docs bug **or** high-quality issue with reproduction |
| U2 | Open PR or issue | Correct, small, tests if needed, calm description |
| U3 | Engage review | Respond to maintainers; split if asked (Anshul/#2009 culture) |
| U4 | Never | Bulk YAML dump · cosmetic spam · rate-war with AlgoArtist06 |

**#1 preference order:** (1) merged small fix (2) open PR with serious review (3) excellent issue that maintainers thank.  
**Timebox:** do not block Apply waiting for merge. Open before or just after Apply; chase merge in warm period.

**Candidate themes (examples — verify still open before coding):**

- Param schema / default consistency (class of #1967)  
- Documentation of extraction → review → param YAML path  
- Markup/grounding note as issue if not PR-ready  
- One dual-new name investigated offline → **issue** with evidence (not dump)

### WS-5 — Apply + presence (must)

| ID | Deliverable | When |
|----|-------------|------|
| A1 | Rotate API key if pasted | Immediate |
| A2 | LFX deadline still Accepting? | Immediate |
| A3 | Resume PDF personal fields | Jul 26–27 |
| A4 | Essay final vs ledger + #1 narrative | Jul 28–30 |
| A5 | **Submit Apply** | **Jul 31** (hard stop Aug 2) |
| A6 | Membership follow-up | Parallel |
| A7 | Join sig-parameters + sig-unifieddb | When approved |
| A8 | Calendar subscribe | Parallel |
| A9 | Short list note (5 bullets + monorepo) | After lists (post-Apply OK) |

### WS-6 — Stretch for locking #1 (post-Apply if needed)

| ID | Deliverable | Notes |
|----|-------------|-------|
| X1 | Open-weight snippet leg | If not done pre-Apply |
| X2 | Stratified multi-model 15–25 chunks | Spend go required |
| X3 | Artifact C CSR-context | Pre-register; leakage audit; post-Apply |
| X4 | Interview 60s / 5m / 15m walkthrough | From monorepo only |

---

## 5. Phased calendar (to #1)

### Phase 0 — Today / tonight (hours)

| Who | Task |
|-----|------|
| You | Confirm LFX: challenge text on project page and/or after Apply prereqs; screenshot |
| You | Key rotate; membership status; personal resume fields |
| Agent (on go) | Scaffold `challenge/` + validate + snippets from local ISA |
| Both | Freeze #1 narrative sentence for essay/README |

### Phase 1 — Challenge + CI (Jul 26–28) — **#1 critical path**

| Day | Outcome |
|-----|---------|
| **26** | Snippets + prompts v1–v3 + validate skeleton + bad fixtures |
| **27** | Model runs (or offline-curated then live); CSR=0; hard negatives; CI green |
| **28** | Markup robustness; challenge README + monorepo mentor path; dual-new doc |

**Gate:** If challenge not CI-green by **evening Jul 28**, cut X-stretch; do **not** cut Apply.

### Phase 2 — Upstream + apply polish (Jul 28–30)

| Day | Outcome |
|-----|---------|
| **28–29** | U0–U2: one smart UDB PR/issue opened |
| **29** | Essay red-team (attribution, nulls, schema-valid ≠ correct, no bare recall flex) |
| **30** | Resume PDF final; form dry-run; sleep |

### Phase 3 — APPLY (Jul 31)

| Task |
|------|
| Submit Part II |
| Screenshot status |
| Save pasted answers locally |
| **No new experiments** |

### Phase 4 — Buffer (Aug 1–2)

Only: broken links, factual fixes, late submit if missed.  
**Aug 2 = hard stop for application in.**

### Phase 5 — Lock #1 (Aug 3 – Sep 14)

| Week focus |
|------------|
| Chase UDB review/merge |
| List note + SIG listen mode |
| Finish any challenge stretch (open-weight, n=k caveat) |
| Optional science (stratified multi-model / C) with spend go |
| Interview rehearsal |

---

## 6. Daily “what do I do” (cheat sheet)

| If today is… | Do this for #1 |
|--------------|----------------|
| **Before challenge exists** | Build challenge — nothing else is #1-critical |
| **Challenge green, no UDB** | One smart PR/issue |
| **Challenge + UDB, no Apply** | Essay/resume → **submit** |
| **Applied, lists closed** | Membership bump; then lists |
| **Everything shipped** | Polish narrative; rehearse walkthrough; do not thrash |

---

## 7. README / essay structure (mentor 10-minute path)

### Monorepo root README order

1. One-line: Part II prework + challenge + corpus science (credit Spring).  
2. **Path A — Coding challenge** (2 snippets, validate, CI).  
3. **Path B — Full-corpus science** (metrics tables; mini worse than Claude; v3 null).  
4. **Path C — Export** (83+20 schema-valid drafts).  
5. **Upstream** (link your UDB PR when it exists).  
6. **Apply packet** link.  
7. Limitations + what is *not* claimed.

### Essay order (paste modules)

1. Who you are + ≥30 h/wk + timezone.  
2. Understanding of Part II (5 objs).  
3. Challenge completed (controls, zero on CSR, grounding).  
4. Corpus remeasure + multi-model + export + null ablation (numbers from ledger).  
5. Upstream contribution (link).  
6. 9-week plan ↔ 5 objectives.  
7. Credit @ishaan-arora-1.  
8. What you will **not** do (bulk dump, overclaim).

---

## 8. Spend policy (API)

| Work | Budget posture |
|------|----------------|
| Challenge snippet multi-model | Low (cents–few $); **allowed with key + go** |
| Full 60 re-run | **No** unless explicit reopen |
| Stratified frontier / Artifact C | Post-Apply; hard cap you set |
| CI / docs / validate | $0 |

`--retries 0`. Rotate keys after chat paste.

---

## 9. Risk register

| Risk | Mitigation |
|------|------------|
| Chase Anshul feature-for-feature past Apply | Freeze challenge MVP Jul 28; Apply Jul 31 |
| UDB PR rejected | Still shows judgment; open better issue; don’t spam |
| Merge doesn’t land pre-review | Open + engage is enough for apply; merge is bonus |
| Membership delayed | **Apply anyway**; lists after |
| Overclaim in essay | Red-team vs claim ledger only |
| Second repo | Forbidden |
| PR rate war | Forbidden |
| Incumbent ishaan re-applies | Compete on Part II delta + challenge + export, not authorship |

---

## 10. Scoreboard — target after plan

| Field | Target rank |
|-------|-------------|
| Shared challenge + CI + controls | **#1 or tied with Anshul** |
| Full-corpus multi-model + GT | **#1** (defend) |
| Bulk schema export path | **#1** (defend) |
| Honest ablations | **#1** (defend) |
| UDB merge count | **Not competing on volume** — **≥1 quality signal** |
| Application density + on-time | **#1** |
| Overall mentor ranking | **#1** |

---

## 11. Execution commands (for agents)

| Phrase | Meaning |
|--------|---------|
| `GO #1 phase1` or `GO SPINE+SPEAR phase1` | Challenge scaffold + prompts + validate + CI + README path; no full-corpus API |
| `GO #1 challenge-runs` | Paid/local snippet multi-model (needs key + cap) |
| `GO #1 upstream` | Research + draft one UDB PR/issue (no open without confirm if risky) |
| `GO SPINE apply` | Essay/resume polish only |
| `push` | Ship to GitHub |
| `GO #1 post-apply` | Lists note, stretch science, interview pack |

**Default agent posture until go:** plan only; no push; no paid API; no second repo.

---

## 12. Success checkpoints (checkboxes)

### Must for #1 path

- [ ] Challenge: snippets + v1–v3 + results + CSR=0  
- [ ] Challenge: validate fail-closed + bad fixtures  
- [ ] Challenge: ≥2 models documented  
- [ ] Challenge: hard negatives + markup robustness  
- [ ] CI green on monorepo  
- [ ] Root README 5-min mentor path  
- [ ] Dual-new review queue doc  
- [ ] One UDB PR or high-signal issue opened  
- [ ] Essay + resume final (ledger-safe)  
- [ ] **Apply submitted** (≤ Jul 31 / Aug 2)  
- [ ] Membership → lists when possible  

### Stretch lock

- [ ] UDB PR merged or warmly reviewed  
- [ ] Open-weight snippet leg  
- [ ] List technical note posted  
- [ ] Interview walkthrough rehearsed  

---

## 13. One-paragraph strategy

Become #1 by **matching Anshul on the shared exam and fail-closed engineering**, **beating the field on Spring-faithful full-corpus measurement and schema-valid export**, **adding one careful upstream param contribution**, and **submitting a ledger-honest application on time** — without bulk dumps, second repos, or overclaiming recall. Spine stays the identity; challenge and upstream are no longer optional if the goal is first place.

---

## 14. Immediate next step

1. You: LFX portal check (challenge text + deadline) + resume personal fields.  
2. Agent: on **`GO #1 phase1`** / **`GO SPINE+SPEAR phase1`** — build challenge + CI in monorepo.  
3. Parallel track: pick UDB PR target after reading #1967/#2009.  
4. **Jul 31: Apply.**

---

*This plan is the #1 campaign lock. Prefer it over older “challenge optional / you lead packet” lines in handoffs. Update rank only when public evidence changes.*
