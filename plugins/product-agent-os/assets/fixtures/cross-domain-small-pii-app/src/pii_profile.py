"""Synthetic PII profile marker for cross-domain methodology routing."""


def classify_profile_field(field_name: str) -> str:
    if field_name in {"email", "phone"}:
        return "synthetic_pii"
    return "non_sensitive"
