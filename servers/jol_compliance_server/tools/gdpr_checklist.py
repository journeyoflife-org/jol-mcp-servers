"""GDPR checklist tool — return GDPR checklist for a given feature."""

from __future__ import annotations

from shared.sanitisation.input_sanitiser import InputSanitiser
from shared.sanitisation.output_sanitiser import OutputSanitiser

_sanitiser = InputSanitiser()
_output_sanitiser = OutputSanitiser()

# Standard GDPR checklist items
_GDPR_CHECKLIST = {
    "data_collection": [
        "Is personal data being collected?",
        "Is there a lawful basis for processing?",
        "Has a privacy notice been provided?",
        "Is data minimisation applied?",
    ],
    "data_storage": [
        "Where is data stored (jurisdiction)?",
        "Is encryption at rest applied?",
        "What is the retention period?",
        "Is there a deletion procedure?",
    ],
    "data_sharing": [
        "Are third-party processors identified?",
        "Are Data Processing Agreements in place?",
        "Is cross-border transfer compliant?",
    ],
    "rights": [
        "Can data subjects access their data?",
        "Can data subjects request deletion?",
        "Can data subjects object to processing?",
        "Is data portability supported?",
    ],
    "breach_response": [
        "Is there a breach detection mechanism?",
        "Can breaches be reported within 72 hours (Art. 33)?",
        "Are data subjects notified (Art. 34)?",
    ],
}


def gdpr_checklist(feature_name: str) -> str:
    """Return a GDPR compliance checklist for a given feature.

    Args:
        feature_name: Name of the feature to generate a checklist for.

    Returns:
        Formatted GDPR checklist.
    """
    safe_name = _sanitiser.validate(feature_name, "feature_name")

    lines = [f"# GDPR Checklist: {safe_name}", ""]

    for category, items in _GDPR_CHECKLIST.items():
        lines.append(f"## {category.replace('_', ' ').title()}")
        for item in items:
            lines.append(f"- [ ] {item}")
        lines.append("")

    output = "\n".join(lines)
    return _output_sanitiser.sanitise(output)
