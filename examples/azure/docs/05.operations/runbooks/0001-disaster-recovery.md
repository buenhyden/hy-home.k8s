---
title: 'Azure Disaster Recovery Runbook'
type: sdlc/runbook
status: accepted
owner: platform
updated: 2026-07-06
---

# Azure Disaster Recovery Runbook

## Overview

Azure(AKS) 환경으로 마이그레이션된 `hy-home.k8s` 인프라에서 발생 가능한 중대 장애 및 재해 발생 시 서비스 복구 절차를 정의한다. 본 런북은 2026-05-09 공식 지원 스냅샷 기준 Azure 복구 기술 및 서비스 수준 목표(SLO)를 기반으로 작성되었다.

## Snapshot Boundary

This document is an example-local SDLC snapshot for cloud migration reference. It follows the repository's Cloud Example Snapshot boundary and is not live provider-latest guidance.

## Disaster Scenarios

1. **Scenario A**: AKS 리전 장애 및 컨트롤 플레인 붕괴.
2. **Scenario B**: 핵심 데이터베이스(PostgreSQL/Redis) 손상 또는 데이터 유실.
3. **Scenario C**: 침해 사고(보안 사고)로 인한 원본 리소스 훼손.

## Recovery Objectives (SLO)

- **RTO (Recovery Time Objective)**: 1시간 이내 (중대 사고 기준).
- **RPO (Recovery Point Objective)**: 5분 이내 (DB 데이터 유실 기준).

## Step-by-Step Recovery Procedures

### 1. AKS Cluster Recovery (Scenario A)

1. Bicep 인프라 코드를 활용하여 타겟 리전에 AKS 클러스터를 재배포한다.
2. ArgoCD를 새로운 클러스터에 배포하고 Git 리포지토리와 동기화한다.
3. **AGC** 엔드포인트를 신규 생성된 인스턴스로 전환하고 트래픽을 유입한다.

### 2. Database Restore (Scenario B)

1. **Azure Database for PostgreSQL Flexible Server** 의 Point-in-time Restore(PITR) 기능을 활용한다.
2. 장애 발생 직전의 시점으로 데이터베이스를 복원한다.
3. 애플리케이션 Pod의 `REDIS_HOST` 및 `DATABASE_HOST` 환경 변수를 업데이트한다.

### 3. Key Vault Recovery (Scenario C)

1. Key Vault의 `Soft Delete` 기능을 활용하여 삭제된 시크릿 및 키를 복구한다.
2. 위조된 서비스 주체(Service Principal)의 권한을 차단하고 RBAC 설정을 초기화한다.

## Post-Mortem Requirements

- 장애 복구 후 48시간 이내에 원인 분석 보고서(Post-mortem)를 작성한다.
- 재발 방지를 위한 ARD(Architecture Decision Record)를 02.architecture/decisions 경로에 업데이트한다.

## Escalation Matrix

- **Primary Contact**: Infrastructure Engineer / On-call SRE.
- **Secondary Contact**: Platform Security Lead.
- **Tools**: Azure Service Health, Monitor Dashboards, ArgoCD UI.

## Runbook Type

Example-local cloud operations runbook.

## Purpose

The purpose of this snapshot is to show the intended operational flow while preserving the no-live-mutation boundary.

## Canonical References

- Cloud Example Snapshot inventory.
- Sibling example-local SDLC documents under the same provider docs tree.

## When to Use

Use this runbook as a reference when planning an approved sandbox exercise for Azure; do not use it as a live production instruction without refresh.

## Procedure or Checklist

- Review existing procedure sections in this document.
- Replace placeholders in a sandbox plan.
- Capture validation evidence before promoting any live action.

## Verification Steps

- Confirm commands and resource names against current official provider docs.
- Confirm no secrets or private values are recorded in the repository.

## Observability and Evidence Sources

- Provider portal or CLI output captured outside the repository when sensitive.
- Repository task records for non-secret validation summaries.

## Safe Rollback or Recovery Procedure

Stop the exercise, preserve non-secret evidence, and revert any example edits if assumptions no longer match current provider behavior.

## Related Documents

- **PARD**: [../01.requirements/2026-03-31-azure-migration.md](../../01.requirements/2026-03-31-azure-migration.md)
- **Spec**: [../03.specs/azure-migration/spec.md](../../03.specs/azure-migration/spec.md)
- **Operations**: [../05.operations/policies/azure-maintenance-policy.md](../policies/azure-maintenance-policy.md)
