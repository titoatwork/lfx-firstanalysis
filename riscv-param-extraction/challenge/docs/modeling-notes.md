# Modeling notes (challenge CMO snippet)

## Independent axes

The source sentence makes capacity, organization, and block size
**implementation-specific** together, but nothing in the text forces a shared
value space. Prefer **three parameters** over one bundled parameter.

This matches the review culture illustrated by upstream discussions such as
riscv-unified-db PR #2009 (split over-broad parameter modeling) — cited as
**public maintainer precedent**, not personal affiliation.

## CACHE_BLOCK_SIZE

- Exists upstream in UDB (`spec/std/isa/param/CACHE_BLOCK_SIZE.yaml`).
- Type integer, minimum 1, gated on Zicbom/Zicbop/Zicboz aligns with common UDB shape.
- This pack **omits maximum** when the snippet states no upper bound (more honest
  than encoding “unbounded” as 2**64-1 without spec text).

## CACHE_ORGANIZATION

- Opaque `string` schema: the excerpt does not enumerate organizations.
- Reasonable alternate judgment: **decline to emit** (schema-shaped false positive risk).
- Documented as SIG-scoping candidate.

## CSR §2.1

- Correct extract is **zero parameters**.
- Fixed conventions are not implementation-defined parameters.
