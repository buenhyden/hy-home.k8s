---
title: "99.templates/templates"
version: "0.1.0"
type: "common/readme-collection-index"
status: "active"
owner: "platform"
updated: "2026-09-06"
layer: "templates"
---
# 99.templates/templates

## Overview

이 디렉터리는 저장소가 인정하는 모든 authored 문서의 physical form을 담는다.
Form directory 이름은 그 form을 소유하는 책임 family를, 파일 이름은 그 form이 만드는
문서 kind를 말한다. Form은 계약을 정의하지 않는다. 계약은
[registry](../registry.json)와 [frontmatter schema](../contracts/frontmatter.schema.json)가
소유하고, form은 그 계약을 저자가 채울 수 있는 모양으로 보여줄 뿐이다.

## Scope

### In Scope

- 각 profile이 소유하는 physical form 파일
- 저자가 채워야 할 값의 placeholder와 author prompt

### Out of Scope

- profile 선택 규칙, key 문법, lifecycle 상태 (registry와 schema가 소유)
- 완성된 문서의 예시나 사본
- form 디렉터리별 README (이 카탈로그 하나만 둔다)

## Item Index

```text
templates/
├── architecture/   decision, description
├── archive/        migration, tombstone
├── common/         repository, documentation·stage, package, runtime-governance entrypoint README form
├── governance/     contract, provider, role, rule, skill
├── operations/     guide, incident, policy, postmortem, runbook
├── references/     audit·data·research 의 pack form과 reference form
├── requirements/   requirement-package
├── runtime/        claude-agent (Markdown), codex-agent (TOML)
└── specs/          spec, plan, task
```

## Add and Find

1. 만들려는 문서의 경로로 [registry](../registry.json)에서 profile을 하나만
   해석하고, 그 profile이 지정한 form을 읽는다.
2. 새 form은 그 form이 만드는 문서 이름으로 짓고, 소유 family 디렉터리에 두며,
   디렉터리 이름을 파일 이름에 반복하지 않는다.
3. 새 form은 Registry의 "template_source"와
   "relationships.source_profile_ids"에 명시적으로 연결한다. source가 없는
   required form, 소유 profile이 없는 form, 암묵적 공유 form은 계약 위반이다.
4. 확장자는 그 form을 읽는 런타임이 읽는 확장자를 쓴다.

## Related Documents

- [Stage 99 README](../README.md)
- [Document Profile Registry](../registry.json)
- [Frontmatter Schema](../contracts/frontmatter.schema.json)
- [Document Authoring Policy](../../../.agents/governance/document-authoring.md)
