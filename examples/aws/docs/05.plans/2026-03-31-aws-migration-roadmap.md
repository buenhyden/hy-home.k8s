# AWS Migration Implementation Plan (Roadmap)

## Overview (KR)

이 문서는 hy-home.k8s 로컬 K3s 환경을 AWS 클라우드로 전이하기 위한 단계별 실행 계획을 정의한다. 인프라 기반 구축, 데이터 전이, 워크로드 배포 및 서비스 전환의 과정을 포함한다.

## Context

로컬 환경의 한계를 극복하고 AWS의 고가용성 및 관리 편의성을 확보하기 위해 체계적인 이관 절차가 필요하다. 서비스 중단을 최소화하기 위해 단계적(Phased) 접근 방식을 취한다.

## Goals & In-Scope

- **Goals**: 무중단 또는 최소 중단 마이그레이션 달성, 관리형 서비스로의 전환 완료.
- **In Scope**: AWS 리소스 구축(IaC), 데이터베이스 덤프/복원 테스트, EKS 워크로드 배포.

## Non-Goals & Out-of-Scope

- **Non-goals**: 온프레미스와의 영구적 하이브리드 연결 (이관 완료 후 로컬은 폐기 예정).
- **Out of Scope**: 애플리케이션의 아키텍처적 전면 재설계 (클라우드 최적화 설정은 포함하되 소스 코드는 유지).

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-001 | AWS Foundation 구축 (VPC, IAM, EKS) | `terraform/*` | REQ-PRD-FUN-01 | `kubectl get nodes` 확인 |
| PLN-002 | Platform Services 설치 (Karpenter, ESO) | `kubernetes/*` | REQ-PRD-FUN-02 | Add-on Pod 상태 확인 |
| PLN-003 | Managed Data Services 프로비저닝 | `terraform/rds.tf` | REQ-PRD-FUN-02 | DB 접속 테스트 |
| PLN-004 | Workload Deployment 및 검증 | `gitops/*` | REQ-PRD-FUN-03 | 앱 정상 동작 확인 |
| PLN-005 | Traffic Cutover 및 최종 안정화 | `terraform/route53.tf` | REQ-PRD-MET-01 | DNS 전환 및 모니터링 |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-001 | Infra | EKS 클러스터 접속 및 노드 상태 확인 | `kubectl get nodes` | Ready 상태의 노드 확인 |
| VAL-PLN-002 | Connect | RDS/ElastiCache 도달 가능성 테스트 | `nc -zv <endpoint> <port>` | Connection successful |
| VAL-PLN-003 | Secret | Secrets Manager 데이터 동기화 확인 | `kubectl get secret <name>` | 로컬 K8s에 시크릿 존재 |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| 데이터 전이 시 다운타임 발생 | High | 사전 덤프/복원 테스트 수행 및 가동 중단 최소화 시점 선정 |
| AWS 비용 급증 | Medium | CloudWatch Alarms 설정 및 리소스 태깅을 통한 비용 추적 |

## Completion Criteria

- [x] AWS 인프라 구축 완료
- [x] 모든 데이터 Managed Service로 이관 완료
- [x] 서비스 엔드포인트 정상 전환 확인
- [x] 마이그레이션 완료 보고서 작성

## Related Documents

- **PRD**: [../01.prd/2026-03-31-aws-migration-prd.md](file:///home/hy/project-infra/hy-home.k8s/examples/aws/docs/01.prd/2026-03-31-aws-migration-prd.md)
- **ARD**: [../02.ard/0001-aws-cloud-native-architecture.md](file:///home/hy/project-infra/hy-home.k8s/examples/aws/docs/02.ard/0001-aws-cloud-native-architecture.md)
- **Spec**: [../04.specs/aws-migration/spec.md](file:///home/hy/project-infra/hy-home.k8s/examples/aws/docs/04.specs/aws-migration/spec.md)
- **Tasks**: [../06.tasks/2026-03-31-aws-migration-tasks.md](file:///home/hy/project-infra/hy-home.k8s/examples/aws/docs/06.tasks/2026-03-31-aws-migration-tasks.md)
