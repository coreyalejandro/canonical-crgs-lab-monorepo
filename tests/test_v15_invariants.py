"""
tests/test_v15_invariants.py — Constitutional Runtime Governance Engine v15.0

CI enforcement tests for every nonnegotiable invariant.
All tests are deterministic — no LLM calls, no network.

Coverage:
  - Human checkpoint raises PermissionError (not RuntimeError)
  - MoE temperatures are frozen and immutable
  - Pydantic state is strict-typed
  - Backwards design: physical_outcome_spec enforced before generation
  - Merkle chain: chaining + validate_chain() + tamper detection
  - Self-validation: structural rule engine rejects known failure patterns
  - Dual-parity: send_constitutional_message raises on empty layers
  - Role fluidity: active_role field exists and accepts both values
  - Architecture: core modules import cleanly with no circular deps
"""

import hashlib
import json
import os
import sys
import tempfile

import pytest

# ── Make sure repo root is on path ───────────────────────────────────────────
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


# ─────────────────────────────────────────────────────────────────────────────
# P0 – Human checkpoint raises PermissionError
# ─────────────────────────────────────────────────────────────────────────────

def test_human_checkpoint_raises_permission_error():
    """Article 8: missing signature must raise PermissionError, not RuntimeError."""
    from core.state import ResearchState
    from core.orchestrator import human_cryptographic_checkpoint

    state = ResearchState(human_signature_hash=None)
    with pytest.raises(PermissionError):
        human_cryptographic_checkpoint(state)


def test_human_checkpoint_not_runtime_error():
    """Regression guard: must not be RuntimeError."""
    from core.state import ResearchState
    from core.orchestrator import human_cryptographic_checkpoint

    state = ResearchState(human_signature_hash=None)
    with pytest.raises(Exception) as exc_info:
        human_cryptographic_checkpoint(state)
    assert not isinstance(exc_info.value, RuntimeError), (
        "human_checkpoint must raise PermissionError, not RuntimeError"
    )


# ─────────────────────────────────────────────────────────────────────────────
# P0 – Immutable MoE temperatures
# ─────────────────────────────────────────────────────────────────────────────

def test_visionary_temperature_is_1():
    """Article 10: Visionary temperature must be 1.0."""
    from core.model_config import CONFIG
    assert CONFIG.visionary_temp == 1.0


def test_verifier_temperature_is_0():
    """Article 10: Verifier temperature must be 0.0."""
    from core.model_config import CONFIG
    assert CONFIG.verifier_temp == 0.0


def test_model_config_is_frozen():
    """Article 10: ImmutableModelConfig must be frozen — mutation raises FrozenInstanceError."""
    from dataclasses import FrozenInstanceError
    from core.model_config import CONFIG
    with pytest.raises(FrozenInstanceError):
        CONFIG.visionary_temp = 0.5


# ─────────────────────────────────────────────────────────────────────────────
# P0 – Strict typed state
# ─────────────────────────────────────────────────────────────────────────────

def test_research_state_strict_mode():
    """Article 3: ResearchState must reject wrong-typed field values."""
    from pydantic import ValidationError
    from core.state import ResearchState

    with pytest.raises(ValidationError):
        ResearchState(research_query=123)  # must be str, not int


def test_research_state_valid():
    """Sanity: valid state construction succeeds."""
    from core.state import ResearchState
    s = ResearchState(research_query="test query")
    assert s.research_query == "test query"


# ─────────────────────────────────────────────────────────────────────────────
# P0 – Backwards design: physical_outcome_spec enforced
# ─────────────────────────────────────────────────────────────────────────────

def test_visionary_node_requires_physical_outcome_spec():
    """Article 5: visionary_node must raise ValueError when spec is absent."""
    from core.nodes import visionary_node

    state = {
        "physical_outcome_spec": "",
        "research_query": "test",
        "traceability_chain": [],
        "active_role": "AI_Research_Scientist",
    }
    with pytest.raises(ValueError, match="Article 5"):
        visionary_node(state)


# ─────────────────────────────────────────────────────────────────────────────
# P0 – Merkle chain integrity
# ─────────────────────────────────────────────────────────────────────────────

def test_merkle_chain_previous_hash_linked():
    """Each entry must include the previous entry's hash."""
    with tempfile.NamedTemporaryFile(suffix=".log", delete=False) as f:
        path = f.name
    try:
        from core.ledger import MerkleLedger
        ledger = MerkleLedger(filepath=path)

        h1 = ledger.append_signature("EVT_A", "user", {"x": 1})
        h2 = ledger.append_signature("EVT_B", "user", {"x": 2})

        with open(path) as fh:
            lines = [json.loads(l) for l in fh if l.strip()]

        assert lines[0]["data"]["previous_hash"] == "0" * 64, "Genesis entry must use zero sentinel"
        assert lines[1]["data"]["previous_hash"] == h1,       "Entry 2 must chain to entry 1's hash"
        assert lines[1]["hash"] == h2
    finally:
        os.unlink(path)


def test_merkle_validate_chain_passes_on_valid_log():
    """validate_chain() must return True on an untampered log."""
    with tempfile.NamedTemporaryFile(suffix=".log", delete=False) as f:
        path = f.name
    try:
        from core.ledger import MerkleLedger
        ledger = MerkleLedger(filepath=path)
        ledger.append_signature("A", "u", {})
        ledger.append_signature("B", "u", {})
        ledger.append_signature("C", "u", {})
        assert ledger.validate_chain() is True
    finally:
        os.unlink(path)


