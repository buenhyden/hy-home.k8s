---
title: "Agent and Document Governance Architecture"
version: "1.0.0"
type: "sdlc/architecture-description"
status: "active"
owner: "platform"
updated: "2026-09-05"
layer: "architecture"
artifact_id: "AD-0006"
---

# Agent and Document Governance Architecture

## Overview

이 Architecture는 Agent·문서·검증·실행 증거의 current owner 경계를 설명한다.
[REQ-0003](../../01.requirements/0003-workspace-agent-governance-platform.md)의 요구를
[ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md),
[ADR-0031](../decisions/0031-current-corpus-retention-and-validation-ownership.md),
[ADR-0032](../decisions/0032-completed-and-terminal-document-retention.md)에 따라 배치한다.
실제 구현과 미완료 수렴은 [Spec 0054](../../03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md)가 소유한다.

## Boundaries & Non-goals

이 문서는 소유 경계, 흐름, 증거 class 및 품질 속성을 소유한다. Machine route·schema·state enum,
역할 roster, validator argv와 작업 상태는 아래 canonical owner를 참조하며 복제하지 않는다.
GitOps desired state와 플랫폼 interface는 [AD-0007](./0007-current-local-gitops-platform.md)가 소유한다.
외부 계정·credential·provider capability 및 live runtime은 이 문서의 구현 증거가 아니다.
별도 governance registry, provider별 정책 fork, Release family 또는 shared progress ledger를 만들지 않는다.

## Quality Attributes

| Attribute | Boundary | Evidence |
| --- | --- | --- |
| Consistency | 책임별 단일 machine/prose owner와 thin projection | Registry/schema, profile, owner 및 adapter parity |
| Verifiability | Repository-static, provider-runtime, hosted-CI, remote/live 분리 | Class별 직접 관측; 미관측은 owner와 retry trigger |
| Reliability | 제한된 retry와 no-progress stop, 안전한 resume | Loop contract 및 positive/negative recovery fixture |
| Security | 최소 권한과 승인 경계; 비밀정보·auth·전체 transcript 배제 | Static guardrail과 독립 review; 실행 권한은 별도 승인 |
| Recoverability | 일반 변경의 Git 복구와 봉인 evidence 무결성 분리 | Consumer 승계, source commit/blob/digest 및 legal lifecycle edge |
| Maintainability | 고정 census나 중복 wrapper 대신 실제 consumer graph | Targeted/affected/staged/all-files lane과 직접 negative fixture |

## System Overview & Context

### Authority planes

| Plane | Canonical owner | Consumers and limits |
| --- | --- | --- |
| Agent role/skill machine truth | [Agent Registry](../../../.agents/registry.json) and [schema](../../../.agents/contracts/agent-registry.schema.json) | Current Claude/Codex projections; native discovery와 runtime enforcement는 별도 증거 |
| Human execution policy | [Stage 00](../../00.agent-governance/README.md) | Root/provider gateway, 역할 책임, 승인·품질·문서 authoring; machine schema 복제 금지 |
| Document machine contract and forms | [Stage 99 Registry](../../99.templates/registry.json) and [forms](../../99.templates/README.md) | Profile, route, metadata, identity, lifecycle 및 template consumer |
| Validation dispatch | [Validation Registry](../../../scripts/validation/registry.json) | Local/CI affected-path, lane, argv; validator별 고유 실패 의미는 유지 |
| Execution | [Stage 03](../../03.specs/README.md) | Package-local Spec/Plan/Tasks; 상태·순서·검증 evidence를 중앙 roster로 복제하지 않음 |
| Operations and reference | [Stage 05](../../05.operations/README.md), [Stage 90](../../90.references/README.md) | 운영 절차와 관측 근거 분리; Reference는 승인 또는 현재 정책의 대체물이 아님 |
| Historical recovery | [Stage 98](../../98.archive/README.md) and reachable Git | 봉인 기록과 완료 package; current 실행 authority 또는 재활성화 경로가 아님 |

역할과 surface 수는 Registry에서 도출한다. `.agents`는 공통 machine/asset owner이며
독립 provider-native runtime을 뜻하지 않는다. 과거 local/Antigravity/Gemini proposal은 현재
지원 roster가 아니다. 현재 provider projection 파일은 repository-static configuration이고
인증된 discovery/run을 관측했다는 증거가 아니다.

