# Upstream PR drafts (status)

Small, issue-linked param data fixes prepared during prework. **Do not open** if another contributor already owns the fix.

| Draft | Issue | Status (2026-07-26) |
|-------|-------|---------------------|
| `fix-stval-width-bounds/` | #2102 | **Do not open** — covered by others (#2103) |
| `fix-hpm-events-dup-index/` | #2046 | **Do not open** — covered by others (#2047) |
| `fix-hpm-mcountinhibit-typo/` | typo | Superseded by HPM_EVENTS draft |
| `fix-mtvec-base-alignment-4096/` | power-of-two enum | **Do not open competing PR** while maintainer PR #2090 edits same files; raised as review comment instead |

Public upstream contribution so far: comment on [riscv-unified-db#2090](https://github.com/riscv/riscv-unified-db/pull/2090) (MTVEC enum `0xfff` vs power-of-two / `0x1000`).

Open a new draft only after a fresh audit finds an **original, unclaimed, deterministic** defect with a regression test.
