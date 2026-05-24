---
title: 'Task: P3 GitOps Secret Runtime Remediation'
type: task
status: active
owner: platform
updated: 2026-05-24
---

# Task: P3 GitOps Secret Runtime Remediation

## Overview (KR)

이 문서는 승인된 P3 ArgoCD, Vault, ESO, secret/runtime remediation의 구현·검증
작업 목록이다. 작업은 GitOps repository desired state와 read-only runtime metadata
검증으로 제한하며, secret 값 출력과 live mutation은 금지한다.

## Inputs

- **Parent Spec**: [../../03.specs/006-workspace-harness-gap-analysis/spec.md](../../03.specs/006-workspace-harness-gap-analysis/spec.md)
- **Parent Plan**: [../plans/2026-05-24-p3-gitops-secret-runtime-remediation.md](../plans/2026-05-24-p3-gitops-secret-runtime-remediation.md)
- **Source Gap Plan**: [../plans/2026-05-24-workspace-harness-gap-analysis.md](../plans/2026-05-24-workspace-harness-gap-analysis.md)

## Working Rules

- Use `gitops-workflow`, `k8s-security-audit`, and `k8s-validate`.
- Do not print or inspect secret values.
- Do not run `kubectl apply`, `kubectl patch`, `argocd app sync`, `vault write`,
  or `vault kv` mutation commands in this task.
- Make repository-backed changes first, then run static validation.
- Read-only runtime checks may inspect metadata/status only.

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P3-GITOPS-T-001 | Create approved P3 plan/task evidence and indexes | doc | VAL-SPC-006 / P3 deferrals | P3-PLN-001 | repo quality gate | Platform | In Progress |
| P3-GITOPS-T-002 | Add ESO DNS/API egress policy coverage | impl | GitOps deferred items | P3-PLN-002 | static contract and manifest validation | Platform | Todo |
| P3-GITOPS-T-003 | Add Vault notifications read policy coverage | impl | Vault deferred items | P3-PLN-003 | static contract and secret scan | Platform | Todo |
| P3-GITOPS-T-004 | Align apps AppProject ExternalSecret permission and sample remoteRef key | impl | App onboarding deferred items | P3-PLN-004 | static contract and manifest validation | Platform | Todo |
| P3-GITOPS-T-005 | Add ArgoCD-owned cluster-local config app path | impl | Bootstrap ownership deferred item | P3-PLN-005 | GitOps structure and static contract validation | Platform | Todo |
| P3-GITOPS-T-006 | Run repo-static validation bundle | test | Verification | P3-PLN-006 | verification summary | Platform | Todo |
| P3-GITOPS-T-007 | Run approved read-only runtime metadata checks | eval | Verification | P3-PLN-006 | live metadata summary without secret values | Platform | Todo |
| P3-GITOPS-T-008 | Append progress memory | memory | Memory Strategy | P3-PLN-001 | progress entry | Platform | Todo |

## Suggested Types

- `impl`
- `test`
- `eval`
- `doc`
- `ops`

## Agent-specific Types (If Applicable)

- `guardrail`
- `memory`
- `eval`

## Phase View

### Phase 1 - Traceability

- [x] P3-GITOPS-T-001 Create approved P3 plan/task evidence and indexes.

### Phase 2 - Repository Desired State

- [ ] P3-GITOPS-T-002 Add ESO DNS/API egress policy coverage.
- [ ] P3-GITOPS-T-003 Add Vault notifications read policy coverage.
- [ ] P3-GITOPS-T-004 Align apps AppProject ExternalSecret permission and sample remoteRef key.
- [ ] P3-GITOPS-T-005 Add ArgoCD-owned cluster-local config app path.

### Phase 3 - Verification

- [ ] P3-GITOPS-T-006 Run repo-static validation bundle.
- [ ] P3-GITOPS-T-007 Run approved read-only runtime metadata checks.
- [ ] P3-GITOPS-T-008 Append progress memory.

## Verification Summary

- **Test Commands**: pending.
- **Eval Commands**: pending.
- **Logs / Evidence Location**: this task document after implementation.

## Related Documents

- **Spec**: [../../03.specs/006-workspace-harness-gap-analysis/spec.md](../../03.specs/006-workspace-harness-gap-analysis/spec.md)
- **Plan**: [../plans/2026-05-24-p3-gitops-secret-runtime-remediation.md](../plans/2026-05-24-p3-gitops-secret-runtime-remediation.md)
- **Source Plan**: [../plans/2026-05-24-workspace-harness-gap-analysis.md](../plans/2026-05-24-workspace-harness-gap-analysis.md)
- **GitOps README**: [../../../gitops/README.md](../../../gitops/README.md)
- **Vault Policy**: [../../../infrastructure/vault/policies/eso-read.hcl](../../../infrastructure/vault/policies/eso-read.hcl)
