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
| 1. Measured tables | [riscv-param-extraction/docs/metrics.md](./riscv-param-extraction/docs/metrics.md) |
| 2. Pilot manifest (models, tokens, cost, limitations) | [riscv-param-extraction/manifests/pilot-machine-adoc.md](./riscv-param-extraction/manifests/pilot-machine-adoc.md) |
| 3. Artifact B code + drafts | [riscv-param-extraction/](./riscv-param-extraction/) |
| 4. How presentation is locked | [GITHUB-PRESENTATION.md](./GITHUB-PRESENTATION.md) |

### Snapshot numbers (do not invent beyond these)

| Item | Value |
|------|--------|
| Part I v2 remeasure (GT 185) | adj recall **72.9%**, class acc **88.4%**, WARL **50%** |
| Same vs live GT 223 | adj recall **64.2%** |
| Pilot machine.adoc | **model split**: gpt-4o (chunk_021) + gpt-4o-mini (chunk_020); ~**$0.05** |
| Artifact B | **83/83** named + **20/20** new schema-valid drafts |
| Artifact A multi-model | **Not run** |
| named=yes in CSV | **87** rows / **83** unique — never claim 97 without recount |

Honest pilot claim: completed machine.adoc with **model split** because gpt-4o org TPM (30k) blocked the large chunk (~44k input). **Not** a pure gpt-4o full pilot.

---

## Repo map

| Path | Role |
|------|------|
| **[riscv-param-extraction/](./riscv-param-extraction/)** | Public prototype: metrics, pilot manifest, Artifact B |
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
| **[HANDSOFF.md](./HANDSOFF.md)** | Hard no-touch list |
| **[RECURRING_MISTAKES.md](./RECURRING_MISTAKES.md)** | Known failure modes |
| **[.grok/rules/](./.grok/rules/)** | Context map, hard constraints, measured facts |
| [AGENT-RULES.md](./AGENT-RULES.md) | Full session law |
| [LEFTOVER-WORK.md](./LEFTOVER-WORK.md) | Canonical live leftovers |
| [PHASE2-PLAN.md](./PHASE2-PLAN.md) | Artifact A plan |
| [HANDOFF-NEW-SESSION.md](./HANDOFF-NEW-SESSION.md) | New-chat kickoff paste |
| [NEXT-SESSION-PROMPT.md](./NEXT-SESSION-PROMPT.md) | Short kickoff pointer |
| [HANDOFF-NEXT-SESSION.md](./HANDOFF-NEXT-SESSION.md) | Pilot-budget handoff (historical) |
| [PHASE1-CLOSEOUT.md](./PHASE1-CLOSEOUT.md) | Phase 1 closeout bridge |
| [PHASE1-STATUS.md](./PHASE1-STATUS.md) | Short status board |
| [riscv-param-extraction/AGENTS.md](./riscv-param-extraction/AGENTS.md) | Prototype package rules |

---

## Limitations

- Artifact A (full multi-model vs Claude) not run.  
- Pilot used two OpenAI models on machine.adoc (TPM).  
- Artifact B drafts are **DRAFT** — not unsolicited UDB merges.  
- Apply to Part II only after A+B evidence (plan: Jul 31–Aug 2).

---

## Apply window (plan)

Submit Part II **Jul 31–Aug 2** (not last day). Official deadline through **2026-08-05**.
