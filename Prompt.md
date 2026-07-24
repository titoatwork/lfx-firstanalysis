# Prompt.md — Master Execution Prompt (LFX Part II Selection Packet)

> **What this file is.** A single, self-contained prompt you paste into a fresh agent/chat
> session. It drives that agent, step by step, to finish the remaining LFX Fall 2026 Part II
> campaign and produce the final selection packet — **automatically stopping to ask you** for
> anything only you can provide (API key, spend approval, a `git push`, your clone location,
> personal résumé fields, the final Apply click).
>
> **Who runs it.** An execution agent (possibly a smaller/weaker model). This file therefore
> spells everything out: exact commands, exact stop-gates, exact question wording, and hard
> guardrails so the agent cannot wander off-plan or invent numbers.
>
> **Non-negotiable behavior:** when the agent hits something it does not have and cannot safely
> assume, it must **PAUSE and ASK the user** using the template in §7 — and then wait. It must
> never spend money, push to GitHub, create a second repo, or fabricate a result to "keep going."

---

## 0. HOW TO USE THIS FILE

1. Open a new agent session **inside the repo** `lfx-firstanalysis/` (the folder that contains
   this `Prompt.md`).
2. Paste this entire file as the first message, prefixed with:
   `EXECUTE Prompt.md. Role: execution only. Follow every step in order. Ask me when blocked.`
3. The agent runs **§8 Execution Plan** top to bottom. At each **STOP-AND-ASK GATE** it pauses,
   asks you (using §7), and waits for your reply before continuing.
4. You supply keys / approvals / personal fields when asked. The agent does the rest and hands
   you a finished, reviewable packet plus a short "what I changed / what you must click" report.

**The agent must read these repo files before doing real work** (they are the law; this prompt
summarizes them but does not replace them):
`AGENTS.md`, `HANDSOFF.md`, `RECURRING_MISTAKES.md`, `.grok/rules/*`, `AGENT-RULES.md`,
`PLAN-SOURCE-OF-TRUTH.md`, `PROGRESS.md`, `LEFTOVER-WORK.md`, `PHASE2-PLAN.md`,
`GITHUB-PRESENTATION.md`, `riscv-param-extraction/docs/metrics.md`,
`riscv-param-extraction/manifests/pilot-machine-adoc.md`.

---

## 1. PRIME DIRECTIVE & ROLE

- **Role:** Execution agent. The **user owns the plan**; you track state and execute on go.
  Do **not** invent a parallel roadmap. Do **not** restart finished work.
- **Mission:** Make rejection from LFX Fall 2026 **Part II — AI-assisted extraction of
  architectural parameters from RISC-V specifications** irrational, by finishing the
  mentor-auditable evidence packet and preparing the application, before the **2026-08-05**
  deadline (target submission **Jul 31 – Aug 2**; today is **2026-07-24**).
- **Project:** https://mentorship.lfx.linuxfoundation.org/project/22296947-cecb-4a8f-8bcb-4f34710e9f66
- **Upstream:** https://github.com/riscv/riscv-unified-db · **Mentors:** Allen Baum (precision /
  provenance), Ajit Dingankar (metrics / baselines / ablations).
- **Quality bar (hard):** exceptional, domain-accurate work — not generic AI-slop. Slow is fine:
  research → design → implement → critique → rewrite. Use the real vocabulary
  (param, WARL, adjusted recall, provenance, manifest). No emoji walls, no "my journey," no fake
  certainty.
- **Honesty (hard):** never invent metrics, merges, pilot/Artifact-A results, or Part I
  authorship. If a number does not exist on disk from a real run, it does not exist.

---

## 2. THE END RESULT (Definition of Done)

When you are finished, the following exist, are internally consistent, and are ready for the user
to review, push (on their word), and submit:

**Technical evidence (in `riscv-param-extraction/`):**
- [ ] **Artifact A** actually run: a second model (default **gpt-4o-mini**, `PROMPT_VERSION=v2`)
      extracted over the Part I chunk set, merged, and analyzed.
