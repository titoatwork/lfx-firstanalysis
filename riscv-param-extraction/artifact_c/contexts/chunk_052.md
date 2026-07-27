## CSR and field reference for this excerpt
Definitions of CSRs named in the text above. Reference material only.

### CSR `scountovf`
Supervisor Count Overflow | address 3488 | privilege S

A 32-bit read-only register that contains shadow copies of the OF bits in the 29 `mhpmevent` CSRs
(`mhpmevent3` - `mhpmevent31`) — where `scountovf` bit X corresponds to `mhpmeventX`.

This register enables supervisor-level overflow interrupt handler
software to quickly and easily determine which counter(s) have overflowed
without needing to make an execution environment call up to M-mode.

Read ...

Fields:
- `OF3` (bits 3)
    [when="PARAM_018[3] == true"]
    Shadow copy of mhpmevent3 overflow (OF) bit.
    
    [when="PARAM_018[3] == false"]
    This field is read-only zero because the counter is not enabled.
- `OF4` (bits 4)
    [when="PARAM_018[4] == true"]
    Shadow copy of mhpmevent4 overflow (OF) bit.
    
    [when="PARAM_018[4] == false"]
    This field is read-only zero because the counter is not enabled.
- `OF5` (bits 5)
    [when="PARAM_018[5] == true"]
    Shadow copy of mhpmevent5 overflow (OF) bit.
    
    [when="PARAM_018[5] == false"]
    This field is read-only zero because the counter is not enabled.
- `OF6` (bits 6)
    [when="PARAM_018[6] == true"]
    Shadow copy of mhpmevent6 overflow (OF) bit.
    
    [when="PARAM_018[6] == false"]
    This field is read-only zero because the counter is not enabled.
- `OF7` (bits 7)
    [when="PARAM_018[7] == true"]
    Shadow copy of mhpmevent7 overflow (OF) bit.
    
    [when="PARAM_018[7] == false"]
    This field is read-only zero because the counter is not enabled.
- `OF8` (bits 8)
    [when="PARAM_018[8] == true"]
    Shadow copy of mhpmevent8 overflow (OF) bit.
    
    [when="PARAM_018[8] == false"]
    This field is read-only zero because the counter is not enabled.
- `OF9` (bits 9)
    [when="PARAM_018[9] == true"]
    Shadow copy of mhpmevent9 overflow (OF) bit.
    
    [when="PARAM_018[9] == false"]
    This field is read-only zero because the counter is not enabled.
- `OF10` (bits 10)
    [when="PARAM_018[10] == true"]
    Shadow copy of mhpmevent10 overflow (OF) bit.
    
    [when="PARAM_018[10] == false"]
    This field is read-only zero because the counter is not enabled.
- `OF11` (bits 11)
    [when="PARAM_018[11] == true"]
    Shadow copy of mhpmevent11 overflow (OF) bit.
    
    [when="PARAM_018[11] == false"]
    This field is read-only zero because the counter is not enabled.
- `OF12` (bits 12)
    [when="PARAM_018[12] == true"]
    Shadow copy of mhpmevent12 overflow (OF) bit.
    
    [when="PARAM_018[12] == false"]
    This field is read-only zero because the counter is not enabled.
- `OF13` (bits 13)
    [when="PARAM_018[13] == true"]
    Shadow copy of mhpmevent13 overflow (OF) bit.
    
    [when="PARAM_018[13] == false"]
    This field is read-only zero because the counter is not enabled.
- `OF14` (bits 14)
    [when="PARAM_018[14] == true"]
    Shadow copy of mhpmevent14 overflow (OF) bit.
    
    [when="PARAM_018[14] == false"]
    This field is read-only zero because the counter is not enabled.

### CSR `mcounteren`
Machine Counter Enable | address 774 | privilege M

The counter-enable `mcounteren` register is a 32-bit register that controls the availability
of the hardware performance-monitoring counters to

S-mode

U-mode

the next-lower privileged mode

.

The settings in this register only control accessibility. The act of reading or writing this
register does not affect the underlying counters, which continue to increment even when not
accessible.

When ...

Fields:
- `CY`
    When set, the `cycle` CSR (an alias of `mcycle`) is accessible to
    
    S-mode.
    
    U-mode.
    
    When `scounteren.CY` is also set, `cycle` is further accessible to U-mode.
    
    When `hcounteren.CY` is also set, `cycle` is further accessible to VS-mode.
    
    When `hcounteren.CY` && `scounteren.CY` are both set, `cycle` is further accessible to VU-mode.
