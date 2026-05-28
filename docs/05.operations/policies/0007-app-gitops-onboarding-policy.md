---
title: '앱 GitOps 온보딩 정책'
type: operation
status: active
owner: platform
updated: 2026-05-22
---

# 앱 GitOps 온보딩 정책

## Overview (KR)

이 문서는 `hy-home.k8s` 클러스터에 새로운 애플리케이션을 온보딩할 때 따라야 하는
플랫폼 운영 정책을 정의한다.

이 정책은 `gitops/workloads/<appname>/`에 새 앱을 추가할 때 필요한 배포 리소스, 네트워킹, 보안, GitOps 워크플로우 통제를 정의한다.

## Current Contract Note

이 정책은 현재 앱 온보딩의 기준 계약이다. 실행 절차는
[GitHub 앱 GitOps 온보딩 가이드](../guides/0008-github-app-gitops-onboarding-guide.md)와
[GitHub 앱 GitOps 온보딩 런북](../runbooks/0010-github-app-gitops-onboarding-runbook.md)이 담당한다.
기존 범용 온보딩 문서(0005 가이드, 0006 런북)는 삭제됐으며
[0008 가이드](../guides/0008-github-app-gitops-onboarding-guide.md)와
[0010 런북](../runbooks/0010-github-app-gitops-onboarding-runbook.md)으로 대체됐다.

## Purpose

`운영 정책 — WSL2 k3d/k3s GitOps 앱 온보딩`

## Policy Scope

- `apps` namespace에 배포되는 신규 애플리케이션 workload
- Argo Rollouts, AnalysisTemplate, ingress-nginx, cert-manager, Istio sidecar/mTLS 패턴
- 앱 단위 Vault/ExternalSecret 연동과 Traefik local dynamic config 연결

## Applies To

- **Systems**: `gitops/workloads/`, `examples/sample-app/`, `gitops/clusters/local/appproject-apps.yaml`
- **Agents**: 문서/운영 자동화 에이전트
- **Environments**: WSL2 local cluster

## Controls

세부 통제는 아래 1-4장에 정의한다. 모든 신규 앱은 Rollout, AnalysisTemplate, 명시적 ingress/TLS, GitOps PR flow, secret/Vault 경계를 따라야 한다.
구체적인 manifest 작성 순서와 검증 명령은 [GitHub 앱 GitOps 온보딩 가이드](../guides/0008-github-app-gitops-onboarding-guide.md)와 [GitHub 앱 GitOps 온보딩 런북](../runbooks/0010-github-app-gitops-onboarding-runbook.md)이 소유한다.

---

## 1. 배포 리소스 정책

### 1-1. Rollout 필수

apps namespace의 모든 워크로드는 `argoproj.io/v1alpha1/Rollout`을 사용해야 한다.
Deployment는 `appproject-apps` whitelist에 포함되어 있으나, 플랫폼 정책상 허용하지 않는다.

**이유**: canary 전략으로 점진적 트래픽 전환과 자동 rollback을 보장하기 위함.

**Required evidence**: `gitops/workloads/<appname>/rollout.yaml`이 존재하고 고정 이미지 태그와 canary 전략을 사용한다.

### 1-2. AnalysisTemplate 필수

모든 Rollout은 canary 단계에서 AnalysisTemplate을 참조해야 한다.

- **Prometheus 주소**: `http://prometheus-external.platform.svc.cluster.local:9090`
- **기본 측정 지표**: `kube_pod_container_status_restarts_total` (컨테이너 재시작 횟수)
- **측정 주기**: 30s, failureLimit: 1
- **Required evidence**: `analysis-template.yaml`이 Rollout canary 단계에서 참조된다.

### 1-3. 이미지 태그

| 항목       | 정책                                                |
| ---------- | --------------------------------------------------- |
| 태그       | 고정 버전 태그 사용 (`v1.0.0`, SHA) — `latest` 금지 |
| 레지스트리 | GitHub Container Registry(`ghcr.io`) 권장           |
| 가시성     | Public 패키지로 설정 (홈랩 환경)                    |

---

## 2. 네트워킹 정책

### 2-1. Istio 포트 명명 규칙

Service의 port 이름은 반드시 `http-` 접두사를 포함해야 한다.

