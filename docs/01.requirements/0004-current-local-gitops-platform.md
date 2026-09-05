---
title: "Local GitOps Platform and Delivery Assurance Requirements"
version: "1.0.0"
type: "sdlc/requirement"
status: "active"
owner: "platform"
updated: "2026-09-05"
layer: "requirements"
artifact_id: "REQ-0004"
---

# Local GitOps Platform and Delivery Assurance Requirements

## Overview

이 문서는 로컬 GitOps 플랫폼의 사용자 가치, 운영 경계 및 delivery assurance 요구를 소유한다.
구체 topology와 구현 선택은 [AD-0007](../02.architecture/descriptions/0007-current-local-gitops-platform.md),
공통 거버넌스·검증·승인 요구는 [REQ-0003](./0003-workspace-agent-governance-platform.md)가 소유한다.

## Vision

사용자는 저장소의 desired state와 깊이가 구분된 증거로 로컬 플랫폼을 재현하고 안전하게 변경할 수 있어야 한다.

## Problem Statement

현재 desired state, 과거 문서와 실제 runtime 상태를 혼동하면 제거된 기능 또는 검증되지 않은 보안 수준을
지원한다고 안내할 수 있다. 정적 구성이 있다는 사실과 reconciliation 또는 외부 서비스 가용성은 분리해야 한다.

## Personas

- Platform engineer: 플랫폼 소유 경계와 외부 서비스 인터페이스를 관리한다.
- Operator: 현재 UI, GitOps 상태와 제한된 관측 증거로 운영한다.
- Application author: workload와 cloud example의 검증·온보딩 경계를 따른다.

## Key Use Cases

- 변경자가 각 surface의 semantic owner와 필요한 정적 검증을 찾는다.
- 운영자가 플랫폼/workload 경계와 외부 서비스 의존성을 확인한다.
- 검토자가 실패·fallback·DEFER 및 live 미관측 상태를 분리해 판정한다.
- 실행자가 미완료 assurance package를 선행 검증과 승인 범위에 맞게 재개한다.

## Functional Requirements

- **REQ-0004-FR-0001**: 로컬 플랫폼의 desired state는 저장소에서 소유 경계를 구분해 재현 가능하게 선언되어야 한다.
- **REQ-0004-FR-0002**: 플랫폼 구성 요소와 사용자 workload의 조정·소유·권한 경계를 분리해야 한다.
- **REQ-0004-FR-0003**: 외부 비밀정보·데이터·관측 서비스 연결은 명시적인 서비스 인터페이스로 표현하고 외부 runtime 생성과 구분해야 한다.
- **REQ-0004-FR-0004**: 운영자는 현재 지원되는 cluster UI에 접근할 수 있어야 하며 제거된 UI를 현재 구현으로 안내하지 않아야 한다.
- **REQ-0004-FR-0005**: 변경 범위의 추적된 surface는 변경, 근거 있는 무변경 또는 owner·재시도 조건이 있는 DEFER로 분류되어야 한다.
- **REQ-0004-FR-0006**: 재개·복구·미커밋 변경은 semantic owner에 따라 채택 또는 제외하고 임시 branch/stash/generated identity를 현재 권위로 고정하지 않아야 한다.
- **REQ-0004-FR-0007**: GitHub의 label과 code ownership 투영은 단일 affected-path owner와 일치하고 누락·중복·모호한 라우팅을 검증해야 한다.
- **REQ-0004-FR-0008**: 플랫폼 검증 결과는 syntax, render, schema/policy, product semantic 및 live observation 깊이와 도구·fallback·lane·결과를 구분해야 한다.
- **REQ-0004-FR-0009**: 실행 가능한 cloud example은 예제 옆의 안내 및 provider-native 정적 검증을 갖추되 credential이나 apply/deploy 없이 검증할 수 있어야 한다.
- **REQ-0004-FR-0010**: Ingress reference, 리소스 종류, GitOps 구조, policy, 비밀정보 동기화와 명시적 local-only transport 예외를 fail-closed로 검사해야 한다.
- **REQ-0004-FR-0011**: 플랫폼 assurance 작업은 순서가 있는 package별 검토·검증·rollback 단위로 수행하고 최종 local-only integration을 증명해야 한다.
- **REQ-0004-FR-0012**: 정확한 infrastructure·workflow·dependency·example 버전은 실행 소스 또는 검토된 lock에서 확인하고 Reference mirror를 실행 선행조건으로 요구하지 않아야 한다.
- **REQ-0004-FR-0013**: 자기 저장소의 지속 조정 source와 외부 배포 source의 revision 정책을 구분하고 다중 운영자·환경 또는 history rewrite 도입 때 재검토해야 한다.
- **REQ-0004-FR-0014**: Pod security 강제 수준은 저장소가 소유하고 정적으로 검증한 workload 근거에 비례해야 한다. Chart·injection·runtime 불확실성은 audit/warn으로 구분하고 CNI desired state를 live 증거로 승격하지 않는다.
- **REQ-0004-NFR-0001**: 로컬 플랫폼은 인증서, ingress, service mesh, 관측 UI, 점진적 배포, 알림, monitoring 및 외부 비밀정보 연동의 현재 통합 범위를 제공해야 한다.
- **REQ-0004-NFR-0002**: Secret value, token 및 private key는 Git, 문서 또는 로그에 기록하지 않아야 한다.
- **REQ-0004-NFR-0003**: Image와 artifact assurance는 fail-closed로 유지하되 검증 없는 일괄 digest 전환은 하지 않고 후속 provenance 의무는 consumer·owner·trigger로 명시해야 한다.
- **REQ-0004-IF-0001**: 과거 기록은 current 실행 권위와 분리해야 한다. 완료 package의 명시적 역사 인용은 허용하되 봉인 record를 현재 구현 지침으로 사용하지 않는다.

