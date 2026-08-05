#!/usr/bin/env python3
"""
Re-derive every registered number from committed artifacts, and fail on mismatch.

Coverage is the CLAIMS table below, not a scan of the prose. This proves the
registered figures against their artifacts; it does not prove that every figure
appearing in the documents was registered here.

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
import re
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
AC_RUNS = ROOT / "artifact_c" / "runs"
GOLD_AUDIT = ROOT / "analysis" / "gold_classification_audit.json"
SCHEMA_SHAPES = ROOT / "analysis" / "param_schema_shapes.json"


def _idl_audit_dissenters() -> tuple:
    """The parameters the IDL-consumption audit says the gold labels wrongly."""
    d = json.loads(GOLD_AUDIT.read_text(encoding="utf-8"))
    return tuple(sorted(r["name"] for r in d["disagree"]))

RUN1 = "20260727T201408Z_gpt-4o-mini-2024-07-18"
RUN2 = "20260727T203634Z_gpt-4o-mini-2024-07-18"
RUN3 = "20260728T011101Z_gpt-4o-mini-2024-07-18"
RUN4 = "20260728T013748Z_gpt-4o-mini-2024-07-18"


@dataclass
class Claim:
    """One published number, and where it must be re-derivable from.

    `audit_level` records a second, weaker guarantee that this harness used to
    conflate with the first:

      full_run        the number re-derives from a committed file AND the run
                      behind that file is reproducible from committed artefacts
      aggregate_only  the number re-derives from a committed file, but the run
                      behind it left no per-chunk or alignment trail, so it can
                      never be cross-checked

    Passing `verify_claims.py` proved only the first half until 2026-07-28.
    Artifact A slipped through on that gap: its exact-match count is real and
    re-derives, and there is no artefact anywhere that could contradict it.
    """

    claim_id: str
    stated: object
    where_published: str
    artifact: Path
    getter: object
    note: str = ""
    tol: float = 0.0
    tags: list[str] = field(default_factory=list)
    audit_level: str = "full_run"


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
NEMOTRON_RUN = "20260728T015526Z_nvidia_nemotron-3-ultra-550b-a55b_free"


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
        # Both providers refuse with a daily request quota, they just word it
        # differently: Gemini RESOURCE_EXHAUSTED, OpenRouter "Rate limit
        # exceeded: free-models-per-day". The wording initially read as a
        # throughput cap, which was wrong. Everything else is this machine
        # failing, and must never be reported as a vendor limit.
        if "RESOURCE_EXHAUSTED" in err or "Rate limit" in err:
            return "quota"
        if "getaddrinfo" in err or "unreachable" in err:
            return "network"
        return "other"

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

    # ---- the cross-check that was impossible until 2026-07-28 ----
    # `exact_matches_evaluated` is a lower bound (analyze.py:510 filters by
    # class_match is not None). Until the alignment files were recovered from a
    # git stash, nothing could confirm it for these two runs. Now both do.
    Claim("artifactA.alignment_exact", 11, "metrics.md §5, PRIMARY_RESULTS.md",
          RESULTS / "artifact_a" / "v2" / "alignment_gpt-4o-mini.json",
          lambda d: sum(1 for r in (d if isinstance(d, list) else d.get("alignments", []))
                        if r.get("match_type") == "exact"),
          tags=["artifactA", "recovered"]),
    Claim("v3.alignment_exact", 10, "metrics.md §6, PRIMARY_RESULTS.md",
          RESULTS / "artifact_a" / "v3" / "alignment_gpt-4o-mini.json",
          lambda d: sum(1 for r in (d if isinstance(d, list) else d.get("alignments", []))
                        if r.get("match_type") == "exact"),
          tags=["artifactA", "recovered"]),
    # The deduped list is what makes the model-exclusive sets recomputable.
    Claim("artifactA.recovered_deduped", 230, "metrics.md §5.3",
          RESULTS / "artifact_a" / "v2" / "deduped_gpt-4o-mini.json",
          lambda d: d.get("total_unique_parameters"), tags=["artifactA", "recovered"]),

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

    # The WARL ratios are registered; the percentages the documents actually print
    # beside them were not, so a typo in either would have gone unnoticed. Both
    # come from the same artifact as the ratio above.
    Claim("artifactA.warl_pct", 12.5, "metrics.md §5.2, §6 comparison, riscv-param-extraction/README.md",
          RESULTS / "metrics_gpt-4o-mini.json",
          lambda m: round(100 * m["per_class_recall"]["NORM_CSR_WARL"]["found"]
                          / m["per_class_recall"]["NORM_CSR_WARL"]["total"], 1),
          tol=0.05, tags=["artifactA"]),
    Claim("v3.warl_pct", 8.3, "metrics.md §6 comparison",
          RESULTS / "metrics_gpt-4o-mini.v3.json",
          lambda m: round(100 * m["per_class_recall"]["NORM_CSR_WARL"]["found"]
                          / m["per_class_recall"]["NORM_CSR_WARL"]["total"], 1),
          tol=0.05, tags=["v3"]),

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
    # The spread is the number the variance argument rests on, and it was printed
    # in the arm table without being derived from the two runs beside it.
    Claim("artifactC.armA_spread", 10.7, "PRIMARY_RESULTS.md arm table",
          arm_metrics(RUN2, "A"),
          lambda m: round(pct(m, "adjusted_recall")
                          - pct(json.loads(arm_metrics(RUN1, "A").read_text(encoding="utf-8")),
                                "adjusted_recall"), 1),
          tol=0.05, tags=["artifactC"]),
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
    # Recovered 2026-07-28 from a git stash on the UDB clone. Both alignment
    # files are committed under results/artifact_a/, so these cross-check.
    Claim("decomp.mini_exact", 11, "PRIMARY_RESULTS.md",
          RESULTS / "metrics_gpt-4o-mini.json",
          lambda m: m["exact_matches_evaluated"], tags=["decomp"]),
    Claim("decomp.mini_share", 80.7, "PRIMARY_RESULTS.md",
          RESULTS / "metrics_gpt-4o-mini.json",
          lambda m: round(100 * (m["matched_udb_count"] - m["exact_matches_evaluated"])
                          / m["matched_udb_count"], 1), tol=0.05, tags=["decomp"]),

    # The exact-name pair is the sharpest number on the public surface: it is the
    # "7.8x, not 2.3x" in README.md's proof table and in EVIDENCE.md 2.5. It was
    # published in five places and registered in none, so verify.sh never checked
    # it. The denominator is the scored per-class total (100+51+24+2 = 177), not
    # total_udb_params (185); the eight-entry difference is why 86/185 does not
    # reproduce 48.6.
    Claim("decomp.claude_exact_name_recall", 48.6, "README.md, metrics.md §5, PRIMARY_RESULTS.md",
          RESULTS / "metrics_claude-sonnet-4.part1-committed.json",
          lambda m: round(100 * m["exact_matches_evaluated"]
                          / sum(c["total"] for c in m["per_class_recall"].values()), 1),
          tol=0.05, tags=["decomp"]),
    Claim("decomp.mini_exact_name_recall", 6.2, "README.md, metrics.md §5, PRIMARY_RESULTS.md",
          RESULTS / "metrics_gpt-4o-mini.json",
          lambda m: round(100 * m["exact_matches_evaluated"]
                          / sum(c["total"] for c in m["per_class_recall"].values()), 1),
          tol=0.05, tags=["decomp"]),
    Claim("decomp.exact_name_denominator", 177, "metrics.md §5",
          RESULTS / "metrics_claude-sonnet-4.part1-committed.json",
          lambda m: sum(c["total"] for c in m["per_class_recall"].values()), tags=["decomp"]),
    Claim("decomp.v3_exact", 10, "PRIMARY_RESULTS.md",
          RESULTS / "metrics_gpt-4o-mini.v3.json",
          lambda m: m["exact_matches_evaluated"], tags=["decomp"]),

    # ---- the reproducible cross-model comparison that replaced 7.8x ----
    # Both complete arm A runs land on 9 exact matches. 86/9 = 9.6x, and the
    # adjusted denominator (177) cancels, so the ratio needs no separate gate.
    Claim("decomp.armA_run1_exact", 9, "README.md, metrics.md, PRIMARY_RESULTS.md",
          DECOMP, d_exact(RUN1, "A"), tags=["decomp", "crossmodel"]),
    Claim("decomp.crossmodel_exact_ratio", 9.6,
          "README.md, metrics.md, PRIMARY_RESULTS.md",
          DECOMP,
          lambda d: round(86 / min(r["exact"] for r in d["rows"] if r["arm"] == "A"), 1),
          tol=0.05, tags=["decomp", "crossmodel"]),
    # The published text says both arm A runs agree at 9. A ratio built on min()
    # would still pass if one of them vanished, so the agreement is gated too.
    # Found by sabotage-testing the two claims above.
    Claim("decomp.armA_exact_agreement", 2,
          "README.md, metrics.md, PRIMARY_RESULTS.md",
          DECOMP,
          lambda d: sum(1 for r in d["rows"] if r["arm"] == "A" and r["exact"] == 9),
          tags=["decomp", "crossmodel"]),

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

    # ---- third provider, third failure mode: OpenRouter throughput cap ----
    # No network failures here at all, so unlike the Gemini arm B this one is
    # cleanly attributable to the vendor.
    Claim("nemotron.armA_ok", 50, "PRIMARY_RESULTS.md limitations",
          AC_RUNS / NEMOTRON_RUN / "RUN_MANIFEST.json",
          call_outcome("A", "ok"), tags=["nemotron"]),
    Claim("nemotron.armA_refused", 9, "PRIMARY_RESULTS.md limitations",
          AC_RUNS / NEMOTRON_RUN / "RUN_MANIFEST.json",
          call_outcome("A", "quota"), tags=["nemotron"]),
    Claim("nemotron.armA_network", 0, "PRIMARY_RESULTS.md limitations",
          AC_RUNS / NEMOTRON_RUN / "RUN_MANIFEST.json",
          call_outcome("A", "network"), tags=["nemotron"]),
    Claim("nemotron.armB_ok", 0, "PRIMARY_RESULTS.md limitations",
          AC_RUNS / NEMOTRON_RUN / "RUN_MANIFEST.json",
          call_outcome("B", "ok"), tags=["nemotron"]),
    Claim("nemotron.armB_refused", 60, "PRIMARY_RESULTS.md limitations",
          AC_RUNS / NEMOTRON_RUN / "RUN_MANIFEST.json",
          call_outcome("B", "quota"), tags=["nemotron"]),
    # The fragment must stay below the 60-chunk gate. If a future edit ever
    # pushes it to 60 without a real re-run, this fails rather than letting a
    # 50-chunk arm into a published table.
    Claim("nemotron.armA_is_fragment", True, "PRIMARY_RESULTS.md limitations",
          AC_RUNS / NEMOTRON_RUN / "RUN_MANIFEST.json",
          lambda d: call_outcome("A", "ok")(d) < 60, tags=["nemotron"]),
    # OpenRouter states its daily cap in the 429 body. The run returned exactly
    # that many successes before the first refusal, so unlike Gemini's the limit
    # here is measured rather than cited. Both halves are gated: the stated
    # number, and the fact that it equals the observed ceiling.
    Claim("nemotron.stated_daily_limit", 50, "PRIMARY_RESULTS.md limitations",
          AC_RUNS / NEMOTRON_RUN / "RUN_MANIFEST.json",
          lambda d: next(iter({
              int(m) for c in d["calls"]
              for m in re.findall(r"'X-RateLimit-Limit': '(\d+)'", c.get("error") or "")
          }), None), tags=["nemotron"]),
    Claim("nemotron.limit_equals_observed", True, "PRIMARY_RESULTS.md limitations",
          AC_RUNS / NEMOTRON_RUN / "RUN_MANIFEST.json",
          lambda d: sum(1 for c in d["calls"] if c.get("ok")) == next(iter({
              int(m) for c in d["calls"]
              for m in re.findall(r"'X-RateLimit-Limit': '(\d+)'", c.get("error") or "")
          }), -1), tags=["nemotron"]),

    # --- objective-2 gold classification audit -------------------------------
    # These are gated because they are about to be stated in public on issue
    # #2200, and rule 4 ("re-derive before and after touching a published
    # number") only has force over numbers this harness actually knows about.
    # Every one re-derives from analysis/gold_classification_audit.json, which
    # is committed; `audit_gold_classification.py` regenerates it offline with
    # no model call. What is NOT re-derivable from this repo alone is listed in
    # UNVERIFIABLE below, so the split stays visible.
    Claim("gold_audit.gold_size", 185, "GOLD-CLASSIFICATION-AUDIT.md, issue #2200",
          GOLD_AUDIT, lambda d: d["gold_size"], tags=["gold_audit"]),
    # The gold states its own size in metadata. Gating both means 185 has to
    # agree with itself from two places, not just be counted once.
    Claim("gold_audit.gold_declared_total", 185, "GOLD-CLASSIFICATION-AUDIT.md",
          GOLD_AUDIT, lambda d: d["provenance"]["gold_declared_total"],
          tags=["gold_audit"]),
    Claim("gold_audit.evidence_params", 10, "GOLD-CLASSIFICATION-AUDIT.md, issue #2200",
          GOLD_AUDIT, lambda d: d["evidence_params"], tags=["gold_audit"]),
    Claim("gold_audit.agree", 4, "GOLD-CLASSIFICATION-AUDIT.md, issue #2200",
          GOLD_AUDIT, lambda d: len(d["agree"]), tags=["gold_audit"]),
    Claim("gold_audit.disagree", 4, "GOLD-CLASSIFICATION-AUDIT.md, issue #2200",
          GOLD_AUDIT, lambda d: len(d["disagree"]), tags=["gold_audit"]),
    # The four names are the claim, not just their count: naming the wrong
    # parameter in public is the failure mode a bare "4" would not catch.
    Claim("gold_audit.disagree_names",
          ("SXLEN", "UXLEN", "VSXLEN", "VUXLEN"),
          "GOLD-CLASSIFICATION-AUDIT.md, issue #2200",
          GOLD_AUDIT, lambda d: tuple(sorted(r["name"] for r in d["disagree"])),
          tags=["gold_audit"]),
    # Each disagreeing entry is high confidence. That is what makes the pattern
    # one-directional rather than a set of hedged guesses.
    Claim("gold_audit.disagree_all_high", True, "issue #2200",
          GOLD_AUDIT,
          lambda d: all(r["confidence"] == "high" for r in d["disagree"]),
          tags=["gold_audit"]),
    Claim("gold_audit.not_in_gold", 2, "GOLD-CLASSIFICATION-AUDIT.md",
          GOLD_AUDIT, lambda d: len(d["not_in_gold"]), tags=["gold_audit"]),
    Claim("gold_audit.name_recognition", 21, "GOLD-CLASSIFICATION-AUDIT.md, issue #2200",
          GOLD_AUDIT, lambda d: d["name_recognition_profile"]["count"],
          tags=["gold_audit"]),
    # The published assertion is not "21 entries used that template", it is that
    # all 21 landed on one class at one confidence. Gate the distribution, not
    # the headcount, or the interesting half of the sentence stays ungated.
    Claim("gold_audit.name_recognition_classes", (("NORM_DIRECT", 21),),
          "GOLD-CLASSIFICATION-AUDIT.md, issue #2200",
          GOLD_AUDIT,
          lambda d: tuple(sorted(d["name_recognition_profile"]["by_class"].items())),
          tags=["gold_audit"]),
    Claim("gold_audit.name_recognition_confidence", (("high", 21),),
          "GOLD-CLASSIFICATION-AUDIT.md, issue #2200",
          GOLD_AUDIT,
          lambda d: tuple(sorted(d["name_recognition_profile"]["by_confidence"].items())),
          tags=["gold_audit"]),
    Claim("gold_audit.warl_in_gold", 26, "GOLD-CLASSIFICATION-AUDIT.md, issue #2200",
          GOLD_AUDIT, lambda d: d["warl_in_gold"], tags=["gold_audit"]),
    Claim("gold_audit.warl_stale", 4, "GOLD-CLASSIFICATION-AUDIT.md, issue #2200",
          GOLD_AUDIT, lambda d: len(d["warl_stale"]), tags=["gold_audit"]),
    Claim("gold_audit.warl_stale_names",
          ("STVEC_MODE_DIRECT", "STVEC_MODE_VECTORED",
           "VSTVEC_MODE_DIRECT", "VSTVEC_MODE_VECTORED"),
          "GOLD-CLASSIFICATION-AUDIT.md, issue #2200",
          GOLD_AUDIT, lambda d: tuple(sorted(d["warl_stale"])), tags=["gold_audit"]),
    Claim("gold_audit.warl_undecidable", 18, "GOLD-CLASSIFICATION-AUDIT.md, issue #2200",
          GOLD_AUDIT, lambda d: len(d["warl_undecidable"]), tags=["gold_audit"]),
    # "18 of 26" is only honest if 4 + 4 + 18 accounts for all 26 with nothing
    # double-counted. Gating the partition stops a future edit from moving one
    # bucket and leaving the published ratio silently wrong.
    Claim("gold_audit.warl_partitions", True, "issue #2200",
          GOLD_AUDIT,
          lambda d: (len(d["agree"]) + len(d["warl_stale"])
                     + len(d["warl_undecidable"]) == d["warl_in_gold"]),
          tags=["gold_audit"]),
    Claim("gold_audit.warl_buckets_disjoint", True, "issue #2200",
          GOLD_AUDIT,
          lambda d: len({r["name"] for r in d["agree"]}
                        | set(d["warl_stale"]) | set(d["warl_undecidable"]))
                    == d["warl_in_gold"],
          tags=["gold_audit"]),
    # The 10 parameters the IDL decides must also account for exactly: those the
    # gold agrees with, those it disagrees with, and those absent from the gold.
    Claim("gold_audit.evidence_partitions", True, "issue #2200",
          GOLD_AUDIT,
          lambda d: (len(d["agree"]) + len(d["disagree"])
                     + len(d["not_in_gold"]) == d["evidence_params"]),
          tags=["gold_audit"]),

    # --- schema-shape audit, the second and independent route ------------------
    # These were left ungated when the script landed. They are gated now because
    # the schema-shape result is cited in PARAM-SCHEMA-SHAPES.md, in the claim
    # ledger, and in a public comment on issue #2251, and an ungated number that
    # three documents rely on is exactly what this harness exists to prevent.
    Claim("schema_shapes.params_scanned", 227, "PARAM-SCHEMA-SHAPES.md",
          SCHEMA_SHAPES, lambda d: d["params_scanned"], tags=["schema_shapes"]),
    Claim("schema_shapes.array_params", 15, "PARAM-SCHEMA-SHAPES.md",
          SCHEMA_SHAPES, lambda d: d["array_params"], tags=["schema_shapes"]),
    Claim("schema_shapes.set_enum_total", 9, "PARAM-SCHEMA-SHAPES.md, issue #2251",
          SCHEMA_SHAPES, lambda d: d["summary"]["set_enum"]["total"],
          tags=["schema_shapes"]),
    Claim("schema_shapes.bitmask_total", 5, "PARAM-SCHEMA-SHAPES.md",
          SCHEMA_SHAPES, lambda d: d["summary"]["bitmask"]["total"],
          tags=["schema_shapes"]),
    Claim("schema_shapes.set_integer_total", 1, "PARAM-SCHEMA-SHAPES.md",
          SCHEMA_SHAPES, lambda d: d["summary"]["set_integer"]["total"],
          tags=["schema_shapes"]),
    # Every array parameter must land in exactly one of the three shapes. If a
    # fourth shape ever appears, "all 15 fall into three shapes" stops being true
    # and the writeup's central sentence is wrong.
    Claim("schema_shapes.families_partition", True, "PARAM-SCHEMA-SHAPES.md",
          SCHEMA_SHAPES,
          lambda d: sum(g["total"] for g in d["summary"].values()) == d["array_params"],
          tags=["schema_shapes"]),
    # The published result is that two shapes are labelled consistently and
    # exactly one is split. Gate all three verdicts, not just the interesting one.
    Claim("schema_shapes.bitmask_consistent", True, "PARAM-SCHEMA-SHAPES.md",
          SCHEMA_SHAPES, lambda d: d["summary"]["bitmask"]["consistent"],
          tags=["schema_shapes"]),
    Claim("schema_shapes.set_integer_consistent", True, "PARAM-SCHEMA-SHAPES.md",
          SCHEMA_SHAPES, lambda d: d["summary"]["set_integer"]["consistent"],
          tags=["schema_shapes"]),
    Claim("schema_shapes.set_enum_is_split", False, "PARAM-SCHEMA-SHAPES.md",
          SCHEMA_SHAPES, lambda d: d["summary"]["set_enum"]["consistent"],
          tags=["schema_shapes"]),
    Claim("schema_shapes.bitmask_all_csr_rw", (("NORM_CSR_RW", 5),),
          "PARAM-SCHEMA-SHAPES.md",
          SCHEMA_SHAPES,
          lambda d: tuple(sorted(d["summary"]["bitmask"]["labels"].items())),
          tags=["schema_shapes"]),
    # The convergence is the finding, so it is gated as an invariant rather than
    # left as prose. The set_enum members the gold calls NORM_DIRECT must be
    # exactly the set the IDL-consumption audit flags, derived from a different
    # artifact by different logic. If a future edit breaks the agreement, this
    # fails loudly instead of the two documents quietly disagreeing.
    Claim("schema_shapes.converges_with_idl_audit", True,
          "PARAM-SCHEMA-SHAPES.md, issue #2251",
          SCHEMA_SHAPES,
          lambda d: tuple(sorted(r["name"] for r in d["groups"]["set_enum"]
                                 if r["gold"] == "NORM_DIRECT")) == _idl_audit_dissenters(),
          tags=["schema_shapes"]),
    Claim("schema_shapes.dissenters",
          ("SXLEN", "UXLEN", "VSXLEN", "VUXLEN"),
          "PARAM-SCHEMA-SHAPES.md, issue #2251",
          SCHEMA_SHAPES,
          lambda d: tuple(sorted(r["name"] for r in d["groups"]["set_enum"]
                                 if r["gold"] == "NORM_DIRECT")),
          tags=["schema_shapes"]),
]

# Claims that are true but cannot be re-derived from anything committed.
# Listed so the harness is honest about its own coverage.
UNVERIFIABLE = [
    # "live" was the wrong word for both of these and was corrected 2026-08-05.
    # 223 is the parameter count at the corpus pin `c184e313`, not on main:
    # `.udb-corpus` forked from main at `ba151afc` (2026-04-02) and main carries
    # 227 as of `52822ae6`. A pinned number described as live invites a reader to
    # compare it against a tree it was never measured on.
    ("gt223.total", "223 UDB parameters at corpus pin c184e313 (main: 227 at 52822ae6)",
     "regenerated from a local UDB checkout; ground_truth.json is not committed"),
    ("part1.vs_gt223", "64.2% adjusted recall against GT223, the corpus-pin gold",
     "scored against the uncommitted corpus-pin gold, not against main"),
    # Published in the same breath as 64.2 and unaccounted for the same reason.
    # Separated out so a reader looking for either finds it by name.
    ("part1.vs_gt223_class_acc", "88.6% classification accuracy against GT223",
     "same uncommitted corpus-pin gold as part1.vs_gt223"),
    ("gt223.strong_match", "91% strong match when GT223 was regenerated at c184e313",
     "property of the regeneration run against an uncommitted gold; the run log is "
     "not in this repository"),
    # EVIDENCE.md 2.4 republishes this from the #2317 comment, in bold, and it was
    # the only bold figure on the public surface that was neither checked nor
    # declared. It stays declared rather than registered because the criterion is
    # stated in prose ("live requirements that reference a different parameter")
    # and never encoded. Re-deriving it here by regex over origin/main at 4cf908e8
    # gives 48 counting every parameter name, 37 excluding MXLEN, 31 excluding the
    # whole XLEN family. None is 44, and a regex is a worse instrument than the IDL
    # the original reading used, so this reports the figure as posted upstream and
    # does not assert it is right.
    ("upstream.param_to_param_requirements",
     "44 of 227 params carry live requirements referencing another param (issue #2317)",
     "criterion stated in prose, not encoded; needs the IDL front end rather than a "
     "regex, and no toolchain here runs it"),
    # artifactA.exclusive_sets was listed here from 2026-07-25 to 2026-07-28.
    # It is now checkable: the deduped lists were recovered from a git stash on
    # the UDB clone, and `pipeline/agreement.py` reproduces the committed counts
    # exactly (236 / 218 / 9 / 227 / 209). Gated as agreement.* instead.
    ("pilot.cost", "pilot ~$0.05 model split",
     "provider billing, not reproducible from artifacts"),
    ("gemini.daily_limit", "20 free-tier requests per day for gemini-3.6-flash",
     "the 429 body is truncated before the quota identifier, so the artifact "
     "shows refusal but never states the allowance; vendor documentation, not "
     "a measurement, and PRIMARY_RESULTS.md now says so"),
    # The gold_audit.* claims above re-derive from the committed audit JSON, but
    # regenerating that JSON from scratch needs two inputs this repo does not
    # carry: the pinned gold (gitignored, and upstream it exists only inside the
    # unmerged PR #1766) and a UDB checkout. Both are pinned by digest in the
    # artifact's `provenance` block so a third party can confirm they had the
    # same bytes, which is the most this repo can offer without vendoring them.
    ("gold_audit.regenerable_here", "re-running the gold audit end to end",
     "needs the gitignored pinned gold and a UDB checkout; provenance records "
     "gold_canonical_sha256 and scanned_sha256 so the inputs are identifiable"),
    # Confirmed by re-running the audit against an export of main's two scanned
    # trees: every count and every name list came out identical, with a
    # different scanned_sha256 proving the trees really did differ. That
    # comparison is a session result, not a committed artifact.
    ("gold_audit.branch_independent", "the audit numbers do not depend on which "
     "UDB branch is scanned",
     "reproduced against main during review, but only the topic-branch run is "
     "committed, so the comparison itself is not re-derivable here"),
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

    aggregate_only = [c for c in claims if c.audit_level == "aggregate_only"]
    if aggregate_only:
        print(f"\nre-derives but cannot be audited : {len(aggregate_only)}")
        for c in aggregate_only:
            print(f"  {c.claim_id:<26} {c.artifact.relative_to(ROOT)}")
        print("  The run behind these left no per-chunk or alignment trail, so no")
        print("  artefact could contradict them. They pass. Do not lead with them.")

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