- `TM` (bits 1), access RO
    Placeholder for delegating `time` to less-privileged modes; however, since `time`
    is memory-mapped rather than a CSR, this field is always read-only zero.
- `IR` (bits 2)
    When set, the `instret` CSR (an alias of `minstret`) is accessible to
    
    S-mode.
    
    U-mode.
    
    When `scounteren.IR` is also set, `instret` is further accessible to U-mode.
    
    When `hcounteren.IR` is also set, `instret` is further accessible to VS-mode.
    
    When `hcounteren.IR` && `scounteren.IR` are both set, `instret` is further accessible to VU-mode.
- `HPM3` (bits 3)
    When set, the `hpmcounter3` CSR (an alias of `mhpmcounter3`) is accessible to
    
    S-mode.
    
    U-mode.
    
    When `scounteren.HPM3` is also set, `hpmcounter3` is further accessible to U-mode.
    
    When `hcounteren.HPM3` is also set, `hpmcounter3` is further accessible to VS-mode.
    
    When `hcounteren.HPM3` && `scounteren.HPM3` are both set, `hpmcounter3` is further accessible to VU-mode.
- `HPM4` (bits 4)
    When set, the `hpmcounter4` CSR (an alias of `mhpmcounter4`) is accessible to
    
    S-mode.
    
    U-mode.
    
    When `scounteren.HPM4` is also set, `hpmcounter4` is further accessible to U-mode.
    
    When `hcounteren.HPM4` is also set, `hpmcounter4` is further accessible to VS-mode.
    
    When `hcounteren.HPM4` && `scounteren.HPM4` are both set, `hpmcounter4` is further accessible to VU-mode.
- `HPM5` (bits 5)
    When set, the `hpmcounter5` CSR (an alias of `mhpmcounter5`) is accessible to
    
    S-mode.
    
    U-mode.
    
    When `scounteren.HPM5` is also set, `hpmcounter5` is further accessible to U-mode.
    
    When `hcounteren.HPM5` is also set, `hpmcounter5` is further accessible to VS-mode.
    
    When `hcounteren.HPM5` && `scounteren.HPM5` are both set, `hpmcounter5` is further accessible to VU-mode.
- `HPM6` (bits 6)
    When set, the `hpmcounter6` CSR (an alias of `mhpmcounter6`) is accessible to
    
    S-mode.
    
    U-mode.
    
    When `scounteren.HPM6` is also set, `hpmcounter6` is further accessible to U-mode.
    
    When `hcounteren.HPM6` is also set, `hpmcounter6` is further accessible to VS-mode.
    
    When `hcounteren.HPM6` && `scounteren.HPM6` are both set, `hpmcounter6` is further accessible to VU-mode.
- `HPM7` (bits 7)
    When set, the `hpmcounter7` CSR (an alias of `mhpmcounter7`) is accessible to
    
    S-mode.
    
    U-mode.
    
    When `scounteren.HPM7` is also set, `hpmcounter7` is further accessible to U-mode.
    
    When `hcounteren.HPM7` is also set, `hpmcounter7` is further accessible to VS-mode.
    
    When `hcounteren.HPM7` && `scounteren.HPM7` are both set, `hpmcounter7` is further accessible to VU-mode.
- `HPM8` (bits 8)
    When set, the `hpmcounter8` CSR (an alias of `mhpmcounter8`) is accessible to
    
    S-mode.
    
    U-mode.
    
    When `scounteren.HPM8` is also set, `hpmcounter8` is further accessible to U-mode.
    
    When `hcounteren.HPM8` is also set, `hpmcounter8` is further accessible to VS-mode.
    
    When `hcounteren.HPM8` && `scounteren.HPM8` are both set, `hpmcounter8` is further accessible to VU-mode.
- `HPM9` (bits 9)
    When set, the `hpmcounter9` CSR (an alias of `mhpmcounter9`) is accessible to
    
    S-mode.
    
    U-mode.
    
    When `scounteren.HPM9` is also set, `hpmcounter9` is further accessible to U-mode.
    
    When `hcounteren.HPM9` is also set, `hpmcounter9` is further accessible to VS-mode.
    
    When `hcounteren.HPM9` && `scounteren.HPM9` are both set, `hpmcounter9` is further accessible to VU-mode.
