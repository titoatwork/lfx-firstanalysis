"""Name and text normalization for leakage + scoring."""

from __future__ import annotations

import re
import unicodedata


_NON_ALNUM = re.compile(r"[^A-Z0-9]+")
_WS = re.compile(r"\s+")


def normalize_param_name(name: str) -> str:
    """Upper snake-ish: keep A-Z0-9 only, uppercased (underscores removed for match)."""
    if not name:
        return ""
    s = unicodedata.normalize("NFKC", name).upper()
    s = _NON_ALNUM.sub("", s)
    return s


def normalize_ws(text: str) -> str:
    return _WS.sub(" ", text or "").strip()


def name_variants(name: str) -> set[str]:
    """Exact form + underscore-stripped normalized form."""
    raw = (name or "").strip()
    out = set()
    if raw:
        out.add(raw)
        out.add(raw.upper())
        out.add(normalize_param_name(raw))
    return {x for x in out if x}
