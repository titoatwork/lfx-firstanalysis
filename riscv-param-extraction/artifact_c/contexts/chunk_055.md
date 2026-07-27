## CSR and field reference for this excerpt
Definitions of CSRs named in the text above. Reference material only.

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

### CSR `sip`
Supervisor Interrupt Pending | address 324 | privilege S

A restricted view of the interrupt pending bits in `mip`.

Hypervisor-related interrupts (VS-mode interrupts and Supervisor Guest interrupts) are not reflected
in `sip` even though those interrupts can be taken in HS-mode. Instead, they are reported through `hip`.

Fields:
- `SSIP` (bits 1), access RW
    *Supervisor Software Interrupt Pending*
    
    Reports the current pending state of an (H)S-mode software interrupt.
    
    When Supervisor Software Interrupts are not delegated to (H)S-mode (`mideleg.SSI` is clear), `sip.SSIP` is read-only 0.
    
    Otherwise, `sip.SSIP` is an alias of `mip.SSIP`.
    
    When using AIA/IMSIC, IPIs are expected to be delivered as external interrupts
    and SSIP is not backed by any hardware update (aside from any aliasing effects).
    
    However, SSIP is still writable by S-mode software and, when written, can be used to
    generate an S-mode Software Interrupt.
    
    Since it is an alias, writes ...
