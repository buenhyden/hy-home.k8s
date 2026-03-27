# 09.runbooks

> 반복 가능한 운영 작업을 즉시 실행할 수 있는 체크리스트/절차 문서를 관리한다.

## Overview

이 경로는 운영자가 장애 상황 또는 재구축 상황에서 바로 실행 가능한 절차를 제공한다.  
정책 정의는 `08.operations`, 가이드 설명은 `07.guides`, 사고 분석은 `11.postmortems`에서 관리한다.

## Audience

이 README의 주요 독자:

- Operators
- Developers
- Documentation Writers
- AI Agents

## Scope

### In Scope

- 실행 순서 중심 체크리스트
- 검증 커맨드와 성공 기준
- 오류 시그니처 기반 트러블슈팅
- 안전한 롤백/복구 절차

### Out of Scope

- 정책 통제의 정의 자체
- 튜토리얼 중심 배경 설명
- 사고 원인 분석 보고서

## Structure

```text
09.runbooks/
├── 0001-argocd-platform-bootstrap-runbook.md  # k3d + ArgoCD 부트스트랩/복구 런북
└── README.md                                  # This file
```

## How to Work in This Area

1. 관련 Spec/Operations를 먼저 확인해 계약값을 고정한다.
2. `../99.templates/runbook.template.md` 기반으로 작성한다.
3. 절차는 명령 실행 순서와 검증 기준을 함께 제시한다.
4. 복구 절차에는 롤백, 재동기화, 증적 수집 단계를 반드시 포함한다.

## Related References

- [07.guides](../07.guides/README.md)
- [08.operations](../08.operations/README.md)
- [10.incidents](../10.incidents/README.md)
- [11.postmortems](../11.postmortems/README.md)

## Documentation Standards

- Runbook은 즉시 실행 가능한 형태를 유지한다.
- 명령은 복붙 가능한 블록으로 제공한다.
- 비밀 값은 문서에 기록하지 않고 Vault 경로만 명시한다.

## Traceability Rules

- 각 Runbook은 Canonical References에 ARD/ADR/Spec/Plan을 연결한다.
- Incident/Postmortem 인덱스와 상호 링크를 유지한다.
- 상대 경로 링크만 사용한다.

## Template Usage

- 런북 템플릿: [`../99.templates/runbook.template.md`](../99.templates/runbook.template.md)
- README 템플릿: [`../99.templates/readme.template.md`](../99.templates/readme.template.md)

## Metadata Expectations

- 사용 시점(When to Use)과 검증 항목을 명확히 유지한다.
- 트러블슈팅 에러 시그니처는 실제 로그 문구 기준으로 작성한다.
- 인덱스 상태/수정일을 최신으로 유지한다.

## Usage Instructions

런북 실행 시 핵심 흐름:

1. 사전 점검(외부 서비스/Vault/포트)
2. 부트스트랩 실행
3. ArgoCD/ESO/서비스 인터페이스 검증
4. 오류 시그니처 기반 트러블슈팅
5. 롤백/복구 및 hard refresh

## Verification and Monitoring

- 로그 위치: `kubectl -n argocd logs`, `kubectl -n external-secrets logs`
- 상태 점검: `argocd app list`, `kubectl -n argocd get applications`
- 재검증 기준 문서: [`0001-argocd-platform-bootstrap-runbook.md`](./0001-argocd-platform-bootstrap-runbook.md)

## Incident and Recovery Links

- Runbooks: [`./README.md`](./README.md)
- Incident Records: [`../10.incidents/README.md`](../10.incidents/README.md)
- Postmortems: [`../11.postmortems/README.md`](../11.postmortems/README.md)

## SSoT References

- [ARD](../02.ard/0001-wsl-k3d-argocd-platform.md)
- [ADR](../03.adr/0004-external-services-endpoints-and-valkey-backend.md)
- [Spec](../04.specs/001-wsl-k3d-argocd-platform/spec.md)
- [Operations Policy](../08.operations/0001-k8s-gitops-operations-policy.md)

## 문서 인덱스

| 문서 | 설명 | 상태 | 최종 수정 |
| --- | --- | --- | --- |
| [`0001-argocd-platform-bootstrap-runbook.md`](./0001-argocd-platform-bootstrap-runbook.md) | 검증 커맨드 기반 부트스트랩/트러블슈팅/복구 런북 | Active | 2026-03-27 |
