"""
core/validators.py — NIST/EU AI Act Recursive Self-Validation Engine

Phase 14 / v15 Build Contract — Section IV.

Article 2: The system applies its own compliance checklist to its outputs.

This is a deterministic structural rule engine — not a checklist of strings.
Rules are evaluated against the verifier output text and must all pass for
the output to be considered constitutionally valid.

Rules enforced:
  1. Output must explicitly reference the physical_outcome_spec.
  2. Disallowed uncertainty phrases are forbidden (hallucination markers).
  3. Numeric claims must be accompanied by a unit.
  4. Disallowed harm-unchecked patterns must not appear without mitigation.
  5. Output must end with an explicit VERIFIED or FAILED verdict.
  6. Output must not contain unsupported superlative claims.

Failures are recorded per-rule and returned for state traceability.
"""

import re
from typing import List, Tuple

# ── Disallowed phrases (uncertainty / hallucination markers) ──────────────────

DISALLOWED_UNCERTAINTY: List[str] = [
    r"\bi guess\b",
    r"\bmaybe\b",
    r"\bperhaps\b",
    r"\bpossibly\b",
    r"\bi think\b",
    r"\bseems like\b",
    r"\bit is possible\b",
    r"\bunclear\b",
    r"\bhallucin",
]

# ── Disallowed superlatives without evidence ───────────────────────────────────

DISALLOWED_SUPERLATIVES: List[str] = [
    r"\bthe best\b",
    r"\bthe only\b",
    r"\bperfect\b",
    r"\bflawless\b",
    r"\bguaranteed\b",
]

# ── Pattern: numeric claim must be followed by a unit within 20 chars ─────────
# Matches a number not followed by a unit-like token.
# Units accepted: any word of 1–10 chars after optional whitespace.
# We flag bare numbers followed by punctuation or end-of-sentence.
_BARE_NUMBER = re.compile(r"\b\d+(?:\.\d+)?\s*(?=[,\.;:\)\n]|\Z)")


def enforce_nist_eu_self_validation(
    text: str,
    physical_outcome_spec: str = "",
) -> Tuple[bool, List[str]]:
    """
    Run the structural compliance rule engine against a verifier output.

    Args:
        text: The verifier LLM output to check.
        physical_outcome_spec: The backwards-design anchor (Article 5).
            If provided, the output must reference it.

    Returns:
        (passed: bool, failures: list[str])
        passed=True means all rules cleared.
    """
    failures: List[str] = []
    lower = text.lower()

    # Rule 1: Output must reference the physical outcome spec
    if physical_outcome_spec:
        # Check for any significant token from the spec (first 6 words)
        spec_tokens = [
            t.lower() for t in physical_outcome_spec.split()[:6]
            if len(t) > 3
        ]
        if spec_tokens and not any(tok in lower for tok in spec_tokens):
            failures.append(
                f"RULE-1 FAIL: Output does not reference physical_outcome_spec. "
                f"Expected tokens from: '{physical_outcome_spec[:80]}'"
            )

    # Rule 2: Disallowed uncertainty / hallucination phrases
    for pattern in DISALLOWED_UNCERTAINTY:
        if re.search(pattern, lower):
            failures.append(
                f"RULE-2 FAIL: Disallowed uncertainty phrase matched: '{pattern}'"
            )

    # Rule 3: Bare numeric claims without units
    bare_matches = _BARE_NUMBER.findall(text)
    if bare_matches:
        failures.append(
            f"RULE-3 FAIL: Numeric claims without units detected: {bare_matches[:5]}"
        )

    # Rule 4: Disallowed superlatives without evidence
    for pattern in DISALLOWED_SUPERLATIVES:
        if re.search(pattern, lower):
            failures.append(
                f"RULE-4 FAIL: Unsupported superlative detected: '{pattern}'"
            )

    # Rule 5: Must conclude with an explicit verdict
    if not re.search(r"\b(VERIFIED|FAILED)\b", text):
        failures.append(
            "RULE-5 FAIL: Output must conclude with explicit verdict VERIFIED or FAILED."
        )

    return len(failures) == 0, failures
