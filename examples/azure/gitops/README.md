---
title: "Azure GitOps (Platform Manifests)"
version: "1.0.0"
type: "common/readme"
status: "active"
owner: "platform"
updated: "2026-11-20"
---
# Azure GitOps (Platform Manifests)

## 문서 개요

### 목적과 독자

이 README는 examples/azure/gitops의 사용·연결·검사 위치를 찾는 운영자와 기여자를 안내한다. 현재 역할은 [Service](#service)와 [Usage](#usage)에 기록한다.

### 책임과 적용 범위

platform은 examples/azure/gitops의 진입 경로를 유지한다. 이 경로의 파일과 경계는 [Purpose](#purpose), 사용 조건은 [Usage](#usage), 검사는 [Checks](#checks)가 설명한다.

## 내용 계약

### 입력과 전제

입력과 전제는 아래 역할별 본문의 해당 절에 기록한다.

### 본문과 규칙


#### Service

##### Purpose

> 이 경로는 Azure 환경에서 클러스터 전반의 공통 플랫폼 리소스를 GitOps 방식으로 관리하는 매니페스트를 포함한다.

본 디렉토리는 ArgoCD 등을 통해 AKS 클러스터에 클라우드 기반 관리형 플랫폼 리소스를 선언적으로 배포하기 위한 설정 파일을 관리한다. Azure Managed Identity 연동, Gateway API 리소스, 그리고 시크릿 관리 설정을 포함한다.

```text
gitops/
├── platform/    # Managed Identity 연동, AGC Gateway, Secrets Store CSI SecretProviderClass
└── README.md    # 본 문서
```

- [Azure executable example entrypoint](../README.md)

###### Audience

이 README의 주요 독자:

- Platform Engineers
- DevOps Engineers

##### Interfaces

이 문서는 참조 자산의 경계만 다루며 별도의 외부 입출력 계약을 정의하지 않는다.

###### Security Boundary

보안 경계는 Usage > Prerequisites에 적혀 있다.

#### Usage

##### Prerequisites

Azure resource ID와 client ID는 검토된 infrastructure 출력으로만 들어오고
secret 값은 이 manifest에 들어오지 않는다. Managed Identity와 Secret Store CSI
설정을 사용하며 변경은 클러스터를 직접 바꾸지 않고 GitOps pull 모델로 적용한다.

###### Scope

<a id="in-scope"></a>
**In Scope**

- Azure Managed Identity 및 Federated Credential 연동 설정 (platform/dir)
- Azure Application Gateway for Containers (AGC)용 Gateway API 정의
- 클러스터 공통 플랫폼 가동을 위한 컨트롤러 설정 및 헬름 차트 구성

<a id="out-of-scope"></a>
**Out of Scope**

- 일반 애플리케이션 리소스 (kubernetes/ 참조)
- 클라우드 하드 인프라 프로비저닝 (infrastructure/ 참조)
- 클러스터 외부의 수동 운영 작업

##### Selected Start

###### Working Procedure

1. [infrastructure/main.bicep](../infrastructure/main.bicep)에서 생성된 Client ID 등을 매니페스트에 반영한다.
2. 매니페스트 변경은 반드시 GitOps 풀 모델(ArgoCD)을 통해 클러스터에 반영되어야 한다.
3. [Azure example boundary](../README.md)와 현재 Azure 공식 자료를 함께 검토한다.

###### Link Basis

이 README의 링크 기준 위치는 `examples/azure/gitops/`다.

- 같은 폴더의 파일과 하위 경로는 현재 README 위치 기준 상대 링크로 연결한다.
- 상위 저장소 문서나 다른 stage 문서는 필요한 만큼 `../`로 올라가서 연결한다.
- 다른 README의 상대 링크를 그대로 복사하지 말고, 이 파일 위치 기준으로 다시 계산한다.

###### Reference Links

- **Example boundary**: [Azure reference implementation](../README.md)
- **Infrastructure**: [../infrastructure/README.md](../infrastructure/README.md)
- **Repository operations**: GitOps platform runbook (`docs/05.operations/03.runbooks/README.md`)

#### Checks

##### Readiness

리뷰 전에 manifest 문법과 저장소 계약을 검증한다. Azure 리소스, identity,
구독, live AKS 준비 상태를 주장하려면 provider·runtime 증거가 따로 필요하며
이 스냅샷으로는 성립하지 않는다.

##### Failure Handling

이 문서는 참조 전용 예시를 다루며 live 환경을 변경하지 않으므로 관측과 복구 절차가 없다.

###### Runbook Links

runbook 링크는 Selected Start의 Reference Links에 있다.

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
