---
title: 'Task: Current Implementation Docs Alignment'
type: sdlc/task
status: done
owner: platform
updated: 2026-07-13
---

# Task: Current Implementation Docs Alignment

## Overview

This document tracks implementation and verification tasks for current
implementation docs alignment. The evidence covers active docs cleanup,
archive Tombstone creation, validator hardening, and regression checks. The
follow-up currentness pass extended through `docs/05.operations` is owned by
the [Docs 01-05 Current Implementation Alignment Task](./2026-06-02-docs-01-05-current-implementation-alignment.md).

## Inputs

- **Parent Spec**: [../../03.specs/008-current-local-gitops-platform/spec.md](../../03.specs/008-current-local-gitops-platform/spec.md)
- **Parent Plan**: [../plans/2026-06-02-current-implementation-docs-alignment.md](../plans/2026-06-02-current-implementation-docs-alignment.md)

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-001 | Create current baseline PRD/ARD/ADR/Spec chain | doc | Related Inputs | PLN-001 | Template coverage and link validation passed | platform | Done |
| T-002 | Add archive Tombstone stage and template | doc | Governance Contract | PLN-002 | Archive template mapping validation passed | platform | Done |
| T-003 | Move old conflicting docs to Tombstones | doc | Migration / Transition Plan | PLN-003 | Active stale-contract scan passed | platform | Done |
| T-004 | Update active README indexes and related links | doc | Related Documents | PLN-004 | Markdown link validation passed | platform | Done |
| T-005 | Harden repo quality gate, hook trigger, and PR QA checklist | test | Verification Commands | PLN-005 | `bash scripts/validate-repo-quality-gates.sh .` passed | platform | Done |
| T-006 | Run regression checks | test | Success Criteria | PLN-001..005 | Required regression commands passed | platform | Done |

### Phase View

### Phase 1

- [x] T-001 Create current baseline chain
- [x] T-002 Add archive stage

### Phase 2

- [x] T-003 Move old docs
- [x] T-004 Update links
- [x] T-005 Harden validator
- [x] T-006 Run regression checks

## Approval and Safety Boundaries

- **Allowed Paths**: `T-001 through T-006` is limited to these Current Implementation Docs Alignment owners and Task-Table surfaces:
  - `docs/04.execution/tasks/2026-06-02-current-implementation-docs-alignment.md`
  - `docs/03.specs/008-current-local-gitops-platform/spec.md`
  - `docs/04.execution/plans/2026-06-02-current-implementation-docs-alignment.md`
- **Forbidden Paths**: runtime manifests, provider or CI settings, secret values, generated/local state, and paths outside the Current Implementation Docs Alignment work items and linked evidence owners.
- **Approval Required**: Human approval is required before Current Implementation Docs Alignment protected-file expansion, deletion/relocation, runtime/CI/provider mutation, credential access, publication, push, or merge beyond the parent Plan.
- **Static Validation**: Preserve the Current Implementation Docs Alignment outcomes and limitations recorded in Verification Summary; use these recorded checks:
  - `bash -n scripts/validate-repo-quality-gates.sh`
  - `bash -n docs/00.agent-governance/hooks/k8s-pre-edit.sh`
  - `bash -n docs/00.agent-governance/hooks/post-validate.sh`
  - `git diff --check`
- **Live Validation**: DEFER — Current Implementation Docs Alignment is closed by repository-static/documentation evidence; historical live commands, if any, are not authority for a new cluster, provider, external-service, or deployment claim.
- **Secret / Vault Handling**: No secret value is required for Current Implementation Docs Alignment; do not read or print tokens, credentials, Vault/Kubernetes Secret data, kubeconfigs, auth files, private logs, or shell history.
- **Rollback Plan**: Revert the logical Current Implementation Docs Alignment change set for `T-001 through T-006` and restore its allowed implementation/evidence paths with this Task and parent Plan; documentation rollback does not authorize live mutation.
- **Evidence Location**: Durable Current Implementation Docs Alignment evidence remains in:
  - `docs/04.execution/tasks/2026-06-02-current-implementation-docs-alignment.md`
  - `docs/03.specs/008-current-local-gitops-platform/spec.md`
  - `docs/04.execution/plans/2026-06-02-current-implementation-docs-alignment.md`

## Verification Summary

- **Test Commands**:
  - `bash -n scripts/validate-repo-quality-gates.sh` — PASS
  - `bash -n docs/00.agent-governance/hooks/k8s-pre-edit.sh` — PASS
  - `bash -n docs/00.agent-governance/hooks/post-validate.sh` — PASS
  - `git diff --check` — PASS
  - `bash scripts/validate-repo-quality-gates.sh .` — PASS
  - `bash infrastructure/tests/verify-contracts-static.sh` — PASS
  - `bash scripts/validate-gitops-structure.sh` — PASS
  - `bash scripts/validate-k8s-manifests.sh .` — PASS
  - `bash scripts/check-secret-handling.sh .` — PASS
  - `bash scripts/validate-policy-gates.sh .` — PASS
- **Eval Commands**: not applicable.
- **Logs / Evidence Location**: this task document, current baseline docs, and final command output in the implementation handoff.

## Traceability

- **Spec**: [../../03.specs/008-current-local-gitops-platform/spec.md](../../03.specs/008-current-local-gitops-platform/spec.md)
- **Plan**: [../plans/2026-06-02-current-implementation-docs-alignment.md](../plans/2026-06-02-current-implementation-docs-alignment.md)
- **Follow-up Task**: [./2026-06-02-docs-01-05-current-implementation-alignment.md](./2026-06-02-docs-01-05-current-implementation-alignment.md)
- **Archive Index**: [../../98.archive/README.md](../../98.archive/README.md)
