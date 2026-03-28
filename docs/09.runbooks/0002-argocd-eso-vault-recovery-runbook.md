# ArgoCD ESO Vault Recovery Runbook

## Runbook Type

`WSL2 k3d/k3s 운영 핫픽스`

## Overview (KR)

이 런북은 `ClusterSecretStore/vault-backend Ready=False` 상황에서 수동 EndpointSlice 핫픽스로 연동을 복구하고, ArgoCD/ESO 상태를 정상화한 뒤 TLS/CI 계약 회귀를 점검하는 절차를 제공한다.

## Purpose

`vault-external` endpoint 부재 또는 연결 거부로 발생하는 ESO/Vault 연동 장애를 빠르게 복구하고, 계약 회귀를 방지한다.

## Canonical References

- [`../02.ard/0002-wsl2-k3d-argocd-ha-platform.md`](../02.ard/0002-wsl2-k3d-argocd-ha-platform.md)
- [`../03.adr/0005-wsl2-ha-baseline-and-external-endpoint-contract.md`](../03.adr/0005-wsl2-ha-baseline-and-external-endpoint-contract.md)
- [`../04.specs/002-wsl2-k3d-argocd-ha-platform/spec.md`](../04.specs/002-wsl2-k3d-argocd-ha-platform/spec.md)
- [`../05.plans/2026-03-28-wsl2-k3d-argocd-ha-platform.md`](../05.plans/2026-03-28-wsl2-k3d-argocd-ha-platform.md)

## When to Use

- `vault-backend`가 `Ready=False`
- ESO 로그에 `connection refused` 또는 `InvalidProviderConfig` 반복
- `argocd-external-valkey`가 `SecretSyncedError`
- 복구 후 ArgoCD HTTPS 진입점(`argocd.127.0.0.1.nip.io`) 회귀가 의심될 때

## Procedure or Checklist

### Checklist

- [ ] `kubectl` 컨텍스트 확인
- [ ] 평문 시크릿/토큰 출력 금지
- [ ] 복구 전 상태 스냅샷 수집

### Procedure

1. 사전 스냅샷을 저장한다.

```bash
kubectl -n external-secrets get clustersecretstore vault-backend -o yaml
kubectl -n argocd get externalsecret argocd-external-valkey -o yaml
kubectl -n argocd get app platform-eso-config platform-argocd-config -o wide
kubectl -n external-secrets logs deploy/external-secrets --tail=200 | \
  rg -i 'vault|clustersecretstore|error|connection refused'
```

1. `EndpointSlice` 핫픽스를 적용한다.

```bash
cat <<'YAML' | kubectl apply -f -
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
      - 172.30.0.10
YAML
```

1. Store/ExternalSecret/ArgoCD 상태를 재평가한다.

```bash
kubectl -n platform get endpointslice vault-external-1 -o yaml
kubectl -n external-secrets get clustersecretstore vault-backend
kubectl -n argocd get externalsecret argocd-external-valkey
kubectl -n argocd get app platform-eso-config platform-argocd-config
```

1. 필요 시 ArgoCD 재평가/동기화를 수행한다.

```bash
argocd app get platform-eso-config --hard-refresh
argocd app get platform-argocd-config --hard-refresh
argocd app sync platform-eso-config
argocd app sync platform-argocd-config
```

1. 런타임 계약 회귀를 검증한다.

```bash
./infrastructure/tests/verify-network-policies.sh
./infrastructure/tests/verify-ingress-tls.sh
CHECK_TRAEFIK_443=true ./infrastructure/tests/verify-ingress-tls.sh
./infrastructure/tests/run-all.sh
```

1. CI 정적 계약 회귀를 검증한다.

```bash
./infrastructure/tests/verify-contracts-static.sh
bash -n infrastructure/bootstrap-local.sh infrastructure/tests/*.sh
```

1. GitOps source gate를 확인한다(로컬 파일 수정만으로 반영되지 않음).

```bash
kubectl -n argocd get app root-platform -o yaml | \
  rg 'path: gitops/apps/root|targetRevision: main'
```

## Verification Steps

- [ ] `vault-backend Ready=True`
- [ ] `argocd-external-valkey Ready=True`
- [ ] `platform-eso-config`, `platform-argocd-config` Degraded 해소
- [ ] 포트/서비스 계약 회귀 없음
- [ ] `argocd` egress(Valkey + DNS + HTTPS) 통과
- [ ] ingress/TLS 계약(host=`argocd.127.0.0.1.nip.io`, secret=`argocd-local-tls`) 유지 # pragma: allowlist secret
- [ ] Traefik 443 및 fallback 8443 HTTPS 응답 확인
- [ ] CI 정적 계약(`verify-contracts-static.sh`) 통과

## Troubleshooting Signatures

- `connection refused` on `vault-external.platform.svc.cluster.local:8200`
- `InvalidProviderConfig` in ESO controller logs
- `argocd-external-valkey SecretSyncedError`
- TLS handshake error due to SAN mismatch (`cert.pem`)

### SAN mismatch remediation

```bash
openssl x509 -in secrets/certs/cert.pem -noout -ext subjectAltName | \
  rg '127\.0\.0\.1\.nip\.io|\*\.127\.0\.0\.1\.nip\.io'
# 미포함 시 인증서 재발급 후 bootstrap 재실행
./infrastructure/bootstrap-local.sh
```

## Safe Rollback or Recovery Procedure

```bash
kubectl -n platform delete endpointslice vault-external-1
```

- 롤백 후 `verify-contracts-static.sh`와 `run-all.sh`를 재실행한다.
- 동일 증상이 반복되면 Operations 예외 승인 절차를 따른다.

## Related Operational Documents

- **Guide**: [`../07.guides/0002-wsl2-k3d-argocd-ha-setup-guide.md`](../07.guides/0002-wsl2-k3d-argocd-ha-setup-guide.md)
- **Operations Policy**: [`../08.operations/0002-wsl2-k3d-gitops-ha-operations-policy.md`](../08.operations/0002-wsl2-k3d-gitops-ha-operations-policy.md)
