---
title: 'Reference: CI/CD, GitHub Actions, and QA'
type: content/reference
status: active
owner: platform
updated: 2026-08-08
---

# Reference: CI/CD, GitHub Actions, and QA

## Overview

Baseline routing for CI/CD, GitHub Actions, and quality-evidence lanes.

## Reference Type

Repository-static research baseline.

## Authority Boundary

Workflow files and quality standards own automation and evidence semantics;
this reference does not prove hosted runs, delivery, or rollback success.

## Scope

It assigns current workflow and QA research to WERPC-005.

## Definitions / Facts

### CI/CD baseline

`.github/workflows/` is current automation configuration evidence. Hosted CI
and CD behavior are Unverified.

### GitHub Actions baseline

Tracked workflow files are local evidence. GitHub-hosted execution and
permissions resolution are Unverified.

### QA baseline

`scripts/validate-repo-quality-gates.sh` is a local QA entry point. Its result
scope is repository-static and broader delivery readiness is Unverified.

## Sources

WERPC-001 performed no current external CI/CD or Actions research. Predecessor
URLs require current recheck before reuse.

## Review and Freshness

WERPC-005 owns current workflow inventory and source review. Refresh after
workflow, validator, or quality-standard changes.

## Related Documents

- [Platform security](kubernetes-infrastructure-and-security.md)
- [Source ledger](source-coverage-and-migration-ledger.md)
- [Quality standards](../../../00.agent-governance/rules/quality-standards.md)
