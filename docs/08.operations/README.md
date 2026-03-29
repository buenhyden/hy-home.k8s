# 08.operations

> GitOps 플랫폼 운영 정책과 통제 기준(허용/금지/예외/검증)을 관리한다.

## Overview

이 경로는 플랫폼 운영 정책의 단일 기준점이다.
외부 서비스 런타임 분리, Vault 단일 소스, GitOps 경로/브랜치 게이트, 포트 계약 준수 같은 운영 규칙을 문서화한다.

## Audience

이 README의 주요 독자:

- Developers
- Operators
- Documentation Writers
- AI Agents

## Scope

### In Scope

- 운영 정책 문서(Operations Policy)
- 통제 항목(Required/Allowed/Disallowed)
- 예외 승인 흐름
- 정책 검증 방법 및 검토 주기

### Out of Scope

- 실행 절차 중심의 명령 순서 문서
- 장애 타임라인/사후 분석
- 온보딩 중심 가이드

## Structure

```text
08.operations/
├── 0001-k8s-gitops-operations-policy.md  # k3d/ArgoCD/ESO/Vault 운영 정책
├── 0002-wsl2-k3d-gitops-ha-operations-policy.md  # WSL2 HA + TLS/최소권한 + CI 게이트 운영 정책
└── README.md                             # This file
```

## How to Work in This Area

1. 정책 수정 전에 관련 Spec/Runbook을 확인한다.
2. `../99.templates/operation.template.md`를 기준으로 섹션을 유지한다.
3. 통제 변경 시 검증 명령과 예외 승인 흐름을 함께 갱신한다.
4. 문서 변경 후 이 README 인덱스를 동기화한다.

## Related References

- [04.specs](../04.specs/README.md)
- [09.runbooks](../09.runbooks/README.md)
- [10.incidents](../10.incidents/README.md)
- [11.postmortems](../11.postmortems/README.md)

## Documentation Standards

- 정책 문서는 실행 가이드가 아니라 통제 기준을 정의해야 한다.
- 계약 값(서비스명/포트/경로)은 코드/매니페스트와 일치해야 한다.
- 평문 비밀번호/토큰/API key 기재를 금지한다.

## Traceability Rules

- Policy는 최소 1개의 ARD, 1개의 Spec, 1개의 Runbook과 연결한다.
- Incident/Postmortem은 인덱스 링크로 연결해 추적성을 유지한다.
- 링크는 상대 경로로 작성한다.

## Template Usage

- 정책 템플릿: [`../99.templates/operation.template.md`](../99.templates/operation.template.md)
- README 템플릿: [`../99.templates/readme.template.md`](../99.templates/readme.template.md)

## Metadata Expectations

- 정책 문서는 상태와 검토 주기를 명시해야 한다.
- 예외 승인 경로가 변경되면 즉시 문서화한다.
- 인덱스의 `최종 수정` 날짜를 최신화한다.

## Usage Instructions

정책 검토/적용 시 아래 핵심 검증 명령을 사용한다.

```bash
kubectl -n argocd get application root-platform -o yaml | \
  rg 'path: gitops/apps/root|targetRevision: main'
kubectl -n platform get svc,endpointslice | \
  rg 'postgres-(write|read)-external|15432|15433'
kubectl -n platform get svc,endpointslice | \
  rg 'valkey-external|valkey-external-1|172.30.0.12|26379'
./infrastructure/tests/verify-ingress-tls.sh
```

## Verification and Monitoring

- 로그 위치: `kubectl -n argocd logs`, `kubectl -n external-secrets logs`
- 상태 점검: `argocd app list`, `kubectl get applications -n argocd`
- 이상 시 참조 문서: [`../09.runbooks/0001-argocd-platform-bootstrap-runbook.md`](../09.runbooks/0001-argocd-platform-bootstrap-runbook.md)
- 이상 시 참조 문서: [`../09.runbooks/0002-argocd-eso-vault-recovery-runbook.md`](../09.runbooks/0002-argocd-eso-vault-recovery-runbook.md)

## Incident and Recovery Links

- Runbooks: [`../09.runbooks/README.md`](../09.runbooks/README.md)
- Incident Records: [`../10.incidents/README.md`](../10.incidents/README.md)
- Postmortems: [`../11.postmortems/README.md`](../11.postmortems/README.md)

## SSoT References

- [ARD](../02.ard/0002-wsl2-k3d-argocd-ha-platform.md)
- [Spec](../04.specs/002-wsl2-k3d-argocd-ha-platform/spec.md)
- [Runbook](../09.runbooks/0002-argocd-eso-vault-recovery-runbook.md)

## 문서 인덱스

| 문서                                                                                             | 설명                                                                                    | 상태   | 최종 수정  |
| ------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------- | ------ | ---------- |
| [`0001-k8s-gitops-operations-policy.md`](./0001-k8s-gitops-operations-policy.md)                 | 외부 런타임 분리 + Vault 단일 소스 + GitOps 게이트 운영 정책                            | Active | 2026-03-27 |
| [`0002-wsl2-k3d-gitops-ha-operations-policy.md`](./0002-wsl2-k3d-gitops-ha-operations-policy.md) | WSL2 HA 운영 통제(TLS/Traefik 경계, EndpointSlice, 최소권한, CI 게이트, 감사 항목) 정책 | Active | 2026-03-28 |
| [`0003-service-mesh-cert-manager-policy.md`](./0003-service-mesh-cert-manager-policy.md)         | cert-manager/Dashboard/Istio/Kiali 운영 통제(TLS/sidecar/Kiali auth/Traefik 계약) 정책  | Active | 2026-03-29 |
