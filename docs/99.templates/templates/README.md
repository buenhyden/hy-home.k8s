---
title: "99.templates/templates"
version: "0.6.1"
type: "common/readme"
status: "active"
owner: "platform"
updated: "2026-11-13"
layer: "templates"
---

# 99.templates/templates

## Stage Responsibility

### Purpose and Readers

이 디렉터리는 저장소가 인정하는 모든 authored 문서의 physical form을 담는다.
Form directory는 navigation을 위해 physical responsibility surface별로 묶고,
파일 이름은 그 form이 만드는 문서 kind를 말한다. Directory 이름은 Registry profile
family를 정의하지 않는다. 예를 들어 `specs/plan.template.md`는 `sdlc/plan`
profile의 form이다. Form은 계약을 정의하지 않는다. 계약은
[registry](../registry.json)와 [frontmatter schema](../contracts/frontmatter.schema.json)가
소유하고, form은 그 계약을 저자가 채울 수 있는 모양으로 보여줄 뿐이다.

### Inputs and Outputs

#### In Scope

- 각 profile이 소유하는 physical form 파일
- 저자가 채워야 할 값의 placeholder와 author prompt

#### Out of Scope

- profile 선택 규칙, key 문법, lifecycle 상태 (registry와 schema가 소유)
- 완성된 문서의 예시나 사본
- form 디렉터리별 README (이 카탈로그 하나만 둔다)

## Contents

### Current Items

| Path | Purpose |
| --- | --- |
| [architecture/](./architecture/) | decision, description |
| [common/](./common/) | repository, stage-index, collection-index, implementation, workspace-staging, runtime-governance entrypoint README form |
| [governance/](./governance/) | contract, knowledge, prompt, provider, role, rule, skill, vocabulary |
| [evaluations/](./evaluations/) | evaluation-task.template.md, evaluation-score.template.md, evaluation-results.template.md |
| [operations/](./operations/) | guide, incident, policy, postmortem, runbook |
| [references/](./references/) | audit·data·research 의 pack form과 reference form |
| [requirements/](./requirements/) | requirement-package |
| [runtime/](./runtime/) | claude-agent (Markdown), claude-command (Markdown), codex-agent (TOML) |
| [specs/](./specs/) | spec, plan, task |

### Classification

이 README는 분류 표를 따로 두지 않는다. 분류 표를 두게 되면 여기에 둔다.

## Workflow

### Create and Review

1. 만들려는 문서의 경로로 [registry](../registry.json)에서 profile을 하나만
   해석하고, 그 profile이 지정한 form을 읽는다.
2. 새 form은 그 form이 만드는 문서 이름으로 짓고, 기존 physical responsibility
   grouping에 두며, 디렉터리 이름을 파일 이름에 반복하지 않는다. Profile family와
   form 경로의 대응은 Registry에 명시한다.
3. 새 form은 Registry의 "template_source"와
   "relationships.source_profile_ids"에 명시적으로 연결한다. source가 없는
   required form, 소유 profile이 없는 form, 암묵적 공유 form은 계약 위반이다.
   native Codex TOML을 제외한 각 form에는 `mode: template`인 `common/template-*`
   profile이 하나씩 있으며, 그 profile이 원본 profile을 source로 가리킨다.
4. 확장자는 그 form을 읽는 런타임이 읽는 확장자를 쓴다.

### Transition and Exit

이 README는 상태, 승격, 종료 규칙을 따로 두지 않는다. 그런 규칙을 두게 되면 여기에 적는다.

## Related Documents

### Upstream and Downstream

- [Stage 99 README](../README.md)

### Policy and Templates

- [Document Profile Registry](../registry.json)
- [Frontmatter Schema](../contracts/frontmatter.schema.json)
- [Document Authoring Policy](../../../.agents/governance/document-authoring.md)
