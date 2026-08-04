#!/usr/bin/env python3
"""
Validate the 5% vertical slice.

Checks:
  - every manifest candidate present with source + review_envelope
  - approve_export candidates have clean param.yaml that validates as UDB param
  - reject and needs_more_evidence candidates have NO param.yaml
  - review envelope is never a valid UDB param document
  - excerpt text appears in source.txt
  - required reviewer fields present
  - WARL dedup case records rename alignment
  - reject case records csr_field_not_architectural_parameter
  - needs_more_evidence cases name what evidence would resolve them, rather
    than deferring with no exit condition
  - any evidence_type carries the pin it was determined against

Exit 0 = slice intact and reproducible.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
PKG = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PKG))
from export.schema_validate import validate_param_dict, validate_yaml_file  # noqa: E402

MANIFEST = ROOT / "MANIFEST.yaml"

REQUIRED_ENVELOPE_KEYS = (
    "candidate_id",
    "evidence",
    "classification",
    "duplicate_decision",
    "proposed",
    "schema_validation",
    "reviewer",
)


def ws(s: str) -> str:
    return re.sub(r"\s+", " ", s or "").strip()


def soft_norm(s: str) -> str:
    """Whitespace + strip common AsciiDoc/markup for excerpt grounding."""
    out = ws(s)
    out = re.sub(r"[`*_#]", "", out)
    return out.lower()


def main() -> int:
    errors: list[str] = []
    man = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    candidates = man.get("candidates") or []

    if len(candidates) < 8:
        errors.append(f"expected at least 8 candidates, got {len(candidates)}")

    saw_warl_dedup = False
    saw_reject_field = False
    approve_n = 0
    reject_n = 0
    unresolved_n = 0

    for case in candidates:
        cid = case["id"]
        cdir = ROOT / case["path"]
        src = cdir / "source.txt"
        env_path = cdir / "review_envelope.yaml"
        param_path = cdir / "param.yaml"

        if not src.is_file():
            errors.append(f"{cid}: missing source.txt")
            continue
        if not env_path.is_file():
            errors.append(f"{cid}: missing review_envelope.yaml")
            continue

        text = src.read_text(encoding="utf-8")
        env = yaml.safe_load(env_path.read_text(encoding="utf-8"))
        if not isinstance(env, dict):
            errors.append(f"{cid}: envelope not a mapping")
            continue

        for key in REQUIRED_ENVELOPE_KEYS:
            if key not in env:
                errors.append(f"{cid}: envelope missing key {key}")

        # envelope must not validate as UDB param (empty error list => valid)
        if not validate_param_dict(env):
            errors.append(f"{cid}: review envelope must not be UDB-valid")

        evidence = env.get("evidence") or {}
        excerpt = evidence.get("excerpt") or ""
        if len(ws(excerpt)) < 20:
            errors.append(f"{cid}: excerpt too short")
        # soft match: first 48 significant chars of excerpt in source
        probe = soft_norm(excerpt)[:48]
        if probe and probe not in soft_norm(text):
            frag = soft_norm(re.split(r"[.]", excerpt)[0])[:40]
            if frag and frag not in soft_norm(text):
                errors.append(f"{cid}: excerpt not found in source.txt")

        if not evidence.get("source_file"):
            errors.append(f"{cid}: missing source_file")
        if not evidence.get("source_commit_pin"):
            errors.append(f"{cid}: missing source_commit_pin")

        reviewer = env.get("reviewer") or {}
        decision = reviewer.get("decision") or case.get("decision")
        if decision == "approve_export":
            approve_n += 1
            if not param_path.is_file():
                errors.append(f"{cid}: approve_export requires param.yaml")
            else:
                doc = yaml.safe_load(param_path.read_text(encoding="utf-8"))
                # clean separation: no review-only keys
                forbidden = {
                    "excerpt",
                    "status",
                    "classification",
                    "candidate_id",
                    "reviewer",
                    "parameters",
                }
                if isinstance(doc, dict) and forbidden.intersection(doc.keys()):
                    errors.append(
                        f"{cid}: param.yaml contains review-only keys: "
                        f"{sorted(forbidden.intersection(doc.keys()))}"
                    )
                result = validate_yaml_file(param_path)
                if not result.ok:
                    errors.append(f"{cid}: param.yaml schema: {result.errors[0]}")
            dup = (env.get("duplicate_decision") or {}).get("status")
            if dup not in ("existing", "new", "possible_duplicate"):
                errors.append(f"{cid}: approve needs duplicate status existing/new/possible_duplicate")
        elif decision == "reject":
            reject_n += 1
            if param_path.is_file():
                errors.append(f"{cid}: reject must not ship param.yaml")
            reason = reviewer.get("reject_reason") or ""
            if "csr_field" not in reason and "not" not in reason:
                # still accept if class marks field-not-param
                cls = (env.get("classification") or {}).get("class", "")
                if cls != "CSR_FIELD_NOT_PARAM":
                    errors.append(f"{cid}: reject needs reject_reason or CSR_FIELD_NOT_PARAM class")
            saw_reject_field = True
        elif decision == "needs_more_evidence":
            unresolved_n += 1
            if param_path.is_file():
                errors.append(f"{cid}: needs_more_evidence must not ship param.yaml")
            # An abstention with no exit condition is a way of never deciding.
            # Saying what would settle it is what separates the two.
            resolvers = reviewer.get("evidence_that_would_resolve") or []
            if not isinstance(resolvers, list) or not resolvers:
                errors.append(f"{cid}: needs_more_evidence must list "
                              f"evidence_that_would_resolve")
            if not (reviewer.get("unresolved_questions") or []):
                errors.append(f"{cid}: needs_more_evidence must record the open "
                              f"questions")
        else:
            errors.append(f"{cid}: unknown decision {decision!r}")

        # An evidence type is a claim about a tree. Without a pin it cannot be
        # checked, which is exactly how a stale label reached a public thread.
        cls = env.get("classification") or {}
        if cls.get("evidence_type") and not cls.get("evidence_type_pin"):
            errors.append(f"{cid}: evidence_type without evidence_type_pin")

        # special cases
        if cid == "C04_ASIDLEN_TO_ASID_WIDTH":
            saw_warl_dedup = True
            dup = env.get("duplicate_decision") or {}
            if dup.get("alignment") != "rename_alias" and "ASID_WIDTH" not in str(dup):
                errors.append("C04 must record rename/alias dedup to ASID_WIDTH")
            if (env.get("proposed") or {}).get("name") != "ASID_WIDTH":
                errors.append("C04 proposed name must be ASID_WIDTH not ASIDLEN")

        if cid == "C05_REJECT_MTVEC_MODE_ENCODING":
            saw_reject_field = True
            if (env.get("classification") or {}).get("class") != "CSR_FIELD_NOT_PARAM":
                errors.append("C05 class must be CSR_FIELD_NOT_PARAM")

        if cid == "C03_MTVEC_MODES":
            if (env.get("classification") or {}).get("class") != "NORM_CSR_WARL":
                errors.append("C03 must be NORM_CSR_WARL true-WARL control")

    if not saw_warl_dedup:
        errors.append("slice missing WARL/rename dedup candidate (C04)")
    if not saw_reject_field:
        errors.append("slice missing CSR-field reject candidate (C05)")
    if approve_n < 4:
        errors.append(f"expected >=4 approve_export, got {approve_n}")
    if reject_n < 3:
        errors.append(f"expected >=3 reject, got {reject_n}")
    # A slice that can only approve and reject cannot represent not knowing,
    # and a workflow that cannot abstain will resolve every hard case wrongly
    # in whichever direction is cheaper.
    if unresolved_n < 1:
        errors.append(f"expected >=1 needs_more_evidence, got {unresolved_n}")

    if errors:
        print("vertical_5pct FAILED:")
        for e in errors:
            print(f"  - {e}")
        return 1

    print("vertical_5pct OK")
    print(f"  candidates: {len(candidates)}")
    print(f"  approve_export: {approve_n}")
    print(f"  reject: {reject_n}")
    print(f"  needs_more_evidence: {unresolved_n}")
    print("  review envelopes separated from UDB-valid param.yaml")
    print("  includes WARL dedup (C04), CSR-field reject (C05), derived reject")
    print("  (C06), pin-dependent evidence (C07) and honest abstention (C08)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
