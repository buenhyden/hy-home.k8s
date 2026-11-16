---
title: "앱 GitOps 온보딩 정책"
version: "1.6.1"
type: "operation/policy"
status: "active"
owner: "platform"
updated: "2026-11-16"
artifact_id: "POL-0007"
---

# 앱 GitOps 온보딩 정책

## Purpose

### Objective

이 문서는 `hy-home.k8s` 클러스터에 새로운 애플리케이션을 온보딩할 때 따라야 하는
플랫폼 운영 정책을 정의한다.

이 정책은 `gitops/workloads/<appname>/`에 새 앱을 추가할 때 필요한 배포 리소스, 네트워킹, 보안, GitOps 워크플로우 통제를 정의한다.

이 정책은 현재 앱 온보딩의 기준 계약이다. 실행 순서와 검증·복구 절차는
[GitHub 앱 GitOps 온보딩 런북](../runbooks/0010-github-app-gitops-onboarding-runbook.md)이 담당한다.

### Authority

별도 상위 권위 문서 목록은 없으며, 인용된 ADR은 아래 Requirements의 각 통제 본문에 있다.

## Scope

### Applies To

- `apps` namespace에 배포되는 신규 애플리케이션 workload
- Argo Rollouts, AnalysisTemplate, Traefik, cert-manager, Istio sidecar/mTLS 패턴
- 앱 단위 OpenBao/ExternalSecret 연동과 k8s router host 계약

- **Systems**: `gitops/workloads/`, `examples/sample-app/`, `gitops/clusters/local/appproject-apps.yaml`
- **Agents**: 문서/운영 자동화 에이전트
- **Environments**: Linux server local cluster

### Exclusions

이 정책은 Applies To에 적은 범위에서 제외하는 항목을 따로 두지 않으며, bootstrap과 break-glass 예외는 제외가 아니라 Exception Conditions가 가리키는 POL-0001의 공통 예외를 따른다. 제외할 항목이 생기면 그 항목과 담당 문서를 여기에 적는다.

## Rules

### Requirements

| Rule ID | Condition | Level | Evidence | Status |
| --- | --- | --- | --- | --- |
| ONBOARD-R001 | Always | required | RUN-0010 | active |
| ONBOARD-R002 | Always | required | RUN-0010 | active |
| ONBOARD-R003 | Always | required | RUN-0010 | active |
| ONBOARD-R004 | Always | required | 의미 검토 | active |
| ONBOARD-R005 | Always | required | policy-gates | active |
| ONBOARD-R006 | Always | required | policy-gates | active |
| ONBOARD-R007 | Always | recommended | RUN-0010 | active |
| ONBOARD-R008 | Always | required | 의미 검토 | active |
| ONBOARD-R009 | Always | required | 의미 검토 | active |
| ONBOARD-R010 | Always | required | RUN-0010 | active |
| ONBOARD-R011 | Always | required | RUN-0010 | active |
| ONBOARD-R012 | Always | required | RUN-0010 | active |
| ONBOARD-R013 | `hy-k8s.home.arpa/<appname>` 진입이 필요하면 | optional | RUN-0010 | active |
| ONBOARD-R014 | Always | required | RUN-0010 | active |
| ONBOARD-R015 | Always | required | RUN-0010 | active |
| ONBOARD-R016 | adminer를 제거하거나 이동하는 변경일 때 | required | RUN-0010 | active |
| ONBOARD-R017 | Always | required | RUN-0010 | active |
| ONBOARD-R018 | 신규 외부 서비스 연결이 필요할 때 | required | 의미 검토 | active |
| ONBOARD-R019 | management/development PostgreSQL 연결이 필요하면 | required | 의미 검토 | active |
| ONBOARD-R020 | Always | required | 의미 검토 | active |
| ONBOARD-R021 | Always | required | 의미 검토 | active |
| ONBOARD-R022 | Always | required | 의미 검토 | active |
| ONBOARD-R023 | Always | required | 의미 검토 | active |
| ONBOARD-R024 | Always | required | RUN-0010 | active |
| ONBOARD-R025 | Always | required | policy-gates | active |
| ONBOARD-R026 | Always | recommended | RUN-0010 | active |
| ONBOARD-R027 | Always | required | RUN-0010 | active |
| ONBOARD-R028 | Always | required | RUN-0010 | active |
| ONBOARD-R029 | Always | required | RUN-0010 | active |
| ONBOARD-R030 | Always | required | RUN-0010 | active |
| ONBOARD-R031 | Always | required | RUN-0010 | active |
| ONBOARD-R032 | Always | required | RUN-0010 | active |
| ONBOARD-R033 | Always | required | RUN-0010 | active |
| ONBOARD-R034 | Always | required | RUN-0010 | active |
| ONBOARD-R035 | Always | required | 의미 검토 | active |
| ONBOARD-R036 | Always | required | policy-gates | active |
| ONBOARD-R037 | Always | required | 의미 검토 | active |
| ONBOARD-R038 | Always | required | 의미 검토 | active |
| ONBOARD-R039 | 새 앱을 온보딩할 때 | required | RUN-0010 | active |
| ONBOARD-R040 | Always | required | RUN-0010 | active |
| ONBOARD-R041 | Always | required | RUN-0010 | active |
| ONBOARD-R042 | Always | required | RUN-0010 | active |
| ONBOARD-R043 | Always | required | RUN-0010 | active |
| ONBOARD-R044 | Always | required | RUN-0010 | active |
| ONBOARD-R045 | Always | required | RUN-0010 | active |

