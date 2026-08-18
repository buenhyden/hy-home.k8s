---
title: 'Reference: Istio CNI Adoption Evaluation'
type: content/reference
status: active
owner: platform
updated: 2026-08-18
---

# Istio CNI Adoption Evaluation

## Overview

이 문서는 Istio CNI node agent를 이 저장소의 WSL2 + k3d 환경에 도입할 때의
효과·비용·위험을 평가한 결과다.
[ADR 0024](../../02.architecture/decisions/0024-pod-security-standards-staged-adoption.md)가
PSS 도입 순서의 **1단계 선행조건**으로 지목한 항목이며, 실행이 아니라 평가다.

### Purpose

ADR 0024는 "CNI를 설치하면 `istio-init`의 특권 init container가 사라지고 그와
함께 Baseline 위반도 사라진다"고 기록했다. 그 주장이 실제로 성립하는지, 성립한다면
무엇을 대가로 치르는지, k3d에서 무엇이 다른지를 확정하는 것이 이 평가의 목적이다.

### 핵심 결과

**성립한다.** CNI 도입은 특권을 줄이는 정도가 아니라 Baseline을 실제로 잠금
해제한다. 다만 특권은 사라지지 않고 **이동**하며, k3d에는 bare k3s와 다른 경로
설정이 필요하다.

## Reference Type

- Type: adoption-evaluation / external-standard-snapshot
- Source checked: 2026-08-18
- Evidence class: 1차 문서 + Istio 1.25.2 차트의 로컬 `helm template` 렌더링.
  라이브 클러스터 증거가 아니다.
- Refresh trigger: Istio minor 버전 변경, k3d/k3s CNI 경로 변경, ambient mode 도입
  검토, 또는 Istio가 sidecar CNI 문서에 k3s/k3d 절을 추가하는 경우.

## Authority Boundary

- **Authoritative for**:
  - `pilot.cni.enabled` 전후의 주입 init container 차이와 그 PSS 판정.
  - k3d와 bare k3s의 CNI 경로 차이, 그리고 `global.platform=k3d`의 실제 동작.
  - CNI DaemonSet 자체가 요구하는 특권의 범위.
- **Not authoritative for**:
  - 도입 여부와 시점. 그것은 별도 승인과 ADR이 소유한다.
  - 라이브 동작. 어떤 클러스터도 접촉하지 않았고 어떤 pod도 기동하지 않았다.
  - WSL2 커널의 iptables backend(nft vs legacy) 차이가 redirection에 미치는 영향.
    1차 문서에 이 조합에 대한 서술이 없다.
  - ambient mode. 이 평가는 sidecar mode만 다룬다.

## Scope

대상은 Istio `1.25.2`의 `cni` 차트와 `istiod` 차트의 주입 템플릿이다. 현재
이 저장소는 `base`와 `istiod`만 배포하며 `istio-cni` Application이 없다.

`apps`와 `ingress-nginx`가 `istio-injection: enabled`이므로 도입 영향 범위는 그 둘이다.
k3d 클러스터는 서버 1 + 에이전트 3의 **4노드**이고 flannel을 비활성화하지 않았다.

## Definitions / Facts

### 주입 init container 비교

`istiod` 차트의 주입 템플릿은 `pilot.cni.enabled`로 두 분기를 갖는다. 로컬 렌더링으로
확인한 조건식은 다음과 같다.

```text
{{ if .Values.pilot.cni.enabled -}}
- name: istio-validation
{{ else -}}
- name: istio-init
{{ end -}}
```

securityContext 역시 같은 값으로 분기한다.

| 필드                       | `istio-init` (현재)                      | `istio-validation` (CNI 도입 후) |
| -------------------------- | ---------------------------------------- | -------------------------------- |
| `capabilities.add`         | `NET_ADMIN`, `NET_RAW`                   | **없음**                         |
| `capabilities.drop`        | `ALL`                                    | `ALL`                            |
| `runAsUser` / `runAsGroup` | `0` / `0`                                | `1337` / `1337`                  |
| `runAsNonRoot`             | `false`                                  | `true`                           |
| `readOnlyRootFilesystem`   | `false`                                  | `true`                           |
| `allowPrivilegeEscalation` | `global.proxy.privileged` (기본 `false`) | 동일                             |
| **Baseline**               | **위반**                                 | **통과**                         |
| **Restricted**             | 위반                                     | `seccompProfile`만 부족          |

