#!/usr/bin/env python3
"""
Build leakage-audited CSR/field context files from a local UDB checkout.

Does NOT include parameter YAML. Scrubs any parameter-name tokens found in
manifest gold/aliases from CSR field descriptions and IDL snippets.

Usage:
  python build_context.py --udb-root ../../../riscv-unified-db
  python build_context.py --udb-root /path/to/udb --check-only
"""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
from pathlib import Path
from typing import Any

import yaml

from normalize import name_variants, normalize_param_name

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "manifests" / "holdout_cases.yaml"
OUT_DIR = ROOT / "contexts"

# CSR id -> relative path under UDB
CSR_PATHS = {
    "mtvec": "spec/std/isa/csr/mtvec.yaml",
    "mstatus": "spec/std/isa/csr/mstatus.yaml",
    "satp": "spec/std/isa/csr/satp.yaml",
    "vstart": "spec/std/isa/csr/V/vstart.yaml",
    "mcountinhibit": "spec/std/isa/csr/Zicntr/mcountinhibit.yaml",
    "pmpcfg0": "spec/std/isa/csr/I/pmpcfg0.yaml",
}

# IDL / schema tokens that are parameter names — always scrub
ALWAYS_SCRUB = {
    "MTVEC_MODES",
    "MTVEC_ACCESS",
    "MTVEC_ILLEGAL_WRITE_BEHAVIOR",
    "MTVEC_BASE_ALIGNMENT_DIRECT",
    "MTVEC_BASE_ALIGNMENT_VECTORED",
    "MSTATUS_FS_LEGAL_VALUES",
    "MSTATUS_VS_LEGAL_VALUES",
    "HW_MSTATUS_FS_DIRTY_UPDATE",
    "HW_MSTATUS_VS_DIRTY_UPDATE",
    "SATP_MODE_BARE",
    "M_MODE_ENDIANNESS",
    "S_MODE_ENDIANNESS",
    "U_MODE_ENDIANNESS",
    "TRAP_ON_ILLEGAL_WLRL",
    "NUM_USABLE_PMP_ENTRIES",
    "NUM_PMP_ENTRIES",
    "PMP_GRANULARITY",
    "SEW_MIN",
    "ELEN",
    "VLEN",
    "MCOUNTINHIBIT_IMPLEMENTED",
    "COUNTINHIBIT_EN",
    "HPM_COUNTER_EN",
    "MXLEN",
    "SXLEN",
    "UXLEN",
    "PHYS_ADDR_WIDTH",
    "ASID_WIDTH",
    "TRAP_ON_UNIMPLEMENTED_CSR",
}


def load_manifest() -> dict[str, Any]:
    return yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))


def all_scrub_tokens(manifest: dict[str, Any]) -> set[str]:
    tokens = set(ALWAYS_SCRUB)
    for case in manifest["positives"]:
        tokens.add(case["name"])
        tokens.update(case.get("aliases") or [])
    return tokens


def scrub_text(text: str, tokens: set[str]) -> str:
    out = text
    # Longest first to avoid partial double-replace
    for tok in sorted(tokens, key=len, reverse=True):
        if not tok:
            continue
        out = re.sub(rf"(?<![A-Za-z0-9_]){re.escape(tok)}(?![A-Za-z0-9_])", "[PARAM]", out)
        # normalized camel-less form inside dense IDL
        n = normalize_param_name(tok)
        if len(n) >= 10:
            out = out.replace(n, "[PARAM]")
    return out


