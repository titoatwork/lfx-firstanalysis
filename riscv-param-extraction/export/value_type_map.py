"""
Map Part I spreadsheet value_type strings to UDB param `schema` fragments.

Honest about uncertainty: the CSV does not encode enum members, range bounds,
or bitmask widths. Those remain TODOs in the draft rather than invented values.

Mirrors the *inverse* of Part I `export_udb_params.derive_value_type` where
possible (boolean/binary, integer enum/range, arrays for set).
"""

from __future__ import annotations

from typing import Any


# Draft marker embedded in schema when the CSV cannot fully specify the type.
DRAFT_SCHEMA_NOTE = (
    "DRAFT: value domain incomplete from parameters.csv; "
    "human review required before any UDB PR."
)


def schema_for_value_type(value_type: str) -> dict[str, Any]:
    """
    Return a JSON-Schema object suitable for a UDB param `schema:` field.

    Does not invent concrete enum members or range bounds that the CSV lacks.
    """
    vt = (value_type or "").strip().lower()

    if vt == "binary":
        # UDB uses both boolean and two-value integer enums; boolean is the
        # conservative default for implementer yes/no parameters.
        return {"type": "boolean"}

    if vt == "enum":
        # Members unknown from CSV alone — open integer enum placeholder with
        # an explicit draft note (validators accept free-form enum later).
        return {
            "type": "integer",
            "description": (
                f"{DRAFT_SCHEMA_NOTE} "
                "Fill `enum: [...]` from the ISA manual excerpt."
            ),
        }

    if vt == "range":
        return {
            "type": "integer",
            "description": (
                f"{DRAFT_SCHEMA_NOTE} "
                "Fill `minimum` / `maximum` from the ISA manual excerpt."
            ),
        }

    if vt == "set":
        return {
            "type": "array",
            "items": {"type": "integer"},
            "minItems": 1,
            "uniqueItems": True,
            "description": (
                f"{DRAFT_SCHEMA_NOTE} "
                "Constrain `items.enum` when the legal set is known."
            ),
        }

    if vt == "bitmask":
        return {
            "type": "integer",
            "minimum": 0,
            "description": (
                f"{DRAFT_SCHEMA_NOTE} "
                "Bitmask width / legal bits need manual fill from the CSR field."
            ),
        }

    if vt == "value":
        return {
            "type": "integer",
            "description": (
                f"{DRAFT_SCHEMA_NOTE} "
                "Single implementation-defined value; constrain if the spec bounds it."
            ),
        }

    # Unknown / missing — still produce a valid schema object so the file can
    # be reviewed rather than silently dropped.
    return {
        "type": "integer",
        "description": (
            f"{DRAFT_SCHEMA_NOTE} "
            f"Unrecognized value_type={value_type!r}; defaulted to integer."
        ),
    }