- [ ] **Artifact A tables** filled in `docs/metrics.md`, section 5:
      per-class recall vs the committed Claude-sonnet-4 Part I baseline **and** vs ground truth;
      inter-model **agreement** (name overlap / match rate); **hallucination-overlap**
      (proposed-new-by-both vs proposed-new-by-one). Honest numbers even if worse than Claude.
- [ ] **Run manifest(s)** in `manifests/` (Obj 3): model id, prompt version, tokens, cost,
      exact command, commit/branch, chunk set, and every skipped chunk with the reason.
- [ ] **README** updated to the locked order: remeasure → pilot split → **A** → B → limitations.
- [ ] *(Optional, only if A+B are solid and budget remains)* **Stretch C** WARL recall attack,
      in its own section, only if it shows a real lift.

**Application packet (Phase 3):**
- [ ] **Cover letter / essay** finalized with the user's **measured** Part I numbers, links to
      the public A + B evidence, and a **9-week plan mapped 1:1 to the 5 official objectives**
      with fortnight milestones and explicit metric targets.
- [ ] **1-page résumé** ready to export to PDF (personal fields filled from user answers; **no
      CGPA**, no confidential COLIDE link).
- [ ] A short **"what you must click"** handoff: push (if approved), then **Apply** on LFX
      (only the user can click Apply).

**You do not consider yourself done until the user has reviewed the packet.** You never click
Apply, never approve membership, never push without the word "push."

---

## 3. IDENTITY (fixed facts — never re-ask, never substitute)

| Field | Value |
|------|------|
| User | **Ibteshamul Haque** (aka "tito") |
| GitHub | **titoatwork** — the only public home |
| Membership / lists email | **ibteshamulhaque01@gmail.com** |
| Earlier list attempt | ibteshamul.123421@stu.upes.ac.in (UPES) |
| **NEVER use** | friend Gmail **asquare567@gmail.com** — appears in some pasted guides; ignore it everywhere |
| Student employer (RVI form) | UPES, Dehradun |
| Universiti Malaya | June 2026 research **attachment** only (Prof. Por Lip Yee) — **not** degree home |
| Location / availability | India (IST, UTC+5:30); flexible for US-Pacific meetings; **≥30 h/week** for the term |
| Term | ~2026-09-15 → 2026-11-15 (~9 weeks) |

Do not ask the user to restate any of the above. Load it from here and from
`PLAN-SOURCE-OF-TRUTH.md`.

---

## 4. ABSOLUTE RULES (breaking one can tank selection — obey exactly)

These are distilled from `HANDSOFF.md`, `AGENT-RULES.md`, `RECURRING_MISTAKES.md`, and
`.grok/rules/`. When any casual instruction seems to conflict with these, **stop and confirm**.

1. **Single public repo.** The only public home is **`titoatwork/lfx-firstanalysis`**. All
   Phase 2 code lives in the **`riscv-param-extraction/`** folder inside it. **NEVER**
   `gh repo create` or make a second "product" repo. If any doc says "create public repo," it
   means *folder + commit inside this monorepo* — not a new repo. (This mistake was made on
   2026-07-22; do not repeat it.)
2. **Never `git push`** (or force-push, or push tags) without the user typing an explicit
   **"push"**. The user alone ships. When in doubt, stage the commit locally and ask.
3. **Never make a paid API call** without (a) the user's key in the session and (b) an explicit,
   scoped spend approval. No test call "to check." No auto-retry loops (`--retries 0` on paid
   extract paths). No re-spend after a parse failure — diagnose offline and ask.
4. **Never commit, echo, `cat`, or paste an API key** anywhere — not into git, README, a
   manifest, a doc, or the chat. Session environment only; unset after use.
5. **Never push the `riscv-unified-db/` clone** (it is gitignored on purpose) or any `.env`,
   secret, `*.pem`, `slack-notes.md`, `*-PRIVATE.md`, or personal strategy note.
