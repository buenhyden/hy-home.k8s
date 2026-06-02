---
title: 'Task: Phase 4 ESO Vault Runtime Diagnosis'
type: task
status: draft
owner: platform
updated: 2026-06-02
---

# Task: Phase 4 ESO Vault Runtime Diagnosis

## Overview (KR)

이 문서는 Phase 3 live validation 실패 이후 수행한 ESO/Vault runtime diagnosis와 repo-backed runbook 보강 증거를 추적한다.
작업은 read-only live evidence와 documentation update로 제한하며, Vault unseal이나 secret inspection은 수행하지 않는다.

## Inputs

- **Parent Plan**: [Phase 4 ESO Vault Runtime Diagnosis Plan](../plans/2026-06-02-phase-4-eso-vault-runtime-diagnosis.md)
- **Phase 3 Evidence**: [Phase 3 Protected Surface Hardening Task](./2026-06-02-phase-3-protected-surface-hardening.md)
- **Runbook**: [ArgoCD ESO Vault Recovery Runbook](../../05.operations/runbooks/0002-argocd-eso-vault-recovery-runbook.md)

## Working Rules

- Use systematic debugging: root cause before fix.
- Keep GitOps-first boundaries; do not mutate the cluster.
- Do not read or print unseal keys, Vault tokens, Kubernetes Secret data, private credentials, private RTK databases, or shell history.
- Vault unseal and Vault auth writes are operator-bound follow-up actions, not agent actions.
- Documentation and runbook updates still need validation evidence.

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-001 | Reproduce ESO/Vault failure with read-only metadata | eval | N/A | PLN-001 | `ClusterSecretStore/vault-backend Ready=False`; `ExternalSecret` `SecretSyncedError` | platform | Done |
| T-002 | Compare live object and repo desired-state | eval | N/A | PLN-001 | Service, EndpointSlice, ClusterSecretStore, and RBAC match repo contract | platform | Done |
| T-003 | Identify root-cause class | eval | N/A | PLN-001 | Vault health endpoint returns `sealed:true`; ESO logs contain `Vault is sealed` | platform | Done |
| T-004 | Update recovery runbook | doc | N/A | PLN-002 | Runbook includes sealed Vault branch and operator-bound unseal boundary | platform | Done |
| T-005 | Record no-op mutation boundary | guardrail | N/A | PLN-003 | No GitOps/model/provider/CI topology mutation introduced for this diagnosis | platform | Done |
| T-006 | Record execution evidence and validation | doc | N/A | PLN-004, PLN-005 | README indexes, Phase 3 links, progress ledger, static validation | platform | Done |

## Suggested Types

- `eval`
- `doc`
- `guardrail`

## Agent-specific Types (If Applicable)

- `memory`
- `guardrail`
- `eval`

## Phase View (Optional)

### Phase 4

- [x] T-001 Failure reproduction
- [x] T-002 Desired-state comparison
- [x] T-003 Root-cause classification
- [x] T-004 Runbook update
- [x] T-005 Mutation boundary record
- [x] T-006 Validation and handoff evidence

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

## Related Documents

- [Phase 4 ESO Vault Runtime Diagnosis Plan](../plans/2026-06-02-phase-4-eso-vault-runtime-diagnosis.md)
- [Phase 3 Protected Surface Hardening Plan](../plans/2026-06-02-phase-3-protected-surface-hardening.md)
- [Phase 3 Protected Surface Hardening Task](./2026-06-02-phase-3-protected-surface-hardening.md)
- [ArgoCD ESO Vault Recovery Runbook](../../05.operations/runbooks/0002-argocd-eso-vault-recovery-runbook.md)
- [Task Template](../../99.templates/task.template.md)
