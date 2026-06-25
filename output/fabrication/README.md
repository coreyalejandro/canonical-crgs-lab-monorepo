# output/fabrication/ — Cyber-Physical Fabrication Assets

This directory is written by `core/fabrication_engine.py` (Phase 9).

## Files generated here

| File | Format | Purpose |
|---|---|---|
| `alpha_prototype_enclosure.step` | STEP (ISO 10303) | CAD geometry — upload to Protolabs/Xometry for CNC quote |
| `alpha_prototype_enclosure.stl` | STL mesh | 3D print alias — use for FDM/SLA print service uploads |
| `cad_parameters.json` | JSON | Fallback when cadquery not installed — import into any CAD tool |
| `cloud_lab_protocol.json` | JSON | Robotic wet-lab synthesis protocol — POST to Emerald Cloud Lab / Strateos API |

## How geometry is determined

Parameters are read directly from the Phase 8 Bill of Materials (BOM):

```json
{
  "enclosure_length_mm": 120.0,
  "enclosure_width_mm":   60.0,
  "enclosure_height_mm":  20.0,
  "wall_thickness_mm":     2.5
}
```

If the BOM does not include these keys, defaults from `_CAD_DEFAULTS` in
`core/fabrication_engine.py` are used and flagged.

## Provenance

The `cloud_lab_protocol.json` includes a `patent_claims_hash` field — the
first 16 hex characters of SHA-256 of the patent claims text — linking the
physical synthesis protocol to the specific IP filing version.

## Install cadquery for full CAD output

```bash
pip install cadquery==2.4.0
```

Without cadquery installed, the engine degrades gracefully to writing
`cad_parameters.json` and continues the pipeline without halting.
