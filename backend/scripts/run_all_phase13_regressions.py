#!/usr/bin/env python3
"""
SahyogSetu Phase 13: Full Platform Regression Suite Runner
Executes all 10 platform test suites to verify complete technical integrity.
"""

import sys
import subprocess
from pathlib import Path

SUITES = [
    ("Phase 2 Backend Architecture", "backend/tests/test_phase2_backend.py"),
    ("Phase 3 Ingestion & Vectors", "backend/tests/test_phase3_ingestion.py"),
    ("Phase 4 Legal RAG Engine", "backend/tests/test_phase4_rag.py"),
    ("Phase 5 Bhashini Multilingual", "backend/tests/test_phase5_bhashini.py"),
    ("Phase 6 ML Classifiers", "backend/tests/test_phase6_ml.py"),
    ("Phase 7 News Aggregation", "backend/tests/test_phase7_news.py"),
    ("Phase 8 Full-Stack Integration", "backend/tests/test_phase8_integration.py"),
    ("Phase 9 Production Security", "backend/tests/test_phase9_security.py"),
    ("Phase 11 Production Deployment", "backend/tests/test_phase11_deployment.py"),
    ("Phase 13 Jurisdiction Stress", "backend/tests/test_phase13_jurisdiction_stress.py"),
]

def main():
    print("=" * 80)
    print("SAHYOGSETU PHASE 13: FULL PLATFORM REGRESSION RUNNER")
    print("=" * 80)

    total_passed = 0
    failed = []

    for name, path in SUITES:
        print(f"\nRunning {name} ({path})...")
        cmd = [sys.executable, path]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode == 0:
            print(f"  ✓ PASSED: {name}")
            total_passed += 1
        else:
            print(f"  ✗ FAILED: {name}")
            print("STDERR:\n", res.stderr[-500:])
            print("STDOUT:\n", res.stdout[-500:])
            failed.append((name, path))

    print("\n" + "=" * 80)
    print(f"REGRESSION RESULTS: {total_passed} / {len(SUITES)} SUITES PASSED")
    if failed:
        print(f"FAILED SUITES: {[f[0] for f in failed]}")
        sys.exit(1)
    else:
        print("ALL REGRESSION SUITES PASSED WITH 100% SUCCESS!")
    print("=" * 80)

if __name__ == "__main__":
    main()
