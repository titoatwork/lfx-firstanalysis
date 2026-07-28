#!/usr/bin/env python3
"""
Re-derive every published number from committed artifacts, and fail on mismatch.

Nothing here trusts prose. Each claim names the file it must come from and the
path within it. If a claim cannot be checked from a committed artifact, it is
reported as UNVERIFIABLE rather than passing silently, because a harness that
quietly skips what it cannot check is worse than no harness.

No credentials, no network, no model calls. Seconds.

    python scripts/verify_claims.py            # verify
    python scripts/verify_claims.py --list     # show the claim table

Exit codes:
    0  every checkable claim matches
    1  at least one claim disagrees with its artifact
    2  an artifact required by a claim is missing
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
AC_RUNS = ROOT / "artifact_c" / "runs"

RUN1 = "20260727T201408Z_gpt-4o-mini-2024-07-18"
RUN2 = "20260727T203634Z_gpt-4o-mini-2024-07-18"
RUN3 = "20260728T011101Z_gpt-4o-mini-2024-07-18"
RUN4 = "20260728T013748Z_gpt-4o-mini-2024-07-18"


@dataclass
class Claim:
    """One published number, and where it must be re-derivable from."""

    claim_id: str
    stated: object
    where_published: str
    artifact: Path
    getter: object
    note: str = ""
    tol: float = 0.0
    tags: list[str] = field(default_factory=list)


def load(p: Path) -> dict:
    return json.loads(p.read_text(encoding="utf-8"))


def pct(m: dict, key: str) -> float | None:
    """analyze.py writes a fraction plus a '72.9%' string. Return a float percent."""
    s = m.get(f"{key}_pct")
    if s is not None:
        return float(str(s).rstrip("%"))
    v = m.get(key)
    return None if v is None else round(float(v) * 100, 1)


def cls(m: dict, name: str) -> tuple[int, int] | None:
    v = (m.get("per_class_recall") or {}).get(name)
    if isinstance(v, dict) and "found" in v and "total" in v:
        return int(v["found"]), int(v["total"])
    return None


def arm_metrics(run: str, arm: str) -> Path:
    return AC_RUNS / run / f"metrics_arm_{arm}.json"


DECOMP = ROOT / "artifact_c" / "analysis" / "match_decomposition.json"


def decomp_row(run: str, arm: str):
    """One arm's exact/inexact split from decompose_matches.py."""
    def get(d: dict):
        for r in d.get("rows", []):
            if r["run"] == run and r["arm"] == arm:
                return r
        return None
    return get


def d_exact(run: str, arm: str):
    g = decomp_row(run, arm)
    return lambda d: (r := g(d)) and r["exact"]


def d_share(run: str, arm: str):
    """Percentage of matched gold credited by inexact passes rather than exact name."""
    g = decomp_row(run, arm)
    return lambda d: None if (r := g(d)) is None else round(100 * r["inexact_share"], 1)


def decomp_range(field: str, fn):
    return lambda d: fn(r[field] for r in d["rows"])


GEMINI_RUN = "20260728T015247Z_gemini-3.6-flash"


def call_outcome(arm: str, kind: str):
    """Count one arm's calls in a run manifest, split by what actually failed.

    This split is load-bearing rather than cosmetic. A 429 is the provider
    refusing the request; a getaddrinfo failure is this machine losing its
    network mid-run. PRIMARY_RESULTS.md cites only the first as a quota
    result, so both are pinned here and a future run that quietly reclassifies
    one as the other will fail the gate instead of improving the story.
    """

    def classify(err: str) -> str:
        if not err:
            return "ok"
        return "quota" if "RESOURCE_EXHAUSTED" in err else "network"

    return lambda d: sum(
        1 for c in d["calls"]
        if c["arm"] == arm and classify(c.get("error") or "") == kind
    )


