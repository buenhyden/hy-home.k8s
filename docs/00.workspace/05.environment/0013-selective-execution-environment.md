---
title: "선택형 제품 검증 환경 가이드"
version: "0.2.0"
type: "operation/guide"
status: "draft"
owner: "platform"
updated: "2026-11-24"
artifact_id: "GDE-0013"
---

# 선택형 제품 검증 환경 가이드

## 문서 개요

### 목적과 독자

이 가이드는 현재 hy-home.k8s checkout에서 검증할 Application만 선택하는
개발자와 환경 운영자를 위한 절차다. 현재 도구의 실제 지원 범위와 목표
경계, 관측되지 않은 부분을 분리한다.

### 책임과 적용 범위

platform은 이 환경의 준비와 선택형 실행 절차를 소유한다. 실제 제품
구성과 네트워크 설계는 [현재 플랫폼 설명](../../02.architecture/01.descriptions/0007-current-local-gitops-platform.md),
보호 행위는 [승인 및 안전 정책](../04.quality/approval-and-safety.md),
검증 의무는 [품질 정책](../04.quality/quality.md)이 소유한다.

## 내용 계약

### 입력과 전제

현재 checkout, `gitops/apps/root/*.yaml`의 실제 Application 집합,
`scripts/test_cluster.py`의 `catalog`·`plan`·`doctor` 결과, 호스트의
실측 용량과 설치된 Docker/k3d/kubectl 판본을 입력으로 사용한다. 문서의
예상값만으로 실제 네트워크 차단, 디스크 한도 또는 제품 readiness를
증명하지 않는다.

### 본문과 규칙

#### Purpose

##### Audience

개발자는 현재 변경이 소비하는 Application과 최소 의존 집합을 선택한다.
환경 운영자는 호스트 자원, 격리, 권한과 정리 대상을 확인한다. 두 역할
모두 실제 run ID와 현재 Git revision을 기록한다.

##### Outcome

이 문서는 `how-to` 가이드다. 독자는 지원되는 작은 구성의 선택·렌더·API
검사와, 허용된 경우에만 실제 기동·준비도·정리를 각각 수행한다. 실패와
미관측은 원래 상태 그대로 결과 Task에 남긴다. 기존 [독립 검토 환경
가이드](./0012-independent-review-environment.md)의 네이티브 권한과
한정 호출 절차를 재사용한다.

###### Boundaries

현재 `test_cluster.py`는 선택한 로컬 Kustomize Application의 dependency
closure, loopback API와 전용 kubeconfig, run 소유 cleanup을 제공한다.
[공용 admission](../../../scripts/environment_admission.py)은 같은 계정과
호스트의 직접 실행과 [dispatcher](../../../scripts/work_parallel.py), 독립
clone과 linked worktree를 하나의 상태에서 합산해 활성 구성 합집합과
CPU·메모리·논리 디스크를 원자적으로 예약한다. Git checkout은 편집을
분리할 뿐 OS sandbox가 아니다. 직접 `up`(host 경로)은
[환경 adapter](../../../scripts/test_cluster_environment.py)로 소유 내부
Docker network를 isolated gateway mode와 IPv6 꺼짐으로 만든다. 호스트는
그 bridge에 주소를 두지 않고, node는 그 network 하나에만 붙으며,
`kubectl`은 node 안에서 자기 API로 실행된다. node CPU·메모리와 namespace
quota를 적용하고, 만료 timer를 자원 생성 전에 무장하며, 소유 자원의
부재를 확인한 뒤에만 예약을 푼다. 디스크는 15초마다 node 사용량을 재는
watchdog이 예산 초과 또는 측정 실패 세 번에 node를 멈추는 polling 상한이며
kernel quota가 아니다. `up --vm`은 같은 선택 집합을 소유된 QEMU 사용자
서비스 안에서 실행하도록 연결한다. 제품 NetworkPolicy는 생산 LAN의 외부
서비스로 가는 egress를 허용하므로, 이 network 또는 VM 경계가 정책 아래에서
host와 LAN을 막는다.
원격 chart·CRD 의존 구성과 App-of-Apps root는 현재 `catalog`에서
거절된다. 구현과 합성 회귀는 실제 VM 부팅이나 제품 기능 성공이 아니다.
호스트 외부 방화벽, 전역 Docker
설정, 운영 credential, 생산 endpoint 요청, 모든 Application 동시 실행은
절차의 입력이 아니다. P12 작업자 격리와 P06 검토자 권한도 별도 owner다.

