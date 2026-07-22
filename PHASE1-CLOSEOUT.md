# Phase 1 — Closeout & next-session handoff

**Date closed (this session):** 2026-07-21  
**Plan lock:** `PLAN-SOURCE-OF-TRUTH.md` (identity/emails live there only)  
**User Gmail (membership):** `ibteshamulhaque01@gmail.com`  
**UPES (earlier list attempt):** `ibteshamul.123421@stu.upes.ac.in`

This file is the **single entry point** for any new session continuing Phase 1 leftovers or starting Phase 2.

---

## Phase 1 verdict

| Track | Status | Notes |
|-------|--------|--------|
| **Technical immersion** | **COMPLETE** for this session | Clone, PRs, read pack, GT, metrics — done |
| **Community immersion** | **IN PROGRESS** | Membership submitted; list/Slack/calendar/LFX profile need user + roster |
| **Pilot extract** | **READY TO RUN** | Needs user API key; commands below |

**Do not re-clone UDB or re-fetch PRs** unless missing.  
**Do not re-run full deep research from zero** — use `PHASE1-IMMERSION/DEEP-STUDY-COMPLETE.md`.

---

## 1. Technical — DONE (facts)

### 1.1 Repository

| Item | Value |
|------|--------|
| Path | `Desktop\LFX-Mentorship\riscv-unified-db\` |
| Branch | `lfx-1832` (fullest Part I tree) |
| Local PR branches | `lfx-1765`, `lfx-1766`, `lfx-1791`, `lfx-1792`, `lfx-1793`, `lfx-1831`, `lfx-1832` |
| isa-manual | `ext/riscv-isa-manual` checked out; **74** `.adoc` files |

Fetch already done historically:

```powershell
cd "C:\Users\Ibteshamul Haque\Desktop\LFX-Mentorship\riscv-unified-db"
# already present — only if missing:
# git fetch origin pull/1765/head:lfx-1765  ... (1766 1791 1792 1793 1831 1832)
git checkout lfx-1832
```

**Note:** Working tree may be **dirty** under `param_extraction/data/` and some `results/` because Phase 1 scripts were re-run (223-param GT). Part I committed metrics remain under `param_extraction/results/v2/`.

### 1.2 Phase 1 ground truth reproduce ($0) — DONE

Commands used (re-run anytime):

```powershell
cd "C:\Users\Ibteshamul Haque\Desktop\LFX-Mentorship\riscv-unified-db"
python param_extraction\scripts\export_udb_params.py
python param_extraction\scripts\map_params_to_spec.py
python param_extraction\scripts\generate_report.py
```

**Measured (regenerated GT on current UDB):**

| Metric | Value |
|--------|--------|
| Real params | **223** (Part I freeze was **185**, +38) |
| Spec files / lines | 74 / ~52878 |
| Any match / strong | 100% / 91% |
| Classes | DIRECT 140 · CSR_RW 55 · WARL 26 · SW_RULE 2 |

Outputs: `param_extraction/data/ground_truth.json`, `spec_mappings.json`, `phase1_report.txt`, `parameters_catalog.csv`, `udb_param_names.txt`  
Copy of report: `PHASE1-IMMERSION/06-measured-local/phase1_report-regenerated.txt`

### 1.3 Part I metrics remeasure — DONE

Against committed GT 185 + v2 `claude-sonnet-4` results:

| Metric | User-measured |
|--------|----------------|
| Adjusted recall | **72.9%** (exact match to Part I PR) |
| Classification accuracy | **88.4%** |
| WARL recall | **50%** (12/24) |
| Deduped LLM params | 346 |

Against live GT 223: adjusted recall **64.2%** (UDB grew; WARL still 50%).

Source: `PHASE1-IMMERSION/06-measured-local/metrics_summary.json`

### 1.4 Study / reading — DONE (pack on disk)

| Resource | Path |
|----------|------|
| **Master deep study** | `PHASE1-IMMERSION/DEEP-STUDY-COMPLETE.md` |
| Pack index | `PHASE1-IMMERSION/INDEX.md` |
| Issues #1747, #1751 + all LFX bodies | `PHASE1-IMMERSION/02-github-issues/` |
| PRs #1765–#1832 | `PHASE1-IMMERSION/03-part1-prs/` |
| taxonomy, v2 prompt, script heads | `PHASE1-IMMERSION/04-pipeline-docs/` |
| param_schema + sample YAML | `PHASE1-IMMERSION/05-schemas-samples/` |
| SIG RSS digest | `PHASE1-IMMERSION/07-sig-parameters/` |
| CONTRIBUTING, isa-manual index | `PHASE1-IMMERSION/08-udb-docs/` |

Read order from plan is covered by deep study + source dumps. Full `extract.py`/`analyze.py` live in repo for pilot/A.

### 1.5 Pilot extract — NOT RUN (blocked on API)

**Purpose:** Plan requires one pilot on `machine.adoc` (~cents).

```powershell
cd "C:\Users\Ibteshamul Haque\Desktop\LFX-Mentorship\riscv-unified-db"
# Set ONE of:
#   $env:ANTHROPIC_API_KEY = "..."
#   $env:OPENAI_API_KEY = "..."
# Gemini: per Google AI client env used by extract.py
python param_extraction\scripts\extract.py pilot --model claude
# or: --model gpt4o  |  --model gemini
```

Models in code: `claude` → claude-sonnet-4-20250514; `gpt4o` → gpt-4o-2024-11-20; `gemini` → gemini-2.5-pro.

**After pilot:** log tokens/cost in a small manifest under `PHASE1-IMMERSION/06-measured-local/pilot-manifest.md` (create if missing). Then mark pilot DONE in status board below.

---

## 2. Community — IN PROGRESS (user + wait)

### 2.1 Membership — SUBMITTED

| Item | Detail |
|------|--------|
| Type | **Individual** membership + Schedule A |
| Processing | “within the week” (RVI) |
| Email on form | `ibteshamulhaque01@gmail.com` |
| Kendall | `kendall@riscv.org` — reply sent mapping Gmail for sig-parameters; work thread may be UPES |
| Employer on form | UPES, Dehradun |

**Next:** wait for approval email; if >5 business days, polite bump to Kendall + `info@riscv.org`.  
**Do not** re-submit Schedule A unless they ask.

### 2.2 Lists — AFTER membership active

From **`ibteshamulhaque01@gmail.com`** (roster email):

1. Login https://lists.riscv.org/login  
2. Join https://lists.riscv.org/g/sig-parameters  
   or empty email to `sig-parameters+subscribe@lists.riscv.org`  
3. Join https://lists.riscv.org/g/sig-unifieddb  
   or `sig-unifieddb+subscribe@lists.riscv.org`  
4. Confirm link in email if sent  
5. Read **all** archives (~50+ topics) — partial RSS already in `PHASE1-IMMERSION/07-sig-parameters/`

**Do not** spam subscribe before roster maps.

### 2.3 Calendar — USER (can do anytime)

- https://tech.riscv.org/calendar/  
- Community meetings calendar (Google embed from riscv.org if needed)  
- Parameters SIG: biweekly pattern; listen; one-sentence intro only if asked  

### 2.4 Slack — USER (can do anytime)

- Join RISC-V International Slack via official invite (riscv.org or current plan invite)  
- Channel: **`#risc-v-mentorship-questions` only** for logistics (deadlines, process)  
- **Never** technical design Qs there  

