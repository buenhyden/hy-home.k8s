---
title: "Workspace Agent and Document Governance Requirements"
version: "1.0.0"
type: "sdlc/requirement"
status: "active"
owner: "platform"
updated: "2026-09-05"
layer: "requirements"
artifact_id: "REQ-0003"
---

# Workspace Agent and Document Governance Requirements

## Overview

이 문서는 Agent 실행과 문서 거버넌스의 현재 사용자 요구를 소유한다. 역할·skill의 machine truth는
[Agent Registry](../../.agents/registry.json), 사람용 실행 규칙은 [Stage 00](../00.agent-governance/README.md),
문서 형식은 [Stage 99](../99.templates/README.md), 구현과 미완료 수렴은
[Spec 0054](../03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md)가 소유한다.
이 Requirement는 구현 inventory, provider roster 또는 일회성 migration 계획의 복제본이 아니다.

## Vision

운영자는 작업의 책임, 허용 범위, 현재 문서 권위와 실제 증거 깊이를 일관되게 판단하고
검토 가능한 변경을 안전하게 재개할 수 있어야 한다.

## Problem Statement

정책·machine contract·실행 이력을 여러 문서에 복제하면 현재 지원과 미완료 작업의 경계가 갈라진다.
정적 선언을 runtime 증거로 오인하거나 과거 프로그램 숫자를 현재 admission 기준으로 쓰지 않아야 한다.

## Personas

- Maintainer: 중복 없는 owner와 복구 가능한 변경을 관리한다.
- Agent operator와 implementer: 승인·stop·handoff 경계를 지키며 작업한다.
- Reviewer와 quality engineer: 역할을 분리해 계약, 실패 의미 및 증거 깊이를 검토한다.

## Key Use Cases

- 작업자가 현재 Registry와 실행 정책에서 역할·skill·승인 owner를 찾는다.
- 실패한 작업이 민감정보 없는 checkpoint와 제한된 retry 후 안전하게 중지·재개한다.
- 문서 변경자가 현재 소비자를 승계하고 결정 이력·봉인 증거를 보존한다.
- 검토자가 로컬 정적 결과와 외부 관측을 구분하고 미완료 작업을 다음 Task에 연결한다.

## Functional Requirements