**이유**: Istio가 HTTP 프로토콜로 자동 인식하여 올바른 메트릭과 트레이싱을 수집한다.

### 2-2. Ingress 설정

신규 앱 Ingress는 `ingressClassName: nginx`, `cert-manager.io/cluster-issuer: mkcert-ca-issuer`, `nginx.ingress.kubernetes.io/ssl-redirect: "true"`, `<appname>.127.0.0.1.nip.io` host 계약을 따라야 한다.

### 2-3. Traefik 연동 필수

모든 `*.127.0.0.1.nip.io` 도메인은 외부 Traefik router 설정이 있어야 한다.

- **위치**: `hy-home.docker/infra/01-gateway/traefik/dynamic/<appname>-k3d.yaml`
- **패턴**: `examples/sample-app/traefik-k3d.yaml.example` 참조
- **Required evidence**: 별도 Traefik repo 변경이 리뷰되고 k8s Ingress host와 router rule이 일치한다.

---

## 3. 보안 정책

### 3-1. Istio mTLS

`apps` namespace에 PeerAuthentication STRICT가 적용되어 있다.

- **신규 앱**: 별도 PeerAuthentication 불필요 (namespace 정책 자동 적용)
- **전제**: Pod에 Istio sidecar가 주입되어야 함 (`apps` namespace에 `istio-injection: enabled` 라벨)

### 3-2. NetworkPolicy

현재 `apps` namespace 전체에 egress 정책이 적용된다:

- postgres (172.18.0.15:15432, 15433) egress 허용
- kube-dns egress 허용
- Istiod egress 허용

**신규 외부 서비스 연결 필요 시**: `gitops/platform/network-policies/apps-egress.yaml`에 egress 규칙을 추가하고 Platform 팀(운영자 본인)에 변경 요청한다.

### 3-3. 시크릿 관리

| 항목            | 정책                                                 |
| --------------- | ---------------------------------------------------- |
| 시크릿 저장     | Vault (`secret/apps/<appname>/config`)               |
| k8s Secret 생성 | ExternalSecret(ESO)만 사용, 직접 Secret 생성 금지    |
| 환경변수        | `envFrom.secretRef` 사용 (개별 `env.valueFrom` 지양) |
| Vault 경로 규칙 | `secret/apps/<appname>/config`                       |
| ESO remoteRef   | `apps/<appname>/config` (`secret` mount prefix 제외) |

---

## 4. GitOps 워크플로우 정책

### 4-1. 파일 배치 규칙

`gitops/workloads/<appname>/`는 `apps-generator` 자동 감지 경로다.
필수 파일은 `kustomization.yaml`, `rollout.yaml`, `service.yaml`, `ingress.yaml`, `analysis-template.yaml`이다.
`external-secret.yaml`은 Vault/ESO 연동이 필요한 경우에만 추가한다.

### 4-2. 네이밍 규칙

| 항목        | 규칙                           | 예시                        |
| ----------- | ------------------------------ | --------------------------- |
| `<appname>` | 소문자, 하이픈 구분            | `my-api`                    |
| 도메인      | `<appname>.127.0.0.1.nip.io`   | `my-api.127.0.0.1.nip.io`   |
| TLS Secret  | `<appname>-tls`                | `my-api-tls`                |
| Vault 경로  | `secret/apps/<appname>/config` | `secret/apps/my-api/config` |
| ESO key     | `apps/<appname>/config`        | `apps/my-api/config`        |

### 4-3. 금지 사항

- `kubectl apply`로 직접 클러스터 변경 (human-approved AppProject bootstrap/break-glass 제외)
- `latest` 태그 이미지 사용
- Git 없이 ArgoCD UI에서만 변경
- `namespace: default` 사용 (반드시 `apps` 또는 플랫폼 지정 namespace)

---

## 5. 온보딩 통제 체크리스트

새 앱 온보딩은 아래 정책 게이트를 만족해야 한다. 실행 순서와 체크리스트는 [GitHub 앱 GitOps 온보딩 런북](../runbooks/0010-github-app-gitops-onboarding-runbook.md)이 소유한다.

