# 98.archive

> 현재 구현과 상충되는 old `docs/01-05` 문서의 Tombstone을 보관하는 중앙 archive stage다.

> [!NOTE]
> All AI agent interactions with this stage must comply with the [Agent Governance Hub](../00.agent-governance/README.md).

## Overview

`98.archive/`는 active 문서 stage에서 제거된 old 문서의 Tombstone만 보관한다.
원문 본문은 보존하지 않고, 원래 경로, archive 사유, 현재 대체 문서, 구현 증거만 남긴다.
Archive Reason과 Tombstone 링크는 historical evidence이며, 현재 운영 계약은
Current Replacement 문서가 소유한다.
`docs/98.archive/05.operations/guides`, `docs/98.archive/05.operations/policies`,
`docs/98.archive/05.operations/runbooks`, `docs/98.archive/05.operations/incidents`
mirror는 operations bucket 구조를 그대로 보존한다.

## Audience

이 README의 주요 독자:

- Platform Engineers
- Documentation Writers
- Architecture Reviewers
- AI Agents

## Scope

### In Scope

- `docs/01.requirements`, `docs/02.architecture`, `docs/03.specs`, `docs/04.execution`, `docs/05.operations`에서 제거된 old 문서 Tombstone
- 원래 docs 하위 경로를 보존하는 mirror layout
- active 문서가 archive를 직접 참조하지 않도록 하는 Index Only 연결
- Tombstone을 현재 desired-state 입력이 아닌 historical evidence로 해석하는 경계

### Out of Scope

- 현재 요구사항, 아키텍처, 명세, 계획, 작업 증적의 정본
- 원문 historical body 보관
- reference 문서나 외부 표준 snapshot

## Structure

```text
98.archive/
├── 01.requirements/
├── 02.architecture/
│   ├── requirements/
│   └── decisions/
├── 03.specs/
├── 04.execution/
│   ├── plans/
│   └── tasks/
├── 05.operations/
│   ├── guides/
│   ├── policies/
│   ├── runbooks/
│   └── incidents/
└── README.md
```

## How to Work in This Area

1. active 문서가 현재 구현과 상충하고 본문 재작성보다 제거가 맞으면 원래 docs 하위 경로를 `98.archive/` 아래에 mirror한다.
2. archive로 이동한 문서는 `../99.templates/templates/common/archive-tombstone.template.md` 구조의 Tombstone으로 교체한다.
3. Tombstone에는 원문 본문을 남기지 않는다.
4. active 문서와 README는 이 archive README만 Index Only로 연결하고, 개별 Tombstone을 직접 current input으로 사용하지 않는다.
5. 현재 구현 범위가 줄어들지 않도록 대체 PRD/ARD/ADR/Spec/Plan/Task 또는 현재 구현 README를 먼저 확정한다.

## Link Basis

이 README의 링크 기준 위치는 `docs/98.archive/`다.

- active stage는 `../01.requirements/`, `../02.architecture/`, `../03.specs/`, `../04.execution/`, `../05.operations/`로 연결한다.
- template stage는 `../99.templates/`로 연결한다.
- tombstone 파일 내부 링크는 각 mirror 위치 기준으로 다시 계산한다.

## Archive Index

### 01.requirements

| Original Path | Tombstone | Current Replacement | Archive Reason |
| --- | --- | --- | --- |
| `docs/01.requirements/2026-03-27-wsl-k3d-argocd-platform.md` | [`01.requirements/2026-03-27-wsl-k3d-argocd-platform.md`](./01.requirements/2026-03-27-wsl-k3d-argocd-platform.md) | [`../01.requirements/004-current-local-gitops-platform.md`](../01.requirements/004-current-local-gitops-platform.md) | Old baseline PRD replaced by current repo-backed platform baseline. |
| `docs/01.requirements/2026-03-28-wsl2-k3d-argocd-ha-platform.md` | [`01.requirements/2026-03-28-wsl2-k3d-argocd-ha-platform.md`](./01.requirements/2026-03-28-wsl2-k3d-argocd-ha-platform.md) | [`../01.requirements/004-current-local-gitops-platform.md`](../01.requirements/004-current-local-gitops-platform.md) | Old endpoint/bootstrap requirement replaced by current `172.18.x` GitOps contract. |
| `docs/01.requirements/2026-03-29-platform-expansion-dashboard-mesh.md` | [`01.requirements/2026-03-29-platform-expansion-dashboard-mesh.md`](./01.requirements/2026-03-29-platform-expansion-dashboard-mesh.md) | [`../01.requirements/004-current-local-gitops-platform.md`](../01.requirements/004-current-local-gitops-platform.md) | Mixed current/old expansion PRD replaced by current platform baseline. |

