# ArgoCD ESO Vault Recovery Runbook

: WSL2 k3d/k3s 운영 핫픽스

## Overview (KR)

이 런북은 `ClusterSecretStore/vault-backend Ready=False` 상황에서 수동 EndpointSlice 핫픽스로 연동을 복구하고, ArgoCD/ESO 상태를 정상화하는 즉시 실행 절차를 제공한다.

## Purpose

`vault-external` endpoint 부재 또는 연결 거부로 발생하는 ESO/Vault 연동 장애를 빠르게 복구한다.

## Canonical References

- [`../02.ard/0002-wsl2-k3d-argocd-ha-platform.md`](../02.ard/0002-wsl2-k3d-argocd-ha-platform.md)
- [`../03.adr/0005-wsl2-ha-baseline-and-external-endpoint-contract.md`](../03.adr/0005-wsl2-ha-baseline-and-external-endpoint-contract.md)
- [`../04.specs/002-wsl2-k3d-argocd-ha-platform/spec.md`](../04.specs/002-wsl2-k3d-argocd-ha-platform/spec.md)
- [`../05.plans/2026-03-28-wsl2-k3d-argocd-ha-platform.md`](../05.plans/2026-03-28-wsl2-k3d-argocd-ha-platform.md)

## When to Use

- `vault-backend`가 `Ready=False`
- ESO 로그에 `connection refused` 또는 `InvalidProviderConfig` 반복
- `argocd-external-valkey`가 `SecretSyncedError`

## Procedure or Checklist

### Checklist

- [ ] `kubectl` 컨텍스트가 대상 클러스터인지 확인
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

2. `EndpointSlice` 핫픽스를 적용한다.

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

3. Store/ExternalSecret/ArgoCD 상태를 재평가한다.

```bash
kubectl -n platform get endpointslice vault-external-1 -o yaml
kubectl -n external-secrets get clustersecretstore vault-backend
kubectl -n argocd get externalsecret argocd-external-valkey
kubectl -n argocd get app platform-eso-config platform-argocd-config
```

4. 필요 시 ArgoCD 재평가/동기화를 수행한다.

```bash
argocd app get platform-eso-config --hard-refresh
argocd app get platform-argocd-config --hard-refresh
argocd app sync platform-eso-config
argocd app sync platform-argocd-config
```

5. 회귀 검증을 수행한다.

```bash
kubectl -n argocd get application root-platform -o yaml | \
  rg 'path: gitops/apps/root|targetRevision: main'
kubectl -n platform get svc,endpointslice | \
  rg 'postgres-(write|read)-external|15432|15433|vault-external|8200|valkey-external|172.30.0.12|26379'
./infrastructure/tests/verify-network-policies.sh
```

## Verification Steps

- [ ] `vault-backend Ready=True`
- [ ] `argocd-external-valkey Ready=True`
- [ ] `platform-eso-config`, `platform-argocd-config`에서 Degraded 해소
- [ ] 포트/서비스 계약 회귀 없음
- [ ] 네트워크 정책 계약(`argocd`/`external-secrets` egress) 통과

## Observability and Evidence Sources

- **Signals**: ExternalSecrets controller logs, ClusterSecretStore status, ArgoCD app health
- **Evidence to Capture**:
  - 전/후 상태 YAML (`ClusterSecretStore`, `ExternalSecret`, `Application`)
  - 오류 시그니처 로그 (`connection refused`, `InvalidProviderConfig`)
  - 검증 스크립트 결과(`run-all.sh`)

## Safe Rollback or Recovery Procedure

- [ ] 수동 EndpointSlice 제거(필요 시)

```bash
kubectl -n platform delete endpointslice vault-external-1
```

- [ ] 기존 운영 상태로 롤백 후 근본원인 분석/백로그 등록
- [ ] 백로그 등록 항목:
  - EndpointSlice 수동 의존 제거 구조 개선
  - AppProject/Vault 정책 변경 필요성 검토

## Agent Operations (If Applicable)

- **Prompt Rollback**: 변경 전 문서 버전으로 복귀
- **Model Fallback**: 보수적 복구 절차 우선
- **Tool Disable / Revoke**: 자동 변경 중단
- **Eval Re-run**: `./infrastructure/tests/run-all.sh`
- **Trace Capture**: `docs/06.tasks/...`에 증적 반영

## Related Operational Documents

- **Guide**: [`../07.guides/0002-wsl2-k3d-argocd-ha-setup-guide.md`](../07.guides/0002-wsl2-k3d-argocd-ha-setup-guide.md)
- **Operations Policy**: [`../08.operations/0002-wsl2-k3d-gitops-ha-operations-policy.md`](../08.operations/0002-wsl2-k3d-gitops-ha-operations-policy.md)
