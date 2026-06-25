# Blockchain Governance Roadmap
**Governed by:** CANONICAL_INTENT.md v1.1
**Implementation Tier:** Tier 5–6 (Tier-1 Academic + Fortune 500)
**Budget Range:** $1,000,000 – $1,000,000,000
**Current Status:** NOT YET IMPLEMENTED — design-stage specification only

---

## Why This Exists

The Canonical Intent Statement commits to "blockchain-runtime-verified" governance.
This document defines what that means, what it does NOT mean, and what the
implementation milestone is that will make the claim verifiable.

## What "Blockchain-Runtime-Verified" Means

At Tier 5–6 scale, governance records must be:
1. Tamper-evident across organizations that share no common trust anchor
2. Independently auditable without access to the operator's internal systems
3. Compliant with EU AI Act Article 12 (record-keeping) at consortium scale

The MerkleLedger in `core/ledger.py` satisfies requirements 1–2 for a
single-operator context (append-only, SHA-256 hash-chained). Blockchain
is the *multi-operator extension* of the same architecture.

## What It Does NOT Mean

- A public cryptocurrency or token
- Any existing deployment on Ethereum, Solana, or similar
- A requirement at Tiers 1–4 ($100–$1,000,000)

## Technology Choice (to be selected at Tier 5 milestone)

Candidate: Hyperledger Fabric (permissioned, consortium, GDPR-compatible)
Candidate: Ethereum L2 with private mempool (public auditability)
Decision gate: When the first Fortune 500 pilot is contracted.

## Implementation Milestone

This claim is VERIFIED when:
1. `governance/blockchain/` directory contains a deployed smart contract
2. `core/ledger.py` has a `BlockchainLedger` subclass that writes to the chain
3. An independent auditor can verify a governance record using only the
   contract ABI and a public RPC endpoint

Until that milestone, this document is the canonical statement of intent.
