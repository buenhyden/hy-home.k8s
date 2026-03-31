# Azure Onboarding Guide

## Overview (KR)

이 문서는 Azure AKS 및 관련 관리형 서비스를 이용하기 위한 개발자 온보딩 가이드라인을 정의한다. 로컬 k3s 환경에 익숙한 팀원들이 Azure 클라우드 인프라(AKS, AGC, MI)를 이해하고, 필요한 도구 설치부터 클러스터 접속까지의 과정을 원활히 수행할 수 있도록 돕는다.

## Purpose

새로운 팀원이나 운영자가 `hy-home.k8s` Azure 모델 시스템에 성공적으로 합류하고, 표준화된 절차에 따라 개발 및 운영을 시작할 수 있도록 한다.

## Canonical References

- **Spec**: [../04.specs/azure-migration/spec.md](../04.specs/azure-migration/spec.md)
- **ADR**: [../03.adr/README.md](../03.adr/README.md)
- **Plan**: [../05.plans/2026-03-31-migration-strategy.md](../05.plans/2026-03-31-migration-strategy.md)

## Onboarding Checklist

- [ ] Azure Subscription 접근 권한 확인 (Entra ID 계정).
- [ ] Azure CLI 및 Bicep CLI 설치.
- [ ] Kubectl 1.30+ 및 Helm 3.x 설치.
- [ ] 로컬 Git 환경 내 `examples/azure/` 경로 코드 확보.

## Step-by-Step Procedure

### Step 1: Tool Installation
Azure 환경 제어를 위해 다음 도구들을 설치한다.
```bash
# Azure CLI
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Bicep CLI
az bicep install
```

### Step 2: Authentication & Context Setup
Azure 구독에 로그인하고 AKS 컨텍스트를 설정한다.
```bash
# Login to Azure
az login --tenant <TENANT_ID>

# Get AKS Credentials
az aks get-credentials --resource-group hy-home-k8s-prod-rg --name hy-home-aks-cluster
```

### Step 3: Architecture Understanding
[02.ard/0001-azure-migration-architecture.md](../02.ard/0001-azure-migration-architecture.md) 문서를 통해 전체 시스템 구조(AGC, OIDC, Managed DB)를 숙지한다.

## Verification

- [ ] `az account show`를 실행하여 올바른 구독이 활성화되었는지 확인.
- [ ] `kubectl get nodes`를 실행하여 AKS 클러스터와 통신이 원활한지 확인.
- [ ] `az identity list`를 실행하여 Workload Identity용 Managed Identity가 노출되는지 확인.

## Troubleshooting

- **403 Forbidden**: Role-Based Access Control(RBAC) 권한이 부족한 경우 클러스터 관리자에게 `Azure Kubernetes Service Cluster User Role` 요청.
- **Login Issues**: `az login --use-device-code`를 사용하여 브라우저 로그인을 시도.

## Related Guides

- **Tasks**: [../06.tasks/2026-03-31-migration-tasks.md](../06.tasks/2026-03-31-migration-tasks.md)
- **Runbook**: [../09.runbooks/0001-disaster-recovery.md](../09.runbooks/0001-disaster-recovery.md)