### 02.architecture

| Original Path | Tombstone | Current Replacement | Archive Reason |
| --- | --- | --- | --- |
| `docs/02.architecture/requirements/0001-wsl-k3d-argocd-platform.md` | [`02.architecture/requirements/0001-wsl-k3d-argocd-platform.md`](./02.architecture/requirements/0001-wsl-k3d-argocd-platform.md) | [`../02.architecture/requirements/0007-current-local-gitops-platform.md`](../02.architecture/requirements/0007-current-local-gitops-platform.md) | Old reference architecture replaced by current ARD. |
| `docs/02.architecture/requirements/0002-wsl2-k3d-argocd-ha-platform.md` | [`02.architecture/requirements/0002-wsl2-k3d-argocd-ha-platform.md`](./02.architecture/requirements/0002-wsl2-k3d-argocd-ha-platform.md) | [`../02.architecture/requirements/0007-current-local-gitops-platform.md`](../02.architecture/requirements/0007-current-local-gitops-platform.md) | Old HA architecture replaced by current ARD. |
| `docs/02.architecture/requirements/0003-platform-expansion-mesh-dashboard.md` | [`02.architecture/requirements/0003-platform-expansion-mesh-dashboard.md`](./02.architecture/requirements/0003-platform-expansion-mesh-dashboard.md) | [`../02.architecture/requirements/0007-current-local-gitops-platform.md`](../02.architecture/requirements/0007-current-local-gitops-platform.md) | Old expansion architecture replaced by current ARD. |
| `docs/02.architecture/decisions/0001-k3d-topology-and-network.md` | [`02.architecture/decisions/0001-k3d-topology-and-network.md`](./02.architecture/decisions/0001-k3d-topology-and-network.md) | [`../02.architecture/decisions/0014-current-local-gitops-platform-contract.md`](../02.architecture/decisions/0014-current-local-gitops-platform-contract.md) | Old network decision replaced by current local platform contract. |
| `docs/02.architecture/decisions/0004-external-services-endpoints-and-valkey-backend.md` | [`02.architecture/decisions/0004-external-services-endpoints-and-valkey-backend.md`](./02.architecture/decisions/0004-external-services-endpoints-and-valkey-backend.md) | [`../02.architecture/decisions/0014-current-local-gitops-platform-contract.md`](../02.architecture/decisions/0014-current-local-gitops-platform-contract.md) | Old external service endpoint decision replaced by current contract. |
| `docs/02.architecture/decisions/0005-wsl2-ha-baseline-and-external-endpoint-contract.md` | [`02.architecture/decisions/0005-wsl2-ha-baseline-and-external-endpoint-contract.md`](./02.architecture/decisions/0005-wsl2-ha-baseline-and-external-endpoint-contract.md) | [`../02.architecture/decisions/0014-current-local-gitops-platform-contract.md`](../02.architecture/decisions/0014-current-local-gitops-platform-contract.md) | Old HA endpoint decision replaced by current contract. |
| `docs/02.architecture/decisions/0007-kubernetes-dashboard-v3.md` | [`02.architecture/decisions/0007-kubernetes-dashboard-v3.md`](./02.architecture/decisions/0007-kubernetes-dashboard-v3.md) | [`../02.architecture/decisions/0014-current-local-gitops-platform-contract.md`](../02.architecture/decisions/0014-current-local-gitops-platform-contract.md) | Removed cluster UI decision replaced by current Headlamp contract. |
| `docs/02.architecture/decisions/0010-headlamp-replaces-dashboard.md` | [`02.architecture/decisions/0010-headlamp-replaces-dashboard.md`](./02.architecture/decisions/0010-headlamp-replaces-dashboard.md) | [`../02.architecture/decisions/0014-current-local-gitops-platform-contract.md`](../02.architecture/decisions/0014-current-local-gitops-platform-contract.md) | Replacement ADR folded into current platform contract to keep active docs free of old UI terms. |

### 03.specs

