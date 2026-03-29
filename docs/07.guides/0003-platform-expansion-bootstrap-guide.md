# Platform Expansion Bootstrap Guide

## Overview (KR)

이 문서는 cert-manager, Kubernetes Dashboard, Istio, Kiali가 추가된 확장 플랫폼을 WSL2에서 부트스트랩하는 방법을 설명한다.
기존 `bootstrap-local.sh` 기반 흐름을 확장하며, 신규 컴포넌트의 사전 조건과 검증 절차를 포함한다.

## Guide Type

`how-to`

## Target Audience

- Platform Engineer
- DevOps Engineer

## Purpose

외부 서비스 IP 수정과 신규 컴포넌트(cert-manager/Dashboard/Istio/Kiali)를 포함한 플랫폼을 재현 가능하게 부트스트랩하고 검증한다.

## Prerequisites

### 필수 도구

```bash
k3d --version   # v5.8.3 이상
kubectl version --client
helm version    # v3.x
docker info
curl --version
jq --version
openssl version
```

### 필수 파일

```
secrets/certs/cert.pem          # argocd용 TLS cert (mkcert 발급)
secrets/certs/key.pem           # argocd용 TLS key
secrets/certs/rootCA.pem        # mkcert rootCA cert
secrets/certs/rootCA-key.pem    # mkcert rootCA key (cert-manager ClusterIssuer용)
```

> **rootCA.pem이 로컬 신뢰 저장소에 등록되어 있어야** Dashboard/Kiali HTTPS 접근이 브라우저에서 신뢰된다.

### 환경 변수

```bash
export VAULT_TOKEN="<token>"
export VAULT_ADDR="https://vault.127.0.0.1.nip.io"   # 또는 실제 주소
# 선택적 오버라이드:
export ARGOCD_HOST="argocd.127.0.0.1.nip.io"
export POSTGRES_WRITE_ADDR="172.19.0.11"
export POSTGRES_READ_ADDR="172.19.0.11"
export VALKEY_ADDR="172.19.0.12"
```

### 외부 서비스 확인

```bash
# infra_net 서비스 연결 확인
curl -ks https://vault.127.0.0.1.nip.io/v1/sys/health | jq '.sealed'
nc -z 172.19.0.11 15432 && echo "postgres-write OK"
nc -z 172.19.0.12 6379 && echo "valkey OK"
nc -z 172.19.0.20 9090  && echo "prometheus OK"  # Kiali용
nc -z 172.19.0.21 3100  && echo "loki OK"        # 로그 수집
nc -z 172.19.0.22 3200  && echo "tempo OK"       # Kiali/트레이싱용
nc -z 172.19.0.23 4317  && echo "alloy OK"       # OTLP gRPC 수신
nc -z 172.19.0.24 3000  && echo "grafana OK"     # Kiali용
```

## Step-by-step Instructions

### 0. Docker Traefik 동적 설정 배포 (신규 호스트명 필요 시)

Dashboard(`k8s-dashboard.127.0.0.1.nip.io`)와 Kiali(`kiali.127.0.0.1.nip.io`)에 접근하려면
외부 Docker Traefik에 라우팅 파일이 등록되어 있어야 한다.

```bash
# Docker Traefik의 동적 설정 마운트 경로 확인 (예시)
# docker inspect <traefik-container> | jq '.[].Mounts'

# traefik/ 디렉토리의 라우팅 파일을 동적 설정 디렉토리에 복사
cp traefik/dashboard-k3d.yaml  <traefik-dynamic-conf-dir>/
cp traefik/kiali-k3d.yaml      <traefik-dynamic-conf-dir>/
# argocd-k3d.yaml은 이미 배포되어 있으면 생략 가능

# Traefik이 파일 변경을 자동 감지함 (File Provider)
# 신규 라우터 등록 확인: Traefik 대시보드 또는 로그 확인
```

> **Note**: Traefik 라우팅 파일은 외부 관리 대상이며 이 repo에서 직접 배포하지 않는다.
> `traefik/*.yaml`은 참조 복사본이다 (운영 정책: `0003-service-mesh-cert-manager-policy.md` §Traefik Router 계약).

### 1. 기존 플랫폼 부트스트랩 (변경 없음)

```bash
cd /path/to/hy-home.k8s
VAULT_TOKEN="<token>" bash infrastructure/bootstrap-local.sh
```

bootstrap 단계 (`[1/11]`~`[11/11]`):

