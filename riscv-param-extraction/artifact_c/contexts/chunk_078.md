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

### CSR `hstatus`
Hypervisor Status | address 1536 | privilege S

The hstatus register tracks and controls a VS-mode guest.

Unlike fields in `sstatus`, which are all aliases of fields `mstatus`,
bits in `hstatus` are independent bits and do not have aliases.

Fields:
- `VSXL` (bits 33-32)
    [{'text': 'Determines the effective XLEN in VS-mode. Valid values are:\n\n[separator="!"]\n!===\n! Value ! PARAM_182\n\n! 0     ! 32\n! 1     ! 64\n!===\n', 'when()': 'return $array_size(PARAM_182) > 1;'}, {'text': 'Because the implementation only supports a single PARAM_182 == 32, this field is read-only-0.\n', 'when()': 'return $array_size(PARAM_182) == 1 && $array_includes?(PARAM_182, 32);'}, {'text': 'Because the implementation only supports a single PARAM_182 == 64, this field is read-only-1.\n', 'when()': 'return $array_size(PARAM_182) == 1 && $array_includes?(PARAM_182, 64);'}]
- `VTSR` (bits 22), access RW
    When `hstatus.VTSR` is set, executing the `sret` instruction in VS-mode
    raises a `Virtual Instruction` exception.
    
    When `hstatus.VTSR` is clear, an `sret` instruction in VS-mode returns control
    to the mode stored in `vsstatus.SPP`.
- `VTW` (bits 21), access RW
    When `hstatus.VTW` is set, a `wfi` instruction executed in VS-mode raises
    a `Virtual Instruction` exception after waiting an implementation-defined
    amount of time (which can be 0).
    
    When both `hstatus.VTW` and `mstatus.TW` are clear, a `wfi` instruction
    executes in VS-mode without a timeout period.
    
    The `wfi` instruction is also affected by `mstatus.TW`, as shown below:
    
    [separator="!",%autowidth,%footer]
    !===
    .2+! [.rotate]#`mstatus.TW`# .2+! [.rotate]#`hstatus.VTW`# 4+^.>! `wfi` behavior
    h! HS-mode h! U-mode h! VS-mode h! VU-mode
    
    ! 0 ! 0 ! Wait ! Trap (I) ! Wait ! Trap (V)
    ! 0 ! 1 ! Wait ! ...
- `VTVM` (bits 20), access RW
    When set, a 'Virtual Instruction` trap occurs when executing an `sfence.vma`, `sinval.vma`,
    or an explicit CSR access of the `satp` (really `vsatp`) register when in VS-mode.
    
    When clear, the instructions execute as normal in VS-mode.
    
    Notably, `hstatus.VTVM` does *not* cause `hfence.vvma`, `sfence.w.inval`, or `sfence.inval.ir` to trap.
    
    `mstatus.TVM` does not affect the VS-mode instructions controlled by `hstatus.TVTM`.
- `VGEIN` (bits 17-12)
    Selects the guest external interrupt source for VS-level external interrupts.
    
    When `hstatus.VGEIN` == 0, no external interrupt source is selected.
    
    When `hstatus.VGEIN` != 0, it selects which bit of `hgeip` is currently active in VS-mode.
- `HU` (bits 9), access RW
    When set, the hypervisor load/store instructions (`hlv`, `hlvx`, and `hsv`) can be
    executed in U-mode.
    
    When clear, the hypervisor load/store instructions cause an `Illegal Instruction` trap.
- `SPVP` (bits 8), access RW
    Written by hardware:
    
    * When taking a trap into HS-mode from VS-mode or VU-mode, `hstatus.SPVP` is written with the nominal privilege mode
    
    Notably, unlike its analog `mstatus.SPP`, `hstatus.SPVP` is *not* cleared when returning from a trap.
    
    Can also be written by software without immediate side-effect.
    
    Affects execution by:
    
    * Controls the effective privilege level applied to the hypervisor load/store instructions, `hlv`, `hlvx`, and `hsv`.
