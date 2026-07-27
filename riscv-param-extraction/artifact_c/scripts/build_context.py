#!/usr/bin/env python3
"""
Build leakage-audited CSR-field context blocks for the Artifact C arms.

Registered constraint (see ../PREREGISTRATION.md): context selection must be
driven by the CHUNK TEXT ONLY. The gold is used for scrubbing and for scoring,
never for deciding which CSRs a chunk gets. Anything else makes the experiment
circular.

What a context block contains:
  - CSR name, long_name, address, privilege mode
  - per-field: name, bit location, access type, description (truncated)

What it must never contain:
  - parameter YAML, param_schema content, gold classifications
  - any gold parameter name or normalised variant

The leak scan is fail-closed: if a gold name survives scrubbing into any context
file, the build aborts and writes nothing.

Usage:
  python build_context.py --udb-root ../../../.udb-corpus
  python build_context.py --udb-root ../../../.udb-corpus --check-only
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "contexts"

# CSR names that are ordinary English words or common tokens. Requiring a
# monospace/backtick or explicit CSR-word context stops every chunk pulling
# these in spuriously.
AMBIGUOUS = {
    "time", "cycle", "instret", "frm", "fflags", "fcsr",
    "seed", "menvcfg", "senvcfg",
}

MAX_FIELD_DESC = 600
MAX_CSR_DESC = 400
MAX_FIELDS_PER_CSR = 12
MAX_CSRS_PER_CHUNK = 8

# Unrendered ERB from the CSR sources; strip so the model sees prose not template.
ERB = re.compile(r"<%-?.*?-?%>", re.S)
BLANKS = re.compile(r"\n{3,}")


@dataclass
class Csr:
    name: str
    path: str
    long_name: str = ""
    address: str = ""
    priv: str = ""
    description: str = ""
    fields: list[dict] = field(default_factory=list)


def clean(text: str, limit: int) -> str:
    if not text:
        return ""
    t = ERB.sub("", str(text))
    t = BLANKS.sub("\n\n", t).strip()
    if len(t) > limit:
        t = t[:limit].rsplit(" ", 1)[0] + " ..."
    return t


def load_csrs(udb: Path) -> dict[str, Csr]:
    out: dict[str, Csr] = {}
    for p in sorted((udb / "spec" / "std" / "isa" / "csr").rglob("*.yaml")):
        try:
            doc = yaml.safe_load(p.read_text(encoding="utf-8", errors="replace"))
        except Exception:
            continue
        if not isinstance(doc, dict) or doc.get("kind") != "csr":
            continue
        name = doc.get("name") or p.stem
        c = Csr(
            name=name,
            path=str(p.relative_to(udb)).replace("\\", "/"),
            long_name=str(doc.get("long_name") or ""),
            address=str(doc.get("address") or ""),
            priv=str(doc.get("priv_mode") or ""),
            description=clean(doc.get("description", ""), MAX_CSR_DESC),
        )
        flds = doc.get("fields") or {}
        if isinstance(flds, dict):
            for fname, fbody in flds.items():
                if not isinstance(fbody, dict):
                    continue
                loc = (
                    fbody.get("location")
                    or fbody.get("location_rv64")
                    or fbody.get("location_rv32")
                    or ""
                )
                c.fields.append({
                    "name": str(fname),
                    "location": str(loc),
                    "type": str(fbody.get("type") or ""),
                    "description": clean(fbody.get("description", ""), MAX_FIELD_DESC),
                })
        out[name] = c
    return out


def gold_variants(gt_path: Path) -> tuple[set[str], dict[str, str]]:
    """Gold names plus normalised variants. Returns (variants, variant -> gold name)."""
    gt = json.loads(gt_path.read_text(encoding="utf-8"))
    names = {p["name"] for p in gt["parameters"]}
    variants: set[str] = set()
    back: dict[str, str] = {}
    for n in names:
        for v in (
            n, n.lower(), n.replace("_", ""), n.replace("_", "").lower(),
            n.replace("_", " "), n.replace("_", " ").lower(), n.replace("_", "-").lower(),
        ):
            if len(v) >= 4:
                variants.add(v)
                back.setdefault(v, n)
    return variants, back


def csrs_in_chunk(text: str, csrs: dict[str, Csr]) -> list[str]:
    """Select CSRs mentioned by the chunk. Chunk text only, never the gold."""
    hits: list[tuple[int, str]] = []
    for name, _ in csrs.items():
        if len(name) < 3:
            continue
        pat = re.compile(r"(?<![A-Za-z0-9_])" + re.escape(name) + r"(?![A-Za-z0-9_])")
        n = len(pat.findall(text))
        if n == 0:
            continue
        if name in AMBIGUOUS:
            # require a monospace or explicit-CSR context somewhere
            near = re.compile(
                r"`" + re.escape(name) + r"`|"
                + re.escape(name) + r"\s+(?:CSR|register|field)|"
                + r"(?:CSR|register)\s+" + re.escape(name)
            )
            if not near.search(text):
                continue
        hits.append((n, name))
    hits.sort(key=lambda t: (-t[0], t[1]))
    return [n for _, n in hits[:MAX_CSRS_PER_CHUNK]]


def render(csr: Csr) -> str:
    lines = [f"### CSR `{csr.name}`"]
    meta = []
    if csr.long_name:
        meta.append(csr.long_name)
    if csr.address:
        meta.append(f"address {csr.address}")
    if csr.priv:
        meta.append(f"privilege {csr.priv}")
    if meta:
        lines.append(" | ".join(meta))
    if csr.description:
        lines += ["", csr.description]
    if csr.fields:
        lines += ["", "Fields:"]
        for f in csr.fields[:MAX_FIELDS_PER_CSR]:
            head = f"- `{f['name']}`"
            if f["location"]:
                head += f" (bits {f['location']})"
            if f["type"]:
                head += f", access {f['type']}"
            lines.append(head)
            if f["description"]:
                for ln in f["description"].splitlines():
                    lines.append(f"    {ln}")
    return "\n".join(lines)


def build_pseudonyms(gt_path: Path) -> dict[str, str]:
    """Stable pseudonym per gold parameter, shared across all context files.

    A visible marker such as [REDACTED] would itself be a leak: it announces
    "a parameter name belongs here", handing the model location even without
    the name. A neutral pseudonym keeps the sentence grammatical, keeps
    cross-references consistent between contexts, and carries no information
    about the real name.
    """
    gt = json.loads(gt_path.read_text(encoding="utf-8"))
    names = sorted({p["name"] for p in gt["parameters"]})
    return {n: f"PARAM_{i:03d}" for i, n in enumerate(names, 1)}


def scrub(text: str, variants: set[str], pseudo: dict[str, str],
          var_to_gold: dict[str, str]) -> tuple[str, int]:
    """Replace gold parameter names with their stable pseudonyms."""
    n = 0
    for v in sorted(variants, key=len, reverse=True):
        pat = re.compile(r"(?<![A-Za-z0-9_])" + re.escape(v) + r"(?![A-Za-z0-9_])", re.I)
        repl = pseudo.get(var_to_gold.get(v, ""), "PARAM_UNSPECIFIED")
        text, k = pat.subn(repl, text)
        n += k
    return text, n


def leak_check(text: str, variants: set[str]) -> list[str]:
    found = []
    for v in variants:
        pat = re.compile(r"(?<![A-Za-z0-9_])" + re.escape(v) + r"(?![A-Za-z0-9_])", re.I)
        if pat.search(text):
            found.append(v)
    return found


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--udb-root", required=True, type=Path)
    ap.add_argument("--check-only", action="store_true")
    args = ap.parse_args()

    udb = args.udb_root.resolve()
    chunks_dir = udb / "param_extraction" / "chunks"
    gt_path = udb / "param_extraction" / "data" / "ground_truth.json"
    for p in (chunks_dir, gt_path):
        if not p.exists():
            print(f"missing: {p}", file=sys.stderr)
            return 2

    csrs = load_csrs(udb)
    variants, var_to_gold = gold_variants(gt_path)
    pseudo = build_pseudonyms(gt_path)
    print(f"CSRs loaded            : {len(csrs)}")
    print(f"gold scrub variants    : {len(variants)}")

    # The 60 param-bearing chunks are the scored corpus; report coverage on them.
    inv_path = ROOT.parent / "results" / "artifact_a_chunk_inventory.json"
    scored_ids = set()
    if inv_path.exists():
        inv = json.loads(inv_path.read_text(encoding="utf-8"))
        scored_ids = {c["chunk_id"] for c in inv.get("chunks", [])}

    built, leaked, stats = {}, [], []
    for cp in sorted(chunks_dir.glob("chunk_*.txt")):
        text = cp.read_text(encoding="utf-8", errors="replace")
        picked = csrs_in_chunk(text, csrs)
        if not picked:
            stats.append((cp.stem, 0, 0, 0))
            continue
        blocks = [render(csrs[n]) for n in picked]
        body = (
            "## CSR and field reference for this excerpt\n"
            "Definitions of CSRs named in the text above. Reference material only.\n\n"
            + "\n\n".join(blocks)
        )
        scrubbed, nrep = scrub(body, variants, pseudo, var_to_gold)
        residual = leak_check(scrubbed, variants)
        if residual:
            leaked.append((cp.stem, sorted(residual)[:5]))
        built[cp.stem] = scrubbed
        stats.append((cp.stem, len(picked), nrep, len(scrubbed)))

    with_ctx = [s for s in stats if s[1] > 0]
    print(f"chunks with context    : {len(with_ctx)} / {len(stats)}")
    if with_ctx:
        print(f"avg CSRs per chunk     : {sum(s[1] for s in with_ctx)/len(with_ctx):.1f}")
        print(f"avg context chars      : {sum(s[3] for s in with_ctx)/len(with_ctx):.0f}")
        print(f"max context chars      : {max(s[3] for s in with_ctx)}")
    print(f"gold names pseudonymised: {sum(s[2] for s in stats)}")

    if scored_ids:
        cov = [s for s in stats if s[0] in scored_ids and s[1] > 0]
        print(f"\nCOVERAGE ON THE SCORED CORPUS (the 60 param-bearing chunks)")
        print(f"  chunks receiving context : {len(cov)} / {len(scored_ids)}")
        print(f"  chunks with NO context   : {len(scored_ids) - len(cov)}  (treatment == baseline for these)")
        if cov:
            print(f"  avg CSRs per covered chunk: {sum(s[1] for s in cov)/len(cov):.1f}")

    if leaked:
        print("\nFAIL-CLOSED: gold names survived scrubbing", file=sys.stderr)
        for cid, names in leaked[:10]:
            print(f"  {cid}: {names}", file=sys.stderr)
        print("nothing written", file=sys.stderr)
        return 1
    print("leak scan              : clean")

    if args.check_only:
        print("\ncheck-only, nothing written")
        return 0

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for cid, body in built.items():
        (OUT_DIR / f"{cid}.md").write_text(body, encoding="utf-8")
    (OUT_DIR / "INDEX.json").write_text(
        json.dumps(
            {
                "udb_sha_note": "pin recorded by the runner",
                "chunks_with_context": len(built),
                "chunks_total": len(stats),
                "per_chunk": {s[0]: {"csrs": s[1], "scrubbed": s[2], "chars": s[3]} for s in stats},
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"\nwrote {len(built)} context files to {OUT_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
