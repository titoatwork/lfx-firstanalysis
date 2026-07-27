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

### CSR `sstatus`
Supervisor Status | address 256 | privilege S

The sstatus register tracks and controls the hart's current operating state.

All fields in sstatus are aliases of the same field in mstatus.

Fields:
- `SD` (bits 63), access RO-H
    *State Dirty*
    
    Alias of `mstatus.SD`.
- `UXL` (bits 33-32), access RO
    *U-mode XLEN*
    
    Alias of `mstatus.UXL`.
- `MXR` (bits 19), access RW
    *Make eXecutable Readable*
    
    Alias of `mstatus.MXR`.
- `SUM` (bits 18), access RW
    *permit Supervisor Memory Access*
    
    Alias of `mstatus.SUM`.
- `XS` (bits 16-15), access RO
    Custom (X) extension context Status.
    
    Alias of `mstatus.XS`.
- `FS` (bits 14-13), access RW-H
    Floating point context status.
    
    Alias of `mstatus.FS`.
- `VS` (bits 10-9), access RW-H
    Vector context status.
    
    Alias of `mstatus.VS`.
- `SPP` (bits 8), access RW-H
    *S-mode Previous Privilege*
    
    Alias of `mstatus.SPP`.
- `UBE` (bits 6), access RO
    *U-mode Big Endian*
    
    Alias of `mstatus.UBE`.
- `SPIE` (bits 5), access RW-H
    *S-mode Previous Interrupt Enable*
    
    Alias of `mstatus.SPIE`.
- `SIE` (bits 1), access RW-H
    *S-mode Interrupt Enable*
    
    Alias of `mstatus.SIE`.

### CSR `vsstatus`
Virtual Supervisor Status | address 512 | privilege VS

The vsstatus register tracks and controls the hart's current operating state.

It is VS-mode's version of `sstatus`, and substitutes for it when in VS-mode
(_i.e._, in VS-mode CSR address 0x100 is `vsstatus`, not `sstatus`).

Unlike the relationship between `sstatus` and `mstatus`, none of the bits in `vsstatus` are
aliases of another field.

Fields:
- `SD` (bits 63), access RO-H
    *State Dirty*
    
    Read-only bit that summarizes whether any of the
    `vsstatus.FS`,  `vsstatus.VS`,  or `vsstatus.XS`
    fields signal the presence of some dirty state
    (_i.e._, any of them hold the value `11`).
    
    This bit is _not_ an alias of `mstatus.SD` since
    it only reflects the state visible to VS-mode
    (_e.g._, `status.FS` does not affect `vsstatus.SD`).
- `UXL` (bits 33-32)
    *VU-mode XLEN*
    
    Sets the effective XLEN for VU-mode (0 = 32-bit, 1 = 64-bit, 2 = 128-bit).
    
    [when,"PARAM_184 == 32"]
    Since the hart only supports PARAM_184==32, this is hardwired to 0.
    
    [when,"PARAM_184 == 64"]
    Since the hart only supports PARAM_184==64, this is hardwired to 1.
- `MXR` (bits 19), access RW
    *Make eXecutable Readable*
    
    Makes it possible to read executable pages when loading from effective VU-mode or VS-mode
    (normally, executable pages are not readable).
    
    * When 1, load in effective VU-mode or VS-mode from pages marked readable *or executable*
      are allowed as long as the page is marked readable (or executable and `status.MXR` is set) in the
      G-stage translation.
    * When 0, load in effective VU-mode or VS-mode from pages marked executable raise a
      Page Fault exception (unless `sstatus.MXR` is also set, in which case the above applies).
    
    'vsstatus.MXR' affects all loads that ...
- `SUM` (bits 18), access RW
    *permit Supervisor Memory Access*
    
    Allows VS-mode to read user pages.
    
    Applies to the following loads and stores:
    
    * All loads and stores in VS-mode.
    * All loads and stores in M-mode when `mstatus.MPRV` == 1, `mstatus.MPP` == 1, and `mstatus.MPV` == 1
    * Loads and stores generated by one of the `hlv.*`, `hlvx.*`, or `hsv.*` instructions.
    
    When `vsstatus.SUM` is 0, the loads and stores from the above categories cause an
    `Illegal Instruction` exception if they access a user page during VS-level translation.
    Otherwise, a load or store from the above categories is permitted to access a user ...
- `XS` (bits 16-15), access RO
    *Custom (X) extension context Status*
    
    Summarizes the current state of any custom extension state.
    Either 0 - Off, 1 - Initial, 2 - Clean, 3 - Dirty.
    Since there are no custom extensions, this field is read-only 0.
- `FS` (bits 14-13), access RW-H
    *Floating point context status*
    
    When 0, floating point instructions (from F and D extensions) in VS-mode or VU-mode are disabled,
    and cause ILLEGAL INSTRUCTION exceptions.
    Floating point instructions in all modes, including VS-mode and VU-mode,
    are similarly disabled when `mstatus.FS` is clear.
    
    When a floating point register, or the `fcsr` register is written in VS-mode or VU-mode,
    `vsstatus.FS` is written with the value 3.
    
    Values 1 and 2 are valid write values for software, but are not interpreted by hardware
    other than to possibly enable a previously-disabled floating point unit.
- `VS` (bits 10-9), access RW-H
    *Vector context status*
    
    When 0, vector instructions (from the V extension) are disabled, and cause ILLEGAL INSTRUCTION exceptions.
    When a vector register or vector CSR is written, VS obtains the value 3.
    Values 1 and 2 are valid write values for software, but are not interpreted by hardware
    other than to possibly enable a previously-disabled vector unit.
- `SPP` (bits 8), access RW-H
    *VS-mode Previous Privilege*
    
    Written with the prior nominal privilege level (_i.e._, 0 for VU-mode and 1 for VS-mode)
    when entering VS-mode from an exception/interrupt.
    Can also be written by software without immediate side-effect.
    
    On a return from an exception from VS-mode, the machine will enter the nominal privilege level
    stored in `vsstatus.SPP`.
- `UBE` (bits 6)
    *VU-mode Big Endian*
    
    Controls the endianness of VU-mode (0 = little, 1 = big).
    
    [when,"PARAM_185 == 'little'"]
    Since the CPU does not support big endian, this is hardwired to 0.
    
    [when,"PARAM_185 == 'big'"]
    Since the CPU does not support big endian, this is hardwired to 1.
- `SPIE` (bits 5), access RW-H
    *VS-mode Previous Interrupt Enable*
    
    Written by hardware in two cases:
    
    * Written with prior value of `vsstatus.SIE` when entering VS-mode from an exception/interrupt.
    * Written with the value 1 when returning from an exception in VS-mode (via the `sret` instruction).
    
    Can also be written by software without immediate side effect.
    
    Other than serving as a record of nested traps as described above, `vsstatus.SPIE` does not affect execution.
- `SIE` (bits 1), access RW-H
    *VS-mode Interrupt Enable*
    
    Written by hardware in two cases:
    
    * Written with the value 0 when entering VS-mode from an exception/interrupt.
    * Written with the prior value of `vsstatus.SPIE` when returning from an exception in VS-mode (via `sret`).
    
    Affects execution by:
    
    * When 0, all VS-mode interrupts are disabled when the current privilege level is VS ((H)S-mode and M-mode interrupts are still enabled).
    * When 1, VS-mode interrupts that are not otherwise disabled with a field in `vsie` are enabled.