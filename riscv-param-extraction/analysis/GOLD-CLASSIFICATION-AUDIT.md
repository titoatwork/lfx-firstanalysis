# Auditing the gold's classifications against UnifiedDB structure

**Objective 2 of the Part II project is "extend the classification scheme, only with
evidence."** This is a slice of that, delivered before the term rather than described.

Every recall and classification figure in this repository is scored against a pinned
gold of 185 parameters. Each entry carries a class from `taxonomy.md`, a confidence,
and a free-text reason. Those labels were produced by a model. This audit does not
re-run one. It asks a narrower question that the data can answer on its own:

> For which parameters does UnifiedDB itself decide the class, and where does that
> decision disagree with the gold?

Reproduce, offline and free:

```bash
python scripts/audit_gold_classification.py
```

---

## What the data decides

`taxonomy.md` defines `NORM_CSR_WARL` as the case where "the parameter **is** the set
of legal values". UnifiedDB expresses that in two idioms, and both are mechanical:

```
membership    $array_includes?(P, csr_value.X)    legalises a write against P
cardinality   $array_size(P) <op>                 the size of P decides RO vs RW
```

Ten parameters are consumed that way. Eight are in the pinned gold. The gold agrees
on four and disagrees on four.

## Finding 1: four legal-value sets are labelled `NORM_DIRECT`

| Parameter | Gold | Confidence | Idiom | Gold's stated reason |
|---|---|---|---|---|
| `SXLEN` | `NORM_DIRECT` | high | membership, cardinality | "Well-known architectural parameter 'SXLEN'" |
| `UXLEN` | `NORM_DIRECT` | high | cardinality | "Well-known architectural parameter 'UXLEN'" |
| `VSXLEN` | `NORM_DIRECT` | high | membership, cardinality | "Well-known architectural parameter 'VSXLEN'" |
| `VUXLEN` | `NORM_DIRECT` | high | cardinality | "Well-known architectural parameter 'VUXLEN'" |

All four have the same schema shape as `MTVEC_MODES` and `MSTATUS_FS_LEGAL_VALUES`,
which the gold labels `NORM_CSR_WARL` and which `taxonomy.md` names as its own
examples of that class: `type: array` over an enumerated `items`, bounded by
`minItems`/`maxItems`, with `uniqueItems: true`. That is the encoding of a set of
legal values.

The schema shape is suggestive on its own. What settles it is that the CSR
definitions compute field mutability from the parameter's cardinality:

| Parameter | Field | Site on `main` | What the parameter decides |
|---|---|---|---|
| `SXLEN` | `mstatus.SXL` | `spec/std/isa/csr/mstatus.yaml:197` in `type()` | `$array_size(SXLEN) > 1` selects `RW` over `RO` |
| `UXLEN` | `mstatus.UXL` | `spec/std/isa/csr/mstatus.yaml:247` in `type()` | `$array_size(UXLEN) > 1` selects `RW` over `RO` |
| `VSXLEN` | `hstatus.VSXL` | `spec/std/isa/csr/hstatus.yaml:49-54` in `type()` | `$array_size(VSXLEN) == 1` selects `RO` |
| `VUXLEN` | `vsstatus.UXL` | `spec/std/isa/csr/vsstatus.yaml:60-62` in `type()`, `reset_value()` | size selects `RW` over `RO`; reset returns `UNDEFINED_LEGAL` or `VUXLEN[0]` |

A parameter whose cardinality decides whether a CSR field is writable is that
field's set of legal values, which is what `NORM_CSR_WARL` denotes. Same encoding,
same consumption, opposite label.

One precision, because it is the reason a heuristic missed these: the idioms for
these four sit in `type()` and `reset_value()`, whereas `MTVEC_MODES` and
`MSTATUS_FS_LEGAL_VALUES` are consumed in `sw_write()`. The idiom is shared; the
enclosing function is not.

**The reason column is the mechanism.** Twenty-one of the 185 entries carry a reason
of the form "Well-known architectural parameter 'X'". All 21 are `high` confidence
and all 21 are `NORM_DIRECT`. Where the classifier recognised a name it stopped
looking at structure, and the failure is one-directional.

## Finding 2: the class is not decidable from syntax for most of its members

Of the 26 gold entries labelled `NORM_CSR_WARL`:

| | count |
|---|---:|
| confirmed by a decidable idiom | 4 |
| parameter no longer exists in UnifiedDB | 4 |
| not decidable from syntax | 18 |

