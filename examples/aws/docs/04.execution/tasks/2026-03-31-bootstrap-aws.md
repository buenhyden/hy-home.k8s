# Task: AWS Infrastructure Migration Implementation

## Overview

이 문서는 로컬 K3s 인프라를 AWS 환경으로 이식하는 과정에서 발생하는 모든 세부 작업 목록이다. Spec과 Plan에서 정의된 마일스톤에 따라 실제 구현 및 검증 과정을 추적한다.

## Inputs

- **Parent Spec**: [../03.specs/aws-migration/spec.md](../../03.specs/aws-migration/spec.md)
- **Parent Plan**: [../04.execution/plans/2026-03-31-aws-migration-plan.md](../plans/2026-03-31-aws-migration-plan.md)

## Working Rules

- 모든 작업은 완료 후 증빙(Evidence)을 남긴다.
- 인프라 코드는 배포 전 `terraform validate`를 통과해야 한다.
- 문서 작업은 상대 경로 링크의 무결성을 확인한다.

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-001 | AWS 마이그레이션 PRD 작성 | doc | §1 | Phase 1 | `file existence` | AI Agents | Done |
| T-002 | AWS 마이그레이션 ARD 작성 | doc | §2 | Phase 1 | `file existence` | AI Agents | Done |
| T-003 | Secret Manager 전환 ADR 작성 | doc | §3 | Phase 1 | ADR-001 | AI Agents | Done |
| T-004 | Terraform main.tf 코드 작성 | impl | §4 | Phase 2 | `tf validate` | AI Agents | Done |
| T-005 | K8s External Service 매니페스트 작성 | impl | §5 | Phase 3 | `kubectl diff` | AI Agents | Done |
| T-006 | 인프라 셋업 가이드 작성 | doc | §7 | Phase 4 | `file existence` | AI Agents | Done |

## Phase View

### Phase 1: 설계 및 문서화

- [x] T-001 PRD 작성
- [x] T-002 ARD 작성
- [x] T-003 ADR 작성

### Phase 2: 인프라 코드화 (IaC)

- [x] T-004 Terraform 코드 작성

### Phase 3: Kubernetes 연동

- [x] T-005 서비스 매니페스트 작성

### Phase 4: 운영 가이드 및 검증

- [x] T-006 가이드 작성

## Verification Summary

- **Infrastructure Check**: `terraform validate` (Draft checked)
- **Manifest Check**: `kubectl diff` (Draft checked)
- **Documentation Check**: Relative Link Integrity (Checked)
