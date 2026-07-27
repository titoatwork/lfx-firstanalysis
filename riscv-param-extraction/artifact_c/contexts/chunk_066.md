## CSR and field reference for this excerpt
Definitions of CSRs named in the text above. Reference material only.

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