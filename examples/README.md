# examples

> `hy-home.k8s` 플랫폼의 앱 온보딩 예시와 cloud target 참조 구현을 관리한다.

## Overview

이 경로는 실제 운영 manifest의 복제본이 아니라, 새 앱 또는 cloud target을 설계할 때 참고하는 예시를 담는다. `sample-app/`은 로컬 k3d GitOps 최소 온보딩 템플릿이고, `aws/`, `azure/`는 [Tech Stack Version Inventory](../docs/90.references/versions/tech-stack-version-inventory.md)의 `Cloud Example Snapshot` 기준을 따르는 cloud migration 참조 자산이다.

AWS/Azure 예시는 계정이나 live cluster를 변경하지 않는다. 실제 배포를 계획할 때는 새 provider 검증 결과로 `Cloud Example Snapshot`을 갱신하고 비용, IAM/RBAC, 네트워크 경계를 다시 확인해야 한다.

활성 desired state의 정본은 `gitops/`이며, `examples/`는 복사하거나 비교하기 위한 reference-only 영역이다.

## Audience

이 README의 주요 독자:

- Developers
- Operators
- Cloud Architects
- Documentation Writers
- AI Agents

## Scope

### In Scope

- GitOps 앱 온보딩 예시와 placeholder 치환 흐름
- AWS EKS 1.35 target Terraform 참조 구현
- AKS 1.35 target Bicep/Kubernetes 참조 구현
- cloud migration 문서 샘플과 학습 자료

### Out of Scope

- 실제 AWS/Azure 계정 배포
- live Kubernetes 클러스터 변경
- production-grade 비용 산정과 SLA 보장
- secret material 또는 provider credential 저장

## Structure

```text
examples/
├── aws/             # EKS 1.35 target + Terraform AWS provider 6.x 참조 예시
├── azure/           # AKS 1.35 target + Bicep/AGC 참조 예시
├── sample-app/      # GitOps 앱 온보딩 예시
└── README.md        # This file
```

## How to Work in This Area

1. 로컬 앱 온보딩은 [sample-app](sample-app/README.md)을 복사해 시작한다.
2. AWS/Azure 예시는 [Tech Stack Version Inventory](../docs/90.references/versions/tech-stack-version-inventory.md)의 `Cloud Example Snapshot` 기준과 맞춰 수정한다.
3. provider module, Kubernetes version, ingress/gateway 선택이 바뀌면 관련 README와 docs 예시를 같은 변경에서 갱신한다.
4. 변경 후 `bash scripts/validate-repo-quality-gates.sh .`와 outdated marker scan을 실행한다.

## Link Basis

이 README의 링크 기준 위치는 `examples/`다.

- 같은 폴더의 파일과 하위 경로는 현재 README 위치 기준 상대 링크로 연결한다.
- 상위 저장소 문서나 다른 stage 문서는 필요한 만큼 `../`로 올라가서 연결한다.
- 다른 README의 상대 링크를 그대로 복사하지 말고, 이 파일 위치 기준으로 다시 계산한다.

## Related Documents

- [Root README](../README.md)
- [GitOps README](../gitops/README.md)
- [Tech Stack Version Inventory](../docs/90.references/versions/tech-stack-version-inventory.md)
- [Ingress NGINX retirement statement](https://kubernetes.io/blog/2026/01/29/ingress-nginx-statement/)

## 예시 목록

| 디렉토리 | 설명 | 관련 문서 |
| --- | --- | --- |
| [`sample-app`](sample-app) | Rollout + AnalysisTemplate + Ingress + ESO 패턴 최소 앱 온보딩 템플릿 | [Guide](../docs/05.operations/guides/0008-github-app-gitops-onboarding-guide.md) · [Runbook](../docs/05.operations/runbooks/0010-github-app-gitops-onboarding-runbook.md) · [Policy](../docs/05.operations/policies/0007-app-gitops-onboarding-policy.md) |
| [`aws`](aws) | EKS 1.35 target, Terraform AWS provider 6.x 기반 AWS migration 참조 예시 | [AWS docs](aws/docs/README.md) |
| [`azure`](azure) | AKS 1.35 target, Bicep, AGC/Gateway API 기반 Azure migration 참조 예시 | [Azure docs](azure/docs/README.md) |

## Example Role Matrix

| Example path | Role | Active source of truth | Validation |
| --- | --- | --- | --- |
| `sample-app/` | Minimal local k3d GitOps onboarding template with placeholders. | Compare with `../gitops/workloads/adminer/` before copying patterns beyond Rollout, Service, Ingress, AnalysisTemplate, ExternalSecret, and Traefik dynamic config. | `bash scripts/validate-repo-quality-gates.sh .`; `bash scripts/validate-k8s-manifests.sh .`; `bash scripts/check-secret-handling.sh .` |
| `aws/` | Cloud migration reference snapshot for AWS. | `../docs/90.references/versions/tech-stack-version-inventory.md` `Cloud Example Snapshot`; not live provider-latest guidance. | `bash scripts/validate-repo-quality-gates.sh .`; `bash scripts/validate-k8s-manifests.sh .`; `bash scripts/check-secret-handling.sh .` |
| `azure/` | Cloud migration reference snapshot for Azure. | `../docs/90.references/versions/tech-stack-version-inventory.md` `Cloud Example Snapshot`; not live provider-latest guidance. | `bash scripts/validate-repo-quality-gates.sh .`; `bash scripts/validate-k8s-manifests.sh .`; `bash scripts/check-secret-handling.sh .` |

## 사용 방법

각 예시 디렉터리의 `README.md`를 참조한다. 새 앱 온보딩 시 `sample-app/`을 복사하여 플레이스홀더를 교체하는 것이 시작점이고, fuller active reference는 `gitops/workloads/adminer/`와 비교한다.

```bash
cp -r examples/sample-app gitops/workloads/<appname>
```

## 구현 참조

로컬 앱 패턴을 확인할 때는 활성 GitOps 구현과 예시 템플릿을 구분한다.

- [`../gitops/workloads/adminer`](../gitops/workloads/adminer) — DB 관리 UI (Rollout + AnalysisTemplate + PeerAuthentication)
