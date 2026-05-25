---
title: 'WSL2 k3d/k3s ArgoCD HA Setup Guide'
type: guide
status: active
owner: platform
updated: 2026-05-26
---

# WSL2 k3d/k3s ArgoCD HA Setup Guide

## Overview (KR)

이 문서는 WSL2 환경에서 멀티노드 k3d 클러스터와 ArgoCD/ESO/Vault/외부 서비스 계약을 설정하고 검증하는 방법을 설명한다.

> **현재 실행계약 메모 (2026-05-09)**: 현재 `gitops/platform/external-services/`와 정적 검증 스크립트는 외부 서비스 EndpointSlice/CIDR을 `172.18.x` 기준으로 고정한다. 이 문서의 `172.19.x` 언급은 k3d 네트워크 경로 문제를 설명하는 역사적 `infra_net` 맥락으로만 해석한다.

## Guide Type

`how-to`

## Target Audience

- Developer
- Operator

## Purpose

운영 계약(TLS/외부 서비스/최소권한)을 유지하면서, 로컬 런타임 검증과 CI 정적 검증을 분리해 재현성을 높인다.

## Prerequisites

- Windows + WSL2(Ubuntu)
- WSL-native Docker available from the WSL shell
- `kubectl`, `k3d`, `helm`, `argocd`, `rg` 설치
- 외부 런타임(Vault/PostgreSQL/Valkey) 기동 상태
- 인증서 파일 준비: `secrets/certs/cert.pem`, `secrets/certs/key.pem`, `secrets/certs/rootCA.pem`

### WSL2 커널 파라미터 사전 확인

k3d 4노드(server-0 + agent-0/1/2) 구성은 각 노드마다 kubelet/containerd/k3s가 다수의 inotify 인스턴스를 소비한다.
기본값(128)이 부족하면 kubelet이 `inotify_init: too many open files`로 실패하며 노드가 NotReady 상태가 된다.

```bash
# 현재 값 확인
cat /proc/sys/fs/inotify/max_user_instances  # 512 이상 필요

# 부족한 경우 조정 (sudo 필요)
sudo sysctl -w fs.inotify.max_user_instances=1024
echo 'fs.inotify.max_user_instances=1024' | sudo tee /etc/sysctl.d/99-k3d.conf
```

`bootstrap-local.sh`는 이 값을 512 미만이면 즉시 실패시킨다.

### Vault Docker 네트워크 연결 확인

Vault 컨테이너는 k3d-hyhome Docker 네트워크에 연결되어 있어야 한다.
k3d 노드는 infra_net(172.19.0.0/16)에 라우트가 없으므로, Vault가 infra_net에만 있으면
`vault-external` EndpointSlice를 통한 k3d → Vault 연결이 불가능하다.

```bash
# vault가 k3d-hyhome 네트워크에 있는지 확인
docker inspect vault --format '{{(index .NetworkSettings.Networks "k3d-hyhome").IPAddress}}'

# 없는 경우 연결 (human-approved bootstrap/break-glass only)
docker network connect k3d-hyhome vault
```

### 로컬 툴체인 사전 요구사항

정적 검증과 pre-commit 훅을 로컬에서 실행하려면 아래 도구가 필요하다.
CI에서는 `pre-commit/action@v3.0.1`이 모든 도구를 자동 설치하므로 CI 커버리지에는 영향이 없다.
로컬 PATH 설정이 불일치하면 pre-commit 훅이 조용히 스킵될 수 있다.

#### 필수 도구 설치

```bash
# pre-commit (훅 러너)
pip install pre-commit
# 또는: pip3 install pre-commit

# shellcheck (셸 스크립트 린팅) — Ubuntu/Debian
sudo apt-get install shellcheck

# actionlint (GitHub Actions 워크플로우 린팅)
go install github.com/rhysd/actionlint/cmd/actionlint@latest

# zizmor (워크플로우 보안 스캐닝)
pip install zizmor

# kube-linter (Kubernetes 매니페스트 린팅)
go install golang.stackrox.io/kube-linter/cmd/kube-linter@latest
```

#### 선택 도구 설치

