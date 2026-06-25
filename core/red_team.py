"""
core/red_team.py — Adversarial Red Team Evaluator

Section II of the Phase 3 Build Contract.

The RedTeamEvaluator forces the Judge LLM into an explicitly adversarial
stance.  It is programmatically required to:

  1. Query the Neo4j Knowledge Graph for [:CONTRADICTS] relationships
     relevant to the hypothesis under evaluation.
  2. Bind the LLM to an aggressive debunking prompt at temperature=0.0.
  3. Accept only "SURVIVED" as a passing verdict — any other output raises
     AdversarialVetoError and returns the payload to the revision loop.

Constitutional contract: the Red Team step is NON-OPTIONAL.  A payload
that has not passed adversarial review MUST NOT be forwarded to the
LaTeX compiler.  This is enforced by the LangGraph state machine routing
condition in core/graph_builder.py (Phase 4).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from langchain_core.prompts import PromptTemplate

from core.llm_binding import get_deterministic_generator, HypothesisPayload


# ── Custom exception ──────────────────────────────────────────────────────────

class AdversarialVetoError(Exception):
    """
    Raised when the Red Team attack successfully identifies a structural flaw
    in the hypothesis payload.  The message contains the exact flaw text
    returned by the adversarial LLM so the revision loop can act on it.
    """


# ── Attack result dataclass ───────────────────────────────────────────────────

@dataclass
class RedTeamResult:
    status: str                        # "verified_and_stress_tested" | "vetoed"
    contradictions_found: int = 0
    flaw: str | None = None
    raw_verdict: str = ""
    attack_metadata: dict = field(default_factory=dict)


# ── Adversarial prompt ────────────────────────────────────────────────────────

_ATTACK_PROMPT = PromptTemplate.from_template(
    "You are a Tier-1 academic peer reviewer. Your sole directive is to DEBUNK the "
    "following hypothesis using only the contradictory evidence supplied.\n\n"
    "Hypothesis:\n{hypothesis}\n\n"
    "Claims under review:\n{claims}\n\n"
    "Contradictory evidence from the Knowledge Graph:\n{contradictions}\n\n"
    "Rules:\n"
    "- If the hypothesis withstands all contradictory evidence, output exactly: SURVIVED\n"
    "- If you identify a structural flaw, output exactly: FLAW: <one-sentence description>\n"
    "- Do not output anything else."
)


# ── Red Team Evaluator ────────────────────────────────────────────────────────

class RedTeamEvaluator:
    """
    Executes a deterministic adversarial attack on a verified HypothesisPayload.

    Usage:
        driver = GraphDatabase.driver(uri, auth=(user, password))
        with driver.session() as session:
            evaluator = RedTeamEvaluator(neo4j_session=session)
            result = evaluator.execute_attack(payload)
    """

    def __init__(self, neo4j_session: Any) -> None:
        self.db = neo4j_session
        # Adversarial LLM is the same deterministic generator — temperature=0.0.
        # The prompt forces the adversarial role; the temperature prevents drift.
        self.adversarial_llm = get_deterministic_generator()

    # ── Private helpers ───────────────────────────────────────────────────────

    def _fetch_contradictions(self, keyword: str) -> list[dict]:
        """
        Retrieve all [:CONTRADICTS] relationships from Neo4j whose claim text
        contains the given keyword.  Returns an empty list if the graph has no
        contradictory evidence — this is a valid (strong) result for the payload.
        """
        query = (
            "MATCH (p:Paper)-[:CONTRADICTS]->(c:Claim) "
            "WHERE toLower(c.text) CONTAINS toLower($keyword) "
            "RETURN p.id AS paper_id, p.title AS paper_title, c.text AS claim_text"
        )
        result = self.db.run(query, keyword=keyword)
        return result.data()

    @staticmethod
    def _extract_keyword(payload: HypothesisPayload | dict) -> str:
        """
        Pull the most discriminating keyword from the hypothesis sentence.
        Uses the longest word as a simple heuristic; Phase 4 will replace
        this with a proper keyphrase extractor.
        """
        hypothesis_text: str = (
            payload.hypothesis if isinstance(payload, HypothesisPayload)
            else payload.get("hypothesis", "")
        )
        words = [w.strip(".,;:()") for w in hypothesis_text.split() if len(w) > 5]
        return max(words, key=len) if words else hypothesis_text[:32]

    # ── Public API ────────────────────────────────────────────────────────────

    def execute_attack(
        self,
        hypothesis_payload: HypothesisPayload | dict,
    ) -> RedTeamResult:
        """
        Execute a deterministic adversarial attack on the verified hypothesis.

        Steps:
          1. Extract keyword from hypothesis text.
          2. Query Neo4j for [:CONTRADICTS] relationships.
          3. Bind adversarial LLM to the attack prompt.
          4. Parse verdict: "SURVIVED" passes; "FLAW: ..." raises AdversarialVetoError.

        Returns:
            RedTeamResult with status="verified_and_stress_tested" on pass.

        Raises:
            AdversarialVetoError: if the hypothesis fails the adversarial review.
        """
        # Normalise input — accept both Pydantic model and plain dict
        if isinstance(hypothesis_payload, HypothesisPayload):
            hypothesis = hypothesis_payload.hypothesis
            claims = hypothesis_payload.claims
        else:
            hypothesis = hypothesis_payload.get("hypothesis", "")
            claims = hypothesis_payload.get("claims", [])

        keyword = self._extract_keyword(hypothesis_payload)

        # 1. Retrieve contradictory evidence (may be empty — that is valid)
        contradictions = self._fetch_contradictions(keyword)
        contradiction_text = (
            "\n".join(
                f"- [{r['paper_title']}] {r['claim_text']}" for r in contradictions
            )
            if contradictions
            else "No contradictory evidence found in Knowledge Graph."
        )

        # 2. Build attack chain — prompt | structured LLM
        chain = _ATTACK_PROMPT | self.adversarial_llm

        # 3. Invoke — temperature=0.0 guarantees deterministic verdict
        raw_result = chain.invoke({
            "hypothesis": hypothesis,
            "claims": "\n".join(f"- {c}" for c in claims),
            "contradictions": contradiction_text,
        })

        # Extract text regardless of whether result is a string or Pydantic model
        verdict_text: str = (
            raw_result if isinstance(raw_result, str)
            else getattr(raw_result, "hypothesis", str(raw_result))
        )

        # 4. Parse verdict
        if "SURVIVED" in verdict_text.upper():
            return RedTeamResult(
                status="verified_and_stress_tested",
                contradictions_found=len(contradictions),
                raw_verdict=verdict_text,
                attack_metadata={"keyword": keyword},
            )

        # Extract flaw description if present
        flaw = verdict_text.replace("FLAW:", "").strip() if "FLAW" in verdict_text.upper() else verdict_text

        raise AdversarialVetoError(
            f"Adversarial Veto: Hypothesis failed Red Team attack.\n"
            f"Keyword searched: '{keyword}'\n"
            f"Contradictions found: {len(contradictions)}\n"
            f"Flaw identified: {flaw}"
        )
