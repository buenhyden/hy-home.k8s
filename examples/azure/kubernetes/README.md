# Azure Kubernetes (App Manifests)

> 이 경로는 AKS 클러스터에서 구동되는 개별 애플리케이션의 Kubernetes 매니페스트를 관리한다.

## Overview

본 디렉토리는 Azure 배포 환경(AKS 1.35 target)에 최적화된 애플리케이션 매니페스트를 포함한다. 특히 Azure Workload Identity 연동용 Service Account, Secret Store CSI 볼륨 마운트, 리소스 제한 설정(Resource Limit) 및 헬스 체크 설정을 관리한다.

## Audience

이 README의 주요 독자:

- Application Developers
- DevOps Engineers
- AI Agents

## Scope

### In Scope

- 개별 마이크로서비스의 Deployment, Service, ConfigMap 매니페스트
- Workload Identity 연동을 위한 전용 Service Account 정의
- Secret Store CSI 드라이버를 통한 외부 시크릿(AKV) 마운트 설정
- 파드 어피니티 및 안티 어피니티 등 스케줄링 전략

### Out of Scope

- 클러스터 전반의 공통 플랫폼 리소스 (gitops/ platform/ 참조)
- Azure 인프라 리소스 관리 (infrastructure/ 참조)
- 애플리케이션 빌드 파이프라인 (CI)

## Structure

```text
kubernetes/
├── sample-app.yaml     # Workload Identity 및 CSI가 적용된 샘플 앱
└── README.md           # 본 문서
```

## How to Work in This Area

1. [sample-app.yaml](sample-app.yaml)을 템플릿으로 사용하여 새 서비스를 정의한다.
2. 매니페스트 작성 전 [Spec](../docs/03.specs/azure-migration/spec.md)의 가이드와 통제 표준을 반드시 확인한다.
3. 리소스 제한(Requests/Limits)은 실제 워크로드의 프로파일을 바탕으로 설정한다.

## Link Basis

이 README의 링크 기준 위치는 `examples/azure/kubernetes/`다.

- 같은 폴더의 파일과 하위 경로는 현재 README 위치 기준 상대 링크로 연결한다.
- 상위 저장소 문서나 다른 stage 문서는 필요한 만큼 `../`로 올라가서 연결한다.
- 다른 README의 상대 링크를 그대로 복사하지 말고, 이 파일 위치 기준으로 다시 계산한다.

## Related Documents

- **Guide**: [../docs/05.operations/guides/0001-azure-onboarding-guide.md](../docs/05.operations/guides/0001-azure-onboarding-guide.md)
- **GitOps**: [../gitops/README.md](../gitops/README.md)
- **Infrastructure**: [../infrastructure/main.bicep](../infrastructure/main.bicep)

## AI Agent Guidance

1. 매니페스트 생성 시 `azure.workload.identity/use: "true"` 라벨 누락 여부를 반드시 확인한다.
2. 모든 시크릿은 `secrets-store.csi.k8s.io` 볼륨을 통해 파일로 마운트하여 사용하도록 설계한다.
3. 리소스 태그 및 라벨링 규칙을 준수하여 관리 편의성을 높인다.
