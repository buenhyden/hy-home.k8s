---
title: "02.architecture"
version: "0.9.0"
type: "common/readme"
status: "active"
owner: "platform"
updated: "2026-11-13"
---
# 02.architecture

## Stage Responsibility

### Purpose and Readers

> 요구사항을 아키텍처 요구와 결정 기록으로 연결하는 canonical architecture stage다.

`02.architecture/`는 요구사항을 시스템 구조와 의사결정으로 연결하는 아키텍처 허브다.
Architecture Description은 `descriptions/`에, 결정 기록은 `decisions/`에 둔다.

이 stage는 현재 구조와 결정을 보존한다. 현재 repo-backed 실행계약은
[`gitops/`](../../gitops/), [`scripts/validate-infrastructure-contracts.sh`](../../scripts/validate-infrastructure-contracts.sh),
정적 검증 스크립트가 우선한다. ADR을 포함해 더 이상 현재가 아닌 문서는 current consumer와 의미를
승계한 뒤 이 stage를 떠난다. Architecture Description의 Archived Lineage 표에 요약하고 [문서 수명주기 정책](../../.agents/governance/document-lifecycle.md)에 따른 처분 전 확인을 거쳐 삭제한다. 원본은 확인된 Git 이력에서 복구한다([ADR-0053](./decisions/0053-unvalidated-archive.md)). Stage 98은
검증하지 않는 기록 보관소이며 현재 실행 권위가 아니다.

#### Stage Readers

- Platform Engineers
- GitOps Operators
- Architecture Reviewers

### Inputs and Outputs

#### In Scope

- 시스템 경계, 품질 속성, 배포 구조, 데이터/인프라 관점의 요구사항
- 선택지, 결정 근거, 결과를 남기는 Architecture Decision Record
- Requirement Package, Spec, Plan, Operations 문서로 이어지는 추적 링크

#### Out of Scope

- 제품 요구사항 원문
- 파일 단위 구현 명세
- 실행 순서와 작업 증적
- 반복 운영 절차

## Contents

### Current Items

| Path | Purpose |
| --- | --- |
| [descriptions/](./descriptions/) | Architecture Description과 참조 모델 |
| [decisions/](./decisions/) | 아키텍처 결정 기록(ADR) |
| [AGENTS.md](./AGENTS.md) | 이 stage에 적용되는 AI 에이전트 지시 |
| [CLAUDE.md](./CLAUDE.md) | Claude가 이 stage의 `AGENTS.md`를 불러오게 하는 한 줄 `@AGENTS.md` import |

### Classification

#### Reader Route

| 찾는 것 | 먼저 볼 위치 | 판단 기준 |
| --- | --- | --- |
| 현재 외부 서비스 host 주소·gateway hostname, Headlamp, network policy 계약 | [`gitops/platform/external-services/`](../../gitops/platform/external-services/), [`gitops/platform/network-policies/`](../../gitops/platform/network-policies/), [`validate-infrastructure-contracts.sh`](../../scripts/validate-infrastructure-contracts.sh) | 현재 desired state와 정적 계약 검증이 우선한다. |
| 시스템 경계와 품질 속성 | [`descriptions/`](./descriptions/) | AD는 Requirement Package를 현재 구조와 참조 모델로 해석한다. |
| 기술 선택과 현재 decision record | [`decisions/`](./decisions/) | ADR은 현재 구현 기준의 결정, 대안, 결과를 보존한다. |
| 구현자가 따라야 할 계약 | [`../03.specs/`](../03.specs/) | 파일/manifest/API 수준 상세 설계는 Spec stage가 소유한다. |
| 운영 정책과 복구 절차 | [`../05.operations/`](../05.operations/) | 실행 절차, 정책, runbook은 Operations stage가 소유한다. |

## Workflow

### Create and Review

1. 요구사항을 시스템 경계와 품질 속성으로 확장할 때는 `descriptions/`를 갱신한다.
2. 기술 선택이나 운영 모델 결정은 `decisions/`에 ADR로 기록한다.
3. AD target은 `docs/02.architecture/descriptions/####-<system-or-domain>.md`, ADR target은 `docs/02.architecture/decisions/####-<short-title>.md`를 따른다. 유형은 부모 폴더가 결정하고 안정 ID는 frontmatter의 `AD-####`/`ADR-####`로 유지한다.
4. 구현자가 따라야 할 상세 계약은 `../03.specs/`로 넘긴다.
5. 운영 정책이나 복구 절차는 `../05.operations/`로 넘긴다.
6. Architecture Description에는 arc42의 목적별 구조를 비례적으로 적용하고,
   C4 System Context/Container를 우선 검토한다. Component·Dynamic·Deployment
   view는 실제 이해 가치가 있을 때만 사용하며, Kubernetes manifest와 GitOps
   desired state를 문서 본문에 복제하지 않는다.

#### Relative Link Rules

이 README의 링크 기준 위치는 `docs/02.architecture/`다.

- 하위 아키텍처 폴더는 `./descriptions/`, `./decisions/`로 연결한다.
- 인접 stage는 `../01.requirements/`, `../03.specs/`, `../05.operations/`로 연결한다.
- root-level 구현 경로는 `../../gitops/`, `../../infrastructure/`처럼 repository root 기준으로 올라간다.
- AD/ADR 문서 안의 링크는 각 하위 폴더의 최종 문서 위치 기준으로 다시 계산한다.
- AD는 자신이 다루는 Requirement의 각 member를 `Lifecycle Traceability`의 `Upstream requirement` 열에서 인용한다. Requirement는 downstream 링크 열을 두지 않으며, 인용되지 않은 member는 `REQUIREMENT-COVERAGE` 검사가 거부한다.

### Transition and Exit

1. ADR 전체를 대체할 때는 후속 ADR의 `supersedes`와 Traceability가 이전 ID를 유지하고 AD Archived Lineage가 요약한다. 삭제 전에는 [문서 수명주기 정책](../../.agents/governance/document-lifecycle.md)의 처분 조건을 확인한다. 일부 조항만 개정할 때는 기존 ADR을 보존하고 후속 ADR의 Traceability에 개정 범위를 적는다.

## Related Documents

### Upstream and Downstream

- [Requirements README](../01.requirements/README.md)
- [Architecture Descriptions](./descriptions/README.md)
- [Architecture Decisions](./decisions/README.md)
- [Specs README](../03.specs/README.md)
- [Operations README](../05.operations/README.md)
- [Archive Index](../98.archive/README.md)

### Policy and Templates

- [Document Stage Routing](../../.agents/governance/document-authoring.md)
- [Templates README](../99.templates/README.md)