- `SPV` (bits 7), access RW
    Written by hardware:
    
    * On a trap into HS-mode, hardware writes 1 when the prior mode was VS-mode or VU-mode, and 0 otherwise.
    
    Can also be written by software without immediate side-effect.
    
    Affects execution by:
    
    * When an `sret` instruction in executed in HS-mode or M-mode,
      control returns to VS-mode or VU-mode (as selected by `mstatus.SPP`) when
      `hstatus.SPV` is 1 and to HS-mode or U-mode otherwise.
- `GVA` (bits 6), access RW
    Written by hardware whenever a trap is taken into HS-mode:
    
    * Writes 1 when a trap causes a guest virtual address to be written into `stval` (`Breakpoint`, `* Address Misaligned`, `* Access Fault`, `* Page Fault`, or `* Guest-Page Fault`).
    * Writes 0 otherwise
    
    Does not affect execution.
- `VSBE` (bits 5)
    [{'text': 'Controls the endianness of data VS-mode (0 = little, 1 = big).\nInstructions are always little endian, regardless of the data setting.\n'}, {'text': 'Since the CPU does not support big endian in VS-mode, this is hardwired to 0.\n', 'when()': 'return PARAM_183 == "little";'}, {'text': 'Since the CPU does not support little endian in VS-mode, this is hardwired to 1.\n', 'when()': 'return PARAM_183 == "big";'}]

### CSR `mseccfg`
Machine Security Configuration | address 1863 | privilege M

Machine Security Configuration

### CSR `stval`
Supervisor Trap Value | address 323 | privilege S

Holds trap-specific information

Fields:
- `VALUE` (bits 63-0), access RW-H
    Written with trap-specific information when a trap is taken into S-mode.
    
    The values are:
    
    [separator="!"]
    !===
    ! Exception type ! Value
    
    ! [0] Instruction address misaligned ! The misaligned virtual PC (same as the value written to `mepc`).
    ! [1] Instruction access fault ! The  portion of the  virtual PC causing the access fault (same as the value written to `mepc`).
    ! [2] Illegal Instruction ! The encoding of the illegal instruction.
    ! [3] Breakpoint
    ! [when,"PARAM_109 == true"]
      When caused by an EBREAK instruction, the virtual PC of the breakpoint instruction.
    
      ...

### CSR `satp`
Supervisor Address Translation and Protection | address 384 | privilege S

Controls the translation mode in (H)S-mode and U-mode, and holds the current ASID and page table base pointer.

Fields:
- `MODE` (bits 63-60), access RW-R
    *Translation Mode*
    
    Controls the current translation mode according to the table below.
    
    [separator="!",%autowidth]
    !===
    ! Value ! Name ! Description
    
    ! 0 ! Bare a! No translation -> virtual address == physical address
    
    ! 8 ! Sv39 ! 39-bit virtual address translation
    
    ! 9 ! Sv48 ! 48-bit virtual address translation
    
    ! 10 ! Sv57 ! 57-bit virtual address translation
    
    !===
    
    Any other value shall be ignored on a write.
- `ASID` (bits 59-44), access RW-R
    *Address Space ID*
- `PPN` (bits 43-0), access RW-R
    *Physical Page Number*
    
    The physical address of the active root page table is PPN << 12.
    
    Can only hold values that correspond to a valid page table base, which
    will be implementation-dependent.

### CSR `stvec`
Supervisor Trap Vector | address 261 | privilege S

Controls where traps jump.

Fields:
- `BASE` (bits 63-2), access RW-R
    Bit 63:0 of the virtual address of the exception vector for any trap taken into S-mode.
    
    If the base address is written with a non-cannonical address (_i.e._, bits 63: do not match bit ),
    the write should be ignored.
- `MODE` (bits 1-0), access RW-R
    Vectoring mode for asynchronous interrupts.
    
    0 - Direct, 1 - Vectored
    
    When Direct, all synchronous exceptions and asynchronous interrupts jump to (`stvec.BASE` << 2).
    
    When Vectored, asynchronous interrupts jump to (`stvec.BASE` << 2 + `scause.CAUSE`*4) while synchronous exceptions continue to jump to (`stvec.BASE` << 2).