- `HPM10` (bits 10)
    When set, the `hpmcounter10` CSR (an alias of `mhpmcounter10`) is accessible to
    
    S-mode.
    
    U-mode.
    
    When `scounteren.HPM10` is also set, `hpmcounter10` is further accessible to U-mode.
    
    When `hcounteren.HPM10` is also set, `hpmcounter10` is further accessible to VS-mode.
    
    When `hcounteren.HPM10` && `scounteren.HPM10` are both set, `hpmcounter10` is further accessible to VU-mode.
- `HPM11` (bits 11)
    When set, the `hpmcounter11` CSR (an alias of `mhpmcounter11`) is accessible to
    
    S-mode.
    
    U-mode.
    
    When `scounteren.HPM11` is also set, `hpmcounter11` is further accessible to U-mode.
    
    When `hcounteren.HPM11` is also set, `hpmcounter11` is further accessible to VS-mode.
    
    When `hcounteren.HPM11` && `scounteren.HPM11` are both set, `hpmcounter11` is further accessible to VU-mode.

### CSR `mip`
Machine Interrupt Pending | address 836 | privilege M

The `mie` and `mip` CSRs are PARAM_074-bit read/write registers used when
the CLINT or PLIC interrupt controllers are present.
Note that the CLINT refers to an interrupt controller
used by some RISC-V implementations but isn't a ratified
RISC-V International standard.

The `mip` CSR contains information on pending interrupts, while `mie` is the corresponding
CSR containing interrupt enable ...

Fields:
- `SSIP` (bits 1), access RW
    *Supervisor Software Interrupt Pending*
    
    Reports the current pending state of an (H)S-mode software interrupt, which is generated by writing to this field.
    
    When using AIA/IMSIC, IPIs are expected to be delivered as external interrupts
    and SSIP is not backed by any hardware update (aside from any aliasing effects).
    However, SSIP is still writable by M-mode software and, when written, can be used to
    generate an S-mode Software Interrupt.
    
    _Aliases__Alias_:
    
    * `sip.SSIP` when `mideleg.SSI` is set
    
    * `mvip.SSIP`
- `VSSIP` (bits 2), access RW
    *Virtual Supervisor Software Interrupt Pending*
    
    Reports the current pending state of a VS-mode software interrupt, which is generated by writing to this field.
    
    When using AIA/IMSIC, IPIs are expected to be delivered as external interrupts and VSSIP is not backed by any hardware update (aside from any aliased writes).
    However, VSSIP is still writable by M-mode software and, when written, can be used to
    generate a VS-mode Software Interrupt.
    
    _Aliases_:
    
    * `hip.VSSIP`
    * `hvip.VSSIP`
    * `vsip.SSIP` when `hideleg.VSSI` is set
- `MSIP` (bits 3), access RO
    *Machine Software Interrupt Pending*
    
    Unused field.
    
    With AIA/IMSIC, IPIs are delivered as external interrupts. As a result, this bit is
    unused and hardwired to 0.
- `STIP` (bits 5), access RW
    *Supervisor Timer Interrupt Pending*
    
    Reports the current pending state of an (H)S-mode timer interrupt
    
    , which is normally controlled by the `stimecmp` CSR.
    
    , which is generated by software by writing to `mip.STIP`or its alias `mvip.STIP`.
    
    When `menvcfg.STCE` is set, `mip.STIP` is RO-H, and is completely controlled by the timer interrupt device (using `stimecmp`).
    
    When `menvcfg.STCE` is clear, `mip.STIP` is RW, and M-mode software may write the bit to inject a Supervisor Timer Interrupt.
    
    _Aliases__Alias_:
    
    * `sip.STIP` when `mideleg.STI` is set (though `sip.STIP` is a read-only view)
    
    * ...
- `VSTIP` (bits 6), access RO-H
    *Virtual Supervisor Timer Interrupt Pending*
    
    Reports the current pending state of a VS-mode timer interrupt
    
    , which is normally controlled by the `vstimecmp` CSR, but can also be injected by the hypervisor through `hvip.VSTIP`.
    
    , which is generated by M-mode and/or HS-mode software by writing to `hvip.VSTIP`.
    
    When `menvcfg.STCE` is set (enabling the `Sstc` extension), `mip.VSTIP` is the logical OR of `hvip.VSTIP` and the VS-level interrupt signal generated by the timer device (controlled by the value of `vstimecmp`).
    
    When `menvcfg.STCE` is clear (disabling the `Sstc` extension), ...
