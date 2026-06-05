# Task: Azure Migration Implementation

## Overview

이 문서는 `hy-home.k8s` 인프라의 Azure 마이그레이션 구현 및 검증 작업 목록이다. 설계 명세(Spec)와 마이그레이션 전략(Plan)에서 도출된 세부 태스크를 추적한다.

## Inputs

- **Parent Spec**: [../03.specs/2026-03-31-resource-specs.md](../../03.specs/2026-03-31-resource-specs.md)
- **Parent Plan**: [../04.execution/plans/2026-03-31-migration-strategy.md](../plans/2026-03-31-migration-strategy.md)

## Working Rules

- 인프라(Bicep) 배포 전 `what-if`를 통해 영향도를 먼저 확인한다.
- 모든 쿠버네티스 리소스는 `dry-run` 검증 후 적용한다.
- 2026년 보안 표준(Workload Identity) 적용을 최우선으로 한다.

## Task Table

| Task ID | Description | Type | Parent Spec Section | Parent Plan Phase | Validation / Evidence | Status |
| --- | --- | --- | --- | --- | --- | --- |
| T-001 | PRD/ARD/ADR/Spec 작성 | doc | All | Phase 1 | 파일 존재 확인 | [x] Done |
| T-002 | `main.bicep` 기초 아키텍처 완성 | impl | §1, §2 | Phase 1 | `bicep lint` | [ ] Todo |
| T-003 | Managed 서비스 (DB/Redis) Bicep 작성 | impl | §3 | Phase 2 | 리소스 배포 확인 | [ ] Todo |
| T-004 | AGC (Application Gateway) Bicep 구성 | impl | §1 | Phase 2 | ALB Controller 연결 | [ ] Todo |
| T-005 | Workload Identity 매니페스트 작성 | impl | §2 | Phase 1 | ServiceAccount 속성 확인 | [ ] Todo |
| T-006 | KeyVault Secret Store 연동 매니페스트 | impl | §2 | Phase 2 | SecretProviderClass 생성 | [ ] Todo |
| T-007 | 운영 가이드 및 런북(07-09) 작성 | doc | All | Phase 4 | 가이드 리뷰 | [ ] Todo |
| T-008 | 최종 README 인덱싱 및 검증 | doc | All | Phase 5 | 링크 유효성 체크 | [ ] Todo |

## Verification Summary

- **Test Commands**: `az deployment group what-if`, `kubectl get gateway`, `kubectl get secretproviderclass`
- **Logs / Evidence Location**: `examples/azure/logs/` (필요 시 생성)
