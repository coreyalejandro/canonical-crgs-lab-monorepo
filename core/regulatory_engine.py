"""
core/regulatory_engine.py — Regulatory Compliance Engine

Phase 10 Build Contract — Section II.  The final microservice.

Analyzes the physical BOM and patent claims from Phases 8–9, cross-references
them against an ingested database of federal and international regulatory codes,
and generates the compliance testing protocol the alpha prototype must complete
before legal consumer market entry.

Regulatory frameworks addressed:
  - ISO 9001   — Quality Management Systems
  - ISO 13485  — Medical Device Quality Management (if applicable)
  - FDA 21 CFR — Food, Drug, and Cosmetic Act (Class I/II/III devices)
  - FCC Part 15 — Radio Frequency emissions (electronic devices)
  - CE Marking — European Conformity (all EU market products)
  - UN 38.3    — Battery transport and safety testing
  - UL 94      — Flammability of Plastic Materials
  - RoHS       — Restriction of Hazardous Substances (EU/UK)

Constitutional contract:
  - The compliance pathway is determined by the LLM at temperature=0.0 —
    deterministic, reproducible, auditable.
  - The output is strict JSON validated before writing.
  - regulatory_assets is written to state so compile_pdf can include the
    compliance roadmap in the terminal dossier.
  - The engine never silently produces an empty pathway — if the LLM
    output cannot be parsed as JSON, a structured fallback is used and
    flagged with a warning so the dossier always has a compliance section.

Pipeline position:
    fabricate → [regulate] → compile_pdf → END
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from langchain_core.prompts import PromptTemplate

from core.llm_binding import get_deterministic_generator


# ── Constants ─────────────────────────────────────────────────────────────────

DEFAULT_OUTPUT_DIR = os.getenv("REGULATORY_OUTPUT_DIR", "./output/regulatory")

# ── Prompts ───────────────────────────────────────────────────────────────────

_REGULATORY_PROMPT = PromptTemplate.from_template(
    "You are a senior regulatory affairs specialist with expertise in FDA, FCC, "
    "CE, ISO, and international product safety standards.\n\n"
    "Analyze the following product framework and Bill of Materials. "
    "Output ONLY valid JSON (no markdown fences, no commentary) with exactly "
    "these top-level keys:\n"
    "  'applicable_standards': list of objects with 'standard', 'body', 'scope'\n"
    "  'testing_protocols': list of objects with 'test_name', 'standard_ref', "
    "'estimated_cost_usd', 'estimated_weeks'\n"
    "  'market_entry_sequence': ordered list of strings describing the "
    "go-to-market compliance steps\n"
    "  'estimated_total_compliance_cost_usd': number\n"
    "  'estimated_total_weeks': number\n\n"
    "Product Framework:\n{hypothesis}\n\n"
    "Bill of Materials:\n{bom_data}\n\n"
    "Patent Claims (first 500 chars):\n{patent_claims}"
)

# ── Regulatory Engine ─────────────────────────────────────────────────────────

class RegulatoryEngine:
    """
    Maps a physical product against federal and international compliance standards,
    then generates an actionable pre-market testing protocol.
    """

    def __init__(self, output_dir: str = DEFAULT_OUTPUT_DIR) -> None:
        self.output_dir    = Path(output_dir)
        self.compliance_llm = get_deterministic_generator()
        self.output_dir.mkdir(parents=True, exist_ok=True)

    # ── Pathway determination ─────────────────────────────────────────────────

    def determine_regulatory_pathway(
        self,
        bom_data: dict[str, Any],
        hypothesis: str,
        patent_claims: str = "",
    ) -> dict[str, Any]:
        """
        Use the deterministic LLM to map the product against applicable
        regulatory standards.

        Returns a validated compliance pathway dict.
        Falls back to a structured minimum payload on JSON parse failure.
        """
        print("[regulatory] Scanning federal/international regulatory pathways...")

        chain  = _REGULATORY_PROMPT | self.compliance_llm
        result = chain.invoke({
            "hypothesis":    hypothesis,
            "bom_data":      json.dumps(bom_data, indent=2),
            "patent_claims": patent_claims[:500],
        })

        raw = result.hypothesis if hasattr(result, "hypothesis") else str(result)
        raw = raw.strip()
        if raw.startswith("```"):
            raw = raw.split("\n", 1)[-1].rsplit("```", 1)[0].strip()

        try:
            pathway = json.loads(raw)
            # Validate required keys
            for key in ("applicable_standards", "testing_protocols",
                        "market_entry_sequence"):
                if key not in pathway:
                    raise ValueError(f"Missing required key: {key!r}")
            print(
                f"[regulatory] Pathway determined — "
                f"{len(pathway.get('applicable_standards', []))} standards, "
                f"{len(pathway.get('testing_protocols', []))} tests."
            )
            return pathway

        except (json.JSONDecodeError, ValueError) as exc:
            print(f"[regulatory] WARNING: LLM output not valid JSON ({exc}). Using structured fallback.")
            return {
                "applicable_standards": [
                    {"standard": "ISO 9001:2015", "body": "ISO",
                     "scope": "Quality management — baseline for all manufactured products"},
                    {"standard": "CE Marking",    "body": "EU Commission",
                     "scope": "EU market entry — mandatory for all electronic/physical products"},
                    {"standard": "FCC Part 15",   "body": "FCC",
                     "scope": "RF emissions — required for all electronic devices sold in the US"},
                    {"standard": "RoHS 3 (2015/863/EU)", "body": "EU",
                     "scope": "Hazardous substance restriction for EU/UK market entry"},
                ],
                "testing_protocols": [
                    {"test_name": "ISO 9001 QMS Audit",
                     "standard_ref": "ISO 9001:2015",
                     "estimated_cost_usd": 5000, "estimated_weeks": 4},
                    {"test_name": "FCC Part 15 RF Emissions",
                     "standard_ref": "47 CFR Part 15",
                     "estimated_cost_usd": 8000, "estimated_weeks": 6},
                    {"test_name": "CE Technical File + Declaration of Conformity",
                     "standard_ref": "EU 2019/1782",
                     "estimated_cost_usd": 12000, "estimated_weeks": 8},
                    {"test_name": "RoHS Material Analysis",
                     "standard_ref": "EU 2015/863",
                     "estimated_cost_usd": 3000, "estimated_weeks": 3},
                ],
                "market_entry_sequence": [
                    "1. Complete ISO 9001 QMS audit and correct non-conformances",
                    "2. Submit prototype for FCC Part 15 RF emissions testing",
                    "3. Prepare CE Technical File and Declaration of Conformity",
                    "4. Commission RoHS material analysis from accredited lab",
                    "5. Compile regulatory dossier and engage notified body if required",
                    "6. File for market authorization and register product",
                ],
                "estimated_total_compliance_cost_usd": 28000,
                "estimated_total_weeks": 16,
                "_fallback": True,
                "_fallback_reason": str(exc),
            }

    # ── Dossier generation ────────────────────────────────────────────────────

    def generate_compliance_dossier(
        self, compliance_pathway: dict[str, Any]
    ) -> str:
        """
        Write the actionable testing protocol to
        ./output/regulatory/compliance_testing_protocol.json.

        Returns the path to the written file.
        """
        print("[regulatory] Drafting pre-market regulatory testing protocols...")

        dossier_path = self.output_dir / "compliance_testing_protocol.json"
        dossier_path.write_text(json.dumps(compliance_pathway, indent=4))

        total_cost  = compliance_pathway.get("estimated_total_compliance_cost_usd", "?")
        total_weeks = compliance_pathway.get("estimated_total_weeks", "?")
        print(
            f"[regulatory] Compliance protocol locked: {dossier_path} "
            f"(est. ${total_cost:,} over {total_weeks} weeks)"
            if isinstance(total_cost, (int, float))
            else f"[regulatory] Compliance protocol locked: {dossier_path}"
        )
        return str(dossier_path)


# ── LangGraph node ────────────────────────────────────────────────────────────

def regulatory_node(state: dict) -> dict:
    """
    LangGraph node: BOM + hypothesis + patent claims → compliance pathway JSON.

    Pipeline position: fabricate → [regulate] → compile_pdf → END

    Reads commercial_blueprint and hypothesis_payload from state.
    Returns state with regulatory_assets added.
    """
    print("[regulatory] Initiating Regulatory Compliance and GTM Phase...")

    engine       = RegulatoryEngine()
    blueprint    = state.get("commercial_blueprint") or {}
    payload      = state.get("hypothesis_payload")   or {}
    bom          = blueprint.get("bill_of_materials") or {}
    hypothesis   = payload.get("hypothesis", payload.get("hypothesis_title", ""))
    patent_claims = blueprint.get("patent_claims", "")

    pathway = engine.determine_regulatory_pathway(bom, hypothesis, patent_claims)
    dossier = engine.generate_compliance_dossier(pathway)

    print("[regulatory] Regulatory compliance pathway and GTM dossier complete.")

    return {
        **state,
        "regulatory_assets": {
            "compliance_pathway_data": pathway,
            "dossier_path":            dossier,
        },
    }
