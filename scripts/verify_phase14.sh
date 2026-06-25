#!/usr/bin/env bash
set -uo pipefail

PASS=0; FAIL=0
ROOT="$(pwd)"

check() {
  local label="$1"; shift
  if "$@" >/dev/null 2>&1; then
    echo "  PASS: $label"; PASS=$((PASS+1))
  else
    echo "  FAIL: $label"; FAIL=$((FAIL+1))
  fi
}

cd "$ROOT"

echo "=== PHASE 14 COMPLETION GATE ==="

# GAP-01
check "core/boot.py exists"         test -f core/boot.py
check "core/orchestrator.py exists" test -f core/orchestrator.py
check "ui/web_engine.py exists"     test -f ui/web_engine.py
check "README.md exists"            test -f README.md
check "CANONICAL_INTENT.md exists"  test -f CANONICAL_INTENT.md

# GAP-02
check "boot.py has literal hash"    grep -q '^CONSTITUTION_HASH = "' core/boot.py

# GAP-03
check "orchestrator imports ResearchState"   grep -q "ResearchState" core/orchestrator.py
if grep -q "StateGraph(dict)" core/orchestrator.py 2>/dev/null; then
  echo "  FAIL: orchestrator has no StateGraph(dict)"; FAIL=$((FAIL+1))
else
  echo "  PASS: orchestrator has no StateGraph(dict)"; PASS=$((PASS+1))
fi

# GAP-04
if grep -q "<<<<<<" "CRGS-LAB-PRODUCTS/agent-sentinel-alignment-anomaly-detector/README.md" 2>/dev/null; then
  echo "  FAIL: no merge markers in sentinel README"; FAIL=$((FAIL+1))
else
  echo "  PASS: no merge markers in sentinel README"; PASS=$((PASS+1))
fi
if grep -q "your-org" "CRGS-LAB-PRODUCTS/agent-sentinel-alignment-anomaly-detector/README.md" 2>/dev/null; then
  echo "  FAIL: no your-org placeholder in sentinel README"; FAIL=$((FAIL+1))
else
  echo "  PASS: no your-org placeholder in sentinel README"; PASS=$((PASS+1))
fi

# GAP-05
if grep -q "Phase 1 Active" README.md 2>/dev/null; then
  echo "  FAIL: README not stale (Phase 1 Active removed)"; FAIL=$((FAIL+1))
else
  echo "  PASS: README not stale (Phase 1 Active removed)"; PASS=$((PASS+1))
fi
check "README shows Phase 13 Complete" grep -q "Phase 13 Complete" README.md

# GAP-06
check "Phase 13 underscore filename exists" test -f "BUILD-CONTRACT-PLANS/CRGS-LAB-BUILD-CONTRACT-PLANS_PHASE_13.md"
if test -f "BUILD-CONTRACT-PLANS/CRGS-LAB-BUILD-CONTRACT-PLANS_PHASE 13.md" 2>/dev/null; then
  echo "  FAIL: Phase 13 space filename gone"; FAIL=$((FAIL+1))
else
  echo "  PASS: Phase 13 space filename gone"; PASS=$((PASS+1))
fi
if grep -qi "dillinger" "BUILD-CONTRACT-PLANS/CRGS-LAB-BUILD-CONTRACT-PLANS_PHASE_13.md" 2>/dev/null; then
  echo "  FAIL: Phase 13 no Dillinger artifacts"; FAIL=$((FAIL+1))
else
  echo "  PASS: Phase 13 no Dillinger artifacts"; PASS=$((PASS+1))
fi

# GAP-07
check "CANONICAL_INTENT.md has v1.1 amendment" grep -q "1.1" CANONICAL_INTENT.md

# GAP-08
check "CCD V&T file present"      test -f CRGS-LAB-PRODUCTS/ccd-research-framework/VERIFICATION_AND_TRUTH.md
check "MADMall V&T file present"  test -f CRGS-LAB-PRODUCTS/mad-mall-production/VERIFICATION_AND_TRUTH.md
check "Sentinel V&T file present" test -f CRGS-LAB-PRODUCTS/agent-sentinel-alignment-anomaly-detector/VERIFICATION_AND_TRUTH.md

# GAP-09
check "BLOCKCHAIN_ROADMAP.md present"          test -f BLOCKCHAIN_ROADMAP.md
check "BLOCKCHAIN_ROADMAP NOT YET IMPLEMENTED" grep -q "NOT YET IMPLEMENTED" BLOCKCHAIN_ROADMAP.md

# GAP-10
check "MODULE_STATUS date updated" grep -q "2026-06-25" CRGS-LAB-PRODUCTS/the-living-constitution-2.0/MODULE_STATUS.md

echo ""
echo "=== RESULTS: $PASS passed | $FAIL failed ==="
if [ "$FAIL" -eq 0 ]; then
  echo "PHASE 14 COMPLETE"
else
  echo "PHASE 14 INCOMPLETE — resolve FAIL items"
  exit 1
fi
