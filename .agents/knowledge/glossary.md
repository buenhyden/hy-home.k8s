---
title: "Repository Vocabulary"
version: "2.0.0"
type: "governance/vocabulary"
status: "active"
owner: "platform"
updated: "2026-11-15"
---

# Repository Vocabulary

## Purpose

This document owns the meaning of the shared governance terms used across this
repository. Each term names the policy role and file that own its operating
rules; those owners decide how approval, transitions, commands and checks
work, and they use these meanings without redefining them.
ADR-0058 (listed in the
[decision index](../../docs/02.architecture/decisions/README.md)) admits this one definition document into the otherwise pointer-only knowledge
surface.

## Scope

In scope: the common terms of the adopted vocabulary contract and the
repository terms under Local Extensions. Out of scope: approval steps, state
transitions, allowed commands, check algorithms and service-specific
operating detail, which stay with the owners each row names.

## Normative Language

The key words MUST, MUST NOT, SHOULD and MAY, when capitalized, are read as
described in RFC 2119 and RFC 8174. Their authority comes from the user and the
owning project contract, not from the RFCs, and choosing a stronger word does
not make an unenforced rule enforced. This document itself defines meanings and
states no obligation.

## Repository Vocabulary

| Term ID | Term | Korean | Definition | Not to Confuse | Policy Owner | Contract Version |
| --- | --- | --- | --- | --- | --- | --- |
| TERM-AUTHORITY | Authority | 권한 근거 | The decision maker and permitting basis valid for a stated scope, action and edition. A file existing or a tool running creates no authority. | An execution result; a supported feature | [Approval and risk boundary policy](../governance/approval-and-safety.md) | 3.0.1 |
| TERM-GOVERNANCE | Governance | 거버넌스 | The system that assigns who proposes, owns, approves, applies, excepts and changes rules. | An index that copies every policy body | [Governance canon](../governance/agent-execution.md) | 3.0.1 |
| TERM-POLICY | Policy | 정책 | The current norm that sets permissions, duties, prohibitions and exceptions for a goal and scope. | A single Task record | [Sole author of that policy](../governance/sdlc.md) | 3.0.1 |
| TERM-RULE | Rule | 규칙 | A normative unit under a policy that makes a condition, the expected behavior and the violation judgment concrete. | Changing only a checker's expected value | [Policy and rule canon](../governance/sdlc.md) | 3.0.1 |
| TERM-CONTRACT | Contract | 계약 | A versioned agreement between producer and consumer on meaning, inputs and outputs, invariants and verification rules. | A particular implementation language | [Common contract canon](../governance/sdlc.md) | 3.0.1 |
| TERM-CANONICAL | Canonical Source | 단일 정본 | The one source with independent authoring authority for a meaning; every derived copy tracks its source and edition. | Merely having a single copy | [Canonical source and distribution policy](../governance/document-authoring.md) | 3.0.1 |
| TERM-APPROVAL | Approval | 승인 | A decision that grants authority to perform a named change or execution within a named scope. It is distinct from accepting a result. | Acceptance; a passing test; a merge | [Approval boundary policy](../governance/approval-and-safety.md) | 3.0.1 |
| TERM-ADOPTION | Adoption | 채택 | The state in which a given edition of a common contract is reflected in a workspace's producers and consumers and verified there. | Approval of the common target | [Contract implementer](../governance/document-authoring.md) | 3.0.1 |
| TERM-EXECUTION | Execution | 실행 | An action actually carried out on a real target, environment and edition, as opposed to a proposed command or a declared setting. | A plan; a configuration | [Executing Task](../workflows/work-lifecycle.md) | 3.0.1 |
| TERM-VERIFICATION | Verification | 검증 | Confirming, by observation, test or review, that an output meets its stated requirement or contract. | Validation; user acceptance | [Verification policy](../governance/quality.md) | 3.0.1 |
| TERM-VALIDATION | Validation | 목적 적합성 확인 | Confirming, under the relevant conditions, that an output serves its intended use and the actual need. | Judging by a tool named validate alone | [Quality and acceptance policy](../governance/quality.md) | 3.0.1 |
| TERM-ACCEPTANCE | Acceptance | 인수 | A decision by an authorized party to accept a stated criterion together with its evidence, keeping the basis for how required failures and exceptions were handled. | Approval; a merged pull request | [Acceptance criterion owner](../governance/document-lifecycle.md) | 3.0.1 |
| TERM-COMPLETION | Completion | 완료 | A scoped closure reached when the work's required execution, checks and acceptance conditions are met. It does not close integration, deployment or other Tasks by itself. | Turning every state into completed | [SDLC and Task owner](../governance/document-lifecycle.md) | 3.0.1 |
| TERM-PROMOTION | Promotion | 지속 의미 승격 | Handing the lasting meaning of an open change, as the Plan maps it, to the current requirement, design, operations or governance owner. | Moving a file; copying Task state | [Plan and the receiving current document](../governance/document-lifecycle.md) | 3.0.1 |
| TERM-RETIREMENT | Retirement | 문서 종료 | A decision that ends a document's current effect and fixes its successor owner, lineage and any needed historical basis. | Unconditional deletion | [Document lifecycle policy](../governance/document-lifecycle.md) | 3.0.1 |
| TERM-ARCHIVE | Archive | 역사 보관 | The holding state of information whose preservation is actually approved. Development trial and error from before the final cutover is not kept by archiving around it; an operational retention duty follows its own target and decision. | Treating vault retention as the end of development | [Preservation and disposition policy](../governance/document-lifecycle.md) | 3.0.1 |
| TERM-REMOVAL | Removal | 사본 제거 | Taking away the actual copies of, or accessible references to, an approved target, keeping the deletion scope, any remaining copy and the authority apart. The Q01 and Q10 final cutover requires no recovery copy of the past to be kept. | Rewriting Git history; destroying a source without basis | [Disposition Task](../governance/document-lifecycle.md) | 3.0.1 |
| TERM-SUPERSESSION | Supersession | 대체 | A relation in which a new meaning owner takes over the valid scope of an earlier document or decision and links the lineage. | A simple title change | [Lifecycle and relationship contract](../governance/document-lifecycle.md) | 3.0.1 |
| TERM-HOLD | Preservation Hold | 보존 보류 | A preservation condition that blocks disposal of a given source or evidence until a resolving basis exists. | A blanket stop on all execution | [Preservation owner](../governance/document-lifecycle.md) | 3.0.1 |
| TERM-REGISTRY | Registry | 등록 계약 | The machine-readable contract that states document profiles, forms, states, relationships and generator bindings. Approval does not exempt it from reform. | A frozen baseline | [Registry contract author](../../docs/99.templates/README.md) | 3.0.1 |
| TERM-TEMPLATE | Template | 템플릿 | The authoring form that implements one role's common rules, policy, fields, headings, tables, relationships and lifecycle. | A copied example; a heading list only | [TemplateDefinition and registry](../../docs/99.templates/README.md) | 3.0.1 |
| TERM-PROFILE | Document Profile | 문서 프로필 | The conditions under which fields, sections, relationships, lifecycle and template apply to one document role. It differs from an execution profile that selects checks. | A validation profile | [Registry](../../docs/99.templates/README.md) | 3.0.1 |
| TERM-TASK | Task | 실행 업무 기록 | The single authored record of a scope's execution, blockers, observations, evidence and acceptance decision; other documents reference or derive from it. | A duplicate progress table in a Plan | [Executing owner](../../docs/03.specs/README.md) | 3.0.1 |
| TERM-EVIDENCE | Evidence | 증거 | The actual source, target edition, conditions and result that support a claim, with static, local, remote, native and operational scope kept apart. | A memory summary; a planned command | [The Task and the evidence producer](../governance/quality.md) | 3.0.1 |
| TERM-RESOLVES | Resolves | 증거 해소 관계 | An explicit link stating that later evidence meets the same obligation, input conditions and guarantee and so settles an earlier failure or unrun check. | A newer PASS erasing every failure | [Evidence judge](../../docs/03.specs/README.md) | 3.0.1 |
| TERM-HARNESS | Harness | 에이전트 실행 체계 | The execution setup that connects instructions, routing, permissions, state, tools, observation, termination and recovery. | Assuming an instruction file is applied because it exists | [Harness contract](../governance/agent-execution.md) | 3.0.1 |
| TERM-NATIVE-EVIDENCE | Native Runtime Evidence | 네이티브 실행 증거 | A result observed on the installed provider, edition and real tool path. | A direct function test; an official description | [Native runtime verification owner](../../.claude/provider.md) | 3.0.1 |
| TERM-PROJECTION | Projection | 통제된 파생본 | Consumable text generated or synchronized from a canonical source plus an explicit local binding; it has no separate authority to author policy. | An independent manual copy | [Generation and distribution owner](../roles/README.md) | 3.0.1 |
| TERM-EXCEPTION | Exception | 명시적 예외 | A limited departure from a standard with an approved condition, scope, reason, period or end condition, and verification. | Keeping an existing difference forever | [Approver of the policy concerned](../governance/approval-and-safety.md) | 3.0.1 |
| TERM-UNVERIFIED | Unverified | 미검증 | The state of lacking the basis a current claim needs; it asserts neither a gap, nor inapplicability, nor completion. | A confirmed missing implementation | [Survey and judgment owner](../governance/quality.md) | 3.0.1 |
| TERM-KEEP | Keep | 구현 유지 | An action taken when fit between the current target and its real consumers is confirmed, so no implementation change is needed; unfinished acceptance stays recorded separately. | An exemption from reform because of past approval | [Change owner](../workflows/work-lifecycle.md) | 3.0.1 |
| TERM-RELEASE-OPERATION | Release Operation | 배포 버전 발행 | The operation that manages tags, artifacts, GitHub Releases and public delivery. It is not a separate development document role. | Reintroducing a Release document role | [Git and delivery owner](../governance/git.md) | 3.0.1 |
| TERM-PUBLIC-CONTRACT | Public Contract | 공개 계약 | The promise of keys, forms, meanings, states, relationships and outputs that real consumers rely on. | Implementation detail | [Document version and identity policy](../governance/document-authoring.md) | 3.0.1 |
| TERM-COMPATIBILITY | Compatibility | 호환성 | The relation in which earlier valid producers and consumers keep working on a new edition without breaking the Public Contract. | Having fixed every consumer in the same pull request | [Document version and identity policy](../governance/document-authoring.md) | 3.0.1 |
| TERM-CONTRACT-VERSION | Contract Version | 계약 판본 | The three-component numeric version of the meaning and form under one contract ID. | An external package label | [Document version and identity policy](../governance/document-authoring.md) | 3.0.1 |
| TERM-REGISTRY-SCHEMA-VERSION | Registry Schema Version | 레지스트리 스키마 판본 | The document contract version of the data structure that code reading the registry expects. | A database's internal migration integer | [Document version and identity policy](../governance/document-authoring.md) | 3.0.1 |
| TERM-DOCUMENT-REVISION | Document Revision | 문서 개정 판본 | The three-component numeric `version` that marks a revision of one document's content. | A product version; a document's issue number | [Document version and identity policy](../governance/document-authoring.md) | 3.0.1 |
| TERM-PRERELEASE | Prerelease | 사전 배포판 | The hyphen extension of general SemVer. The numeric profile for documents and contracts does not use it. | A draft status | [Document version and identity policy](../governance/document-authoring.md) | 3.0.1 |
| TERM-BUILD-METADATA | Build Metadata | 빌드 메타데이터 | The plus extension of general SemVer. The numeric profile for documents and contracts does not use it. | A document content revision | [Document version and identity policy](../governance/document-authoring.md) | 3.0.1 |
| TERM-BASELINE-NAMESPACE | Baseline Namespace | 기준선 번호 공간 | The space that keeps current document issue numbers from colliding. | Resetting a version | [Document version and identity policy](../governance/document-authoring.md) | 3.0.1 |
| TERM-DRAFT | Draft | 초안 | A document that may be written, completed and reviewed. On its own it gives no authority or evidence for implementation, operational application or a completion decision; its document status, a separate execution approval and actual completion or acceptance are different facts. | Authority to implement; operational application; completion | [Document lifecycle policy](../governance/document-lifecycle.md) | 3.0.1 |
| TERM-READINESS | Readiness | 착수 준비 | The state in which the current inputs, environment, authority and scope meet the conditions to start a given piece of work. | Approval; acceptance | [Work start policy](../workflows/work-lifecycle.md) | 3.0.1 |
| TERM-DESIGN-FIT | Design Fitness | 설계 적합성 | The result of comparing an existing implementation's meaning, interfaces and guarantees with the target design derived from current requirements. | A past completion; an identical structure | [Design owner](../governance/sdlc.md) | 3.0.1 |

