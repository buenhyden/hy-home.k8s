# docs: 프로젝트 문서 허브

> 요구사항부터 운영·참조 자료까지의 canonical documentation taxonomy를 안내하는 진입점이다.

> [!NOTE]
> All AI agent interactions with this documentation suite must comply with the [Agent Governance Hub](./00.agent-governance/README.md).

## Overview

`docs/`는 `hy-home.k8s`의 요구사항, 아키텍처, 결정, 명세, 실행 계획, 작업 증적, 운영 절차, 사고 기록, 참조 자료, 템플릿을 연결하는 문서 SSoT다. 단순 기록 저장소가 아니라 k3d/GitOps 홈랩을 사람이 운영하고 AI Agent가 안전하게 협업하기 위한 추적 가능한 작업 체계다.

문서는 Spec-First 흐름을 따른다. 기획의 맥락은 설계와 결정으로 이어지고, 상세 명세와 실행 계획을 거쳐 작업 증적, 운영 지침, 런북, 사고 기록으로 연결된다.
AWS/Azure 예시와 외부 기술 버전 기준처럼 빠르게 변할 수 있는 참조값은 [90.references](./90.references/README.md)와 [tech-stack-version-inventory.md](./90.references/data/tech-stack-version-inventory.md)에 스냅샷 기준일과 함께 기록한다. LLM-readable 탐색용 링크맵은 [LLM WIKI Reference Index](./90.references/llm-wiki/README.md)와 [generated wiki index](./90.references/llm-wiki/wiki-index.md)를 사용하되, 정책과 절차의 정본은 각 canonical stage에 둔다.

## Audience

이 README의 주요 독자:

- Developers
- Operators
- Documentation Writers
- AI Agents

## Scope

### In Scope

- `00.agent-governance` 아래의 Agent 정책, 실행 규칙, workspace governance
- `01.requirements`부터 `05.operations/incidents`까지의 요구사항, 아키텍처, 결정, 명세, 계획, 작업, 가이드, 운영, 런북, 사고 기록
- `90.references` 아래의 사실 기반 참조 자료와 lookup material
- `98.archive` 아래의 old 문서 Tombstone과 중앙 archive index
- `99.templates` 아래의 승인된 문서 템플릿
- 각 stage README의 목적, 포함할 내용, 관련 폴더, 예시 안내

### Out of Scope

- 허용 목록에 없는 `docs/` top-level 폴더
- 임시 작업물, scratch 문서, 중복 템플릿
- GitOps manifests, bootstrap scripts, GitHub workflow 자체의 상세 설명
- live cluster 변경 절차를 대체하는 임의 문서

## Structure

```text
docs/
├── 00.agent-governance/   # Agent policies, execution rules, workspace governance
├── 01.requirements/       # Product and feature requirements
├── 02.architecture/
│   ├── requirements/      # Architecture requirements and reference model
│   └── decisions/         # Architecture decision records
├── 03.specs/              # Software, automation, and Agent design specifications
├── 04.execution/
│   ├── plans/             # Execution, rollout, and migration plans
│   └── tasks/             # Implementation and validation task lists
├── 05.operations/
│   ├── guides/            # Steady-state user/developer/operator guides
│   ├── policies/          # Shared operational policies and standards
│   ├── runbooks/          # Executable operational procedures
│   └── incidents/         # Incident records and postmortems
├── 90.references/         # Factual references and lookup material
├── 98.archive/            # Metadata-only Tombstones for old docs
├── 99.templates/          # Document templates
└── README.md              # This file
```

## How to Work in This Area