```bash
# graphify (지식 그래프, 선택사항)
# rtk (Codex CLI 프록시, 선택사항)
which graphify rtk 2>/dev/null || echo "Optional tools not installed — CI unaffected"
```

#### WSL2 비대화형 셸 PATH 설정

WSL2 비대화형 셸(pre-commit, CI 에뮬레이션)은 `.bashrc`/`.zshrc`를 로드하지 않으므로
`~/.local/bin`, `~/.go/bin` 등이 PATH에서 누락될 수 있다.

```bash
# ~/.profile에 추가 (로그인 셸에서 적용)
echo 'export PATH="$HOME/.local/bin:$(go env GOPATH)/bin:$PATH"' >> ~/.profile

# 시스템 전체 적용이 필요한 경우 /etc/environment 수정 (sudo 필요, 재부팅 후 적용)
# sudo sed -i 's|PATH="|PATH="/home/<user>/.local/bin:/home/<user>/go/bin:|' /etc/environment
```

#### 설치 검증

```bash
command -v shellcheck actionlint zizmor pre-commit kube-linter
# 각 도구가 경로를 출력하면 정상

pre-commit run --all-files  # 로컬 전체 pre-commit 검증
```

> **참고**: CI는 `.github/workflows/ci.yml`의 `pre-commit/action@v3.0.1`이 actionlint, zizmor,
> shellcheck, kube-linter 등을 런타임에 자동 설치한다. 로컬 PATH 불일치는 로컬 개발자 경험(DX)
> 문제이며 CI 커버리지에는 영향이 없다.

## Step-by-step Instructions

1. 클러스터 baseline을 생성/확인한다.

```bash
k3d cluster create --config infrastructure/k3d/k3d-cluster.yaml
kubectl get nodes -o wide
```

1. 인증서 SAN과 ArgoCD 호스트 계약을 점검한다.

```bash
openssl x509 -in secrets/certs/cert.pem -noout -ext subjectAltName | \
  rg '127\.0\.0\.1\.nip\.io|\*\.127\.0\.0\.1\.nip\.io'
```

1. SAN이 미포함이면 재발급 후 동일 경로에 교체한다.