세부 통제는 아래 1-5장에 정의한다. 모든 신규 앱은 Rollout, AnalysisTemplate, 명시적 ingress/TLS, GitOps PR flow, secret/OpenBao 경계를 따라야 한다.

---

#### 1. 배포 리소스 정책



#### 1-1. Rollout 필수

`ONBOARD-R001`

apps namespace의 모든 워크로드는 `argoproj.io/v1alpha1/Rollout`을 사용해야 한다.
Deployment는 현재 `appproject-apps` namespaceResourceWhitelist에 포함되지 않으며, 플랫폼 정책상 신규 앱은 Rollout을 사용한다.

**이유**: canary와 분석 게이트로 단계적 전환과 실패 시 중단·복구 경로를
제공하기 위함이다. 실제 rollback의 성공은 해당 Rollout의 운영 증거로 판정한다.

**Required evidence**: `gitops/workloads/<appname>/rollout.yaml`이 존재하고 고정 이미지 태그와 canary 전략을 사용한다.

#### 1-2. AnalysisTemplate 필수

`ONBOARD-R002`

모든 Rollout은 canary 단계에서 AnalysisTemplate을 참조해야 한다.

- `ONBOARD-R003` **Prometheus 주소**: `https://prometheus.hy.home.arpa`. `Authorization` header는
  `args`의 `secretKeyRef`로 platform 소유 `apps/prometheus-api-auth` Secret에서 읽는다(ADR-0046).
- `ONBOARD-R004` **기본 측정 지표**: `kube_pod_container_status_restarts_total` (컨테이너 재시작 횟수)
- `ONBOARD-R005` **측정 주기**: 30s, `count: 4`(유한한 canary step 측정), failureLimit: 1
- **Required evidence**: `analysis-template.yaml`이 Rollout canary 단계에서 참조된다.

#### 1-3. 이미지 태그

| 항목       | 정책                                                |
| ---------- | --------------------------------------------------- |
| `ONBOARD-R006` 태그       | 고정 버전 태그 사용 (`v1.0.0`, SHA) — `latest` 금지 |
| `ONBOARD-R007` 레지스트리 | GitHub Container Registry(`ghcr.io`) 권장           |
| `ONBOARD-R008` 가시성     | Public 패키지로 설정 (홈랩 환경)                    |

---

#### 2. 네트워킹 정책



#### 2-1. Istio 포트 명명 규칙

`ONBOARD-R009`

Service의 port 이름은 반드시 `http-` 접두사를 포함해야 한다.

**이유**: Istio가 HTTP 프로토콜로 자동 인식하여 올바른 메트릭과 트레이싱을 수집한다.

