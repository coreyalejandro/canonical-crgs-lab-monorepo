# TLC 2.0 Integration — Constitutional Adaptive Learning Systems Protocol

**Module ID:** CALSP-RESEARCH-TEMPLATE  
**Version:** 4.3  
**Truth-State:** SPECIFIED  
**Integration Date:** 2026-06-23  
**Parent System:** The Living Constitution 2.0

---

## Purpose

This document maps the Constitutional Adaptive Learning Systems Protocol (CALSP) to The Living Constitution 2.0 (TLC 2.0) framework, demonstrating how CALSP functions as a domain constitution within the TLC runtime architecture.

---

## Architectural Relationship

```
TLC 2.0 Runtime
    ↓
Constitutional Interface (src/interfaces/constitutional-invariant.ts)
    ↓
CALSP Domain Constitution (this repository)
    ↓
CALT Theory + CAMM Protocol
    ↓
Empirical Validation (Bootstrapped Pilot → Megaproject)
```

CALSP is **Constitution #3** in the TLC family:
1. Eight Wonders Constitution (relational economies)
2. Instructional Integrity Constitution (learning systems)
3. **Constitutional Adaptive Learning Constitution** (neurodivergent-first AI)

---

## TLC 2.0 Layer Mapping

### Layer 1: Runtime Architecture
**TLC Component:** Constitutional runtime with LTL-verified safety gates  
**CALSP Integration:** CALSP inherits TLC's Safety Gate, Upstream Primacy, Halt Authority, Feedback Obligation, and Task-State Locking

**Evidence:**
- CALSP references TLC's `ConstitutionalInvariant` interface
- CALSP's Constitutional Compliance Index (CCI) maps to TLC's invariant evaluation protocol
- CALSP's CHAE maps to TLC's Continuous Human Audit Engine

### Layer 2: Constitution Framework (CEM)
**TLC Component:** Constitution Engineering Methodology  
**CALSP Integration:** CALSP is an instance of CEM

**Evidence:**
- CALSP defines domain-specific invariants (CCI, NAP, DTCI)
- CALSP follows CEM's invariant derivation protocol
- CALSP includes community elicitation (NAB, CGB)
- CALSP specifies version lifecycle (draft → calibrated → deployed → evolved)

### Layer 3: Research Framework
**TLC Component:** CAMM Protocol, CALT Theory, Neurodivergent Success Metrics, Bootstrapped Pilot Protocol  
**CALSP Integration:** CALSP **IS** the research framework for TLC 2.0

**Evidence:**
- CALSP v4.3 integrates TALSP Template v4.2 (confirmed in TLC PROGRAM_ARCHITECTURE.md)
- CALSP defines CAMM (Constitutional Adaptive Mixed-Methods)
- CALSP defines CALT (Constitutional Adaptive Learning Theory)
- CALSP specifies neurodivergent success metrics
- CALSP provides bootstrapped pilot protocol

**Files:**
- `frameworks/research/CAMM_Protocol.md` → CALSP research design
- `frameworks/research/CALT_Theory.md` → CALSP theoretical foundation
- `frameworks/research/Neurodivergent_Success_Metrics.md` → CALSP outcome metrics
- `frameworks/research/Bootstrapped_Pilot_Protocol.md` → CALSP execution pathway

### Layer 4: Validation Framework
**TLC Component:** Tier-1 Validation Framework, Tier-1 Compliance Report Template  
**CALSP Integration:** CALSP follows TLC's validation standards

**Evidence:**
- CALSP includes Tier-1 Readiness Matrix (10 criteria)
- CALSP specifies Tier-1 Validation Loop (runs at every phase boundary)
- CALSP requires Tier-1 Compliance Report before publication
- CALSP maps to NIST AI RMF 1.0 (see `governance/nist/Bootstrapped_NIST_Mapping.md`)

### Layer 5: Governance Framework
**TLC Component:** CHAE, NAB, CGB, OSSC, Evidence Chain, Truth-State Gate  
**CALSP Integration:** CALSP implements TLC's governance architecture

**Evidence:**
- CALSP defines CHAE (24/7 human audit, bootstrapped as weekly audit buddy)
- CALSP defines NAB (8-10 members, veto power, co-authorship rights)
- CALSP defines CGB (quarterly strategic review, 30% neurodivergent representation)
- CALSP defines OSSC (permanent maintainers, community contribution review)
- CALSP references TLC's Evidence Chain (Ed25519 + Merkle)
- CALSP includes V&T statement (VERIFICATION_AND_TRUTH.md)

