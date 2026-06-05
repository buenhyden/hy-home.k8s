# AWS Infrastructure Migration Implementation Plan

## Overview

이 문서는 로컬 K3s 인프라를 AWS EKS 환경으로 성공적으로 이식하기 위한 통합 실행 계획서다. 인프라 프로비저닝, 서비스 이전, 최종 검증까지의 전 과정을 단계별로 정의한다.

## Context

현재 로컬 `k3d` 기반의 설정과 `bootstrap-local.sh` 루틴을 클라우드 환경으로 매끄럽게 전환하기 위해 명확한 타임라인과 검증 절차가 필요하다.

## Goals & In-Scope

- **Goals**: AWS 환경에서 서비스 안정성 확보, 가동 중단 최소화, 인프라 관리 코드화(IaC).
- **In Scope**: VPC/Network 설정, EKS 클러스터 구축, RDS/ElastiCache 배포, ArgoCD 연동.

## Non-Goals & Out-of-Scope

- **Non-goals**: 로컬 인프라의 즉각적인 폐기 (병행 운영 후 폐기 검토).
- **Out of Scope**: 프론트엔드/백엔드 애플리케이션 소스 코드 리팩토링.

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-001 | AWS 기반 설계 문서화 | [aws-cloud-architecture.md](../../02.architecture/requirements/aws-cloud-architecture.md) | REQ-PRD-FUN-01 | 문서 승인 완료 |
| PLN-002 | Terraform IaC 작성 | [main.tf](../../../terraform/main.tf) | REQ-PRD-FUN-02 | `terraform validate` 패스 |
| PLN-003 | EKS 클러스터 프로비저닝 | - | REQ-PRD-FUN-03 | `kubectl get nodes` 확인 |
| PLN-004 | 서비스 연동 매니페스트 배포 | [external-services-aws.yaml](../../../kubernetes/external-services-aws.yaml) | REQ-PRD-FUN-04 | 서비스 엔드포인트 확인 |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-001 | Infrastructure | AWS Resource Check | `terraform show` | 모든 리소스 Running 상태 |
| VAL-PLN-002 | Connectivity | DB/Redis Access | `telnet <endpoint> <port>` | 연결 성공 (Open) |
| VAL-PLN-003 | Application | Health Check | `curl -f http://<alb-dns>/health` | HTTP 200 OK |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| 데이터 마이그레이션 오류 | High | 이전 전 스냅샷 생성 및 롤백 절차 수립 |
| 클라우드 비용 초과 | Medium | 비용 알람 설정 및 필요 리소스 최소화 (Right-sizing) |
| 네트워크 보안 설정 지연 | Medium | 사전에 Security Group 및 IAM Role 매트릭스 확정 |

## Completion Criteria

- [x] AWS 설계 및 문서화 완료
- [x] Terraform 프로비저닝 코드 작성 완료
- [x] Kubernetes 연동 매니페스트 작성 완료
- [ ] 실제 인프라 배포 및 검증 통과 (실행 단계)

## Related Documents

- **PARD**: [../01.requirements/2026-03-31-aws-migration-prd.md](../../01.requirements/2026-03-31-aws-migration-prd.md)
- **AARD**: [../02.architecture/requirements/2026-03-31-aws-migration-ard.md](../../02.architecture/requirements/2026-03-31-aws-migration-ard.md)
- **Spec**: [../03.specs/aws-migration/spec.md](../../03.specs/aws-migration/spec.md)
- **ADR**: [../02.architecture/decisions/2026-03-31-replace-vault-with-secrets-manager.md](../../02.architecture/decisions/2026-03-31-replace-vault-with-secrets-manager.md)
