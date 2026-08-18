---
title: 'Reference: Pod Security Compliance Inventory'
type: content/reference
status: active
owner: platform
updated: 2026-08-18
---

# Pod Security Compliance Inventory

## Overview

이 문서는 `hy-home.k8s`가 배포하는 모든 워크로드를 Kubernetes Pod Security
Standards의 **Baseline**과 **Restricted** 프로파일에 대해 판정한 인벤토리다.
[ADR 0024](../../02.architecture/decisions/0024-pod-security-standards-staged-adoption.md)가
"Helm 소유 네임스페이스의 준수 여부는 조사되지 않았다"고 명시적으로 남긴 공백을 채운다.

### Purpose

PSS 라벨을 붙이기 전에 무엇이 통과하고 무엇이 걸리는지 알기 위한 것이다. 판정은
차트 기본값이 아니라 **이 저장소가 실제로 설치하는 구성** 기준이며, 그 차이가
결과를 바꾸는 사례가 실제로 하나 있다.

### 핵심 결과

**26개 워크로드 전부가 Baseline을 통과한다.** 이 플랫폼에서 Baseline을 위반하는
것은 차트도 워크로드도 아니고, Istio가 `apps`와 `ingress-nginx`의 pod에 주입하는
`istio-init` init container 하나뿐이다.

**Restricted 미달은 남지 않았다.** 조사 시점의 6건은 모두 이 저장소의 values와
매니페스트로 닫혔다. 마지막 `adminer`는 이미지 `/etc/passwd`를 직접 읽어 UID 999를
확인한 뒤 `runAsUser`/`runAsNonRoot`를 함께 적용해 커플링을 해소했다. `seccompProfile`은 Restricted에만 있고 Baseline에는 없는 통제라, 잘
하드닝된 것처럼 보이는 워크로드가 정확히 여기서 갈린다.

## Reference Type

- Type: platform-compliance-inventory / external-standard-snapshot
- Source checked: 2026-08-18
- Evidence class: `repo-static` + 로컬 `helm template` 렌더링. 라이브 admission
  결과가 아니다.
- Refresh trigger: 차트 버전 변경, Application `helm.values` 변경, 저장소 저작
  워크로드의 `securityContext` 변경, 또는 PSS 프로파일 정의 자체의 변경.

## Authority Boundary

- **Authoritative for**:
  - 아래 `Definitions / Facts`에 기록된 워크로드별 Baseline/Restricted 판정.
  - 각 Restricted 실패의 차단 사유와 values 키를 통한 해결 경로.
- **Not authoritative for**:
  - 라이브 클러스터의 실제 admission 결과. PSA는 클러스터의 `enforce-version`에
    따라 세부 판정이 달라질 수 있고, 이 문서는 어떤 클러스터도 접촉하지 않았다.
  - PSS 도입 여부와 순서. 그것은 ADR 0024가 소유한다.
  - Kiali operand(Kiali 서버) pod spec. operator가 런타임에 생성하므로 차트
    기본값 범위 밖이다.
  - cert-manager ACME HTTP-01 solver pod. controller가 런타임에 생성한다.
  - 워크로드에 사이드카가 주입된 뒤의 최종 pod spec. Istio 주입 결과는
    `istio-cni-adoption-evaluation.md`가 다룬다.

## Scope

대상은 `gitops/`가 선언하는 9개 네임스페이스와, GitOps 밖에서 bootstrap이 직접
설치하는 `argocd` 네임스페이스다.

판정 방법은 두 갈래다. 저장소가 pod spec을 저작하는 워크로드는 매니페스트를 직접
읽었고, Helm 차트가 소유하는 워크로드는 **이 저장소의 `helm.values` 재정의를
적용한 상태로** 차트를 로컬 렌더링했다.

`platform` 네임스페이스는 pod을 하나도 갖지 않아(Service 9, EndpointSlice 9,
NetworkPolicy 6) 판정 대상이 없다. Istio `base` 차트도 CRD/RBAC/webhook만
배포하고 워크로드를 만들지 않는다.

## Definitions / Facts

### 네임스페이스별 소유권