`istio-validation`은 iptables를 적용하지 않고 redirection이 올바로 설정되었는지
검증만 한다(`--run-validation`, `--skip-rule-apply`). 설정되지 않았으면 pod 기동을
막는다.

### 특권의 이동

CNI 도입은 특권을 없애지 않고 **모든 주입 pod에서 노드당 하나의 DaemonSet으로**
옮긴다. 렌더링으로 확인한 `install-cni` 컨테이너의 securityContext는 다음과 같다.

```yaml
privileged: false
runAsUser: 0
runAsGroup: 0
runAsNonRoot: false
capabilities:
  drop: [ALL]
  add: [NET_ADMIN, NET_RAW, SYS_PTRACE, SYS_ADMIN, DAC_OVERRIDE]
```

`privileged: true`가 아니라 capability로 한정된 점은 주목할 만하다. 다만 `/proc`
hostPath가 기본으로 마운트된다(`repair.repairPods: true`가 기본이며, 그 기능이
`SYS_ADMIN`을 요구한다). sidecar mode에서는 `hostNetwork`를 쓰지 않는다.

거래의 본질은 이것이다. **트래픽을 서비스하는 2개 네임스페이스의 영구 예외가,
트래픽을 서비스하지 않는 1개 네임스페이스의 영구 예외로 바뀐다.** `istio-system`은
이후 Baseline을 만족할 수 없으며 `privileged` 라벨이 필요하다.

### k3d 경로 — 평가의 실질 산출물

k3s는 표준 CNI 경로를 쓰지 않는다. Istio는 이를 위해 platform profile을 제공하며,
**k3d와 bare k3s의 값이 다르다**.

|          | `cniBinDir`                     | `cniConfDir`                               |
| -------- | ------------------------------- | ------------------------------------------ |
| 기본값   | `/opt/cni/bin`                  | `/etc/cni/net.d`                           |
| bare k3s | `/var/lib/rancher/k3s/data/cni` | `/var/lib/rancher/k3s/agent/etc/cni/net.d` |
| **k3d**  | **`/bin`**                      | `/var/lib/rancher/k3s/agent/etc/cni/net.d` |

k3d에서 `/bin`인 이유는 "노드"가 k3s 컨테이너이고 바이너리가 그 rootfs에 있기 때문이다.

**`--set global.platform=k3d`가 standalone Helm 차트에서 실제로 동작한다.** 차트의
profile 병합 로직이 flat values에 도달하는지 문서만으로는 확정할 수 없었으나, 로컬
렌더링이 `cni-bin-dir → /bin`, `cni-net-dir → /var/lib/rancher/k3s/agent/etc/cni/net.d`를
출력해 확정했다. platform을 지정하지 않으면 기본 경로가 그대로 나온다.

Istio는 이 내용을 **ambient platform prerequisites 문서에만** 기록하고 sidecar CNI
문서에는 k3s/k3d 절을 두지 않는다.

### chaining과 flannel

`chained: true`가 기본이며, Istio는 기존 primary CNI의 conflist에 자신을 덧붙인다.
k3s/k3d의 번들 flannel은 conflist를 발행하므로 chaining이 성립하고, OpenShift와 달리
`chained: false`가 필요하지 않다.

`cniConfFileName`은 기본이 빈 값이며 그 경우 conf 디렉터리의 **첫 파일**을 쓴다.
그 디렉터리에 다른 파일이 생기면 잘못된 conflist에 chaining될 수 있으므로 실제
flannel conflist 파일명을 고정하는 편이 안전하다. 그 파일명은 k3s 문서에 없어
노드에서 직접 읽어야 한다.

### 순서와 경합

- `istiod`에 `pilot.cni.enabled=true`를 설정해야 주입이 전환된다. revision마다
  설정해야 한다.
- CNI와 control plane은 `1.x-1`, `1.x`, `1.x+1` 호환이므로 업그레이드 순서는 자유롭다.
- DaemonSet이 스케줄된 시점과 플러그인이 준비된 시점 사이에 문서화된 경합이 있다.
  완화책이 기본 활성이다: `istio-validation`이 redirection 미설정을 감지해 기동을
  막고, `repair.repairPods: true`가 in-place로 교정한다.