| Original Path | Tombstone | Current Replacement | Archive Reason |
| --- | --- | --- | --- |
| `docs/03.specs/001-wsl-k3d-argocd-platform/spec.md` | [`03.specs/001-wsl-k3d-argocd-platform/spec.md`](./03.specs/001-wsl-k3d-argocd-platform/spec.md) | [`../03.specs/008-current-local-gitops-platform/spec.md`](../03.specs/008-current-local-gitops-platform/spec.md) | Old baseline spec replaced by current spec. |
| `docs/03.specs/002-wsl2-k3d-argocd-ha-platform/spec.md` | [`03.specs/002-wsl2-k3d-argocd-ha-platform/spec.md`](./03.specs/002-wsl2-k3d-argocd-ha-platform/spec.md) | [`../03.specs/008-current-local-gitops-platform/spec.md`](../03.specs/008-current-local-gitops-platform/spec.md) | Old HA spec replaced by current spec. |
| `docs/03.specs/003-platform-expansion/spec.md` | [`03.specs/003-platform-expansion/spec.md`](./03.specs/003-platform-expansion/spec.md) | [`../03.specs/008-current-local-gitops-platform/spec.md`](../03.specs/008-current-local-gitops-platform/spec.md) | Mixed old/current expansion spec replaced by current spec. |
| `docs/03.specs/007-docs-governance-consistency/spec.md` | [`03.specs/007-docs-governance-consistency/spec.md`](./03.specs/007-docs-governance-consistency/spec.md) | [`../04.execution/plans/2026-06-02-docs-01-05-current-implementation-alignment.md`](../04.execution/plans/2026-06-02-docs-01-05-current-implementation-alignment.md) | Completed governance cleanup snapshot with old hook path contract; replaced by current 01-05 alignment evidence. |

### 04.execution

| Original Path | Tombstone | Current Replacement | Archive Reason |
| --- | --- | --- | --- |
| `docs/04.execution/plans/2026-03-27-wsl-k3d-argocd-platform.md` | [`04.execution/plans/2026-03-27-wsl-k3d-argocd-platform.md`](./04.execution/plans/2026-03-27-wsl-k3d-argocd-platform.md) | [`../04.execution/plans/2026-06-02-current-implementation-docs-alignment.md`](../04.execution/plans/2026-06-02-current-implementation-docs-alignment.md) | Old execution evidence replaced by current cleanup plan. |
| `docs/04.execution/plans/2026-03-28-wsl2-k3d-argocd-ha-platform.md` | [`04.execution/plans/2026-03-28-wsl2-k3d-argocd-ha-platform.md`](./04.execution/plans/2026-03-28-wsl2-k3d-argocd-ha-platform.md) | [`../04.execution/plans/2026-06-02-current-implementation-docs-alignment.md`](../04.execution/plans/2026-06-02-current-implementation-docs-alignment.md) | Old execution evidence replaced by current cleanup plan. |
| `docs/04.execution/plans/2026-03-29-platform-expansion.md` | [`04.execution/plans/2026-03-29-platform-expansion.md`](./04.execution/plans/2026-03-29-platform-expansion.md) | [`../04.execution/plans/2026-06-02-current-implementation-docs-alignment.md`](../04.execution/plans/2026-06-02-current-implementation-docs-alignment.md) | Old expansion execution evidence replaced by current cleanup plan. |
| `docs/04.execution/plans/2026-05-09-k3d-agent-first-remediation.md` | [`04.execution/plans/2026-05-09-k3d-agent-first-remediation.md`](./04.execution/plans/2026-05-09-k3d-agent-first-remediation.md) | [`../04.execution/plans/2026-06-02-current-implementation-docs-alignment.md`](../04.execution/plans/2026-06-02-current-implementation-docs-alignment.md) | Old remediation plan used historical-contract separation that is no longer active policy. |
| `docs/04.execution/plans/2026-05-22-spec-execution-implementation-audit.md` | [`04.execution/plans/2026-05-22-spec-execution-implementation-audit.md`](./04.execution/plans/2026-05-22-spec-execution-implementation-audit.md) | [`../04.execution/plans/2026-06-02-current-implementation-docs-alignment.md`](../04.execution/plans/2026-06-02-current-implementation-docs-alignment.md) | Old audit evidence replaced by current cleanup evidence. |
| `docs/04.execution/plans/2026-05-28-docs-governance-consistency.md` | [`04.execution/plans/2026-05-28-docs-governance-consistency.md`](./04.execution/plans/2026-05-28-docs-governance-consistency.md) | [`../04.execution/plans/2026-06-02-docs-01-05-current-implementation-alignment.md`](../04.execution/plans/2026-06-02-docs-01-05-current-implementation-alignment.md) | Completed governance cleanup snapshot superseded by current 01-05 alignment plan. |
| `docs/04.execution/plans/2026-05-30-common-agent-governance-refactoring.md` | [`04.execution/plans/2026-05-30-common-agent-governance-refactoring.md`](./04.execution/plans/2026-05-30-common-agent-governance-refactoring.md) | [`../04.execution/plans/2026-06-01-stage-00-canonical-adapter-redesign.md`](../04.execution/plans/2026-06-01-stage-00-canonical-adapter-redesign.md) | Superseded-only governance plan. |
| `docs/04.execution/tasks/2026-03-27-wsl-k3d-argocd-platform.md` | [`04.execution/tasks/2026-03-27-wsl-k3d-argocd-platform.md`](./04.execution/tasks/2026-03-27-wsl-k3d-argocd-platform.md) | [`../04.execution/tasks/2026-06-02-current-implementation-docs-alignment.md`](../04.execution/tasks/2026-06-02-current-implementation-docs-alignment.md) | Old execution evidence replaced by current cleanup task. |
| `docs/04.execution/tasks/2026-03-28-wsl2-k3d-argocd-ha-platform.md` | [`04.execution/tasks/2026-03-28-wsl2-k3d-argocd-ha-platform.md`](./04.execution/tasks/2026-03-28-wsl2-k3d-argocd-ha-platform.md) | [`../04.execution/tasks/2026-06-02-current-implementation-docs-alignment.md`](../04.execution/tasks/2026-06-02-current-implementation-docs-alignment.md) | Old execution evidence replaced by current cleanup task. |
| `docs/04.execution/tasks/2026-03-29-platform-expansion.md` | [`04.execution/tasks/2026-03-29-platform-expansion.md`](./04.execution/tasks/2026-03-29-platform-expansion.md) | [`../04.execution/tasks/2026-06-02-current-implementation-docs-alignment.md`](../04.execution/tasks/2026-06-02-current-implementation-docs-alignment.md) | Old expansion evidence replaced by current cleanup task. |
| `docs/04.execution/tasks/2026-05-09-k3d-agent-first-remediation.md` | [`04.execution/tasks/2026-05-09-k3d-agent-first-remediation.md`](./04.execution/tasks/2026-05-09-k3d-agent-first-remediation.md) | [`../04.execution/tasks/2026-06-02-current-implementation-docs-alignment.md`](../04.execution/tasks/2026-06-02-current-implementation-docs-alignment.md) | Old remediation task used historical-contract separation that is no longer active policy. |
| `docs/04.execution/tasks/2026-05-22-spec-execution-implementation-audit.md` | [`04.execution/tasks/2026-05-22-spec-execution-implementation-audit.md`](./04.execution/tasks/2026-05-22-spec-execution-implementation-audit.md) | [`../04.execution/tasks/2026-06-02-current-implementation-docs-alignment.md`](../04.execution/tasks/2026-06-02-current-implementation-docs-alignment.md) | Old audit evidence replaced by current cleanup evidence. |
| `docs/04.execution/tasks/2026-05-28-docs-governance-consistency.md` | [`04.execution/tasks/2026-05-28-docs-governance-consistency.md`](./04.execution/tasks/2026-05-28-docs-governance-consistency.md) | [`../04.execution/tasks/2026-06-02-docs-01-05-current-implementation-alignment.md`](../04.execution/tasks/2026-06-02-docs-01-05-current-implementation-alignment.md) | Completed governance cleanup snapshot superseded by current 01-05 alignment task. |
| `docs/04.execution/tasks/2026-05-30-governance-refactoring.md` | [`04.execution/tasks/2026-05-30-governance-refactoring.md`](./04.execution/tasks/2026-05-30-governance-refactoring.md) | [`../04.execution/tasks/2026-06-01-stage-00-canonical-adapter-redesign.md`](../04.execution/tasks/2026-06-01-stage-00-canonical-adapter-redesign.md) | Superseded-only governance task. |