- `MTIP` (bits 7), access RO-H
    *Machine Timer Interrupt Pending*
    
    Reports the current pending state of an M-mode timer interrupt.
    
    Bit is controlled by the timer device (using `mtimecmp`), and is not writable.
- `SEIP` (bits 9), access RW-H
    *Supervisor External Interrupt Pending*
    
    Reports the current pending state of an (H)S-mode external interrupt.
    
    This field has two parts: a software-writable shadow value and a wire from the interrupt controller.
    The value presented to software in the bit on a CSR read is the logical OR of the software-writable value and the interrupt controller value.
    When software writes this bit, only the shadow value is updated (the interrupt controller is not notified of the write).
    
    The software-writable shadow value is aliased in `mvip.SEIP` (`Smaia` extension).
    
    _Alias_:
    
    * `sip.SEIP` when ...
- `VSEIP` (bits 10), access RO-H
    *Virtual Supervisor External Interrupt Pending*
    
    Reports the current pending state of a VS-mode external interrupt.
    
    This field is the logical OR of `hvip.VSEIP` and the wire coming from the interrupt controller.
    
    The field is not writable by software
    
    (_i.e._, unlike the behavior of `mip.SEIP`/`mvip.SEIP`, attempted writes to `mip.VSEIP` do not propagate to `hvip.VSEIP`)
    
    .
    
    _Aliases_:
    
    * `hip.VSEIP`
    * `vsip.SEIP` when `hideleg.VSEI` is set
- `MEIP` (bits 11), access RO-H
    *Machine External Interrupt Pending*
    
    Reports the current pending state of an M-mode external interrupt.
    
    MEIP is controlled by the external interrupt controller (AIA) .
    It is not writable by software.
- `SGEIP` (bits 12), access RO-H
    *Supervisor Guest External Interrupt Pending*
    
    Read-only summary of any pending Supervisor Guest External Interrupt Pending, i.e.:
    the logical-OR reduction of the `hgeip` register.
    
    _Alias_:
    
    * `hip.SGEIP`
- `LCOFIP` (bits 13), access RW-H
    *Local Counter Overflow Interrupt pending*
    
    When `hideleg.LCOFI` is set,
    `vsip.LCOFIP`, `sip.LCOFIP`, and `mip.LCOFIP` are all aliases.
    
    When a counter overflow interrupt occurs, a hidden sticky bit is set.
    
    Software writes 0 to `mip.LCOFIP` to clear the pending interrupt.
    
    _Aliases__Alias_:
    
    * `sip.LCOFIP` when `mideleg.LCOFI` is set
    
    * `vsip.LCOFIP` when `hideleg.LCOFI` is set

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

### CSR `mie`
Machine Interrupt Enable | address 772 | privilege M

mip.yaml#/description

Fields:
- `SSIE` (bits 1), access RW
    Enables Supervisor Software Interrupts.
- `VSSIE` (bits 2), access RW
    Enables Virtual Supervisor Software Interrupts.
- `MSIE` (bits 3), access RW
    Enables Machine Software Interrupts.
- `STIE` (bits 5), access RW
    Enables Supervisor Timer Interrupts.
- `VSTIE` (bits 6), access RW
    Enables Virtual Supervisor Timer Interrupts.
- `MTIE` (bits 7), access RW
    Enables Machine Timer Interrupts.
- `SEIE` (bits 9), access RW
    Enables Supervisor External Interrupts.
- `VSEIE` (bits 10), access RW
    Enables Virtual Supervisor External Interrupts.
- `MEIE` (bits 11), access RW
    Enables Machine External Interrupts.
- `SGEIE` (bits 12), access RW
    Enables Supervisor Guest External Interrupts
- `LCOFIE` (bits 13), access RW
    Enables Local Counter Overflow Interrupts.

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

### CSR `hcounteren`
Hypervisor Counter Enable | address 1542 | privilege S

Together with `scounteren`, delegates control of the hardware performance-monitoring counters
to VS/VU-mode

See `cycle` for a table describing how exceptions occur.

