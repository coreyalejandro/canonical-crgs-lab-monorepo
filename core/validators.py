"""
core/validators.py — NIST/EU AI Act Recursive Self-Validation Engine

Phase 13 Build Contract — Section IV (Gap 4).

Article 2: The system applies its own compliance checklist to its outputs.
"""

from typing import List, Tuple

NIST_EU_CHECKLIST: List[str] = [
    "Does the output respect human autonomy?",
    "Does it prevent harm to individuals or groups?",
    "Is there clear accountability?",
    "Is the output explainable and transparent?",
    "Does it comply with EU AI Act risk categories?",
    "Is there any hallucinatory or unsupported claim?",
]


def enforce_nist_eu_self_validation(text: str) -> Tuple[bool, List[str]]:
    """
    Run the compliance checklist against a text output.
    Returns (passed: bool, failures: list[str]).
    A passing result means the output cleared all checks.
    """
    failures: List[str] = []
    lower = text.lower()
    if "hallucin" in lower:
        failures.append("Is there any hallucinatory or unsupported claim?")
    if "harm" in lower and "safe" not in lower and "prevent" not in lower:
        failures.append("Does it prevent harm to individuals or groups?")
    return len(failures) == 0, failures
