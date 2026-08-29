# 99.templates

> repo-authored 문서와 README가 시작해야 하는 canonical template stage다.

> [!NOTE]
> All AI agent interactions with this stage must comply with the [Agent Governance Hub](../00.agent-governance/README.md).

## Overview

이 경로는 문서 작성에 쓰는 form과 그 form을 설명하는 support contract를
분리한다. 정확한 경로, profile, frontmatter, 상태, heading, template 연결은
[Document Profile Registry](./registry.json)와
[Route and Corpus Contract](./contracts/route-contract.json)가 나누어 소유한다.
README는 해당 machine contract를 복제하지 않고 사람이 올바른 소유자를 찾도록
안내한다.

## Stage Contract

### Responsibility Boundary

| Surface | Role | Canonical owner |
| --- | --- | --- |
| Machine contract | 경로를 정확히 하나의 profile과 form으로 분류하고 검증한다. | [Document Profile Registry](./registry.json) |
| Support | 역할, 수명주기, metadata, 선택 절차, legacy 정리의 이유와 방법을 설명한다. | [`support/`](./support/README.md) |
| Forms | 작성자가 복사한 뒤 topic-specific 사실과 증거로 채우는 최소 구조를 제공한다. | [`templates/`](./templates/README.md) |
| Authored documents | 요구, 결정, 명세, 실행, 운영, 참조, 보존 증거를 소유한다. | `docs/01.requirements`부터 `docs/05.operations`, `docs/90.references`, `docs/98.archive` |

이 stage는 실제 PRD, AD, ADR, Spec, Plan, Task, 운영 기록이나 기능별 구현
계약을 소유하지 않는다. Form에는 재사용 가능한 구조만 두고, 공통 규칙은 support
또는 Stage 00 governance로 돌려보낸다.

### Form Family Inventory

- **Common forms**: README profile, governance reference, durable reference,
  archive record, archive migration control, memory, progress entry를 위한
  Markdown form이다.
- **Core SDLC forms**: PRD, optional SRS, optional Interface Requirement, AD,
  ADR, Spec, Plan, Task의 단계별 책임과
  handoff를 기록한다.
- **Spec helper and native forms**: API, agent, data model, test 보조 문서와
  OpenAPI, GraphQL, protobuf 계약을 feature Spec 아래에 둔다.
- **Operations forms**: Guide, Policy, Runbook, Incident, Postmortem의 서로 다른
  운영 증거 책임을 유지한다.

현재 physical form의 전체 목록과 각각의 소유 profile은 README가 아니라 registry와
repository quality gate에서 계산한다. `memory.template.md`와
`progress.template.md`는 `00.agent-governance/memory/`의 서로 다른 memory와
progress 책임을 지원한다.

## Document Index

```text
99.templates/
├── contracts/          # machine contracts and their schemas
│   ├── document-profile.schema.json
│   ├── frontmatter.schema.json
│   ├── registry-form.schema.json
│   ├── route-contract.json
│   └── route-contract.schema.json
├── support/            # rationale, procedure, cleanup
│   └── *.md
├── templates/          # copyable forms only
│   ├── common/
│   └── sdlc/
├── registry.json
└── README.md
```

- [Document Profile Registry](./registry.json)
- [Route and Corpus Contract](./contracts/route-contract.json)
- [Template Support Contracts](./support/README.md)
- [Template Forms](./templates/README.md)
- [Document Contract](./support/document-contract.md)
- [Document Lifecycle](./support/document-lifecycle.md)

## Authoring Workflow

1. **Classify**: repository-relative target path를 registry로 분류하고 정확히 하나의
   profile이 선택되는지 확인한다.
2. **Copy**: 선택된 profile의 canonical form을 복사한다. 이웃 파일명이나 README
   목록으로 form을 추측하지 않는다.
3. **Author**: 모든 prompt와 placeholder를 제거하고, 각 section을 문서의 topic에
   맞는 조사 결과, 결정, 링크, 검증 증거로 채운다. 상대 링크는 최종 target
   위치에서 다시 계산한다.
4. **Validate**: registry, Markdown profile, link/owner 검증과 repository quality
   gate를 실행하고 repo-static 결과와 remote/live 결과를 구분해 기록한다.

Template 선택, form/body/frontmatter rationale은 [Document
Contract](./support/document-contract.md)를 따르고, lifecycle·supersession·retention·archive
및 legacy disposition은 [Document Lifecycle](./support/document-lifecycle.md)을 따른다.
README는 frontmatter-free이며 선택된 README profile의 heading contract만 따른다.

## Related Documents

- [Docs README](../README.md)
- [Agent Governance Hub](../00.agent-governance/README.md)
- [Document Authoring Policy](../00.agent-governance/rules/document-authoring.md)
- [Template Support Contracts](./support/README.md)