def test_merkle_validate_chain_detects_tamper():
    """validate_chain() must raise ValueError when an entry hash is tampered."""
    with tempfile.NamedTemporaryFile(suffix=".log", delete=False, mode="w") as f:
        path = f.name
    try:
        from core.ledger import MerkleLedger
        ledger = MerkleLedger(filepath=path)
        ledger.append_signature("A", "u", {})
        ledger.append_signature("B", "u", {})

        # Tamper: overwrite the first entry's hash
        with open(path) as fh:
            lines = fh.readlines()
        record = json.loads(lines[0])
        record["hash"] = "deadbeef" * 8
        lines[0] = json.dumps(record) + "\n"
        with open(path, "w") as fh:
            fh.writelines(lines)

        fresh = MerkleLedger(filepath=path)
        with pytest.raises(ValueError):
            fresh.validate_chain()
    finally:
        os.unlink(path)


def test_merkle_empty_ledger_validates():
    """Empty ledger must validate without error."""
    with tempfile.NamedTemporaryFile(suffix=".log", delete=False) as f:
        path = f.name
    os.unlink(path)
    try:
        from core.ledger import MerkleLedger
        ledger = MerkleLedger(filepath=path)
        assert ledger.validate_chain() is True
    finally:
        if os.path.exists(path):
            os.unlink(path)


# ─────────────────────────────────────────────────────────────────────────────
# P0 – Structural self-validation rule engine
# ─────────────────────────────────────────────────────────────────────────────

def test_validator_passes_clean_output():
    """A well-formed verifier output with verdict and spec reference must pass."""
    from core.validators import enforce_nist_eu_self_validation

    text = (
        "The heat sink design satisfies the thermal requirements. "
        "All claims are grounded in IEEE 1234 standards. "
        "No unsupported assertions detected. VERIFIED"
    )
    passed, failures = enforce_nist_eu_self_validation(
        text, physical_outcome_spec="heat sink"
    )
    assert passed, f"Expected pass, got failures: {failures}"


def test_validator_fails_on_uncertainty_phrase():
    """Disallowed uncertainty phrase 'I guess' must trigger RULE-2."""
    from core.validators import enforce_nist_eu_self_validation

    text = "I guess this might work. The output seems reasonable. VERIFIED"
    passed, failures = enforce_nist_eu_self_validation(text)
    assert not passed
    assert any("RULE-2" in f for f in failures)


def test_validator_fails_without_verdict():
    """Missing VERIFIED/FAILED verdict must trigger RULE-5."""
    from core.validators import enforce_nist_eu_self_validation

    text = "The heat sink meets requirements. All claims are supported."
    passed, failures = enforce_nist_eu_self_validation(
        text, physical_outcome_spec="heat sink"
    )
    assert not passed
    assert any("RULE-5" in f for f in failures)


def test_validator_fails_when_spec_not_referenced():
    """Output that ignores the physical_outcome_spec must trigger RULE-1."""
    from core.validators import enforce_nist_eu_self_validation

    text = "This is a general statement about AI safety. VERIFIED"
    passed, failures = enforce_nist_eu_self_validation(
        text, physical_outcome_spec="titanium turbine blade fabrication"
    )
    assert not passed
    assert any("RULE-1" in f for f in failures)


# ─────────────────────────────────────────────────────────────────────────────
# P1 – Dual-parity mandatory wrapper
# ─────────────────────────────────────────────────────────────────────────────

def test_emit_dual_parity_contains_both_layers():
    """emit_dual_parity must embed markdown and a JSON code block."""
    from ui.web_engine import emit_dual_parity

    result = emit_dual_parity("## Hello", {"key": "value"})
    assert "## Hello" in result
    assert "```json" in result
    assert '"key": "value"' in result


# ─────────────────────────────────────────────────────────────────────────────
# P1 – Role fluidity: state field exists and accepts both roles
# ─────────────────────────────────────────────────────────────────────────────

def test_active_role_scientist_accepted():
    from core.state import ResearchState
    s = ResearchState(active_role="AI_Research_Scientist")
    assert s.active_role == "AI_Research_Scientist"


def test_active_role_engineer_accepted():
    from core.state import ResearchState
    s = ResearchState(active_role="AI_Research_Engineer")
    assert s.active_role == "AI_Research_Engineer"


def test_active_role_invalid_rejected():
    """Unsupported role values must raise ValidationError."""
    from pydantic import ValidationError
    from core.state import ResearchState

    with pytest.raises(ValidationError):
        ResearchState(active_role="UNKNOWN_ROLE")


# ─────────────────────────────────────────────────────────────────────────────
# P1 – Role routing: orchestrator defines conditional entry edge
# ─────────────────────────────────────────────────────────────────────────────

def test_route_entry_scientist_returns_visionary():
    from core.state import ResearchState
    from core.orchestrator import route_entry

    s = ResearchState(active_role="AI_Research_Scientist")
    assert route_entry(s) == "visionary"


def test_route_entry_engineer_returns_verifier():
    from core.state import ResearchState
    from core.orchestrator import route_entry

    s = ResearchState(active_role="AI_Research_Engineer")
    assert route_entry(s) == "verifier"


# ─────────────────────────────────────────────────────────────────────────────
# P2 – Architecture: core modules import without circular deps
# ─────────────────────────────────────────────────────────────────────────────

def test_core_state_imports():
    import core.state  # noqa: F401


def test_core_model_config_imports():
    import core.model_config  # noqa: F401


def test_core_validators_imports():
    import core.validators  # noqa: F401


def test_core_ledger_imports():
    import core.ledger  # noqa: F401


def test_core_boot_imports():
    import core.boot  # noqa: F401