## Success / Acceptance Criteria

현재 desired-state 구조, Kubernetes syntax와 product static contract가 해당 validator를 통과해야 한다.
Delivery assurance는 모든 in-scope surface에 분류·검증 깊이·결과·한계를 남겨야 하며
원격·runtime 미관측을 정적 PASS로 대체하지 않는다. 아래 trace의 member별 판정은 AD와 해당 Spec에 연결된다.

- **Acceptance criterion 01**: 현재 platform product static contract를 검증한다.
- **Acceptance criterion 02**: Root, platform 및 workload의 GitOps 소유·조정 경계를 검증한다.
- **Acceptance criterion 03**: 추적된 Kubernetes manifest의 syntax를 검증한다.
- **Acceptance criterion 04**: 현재 문서와 historical Archive의 권위 분리 및 관련 repository gate를 검증한다.

## Scope and Non-goals

현재 로컬 플랫폼, platform/workload 분리, 외부 서비스 연결, 온보딩 예제 및 local-only assurance가 범위다.
외부 runtime 생성, cloud provisioning, 승인 없는 cluster 변경 및 검증 없는 blanket digest 전환은 범위가 아니다.

## Risks, Dependencies, and Assumptions

외부 서비스와 실제 클러스터 가용성은 별도 준비·관측이 필요하다. 이 문서 갱신은 live 검증이나 배포가 아니다.
비밀정보 읽기, push, cloud 작업과 live mutation에는 별도 승인이 필요하다.

### Unfinished delivery assurance

[0047](../03.specs/0047-current-surface-and-stash-reconciliation/spec.md)은 active resumption owner이며
구현 Tasks는 미완료다. [0048](../03.specs/0048-github-routing-and-ci-evidence/spec.md),
[0049](../03.specs/0049-platform-validation-and-security-evidence/spec.md),
[0050](../03.specs/0050-example-iac-and-validator-qa/spec.md),
[0051](../03.specs/0051-repository-assurance-integration-and-closure/spec.md)은 순차 선행 gate를 기다린다.
원래 REQ-0007 프로그램 이력은 유지하며 현재 플랫폼 의미를 이 문서로, 공통 라우팅·승인·QA 의미를 REQ-0003으로 승계한다.
이 승계는 어느 tranche 또는 Spec 0054 WP-013의 완료 선언도 아니다.

## Traceability

### Lifecycle Traceability

