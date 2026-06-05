# Azure AKS Deployment & Onboarding Guide

## Overview

이 문서는 로컬 K3s 환경에서 Azure AKS로 인프라를 이전한 후, 관리자가 클러스터를 배포하고 운영 환경에 온보딩하기 위한 가이드를 제공한다.

## Guide Type

`onboarding | how-to`

## Target Audience

- System Administrator
- Platform Engineer
- DevOps Specialist

## Purpose

이 가이드는 Bicep 기반 인프라 정의를 검토하고 AKS 클러스터 접근과 워크로드 연동 상태를 확인하는 reference-only 절차를 안내한다.

## Prerequisites

- **Azure CLI**: 최신 버전 설치 필수.
- **Bicep CLI**: 인프라 배포를 위해 필요.
- **kubectl**: 클러스터 제어용.
- **Azure Account**: 충분한 권한(Contributor + User Access Administrator)을 가진 계정.

## Step-by-step Instructions

### 1. Bicep 인프라 배포

리소스 그룹과 제공된 Bicep 템플릿의 변경 내용을 배포 전 검토한다. 실제 배포는 operator-approved change로 별도 실행한다.

```bash
# reference-only Azure sandbox; no live resource mutation
az deployment group what-if \
  --resource-group rg-hyhome-prod \
  --template-file infrastructure/main.bicep \
  --parameters adminName=admin@example.com adminObjectId=0000-0000-0000-0000
```

### 2. AKS 클러스터 자격 증명 획득

배포된 클러스터 접근은 기본 kubeconfig를 변경하지 않는 임시 파일로 확인한다.

```bash
TMP_KUBECONFIG="$(mktemp)"
az aks get-credentials --resource-group rg-hyhome-prod --name hyhome-aks --file "$TMP_KUBECONFIG" --overwrite-existing
KUBECONFIG="$TMP_KUBECONFIG" kubectl get nodes
```

### 3. ALB Controller (AGC) 설치

Azure Application Gateway for Containers 컨트롤러 매니페스트를 배포 전 렌더링한다.

```bash
helm template alb-controller oci://mcr.microsoft.com/azure-alb/charts/alb-controller \
  --version 1.0.0 \
  --set albId=$ALB_ID > /tmp/alb-controller.rendered.yaml
```

### 4. Workload Identity 및 Secret 연동 확인

애플리케이션이 Key Vault 시크릿을 정상적으로 가져오는지 secret value를 출력하지 않는 상태 점검으로 확인한다.

```bash
kubectl diff -f kubernetes/manifests/workload-identity.yaml
kubectl diff -f kubernetes/manifests/external-secrets-azure.yaml
kubectl get externalsecret db-credentials -o jsonpath='{.status.conditions[?(@.type=="Ready")].status}'
```

## Common Pitfalls

- **Bicep Parameter Missing**: `adminObjectId`를 누락할 경우 DB 권한 설정에서 오류가 발생할 수 있다.
- **Managed Identity Delay**: Identity 생성 후 Federated Identity 연동 시 전파 대기 시간(약 1-2분)이 필요할 수 있다.

## Related Documents

- **Spec**: [../03.specs/2026-03-31-resource-specs.md](../../03.specs/2026-03-31-resource-specs.md)
- **Operation**: [../05.operations/policies/2026-03-31-azure-ops-policy.md](../policies/2026-03-31-azure-ops-policy.md)
- **Runbook**: [../05.operations/runbooks/2026-03-31-fault-tolerance-runbook.md](../runbooks/2026-03-31-fault-tolerance-runbook.md)
