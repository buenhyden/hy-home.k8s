---
title: "Common Repository Vocabulary"
version: "0.1.0"
type: "governance/vocabulary"
status: "draft"
owner: "platform"
updated: "2026-11-20"
---

# Repository Vocabulary

## Purpose

저장소 간 공유하는 작업·거버넌스 용어의 의미를 이 문서 하나에서 정의한다. 각 행의 링크는 동작 규칙과 소비자를 소유하는 현재 문서를 가리킨다. 용어 정의는 승인·실행 권한을 부여하지 않는다.

## Scope

공통 용어의 의미, TERM ID, 혼동할 개념, 정책 소유자와 계약 판본을 다룬다. K8s 클러스터·context·namespace·application처럼 이 환경에서만 쓰는 의미는 [로컬 용어집](../../docs/00.workspace/01.project/glossary.md)에 둔다. 규칙·상태 전이·검사 알고리즘은 각 정책과 Stage 99 Registry가 소유한다.

## Normative Language

대문자 MUST, MUST NOT, SHOULD, MAY는 RFC 2119와 RFC 8174의 읽기 규칙을 따른다. 이 어휘 문서나 강한 표현 자체는 권한을 만들지 않는다.

## Repository Vocabulary

| Term ID | Term | Korean | Definition | Not to Confuse | Policy Owner | Contract Version |
| --- | --- | --- | --- | --- | --- | --- |
| TERM-AUTHORITY | Authority | 권한 근거 | The decision maker and permitting basis valid for a stated scope, action and edition. A file existing or a tool running creates no authority. | An execution result; a supported feature | [Approval and risk boundary policy](../../docs/00.workspace/04.quality/approval-and-safety.md) | 3.0.1 |
| TERM-GOVERNANCE | Governance | 거버넌스 | The system that assigns who proposes, owns, approves, applies, excepts and changes rules. | An index that copies every policy body | [Governance canon](../governance/agent-execution.md) | 3.0.1 |
| TERM-POLICY | Policy | 정책 | The current norm that sets permissions, duties, prohibitions and exceptions for a goal and scope. | A single Task record | [Sole author of that policy](../../docs/00.workspace/03.process/sdlc.md) | 3.0.1 |
| TERM-RULE | Rule | 규칙 | A normative unit under a policy that makes a condition, the expected behavior and the violation judgment concrete. | Changing only a checker's expected value | [Policy and rule canon](../../docs/00.workspace/03.process/sdlc.md) | 3.0.1 |
| TERM-CONTRACT | Contract | 계약 | A versioned agreement between producer and consumer on meaning, inputs and outputs, invariants and verification rules. | A particular implementation language | [Common contract canon](../../docs/00.workspace/03.process/sdlc.md) | 3.0.1 |
| TERM-CANONICAL | Canonical Source | 단일 정본 | The one source with independent authoring authority for a meaning; every derived copy tracks its source and edition. | Merely having a single copy | [Canonical source and distribution policy](../../docs/00.workspace/03.process/document-authoring.md) | 3.0.1 |
| TERM-APPROVAL | Approval | 승인 | A decision that grants authority to perform a named change or execution within a named scope. It is distinct from accepting a result. | Acceptance; a passing test; a merge | [Approval boundary policy](../../docs/00.workspace/04.quality/approval-and-safety.md) | 3.0.1 |
| TERM-ADOPTION | Adoption | 채택 | The state in which a given edition of a common contract is reflected in a workspace's producers and consumers and verified there. | Approval of the common target | [Contract implementer](../../docs/00.workspace/03.process/document-authoring.md) | 3.0.1 |
| TERM-EXECUTION | Execution | 실행 | An action actually carried out on a real target, environment and edition, as opposed to a proposed command or a declared setting. | A plan; a configuration | [Executing Task](../workflows/work-lifecycle.md) | 3.0.1 |
| TERM-VERIFICATION | Verification | 검증 | Confirming, by observation, test or review, that an output meets its stated requirement or contract. | Validation; user acceptance | [Verification policy](../../docs/00.workspace/04.quality/quality.md) | 3.0.1 |
| TERM-VALIDATION | Validation | 목적 적합성 확인 | Confirming, under the relevant conditions, that an output serves its intended use and the actual need. | Judging by a tool named validate alone | [Quality and acceptance policy](../../docs/00.workspace/04.quality/quality.md) | 3.0.1 |
| TERM-ACCEPTANCE | Acceptance | 인수 | A decision by an authorized party to accept a stated criterion together with its evidence, keeping the basis for how required failures and exceptions were handled. | Approval; a merged pull request | [Acceptance criterion owner](../../docs/00.workspace/03.process/document-lifecycle.md) | 3.0.1 |
| TERM-COMPLETION | Completion | 완료 | A scoped closure reached when the work's required execution, checks and acceptance conditions are met. It does not close integration, deployment or other Tasks by itself. | Turning every state into completed | [SDLC and Task owner](../../docs/00.workspace/03.process/document-lifecycle.md) | 3.0.1 |
| TERM-PROMOTION | Promotion | 지속 의미 승격 | Handing the lasting meaning of an open change, as the Plan maps it, to the current requirement, design, operations or governance owner. | Moving a file; copying Task state | [Plan and the receiving current document](../../docs/00.workspace/03.process/document-lifecycle.md) | 3.0.1 |
| TERM-RETIREMENT | Retirement | 문서 종료 | A decision that ends a document's current effect and fixes its successor owner, lineage and any needed historical basis. | Unconditional deletion | [Document lifecycle policy](../../docs/00.workspace/03.process/document-lifecycle.md) | 3.0.1 |
| TERM-ARCHIVE | Archive | 역사 보관 | The holding state of information whose preservation is actually approved. Development trial and error from before the final cutover is not kept by archiving around it; an operational retention duty follows its own target and decision. | Treating vault retention as the end of development | [Preservation and disposition policy](../../docs/00.workspace/03.process/document-lifecycle.md) | 3.0.1 |
| TERM-REMOVAL | Removal | 사본 제거 | Taking away the actual copies of, or accessible references to, an approved target, keeping the deletion scope, any remaining copy and the authority apart. An approved final transition keeps no recovery copy of its removal targets, as REQ-0003-FR-0020 requires. | Rewriting Git history; destroying a source without basis | [Disposition Task](../../docs/00.workspace/03.process/document-lifecycle.md) | 3.0.1 |
| TERM-SUPERSESSION | Supersession | 대체 | A relation in which a new meaning owner takes over the valid scope of an earlier document or decision and links the lineage. | A simple title change | [Lifecycle and relationship contract](../../docs/00.workspace/03.process/document-lifecycle.md) | 3.0.1 |
| TERM-HOLD | Preservation Hold | 보존 보류 | A preservation condition that blocks disposal of a given source or evidence until a resolving basis exists. | A blanket stop on all execution | [Preservation owner](../../docs/00.workspace/03.process/document-lifecycle.md) | 3.0.1 |
| TERM-REGISTRY | Registry | 등록 계약 | The machine-readable contract that states document profiles, forms, states, relationships and generator bindings. Approval does not exempt it from reform. | A frozen baseline | [Registry contract author](../../docs/99.templates/README.md) | 3.0.1 |
| TERM-TEMPLATE | Template | 템플릿 | The authoring form that implements one role's common rules, policy, fields, headings, tables, relationships and lifecycle. | A copied example; a heading list only | [TemplateDefinition and registry](../../docs/99.templates/README.md) | 3.0.1 |
| TERM-PROFILE | Document Profile | 문서 프로필 | The conditions under which fields, sections, relationships, lifecycle and template apply to one document role. It differs from an execution profile that selects checks. | A validation profile | [Registry](../../docs/99.templates/README.md) | 3.0.1 |
| TERM-TASK | Task | 실행 업무 기록 | The single authored record of a scope's execution, blockers, observations, evidence and acceptance decision; other documents reference or derive from it. | A duplicate progress table in a Plan | [Executing owner](../../docs/03.specs/README.md) | 3.0.1 |
| TERM-EVIDENCE | Evidence | 증거 | The actual source, target edition, conditions and result that support a claim, with static, local, remote, native and operational scope kept apart. | A memory summary; a planned command | [The Task and the evidence producer](../../docs/00.workspace/04.quality/quality.md) | 3.0.1 |
| TERM-RESOLVES | Resolves | 증거 해소 관계 | An explicit link stating that later evidence meets the same obligation, input conditions and guarantee and so settles an earlier failure or unrun check. | A newer PASS erasing every failure | [Evidence judge](../../docs/03.specs/README.md) | 3.0.1 |
| TERM-HARNESS | Harness | 에이전트 실행 체계 | The execution setup that connects instructions, routing, permissions, state, tools, observation, termination and recovery. | Assuming an instruction file is applied because it exists | [Harness contract](../governance/agent-execution.md) | 3.0.1 |
| TERM-NATIVE-EVIDENCE | Native Runtime Evidence | 네이티브 실행 증거 | A result observed on the installed provider, edition and real tool path. | A direct function test; an official description | [Quality evidence policy](../../docs/00.workspace/04.quality/quality.md) | 3.0.1 |
| TERM-PROJECTION | Projection | 통제된 파생본 | Consumable text generated or synchronized from a canonical source plus an explicit local binding; it has no separate authority to author policy. | An independent manual copy | [Generation and distribution owner](../roles/README.md) | 3.0.1 |
| TERM-EXCEPTION | Exception | 명시적 예외 | A limited departure from a standard with an approved condition, scope, reason, period or end condition, and verification. | Keeping an existing difference forever | [Approver of the policy concerned](../../docs/00.workspace/04.quality/approval-and-safety.md) | 3.0.1 |
| TERM-UNVERIFIED | Unverified | 미검증 | The state of lacking the basis a current claim needs; it asserts neither a gap, nor inapplicability, nor completion. | A confirmed missing implementation | [Survey and judgment owner](../../docs/00.workspace/04.quality/quality.md) | 3.0.1 |
| TERM-KEEP | Keep | 구현 유지 | An action taken when fit between the current target and its real consumers is confirmed, so no implementation change is needed; unfinished acceptance stays recorded separately. | An exemption from reform because of past approval | [Change owner](../workflows/work-lifecycle.md) | 3.0.1 |
| TERM-RELEASE-OPERATION | Release Operation | 배포 버전 발행 | The operation that manages tags, artifacts, GitHub Releases and public delivery. It is not a separate development document role. | Reintroducing a Release document role | [Git and delivery owner](../../docs/00.workspace/03.process/git.md) | 3.0.1 |
| TERM-PUBLIC-CONTRACT | Public Contract | 공개 계약 | The promise of keys, forms, meanings, states, relationships and outputs that real consumers rely on. | Implementation detail | [Document version and identity policy](../../docs/00.workspace/03.process/document-authoring.md) | 3.0.1 |
| TERM-COMPATIBILITY | Compatibility | 호환성 | The relation in which earlier valid producers and consumers keep working on a new edition without breaking the Public Contract. | Having fixed every consumer in the same pull request | [Document version and identity policy](../../docs/00.workspace/03.process/document-authoring.md) | 3.0.1 |
| TERM-CONTRACT-VERSION | Contract Version | 계약 판본 | The three-component numeric version of the meaning and form under one contract ID. | An external package label | [Document version and identity policy](../../docs/00.workspace/03.process/document-authoring.md) | 3.0.1 |
| TERM-REGISTRY-SCHEMA-VERSION | Registry Schema Version | 레지스트리 스키마 판본 | The document contract version of the data structure that code reading the registry expects. | A database's internal migration integer | [Document version and identity policy](../../docs/00.workspace/03.process/document-authoring.md) | 3.0.1 |
| TERM-DOCUMENT-REVISION | Document Revision | 문서 개정 판본 | The three-component numeric `version` that marks a revision of one document's content. | A product version; a document's issue number | [Document version and identity policy](../../docs/00.workspace/03.process/document-authoring.md) | 3.0.1 |
| TERM-PRERELEASE | Prerelease | 사전 배포판 | The hyphen extension of general SemVer. The numeric profile for documents and contracts does not use it. | A draft status | [Document version and identity policy](../../docs/00.workspace/03.process/document-authoring.md) | 3.0.1 |
| TERM-BUILD-METADATA | Build Metadata | 빌드 메타데이터 | The plus extension of general SemVer. The numeric profile for documents and contracts does not use it. | A document content revision | [Document version and identity policy](../../docs/00.workspace/03.process/document-authoring.md) | 3.0.1 |
| TERM-BASELINE-NAMESPACE | Baseline Namespace | 기준선 번호 공간 | The space that keeps current document issue numbers from colliding. | Resetting a version | [Document version and identity policy](../../docs/00.workspace/03.process/document-authoring.md) | 3.0.1 |
| TERM-DRAFT | Draft | 초안 | A document that may be written, completed and reviewed. On its own it gives no authority or evidence for implementation, operational application or a completion decision; its document status, a separate execution approval and actual completion or acceptance are different facts. | Authority to implement; operational application; completion | [Document lifecycle policy](../../docs/00.workspace/03.process/document-lifecycle.md) | 3.0.1 |
| TERM-READINESS | Readiness | 착수 준비 | The state in which the current inputs, environment, authority and scope meet the conditions to start a given piece of work. | Approval; acceptance | [Work start policy](../workflows/work-lifecycle.md) | 3.0.1 |
| TERM-DESIGN-FIT | Design Fitness | 설계 적합성 | The result of comparing an existing implementation's meaning, interfaces and guarantees with the target design derived from current requirements. | A past completion; an identical structure | [Design owner](../../docs/00.workspace/03.process/sdlc.md) | 3.0.1 |
| TERM-REQUIREMENT | Requirement | 요구사항 | A durable need together with the boundary at which it counts as accepted. | A design or a change contract | [Requirements stage](../../docs/01.requirements/README.md) | 1.0.0 |
| TERM-ARCHITECTURE-DESCRIPTION | Architecture Description | 아키텍처 설명 | The current structural view of a system and its boundaries. | A decision record | [Architecture stage](../../docs/02.architecture/README.md) | 1.0.0 |
| TERM-ARCHITECTURE-DECISION | Architecture Decision Record | 아키텍처 결정 기록 | A durable choice with the reasons it was made. | The structural view itself | [Architecture stage](../../docs/02.architecture/README.md) | 1.0.0 |
| TERM-SPEC | Spec | 명세 | The approved contract for one change and its acceptance criteria. | Its execution order or its evidence | [Spec stage](../../docs/03.specs/README.md) | 1.0.0 |
| TERM-PLAN | Plan | 계획 | The approved order, risks and planned checks for carrying out a Spec. | The record of what actually ran | [Spec stage](../../docs/03.specs/README.md) | 1.0.0 |
| TERM-ISSUE | GitHub Issue or Project | 이슈와 프로젝트 | A request with its priority, or a board that displays the state of work. | The Spec or Task it points to | [SDLC contract](../../docs/00.workspace/03.process/sdlc.md) | 1.0.0 |
| TERM-CONTROL | Control | 통제 | The mechanism that enforces a rule. | The rule it enforces | [SDLC contract](../../docs/00.workspace/03.process/sdlc.md) | 1.0.0 |
| TERM-PROVIDER | Provider | 제공자 | The adapter contract for one agent runtime. | A neutral role | [Agent execution policy](../governance/agent-execution.md) | 1.0.0 |
| TERM-ROLE | Role | 역할 | A neutral responsibility together with its allowed scope. | An agent instance | [Role registry](../roles/README.md) | 1.0.0 |
| TERM-AGENT | Agent | 에이전트 | A running instance that acts in some role. | The role definition | [Role registry](../roles/README.md) | 1.0.0 |
| TERM-SKILL | Skill | 스킬 | A reusable, invocable procedure. | A native registration | [Agent execution policy](../governance/agent-execution.md) | 1.0.0 |
| TERM-HOOK | Hook | 훅 | A callback the runtime or Git fires on an event. | A quality gate | [Quality policy](../../docs/00.workspace/04.quality/quality.md) | 1.0.0 |
| TERM-GATE | Gate | 게이트 | A quality decision that blocks progress when it fails. | The script that implements it | [Quality policy](../../docs/00.workspace/04.quality/quality.md) | 1.0.0 |
| TERM-VALIDATOR | Validator | 검사기 | An executable check that implements a gate's decision. | The gate decision itself | [Validation registry](../../scripts/validation/registry.json) | 1.0.0 |
| TERM-FIXTURE | Fixture | 테스트 입력 | A bounded, independent input built for a test. | Production policy input | [Quality policy](../../docs/00.workspace/04.quality/quality.md) | 1.0.0 |
| TERM-QA | QA | 품질 검사 | The set of quality checks run over a change. | Hosted CI results | [Quality policy](../../docs/00.workspace/04.quality/quality.md) | 1.0.0 |
| TERM-CI | CI | 지속 통합 | Orchestration that integrates changes and runs the hosted checks the quality policy selects. | Local QA | [Quality policy](../../docs/00.workspace/04.quality/quality.md) | 1.1.0 |
| TERM-CD | CD | 지속 전달 | Delivery of declared state and its reconciliation into environments. | A commit or a passing check | [SDLC contract](../../docs/00.workspace/03.process/sdlc.md) | 1.0.0 |
| TERM-DEPLOYMENT | Deployment | 배포 | Applying a declared version to an environment. | A release operation | [SDLC contract](../../docs/00.workspace/03.process/sdlc.md) | 1.0.0 |
| TERM-GUIDE | Guide | 가이드 | Explanatory operating knowledge for a reader. | A triggered procedure | [Operations stage](../../docs/05.operations/README.md) | 1.0.0 |
| TERM-RUNBOOK | Runbook | 런북 | Triggered operating steps that carry their own rollback and verification. | Background explanation | [Operations stage](../../docs/05.operations/README.md) | 1.0.0 |
| TERM-WORKSPACE | Workspace | 작업환경 | 개발·검증·협업이 이루어지는 현재 환경과 그 운영 경계. | 저장소 자체 또는 배포 대상 환경 | [Workspace SDLC](../../docs/00.workspace/03.process/sdlc.md) | 0.1.0 |
| TERM-REPOSITORY | Repository | 저장소 | 버전 관리되는 파일과 이력을 담는 작업 단위. 하나의 작업환경이 여러 저장소를 다룰 수 있다. | 현재 세션이나 배포 환경 | [Git policy](../../docs/00.workspace/03.process/git.md) | 0.1.0 |
| TERM-DESIGN | Design | 설계 | 요구를 충족하기 위해 선택한 구조와 동작의 설명. | 구현 결과 또는 실행 기록 | [SDLC ownership policy](../../docs/00.workspace/03.process/sdlc.md) | 0.1.0 |
| TERM-IMPLEMENTATION | Implementation | 구현 | 선택한 설계와 변경 계약을 실제 파일·설정·동작에 반영한 결과. | 설계 초안이나 검증 결과 | [Spec stage](../../docs/03.specs/README.md) | 0.1.0 |
| TERM-BRIEF | Brief | 작업 브리핑 | 현재 목표·범위·유지할 부분·수정할 부분·질문·검증 계획을 짧게 전달하는 시작 설명. | 승인 또는 완료 판정 | [Work lifecycle](../workflows/work-lifecycle.md) | 0.1.0 |
| TERM-SHARED-MEMORY | Shared Memory | 공유 메모리 | 작업환경이 세션 간 재사용하도록 관리하는 범위와 출처가 있는 기억 저장소. | 원본 세션 기록 또는 현재 권위 문서 | [Context and Memory](../governance/context-and-memory.md) | 0.1.0 |
| TERM-SESSION | Session | 세션 | 한 실행 주체가 특정 시점과 환경에서 수행한 연속 작업 맥락. | 장기 저장소 또는 Task | [Context and Memory](../governance/context-and-memory.md) | 0.1.0 |
| TERM-WORK-UNIT | Work Unit | 작업 단위 | 계획 안에서 소유자와 의존성·완료 조건을 구분해 실행할 수 있는 범위. | Task 문서 전체 또는 에이전트 세션 | [Plan stage](../../docs/03.specs/README.md) | 0.1.0 |
| TERM-LEASE | Lease | 작업 임대 | 병렬 작업에서 특정 소유자에게 정해진 시간·범위의 쓰기 점유를 부여하는 조정 기록. | 영구 소유권 또는 승인 | [Delegated Development](../workflows/delegated-development.md) | 0.1.0 |
| TERM-INDEPENDENT-REVIEW | Independent Review | 독립 검토 | 변경 작성자와 분리된 검토 주체가 범위와 위험에 맞춰 결과를 평가하는 절차. | 작성자의 자체 검증 또는 사용자 인수 | [Quality policy](../../docs/00.workspace/04.quality/quality.md) | 0.1.0 |
| TERM-CURRENT-BASELINE | Current Baseline | 현행 기준선 | 지금 적용되는 요구·설계·정책·구현을 판단할 때 사용하는 실제 판본과 상태. | 과거 스냅샷 또는 계획한 목표 | [Document lifecycle](../../docs/00.workspace/03.process/document-lifecycle.md) | 0.1.0 |

