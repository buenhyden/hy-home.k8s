---
title: 'Workspace Agent Governance Platform Requirement Package'
version: "1.0.0"
type: sdlc/requirement
layer: "requirements"
status: active
owner: platform
updated: 2026-08-22
artifact_id: "REQ-0003"
---

# Workspace Agent Governance Platform Requirement Package

## Overview

이 문서는 `hy-home.k8s`의 AI Agent 거버넌스 플랫폼에 대한 제품 요구를 정의한다. 플랫폼은
`docs/00.agent-governance/**`를 durable policy의 system of record로 삼고, 짧은 root/provider
gateway, 기계 검증 가능한 harness contract, provider-native adapter, 반복 가능한 QA와 평가
루프를 결합한다. 아래 네-surface 및 fixed-cardinality 내용은 2026-08-01
predecessor proposal의 역사적 목표이며 현재 terminal authority가 아니다.
current authority는
[ADR-0030](../02.architecture/decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md)과
[Spec 0054](../03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md)다.
실제 provider/surface admission과 roster cardinality reconciliation은 WP-003 소유다.

### Historical predecessor context

The following four-surface table and dated provider observations preserve the
2026-08-01 predecessor proposal only. They are non-authoritative for current
provider admission, cardinality, or topology.

| Surface | 역할 | native/runtime 주장 경계 |
| --- | --- | --- |
| `.agents/**` | shared assets와 local/Antigravity adapter | Gemini CLI native surface가 아니다. |
| `.claude/**` | Claude Code native agent, setting, hook adapter | 정적 형식과 실제 discovery/authenticated run 증거를 분리한다. |
| `.codex/**` | Codex native agent와 project config adapter | 정적 형식과 실제 discovery/authenticated run 증거를 분리한다. |
| `.gemini/**` | Gemini CLI native agent와 project setting adapter | 도입 후에도 provider transition/auth 조건과 canary 증거를 별도로 관리한다. |

설계의 고정 외부 사실 관찰 기준은 **2026-07-10 10:00 Asia/Seoul**
(`2026-07-10T01:00:00Z`)이다. 이후의 모델명, CLI 동작,
인증 정책은 별도 evidence refresh로 다루며, repository-static 구현과 provider-runtime
readiness를 분리한다.

## Vision

운영자는 동일한 역할 계약을 registry-admitted provider surface에서 예측 가능하게 실행하고, 역할 특성에 맞는
provider model과 reasoning effort를 선택하며, 실패를 무한 반복하지 않는 loop와 검증 증거로
결과를 신뢰할 수 있어야 한다. Human은 목표와 승인 경계를 정하고 Agent는 격리된 환경에서
구현·검토·검증을 수행한다. 저장소 지식, 명시적 계약, fixture와 CI가 의도와 실행 사이의
feedback loop를 구성한다.

## Problem Statement

현재 Stage 00 canonical core와 Claude/Codex/local adapter는 존재하지만, 계약은 10개 역할과
3개 surface에 고정되어 있고 Gemini native surface, provider 인증 canary, 역할별 model/effort
적합성, bounded recovery, checkpoint/compaction, eval admission이 하나의 기계 계약으로 닫혀
있지 않다. 정적 파일의 존재를 runtime discovery로 오인하거나, 실패 Agent를 같은 조건으로
재시도하거나, model ID와 역할의 위험도를 검증 없이 결합할 수 있다. 기존 10/30 주장을
유지한 채 별도 문서·행렬을 추가하면 단일 roster와 current-owner 원칙도 다시 분기된다.