#### Prerequisites

##### Environment

현재 판본과 입력을 다음과 같이 확인한다. `doctor`의 출력은 호스트
사전 점검이며 제품 pod의 실제 readiness가 아니다.

```bash
git rev-parse HEAD
docker --version
k3d version
kubectl version --client
qemu-system-x86_64 --version
qemu-img --version
python3 scripts/test_cluster.py doctor
python3 scripts/test_cluster.py catalog
```

도구를 실행할 Python과 현재 동기화된 checkout을 기록한다. Python 검증
의존성은 [GDE-0011](./0011-local-validation-environment.md)의 hash lock과
별도 checkout 밖 venv를 따른다. 선택 환경의 전용 kubeconfig와 loopback API를
사용하고 현재 사용자의 기본 context를 변경하지 않는다. Docker 이미지와
chart의 cache, pull 필요 여부를 분리해 기록한다. 제품 pod 기동 전에
CPU·메모리·디스크·시간의 실제 시행 가능한 한도와 생산 LAN 격리 경계를
확인한다.

현재 호스트에서 QEMU 8.2.2는 있으나 `/dev/kvm` 접근은 불가하다.
선택한 VM 경로는 TCG를 사용한다. 사용자 manager는 기본 셸의 bus 설정이
빠져 실패한 적이 있으므로 `XDG_RUNTIME_DIR=/run/user/1000`과
`DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus`의 실제
사용자 bus를 확인한다. 작은 소유 사용자 단위에서는 `cpu.max`가
`200000 100000`, `memory.max`가 `4294967296`으로 확인됐다.
이 결과만으로 QEMU 부팅·게스트 디스크·네트워크를 성공으로 처리하지 않는다.

##### Authority

현재 요청이 허용한 대상과 시간, 소유 자원을 먼저 확인한다. 실제 Docker
container 또는 k3d cluster 생성, 네트워크 probe, 이미지 pull, host/VM
변경은 각 대상·executor·rollback과 현재 권한을 결과 Task에 남긴 후
수행한다. 전역 방화벽이나 Docker daemon 변경을 이 가이드에서 암묵적으로
허가하지 않는다. 제품 서비스에는 운영 kubeconfig, Docker socket,
secret 또는 host mount를 전달하지 않는다.

P07의 실제 VM 실행 전에는 여덟 문자 run ID, 사용자 단위 이름,
`.workspace-test/<run-id>`의 전용 경로, 600초 만료시각과 정리 대상을
한 번만 정한다. 기본 사용자 bus 실패를 관리자 권한 요구나 기능 미지원으로
오인하지 않는다. 새 계정·결제·root 권한 또는 다른 제품 환경을 암묵적으로
추가하지 않는다.
초기 private intent를 기록한 뒤 VM unit이나 guest 파일을 만들기 전에,
해당 token의 `hyk8s-owned-p07vm001-${token}.timer`와 대응 `.service`를
원래 600초 기한에 맞춰 무장한다. 무장에 실패하거나 상태를 확인할 수
없으면 VM 생성을 중단하고 intent를 복구 근거로 남긴다. 만료와 정상
종료 모두 정확한 token·unit·process 소유를 확인한 뒤 해당 timer,
service, VM unit과 파일만 정리한다. timer 설치·만료·정리는 실제 VM
실행에서 별도로 확인하기 전까지 미관측이다.

#### Procedure

##### Steps