6. **Never re-run the pilot** (`extract.py pilot` / machine.adoc) and **never restart Phase 1**
   (no re-clone-from-zero of study, no re-scrape of issues/PRs, no re-inventing metrics). Phase 1
   technical work and the pilot are **DONE**.
7. **Never open an unsolicited big PR** to `riscv/riscv-unified-db`. Pre-apply merges required:
   **0**. A small draft PR is a *maybe*, only after A+B + membership + a list ask.
8. **Never invent numbers.** Use only the measured facts in §5 or new numbers produced by a real
   run you just executed and manifested.
9. **Named-param count is 87 rows / 83 unique.** Never write "97."
10. **Pilot claim is `COMPLETE_WITH_MODEL_SPLIT`** (chunk_021 gpt-4o, chunk_020 gpt-4o-mini) —
    never "a pure gpt-4o full machine.adoc pilot."
11. **Part I credit stays with @ishaan-arora-1 / PRs #1765–#1832.** This repo *reproduces and
    extends*; it never claims Spring authorship.
12. **Channels:** mentorship Slack `#risc-v-mentorship-questions` is **logistics only** (never
    technical design). Technical discussion goes to sig-parameters / sig-unifieddb, and only
    **after** membership approval maps the roster Gmail. No cold email to mentors.
13. **LFX mentee profile ≠ Apply.** Apply is Phase 3 only, and **only the user clicks it**.
14. **Résumé:** 1 page, **no CGPA**, no confidential COLIDE URL.

---

## 5. MEASURED FACTS (cite these; do not invent; update only after a real remeasure)

```
Ground truth (regenerated on live UDB):  223 params; 100% any-keyword / 91% strong match
                                          classes: DIRECT 140 · CSR_RW 55 · WARL 26 · SW_RULE 2
Part I v2 remeasure vs committed GT 185:  adjusted recall 72.9% · class acc 88.4% · WARL 50% (12/24)
Same LLM output vs live GT 223:           adjusted recall 64.2% · class acc 88.6% · WARL 50%
parameters.csv named=yes:                 87 rows / 83 unique  (all 83 already exist in UDB)
Artifact B (named export):                83/83 schema-valid
Artifact B (new, limit 20):               20/20 schema-valid
Pilot machine.adoc:                       COMPLETE_WITH_MODEL_SPLIT, ~$0.05 total
  chunk_021  gpt-4o-2024-11-20        ~10,115 in / 1,152 out · 6 params · ~$0.037
  chunk_020  gpt-4o-mini-2024-07-18   ~44,874 in / 1,541 out · 9 params · ~$0.008
  reason for split: gpt-4o org TPM 30,000 rejected the ~44k-input chunk
Artifact A multi-model:                   NOT RUN  ← this is the main remaining technical work
```
Source of truth for public tables: `riscv-param-extraction/docs/metrics.md`.
Local remeasure JSON: `PHASE1-IMMERSION/06-measured-local/metrics_summary.json`.

**Metric targets to promise in the 9-week plan** (goals, not measured): adjusted recall
72.9% → **85%+**; WARL recall 50% → **75%+**; N schema-valid param files in reviewed PRs.

---

## 6. GROUND STATE (what is done vs what is left)

**DONE — do not redo:**
- Phase 1 immersion, deep study, UDB clone + Part I PR branches, GT reproduce (223), Part I v2
  remeasure (72.9% / 88.4% / WARL 50%).
- Pilot machine.adoc (`COMPLETE_WITH_MODEL_SPLIT`, ~$0.05).
- **Artifact B**: `riscv-param-extraction/export/csv_to_param_yaml.py` → 83 named + 20 new
  schema-valid drafts, with reports and tests. (Optional enum/range domain polish only if asked.)
