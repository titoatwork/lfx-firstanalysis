## CSR and field reference for this excerpt
Definitions of CSRs named in the text above. Reference material only.

### CSR `mnstatus`
Machine NMI Status | address 1860 | privilege M

The mnstatus register tracks and controls the hart's current NMI operating state.

Fields:
- `MNPP` (bits 12-11), access RW-H
    M-mode NMI Previous Privilege.
    
    Written by hardware in two cases:
    
    * Written with the prior nominal privilege level when entering M-mode NMI from an exception/interrupt.
    * Written with 0 when executing an `mnret` instruction to return from a double exception / NMI in M-mode.
    
    Can also be written by software without immediate side-effect.
    
    Affects execution in two cases:
    
    * On a return from a double exception / NMI from M-mode, the machine will
    enter the privilege level stored in MNPP before clearing the field.
    * When `mnstatus.MNPRV` is set, loads and stores behave as if the current privilege ...
- `MNPELP` (bits 9), access RW-H
    M-mode NMI Previous Expected Landing Pad state.
    
    Defined by the Zicfilp extension. Holds the previous
    Expected Landing Pad (ELP) state when entering M-mode NMI.
- `MNPV` (bits 7), access RW-H
    *Machine Previous NMI Virtualization mode*
    
    Written with the prior virtualization mode when entering M-mode from an exception/interrupt.
    When returning via an MRET instruction, the virtualization mode becomes the value of MPV unless MPP=3, in which case the virtualization mode is always 0.
    Can also be written by software.
- `NMIE` (bits 3), access RW-H
    *M-mode NMI Enable*
    
    Written by hardware in two cases:
    
    * Written with the value 0 when entering M-mode NMI.
    * Written with the value 0 when entering M-mode double trap.
    
    Written by software in one case only:
    
    * The NMIE is 0 on reset for boot code to initialize system to service NMIs. Once SW writes NMIE to 1, it cannot be changed anymore by SW.
    
    Affects execution by:
    
    * When 0, all non-maskable interrupts and exceptions are disabled when the current privilege level is M.
    * When 1, NMI or double trap is possible.

### CSR `mnepc`
Machine Exception Program Counter | address 1857 | privilege M

Written with the PC of an instruction on an exception or interrupt taken in M-mode.

Also controls where the hart jumps on an exception return from M-mode.

Fields:
- `PC` (bits 63-0), access RW-RH
    When a NMI / double trap is taken into M-mode, `mnepc.PC` is written with the virtual address of the
    instruction that was interrupted or that encountered the exception.
    Otherwise, `mnepc.PC` is never written by the implementation, though it may be explicitly written
    by software.
    
    On an exception return from M-mode NMI / double trap (from the MNRET instruction),
    control transfers to the virtual address read out of `mnepc.PC`.
    
    [when,"ext?(:C)"]
    Because PCs are always halfword-aligned, bit 0 of `mnepc.PC` is always
    read-only 0.
    
    [when,"!ext?(:C)"]
    Because PCs are always word-aligned, bits 1:0 ...

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

### CSR `mncause`
Resumable NMI cause | address 1858 | privilege M

The mncause CSR holds the reason for the NMI.
If the reason is an interrupt, bit PARAM_074-1 is set to 1, and the NMI cause is encoded in
the least-significant bits.
If the reason is an interrupt and NMI causes are not supported,
bit PARAM_074-1 is set to 1, and zero is written to the least-significant bits.
If the reason is an exception within M-mode that results in a double trap as
specified in the ...

Fields:
- `INT` (bits 63), access RW-H
    Written by hardware when a resumable NMI is taken into M-mode.
    
    When set, the last non-maskable exception was caused by an asynchronous Interrupt.
    
    [when,"PARAM_168 == true"]
    If `mcause` is written with an undefined cause (combination of `mcause.INT` and `mcause.CODE`), an `Illegal Instruction` exception occurs.
    
    [when,"PARAM_168 == false"]
    If `mcause` is written with an undefined cause (combination of `mcause.INT` and `mcause.CODE`), neither `mcause.INT` nor `mcause.CODE` are modified.
- `CODE` (bits 62-0), access RW-H
    TODO

### CSR `mnscratch`
Machine Scratch Register | address 1856 | privilege M

Scratch register for software use in NMI / double trap. Bits are not
interpreted by hardware.

Fields:
- `SCRATCH` (bits 63-0), access RW
    Scratch value

### CSR `mcause`
Machine Cause | address 834 | privilege M

Reports the cause of the latest exception.

Fields:
- `INT` (bits 63), access RW-RH
    Written by hardware when a trap is taken into M-mode.
    
    When set, the last exception was caused by an asynchronous Interrupt.
    
    `mcause.INT` is writable.
    
    [when,"PARAM_168 == true"]
    If `mcause` is written with an undefined cause (combination of `mcause.INT` and `mcause.CODE`), an `Illegal Instruction` exception occurs.
    
    [when,"PARAM_168 == false"]
    If `mcause` is written with an undefined cause (combination of `mcause.INT` and `mcause.CODE`), neither `mcause.INT` nor `mcause.CODE` are modified.
- `CODE` (bits 62-0), access RW-RH
    Written by hardware when a trap is taken into M-mode.
    
    Holds the interrupt or exception code for the last taken trap.
    
    `mcause.CODE` is writable.
    
    [when,"PARAM_168 == true"]
    If `mcause` is written with an undefined cause (combination of `mcause.INT` and `mcause.CODE`), an `Illegal Instruction` exception occurs.
    
    [when,"PARAM_168 == false"]
    If `mcause` is written with an undefined cause (combination of `mcause.INT` and `mcause.CODE`), neither `mcause.INT` nor `mcause.CODE` are modified.
    
    Valid interrupt codes are:
    [separator="!"]
    !===
    
    !  ! 
    
    !===
    
    Valid exception codes ...

### CSR `mepc`
Machine Exception Program Counter | address 833 | privilege M

Written with the PC of an instruction on an exception or interrupt taken in M-mode.

Also controls where the hart jumps on an exception return from M-mode.

Fields:
- `PC` (bits 63-0), access RW-RH
    When a trap is taken into M-mode, `mepc.PC` is written with the virtual address of the
    instruction that was interrupted or that encountered the exception.
    Otherwise, `mepc.PC` is never written by the implementation, though it may be explicitly written
    by software.
    
    On an exception return from M-mode (from the MRET instruction),
    control transfers to the virtual address read out of `mepc.PC`.
    
    [when,"ext?(:C)"]
    Because PCs are always halfword-aligned, bit 0 of `mepc.PC` is always
    read-only 0.
    
    [when,"!ext?(:C)"]
    Because PCs are always word-aligned, bits 1:0 of `mepc.PC` are always
    read-only ...

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