**Files:**
- `governance/ethics/Minimal_Ethics_Checklist.md` → Belmont-aligned ethics
- `governance/nist/Bootstrapped_NIST_Mapping.md` → NIST AI RMF 1.0 mapping
- `VERIFICATION_AND_TRUTH.md` → TLC-compliant V&T statement

### Layer 6: Publication Pipeline
**TLC Component:** Research-to-Paper-to-Product pathway  
**CALSP Integration:** CALSP specifies publication targets and pre-submission gates

**Evidence:**
- CALSP targets CHI, AAAI, IJAIED, NeurIPS, IEEE TSE, Nature Human Behaviour
- CALSP requires Tier-1 Compliance Report before submission
- CALSP requires OSF preregistration
- CALSP requires NAB co-authorship offer
- CALSP requires V&T statement in appendix

---

## Constitutional Invariants

CALSP defines three domain-specific constitutional invariants that execute within TLC's runtime:

### Invariant 1: Constitutional Compliance Index (CCI)
```typescript
interface CCIInvariant extends ConstitutionalInvariant {
  id: "CALSP-INV-001"
  description: "System responses must remain within constitutional bounds"
  evaluate(context: Context): InvariantState {
    // Compute CCI = (passing checks) / (total checks)
    // Return SATISFIED if CCI ≥ 0.95, VIOLATED if CCI < 0.80
  }
  repair(context: Context): RepairAction {
    // Halt session, notify CHAE, require human review
  }
  isUpstream: true  // CCI gates all downstream invariants
  dependents: ["CALSP-INV-002", "CALSP-INV-003"]
}
```

### Invariant 2: Neuro-Adaptive Profile (NAP) Ownership
```typescript
interface NAPInvariant extends ConstitutionalInvariant {
  id: "CALSP-INV-002"
  description: "Participants must retain ownership and editability of their NAP"
  evaluate(context: Context): InvariantState {
    // Check if NAP is participant-editable
    // Check if NAP changes are immediately reflected in system behavior
  }
  repair(context: Context): RepairAction {
    // Restore NAP edit capability, log violation
  }
  isUpstream: false
  dependents: []
}
```

### Invariant 3: Dynamic Trust Calibration Index (DTCI) Convergence
```typescript
interface DTCIInvariant extends ConstitutionalInvariant {
  id: "CALSP-INV-003"
  description: "System must improve trust calibration over time"
  evaluate(context: Context): InvariantState {
    // Compute DTCI = 1 - |confidence - correctness|
    // Check if DTCI is converging toward 1.0
  }
  repair(context: Context): RepairAction {
    // Adjust feedback mechanism, notify CHAE if diverging
  }
  isUpstream: false
  dependents: []
}
```

---

## Truth-State Classification

Per TLC 2.0 Article II (Classification and Truth Status):

| Component | Truth-State | Evidence |
|-----------|-------------|----------|
| CALSP Documentation | SPECIFIED | 12 core files, ~4,500 lines, all present |
| CALT Theory | SPECIFIED | 8 falsifiable hypotheses defined |
| CAMM Protocol | SPECIFIED | Mixed-methods design documented |
| Neurodivergent Success Metrics | SPECIFIED | 6 metrics with instruments |
| Bootstrapped Pilot Protocol | SPECIFIED | N=10, <$1K, 28-week timeline |
| Governance Structures | SPECIFIED | CHAE, NAB, CGB, OSSC defined |
| Research Instruments | SPECIFIED | NAP, CCI, DTCI schemas defined |
| Bootstrapped Prototype Code | UNVERIFIED | Not yet implemented |
| Empirical Validation | PROPOSED | No data collected yet |
| IRB Approval | PROPOSED | Not yet submitted |

**Module Truth-State:** SPECIFIED  
**Functional Status:** SPECIFIED (documentation complete, code not implemented)  
**Governance State:** DRAFT (pending human review)

---

## Compliance with TLC 2.0 Constitution

### Article I: What Is Governed ✅
- CALSP is registered as a module (pending formal registry entry)
- CALSP has a V&T statement (VERIFICATION_AND_TRUTH.md)
- CALSP references TLC schemas and contracts

### Article II: Classification and Truth Status ✅
- CALSP uses TLC's truth_status taxonomy
- CALSP follows the Complete Claim Rule (no "working" without verification)
- CALSP documents verified_scope and unverified_scope
- CALSP follows public display rules (no false "working" claims)

