---
title: 'Task: AKS Cluster Provisioning'
type: sdlc/task
status: active
owner: platform
updated: 2026-07-06
---

# Task: AKS Cluster Provisioning

## Overview

이 작업은 `main.bicep` 인프라 코드를 실행하여 Azure에 기본적인 쿠버네티스 서비스(AKS) 및 관련 VNet 리소스를 구축하는 것을 목표로 한다.

## Snapshot Boundary

This document is an example-local SDLC snapshot for cloud migration reference. It follows the repository's Cloud Example Snapshot boundary and is not live provider-latest guidance.

## Task Table

| ID | Task | Status | Updated | Evidence |
| :--- | :--- | :--- | :--- | :--- |
| **01** | Bicep 템플릿 구문 검사(`az bicep build`) | [ ] | 2026-03-31 | - |
| **02** | Azure 리소스 그룹(`rg-hyhome`) 생성 | [ ] | 2026-03-31 | - |
| **03** | `main.bicep`을 통한 리소스 배포(`What-If` 포함) | [ ] | 2026-03-31 | - |
| **04** | AKS 노드 풀 생성 성공 여부 확인 | [ ] | 2026-03-31 | - |
| **05** | `az aks get-credentials --file`을 이용한 임시 kubeconfig 검증 | [ ] | 2026-03-31 | - |

## Performance & Quality Expectations

- **Provisioning Time**: Bicep 배포는 15분 이내에 완료되어야 함.
- **Connectivity**: AKS API 서버에 로컬 터미널에서 `kubectl get nodes` 명령이 즉시 가능해야 함.
- **Security**: 기본 NSG 규칙이 SSH 노출을 허용하지 않아야 함.

## Related Documents

- **Plan**: [../04.execution/plans/2026-03-31-azure-migration.md](../plans/2026-03-31-azure-migration.md)
- **Spec**: [../03.specs/azure-migration/spec.md](../../03.specs/azure-migration/spec.md)
- **IaC**: [../../infrastructure/main.bicep](../../../infrastructure/main.bicep)
