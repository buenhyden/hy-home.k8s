---
title: 'Phase 4 ESO Vault Runtime Diagnosis Plan'
type: plan
status: draft
owner: platform
updated: 2026-06-02
---

# Phase 4 ESO Vault Runtime Diagnosis Plan

## Overview (KR)

이 문서는 Phase 3 live validation에서 발견된 ESO/Vault runtime readiness 실패를 root cause 기준으로 분류하고, repo-backed 후속 증적과 operator-bound 복구 경계를 고정하는 계획이다.
Phase 4는 GitOps desired-state를 추측으로 변경하지 않고, `vault-backend Ready=False`의 실제 원인을 live metadata와 existing runbook evidence로 확인한다.

## Context

Phase 3 read-only live validation에서 `bash infrastructure/tests/run-all.sh`가 ESO/Vault integration 단계에서 실패했다.
`ClusterSecretStore/vault-backend`는 `Ready=False`, reason `InvalidProviderConfig`였고, dependent `ExternalSecret`들은 `SecretSyncedError`를 보고했다.

추가 read-only 진단은 다음을 확인했다.

- `vault-external` Service와 EndpointSlice는 repo desired-state와 일치한다.
- Vault endpoint `http://172.18.0.8:8200/v1/sys/health`는 응답하지만 `sealed:true`를 반환한다.
- ESO controller logs show Kubernetes auth login fails with HTTP 503 and `Vault is sealed`.
- External services, network policies, ingress/TLS static/live checks mostly pass, with Kiali TLS warning tracked separately.

## Goals & In-Scope

- **Goals**:
  - ESO/Vault failure를 endpoint drift가 아니라 Vault sealed runtime prerequisite failure로 분류한다.
  - Existing recovery runbook에 sealed Vault 분기와 operator-bound unseal boundary를 추가한다.
  - Secret values, Vault tokens, unseal keys, root tokens를 조회하지 않는다.
  - Phase 4 diagnosis evidence를 Plan/Task/README/progress ledger로 추적 가능하게 남긴다.
- **In Scope**:
  - Read-only Kubernetes metadata and controller log diagnosis.
  - Read-only Vault unauthenticated health endpoint check.
  - Runbook guidance update under `docs/05.operations/runbooks/`.
  - Execution Plan/Task, README indexes, Phase 3 downstream links, and progress ledger updates.

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - Perform Vault unseal.
  - Modify Vault auth mount, Vault policy, Vault secret values, or external Vault runtime configuration.
  - Change GitOps manifests without a repo-backed drift finding.
  - Change model policy, provider config, CI topology, or Stage 00 architecture.
- **Out of Scope**:
  - Unseal key, root token, Vault token, secret value, private RTK database, credential, or shell history inspection.
  - `kubectl apply`, `kubectl patch`, `argocd app sync`, `vault write`, `vault kv put`, deployment, publish, or destructive Git action.

## Requirements & Acceptance Criteria

