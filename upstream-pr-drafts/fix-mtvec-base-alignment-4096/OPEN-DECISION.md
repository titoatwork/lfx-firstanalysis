# Open decision — do **not** open competing PR yet

**Date:** 2026-07-27  
**Branch:** `fix/mtvec-base-alignment-4096` (fork `titoatwork/riscv-unified-db`)

## Facts

| Item | Status |
|------|--------|
| Maintainer PR #2090 | **Open**, edits tvec/alignment params |
| Our comment on #2090 | Posted; **no maintainer reply yet** |
| #2090 head still has `0xfff` in both MTVEC alignment enums | Yes (as of last check) |
| Our branch | 2 YAML fixes + regression test wired into `run.rb` + CI matrix |

## Rule

**Do not open** a separate PR against `main` while #2090 is active on the same files (visible race).

## Sequence

1. **Wait ~24h** (from comment / this note) for #2090 response or update.  
2. If they accept / fix `0xfff` in #2090 → **let them**; comment is the credibility signal.  
3. If a maintainer asks for a patch on that branch → offer the small diff there.  
4. **Only open our PR** if #2090 closes/merges **without** the correction, or a maintainer **explicitly** recommends a separate PR.  
5. Before opening: **rebase** on current `origin/main`, keep test wired, run `./bin/ruby tools/ruby-gems/udb/test/test_mtvec_base_alignment_pow2.rb` (and broader suite if environment allows).

## Title (when/if open)

```text
fix(param): correct 4095 typo in MTVEC_BASE_ALIGNMENT power-of-two enums
```

Body: `PR_BODY.md` (no separate Author section).
