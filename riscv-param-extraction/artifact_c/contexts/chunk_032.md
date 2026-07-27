## CSR and field reference for this excerpt
Definitions of CSRs named in the text above. Reference material only.

### CSR `misa`
Machine ISA Control | address 769 | privilege M

Reports the XLEN and "major" extensions supported by the ISA.

Fields:
- `MXL` (bits 63-62), access RO
    XLEN in M-mode.
- `A`
    Indicates support for the `A` (atomic) extension.
    
    [when,"PARAM_063 == true"]
    Writing 0 to this field will cause all atomic instructions to raise an `IllegalInstruction` exception.
- `B` (bits 1)
    Indicates support for the `B` (bitmanip) extension.
    
    [when,"PARAM_064 == true"]
    Writing 0 to this field will cause all bitmanip instructions to raise an `IllegalInstruction` exception.
- `C` (bits 2)
    Indicates support for the `C` (compressed) extension.
    
    [when,"PARAM_065 == true"]
    Writing 0 to this field will cause all compressed instructions to raise an `IllegalInstruction` exception.
    Additionally, IALIGN becomes 32.
- `D` (bits 3)
    Indicates support for the `D` (double precision float) extension.
    
    [when,"PARAM_066 == true"]
    --
    Writing 0 to this field will cause all double-precision floating point instructions to raise an `IllegalInstruction` exception.
    
    Additionally, the upper 32-bits of the f registers will read as zero.
    --
- `F` (bits 5)
    Indicates support for the `F` (single precision float) extension.
    
    [when,"PARAM_067 == true"]
    --
    Writing 0 to this field will cause all floating point (single and double precision) instructions to raise an `IllegalInstruction` exception.
    
    Writing 0 to this field with `misa.D` set will result in UNDEFINED behavior.
    --
- `G` (bits 6)
    Indicates support for all of the following extensions: `I`, `A`, `M`, `F`, `D`.
- `H` (bits 7)
    Indicates support for the `H` (hypervisor) extension.
    
    [when,"PARAM_068 == true"]
    Writing 0 to this field will cause all attempts to enter VS- or VU- mode, execute a hypervisor instruction, or access a hypervisor CSR to raise an `IllegalInstruction` fault.
- `I` (bits 8), access RO
    Indicates support for the `I` (base) extension.
- `M` (bits 12)
    Indicates support for the `M` (integer multiply/divide) extension.
    
    [when,"PARAM_069 == true"]
    Writing 0 to this field will cause all attempts to execute an integer multiply or divide instruction to raise an `IllegalInstruction` exception.
- `Q` (bits 16)
    Indicates support for the `Q` (quad precision float) extension.
    
    [when,"PARAM_070 == true"]
    --
    Writing 0 to this field will cause all quad-precision floating point instructions to raise an `IllegalInstruction` exception.
    --
- `S` (bits 18)
    Indicates support for the `S` (supervisor mode) extension.
    
    [when,"PARAM_071 == true"]
    Writing 0 to this field will cause all attempts to enter S-mode or access S-mode state to raise an exception.

### CSR `mstatus`
Machine Status | address 768 | privilege M

The mstatus register tracks and controls the hart's current operating state.

Fields:
- `SD` (bits 63)
    Read-only bit that summarizes whether either the FS, XS, or VS
    fields signal the presence of some dirty state.
- `MDT` (bits 42), access RW-H
    Written to 1 when entering M-mode from an exception/interrupt.
    When returning via an MRET instruction, the bit is written to 0.
    On reset in set to 1, and software should write it to 0 when boot sequence is done.
    When mstatus.MDT=1, direct write by CSR instruction cannot set mstatus.MIE to 1, if not written together.
- `MPV` (bits 39), access RW-H
    Written with the prior virtualization mode when entering M-mode from an exception/interrupt.
    When returning via an MRET instruction, the virtualization mode becomes the value of MPV unless MPP=3, in which case the virtualization mode is always 0.
    Can also be written by software.
- `GVA` (bits 38), access RW-H
    When a trap is taken and a guest virtual address is written into mtval, GVA is set.
    When a trap is taken and a guest virtual address is written into mtval, GVA is cleared.
- `MBE` (bits 37)
    Controls the endianness of data M-mode (0 = little, 1 = big).
    Instructions are always little endian, regardless of the data setting.
    
    [when,"PARAM_075 == little"]
    Since the CPU does not support big endian, this is hardwired to 0.
    
    [when,"PARAM_075 == big"]
    Since the CPU does not support little endian, this is hardwired to 1.