| Requirement ID | Acceptance criterion | Downstream owner |
| --- | --- | --- |
| REQ-0004-FR-0001 | 로컬 플랫폼의 desired state는 저장소에서 소유 경계를 구분해 재현 가능하게 선언되어야 한다. 충족 여부를 해당 owner의 정적 검증과 별도 관측 증거로 판정한다. | [AD-0007](../02.architecture/descriptions/0007-current-local-gitops-platform.md) |
| REQ-0004-FR-0002 | 플랫폼 구성 요소와 사용자 workload의 조정·소유·권한 경계를 분리해야 한다. 충족 여부를 해당 owner의 정적 검증과 별도 관측 증거로 판정한다. | [AD-0007](../02.architecture/descriptions/0007-current-local-gitops-platform.md) |
| REQ-0004-FR-0003 | 외부 비밀정보·데이터·관측 서비스 연결은 명시적인 서비스 인터페이스로 표현하고 외부 runtime 생성과 구분해야 한다. 충족 여부를 해당 owner의 정적 검증과 별도 관측 증거로 판정한다. | [AD-0007](../02.architecture/descriptions/0007-current-local-gitops-platform.md) |
| REQ-0004-FR-0004 | 운영자는 현재 지원되는 cluster UI에 접근할 수 있어야 하며 제거된 UI를 현재 구현으로 안내하지 않아야 한다. 충족 여부를 해당 owner의 정적 검증과 별도 관측 증거로 판정한다. | [AD-0007](../02.architecture/descriptions/0007-current-local-gitops-platform.md) |
| REQ-0004-FR-0005 | 변경 범위의 추적된 surface는 변경, 근거 있는 무변경 또는 owner·재시도 조건이 있는 DEFER로 분류되어야 한다. 충족 여부를 해당 owner의 정적 검증과 별도 관측 증거로 판정한다. | [AD-0007](../02.architecture/descriptions/0007-current-local-gitops-platform.md) |
| REQ-0004-FR-0006 | 재개·복구·미커밋 변경은 semantic owner에 따라 채택 또는 제외하고 임시 branch/stash/generated identity를 현재 권위로 고정하지 않아야 한다. 충족 여부를 해당 owner의 정적 검증과 별도 관측 증거로 판정한다. | [AD-0007](../02.architecture/descriptions/0007-current-local-gitops-platform.md) |
| REQ-0004-FR-0007 | GitHub의 label과 code ownership 투영은 단일 affected-path owner와 일치하고 누락·중복·모호한 라우팅을 검증해야 한다. 충족 여부를 해당 owner의 정적 검증과 별도 관측 증거로 판정한다. | [AD-0007](../02.architecture/descriptions/0007-current-local-gitops-platform.md) |
| REQ-0004-FR-0008 | 플랫폼 검증 결과는 syntax, render, schema/policy, product semantic 및 live observation 깊이와 도구·fallback·lane·결과를 구분해야 한다. 충족 여부를 해당 owner의 정적 검증과 별도 관측 증거로 판정한다. | [AD-0007](../02.architecture/descriptions/0007-current-local-gitops-platform.md) |
| REQ-0004-FR-0009 | 실행 가능한 cloud example은 예제 옆의 안내 및 provider-native 정적 검증을 갖추되 credential이나 apply/deploy 없이 검증할 수 있어야 한다. 충족 여부를 해당 owner의 정적 검증과 별도 관측 증거로 판정한다. | [AD-0007](../02.architecture/descriptions/0007-current-local-gitops-platform.md) |
| REQ-0004-FR-0010 | Ingress reference, 리소스 종류, GitOps 구조, policy, 비밀정보 동기화와 명시적 local-only transport 예외를 fail-closed로 검사해야 한다. 충족 여부를 해당 owner의 정적 검증과 별도 관측 증거로 판정한다. | [AD-0007](../02.architecture/descriptions/0007-current-local-gitops-platform.md) |
| REQ-0004-FR-0011 | 플랫폼 assurance 작업은 순서가 있는 package별 검토·검증·rollback 단위로 수행하고 최종 local-only integration을 증명해야 한다. 충족 여부를 해당 owner의 정적 검증과 별도 관측 증거로 판정한다. | [AD-0007](../02.architecture/descriptions/0007-current-local-gitops-platform.md) |
| REQ-0004-FR-0012 | 정확한 infrastructure·workflow·dependency·example 버전은 실행 소스 또는 검토된 lock에서 확인하고 Reference mirror를 실행 선행조건으로 요구하지 않아야 한다. 충족 여부를 해당 owner의 정적 검증과 별도 관측 증거로 판정한다. | [AD-0007](../02.architecture/descriptions/0007-current-local-gitops-platform.md) |
| REQ-0004-FR-0013 | 자기 저장소의 지속 조정 source와 외부 배포 source의 revision 정책을 구분하고 다중 운영자·환경 또는 history rewrite 도입 때 재검토해야 한다. 충족 여부를 해당 owner의 정적 검증과 별도 관측 증거로 판정한다. | [AD-0007](../02.architecture/descriptions/0007-current-local-gitops-platform.md) |
| REQ-0004-FR-0014 | Pod security 강제 수준은 저장소가 소유하고 정적으로 검증한 workload 근거에 비례해야 한다. Chart·injection·runtime 불확실성은 audit/warn으로 구분하고 CNI desired state를 live 증거로 승격하지 않는다. 충족 여부를 해당 owner의 정적 검증과 별도 관측 증거로 판정한다. | [AD-0007](../02.architecture/descriptions/0007-current-local-gitops-platform.md) |
| REQ-0004-NFR-0001 | 로컬 플랫폼은 인증서, ingress, service mesh, 관측 UI, 점진적 배포, 알림, monitoring 및 외부 비밀정보 연동의 현재 통합 범위를 제공해야 한다. 충족 여부를 해당 owner의 정적 검증과 별도 관측 증거로 판정한다. | [AD-0007](../02.architecture/descriptions/0007-current-local-gitops-platform.md) |
| REQ-0004-NFR-0002 | Secret value, token 및 private key는 Git, 문서 또는 로그에 기록하지 않아야 한다. 충족 여부를 해당 owner의 정적 검증과 별도 관측 증거로 판정한다. | [AD-0007](../02.architecture/descriptions/0007-current-local-gitops-platform.md) |
| REQ-0004-NFR-0003 | Image와 artifact assurance는 fail-closed로 유지하되 검증 없는 일괄 digest 전환은 하지 않고 후속 provenance 의무는 consumer·owner·trigger로 명시해야 한다. 충족 여부를 해당 owner의 정적 검증과 별도 관측 증거로 판정한다. | [AD-0007](../02.architecture/descriptions/0007-current-local-gitops-platform.md) |
| REQ-0004-IF-0001 | 과거 기록은 current 실행 권위와 분리해야 한다. 완료 package의 명시적 역사 인용은 허용하되 봉인 record를 현재 구현 지침으로 사용하지 않는다. 충족 여부를 해당 owner의 정적 검증과 별도 관측 증거로 판정한다. | [AD-0007](../02.architecture/descriptions/0007-current-local-gitops-platform.md) |

