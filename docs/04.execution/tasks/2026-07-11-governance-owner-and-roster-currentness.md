---
title: 'Task: Governance Owner and Roster Currentness'
type: sdlc/task
status: active
owner: platform
updated: 2026-07-11
---

# Task: Governance Owner and Roster Currentness

## Overview

This document tracks implementation and verification work for governance owner
and roster currentness. It keeps tasks derived from Spec 025 and its execution
Plan traceable while preserving repository-static evidence boundaries.

## Inputs

- **Parent Spec**:
  [../../03.specs/025-governance-owner-and-roster-currentness/spec.md](../../03.specs/025-governance-owner-and-roster-currentness/spec.md)
- **Parent Plan**:
  [../plans/2026-07-11-governance-owner-and-roster-currentness.md](../plans/2026-07-11-governance-owner-and-roster-currentness.md)

## Working Rules

- Write failing assertions first for deterministic repository behavior.
- Record evidence for every completed task.
- Treat repository-static validation as bounded evidence, not live runtime
  readiness.
- Keep Spec, Plan, Task, audit, owner, and roster lineage reciprocal.

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RCR-001 | Start reciprocal execution lineage | doc | Interfaces & Data Structures | T-001 | Reciprocal-link assertion | platform | Done |
| RCR-002 | Normalize audit IA and relocate completed audit Plan | doc | Audit Information Architecture | T-002 | Current-pointer and pack assertion | platform | Todo |
| RCR-003 | Reconcile all Spec lifecycle and ownership records | doc | Complete Spec Disposition Ledger | T-003 | Spec status/index assertion | platform | Todo |
| RCR-004 | Reconcile all Plan-to-Task evidence links | doc | Complete Plan Evidence Ledger | T-004 | Plan evidence assertion | platform | Todo |
| RCR-005 | Enforce roster and owner-pointer currentness | guardrail | RMD-004 Implementation Components | T-005 | Fixture self-test and quality gate | platform | Todo |
| RCR-006 | Close lifecycle, evidence, and RMD-004 | doc | Success Criteria & Verification Plan | T-006 | Full validation bundle | platform | Todo |

## Suggested Types

- `impl`
- `test`
- `eval`
- `doc`
- `ops`

## Agent-specific Types (If Applicable)

- `prompt`
- `tool`
- `memory`
- `guardrail`
- `eval`
- `observability`

## Verification Summary

- **Test Commands**: reciprocal-lineage assertion, focused repository quality
  gates, and changed-file pre-commit hooks.
- **Eval Commands**: Not applicable to this documentation-only lineage task.
- **Logs / Evidence Location**: This Task table and the logical commits for
  RCR-001 through RCR-006.
- **Safety Boundary**: No live Kubernetes, Argo CD, Vault, provider-runtime,
  credential, secret-value, remote, publish, push, merge, or third-party
  mutation is authorized by this Task.

## Related Documents

- **Spec**:
  [../../03.specs/025-governance-owner-and-roster-currentness/spec.md](../../03.specs/025-governance-owner-and-roster-currentness/spec.md)
- **Plan**:
  [../plans/2026-07-11-governance-owner-and-roster-currentness.md](../plans/2026-07-11-governance-owner-and-roster-currentness.md)
- **Current Audit Pack**:
  [../../90.references/audits/2026-07-11-weia/README.md](../../90.references/audits/2026-07-11-weia/README.md)
- **Remediation Roadmap**:
  [../../90.references/audits/2026-07-11-weia/remediation-roadmap.md](../../90.references/audits/2026-07-11-weia/remediation-roadmap.md)
- **Harness Catalog**:
  [../../00.agent-governance/harness-catalog.md](../../00.agent-governance/harness-catalog.md)