| Step | Action | Expected Result | On Failure |
| --- | --- | --- | --- |
| 1 | 현재 Git revision, `catalog`와 아래 Application 표를 대조하고 정확한 선택 이름을 적는다. | root와 미지원 경로가 섞이지 않은 최소 후보가 나온다. | source/버전/namespace 불일치가 있으면 표를 현재 root YAML에 맞춰 갱신한다. |
| 2 | `plan`으로 선택과 의존 closure를 확인한다. 전체, wildcard, App-of-Apps root 및 분할 선택으로 전체를 우회하는 요청은 거절한다. | 선택된 closure와 거절 사유가 기록된다. | `unsupported`는 이유와 필요한 chart/CRD controller만 별도 준비한다. |
| 3 | 직접 `up`과 dispatcher가 같은 admission을 쓰는지, 활성 run의 closure 합집합·CPU·메모리·디스크·시간 예약을 호스트 실측 예산과 대조한다. | 한도 초과는 spawn 전에 거절되고 모든 실행이 하나의 상태를 소비한다. | 잠금·lease 소유 또는 경계가 애매하면 기동을 보류하고 lease를 보존한다. |
| 4 | 실제 host/container 또는 VM 생산 LAN 차단을 확인한다. IPv6, 기본 route, proxy, 소유하지 않은 NIC, mount/socket 노출도 확인한다. | 별도 격리 경계와 디스크 한도(VM 고정 디스크 또는 host watchdog의 polling 상한)가 확인된다. | 한쪽이라도 없으면 모든 live k3d node 기동을 차단한다. Namespace/NetworkPolicy만 고른 경우도 예외가 아니다. |
| 5 | 선택한 경로만 render하고 API dry-run 결과를 기록한다. 실제 namespace와 policy를 적용한 뒤에는 임시 통제 probe pod 하나로 금지 경로와 허용 경로를 각각 확인한다. | render, API, 실제 두 경로의 결과가 구분된다. | static 성공으로 LAN 격리를 대체하지 않는다. 생산 endpoint에 요청하지 않는다. |
| 6 | 실제 격리와 디스크 한도가 확인된 경우에만 제품 workload를 시작하고 선택한 readiness를 확인한다. run ID·label·namespace와 생성 자원을 기록한다. | 선택한 closure만 기동하고 readiness 근거가 남는다. | 실패·timeout은 실제 `failed`로 기록하고 소유 자원만 정리한다. |
| 7 | `down` 또는 `sweep` 전에 run 소유 token과 container/cluster label을 검증한다. | 해당 run의 자원만 삭제되고 lease는 확인 후 해제된다. | 소유가 불분명하면 lease와 자원을 보존해 운영자 조사로 넘긴다. |

선택한 VM 경로의 실제 진입점은 `scripts/test_cluster.py up --vm`이다.
`--authority`에는 현재 운영자 요청 참조를, `--run-id`에는 중복되지 않는
여덟 문자 소유 ID를 전달한다. 이 명령은 호스트의 공용 admission을 예약하고
`.workspace-test/<run-id>/vm`에 private owner record를 만든 뒤
`hyk8s-test-<run-id>-vm` 사용자 단위 하나를 기동한다. `status`로 실제
소유 상태를 확인하고, 종료는 같은 run ID에 `down`을 사용한다. 시간 초과나
충돌 후 `sweep`을 쓰더라도 해당 lease와 unit, 프로세스 시작시각·file
identity가 맞는 것만 정리한다. 소유가 애매하면 임대를 남긴다.

2026-11-24 운영자는 반복 실패한 VM 경로 대신 host 경로(option C)를
선택했다. host의 직접 `up`은 isolated network와 디스크 watchdog으로 진행하고,
watchdog이 node를 멈추면 `CLUSTER_DISK_LIMIT`로 실패한다. VM 경로는 선택
사항으로 남는다. 현재 VM 구현의 예산과 검증 순서는 다음과 같다. 이 표는 코드 계약이며
실제 VM 검증 결과가 아니다.