- Public monorepo surface pushed: README, `docs/metrics.md`, pilot manifest, export code, drafts.
- Community: membership submitted (pending), Slack joined, LFX mentee profile + résumé uploaded
  (2026-07-23).

**LEFT — the work this prompt drives:**
- **Artifact A** (multi-model + agreement + hallucination-overlap) — needs a UDB clone on this
  machine, the committed Claude v2 results, a user API key, and scoped spend.
- Unified public surface update (metrics + manifest + README) after A.
- *(Optional)* Stretch C WARL.
- **Phase 3** application packet (cover letter/essay + résumé) and the Apply handoff.
- **User-only actions** (you can guide but not perform): approve membership, join sig-parameters
  / sig-unifieddb once approved, subscribe the SIG calendar, click Apply, push to GitHub.

**Important environment note:** *this checkout currently has NO `riscv-unified-db/` clone.*
Expect to clone it in STEP 1. Do not assume the Part I pipeline, chunks, or Claude v2 results are
already present — verify, and ask if missing.

---

## 7. THE "ASK THE USER" PROTOCOL (how to self-provision — read carefully)

Whenever you need something you do not have and cannot safely produce yourself, **stop and ask**,
then **wait**. Do not guess, do not fabricate, do not proceed on a paid/destructive path.

**Emit exactly this block, filled in:**

```
=== NEED FROM YOU (BLOCKING) ===
WHAT I NEED:   <the specific thing>
WHY:           <one line: which step needs it and what it unblocks>
HOW TO GIVE IT:<exact action for the user — a command to paste, a value to type, a yes/no>
COST/RISK:     <money about to be spent, or "none">  ← include for any paid or push/apply step
UNTIL YOU REPLY, I WILL: not proceed / not spend / not push. I am waiting.
===============================
```

**Mandatory triggers (ask BEFORE acting):**

| Trigger | Ask for | Notes |
|--------|--------|------|
| No local `riscv-unified-db/` found | Path to an existing clone **or** permission to clone it here | Cloning is large; get a yes |
| Committed Part I **Claude v2 results** missing after checkout | Which branch/archive holds `all_results_claude-sonnet-4.json` (+ deduped/alignment) | A's agreement baseline; without it A is only-vs-GT |
| About to make **any paid API call** | The API key **and** an explicit spend cap (e.g. "yes, up to $4.50, gpt-4o-mini") | See §8 STEP 3 for the safe key-handling method |
| Projected spend would exceed the cap (or ~$4.50) | Re-approval, or approval to switch to a stratified/smaller run | Never blow the budget silently |
| A run fails (auth, TPM, parse) | How to proceed | **No automatic re-spend** |
| About to **`git push`** | The literal word "push", and confirmation of which files | Default is to stage locally and stop |
| Building the **résumé** | City, phone, email to show, LinkedIn URL, whether to show GitHub and university name | Bracketed fields in `RESUME-DRAFT.md` |
| Ready to **Apply** on LFX | Confirmation — then hand the user the exact steps (you cannot click) | Apply is user-only |
| Any doc says "create a repo" | Confirm it means the monorepo folder (it does) unless the user names a new repo | Rule §4.1 |
| Genuinely ambiguous scope | A yes/no or A/B choice | Prefer one sharp question over guessing |

**Do NOT ask** about anything already fixed in §3 (identity) or §5 (measured facts). Load those.

---

## 8. EXECUTION PLAN (run in order; each step has a Verify and, where relevant, a STOP-AND-ASK GATE)

> Standing rule for every command below: **discover flags with `--help` before running a script**
> you have not run this session (e.g. `python param_extraction/scripts/extract.py --help`,
> `... analyze.py --help`). Do not assume flag names — the exact CLI lives on the clone, not in
> this prompt. Prefer offline/`$0` work first; treat OpenAI credit as scarce.

### STEP 0 — Load context and confirm state ($0)

