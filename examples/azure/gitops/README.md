# Azure GitOps (Platform Manifests)

> 이 경로는 Azure 환경에서 클러스터 전반의 공통 플랫폼 리소스를 GitOps 방식으로 관리하는 매니페스트를 포함한다.

## Overview

본 디렉토리는 ArgoCD 등을 통해 AKS 클러스터에 클라우드 기반 관리형 플랫폼 리소스를 선언적으로 배포하기 위한 설정 파일을 관리한다. Azure Managed Identity 연동, Gateway API 리소스, 그리고 시크릿 관리 설정을 포함한다.

## Audience

이 README의 주요 독자:

- Platform Engineers
- DevOps Engineers
- AI Agents

## Scope

### In Scope

- Azure Managed Identity 및 Federated Credential 연동 설정 (platform/dir)
- Azure Application Gateway for Containers (AGC)용 Gateway API 정의
- 클러스터 공통 플랫폼 가동을 위한 컨트롤러 설정 및 헬름 차트 구성

### Out of Scope

- 일반 애플리케이션 리소스 (kubernetes/ 참조)
- 클라우드 하드 인프라 프로비저닝 (infrastructure/ 참조)
- 클러스터 외부의 수동 운영 작업

## Structure

```text
gitops/
├── platform/
│   ├── managed-identity.yaml   # Managed Identity 연동
│   └── gateway.yaml            # AGC Gateway 리소스 정의
└── README.md                   # 본 문서
```

## How to Work in This Area

1. [infrastructure/main.bicep](../infrastructure/main.bicep)에서 생성된 Client ID 등을 매니페스트에 반영한다.
2. 매니페스트 변경은 반드시 GitOps 풀 모델(ArgoCD)을 통해 클러스터에 반영되어야 한다.
3. [Spec](../docs/03.specs/azure-migration/spec.md)에 정의된 인터페이스 규격을 준수한다.

## Link Basis

이 README의 링크 기준 위치는 `examples/azure/gitops/`다.

- 같은 폴더의 파일과 하위 경로는 현재 README 위치 기준 상대 링크로 연결한다.
- 상위 저장소 문서나 다른 stage 문서는 필요한 만큼 `../`로 올라가서 연결한다.
- 다른 README의 상대 링크를 그대로 복사하지 말고, 이 파일 위치 기준으로 다시 계산한다.

## Related Documents

- **Spec**: [../docs/03.specs/azure-migration/spec.md](../docs/03.specs/azure-migration/spec.md)
- **Infrastructure**: [../infrastructure/README.md](../infrastructure/README.md)
- **Runbook**: [../docs/05.operations/runbooks/README.md](../docs/05.operations/runbooks/README.md)

## AI Agent Guidance

1. 매니페스트 수정 시 기존 연동된 Azure 리소스(ID, Resource ID 등)가 유효한지 확인한다.
2. 보안 상 중요한 비밀 정보(Secret)는 매니페스트에 직접 커밋하지 않고 Secret Store CSI 드라이버 설정을 사용한다.
3. 리소스 네이밍 및 라벨링 정책을 엄격히 준수한다.