| Requirement | Acceptance Criteria |
| --- | --- |
| REQ-P4-001 | Live failure is reproduced and narrowed to a root-cause class using read-only evidence. |
| REQ-P4-002 | Existing Vault recovery runbook distinguishes sealed Vault from EndpointSlice/network drift. |
| REQ-P4-003 | Operator-bound unseal boundary is documented without secret values or key material. |
| REQ-P4-004 | No GitOps manifest, model policy, provider config, CI topology, secret, or Vault runtime mutation is performed. |
| REQ-P4-005 | Phase 4 Plan/Task, README indexes, Phase 3 downstream links, and progress ledger are updated. |
| REQ-P4-006 | Static validation passes, while live ESO/Vault readiness remains accurately reported as blocked until Vault is unsealed. |

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-001 | Gather read-only live evidence | Kubernetes metadata, ESO logs, Vault health endpoint | REQ-P4-001 | Evidence shows `Vault is sealed` and no secret values are read. |
| PLN-002 | Update recovery runbook sealed-state branch | `docs/05.operations/runbooks/0002-argocd-eso-vault-recovery-runbook.md` | REQ-P4-002, REQ-P4-003 | Runbook includes sealed Vault diagnosis and operator-bound unseal boundary. |
| PLN-003 | Record no-op protected surfaces | GitOps manifests, model/provider/CI surfaces | REQ-P4-004 | Diff review shows no unauthorized manifest/model/provider/CI topology changes. |
| PLN-004 | Record Phase 4 execution evidence | Phase 4 Plan/Task, README indexes, Phase 3 links, progress ledger | REQ-P4-005 | New artifacts are indexed and linked. |
| PLN-005 | Run verification | Repo-static validators and read-only live status checks | REQ-P4-006 | Static checks pass; live ESO/Vault blocker is recorded. |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-P4-001 | Runtime metadata | Check Vault health without credentials | `curl -sS --max-time 5 http://172.18.0.8:8200/v1/sys/health` | Returns initialized/sealed state; no token required. |
| VAL-P4-002 | Runtime logs | Confirm ESO failure signature | `kubectl -n external-secrets logs deploy/external-secrets --since=2h --tail=80` | Contains `Vault is sealed` and no secret values are reported. |
| VAL-P4-003 | Static syntax | Check changed shell-sensitive files if any | `bash -n docs/00.agent-governance/hooks/post-validate.sh docs/00.agent-governance/hooks/lifecycle-guard.sh docs/00.agent-governance/hooks/session-start.sh scripts/validate-repo-quality-gates.sh` | Exit 0. |
| VAL-P4-004 | Diff hygiene | Check whitespace and conflict markers | `git diff --check` | Exit 0. |
| VAL-P4-005 | Wiki index | Confirm generated LLM Wiki index remains current | `bash scripts/generate-llm-wiki-index.sh --check` | PASS. |
| VAL-P4-006 | Repository quality | Run repository quality gates | `bash scripts/validate-repo-quality-gates.sh .` | PASS. |
| VAL-P4-007 | Live readiness boundary | Re-run approved read-only aggregate test | `bash infrastructure/tests/run-all.sh` | Expected to fail until Vault is unsealed; failure must remain recorded. |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Agent attempts to unseal Vault or inspect secrets | High | Keep unseal steps operator-bound and value-free; do not request or print key material. |
| EndpointSlice is changed even though Vault is sealed | Medium | Run health endpoint check before endpoint hotfix and branch on `sealed:true`. |
| Runtime failure is hidden by static validation pass | High | Record repo-static and live readiness evidence separately. |
| Runbook update introduces unsafe command examples | Medium | Mark unseal as operator-bound and avoid inline credentials or secret values. |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**: Diff hygiene, LLM Wiki freshness, repository quality gate, and targeted Phase 4 index scans.
- **Sandbox / Canary Rollout**: Read-only live metadata/log probes only.
- **Human Approval Gate**: Required for Vault unseal, Vault auth writes, secret value inspection, ArgoCD sync, Kubernetes mutation, or Docker network mutation.
- **Rollback Trigger**: If repo quality fails, revert only Phase 4 Plan/Task, runbook wording, README rows, Phase 3 links, and progress ledger entry.
- **Prompt / Model Promotion Criteria**: Not applicable.

## Completion Criteria

- [x] ESO/Vault root-cause class is identified as Vault sealed runtime prerequisite failure.
- [x] Recovery runbook includes sealed Vault diagnosis and operator-bound unseal boundary.
- [x] Phase 4 Plan/Task are indexed and linked from Phase 3.
- [x] Progress ledger records evidence and remaining runtime blocker.
- [x] Static verification commands pass or limitations are recorded.
- [x] No secret value, unseal key, token, live mutation, or unauthorized protected-surface diff is introduced.

## Rollback

- Remove Phase 4 Plan/Task files.
- Remove Phase 4 rows from Plans/Tasks README indexes.
- Remove Phase 4 links from Phase 3 Plan/Task.
- Revert the sealed Vault additions in `0002-argocd-eso-vault-recovery-runbook.md` and its README date/description row.
- Remove the Phase 4 progress ledger entry.

## Related Documents

- **Phase 3 Plan**: [./2026-06-02-phase-3-protected-surface-hardening.md](./2026-06-02-phase-3-protected-surface-hardening.md)
- **Phase 3 Task**: [../tasks/2026-06-02-phase-3-protected-surface-hardening.md](../tasks/2026-06-02-phase-3-protected-surface-hardening.md)
- **Tasks**: [../tasks/2026-06-02-phase-4-eso-vault-runtime-diagnosis.md](../tasks/2026-06-02-phase-4-eso-vault-runtime-diagnosis.md)
- **Vault Recovery Runbook**: [../../05.operations/runbooks/0002-argocd-eso-vault-recovery-runbook.md](../../05.operations/runbooks/0002-argocd-eso-vault-recovery-runbook.md)
- **Current Platform ARD**: [../../02.architecture/requirements/0007-current-local-gitops-platform.md](../../02.architecture/requirements/0007-current-local-gitops-platform.md)
- **Current Platform Spec**: [../../03.specs/008-current-local-gitops-platform/spec.md](../../03.specs/008-current-local-gitops-platform/spec.md)
- **Plan Template**: [../../99.templates/plan.template.md](../../99.templates/plan.template.md)