| Boundary | Implemented candidate | Runtime decision |
| --- | --- | --- |
| 호스트 예약 | 활성 직접/dispatcher 실행을 공용 admission으로 합산; VM run은 2 CPU, 4096 MiB 메모리, 4096 MiB 디스크, 600초 | 현재 host 여유·동시 lease를 실제 확인하고 초과 시 기동 전 거절 |
| 사용자 단위 | `CPUQuota=200%`, `MemoryMax=4G`, `MemorySwapMax=0`, `RuntimeMaxSec`는 최초 600초 기한에서 종료 여유 5초를 뺀 잔여, `TimeoutStopSec=5`, `SendSIGKILL=yes`, `LimitCORE=0`, `KillMode=control-group` | 소유 QEMU와 controller가 같은 cgroup의 실제 `cpu.max`·`memory.max`·`memory.swap.max`에 속하는지 확인 |
| 이미지·디스크 | 공식 Ubuntu 24.04 minimal 2026-11-05 QCOW3 SHA256 `406630c08b5e545fcc7209854b129d47e3af822db128c9f19336593b5a2d3fe0`; source 최대 512 MiB 별도 준비 lease, 고정 RAW 4080 MiB와 OVMF 변수·작은 메타데이터 파일 | HTTPS 대상·SHA·형식·backing 없음·가상 크기를 확인하고 변환; 게스트 단일 `vda` 실제 용량과 ENOSPC·복구를 관측하기 전 hard cap PASS 아님 |
| 준비 네트워크 | TCG 2 vCPU, guest RAM 3072 MiB, NoCloud용 임시 loopback HTTP와 SSH hostfwd; public image와 signed apt package 설치 | 준비용 통신과 제품 런타임을 분리하고 같은 600초 기한을 유지 |
| 제품 런타임 네트워크 | 재부팅 후 metadata guestfwd 제거, QEMU user NIC `restrict=on`, `ipv6=off`, loopback SSH hostfwd만 남김 | 통제된 host dummy endpoint 차단·guest 내부 허용 경로와 선택 namespace policy probe를 모두 실제 확인; 생산 endpoint에는 요청하지 않음 |
| guest 입력·출력 | Git index의 전체 root Application YAML 선언과 선택한 의존 YAML만 추출하고, 경로·상위 symlink·파일 종류를 검사한 뒤 기존 `bounded_io`의 no-follow 제한 읽기를 host에서만 지연 import해 public 실행 script와 합쳐 최대 32 MiB 전송; guest fresh Git 저장소와 host input digest 연결 | untracked 파일·`.git` history·credential·provider 설정·운영 kubeconfig를 보내지 않음; guest 복사본은 기존 5-script closure를 유지하고 일회용 SSH key는 소유 단위 중지 확인 후 삭제 |
| 선택 k3d | guest에서 기존 runner·전용 kubeconfig·loopback API·ResourceQuota/LimitRange 사용; 준비 단계에 필요한 pinned k3s·busybox·pause·k3d-tools 이미지만 pull하고 pause archive를 시작 입력에 사용 | selected closure의 render, API dry-run, 실제 readiness와 정리를 따로 기록 |

현재 guest `up()`의 VM 경로는 서버 dry-run 뒤 Namespace·Quota와
workload가 아닌 정책·인프라만 적용한다. 소유된 dummy nonce를 사용해
선택 namespace의 임시 probe pod로 내부 허용과 통제된 host 방향 거절을
각각 확인하고 probe 자원을 정리한 다음에만 지원되는 제품 workload를
적용한다. 각 Pod·Job의 Ready/complete 또는 controller rollout을
기다리고, outer VM controller도 이 guest `network_probe` 결과가 둘 다
참일 때만 ready로 기록한다. 선택한 kind의 readiness를 지원하지 않거나
probe가 실패하면 그 선택은 거절한다. 이 적용 순서는 현재 소스와 집중
합성 회귀에서 확인한 구현이며, 실제 VM·제품 pod의 runtime PASS는 아니다.
SSH·HTTP 전송 실패 또는 응답 누락은 금지 경로의 성공적인 거절로 세지
않고 별도 실패로 기록한다.

현재 구현의 `catalog`·`plan`·`doctor`는 읽기 중심 사전 점검이다.
`up`·`probe`·`down`은 실제 대상과 권한 확인 후에만 호출한다. 단일 실행의
Application 수 제한은 여러 직접/dispatcher 실행을 합산한 admission의
증거가 아니다. 선택한 chart 또는 CRD가 아직 지원되지 않으면 제품 전체
root 동기화로 우회하지 않는다.

##### Expected Results

각 단계는 `ready`, `failed`, `unsupported`, `missing`, `unobserved`,
`not-applicable`과 이유를 기록한다. 문서 draft, 정적 render, API dry-run,
실제 선택형 기동, 생산 LAN의 금지·허용 probe, cleanup 및 사용자 인수는
서로 별도 결과다. W09-H02의 통제된 두 경로 probe는 host 경로 run
`p07host2`에서 통과했다. 제품 정책을 적용한 `apps`에서 내부 허용과 소유
host 거절을, 정책이 없는 namespace에서 `192.168.0.13`·`192.168.0.14` 거절을
각각 확인했다(SPEC-0229 EVD-088·EVD-089). 선택 가능한 Application에는
pod가 없으므로 제품 workload readiness는 아직 미관측이다.
P06 sandbox 사전 점검, P07의 일곱 차례 실제 모델 검토와 그 수리, 열세 번의
VM 실행 실패와 정리 결과는 [선택형 환경 Task](../../03.specs/0229-selective-environment/01.tasks/tsk-0001-selective-environment.md)에
원래대로 남아 있다. 현재 판정만 요약하면, VM 경로에서는 부팅, NoCloud
준비, restricted 재부팅, guest ENOSPC, VM egress 거절, k3s 시작과 guest API
경로가 관측됐으나 선택 readiness는 반복 실패했다. host 경로는 선택 적용,
namespace probe와 LAN 거절, 소유 정리가 통과했다. Docker `size=32M` 쓰기
상한 실패는 그 명령의 실패로 유지한다. 관측된 provider 청구액은 `null`이다.

