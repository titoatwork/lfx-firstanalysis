## CSR and field reference for this excerpt
Definitions of CSRs named in the text above. Reference material only.

### CSR `henvcfg`
Hypervisor Environment Configuration | address 1546 | privilege S

The henvcfg CSR is a 64-bit read/write register that controls certain characteristics of the
execution environment when virtualization mode V=1.

If bit `henvcfg.FIOM` (Fence of I/O implies Memory) is set to one in henvcfg, `fence`
instructions executed when V=1 are modified so the requirement to order accesses to device I/O
implies also the requirement to order main memory ...

Fields:
- `STCE` (bits 63)
    *STimecmp Enable*
    
    When set, `stimecmp` is operational in VS-mode if `menvcfg.STCE` is also set.
    
    When `menvcfg.STCE` is zero:
     * `henvcfg.STCE` reads-as-zero
     * `vstimecmp` access raises an `IllegalInstruction` exception.
     * `hip.VSTIP` reverts to its defined behavior as if Sstc is not implemented.
     * VS-mode timer interrupts will not be generated
    
    When `menvcfg.STCE` is one and `henvcfg.STCE` is zero:
     * Accessing `stimecmp` in VS-mode or VU-mode (really `vstimecmp`) raises a VirtualInterrupt exception
     * `hip.VSTIP` reverts to its defined behavior as if Sstc is not implemented.
     * VS-mode ...
- `PBMTE` (bits 62)
    *Page Based Memory Type Enable*
    
    The PBMTE bit controls whether the `Svpbmt` extension is available for use in VS-stage
    address translation.
    
    When PBMTE=1, Svpbmt is available for VS-stage address translation.
    
    When PBMTE=0, the implementation behaves as though `Svpbmt` were not implemented for
    VS-stage address translation.
    
    If `Svpbmt` is not implemented, PBMTE is read-only zero.
    
    `henvcfg.PBMTE` is read-as-zero if `menvcfg.PBMTE` is zero.
    
    If the setting of the PBMTE bit in `menvcfg` is changed, an `hfence.gvma` instruction with
    _rs1_=_x0_ and _rs2_=_x0_ suffices to synchronize with respect ...
- `ADUE` (bits 61)
    If the `Svadu` extension is implemented, the ADUE bit controls whether hardware updating of
    PTE A/D bits is enabled for VS-stage address translation.
    
    When ADUE=1, hardware updating of PTE A/D bits is enabled during VS-stage address
    translation, and the implementation behaves as though the Svade extension were not
    implemented for VS-mode address translation.
    
    When ADUE=0, the implementation behaves as though Svade were implemented for VS-stage
    address translation.
    
    If Svadu is not implemented, ADUE is read-only zero.
    
    Furthermore, for implementations with the hypervisor extension, ...
- `CBZE` (bits 7), access RW
    *Cache Block Zero instruction Enable*
    
    Enables the execution of the cache block zero instruction, `CBO.ZERO`,
    
    in S-mode
    
    in U-mode
    .
    
      * `0`: The instruction raises an illegal instruction or virtual instruction exception
      * `1`: The instruction is executed
- `CBCFE` (bits 6), access RW
    *Cache Block Clean and Flush instruction Enable*
    
    Enables the execution of the cache block clean instruction, `CBO.CLEAN`, and the
    cache block flush instruction, `CBO.FLUSH`,
    
    in S-mode
    
    in U-mode
    .
    
      * `0`: The instruction raises an illegal instruction or virtual instruction exception
      * `1`: The instruction is executed
- `CBIE` (bits 5-4), access RW-R
    *Cache Block Invalidate instruction Enable*
    
    Enables the execution of the cache block invalidate instruction, `CBO.INVAL`,
    
    in S-mode
    
    in U-mode
    .
    
      * `00`: The instruction raises an illegal instruction or virtual instruction exception
      * `01`: The instruction is executed and performs a flush operation
      * `10`: _Reserved_
      * `11`: The instruction is executed and performs an invalidate operation
- `SSE` (bits 3), access RW
    *Shadow Stack Enable*
    
    If the SSE field is set to 1, the Zicfiss extension is activated in VS-mode. When the SSE
    field is 0, the Zicfiss extension remains inactive in VS-mode, and the following rules apply
    when V=1 :
    
      - 32-bit Zicfiss instructions will revert to their behavior as defined by Zimop.
    
      - 16-bit Zicfiss instructions will revert to their behavior as defined by Zcmop.
    
      - The pte.xwr=010b encoding in VS-stage page tables becomes reserved.
    
      - The senvcfg.SSE field will read as zero and is read-only.
    
      - When menvcfg.SSE is one, SSAMOSWAP.W/D raises a virtual-instruction ...
- `FIOM`, access RW
    *Fence of I/O implies Memory*
    
    When `menvcfg.FIOM` is set,
    FENCE instructions ordering I/O regions also implicitly order memory regions when executed
    in any mode less privileged than M-mode.
    
    [separator="!",%autowidth,float="center",align="center",cols="^,<",options="header"]
    !===
    !Instruction bit !Meaning when set
    !PI +
    PO
    !Predecessor device input and memory reads (PR implied) +
    Predecessor device output and memory writes (PW implied)
    !SI +
    SO
    !Successor device input and memory reads (SR implied) +
    Successor device output and memory writes (SW implied)
    !===
    
    Similarly, for modes less ...

