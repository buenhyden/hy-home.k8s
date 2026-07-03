# 05.operations/guides

> 운영자와 개발자가 k3d/GitOps 작업을 이해하고 재현할 수 있도록 how-to 중심 가이드를 관리한다.

> [!NOTE]
> All AI agent interactions with this stage must comply with the [Agent Governance Hub](../../00.agent-governance/README.md).

## Overview

이 경로는 안정 상태의 사용법, 온보딩 흐름, 배경 설명을 제공한다.
정책 통제 기준은 [policies](../policies/README.md), 즉시 실행할 복구 절차는 [runbooks](../runbooks/README.md), 실제 사고 기록은 [incidents](../incidents/README.md)에서 관리한다.

| 필요 상황                                        | 문서 유형        |
| ------------------------------------------------ | ---------------- |
| 작업 배경과 선행 조건을 이해해야 함              | Guide            |
| 실행 순서보다 개념, 설정 방법, 주의사항이 중요함 | Guide            |
| 실패 상황에서 바로 따라 할 체크리스트가 필요함   | Runbook으로 이동 |
| 허용/금지/예외 기준을 확인해야 함                | Policy로 이동    |

## Audience

이 README의 주요 독자:

- Developers
- Operators
- Documentation Writers
- AI Agents

## Scope

### In Scope

- 온보딩/이해 중심 가이드
- 선행 조건과 점검 명령
- 공통 실패 패턴 및 회피 방법
- Spec/Operations/Runbook 교차 링크

### Out of Scope

- 정책 통제 기준 정의
- 실시간 장애 대응 절차
- 사후 사고 분석 보고서

## Structure

```text
docs/05.operations/guides/
├── 0001-wsl-k3d-argocd-bootstrap-guide.md         # WSL2 k3d + ArgoCD 부트스트랩 가이드
├── 0002-wsl2-k3d-argocd-ha-setup-guide.md         # WSL2 HA + TLS + 정적 검증 분리 가이드
├── 0003-platform-expansion-bootstrap-guide.md      # cert-manager/Headlamp/Istio/Kiali 확장 가이드
├── 0006-argocd-prometheus-grafana-guide.md         # ArgoCD 메트릭/Prometheus/Grafana 가이드
├── 0007-k8s-observability-bootstrap-guide.md       # 관측성 스택 부트스트랩 가이드
├── 0008-github-app-gitops-onboarding-guide.md      # GitHub 앱 GitOps 온보딩 가이드
├── 0009-llm-wiki-curation-guide.md                 # LLM Wiki curation 가이드
├── 0010-ci-cd-qa-reference-guide.md                # CI/CD & QA 로컬-vs-GitHub 참조 가이드
└── README.md                                       # This file
```

## How to Work in This Area

1. 먼저 관련 Spec/Policy/Runbook을 확인한다. 기본 플랫폼 계약은 [Current Local GitOps Platform Spec](../../03.specs/008-current-local-gitops-platform/spec.md)을 기준으로 삼는다.
2. 새 가이드 추가/수정 시 [guide.template.md](../../99.templates/templates/sdlc/operations/guide.template.md)를 기반으로 작성한다.
3. 실행 명령은 복붙 가능한 형태로 유지하고, 시크릿 값은 절대 직접 기재하지 않는다.
4. 문서 변경 시 이 README의 인덱스(상태/설명/수정일)를 함께 갱신한다.
5. 명령 순서, 롤백, 복구가 핵심이면 가이드에 복제하지 말고 [runbooks](../runbooks/README.md)에 둔다.
6. 허용/금지/예외 승인 기준은 가이드가 아니라 [policies](../policies/README.md)에 둔다.

## Documentation Standards

이 영역의 가이드는 안정 상태의 사용법과 이해를 돕는 문서로 유지한다.

- 모든 Guide 문서는 [guide.template.md](../../99.templates/templates/sdlc/operations/guide.template.md)의 frontmatter와 필수 섹션을 유지한다.
- 기존 Spec, Policy, Runbook이 소유하는 계약을 중복 정의하지 않고 상대 링크로 연결한다.
- 실행 예시는 재현 가능한 형태로 작성하되, live cluster mutation이나 secret 값 노출은 승인된 bootstrap/break-glass 문맥으로 제한한다.

