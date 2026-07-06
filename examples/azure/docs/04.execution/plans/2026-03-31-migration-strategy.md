---
title: 'Azure Migration Strategy (Phase 1)'
type: sdlc/plan
status: active
owner: platform
updated: 2026-07-06
---

# Azure Migration Strategy (Phase 1)

## Overview

로컬 `hy-home.k8s` 인프라를 2026-05-09 공식 지원 스냅샷 기준 Azure(AKS) 환경으로 안정적으로 이전하기 위한 전략적 로드맵을 정의한다. 본 계획은 인프라 기반 확보, 플랫폼 서비스 연동, 애플리케이션 워크로드 이전, 운영 안정화의 4단계로 구성된다.

## Snapshot Boundary

This document is an example-local SDLC snapshot for cloud migration reference. It follows the repository's Cloud Example Snapshot boundary and is not live provider-latest guidance.

## Migration Phases

### Phase 1: Infrastructure Foundations (W1)

- **Goal**: AKS 클러스터 및 네트워크 기반 환경 구축.
- **Tasks**:
  - Bicep을 활용한 VNet, Subnet, AKS(CNI Overlay) 프로비저닝.
  - Entra ID Managed Identity 및 Workload Identity 설정.
- **Dependency**: Azure Subscription 및 RBAC 권한 확보.

### Phase 2: Platform Services Adoption (W2)

- **Goal**: 클라우드 관리형 데이터 및 보안 서비스 연동.
- **Tasks**:
  - PostgreSQL Flexible Server(HA) 및 Redis Premium 배포.
  - Key Vault 프로비저닝 및 Secret Store CSI Driver 설치.
  - **AGC (Gateway API)** 컨트롤러 설치 및 매니페스트 배포.

### Phase 3: Application Migration (W3)

- **Goal**: 실제 워크로드 이전 및 데이터 동기화.
- **Tasks**:
  - ArgoCD를 통한 하이브리드 배포 (Local & Azure 병행).
  - DB 데이터 마이그레이션 및 서비스 엔드포인트 AGC 전환.

### Phase 4: Production Stabilization (W4)

- **Goal**: 운영 모니터링 및 로컬 인프라 해제.
- **Tasks**:
  - Azure Monitor 통합 및 알람 설정.
  - 서비스 성능 검증 및 로컬 k3s 클러스터 완전 중단.

## Success / Acceptance Criteria

1. **W-PLAN-001**: 모든 인프라가 코드로 관리(IaC)되며 자동 배포 성공.
2. **W-PLAN-002**: 다운타임 최소화 (Phase 3 전환 시 1시간 이내).
3. **W-PLAN-003**: 2026년 보안 표준(Passwordless) 100% 준수.

## Context

This plan is a dated Azure migration snapshot. It organizes example work for planning and comparison, not live execution.

## Goals & In-Scope

- **Goals**: Show an example Azure migration flow and validation checkpoints.
- **In Scope**: Reference planning, sequencing, and evidence expectations.

## Non-Goals & Out-of-Scope

- **Non-goals**: Live deployment, provider-latest certification, and credential changes.
- **Out of Scope**: Production readiness without a fresh provider review.

## Work Breakdown

| Task | Description | Validation Criteria |
| --- | --- | --- |
| SNAP-001 | Review the existing phase or milestone content in this document. | Provider assumptions are still accurate for the intended sandbox. |
| SNAP-002 | Re-run repository-static checks before copying example manifests. | Local validation commands pass. |

## Verification Plan

| ID | Level | Description | Pass Criteria |
| --- | --- | --- | --- |
| SNAP-VAL-001 | Static | Review links, commands, and provider assumptions. | No stale provider-latest claim remains. |
| SNAP-VAL-002 | Sandbox | Optional provider sandbox dry run. | Human-approved evidence is recorded separately. |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Provider drift after snapshot date | High | Refresh official docs before live use. |
| Cost or IAM mismatch | High | Require human review and sandbox validation. |

## Completion Criteria

- [ ] Snapshot assumptions reviewed.
- [ ] Repository-static validation completed after any copy or edit.
- [ ] Live execution deferred to an approved provider plan.

## Related Documents

- **PARD**: [../01.requirements/2026-03-31-azure-migration.md](../../01.requirements/2026-03-31-azure-migration.md)
- **AARD**: [../02.architecture/requirements/0001-azure-migration-architecture.md](../../02.architecture/requirements/0001-azure-migration-architecture.md)
- **Tasks**: [../04.execution/tasks/2026-03-31-migration-tasks.md](../tasks/2026-03-31-migration-tasks.md)