CLAIMS: list[Claim] = [
    # ---- metrics.md section 2, Part I remeasure against the pinned gold ----
    Claim("part1.adjusted_recall", 72.9, "metrics.md §2",
          RESULTS / "metrics_claude-sonnet-4.part1-committed.json",
          lambda m: pct(m, "adjusted_recall"), tol=0.05, tags=["part1"]),
    Claim("part1.classification_accuracy", 88.4, "metrics.md §2",
          RESULTS / "metrics_claude-sonnet-4.part1-committed.json",
          lambda m: pct(m, "classification_accuracy"), tol=0.05, tags=["part1"]),
    Claim("part1.warl", (12, 24), "metrics.md §2",
          RESULTS / "metrics_claude-sonnet-4.part1-committed.json",
          lambda m: cls(m, "NORM_CSR_WARL"), tags=["part1"]),
    Claim("part1.direct", (83, 100), "metrics.md §2",
          RESULTS / "metrics_claude-sonnet-4.part1-committed.json",
          lambda m: cls(m, "NORM_DIRECT"), tags=["part1"]),
    Claim("part1.csr_rw", (32, 51), "metrics.md §2",
          RESULTS / "metrics_claude-sonnet-4.part1-committed.json",
          lambda m: cls(m, "NORM_CSR_RW"), tags=["part1"]),
    Claim("part1.deduped", 346, "metrics.md §2",
          RESULTS / "metrics_claude-sonnet-4.part1-committed.json",
          lambda m: m.get("total_llm_params_deduped"), tags=["part1"]),

    # ---- metrics.md section 5, Artifact A on gpt-4o-mini ----
    Claim("artifactA.adjusted_recall", 32.2, "metrics.md §5.2",
          RESULTS / "metrics_gpt-4o-mini.json",
          lambda m: pct(m, "adjusted_recall"), tol=0.05, tags=["artifactA"]),
    Claim("artifactA.warl", (3, 24), "metrics.md §5.2",
          RESULTS / "metrics_gpt-4o-mini.json",
          lambda m: cls(m, "NORM_CSR_WARL"), tags=["artifactA"]),
    Claim("artifactA.direct", (48, 100), "metrics.md §5.2",
          RESULTS / "metrics_gpt-4o-mini.json",
          lambda m: cls(m, "NORM_DIRECT"), tags=["artifactA"]),
    Claim("artifactA.deduped", 230, "metrics.md §5.2",
          RESULTS / "metrics_gpt-4o-mini.json",
          lambda m: m.get("total_llm_params_deduped"), tags=["artifactA"]),

    # ---- metrics.md section 5.3 and 5.4, cross-model agreement ----
    Claim("agreement.jaccard", 3.8, "metrics.md §5.3",
          RESULTS / "artifact_a_agreement.json",
          lambda m: round(float(m["agreement"]["jaccard"]) * 100, 1), tol=0.06,
          tags=["agreement"]),
    Claim("agreement.shared_names", 21, "metrics.md §5.3",
          RESULTS / "artifact_a_agreement.json",
          lambda m: m["agreement"]["shared_count"], tags=["agreement"]),
    Claim("agreement.unique_claude", 346, "metrics.md §5.3",
          RESULTS / "artifact_a_agreement.json",
          lambda m: m["agreement"]["n_a"], tags=["agreement"]),
    Claim("agreement.unique_mini", 230, "metrics.md §5.3",
          RESULTS / "artifact_a_agreement.json",
          lambda m: m["agreement"]["n_b"], tags=["agreement"]),
    Claim("agreement.class_agreement", 81.0, "metrics.md §5.3",
          RESULTS / "artifact_a_agreement.json",
          lambda m: round(float(m["agreement"]["class_agreement_rate"]) * 100, 1),
          tol=0.06, tags=["agreement"]),
    Claim("agreement.proposed_new_both", 9, "metrics.md §5.4",
          RESULTS / "artifact_a_agreement.json",
          lambda m: m["hallucination_overlap"]["n_both"], tags=["agreement"]),
    Claim("agreement.proposed_new_claude", 236, "metrics.md §5.4",
          RESULTS / "artifact_a_agreement.json",
          lambda m: m["hallucination_overlap"]["n_new_a"], tags=["agreement"]),
    Claim("agreement.proposed_new_mini", 218, "metrics.md §5.4",
          RESULTS / "artifact_a_agreement.json",
          lambda m: m["hallucination_overlap"]["n_new_b"], tags=["agreement"]),

    # ---- metrics.md section 6, v3 WARL ablation ----
    Claim("v3.adjusted_recall", 35.0, "metrics.md §6",
          RESULTS / "metrics_gpt-4o-mini.v3.json",
          lambda m: pct(m, "adjusted_recall"), tol=0.05, tags=["v3"]),
    Claim("v3.warl", (2, 24), "metrics.md §6",
          RESULTS / "metrics_gpt-4o-mini.v3.json",
          lambda m: cls(m, "NORM_CSR_WARL"), tags=["v3"]),

    # ---- metrics.md section 7, Artifact B export ----
    Claim("artifactB.named_schema_valid", (83, 83), "metrics.md §7",
          RESULTS / "export_b_named.json",
          lambda m: (m["schema_ok"], m["written"]), tags=["artifactB"]),
    Claim("artifactB.named_schema_fail", 0, "metrics.md §7",
          RESULTS / "export_b_named.json", lambda m: m["schema_fail"], tags=["artifactB"]),
    Claim("artifactB.named_udb_overlap", 83, "metrics.md §7",
          RESULTS / "export_b_named.json", lambda m: m["udb_overlap"], tags=["artifactB"]),
    Claim("artifactB.named_yes_rows", 87, "metrics.md §4",
          RESULTS / "export_b_named.json", lambda m: m["named_yes_rows"], tags=["artifactB"]),
    Claim("artifactB.named_yes_unique", 83, "metrics.md §4",
          RESULTS / "export_b_named.json", lambda m: m["named_yes_unique"], tags=["artifactB"]),
    Claim("artifactB.new_schema_valid", (20, 20), "metrics.md §7",
          RESULTS / "export_b_new.json",
          lambda m: (m["schema_ok"], m["written"]), tags=["artifactB"]),
    Claim("artifactB.new_udb_overlap", 0, "metrics.md §7",
          RESULTS / "export_b_new.json", lambda m: m["udb_overlap"], tags=["artifactB"]),

    # ---- Artifact C, the variance result ----
    Claim("artifactC.armA_run1", 33.9, "PRIMARY_RESULTS.md",
          arm_metrics(RUN1, "A"), lambda m: pct(m, "adjusted_recall"), tol=0.05,
          tags=["artifactC"]),
    Claim("artifactC.armA_run2", 44.6, "PRIMARY_RESULTS.md",
          arm_metrics(RUN2, "A"), lambda m: pct(m, "adjusted_recall"), tol=0.05,
          tags=["artifactC"]),
    Claim("artifactC.armB_run1", 29.4, "PRIMARY_RESULTS.md",
          arm_metrics(RUN1, "B"), lambda m: pct(m, "adjusted_recall"), tol=0.05,
          tags=["artifactC"]),
    Claim("artifactC.armB_run2", 32.2, "PRIMARY_RESULTS.md",
          arm_metrics(RUN2, "B"), lambda m: pct(m, "adjusted_recall"), tol=0.05,
          tags=["artifactC"]),
    Claim("artifactC.armA_csr_rw_run1", (6, 51), "PRIMARY_RESULTS.md",
          arm_metrics(RUN1, "A"), lambda m: cls(m, "NORM_CSR_RW"), tags=["artifactC"]),
    Claim("artifactC.armA_csr_rw_run2", (21, 51), "PRIMARY_RESULTS.md",
          arm_metrics(RUN2, "A"), lambda m: cls(m, "NORM_CSR_RW"), tags=["artifactC"]),
    Claim("artifactC.armB_warl_run1", (2, 24), "PRIMARY_RESULTS.md",
          arm_metrics(RUN1, "B"), lambda m: cls(m, "NORM_CSR_WARL"), tags=["artifactC"]),
    Claim("artifactC.armB_warl_run2", (9, 24), "PRIMARY_RESULTS.md",
          arm_metrics(RUN2, "B"), lambda m: cls(m, "NORM_CSR_WARL"), tags=["artifactC"]),

    # ---- arms C and D, the context arms, both runs ----
    Claim("artifactC.armC_run1", 32.8, "PRIMARY_RESULTS.md",
          arm_metrics(RUN3, "C"), lambda m: pct(m, "adjusted_recall"), tol=0.05,
          tags=["artifactC"]),
    Claim("artifactC.armC_run2", 39.5, "PRIMARY_RESULTS.md",
          arm_metrics(RUN4, "C"), lambda m: pct(m, "adjusted_recall"), tol=0.05,
          tags=["artifactC"]),
    Claim("artifactC.armD_run1", 35.0, "PRIMARY_RESULTS.md",
          arm_metrics(RUN3, "D"), lambda m: pct(m, "adjusted_recall"), tol=0.05,
          tags=["artifactC"]),
    Claim("artifactC.armD_run2", 31.1, "PRIMARY_RESULTS.md",
          arm_metrics(RUN4, "D"), lambda m: pct(m, "adjusted_recall"), tol=0.05,
          tags=["artifactC"]),
    # the bimodal CSR_RW observation
    Claim("artifactC.armC_csr_rw_run1", (5, 51), "PRIMARY_RESULTS.md",
          arm_metrics(RUN3, "C"), lambda m: cls(m, "NORM_CSR_RW"), tags=["artifactC"]),
    Claim("artifactC.armC_csr_rw_run2", (21, 51), "PRIMARY_RESULTS.md",
          arm_metrics(RUN4, "C"), lambda m: cls(m, "NORM_CSR_RW"), tags=["artifactC"]),

    # ---- exact vs inexact decomposition (exploratory, not preregistered) ----
    # The headline of the write-up: the score is mostly awarded by fuzzy matching,
    # and the exact-name component is the stable one.
    Claim("decomp.exact_min", 5, "PRIMARY_RESULTS.md", DECOMP,
          decomp_range("exact", min), tags=["decomp"]),
    Claim("decomp.exact_max", 9, "PRIMARY_RESULTS.md", DECOMP,
          decomp_range("exact", max), tags=["decomp"]),
    Claim("decomp.inexact_min", 47, "PRIMARY_RESULTS.md", DECOMP,
          decomp_range("inexact", min), tags=["decomp"]),
    Claim("decomp.inexact_max", 70, "PRIMARY_RESULTS.md", DECOMP,
          decomp_range("inexact", max), tags=["decomp"]),
    Claim("decomp.share_min", 84.5, "PRIMARY_RESULTS.md", DECOMP,
          lambda d: round(100 * min(r["inexact_share"] for r in d["rows"]), 1),
          tol=0.05, tags=["decomp"]),
    Claim("decomp.share_max", 90.4, "PRIMARY_RESULTS.md", DECOMP,
          lambda d: round(100 * max(r["inexact_share"] for r in d["rows"]), 1),
          tol=0.05, tags=["decomp"]),
    Claim("decomp.armA_run2_exact", 9, "PRIMARY_RESULTS.md", DECOMP,
          d_exact(RUN2, "A"), tags=["decomp"]),
    Claim("decomp.armB_run1_share", 90.4, "PRIMARY_RESULTS.md", DECOMP,
          d_share(RUN1, "B"), tol=0.05, tags=["decomp"]),
    # every arm in the table is a complete 60-chunk run
    Claim("decomp.all_arms_complete", True, "PRIMARY_RESULTS.md", DECOMP,
          lambda d: all(r["chunks"] >= 60 for r in d["rows"]), tags=["decomp"]),
    Claim("decomp.arms_counted", 8, "PRIMARY_RESULTS.md", DECOMP,
          lambda d: len(d["rows"]), tags=["decomp"]),

    # published baselines, same decomposition: the two models differ in kind
    Claim("decomp.claude_exact", 86, "PRIMARY_RESULTS.md",
          RESULTS / "metrics_claude-sonnet-4.part1-committed.json",
          lambda m: m["exact_matches_evaluated"], tags=["decomp"]),
    Claim("decomp.claude_share", 33.3, "PRIMARY_RESULTS.md",
          RESULTS / "metrics_claude-sonnet-4.part1-committed.json",
          lambda m: round(100 * (m["matched_udb_count"] - m["exact_matches_evaluated"])
                          / m["matched_udb_count"], 1), tol=0.05, tags=["decomp"]),
    Claim("decomp.mini_exact", 11, "PRIMARY_RESULTS.md",
          RESULTS / "metrics_gpt-4o-mini.json",
          lambda m: m["exact_matches_evaluated"], tags=["decomp"]),
    Claim("decomp.mini_share", 80.7, "PRIMARY_RESULTS.md",
          RESULTS / "metrics_gpt-4o-mini.json",
          lambda m: round(100 * (m["matched_udb_count"] - m["exact_matches_evaluated"])
                          / m["matched_udb_count"], 1), tol=0.05, tags=["decomp"]),
    Claim("decomp.v3_exact", 10, "PRIMARY_RESULTS.md",
          RESULTS / "metrics_gpt-4o-mini.v3.json",
          lambda m: m["exact_matches_evaluated"], tags=["decomp"]),

    # ---- why cross-provider replication did not complete ----
    # Arm A is the quota evidence: 21 responses, then the provider refused the
    # rest, with no network failure anywhere in the arm. Arm B is not quota
    # evidence at all and must not be quoted as if it were.
    Claim("gemini.armA_ok", 21, "PRIMARY_RESULTS.md limitations",
          AC_RUNS / GEMINI_RUN / "RUN_MANIFEST.json",
          call_outcome("A", "ok"), tags=["gemini"]),
    Claim("gemini.armA_quota", 39, "PRIMARY_RESULTS.md limitations",
          AC_RUNS / GEMINI_RUN / "RUN_MANIFEST.json",
          call_outcome("A", "quota"), tags=["gemini"]),
    Claim("gemini.armA_network", 0, "PRIMARY_RESULTS.md limitations",
          AC_RUNS / GEMINI_RUN / "RUN_MANIFEST.json",
          call_outcome("A", "network"), tags=["gemini"]),
    Claim("gemini.armB_ok", 0, "PRIMARY_RESULTS.md limitations",
          AC_RUNS / GEMINI_RUN / "RUN_MANIFEST.json",
          call_outcome("B", "ok"), tags=["gemini"]),
    Claim("gemini.armB_quota", 7, "PRIMARY_RESULTS.md limitations",
          AC_RUNS / GEMINI_RUN / "RUN_MANIFEST.json",
          call_outcome("B", "quota"), tags=["gemini"]),
    Claim("gemini.armB_network", 53, "PRIMARY_RESULTS.md limitations",
          AC_RUNS / GEMINI_RUN / "RUN_MANIFEST.json",
          call_outcome("B", "network"), tags=["gemini"]),
]

