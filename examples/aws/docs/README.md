# AWS Migration Documentation Hub

> K3s 로컬 인프라의 AWS 클라우드 네이티브 전환을 위한 기술 자산 저장소

## Overview

이 디렉토리는 `hy-home.k8s` 인프라를 AWS EKS 1.35 target 및 Managed Services 환경으로 성공적으로 마이그레이션하기 위한 모든 설계, 계획, 운영 문서를 포함합니다. 2026-05-09 공식 지원 스냅샷 기준으로 구축되었습니다.

## Audience

- Cloud Architects
- DevOps Engineers
- Operations Team
- AI Agents

## Documentation Structure (9 Directories)

| Directory | Purpose | Primary Document |
| :--- | :--- | :--- |
| [01.prd](./01.prd/README.md) | 제품 요구사항 정의 | [AWS Migration PRD](./01.prd/2026-03-31-aws-migration-prd.md) |
| [02.ard](./02.ard/README.md) | 아키텍처 설계서 | [Target Architecture](./02.ard/0001-aws-cloud-native-architecture.md) |
| [03.adr](./03.adr/README.md) | 기술 의사결정 기록 | [Managed Service Selection](./03.adr/0001-aws-managed-services-selection.md) |
| [04.specs](./04.specs/README.md) | 상세 기술 명세 | [AWS Migration Spec](./04.specs/aws-migration/spec.md) |
| [05.plans](./05.plans/README.md) | 마이그레이션 로드맵 | [Migration Roadmap](./05.plans/2026-03-31-aws-migration-roadmap.md) |
| [06.tasks](./06.tasks/README.md) | 개별 실행 작업 리스트 | [Implementation Tasks](./06.tasks/2026-03-31-aws-migration-tasks.md) |
| [07.guides](./07.guides/README.md) | 운영 및 설정 가이드 | [AWS Setup Guide](./07.guides/aws-setup-guide.md) |
| [08.operations](./08.operations/README.md) | 시스템 운영 거버넌스 | [AWS Operations Policy](./08.operations/aws-operations-policy.md) |
| [09.runbooks](./09.runbooks/README.md) | 장애 대응 런북 | [AWS Disaster Recovery](./09.runbooks/aws-disaster-recovery.md) |

## Tech Stack & Standards

- **Cloud Platform**: Amazon Web Services (ap-northeast-2)
- **Container**: Amazon EKS 1.35 target, Karpenter v1.x
- **Data**: RDS Aurora Serverless v2, ElastiCache Serverless
- **Security**: IAM Pod Identity, AWS Secrets Manager + External Secrets Operator
- **IaC**: Terraform v1.14+

## Governance Rules

1. 모든 문서는 `../../../docs/99.templates/`에 정의된 전용 템플릿을 준수해야 합니다.
2. 모든 디렉토리는 자체 `README.md`를 통해 하위 산출물을 인덱싱해야 합니다.
3. 문서 간에는 반드시 상대 경로 링크(Cross-Referencing)를 유지하여 추적성을 확보해야 합니다.

---
마이그레이션 실행 및 상세 작업 내역은 [06.tasks](./06.tasks/README.md)를 참조하십시오.
