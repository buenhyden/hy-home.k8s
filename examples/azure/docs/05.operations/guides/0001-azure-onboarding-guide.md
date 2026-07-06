---
title: 'Azure Onboarding Guide'
type: sdlc/guide
status: accepted
owner: platform
updated: 2026-07-06
---

# Azure Onboarding Guide

## Overview

로컬 k3s에서 Azure AKS로 이전된 신규 인프라 환경(`hy-home.k8s`)에 대한 개발자 및 운영자 온보딩 가이드를 정의한다. 본 문서는 클러스터 접근, 시크릿 관리, 배포 워크플로우에 대한 표준 절차를 포함한다.

## Snapshot Boundary

This document is an example-local SDLC snapshot for cloud migration reference. It follows the repository's Cloud Example Snapshot boundary and is not live provider-latest guidance.

## Prerequisites

- **Tools**:
  - `az` CLI v2.60.0+
  - `kubectl` 1.35-compatible version
  - `fubectl` (Optional, for helper functions)
  - `stern` (For log streaming)

## Enrollment & Authentication

### 1. Azure CLI Login

```bash
az login --tenant <YOUR_TENANT_ID>
az account set --subscription <YOUR_SUBSCRIPTION_ID>
```

### 2. Get AKS Credentials

```bash
TMP_KUBECONFIG="$(mktemp)"
az aks get-credentials --resource-group hy-home-rg --name hy-home-aks --file "$TMP_KUBECONFIG" --overwrite-existing
KUBECONFIG="$TMP_KUBECONFIG" kubectl get nodes
```

### 3. Workload Identity Integration

- 모든 애플리케이션 Pod은 `azure.workload.identity/use: "true"` 라벨을 포함해야 하며, 지정된 `ServiceAccount`를 사용하여 패스워드 없이 Azure 리소스에 접근한다.

## Secret Management (Secret Store CSI)

모든 시크릿은 Azure Key Vault(AKV)에서 중앙 관리된다.

- **Mount Path**: `/mnt/secrets-store`
- **Synchronization**: `SecretProviderClass`를 통해 K8s Native Secret으로 동기화되어 환경 변수로 주입 가능하다.

## Deployment Workflow

1. **GitOps Implementation**: 모든 변경사항은 `gitops/` 디렉토리에 커밋하여 ArgoCD를 통해 반영한다.
2. **Platform Sync**: `gitops/platform/` 하위의 레이어 변경 시 플랫폼 팀의 검토가 선행되어야 한다.

## Troubleshooting

- **Pod ID Issues**: `kubectl get pod -o yaml`에서 `AZURE_FEDERATED_TOKEN_FILE` 환경 변수가 자동 주입되었는지 확인한다.
- **AGC Routing**: `kubectl get gtw,httproute -n gateway-system`으로 게이트웨이 상태를 점검한다.

## Related Documents

- **PARD**: [../01.requirements/2026-03-31-azure-migration.md](../../01.requirements/2026-03-31-azure-migration.md)
- **Operations**: [../05.operations/policies/azure-maintenance-policy.md](../policies/azure-maintenance-policy.md)
- **Runbook**: [../05.operations/runbooks/0001-disaster-recovery.md](../runbooks/0001-disaster-recovery.md)