### 2.5 LFX mentee profile — USER (not Apply)

| | |
|--|--|
| URL | https://mentorship.lfx.linuxfoundation.org/ |
| Meaning | Create/fill **mentee profile** + resume if form allows — **NOT** project Apply |
| Apply to Part II | **Phase 3 only** (Jul 31–Aug 2) after A+B |

---

## 3. Phase 1 checklist (checkbox form for next session)

### Technical
- [x] Clone UDB  
- [x] Fetch lfx-1765…1832  
- [x] isa-manual submodule  
- [x] Read plans/code (deep study pack)  
- [x] Reproduce Phase 1 GT  
- [x] Remeasure Part I metrics (72.9%)  
- [ ] **Pilot machine.adoc** (API key)

### Community
- [x] Individual membership form + Schedule A submitted  
- [x] Kendall notified (Gmail + UPES)  
- [ ] Membership **approved** / roster active  
- [ ] sig-parameters joined + archives read  
- [ ] sig-unifieddb joined  
- [ ] SIG calendar subscribed  
- [ ] Slack joined (logistics channel only)  
- [ ] LFX mentee profile filled (not Apply)

### Documentation
- [x] `PLAN-SOURCE-OF-TRUTH.md`  
- [x] `PHASE1-IMMERSION/` pack  
- [x] This closeout file  

