# 90.references

> 느리게 변하는 기준 지식, 외부 공식 스냅샷, 버전 인벤토리, Agent 학습 자료를 관리한다.

> [!NOTE]
> All AI agent interactions with this stage must comply with the [Agent Governance Hub](../00.agent-governance/README.md).

## Overview

이 경로는 `hy-home.k8s`의 요구사항, 아키텍처 결정, 구현 계약, 운영 절차를 직접 대체하지 않는 durable reference 영역이다. 공식 문서 링크, 기술 버전 인벤토리, 외부 기준 스냅샷, Agent 관련 개념, 학습 로드맵처럼 여러 stage에서 재사용되는 lookup material을 둔다.

진행 중인 요구사항, 의사결정, 실행 계획, 운영 절차는 각각 `01.requirements`부터 `05.operations/runbooks`까지의 canonical stage로 라우팅한다.

`90.references`는 사실과 기준값을 보존하는 곳이다. 단, 이 폴더의 문서가 실행 명령, 배포 승인, live cluster 변경 절차, agent runtime policy를 새로 정의해서는 안 된다.

## Audience

이 README의 주요 독자:

- Developers
- Operators
- Documentation Writers
- AI Agents

## Scope

### In Scope

- 느리게 변하는 외부 기술 기준과 공식 링크
- repo-backed 버전 인벤토리와 cloud example snapshot
- Agent 관련 참고 개념과 학습 자료
- 다른 stage 문서가 참조하는 glossary/standard/lookup material
- 특정 날짜에 확인한 외부 공식 지원 범위와 source checked metadata

### Out of Scope

- 현재 진행 중인 설계 의사결정
- 실행 계획이나 작업 증적
- 운영 절차와 장애 대응 체크리스트
- agent runtime policy의 원본 규칙
- live cluster mutation, Vault writes, deployment approval, release gate 자체

## Structure

```text
docs/90.references/
├── audits/                              # Dated implementation audit snapshots and report index
├── data/                                # Repo-backed inventories, durable catalogs, factual lookup data
├── learning/                            # 학습 로드맵과 이론 연결 자료
├── llm-wiki/                            # LLM-readable generated Markdown link map
├── research/                            # Dated workspace engineering research pack references and source ledgers
└── README.md                            # This file
```

### Reference Index

| 문서 | Reference Type | 역할 | Freshness 기준 |
| --- | --- | --- | --- |
| [data/README.md](./data/README.md) | data reference index | repo-backed inventories, durable catalogs, factual lookup data의 범위와 라우팅 | data reference 문서 추가/이동, category role 변경 시 |
| [data/agent-reference-index.md](./data/agent-reference-index.md) | durable-concept / data-catalog | Agent reference data의 범위와 canonical owner routing | Agent reference 문서 추가/이동, runtime roster 이동, Stage 00 routing 변경 시 |
| [data/tech-stack-version-inventory.md](./data/tech-stack-version-inventory.md) | version-contract-inventory / external-standard-snapshot | repo-backed 버전 기준과 cloud example snapshot | manifest/config/example version 변경 또는 외부 공식 지원 범위 변경 |
| [llm-wiki/README.md](./llm-wiki/README.md) | durable-concept / faq | LLM WIKI boundary and canonical owner link map | docs/examples taxonomy, Agent governance routing, or version inventory path 변경 시 |
| [llm-wiki/wiki-index.md](./llm-wiki/wiki-index.md) | durable-concept / faq | Generated LLM-readable canonical owner index | generator, runtime roster, docs/examples taxonomy, or canonical owner path 변경 시 |
| [learning/infrastructure-to-theory-roadmap.md](./learning/infrastructure-to-theory-roadmap.md) | learning-roadmap | 인프라 구현 경험과 CS/CE 이론 연결 | 학습 자료나 repo 구현 축이 크게 바뀔 때 |
| [audits/README.md](./audits/README.md) | durable-concept index / audit snapshot index | dated implementation audit reports, status vocabulary, evidence rules, and static-vs-live boundary | audit report 추가/이동, status vocabulary 변경, evidence rule 변경 시 |
| [learning/README.md](./learning/README.md) | learning-roadmap index | learning reference 하위 폴더의 범위와 라우팅 | learning reference 문서 추가/이동 시 |
| [research/README.md](./research/README.md) | durable-concept index / source-ledger index | dated workspace engineering research pack 하위 폴더의 범위, source priority, planned/current reference structure | research reference 문서 추가/이동, source priority 변경, parent spec/plan 변경 시 |