- `STIP` (bits 5), access RO-H
    *Supervisor Timer Interrupt Pending*
    
    Reports the current pending state of an (H)S-mode timer interrupt.
    
    When Supervisor Timer Interrupts are not delegated to (H)S-mode (_i.e._, `mideleg.STI` is clear), `sip.STIP` is read-only 0.
    
    Otherwise, `sip.STIP` is a read-only view of `mip.STIP`.
    
    _Aliases__Alias_:
    
    * `mip.STIP` when `mideleg.STI` is set
    
    * `mvip.STIP` when `mideleg.SSI` is set and `menvcfg.STCE` is clear.
    
    To summarize:
    [separator="!",%autowidth]
    !===
    ! `mideleg.STI` ! `sip.STIP` behavior
    
    ! 0 ! read-only 0
    ! 1 ! read-only alias of `mip.STIP` (and `mvip.STIP` when `menvcfg.STCE` is ...
- `SEIP` (bits 9), access RO-H
    *Supervisor External Interrupt Pending*
    
    Reports the current pending state of an (H)S-mode external interrupt.
    
    When Supervisor External Interrupts are not delegated to (H)S-mode (_i.e._, `mideleg.SEI` is clear), `sip.SEIP` is read-only 0.
    
    Otherwise, `sip.SEIP` is a read-only view of `mip.SEIP`.
    
    To summarize:
    [separator="!",%autowidth]
    !===
    ! `mideleg.SEI` ! `sip.SEIP` behavior
    
    ! 0 ! read-only 0
    ! 1 ! read-only alias of `mip.SEIP`
    !===
- `LCOFIP` (bits 13), access RW-H
    *Local Counter Overflow Interrupt pending*
    
    Reports the current pending state of a Local Counter Overflow interrupt.
    
    When Local Counter Overflow interrupts are not delegated to (H)S-mode (_i.e._, `mideleg.LCOFI` is clear), `sip.LCOFIP` is read-only 0.
    
    Otherwise, `sip.LCOFIP` is an alias of `mip.LCOFIP`.
    
    Software writes 0 to `sip.LCOFIP` to clear the pending interrupt.
    
    To summarize:
    [separator="!",%autowidth]
    !===
    ! `mideleg.LCOFI` ! `sip.LCOFIP` behavior
    
    ! 0 ! read-only 0
    ! 1
    a! writable alias of `mip.LCOFIP` (and `vsip.LCOFIP` when `hideleg.LCOFI` is set)
    !===

### CSR `senvcfg`
Supervisor Environment Configuration | address 266 | privilege S

Contains fields that control certain characteristics of the U-mode execution environment.

Fields:
- `CBZE` (bits 7), access RW
    *Cache Block Zero instruction Enable*
    
    Bit is read-only 0 when `menvcfg.CBZE` is clear.
    
    Enables the execution of the cache block zero instruction, `cbo.zero`,
    in U-mode and (in conjunction with `henvcfg.CBZE`) VU-mode.
    
      * `0`: The instruction raises an illegal instruction or virtual instruction exception
      * `1`: The instruction is executed
    
    To summarize access:
    [separator="!",%autowidth]
    !===
    ! `menvcfg.CBZE` ! `senvcfg.CBZE` behavior
    
    ! 0 ! read-only 0
    ! 1
    a! writable, independent bit from `menvcfg.CBZE`
    !===
    
    See `cbo.zero` for a summary of the effect.
- `CBCFE` (bits 6), access RW
    *Cache Block Clean and Flush instruction Enable*
    
    Enables the execution of the cache block clean instruction, `cbo.clean`, and the
    cache block flush instruction, `cbo.flush`,
    
    in S-mode
    
    in U-mode
    .
    
      * `0`: The instruction raises an illegal instruction or virtual instruction exception
      * `1`: The instruction is executed
    
    To summarize access:
    [separator="!",%autowidth]
    !===
    ! `menvcfg.CBCFE` ! `senvcfg.CBCFE` behavior
    
    ! 0 ! read-only 0
    ! 1
    a! writable, independent bit from `menvcfg.CBCFE`
    !===
    
    See `cbo.clean` and/or `cbo.flush` for a summary of the effect.
- `CBIE` (bits 5-4), access RW-R
    *Cache Block Invalidate instruction Enable*
    
    This field has restricted values based on the value of `menvcfg.CBIE`.
    When an invalid value is written, it is ignored and the field remains unchanged.
    
    [separator="!",%autowidth,cols=",.>"]
    !===
    ! [.rotate]#`menvcfg.CBIE`# ! Valid values of `senvcfg.CBIE`
    
    ! 00 ! 00
    ! 01 ! 00, 01
    ! 11 ! 00, 01, 11
    !===
    
    Controls execution of the cache block invalidate instruction, `cbo.inval`,
    in U-mode
    
    and VU-mode (together with `henvcfg.CBIE`)
    
    .
    
      * `00`: The instruction raises an illegal instruction or virtual instruction exception
      * `01`: The instruction ...
- `SSE` (bits 3), access RW
    *Shadow Stack Enable*
    
    When the SSE field is set to 1, the Zicfiss extension is
    activated in VU/U-mode. When the SSE field is 0, the Zicfiss extension remains inactive
    in VU/U-mode, and the following rules apply:
    
      - 32-bit Zicfiss instructions will revert to their behavior as defined by Zimop.
    
      - 16-bit Zicfiss instructions will revert to their behavior as defined by Zcmop.
    
      - When menvcfg.SSE is one, SSAMOSWAP.W/D raises an illegal-instruction exception in U-mode
        and a virtual-instruction exception in VU-mode.
- `FIOM`, access RW
    *Fence of I/O implies Memory*
    
    When either `senvcfg.FIOM` or `menvcfg.FIOM` is set,
    FENCE instructions ordering I/O regions also implicitly order memory regions when executed
    in U-mode as follows:
    
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
    
    Similarly, in U-mode when ...

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

### CSR `sie`
Supervisor interrupt-enable register | address 260 | privilege S

Supervisor interrupt-enable register.

Fields:
- `SSIE` (bits 1), access RW
    Supervisor Software Interrupt Enable
- `STIE` (bits 5), access RW
    Supervisor Timer Interrupt Enable
- `SEIE` (bits 9), access RW
    Supervisor External Interrupt Enable
- `LCOFIE` (bits 13), access RW
    Local Counter Overflow Interrupt Enable

### CSR `time`
Timer for RDTIME Instruction | address 3073 | privilege U

[when,"PARAM_146 == false"]
This CSR does not exist, and access will cause an IllegalInstruction exception.

[when,"PARAM_146 == true"]
--
Shadow of the memory-mapped M-mode CSR `mtime`.

Privilege mode access is controlled with `mcounteren.TM`, `scounteren.TM`, and `hcounteren.TM` as ...

Fields:
- `COUNT` (bits 63-0), access RO-H
    Reports the current wall-clock time from the timer device.
    
    Alias of the `mtime` memory-mapped CSR.

### CSR `sepc`
Supervisor Exception Program Counter | address 321 | privilege S

Written with the PC of an instruction on an exception or interrupt taken in (H)S-mode.

Also controls where the hart jumps on an exception return from (H)S-mode.

Fields:
- `PC` (bits 63-0), access RW-RH
    When a trap is taken into S-mode, `sepc.PC` is written with the virtual address of the
    instruction that was interrupted or that encountered the exception.
    Otherwise, `sepc.PC` is never written by the implementation, though it may be explicitly written
    by software.
    
    On an exception return from S-mode (from the SRET instruction),
    control transfers to the virtual address read out of `sepc.PC`.
    
    Because PCs are always halfwordword-aligned,
    bit 0bits 1:0 of `sepc.PC` are always
    read-only 0.
    
    [when,"ext?(:C) && PARAM_065 == true"]
    When `misa.C` is clear, bit 1 is masked to zero. Writes to bit ...