1. 새 문서를 만들기 전에 [Template Routing Contract](./99.templates/support/template-routing.md)에서 canonical target pattern과 template를 확인한다.
2. 새 문서는 matching template에서 시작하고 [99.templates](./99.templates/README.md)는 inventory summary로 사용한다.
3. 문서가 추가되거나 이동되면 해당 stage의 `README.md` 인덱스와 관련 링크를 같은 변경에서 갱신한다.
4. 사람 대상 README와 개요 문서는 한국어를 유지하고, `00.agent-governance` 정책 문서는 영어를 유지한다.
5. 사람 대상 문서 안에서도 `AI Agent Requirements`, `Agent Execution Notes`, tool/prompt contract처럼 AI Agent가 직접 따라야 하는 섹션은 영어를 우선한다.
6. README 파일은 frontmatter를 요구하지 않는다. README는 경로 목적, scope, structure, workflow, link basis, related documents를 설명하는 entrypoint다.
7. PRD/ARD/ADR/Spec/Plan/Task와 운영·참조 authored 문서는 matching template의 `title`, `type`, `status`, `owner`, `updated` metadata를 유지한다.
8. 템플릿이나 문서 lifecycle 규칙을 바꾸면 이 hub, 대상 stage README, [Template Routing Contract](./99.templates/support/template-routing.md), [99.templates README](./99.templates/README.md), 이미 생성된 문서의 안전한 구조 반영 여부를 함께 점검한다.
9. 일반 운영 변경은 GitOps-first 원칙을 따르며, 문서가 live `kubectl apply`나 외부 Vault 조작을 우회 절차처럼 안내하지 않도록 한다.
10. cloud example 버전을 갱신할 때는 코드, README, [tech-stack-version-inventory.md](./90.references/data/tech-stack-version-inventory.md)를 같은 변경에서 맞춘다.
11. 현재 구현과 상충하는 old 문서는 [`98.archive`](./98.archive/README.md)로 이동하고, 활성 문서는 archive index에만 연결한다.

## Link Basis

이 README의 링크 기준 위치는 `docs/`다.

- stage 링크는 `./<stage>/README.md`를 사용한다.
- root-level implementation 링크는 `../<path>/README.md`를 사용한다.
- nested stage README는 이 hub의 링크를 복사하지 않고, 자기 폴더 기준으로 상대 경로를 다시 계산한다.

## Stage Usage Criteria

모든 변경이 `01.requirements`부터 `05.operations/incidents`까지의 전체 체인을 요구하지는 않는다. 새 기능이나 플랫폼 변경은 영향도에 따라 필요한 stage만 작성하되, 요구사항, 설계 판단, 실행 증적, 운영 절차가 서로 추적 가능해야 한다.

- 제품 요구나 사용자 시나리오가 바뀌면 `01.requirements`를 갱신한다.
- 아키텍처 모델이나 품질 속성이 바뀌면 `02.architecture/requirements`를, 선택지와 결정 근거가 바뀌면 `02.architecture/decisions`을 갱신한다.
- 구현 계약, manifest 구조, agent/tool contract처럼 구현자가 따라야 할 세부 설계는 `03.specs`에 둔다.
- `03.specs/<feature-id>/` 하위 폴더는 기본적으로 별도 README를 요구하지 않는다. 중앙 인덱스와 현재성 판단은 `03.specs/README.md`가 소유하고, feature-local README는 하위 API/agent/data/test 보조 문서가 많아져 탐색 비용이 커질 때만 추가한다.
- 수행 순서와 risk/verification gate는 `04.execution/plans`에, 실제 작업과 evidence는 `04.execution/tasks`에 둔다.
- 운영 지식은 먼저 `05.operations/guides`, `05.operations/policies`, `05.operations/runbooks` 중 하나로 분류한다. guide는 안정 상태 안내, operation은 정책과 경계, runbook은 실행 가능한 절차와 복구 순서를 담당한다.
- 사고가 없으면 `05.operations/incidents`는 README만 있는 상태가 정상이다. 실제 사고 기록과 postmortem이 생길 때만 하위 문서를 추가한다.

## Documentation Flow

`01.requirements` (기획) -> `02.architecture/requirements` / `02.architecture/decisions` (설계와 결정) -> `03.specs` (상세 명세) -> `04.execution/plans` / `04.execution/tasks` (실행과 검증) -> `05.operations/guides` / `05.operations/policies` / `05.operations/runbooks` (운영 지식) -> `05.operations/incidents` (사고와 회고)

## Documentation Contract

이 저장소의 문서 변경은 stage 책임, 템플릿, 링크 기준을 함께 지켜야 한다.

## 문서 역할과 언어 계약