- 재발급 절차: [`../runbooks/0002-argocd-eso-vault-recovery-runbook.md#troubleshooting-signatures`](../runbooks/0002-argocd-eso-vault-recovery-runbook.md#troubleshooting-signatures)

1. 부트스트랩 스크립트로 TLS Secret까지 포함해 초기화를 실행한다.

```bash
export VAULT_TOKEN='<redacted>'
./infrastructure/bootstrap-local.sh
```

1. ArgoCD 및 GitOps root app 상태를 확인한다.

```bash
kubectl -n argocd get application root-platform -o yaml | \
  rg 'path: gitops/apps/root|targetRevision: main'
kubectl -n argocd get applications
```

1. 외부 서비스 인터페이스 계약을 검증한다.

```bash
kubectl -n platform get svc,endpointslice | \
  rg 'postgres-(write|read)-external|15432|15433|172.18.0.15|vault-external|172.18.0.8|8200|valkey-external|172.18.0.9|6379'
```

1. vault-external EndpointSlice를 Vault의 k3d-hyhome IP로 설정한다.

```bash
VAULT_K3D_IP=$(docker inspect vault --format '{{(index .NetworkSettings.Networks "k3d-hyhome").IPAddress}}')
echo "Vault k3d IP: $VAULT_K3D_IP"

# EndpointSlice에 k3d-hyhome IP 적용 (human-approved bootstrap/break-glass only)
cat <<YAML | kubectl apply -f -
apiVersion: discovery.k8s.io/v1
kind: EndpointSlice
metadata:
  name: vault-external-1
  namespace: platform
  labels:
    kubernetes.io/service-name: vault-external
addressType: IPv4
ports:
  - name: http
    protocol: TCP
    port: 8200
endpoints:
  - addresses:
      - ${VAULT_K3D_IP}
YAML
```

> **이유**: `vault-external.platform.svc.cluster.local`은 k8s 내부 Service DNS → EndpointSlice IP로 라우팅된다.
> k3d 노드는 Vault의 infra_net IP(172.19.0.9)로 패킷을 전달할 수 없으므로, k3d-hyhome 네트워크 IP를 사용해야 한다.

1. Vault Kubernetes auth 설정이 올바른지 확인한다.

```bash
# Vault Kubernetes auth 설정 확인 (kubernetes_host가 172.18.0.2:6443이어야 함)
curl -ksS -H "X-Vault-Token: $VAULT_TOKEN" \
  https://vault.127.0.0.1.nip.io/v1/auth/kubernetes/config | \
  python3 -c "import sys,json; d=json.load(sys.stdin)['data']; \
  print('host:', d['kubernetes_host']); \
  print('token_reviewer_jwt_set:', d.get('token_reviewer_jwt_set')); \
  print('disable_local_ca_jwt:', d['disable_local_ca_jwt'])"
```

필요 시 수동 재설정:

```bash
# ESO SA 토큰 발급 (token reviewer JWT 용)
ESO_TOKEN=$(kubectl -n external-secrets create token external-secrets --duration=87600h)

# Vault Kubernetes auth 업데이트
EXISTING_CA=$(curl -ksS -H "X-Vault-Token: $VAULT_TOKEN" \
  https://vault.127.0.0.1.nip.io/v1/auth/kubernetes/config | \
  python3 -c "import sys,json; print(json.load(sys.stdin)['data']['kubernetes_ca_cert'])")

curl -ksS -X POST \
  -H "X-Vault-Token: $VAULT_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"kubernetes_host\": \"https://172.18.0.2:6443\",
    \"kubernetes_ca_cert\": $(echo "$EXISTING_CA" | python3 -c "import sys,json; print(json.dumps(sys.stdin.read()))"),
    \"token_reviewer_jwt\": \"$ESO_TOKEN\",
    \"disable_local_ca_jwt\": true
  }" \
  https://vault.127.0.0.1.nip.io/v1/auth/kubernetes/config
```

## Local Runtime Validation vs CI Static Validation

### Local Runtime Validation (cluster required)

```bash
./infrastructure/tests/run-all.sh
CHECK_TRAEFIK_443=true ./infrastructure/tests/verify-ingress-tls.sh
```

### CI Static Validation (cluster not required)

```bash
./infrastructure/tests/verify-contracts-static.sh
bash -n infrastructure/bootstrap-local.sh infrastructure/tests/*.sh
```

### Workflow Security Validation

`.github/workflows/**` 변경 시 CI에서 자동 수행:

- `actionlint`
- `zizmor`

## Common Pitfalls

- `fs.inotify.max_user_instances < 512` → k3d 에이전트 노드 NotReady, kubelet `too many open files`
- Docker 재시작 후 vault가 k3d-hyhome 네트워크에서 분리됨 → `vault-backend context deadline exceeded`
- `vault-external` EndpointSlice IP가 infra_net(172.19.0.9) → k3d 노드에서 Connection refused
- Vault Kubernetes auth `kubernetes_host`가 `kubernetes.default.svc`(k8s 내부 DNS) → DNS 미해석으로 timeout
- `token_reviewer_jwt` 미설정 시 `disable_local_ca_jwt: true` 조합에서 Vault가 token review 불가
- AppProject wildcard 복원으로 과권한 상태 재발
- `cert.pem` SAN 누락으로 TLS handshake 실패
- 로컬 파일만 수정하고 원격 `main`에 반영하지 않아 ArgoCD 미동기화
- k3d 에이전트 노드 동시 재시작(thundering herd) → containerd inotify 순간 초과 → CRI plugin 실패
  → **해결**: 에이전트 노드를 순차적으로(하나씩) 재시작

## Related Documents

- **Spec**: [`../../03.specs/002-wsl2-k3d-argocd-ha-platform/spec.md`](../../03.specs/002-wsl2-k3d-argocd-ha-platform/spec.md)
- **Operation**: [`../policies/0002-wsl2-k3d-gitops-ha-operations-policy.md`](../policies/0002-wsl2-k3d-gitops-ha-operations-policy.md)
- **Runbook**: [`../runbooks/0002-argocd-eso-vault-recovery-runbook.md`](../runbooks/0002-argocd-eso-vault-recovery-runbook.md)