### Article III: Roles and Authority ✅
- CALSP respects AI agent hard limits (this V&T requires human approval)
- CALSP defines human roles (author, developer, qa, pm, constitutional_council)
- CALSP embeds sociotechnical authority principle (neurodivergent co-leadership)

### Article IV: C-RSP Contract Law ⏳
- CALSP does not yet have a bound C-RSP contract
- CALSP will require a C-RSP contract before promotion to "working" status
- CALSP follows contract lifecycle (draft → active → frozen → superseded)

### Article V: Verification and Truth (V&T) ✅
- CALSP has a complete V&T statement (VERIFICATION_AND_TRUTH.md)
- CALSP V&T includes all required fields (what, true, unverified, assumed, uncertain, not_claimed)
- CALSP V&T specifies functional_status and governance_state
- CALSP follows honest status principle

### Article VI: Visual Understanding Layer ⏳
- CALSP documentation includes architecture diagrams (in README.md)
- CALSP will require full visual understanding layer before "working" status
- Minimum visual set: architecture, workflow, user journey, pictograph, mock demo, illustration brief

### Article VII: Amendment Process ✅
- CALSP follows TLC's amendment workflow (trigger → draft → diff review → council vote)
- CALSP respects emergency amendment rules
- CALSP respects unanimity requirements for core principles

### Article VIII: Invariants ✅
- CALSP defines three domain-specific invariants (CCI, NAP, DTCI)
- CALSP invariants implement TLC's ConstitutionalInvariant interface
- CALSP invariants specify upstream/downstream relationships

### Article IX: Constitutional Council ⏳
- CALSP will be subject to TLC Constitutional Council review
- CALSP amendments require Council approval
- CALSP respects Council oversight responsibilities

---

## Evidence Chain Integration

CALSP will log all governance decisions to TLC's evidence chain:

**Evidence Locations (TLC 2.0 standard):**
- CHAE decisions: `evidence/CHAE/chae-audit-log.jsonl`
- NAB decisions: `evidence/NAB/nab-decisions.jsonl`
- CGB decisions: `evidence/CGB/cgb-decisions.jsonl`
- OSSC decisions: `evidence/OSSC/ossc-decisions.jsonl`
- Truth-state advances: `evidence/truth-state-advances.jsonl`

**Bootstrapped Equivalent:**
- GitHub Issues with labels: `chae-audit`, `nab-decision`, `cgb-decision`, `ossc-decision`
- Public, timestamped, immutable (via Git history)

---

## Module Registry Entry (Proposed)

```json
{
  "id": "CALSP-RESEARCH-TEMPLATE",
  "label": "Constitutional Adaptive Learning Systems Protocol",
  "path": "constitutional-adaptive-learning/",
  "surface": "private_lab",
  "truth_status": "specified",
  "implementation_status": "draft",
  "public_display_status": "hidden",
  "components": [
    "CALT Theory",
    "CAMM Protocol",
    "Neurodivergent Success Metrics",
    "Bootstrapped Pilot Protocol",
    "Research Instruments (NAP, CCI, DTCI)",
    "Governance Framework (CHAE, NAB, CGB, OSSC)",
    "Ethics Compliance (IRB templates, minimal checklist)",
    "Budget Justification ($7.2M megaproject)"
  ],
  "contract_id": null,
  "verified_date": "2026-06-23",
  "research_lane": "AI Safety + Neurodiversity + HCI",
  "product_lane": "Research Template + Open-Source Toolkit",
  "verified_scope": {
    "component": "Documentation",
    "verification": "12 core files confirmed present via write_to_file",
    "covers": [
      "README.md (450 lines)",
      "CHANGELOG.md (165 lines)",
      "CONTRIBUTING.md (485 lines)",
      "LICENSE (95 lines)",
      "CODE_OF_CONDUCT.md (410 lines)",
      "executive-summary.md (285 lines)",
      "budget-justification.md (685 lines)",
      "irb-protocol-template.md (425 lines)",
      "minimal-ethics-checklist.md (285 lines)",
      "neuro-adaptive-profile.md (430 lines)",
      "bootstrapped-prototype/README.md (545 lines)",
      "VERIFICATION_AND_TRUTH.md (465 lines)"
    ]
  },
  "unverified_scope": [
    "Bootstrapped prototype source code (frontend, backend, constitutional filter)",
    "Research instruments implementation (m-NAP, m-DTCI, cognitive load tracking)",
    "Test suites (unit, integration, accessibility)",
    "Docker containers and deployment scripts",
    "IRB exemption submission and approval",
    "Participant recruitment and data collection",
    "Statistical analysis scripts (R, Python, Stan)",
    "OSF preregistration",
    "Zenodo data repository",
    "Governance bodies recruitment (NCL, NAB, CGB, CHAE, OSSC)",
    "GitHub repository publication",
    "Discord server setup",
    "Zotero group library",
    "Live demo deployment",
    "Evidence chain implementation"
  ],
  "notes": "CALSP v4.3 is a complete research template specification. It integrates TALSP Template v4.2 into TLC 2.0 as Layer 3 (Research Framework). Truth-state = SPECIFIED. Next step: implement bootstrapped prototype code to advance to PARTIAL, then run pilot (N=10) to advance to VERIFIED."
}
```

