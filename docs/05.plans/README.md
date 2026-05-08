# 05.plans

> [!NOTE]
> All AI agent interactions with this stage must comply with the [Agent Governance Hub](../00.agent-governance/README.md).

## 목적

이 폴더는 실행 계획(Plan)을 저장한다. Plan은 언제, 누가, 어떤 순서로, 어떤 제약과 위험을 관리하며 작업을 진행하는지 정의한다.

## 포함할 내용

- 목표와 범위
- 단계(Phase) 또는 추적 표
- 위험과 완화 전략
- 검증 게이트
- 완료 기준
- 롤아웃/롤백 전략

## AI Agent 계획에 추가할 내용

- Offline Eval 통과 기준
- Canary/Sandbox Rollout
- Human Approval Gate
- Prompt/Model 버전 승격 기준
- Rollback 조건

## 연결 규칙

- Plan은 PRD/ARD/Spec/ADR를 참조한다.
- Task는 Plan의 단계 또는 Task ID를 상위 참조로 가진다.

## Templates

- `../99.templates/plan.template.md`

## 문서 인덱스

| 문서                                                                                       | 설명                                                                            | 상태  | 최종 수정  |
| ------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------- | ----- | ---------- |
| [`2026-03-27-wsl-k3d-argocd-platform.md`](./2026-03-27-wsl-k3d-argocd-platform.md)         | WSL2 GitOps 플랫폼 단계별 실행 계획                                             | Draft | 2026-03-27 |
| [`2026-03-28-wsl2-k3d-argocd-ha-platform.md`](./2026-03-28-wsl2-k3d-argocd-ha-platform.md) | TLS/최소권한 유지 + 변경영역 기반 CI 정적 게이트 + 롤백 규칙을 포함한 실행 계획 | Draft | 2026-03-28 |
| [`2026-03-29-platform-expansion.md`](./2026-03-29-platform-expansion.md)                   | 2026-03-29 IP 수정 + cert-manager/Dashboard/Istio/Kiali 확장 계획, 현재 실행계약은 Headlamp/172.18.x 기준 | Done  | 2026-05-09 |