1. Read the law files listed in §0. Skim, do not re-derive.
2. Run `git status` and `git branch`. Confirm you are in `titoatwork/lfx-firstanalysis` on a
   working branch (default `main`; if you will make commits, create a topic branch such as
   `analysis/artifact-a` — do **not** commit straight to `main` if you can branch).
3. Print a short **state table**: membership, profile, pilot, Artifact B, Artifact A, apply — and
   confirm it matches `PROGRESS.md` / `LEFTOVER-WORK.md`.
4. **Verify:** you can name the single public repo, the measured numbers, and the fact that A is
   not yet run. If any of §4's rules are unclear, re-read `HANDSOFF.md` before continuing.

### STEP 1 — Locate or clone the UDB pipeline ($0)  — *STOP-AND-ASK GATE if missing*

The Part I pipeline (`param_extraction/scripts/extract.py`, `analyze.py`, chunks, and the
committed Claude v2 results) lives in a local `riscv-unified-db` checkout, **not** in this repo.

1. Look for it at `./riscv-unified-db` (repo root; gitignored) or a sibling `../riscv-unified-db`.
2. **If not found → ASK** (template §7): does the user have a clone elsewhere (give the path), or
   should you clone it here? On approval:
   ```bash
   git clone https://github.com/riscv/riscv-unified-db
   cd riscv-unified-db
   for n in 1765 1766 1791 1792 1793 1831 1832; do
     git fetch origin pull/$n/head:lfx-$n
   done
   git checkout lfx-1832
   git submodule update --init --recursive   # pulls ext/riscv-isa-manual (spec .adoc source)
   ```
3. **Verify the pipeline is usable:**
   - `param_extraction/scripts/extract.py` exists; `python param_extraction/scripts/extract.py --help` runs.
   - `python param_extraction/scripts/extract.py status` shows chunks. If chunks are missing,
     generate them with the chunker (`param_extraction/scripts/chunker.py --help` first). If that
     fails, **ASK** the user which branch/archive has the prepared chunks.
   - The **committed Claude v2 results** exist, e.g.
     `param_extraction/results/v2/all_results_claude-sonnet-4.json` (and `deduped_…` /
     `alignment_…`). **If missing → ASK** where they are (they are the Artifact A baseline). If the
     user cannot supply them, note that Artifact A will compare **vs ground truth only** (still
     valid, but say so honestly) and continue.
   - Ground truth exists: `param_extraction/data/ground_truth.json` (committed freeze = 185).
4. Confirm the checkout is on branch **`lfx-1832`**.

### STEP 2 — Artifact A offline scaffold ($0, no key yet)

Do everything possible before any spend, so the paid run is short and safe.

1. **Chunk inventory + TPM classification.** List every chunk and estimate its input tokens (the
   pipeline estimates at ~3.8 chars/token; use `run_prompt.py estimate` if available). Flag any
   chunk whose estimated input is **≳ 30,000 tokens** as TPM-risky for gpt-4o (org TPM 30k). The
   default model is **gpt-4o-mini**, which cleared the ~44k pilot chunk — but still record sizes
   so you can predict cost and spot outliers. Write this inventory to
   `riscv-param-extraction/manifests/artifact-a-plan.md`.
2. **Confirm the `gpt4o-mini` model alias and `--chunk` filter exist** in the local `extract.py`
   (they were added during the pilot). If missing, add them minimally and locally (this is the
   local UDB tree, **not** an upstream merge) — thin, tested, domain-named.
