"""
core/boot.py — Cryptographic TLC ToCA Boot Integrity

Phase 13 Build Contract — Section I.

The full Living Constitution text is the literal source of law.
Its SHA-256 is pre-compiled into this module. Any mutation of the
text hard-crashes the system before any execution can occur.
"""

import hashlib
import sys

# === THE LIVING CONSTITUTION — FULL TEXT (IMMUTABLE) ===
TLC_TOCA_CANON = """
PREAMBLE: The Living Constitution (TLC) is a platform-agnostic, accessibility-first
constitutional governance-as-code system. It operates under the dual purpose of ensuring
strict compliance with Anthropic, NIST AI RMF, and EU AI Act frameworks, while
simultaneously engineering narrative- and neurodivergent-first AI architectures.

ARTICLE 1: MODULARITY MANDATE — All logic shall be strictly separated into modules
performing one function. Monolithic designs are forbidden.

ARTICLE 2: RECURSIVE SELF-VALIDATION — The system must apply its own verification
frameworks to its own outputs. It eats its own dogfood.

ARTICLE 3: CLEAN CODE STANDARD — All code must be 100% deterministic, strictly typed,
and cleanly structured.

ARTICLE 4: THE BLIND MAN'S TEST — All documentation and output must assume zero prior
knowledge and be unambiguous when read aloud.

ARTICLE 5: BACKWARDS DESIGN — All reasoning must be anchored to a concrete physical
outcome specification before generative work begins.

ARTICLE 6: DUAL-PARITY OUTPUT — Every human-legible output must be accompanied by a
machine-actionable (JSON/YAML) equivalent.

ARTICLE 7: NEURODIVERGENT-FIRST UI/UX — Interfaces must reduce cognitive load via
explicit state signaling, active/passive anchors, and high-contrast logic.

ARTICLE 8: HYBRID-FIRST GOVERNANCE — Autonomous loops must be cryptographically frozen
before high-consequence transitions until human authorization is given.

ARTICLE 9: HYBRID ROLE FLUIDITY — The system shall fluidly transition between
Research Scientist (theory) and Research Engineer (execution) under Human PI control.

ARTICLE 10: MIXTURE OF EXPERTS PARADIGM — The system recognizes machine hallucinations
as lateral ideation and pairs high-temperature models with zero-temperature
models to mirror human cognitive equilibrium.
"""

# Pre-computed at authorship time — recompute with:
#   python3 -c "import hashlib; print(hashlib.sha256(open('core/boot.py').read().split('TLC_TOCA_CANON')[1].split('\"\"\"')[1].encode()).hexdigest())"
# Pre-computed at Phase 14 ratification — DO NOT RECOMPUTE AT RUNTIME.
# Any mutation of TLC_TOCA_CANON above will produce a different runtime hash
# and enforce_cryptographic_boot() will call sys.exit(1).
CONSTITUTION_HASH = "30ac14272f29eee0dbb7a7326520376b2d4a1f44be6ab6fb8281cbbf7e313eef"


def enforce_cryptographic_boot() -> str:
    """
    Hard-crash if TLC_TOCA_CANON has been mutated since Phase 14 ratification.
    Also validates the Merkle audit ledger chain before any execution.
    """
    live_hash = hashlib.sha256(TLC_TOCA_CANON.encode("utf-8")).hexdigest()
    if live_hash != CONSTITUTION_HASH:
        sys.stderr.write(
            f"FATAL: TLC ToCA integrity violated.\n"
            f"  Expected: {CONSTITUTION_HASH}\n"
            f"  Got:      {live_hash}\n"
            "System halted.\n"
        )
        sys.exit(1)

    # Validate Merkle ledger chain on every boot
    from core.ledger import MerkleLedger  # local import avoids circular at module load
    try:
        MerkleLedger().validate_chain()
    except ValueError as exc:
        sys.stderr.write(f"FATAL: Audit ledger chain integrity violated.\n  {exc}\nSystem halted.\n")
        sys.exit(1)

    print(f"✅ TLC ToCA Cryptographically Verified [{live_hash[:16]}…]. Ledger chain intact. Booting Cognitive Boardroom…")
    return live_hash
