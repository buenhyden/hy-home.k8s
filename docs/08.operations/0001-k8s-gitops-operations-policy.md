# K8s GitOps Platform Operations Policy

## Overview (KR)

이 문서는 WSL2 기반 k3d/k3s GitOps 플랫폼의 운영 정책을 정의한다. 접근 통제, 배포 게이트, 예외 승인, 보안 기준을 명시한다.

## Policy Scope

k3d 클러스터, ArgoCD GitOps, ESO/Vault, 외부 PostgreSQL/Valkey 연동 운영 정책.

## Applies To

- **Systems**: k3d cluster, ArgoCD, ESO, Vault integration endpoints
- **Agents**: Docs/DevOps/GitOps automation agents
- **Environments**: Local WSL2 development platform

## Controls

- **Required**:
  - RBAC 최소권한
  - AppProject `sourceRepos`/`destinations` 제한
  - Vault policy namespace/path least privilege
  - NetworkPolicy 기반 egress 제한
  - 문서 변경 시 README 인덱스 동기화
- **Allowed**:
  - 승인된 버전 범위 내 업그레이드
  - 표준 runbook 절차 기반 복구
- **Disallowed**:
  - 평문 시크릿 Git 저장
  - 승인 없는 권한 확장
  - 검증 없는 배포 승격

## Exceptions

- 임시 운영 예외는 platform owner 승인 후 기간/범위/복구조건을 기록해야 한다.

## Verification

- 정책 검증 체크리스트를 runbook 절차와 task 증적으로 확인한다.

## Review Cadence

- 월 1회 정책 리뷰 또는 주요 버전 변경 시 즉시 리뷰.

## AI Agent Policy Section (If Applicable)

- **Model / Prompt Change Process**: 변경 시 ADR 또는 task evidence 필수.
- **Eval / Guardrail Threshold**: 문서 링크/검증 실패 0건.
- **Log / Trace Retention**: task/runbook 증적을 문서에 보존.
- **Safety Incident Thresholds**: 권한 오남용 징후 즉시 에스컬레이션.

## Related Documents

- **ARD**: [`../02.ard/0001-wsl-k3d-argocd-platform.md`](../02.ard/0001-wsl-k3d-argocd-platform.md)
- **Runbook**: [`../09.runbooks/0001-argocd-platform-bootstrap-runbook.md`](../09.runbooks/0001-argocd-platform-bootstrap-runbook.md)
- **Postmortem**: `[../11.postmortems/YYYY/YYYY-MM-DD-<incident-title>.md]`