현재 root Application의 source 개요는 아래와 같다. 이 표의 `main`은
움직이는 Git revision이며 pin이 아니다. 실제 검증에는 checkout HEAD를
따로 고정한다. chart 판본은 root YAML의 명시값이다. `R`은 현재 로컬
render 지원, `U`는 `catalog`가 현재 거절, `X`는 전체 root 거절을 뜻한다.
`platform-namespaces`와 `platform-network-policies`는 run `p07host2`에서
실제로 적용됐고(pod 없음), 나머지 행의 API/live/readiness는 아직
미관측이며, 선택한 구성에서만 실제 검사한다. secret은 테스트 대체물을 요구하고 cleanup은
run token·label로 확인한 소유 자원에 한정한다.

| Application | Source and revision | Namespace | Current render and dependency | API/live/readiness | Secret and cleanup |
| --- | --- | --- | --- | --- | --- |
| platform-argocd-config | local `gitops/platform/argocd`, `main` | argocd | U: external-secrets.io CRD | unobserved | substitute; owned only |
| platform-cert-manager | chart `cert-manager` v1.17.2 | cert-manager | U: remote chart | unobserved | substitute; owned only |
| platform-cert-manager-config | local `gitops/platform/cert-manager`, `main` | cert-manager | U: cert-manager.io CRD | unobserved | substitute; owned only |
| platform-cluster-config | local `gitops/clusters/local`, `main` | argocd | X: App-of-Apps root | not selected | no startup |
| platform-eso-config | local `gitops/platform/eso`, `main` | external-secrets | U: external-secrets.io CRD | unobserved | substitute; owned only |
| platform-external-secrets-operator | chart `external-secrets` 0.14.4 | external-secrets | U: remote chart | unobserved | substitute; owned only |
| platform-external-services | local `gitops/platform/external-services`, `main` | platform | R: namespaces | unobserved | substitute; owned only |
| platform-headlamp | chart `headlamp` 0.41.0 | headlamp | U: remote chart | unobserved | substitute; owned only |
| platform-headlamp-config | local `gitops/platform/headlamp`, `main` | headlamp | R: namespaces | unobserved | substitute; owned only |
| platform-ingress-routes | local `gitops/platform/ingress-routes`, `main` | traefik | R: namespaces | unobserved | substitute; owned only |
| platform-istio-base | chart `base` 1.25.2 | istio-system | U: remote chart | unobserved | substitute; owned only |
| platform-istio-cni | chart `cni` 1.25.2 | istio-system | U: remote chart | unobserved | substitute; owned only |
| platform-istiod | chart `istiod` 1.25.2 | istio-system | U: remote chart | unobserved | substitute; owned only |
| platform-kiali | chart `kiali-operator` 2.10.0 | istio-system | U: remote chart | unobserved | substitute; owned only |
| platform-kiali-config | local `gitops/platform/kiali`, `main` | istio-system | U: external-secrets.io CRD | unobserved | substitute; owned only |
| platform-monitoring | local `gitops/platform/monitoring`, `main` | monitoring | U: external-secrets.io CRD | unobserved | substitute; owned only |
| platform-namespaces | local `gitops/platform/namespaces`, `main` | argocd | R: no local prerequisite | applied in `p07host2`; no pod | substitute; owned only |
| platform-network-policies | local `gitops/platform/network-policies`, `main` | platform | R: namespaces | applied in `p07host2`; LAN probe passed; no pod | substitute; owned only |
| platform-rollouts | chart `argo-rollouts` 2.40.9 | argo-rollouts | U: remote chart | unobserved | substitute; owned only |
| platform-traefik | chart `traefik` 42.1.3 | traefik | U: remote chart | unobserved | substitute; owned only |

#### Troubleshooting

##### Symptoms