1. k3d 클러스터 생성/재사용
2. 외부 의존성 검증 (vault/postgres/valkey TCP + Vault에서 `valkey_password` 읽기)
3. TLS cert 검증 (4개 파일 존재 + SAN 확인)
4. 관측성 endpoints pre-check (warn-only: prometheus/loki/tempo/alloy/grafana)
5. MetalLB 설치 + IPAddressPool + L2Advertisement 적용
6. argocd namespace + Secrets (valkey + TLS) 생성
7. cert-manager namespace + `mkcert-root-ca` Secret 주입
8. ArgoCD Helm 설치
9. GitOps 부트스트랩 리소스 적용
10. ArgoCD 컨트롤 플레인 대기
11. Done (URL 출력 + rootCA hint)

### 2. cert-manager ClusterIssuer 검증

```bash
# ArgoCD가 cert-manager를 sync한 후
kubectl -n cert-manager get deployment cert-manager
kubectl get clusterissuer mkcert-ca-issuer -o jsonpath='{.status.conditions[0].type}'
# 출력: Ready
```

> ClusterIssuer가 `NotReady` 상태면 rootCA Secret 확인:
>
> ```bash
> kubectl -n cert-manager get secret mkcert-root-ca
> ```

### 3. Kubernetes Dashboard 검증

ArgoCD가 `platform-dashboard` 앱을 sync하면:

```bash
kubectl -n kubernetes-dashboard get deployment kubernetes-dashboard
kubectl -n kubernetes-dashboard get certificate dashboard-tls
# 출력: READY=True

# 토큰 발급
kubectl -n kubernetes-dashboard create token dashboard-admin
```

브라우저에서 `https://k8s-dashboard.127.0.0.1.nip.io` 접근 후 토큰 입력.

### 4. Istio 설치 검증

ArgoCD가 `platform-istio-base` → `platform-istiod` 순서로 sync:

```bash
# CRD 설치 확인
kubectl get crd | grep istio.io | head -5

# istiod 가용성
kubectl -n istio-system get deployment istiod
kubectl -n istio-system get pods -l app=istiod
```

### 5. Kiali 설치 검증

```bash
kubectl -n istio-system get deployment kiali
kubectl -n istio-system get certificate kiali-tls

# Kiali Prometheus 연결 확인
kubectl -n istio-system logs deploy/kiali | grep -i "prometheus"
```

브라우저에서 `https://kiali.127.0.0.1.nip.io` 접근.

### 6. 전체 정적 계약 검증

```bash
./infrastructure/tests/verify-contracts-static.sh
```

### 7. 전체 런타임 검증

```bash
./infrastructure/tests/run-all.sh
CHECK_TRAEFIK_443=true ./infrastructure/tests/verify-ingress-tls.sh
```

## Common Pitfalls

### rootCA-key.pem이 없는 경우

cert-manager ClusterIssuer는 CA key가 필요하다. mkcert rootCA key 경로:

```bash
# macOS/Linux
$(mkcert -CAROOT)/rootCA-key.pem
# WSL2에서 mkcert 설치한 경우
$HOME/.local/share/mkcert/rootCA-key.pem
```

`secrets/certs/rootCA-key.pem`에 복사 후 bootstrap 재실행.

### Istio sidecar가 기존 pod에 주입된 경우

기존 namespace(argocd 등)에 `istio-injection=enabled` 레이블이 붙으면 재시작 시 사이드카가 주입된다. 확인:

```bash
kubectl get namespace --show-labels | grep istio-injection
```

의도치 않은 namespace의 레이블은 즉시 제거한다.

### Kiali에서 "No Prometheus" 오류

egress NetworkPolicy cidr 확인:

```bash
kubectl -n istio-system get networkpolicy kiali-egress-to-observability -o yaml
```

`172.19.0.20/32` (Prometheus) cidr이 누락된 경우 manifest 수정 후 ArgoCD sync.

### Dashboard Token이 Unauthorized

```bash
kubectl -n kubernetes-dashboard get clusterrolebinding dashboard-admin
kubectl -n kubernetes-dashboard create token dashboard-admin --duration=24h
```

## Related Documents

- **Spec**: [`../04.specs/003-platform-expansion/spec.md`](../04.specs/003-platform-expansion/spec.md)
- **Operation**: [`../08.operations/0003-service-mesh-cert-manager-policy.md`](../08.operations/0003-service-mesh-cert-manager-policy.md)
- **Runbook**: [`../09.runbooks/0003-platform-expansion-bootstrap-runbook.md`](../09.runbooks/0003-platform-expansion-bootstrap-runbook.md)
- **Previous Guide**: [`./0002-wsl2-k3d-argocd-ha-setup-guide.md`](./0002-wsl2-k3d-argocd-ha-setup-guide.md)