Fields:
- `CY`
    When all of `scounteren.CY`, `mcounteren.CY`, and `hcounteren.CY` are set,
    the `cycle` CSR (an alias of `mcycle`) is accessible to VU-mode.
    
    When `mcounteren.CY` and `hcounteren.CY` are set,
    the `cycle` CSR (an alias of `mcycle`) is accessible to VS-mode.
    
    When `hcounteren.CY` is clear and `mcounteren.CY` is set, then any access to `cycle` in
    VU-mode or VS-mode causes a VirtualInstruction exception.
    
    Summary:
    
    [separator="!",cols="1,1,1,4,4"]
    !===
    .2+h! [.rotate]#`hcounteren.CY`# .2+h! [.rotate]#`mcounteren.CY`# .2+h! [.rotate]#`scounteren.CY`# 2+^.>! `cycle` access behavior
    .>h! VS-mode .>h! ...
- `TM` (bits 1)
    When all of `scounteren.TM`, `mcounteren.TM`, and `hcounteren.TM` are set,
    the `time` CSR (an alias of `mtime` memory-mapped CSR) is accessible to VU-mode.
    
    When `mcounteren.TM` and `hcounteren.TM` are set,
    the `time` CSR (an alias of `mtime`) is accessible to VS-mode.
    
    When `hcounteren.TM` is clear and `mcounteren.TM` is set, then any access to `time` in
    VU-mode or VS-mode causes a VirtualInstruction exception.
    
    Summary:
    
    [separator="!",%autowidth]
    !===
    .2+h! [.rotate]#`hcounteren.TM`# .2+h! [.rotate]#`mcounteren.TM`# .2+h! [.rotate]#`scounteren.TM`# 2+^.>! `cycle` access behavior
    .>h! ...
- `IR` (bits 2)
    When all of `scounteren.IR`, `mcounteren.IR`, and `hcounteren.IR` are set,
    the `instret` CSR (an alias of `minstret`) is accessible to VU-mode.
    
    When `mcounteren.IR` and `hcounteren.IR` are set,
    the `instret` CSR (an alias of `minstret`) is accessible to VS-mode.
    
    When `hcounteren.IR` is clear and `mcounteren.IR` is set, then any access to `instret` in
    VU-mode or VS-mode causes a VirtualInstruction exception.
    
    Summary:
    
    [separator="!",%autowidth]
    !===
    .2+h! [.rotate]#`hcounteren.IR`# .2+h! [.rotate]#`mcounteren.IR`# .2+h! [.rotate]#`scounteren.IR`# 2+^.>! `cycle` access behavior
    .>h! VS-mode ...
- `HPM3` (bits 3)
    When all of `scounteren.HPM3`, `mcounteren.HPM3`, and `hcounteren.HPM3` are set,
    the `hpmcounter3` CSR (an alias of `mhpmcounter3`) is accessible to VU-mode.
    
    When `mcounteren.HPM3` and `hcounteren.HPM3` are set,
    the `hpmcounter3` CSR (an alias of `mhpmcounter3`) is accessible to VS-mode.
    
    When `hcounteren.HPM3` is clear and `mcounteren.HPM3` is set, then any access to `hpmcounter3` in
    VU-mode or VS-mode causes a VirtualInstruction exception.
    
    Summary:
    
    [separator="!",%autowidth]
    !===
    .2+h! [.rotate]#`hcounteren.HPM3`# .2+h! [.rotate]#`mcounteren.HPM3`# .2+h! [.rotate]#`scounteren.HPM3`# ...
- `HPM4` (bits 4)
    When all of `scounteren.HPM4`, `mcounteren.HPM4`, and `hcounteren.HPM4` are set,
    the `hpmcounter4` CSR (an alias of `mhpmcounter4`) is accessible to VU-mode.
    
    When `mcounteren.HPM4` and `hcounteren.HPM4` are set,
    the `hpmcounter4` CSR (an alias of `mhpmcounter4`) is accessible to VS-mode.
    
    When `hcounteren.HPM4` is clear and `mcounteren.HPM4` is set, then any access to `hpmcounter4` in
    VU-mode or VS-mode causes a VirtualInstruction exception.
    
    Summary:
    
    [separator="!",%autowidth]
    !===
    .2+h! [.rotate]#`hcounteren.HPM4`# .2+h! [.rotate]#`mcounteren.HPM4`# .2+h! [.rotate]#`scounteren.HPM4`# ...