### Reviewed member-ID transfer

아래는 현재 의미의 승계표다. 이전 member ID는 원래 결정·프로그램의 이력 식별자이며 재할당되지 않는다.

| Original member ID | Current semantic owner |
| --- | --- |
| REQ-0007-FR-0001 | REQ-0004-FR-0005 |
| REQ-0007-FR-0002 | REQ-0004-FR-0006 |
| REQ-0007-FR-0003 | REQ-0004-FR-0007 / REQ-0003-FR-0016 |
| REQ-0007-FR-0004 | REQ-0003-FR-0017 |
| REQ-0007-FR-0005 | REQ-0004-FR-0008 |
| REQ-0007-FR-0006 | REQ-0004-FR-0010 |
| REQ-0007-FR-0007 | REQ-0004-FR-0009 |
| REQ-0007-FR-0008 | REQ-0003-FR-0028 |
| REQ-0007-FR-0009 | REQ-0003-FR-0007 |
| REQ-0007-FR-0010 | REQ-0004-FR-0011 / REQ-0003-FR-0018 / REQ-0003-FR-0019 |
| REQ-0007-FR-0011 | REQ-0004-FR-0012 |
| REQ-0007-FR-0012 | REQ-0004-FR-0013 |
| REQ-0007-FR-0013 | REQ-0004-FR-0014 |
| REQ-0007-NFR-0001 | REQ-0004-NFR-0003 |
| REQ-0007-NFR-0002 | REQ-0003-FR-0014 |

REQ-0005-FR-0006의 예제와 실행 소스 인접성은 REQ-0004-FR-0009가 함께 승계한다.

- Current architecture: [AD-0007](../02.architecture/descriptions/0007-current-local-gitops-platform.md).
- Platform implementation: [Spec 0008](../03.specs/0008-current-local-gitops-platform/spec.md).
- Shared architecture: [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md).
- Current self-source and namespace decisions remain in the [decision log](../02.architecture/decisions/README.md).