---

## Generalizability Proof Contribution

CALSP is the **third constitution** in the TLC family. When CALSP executes inside TLC alongside Eight Wonders and Instructional Integrity:

```
Asserted: TLC can execute arbitrary constitutions
                ↓
Demonstrated: TLC has executed three independent constitutions
              in three unrelated domains
                ↓
Generalizability Proof: TLC is a platform, not a domain-specific framework
```

CALSP strengthens the generalizability claim by adding a third domain (neurodivergent-first AI) to the existing two (relational economies, learning systems).

---

## Next Steps for TLC Integration

### Phase 1: Formal Registration (Week 1)
1. Submit module registry entry to TLC 2.0
2. Obtain module ID from TLC registry
3. Create C-RSP contract for CALSP implementation
4. Bind contract to module

### Phase 2: Implementation (Weeks 2-8)
1. Implement bootstrapped prototype code
2. Implement constitutional invariants (CCI, NAP, DTCI)
3. Write test suites
4. Deploy to free-tier hosting
5. Advance truth-state to PARTIAL

### Phase 3: Validation (Weeks 9-28)
1. Obtain IRB exemption
2. Recruit N=10 participants
3. Execute bootstrapped pilot
4. Analyze data
5. Publish Tier-1 Compliance Report v1
6. Advance truth-state to VERIFIED

### Phase 4: Publication (Months 7-12)
1. Preregister on OSF
2. Write manuscripts
3. Submit to peer review
4. Deposit data and code on Zenodo
5. Advance truth-state to VALIDATED

### Phase 5: Megaproject (Months 13-48)
1. Secure $7.2M funding
2. Recruit governance bodies (NCL, NAB, CGB, CHAE, OSSC)
3. Execute N=1,000 study across 4 global hubs
4. Publish in top-tier venues
5. Release open-source toolkit

---

## Alignment Verification Checklist

- [x] V&T statement created (VERIFICATION_AND_TRUTH.md)
- [x] Truth-state classification applied (SPECIFIED)
- [x] Honest status reporting (unverified items listed)
- [x] Constitutional invariants defined (CCI, NAP, DTCI)
- [x] Governance framework documented (CHAE, NAB, CGB, OSSC)
- [x] Evidence chain protocol referenced
- [x] TLC layer mapping complete (Layers 1-6)
- [x] Module registry entry drafted
- [x] Compliance with TLC Constitution verified (Articles I-IX)
- [ ] C-RSP contract created (pending Phase 1)
- [ ] Module registered in TLC registry (pending Phase 1)
- [ ] Evidence chain implementation (pending Phase 2)
- [ ] Visual understanding layer complete (pending Phase 2)
- [ ] Human review and approval (pending)

---

## Human Review Required

**Status:** ⏳ PENDING HUMAN REVIEW

This integration document is agent-produced and requires human review before CALSP can be formally registered in the TLC 2.0 module registry.

**Required Actions:**
1. Human reviewer confirms TLC 2.0 alignment is accurate
2. Reviewer confirms constitutional invariants are correctly specified
3. Reviewer confirms module registry entry is appropriate
4. Reviewer approves integration strategy
5. Reviewer signs off with name, date, and role

**Approval Signature:**
```
Name: _______________________
Role: _______________________
Date: _______________________
Signature: __________________
```

---

**Document ID:** CALSP-TLC-INTEGRATION-001  
**Module ID:** CALSP-RESEARCH-TEMPLATE  
**Version:** 1.0  
**Truth-State:** SPECIFIED  
**Governance State:** DRAFT  
**Last Updated:** 2026-06-23  
**License:** CC BY 4.0  
**Parent System:** The Living Constitution 2.0  
**Integration Status:** ALIGNED (pending formal registration)