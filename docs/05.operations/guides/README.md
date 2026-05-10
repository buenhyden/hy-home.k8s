# 05.operations/guides

> 플랫폼/운영 작업을 재현 가능한 절차로 설명하는 가이드 문서를 관리한다.

## 목적

이 폴더는 운영자와 개발자가 k3d/GitOps 작업을 이해하고 재현할 수 있도록 how-to 중심 가이드를 저장한다.

## Overview

이 경로는 운영 정책(`05.operations/policies`)과 실행 런북(`05.operations/runbooks`) 사이에서,
작업 배경과 단계별 수행 방법을 설명하는 how-to 중심 문서를 제공한다.

## Audience

이 README의 주요 독자:

- Developers
- Operators
- Documentation Writers
- AI Agents

## Scope

### In Scope

- 온보딩/실행 가이드
- 선행 조건과 점검 명령
- 공통 실패 패턴 및 회피 방법
- Spec/Operations/Runbook 교차 링크

### Out of Scope

- 정책 통제 기준 정의
- 실시간 장애 대응 절차
- 사후 사고 분석 보고서

## 포함할 내용

이 stage는 위 In Scope 항목만 포함한다. 새 가이드나 인덱스 항목을 추가할 때는 관련 Spec/Operations/Runbook 링크를 함께 갱신한다.

## Structure

```text
docs/05.operations/guides/
├── 0001-wsl-k3d-argocd-bootstrap-guide.md         # WSL2 k3d + ArgoCD 부트스트랩 가이드
├── 0002-wsl2-k3d-argocd-ha-setup-guide.md         # WSL2 HA + TLS + 정적 검증 분리 가이드
├── 0003-platform-expansion-bootstrap-guide.md      # cert-manager/Headlamp/Istio/Kiali 확장 가이드
├── 0004-headlamp-auth-oidc-guide.md                # Headlamp 인증/OIDC 가이드
├── 0005-new-app-gitops-onboarding-guide.md         # 신규 앱 GitOps 온보딩 가이드
├── 0006-argocd-prometheus-grafana-guide.md         # ArgoCD 메트릭/Prometheus/Grafana 가이드
├── 0007-k8s-observability-bootstrap-guide.md       # 관측성 스택 부트스트랩 가이드
├── 0008-github-app-gitops-onboarding-guide.md      # GitHub 앱 GitOps 온보딩 가이드
└── README.md                                       # This file
```

## How to Work in This Area

1. 먼저 [spec.md](../../03.specs/002-wsl2-k3d-argocd-ha-platform/spec.md)에서 현재 계약 값을 확인한다.
2. 새 가이드 추가/수정 시 `../99.templates/guide.template.md`를 기반으로 작성한다.
3. 실행 명령은 복붙 가능한 형태로 유지하고, 시크릿 값은 절대 직접 기재하지 않는다.
4. 문서 변경 시 이 README의 인덱스(상태/설명/수정일)를 함께 갱신한다.

## Related References

- [Agent Governance Hub](../../00.agent-governance/README.md)
- [03.specs](../../03.specs/README.md)
- [05.operations/policies](../policies/README.md)
- [05.operations/runbooks](../runbooks/README.md)

## 관련 폴더

- `03.specs/`: 가이드가 설명하는 구현 계약
- `05.operations/policies/`: 가이드의 운영 정책 기준
- `05.operations/runbooks/`: 가이드에서 이어지는 실행 절차

## Documentation Standards

- 템플릿 기반으로 문서를 작성하고 필수 섹션을 누락하지 않는다.
- 기존 SSoT 문서를 중복 생성하지 않고, 링크로 추적성을 유지한다.
- 사람과 Agent가 동일하게 해석할 수 있도록 계약 값(서비스명/포트/경로)을 명시한다.

## Traceability Rules