- `HPM5` (bits 5)
    When all of `scounteren.HPM5`, `mcounteren.HPM5`, and `hcounteren.HPM5` are set,
    the `hpmcounter5` CSR (an alias of `mhpmcounter5`) is accessible to VU-mode.
    
    When `mcounteren.HPM5` and `hcounteren.HPM5` are set,
    the `hpmcounter5` CSR (an alias of `mhpmcounter5`) is accessible to VS-mode.
    
    When `hcounteren.HPM5` is clear and `mcounteren.HPM5` is set, then any access to `hpmcounter5` in
    VU-mode or VS-mode causes a VirtualInstruction exception.
    
    Summary:
    
    [separator="!",%autowidth]
    !===
    .2+h! [.rotate]#`hcounteren.HPM5`# .2+h! [.rotate]#`mcounteren.HPM5`# .2+h! [.rotate]#`scounteren.HPM5`# ...
- `HPM6` (bits 6)
    When all of `scounteren.HPM6`, `mcounteren.HPM6`, and `hcounteren.HPM6` are set,
    the `hpmcounter6` CSR (an alias of `mhpmcounter6`) is accessible to VU-mode.
    
    When `mcounteren.HPM6` and `hcounteren.HPM6` are set,
    the `hpmcounter6` CSR (an alias of `mhpmcounter6`) is accessible to VS-mode.
    
    When `hcounteren.HPM6` is clear and `mcounteren.HPM6` is set, then any access to `hpmcounter6` in
    VU-mode or VS-mode causes a VirtualInstruction exception.
    
    Summary:
    
    [separator="!",%autowidth]
    !===
    .2+h! [.rotate]#`hcounteren.HPM6`# .2+h! [.rotate]#`mcounteren.HPM6`# .2+h! [.rotate]#`scounteren.HPM6`# ...
- `HPM7` (bits 7)
    When all of `scounteren.HPM7`, `mcounteren.HPM7`, and `hcounteren.HPM7` are set,
    the `hpmcounter7` CSR (an alias of `mhpmcounter7`) is accessible to VU-mode.
    
    When `mcounteren.HPM7` and `hcounteren.HPM7` are set,
    the `hpmcounter7` CSR (an alias of `mhpmcounter7`) is accessible to VS-mode.
    
    When `hcounteren.HPM7` is clear and `mcounteren.HPM7` is set, then any access to `hpmcounter7` in
    VU-mode or VS-mode causes a VirtualInstruction exception.
    
    Summary:
    
    [separator="!",%autowidth]
    !===
    .2+h! [.rotate]#`hcounteren.HPM7`# .2+h! [.rotate]#`mcounteren.HPM7`# .2+h! [.rotate]#`scounteren.HPM7`# ...
- `HPM8` (bits 8)
    When all of `scounteren.HPM8`, `mcounteren.HPM8`, and `hcounteren.HPM8` are set,
    the `hpmcounter8` CSR (an alias of `mhpmcounter8`) is accessible to VU-mode.
    
    When `mcounteren.HPM8` and `hcounteren.HPM8` are set,
    the `hpmcounter8` CSR (an alias of `mhpmcounter8`) is accessible to VS-mode.
    
    When `hcounteren.HPM8` is clear and `mcounteren.HPM8` is set, then any access to `hpmcounter8` in
    VU-mode or VS-mode causes a VirtualInstruction exception.
    
    Summary:
    
    [separator="!",%autowidth]
    !===
    .2+h! [.rotate]#`hcounteren.HPM8`# .2+h! [.rotate]#`mcounteren.HPM8`# .2+h! [.rotate]#`scounteren.HPM8`# ...
- `HPM9` (bits 9)
    When all of `scounteren.HPM9`, `mcounteren.HPM9`, and `hcounteren.HPM9` are set,
    the `hpmcounter9` CSR (an alias of `mhpmcounter9`) is accessible to VU-mode.
    
    When `mcounteren.HPM9` and `hcounteren.HPM9` are set,
    the `hpmcounter9` CSR (an alias of `mhpmcounter9`) is accessible to VS-mode.
    
    When `hcounteren.HPM9` is clear and `mcounteren.HPM9` is set, then any access to `hpmcounter9` in
    VU-mode or VS-mode causes a VirtualInstruction exception.
    
    Summary:
    
    [separator="!",%autowidth]
    !===
    .2+h! [.rotate]#`hcounteren.HPM9`# .2+h! [.rotate]#`mcounteren.HPM9`# .2+h! [.rotate]#`scounteren.HPM9`# ...