- **REQ-0003-FR-0001**: 공통 Agent, Skill, Rule, Hook, Workflow, checkpoint, QA와 문서 정책은 책임별로 하나의 current owner를 가져야 한다.
- **REQ-0003-FR-0002**: Provider gateway와 adapter는 공통 정책을 복제하지 않고 native syntax와 capability 차이만 표현해야 한다.
- **REQ-0003-FR-0003**: Skill provenance는 repo-local, shared, provider-native 및 명시적 외부 요청을 구분하고 누락을 실행 가능한 것으로 추정하지 않아야 한다.
- **REQ-0003-FR-0004**: 작업은 process, branch, 문서, QA, DevOps, CI/CD, security와 Kubernetes의 관련 scope 및 승인 owner에 연결되어야 한다.
- **REQ-0003-FR-0005**: 저장소 변경의 Plan/Task handoff는 실행 명령, 결과, 한계, 남은 작업과 승인 경계를 기록해야 한다.
- **REQ-0003-FR-0006**: 문서의 목적과 형식은 해당 repository form owner를 따라야 하며 외부 형식을 별도 승인 없이 대체 권위로 사용하지 않아야 한다.
- **REQ-0003-FR-0007**: 최소 권한, 비밀정보 비노출, GitOps-first 및 외부·live·파괴적 작업의 명시적 승인 경계를 보존해야 한다.
- **REQ-0003-FR-0008**: 현재 허용된 provider surface만 투영하고 planned 또는 absent surface를 현재 지원으로 계산하지 않아야 한다.
- **REQ-0003-FR-0009**: Provider-native metadata와 repository 문서 형식을 구분하고 정적 형식 적합성을 discovery, 인증 또는 runtime enforcement 증거로 승격하지 않아야 한다.
- **REQ-0003-FR-0010**: 역할과 skill의 machine registry는 semantic, projection, permission, stop, handoff와 검증 책임을 하나의 소유 경계에서 정의해야 한다.
- **REQ-0003-FR-0011**: Agent 반복 실행은 bounded retry, no-progress stop, 안전한 checkpoint·compaction·resume와 escalation을 제공해야 하며 한도는 loop contract가 소유해야 한다.
- **REQ-0003-FR-0012**: 문서 route, profile, metadata, 형식 및 lifecycle edge는 단일 문서 machine owner가 정의하고 prose policy는 책임별 owner에만 있어야 한다.
- **REQ-0003-FR-0013**: 물리적 문서 form은 정확히 하나의 profile에 대응하며 template와 validator가 일치해야 한다.
- **REQ-0003-FR-0014**: Requirement, Architecture, Spec/Plan/Task, 운영 문서, Reference 및 README는 각 목적을 지키고 실행 세부나 관측하지 않은 운영 증거를 상위 문서에 복제하지 않아야 한다. Stage 05의 위치를 유지하고 이 수렴에서 Release family를 만들지 않는다.
- **REQ-0003-FR-0015**: 문서 처분은 고유한 현재 의미와 소비자를 먼저 승계하고 관측 사실·원본 Git 복구를 보존한 뒤 검토된 범위에서 수행해야 한다.
- **REQ-0003-FR-0016**: Affected-path, lane 및 argv 라우팅에는 단일 machine owner가 있어야 하며 독립 계약을 검사하는 validator의 실패 의미를 합치지 않아야 한다.
- **REQ-0003-FR-0017**: CI는 의도된 독립 evidence lane, 누락 없는 aggregate verdict, 최소 권한, immutable 외부 Action 식별자와 artifact 보존 경계를 유지해야 한다. 로컬 검증을 hosted 실행으로 보고하지 않는다.
- **REQ-0003-FR-0018**: 변경은 논리적 커밋, 독립 검토, 비례적인 전체 검증과 되돌릴 수 있는 경계로 전달해야 한다.
- **REQ-0003-FR-0019**: 실행 상태와 순서는 package-local Plan/Task가 소유하고 원래 tranche·follow-up·승계 이력을 왜곡하거나 영구 중앙 roster로 복제하지 않아야 한다.
- **REQ-0003-FR-0020**: 완료 package, 후계자로 대체된 문서, 후계자 없이 끝난 문서를 실제 lifecycle에 따라 구분하고 선언된 봉인 원본·provenance를 보존해야 한다. ADR 본문은 decision log에 남고 기록은 current authority나 재활성화 입력이 될 수 없다.
- **REQ-0003-FR-0021**: Audit, research, data, generated output 및 학습 자료는 근거·관측 시점·소유자를 명시하고 현재 정책 또는 실행 승인의 대체물이 되지 않아야 한다.
- **REQ-0003-FR-0022**: Scratch와 checkpoint는 제한된 비밀정보 없는 임시 상태로 유지하고 durable 실행 증거는 Task에 남겨야 한다. 제거된 공유 progress ledger를 새 current owner로 복원하지 않는다.
- **REQ-0003-FR-0023**: 안정적인 문서 identity와 semantic filename을 유지하고 mandatory/excluded profile의 identity 규칙, 유일성 및 경로 대응을 검증해야 한다. 기존 결정 이력의 식별자를 재할당하지 않는다.
- **REQ-0003-FR-0024**: Compatibility, wrapper 또는 script는 실제 소비자와 고유 rule·negative fixture가 있을 때만 유지하고 승계 증거와 consumer-zero 후 제거해야 한다.
- **REQ-0003-FR-0025**: Agent 시스템의 risk, tool/data trust, oversight, stop, approval, trace, evaluation 및 component provenance 의무는 현재 Registry와 Stage 00 owner에서 구현·검증해야 한다. 정적 선언은 runtime enforcement를 증명하지 않는다.
- **REQ-0003-FR-0026**: Repository-declared, provider-runtime, hosted-CI 및 승인된 remote/live 증거를 분리하고 관측 없이 서로 승격하지 않아야 한다.
- **REQ-0003-FR-0027**: Lifecycle 검증은 profile, state 및 허용 edge를 판정하고 일반 본문 정정·소비자 승계는 semantic/link 검증과 검토된 Git 복구로 판정해야 한다. 봉인 Archive의 무결성 검사는 별도로 유지한다.
- **REQ-0003-FR-0028**: Malformed input, 도구 부재, fallback, 위험 경로와 금지 동작에는 결정적인 직접 negative test가 있어야 하며 required-tool 실패를 diagnostic SKIP으로 숨기지 않아야 한다.
- **REQ-0003-NFR-0001**: Roster와 adapter 수는 현재 Registry에서 도출하고 역할·surface admission과 model fitness는 local need, 최소 권한 및 평가 근거로 정당화해야 한다.
- **REQ-0003-NFR-0002**: Targeted, affected, staged, 전체 unit, all-files 및 formatter/diff 재검증은 같은 필수 계약을 검사하면서 각각의 결과와 변경 스냅샷을 기록해야 한다.
- **REQ-0003-NFR-0003**: 문서 형식과 변경 판단은 해당 일차 근거, 적용 범위 및 검증 증거로 추적 가능해야 하며 외부 표준과 repository convention을 혼동하지 않아야 한다.
- **REQ-0003-NFR-0004**: 발견된 baseline 결함은 계약을 약화하지 않고 처리하며 false positive 판정·환경 제한·미해결 실패를 성공으로 숨기지 않아야 한다.
- **REQ-0003-IF-0001**: Migration은 current owner 전환, 상호 링크, stale claim과 orphan consumer 정리를 같은 검토 단위에서 제공해야 한다.
- **REQ-0003-IF-0002**: 외부 역할 catalog는 아이디어의 provenance일 뿐 admission 또는 정책 권위가 아니어야 한다.