- 각 Guide는 최소 1개의 Spec, 1개의 Operations Policy, 1개의 Runbook과 연결한다.
- 링크는 상대 경로만 사용한다.
- 실재하지 않는 파일은 링크하지 않는다.

## Template Usage

- 가이드 템플릿: [`../99.templates/guide.template.md`](../../99.templates/guide.template.md)
- README 템플릿: [`../99.templates/readme.template.md`](../../99.templates/readme.template.md)

## 예시

- 플랫폼 부트스트랩 설명은 `0001-wsl-k3d-argocd-bootstrap-guide.md`처럼 배경과 절차를 함께 제공한다.
- Headlamp 인증 전환 설명은 `0004-headlamp-auth-oidc-guide.md`처럼 선행 조건, 단계, 검증을 포함한다.

## Metadata Expectations

- 문서 제목은 목적을 즉시 식별 가능해야 한다.
- 상태(`Draft`/`Active`)와 최종 수정일을 인덱스에 유지한다.
- 운영 계약 변경 시 관련 Guide/Operations/Runbook 인덱스를 같이 업데이트한다.

## SSoT References

- [PRD](../../01.requirements/2026-03-28-wsl2-k3d-argocd-ha-platform.md)
- [ARD](../../02.architecture/requirements/0002-wsl2-k3d-argocd-ha-platform.md)
- [Spec](../../03.specs/002-wsl2-k3d-argocd-ha-platform/spec.md)
- [Plan](../../04.execution/plans/2026-03-28-wsl2-k3d-argocd-ha-platform.md)
- [Task](../../04.execution/tasks/2026-03-28-wsl2-k3d-argocd-ha-platform.md)

## 문서 인덱스

| 문서                                                                                         | 설명                                                                    | 상태   | 최종 수정  |
| -------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------- | ------ | ---------- |
| [`0001-wsl-k3d-argocd-bootstrap-guide.md`](./0001-wsl-k3d-argocd-bootstrap-guide.md)         | 외부 서비스 분리 운영 + Vault 기반 부트스트랩/검증 가이드               | Active | 2026-03-27 |
| [`0002-wsl2-k3d-argocd-ha-setup-guide.md`](./0002-wsl2-k3d-argocd-ha-setup-guide.md)         | WSL2 멀티노드 HA + TLS + 런타임/CI 정적 검증 절차를 분리한 운영 가이드  | Active | 2026-05-09 |
| [`0003-platform-expansion-bootstrap-guide.md`](./0003-platform-expansion-bootstrap-guide.md) | cert-manager/Headlamp/Istio/Kiali 포함 확장 플랫폼 부트스트랩 가이드    | Active | 2026-05-09 |
| [`0004-headlamp-auth-oidc-guide.md`](./0004-headlamp-auth-oidc-guide.md)                     | Headlamp 인증/로그인 방식 및 Keycloak OIDC 연동 how-to 가이드           | Active | 2026-05-09 |
| [`0005-new-app-gitops-onboarding-guide.md`](./0005-new-app-gitops-onboarding-guide.md)       | 새 애플리케이션 GitOps 온보딩 (ApplicationSet/Application CR) 가이드    | Active | 2026-05-09 |
| [`0006-argocd-prometheus-grafana-guide.md`](./0006-argocd-prometheus-grafana-guide.md)       | ArgoCD 메트릭 NodePort 수집 + Prometheus 설정 + Grafana 대시보드 가이드 | Active | 2026-05-09 |
| [`0007-k8s-observability-bootstrap-guide.md`](./0007-k8s-observability-bootstrap-guide.md)   | k3d 클러스터 메트릭/로그 수집 관측성 스택 부트스트랩 가이드             | Active | 2026-05-09 |
| [`0008-github-app-gitops-onboarding-guide.md`](./0008-github-app-gitops-onboarding-guide.md) | GitHub 레포 기반 앱 GitOps 온보딩 (Rollout/AnalysisTemplate/mTLS 패턴)  | Active | 2026-05-09 |
