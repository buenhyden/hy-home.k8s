---
title: 'AKS 노드 풀 교체 및 규모 조정 절차'
type: sdlc/runbook
status: accepted
owner: platform
updated: 2026-07-06
---

# AKS 노드 풀 교체 및 규모 조정 절차

## Overview

이 런북은 운영 중인 AKS 클러스터의 특정 노드 풀을 교체하거나 임시적으로 노드 풀의 규모를 변경해야 할 때의 단계별 실행 절차를 정의한다.

## Snapshot Boundary

This document is an example-local SDLC snapshot for cloud migration reference. It follows the repository's Cloud Example Snapshot boundary and is not live provider-latest guidance.

## 1. 노드 풀 교체 (Rolling Update)

기존 노드 풀의 VM 크기를 변경하거나 구성 수정을 위해 새로운 풀로 교체할 때 사용한다.

### 가. 신규 노드 풀 생성

```bash
az aks nodepool add \
  --resource-group rg-hyhome \
  --cluster-name aks-hyhome \
  --name newuserpool \
  --node-count 2 \
  --mode User \
  --node-vm-size Standard_DS3_v2
```

### 나. 기존 노드 드레인 (Drain)

Pod들이 안전하게 신규 노드로 이동하도록 유도한다.

```bash
kubectl drain <old-node-name> --ignore-daemonsets --delete-emptydir-data
```

### 다. 기존 노드 풀 삭제

```bash
az aks nodepool delete \
  --resource-group rg-hyhome \
  --cluster-name aks-hyhome \
  --name userpool
```

## 2. 노드 규모 조정 (Scaling)

트래픽 급증 또는 야간 시간대 비용 절감을 위해 노드 수를 수동으로 조정한다.

### 가. 수동 스케일 아웃 (Scale-out)

```bash
az aks nodepool scale \
  --resource-group rg-hyhome \
  --cluster-name aks-hyhome \
  --name userpool \
  --node-count 5
```

### 나. 자동 크기 조정 (Autoscaler) 활성화

```bash
az aks nodepool update \
  --resource-group rg-hyhome \
  --cluster-name aks-hyhome \
  --name userpool \
  --enable-cluster-autoscaler \
  --min-count 2 \
  --max-count 10
```

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

- **Operation**: [../05.operations/policies/azure-cost-optimization.md](../policies/azure-cost-optimization.md)
- **Task**: [../04.execution/tasks/0001-aks-cluster-provisioning.md](../../04.execution/tasks/0001-aks-cluster-provisioning.md)
- **Monitoring**: Azure Portal의 AKS 인사이트 대시보드
- [Azure Example Documentation Hub](../../README.md)
