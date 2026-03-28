# WSL2 k3d/k3s GitOps HA Operations Policy

## Overview (KR)

이 문서는 WSL2 기반 플랫폼의 운영 통제 기준을 정의한다. 외부 서비스 계약, 보안 최소권한, 복구 절차 준수 기준을 포함한다.

## Policy Scope

- k3d/k3s 멀티노드 로컬 플랫폼
- ArgoCD/ESO/Vault 연동
- 외부 PostgreSQL/Valkey/Vault endpoint 계약

## Applies To

- **Systems**: `gitops/`, `infrastructure/`
- **Agents**: 문서/운영 자동화 에이전트
- **Environments**: WSL2 local cluster

## Controls

- **Required**:
  - 인터페이스 계약 포트 고정(8200/15432/15433/26379)
  - Vault 경로 표준(`secret/platform/argocd`, `secret/platform/postgres-app`)
  - RBAC 최소권한 및 Vault policy 적용
  - README 인덱스/문서 추적성 유지
- **Allowed**:
  - 장애 시 수동 `EndpointSlice` 핫픽스
  - `argocd --hard-refresh` 기반 상태 재평가
- **Disallowed**:
  - 평문 시크릿 커밋
  - 승인 없는 정책 완화/권한 확장

## Exceptions

- 긴급 복구를 위해 수동 EndpointSlice 생성은 허용한다.
- 단, 운영 종료 후 구조 개선 작업(백로그) 등록을 필수로 한다.

## Verification

- 계약 검증:

```bash
kubectl -n platform get svc,endpointslice | \
  rg 'postgres-(write|read)-external|15432|15433|vault-external|8200'
kubectl -n platform get svc valkey-external -o yaml | \
  rg 'host.k3d.internal|26379'
```

- 상태 검증:

```bash
kubectl -n external-secrets get clustersecretstore vault-backend
kubectl -n argocd get externalsecret argocd-external-valkey
kubectl -n argocd get app platform-eso-config platform-argocd-config
```

## Review Cadence

- 운영 변경 시 즉시
- 정기 분기 검토

## AI Agent Policy Section (If Applicable)

- **Model / Prompt Change Process**: 정책/운영 문서 변경은 증적 기반으로만 반영
- **Eval / Guardrail Threshold**: `infrastructure/tests/run-all.sh` PASS
- **Log / Trace Retention**: runbook 절차/명령 로그 보관
- **Safety Incident Thresholds**: Vault/Secret 동기화 실패는 즉시 incident 처리

## Related Documents

- **ARD**: [`../02.ard/0002-wsl2-k3d-argocd-ha-platform.md`](../02.ard/0002-wsl2-k3d-argocd-ha-platform.md)
- **Runbook**: [`../09.runbooks/0002-argocd-eso-vault-recovery-runbook.md`](../09.runbooks/0002-argocd-eso-vault-recovery-runbook.md)
- **Guide**: [`../07.guides/0002-wsl2-k3d-argocd-ha-setup-guide.md`](../07.guides/0002-wsl2-k3d-argocd-ha-setup-guide.md)
