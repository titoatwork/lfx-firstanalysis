# Coding challenge: upload pack

Ibteshamul Haque (`@titoatwork`), LFX Fall 2026 Part II.

**Read `SUBMISSION.md` first.** It answers the three required items in order, and
section 4 records what happened when the extracted parameters were checked
against the live RISC-V Unified Database.

```text
coding-challenge-submission/
  SUBMISSION.md             # the submission: LLMs, prompts, results, cross-check
  LLM-DETAILS.md            # ten models on both snippets, full pass/fail matrix
  prompts/                  # v1 naive, v2 keyword-anchored, v3 final
  snippets/                 # the two challenge snippets, verbatim, + NOTICE.md
  results/
    cmo_cache_blocks.yaml   # 3 parameters, fields as the challenge asks
    csr_address_mapping.yaml  # empty list, which is the correct answer
    udb-shaped/             # same extraction in real UDB schema + EVIDENCE.json
```

**Minimum upload if the form takes only a few files:**
`SUBMISSION.md`, `results/cmo_cache_blocks.yaml`, `results/csr_address_mapping.yaml`,
`prompts/v3_final.txt`.

## The short version

Snippet 1 yields three parameters, of which the database currently models one.
Snippet 2 yields zero, and four of ten models hallucinated one anyway.

The constraint the snippet states most plainly, that a cache block is a naturally
aligned power of two, was missing from the database's own file for that
parameter. It is encoded here, and upstream, because I filed
[#2188](https://github.com/riscv/riscv-unified-db/issues/2188) and fixed it in
[#2189](https://github.com/riscv/riscv-unified-db/pull/2189).

## Attribution

The snippets are RISC-V ISA Manual text, CC-BY-4.0. See
[`snippets/NOTICE.md`](./snippets/NOTICE.md). Everything else here is my own work
under the repository [LICENSE](../LICENSE).