### Consumer and validation flow

1. 작업은 Stage 00에서 scope·역할·skill·승인 경계를 정하고 package-local Plan/Task로 연결한다.
2. 현재 domain owner와 Registry가 변경의 profile, affected-path 및 필수 lane을 선택한다.
3. 각 validator는 독립 계약을 검사하고 결과·fallback·한계를 해당 증거 class로 남긴다.
4. 검토자는 소비자 승계와 negative fixture를 확인하고 stable staged snapshot을 검증한다.
5. Task가 명령·결과·미완료 owner를 기록한다. 외부 실행은 별도 승인과 관측 없이는 발생하지 않는다.

Aggregate는 Registry의 all-files runner를 호출하는 router이지 두 번째 argv 또는 정책 소유자가 아니다.
문서 Registry, Markdown/profile, link/owner, lifecycle, security, CI와 Archive 검사는 실패 의미가
다르므로 orchestration 통합을 이유로 합치거나 약화하지 않는다.

## Data Architecture

### State, identity and evidence

Role/skill identity는 Agent Registry, 문서 identity/profile/state는 Stage 99, lane/argv는
Validation Registry가 소유한다. 일반 current 문서의 본문 변경은 semantic/profile과 link 검증으로
판정하고 ordinary body를 영구 SHA pin으로 고정하지 않는다. Lifecycle validator는
Registry-classified profile/state/허용 edge를 판정한다.

Risk, tool/data trust, oversight, stop, approval, trace, evaluation과 provenance는
현재 Registry 및 Stage 00 책임에 연결된다. 과거 `agentSystems`/`evidenceOwnerPolicies`
proposal을 구현된 병렬 contract로 주장하지 않는다. 고위험 실행이나 runtime enforcement의
정적 선언은 실행 성공 또는 정책 강제 증거가 아니다.

### Terminal disposition and historical lineage

처분 전에 source → current semantic owner → 모든 current consumer → legal terminal route를 증명한다.
완료 package는 ADR-0032에 따라 동일 document type으로 `completed/<stage>/`에 보관한다.
후계자로 대체된 문서는 `superseded/<stage>/`, 후계자 없이 끝난 문서는 `tombstones/<stage>/`의
non-authoritative record로 구분한다. ADR 본문은 상태에 관계없이 decision log에 남는다.
Record envelope의 original path와 source commit/blob/digest는 정확한 원본을 회복하며
봉인 payload를 현재 링크에 맞추어 편집하지 않는다. Terminal ADR의 원래 문서 인용은
명시적 역사 링크로 유지하고 현재 문서는 record를 실행 authority로 소비하지 않는다.

REQ-0005/0006 → REQ-0008은 원래 supersession 이력이다. REQ-0003은 이 수렴의 transitive
current semantic successor이며 원래 decision target을 바꿔 쓰는 것이 아니다.
Migration은 이 다대일 승계의 고유 mapping을 봉인하며 일반 문서마다 영구 pin을 요구하는 관행으로 확장하지 않는다.

### Loop and checkpoint

[Loop lifecycle contract](../../00.agent-governance/contracts/agent-loop-lifecycle.json)가
retry/recovery 한도, failure signature, no-progress stop과 checkpoint class를 소유한다.
Checkpoint는 ignored transient recovery state이고 정책·Task 또는 credential store를 대체하지 않는다.
Compaction과 resume는 완료/미완료 일·검증 결과·다음 행동만 보존하고 민감정보와 전체 transcript를 배제한다.

## Infrastructure & Deployment

추적된 provider config와 projection은 secret-free repository configuration이다. 사용자 인증 저장소는
읽거나 이관하지 않는다. Native parser와 canary는 해당 provider owner의 독립 evidence lane에서 다루며
hosted CI에 provider credential을 추가하지 않는다.

구현 검증 owner는 [document contracts](../../../scripts/document_contracts.py),
[lifecycle](../../../scripts/document_lifecycle.py),
[Archive recovery](../../../scripts/archive_recovery.py),
[Archive validation](../../../scripts/archive_validation.py)와 Validation Registry가 가리키는 lane이다.
정확한 명령과 tool version은 실행 owner에서 읽고 이 Architecture에 복제하지 않는다.

