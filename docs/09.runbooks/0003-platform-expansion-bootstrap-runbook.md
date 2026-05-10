# Platform Expansion Bootstrap Runbook

: WSL2 k3d Platform — cert-manager / Headlamp / Istio / Kiali

## Overview (KR)

이 런북은 cert-manager, Headlamp, Istio, Kiali가 추가된 확장 플랫폼을 부트스트랩하거나 복구하기 위한 즉시 실행 가능한 체크리스트와 증상별 복구 절차를 제공한다.

> 현재 클러스터 UI 계약은 ADR-0010에 따라 Kubernetes Dashboard가 아니라 Headlamp다.
> 오래된 Dashboard 절차는 현재 실행 기준이 아니며, Headlamp 상세 인증 절차는 `0005-headlamp-keycloak-runbook.md`를 따른다.

## Purpose

플랫폼 확장 컴포넌트의 부트스트랩 단계를 재현 가능하게 수행하고, 장애 발생 시 원인별 복구 명령을 제공한다.

## Canonical References

- [`../04.specs/003-platform-expansion/spec.md`](../04.specs/003-platform-expansion/spec.md)
- [`../07.guides/0003-platform-expansion-bootstrap-guide.md`](../07.guides/0003-platform-expansion-bootstrap-guide.md)
- [`../08.operations/0003-service-mesh-cert-manager-policy.md`](../08.operations/0003-service-mesh-cert-manager-policy.md)
- [`../03.adr/0006-cert-manager-mkcert-ca-issuer.md`](../03.adr/0006-cert-manager-mkcert-ca-issuer.md)

## When to Use

- 신규 플랫폼 확장 컴포넌트 설치
- WSL2 재시작 또는 k3d 클러스터 재생성 후 복구
- cert-manager ClusterIssuer NotReady 복구
- Headlamp Token 만료 또는 접근 불가
- Istio/Kiali 배포 실패 복구

## Procedure or Checklist

### Checklist

- [ ] `secrets/certs/cert.pem` / `key.pem` 존재 (ArgoCD용)
- [ ] `secrets/certs/rootCA.pem` 존재 (cert-manager용)
- [ ] `secrets/certs/rootCA-key.pem` 존재 (ClusterIssuer CA key)
- [ ] `rootCA.pem`이 로컬 신뢰 저장소에 등록됨
- [ ] `VAULT_TOKEN` 환경변수 설정
- [ ] Vault unseal 상태: `curl -ks https://vault.127.0.0.1.nip.io/v1/sys/health | jq '.sealed'` → `false`
- [ ] PostgreSQL 연결: `nc -z 172.18.0.15 15432`
- [ ] Valkey 연결: `nc -z 172.18.0.9 6379`
- [ ] Prometheus 연결 (Kiali용): `nc -z 172.18.0.10 9090`
- [ ] Loki 연결 (로그 수집): `nc -z 172.18.0.13 3100`
- [ ] Tempo 연결 (트레이싱): `nc -z 172.18.0.12 3200`
- [ ] Alloy OTLP 연결: `nc -z 172.18.0.11 4317`
- [ ] Grafana 연결 (Kiali용): `nc -z 172.18.0.14 3000`

### Procedure

0. Docker Traefik 동적 설정 파일 배포

   신규 호스트명(Headlamp/Kiali)에 처음 접근하는 경우, 외부 Docker Traefik에 라우터를 등록한다:

   ```bash
   # Traefik 동적 설정 마운트 경로에 파일 복사
   cp traefik/headlamp-k3d.yaml  <traefik-dynamic-conf-dir>/
   cp traefik/kiali-k3d.yaml     <traefik-dynamic-conf-dir>/
   ```

   ArgoCD 라우터(`argocd-k3d.yaml`)가 이미 등록된 경우 생략 가능. Traefik이 File Provider로 자동 감지한다.

1. 기본 플랫폼 부트스트랩 실행

   ```bash
   VAULT_TOKEN="<token>" bash infrastructure/bootstrap-local.sh
   ```

   bootstrap 내부 단계 (`[1/11]`~`[11/11]`):
   - `[1/11]` k3d 클러스터 생성/재사용
   - `[2/11]` 외부 의존성 검증 (vault/postgres/valkey TCP + valkey_password 읽기)
   - `[3/11]` TLS cert 검증 (4개 파일 + SAN)
   - `[4/11]` 관측성 pre-check warn-only (prometheus/loki/tempo/alloy/grafana)
   - `[5/11]` MetalLB + IPAddressPool + L2Advertisement 설치
   - `[6/11]` argocd namespace + Secrets (valkey + TLS)
   - `[7/11]` cert-manager namespace + mkcert-root-ca Secret 주입
   - `[8/11]` ArgoCD Helm 설치
   - `[9/11]` GitOps 부트스트랩 리소스 적용
   - `[10/11]` ArgoCD 컨트롤 플레인 대기
   - `[11/11]` Done

2. cert-manager ClusterIssuer 상태 확인

   ```bash
   kubectl -n cert-manager get deployment cert-manager
   kubectl get clusterissuer mkcert-ca-issuer \
     -o jsonpath='{.status.conditions[0].type}'
   # 출력: Ready
   ```

3. Headlamp 접근 검증

   ```bash
   kubectl -n headlamp get pods,ingress,svc
   kubectl -n headlamp get certificate headlamp-tls 2>/dev/null || \
   kubectl -n headlamp get secret headlamp-tls
   curl -ksS -o /dev/null -w '%{http_code}' https://headlamp.127.0.0.1.nip.io/
   ```

4. Istio 가용성 확인

   ```bash
   kubectl get crd | grep istio.io | wc -l   # 10개 이상
   kubectl -n istio-system get deployment istiod
   ```

