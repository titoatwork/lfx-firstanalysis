Agreed on the locals and on `x0`, and the `x0` point does generalise past Zilsd.

On endianness, one caution before someone builds against it: there is nothing in the IDL to condition on today, and `read_memory` is not currently a place the problem can hide.

The five parameters never reach executable code. In `spec/`, `M_MODE_ENDIANNESS`, `S_MODE_ENDIANNESS`, `U_MODE_ENDIANNESS`, `VS_MODE_ENDIANNESS` and `VU_MODE_ENDIANNESS` are read only by `mstatus`, `mstatush`, `hstatus` and `vsstatus`, and only in `type()` and `reset_value()`, for example `return (M_MODE_ENDIANNESS == "dynamic") ? CsrFieldType::RW : CsrFieldType::RO;`. The one other reference is `Ssube.yaml`, which constrains `U_MODE_ENDIANNESS` under `requirements`, so it gates config validity rather than behaviour. Across all seven files under `spec/std/isa/isa/` the string `endian` appears **0** times. The generated hart gets a `#define UDB_M_MODE_ENDIANNESS_LITTLE`, but that symbol appears only where it is defined, in the two golden files, and is read nowhere. So "act based on the current privilege mode and the endianness of that mode" has no accessor to call.

The second half is the sharper one. A single aligned access does defer byte order outward: `read_memory_aligned` translates, access-checks and runs the memory-model hooks, then hands `LEN` and the physical address to `read_physical_memory` without touching byte order, which matches the interface @henrikg-qc described. But the misaligned path composes bytes in IDL, and that composition is unconditionally little-endian, on both sides:

```
result = result | (read_memory_aligned(8, virtual_address + I, encoding, 1'b0, 1'b0) `<< (8*I));
write_memory_aligned(8, virtual_address + I, (value >> (8*I))[7:0], encoding, 1'b0, 1'b0);
```

The byte at the lowest address takes the least-significant position, with no parameter consulted. `MISALIGNED_SPLIT_STRATEGY` only chooses between that and `"custom"`, which is `unpredictable`.

Latent rather than live: every config in `cfgs/` that sets these parameters sets `little`, so nothing in the tree exercises it. But it does mean hiding the pair semantics inside `read_memory` would inherit the gap rather than avoid it. Worth deciding whether this issue depends on that being modelled first, or is explicitly scoped to leave it alone.
