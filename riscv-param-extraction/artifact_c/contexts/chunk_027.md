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

### CSR `ssp`
Shadow Stack Pointer | address 17 | privilege U

The `ssp` CSR is an unprivileged read-write (URW) CSR that reads and writes
XLEN low order bits of the shadow stack pointer. The `ssp` is always as wide
as the XLEN of the current privilege mode. The bits 1:0 of ssp are read-only
zero. If the PARAM_173 or PARAM_144 may never be 32, then the bit 2 is also read-only
zero.

Fields:
- `VALUE` (bits 63-3), access RW
    The value in ssp points to the top of the shadow stack, which is the address
    of the last element stored on the shadow stack.

### CSR `dcsr`
Debug Control and Status Register | address 1968 | privilege D

Upon entry into Debug Mode, v and prv are updated with the privilege level the hart was previously in,
and cause is updated with the reason for Debug Mode entry. Other than these fields and nmip, the
other fields of dcsr are only writable by the external debugger.

Priority of reasons for entering Debug Mode from highest to lowest is shown below.
5:: resethaltreq
6:: halt group
3:: haltreq
2:: ...

Fields:
- `DEBUGVER` (bits 31-28), access RO
    0 (none):: There is no debug support.
    4 (1.0):: Debug support exists as it is described in this document.
    15 (custom):: There is debug support, but it does not conform to any available version of this spec.
- `EXTCAUSE` (bits 26-24), access RO
    When cause is 7, this optional field contains the value of a more specific halt reason than "other."
    Otherwise it contains 0.
    
    0 (critical error):: The hart entered a critical error state, as defined in the Smdbltrp extension.
    
    All other values are reserved for future versions of this spec, or for use by other RISC-V extensions.
- `CETRIG` (bits 19), access RW
    This bit is part of Smdbltrp and only exists when that extension is implemented.
    0 (disabled):: A hart in a critical error state does not enter
    Debug Mode but instead asserts the critical-error signal to
    the platform.
    1 (enabled):: A hart in a critical error state enters Debug
    Mode instead of asserting the critical-error signal to the
    platform. Upon such entry into Debug Mode, the cause
    field is set to 7, and the extcause field is set to 0, indicating
    a critical error triggered the Debug Mode entry. This cause
    has the highest priority among all reasons for entering
    Debug Mode. Resuming from ...
- `PELP` (bits 18), access RW
    This bit is part of Zicfilp and only exists when that extension is implemented.
    0 (NO_LP_EXPECTED):: No landing pad instruction expected.
    1 (LP_EXPECTED):: A landing pad instruction is expected.
- `EBREAKVS` (bits 17), access RW
    0 (exception):: ebreak instructions in VS-mode behave as described in the Privileged Spec.
    1 (debug mode):: ebreak instructions in VS-mode enter Debug Mode.
    This bit is hardwired to 0 if the hart does not support virtualization mode.
- `EBREAKVU` (bits 16), access RW
    0 (exception):: ebreak instructions in VU-mode behave as described in the Privileged Spec.
    1 (debug mode):: ebreak instructions in VU-mode enter Debug Mode.
    This bit is hardwired to 0 if the hart does not support virtualization mode.
- `EBREAKM` (bits 15), access RW
    0 (exception):: ebreak instructions in M-mode behave as described in the Privileged Spec.
    1 (debug mode):: ebreak instructions in M-mode enter Debug Mode.
- `EBREAKS` (bits 13), access RW
    0 (exception):: ebreak instructions in S-mode behave as described in the Privileged Spec.
    1 (debug mode):: ebreak instructions in S-mode enter Debug Mode.
    This bit is hardwired to 0 if the hart does not support S-mode.
- `EBREAKU` (bits 12), access RW
    0 (exception):: ebreak instructions in U-mode behave as described in the Privileged Spec.
    1 (debug mode):: ebreak instructions in U-mode enter Debug Mode.
    This bit is hardwired to 0 if the hart does not support U-mode.
- `STEPIE` (bits 11)
    0 (interrupts disabled):: Interrupts (including NMI) are disabled during single stepping with step set.
    This value should be supported.
    1 (interrupts enabled):: Interrupts (including NMI) are enabled during single stepping with step set.
    Implementations may hard wire this bit to 0. In that case interrupt behavior can be emulated by the
    debugger. The debugger must not change the value of this bit while the hart is running.
- `STOPCOUNT` (bits 10)
    0 (normal):: Increment counters as usual.
    1 (freeze):: Don’t increment any hart-local counters while in Debug Mode or on ebreak instructions
    that cause entry into Debug Mode. These counters include the instret CSR. On single-hart cores cycle
    should be stopped, but on multi-hart cores it must keep incrementing.
    An implementation may hardwire this bit to 0 or 1.
- `STOPTIME` (bits 9)
    0 (normal):: time continues to reflect mtime.
    1 (freeze):: time is frozen at the time that Debug Mode was entered. When leaving Debug Mode,
    time will reflect the latest value of mtime again.
    While all harts have stoptime=1 and are in Debug Mode, mtime is allowed to stop incrementing.
    An implementation may hardwire this bit to 0 or 1.

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

### CSR `mseccfg`
Machine Security Configuration | address 1863 | privilege M

Machine Security Configuration

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