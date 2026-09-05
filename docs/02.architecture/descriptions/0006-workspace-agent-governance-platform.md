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
[ADR-0034](../decisions/0034-stage-00-governance-and-unified-quality-gates.md)가
공통 거버넌스 설계를, [SPEC-0072](../../03.specs/0072-agent-governance-and-quality-gate-consolidation/spec.md)가
전환과 수용 조건을 소유하며, [Spec 0054](../../03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md)는
더 넓은 미완료 문서 수렴을 소유한다.

### Convergence boundaries

이 문서는 소유 경계, 흐름, 증거 class 및 품질 속성을 소유한다. Machine route·schema·state enum,
역할 roster, validator argv와 작업 상태는 아래 canonical owner를 참조하며 복제하지 않는다.
GitOps desired state와 플랫폼 interface는 [AD-0007](./0007-current-local-gitops-platform.md)가 소유한다.
외부 계정·credential·provider capability 및 live runtime은 이 문서의 구현 증거가 아니다.
별도 governance registry, provider별 정책 fork, Release family 또는 shared progress ledger를 만들지 않는다.

### Convergence quality attributes

| Attribute | Boundary | Evidence |
| --- | --- | --- |
| Consistency | 책임별 단일 machine/prose owner와 thin projection | Registry/schema, profile, owner 및 adapter parity |
| Verifiability | Repository-static, provider-runtime, hosted-CI, remote/live 분리 | Class별 직접 관측; 미관측은 owner와 retry trigger |
| Reliability | 제한된 retry와 no-progress stop, 안전한 resume | Loop contract 및 positive/negative recovery fixture |
| Security | 최소 권한과 승인 경계; 비밀정보·auth·전체 transcript 배제 | Static guardrail과 독립 review; 실행 권한은 별도 승인 |
| Recoverability | 일반 변경의 Git 복구와 봉인 evidence 무결성 분리 | Consumer 승계, source commit/blob/digest 및 legal lifecycle edge |
| Maintainability | 고정 census나 중복 wrapper 대신 실제 consumer graph | Targeted/affected/staged/all-files lane과 직접 negative fixture |

### Convergence authority context

### Authority planes

| Plane | Canonical owner | Consumers and limits |
| --- | --- | --- |
| Agent role/skill machine truth | [공통 거버넌스 role registry](../../../.agents/roles/registry.json) and adjacent schema | Current Claude/Codex projections; native discovery와 runtime enforcement는 별도 증거 |
| Human execution policy | [Common governance](../../../.agents/README.md) | Root/provider gateway, 역할 책임, 승인·품질·문서 authoring; machine schema 복제 금지 |
| Document machine contract and forms | [Stage 99 Registry](../../99.templates/registry.json) and [forms](../../99.templates/README.md) | Profile, route, metadata, identity, lifecycle 및 template consumer |
| Validation dispatch | [Validation Registry](../../../scripts/validation/registry.json) | Local/CI affected-path, lane, argv; validator별 고유 실패 의미는 유지 |
| Execution | [Stage 03](../../03.specs/README.md) | Package-local Spec/Plan/Tasks; 상태·순서·검증 evidence를 중앙 roster로 복제하지 않음 |
| Operations and reference | [Stage 05](../../05.operations/README.md), [Stage 90](../../90.references/README.md) | 운영 절차와 관측 근거 분리; Reference는 승인 또는 현재 정책의 대체물이 아님 |
| Historical recovery | [Stage 98](../../98.archive/README.md) and reachable Git | 봉인 기록과 완료 package; current 실행 authority 또는 재활성화 경로가 아님 |

역할과 surface 수는 공통 거버넌스 registry에서 도출한다. 과거 local/Antigravity/Gemini proposal은 현재
지원 roster가 아니며, `.agents` compatibility surface는 현재 owner가 아니다. 현재 provider projection 파일은 repository-static configuration이고
인증된 discovery/run을 관측했다는 증거가 아니다.

### Consumer and validation flow

1. 작업은 공통 거버넌스에서 scope·역할·skill·승인 경계를 정하고 package-local Plan/Task로 연결한다.
2. 현재 domain owner와 Registry가 변경의 profile, affected-path 및 필수 lane을 선택한다.
3. 각 validator는 독립 계약을 검사하고 결과·fallback·한계를 해당 증거 class로 남긴다.
4. 검토자는 소비자 승계와 negative fixture를 확인하고 stable staged snapshot을 검증한다.
5. Task가 명령·결과·미완료 owner를 기록한다. 외부 실행은 별도 승인과 관측 없이는 발생하지 않는다.