#### 2-2. Ingress 설정

`ONBOARD-R010`

신규 앱 Ingress는 `ingressClassName: nginx`, `cert-manager.io/cluster-issuer: mkcert-ca-issuer`, `nginx.ingress.kubernetes.io/ssl-redirect: "true"`, `<appname>.hy-k8s.home.arpa` host 계약을 따라야 한다.
`nginx` class는 Traefik의 Ingress-NGINX provider가 처리하는 호환 class이며, 은퇴한 ingress-nginx controller를 뜻하지 않는다([ADR-0050](../../02.architecture/decisions/0050-ingress-nginx-replacement-with-traefik.md)).

#### 2-3. k8s router 경로

`ONBOARD-R011`

`*.hy-k8s.home.arpa` 도메인은 k8s 전용 router가 받으므로 외부 저장소 변경이 필요 없다.

- `ONBOARD-R012` **공통 router 통제**: [POL-0001](./0001-k8s-gitops-operations-policy.md)의 ingress/TLS 통제
- `ONBOARD-R013` **apex path(선택)**: `hy-k8s.home.arpa/<appname>` 진입이 필요하면 `gitops/platform/ingress-routes/apex-redirects.yaml`에 같은 형식의 redirect Ingress를 추가하고 `scripts/validate-infrastructure-contracts.sh`의 앱 목록을 함께 갱신한다.
- **Required evidence**: 앱 Ingress host가 `<appname>.hy-k8s.home.arpa`이고, 이름 해석이 k8s router 주소 `192.168.0.14`를 가리킨다.

---

#### 3. 보안 정책



#### 3-1. Istio mTLS

`ONBOARD-R014`

`apps` namespace의 GitOps 목표 상태는 PeerAuthentication STRICT다.

- `ONBOARD-R015` **신규 앱**: 별도 PeerAuthentication 불필요 (namespace 정책 자동 적용)
- `ONBOARD-R016` **현재 소유 위치**: namespace 전체 STRICT `PeerAuthentication default`는
  [adminer의 PeerAuthentication 매니페스트](../../../gitops/workloads/adminer/peer-authentication.yaml)가 선언한다.
  adminer를 제거하거나 이동하는 변경은 이 리소스를 먼저 platform 소유로
  옮겨야 하며, 그렇지 않으면 `apps` 전체의 STRICT mTLS가 함께 사라진다.
- `ONBOARD-R017` **전제**: Pod에 Istio sidecar가 주입되어야 함 (`apps` namespace에 `istio-injection: enabled` 라벨)

#### 3-2. NetworkPolicy

`ONBOARD-R018`

GitOps의 [`allow-egress-apps` 정책](../../../gitops/platform/network-policies/apps-egress.yaml)은 `apps` namespace 전체에 다음 egress 경계를 선언한다.

- `ONBOARD-R019` 현재 앱 egress에 폐기된 `postgres-ha` `15432/15433` 허용은 없다.
  management/development PostgreSQL은 host loopback 전용이므로 현재 K8s
  앱의 DB 연결 대상이 아니다. 연결이 필요하면 서비스 노출, 인증/Secret,
  NetworkPolicy와 운영 권한을 별도 검토한다
- `ONBOARD-R020` Istio sidecar trace용 외부 Alloy OTLP(host `192.168.0.13:4317`) egress 허용
- `ONBOARD-R021` kube-dns egress 허용
- `ONBOARD-R022` Istiod(`15010`, `15012`, `15014`) egress 허용
- `ONBOARD-R023` cluster pod CIDR(`10.42.0.0/16`) egress 허용 (in-cluster mTLS 통신)

**신규 외부 서비스 연결 필요 시**: `gitops/platform/network-policies/apps-egress.yaml`에 egress 규칙을 추가하고 Platform 팀(운영자 본인)에 변경 요청한다.

#### 3-3. 시크릿 관리

