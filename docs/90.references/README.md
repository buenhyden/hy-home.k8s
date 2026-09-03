# 90.references

> 감사, 외부 조사, 데이터 등 비권위 참고 자료를 관리한다.

> [!NOTE]
> AI Agent가 이 Stage를 사용할 때는 [Agent Governance Hub](../00.agent-governance/README.md)를 따른다.

## Overview

`docs/90.references/`는 워크스페이스와 관련된 출처 기반 참고 자료를 둔다.
이 Stage는 요구사항, 아키텍처, 구현 명세, 운영 절차, Agent 정책을 정의하거나
대체하지 않는다. 현재 실행 동작과 버전 값은 Stage 01/02 문서 및 실제
매니페스트·설정·잠금 파일이 소유한다.

## Stage Contract

### In Scope

| Category | Purpose | Required boundary |
| --- | --- | --- |
| Audit | 특정 시점의 저장소 상태를 출처와 함께 비교한 비권위 감사 | 관찰일, 범위, 증거, 미확인 항목을 명시한다. |
| Research | 외부 공식 자료와 저장소 증거를 종합한 조사 | 출처, 확인일, freshness trigger, 추론 한계를 명시한다. |
| Data | 독립적인 참고 가치가 있는 bounded dataset 또는 lookup material | 생성·수집 출처와 갱신 책임을 명시하고 실행 입력으로 승격하지 않는다. |

### Out of Scope

- AI Agent governance, role, skill, provider, permission, runtime policy
- 제품 요구사항, 현재 아키텍처, 구현 계약, 실행 Task 증거
- 운영 Guide, Policy, Runbook, Incident, Postmortem
- 배포 승인, live mutation, secret-bearing procedure
- 매니페스트·설정·잠금 파일을 복제한 현재 버전 인벤토리
- generated wiki, redirect, 이전 본문 복제본, 영구 corpus census
- `audits/`, `data/`, `research/` 밖의 느슨한 authored reference

Stage 90 자료는 현재 Stage 00/01/02/03/05 owner를 인용할 수 있지만,
Stage 98의 문서나 파일을 인용하거나 cross-link하지 않는다. 삭제된 자료의
전체 본문 복구는 Git history가 담당한다.

## Document Index

```text
docs/90.references/
├── audits/
│   └── README.md                      # Audit collection router
├── data/
│   └── README.md                      # Data collection router
├── research/
│   ├── 0001-workspace-engineering/   # 보존된 최신 외부 조사 pack
│   └── README.md                      # Research collection router
└── README.md                          # Stage router
```

세 collection은 동일한 3단 구조를 따른다: collection router `README.md`,
pack router `####-<slug>/README.md`, 그리고 pack member `####-<slug>/m####-<slug>.md`.
현재 pack을 보유한 collection이 Research뿐인 것은 현재 처분 결과일 뿐이며, 고유
목적과 출처 경계를 갖춘 Audit 또는 Data pack의 추가를 금지하지 않는다.

## Authoring Workflow

1. 새 자료가 정책·요구·설계·절차·실행 증거를 정의하는지 확인하고, 그렇다면
   Stage 00/01/02/03/05의 canonical owner에 작성한다.
2. Reference로 유지할 자료는 고유 목적, provenance, observation date,
   authority boundary, freshness trigger, 현재 consumer를 확인한다.
3. 현재 pack은 `audits/####-<slug>/`, `data/####-<slug>/`,
   `research/####-<slug>/` 중 하나에만 둔다. `####`는 category 안에서 고유한
   네 자리 번호이고 `<slug>`는 날짜가 아닌 의미 기반 kebab-case 이름이다.
4. pack `README.md`는 category와 일치하는
   [Audit](../99.templates/templates/references/audit-pack.template.md),
   [Data](../99.templates/templates/references/data-pack.template.md), 또는
   [Research](../99.templates/templates/references/research-pack.template.md)
   template을 사용한다. 내부 report는 같은 family의
   [Audit Reference](../99.templates/templates/references/audit.template.md),
   [Data Reference](../99.templates/templates/references/data.template.md),
   [Research Reference](../99.templates/templates/references/research.template.md)
   template을 사용한다. 관찰일은 frontmatter 또는 source metadata에만 둔다.
5. 이 router와 category router를 같은 변경에서 갱신한다.
6. 참조 자료를 실행 입력이나 중복 control plane으로 사용하지 않는다.
7. 다음 최소 검증을 실행한다.

   ```bash
   rtk python3 scripts/validate-document-contract-registry.py --root . --mode strict
   rtk python3 scripts/validate-markdown-profiles.py --root . --mode strict
   rtk python3 scripts/validate-links-and-owners.py --root . --mode strict
   rtk git diff --check
   ```

## Related Documents

- [Docs Hub](../README.md)
- [Agent Governance Hub](../00.agent-governance/README.md)
- [Requirements](../01.requirements/README.md)
- [Architecture](../02.architecture/README.md)
- [Specs](../03.specs/README.md)
- [Operations](../05.operations/README.md)
- [Research Collection](./research/README.md)
- [Research Reference Template](../99.templates/templates/references/research.template.md)
- [Reference Maintenance Runbook](../05.operations/runbooks/0011-reference-maintenance-runbook.md)
