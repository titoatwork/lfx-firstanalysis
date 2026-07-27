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