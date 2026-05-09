# docs: 프로젝트 문서 허브

> [!NOTE]
> All AI agent interactions with this documentation suite must comply with the [Agent Governance Hub](./00.agent-governance/README.md).

## Overview

`docs/`는 `hy-home.k8s`의 요구사항, 아키텍처, 결정, 명세, 실행 계획, 작업 증적, 운영 절차, 사고 기록, 참조 자료, 템플릿을 연결하는 문서 SSoT다. 단순 기록 저장소가 아니라 k3d/GitOps 홈랩을 사람이 운영하고 AI Agent가 안전하게 협업하기 위한 추적 가능한 작업 체계다.

문서는 Spec-First 흐름을 따른다. 기획의 맥락은 설계와 결정으로 이어지고, 상세 명세와 실행 계획을 거쳐 작업 증적, 운영 지침, 런북, 사고 기록으로 연결된다.
AWS/Azure 예시와 외부 기술 버전 기준처럼 빠르게 변할 수 있는 참조값은 [90.references](./90.references/README.md)와 [tech-stack-version-inventory.md](./90.references/tech-stack-version-inventory.md)에 스냅샷 기준일과 함께 기록한다.

## Audience

이 README의 주요 독자:

- Developers
- Operators
- Documentation Writers
- AI Agents

## Scope

### In Scope

- `00.agent-governance` 아래의 Agent 정책, 실행 규칙, workspace governance
- `01.prd`부터 `10.incidents`까지의 요구사항, 아키텍처, 결정, 명세, 계획, 작업, 가이드, 운영, 런북, 사고 기록
- `90.references` 아래의 사실 기반 참조 자료와 lookup material
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
├── 01.prd/                # Product and feature requirements
├── 02.ard/                # Architecture requirements and reference model
├── 03.adr/                # Architecture decision records
├── 04.specs/              # Software, automation, and Agent design specifications
├── 05.plans/              # Execution, rollout, and migration plans
├── 06.tasks/              # Implementation and validation task lists
├── 07.guides/             # Steady-state user/developer/operator guides
├── 08.operations/         # Shared operational policies and standards
├── 09.runbooks/           # Executable operational procedures
├── 10.incidents/          # Incident records and postmortems
├── 90.references/         # Factual references and lookup material
├── 99.templates/          # Document templates
└── README.md              # This file
```

## How to Work in This Area

1. 새 문서를 만들기 전에 [document-stage-routing.md](./00.agent-governance/rules/document-stage-routing.md)에서 canonical path를 확인한다.
2. 새 문서는 [99.templates](./99.templates/README.md)의 승인된 템플릿에서 시작한다.
3. 문서가 추가되거나 이동되면 해당 stage의 `README.md` 인덱스와 관련 링크를 같은 변경에서 갱신한다.
4. 사람 대상 README와 개요 문서는 한국어를 유지하고, `00.agent-governance` 정책 문서는 영어를 유지한다.
5. 일반 운영 변경은 GitOps-first 원칙을 따르며, 문서가 live `kubectl apply`나 외부 Vault 조작을 우회 절차처럼 안내하지 않도록 한다.
6. cloud example 버전을 갱신할 때는 코드, README, [tech-stack-version-inventory.md](./90.references/tech-stack-version-inventory.md)를 같은 변경에서 맞춘다.

## Documentation Flow

`01.prd` (기획) -> `02.ard` / `03.adr` (설계와 결정) -> `04.specs` (상세 명세) -> `05.plans` / `06.tasks` (실행과 검증) -> `07.guides` / `08.operations` / `09.runbooks` (운영 지식) -> `10.incidents` (사고와 회고)

## 구현 영역 연결

- `gitops/`: 현재 로컬 플랫폼 desired state다. `clusters/local`, `apps/root`, `platform/*`, `workloads/adminer` 변경은 관련 Spec/Policy/Runbook 링크와 함께 추적한다.
- `infrastructure/`: bootstrap, k3d/ArgoCD values, MetalLB root manifest, static contract tests를 둔다. 정상 운영 변경의 정본은 GitOps 경로로 넘긴다.
- `traefik/`: 로컬 플랫폼 UI 접근을 돕는 dynamic config reference다. cloud ingress target이나 ArgoCD canonical 배포 경로로 취급하지 않는다.
- `examples/`: 앱 온보딩과 AWS/Azure migration reference-only 자산이다. 버전 스냅샷은 `90.references/tech-stack-version-inventory.md`와 함께 관리한다.

## Quality Gates

문서 구조와 저장소 품질은 `bash scripts/validate-repo-quality-gates.sh .`로 검증한다. 이 게이트는 다음 계약을 확인한다.

- 허용된 `docs/` top-level 폴더만 존재해야 한다.
- 모든 허용 stage 폴더는 `README.md`를 가져야 하며, 목적, 포함할 내용, 관련 폴더, 예시 섹션을 포함해야 한다.
- 모든 템플릿은 `docs/99.templates/`에 있어야 하고 template inventory에 등록되어야 한다.
- Agent gateway, `.claude`, `.codex`, `docs/00.agent-governance`의 runtime mirror와 harness catalog가 일관되어야 한다.
- GitHub Actions YAML, workflow 중복 step, script reference, obsolete file, tech-stack version drift가 검증되어야 한다.
- 오래된 docs path, Dashboard runtime 계약, legacy stage 표현은 명시된 역사/대체 문맥 없이 재등장하면 안 된다.
- authored docs, README, examples Markdown에는 feature branch + PR flow를 우회하는 direct push 예시가 없어야 한다.

로컬 k3d에서는 기존 ingress-nginx 계약과 [traefik](../traefik/README.md) 보조 노출 경로를 유지한다. Ingress NGINX upstream retirement 이후 cloud target은 AWS ALB/Gateway API, Azure AGC/Gateway API 계열로 분리해 추적한다.

## Related References

- [Root README](../README.md)
- [Agent Governance Hub](./00.agent-governance/README.md)
- [Document Stage Routing Rules](./00.agent-governance/rules/document-stage-routing.md)
- [Stage Authoring Matrix](./00.agent-governance/rules/stage-authoring-matrix.md)
- [Templates README](./99.templates/README.md)
- [Scripts README](../scripts/README.md)
- [Traefik README](../traefik/README.md)
- [Tech Stack Version Inventory](./90.references/tech-stack-version-inventory.md)
