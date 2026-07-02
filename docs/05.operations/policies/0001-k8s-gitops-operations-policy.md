---
title: 'K8s GitOps Platform Operations Policy'
type: sdlc/policy
status: active
owner: platform
updated: 2026-05-21
---

# K8s GitOps Platform Operations Policy

## Overview

이 문서는 WSL2 기반 k3d/k3s GitOps 플랫폼의 운영 정책을 정의한다.
외부 서비스 런타임 분리, Vault 기반 시크릿 통제, GitOps 경로 검증 게이트, 포트 계약 준수 기준을 명시한다.

## Policy Scope

- k3d 클러스터와 ArgoCD GitOps 운영
- ESO + Vault 연동
- 외부 서비스 인터페이스 계약(`valkey-external`, `postgres-write-external`, `postgres-read-external`)
- 문서/검증 증적 운영 기준
- 외부 서비스 런타임 분리 원칙(외부 repo 관리)

## Applies To

- **Systems**: k3d cluster, ArgoCD, External Secrets Operator, Vault, platform namespace services
- **Agents**: Docs/DevOps/GitOps automation agents
- **Environments**: Local WSL2 development platform

## Controls

- **Required**:
  - 외부 서비스 런타임은 별도 워크스페이스(repo)에서만 운영한다.
  - Vault를 시크릿 단일 소스로 사용한다.
    - `secret/platform/argocd` -> `valkey_password`
    - `secret/platform/postgres-app` -> `db_name`, `username`, `password`
  - 시크릿 평문(비밀번호/토큰/API Key)을 문서, YAML, Git history에 저장하지 않는다.
  - GitOps 경로/브랜치 검증 게이트를 적용한다.
    - `root-platform.spec.source.path`는 원격 브랜치 실재 경로여야 한다.
    - `targetRevision`과 실제 운영 브랜치가 일치해야 한다.
  - 외부 서비스 포트 계약을 준수한다.
    - Valkey: `6379`
    - PostgreSQL write: `15432`
    - PostgreSQL read: `15433`
  - RBAC 최소권한 + AppProject source/destination 제한을 유지한다.
  - NetworkPolicy 기반 egress 제한을 유지한다.
  - 문서 변경 시 해당 폴더 `README.md` 인덱스를 동기화한다.
- **Allowed**:
  - 승인된 버전 범위 내 업그레이드
  - 표준 Runbook 기반 복구 및 재동기화
  - 운영 점검 목적의 read-only 진단 커맨드 실행
- **Disallowed**:
  - 평문 시크릿 Git 저장
  - 승인 없는 권한 확장
  - 검증 없는 배포 승격
  - 외부 런타임 의존 리소스를 임의 로컬 값으로 하드코딩

## Exceptions

- 임시 운영 예외는 아래 순서로 승인한다.
  1. 요청자가 범위/기간/위험/복구 조건을 명시한다.
  2. Platform Owner 1차 승인, Security Reviewer 2차 승인.
  3. 만료 시각(UTC)과 종료 조건을 문서화한다.
  4. 만료 후 기본 정책으로 복귀했는지 검증 증적을 남긴다.

## Verification

- 정책 준수 여부는 아래 증적으로 확인한다.

| Control Area | Required Evidence | Runbook Owner |
| --- | --- | --- |
| GitOps root path/branch | `root-platform` Application source path와 `targetRevision`이 운영 계약과 일치함 | [`../runbooks/0001-argocd-platform-bootstrap-runbook.md`](../runbooks/0001-argocd-platform-bootstrap-runbook.md) |
| External service contract | `platform` namespace Service/EndpointSlice가 PostgreSQL/Valkey 서비스명, IP, 포트 계약을 만족함 | [`../runbooks/0001-argocd-platform-bootstrap-runbook.md`](../runbooks/0001-argocd-platform-bootstrap-runbook.md) |
| Secret plane | ESO와 ArgoCD external secret 동기화 상태가 정상이며 평문 secret manifest가 없음 | [`../runbooks/0001-argocd-platform-bootstrap-runbook.md`](../runbooks/0001-argocd-platform-bootstrap-runbook.md) |

- 문서 검증 항목:
  - 템플릿 필수 섹션 누락 0건
  - 상대 링크 오류 0건
  - 평문 비밀번호/토큰 기재 0건

## Review Cadence

- 정기: 월 1회
- 비정기: 아래 변경 시 즉시 리뷰
  - 외부 서비스 접속 계약(포트/서비스명/경로) 변경
  - Vault 경로/권한 모델 변경
  - GitOps 루트 경로/브랜치 전략 변경

## AI Agent Policy Section (If Applicable)

- **Model / Prompt Change Process**: 운영 정책/런북 자동 수정 작업은 PR 단위 증적(변경 파일 + 검증 커맨드 결과)을 남긴다.
- **Eval / Guardrail Threshold**: 링크 오류 0건, 평문 시크릿 0건, 계약 포트 불일치 0건.
- **Log / Trace Retention**: 정책 변경 검증 로그를 관련 Plan/Task/Runbook에 기록한다.
- **Safety Incident Thresholds**: 비밀 유출, 무승인 권한 확장, 운영 경로 불일치 탐지 시 즉시 에스컬레이션한다.

## Related Documents

- **ARD**: [`../../02.architecture/requirements/0007-current-local-gitops-platform.md`](../../02.architecture/requirements/0007-current-local-gitops-platform.md)
- **Spec**: [`../../03.specs/008-current-local-gitops-platform/spec.md`](../../03.specs/008-current-local-gitops-platform/spec.md)
- **Runbook**: [`../runbooks/0001-argocd-platform-bootstrap-runbook.md`](../runbooks/0001-argocd-platform-bootstrap-runbook.md)
- **Postmortem Index**: [`../incidents/README.md`](../incidents/README.md)
