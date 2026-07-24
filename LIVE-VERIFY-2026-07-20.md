# Live re-verification snapshot — 2026-07-20

**Purpose:** Execute the "Re-verify before apply" checklist from [README](./README.md) with **live** GitHub + LFX API pulls, one day after the [spring-baseline](./lfx-riscv-param-extraction-prework/notes/spring-baseline.md) pack (dated 2026-07-19). This file records only what changed or was confirmed today — it does not restate the baseline.

**Method:** LFX project API + GitHub REST API, pulled 2026-07-20. Facts only; no private/admin data.

---

## TL;DR — nothing blocks applying

| Check | Result (07-20) | Verdict |
|-------|----------------|---------|
| Project still accepting | `status: Published`, `acceptApplications: true` | ✅ apply |
| Application window (API) | **2026-07-15 → 2026-08-05** | ✅ open, ~16 days left |
| Term (API) | **2026-09-15 → 2026-11-15** | ✅ |
| Spring Part I PRs | **all 7 still OPEN, unmerged** | ✅ merge debt is real → Part II opening |
| Param gold set | **grew 207 → 228 YAML on `main`** | ⚠️ denominators moved — re-pin gold |

---

## 1. LFX project — confirmed from API

Project `22296947-cecb-4a8f-8bcb-4f34710e9f66`, decoded from `api.mentorship.lfx.linuxfoundation.org`:

| Field | Value |
|-------|-------|
| Name | AI-assisted extraction of architectural parameters from RISC-V specifications — **Part II** |
| Org | RISC-V International (`lfProjectName`) |
| Status | `Published` · `acceptApplications: true` |
| Skills | Generative AI · ISA specifications · Parameterized modeling |
| Mentors | Allen Baum · Ajit Dingankar (GitHub **`adingank-qualcomm`**) |
| Repo | `github.com/riscv/riscv-unified-db` |
| Apply window (epoch → UTC) | `1784073600` = **2026-07-15** → `1785888000` = **2026-08-05** |
| Term (epoch → UTC) | `1789444800` = **2026-09-15** → `1794718800` = **2026-11-15** |
| `activeUsers` | 0 (no accepted mentee yet) |

Origin line from the description, verbatim: *"originally started as an RVI Mentorship for Spring 2026, and continued under the Parameter SIG."*

---

## 2. Spring Part I PRs — LIVE state (re-verified today)

The baseline flagged these as "still open as of 07-19." **Confirmed still open on 07-20**, and all stale since late May:

| PR | Phase | State (07-20) | Last update |
|----|-------|---------------|-------------|
| #1765 | 1 Ground truth | **open** | 2026-05-25 |
| #1766 | 2 Taxonomy+prompts | **open** | 2026-05-25 |
| #1791 | 4 Extract | **open** | 2026-05-25 |
| #1792 | 5 Analyze | **open** | 2026-05-26 |
| #1793 | 6 Refine (V2) | **open** | 2026-05-26 |
| #1831 | 7 Spreadsheet | **open** | 2026-05-26 |
| #1832 | 8 Spec tags | **open** | 2026-05-26 |

**Reading:** ~2 months untouched, zero merged. The Fall brief's ask — *"quality and implementation robustness"* + *"create a GitHub PR ... and follow up with the maintainers on merging them"* — is aimed squarely at this debt. **Landing** > re-discovering.

Consequence unchanged: `param_extraction/` lives only on PR branches, not a clean `main`. To reproduce, fetch branches directly:
```bash
for n in 1765 1766 1791 1792 1793 1831 1832; do git fetch origin pull/$n/head:lfx-$n; done
```

---

## 3. Gold-set drift — the one thing that actually moved

Pinned `riscv/riscv-unified-db` `main` today:

```
SHA ab6b3a6b14f7   committed 2026-07-20T08:49:16Z
```

| Metric | Spring (PR #1765 text) | main @ ab6b3a6b (07-20) | Δ |
|--------|-----------------------:|------------------------:|---|
| `spec/std/isa/param/*.yaml` total | 207 (185 real + 22 MOCK) | **228** | +21 files |
| Files matching `MOCK` (any case) | 22 | **0** | MOCK fixtures gone/renamed |
| Effective real-param gold | 185 | **~228** | **+23%** |

**Why it matters for Part II:**
- Every Spring recall number (62.7% / 72.9% adjusted, WARL 50%, …) was measured against a **185-param** denominator that no longer exists. Re-baselining against the current 228 is Task 0.
- Some of Spring's "233 newly discovered" may since have **landed as real UDB params** — must diff the new ~43 against Spring's discovery list before claiming them again.
- **Action:** always pin gold by SHA (`ab6b3a6b14f7` today) in every eval run; never cite a bare percentage without the SHA.

---

## 4. Where to plug in — orgs confirmed live

| Channel | Handle | Note |
|---------|--------|------|
| Parameter SIG list | `sig-parameters+subscribe@lists.riscv.org` | THE list; tracks Jira **RVG-931** |
| **UDB SIG list** (new find) | `sig-unifieddb+subscribe@lists.riscv.org` | where UDB schema + merge calls happen → objectives 4/5 |
| RISC-V Slack | invite `zt-2ui9mzrsn-…` | channel `#risc-v-mentorship-questions` (logistics only) |
| Mentor (Ajit) GitHub | `adingank-qualcomm` | review his UDB activity before applying |
| Program contact | `mentorships@riscv.org` | |

No official RISC-V Discord exists — the ecosystem runs on Slack + groups.io.

---

## 5. Re-verify checklist — status

From README §"Re-verify before apply":

- [x] LFX still Accepting → **yes** (`acceptApplications: true`)
- [x] Deadline still 5 Aug → **yes** (API `2026-08-05`)
- [x] Spring PR merge state → **all 7 open, unmerged, stale since May**
- [x] Pre-work public URL in essay → *(pending: paste this repo's URL into essay before submit)*

---

## 6. Net delta vs the 07-19 baseline

1. Part I PRs **re-confirmed open** one day later — the "land it" thesis holds.
2. Gold set **185 → 228** and **MOCK fixtures removed** — Spring metrics need re-baselining; pin SHA `ab6b3a6b14f7`.
3. Dates now **exact from API** (not the RISC-V page blurb): apply Jul 15–Aug 5, term Sep 15–Nov 15.
4. Second list to join: **sig-unifieddb**; mentor GitHub handle **adingank-qualcomm**.
5. No change to mentors, skills, repo, or ~1-seat expectation.

---

*Live-verified by workspace tooling on 2026-07-20 against public GitHub/LFX APIs. Spring designs and metrics remain the property of their PR authors and the RVI/UDB community. Study material for Ibteshamul Haque.*