Aggregate는 Registry의 all-files runner를 호출하는 router이지 두 번째 argv 또는 정책 소유자가 아니다.
문서 Registry, Markdown/profile, link/owner, lifecycle, security, CI와 Archive 검사는 실패 의미가
다르므로 orchestration 통합을 이유로 합치거나 약화하지 않는다.

### Convergence data architecture

### State, identity and evidence

Role/skill identity는 공통 거버넌스 registry, 문서 identity/profile/state는 Stage 99, lane/argv는
Validation Registry가 소유한다. 일반 current 문서의 본문 변경은 semantic/profile과 link 검증으로
판정하고 ordinary body를 영구 SHA pin으로 고정하지 않는다. Lifecycle validator는
Registry-classified profile/state/허용 edge를 판정한다.

Risk, tool/data trust, oversight, stop, approval, trace, evaluation과 provenance는
현재 Registry 및 공통 거버넌스 책임에 연결된다. 과거 `agentSystems`/`evidenceOwnerPolicies`
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

[bounded validation runner](../../../scripts/run-validation-lane.py)가
timeout·출력·자식 정리 한도를 소유하고, Task가 no-progress stop과 handoff evidence를 소유한다.
Checkpoint는 ignored transient recovery state이고 정책·Task 또는 credential store를 대체하지 않는다.
Compaction과 resume는 완료/미완료 일·검증 결과·다음 행동만 보존하고 민감정보와 전체 transcript를 배제한다.

### Convergence infrastructure and deployment

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
이 문서는 공통 거버넌스, Claude/Codex 어댑터, 공통 QA와 GitOps 운영의
책임 경계를 설명한다. [ADR-0034](../decisions/0034-stage-00-governance-and-unified-quality-gates.md)가
설계를, [SPEC-0072](../../03.specs/0072-agent-governance-and-quality-gate-consolidation/spec.md)가
전환과 수용 조건을 소유한다. 파일의 존재는 설치된 런타임의 탐색·권한 강제나
호스팅 CI의 성공을 입증하지 않는다. 실제 검증 상태는 해당 Task에서 확인한다.

## Boundaries & Non-goals

- 공통 거버넌스은 공통 정책·역할·스킬 의미와 역할 메타데이터를 소유한다.
- Stage 99는 문서 프로필과 양식을 소유하며 역할 권한이나 실행 성공을 정의하지 않는다.
- 실행 레지스트리와 scripts는 검사 선택, 실행 한도, 실패 처리를 소유한다.
- Provider 계정·인증·모델 접근 권한과 전역 설치는 저장소가 소유하지 않는다.
- GitOps desired state, Kubernetes 정책, 외부 서비스 인터페이스는 기존 도메인에 둔다.

## Quality Attributes

| Attribute | Architecture requirement | Evidence |
| --- | --- | --- |
| Consistency | Common meaning and machine field each have one owner | Role/schema/reference checks and profile routing |
| Security | Native permissions do not exceed registered scope; external mutation needs approval | Independent permission/path rejection tests and native evidence when authorized |
| Reliability | Commands have finite time/output limits and descendant cleanup | Bounded-runner timeout, overflow, cancellation, and pipe regressions |
| Recoverability | Work evidence preserves inputs, failures, ownership, and next action | Task/Git trace; isolated archive recovery checks |
| Reproducibility | Local full and CI share logical gates and configuration | Profile parity, single execution, interpreter and dependency checks |
| Legibility | Gateways point to common owners without copied policy bodies | Native syntax parse and canonical-reference tests |

## System Overview & Context