## Success / Acceptance Criteria

아래 Lifecycle Traceability의 각 member는 연결된 Architecture와 구현 owner의 해당 검증으로 판정한다.
Current role/skill projection, 문서 route·identity·lifecycle, consumer ownership, bounded loop 및
보호된 QA 계약은 positive/negative fixtures로 검증한다. Provider-runtime와 hosted/live 결과는
해당 관측 없이는 PASS로 보고하지 않으며 limitation은 owner와 재시도 조건을 가진다.

- **Acceptance criterion 01**: 공통 정책, machine contract와 실행 evidence의 owner graph가 연결된다.
- **Acceptance criterion 02**: REQ-0003, AD-0006, current ADR와 승인된 Spec/Plan/Task의 trace가 유지된다.
- **Acceptance criterion 03**: Gateway는 thin projection이고 native/static/runtime 증거를 구분한다.
- **Acceptance criterion 04**: 해당 repository static quality gate가 변경 후 통과한다.
- **Acceptance criterion 05**: Repository form owner를 승인 없는 외부 형식이 대체하지 않는다.
- **Acceptance criterion 06**: 현재 Registry에서 도출한 role·surface projection이 일치한다.
- **Acceptance criterion 07**: Provider readiness는 해당 secret-free canary PASS로만 판정하고 ABSENT/DEFER는 한계·owner·retry trigger를 가진다.
- **Acceptance criterion 08**: Machine schema, metadata와 projection의 일관성이 검증된다.
- **Acceptance criterion 09**: Recovery fixture가 retry, stop, checkpoint·compaction·resume와 민감정보 배제를 검증한다.
- **Acceptance criterion 10**: 역할의 input/output, permission, stop, handoff, eval 및 model fitness 근거가 존재한다.
- **Acceptance criterion 11**: 필수 local/CI lane과 전체 QA, formatter·diff 재검증 결과가 추적 가능하다.
- **Acceptance criterion 12**: 현재 surface에 중복 권위·stale claim·orphan consumer가 없고 실제 runtime 한계는 보존된다.