| 네임스페이스       | 소유             | 워크로드 수  | Istio 주입  |
| ------------------ | ---------------- | ------------ | ----------- |
| `monitoring`       | 저장소 저작      | 2            | disabled    |
| `apps`             | 저장소 저작      | 1            | **enabled** |
| `platform`         | 저장소 저작      | 0 (pod 없음) | —           |
| `cert-manager`     | Helm             | 4            | —           |
| `external-secrets` | Helm             | 3            | —           |
| `ingress-nginx`    | Helm             | 3            | **enabled** |
| `istio-system`     | Helm             | 2            | —           |
| `argo-rollouts`    | Helm             | 2            | —           |
| `argocd`           | Helm (GitOps 밖) | 10           | —           |

### Baseline 판정

| 대상                                   | 결과     |
| -------------------------------------- | -------- |
| 26개 워크로드 전부                     | **PASS** |
| Istio `istio-init` 주입 init container | **FAIL** |

`istio-init`은 `NET_ADMIN`과 `NET_RAW`를 `capabilities.add`에 넣는다. Baseline의
capabilities 통제는 `spec.initContainers[*].securityContext.capabilities.add`를
포함하고 허용 목록에 그 둘이 없다. 이 위반은 `apps`와 `ingress-nginx`의 모든
주입 pod에 적용된다.

**이 위반은 istio-cni 도입으로 제거되었다.** `platform-istio-cni` Application과
`pilot.cni.enabled: true`가 함께 반영되면 주입 init container가
`istio-validation`으로 바뀌며, 그 컨테이너는 `capabilities.add`를 갖지 않는다.

대신 새로운 Baseline 예외가 하나 생긴다. `istio-cni-node` DaemonSet은 노드마다
`NET_ADMIN`, `NET_RAW`, `SYS_PTRACE`, `SYS_ADMIN`, `DAC_OVERRIDE`와 `/proc`
hostPath를 요구하므로 Baseline을 만족할 수 없다. 이는 설계상 의도된 것으로,
**트래픽을 서비스하는 2개 네임스페이스의 예외가 트래픽을 서비스하지 않는 1개
네임스페이스의 예외로 바뀐 것**이다. `istio-system`은 향후 PSS를 도입하더라도
`privileged` 라벨이 필요하다.

### Restricted 판정 — 통과

| 네임스페이스       | 차트 / 워크로드                                                           | 워크로드 수 |
| ------------------ | ------------------------------------------------------------------------- | ----------- |
| `cert-manager`     | `cert-manager` v1.17.2 (controller, webhook, cainjector, startupapicheck) | 4           |
| `external-secrets` | `external-secrets` 0.14.4 (controller, webhook, cert-controller)          | 3           |
| `ingress-nginx`    | `ingress-nginx` 4.12.0 (controller, admission create/patch Job)           | 3           |
| `argo-rollouts`    | `argo-rollouts` 2.40.9 controller                                         | 1           |
| `argo-rollouts`    | `argo-rollouts` 2.40.9 dashboard (이 저장소 values로 하드닝)              | 1           |
| `argocd`           | `argo-cd` 10.4.0 (10개 워크로드, `copyutil` init container 2개 포함)      | 10          |
| `monitoring`       | 저장소 저작 `kube-state-metrics`, `alloy-k8s-logs` (seccompProfile 추가)  | 2           |
| `istio-system`     | `istiod` 1.25.2 (이 저장소 values로 seccompProfile 추가)                  | 1           |
| `istio-system`     | `kiali-operator` 2.10.0 (블록 전체 재기술 + seccompProfile)               | 1           |
| `headlamp`         | `headlamp` 0.41.0 (블록 전체 재기술 + 3개 항목 추가)                      | 1           |
| `apps`             | 저장소 저작 `adminer` (이미지 UID 999 관측 후 identity + seccomp 적용)    | 1           |

`argo-cd` 10.4.0은 조사한 차트 중 유일하게 모든 기본 워크로드가
`seccompProfile.type: RuntimeDefault`를 명시한다.

### Restricted 판정 — 실패

**없다.** 조사 시점에는 6개 워크로드가 걸렸으나 모두 닫혔다. 닫는 방식은 세 갈래였다.

