---
title: 'Azure Infrastructure Fault Tolerance Runbook'
type: sdlc/runbook
status: accepted
owner: platform
updated: 2026-07-06
---

# Azure Infrastructure Fault Tolerance Runbook

: Azure Cluster & Managed Services

## Overview

이 런북은 Azure AKS 및 관리형 서비스(PostgreSQL, AGC)에서 발생할 수 있는 주요 장애 시나리오에 대한 즉각적인 실행 절차를 정의한다. 운영자가 즉시 따라 할 수 있는 단계와 검증 기준을 제공한다.

## Snapshot Boundary

This document is an example-local SDLC snapshot for cloud migration reference. It follows the repository's Cloud Example Snapshot boundary and is not live provider-latest guidance.

## Purpose

인프라 장애 시 서비스 다운타임을 최소화하고, 관리형 서비스의 자동/수동 복구 절차를 신속하게 수행하기 위해 작성되었다.

## Canonical References

- [../02.architecture/requirements/2026-03-31-azure-migration-ard.md](../../02.architecture/requirements/2026-03-31-azure-migration-ard.md)
- [../03.specs/2026-03-31-resource-specs.md](../../03.specs/2026-03-31-resource-specs.md)

## When to Use

- AKS 노드 풀의 가용성 문제 발생 시.
- Azure Database for PostgreSQL 연결 지연 또는 DB 인스턴스 중단 시.
- Application Gateway for Containers (AGC) 구성 오류로 인한 외부 접속 불가 시.

## Procedure or Checklist

### 🏗️ AKS Node Pool Recovery

일부 노드가 `NotReady` 상태이거나 파드 스케줄링이 불가능할 경우:

1. 노드 상태 확인: `kubectl get nodes`
2. 이벤트 확인: `kubectl get events -A --sort-by='.lastTimestamp'`
3. 노드 재생성(Reimage) 또는 확장:

    ```bash
    az aks nodepool update --resource-group rg-hyhome-prod --cluster-name hyhome-aks --name userpool --node-count 5
    ```

### 💾 PostgreSQL Flexible Server Failover

DB 접근이 불가능하거나 지연이 발생할 경우:

1. 상태 확인: `az postgres flexible-server show --resource-group rg-hyhome-prod --name hyhome-pg-server`
2. 수동 장애 조치 트리거 (필요 시):

    ```bash
    az postgres flexible-server restart --resource-group rg-hyhome-prod --name hyhome-pg-server --failover Forced
    ```

### 🌐 AGC Configuration Fix

HTTPRoute 또는 Gateway가 정상적으로 작동하지 않을 경우:

1. ALB Controller 로그 확인: `kubectl logs -n azure-alb-system -l app=alb-controller`
2. 리소스 상태 확인: `kubectl get gateway,httproute -A`
3. 상태 메시지(Condition) 체크: `kubectl describe httproute hyhome-route`

## Verification Steps

- [ ] `kubectl get nodes` 결과가 모두 `Ready`인지 확인.
- [ ] `nslookup`을 통한 DB Endpoint 확인: `nslookup hyhome-pg-server.postgres.database.azure.com`
- [ ] AGC Frontend FQDN 접속 확인: `curl -I https://<agc-fqdn>`

## Observability and Evidence Sources

- **Signals**: Azure Monitor Alerts (CPU > 80%, Connection Failure Count).
- **Evidence to Capture**: `kubectl describe`, `az monitor activity-log list`.

## Safe Rollback or Recovery Procedure

- **GitOps Rollback**: `argocd app rollback hyhome-root` 기능을 사용하여 이전 정상 상태의 매니페스트로 복구.
- **Bicep Redployment**: 마지막 성공한 deployment 버전을 사용하여 인프라 재배포.

## Runbook Type

Example-local cloud operations runbook.

## Related Documents

- **Incident index**: [root incident README](../../../../../docs/05.operations/incidents/README.md)
- **Postmortem examples**: 기록이 생기면 root incident/postmortem taxonomy에 맞춰 연결한다.
