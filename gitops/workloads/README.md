# workloads

> ArgoCD ApplicationSet이 스캔하는 애플리케이션 워크로드 매니페스트를 관리한다.

## Overview

이 경로의 각 하위 디렉터리는 독립적인 앱 단위다. 일반적으로 Kustomize 기반 Kubernetes manifest, Argo Rollout, Service, Ingress, AnalysisTemplate을 함께 두며, secret-backed config가 필요한 앱만 ExternalSecret을 포함한다.

새 앱은 [examples/sample-app](../../examples/sample-app/README.md)을 복사해 시작한다. placeholder를 실제 앱 값으로 바꾼 뒤 `gitops/workloads/<appname>` 아래에서 GitOps/manifest/secret 검증을 통과해야 active GitOps desired state로 다룬다.

### Audience

이 README의 주요 독자:

- Application Developers
- Operators
- Documentation Writers
- AI Agents

### Scope

#### In Scope

- 앱별 Kubernetes manifest와 Kustomize 진입점
- Argo Rollouts 기반 progressive delivery 리소스
- External Secrets Operator와 연결되는 Secret 참조
- 앱별 ingress/service/network 관련 선언

#### Out of Scope

- 플랫폼 공통 controller 설치
- 외부 데이터베이스/캐시/Vault 런타임 생성
- cloud target 전용 Terraform/Bicep 코드
- live cluster에 직접 적용하는 운영 절차

## Structure

```text
workloads/
├── adminer/       # 현재 운영 중인 참조 앱 매니페스트
└── README.md      # This file
```

### Workload Coverage Matrix

이 표는 ApplicationSet이 스캔하는 실제 workload 디렉터리와 검증 명령을
연결한다. `validate-repo-quality-gates.sh`는 이 표가 `workloads/*`
디렉터리와 동기화되어 있고, 각 workload가 GitOps 구조, manifest, secret
handling 검증 명령을 명시하는지 확인한다.

| Workload | Purpose and owner | Lifecycle and config | Dependencies, routes, secrets | Validation and operations |
| --- | --- | --- | --- | --- |
| `adminer` | Reference admin workload owned by platform maintainers and app operators. | Managed by the local apps ApplicationSet from `gitops/workloads/adminer/kustomization.yaml`; includes Rollout, services, ingress, Istio routing, PeerAuthentication, and AnalysisTemplate. | Depends on `apps` namespace, Argo Rollouts, ingress, Istio, and the PostgreSQL external service route. | Validate with `bash scripts/validate-gitops-structure.sh`, `bash scripts/validate-k8s-manifests.sh .`, and `bash scripts/check-secret-handling.sh .`; live rollout and ingress checks require intentional cluster validation. |

## Configuration Boundary

Each child directory becomes active desired state only through the repository's
branch, review, and ArgoCD reconciliation flow. Keep plaintext secrets and
credentials out of manifests; use the approved ExternalSecret and external
store boundaries documented by the parent GitOps contract.

## Validation

Run the exact static commands in the workload coverage matrix and parent
[GitOps validation section](../README.md#validation). Repository-static success
does not prove live rollout, route, database, Vault, or ESO readiness.

## Operations

### Working Procedure

1. [examples/sample-app](../../examples/sample-app/README.md)의 파일 구성을 먼저 확인한다.
2. 앱 이름, 이미지 태그, 포트, Vault 경로, ingress host를 실제 값으로 치환한다.
3. `kustomization.yaml`에 모든 리소스가 포함되었는지 확인한다.
4. 변경 후 `bash scripts/validate-gitops-structure.sh`, `bash scripts/validate-k8s-manifests.sh .`, `bash scripts/check-secret-handling.sh .`를 실행한다.

### Link Basis

이 README의 링크 기준 위치는 `gitops/workloads/`다.

- 같은 폴더의 파일과 하위 경로는 현재 README 위치 기준 상대 링크로 연결한다.
- 상위 저장소 문서나 다른 stage 문서는 필요한 만큼 `../`로 올라가서 연결한다.
- 다른 README의 상대 링크를 그대로 복사하지 말고, 이 파일 위치 기준으로 다시 계산한다.

## Related Documents

- [GitOps README](../README.md)
- [App Onboarding Guide](../../docs/05.operations/guides/0008-github-app-gitops-onboarding-guide.md)
- [App Onboarding Policy](../../docs/05.operations/policies/0007-app-gitops-onboarding-policy.md)
- [App Onboarding Runbook](../../docs/05.operations/runbooks/0010-github-app-gitops-onboarding-runbook.md)