- `HPM10` (bits 10)
    When all of `scounteren.HPM10`, `mcounteren.HPM10`, and `hcounteren.HPM10` are set,
    the `hpmcounter10` CSR (an alias of `mhpmcounter10`) is accessible to VU-mode.
    
    When `mcounteren.HPM10` and `hcounteren.HPM10` are set,
    the `hpmcounter10` CSR (an alias of `mhpmcounter10`) is accessible to VS-mode.
    
    When `hcounteren.HPM10` is clear and `mcounteren.HPM10` is set, then any access to `hpmcounter10` in
    VU-mode or VS-mode causes a VirtualInstruction exception.
    
    Summary:
    
    [separator="!",%autowidth]
    !===
    .2+h! [.rotate]#`hcounteren.HPM10`# .2+h! [.rotate]#`mcounteren.HPM10`# .2+h! ...
- `HPM11` (bits 11)
    When all of `scounteren.HPM11`, `mcounteren.HPM11`, and `hcounteren.HPM11` are set,
    the `hpmcounter11` CSR (an alias of `mhpmcounter11`) is accessible to VU-mode.
    
    When `mcounteren.HPM11` and `hcounteren.HPM11` are set,
    the `hpmcounter11` CSR (an alias of `mhpmcounter11`) is accessible to VS-mode.
    
    When `hcounteren.HPM11` is clear and `mcounteren.HPM11` is set, then any access to `hpmcounter11` in
    VU-mode or VS-mode causes a VirtualInstruction exception.
    
    Summary:
    
    [separator="!",%autowidth]
    !===
    .2+h! [.rotate]#`hcounteren.HPM11`# .2+h! [.rotate]#`mcounteren.HPM11`# .2+h! ...

### CSR `mideleg`
Machine Interrupt Delegation | address 771 | privilege M

Controls exception delegation from M-mode to HS/S-mode

By default, all traps at any privilege level are handled in machine
mode, though a machine-mode handler can redirect traps back to the
appropriate level with the `MRET` instruction. To increase performance,
implementations can provide individual read/write bits within `mideleg`
to indicate that certain exceptions and interrupts should
be ...

Fields:
- `SSI` (bits 1), access RW
    *Supervisor Software Interrupt delegation*
    
    When 1, Supervisor Software interrupts are delegated to HS/S-mode.
- `VSSI` (bits 2), access RO
    *Virtual Supervisor Software Interrupt delegation*
    
    When 1, Virtual Supervisor Software interrupts are delegated to HS-mode.
    
    Virtual Supervisor Software Interrupts are always delegated to HS-mode, so this field is read-only one.
- `MSI` (bits 3), access RO
    *Machine Software interrupt delegation*
    
    Since M-mode interrupts cannot be delegated, this field is read-only zero.
- `STI` (bits 5), access RW
    *Supervisor Timer interrupt delegation*
    
    When 1, Supervisor Timer interrupts are delegated to HS/S-mode.
- `VSTI` (bits 6), access RO
    *Virtual Supervisor Timer interrupt delegation*
    
    When 1, Virtual Supervisor Timer interrupts are delegated to HS-mode.
    
    Virtual Supervisor Time Interrupts are always delegated to HS-mode, so this field is read-only one.
- `MTI` (bits 7), access RO
    *Machine Timer interrupt delegation*
    
    Since M-mode interrupts cannot be delegated, this field is read-only zero.
- `SEI` (bits 9), access RW
    *Supervisor External interrupt delegation*
    
    When 1, Supervisor External interrupts are delegated to HS/S-mode.
- `VSEI` (bits 10), access RO
    *Virtual Supervisor External interrupt delegation*
    
    Virtual Supervisor External Interrupts are always delegated to HS-mode, so this field is read-only one.
- `MEI` (bits 11), access RO
    *Machine External interrupt delegation*
    
    Since M-mode interrupts cannot be delegated, this field is read-only zero.
- `SGEI` (bits 12), access RO
    *Supervisor Guest External Interrupt delegation*
    
    Supervisor Guest External interrupts are always delegated to HS-mode, so this field is read-only one.
- `LCOFI` (bits 13), access RW
    *Local Counter Overflow Interrupt delegation*
    
    When 1, local counter overflow interrupts are delegated to (H)S-mode.