| 항목            | 정책                                                 |
| --------------- | ---------------------------------------------------- |
| `ONBOARD-R024` 시크릿 저장     | OpenBao (`secret/apps/<appname>/config`)             |
| `ONBOARD-R025` k8s Secret 생성 | ExternalSecret(ESO)만 사용, 직접 Secret 생성 금지    |
| `ONBOARD-R026` 환경변수        | `envFrom.secretRef` 사용 (개별 `env.valueFrom` 지양) |
| `ONBOARD-R027` OpenBao 경로 규칙 | `secret/apps/<appname>/config`                     |
| `ONBOARD-R028` ESO remoteRef   | `apps/<appname>/config` (`secret` mount prefix 제외) |

---

#### 4. GitOps 워크플로우 정책



#### 4-1. 파일 배치 규칙

`ONBOARD-R029`

`gitops/workloads/<appname>/`는 `apps-generator` 자동 감지 경로다.
필수 파일은 `kustomization.yaml`, `rollout.yaml`, `service.yaml`, `ingress.yaml`, `analysis-template.yaml`이다.
`external-secret.yaml`은 OpenBao/ESO 연동이 필요한 경우에만 추가한다.

#### 4-2. 네이밍 규칙

| 항목        | 규칙                           | 예시                        |
| ----------- | ------------------------------ | --------------------------- |
| `ONBOARD-R030` `<appname>` | 소문자, 하이픈 구분            | `my-api`                    |
| `ONBOARD-R031` 도메인      | `<appname>.hy-k8s.home.arpa`   | `my-api.hy-k8s.home.arpa`   |
| `ONBOARD-R032` TLS Secret  | `<appname>-tls`                | `my-api-tls`                |
| `ONBOARD-R033` OpenBao 경로 | `secret/apps/<appname>/config` | `secret/apps/my-api/config` |
| `ONBOARD-R034` ESO key     | `apps/<appname>/config`        | `apps/my-api/config`        |

#### 4-3. 금지 사항

- `ONBOARD-R035` `kubectl apply`로 직접 클러스터 변경 (operator-approved AppProject bootstrap/break-glass 제외)
- `ONBOARD-R036` `latest` 태그 이미지 사용
- `ONBOARD-R037` Git 없이 ArgoCD UI에서만 변경
- `ONBOARD-R038` `namespace: default` 사용 (반드시 `apps` 또는 플랫폼 지정 namespace)

---

#### 5. 온보딩 통제 체크리스트

`ONBOARD-R039`

새 앱 온보딩은 아래 정책 게이트를 만족해야 한다. 실행 순서와 체크리스트는 [GitHub 앱 GitOps 온보딩 런북](../runbooks/0010-github-app-gitops-onboarding-runbook.md)이 소유한다.

| Policy Gate        | Required Evidence                                                                                                   | Runbook Owner                                                                                                          |
| ------------------ | ------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| `ONBOARD-R040` Repository/package | GitHub CI가 ghcr.io 이미지를 발행하고 패키지 가시성이 홈랩 계약에 맞음                                              | [`../runbooks/0010-github-app-gitops-onboarding-runbook.md`](../runbooks/0010-github-app-gitops-onboarding-runbook.md) |
| `ONBOARD-R041` GitOps manifests   | `rollout.yaml`, `service.yaml`, `ingress.yaml`, `analysis-template.yaml`, `kustomization.yaml`이 필수 계약을 만족함 | [`../runbooks/0010-github-app-gitops-onboarding-runbook.md`](../runbooks/0010-github-app-gitops-onboarding-runbook.md) |
| `ONBOARD-R042` Network/TLS        | `http-` port naming, `ingressClassName=nginx`, `mkcert-ca-issuer`, hy-k8s.home.arpa hostname이 적용됨                         | [`../runbooks/0010-github-app-gitops-onboarding-runbook.md`](../runbooks/0010-github-app-gitops-onboarding-runbook.md) |
| `ONBOARD-R043` External routing   | 앱 host가 k8s router로 해석되고, apex path가 필요하면 redirect Ingress가 추가됨                                     | [`../runbooks/0010-github-app-gitops-onboarding-runbook.md`](../runbooks/0010-github-app-gitops-onboarding-runbook.md) |
| `ONBOARD-R044` Secret handling    | 필요한 경우 OpenBao/ESO를 사용하고 plaintext Kubernetes Secret manifest가 없음                                        | [`../runbooks/0010-github-app-gitops-onboarding-runbook.md`](../runbooks/0010-github-app-gitops-onboarding-runbook.md) |
| `ONBOARD-R045` Runtime health     | 명명된 앱의 ArgoCD Application, Rollout, 실제 Pod ready/desired 수, Ingress/TLS 접근 증적이 남음                         | [`../runbooks/0010-github-app-gitops-onboarding-runbook.md`](../runbooks/0010-github-app-gitops-onboarding-runbook.md) |

