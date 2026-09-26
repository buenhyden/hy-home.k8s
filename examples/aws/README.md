---
title: "AWS Executable Examples"
version: "0.2.0"
type: "common/readme-implementation"
status: "active"
owner: "platform"
updated: "2026-09-26"
---
# AWS Executable Examples

## Overview

### Current authority transfer

원래의 REQ-0007 / AD-0010 program 계보는 역사적 맥락으로만 남는다.
현재 플랫폼 요구사항과 아키텍처는 REQ-0004(`docs/01.requirements/0004-current-local-gitops-platform.md`)와
AD-0007(`docs/02.architecture/descriptions/0007-current-local-gitops-platform.md`)이 소유하고 공통 routing, 승인, QA는 REQ-0003(`docs/01.requirements/0003-workspace-agent-governance-platform.md`)과
AD-0006(`docs/02.architecture/descriptions/0006-workspace-agent-governance-platform.md`)이 소유한다. package 안의 실행 상태와 끝나지 않은
0047..0051 의무는 그대로다. 이 이관은 acceptance나 종료를 뜻하지 않는다.

이 진입점은 실행 가능한 AWS 예시 자산의 경계를 정한다. Terraform과
Kubernetes 파일은 참조 구현이다. 활성 로컬 desired state가 아니며 현재의 AWS
지원, 계정 준비 상태, 비용, provider 최신 설정을 증명하지도 않는다.

## Structure

| 경로 | 역할 | 권한 경계 |
| --- | --- | --- |
| [`terraform/`](terraform/) | VPC, EKS, 데이터, 캐시, secret 서비스 Terraform 예시 | 실행 가능한 참조 자산. 사용 전에 provider 지원 범위와 계정 입력값을 검토한다. |
| [`kubernetes/`](kubernetes/) | Karpenter, External Secrets, 외부 서비스 Kubernetes 예시 | 실행 가능한 참조 자산. 이 저장소의 로컬 ArgoCD 트리가 reconcile하지 않는다. |

## Configuration Boundary

AWS credential, 공개 승인을 받지 않은 계정 식별자, Terraform state,
kubeconfig, 토큰, 키, 인증서, secret 값은 커밋하지 않는다. 버전 제약은 각
Terraform·Kubernetes 파일이 직접 소유한다. 승인된 용도로 쓰기 전에 AWS와
provider의 공식 지원 범위를 다시 확인한다.

## Validation

먼저 저장소 정적 검사를 실행한다.

```bash
bash scripts/validate-k8s-manifests.sh .
bash scripts/check-secret-handling.sh .
python3 scripts/qa.py full
```

이 예시에 `terraform fmt`나 다른 Terraform 명령을 실행하는 저장소 gate는 없다.
그 검증기를 추가하려던 SPEC-0050은 validation registry에 Terraform 검증기가
선언되어 있지 않아 2026-09-24에 철회되었다.

위 명령은 AWS에 인증하지 않으며 live EKS, IAM, 네트워크, 비용, secret,
provider 준비 상태를 증명하지 않는다.

## Operations

이 자산은 provider 운영 절차를 정의하지 않는다. provider나 live cluster에
손대기 전에 정확한 소스 diff, 현재 AWS·provider 공식 지원 범위, credential
경계, 비용, 롤백을 검토하고 사람의 승인을 받는다.

## Related Documents

- [Examples index](../README.md)
- REQ-0004 — 현재 플랫폼 요구사항 (`docs/01.requirements/0004-current-local-gitops-platform.md`)
- AD-0007 — 현재 플랫폼 아키텍처 (`docs/02.architecture/descriptions/0007-current-local-gitops-platform.md`)