## Local Extensions

공통 의미에 대한 로컬 확장은 없다. K8s에 한정된 용어는 [작업환경 용어집](../../docs/00.workspace/01.project/glossary.md)에서 별도 TERM-K8S ID로 정의한다.

## Maintenance

의미 변경은 해당 용어의 정책 소유자와 현재 변경 Task에서 검토한다. 기존 ID는 재사용하고 계약 판본은 변경 범위에 맞춰 갱신한다. Stage 99 문서 profile, 링크·소유자 검사, knowledge 검사로 형식과 경로를 확인한다. 이 초안의 작성과 정적 검사 결과는 별도의 사용자 인수나 공통 계약 채택을 의미하지 않는다.

## References

- [용어집 profile과 양식 안내](../../docs/99.templates/README.md)
- [작업환경 SDLC](../../docs/00.workspace/03.process/sdlc.md)
- [ADR-0058](../../docs/00.workspace/02.architecture/02.decisions/0058-repository-vocabulary-in-knowledge-surface.md) (공통 지식 표면에 용어 정의 문서 수용)
- [ADR-0065](../../docs/00.workspace/02.architecture/02.decisions/0065-shared-vocabulary-and-workspace-ownership.md) (제안된 공통·로컬 소유 위치 정리; 인수 전)
- [로컬 용어집](../../docs/00.workspace/01.project/glossary.md)
