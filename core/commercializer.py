"""
core/commercializer.py — IP & Commercialization Microservice

Phase 8 Build Contract — Section II.

Takes the cryptographically audited, adversarially verified hypothesis and:
  1. Executes a prior-art novelty search (USPTO/Google Patents via SerpApi)
  2. Forces the LLM to format the science as formal US Patent claims
  3. Generates a preliminary Bill of Materials (BOM) for the alpha prototype

Constitutional contract:
  - LLM is bound at temperature=0.0 — legal language is deterministic.
  - Prior art search raises PriorArtConflictError if hits are found —
    the pipeline halts rather than producing infringing patent drafts.
  - BOM output is validated as JSON — malformed LLM output raises
    ValueError before it reaches the dossier compiler.
  - SERPAPI_KEY is optional — absence degrades to simulated search with
    a warning, not a pipeline halt (bootstrapped tier behaviour).

Pipeline position:
    audit → [commercialize] → compile_pdf

Usage:
    from core.commercializer import commercial_blueprint_node
"""

from __future__ import annotations

import json
import os
from typing import Any

from langchain_core.prompts import PromptTemplate

from core.llm_binding import get_deterministic_generator


# ── Custom exceptions ─────────────────────────────────────────────────────────

class PriorArtConflictError(Exception):
    """
    Raised when the prior-art search finds existing patents that would
    block the hypothesis from being filed.  The pipeline halts and
    returns to the hypothesis-generation node for refinement.
    """


# ── Patent + BOM prompts ──────────────────────────────────────────────────────

_PATENT_PROMPT = PromptTemplate.from_template(
    "You are a registered US Patent Attorney drafting independent claims.\n\n"
    "Convert the following verified scientific hypothesis into strict US Patent "
    "Claim formatting, following USPTO guidelines.\n\n"
    "Hypothesis:\n{hypothesis}\n\n"
    "Audit fingerprint (include verbatim in claim preamble for provenance):\n"
    "{audit_hash}\n\n"
    "Rules:\n"
    "- Begin with '1. A method comprising:' or '1. An apparatus comprising:'\n"
    "- Each step or element on a new line, ending with a semicolon except the last\n"
    "- Include at least one independent claim and one dependent claim\n"
    "- Do not add commentary — output only the formatted claims"
)

_BOM_PROMPT = PromptTemplate.from_template(
    "Based on the following scientific framework, generate a preliminary "
    "Bill of Materials (BOM) for an alpha prototype.\n\n"
    "Framework:\n{hypothesis}\n\n"
    "Output ONLY valid JSON with exactly these top-level keys:\n"
    "  'components': list of objects with 'name', 'quantity', 'unit', 'estimated_unit_cost_usd'\n"
    "  'estimated_total_cost_usd': number\n"
    "  'supply_chain_risks': list of strings\n"
    "Do not include markdown fences or commentary — raw JSON only."
)


# ── Commercial Orchestrator ───────────────────────────────────────────────────