| 방식                      | 대상                                              | 비고                                                               |
| ------------------------- | ------------------------------------------------- | ------------------------------------------------------------------ |
| 저장소 매니페스트 편집    | `kube-state-metrics`, `alloy-k8s-logs`, `adminer` | 저장소가 pod spec을 저작하는 워크로드                              |
| values에 단일 키 추가     | `istiod`, `argo-rollouts` dashboard               | 차트가 `securityContext`를 병합하거나 비어 있어 추가가 안전한 경우 |
| values에 블록 전체 재기술 | `kiali-operator`, `headlamp`                      | 차트가 대체형이라 부분 재정의 시 기존 하드닝이 사라지는 경우       |

`adminer`만 이미지 관측이 선행되었다. 이미지 `/etc/passwd`가
`adminer:x:999:999::/home/adminer:/bin/sh`이고 image config의 `User`가 이름
(`adminer`)이므로, `runAsUser: 999`/`runAsGroup: 999`를 `runAsNonRoot`와 함께
지정해 커플링을 해소하면서 `/var/www/html` 소유권을 유지했다.

`readOnlyRootFilesystem`은 세 워크로드(`adminer`, `argo-rollouts` dashboard,
`headlamp`)에서 적용하지 않았다. Restricted 요구사항이 아니며, 어느 경로에 쓰기가
필요한지는 매니페스트만으로 판정되지 않는다.

### 차트 기본값과 실제 설치의 차이

조사에서 유일하게 **차트 기본값 판정이 실제 상태와 달랐던 지점**이다.

`argo-rollouts` 대시보드는 upstream 기본값이 `dashboard.enabled: false`라 기본
설치에서는 배포되지 않는다. 그러나 이 저장소의
`gitops/apps/root/platform-rollouts-app.yaml`은 `dashboard.enabled: true`로
설정하고 Ingress까지 붙인다. 따라서 이 실패는 잠재적 결함이 아니라 **활성 결함**이다.

`adminer`와 성격이 같다. 둘 다 "저장소가 켠 워크로드인데 하드닝은 하지 않은 것"이며,
저장소가 _저작한_ 것과 저장소가 _활성화한_ 것 사이의 틈에서 나왔다.

**조치 완료.** `gitops/apps/root/platform-rollouts-app.yaml`의
`dashboard.containerSecurityContext`에 `allowPrivilegeEscalation: false`,
`capabilities.drop: [ALL]`, `seccompProfile.type: RuntimeDefault`를 추가해 대시보드는
Restricted를 통과한다. 세 항목 모두 이미지 정의와 포트만으로 성립한다: 이미지가
`gcr.io/distroless/static-debian12` + `USER 999`(숫자)이고 단일 Go 바이너리라 setuid
전환이 없으며, 3100 포트는 1024를 넘어 `NET_BIND_SERVICE`가 필요 없다.

`readOnlyRootFilesystem`은 의도적으로 제외했다. **Restricted 요구사항이 아니며**,
같은 차트의 controller는 그 항목을 켜면서 `/tmp`와
`/home/argo-rollouts/plugin-bin`에 emptyDir을 함께 마운트하는 반면 대시보드에는
볼륨이 없다. 켜려면 어느 경로에 쓰기가 필요한지 관측이 선행되어야 한다.

### 주입 네임스페이스와 pod-level seccompProfile

Istio 주입은 워크로드의 pod spec에 컨테이너를 추가하므로, 주입 네임스페이스의
Restricted 판정은 워크로드 자신의 설정만으로 결정되지 않는다.

**Istio는 `seccompProfile`을 gateway 템플릿에만 설정한다.** 주입되는
`istio-proxy`와 `istio-validation`에는 설정하지 않는다. Restricted의 seccomp
규칙은 pod 레벨 값 하나 또는 _모든_ 컨테이너의 값을 요구하므로, 주입 pod는
**pod 레벨 `seccompProfile`이 있어야만** 도달한다. 컨테이너 레벨에만 두면 주입된
컨테이너가 채우지 못해 pod 전체가 탈락한다.

나머지 통제는 주입 컨테이너가 이미 만족한다. 기본 경로(`REDIRECT` 인터셉션,
`capNetBindService` 미사용, `IPTABLES_TRACE_LOGGING` 미설정)에서 `istio-proxy`는
`capabilities.drop: [ALL]`에 `add` 없음, `allowPrivilegeEscalation: false`,
`privileged: false`, `readOnlyRootFilesystem: true`, `runAsNonRoot: true`,
`runAsUser: 1337`이다. `istio-validation`도 같다. 단 `TPROXY` 인터셉션이나
`capNetBindService` 주석을 쓰면 `runAsUser: 0`으로 바뀌어 Restricted에서 탈락한다.

