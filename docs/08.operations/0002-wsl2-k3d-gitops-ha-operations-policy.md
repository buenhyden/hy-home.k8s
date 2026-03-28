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
  - Valkey는 `Service + EndpointSlice(172.30.0.12:26379)` 모델 사용
  - Vault 경로 표준(`secret/platform/argocd`, `secret/platform/postgres-app`)
  - ArgoCD 공식 HTTPS host는 `argocd.127.0.0.1.nip.io`를 사용
  - `argocd-local-tls`(`kubernetes.io/tls`) Secret 유지
  - `ingress-nginx-controller`는 `LoadBalancer` 타입 유지
  - 외부 Traefik 443 -> k3d 8443 라우팅 계약 유지
  - RBAC 최소권한 및 Vault policy 적용
  - AppProject allow-list 기반 리소스 권한 통제
  - 네임스페이스별 egress 정책 적용(`platform`, `argocd`, `external-secrets`)
  - README 인덱스/문서 추적성 유지
- **Allowed**:
  - 장애 시 수동 `EndpointSlice` 핫픽스
  - `argocd --hard-refresh` 기반 상태 재평가
  - `CHECK_TRAEFIK_443=true` 기반 운영 TLS 점검
- **Disallowed**:
  - 평문 시크릿 커밋
  - 승인 없는 정책 완화/권한 확장
  - 로컬 파일 수정 상태만으로 배포 완료로 판단하는 행위

## Exceptions

- 긴급 복구를 위해 수동 EndpointSlice 생성은 허용한다.
- 단, 운영 종료 후 구조 개선 작업(백로그) 등록을 필수로 한다.
- 예외 승인 절차:
  1. 장애 증적 첨부(로그, 상태 YAML)
2. 플랫폼 오너 승인
3. 실행 후 회귀 검증(`run-all.sh`)
4. 외부 Traefik 라우팅 변경 시 외부 저장소 변경 PR 링크 첨부

## Verification

- 계약 검증:

```bash
kubectl -n platform get svc,endpointslice | \
  rg 'postgres-(write|read)-external|15432|15433|vault-external|8200|valkey-external|172.30.0.12|26379'
./infrastructure/tests/verify-ingress-tls.sh
```

- 상태 검증:

```bash
kubectl -n external-secrets get clustersecretstore vault-backend
kubectl -n argocd get externalsecret argocd-external-valkey
kubectl -n argocd get app platform-eso-config platform-argocd-config
./infrastructure/tests/verify-network-policies.sh
CHECK_TRAEFIK_443=true ./infrastructure/tests/verify-ingress-tls.sh
```

- GitOps source gate:

```bash
kubectl -n argocd get app root-platform -o yaml | \
  rg 'path: gitops/apps/root|targetRevision: main'
```

## Review Cadence

- 운영 변경 시 즉시
- 정기 분기 검토

## AI Agent Policy Section (If Applicable)

- **Model / Prompt Change Process**: 정책/운영 문서 변경은 증적 기반으로만 반영
- **Eval / Guardrail Threshold**: `infrastructure/tests/run-all.sh` PASS
- **Log / Trace Retention**: runbook 절차/명령 로그 보관
- **Safety Incident Thresholds**: Vault/Secret 동기화 실패는 즉시 incident 처리
- **Audit Items**:
  - AppProject 권한 확장 여부
  - Vault policy 경로 확장 여부
  - EndpointSlice 수동 변경 이력
  - ArgoCD ingress host/TLS secret/service type 회귀 여부
  - 외부 Traefik 라우팅 계약(`443 -> 8443`) 변경 이력

## Related Documents

- **ARD**: [`../02.ard/0002-wsl2-k3d-argocd-ha-platform.md`](../02.ard/0002-wsl2-k3d-argocd-ha-platform.md)
- **Runbook**: [`../09.runbooks/0002-argocd-eso-vault-recovery-runbook.md`](../09.runbooks/0002-argocd-eso-vault-recovery-runbook.md)
- **Guide**: [`../07.guides/0002-wsl2-k3d-argocd-ha-setup-guide.md`](../07.guides/0002-wsl2-k3d-argocd-ha-setup-guide.md)
