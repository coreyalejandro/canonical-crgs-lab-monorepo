# output/regulatory/ — Regulatory Compliance Assets

This directory is written by `core/regulatory_engine.py` (Phase 10).

## Files generated here

| File | Format | Purpose |
|---|---|---|
| `compliance_testing_protocol.json` | JSON | Full regulatory compliance pathway — applicable standards, testing protocols, market-entry sequence |

## Structure of `compliance_testing_protocol.json`

```json
{
  "applicable_standards": [
    { "standard": "ISO 9001:2015", "body": "ISO", "scope": "..." },
    { "standard": "FCC Part 15",   "body": "FCC", "scope": "..." }
  ],
  "testing_protocols": [
    {
      "test_name": "RF Emissions Testing",
      "standard_ref": "47 CFR Part 15",
      "estimated_cost_usd": 8000,
      "estimated_weeks": 6
    }
  ],
  "market_entry_sequence": [
    "1. Complete ISO 9001 QMS audit...",
    "2. Submit for FCC Part 15 testing..."
  ],
  "estimated_total_compliance_cost_usd": 28000,
  "estimated_total_weeks": 16
}
```

## Regulatory frameworks addressed

- **ISO 9001** — Quality Management Systems (all manufactured products)
- **FDA 21 CFR** — Class I/II/III device pathways (if applicable)
- **FCC Part 15** — RF emissions (all electronic products sold in the US)
- **CE Marking** — European Conformity (EU market entry)
- **UN 38.3** — Battery transport safety (if product contains cells)
- **UL 94** — Flammability of plastic materials
- **RoHS 3** — Restriction of hazardous substances (EU/UK)