## Scope and Non-goals

현재 owner 경계, 승인, 문서 lifecycle, 검증 책임과 실행 handoff가 범위다.
새 provider admission, 외부 역할 catalog vendoring, 비밀정보 수집, live 변경 또는 Release family 신설은 범위가 아니다.
제거된 공유 progress ledger와 과거 proposal의 `agentSystems`/`evidenceOwnerPolicies`를
현재 구현으로 주장하거나 새 병렬 registry로 복원하지 않는다. FR-0025의 지속 의무는 현재 owner에서 검증한다.

## Risks, Dependencies, and Assumptions

구체 provider/model 가용성과 인증 증거는 해당 owner가 갱신한다. 정적 파일은 runtime discovery가 아니다.
역할 수, provider 수, retry 상수와 validator argv는 이 문서에 별도 고정하지 않는다.
[ADR-0030](../02.architecture/decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md),
[ADR-0031](../02.architecture/decisions/0031-current-corpus-retention-and-validation-ownership.md),
[ADR-0032](../02.architecture/decisions/0032-completed-and-terminal-document-retention.md)의 현재 경계를 따른다.

### Agent execution and approval requirements

- **Allowed Actions**: Inspect current owners, edit approved repository scope, and run non-destructive local validation.
- **Disallowed Actions**: Read secret values, invent runtime evidence, restore obsolete governance owners, or mutate external/live systems without approval.
- **Human-in-the-loop Requirement**: Obtain approval for destructive Git, external actions, provider authentication, deployment, or secret handling.
- **Evaluation Expectation**: Preserve independent review, stable-snapshot validation results, failure limitations, and package-local unfinished ownership.

### Unfinished execution and original lineage

Spec 0054의 WP-013과 TSK-0013은 여전히 미완료다. Stage 99 축소, transition control 처분 및
최종 package retention은 이 요구 승계로 완료되지 않는다.
[Spec 0047](../03.specs/0047-current-surface-and-stash-reconciliation/spec.md)은 재개 경로가 활성화되었지만
구현 Tasks는 미완료이며, [0048](../03.specs/0048-github-routing-and-ci-evidence/spec.md),
[0049](../03.specs/0049-platform-validation-and-security-evidence/spec.md),
[0050](../03.specs/0050-example-iac-and-validator-qa/spec.md),
[0051](../03.specs/0051-repository-assurance-integration-and-closure/spec.md)은 선행 증거에 따른 순차 실행을 기다린다.
플랫폼별 의무는 [REQ-0004](./0004-current-local-gitops-platform.md)가 함께 소유한다.

원래 REQ-0005/0006은 REQ-0008로 대체되었다. 현재 의미는 이 문서로 다시 승계되지만
원래 결정이 REQ-0003을 위해 작성되었다는 뜻은 아니다. 과거 고정 tranche/corpus 수,
Spec 033의 follow-up 구분, ARD→AD identity 변환은 역사이며 현재 roster 규칙이 아니다.
REQ-0006의 Plan/Task-only retention과 REQ-0008의 모든 Stage 98 링크 금지는 ADR-0032의
package retention 및 명시적 역사 인용 경계로 대체된다. 봉인 record는 계속 current authority가 아니다.

## Traceability

### Lifecycle Traceability