## Local Extensions

Repository terms. They follow the same columns, never reuse a common Term ID
and never redefine a common term. Their Contract Version is the local
extension's own numeric version. Where each one lives and what rules govern it
stay in the SDLC contract's ownership and placement table.

| Term ID | Term | Korean | Definition | Not to Confuse | Policy Owner | Contract Version |
| --- | --- | --- | --- | --- | --- | --- |
| TERM-REQUIREMENT | Requirement | 요구사항 | A durable need together with the boundary at which it counts as accepted. | A design or a change contract | [Requirements stage](../../docs/01.requirements/README.md) | 1.0.0 |
| TERM-ARCHITECTURE-DESCRIPTION | Architecture Description | 아키텍처 설명 | The current structural view of a system and its boundaries. | A decision record | [Architecture stage](../../docs/02.architecture/README.md) | 1.0.0 |
| TERM-ARCHITECTURE-DECISION | Architecture Decision Record | 아키텍처 결정 기록 | A durable choice with the reasons it was made. | The structural view itself | [Architecture stage](../../docs/02.architecture/README.md) | 1.0.0 |
| TERM-SPEC | Spec | 명세 | The approved contract for one change and its acceptance criteria. | Its execution order or its evidence | [Spec stage](../../docs/03.specs/README.md) | 1.0.0 |
| TERM-PLAN | Plan | 계획 | The approved order, risks and planned checks for carrying out a Spec. | The record of what actually ran | [Spec stage](../../docs/03.specs/README.md) | 1.0.0 |
| TERM-ISSUE | GitHub Issue or Project | 이슈와 프로젝트 | A request with its priority, or a board that displays the state of work. | The Spec or Task it points to | [SDLC contract](../governance/sdlc.md) | 1.0.0 |
| TERM-CONTROL | Control | 통제 | The mechanism that enforces a rule. | The rule it enforces | [SDLC contract](../governance/sdlc.md) | 1.0.0 |
| TERM-PROVIDER | Provider | 제공자 | The adapter contract for one agent runtime. | A neutral role | [Provider note](../../.claude/provider.md) | 1.0.0 |
| TERM-ROLE | Role | 역할 | A neutral responsibility together with its allowed scope. | An agent instance | [Role registry](../roles/README.md) | 1.0.0 |
| TERM-AGENT | Agent | 에이전트 | A running instance that acts in some role. | The role definition | [Role registry](../roles/README.md) | 1.0.0 |
| TERM-SKILL | Skill | 스킬 | A reusable, invocable procedure. | A native registration | [Agent execution policy](../governance/agent-execution.md) | 1.0.0 |
| TERM-HOOK | Hook | 훅 | A callback the runtime or Git fires on an event. | A quality gate | [Quality policy](../governance/quality.md) | 1.0.0 |
| TERM-GATE | Gate | 게이트 | A quality decision that blocks progress when it fails. | The script that implements it | [Quality policy](../governance/quality.md) | 1.0.0 |
| TERM-VALIDATOR | Validator | 검사기 | An executable check that implements a gate's decision. | The gate decision itself | [Validation registry](../../scripts/validation/registry.json) | 1.0.0 |
| TERM-FIXTURE | Fixture | 테스트 입력 | A bounded, independent input built for a test. | Production policy input | [Quality policy](../governance/quality.md) | 1.0.0 |
| TERM-QA | QA | 품질 검사 | The set of quality checks run over a change. | Hosted CI results | [Quality policy](../governance/quality.md) | 1.0.0 |
| TERM-CI | CI | 지속 통합 | Orchestration that integrates changes and runs the hosted checks the quality policy selects. | Local QA | [Quality policy](../governance/quality.md) | 1.1.0 |
| TERM-CD | CD | 지속 전달 | Delivery of declared state and its reconciliation into environments. | A commit or a passing check | [SDLC contract](../governance/sdlc.md) | 1.0.0 |
| TERM-DEPLOYMENT | Deployment | 배포 | Applying a declared version to an environment. | A release operation | [SDLC contract](../governance/sdlc.md) | 1.0.0 |
| TERM-GUIDE | Guide | 가이드 | Explanatory operating knowledge for a reader. | A triggered procedure | [Operations stage](../../docs/05.operations/README.md) | 1.0.0 |
| TERM-RUNBOOK | Runbook | 런북 | Triggered operating steps that carry their own rollback and verification. | Background explanation | [Operations stage](../../docs/05.operations/README.md) | 1.0.0 |

## Maintenance

A term changes only through a change package that names it; the policy owner
in its row reviews the meaning. Adopting a later contract edition updates the
common rows and their Contract Version together, keeping Term IDs stable. The
knowledge validator judges this file: well-formed unique Term IDs, existing
owner paths and no span copied from an owner.

## References

- [Architecture decision index](../../docs/02.architecture/decisions/README.md) (ADR-0058, ADR-0036)
- [Requirements stage](../../docs/01.requirements/README.md) (REQ-0003-FR-0032)
- [SDLC contract](../governance/sdlc.md)
- [Common Knowledge](README.md)
