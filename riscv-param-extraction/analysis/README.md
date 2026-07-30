# Auditing the gold's own classification labels

Every recall and classification figure in this repository is scored against a pinned
gold of 185 parameters. Each entry carries a class from `taxonomy.md`, a confidence
and a free-text reason, and those labels were produced by a model. Neither audit here
re-runs one. Both ask a narrower question that UnifiedDB can answer on its own, and
they ask it two different ways.

| Audit | Question it asks | Script |
|---|---|---|
| [Gold classification](./GOLD-CLASSIFICATION-AUDIT.md) | how does the IDL **consume** this parameter? | `scripts/audit_gold_classification.py` |
| [Schema shapes](./PARAM-SCHEMA-SHAPES.md) | what **is** this parameter, per its own JSON schema? | `scripts/audit_param_schema_shapes.py` |

Both are offline, free, deterministic, and exit 0. Run either from
`riscv-param-extraction/`:

```bash
python scripts/audit_gold_classification.py      # add --json for the artifact
python scripts/audit_param_schema_shapes.py      # add --json for the artifact
```

Each writes a machine-readable companion, `gold_classification_audit.json` and
`param_schema_shapes.json`, whose `provenance` block pins the gold by a digest of its
**parsed** content rather than its bytes. That distinction matters: this checkout has
`core.autocrlf` on, so the local gold is CRLF while the upstream copy is LF, and the
two hash differently while parsing identically.

## Why there are two

`taxonomy.md:43` defines `NORM_CSR_WARL` as the case where "The parameter IS the set
of legal values." That can be checked from how the IDL uses a parameter, or from what
the parameter's schema declares it to be. The two routes share no code and no logic
beyond reading the same gold.

They agree. Out of 227 parameters, both single out the same four as labelled
`NORM_DIRECT` when the evidence says otherwise:

```
IDL-consumption method flags : SXLEN  UXLEN  VSXLEN  VUXLEN
schema-shape method flags    : SXLEN  UXLEN  VSXLEN  VUXLEN
```

Two routes that disagreed would mean one of them was wrong. Two that agree on four
names out of 227 is the reason the second one exists.

## What they do not claim

Neither audit claims the gold is bad work. The schema-shape audit finds the gold
labelling two of its three structural families **perfectly consistently**, including
the genuinely hard case that separates a set of legal values from a per-bit
writability mask, which no parameter name reveals.

Both audits also report the region they cannot decide rather than guessing at it. The
IDL audit measures that region at 18 of 26, and that measurement is the substance of
the comment on upstream issue
[#2200](https://github.com/riscv/riscv-unified-db/issues/2200).

Eighteen counts from the IDL audit are gated in `scripts/verify_claims.py` and
re-derive from the committed JSON:

```bash
python scripts/verify_claims.py --tag gold_audit
```

The schema-shape audit's counts are gated too, under their own tag:

```bash
python scripts/verify_claims.py --tag schema_shapes
```

That set includes the convergence itself as an invariant: the `set_enum` members
the gold calls `NORM_DIRECT` must equal the `disagree` list in the other audit's
artifact. The two are derived from different files by different logic, so if a
future edit breaks the agreement the harness fails rather than the two documents
quietly disagreeing.
