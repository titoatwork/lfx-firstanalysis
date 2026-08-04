"""Inter-model agreement and hallucination-overlap for Artifact A."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class AgreementReport:
    model_a: str
    model_b: str
    n_a: int
    n_b: int
    shared_names: list[str]
    only_a: list[str]
    only_b: list[str]
    union: int
    jaccard: float
    match_rate_vs_a: float  # |shared| / |A|
    match_rate_vs_b: float  # |shared| / |B|
    shared_class_agree: int
    shared_class_disagree: int
    class_agreement_rate: float | None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class HallucinationOverlapReport:
    """Proposed-new = not in UDB name set; optional high-confidence filter."""

    model_a: str
    model_b: str
    confidence_filter: str  # "high" | "any"
    new_a: list[str]
    new_b: list[str]
    both_new: list[str]
    only_a_new: list[str]
    only_b_new: list[str]
    n_new_a: int
    n_new_b: int
    n_both: int
    n_only_a: int
    n_only_b: int
    # of new-A, fraction also proposed new by B
    overlap_rate_vs_a: float | None
    overlap_rate_vs_b: float | None
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ClassRecallRow:
    cls: str
    found: int
    total: int
    recall: float | None = None

    def __post_init__(self) -> None:
        if self.total > 0:
            self.recall = self.found / self.total


def params_by_name(params: list[dict]) -> dict[str, dict]:
    return {p["parameter_name"]: p for p in params if p.get("parameter_name")}


def _name_set(params: list[dict]) -> set[str]:
    return {p["parameter_name"] for p in params if p.get("parameter_name")}


def is_proposed_new(param: dict, udb_names: set[str]) -> bool:
    """True if the param is not an existing UDB name.

    Uses ``existing_udb_name`` when present; always checks the name against
    the UDB name set (stricter: the name must not be a param in the scanned
    UDB tree either, whichever revision that tree is on).
    """
    name = param.get("parameter_name") or ""
    existing = param.get("existing_udb_name")
    if existing not in (None, "", "null", "None"):
        # Model claims a UDB mapping
        if str(existing) in udb_names or name in udb_names:
            return False
    if name in udb_names:
        return False
    return True


def compute_agreement(
    params_a: list[dict],
    params_b: list[dict],
    *,
    model_a: str = "model_a",
    model_b: str = "model_b",
) -> AgreementReport:
    by_a = params_by_name(params_a)
    by_b = params_by_name(params_b)
    names_a = set(by_a)
    names_b = set(by_b)
    shared = sorted(names_a & names_b)
    only_a = sorted(names_a - names_b)
    only_b = sorted(names_b - names_a)
    union = len(names_a | names_b)
    jaccard = (len(shared) / union) if union else 0.0
    match_a = (len(shared) / len(names_a)) if names_a else 0.0
    match_b = (len(shared) / len(names_b)) if names_b else 0.0

    agree = 0
    disagree = 0
    for name in shared:
        ca = (by_a[name].get("class") or "").strip()
        cb = (by_b[name].get("class") or "").strip()
        if not ca or not cb:
            continue
        if ca == cb:
            agree += 1
        else:
            disagree += 1
    evaluated = agree + disagree
    class_rate = (agree / evaluated) if evaluated else None

    return AgreementReport(
        model_a=model_a,
        model_b=model_b,
        n_a=len(names_a),
        n_b=len(names_b),
        shared_names=shared,
        only_a=only_a,
        only_b=only_b,
        union=union,
        jaccard=round(jaccard, 4),
        match_rate_vs_a=round(match_a, 4),
        match_rate_vs_b=round(match_b, 4),
        shared_class_agree=agree,
        shared_class_disagree=disagree,
        class_agreement_rate=round(class_rate, 4) if class_rate is not None else None,
    )


def compute_hallucination_overlap(
    params_a: list[dict],
    params_b: list[dict],
    udb_names: set[str],
    *,
    model_a: str = "model_a",
    model_b: str = "model_b",
    high_confidence_only: bool = True,
) -> HallucinationOverlapReport:
    def select(params: list[dict]) -> set[str]:
        out: set[str] = set()
        for p in params:
            name = p.get("parameter_name")
            if not name:
                continue
            if high_confidence_only and str(p.get("confidence", "")).lower() != "high":
                continue
            if is_proposed_new(p, udb_names):
                out.add(name)
        return out

    new_a = select(params_a)
    new_b = select(params_b)
    both = sorted(new_a & new_b)
    only_a = sorted(new_a - new_b)
    only_b = sorted(new_b - new_a)
    rate_a = (len(both) / len(new_a)) if new_a else None
    rate_b = (len(both) / len(new_b)) if new_b else None
    note = (
        "Proposed-new = name not in UDB set and no trusted existing_udb_name hit; "
        + ("confidence==high only." if high_confidence_only else "any confidence.")
    )
    return HallucinationOverlapReport(
        model_a=model_a,
        model_b=model_b,
        confidence_filter="high" if high_confidence_only else "any",
        new_a=sorted(new_a),
        new_b=sorted(new_b),
        both_new=both,
        only_a_new=only_a,
        only_b_new=only_b,
        n_new_a=len(new_a),
        n_new_b=len(new_b),
        n_both=len(both),
        n_only_a=len(only_a),
        n_only_b=len(only_b),
        overlap_rate_vs_a=round(rate_a, 4) if rate_a is not None else None,
        overlap_rate_vs_b=round(rate_b, 4) if rate_b is not None else None,
        notes=note,
    )


def markdown_agreement_table(report: AgreementReport) -> str:
    lines = [
        f"| Metric | Value |",
        f"|--------|------:|",
        f"| Model A | {report.model_a} |",
        f"| Model B | {report.model_b} |",
        f"| Unique params A | {report.n_a} |",
        f"| Unique params B | {report.n_b} |",
        f"| Shared names | {len(report.shared_names)} |",
        f"| Only A | {len(report.only_a)} |",
        f"| Only B | {len(report.only_b)} |",
        f"| Jaccard (name) | {report.jaccard:.1%} |",
        f"| Match rate vs A (|shared|/|A|) | {report.match_rate_vs_a:.1%} |",
        f"| Match rate vs B (|shared|/|B|) | {report.match_rate_vs_b:.1%} |",
    ]
    if report.class_agreement_rate is not None:
        lines.append(
            f"| Class agreement on shared (evaluated) | "
            f"{report.class_agreement_rate:.1%} "
            f"({report.shared_class_agree}/"
            f"{report.shared_class_agree + report.shared_class_disagree}) |"
        )
    else:
        lines.append("| Class agreement on shared | — |")
    return "\n".join(lines)


def markdown_hallucination_table(report: HallucinationOverlapReport) -> str:
    def pct(x: float | None) -> str:
        return "—" if x is None else f"{x:.1%}"

    lines = [
        f"| Metric | Value |",
        f"|--------|------:|",
        f"| Confidence filter | {report.confidence_filter} |",
        f"| Proposed-new A | {report.n_new_a} |",
        f"| Proposed-new B | {report.n_new_b} |",
        f"| Both models (overlap) | {report.n_both} |",
        f"| Only A | {report.n_only_a} |",
        f"| Only B | {report.n_only_b} |",
        f"| Overlap rate vs A | {pct(report.overlap_rate_vs_a)} |",
        f"| Overlap rate vs B | {pct(report.overlap_rate_vs_b)} |",
    ]
    return "\n".join(lines)
