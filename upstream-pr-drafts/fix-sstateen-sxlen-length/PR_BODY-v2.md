`sstateen0` through `sstateen3` carry `length: MXLEN`, which sizes a supervisor CSR by a mode that does not define its width. They now take the `*stateen*` family's fixed `length: 64`. `hstateen0`-`hstateen3` are already `priv_mode: S` at a fixed 64, so this is an established shape rather than a new one; eight supervisor-visible CSRs use it today.

The `DATA` field on `sstateen1`, `sstateen2` and `sstateen3` collapses to `location: 31-0`, leaving bits 63-32 undefined and read-only zero. That is what the description already in these files says: "4 * 64 = 256 bits for machine and hypervisor levels, and 4 * 32 = 128 bits for supervisor level", and the upper 32 bits of an `mstateen` CSR control state "inherently inaccessible to user level, so no corresponding enable bits in the supervisor-level `sstateen` CSR are applicable". The absence of `sstateen0h`-`sstateen3h` in the tree agrees. A range narrower than its fixed-width register is the ordinary shape here: 291 fields already do it.

Keeping the `location_rv32`/`location_rv64` pair inside a fixed-width register would instead have made these the only CSRs of their kind. Of the 461 CSRs under `spec/`, the 137 with an XLEN-dependent field location all have a symbolic `length`, and none of the 288 with a fixed integer `length` do.

Closes #2394
