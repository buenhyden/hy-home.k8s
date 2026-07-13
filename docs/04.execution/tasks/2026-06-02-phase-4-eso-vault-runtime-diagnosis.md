---
title: 'Task: Phase 4 ESO Vault Runtime Diagnosis'
type: sdlc/task
status: done
owner: platform
updated: 2026-07-13
---

# Task: Phase 4 ESO Vault Runtime Diagnosis

## Overview

This document tracks evidence for the ESO/Vault runtime diagnosis and
repo-backed runbook hardening performed after Phase 3 live validation failed.
The work is limited to read-only live evidence and documentation updates; Vault
unseal and secret inspection are not performed.

## Inputs

- **Parent Plan**: [Phase 4 ESO Vault Runtime Diagnosis Plan](../plans/2026-06-02-phase-4-eso-vault-runtime-diagnosis.md)
- **Phase 3 Evidence**: [Phase 3 Protected Surface Hardening Task](./2026-06-02-phase-3-protected-surface-hardening.md)
- **Runbook**: [ArgoCD ESO Vault Recovery Runbook](../../05.operations/runbooks/0002-argocd-eso-vault-recovery-runbook.md)

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-001 | Reproduce ESO/Vault failure with read-only metadata | eval | N/A | PLN-001 | `ClusterSecretStore/vault-backend Ready=False`; `ExternalSecret` `SecretSyncedError` | platform | Done |
| T-002 | Compare live object and repo desired-state | eval | N/A | PLN-001 | Service, EndpointSlice, ClusterSecretStore, and RBAC match repo contract | platform | Done |
| T-003 | Identify root-cause class | eval | N/A | PLN-001 | Vault health endpoint returns `sealed:true`; ESO logs contain `Vault is sealed` | platform | Done |
| T-004 | Update recovery runbook | doc | N/A | PLN-002 | Runbook includes sealed Vault branch and operator-bound unseal boundary | platform | Done |
| T-005 | Record no-op mutation boundary | guardrail | N/A | PLN-003 | No GitOps/model/provider/CI topology mutation introduced for this diagnosis | platform | Done |
| T-006 | Record execution evidence and validation | doc | N/A | PLN-004, PLN-005 | README indexes, Phase 3 links, progress ledger, static validation | platform | Done |

### Phase View

### Phase 4

- [x] T-001 Failure reproduction
- [x] T-002 Desired-state comparison
- [x] T-003 Root-cause classification
- [x] T-004 Runbook update
- [x] T-005 Mutation boundary record
- [x] T-006 Validation and handoff evidence

## Approval and Safety Boundaries

- **Allowed Paths**: `T-001 through T-006` is limited to these Phase 4 ESO Vault Runtime Diagnosis owners and Task-Table surfaces:
  - `docs/04.execution/tasks/2026-06-02-phase-4-eso-vault-runtime-diagnosis.md`
  - `docs/04.execution/plans/2026-06-02-phase-4-eso-vault-runtime-diagnosis.md`
  - `docs/04.execution/tasks/2026-06-02-phase-3-protected-surface-hardening.md`
  - `docs/05.operations/runbooks/0002-argocd-eso-vault-recovery-runbook.md`
- **Forbidden Paths**: Vault data/auth state, Kubernetes Secret values, unseal material, kubeconfigs, shell history, and paths outside the Phase 4 ESO Vault Runtime Diagnosis evidence/control surfaces.
- **Approval Required**: Human approval is required before any Phase 4 ESO Vault Runtime Diagnosis Vault unseal/auth write, Secret access, live Kubernetes or Argo CD mutation, remote publication, push, or merge.
- **Static Validation**: Preserve the Phase 4 ESO Vault Runtime Diagnosis outcomes and limitations recorded in Verification Summary; use these recorded checks:
  - `bash infrastructure/tests/run-all.sh`
  - `git diff --check`
  - `bash scripts/generate-llm-wiki-index.sh --check`
  - `bash scripts/validate-repo-quality-gates.sh .`
- **Live Validation**: Only the recorded read-only Phase 4 ESO Vault Runtime Diagnosis lane (`curl -sS --max-time 5 http://172.18.0.8:8200/v1/sys/health`) is in scope; it does not authorize mutation or broaden the cited observation into readiness.
- **Secret / Vault Handling**: The Phase 4 ESO Vault Runtime Diagnosis lane must not read, print, enumerate, move, or rewrite Vault tokens, unseal keys, Secret data, credentials, kubeconfigs, private RTK data, or shell history; operator recovery remains out of scope.
- **Rollback Plan**: Revert the logical Phase 4 ESO Vault Runtime Diagnosis change set for `T-001 through T-006` and restore its allowed implementation/evidence paths with this Task and parent Plan; documentation rollback does not authorize live mutation.
- **Evidence Location**: Durable Phase 4 ESO Vault Runtime Diagnosis evidence remains in:
  - `docs/04.execution/tasks/2026-06-02-phase-4-eso-vault-runtime-diagnosis.md`
  - `docs/04.execution/plans/2026-06-02-phase-4-eso-vault-runtime-diagnosis.md`
  - `docs/04.execution/tasks/2026-06-02-phase-3-protected-surface-hardening.md`
  - `docs/05.operations/runbooks/0002-argocd-eso-vault-recovery-runbook.md`

## Verification Summary

- **Test Commands**:
  - `curl -sS --max-time 5 http://172.18.0.8:8200/v1/sys/health` — PASS command exit 0; response reports `sealed:true`.
  - `kubectl -n external-secrets logs deploy/external-secrets --since=2h --tail=80` — PASS command exit 0; logs show `Vault is sealed`.
  - `bash infrastructure/tests/run-all.sh` — expected FAIL until operator unseals Vault; failure remains `vault-backend Ready is not True`.
  - `git diff --check` — PASS.
  - `bash scripts/generate-llm-wiki-index.sh --check` — PASS.
  - `bash scripts/validate-repo-quality-gates.sh .` — PASS.
  - `bash scripts/check-secret-handling.sh .` — PASS.
- **Eval Commands**:
  - Live/repo desired-state comparison for `vault-backend`, `vault-external`, `vault-external-1`, service account, and token reviewer binding — PASS; no repo manifest drift identified.
  - Secret-value boundary review — PASS; no Secret data, Vault token, root token, or unseal key was read or printed.
  - Targeted Phase 4 index/frontmatter/related-documents scans — PASS.
- **Logs / Evidence Location**:
  - This task document after final verification.
  - [Progress ledger](../../00.agent-governance/memory/progress.md).

## Traceability

- [Phase 4 ESO Vault Runtime Diagnosis Plan](../plans/2026-06-02-phase-4-eso-vault-runtime-diagnosis.md)
- [Phase 3 Protected Surface Hardening Plan](../plans/2026-06-02-phase-3-protected-surface-hardening.md)
- [Phase 3 Protected Surface Hardening Task](./2026-06-02-phase-3-protected-surface-hardening.md)
- [ArgoCD ESO Vault Recovery Runbook](../../05.operations/runbooks/0002-argocd-eso-vault-recovery-runbook.md)
- [Task Template](../../99.templates/templates/sdlc/execution/task.template.md)