## Traceability Rules

Guide 문서는 가능한 경우 다음 문서와 연결되어야 한다.

- upstream 요구사항/아키텍처/스펙: PRD, ARD, ADR, Spec, Plan
- sibling 운영 문서: 관련 Policy, Runbook, Incident 경로
- 하위 실행 증적: Task 또는 validation guide

## Link Basis

이 README의 링크 기준 위치는 `docs/05.operations/guides/`다.

- 같은 폴더의 Guide 문서는 `./`로 시작한다.
- sibling operations folder는 `../policies/`, `../runbooks/`, `../incidents/`로 연결한다.
- upstream docs stage는 `../../01.requirements/`, `../../02.architecture/`, `../../03.specs/`, `../../04.execution/`로 연결한다.

## Related Documents

- [Agent Governance Hub](../../00.agent-governance/README.md)
- [03.specs](../../03.specs/README.md)
- [05.operations/policies](../policies/README.md)
- [05.operations/runbooks](../runbooks/README.md)
- [05.operations/incidents](../incidents/README.md)
- [PRD](../../01.requirements/2026-06-02-current-local-gitops-platform.md)
- [ARD](../../02.architecture/requirements/0007-current-local-gitops-platform.md)
- [Spec](../../03.specs/008-current-local-gitops-platform/spec.md)
- [Plan](../../04.execution/plans/2026-06-02-current-implementation-docs-alignment.md)
- [Task](../../04.execution/tasks/2026-06-02-current-implementation-docs-alignment.md)
- [Guide Template](../../99.templates/templates/sdlc/operations/guide.template.md)
- [README Template](../../99.templates/templates/common/readme.template.md)

## 문서 인덱스

| 문서                                                                                           | 설명                                                                    | 상태   | 최종 수정  |
| ---------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------- | ------ | ---------- |
| [`./0001-wsl-k3d-argocd-bootstrap-guide.md`](./0001-wsl-k3d-argocd-bootstrap-guide.md)         | 외부 서비스 분리 운영 + Vault 기반 부트스트랩/검증 가이드               | Active | 2026-05-22 |
| [`./0002-wsl2-k3d-argocd-ha-setup-guide.md`](./0002-wsl2-k3d-argocd-ha-setup-guide.md)         | WSL2 멀티노드 HA + TLS + 런타임/CI 정적 검증 절차를 분리한 운영 가이드  | Active | 2026-06-02 |
| [`./0003-platform-expansion-bootstrap-guide.md`](./0003-platform-expansion-bootstrap-guide.md) | cert-manager/Headlamp/Istio/Kiali 포함 확장 플랫폼 부트스트랩 가이드    | Active | 2026-06-02 |
| [`./0006-argocd-prometheus-grafana-guide.md`](./0006-argocd-prometheus-grafana-guide.md)       | ArgoCD 메트릭 NodePort 수집 + Prometheus 설정 + Grafana 대시보드 가이드 | Active | 2026-05-09 |
| [`./0007-k8s-observability-bootstrap-guide.md`](./0007-k8s-observability-bootstrap-guide.md)   | k3d 클러스터 메트릭/로그 수집 관측성 스택 부트스트랩 가이드             | Active | 2026-05-09 |
| [`./0008-github-app-gitops-onboarding-guide.md`](./0008-github-app-gitops-onboarding-guide.md) | GitHub 레포 기반 앱 GitOps 온보딩 (최소 템플릿 + active reference 구분) | Active | 2026-05-26 |
| [`./0009-llm-wiki-curation-guide.md`](./0009-llm-wiki-curation-guide.md)                       | LLM Wiki generated index와 `wiki-curator` agent 사용 가이드             | Active | 2026-05-10 |
| [`./0010-ci-cd-qa-reference-guide.md`](./0010-ci-cd-qa-reference-guide.md)                     | CI/CD QA 검증 로컬-vs-GitHub Actions 경계, script gate, currentness gate 참조 가이드 | Active | 2026-07-04 |
