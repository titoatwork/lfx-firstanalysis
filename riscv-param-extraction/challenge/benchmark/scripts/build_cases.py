#!/usr/bin/env python3
"""Populate benchmark case source.txt + extraction.yaml (independent of GT file body)."""

from __future__ import annotations

from pathlib import Path

import yaml

CASES = Path(__file__).resolve().parents[1] / "cases"

SOURCES = {
    "CACHE_BLOCK_SIZE": (
        "The capacity and organization of a cache and the size of a cache block "
        "are both implementation-specific. In the initial set of CMO extensions, "
        "the size of a cache block shall be uniform throughout the system."
    ),
    "NUM_PMP_ENTRIES": (
        "An implementation may have zero, sixteen, or sixty-four physical memory "
        "protection entries. The number of implemented PMP entries is "
        "implementation-defined within the architectural constraints."
    ),
    "PHYS_ADDR_WIDTH": (
        "The size of the physical address space is implementation-defined. "
        "PHYS_ADDR_WIDTH is the number of bits in a physical address."
    ),
    "ASID_WIDTH": (
        "The number of implemented ASID bits is implementation-defined, with a "
        "maximum of 16 for XLEN=64 and 9 for XLEN=32."
    ),
    "MXLEN": (
        "The MXL field indicates the effective XLEN in M-mode, a constant termed "
        "MXLEN. MXLEN is 32 or 64."
    ),
    "MTVEC_MODES": (
        "If mtvec is writable, the set of values the MODE field may hold can vary "
        "by implementation. MODE may support Direct and/or Vectored modes."
    ),
    "HPM_COUNTER_EN": (
        "Which hardware performance counters are implemented is "
        "implementation-defined. Software discovers which counters exist."
    ),
    "PMLEN": (
        "The number of high-order bits of an address that are masked by the "
        "pointer masking facility is implementation-defined."
    ),
    "MISALIGNED_LDST": (
        "Support for misaligned loads and stores to main memory is "
        "implementation-defined. An implementation may raise a misaligned "
        "exception instead."
    ),
    "TIME_CSR_IMPLEMENTED": (
        "Whether a real hardware time CSR exists is implementation-defined. "
        "Implementations can provide a real CSR or emulate access at M-mode."
    ),
    "MISALIGNED_AMO": (
        "Support for misaligned AMOs may be implementation-defined."
    ),
    "LRSC_RESERVATION_STRATEGY": (
        "The reservation-set size and strategy for LR/SC is "
        "implementation-defined within architectural constraints."
    ),
    "COUNTINHIBIT_EN": (
        "Which count-inhibit bits are implemented is implementation-defined."
    ),
    "ELEN": (
        "ELEN is the maximum size in bits of a vector element that any operation "
        "can produce or consume. ELEN is implementation-defined for the V extension."
    ),
    "VLEN": (
        "VLEN is the number of bits in a single vector register. VLEN is an "
        "implementation-defined power of two."
    ),
}

SCHEMAS: dict[str, dict] = {
    "CACHE_BLOCK_SIZE": {"type": "integer", "minimum": 1},
    "NUM_PMP_ENTRIES": {"type": "integer", "enum": [0, 16, 64]},
    "PHYS_ADDR_WIDTH": {"type": "integer", "minimum": 1, "maximum": 64},
    "ASID_WIDTH": {"type": "integer", "minimum": 0, "maximum": 16},
    "MXLEN": {"type": "integer", "enum": [32, 64]},
    "MTVEC_MODES": {
        "type": "array",
        "items": {"type": "integer", "enum": [0, 1]},
        "minItems": 1,
        "uniqueItems": True,
    },
    "HPM_COUNTER_EN": {"type": "array", "items": {"type": "boolean"}, "minItems": 1},
    "PMLEN": {"type": "integer"},
    "MISALIGNED_LDST": {"type": "boolean"},
    "TIME_CSR_IMPLEMENTED": {"type": "boolean"},
    "MISALIGNED_AMO": {"type": "boolean"},
    # Intentional possible type-fidelity miss vs upstream if GT uses enum/object
    "LRSC_RESERVATION_STRATEGY": {"type": "string"},
    "COUNTINHIBIT_EN": {"type": "array", "items": {"type": "boolean"}},
    "ELEN": {"type": "integer"},
    "VLEN": {"type": "integer"},
}


def main() -> None:
    for name, src in SOURCES.items():
        d = CASES / name
        d.mkdir(parents=True, exist_ok=True)
        (d / "source.txt").write_text(src.strip() + "\n", encoding="utf-8")
        doc = {
            "$schema": "param_schema.json#",
            "kind": "parameter",
            "name": name,
            "long_name": name.replace("_", " ").title() + " (re-derived)",
            "description": src.strip(),
            "definedBy": {"extension": {"name": "Sm"}},
            "schema": SCHEMAS[name],
        }
        (d / "extraction.yaml").write_text(
            yaml.safe_dump(doc, sort_keys=False, allow_unicode=True),
            encoding="utf-8",
        )
    print(f"populated {len(SOURCES)} cases under {CASES}")


if __name__ == "__main__":
    main()