## How to Work in This Area

1. 새 참고 자료가 정책/계약/절차를 정의하는지 확인한다. 그렇다면 `00.agent-governance`, `03.specs`, `05.operations/policies`, `05.operations/runbooks`로 라우팅한다.
2. 버전 기준을 갱신할 때는 실제 manifest/config/example code와 [tech-stack-version-inventory.md](./data/tech-stack-version-inventory.md)를 같은 변경에서 맞춘다.
3. 외부 공식 기준은 확인일을 명시하고 링크를 남긴다.
4. 새 파일을 만들 경우 [reference template](../99.templates/templates/common/reference.template.md)을 사용하고 이 README 인덱스를 갱신한다. canonical target pattern은 `docs/90.references/<category>/<topic>.md`다. `llm-wiki/wiki-index.md`는 `scripts/generate-llm-wiki-index.sh`로만 갱신한다.
5. 모든 reference 문서는 `Reference Type`, `Authority Boundary`, `Review and Freshness`를 포함해야 한다.

## Link Basis

이 README의 링크 기준 위치는 `docs/90.references/`다.

- 하위 reference folder는 `./audits/`, `./data/`, `./learning/`, `./llm-wiki/`, `./research/`로 연결한다.
- consumer stage는 `../01.requirements/`, `../02.architecture/`, `../03.specs/`, `../04.execution/`, `../05.operations/`로 연결한다.
- root-level source file은 이 README 기준으로 `../../<path>`를 사용한다.
- 새 reference 문서 안의 링크는 최종 reference 파일 위치 기준으로 다시 계산하고, optional target은 code literal로 남긴다.

## Role and Authority Boundary

`90.references`의 역할은 다음 다섯 가지다.

| 역할 | 설명 | 예시 | 소유하지 않는 것 |
| --- | --- | --- | --- |
| Durable concept reference | 여러 stage가 반복 참조하는 느리게 변하는 개념을 설명한다. | glossary, Agent 개념, 학습 로드맵 | 기능별 설계, 실행 계획 |
| Data reference inventory | repo-backed manifest/config와 함께 검증되는 버전 기준, durable catalog, factual lookup data를 모은다. | k3s image, Helm chart, GitHub Actions pin, Agent reference catalog | 실제 upgrade 실행 절차, runtime policy |
| External standard snapshot | 특정 날짜에 확인한 외부 공식 지원 범위를 기록한다. | EKS/AKS 지원 버전, upstream retirement notice | cloud live deployment 지침 |
| Learning/reference roadmap | 구현 경험을 이론 학습 자료와 연결한다. | infrastructure-to-theory roadmap | 운영 runbook, incident response |
| Dated implementation audit snapshot | 특정 날짜의 local implementation status와 repo-backed evidence를 요약한다. | workspace harness implementation audit | active policy, plans, tasks, runbooks, CI semantics, live runtime readiness |

권한 경계는 다음과 같다.

- `90.references`는 factual lookup과 dated snapshot의 SSoT다.
- 제품 요구는 `01.requirements`, 아키텍처 요구/결정은 `02.architecture`, 구현 계약은 `03.specs`, 실행 계획/작업 증적은 `04.execution`, 운영 지식은 `05.operations`가 SSoT다.
- `90.references/data/tech-stack-version-inventory.md`의 버전 값은 실제 repo manifest/config와 함께 유지될 때만 기준값으로 취급한다.
- 외부 기준은 시간에 따라 바뀌므로 `Source checked`, `Last reviewed`, refresh trigger를 남긴다.
- Audit snapshot은 checked-date 기준 implementation evidence를 요약할 뿐이며 active policy, plans, tasks, runbooks, CI semantics, live runtime readiness를 소유하지 않는다.