사람이 읽는 안내와 요약은 한국어를 우선하고, AI Agent가 실행 기준으로 삼는
정책·프롬프트·도구·검증 계약은 영어를 우선한다. 한 문서가 두 독자를 함께
상대하면 사람용 맥락은 한국어로, `AI Agent Requirements` 같은 에이전트용
요구사항 섹션은 영어로 작성한다.

실행 계약에 가까운 문서는 영어를 기본값으로 둔다. `docs/03.specs/**/spec.md`
는 구현 명세이므로 영어로 작성하고, `docs/04.execution/plans/*.md`와
`docs/04.execution/tasks/*.md`도 계획·검증·handoff 증적이므로 영어로
작성한다. 반대로 README와 운영 안내처럼 사람이 먼저 읽는 문서는 한국어로
두되, 그 안에 들어가는 AI Agent 실행 지시나 도구 계약은 영어로 분리한다.
`docs/90.references`의 reference 문서는 사람용 개요와 lookup 설명에는 한국어를
쓸 수 있지만, `Authority Boundary`, `Sources`, `Review and Freshness`,
version support boundary, generated-index contract처럼 사실 계약으로 소비되는
필드는 영어를 우선한다.

각 stage의 역할은 아래와 같이 분리한다.

| Lifecycle Stage | Folder | Canonical Template | Required Responsibility |
| --- | --- | --- | --- |
| Requirement | [`01.requirements`](./01.requirements/README.md) | [`prd.template.md`](./99.templates/templates/sdlc/requirements/prd.template.md) | 사용자 문제, 범위, 기능 요구사항, 성공/수용 기준 |
| Architecture Requirement | [`02.architecture/requirements`](./02.architecture/requirements/README.md) | [`ard.template.md`](./99.templates/templates/sdlc/architecture/ard.template.md) | 시스템 경계, 품질 속성, 참조 구조 |
| Architecture Decision | [`02.architecture/decisions`](./02.architecture/decisions/README.md) | [`adr.template.md`](./99.templates/templates/sdlc/architecture/adr.template.md) | 하나의 결정, 맥락, 결과, 대안 |
| Specification | [`03.specs`](./03.specs/README.md) | [`spec.template.md`](./99.templates/templates/sdlc/specs/spec.template.md) | 구현 계약, 인터페이스, 검증 기준 |
| Plan | [`04.execution/plans`](./04.execution/plans/README.md) | [`plan.template.md`](./99.templates/templates/sdlc/execution/plan.template.md) | 실행 순서, 리스크, rollout, verification gate |
| Task | [`04.execution/tasks`](./04.execution/tasks/README.md) | [`task.template.md`](./99.templates/templates/sdlc/execution/task.template.md) | 작업 단위, evidence, 완료 상태 |
| Operation | [`05.operations`](./05.operations/README.md) | guide/policy/runbook templates | 안정 상태 안내, 정책, 실행 절차 |
| Reference | [`90.references`](./90.references/README.md) | [`reference.template.md`](./99.templates/templates/common/reference.template.md) | lookup material, glossary, appendix, version snapshot, dated source/freshness boundary |
| Archive | [`98.archive`](./98.archive/README.md) | [`archive-tombstone.template.md`](./99.templates/templates/common/archive-tombstone.template.md) | old 문서의 original-path mirror와 metadata-only Tombstone |

- README와 index 문서는 해당 폴더의 목적, scope, structure, workflow, link basis, related documents를 유지한다.
- README와 index 문서는 frontmatter 없이 작성한다. 다른 authored stage 문서는 matching template의 `title`, `type`, `status`, `owner`, `updated` metadata를 유지한다.
- 모든 authored stage 문서는 `Related Documents`를 통해 upstream/downstream 문맥을 연결한다.
- Spec의 `Related Inputs`는 upstream 입력 요약으로 사용할 수 있지만,
  `Related Documents` 섹션의 upstream/downstream 링크를 대체하지 않는다.
