## CSR and field reference for this excerpt
Definitions of CSRs named in the text above. Reference material only.

### CSR `vstart`
Vector Start Index | address 8 | privilege U

Specifies the index of the first element to be executed by a vector instruction.

Fields:
- `VALUE` (bits 63-0), access RW-RH
    Normally, vstart is only written by hardware on a trap on a vector instruction, with the vstart value
    representing the element on which the trap was taken (either a synchronous exception or an
    asynchronous interrupt), and at which execution should resume after a resumable trap is handled.
    All vector instructions are defined to begin execution with the element number given in the vstart
    CSR, leaving earlier elements in the destination vector undisturbed, and to reset the vstart CSR to
    zero at the end of execution.
    
    [NOTE]
    All vector instructions, including vset{i}vl{i}, reset the vstart CSR to ...

### CSR `vtype`
Vector Type | address 3105 | privilege U

Provides the default type used to interpret the contents of the vector register file.

Fields:
- `VILL` (bits 63), access RO-H
    The vill bit is used to encode that a previous vset{i}vl{i} instruction attempted to write an
    unsupported value to vtype.
    
    [NOTE]
    The vill bit is held in bit XLEN-1 of the CSR to support checking for illegal values with a
    branch on the sign bit.
    
    If the vill bit is set, then any attempt to execute a vector instruction that depends upon vtype will
    raise an illegal-instruction exception.
    
    When the vill bit is set, the other XLEN-1 bits in vtype shall be zero.
    
    It is recommended that at reset, vill is set.
- `VMA` (bits 7), access RO-H
    Vector mask agnostic bit. Modifies the behavior of destination inactive masked-off elements during the
    execution of vector instructions.
    
    A value of 0 means inactive elements are undisturbed, meaning the corresponding set of destination elements
    in a vector register group retain the value they previously held.
    
    A value of 1 means inactive elements are agnostic, meaning the corresponding set of destination elements
    in any vector destination operand can either retain the value they previously held, or are overwritten with 1s.
    Within a single vector instruction, each destination element can be ...
- `VTA` (bits 6), access RO-H
    Vector tail agnostic bit. Modifies the bahavior of destination tail elements during the execution of vector
    instructions.
    
    A value of 0 means tail elements are undisturbed, meaning the corresponding set of destination elements
    in a vector register group retain the value they previously held.
    
    A value of 1 means tail elements are agnostic, meaning the corresponding set of destination elements
    in any vector destination operand can either retain the value they previously held, or are overwritten with 1s.
    Within a single vector instruction, each destination element can be either left undisturbed ...
- `VSEW` (bits 5-3), access RO-H
    The value in vsew sets the dynamic selected element width (SEW).
    
    [separator="!"]
    !===
    ! vsew[2:0] ! SEW ! Elements per vector register
    ! 000 ! 8 ! 16
    ! 001 ! 16 ! 8
    ! 010 ! 32 ! 4
    ! 011 ! 64 ! 2
    ! 1XX ! Reserved ! Reserved
    !===
    
    It is recommended that at reset, vill is set, and the remaining bits in vtype are zero.
- `VLMUL` (bits 2-0), access RO-H
    Vector register group multiplier.
    
    Multiple vector registers can be grouped together, so that a single vector instruction can operate on
    multiple vector registers. The term vector register group is used herein to refer to one or more vector
    registers used as a single operand to a vector instruction. Vector register groups can be used to provide
    greater execution efficiency for longer application vectors, but the main reason for their inclusion is to
    allow double-width or larger elements to be operated on with the same vector length as single-width
    elements. The vector length multiplier, LMUL, ...

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

### CSR `frm`
Floating-Point Dynamic Rounding Mode | address 2 | privilege U

Rounding modes are encoded as follows:

[[rm]]
.Rounding mode encoding.
[%autowidth,float="center",align="center",cols="^,^,<",options="header"]
!===
!Rounding Mode |Mnemonic |Meaning
!000 !RNE !Round to Nearest, ties to Even
!001 !RTZ !Round towards Zero
!010 !RDN !Round Down (towards latexmath:[$-\infty$])
!011 !RUP !Round Up (towards latexmath:[$+\infty$])
!100 !RMM !Round to Nearest, ties to ...

Fields:
- `ROUNDINGMODE` (bits 2-0), access RW-H
    Rounding mode data.