[OpenAI의 harness engineering 사례](https://openai.com/index/harness-engineering/)는 짧은
agent map, 저장소 지식의 system-of-record화, 기계적 invariant, worktree 격리와 feedback
loop가 장기 실행 신뢰성에 필요함을 보여 준다. 이 워크스페이스에는 이를 provider-neutral
contract와 각 provider의 실제 schema·runtime evidence로 변환할 요구가 있다.

## Personas

- **Platform Maintainer**: canonical contract, provider adapter, CI와 lifecycle owner가 갈라지지
  않도록 관리한다.
- **AI Agent Operator**: 역할·model·reasoning effort·tool permission을 작업 위험과 비용에 맞게
  선택하고 provider runtime evidence를 확인한다.
- **Implementer / Reviewer**: 분리된 역할, bounded retry, checkpoint와 평가 fixture를 사용해
  구현과 검토를 독립적으로 수행한다.
- **Documentation Researcher**: 기준 시점과 official primary source를 보존하고 최신 사실과
  추론을 구분한다.
- **Quality Engineer**: 정적 parity, schema, fixture, CI, `pre-commit --all-files` 및 canary
  결과의 실패 의미를 판정한다.
- **Security / GitOps Reviewer**: secret, external action, live mutation, destructive git과
  provider credential 경계를 검토한다.

## Key Use Cases

- **STORY-01**: 운영자는 canonical harness contract 한 곳에서 current roster, 역할 semantic,
  surface projection과 검증 상태를 확인한다.
- **STORY-02**: 작업 라우터는 역할의 복잡도, 위험, context, tool use, 비용·latency 및 eval
  결과를 바탕으로 provider별 model과 reasoning effort를 선택한다.
- **STORY-03**: admitted provider 운영자는 repo-static parse와 discovery/run canary를
  별도 증거로 관리한다. Provider-runtime readiness는 해당 provider PASS가 필요하지만,
  repository-local closure는 `ABSENT`/`DEFER`의 owner와 retry trigger를 보존할 수 있다.
- **STORY-04**: 실패한 Agent는 동일 failure signature를 제한 횟수만 재시도하고, 진행이 없으면
  checkpoint와 재현 증거를 남긴 뒤 사람에게 escalation한다.
- **STORY-05**: 새 역할은 agency-agents 등 외부 catalog 이름을 복사해서가 아니라 repository
  gap, 최소 권한, input/output, stop condition, handoff와 eval fixture가 증명될 때만 admission된다.
- **STORY-06**: governance 변경은 targeted·affected·staged·all-files 순서의 QA와 독립 review를
  거쳐 논리 커밋으로 전달된다.
- **STORY-07**: migration은 legacy contract, duplicate matrix, stale 10/30/3 claim과
  `.gemini` native surface가 없다는 stale claim을 새 current-owner로 소비자가 전환된 뒤
  제거하되 실제 runtime `ABSENT`/`DEFER` 증거는 보존한다.

## Functional Requirements

| Requirement ID | Requirement | Priority | Verification intent |
| --- | --- | --- | --- |
| REQ-0003-FR-0001 | Stage 00은 Agent, Skill, Rule, Hook, Workflow, Memory, QA/CI/CD, Model Policy와 Template Contract의 공통 정의 및 owner 경계를 제공해야 한다. | Must | Stage 00 index, contract와 owner validation이 중복 SSoT 없이 통과한다. |
| REQ-0003-FR-0002 | Provider gateway와 adapter는 공통 governance를 복제하지 않고 surface-specific syntax와 capability 차이만 표현해야 한다. | Must | Root/provider shim의 크기·링크·duplicate-policy 검사가 통과한다. |
| REQ-0003-FR-0003 | Skill routing은 repo-local, shared, provider-native 및 명시적으로 요청된 외부 skill을 구분하고 누락을 gap으로 기록해야 한다. | Must | Catalog provenance와 missing-capability evidence가 검증된다. |
| REQ-0003-FR-0004 | Process, branch, documentation, QA, DevOps, CI/CD, security와 Kubernetes skill 축은 공통 strategy lens와 scope contract에 연결되어야 한다. | Must | Scope/import와 role routing 검사가 모든 축의 current owner를 찾는다. |
| REQ-0003-FR-0005 | Repo-changing Agent 작업은 SDLC Plan/Task 또는 승인된 progress/checkpoint surface에 검증 증거와 한계를 남겨야 한다. | Must | Handoff가 명령, 결과, limitation과 next action을 포함한다. |
| REQ-0003-FR-0006 | 문서 stage와 template mapping은 `docs/99.templates`의 form contract와 Stage 00 routing contract를 따라야 한다. | Must | Document profile, cross-link와 template conformance 검사가 통과한다. |
| REQ-0003-FR-0007 | 모든 Agent는 GitOps-first, no-plaintext-secret, no-unapproved-live-mutation, least privilege와 명시적 external-action approval 경계를 지켜야 한다. | Must | Policy lint와 review evidence에 위반이 없다. |
| REQ-0003-FR-0008 | Provider surface는 registry-admitted current owner만 투영하며 planned/absent surface를 current로 세지 않아야 한다. | Must | ADR-0030과 WP-003가 소유한 roster에서 repository-static claim과 provider-runtime claim이 분리된다. |
| REQ-0003-FR-0009 | 각 admitted provider는 native schema와 독립 evidence class를 사용해야 하며 특정 provider나 surface를 미리 의무화하지 않는다. | Must | WP-003 admission 결과와 provider별 PASS/FAIL/BLOCKED/ABSENT/DEFER 기록이 일치하고 PASS만 runtime readiness를 증명한다. |
| REQ-0003-FR-0010 | 단일 versioned machine harness contract는 역할 semantic, surface projection, evidence requirement, permission, stop condition과 handoff를 정의하고 schema로 검증되어야 한다. | Must | Contract/schema가 current roster와 모든 adapter를 단일 소유자로 검증한다. |
| REQ-0003-FR-0011 | Agent loop는 동일 failure signature 자동 재시도 최대 2회, task 자동 recovery 기본 최대 3회, 동일 결과 2회 무진행 시 stop/escalate를 적용하고 secret/transcript 없는 checkpoint·compaction·resume 계약을 제공해야 한다. | Must | Recovery fixture가 retry ceiling, no-progress stop, safe checkpoint와 resume를 재현한다. |
| REQ-0003-NFR-0001 | Canonical roster와 adapter cardinality는 current registry inventory에서 도출되고, 새 역할/surface는 역할별 eval/admission과 model fitness를 통과해야 한다. | Must | WP-003의 derived parity, eval fixture와 fitness decision이 검증되며 fixed count를 authority로 사용하지 않는다. |
| REQ-0003-NFR-0002 | CI/QA는 targeted → affected → staged → tests → `pre-commit run --all-files` → formatter review → rerun → diff check 순서를 제공하고 agent-governance static lane을 최소 권한·고정 action SHA로 실행해야 한다. | Must | 로컬과 GitHub evidence가 같은 필수 lane과 실패 의미를 보고한다. |
| REQ-0003-IF-0001 | Migration은 consumer를 새 current owner로 전환한 뒤 legacy contract/schema, duplicate roster·matrix, stale provider/runtime/model claim과 일회성 산출물을 제거하고 cross-link를 갱신해야 한다. | Must | 금지 패턴 및 orphan-reference 검사가 stale legacy 0건을 보고한다. |
| REQ-0003-IF-0002 | `agency-agents`는 비권위적 아이디어 catalog로만 사용하며, 실제 역할 추가는 repository gap, 최소 semantic contract와 eval evidence를 만족할 때만 허용해야 한다. | Must | 각 admitted role이 provenance가 아닌 local need와 fixture로 정당화된다. |

## Success / Acceptance Criteria

| Requirement ID | Acceptance criterion |
| --- | --- |
| N/A — Acceptance criterion 01 remains acceptance-only | Stage 00 governance hub, harness catalog, model policy, provider note, hook, QA와 template routing이 하나의 owner graph로 연결된다. |
| N/A — Acceptance criterion 02 remains acceptance-only | REQ-0003 → AD-0006 → ADR-0030 → Spec 0054 → Plan/Task의 reciprocal lifecycle chain이 존재한다. |
| N/A — Acceptance criterion 03 remains acceptance-only | Root/provider gateway는 durable policy를 복제하지 않고 native, repo-static, runtime evidence를 구분한다. |
| N/A — Acceptance criterion 04 remains acceptance-only | Repository static quality gate가 governance 변경 후 PASS한다. |
| N/A — Acceptance criterion 05 remains acceptance-only | 별도 template-policy 승인 없이 외부 documentation format을 repository template contract 대체물로 사용하지 않는다. |
| N/A — Acceptance criterion 06 remains acceptance-only | Current registry-derived role와 admitted surface adapter가 누락·추가·semantic drift 없이 일치한다. |
| N/A — Acceptance criterion 07 remains acceptance-only | 각 admitted provider의 secret-free canary record가 존재한다. Provider-runtime readiness는 해당 record의 PASS가 필요하며, repository-local closure의 `ABSENT`/`DEFER`는 limitation, owner와 retry trigger를 포함한다. |
| N/A — Acceptance criterion 08 remains acceptance-only | Machine harness contract/schema, provider metadata schema, adapter projection과 current-owner 검사가 모두 PASS한다. |
| N/A — Acceptance criterion 09 remains acceptance-only | Loop fixture가 retry ceiling, no-progress escalation, checkpoint/compaction/resume 및 민감정보 배제를 검증한다. |
| N/A — Acceptance criterion 10 remains acceptance-only | 모든 역할에 input/output/permission/stop/handoff/eval과 provider별 model/effort fitness 근거가 존재한다. |
| N/A — Acceptance criterion 11 remains acceptance-only | Targeted·affected·staged·tests·`pre-commit run --all-files`·formatter/diff rerun과 agent-governance CI lane이 PASS한다. |
| N/A — Acceptance criterion 12 remains acceptance-only | Legacy contract, duplicate current-owner, stale 10/30/3 및 `.gemini`-surface-absent claim, orphan link가 active surface에서 0건이며 실제 runtime limitation은 별도 evidence class로 남는다. |

## Scope and Non-goals

### In Scope

- Stage 00 canonical governance와 versioned machine harness contract/schema.
- Registry-derived roster 및 WP-003에서 검증·admit된 provider-native surface.
- Provider별 native metadata, project configuration, model/reasoning effort, tool/MCP 및 authenticated canary.
- Bounded retry, checkpoint, compaction, handoff, eval/admission 및 model fitness.
- Agent-governance CI/QA, legacy cutover와 cross-link/current-owner 정리.
- 기존 문서 lifecycle 프로그램 Specs 038–040 완료 후 Specs 041–046을 순차 실행하는 경계.

### Out of Scope

- Agent가 Kubernetes desired state 외의 live cluster나 external service를 직접 변경하는 것.
- Credential, token, auth file, shell history 또는 full provider transcript를 저장소에 수집하는 것.
- Provider 모델을 이름만 최신이라는 이유로 자동 승격하거나 eval 없이 모든 역할에 동일 모델을 지정하는 것.
- `agency-agents`의 persona·prompt를 그대로 vendoring하거나 외부 catalog를 governance authority로 삼는 것.
- 이 프로그램과 무관한 application, GitOps desired state 또는 documentation template 전면 개편.

## Risks, Dependencies, and Assumptions

- **Prerequisite**: 활성 [Spec 038](../03.specs/0038-reference-information-architecture/spec.md),
  [Spec 039](../03.specs/0039-github-ci-qa-evidence/spec.md),
  [Spec 040](../03.specs/0040-contract-cutover-and-program-closure/spec.md)이 먼저 완료되어야 한다.
- **Downstream sequence**: Specs 041 → 042 → 043 → 044 → 045 → 046은 foundation-first
  순서를 지키며, 후속 Spec은 선행 acceptance evidence를 소비한다.
- Model availability, effort enum, CLI schema와 authentication은 변한다. Concrete value는 기준 시점
  official source와 authenticated canary가 함께 증명해야 하며 이름 추론은 금지한다.
- `.gemini/**` 형식 채택과 특정 Gemini 로그인 경로의 가용성을 동일시하지 않는다.
- GitHub-hosted CI에는 provider credential을 넣지 않는다. Authenticated canary는 local/manual
  evidence lane에서 실행하고 secret-free 결과만 기록한다.
- `.agent-work/checkpoint.json`은 ignore된 transient recovery state이며 durable SDLC, credential
  store 또는 full transcript가 아니다.
- ADR-0019와 ADR-0013은 predecessor 실행과 external-lane limitation을
  보존하는 superseded historical decisions다. ADR-0030이 current terminal decision이다.

### Research and provider evidence baseline

- Harness와 loop 원칙: [OpenAI Harness Engineering](https://openai.com/index/harness-engineering/),
  [OpenAI Agent Improvement Loop](https://developers.openai.com/cookbook/examples/agents_sdk/agent_improvement_loop).
- Claude native metadata/settings/hooks와 기준 모델 근거:
  [subagents](https://code.claude.com/docs/en/sub-agents),
  [configuration](https://code.claude.com/docs/en/configuration),
  [hooks](https://code.claude.com/docs/en/hooks),
  [memory](https://code.claude.com/docs/en/memory),
  [model configuration](https://code.claude.com/docs/en/model-config).
- Codex native metadata/config와 기준 모델 근거:
  [subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents),
  [configuration](https://learn.chatgpt.com/docs/config-file/config-reference),
  [model catalog](https://developers.openai.com/api/docs/models).
- Gemini native metadata/config:
  [documentation](https://geminicli.com/docs/),
  [subagents](https://geminicli.com/docs/core/subagents/),
  [hooks](https://geminicli.com/docs/hooks/reference/),
  [project context](https://geminicli.com/docs/cli/gemini-md/),
  [model selection](https://geminicli.com/docs/cli/model/),
  [generation settings](https://geminicli.com/docs/cli/generation-settings/).
- CI/QA: [GitHub Actions secure use](https://docs.github.com/en/actions/reference/security/secure-use),
  [pre-commit](https://pre-commit.com/).
- Role inspiration only: [agency-agents](https://github.com/msitarzewski/agency-agents).

## Traceability

### Lifecycle Traceability

| Requirement ID | Acceptance criterion | Downstream owner |
| --- | --- | --- |
| REQ-0003-FR-0001 | 공통 governance와 owner graph가 단일 current source로 검증된다. | [AD 0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-FR-0002 | Provider gateway가 thin adapter 경계를 지킨다. | [AD 0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-FR-0003 | Skill provenance와 missing gap이 기계 검증된다. | [AD 0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-FR-0004 | 모든 strategy axis와 scope owner를 찾을 수 있다. | [AD 0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-FR-0005 | Repo-changing handoff에 evidence와 limitation이 남는다. | [AD 0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-FR-0006 | Template/profile/cross-link 검사가 통과한다. | [AD 0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-FR-0007 | GitOps, secret, privilege와 external-action guardrail 위반이 없다. | [AD 0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-FR-0008 | Registry-admitted surface가 공통 semantic과 분리된 native claim을 가진다. | [AD 0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-FR-0009 | Schema/model/effort/MCP 및 admitted provider의 독립 canary record가 검증된다. | [AD 0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-FR-0010 | Machine harness contract/schema가 모든 역할과 adapter를 검증한다. | [AD 0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-FR-0011 | Bounded loop/checkpoint/compaction fixture가 recovery 경계를 증명한다. | [AD 0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-NFR-0001 | Registry-derived role/adapter parity 및 eval/model fitness가 검증된다. | [AD 0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-NFR-0002 | CI/QA/all-files evidence가 필수 lane 전체를 통과한다. | [AD 0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-IF-0001 | Legacy와 orphan current-owner가 active surface에 남지 않는다. | [AD 0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| REQ-0003-IF-0002 | 외부 role idea가 local gap과 eval을 통과해야 admission된다. | [AD 0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| N/A — Acceptance criterion 01 remains acceptance-only | Stage 00 owner graph가 모순 없이 연결된다. | [AD 0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| N/A — Acceptance criterion 02 remains acceptance-only | Requirement Package→AD→ADR→Spec→Plan/Task reciprocal chain이 존재한다. | [AD 0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| N/A — Acceptance criterion 03 remains acceptance-only | Gateway가 policy를 복제하지 않고 evidence class를 구분한다. | [AD 0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| N/A — Acceptance criterion 04 remains acceptance-only | Repository static quality gate가 PASS한다. | [AD 0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| N/A — Acceptance criterion 05 remains acceptance-only | Repository template contract가 유일한 form authority로 유지된다. | [AD 0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| N/A — Acceptance criterion 06 remains acceptance-only | Registry-derived roles와 admitted adapters가 parity를 이룬다. | [AD 0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| N/A — Acceptance criterion 07 remains acceptance-only | 각 admitted provider의 canary record와 runtime-readiness 경계가 검증된다. | [AD 0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| N/A — Acceptance criterion 08 remains acceptance-only | Contract/schema/provider metadata parity가 PASS한다. | [AD 0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| N/A — Acceptance criterion 09 remains acceptance-only | Bounded loop recovery와 safe resume가 fixture로 검증된다. | [AD 0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| N/A — Acceptance criterion 10 remains acceptance-only | 역할별 eval/model fitness evidence가 존재한다. | [AD 0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| N/A — Acceptance criterion 11 remains acceptance-only | CI와 all-files QA가 PASS한다. | [AD 0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |
| N/A — Acceptance criterion 12 remains acceptance-only | Stale legacy와 orphan reference가 0건이다. | [AD 0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) |

- **AD**: [AD 0006](../02.architecture/descriptions/0006-workspace-agent-governance-platform.md)
- **Current terminal decision**: [ADR 0030](../02.architecture/decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md)
- **Current implementation authority**: [Spec 0054](../03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md)
- **Historical predecessor**: [ADR 0019](../02.architecture/decisions/0019-provider-native-agent-harness-and-loop-model.md)
- **Prerequisite Specs**: [Spec 038](../03.specs/0038-reference-information-architecture/spec.md),
  [Spec 039](../03.specs/0039-github-ci-qa-evidence/spec.md),
  [Spec 040](../03.specs/0040-contract-cutover-and-program-closure/spec.md)
- **Delivery Specs**: [Spec 041](../03.specs/0041-stage-00-agent-governance-contract/spec.md),
  [Spec 042](../03.specs/0042-provider-native-runtime-and-model-evidence/spec.md),
  [Spec 043](../03.specs/0043-agent-harness-loop-lifecycle/spec.md),
  [Spec 044](../03.specs/0044-agent-roster-evaluation-and-admission/spec.md),
  [Spec 045](../03.specs/0045-agent-governance-ci-qa-cutover/spec.md),
  [Spec 046](../03.specs/0046-agent-governance-program-closure/spec.md)
- **Agent design**: [Workspace Agent Governance Program Design](../03.specs/0041-stage-00-agent-governance-contract/spec.md)
