fix(param): require VSXLEN and VUXLEN to support 32 when their parent can

---

`VSXLEN` and `VUXLEN` each constrained only their upper bound, so `VSXLEN: [32, 64]` with `VUXLEN: [64]` was accepted. In that hart `hstatus.VSXL` is read-write and can select RV32 for VS-mode, while `vsstatus.UXL` is hardwired to 64, leaving VU-mode wider than VS-mode. The same gap allowed `SXLEN: [32, 64]` with `VSXLEN: [64]`.

The privileged spec settles both: when HSXLEN=32 the VSXL field does not exist and VSXLEN=32, and when VSXLEN=32 the UXL field does not exist and VU-mode XLEN=32. So a hart whose parent mode can run in RV32 must support 32 in the child. `UXLEN` already carries this clause against `SXLEN`; this adds the two missing hypervisor analogues.

No config under `cfgs/` changes status. Of the five that set any of these parameters, none is newly rejected.

Closes #2254