| Component | Canonical owner | Responsibility |
| --- | --- | --- |
| Entry | Root `AGENTS.md` and `CLAUDE.md` | Explicitly select common policy and relevant procedures |
| Policy | `.agents/governance/` | Approval, security, Git, document and quality meaning |
| Role metadata | `.agents/roles/registry.json` and adjacent schema | Stable IDs, permissions, handoffs, skill and adapter references |
| Role bodies and procedures | `.agents/roles/` and `.agents/skills/` | Neutral responsibilities and reusable work steps |
| Provider contract | `.claude/provider.md` and `.codex/provider.md` | Supported native syntax, loading route, and evidence limits |
| Native adapters | `.claude/` and `.codex/` | Native metadata and explicit common references |
| QA execution | `scripts/qa.py`, validation registry and bounded runner | Profile selection, one execution per gate/input, fail-closed results |
| Change evidence | Stage 03 Task and Git | Actual commands, scope, failures, limitations and handoff |

Claude exposes common `SKILL.md` packages through one relative link per skill.
Codex discovers the packages under `.agents/skills/`; both providers require
explicit invocation. Root instructions also require reading the selected role
and its common procedures. No provider generator or compatibility skill copy
is needed. A native hook is registered only for an actual supported event;
routine tool completion does not invoke whole-repository QA. ADR-0035 owns the
current authority location; ADR-0034's QA/CD boundary remains effective.

## Data Architecture

Role metadata references canonical role bodies and skill IDs; it does not copy
policy prose. Provider files retain native format and model bindings. Static
metadata validation cannot prove account availability or authenticated execution.

QA profiles contain gate IDs. The execution registry alone owns commands and
selection configuration; the runner owns bounded process handling. Quick checks
working-tree changes, full checks the final working tree, and staged validation
checks the real index in an isolated snapshot. CI checks its immutable checkout.
Snapshot preparation preserves Git history for recovery while keeping the user's
index and working files unchanged.

Historical facts remain in Git or isolated retained records. Active policy,
provider loading, and command selection do not consume a retired proposal as
current authority. Test fixtures are bounded synthetic inputs, never production
configuration or runtime admission evidence.

## Infrastructure & Deployment

GitHub Actions validates repository bytes through the common QA entrypoint.
`ci-summary` retains its externally observed check name and propagates failure,
cancellation, missing results, and unexpected skips. Static QA uses pinned tools
and minimal permissions; it does not need provider credentials or a cluster.

Argo CD reconciles `gitops/` desired state within the existing operating boundary.
`infrastructure/` supplies bootstrap support, `traefik/` carries integration
references, and `examples/` contains examples. `policy/` is Kubernetes
Conftest/Rego policy, separate from common agent policy. External Vault,
PostgreSQL, and Valkey remain interface contracts, not services operated by QA.

A local commit does not authorize push, PR creation, workflow dispatch, release,
cluster mutation, or external service changes. Hosted, native provider, and live
verification require their own actual evidence and applicable authorization.

## Traceability

### Lifecycle Traceability