- **PSA는 admission 시점 검사이므로**, Baseline을 켜도 이미 `istio-init`을 달고
  도는 pod은 축출되지 않는다. 재생성될 때 거부된다. 주입 네임스페이스를 롤링해야
  실제로 수렴한다.

### 실패와 롤백

경로를 잘못 설정하면 crash가 아니라 **조용한 정체**로 나타난다. 에이전트가 커널이
읽지 않는 디렉터리에 쓰므로 redirection이 설치되지 않고, 새 주입 pod이
`istio-validation`에서 `Init:0/1`로 멈춘다. k3d에서 가장 가능성이 높은 원인은
`cniBinDir`이 `/bin`이 아닌 것이다.

정상 종료 시 에이전트는 자기 흔적을 지운다. conflist에서 `"type": "istio-cni"`
항목만 외과적으로 제거하고 바이너리도 삭제한다.

**롤백 순서가 중요하다.** `pilot.cni.enabled=false`를 **먼저** 적용하고 그다음 CNI
차트를 제거한다. 반대로 하면 새 pod이 `istio-init`도 CNI도 받지 못한다.

### k3d 고유 위험

- **`cniBinDir` 오설정** — bare k3s 안내를 따르면 틀린다. 이것이 단일 최대 위험이다.
- **바이너리가 노드 컨테이너의 writable layer에 들어간다.** `k3d cluster stop/start`는
  견디지만 **노드 재생성이나 이미지 업그레이드는 견디지 못한다.** 재생성 후
  DaemonSet이 재설치될 때까지 주입 pod이 뜨지 못한다.
- **4노드 전부에서 설치가 성공해야 한다.** 에이전트 3개가 각각 자기 노드에 설치한다.
- **강제 종료 시 conflist 오염** — 정리는 5초 grace period 안에서만 일어난다.
  강제 kill된 노드에 잔존 항목이 남으면 그 노드의 **모든 pod 네트워킹**이 깨진다.
  메시 트래픽만이 아니다. k3d 노드 컨테이너는 랩 정리 중 강제 kill되기 쉽다.
- **GitOps 순서** — ArgoCD sync wave에서 `istio-cni`가 `istiod`의 플래그 전환보다
  앞서야 하고, 둘 다 `base`보다 뒤여야 한다.

## Sources

- [Istio 1.25 — Install Istio with the Istio CNI plugin](https://istio.io/v1.25/docs/setup/additional-setup/cni/)
- [Istio — Platform-Specific Prerequisites (k3s/k3d)](https://istio.io/v1.25/docs/ambient/install/platform-prerequisites/)
- [istio/istio @ 1.25.2 — helm-profiles/platform-k3d.yaml](https://github.com/istio/istio/blob/1.25.2/manifests/helm-profiles/platform-k3d.yaml)
- [istio/istio @ 1.25.2 — injection-template.yaml](https://github.com/istio/istio/blob/1.25.2/manifests/charts/istio-control/istio-discovery/files/injection-template.yaml)
- [istio/istio @ 1.25.2 — cni/pkg/install/install.go](https://github.com/istio/istio/blob/1.25.2/cni/pkg/install/install.go)
- [k3s-io/k3s#1434 — Deterministic cni-bin-dir](https://github.com/k3s-io/k3s/issues/1434)
- `helm template` 로컬 렌더링 (2026-08-18): `cni-1.25.2` (기본값 및
  `--set global.platform=k3d`), `istiod-1.25.2` (기본값 및
  `--set pilot.cni.enabled=true`).

## Review and Freshness

- Source checked: 2026-08-18.
- Istio minor 버전이 오르면 주입 템플릿과 platform profile 값을 재확인해야 한다.
- 확정하지 못한 항목: k3s/k3d 번들 flannel의 conflist 파일명(노드에서 직접 읽어야
  함), k3s 재시작 시 flannel conflist 재작성 여부, 이미 주입된 pod의 재시작
  필요 여부(문서에 서술 없음), k3d 고유 실패 사례 보고(발견되지 않음).
- 이 평가는 어떤 클러스터도 접촉하지 않았다. 도입 결정과 실행은 별도 승인 대상이다.

## Related Documents

- [ADR 0024 — Pod Security Standards 단계 도입](../../02.architecture/decisions/0024-pod-security-standards-staged-adoption.md)
- [Pod Security Compliance Inventory](./pod-security-compliance-inventory.md)
- [Tech Stack Version Inventory](./tech-stack-version-inventory.md)
