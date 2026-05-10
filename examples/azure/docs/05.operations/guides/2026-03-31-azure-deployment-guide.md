# Azure AKS Deployment & Onboarding Guide

## Overview (KR)

이 문서는 로컬 K3s 환경에서 Azure AKS로 인프라를 이전한 후, 관리자가 클러스터를 배포하고 운영 환경에 온보딩하기 위한 가이드를 제공한다.

## Guide Type

`onboarding | how-to`

## Target Audience

- System Administrator
- Platform Engineer
- DevOps Specialist

## Purpose

이 가이드는 Bicep을 이용한 인프라 프로비저닝부터 AKS 클러스터 접근 설정, 그리고 첫 번째 워크로드 배포 확인까지의 과정을 안내한다.

## Prerequisites

- **Azure CLI**: 최신 버전 설치 필수.
- **Bicep CLI**: 인프라 배포를 위해 필요.
- **kubectl**: 클러스터 제어용.
- **Azure Account**: 충분한 권한(Contributor + User Access Administrator)을 가진 계정.

## Step-by-step Instructions

### 1. Bicep 인프라 배포

리소스 그룹을 생성하고 제공된 Bicep 템플릿을 사용하여 인프라를 프로비저닝한다.

```bash
# 리소스 그룹 생성
az group create --name rg-hyhome-prod --location koreacentral

# Bicep 배포 (adminObjectId는 본인의 Entra ID 객체 ID 입력)
az deployment group create \
  --resource-group rg-hyhome-prod \
  --template-file infrastructure/main.bicep \
  --parameters adminName=admin@example.com adminObjectId=0000-0000-0000-0000
```

### 2. AKS 클러스터 자격 증명 획득

배포된 클러스터에 접근하기 위해 `kubeconfig`를 업데이트한다.

```bash
az aks get-credentials --resource-group rg-hyhome-prod --name hyhome-aks
```

### 3. ALB Controller (AGC) 설치

Azure Application Gateway for Containers를 제어하기 위한 컨트롤러를 클러스터에 설치한다.

```bash
# Helm을 통한 설치 (사전 정의된 가이드 준수)
helm install alb-controller oci://mcr.microsoft.com/azure-alb/charts/alb-controller \
  --version 1.0.0 \
  --set albId=$ALB_ID
```

### 4. Workload Identity 및 Secret 연동 확인

애플리케이션이 Key Vault 시크릿을 정상적으로 가져오는지 테스트한다.

```bash
# reference-only Azure sandbox; operator-approved bootstrap only
kubectl apply -f kubernetes/manifests/workload-identity.yaml
kubectl apply -f kubernetes/manifests/external-secrets-azure.yaml
kubectl get secret db-credentials -o yaml
```

## Common Pitfalls

- **Bicep Parameter Missing**: `adminObjectId`를 누락할 경우 DB 권한 설정에서 오류가 발생할 수 있다.
- **Managed Identity Delay**: Identity 생성 후 Federated Identity 연동 시 전파 대기 시간(약 1-2분)이 필요할 수 있다.

## Related Documents

- **Spec**: [../03.specs/2026-03-31-resource-specs.md](../../03.specs/2026-03-31-resource-specs.md)
- **Operation**: [../05.operations/policies/2026-03-31-azure-ops-policy.md](../policies/2026-03-31-azure-ops-policy.md)
- **Runbook**: [../05.operations/runbooks/2026-03-31-fault-tolerance-runbook.md](../runbooks/2026-03-31-fault-tolerance-runbook.md)