### CSR `menvcfg`
Machine Environment Configuration | address 778 | privilege M

Contains fields that control certain characteristics of the execution environment
for modes less privileged than M-mode.

The `menvcfg` CSR controls
certain characteristics of the execution environment for modes less
privileged than M.

If bit FIOM (Fence of I/O implies Memory) is set to one in `menvcfg`,
FENCE instructions executed in modes less privileged than M are modified
so the requirement ...

Fields:
- `STCE` (bits 63), access RW
    *STimecmp Enable*
    
    When set, `stimecmp` is operational.
    
    When clear, `stimecmp` access in a mode other than M-mode raises an `Illegal Instruction` trap.
    S-mode timer interrupts will not be generated when clear, and `mip` and `sip` revert to their prior behavior without `Sstc`.
- `PBMTE` (bits 62), access RW
    *Page Based Memory Type Enable*
    
    The PBMTE bit controls whether the Svpbmt extension is available for use in S-modeand G-stage
    address translation (i.e., for page tables pointed to by satp or hgatp). When PBMTE=1, Svpbmt is
    available for S-mode  and G-stage  address translation. When PBMTE=0, the implementation behaves
    as though Svpbmt were not implemented. If Svpbmt is not implemented, PBMTE is read-only zero.
    
    Furthermore, henvcfg.PBMTE is read-only zero if
    menvcfg.PBMTE is zero.
    
    After changing `menvcfg.PBMTE`, executing an `sfence.vma` instruction with _rs1_=_x0_ and
    _rs2_=_x0_ suffices ...
- `ADUE` (bits 61)
    If the Svadu extension is implemented, the ADUE bit controls whether hardware updating of
    PTE A/D bits is enabled for S-mode and G-stage address translations. When ADUE=1, hardware
    updating of PTE A/D bits is enabled during S-mode address translation, and the
    implementation behaves as though the Svade extension were not implemented for S-mode address
    translation.
    
    When the hypervisor extension is implemented, if ADUE=1, hardware updating of PTE A/D bits
    is enabled during G-stage address translation, and the implementation behaves as though the
    Svade extension were not implemented for G-stage ...
- `CBZE` (bits 7), access RW
    *Cache Block Zero instruction Enable*
    
    Enables the execution of the cache block zero instruction, `CBO.ZERO`,
    
    in S-mode
    
    in U-mode
    .
    
      * `0`: The instruction raises an illegal instruction or virtual instruction exception
      * `1`: The instruction is executed
- `CBCFE` (bits 6), access RW
    *Cache Block Clean and Flush instruction Enable*
    
    Enables the execution of the cache block clean instruction, `CBO.CLEAN`, and the
    cache block flush instruction, `CBO.FLUSH`,
    
    in S-mode
    
    in U-mode
    .
    
      * `0`: The instruction raises an illegal instruction or virtual instruction exception
      * `1`: The instruction is executed
- `CBIE` (bits 5-4), access RW-R
    *Cache Block Invalidate instruction Enable*
    
    Enables the execution of the cache block invalidate instruction, `CBO.INVAL`,
    
    in S-mode
    
    in U-mode
    .
    
      * `00`: The instruction raises an illegal instruction or virtual instruction exception
      * `01`: The instruction is executed and performs a flush operation
      * `10`: _Reserved_
      * `11`: The instruction is executed and performs an invalidate operation
- `SSE` (bits 3), access RW
    *Shadow Stack Enable*
    
    When the SSE field is set to 1 the Zicfiss extension isactivated in S-mode. When SSE
    field is 0, the following rules apply to privilege modes that are less than M:
    
      - 32-bit Zicfiss instructions will revert to their behavior as defined by Zimop.
    
      - 16-bit Zicfiss instructions will revert to their behavior as defined by Zcmop.
    
      - The pte.xwr=010b encoding in VS/S-stage page tables becomes reserved.
    
      - SSAMOSWAP.W/D raises an illegal-instruction exception.
    
    When menvcfg.SSE is 0, the henvcfg.SSE and senvcfg.SSE fields are read-only zero.
- `FIOM`, access RW
    *Fence of I/O implies Memory*
    
    When `menvcfg.FIOM` is set,
    FENCE instructions ordering I/O regions also implicitly order memory regions when executed
    in any mode less privileged than M-mode.
    
    [separator="!",%autowidth,float="center",align="center",cols="^,<",options="header"]
    !===
    !Instruction bit !Meaning when set
    !PI +
    PO
    !Predecessor device input and memory reads (PR implied) +
    Predecessor device output and memory writes (PW implied)
    !SI +
    SO
    !Successor device input and memory reads (SR implied) +
    Successor device output and memory writes (SW implied)
    !===
    
    Similarly, for modes less ...