**조치 완료.** `adminer`는 `seccompProfile`을 컨테이너 레벨에서 pod 레벨로 옮겼고,
`ingress-nginx`는 `controller.podSecurityContext`와
`controller.admissionWebhooks.patch.securityContext`에 추가했다. 후자는 admission
webhook Job 두 개의 pod 레벨 키다. `controller.containerSecurityContext`는 건드리지
않았다 — 그 키는 helper 출력 전체를 대체하므로 지정하면 차트가 넣던
`drop: [ALL]`과 `add: [NET_BIND_SERVICE]`가 사라진다.

### values 재정의 함정

세 차트는 `securityContext` 키를 **병합이 아니라 전체 대체**로 처리한다. 부분
재정의는 차트가 이미 제공하던 하드닝을 조용히 제거한다.

| 차트             | 함정                                                                                                                                                                                                                |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `kiali-operator` | `securityContext`를 지정하면 하드코딩된 기본 블록이 통째로 사라진다. `seccompProfile`만 추가하면 오히려 Restricted에서 더 멀어진다.                                                                                 |
| `ingress-nginx`  | `controller.containerSecurityContext`를 지정하면 helper가 넣던 `drop: [ALL]`과 `add: [NET_BIND_SERVICE]`가 사라진다.                                                                                                |
| `headlamp`       | 반대 방향의 함정이다. 템플릿에 Restricted-clean한 `$defaultSC` 기본 dict가 있으나, `values.yaml`이 `securityContext`를 채워두어 **기본 설치에서는 그 블록이 적용되지 않는다**. 키를 비우면 오히려 준수 상태가 된다. |

### 이 저장소의 재정의 현황

8개 chart Application의 `helm.values`를 전수 확인한 결과, **보안 관련 재정의는
하나도 없다**. `ingress-nginx`도 `controller.service.type: LoadBalancer` 하나뿐이라,
k3d 홈랩에서 흔한 `hostPort.enabled` / `hostNetwork: true` 단축 경로를 쓰지 않았다.
그 둘은 Baseline을 직접 위반한다.

유일한 보안 관련 값이 `argo-rollouts`의 `dashboard.enabled: true`이며, 그것이 위의
활성 결함을 만든다.

## Sources

- [Kubernetes Pod Security Standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/)
  — Baseline capabilities 허용 목록과 Restricted의 추가 통제 4종.
- `helm template` 로컬 렌더링 (2026-08-18): `cert-manager` v1.17.2,
  `external-secrets` 0.14.4, `ingress-nginx` 4.12.0, `argo-rollouts` 2.40.9
  (`--set dashboard.enabled=true`), `istiod` 1.25.2, `kiali-operator` 2.10.0,
  `headlamp` 0.41.0, `argo-cd` 10.4.0.
- 저장소 매니페스트: `gitops/platform/monitoring/*.yaml`,
  `gitops/workloads/adminer/rollout.yaml`, `gitops/apps/root/*.yaml`,
  `gitops/platform/namespaces/*.yaml`.

## Review and Freshness

- Source checked: 2026-08-18.
- 이 판정은 관측 시점의 차트 버전과 이 저장소의 values에 종속된다. 차트 버전을
  올리거나 `helm.values`를 바꾸면 재판정이 필요하다.
- 렌더링 결과는 선언된 의도이며 admission 결과가 아니다. 라이브 확인은
  `live-cluster` 증거 계열로 분리된다.
- Kiali operand, cert-manager ACME solver pod, 사이드카 주입 후 최종 pod spec은
  이 인벤토리 범위 밖이며 별도 관측이 필요하다.

## Related Documents

- [ADR 0024 — Pod Security Standards 단계 도입](../../02.architecture/decisions/0024-pod-security-standards-staged-adoption.md)
- [Istio CNI 도입 평가](./istio-cni-adoption-evaluation.md)
- [Spec 060 — workload security context baseline](../../03.specs/060-workload-security-context-baseline/spec.md)
- [Tech Stack Version Inventory](./tech-stack-version-inventory.md)
