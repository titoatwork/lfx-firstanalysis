# LFX Mentorship — lfx-firstanalysis

**Owner:** Ibteshamul Haque · GitHub: [titoatwork](https://github.com/titoatwork)  
**Primary project:** [AI-assisted architectural parameter extraction – Part II](https://mentorship.lfx.linuxfoundation.org/project/22296947-cecb-4a8f-8bcb-4f34710e9f66)  
**Mentors:** Allen Baum, Ajit Dingankar · **Upstream:** [riscv/riscv-unified-db](https://github.com/riscv/riscv-unified-db)

**Single public home** for this campaign. Do not treat any other personal repo as the prototype product surface.

Part I (Spring) already built extract → analyze → spreadsheet on open PR branches (#1765–#1832, mentee [@ishaan-arora-1](https://github.com/ishaan-arora-1)). This repo **reproduces**, **measures**, and adds **export + pilot evidence** — it does not claim Part I authorship.

---

## 5-minute mentor path

| Step | Open |
|------|------|
| 1. **Coding challenge pack** | [riscv-param-extraction/challenge/](./riscv-param-extraction/challenge/) (2 snippets · validate · CSR=0 · CI) |
| 2. Measured corpus tables | [riscv-param-extraction/docs/metrics.md](./riscv-param-extraction/docs/metrics.md) |
| 3. Snippet vs corpus comparison | Challenge README **Path A / Path B** table |
| 4. Artifact A / pilot manifests | [manifests/](./riscv-param-extraction/manifests/) |
| 5. Artifact B export + drafts | [riscv-param-extraction/](./riscv-param-extraction/) (`export/`, `drafts/`) |
| 6. Apply packet (local) | [application-packet/](./application-packet/) |
| 7. Agent rules | [AGENT-RULES.md](./AGENT-RULES.md) · [AGENTS.md](./AGENTS.md) |

### Two paths (do not collapse them)

| Path | What it proves | What it is not |
|------|----------------|----------------|
| **A — Challenge** | Shared LFX coding task: optionality extract, grounding, schema YAML, zero on CSR negative control, fail-closed fixtures | Not full-manual recall |
| **B — Corpus science** | GT223/185 remeasure, 60-chunk multi-model, bulk export, honest WARL null | Not a substitute for the challenge pack |

Spring credit: [@ishaan-arora-1](https://github.com/ishaan-arora-1) / UDB PRs #1765–#1832.

### Snapshot numbers (do not invent beyond these)

| Item | Value |
|------|--------|
| Part I v2 remeasure (GT 185) | adj recall **72.9%**, class acc **88.4%**, WARL **50%** |
| Same vs live GT 223 | adj recall **64.2%** |
| Pilot machine.adoc | **model split**: gpt-4o (chunk_021) + gpt-4o-mini (chunk_020); ~**$0.05** |
| Artifact B | **83/83** named + **20/20** new schema-valid drafts |
| Artifact A multi-model | **Done** — gpt-4o-mini adj **32.2%** vs Claude **72.9%**; Jaccard **3.8%**; ~**$0.16** (see metrics §5) |
| named=yes in CSV | **87** rows / **83** unique — never claim 97 without recount |

Honest pilot claim: completed machine.adoc with **model split** because gpt-4o org TPM (30k) blocked the large chunk (~44k input). **Not** a pure gpt-4o full pilot.

---

## Repo map

| Path | Role |
|------|------|
| **[riscv-param-extraction/](./riscv-param-extraction/)** | Public prototype: metrics, export, challenge, manifests |
| **[riscv-param-extraction/challenge/](./riscv-param-extraction/challenge/)** | LFX coding-challenge supersession pack |
| [application-packet/](./application-packet/) | Part II essay / plan / claim ledger |
| [PHASE1-IMMERSION/](./PHASE1-IMMERSION/) | Phase 1 evidence pack (issues, PR dumps, deep study) |
| [PLAN-SOURCE-OF-TRUTH.md](./PLAN-SOURCE-OF-TRUTH.md) | Locked plan |
| [PROGRESS.md](./PROGRESS.md) | Done vs left |
| [AGENTS.md](./AGENTS.md) / [AGENT-RULES.md](./AGENT-RULES.md) | Grok entry + full session rules |
| [GITHUB-PRESENTATION.md](./GITHUB-PRESENTATION.md) | How work is shown on GitHub |

### Local only (not in this GitHub repo)

| Path | Why |
|------|-----|
| `riscv-unified-db/` | Full upstream clone + `lfx-*` branches — clone separately; gitignored |

---

## Agent / session files (Grok-first)

| Path | What |
|------|------|
| **[AGENTS.md](./AGENTS.md)** | **Grok auto-load** — short ops + current work |
| **[AGENT-RULES.md](./AGENT-RULES.md)** | Full agent law |
| **[HANDSOFF.md](./HANDSOFF.md)** | Hard no-touch list |
| **[RECURRING_MISTAKES.md](./RECURRING_MISTAKES.md)** | Known failure modes |
| **[.grok/rules/](./.grok/rules/)** | Context map, hard constraints, measured facts |
| [LEFTOVER-WORK.md](./LEFTOVER-WORK.md) | Canonical live leftovers |
| [PROGRESS.md](./PROGRESS.md) | Done vs left |
| **[application-packet/](./application-packet/)** | Local Part II essay, 9-week plan, resume content, claim ledger |
| [PHASE2-PLAN.md](./PHASE2-PLAN.md) | Phase 2 A/B path (historical + status) |
| **[HANDOFF-2026-07-26.md](./HANDOFF-2026-07-26.md)** | **Canonical** next-chat handoff (2026-07-26) |
| [NEXT-SESSION-PROMPT.md](./NEXT-SESSION-PROMPT.md) | Short kickoff paste |
| [PLAN-SPINE-AND-SPEAR.md](./PLAN-SPINE-AND-SPEAR.md) · [TIMELINE-SPINE-SPEAR.md](./TIMELINE-SPINE-SPEAR.md) | Spine+spear doctrine + calendar |
| [HANDOFF-NEW-SESSION.md](./HANDOFF-NEW-SESSION.md) | Older kickoff (may lag) |
| [PHASE1-CLOSEOUT.md](./PHASE1-CLOSEOUT.md) | Phase 1 closeout bridge |
| [PHASE1-STATUS.md](./PHASE1-STATUS.md) | Short status board |
| [riscv-param-extraction/AGENTS.md](./riscv-param-extraction/AGENTS.md) | Prototype package rules |

---

## Limitations

- Artifact A second model is **gpt-4o-mini** (not full gpt-4o); mini **underperforms** Claude on recall (honest ablation).  
- Pilot used two OpenAI models on machine.adoc (TPM).  
- Artifact B drafts are **DRAFT** — not unsolicited UDB merges.  
- Challenge `results/curated/` are **quote-grounded reference results** for CI; live multi-model API matrices are optional under `challenge/results/live/`.  
- Do **not** claim challenge-scale scores beat Spring corpus recall on equal footing.  
- Apply to Part II target **Jul 31** (hard stop Aug 2; official ~Aug 5).

---

## Apply window (plan)

Submit Part II **Jul 31–Aug 2** (not last day). Official deadline through **2026-08-05**.