5. Kiali 가용성 + Prometheus 연결 확인

   ```bash
   kubectl -n istio-system get deployment kiali
   kubectl -n istio-system logs deploy/kiali | grep -i prometheus | tail -5
   ```

6. 전체 정적 계약 검증

   ```bash
   ./infrastructure/tests/verify-contracts-static.sh
   ```

## Safe Rollback or Recovery Procedure

### cert-manager ClusterIssuer NotReady

**증상**: `kubectl get clusterissuer mkcert-ca-issuer` → `READY=False`

> **Execution boundary**: Secret 재주입과 controller 재시작은 bootstrap 또는 human-approved break-glass 전용이다.

```bash
# 1. rootCA Secret 존재 확인
kubectl -n cert-manager get secret mkcert-root-ca

# 2. Secret 없으면 재주입 (bootstrap/break-glass only)
kubectl -n cert-manager create secret tls mkcert-root-ca \
  --cert=secrets/certs/rootCA.pem \
  --key=secrets/certs/rootCA-key.pem \
  --dry-run=client -o yaml | kubectl apply -f -

# 3. cert-manager controller 재시작
kubectl -n cert-manager rollout restart deploy/cert-manager

# 4. ClusterIssuer 상태 재확인 (30초 대기)
kubectl wait clusterissuer mkcert-ca-issuer \
  --for=condition=Ready --timeout=60s
```

### Headlamp TLS NotReady

**증상**: `kubectl -n headlamp get certificate headlamp-tls` → `READY=False`

```bash
# 1. ClusterIssuer Ready 상태 선행 확인 (위 절차 참조)

# 2. Certificate 이벤트 확인
kubectl -n headlamp describe certificate headlamp-tls

# 3. cert-manager 로그 확인
kubectl -n cert-manager logs deploy/cert-manager | grep -i "headlamp" | tail -20

# 4. Certificate CR 재apply (ArgoCD hard-refresh)
argocd app get platform-headlamp-config --hard-refresh
```

### Headlamp Token Unauthorized

**증상**: 브라우저 `https://headlamp.127.0.0.1.nip.io` 접근 시 401

```bash
# ClusterRoleBinding 확인
kubectl get clusterrolebinding headlamp-admin

# 토큰 재발급
kubectl -n headlamp create token headlamp-admin --duration=1h
```

### Istiod CrashLoop / OOMKilled

**증상**: `kubectl -n istio-system get pods -l app=istiod` → CrashLoopBackOff 또는 OOMKilled

```bash
# 1. 자원 사용량 확인
kubectl -n istio-system top pod -l app=istiod

# 2. istiod Helm values에서 requests 축소
# gitops/platform/istio/istiod-values.yaml 수정:
#   pilot.resources.requests.memory: "64Mi"  # 128Mi → 64Mi
# ArgoCD sync 후 확인

# 3. 재시작
kubectl -n istio-system rollout restart deploy/istiod
```

### Kiali "No Prometheus" 오류

**증상**: Kiali UI에서 "No Prometheus" 또는 "Prometheus unreachable"

```bash
# 1. Prometheus 연결 확인
nc -z 172.18.0.10 9090 && echo "OK" || echo "FAIL"

# 2. egress NetworkPolicy 확인
kubectl -n istio-system get networkpolicy kiali-egress-to-observability -o yaml
# cidr 172.18.0.10/32 존재 여부 확인

# 3. Kiali config 확인
kubectl -n istio-system get configmap kiali -o yaml | grep prometheus

# 4. Kiali 재시작
kubectl -n istio-system rollout restart deploy/kiali
```

### Istio CRD 없이 istiod 설치 오류

**증상**: `platform-istiod` ArgoCD app sync 실패 — CRD not found

```bash
# 1. istio-base sync 상태 확인
argocd app get platform-istio-base

# 2. operator-triggered reconciliation only (sync-wave 강제)
argocd app sync platform-istio-base --prune

# 3. CRD 설치 확인 후 istiod sync
kubectl get crd | grep istio.io | wc -l
# operator-triggered reconciliation only
argocd app sync platform-istiod
```

## Verification Steps

```bash
# 정적 계약
./infrastructure/tests/verify-contracts-static.sh

# 런타임
kubectl get clusterissuer mkcert-ca-issuer
kubectl -n headlamp get certificate headlamp-tls 2>/dev/null || kubectl -n headlamp get secret headlamp-tls
kubectl -n istio-system get deploy istiod kiali

# TLS 접근
curl -sk https://headlamp.127.0.0.1.nip.io -o /dev/null -w '%{http_code}\n'
curl -sk https://kiali.127.0.0.1.nip.io -o /dev/null -w '%{http_code}\n'
```

## Observability and Evidence Sources

- **Signals**: ClusterIssuer readiness, Headlamp TLS state, Istiod/Kiali deployment availability, ArgoCD Application health.
- **Evidence to Capture**: static contract output, relevant Kubernetes events, cert-manager logs, Kiali Prometheus connection logs.

## Related Documents

- **Guide**: [`../07.guides/0003-platform-expansion-bootstrap-guide.md`](../07.guides/0003-platform-expansion-bootstrap-guide.md)
- **Spec**: [`../04.specs/003-platform-expansion/spec.md`](../04.specs/003-platform-expansion/spec.md)
- **Operations**: [`../08.operations/0003-service-mesh-cert-manager-policy.md`](../08.operations/0003-service-mesh-cert-manager-policy.md)
- **ADR-0010**: [`../03.adr/0010-headlamp-replaces-dashboard.md`](../03.adr/0010-headlamp-replaces-dashboard.md)
- **Previous Runbook**: [`./0001-argocd-platform-bootstrap-runbook.md`](./0001-argocd-platform-bootstrap-runbook.md)
