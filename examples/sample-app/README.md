---
title: "sample-app"
version: "1.0.0"
type: "common/readme"
status: "active"
owner: "platform"
updated: "2026-11-20"
---
# sample-app

## 문서 개요

### 목적과 독자

이 README는 examples/sample-app의 사용·연결·검사 위치를 찾는 운영자와 기여자를 안내한다. 현재 역할은 [Service](#service)와 [Usage](#usage)에 기록한다.

### 책임과 적용 범위

platform은 examples/sample-app의 진입 경로를 유지한다. 이 경로의 파일과 경계는 [Purpose](#purpose), 사용 조건은 [Usage](#usage), 검사는 [Checks](#checks)가 설명한다.

## 내용 계약

### 입력과 전제

입력과 전제는 아래 역할별 본문의 해당 절에 기록한다.

### 본문과 규칙


#### Service

##### Purpose

> 새 애플리케이션을 `hy-home.k8s` GitOps 경로에 온보딩할 때 사용하는 최소 템플릿 예시다.

이 디렉터리는 `hy-home.k8s` 클러스터에 새로운 앱을 온보딩할 때 참조하는 최소 GitOps 템플릿이다. Rollout, Service, Ingress, AnalysisTemplate, ExternalSecret 예시를 함께 제공해 앱별 manifest 세트를 빠르게 만들 수 있게 한다. stable/canary Service와 Istio routing까지 포함한 fuller active reference는 `gitops/workloads/adminer/`를 기준으로 확인한다.

예시는 feature branch + PR flow를 전제로 한다. `main`에 직접 반영하는 흐름은 저장소 운영 정책과 quality gate에서 허용하지 않는다.

복사된 디렉터리는 `<appname>`, `<owner>`, `<tag>`, `<port>` placeholder를 모두 교체하고 정적 검증을 통과하기 전까지 active GitOps desired state로 간주하지 않는다. ExternalSecret 예시는 ESO `remoteRef.key` 규칙만 보여 주며 secret values를 문서나 manifest에 쓰지 않는다.

```text
examples/sample-app/
├── kustomization.yaml        # Kustomize 진입점
├── rollout.yaml              # Argo Rollout (canary 전략)
├── service.yaml              # Service (Istio http- 포트 명명 규칙)
├── ingress.yaml              # Ingress (nginx + cert-manager mkcert TLS)
├── analysis-template.yaml    # AnalysisTemplate (Prometheus 재시작 검사)
└── external-secret.yaml      # ExternalSecret (OpenBao 연동, 선택 사항)
```

- 참조 구현: [`../../gitops/workloads/adminer`](../../gitops/workloads/adminer)

###### Audience

이 README의 주요 독자:

- Application Developers
- Operators
- Documentation Writers

##### Interfaces

- Policy: `../../docs/05.operations/policies/README.md` (`docs/05.operations/02.policies/README.md`)

###### Security Boundary

보안 경계는 Usage > Prerequisites에 적혀 있다.

#### Usage

##### Prerequisites

`gitops/workloads/<appname>/`로 올리기 전에 `<appname>`, `<owner>`, `<tag>`,
`<port>` placeholder를 모두 바꾼다. secret 값, 토큰, 개인 키는 예시 밖에 두고
아래에 설명한 Vault mount-prefix 경계를 지킨다.

###### Scope

<a id="in-scope"></a>
**In Scope**

- 앱별 GitOps manifest 템플릿
- placeholder 치환 방식
- Argo Rollouts, ESO, Ingress, AnalysisTemplate 구성 예시
- k8s 전용 router가 받는 `<appname>.hy-k8s.home.arpa` host 계약

<a id="out-of-scope"></a>
**Out of Scope**

- 실제 애플리케이션 소스 코드
- live cluster에 직접 리소스를 적용하는 절차
- production secret 값 또는 credential 예시
- AWS/Azure cloud target 구현

###### 현재 플랫폼 전제 조건

- `apps` namespace에 `PeerAuthentication STRICT` 적용 중 → Istio mTLS 강제
- `apps` namespace NetworkPolicy → postgres(host `192.168.0.13:15432/15433`, ADR-0046) egress 허용
- ExternalSecret 사용 시 Vault CLI 경로는 `secret/apps/<appname>/config`지만,
  `vault-backend` ClusterSecretStore의 `path: secret` 설정 때문에
  `remoteRef.key`는 `apps/<appname>/config` 형식을 사용한다.
- `remoteRef.key`는 Vault mount prefix를 제외한 key convention만 기록하며,
  secret values, token, private key는 예시 manifest나 README에 남기지 않는다.
- `traefik`에 Istio sidecar 주입 → mTLS 체인 완성
- AnalysisTemplate이 Prometheus API(`https://prometheus.hy.home.arpa`)에 접근 필요. Basic Auth header는 platform이 관리하는 `apps/prometheus-api-auth` Secret에서 읽는다 (ADR-0046)

##### Selected Start

###### Working Procedure

###### 1. 플레이스홀더 교체

파일 내 `<appname>`, `<owner>`, `<tag>`, `<port>`를 실제 값으로 교체한다.
placeholder가 남은 상태의 파일은 `gitops/workloads/<appname>` active 경로에 커밋하지 않는다.

| 플레이스홀더 | 설명                     | 예시        |
| ------------ | ------------------------ | ----------- |
| `<appname>`  | 앱 이름 (소문자, 하이픈) | `my-api`    |
| `<owner>`    | GitHub 사용자명/조직명   | `buenhyden` |
| `<tag>`      | 컨테이너 이미지 태그     | `v1.2.3`    |
| `<port>`     | 앱 listen 포트           | `8080`      |

###### 2. workloads 디렉토리에 복사

```bash
cp -r examples/sample-app gitops/workloads/<appname>
# 플레이스홀더 일괄 교체
sed -i 's/<appname>/my-api/g; s/<owner>/buenhyden/g; s/<tag>/v1.0.0/g; s/<port>/8080/g' \
  gitops/workloads/<appname>/*.yaml
```

###### 3. 접속 이름 확인

`<appname>.hy-k8s.home.arpa`는 k8s 전용 router(`192.168.0.14`)가 받는다. 외부
저장소 변경 없이 이름 해석만 그 주소를 가리키면 된다.

###### 4. feature branch + PR flow로 반영

```bash
git checkout -b feat/<appname>-gitops
git add gitops/workloads/<appname>/
git commit -m "feat: add <appname> to GitOps"
git push origin feat/<appname>-gitops
```

PR review 후 `main`에 병합되면 ArgoCD `apps-generator` ApplicationSet이 자동으로 Application을 생성하고 배포한다.

###### Link Basis

이 README의 링크 기준 위치는 `examples/sample-app/`다.

- 같은 폴더의 파일과 하위 경로는 현재 README 위치 기준 상대 링크로 연결한다.
- 상위 저장소 문서나 다른 stage 문서는 필요한 만큼 `../`로 올라가서 연결한다.
- 다른 README의 상대 링크를 그대로 복사하지 말고, 이 파일 위치 기준으로 다시 계산한다.

#### Checks

##### Readiness

복사본을 desired state로 다루기 전에 placeholder가 남지 않았는지 확인하고
상위 [examples contract](../README.md#checks)에 나열된 저장소 품질,
Kubernetes manifest, secret 처리 검사를 실행한다.

##### Failure Handling

이 문서는 참조 전용 예시를 다루며 live 환경을 변경하지 않으므로 관측과 복구 절차가 없다.

###### Runbook Links

- Runbook: `../../docs/05.operations/runbooks/README.md` (`docs/05.operations/03.runbooks/README.md`)

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