---

## 4. Measured numbers (copy into Phase 3 later)

```
Phase 1 GT (live UDB): 223 params; 100% any / 91% strong spec match
Part I v2 remeasure (GT185): adjusted recall 72.9%, class acc 88.4%, WARL 50%
Live GT223 remeasure: adjusted recall 64.2%, class acc 88.6%, WARL 50%
parameters.csv named=yes: ~87 (verify before claiming 97)
```

---

## 5. What Phase 2 needs (do not start until Phase 1 pilot preferred)

Per `PLAN-SOURCE-OF-TRUTH.md`:

| ID | Work |
|----|------|
| **A** | Second model full/compare vs claude-sonnet-4 |
| **B** | parameters.csv → draft param YAML + schema validate |
| **C** | WARL stretch only if A+B done |
| Repo | Public under **user** GitHub (`titoatwork` unless user says otherwise) |
| Etiquette | No big UDB PR; list note after A+B |

---

## 6. Next session kickoff (paste as-is)

```text
EXECUTE PLAN-SOURCE-OF-TRUTH.md + PHASE1-CLOSEOUT.md
Role: execution only until I change instructions.
Phase 1 technical = COMPLETE except pilot.
Community = membership waiting; Slack/calendar/LFX profile/list per PHASE1-CLOSEOUT.
Do NOT re-clone or restart deep study from zero.
Next: [pilot if API ready] OR [user confirms Slack/calendar/LFX done] OR [start Phase 2 A scaffold].
API: [none | claude | gpt4o | gemini]
GitHub for public repo: [titoatwork | other: ___]
```

Identity rules (emails, no-friend-accounts) are **only** in `PLAN-SOURCE-OF-TRUTH.md` — user need not repeat them every session.

---

## 7. Agent anti-confusion rules

1. **Plan lock** = `PLAN-SOURCE-OF-TRUTH.md` only until user replaces it (includes identity/email rules — do not ask user to restate).  
2. **Never** treat LFX profile as project Apply.  
3. **Never** open unsolicited big UDB PRs in Phase 1–2.  
4. Prefer reading `PHASE1-IMMERSION/DEEP-STUDY-COMPLETE.md` over re-scraping all issues.  
5. Pilot before claiming Phase 1 fully closed on the plan’s own checklist.  
6. Quality: exceptional code, slow, multi-iterate (user doctrine).  
7. Public repo presentation: follow **`GITHUB-PRESENTATION.md`** only — no invented layouts/README styles.  

---

## 8. File map (workspace root)

```
Desktop/LFX-Mentorship/
  PLAN-SOURCE-OF-TRUTH.md      ← plan lock
  GITHUB-PRESENTATION.md       ← how we present on GitHub (do not invent)
  PHASE1-CLOSEOUT.md           ← THIS FILE (session bridge)
  PHASE1-STATUS.md             ← live status board
  HANDOFF-CONTRIBUTOR.md       ← older handoff; defer to plan lock
  PHASE1-IMMERSION/            ← evidence pack
  riscv-unified-db/            ← code (lfx-1832)
  lfx-riscv-param-extraction-prework/  ← essay seeds only
```

---

*Phase 1 technical closed 2026-07-21. Community + pilot remain for user/next session.*