### Unfinished ownership

Spec 0054 WP-013/TSK-0013은 미완료다. 이 authority 승계는 Stage 99 축소, transition-control 제거,
최종 archive-link/package retention 또는 프로그램 closure를 수행하지 않는다.
Specs 0047..0051의 플랫폼 구현·검증은 [AD-0007](./0007-current-local-gitops-platform.md)의
package별 owner가 보유하며, 이 문서는 공통 라우팅·승인·QA 경계를 제공한다.

## Traceability

### Lifecycle Traceability

| Upstream requirement | Quality attribute or boundary | ADR / Spec |
| --- | --- | --- |
| [REQ-0003-FR-0001](../../01.requirements/0003-workspace-agent-governance-platform.md) | Agent Registry, Stage 00 prose and Stage 99 document-contract authority planes | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [Spec 0054](../../03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |
| [REQ-0003-FR-0002](../../01.requirements/0003-workspace-agent-governance-platform.md) | Thin provider projections with native syntax isolated from shared policy | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [Spec 0054](../../03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |
| [REQ-0003-FR-0003](../../01.requirements/0003-workspace-agent-governance-platform.md) | Skill-source provenance and unavailable-capability boundary | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [Spec 0054](../../03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |
| [REQ-0003-FR-0004](../../01.requirements/0003-workspace-agent-governance-platform.md) | Package-local scope and approval handoff into domain owners | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [Spec 0054](../../03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |
| [REQ-0003-FR-0005](../../01.requirements/0003-workspace-agent-governance-platform.md) | Task-owned durable evidence and ignored transient checkpoint separation | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [Spec 0054](../../03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |
| [REQ-0003-FR-0006](../../01.requirements/0003-workspace-agent-governance-platform.md) | Repository form owner separated from external reference formats | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [Spec 0054](../../03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |
| [REQ-0003-FR-0007](../../01.requirements/0003-workspace-agent-governance-platform.md) | Stage 00 approval gates around secret, external and live execution | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [Spec 0054](../../03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |
| [REQ-0003-FR-0008](../../01.requirements/0003-workspace-agent-governance-platform.md) | Registry-derived provider projection admission | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [Spec 0054](../../03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |
| [REQ-0003-FR-0009](../../01.requirements/0003-workspace-agent-governance-platform.md) | Static provider metadata versus authenticated runtime evidence | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [Spec 0054](../../03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |
| [REQ-0003-FR-0010](../../01.requirements/0003-workspace-agent-governance-platform.md) | Agent Registry ownership of permission, stop and handoff semantics | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [Spec 0054](../../03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |
| [REQ-0003-FR-0011](../../01.requirements/0003-workspace-agent-governance-platform.md) | Loop contract as bounded retry, no-progress and resume owner | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [Spec 0054](../../03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |
| [REQ-0003-FR-0012](../../01.requirements/0003-workspace-agent-governance-platform.md) | Stage 99 machine contract versus Stage 00 authoring policy | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [Spec 0054](../../03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |
| [REQ-0003-FR-0013](../../01.requirements/0003-workspace-agent-governance-platform.md) | One form route per document profile with schema/template parity | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [Spec 0054](../../03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |
| [REQ-0003-FR-0014](../../01.requirements/0003-workspace-agent-governance-platform.md) | Stage-specific purpose boundaries and no parallel Release family | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [Spec 0054](../../03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |
| [REQ-0003-FR-0015](../../01.requirements/0003-workspace-agent-governance-platform.md) | Consumer transfer before source disposition with Git recovery evidence | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [Spec 0054](../../03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |
| [REQ-0003-FR-0016](../../01.requirements/0003-workspace-agent-governance-platform.md) | Validation Registry dispatch and independent validator failure meanings | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [Spec 0054](../../03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |
| [REQ-0003-FR-0017](../../01.requirements/0003-workspace-agent-governance-platform.md) | Independent CI evidence lanes and remote-observation boundary | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [Spec 0054](../../03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |
| [REQ-0003-FR-0018](../../01.requirements/0003-workspace-agent-governance-platform.md) | Exact-diff review and rollback-ready logical delivery units | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [Spec 0054](../../03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |
| [REQ-0003-FR-0019](../../01.requirements/0003-workspace-agent-governance-platform.md) | Package-local sequencing with unchanged historical program lineage | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [Spec 0054](../../03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |
| [REQ-0003-FR-0020](../../01.requirements/0003-workspace-agent-governance-platform.md) | ADR-0032 categorized records and completed-package retention | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [Spec 0054](../../03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |
| [REQ-0003-FR-0021](../../01.requirements/0003-workspace-agent-governance-platform.md) | Reference provenance separated from current execution authority | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [Spec 0054](../../03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |
| [REQ-0003-FR-0022](../../01.requirements/0003-workspace-agent-governance-platform.md) | Ignored checkpoint state versus Task-owned durable execution evidence | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [Spec 0054](../../03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |
| [REQ-0003-FR-0023](../../01.requirements/0003-workspace-agent-governance-platform.md) | Profile-owned stable identity and source-preserving migration mapping | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [Spec 0054](../../03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |
| [REQ-0003-FR-0024](../../01.requirements/0003-workspace-agent-governance-platform.md) | Consumer-zero removal of compatibility surfaces after semantic transfer | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [Spec 0054](../../03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |
| [REQ-0003-FR-0025](../../01.requirements/0003-workspace-agent-governance-platform.md) | Current Agent Registry and Stage 00 risk, trust and approval owners | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [Spec 0054](../../03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |
| [REQ-0003-FR-0026](../../01.requirements/0003-workspace-agent-governance-platform.md) | Separate repository-static, provider-runtime, hosted-CI and live evidence | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [Spec 0054](../../03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |
| [REQ-0003-FR-0027](../../01.requirements/0003-workspace-agent-governance-platform.md) | Lifecycle edges separated from ordinary body edits and sealed integrity | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [Spec 0054](../../03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |
| [REQ-0003-FR-0028](../../01.requirements/0003-workspace-agent-governance-platform.md) | Direct negative fixtures with explicit tool-failure and fallback diagnostics | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [Spec 0054](../../03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |
| [REQ-0003-NFR-0001](../../01.requirements/0003-workspace-agent-governance-platform.md) | Registry-derived admission rather than a frozen role/provider census | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [Spec 0054](../../03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |
| [REQ-0003-NFR-0002](../../01.requirements/0003-workspace-agent-governance-platform.md) | Stable target-path snapshots across focused and aggregate validation lanes | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [Spec 0054](../../03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |
| [REQ-0003-NFR-0003](../../01.requirements/0003-workspace-agent-governance-platform.md) | Primary-source traceability with repository conventions labeled separately | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [Spec 0054](../../03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |
| [REQ-0003-NFR-0004](../../01.requirements/0003-workspace-agent-governance-platform.md) | Explicit baseline-failure and environment-limit reporting | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [Spec 0054](../../03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |
| [REQ-0003-IF-0001](../../01.requirements/0003-workspace-agent-governance-platform.md) | Atomic owner/consumer migration and reciprocal-link validation | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [Spec 0054](../../03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |
| [REQ-0003-IF-0002](../../01.requirements/0003-workspace-agent-governance-platform.md) | External catalog provenance without policy or permission authority | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [Spec 0054](../../03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |

### Architecture responsibility transfer

| Original description | Retained current responsibility | Consumer transfer |
| --- | --- | --- |
| AD-0008 | This AD: document machine owner, form parity, purpose-specific README, affected routing, CI/security and review boundaries | REQ-0003 member-ID map; terminal ADRs retain original decision citations |
| AD-0009 | This AD: lifecycle/profile evidence, legal recovery, package-local lineage, Reference/scratch and non-promotable evidence | REQ-0003 member-ID map; original follow-up and supersession chronology unchanged |
| AD-0011 | This AD: authority planes, stable identity, current taxonomy, validator ownership, consumer-zero and lifecycle/body separation | REQ-0003 and Spec 0054; original Spec 0052 history preserved |
| AD-0010, shared assurance boundary | This AD: validation routing, CI/QA, approval and direct negative tests; AD-0007 retains platform-specific design | REQ-0003/0004 explicit member transfer and Specs 0047..0051 |

The replacement record and this responsibility table express semantic succession, not a new claim that historical
ADRs originally served this AD. Original ADR bodies and reciprocal decision supersession remain in the decision log.