## Reference Folder Roles

`90.references` 하위 폴더의 목적은 다음처럼 나눈다.

| Folder | Role | Language Boundary |
| --- | --- | --- |
| `audits/` | dated implementation audit snapshot, local evidence comparison, status vocabulary, and follow-up routing | 사람용 설명은 한국어 가능, audit status, evidence boundary, and static-vs-live limitation은 영어-first |
| `data/` | repo-backed version contracts, durable Agent reference catalog boundaries, and factual lookup tables | 사람용 설명은 한국어 가능, source-checked values, freshness triggers, and canonical owner boundaries는 영어-first |
| `learning/` | 구현 경험을 CS/CE 이론과 장기 학습 로드맵으로 연결하는 자료 | 학습 맥락은 한국어 가능, authoritative boundary와 freshness rule은 영어로 유지 |
| `llm-wiki/` | LLM-readable canonical owner link map과 generated index | 링크맵 설명은 혼합 가능, generated content와 canonical owner boundary는 영어-first |
| `research/` | Dated workspace engineering research pack reference, source ledger, source priority를 관리하는 자료 | 사람용 설명은 한국어 가능, source authority와 non-authoritative market scan boundary는 영어-first |

## Language Boundary

`90.references`는 사람이 먼저 읽는 reference hub이므로 README와 개요 문장은
한국어를 사용할 수 있다. 다만 reference 문서가 AI Agent나 자동화가 판단 기준으로
읽는 `Reference Type`, `Authority Boundary`, `Sources`, `Review and Freshness`,
generated-index contract, version support boundary를 포함할 때는 해당 필드를
영어-first로 유지한다.

Reference 문서는 정책, 실행 절차, 배포 승인, runtime permission을 새로 정의하지
않는다. 그런 내용이 필요하면 `00.agent-governance`, `03.specs`,
`04.execution`, `05.operations/policies`, `05.operations/runbooks` 중 canonical
owner로 이동하고, `90.references`에는 dated source, lookup fact, freshness
trigger만 남긴다.

## Required Reference Format

새 reference 문서는 [reference.template.md](../99.templates/templates/common/reference.template.md)의 필수 heading을 유지한다.
`README.md` 인덱스 파일은 탐색 진입점이므로 전체 reference 템플릿을 복제하지 않고 필요한 필드의 요약만 둘 수 있다.
README 인덱스는 frontmatter를 요구하지 않지만, authored reference 문서는 `title`, `type`, `status`, `owner`, `updated` metadata를 유지한다.

- `Overview`: 이 reference가 무엇을 설명하는지 한국어로 요약. AI-agent-only reference라면 `Overview`로 영어 작성 가능.
- `Purpose`: 이 reference가 존재하는 이유
- `Reference Type`: version-contract-inventory, external-standard-snapshot, durable-concept, learning-roadmap, glossary, faq 중 하나
- `Authority Boundary`: authoritative for / not authoritative for
- `Scope`: 포함/제외 범위
- `Definitions / Facts`: 재사용 가능한 사실, 용어, 기준값
- `Sources`: 공식 또는 repo-backed source
- `Review and Freshness`: 검토 주기, 마지막 검토일, 갱신 trigger
- `Related Documents`: 이 reference를 소비하는 stage 문서

## Related Documents

- [Docs README](../README.md)
- [Agent Governance Hub](../00.agent-governance/README.md)
- [Templates README](../99.templates/README.md)
- [Audit Reference README](./audits/README.md)
- [Research Reference README](./research/README.md)
- [Tech Stack Version Inventory](./data/tech-stack-version-inventory.md)
- [Reference Maintenance Runbook](../05.operations/runbooks/0011-reference-maintenance-runbook.md)
