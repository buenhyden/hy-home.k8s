---
title: 'Task: WSL2 k3d/k3s ArgoCD HA Platform Execution'
type: task
status: complete
owner: platform-team
updated: 2026-05-18
---

# Task: WSL2 k3d/k3s ArgoCD HA Platform Execution

## Overview (KR)

이 문서는 WSL2 GitOps 플랫폼 고도화 작업을 TDD(RED/GREEN/REFACTOR) 중심으로 추적한다. 이번 사이클은 `gitops/`, `infrastructure/`, `.github/` 동시 변경을 포함한다.

## Inputs

- **Parent Spec**: [`../../03.specs/002-wsl2-k3d-argocd-ha-platform/spec.md`](../../03.specs/002-wsl2-k3d-argocd-ha-platform/spec.md)
- **Parent Plan**: [`../plans/2026-03-28-wsl2-k3d-argocd-ha-platform.md`](../plans/2026-03-28-wsl2-k3d-argocd-ha-platform.md)

## Working Rules

- RED: 실패 조건을 먼저 정의한다.
- GREEN: 최소 변경으로 통과한다.
- REFACTOR: 검증 메시지/계약 문구를 표준화한다.

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Status |
| --- | --- | --- | --- | --- | --- | --- |
| T-001 | `argocd` egress 정책에 DNS/HTTPS 허용 추가 | impl | Network Policy Contracts | Phase 1 | `verify-network-policies.sh` | Done |
| T-002 | `appproject-apps` wildcard 제거 및 allow-list 적용 | impl | Guardrails | Phase 1 | `verify-contracts-static.sh` | Done |
| T-003 | `bootstrap-local.sh` 실패 메시지 표준화 | refactor | File-level Contract | Phase 1 | `bash -n` + 로그 확인 | Done |
| T-004 | 정적 계약 스크립트 `verify-contracts-static.sh` 신규 작성 | test | CI Static Contracts | Phase 2 | 스크립트 standalone PASS | Done |
| T-005 | CI workflow 변경영역 분기 구조 반영 | impl | CI Architecture | Phase 2 | workflow YAML 검증 | Done |
| T-006 | workflow-security gate(actionlint/zizmor) 추가 | impl | CI Architecture | Phase 2 | `.github` 변경 시 강제 실행 | Done |
| T-007 | shell-static gate(`bash -n`, `shellcheck`) 추가 | test | CI Architecture | Phase 2 | shell 스크립트 정적 검증 | Done |
| T-008 | dependabot docker/pip 경로 정리 | impl | File-level Contract | Phase 2 | config lint/리뷰 | Done |
| T-009 | PRD/ARD/ADR/SPEC 문서 업데이트 | doc | Traceability | Phase 3 | 상대 링크/계약 반영 | Done |
| T-010 | PLAN/TASK/GUIDE/OPER/RUN 문서 업데이트 | doc | Traceability | Phase 3 | 절차/게이트 반영 | Done |
| T-011 | 01~09 README 인덱스 동기화 | doc | Governance Contract | Phase 3 | 인덱스 설명/수정일 반영 | Done |

## Suggested Types

- `impl`
- `test`
- `eval`
- `doc`
- `ops`
- `refactor`

## TDD Scenarios by Component

### TC-01 Network Policy (`argocd` egress)

- RED: Valkey만 허용된 정책에서 repo-server fetch 실패 위험을 명시
- GREEN: DNS(53), HTTPS(443) 허용 추가
- REFACTOR: 정책명/계약 문구를 문서와 일치

### TC-02 AppProject Least Privilege

- RED: `namespaceResourceWhitelist * / *` 검출 시 실패
- GREEN: 최소 allow-list 리소스만 허용
- REFACTOR: 신규 리소스 추가 절차를 운영 정책으로 분리

### TC-03 Static Contract Script

- RED: root app path/revision, external service 계약, TLS 계약, Vault policy, wildcard 금지 중 하나라도 불일치 시 실패
- GREEN: `verify-contracts-static.sh` PASS
- REFACTOR: 실패 메시지 `[FAIL] cause` 표준 유지

### TC-04 Workflow Security

- RED: `.github/workflows/**` 변경 시 보안 검증 누락
- GREEN: `actionlint`, `zizmor` 잡 강제
- REFACTOR: `ci-summary`에서 집계 실패 기준 일원화

### TC-05 Shell Static

- RED: shell 문법 오류/취약 패턴 누락
- GREEN: `bash -n`, `shellcheck` 통과
- REFACTOR: 대상 경로를 `infrastructure/**/*.sh`, `scripts/**/*.sh`로 고정

### TC-06 Runtime Regression

- RED: 런타임 계약 검증 누락
- GREEN: `run-all.sh` + `verify-ingress-tls.sh` PASS
- REFACTOR: CI 정적 검증과 런타임 검증을 분리 운영

## Verification Summary

- **Static**:
  - `bash -n infrastructure/bootstrap-local.sh infrastructure/tests/*.sh`
  - `./infrastructure/tests/verify-contracts-static.sh`
- **Runtime**:
  - `./infrastructure/tests/run-all.sh`
  - `CHECK_TRAEFIK_443=true ./infrastructure/tests/verify-ingress-tls.sh`
- **CI Security**:
  - `actionlint`
  - `zizmor`

## Evidence Location

- Scripts: `infrastructure/tests/*`
- Workflow: `.github/workflows/ci.yml`
- Ops 증적: [`../../05.operations/runbooks/0002-argocd-eso-vault-recovery-runbook.md`](../../05.operations/runbooks/0002-argocd-eso-vault-recovery-runbook.md)

## Related Documents

- **Spec**: [`../../03.specs/002-wsl2-k3d-argocd-ha-platform/spec.md`](../../03.specs/002-wsl2-k3d-argocd-ha-platform/spec.md)
- **Plan**: [`../plans/2026-03-28-wsl2-k3d-argocd-ha-platform.md`](../plans/2026-03-28-wsl2-k3d-argocd-ha-platform.md)
- **Runbook**: [`../../05.operations/runbooks/0002-argocd-eso-vault-recovery-runbook.md`](../../05.operations/runbooks/0002-argocd-eso-vault-recovery-runbook.md)
