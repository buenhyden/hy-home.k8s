---
title: "Azure Kubernetes (App Manifests)"
version: "1.0.0"
type: "common/readme"
status: "active"
owner: "platform"
updated: "2026-11-20"
---
# Azure Kubernetes (App Manifests)

## 문서 개요

### 목적과 독자

이 README는 examples/azure/kubernetes의 사용·연결·검사 위치를 찾는 운영자와 기여자를 안내한다. 현재 역할은 [Service](#service)와 [Usage](#usage)에 기록한다.

### 책임과 적용 범위

platform은 examples/azure/kubernetes의 진입 경로를 유지한다. 이 경로의 파일과 경계는 [Purpose](#purpose), 사용 조건은 [Usage](#usage), 검사는 [Checks](#checks)가 설명한다.

## 내용 계약

### 입력과 전제

입력과 전제는 아래 역할별 본문의 해당 절에 기록한다.

### 본문과 규칙


#### Service

##### Purpose

> 이 경로는 AKS 클러스터에서 구동되는 개별 애플리케이션의 Kubernetes 매니페스트를 관리한다.

본 디렉토리는 Azure 배포 환경(AKS 1.35 target)에 최적화된 애플리케이션 매니페스트를 포함한다. 특히 Azure Workload Identity 연동용 Service Account, Secret Store CSI 볼륨 마운트, 리소스 제한 설정(Resource Limit) 및 헬스 체크 설정을 관리한다.

```text
kubernetes/
├── manifests/          # AGC Gateway, External Secrets, 외부 서비스, Workload Identity 매니페스트
├── sample-app.yaml     # Workload Identity 및 CSI가 적용된 샘플 앱
└── README.md           # 본 문서
```

- [Azure executable example entrypoint](../README.md)

###### Audience

이 README의 주요 독자:

- Application Developers
- DevOps Engineers

##### Interfaces

이 문서는 참조 자산의 경계만 다루며 별도의 외부 입출력 계약을 정의하지 않는다.

###### Security Boundary

보안 경계는 Usage > Prerequisites에 적혀 있다.

#### Usage

##### Prerequisites

Workload Identity와 `secrets-store.csi.k8s.io` 참조를 사용하고 Azure
credential이나 secret 값은 커밋하지 않는다. 승격하기 전에 resource request,
limit, label, provider 식별자를 workload profile과 작성 시점이 고정된 migration
명세에 비추어 검토한다.

###### Scope

<a id="in-scope"></a>
**In Scope**

- 개별 마이크로서비스의 Deployment, Service, ConfigMap 매니페스트
- Workload Identity 연동을 위한 전용 Service Account 정의
- Secret Store CSI 드라이버를 통한 외부 시크릿(AKV) 마운트 설정
- 파드 어피니티 및 안티 어피니티 등 스케줄링 전략

<a id="out-of-scope"></a>
**Out of Scope**

- 클러스터 전반의 공통 플랫폼 리소스 (gitops/ platform/ 참조)
- Azure 인프라 리소스 관리 (infrastructure/ 참조)
- 애플리케이션 빌드 파이프라인 (CI)

##### Selected Start

###### Working Procedure

1. [sample-app.yaml](sample-app.yaml)을 템플릿으로 사용하여 새 서비스를 정의한다.
2. 매니페스트 작성 전 [Azure example boundary](../README.md)와 저장소 정책을 확인하고 현재 공식 자료로 재검증한다.
3. 리소스 제한(Requests/Limits)은 실제 워크로드의 프로파일을 바탕으로 설정한다.

###### Link Basis

이 README의 링크 기준 위치는 `examples/azure/kubernetes/`다.

- 같은 폴더의 파일과 하위 경로는 현재 README 위치 기준 상대 링크로 연결한다.
- 상위 저장소 문서나 다른 stage 문서는 필요한 만큼 `../`로 올라가서 연결한다.
- 다른 README의 상대 링크를 그대로 복사하지 말고, 이 파일 위치 기준으로 다시 계산한다.

###### Reference Links

- **Example boundary**: [Azure reference implementation](../README.md)
- **GitOps**: [../gitops/README.md](../gitops/README.md)
- **Infrastructure**: [../infrastructure/main.bicep](../infrastructure/main.bicep)

#### Checks

##### Readiness

리뷰 전에 Kubernetes 문법과 저장소 계약을 검증한다. 이 정적 예시는 live AKS,
Azure Key Vault, Workload Identity, CSI driver의 준비 상태를 증명하지 않는다.

##### Failure Handling

이 문서는 참조 전용 예시를 다루며 live 환경을 변경하지 않으므로 관측과 복구 절차가 없다.

###### Runbook Links

이 문서는 참조 전용 예시를 다루므로 runbook 링크가 없다.

## 적용과 확인

### 적용 방법

아래 역할별 본문에 기록된 사용 조건과 절차를 적용한다.

### 확인 기준

아래 역할별 본문의 검증·확인 조건과 그 한계에 따른다.

## 관계와 출처

### 관련 문서

관련 문서와 정본 링크는 아래 역할별 본문에서 확인한다.

### 외부 근거

외부 근거가 사용된 경우 아래 역할별 본문의 출처와 적용 범위에서 확인한다.
