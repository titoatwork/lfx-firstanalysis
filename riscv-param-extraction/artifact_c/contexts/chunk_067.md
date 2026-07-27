## CSR and field reference for this excerpt
Definitions of CSRs named in the text above. Reference material only.

### CSR `jvt`
Table Jump Base Vector and Control Register | address 23 | privilege U

The `jvt` register is an XLEN-bit WARL read/write register that holds the jump table configuration,
consisting of the jump table base address (BASE) and the jump table mode (MODE).

`jvt` CSR adds architectural state to the system software context (such as an OS process), therefore
must be saved/restored on context switches.

Fields:
- `BASE` (bits 63-6)
    The value in the BASE field must always be aligned on a 64-byte boundary. Note that the CSR contains only
    bits XLEN-1 through 6 of the address base. When computing jump-table accesses, the lower six bits of base
    are filled with zeroes to obtain an XLEN-bit jump-table base address `jvt.base` that is always aligned on a
    64-byte boundary.
    
    `jvt.base` is a virtual address, whenever virtual memory is enabled.
    
    The memory pointed to by `jvt.base` is treated as instruction memory for the purpose of executing table
    jump instructions, implying execute access permission.
- `MODE` (bits 5-0)
    `jvt.mode` is a WARL field, so can only be programmed to modes which are implemented. Therefore the
    discovery mechanism is to attempt to program different modes and read back the values to see which
    are available. Jump table mode must be implemented.

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