`catalog`의 `unsupported`는 설치된 controller가 없거나 remote chart
렌더링을 현재 runner가 지원하지 않는 등 원인별로 다르다. `plan`의 거절은
전체 선택, closure 한도 또는 현재 지원 범위에서 발생할 수 있다. host
disk 공간이 충분해 보여도 실제 per-run hard cap이 없을 수 있다.
2026-11-20의 소유된 작은 Docker 진단에서는 Engine 29.9.2가
`storage-opt size=32M`을 받아들였으나, `alpine:3.24.3` 컨테이너가
40 MiB(41943040 bytes)를 `/quota-test`에 쓰고 exit 0으로 종료했다.
따라서 이 호스트·driver의 검사된 경로는 실제 hard disk cap이 `failed`다.
처음 붙인 `docker start -a` CLI가 60초에 timeout된 것과 별개로,
컨테이너 inspect·logs에서 완료와 쓰기량을 확인했다. 소유 label을 확인한
뒤 해당 컨테이너를 삭제했고, 후속 inspect는 `no such object`였다.
host 경로는 이 쓰기 상한 대신 node 디스크 watchdog을 쓴다. QEMU/TCG VM
경로에서는 부팅·게스트 ENOSPC·VM egress 거절이 관측됐으나 선택 k3d
준비도는 통과하지 못했다.
NetworkPolicy allow는 합산되므로 추가 deny만으로 기존 production LAN
allow를 상쇄하지 못한다. 예약과 시뮬레이션만으로 hard cap을 증명하지
않는다.

##### Next Action

지원 불가 기능은 해당 chart 판본·controller·CRD와 최소 selected scope를
정한 뒤 구현 owner에게 넘긴다. host 네트워크나 디스크 강제 기능이 없으면
제품 workload 기동을 멈추고 현재 실패·미관측을 분리해 기록한다. 기존
`up` 실패 후에는 PID만으로 lease를 지우지 않는다. 시작 전 durable intent,
child gate·tombstone·owner label의 실제 상태를 확인하고 애매하면 lease를
남긴다. 운영 권한이나 비용 범위가 바뀌면 그 대상만 별도로 결정한다.
Docker `size=32M` 실패는 그 경로의 현재 실패로 유지한다. VM에서 나중에
고정 guest disk와 ENOSPC가 실제 통과하더라도 Docker 명령의 실패를
같은 명령의 PASS로 덮어쓰지 않는다. 선택된 실행 경로를 VM으로 한정한
근거와 적용 범위를 별도로 기록한다. VM 시작·NoCloud·SSH·guest 부팅·
기한·파일 정리 중 어디서 실패했는지 단계를 특정하고, 준비용 egress와
제품 runtime egress의 결과를 섞지 않는다.

##### Lifecycle Traceability

| Promoted owner | Audience outcome | Operating surface |
| --- | --- | --- |
| [SPEC-0223 Task](../../03.specs/0223-work-residue-handoff/01.tasks/tsk-0001-work-residue-handoff.md) | W09-H02는 P07 host 경로의 실제 LAN 거절 관측으로 닫혔고, W07-H05의 별개 검토자 실패는 유지한다. | 현재 checkout의 선택형 k3d 검증과 P06 검토 경계 |

## 적용과 확인

### 적용 방법

`doctor`와 `catalog`로 현재 능력을 읽고 선택한 Application만 `plan`한다.
실제 생성·probe·정리는 단계별 권한, 소유, 격리, resource cap을 확인한
뒤 진행한다.

### 확인 기준

현재 `catalog`의 분류는 설치 도구와 source revision이 같을 때만 재사용한다.
문서와 static QA의 PASS는 실제 k3d readiness, 생산 LAN 차단 또는 사용자
인수의 증거가 아니다. 실제 결과는 소유 Task에 기록한다.

## 관계와 출처

### 관련 문서

| Relation | Target |
| --- | --- |
| operates | [현재 로컬 GitOps 플랫폼](../../02.architecture/01.descriptions/0007-current-local-gitops-platform.md) |
| cites | [기존 잔여 Task](../../03.specs/0223-work-residue-handoff/01.tasks/tsk-0001-work-residue-handoff.md) |

### 외부 근거

추가 외부 조사는 이 가이드에 사용하지 않았다. 현재 root YAML, runner의
실제 `catalog` 결과 및 동봉 P07 설계를 적용했다.