# Claims that are true but cannot be re-derived from anything committed.
# Listed so the harness is honest about its own coverage.
UNVERIFIABLE = [
    ("gt223.total", "223 live UDB parameters",
     "regenerated from a local UDB checkout; ground_truth.json is not committed"),
    ("part1.vs_gt223", "64.2% adjusted recall against live GT223",
     "scored against the uncommitted live gold"),
    ("artifactA.exclusive_sets", "227 Claude-only / 209 mini-only candidates",
     "per-chunk outputs were not retained; only the aggregate counts survive"),
    ("pilot.cost", "pilot ~$0.05 model split",
     "provider billing, not reproducible from artifacts"),
    ("gemini.daily_limit", "20 free-tier requests per day for gemini-3.6-flash",
     "the 429 body is truncated before the quota identifier, so the artifact "
     "shows refusal but never states the allowance; vendor documentation, not "
     "a measurement, and PRIMARY_RESULTS.md now says so"),
]


def compare(stated, got, tol: float) -> bool:
    if got is None:
        return False
    if isinstance(stated, tuple):
        return tuple(got) == stated
    if isinstance(stated, float):
        return abs(float(got) - stated) <= tol
    return got == stated


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", action="store_true", help="print the claim table and exit")
    ap.add_argument("--tag", help="verify only claims with this tag")
    args = ap.parse_args()

    claims = [c for c in CLAIMS if not args.tag or args.tag in c.tags]

    if args.list:
        print(f"{'claim':<34}{'stated':<16}{'published in':<24}artifact")
        for c in claims:
            print(f"  {c.claim_id:<32}{c.stated!s:<16}{c.where_published:<24}"
                  f"{c.artifact.relative_to(ROOT)}")
        return 0

    ok = bad = missing = 0
    failures = []

    for c in claims:
        if not c.artifact.exists():
            missing += 1
            failures.append(f"MISSING ARTIFACT  {c.claim_id}  ({c.artifact.relative_to(ROOT)})")
            continue
        try:
            got = c.getter(load(c.artifact))
        except Exception as exc:  # noqa: BLE001 - a broken getter is a failed claim
            bad += 1
            failures.append(f"ERROR             {c.claim_id}  {type(exc).__name__}: {exc}")
            continue
        if compare(c.stated, got, c.tol):
            ok += 1
        else:
            bad += 1
            failures.append(
                f"MISMATCH          {c.claim_id}\n"
                f"     published in {c.where_published}: {c.stated}\n"
                f"     artifact says {c.artifact.relative_to(ROOT)}: {got}"
            )

    print(f"claims checked : {len(claims)}")
    print(f"  verified     : {ok}")
    print(f"  mismatched   : {bad}")
    print(f"  missing      : {missing}")

    if failures:
        print("\n" + "\n".join(failures))

    print(f"\nnot checkable from committed artifacts : {len(UNVERIFIABLE)}")
    for cid, what, why in UNVERIFIABLE:
        print(f"  {cid:<26} {what}")
        print(f"  {'':<26} why: {why}")

    if missing:
        return 2
    if bad:
        return 1
    print("\nevery checkable published number re-derives from a committed artifact")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
