# AWS Migration Documentation Hub

> K3s 로컬 인프라의 AWS 클라우드 네이티브 전환을 위한 기술 자산 저장소

## Overview

이 디렉토리는 `hy-home.k8s` 인프라를 AWS EKS 1.35 target 및 Managed Services 환경으로 전환할 때 참고하는 설계, 계획, 운영 문서 예시를 포함합니다. 버전 현재성은 [Tech Stack Version Inventory](../../../docs/90.references/versions/tech-stack-version-inventory.md)의 `Cloud Example Snapshot`을 기준으로 확인하며, 현재 로컬 플랫폼의 active SSoT나 실제 AWS 배포 절차를 대체하지 않습니다.

## Audience

- Cloud Architects
- DevOps Engineers
- Operations Team
- AI Agents

## Scope

### In Scope

- AWS EKS 1.35 target migration reference 문서
- Terraform AWS provider 6.x 기반 예시 구조
- Managed Services 전환 시 검토할 PRD/ARD/ADR/Spec/Plan/Task/Guide/Policy/Runbook 예시

### Out of Scope

- 실제 AWS 계정 프로비저닝
- live Kubernetes 클러스터 변경
- 로컬 k3d desired state의 정본 변경

## Structure

| Directory | Purpose | Primary Document |
| :--- | :--- | :--- |
| [01.requirements](01.requirements/README.md) | 제품 요구사항 정의 | [AWS Migration PRD](01.requirements/2026-03-31-aws-migration-prd.md) |
| [02.architecture/requirements](02.architecture/requirements/README.md) | 아키텍처 설계서 | [Target Architecture](02.architecture/requirements/0001-aws-cloud-native-architecture.md) |
| [02.architecture/decisions](02.architecture/decisions/README.md) | 기술 의사결정 기록 | [Managed Service Selection](02.architecture/decisions/0001-aws-managed-services-selection.md) |
| [03.specs](03.specs/README.md) | 상세 기술 명세 | [AWS Migration Spec](03.specs/aws-migration/spec.md) |
| [04.execution/plans](04.execution/plans/README.md) | 마이그레이션 로드맵 | [Migration Roadmap](04.execution/plans/2026-03-31-aws-migration-roadmap.md) |
| [04.execution/tasks](04.execution/tasks/README.md) | 개별 실행 작업 리스트 | [Implementation Tasks](04.execution/tasks/2026-03-31-aws-migration-tasks.md) |
| [05.operations/guides](05.operations/guides/README.md) | 운영 및 설정 가이드 | [AWS Setup Guide](05.operations/guides/aws-setup-guide.md) |
| [05.operations/policies](05.operations/policies/README.md) | 시스템 운영 거버넌스 | [AWS Operations Policy](05.operations/policies/aws-operations-policy.md) |
| [05.operations/runbooks](05.operations/runbooks/README.md) | 장애 대응 런북 | [AWS Disaster Recovery](05.operations/runbooks/aws-disaster-recovery.md) |

## Tech Stack & Standards

- **Cloud Platform**: Amazon Web Services (ap-northeast-2)
- **Container**: Amazon EKS 1.35 target, Karpenter v1.x
- **Data**: RDS Aurora Serverless v2, ElastiCache Serverless
- **Security**: IAM Pod Identity, AWS Secrets Manager + External Secrets Operator
- **IaC**: Terraform v1.14+

## How to Work in This Area

1. 이 경로의 문서는 AWS migration reference로만 사용합니다.
2. 버전 기준을 바꾸면 [Tech Stack Version Inventory](../../../docs/90.references/versions/tech-stack-version-inventory.md)를 같은 변경에서 갱신합니다.
3. 실제 AWS 배포 전에는 provider 공식 지원 버전, IAM/RBAC, 비용, 네트워크 경계를 다시 확인합니다.
4. 문서 간에는 상대 경로 링크를 유지하여 추적성을 확보합니다.

## Link Basis

이 README의 링크 기준 위치는 `examples/aws/docs/`다.

- 같은 폴더의 파일과 하위 경로는 현재 README 위치 기준 상대 링크로 연결한다.
- 상위 저장소 문서나 다른 stage 문서는 필요한 만큼 `../`로 올라가서 연결한다.
- 다른 README의 상대 링크를 그대로 복사하지 말고, 이 파일 위치 기준으로 다시 계산한다.

## Related Documents

- [Examples README](../../README.md)
- [Tech Stack Version Inventory](../../../docs/90.references/versions/tech-stack-version-inventory.md)

---
마이그레이션 실행 및 상세 작업 내역은 [04.execution/tasks](04.execution/tasks/README.md)를 참조하십시오.
