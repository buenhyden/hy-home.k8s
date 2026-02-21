#!/usr/bin/env bash

# Quality Gate: Test Coverage Enforcement
# Requirement ID: [REQ-TST-04] Coverage Minimum >= 80%

set -euo pipefail

# This is a sample gate script meant to be executed by CI/CD workflows.
# It reads a coverage report summary (e.g., from Jest or Go test output)
# and ensures the total line coverage meets the 80% baseline.

MIN_COVERAGE=80
COVERAGE_FILE=$1

if [ ! -f "$COVERAGE_FILE" ]; then
  echo "Error: Coverage report file '$COVERAGE_FILE' not found."
  exit 1
fi

# Example parsing logic (depends on your actual coverage tool output):
# Here we just mock parsing a simple "Lines: 85%" string from the file.
# Replace this grep/awk logic with actual parsing for lcov, jacoco, etc.
ACTUAL_COVERAGE=$(grep -oP 'Lines:\s*\K[0-9]+' "$COVERAGE_FILE" || echo 0)

echo "Required Coverage: ${MIN_COVERAGE}%"
echo "Actual Coverage:   ${ACTUAL_COVERAGE}%"

if [ "$ACTUAL_COVERAGE" -lt "$MIN_COVERAGE" ]; then
  echo "❌ QUALITY GATE FAILED: Code coverage is below the ${MIN_COVERAGE}% minimum threshold."
  exit 1
else
  echo "✅ QUALITY GATE PASSED: Code coverage meets the standard."
  exit 0
fi