3. **Write the agreement/analysis scaffold** in `riscv-param-extraction/pipeline/` (it is
   currently an empty scaffold). Thin, domain-named scripts — not a generic app. It must, given
   two merged result sets (Claude v2 and the new model):
   - compute **inter-model agreement**: shared parameter names, unique-to-each, match rate;
   - compute **hallucination-overlap**: of params each model proposes as **new** (not in UDB) at
     high confidence, how many overlap (both models → more likely real) vs appear for only one
     (more likely a hallucination);
   - emit markdown tables ready to paste into `docs/metrics.md` §5.
   For **per-class recall / classification accuracy** of the new model, reuse the existing
   `analyze.py` (run it against the new model's merged file) rather than reimplementing — check
   `analyze.py --help` for the model-selection flag. Test your scaffold offline against the
   **existing Claude results** (structure/shape only) so it is known-good before the paid run.
4. **Write the manifest template** `manifests/artifact-a-<model>.md` with every field from Obj 3
   (model id, prompt version, tokens, cost, command, commit/branch, chunk set, skips) left blank
   to fill after the run.
5. **READY gate.** Summarize: chunk count, estimated total input tokens, a cost estimate for
   gpt-4o-mini (Part I Claude scale was ~1.03M input / ~83k output tokens across ~60 chunks; at
   gpt-4o-mini rates a clean full run is typically **well under $5**), and the exact command you
   will run. Then proceed to STEP 3's gate.

### STEP 3 — Artifact A paid run  — *STOP-AND-ASK GATE (money)*

1. **ASK** (template §7, COST/RISK filled): request the API key **and** an explicit spend cap
   and model confirmation (default: `gpt-4o-mini`, `PROMPT_VERSION=v2`, `--retries 0`, no
   `--force`). Present the STEP 2 cost estimate. **Wait.**
2. **Safe key handling** (never let the key touch git or the transcript):
   - Preferred: instruct the user to create `riscv-unified-db/.env` containing
     `OPENAI_API_KEY=sk-...` (the path `.env` is already gitignored). Then load it only for the
     run and unset after — **never** `cat` or echo it:
     ```bash
     cd riscv-unified-db
     git check-ignore .env            # MUST print ".env"; if it does not, STOP — do not proceed
     set -a; source ./.env; set +a
     export PROMPT_VERSION=v2
     ```
   - Alternative: the user pastes `export OPENAI_API_KEY=...` themselves in the session shell
     (e.g. via the `! ` prefix). Either way, you never print the value.
3. **Run, watching burn rate.** Prefer a first small batch to measure real cost, then continue:
   ```bash
   # Confirm exact subcommand/flags first:
   python param_extraction/scripts/extract.py --help
   # Full (or near-full) second-model run:
   python param_extraction/scripts/extract.py run --model gpt4o-mini --retries 0 -v
   ```
   - If a chunk fails on TPM, **skip it and record the skip** (do not switch to paid gpt-4o to
     "rescue" it without a fresh gate). If projected spend approaches the cap, **STOP and ASK**.
   - Do **not** re-run Claude. Do **not** re-pilot.
4. **Clean up:** `unset OPENAI_API_KEY` (and remind the user they may delete `.env`). Confirm no
   key landed in any tracked file (`git status`, and grep the diff for `sk-` before any commit).
5. **Verify:** per-chunk result JSON exists under `param_extraction/results/v2/gpt-4o-mini/`.

### STEP 4 — Merge, analyze, and fill the tables ($0 after the run)

1. **Merge** the new model's per-chunk results:
   `python param_extraction/scripts/extract.py merge --model gpt4o-mini` (confirm flag via
   `--help`) → `all_results_gpt-4o-mini.json`.
2. **Single-model metrics** for the new model via `analyze.py` (dedup → align → metrics → report;
   there may be an `all` mode). Compute per-class recall and classification accuracy vs
   **GT 185** (note vs live GT 223 if useful), and WARL-class recall specifically.
3. **Cross-model analysis** with your STEP 2 pipeline scripts: inter-model agreement and
   hallucination-overlap vs the committed Claude v2 results.
4. **Fill `riscv-param-extraction/docs/metrics.md` §5** and **complete the manifest**
   `manifests/artifact-a-gpt-4o-mini.md` with real tokens/cost/command/commit/skips.
5. **Honesty check:** if the new model is worse than Claude on some/all classes, **say so
   plainly**. Never write "matched or beat Claude" unless the tables show it. Never claim a "full
   gpt-4o multi-model matrix" — it is a gpt-4o-mini second-model run.
6. **Verify:** a mentor could clone, run one command, and reproduce a number in your table. Every
   table cell traces to a committed report or manifest.

### STEP 5 — Update the public surface ($0; do NOT push yet)

1. Update `riscv-param-extraction/README.md` to the locked order (`GITHUB-PRESENTATION.md`):
   one-paragraph framing → **measured tables** (remeasure → pilot split → **A** → B) → reproduce
   commands → **limitations** (honest: gpt-4o-mini not gpt-4o; any skipped chunks; A vs baseline
   caveats) → links (Part I PRs; later a list post).
2. Add a dated worklog `riscv-param-extraction/docs/WORKLOG-<today>.md` so new work is not
   confused with Phase 1 commits.
3. Make **small, domain-named commits locally** (e.g. `A: gpt-4o-mini second-model run + agreement
   tables + manifest`). **Do not push.** Then **STOP-AND-ASK** whether to push, listing exactly
   which files would go public (mentor-auditable evidence only — never the clone, keys, or
   personal notes).

### STEP 6 — *(Optional)* Stretch C: WARL recall attack ($ — only if A+B solid and budget left)

Only attempt if the user approves and budget remains. Feed UDB CSR-field YAML as auxiliary
context to attack the `NORM_CSR_WARL` recall scar (Part I = 50%). Same spend gate as STEP 3.
Present it as a separate `docs/metrics.md` section **only if it shows a real lift** — otherwise
report the null result honestly and drop it.

### STEP 7 — Phase 3 application packet ($0)  — *STOP-AND-ASK GATE for résumé personal fields*

Build these as **local files** for the user to review; they are application materials, not
mentor-repo pushes (do not push them into the public repo unless the user says so).

1. **Cover letter / essay** — refine `lfx-riscv-param-extraction-prework/application/essay-part-ii.md`
   (do not paste the generic profile intro). It must contain:
   - one line: who + research (IoT IDS, on-device LLM, Prof. Por Lip Yee, manuscript in prep);
   - **3 lines of Part I numbers the user measured** (72.9% adjusted recall, 88.4% class acc,
     WARL 50%) — framed as *reproduction*, crediting @ishaan-arora-1 / PRs #1765–#1832;
   - **"I built"**: links to the public A tables + B exporter/drafts (and pilot manifest);
   - a **9-week plan mapped 1:1 to the 5 objectives**, in fortnight milestones, with explicit
     metric targets (adjusted recall 72.9% → 85%+; WARL 50% → 75%+; N schema-valid param files in
     small reviewed PRs). Expand the 4-week scaffold in
     `lfx-riscv-param-extraction-prework/notes/four-week-plan.md` to the ~9-week term
     (2026-09-15 → 2026-11-15);
   - logistics: ≥30 h/week, IST but flexible for US-Pacific; honest ranges and limitations.
   - Tune tone for both mentors: Baum wants auditable provenance; Dingankar wants
     baselines/ablations/metrics.
2. **The 5 official objectives** the plan must map to:
   1. LLM extract priv + unpriv; improve recall vs gold (Manual chapter YAML / keyword_matches /
      UDB YAML).
   2. Extend the classification scheme.
   3. AI agents/skills + reproducible workflows (manifests).
   4. Export → UDB YAML.
   5. Reviewed PR + maintainer merge follow-up.
3. **Résumé** — from `RESUME-DRAFT.md`. **ASK** the user for the bracketed fields (city, phone,
   the email to display, LinkedIn URL, whether to show GitHub, whether to name the university).
   Keep it **1 page, no CGPA, no confidential COLIDE link**. Produce a clean Markdown/Docs-ready
   version named `Ibteshamul_Haque_Resume_LFX_Fall2026`.
4. **Verify:** every claim in the packet is honest and every metric matches §5 or a real A run.

### STEP 8 — Final handoff (user-only actions)

Produce a short report with three lists:
1. **What I changed** (files created/edited, commits made — not pushed).
2. **Decisions/assumptions** I made and any honest limitations in the A results.
3. **What only you can do**, with exact steps:
   - `git push` (if you approve — say "push");
   - subscribe the SIG calendar; after membership approval, join sig-parameters + sig-unifieddb
     from `ibteshamulhaque01@gmail.com` and read the archives; *(optional, after A+B are public)* a
     short calm sig-parameters note with the repo link and ~5 bullets;
   - **Apply** to Part II on LFX (paste the essay, complete prerequisites, confirm Pending) — the
     agent cannot click this; target **Jul 31 – Aug 2**.

---

## 9. FILE-UPDATE MAP (touch these; leave the rest)

| When | Create / edit |
|------|---------------|
| A scaffold | `riscv-param-extraction/pipeline/*` (agreement + hallucination-overlap), `manifests/artifact-a-plan.md` |
| A run | `manifests/artifact-a-gpt-4o-mini.md` (real tokens/cost/skips) |
| A results | `riscv-param-extraction/docs/metrics.md` §5, `docs/WORKLOG-<today>.md` |
| Surface | `riscv-param-extraction/README.md` (locked order) |
| State bookkeeping | `PROGRESS.md`, `LEFTOVER-WORK.md`, `LEFT-TODO.md`, root `AGENTS.md`, `PHASE1-STATUS.md` — flip the Artifact-A checkboxes when A is real |
| Application | `lfx-riscv-param-extraction-prework/application/essay-part-ii.md`, `RESUME-DRAFT.md` (+ résumé export) |

**Do not** edit public metrics to "look better" without a real remeasure. **Do not** vendor the
UDB clone into this repo. **Do not** create new top-level docs unless a step above names one.

---

## 10. FAILURE HANDLING

- **Auth error:** key/env problem — re-check the key was loaded (never printed); ask the user.
- **TPM rejection (large chunk on gpt-4o):** expected above ~30k input; on gpt-4o-mini it should
  pass. Skip and record the skip; do not silently switch models mid-run without a gate.
- **Parse/JSON failure on a chunk:** diagnose **offline**; do **not** auto re-spend. Ask before a
  second paid attempt.
- **Missing pipeline pieces (chunks, Claude results, GT):** STEP 1/§7 — ask; do not fabricate.
- **Anything that would push, spend, delete, or contact people:** stop and confirm.
- **You are unsure:** prefer asking one sharp question over guessing. Silence + a fabricated
  number is the worst outcome here.

---

## 11. FINAL DELIVERABLE CHECKLIST (the agent ticks these before declaring done)

- [ ] Artifact A ran on a real second model; results on disk; **no key in any tracked file**.
- [ ] `docs/metrics.md` §5 filled with per-class recall, agreement, hallucination-overlap — honest.
- [ ] `manifests/artifact-a-*.md` complete (model, prompt version, tokens, cost, command, commit,
      chunk set, skips).
- [ ] README in locked order; limitations honest; numbers consistent with §5.
- [ ] State files updated (A checkboxes flipped).
- [ ] Cover letter/essay: measured Part I numbers + A/B links + 9-week plan ↔ 5 objectives +
      30 h/week + IST; Part I credited to @ishaan-arora-1.
- [ ] Résumé: 1 page, personal fields filled, no CGPA, no COLIDE link.
- [ ] Nothing pushed without an explicit "push"; no second repo; no unsolicited UDB PR; no invented
      numbers; friend Gmail never used.
- [ ] Final handoff report delivered: what changed · assumptions/limits · what the user must click
      (push, join lists, **Apply** by Jul 31–Aug 2).

---

*This prompt is an agent-facing runbook — keep it local; it is not a mentor-facing file and should
not be pushed to the public repo unless the user explicitly says so. It does not replace
`PLAN-SOURCE-OF-TRUTH.md`; it operationalizes it. If the user issues a new plan, that plan wins.*