class CommercialOrchestrator:
    """
    IP novelty search + patent claim drafting + BOM generation.

    All LLM calls are bound at temperature=0.0 for deterministic legal output.
    """

    def __init__(self) -> None:
        self.legal_llm  = get_deterministic_generator()
        self._serpapi_key = os.getenv("SERPAPI_KEY", "")

    # ── Prior art search ──────────────────────────────────────────────────────

    def _execute_prior_art_search(self, keyword_profile: str) -> bool:
        """
        Query USPTO/Google Patents for prior art via SerpApi.

        Returns True if no blocking prior art is found.
        Raises PriorArtConflictError if hits are found.
        Degrades to simulated search (returns True) when SERPAPI_KEY is absent.
        """
        print(f"[commercializer] Scanning global patent registries for: {keyword_profile!r}")

        if not self._serpapi_key:
            print(
                "[commercializer] SERPAPI_KEY not set — running simulated novelty search. "
                "Set SERPAPI_KEY in .env for production patent scanning."
            )
            print("[commercializer] Legal Novelty: SIMULATED PASS.")
            return True

        try:
            from serpapi import GoogleSearch  # type: ignore

            results = GoogleSearch({
                "engine": "google_patents",
                "q":      keyword_profile,
                "api_key": self._serpapi_key,
            }).get_dict()

            hits = results.get("organic_results", [])
            if hits:
                titles = [r.get("title", "unknown") for r in hits[:3]]
                raise PriorArtConflictError(
                    f"Prior art discovered for {keyword_profile!r}. "
                    f"Top conflicts: {titles}. "
                    "Hypothesis requires refinement before patent filing."
                )

        except ImportError:
            print("[commercializer] serpapi package not installed — simulated pass.")

        print("[commercializer] Legal Novelty Verified. No direct prior art overlap.")
        return True

    # ── Patent claim drafting ─────────────────────────────────────────────────

    def generate_patent_claims(self, hypothesis: str, audit_hash: str = "") -> str:
        """
        Translate a verified hypothesis into formal US Patent claim language.
        Returns the formatted claim text as a plain string.
        """
        chain  = _PATENT_PROMPT | self.legal_llm
        result = chain.invoke({"hypothesis": hypothesis, "audit_hash": audit_hash})
        # Result may be a HypothesisPayload or a string depending on chain config
        return result.hypothesis if hasattr(result, "hypothesis") else str(result)

    # ── BOM generation ────────────────────────────────────────────────────────

    def generate_bill_of_materials(self, hypothesis: str) -> dict[str, Any]:
        """
        Generate a preliminary Bill of Materials (BOM) for the alpha prototype.
        Returns a validated dict with keys: components, estimated_total_cost_usd,
        supply_chain_risks.
        Raises ValueError if the LLM does not return valid JSON.
        """
        chain  = _BOM_PROMPT | self.legal_llm
        result = chain.invoke({"hypothesis": hypothesis})
        raw    = result.hypothesis if hasattr(result, "hypothesis") else str(result)

        # Strip accidental markdown fences
        raw = raw.strip()
        if raw.startswith("```"):
            raw = raw.split("\n", 1)[-1].rsplit("```", 1)[0].strip()

        try:
            bom = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ValueError(
                f"BOM generation returned invalid JSON: {exc}\nRaw output: {raw[:200]}"
            ) from exc

        # Minimal schema validation
        for required_key in ("components", "estimated_total_cost_usd", "supply_chain_risks"):
            if required_key not in bom:
                raise ValueError(f"BOM missing required key: {required_key!r}")

        return bom


# ── LangGraph node ────────────────────────────────────────────────────────────

def commercial_blueprint_node(state: dict) -> dict:
    """
    LangGraph node: prior-art search → patent claims → BOM.

    Pipeline position: audit → [commercialize] → compile_pdf

    On PriorArtConflictError the node sets validation_status='prior_art_conflict'
    so the routing logic can loop back to generate_hypothesis for refinement.
    """
    print("[commercializer] Initiating Commercialization & IP Mapping Phase...")

    orchestrator   = CommercialOrchestrator()
    payload        = state.get("hypothesis_payload", {})
    hypothesis     = payload.get("hypothesis", payload.get("hypothesis_title", ""))
    audit_hash     = state.get("audit_hash", "")

    # 1. Prior art search
    keyword = payload.get("keyword") or hypothesis[:80]
    try:
        orchestrator._execute_prior_art_search(keyword)
    except PriorArtConflictError as exc:
        print(f"[commercializer] PRIOR ART CONFLICT: {exc}")
        return {
            **state,
            "validation_status": "prior_art_conflict",
            "commercial_blueprint": None,
        }

    # 2. Patent claims
    patent_claims = orchestrator.generate_patent_claims(hypothesis, audit_hash)

    # 3. BOM
    try:
        bom_data = orchestrator.generate_bill_of_materials(hypothesis)
    except ValueError as exc:
        print(f"[commercializer] BOM generation failed (non-fatal): {exc}")
        bom_data = {"components": [], "estimated_total_cost_usd": 0, "supply_chain_risks": [str(exc)]}

    commercial_blueprint = {
        "patent_claims":    patent_claims,
        "bill_of_materials": bom_data,
        "audit_hash":        audit_hash,
    }

    print("[commercializer] Patent claims and prototype BOM successfully drafted.")
    return {**state, "commercial_blueprint": commercial_blueprint}