| Requirement ID | Acceptance criterion | Downstream owner |
| --- | --- | --- |
| REQ-0003-FR-0001 | 공통 Agent, Skill, Rule, Hook, Workflow, checkpoint, QA와 문서 정책은 책임별로 하나의 current owner를 가져야 한다. 충족 여부를 해당 owner의 정적 검증과 별도 관측 증거로 판정한다. | [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-FR-0002 | Provider gateway와 adapter는 공통 정책을 복제하지 않고 native syntax와 capability 차이만 표현해야 한다. 충족 여부를 해당 owner의 정적 검증과 별도 관측 증거로 판정한다. | [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-FR-0003 | Skill provenance는 repo-local, shared, provider-native 및 명시적 외부 요청을 구분하고 누락을 실행 가능한 것으로 추정하지 않아야 한다. 충족 여부를 해당 owner의 정적 검증과 별도 관측 증거로 판정한다. | [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-FR-0004 | 작업은 process, branch, 문서, QA, DevOps, CI/CD, security와 Kubernetes의 관련 scope 및 승인 owner에 연결되어야 한다. 충족 여부를 해당 owner의 정적 검증과 별도 관측 증거로 판정한다. | [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-FR-0005 | 저장소 변경의 Plan/Task handoff는 실행 명령, 결과, 한계, 남은 작업과 승인 경계를 기록해야 한다. 충족 여부를 해당 owner의 정적 검증과 별도 관측 증거로 판정한다. | [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-FR-0006 | 문서의 목적과 형식은 해당 repository form owner를 따라야 하며 외부 형식을 별도 승인 없이 대체 권위로 사용하지 않아야 한다. 충족 여부를 해당 owner의 정적 검증과 별도 관측 증거로 판정한다. | [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-FR-0007 | 최소 권한, 비밀정보 비노출, GitOps-first 및 외부·live·파괴적 작업의 명시적 승인 경계를 보존해야 한다. 충족 여부를 해당 owner의 정적 검증과 별도 관측 증거로 판정한다. | [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-FR-0008 | 현재 허용된 provider surface만 투영하고 planned 또는 absent surface를 현재 지원으로 계산하지 않아야 한다. 충족 여부를 해당 owner의 정적 검증과 별도 관측 증거로 판정한다. | [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-FR-0009 | Provider-native metadata와 repository 문서 형식을 구분하고 정적 형식 적합성을 discovery, 인증 또는 runtime enforcement 증거로 승격하지 않아야 한다. 충족 여부를 해당 owner의 정적 검증과 별도 관측 증거로 판정한다. | [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-FR-0010 | 역할과 skill의 machine registry는 semantic, projection, permission, stop, handoff와 검증 책임을 하나의 소유 경계에서 정의해야 한다. 충족 여부를 해당 owner의 정적 검증과 별도 관측 증거로 판정한다. | [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-FR-0011 | Agent 반복 실행은 bounded retry, no-progress stop, 안전한 checkpoint·compaction·resume와 escalation을 제공해야 하며 한도는 loop contract가 소유해야 한다. 충족 여부를 해당 owner의 정적 검증과 별도 관측 증거로 판정한다. | [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-FR-0012 | 문서 route, profile, metadata, 형식 및 lifecycle edge는 단일 문서 machine owner가 정의하고 prose policy는 책임별 owner에만 있어야 한다. 충족 여부를 해당 owner의 정적 검증과 별도 관측 증거로 판정한다. | [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-FR-0013 | 물리적 문서 form은 정확히 하나의 profile에 대응하며 template와 validator가 일치해야 한다. 충족 여부를 해당 owner의 정적 검증과 별도 관측 증거로 판정한다. | [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-FR-0014 | Requirement, Architecture, Spec/Plan/Task, 운영 문서, Reference 및 README는 각 목적을 지키고 실행 세부나 관측하지 않은 운영 증거를 상위 문서에 복제하지 않아야 한다. Stage 05의 위치를 유지하고 이 수렴에서 Release family를 만들지 않는다. 충족 여부를 해당 owner의 정적 검증과 별도 관측 증거로 판정한다. | [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-FR-0015 | 문서 처분은 고유한 현재 의미와 소비자를 먼저 승계하고 관측 사실·원본 Git 복구를 보존한 뒤 검토된 범위에서 수행해야 한다. 충족 여부를 해당 owner의 정적 검증과 별도 관측 증거로 판정한다. | [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-FR-0016 | Affected-path, lane 및 argv 라우팅에는 단일 machine owner가 있어야 하며 독립 계약을 검사하는 validator의 실패 의미를 합치지 않아야 한다. 충족 여부를 해당 owner의 정적 검증과 별도 관측 증거로 판정한다. | [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-FR-0017 | CI는 의도된 독립 evidence lane, 누락 없는 aggregate verdict, 최소 권한, immutable 외부 Action 식별자와 artifact 보존 경계를 유지해야 한다. 로컬 검증을 hosted 실행으로 보고하지 않는다. 충족 여부를 해당 owner의 정적 검증과 별도 관측 증거로 판정한다. | [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-FR-0018 | 변경은 논리적 커밋, 독립 검토, 비례적인 전체 검증과 되돌릴 수 있는 경계로 전달해야 한다. 충족 여부를 해당 owner의 정적 검증과 별도 관측 증거로 판정한다. | [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-FR-0019 | 실행 상태와 순서는 package-local Plan/Task가 소유하고 원래 tranche·follow-up·승계 이력을 왜곡하거나 영구 중앙 roster로 복제하지 않아야 한다. 충족 여부를 해당 owner의 정적 검증과 별도 관측 증거로 판정한다. | [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-FR-0020 | 완료 package, 후계자로 대체된 문서, 후계자 없이 끝난 문서를 실제 lifecycle에 따라 구분하고 선언된 봉인 원본·provenance를 보존해야 한다. ADR 본문은 decision log에 남고 기록은 current authority나 재활성화 입력이 될 수 없다. 충족 여부를 해당 owner의 정적 검증과 별도 관측 증거로 판정한다. | [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-FR-0021 | Audit, research, data, generated output 및 학습 자료는 근거·관측 시점·소유자를 명시하고 현재 정책 또는 실행 승인의 대체물이 되지 않아야 한다. 충족 여부를 해당 owner의 정적 검증과 별도 관측 증거로 판정한다. | [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-FR-0022 | Scratch와 checkpoint는 제한된 비밀정보 없는 임시 상태로 유지하고 durable 실행 증거는 Task에 남겨야 한다. 제거된 공유 progress ledger를 새 current owner로 복원하지 않는다. 충족 여부를 해당 owner의 정적 검증과 별도 관측 증거로 판정한다. | [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-FR-0023 | 안정적인 문서 identity와 semantic filename을 유지하고 mandatory/excluded profile의 identity 규칙, 유일성 및 경로 대응을 검증해야 한다. 기존 결정 이력의 식별자를 재할당하지 않는다. 충족 여부를 해당 owner의 정적 검증과 별도 관측 증거로 판정한다. | [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-FR-0024 | Compatibility, wrapper 또는 script는 실제 소비자와 고유 rule·negative fixture가 있을 때만 유지하고 승계 증거와 consumer-zero 후 제거해야 한다. 충족 여부를 해당 owner의 정적 검증과 별도 관측 증거로 판정한다. | [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-FR-0025 | Agent 시스템의 risk, tool/data trust, oversight, stop, approval, trace, evaluation 및 component provenance 의무는 현재 Registry와 Stage 00 owner에서 구현·검증해야 한다. 정적 선언은 runtime enforcement를 증명하지 않는다. 충족 여부를 해당 owner의 정적 검증과 별도 관측 증거로 판정한다. | [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-FR-0026 | Repository-declared, provider-runtime, hosted-CI 및 승인된 remote/live 증거를 분리하고 관측 없이 서로 승격하지 않아야 한다. 충족 여부를 해당 owner의 정적 검증과 별도 관측 증거로 판정한다. | [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-FR-0027 | Lifecycle 검증은 profile, state 및 허용 edge를 판정하고 일반 본문 정정·소비자 승계는 semantic/link 검증과 검토된 Git 복구로 판정해야 한다. 봉인 Archive의 무결성 검사는 별도로 유지한다. 충족 여부를 해당 owner의 정적 검증과 별도 관측 증거로 판정한다. | [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-FR-0028 | Malformed input, 도구 부재, fallback, 위험 경로와 금지 동작에는 결정적인 직접 negative test가 있어야 하며 required-tool 실패를 diagnostic SKIP으로 숨기지 않아야 한다. 충족 여부를 해당 owner의 정적 검증과 별도 관측 증거로 판정한다. | [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-NFR-0001 | Roster와 adapter 수는 현재 Registry에서 도출하고 역할·surface admission과 model fitness는 local need, 최소 권한 및 평가 근거로 정당화해야 한다. 충족 여부를 해당 owner의 정적 검증과 별도 관측 증거로 판정한다. | [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-NFR-0002 | Targeted, affected, staged, 전체 unit, all-files 및 formatter/diff 재검증은 같은 필수 계약을 검사하면서 각각의 결과와 변경 스냅샷을 기록해야 한다. 충족 여부를 해당 owner의 정적 검증과 별도 관측 증거로 판정한다. | [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-NFR-0003 | 문서 형식과 변경 판단은 해당 일차 근거, 적용 범위 및 검증 증거로 추적 가능해야 하며 외부 표준과 repository convention을 혼동하지 않아야 한다. 충족 여부를 해당 owner의 정적 검증과 별도 관측 증거로 판정한다. | [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-NFR-0004 | 발견된 baseline 결함은 계약을 약화하지 않고 처리하며 false positive 판정·환경 제한·미해결 실패를 성공으로 숨기지 않아야 한다. 충족 여부를 해당 owner의 정적 검증과 별도 관측 증거로 판정한다. | [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-IF-0001 | Migration은 current owner 전환, 상호 링크, stale claim과 orphan consumer 정리를 같은 검토 단위에서 제공해야 한다. 충족 여부를 해당 owner의 정적 검증과 별도 관측 증거로 판정한다. | [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-IF-0002 | 외부 역할 catalog는 아이디어의 provenance일 뿐 admission 또는 정책 권위가 아니어야 한다. 충족 여부를 해당 owner의 정적 검증과 별도 관측 증거로 판정한다. | [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |

### Reviewed member-ID transfer

아래는 현재 의미의 승계표다. 이전 member ID는 원래 결정·프로그램의 이력 식별자이며 재할당되지 않는다.

| Original member ID | Current semantic owner |
| --- | --- |
| REQ-0005-FR-0001 | REQ-0003-FR-0012 |
| REQ-0005-FR-0002 | REQ-0003-FR-0013 |
| REQ-0005-FR-0003 | REQ-0003-FR-0014 |
| REQ-0005-FR-0004 | REQ-0003-FR-0012 |
| REQ-0005-FR-0005 | REQ-0003-FR-0015 |
| REQ-0005-FR-0006 | REQ-0004-FR-0009 |
| REQ-0005-FR-0007 | REQ-0003-FR-0016 |
| REQ-0005-FR-0008 | REQ-0003-FR-0017 |
| REQ-0005-FR-0009 | REQ-0003-FR-0009 |
| REQ-0005-FR-0010 | REQ-0003-FR-0018 |
| REQ-0005-NFR-0001 | REQ-0003-NFR-0003 |
| REQ-0005-NFR-0002 | REQ-0003-FR-0015 |
| REQ-0006-FR-0001 | REQ-0003-FR-0012 |
| REQ-0006-FR-0002 | REQ-0003-FR-0019 |
| REQ-0006-FR-0003 | REQ-0003-FR-0012 |
| REQ-0006-FR-0004 | REQ-0003-FR-0020 |
| REQ-0006-FR-0005 | REQ-0003-FR-0020 |
| REQ-0006-FR-0006 | REQ-0003-FR-0020 |
| REQ-0006-FR-0007 | REQ-0003-FR-0019 |
| REQ-0006-FR-0008 | REQ-0003-FR-0021 |
| REQ-0006-FR-0009 | REQ-0003-FR-0022 |
| REQ-0006-FR-0010 | REQ-0003-FR-0017 |
| REQ-0006-FR-0011 | REQ-0003-FR-0018 |
| REQ-0006-NFR-0001 | REQ-0003-FR-0007 |
| REQ-0006-NFR-0002 | REQ-0003-FR-0014 |
| REQ-0008-FR-0001 | REQ-0003-FR-0019 |
| REQ-0008-FR-0002 | REQ-0003-FR-0023 |
| REQ-0008-FR-0003 | REQ-0003-FR-0014 |
| REQ-0008-FR-0004 | REQ-0003-FR-0023 |
| REQ-0008-FR-0005 | REQ-0003-FR-0012 |
| REQ-0008-FR-0006 | REQ-0003-FR-0013 |
| REQ-0008-FR-0007 | REQ-0003-FR-0014 |
| REQ-0008-FR-0008 | REQ-0003-FR-0015 |
| REQ-0008-FR-0009 | REQ-0003-FR-0020 |
| REQ-0008-FR-0010 | REQ-0003-FR-0024 |
| REQ-0008-FR-0011 | REQ-0003-FR-0016 |
| REQ-0008-FR-0012 | REQ-0003-FR-0024 |
| REQ-0008-FR-0013 | REQ-0003-FR-0025 |
| REQ-0008-FR-0014 | REQ-0003-FR-0026 |
| REQ-0008-FR-0015 | REQ-0003-FR-0022 |
| REQ-0008-FR-0016 | REQ-0003-NFR-0004 |
| REQ-0008-FR-0017 | REQ-0003-FR-0027 |
| REQ-0008-NFR-0001 | REQ-0003-FR-0019 |
| REQ-0008-NFR-0002 | REQ-0003-FR-0007 |
| REQ-0008-NFR-0003 | REQ-0003-FR-0012 / REQ-0003-FR-0023 |
| REQ-0008-NFR-0004 | REQ-0003-FR-0023 |
| REQ-0008-NFR-0005 | REQ-0003-FR-0020 / REQ-0003-FR-0015 |
| REQ-0008-NFR-0006 | REQ-0003-FR-0024 |
| REQ-0007-FR-0001 | REQ-0004-FR-0005 |
| REQ-0007-FR-0002 | REQ-0004-FR-0006 |
| REQ-0007-FR-0003 | REQ-0004-FR-0007 / REQ-0003-FR-0016 |
| REQ-0007-FR-0004 | REQ-0003-FR-0017 |
| REQ-0007-FR-0005 | REQ-0004-FR-0008 |
| REQ-0007-FR-0006 | REQ-0004-FR-0010 |
| REQ-0007-FR-0007 | REQ-0004-FR-0009 |
| REQ-0007-FR-0008 | REQ-0003-FR-0028 |
| REQ-0007-FR-0009 | REQ-0003-FR-0007 |
| REQ-0007-FR-0010 | REQ-0004-FR-0011 / REQ-0003-FR-0018 / REQ-0003-FR-0019 |
| REQ-0007-FR-0011 | REQ-0004-FR-0012 |
| REQ-0007-FR-0012 | REQ-0004-FR-0013 |
| REQ-0007-FR-0013 | REQ-0004-FR-0014 |
| REQ-0007-NFR-0001 | REQ-0004-NFR-0003 |
| REQ-0007-NFR-0002 | REQ-0003-FR-0014 |

- Current architecture: [AD-0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md).
- Current integration: [Spec 0054](../03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) and its package-local Plan/Tasks.
- Original decision bodies remain in the [decision log](../02.architecture/decisions/README.md); recovery is indexed in [Stage 98](../98.archive/README.md).