def extract_csr_context(csr_doc: dict[str, Any], tokens: set[str]) -> str:
    lines: list[str] = []
    name = csr_doc.get("name", "?")
    lines.append(f"# CSR context (scrubbed) — {name}")
    lines.append("# Parameter names and gold schema values removed for leakage control.")
    if csr_doc.get("long_name"):
        lines.append(f"CSR long_name: {scrub_text(str(csr_doc['long_name']), tokens)}")
    if csr_doc.get("description"):
        lines.append("CSR description:")
        lines.append(scrub_text(str(csr_doc["description"]), tokens))
    if csr_doc.get("address") is not None:
        lines.append(f"address: {csr_doc['address']}")
    if "writable" in csr_doc:
        lines.append(f"writable: {csr_doc['writable']}")
    if csr_doc.get("priv_mode"):
        lines.append(f"priv_mode: {csr_doc['priv_mode']}")
    if csr_doc.get("length"):
        lines.append(f"length: {scrub_text(str(csr_doc['length']), tokens)}")

    fields = csr_doc.get("fields") or {}
    if isinstance(fields, dict):
        lines.append("fields:")
        for fname, fval in fields.items():
            if not isinstance(fval, dict):
                continue
            lines.append(f"  - field: {fname}")
            for key in ("location", "location_rv32", "location_rv64", "description"):
                if key in fval and fval[key] is not None:
                    val = scrub_text(str(fval[key]), tokens)
                    # Drop pure IDL type()/sw_write bodies that are mostly param refs
                    if key == "description":
                        lines.append(f"    description: |")
                        for ln in val.splitlines() or [""]:
                            lines.append(f"      {ln}")
            # Include a sanitized type hint only if short and scrubbed
            for key in ("type", "type()"):
                if key in fval and isinstance(fval[key], str) and len(fval[key]) < 200:
                    scrubbed = scrub_text(fval[key], tokens)
                    if "[PARAM]" in scrubbed or "CsrFieldType" in scrubbed:
                        lines.append(f"    type_hint: {scrubbed}")
    return "\n".join(lines).rstrip() + "\n"


def build_one(udb: Path, csr_id: str, tokens: set[str]) -> tuple[str, str]:
    rel = CSR_PATHS[csr_id]
    path = udb / rel
    if not path.is_file():
        raise FileNotFoundError(path)
    raw = path.read_text(encoding="utf-8")
    doc = yaml.safe_load(raw)
    if not isinstance(doc, dict):
        raise ValueError(f"CSR not mapping: {path}")
    body = extract_csr_context(doc, tokens)
    # Second-pass: drop lines that still contain raw UPPER_SNAKE param-like leftovers
    # that match scrub tokens normalized
    final_lines = []
    norm_tokens = {normalize_param_name(t) for t in tokens if len(normalize_param_name(t)) >= 10}
    for line in body.splitlines():
        nline = normalize_param_name(line)
        if any(t in nline for t in norm_tokens if t):
            # keep line only if already scrubbed markers present
            if "[PARAM]" not in line:
                line = re.sub(r"\b[A-Z][A-Z0-9_]{7,}\b", "[PARAM]", line)
        final_lines.append(line)
    body = "\n".join(final_lines) + "\n"
    sha = hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]
    header = f"# source_relpath: {rel}\n# source_sha256_16: {sha}\n"
    return header + body, sha


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--udb-root", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, default=OUT_DIR)
    parser.add_argument("--check-only", action="store_true", help="Build to memory; do not write")
    args = parser.parse_args()

    udb = args.udb_root
    if not udb.is_dir():
        print(f"ERROR: udb root missing: {udb}", file=sys.stderr)
        return 2

    manifest = load_manifest()
    tokens = all_scrub_tokens(manifest)
    needed = set()
    for case in manifest["positives"]:
        needed.update(case.get("csr_context_ids") or [])

    args.out_dir.mkdir(parents=True, exist_ok=True)
    meta: dict[str, Any] = {"csr": {}}

    for csr_id in sorted(needed):
        if csr_id not in CSR_PATHS:
            print(f"ERROR: unknown csr id {csr_id}", file=sys.stderr)
            return 2
        body, sha = build_one(udb, csr_id, tokens)
        meta["csr"][csr_id] = {"sha256_16": sha, "path": CSR_PATHS[csr_id]}
        # verify scrub
        for tok in tokens:
            for v in name_variants(tok):
                if len(v) >= 8 and re.search(rf"(?<![A-Za-z0-9_]){re.escape(v)}(?![A-Za-z0-9_])", body, re.I):
                    print(f"ERROR: residual token {v} in {csr_id}", file=sys.stderr)
                    return 1
        if not args.check_only:
            out = args.out_dir / f"{csr_id}.txt"
            out.write_text(body, encoding="utf-8")
            print(f"wrote {out.relative_to(ROOT)} ({len(body)} bytes)")

    meta_path = args.out_dir / "CONTEXT_META.json"
    if not args.check_only:
        meta_path.write_text(json_dumps(meta), encoding="utf-8")
        print(f"wrote {meta_path.name}")
    print("build_context: OK")
    return 0


def json_dumps(obj: Any) -> str:
    import json

    return json.dumps(obj, indent=2, sort_keys=True) + "\n"


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    raise SystemExit(main())