| Upstream requirement | Quality attribute or boundary | ADR / Spec |
| --- | --- | --- |
| [REQ-0003-FR-0001](../../01.requirements/0003-workspace-agent-governance-platform.md) | Agent Registry, 공통 거버넌스 prose and Stage 99 document-contract authority planes | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [Spec 0054](../../03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |
| [REQ-0003-FR-0002](../../01.requirements/0003-workspace-agent-governance-platform.md) | Thin provider projections with native syntax isolated from shared policy | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [Spec 0054](../../03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |
| [REQ-0003-FR-0003](../../01.requirements/0003-workspace-agent-governance-platform.md) | Skill-source provenance and unavailable-capability boundary | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [Spec 0054](../../03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |
| [REQ-0003-FR-0004](../../01.requirements/0003-workspace-agent-governance-platform.md) | Package-local scope and approval handoff into domain owners | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [Spec 0054](../../03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |
| [REQ-0003-FR-0005](../../01.requirements/0003-workspace-agent-governance-platform.md) | Task-owned durable evidence and ignored transient checkpoint separation | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [Spec 0054](../../03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |
| [REQ-0003-FR-0006](../../01.requirements/0003-workspace-agent-governance-platform.md) | Repository form owner separated from external reference formats | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [Spec 0054](../../03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |
| [REQ-0003-FR-0007](../../01.requirements/0003-workspace-agent-governance-platform.md) | 공통 거버넌스 approval gates around secret, external and live execution | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [Spec 0054](../../03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |
| [REQ-0003-FR-0008](../../01.requirements/0003-workspace-agent-governance-platform.md) | Registry-derived provider projection admission | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [Spec 0054](../../03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |
| [REQ-0003-FR-0009](../../01.requirements/0003-workspace-agent-governance-platform.md) | Static provider metadata versus authenticated runtime evidence | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [Spec 0054](../../03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |
| [REQ-0003-FR-0010](../../01.requirements/0003-workspace-agent-governance-platform.md) | Agent Registry ownership of permission, stop and handoff semantics | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [Spec 0054](../../03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |
| [REQ-0003-FR-0011](../../01.requirements/0003-workspace-agent-governance-platform.md) | Loop contract as bounded retry, no-progress and resume owner | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [Spec 0054](../../03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |
| [REQ-0003-FR-0012](../../01.requirements/0003-workspace-agent-governance-platform.md) | Stage 99 machine contract versus 공통 거버넌스 authoring policy | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [Spec 0054](../../03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |
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
| [REQ-0003-FR-0025](../../01.requirements/0003-workspace-agent-governance-platform.md) | Current Agent Registry and 공통 거버넌스 risk, trust and approval owners | [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md), [Spec 0054](../../03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |
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
The existing requirement IDs retain their identity. ADR-0034 and SPEC-0072
own the current governance and QA implementation; predecessor decisions remain
historical evidence rather than parallel operating instructions.

| Upstream requirement | Quality attribute or boundary | ADR / Spec |
| --- | --- | --- |
| [REQ-0003-FR-0001](../../01.requirements/0003-workspace-agent-governance-platform.md) | 공통 거버넌스 durable policy와 owner graph | [ADR 0034](../decisions/0034-stage-00-governance-and-unified-quality-gates.md) |
| [REQ-0003-FR-0002](../../01.requirements/0003-workspace-agent-governance-platform.md) | Thin gateway와 provider projection | [ADR 0034](../decisions/0034-stage-00-governance-and-unified-quality-gates.md) |
| [REQ-0003-FR-0003](../../01.requirements/0003-workspace-agent-governance-platform.md) | Skill provenance와 gap evidence | [ADR 0034](../decisions/0034-stage-00-governance-and-unified-quality-gates.md) |
| [REQ-0003-FR-0004](../../01.requirements/0003-workspace-agent-governance-platform.md) | Strategy axis와 scope owner | [ADR 0034](../decisions/0034-stage-00-governance-and-unified-quality-gates.md) |
| [REQ-0003-FR-0005](../../01.requirements/0003-workspace-agent-governance-platform.md) | Execution/checkpoint/handoff evidence | [ADR 0034](../decisions/0034-stage-00-governance-and-unified-quality-gates.md) |
| [REQ-0003-FR-0006](../../01.requirements/0003-workspace-agent-governance-platform.md) | Form/profile와 routing contract | [ADR 0034](../decisions/0034-stage-00-governance-and-unified-quality-gates.md) |
| [REQ-0003-FR-0007](../../01.requirements/0003-workspace-agent-governance-platform.md) | GitOps, secret, privilege와 approval boundary | [ADR 0034](../decisions/0034-stage-00-governance-and-unified-quality-gates.md) |
| [REQ-0003-FR-0008](../../01.requirements/0003-workspace-agent-governance-platform.md) | Registry-derived admitted-provider projection | [ADR 0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md) |
| [REQ-0003-FR-0009](../../01.requirements/0003-workspace-agent-governance-platform.md) | Provider schema/model/effort/MCP와 canary | [ADR 0034](../decisions/0034-stage-00-governance-and-unified-quality-gates.md) |
| [REQ-0003-FR-0010](../../01.requirements/0003-workspace-agent-governance-platform.md) | Machine harness contract/schema | [ADR 0034](../decisions/0034-stage-00-governance-and-unified-quality-gates.md) |
| [REQ-0003-FR-0011](../../01.requirements/0003-workspace-agent-governance-platform.md) | Bounded loop/checkpoint/compaction | [ADR 0034](../decisions/0034-stage-00-governance-and-unified-quality-gates.md) |
| [REQ-0003-NFR-0001](../../01.requirements/0003-workspace-agent-governance-platform.md) | Registry-derived parity and eval/admission | [ADR 0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md) |
| [REQ-0003-NFR-0002](../../01.requirements/0003-workspace-agent-governance-platform.md) | CI/QA/all-files evidence | [ADR 0034](../decisions/0034-stage-00-governance-and-unified-quality-gates.md) |
| [REQ-0003-IF-0001](../../01.requirements/0003-workspace-agent-governance-platform.md) | Legacy cutover/current-owner integrity | [ADR 0034](../decisions/0034-stage-00-governance-and-unified-quality-gates.md) |
| [REQ-0003-IF-0002](../../01.requirements/0003-workspace-agent-governance-platform.md) | Evidence-only external role admission | [ADR 0034](../decisions/0034-stage-00-governance-and-unified-quality-gates.md) |
| N/A — [Acceptance criterion 01](../../01.requirements/0003-workspace-agent-governance-platform.md) remains package-owned | Owner graph consistency | [ADR 0034](../decisions/0034-stage-00-governance-and-unified-quality-gates.md) |
| N/A — [Acceptance criterion 02](../../01.requirements/0003-workspace-agent-governance-platform.md) remains package-owned | Reciprocal lifecycle chain | [ADR 0034](../decisions/0034-stage-00-governance-and-unified-quality-gates.md) |
| N/A — [Acceptance criterion 03](../../01.requirements/0003-workspace-agent-governance-platform.md) remains package-owned | Gateway/evidence-class separation | [ADR 0034](../decisions/0034-stage-00-governance-and-unified-quality-gates.md) |
| N/A — [Acceptance criterion 04](../../01.requirements/0003-workspace-agent-governance-platform.md) remains package-owned | Repository static gate | [ADR 0034](../decisions/0034-stage-00-governance-and-unified-quality-gates.md) |
| N/A — [Acceptance criterion 05](../../01.requirements/0003-workspace-agent-governance-platform.md) remains package-owned | Template form authority | [ADR 0034](../decisions/0034-stage-00-governance-and-unified-quality-gates.md) |
| N/A — [Acceptance criterion 06](../../01.requirements/0003-workspace-agent-governance-platform.md) remains package-owned | Registry-derived role/provider parity | [ADR 0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md) |
| N/A — [Acceptance criterion 07](../../01.requirements/0003-workspace-agent-governance-platform.md) remains package-owned | Admitted-provider independent canary classification and readiness evidence | [ADR 0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md) |
| N/A — [Acceptance criterion 08](../../01.requirements/0003-workspace-agent-governance-platform.md) remains package-owned | Contract/schema/provider parity | [ADR 0034](../decisions/0034-stage-00-governance-and-unified-quality-gates.md) |
| N/A — [Acceptance criterion 09](../../01.requirements/0003-workspace-agent-governance-platform.md) remains package-owned | Recovery fixture and safe resume | [ADR 0034](../decisions/0034-stage-00-governance-and-unified-quality-gates.md) |
| N/A — [Acceptance criterion 10](../../01.requirements/0003-workspace-agent-governance-platform.md) remains package-owned | Eval/model-fitness evidence | [ADR 0034](../decisions/0034-stage-00-governance-and-unified-quality-gates.md) |
| N/A — [Acceptance criterion 11](../../01.requirements/0003-workspace-agent-governance-platform.md) remains package-owned | CI and all-files gate | [ADR 0034](../decisions/0034-stage-00-governance-and-unified-quality-gates.md) |
| N/A — [Acceptance criterion 12](../../01.requirements/0003-workspace-agent-governance-platform.md) remains package-owned | Zero stale legacy/orphan reference | [ADR 0034](../decisions/0034-stage-00-governance-and-unified-quality-gates.md) |

- **Requirement Package**: [REQ-0003](../../01.requirements/0003-workspace-agent-governance-platform.md)
- **Current decision**: [ADR-0034](../decisions/0034-stage-00-governance-and-unified-quality-gates.md)
- **Current implementation**: [SPEC-0072](../../03.specs/0072-agent-governance-and-quality-gate-consolidation/spec.md)
- **Wider SDLC program**: [SPEC-0054](../../03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md)
- **Historical decisions**: [ADR-0019](../decisions/0019-provider-native-agent-harness-and-loop-model.md), [ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md)

The prior architecture narrative is recoverable from this same path at commit
`bb73116b7b09c4f257fc81baa12cfa8359495fc0`. Its retired providers, fixed retry
counts, synthetic runtime records, and separate agent CI topology are not
current contracts.