The 18 are not errors. They are the region where `taxonomy.md`'s two CSR classes
cannot be separated by inspection, because the same syntax serves both roles:

```
if (SATP_MODE_BARE && csr_value.MODE == 0)   decides whether one value is legal
if (JVT_READ_ONLY) return CSR[jvt].BASE      gates mutability, ignores the write
```

Both are a bare boolean test inside `sw_write`. Telling them apart needs the
surrounding logic, not a pattern.

**Two heuristics were built for this and both discarded.** Proximity to `csr_value`
misfiled the whole `SV*X4_TRANSLATION` family; the enclosing IDL function misfiled
`JVT_READ_ONLY` and `MTVEC_ILLEGAL_WRITE_BEHAVIOR` as legal-value sets while missing
`SXLEN` entirely. Both were caught only against cases already read by hand. The
script now reports the undecidable region instead of guessing at it, and says so.

This is the same boundary reported upstream as
[#2200](https://github.com/riscv/riscv-unified-db/issues/2200), where `taxonomy.md`'s
`NORM_CSR_WARL` definition and its decision tree disagree. That issue argued the
boundary is ambiguous. This measures how much of the class sits inside the ambiguity:
**18 of 26.**

## Finding 3: four gold entries name parameters that no longer exist

`STVEC_MODE_DIRECT`, `STVEC_MODE_VECTORED`, `VSTVEC_MODE_DIRECT` and
`VSTVEC_MODE_VECTORED` were deleted by `90a989bf`, which is upstream PR
[#2090](https://github.com/riscv/riscv-unified-db/pull/2090), the same PR where a
review comment of mine was adopted. The gold has not been regenerated since, so four
of the 185 entries score against parameters the database dropped.

An unfiltered `git grep` over the whole `main` tree returns zero files for all four
names, with known-present names used as controls to prove the search works. A code
search alone would not settle this, because it is a filtered index.

## What this changes, and what it does not

It does not change any recall figure in this repository. Recall is scored on
parameter names, and none of these findings adds or removes a name.

It does bear on **classification accuracy**, which is computed only over exact
matches with a non-null `class_match`. Four systematically wrong labels and four
stale entries sit inside that denominator.

It does not claim the 18 undecidable entries are wrong. It claims they are not
checkable from the data, which is a different and more useful statement: it locates
exactly where a classifier has to reason rather than pattern-match, and 21 entries
show what happens when it does not.

## Honest limits

- The two idioms are a **sufficient** condition for a legal-value set, not a
  necessary one. A set encoded as a family of per-value booleans is invisible to them.
- `STVEC_MODES` and `VSTVEC_MODES` are consumed as legal-value sets but are absent
  from the 185-parameter freeze, so they are reported and not scored.
- No model was run. Nothing here measures whether a model would classify better; it
  measures where the existing labels are checkable.

## Provenance

Every count above is gated in `scripts/verify_claims.py` under the `gold_audit` tag
and re-derives from `analysis/gold_classification_audit.json`:

```bash
python scripts/verify_claims.py --tag gold_audit
```

The artifact's `provenance` block pins both inputs, so a reader can confirm they held
the same bytes rather than taking the counts on trust:

- `gold_canonical_sha256` digests the gold's **parsed** content. A digest of the raw
  bytes would be useless for citation: this checkout has `core.autocrlf` on, so the
  local file is CRLF while the upstream blob is LF. The two hash differently and parse
  identically. The pinned gold was confirmed against the upstream copy this way, and
  the parsed documents are equal.
- `scanned_sha256` digests the 396 CSR files and 227 parameter files actually read,
  with newlines normalised. A git revision alone would not pin this, since the tree
  can be dirty or can be an export rather than a checkout.

The committed run scans a topic-branch checkout. The audit was re-run against an
export of `main`'s two scanned trees: every count and every name list came out
identical, while `scanned_sha256` differed, which shows the trees genuinely differed
and the findings do not depend on which of them is read. Two limits of that check are
recorded in the harness under `UNVERIFIABLE`, because the comparison itself is a
session result rather than a committed artifact.

The gold audited here is the 185-entry freeze. Upstream, that file exists only inside
the unmerged PR [#1766](https://github.com/riscv/riscv-unified-db/pull/1766); there is
no `param_extraction/` tree on `main`.