### 05.operations

| Original Path | Tombstone | Current Replacement | Archive Reason |
| --- | --- | --- | --- |
| `docs/05.operations/guides/0004-headlamp-auth-oidc-guide.md` | [`05.operations/guides/0004-headlamp-auth-oidc-guide.md`](./05.operations/guides/0004-headlamp-auth-oidc-guide.md) | [`../05.operations/guides/README.md`](../05.operations/guides/README.md) | Headlamp OIDC guide referenced missing desired-state files and secret contract; current repo owns Headlamp through chart/ingress/TLS runbook and ADR-0014. |
| `docs/05.operations/runbooks/0005-headlamp-keycloak-runbook.md` | [`05.operations/runbooks/0005-headlamp-keycloak-runbook.md`](./05.operations/runbooks/0005-headlamp-keycloak-runbook.md) | [`../05.operations/runbooks/0004-rollouts-notifications-headlamp-runbook.md`](../05.operations/runbooks/0004-rollouts-notifications-headlamp-runbook.md) | Headlamp Keycloak/OIDC runtime desired state is not present in GitOps SSoT; current operations use the Headlamp chart/ingress/TLS runbook. |

## Related Documents

- [Docs README](../README.md)
- [Document Stage Routing](../00.agent-governance/rules/document-stage-routing.md)
- [Templates README](../99.templates/README.md)
- [Archive Tombstone Template](../99.templates/templates/common/archive-tombstone.template.md)