| Policy Gate        | Required Evidence                                                                                                   | Runbook Owner                                                                                                          |
| ------------------ | ------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| Repository/package | GitHub CI가 ghcr.io 이미지를 발행하고 패키지 가시성이 홈랩 계약에 맞음                                              | [`../runbooks/0010-github-app-gitops-onboarding-runbook.md`](../runbooks/0010-github-app-gitops-onboarding-runbook.md) |
| GitOps manifests   | `rollout.yaml`, `service.yaml`, `ingress.yaml`, `analysis-template.yaml`, `kustomization.yaml`이 필수 계약을 만족함 | [`../runbooks/0010-github-app-gitops-onboarding-runbook.md`](../runbooks/0010-github-app-gitops-onboarding-runbook.md) |
| Network/TLS        | `http-` port naming, `ingressClassName=nginx`, `mkcert-ca-issuer`, nip.io hostname이 적용됨                         | [`../runbooks/0010-github-app-gitops-onboarding-runbook.md`](../runbooks/0010-github-app-gitops-onboarding-runbook.md) |
| External routing   | 외부 Traefik dynamic config가 별도 Traefik repo에서 리뷰되고 k8s Ingress 계약과 일치함                              | [`../runbooks/0010-github-app-gitops-onboarding-runbook.md`](../runbooks/0010-github-app-gitops-onboarding-runbook.md) |
| Secret handling    | 필요한 경우 Vault/ESO를 사용하고 plaintext Kubernetes Secret manifest가 없음                                        | [`../runbooks/0010-github-app-gitops-onboarding-runbook.md`](../runbooks/0010-github-app-gitops-onboarding-runbook.md) |
| Runtime health     | ArgoCD Application, Rollout, Pod readiness, Ingress/TLS 접근 증적이 남음                                            | [`../runbooks/0010-github-app-gitops-onboarding-runbook.md`](../runbooks/0010-github-app-gitops-onboarding-runbook.md) |

---

## Exceptions

- `kubectl apply` 또는 AppProject live 반영은 human-approved bootstrap/break-glass 상황에서만 허용한다.
- ExternalSecret이 필요 없는 앱은 Vault 연동 파일을 생략할 수 있지만, plaintext Kubernetes Secret manifest는 허용하지 않는다.

## Verification

- 정적 검증 증적: GitOps 구조, k8s manifest, secret-handling 검증이 통과해야 한다.
- 런타임 증적: 온보딩 후 ArgoCD Application `Synced/Healthy`, Rollout `Healthy`, Pod `2/2 Running`, Ingress TLS 발급 상태를 확인한다.
- 실행 가능한 검증 명령과 실패 시 복구 절차는 [GitHub 앱 GitOps 온보딩 런북](../runbooks/0010-github-app-gitops-onboarding-runbook.md)을 따른다.

## Review Cadence

- 새 앱 온보딩 또는 `examples/sample-app/` 변경 시마다 검토한다.
- Rollouts, Istio, cert-manager, Vault/ESO 계약 변경 시 관련 guide/runbook과 함께 검토한다.

## AI Agent Policy Section (If Applicable)

이 정책은 인프라 리소스를 직접 관리하며 AI Agent 모델/프롬프트/평가 정책이 별도 적용되지 않는다.
단, Agent가 이 정책 범위의 리소스를 조작할 경우 [운영 거버넌스](../../00.agent-governance/README.md)에 따른다.

## Related Documents

- **Guide**: [`../guides/0008-github-app-gitops-onboarding-guide.md`](../guides/0008-github-app-gitops-onboarding-guide.md)
- **Runbook**: [`../runbooks/0010-github-app-gitops-onboarding-runbook.md`](../runbooks/0010-github-app-gitops-onboarding-runbook.md)
- **예시 템플릿**: [`../../../examples/sample-app`](../../../examples/sample-app)
- **참조 구현**: [`../../../gitops/workloads/adminer`](../../../gitops/workloads/adminer)
- **AppProject**: [`../../../gitops/clusters/local/appproject-apps.yaml`](../../../gitops/clusters/local/appproject-apps.yaml)
- **NetworkPolicy**: [`../../../gitops/platform/network-policies/apps-egress.yaml`](../../../gitops/platform/network-policies/apps-egress.yaml)
