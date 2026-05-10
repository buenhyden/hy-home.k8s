# 05.operations/runbooks

> 반복 가능한 운영 작업을 즉시 실행할 수 있는 체크리스트/절차 문서를 관리한다.

## 목적

이 폴더는 k3d/GitOps 플랫폼에서 반복 실행하는 운영 절차와 복구 절차를 저장한다.

## Overview

이 경로는 운영자가 장애 상황 또는 재구축 상황에서 바로 실행 가능한 절차를 제공한다.
정책 정의는 `05.operations/policies`, 가이드 설명은 `05.operations/guides`, 사고 분석은 `05.operations/incidents`에서 관리한다.

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

## 포함할 내용

이 stage는 위 In Scope 항목만 포함한다. 런북 수정 시 명령 순서, 성공 기준, 롤백/복구 증적을 함께 유지한다.

## Structure

```text
docs/05.operations/runbooks/
├── 0001-argocd-platform-bootstrap-runbook.md               # k3d + ArgoCD 부트스트랩/복구 런북
├── 0002-argocd-eso-vault-recovery-runbook.md               # Vault/ESO 복구 + TLS/CI 계약 회귀 검증
├── 0003-platform-expansion-bootstrap-runbook.md             # cert-manager/Headlamp/Istio/Kiali 부트스트랩
├── 0004-rollouts-notifications-headlamp-runbook.md          # Rollouts/Notifications/Headlamp 운영
├── 0005-headlamp-keycloak-runbook.md                        # Headlamp token/OIDC 전환 운영
├── 0006-new-app-onboarding-runbook.md                       # 신규 앱 온보딩 절차
├── 0007-kiali-observability-connectivity-runbook.md         # Kiali 관측성 연결 복구
├── 0008-argocd-metrics-prometheus-runbook.md                # ArgoCD metrics/Prometheus 복구
├── 0009-k8s-observability-runbook.md                        # 관측성 스택 장애 진단
├── 0010-github-app-gitops-onboarding-runbook.md             # GitHub 앱 온보딩 절차
└── README.md                                                # This file
```

## How to Work in This Area

1. 관련 Spec/Operations를 먼저 확인해 계약값을 고정한다.
2. `../99.templates/runbook.template.md` 기반으로 작성한다.
3. 절차는 명령 실행 순서와 검증 기준을 함께 제시한다.
4. 복구 절차에는 롤백, 재동기화, 증적 수집 단계를 반드시 포함한다.

## Related References

- [05.operations/guides](../guides/README.md)
- [05.operations/policies](../policies/README.md)
- [05.operations/incidents](../incidents/README.md)

## 관련 폴더

- `05.operations/guides/`: 절차의 배경과 how-to 설명
- `05.operations/policies/`: 런북이 따라야 할 운영 정책
- `05.operations/incidents/`: 런북 실행 결과가 연결되는 사고 기록

## Documentation Standards

- Runbook은 즉시 실행 가능한 형태를 유지한다.
- 명령은 복붙 가능한 블록으로 제공한다.
- 비밀 값은 문서에 기록하지 않고 Vault 경로만 명시한다.

## Traceability Rules

- 각 Runbook은 Canonical References에 ARD/ADR/Spec/Plan을 연결한다.
- Incident/Postmortem 인덱스와 상호 링크를 유지한다.
- 상대 경로 링크만 사용한다.

## Template Usage

- 런북 템플릿: [`../99.templates/runbook.template.md`](../../99.templates/runbook.template.md)
- README 템플릿: [`../99.templates/readme.template.md`](../../99.templates/readme.template.md)

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
- 재검증 기준 문서: [`0002-argocd-eso-vault-recovery-runbook.md`](./0002-argocd-eso-vault-recovery-runbook.md)

## Incident and Recovery Links

- Runbooks: [`./README.md`](./README.md)
- Incident Records: [`../05.operations/incidents/README.md`](../incidents/README.md)
- Postmortems: [`../05.operations/incidents/README.md`](../incidents/README.md)

## 예시

- 플랫폼 부트스트랩은 `0001-argocd-platform-bootstrap-runbook.md`를 따른다.
- Vault/ESO 복구는 `0002-argocd-eso-vault-recovery-runbook.md`를 따른다.

## SSoT References

- [ARD](../../02.architecture/requirements/0002-wsl2-k3d-argocd-ha-platform.md)
- [ADR](../../02.architecture/decisions/0005-wsl2-ha-baseline-and-external-endpoint-contract.md)
- [Spec](../../03.specs/002-wsl2-k3d-argocd-ha-platform/spec.md)
- [Operations Policy](../policies/0002-wsl2-k3d-gitops-ha-operations-policy.md)

## 문서 인덱스

| 문서                                                                                                     | 설명                                                              | 상태   | 최종 수정  |
| -------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------- | ------ | ---------- |
| [`0001-argocd-platform-bootstrap-runbook.md`](./0001-argocd-platform-bootstrap-runbook.md)               | 검증 커맨드 기반 부트스트랩/트러블슈팅/복구 런북                  | Active | 2026-03-27 |
| [`0002-argocd-eso-vault-recovery-runbook.md`](./0002-argocd-eso-vault-recovery-runbook.md)               | Vault-ESO 복구 + TLS/Ingress + CI 정적 계약 회귀/증적 검증 런북   | Active | 2026-05-09 |
| [`0003-platform-expansion-bootstrap-runbook.md`](./0003-platform-expansion-bootstrap-runbook.md)         | cert-manager/Headlamp/Istio/Kiali 부트스트랩 및 증상별 복구 런북  | Active | 2026-05-09 |
| [`0004-rollouts-notifications-headlamp-runbook.md`](./0004-rollouts-notifications-headlamp-runbook.md)   | Argo Rollouts/Notifications/Headlamp 설치 및 운영 런북            | Active | 2026-05-09 |
| [`0005-headlamp-keycloak-runbook.md`](./0005-headlamp-keycloak-runbook.md)                               | Headlamp ServiceAccount 토큰 로그인 및 Keycloak OIDC 전환 런북    | Active | 2026-05-09 |
| [`0006-new-app-onboarding-runbook.md`](./0006-new-app-onboarding-runbook.md)                             | 새 애플리케이션 GitOps 온보딩 체크리스트 및 트러블슈팅 런북       | Active | 2026-05-09 |
| [`0007-kiali-observability-connectivity-runbook.md`](./0007-kiali-observability-connectivity-runbook.md) | Kiali 관측성 서비스 연결 장애 진단 및 복구 런북                   | Active | 2026-05-09 |
| [`0008-argocd-metrics-prometheus-runbook.md`](./0008-argocd-metrics-prometheus-runbook.md)               | ArgoCD 메트릭 NodePort/Prometheus 수집 장애 진단 및 복구 런북     | Active | 2026-05-09 |
| [`0009-k8s-observability-runbook.md`](./0009-k8s-observability-runbook.md)                               | kube-state-metrics/alloy/alert_rules/AppProject 장애 진단 런북    | Active | 2026-05-09 |
| [`0010-github-app-gitops-onboarding-runbook.md`](./0010-github-app-gitops-onboarding-runbook.md)         | GitHub 레포 기반 앱 온보딩 절차 런북 (배포/검증/rollback/Vault)   | Active | 2026-05-09 |
