#!/usr/bin/env python3
"""CLI: inter-model agreement + hallucination-overlap (offline, $0).

Examples::

  python -m pipeline.compare_models \\
    --a ../riscv-unified-db/param_extraction/results/v2/deduped_claude-sonnet-4.json \\
    --b ../riscv-unified-db/param_extraction/results/v2/deduped_gpt-4o-mini.json \\
    --model-a claude-sonnet-4 --model-b gpt-4o-mini \\
    --udb-gt ../riscv-unified-db/param_extraction/data/ground_truth.json \\
    --out results/artifact_a_agreement.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .agreement import (
    compute_agreement,
    compute_hallucination_overlap,
    markdown_agreement_table,
    markdown_hallucination_table,
)
from .load_results import load_param_list, load_udb_names, load_udb_names_from_yaml_dir


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Artifact A: agreement + hallucination-overlap (no API)",
    )
    parser.add_argument("--a", type=Path, required=True, help="Model A merged/deduped JSON")
    parser.add_argument("--b", type=Path, required=True, help="Model B merged/deduped JSON")
    parser.add_argument("--model-a", default="model_a")
    parser.add_argument("--model-b", default="model_b")
    parser.add_argument(
        "--udb-gt",
        type=Path,
        help="ground_truth.json for UDB name set (proposed-new filter)",
    )
    parser.add_argument(
        "--udb-param-dir",
        type=Path,
        help="spec/std/isa/param directory (alternative to --udb-gt)",
    )
    parser.add_argument(
        "--any-confidence",
        action="store_true",
        help="Include medium/low in proposed-new (default: high only)",
    )
    parser.add_argument("--out", type=Path, help="Write full JSON report")
    parser.add_argument(
        "--md-out",
        type=Path,
        help="Write markdown tables (for metrics.md paste)",
    )
    args = parser.parse_args(argv)

    params_a = load_param_list(args.a)
    params_b = load_param_list(args.b)

    if args.udb_gt:
        udb_names = load_udb_names(args.udb_gt)
    elif args.udb_param_dir:
        udb_names = load_udb_names_from_yaml_dir(args.udb_param_dir)
    else:
        print("error: provide --udb-gt or --udb-param-dir", file=sys.stderr)
        return 2

    agr = compute_agreement(
        params_a,
        params_b,
        model_a=args.model_a,
        model_b=args.model_b,
    )
    hall = compute_hallucination_overlap(
        params_a,
        params_b,
        udb_names,
        model_a=args.model_a,
        model_b=args.model_b,
        high_confidence_only=not args.any_confidence,
    )

    payload = {
        "agreement": agr.to_dict(),
        "hallucination_overlap": hall.to_dict(),
        "udb_name_count": len(udb_names),
    }

    md = (
        "### Inter-model agreement (parameter names)\n\n"
        + markdown_agreement_table(agr)
        + "\n\n### Hallucination-overlap (proposed-new)\n\n"
        + markdown_hallucination_table(hall)
        + f"\n\n_{hall.notes} UDB names loaded: {len(udb_names)}._\n"
    )

    print(md)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        # Compact lists in summary file: keep counts + sample names
        summary = {
            "agreement": {
                **{k: v for k, v in agr.to_dict().items() if k not in (
                    "shared_names", "only_a", "only_b"
                )},
                "shared_count": len(agr.shared_names),
                "only_a_count": len(agr.only_a),
                "only_b_count": len(agr.only_b),
                "shared_names_sample": agr.shared_names[:40],
                "only_a_sample": agr.only_a[:40],
                "only_b_sample": agr.only_b[:40],
            },
            "hallucination_overlap": {
                **{k: v for k, v in hall.to_dict().items() if k not in (
                    "new_a", "new_b", "both_new", "only_a_new", "only_b_new"
                )},
                "both_new_sample": hall.both_new[:40],
                "only_a_new_sample": hall.only_a_new[:40],
                "only_b_new_sample": hall.only_b_new[:40],
            },
            "udb_name_count": len(udb_names),
        }
        args.out.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
        print(f"Wrote {args.out}", file=sys.stderr)
    if args.md_out:
        args.md_out.parent.mkdir(parents=True, exist_ok=True)
        args.md_out.write_text(md, encoding="utf-8")
        print(f"Wrote {args.md_out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
