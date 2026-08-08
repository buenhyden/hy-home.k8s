---
title: 'Reference: Kubernetes, Infrastructure, and Security'
type: content/reference
status: active
owner: platform
updated: 2026-08-08
---

# Reference: Kubernetes, Infrastructure, and Security

## Overview

Baseline routing for Kubernetes desired state, infrastructure, and security.

## Reference Type

Repository-static research baseline.

## Authority Boundary

GitOps, infrastructure, policy, and operations owners retain authority. This
reference does not authorize cluster inspection or prove live enforcement.

## Scope

It assigns platform and security source review to WERPC-004.

## Definitions / Facts

### Kubernetes baseline

`gitops/` is repository-static desired-state evidence. Cluster reconciliation
and workload readiness are Unverified.

### Infrastructure baseline

`infrastructure/` is repository-static infrastructure evidence. Provisioned
state and remote health are Unverified.

### Security baseline

`policy/` is security-control evidence. Enforcement effectiveness and secret
handling at runtime are Unverified.

## Sources

No external platform or security source was reviewed in WERPC-001. Historical
source URLs are dated predecessor evidence requiring later recheck.

## Review and Freshness

WERPC-004 owns source-backed findings. Refresh after an approved control or
desired-state contract change; live verification remains separately authorized.

## Related Documents

- [CI/CD and QA](ci-cd-github-actions-and-qa.md)
- [Source ledger](source-coverage-and-migration-ledger.md)
- [Operations policies](../../../05.operations/policies/README.md)