- `SBE` (bits 36)
    Controls the endianness of S-mode (0 = little, 1 = big).
    Instructions are always little endian, regardless of the data setting.
    
    [when,"PARAM_145 == little"]
    Since the CPU does not support big endian, this is hardwired to 0.
    
    [when,"PARAM_145 == big"]
    Since the CPU does not support little endian, this is hardwired to 1.
- `SXL` (bits 35-34)
    Sets the effective XLEN for S-mode (0 = 32-bit, 1 = 64-bit, 2 = 128-bit [reserved]).
    
    [when,"PARAM_144==32"]
    Since the CPU only supports PARAM_144==32, this is hardwired to 1.
    
    [when,"PARAM_144==64"]
    Since the CPU only supports PARAM_144==64, this is hardwired to 2.
    
    [when,"PARAM_144=3264"]
    --
    It is not valid to have PARAM_144 less than PARAM_173.
    
    It is UNDEFINED_LEGAL what will happen if a software sets `mstatus.SXL` to be greater than `mstatus.UXL`.
    
    It is UNDEFINED_LEGAL to set the MSB of SXL.
    --
- `UXL` (bits 33-32)
    U-mode XLEN.
    
    Sets the effective XLEN for U-mode (1 = 32-bit, 2 = 64-bit, 3 = 128-bit [reserved]).
    
    [when,"PARAM_173 == 32"]
    Since the CPU only supports PARAM_173==32, this is hardwired to 1.
    
    [when,"PARAM_173 == 64"]
    Since the CPU only supports PARAM_173==64, this is hardwired to 2.
    
    [when,"PARAM_173 == 3264"]
    --
    It is not valid to have PARAM_144 less than PARAM_173.
    
    It is UNDEFINED_LEGAL what will happen if a software sets `mstatus.SXL` to be greater than `mstatus.UXL`.
    
    It is UNDEFINED_LEGAL to set the MSB of UXL.
    --
- `TSR` (bits 22), access RW
    When 1, attempts to execute the `sret` instruction while executing in HS/S-mode
    will raise an Illegal Instruction exception.
    
    [when,"ext?(:H)"]
    Does not affect the behavior of `sret` in VS_mode (see `hstatus.VTSR`).
- `TW` (bits 21), access RW
    When 1, the WFI instruction will raise an Illegal Instruction trap after an
    implementaion-defined wait period when executed in a mode other than M-mode.
    
    When 0, the `wfi` instruction is permitted to wait forever in (H)S-mode but must
    trap after an implementation-defined wait period in U-mode.
- `TVM` (bits 20)
    When 1, an `Illegal Instruction` trap occurs when
    
    * writing the `satp` CSR, executing an `sfence.vma`, or executing an `sinval.vma` while in (H)S-mode (but not VS-mode)
    * writing the `hgtap` CSR, executing an `hfence.gvma`, or executing an `hinval.gvma` while in HS-mode
    
    Notably, `mstatus.TVM` does *not* cause
    
    *`hfence.vvma`, `sfence.w.inval`, or `sfence.inval.ir` to trap.
    * Any additional traps in VS-mode (controlled via `hstatus.VTVM` instead).
- `MXR` (bits 19), access RW
    When 1, loads from pages marked readable *or executable* are allowed.
    When 0, loads from pages marked executable raise a Page Fault exception.

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

### CSR `hedelegh`
Hypervisor Exception Delegation High | address 1554 | privilege S

Controls exception delegation from HS-mode to VS-mode.

Alias of upper bits of `hedeleg`[63:32].

### CSR `henvcfgh`
most-significant 32 bits of Hypervisor Environment Configuration | address 1562 | privilege S

The henvcfgh CSR is a 32-bit read/write register for the most-significant 32 bits of `henvcfg`.

Fields:
- `STCE` (bits 31)
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
- `PBMTE` (bits 30)
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
- `ADUE` (bits 29)
    If the `Svadu` extension is implemented, the ADUE bit controls whether hardware updating of
    PTE A/D bits is enabled for VS-stage address translation.
    
    When ADUE=1, hardware updating of PTE A/D bits is enabled during VS-stage address
    translation, and the implementation behaves as though the Svade extension were not
    implemented for VS-mode address translation.
    
    When ADUE=0, the implementation behaves as though Svade were implemented for VS-stage
    address translation.
    
    If Svadu is not implemented, ADUE is read-only zero.
    
    Furthermore, for implementations with the hypervisor extension, ...