- Markdown 링크는 최종 문서 위치 기준 상대 경로를 사용한다. 아직 존재하지 않는 optional 경로나 placeholder는 Markdown 링크가 아니라 code literal로 남긴다.
- stale 문서는 현재 구현과 비교해 갱신, 병합, archive 중 하나로 정리한다. 현재 구현과 상충하는 old 문서는 [`98.archive`](./98.archive/README.md)에 Tombstone으로 이동하고 활성 문서에서는 archive index만 연결한다.
- 문서를 제거하거나 archive로 이동하는 일은 관련 링크 갱신, current replacement 확인, 리뷰 가능한 diff가 있을 때만 허용한다.
- 문서 stage나 템플릿이 바뀌면 관련 stage README, [Template Routing Contract](./99.templates/support/template-routing.md), [`99.templates/README.md`](./99.templates/README.md)를 같은 변경에서 맞춘다.

## 구현 영역 연결

- `gitops/`: 현재 로컬 플랫폼 desired state다. `clusters/local`, `apps/root`, `platform/*`, `workloads/adminer` 변경은 관련 Spec/Policy/Runbook 링크와 함께 추적한다.
- `infrastructure/`: bootstrap, k3d/ArgoCD values, MetalLB root manifest, static contract tests를 둔다. 정상 운영 변경의 정본은 GitOps 경로로 넘긴다.
- `traefik/`: 로컬 플랫폼 UI 접근을 돕는 dynamic config reference다. cloud ingress target이나 ArgoCD canonical 배포 경로로 취급하지 않는다.
- `examples/`: 앱 온보딩과 AWS/Azure migration reference-only 자산이다. 버전 스냅샷은 `90.references/data/tech-stack-version-inventory.md`와 함께 관리한다.

## Quality Gates

문서 구조와 저장소 품질은 `bash scripts/validate-repo-quality-gates.sh .`로 검증한다. 이 게이트는 다음 계약을 확인한다.

- 허용된 `docs/` top-level 폴더만 존재해야 한다.
- 모든 허용 stage 폴더는 `README.md`를 가져야 하며, validator의 README base section인 `Overview`, `Audience`, `Scope`, `Structure`, `How to Work in This Area`, `Link Basis`, `Related Documents`를 유지해야 한다.
- 모든 템플릿은 `docs/99.templates/`에 있어야 하고 template inventory에 등록되어야 한다.
- authored stage 문서는 템플릿의 필수 heading을 유지해야 한다. `If Applicable`과 `Optional` 섹션은 실제 필요가 있을 때만 작성한다.
- archive Tombstone은 `archive-tombstone.template.md` 구조를 유지하고 old body를 보존하면 안 된다.
- `reference.template.md`는 archive 정책을 소유하지 않으며 archive 언어가 포함되면 안 된다.
- Agent gateway, `.claude`, `.codex`, `docs/00.agent-governance`의 runtime mirror와 harness catalog가 일관되어야 한다.
- GitHub Actions YAML, workflow 중복 step, script reference, obsolete file, tech-stack version drift가 검증되어야 한다.
- 오래된 docs path, Dashboard runtime 계약, legacy stage 표현은 명시된 역사/대체 문맥 없이 재등장하면 안 된다.
- authored docs, README, examples Markdown에는 feature branch + PR flow를 우회하는 direct push 예시가 없어야 한다.

로컬 k3d에서는 기존 ingress-nginx 계약과 [traefik](../traefik/README.md) 보조 노출 경로를 유지한다. Ingress NGINX upstream retirement 이후 cloud target은 AWS ALB/Gateway API, Azure AGC/Gateway API 계열로 분리해 추적한다.

## Related Documents

- [Root README](../README.md)
- [Agent Governance Hub](./00.agent-governance/README.md)
- [Document Stage Routing Rules](./00.agent-governance/rules/document-stage-routing.md)
- [Stage Authoring Matrix](./00.agent-governance/rules/stage-authoring-matrix.md)
- [Template Routing Contract](./99.templates/support/template-routing.md)
- [Templates README](./99.templates/README.md)
- [Archive Index](./98.archive/README.md)
- [Scripts README](../scripts/README.md)
- [Traefik README](../traefik/README.md)
- [Tech Stack Version Inventory](./90.references/data/tech-stack-version-inventory.md)
- [LLM WIKI Reference Index](./90.references/llm-wiki/README.md)
- [Generated LLM WIKI Index](./90.references/llm-wiki/wiki-index.md)