---

### Enforcement

- 정적 검증 증적: GitOps 구조, k8s manifest, secret-handling 검증이 통과해야 한다.
- 런타임 증적: 승인된 온보딩 후 명명된 ArgoCD Application의 `Synced/Healthy`, Rollout 상태, 실제 Pod ready/desired 컨테이너 수와 Ingress TLS 상태를 확인한다. 현재 sample의 `2/2`를 모든 새 앱의 고정 컨테이너 수로 취급하지 않는다.
- 실행 가능한 검증 명령과 실패 시 복구 절차는 [GitHub 앱 GitOps 온보딩 런북](../runbooks/0010-github-app-gitops-onboarding-runbook.md)을 따른다.

- 새 앱 온보딩 또는 `examples/sample-app/` 변경 시마다 검토한다.
- Rollouts, Istio, cert-manager, OpenBao/ESO 계약 변경 시 관련 policy/runbook과 함께 검토한다.
- [REQ-0004 workload 온보딩 시나리오](../../01.requirements/0004-current-local-gitops-platform.md#quality-scenario-workload-onboarding)가
  적용 가능한 정적 통제의 판정식·표본·목표와 운영 관측의 별도 결정을 소유한다.
  이 정책의 adminer 분석 주기와 canary 설정은 현재 구성 예시이며 새 앱의
  보편적인 가용성 목표가 아니다.

- **Runbook**: [`../runbooks/0010-github-app-gitops-onboarding-runbook.md`](../runbooks/0010-github-app-gitops-onboarding-runbook.md)
- **예시 템플릿**: [`../../../examples/sample-app`](../../../examples/sample-app)
- **참조 구현**: [`../../../gitops/workloads/adminer`](../../../gitops/workloads/adminer)
- **AppProject**: [`../../../gitops/clusters/local/appproject-apps.yaml`](../../../gitops/clusters/local/appproject-apps.yaml)
- **NetworkPolicy**: [`../../../gitops/platform/network-policies/apps-egress.yaml`](../../../gitops/platform/network-policies/apps-egress.yaml)

## Exceptions

### Exception Conditions

- `kubectl apply` 또는 AppProject live 반영은 [POL-0001](./0001-k8s-gitops-operations-policy.md#exceptions)의 operator-approved bootstrap/break-glass 공통 예외를 따른다.
- ExternalSecret이 필요 없는 앱은 OpenBao 연동 파일을 생략할 수 있지만, plaintext Kubernetes Secret manifest는 허용하지 않는다.

### Approval and Review

예외 승인은 위 Exception Conditions가 가리키는 POL-0001의 operator-approved bootstrap/break-glass 공통 예외를 따른다.

## Ownership

### Responsibilities

책임 주체는 아래 Lifecycle Traceability 표의 Control owner 열에 적혀 있다.

### Change and Adoption

변경 검토 시점은 위 Enforcement의 새 앱 온보딩 및 계약 변경 시 검토 항목을 따른다.

### Lifecycle Traceability

| Promoted owner | Control owner | Enforcement surface |
| --- | --- | --- |
| N/A — the app-onboarding policy is promoted from the current sample/adminer patterns and operations workflow, with no eligible upstream document available to link as the promoting owner | Platform Owner for workload admission and AppProject exceptions; application owner for image, rollout, and runtime evidence | required Rollout/AnalysisTemplate manifests, fixed image tags, ingress/TLS and Istio contracts, OpenBao/ESO boundary, PR review, and GitOps/manifest/secret validation gates |
