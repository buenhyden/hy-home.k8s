---
title: 'Workspace Agent Governance Platform Architecture Reference Document'
type: sdlc/ard
status: active
owner: platform
updated: 2026-07-26
---

# Workspace Agent Governance Platform Architecture Reference Document (ARD)

## Overview

이 문서는 Stage 00 canonical governance를 네 provider surface에 투영하고, runtime evidence와
feedback loop로 닫는 참조 아키텍처를 정의한다. 핵심 구조는
`canonical policy + machine harness contract + provider projection + execution loop + evidence gate`다.
설계의 현재 외부 사실 관찰 기준은 **2026-07-26 Asia/Seoul**이며, concrete provider schema와
model 값은 official primary source와 native parse/runtime evidence가 함께 입증할 때만
provider-runtime current가 된다.

[OpenAI Harness Engineering](https://openai.com/index/harness-engineering/)의 짧은 map,
repo-local system of record, 기계적 invariant, 격리 환경과 feedback loop 원칙을 이 저장소의
Stage 00, schema validator, worktree와 SDLC evidence에 맞게 적용한다. 이 사례는 방향 근거이지
다른 provider의 native capability를 대신하는 증거가 아니다.

## Boundaries & Non-goals

### Owns

- `docs/00.agent-governance/**`의 durable policy, current roster, provider note, quality와 lifecycle contract.
- 단일 versioned `harness-contract`와 schema 및 네 surface projection rule.
- `.agents/**` local/Antigravity, `.claude/**`, `.codex/**`, `.gemini/**`의 adapter ownership.
- 역할별 model/reasoning-effort decision, provider config/MCP allowlist와 runtime canary evidence model.
- Bounded retry, checkpoint, compaction, resume, handoff, eval/admission과 legacy cutover.
- Spec 039가 제공하는 baseline CI/QA를 소비하고 Spec 045에서 추가하는 agent-governance static lane.

### Consumes

- `docs/99.templates/**`의 form/profile contract와 Stage 00의 routing contract.
- GitHub Actions, pre-commit, repository quality gate, provider CLI와 local credential store.
- Specs 038–040에서 완료되는 reference IA, CI/QA evidence 및 lifecycle cutover.
- Kubernetes/GitOps/security/operations 문서를 역할 수행의 domain context로 소비하되 소유하지 않는다.

### Does Not Own

- `gitops/**`와 `infrastructure/**`의 desired-state semantics 및 live runtime state.
- Provider account, billing, credential 값, shell history, auth file 또는 private transcript.
- Provider vendor의 모델 lifecycle, CLI distribution 또는 authentication policy.

### Non-goals

- 네 provider에 독립된 governance fork를 만드는 것.
- `.agents/**`를 Gemini CLI native evidence로 취급하는 것.
- Provider-authenticated canary를 GitHub-hosted secret lane으로 실행하는 것.
- 모든 역할에 같은 model/effort를 적용하거나 모델명을 “최신”이라는 이유만으로 자동 승격하는 것.
- `agency-agents` prompt/persona를 vendoring하거나 외부 catalog를 admission authority로 삼는 것.
- Live cluster/service mutation, secret material 수집, unrelated application 또는 GitOps 개편.

## Quality Attributes

| Attribute | Architecture requirement | Measure |
| --- | --- | --- |
| Consistency | Machine contract가 역할 semantic과 surface projection의 유일한 machine owner다. | 12 role × 4 surface = 48 adapter exact parity, duplicate owner 0건 |
| Verifiability | Static shape, native discovery와 authenticated run을 별도 evidence class로 관리한다. | Contract/schema/config PASS와 Claude·Codex·Gemini별 독립 canary record; PASS만 runtime readiness |
| Reliability | 동일 실패의 무한 반복을 차단하고 재현 가능한 state만 checkpoint한다. | 동일 signature retry ≤2, task recovery ≤3, 동일 결과 2회면 stop |
| Security | Least privilege, GitOps-first, secret-free evidence와 명시적 external-action approval을 적용한다. | Secret/auth/transcript 저장 0건, CI write permission 불필요, action full SHA |
| Evolvability | Provider schema/model 변화는 cutoff ledger, eval과 canary를 통해 갱신한다. | Source date·model compatibility·fitness fixture 없는 승격 0건 |
| Legibility | Root/provider gateway는 map이고 durable rule은 Stage 00에 한 번만 존재한다. | Duplicate policy/stale current claim 0건, cross-link validator PASS |
| Recoverability | Compact checkpoint가 안전한 resume와 human escalation을 지원한다. | Redacted checkpoint schema와 recovery fixture PASS |
| Operability | Local QA와 CI가 같은 contract/schema/parity failure를 진단한다. | Targeted→all-files lane 및 repository quality gate PASS |

## System Overview & Context

### Logical components

| Component | Canonical owner | Responsibility | Evidence |
| --- | --- | --- | --- |
| Governance map | `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, provider baseline | 짧은 bootstrap과 deeper owner routing | Thin-gateway/duplicate-policy lint |
| Durable policy | `docs/00.agent-governance/**` | scope, role, model, quality, approval, lifecycle | Document profile/current-owner/cross-link validation |
| Machine harness contract | `docs/00.agent-governance/contracts/harness-contract.json` plus schema | roles, semantics, surface projection, evidence, stop/handoff | JSON schema, semantic/parity validators |
| Shared/local surface | `.agents/**` | shared skill/workflow/output style와 local/Antigravity adapter | Parse, link and role projection checks |
| Claude surface | `.claude/**` | Claude-native agent/settings/hooks projection | Static schema plus authenticated Claude canary |
| Codex surface | `.codex/**` | Codex-native agents/project config projection | TOML parse plus authenticated Codex canary |
| Gemini surface | `.gemini/**` | Gemini-native agents/project settings projection | Frontmatter/JSON parse plus authenticated Gemini canary |
| Loop state | `.agent-work/checkpoint.json` | ignored, redacted, bounded recovery state | Checkpoint schema and recovery fixtures |
| Eval/QA evidence | tests, scripts, `.github/**`, SDLC Task | admission, fitness, parity, CI/all-files evidence | Local/CI command result and logical commit |

기존 `agent-role-semantics.json`과 schema는 새 contract의 병행 SSoT가 아니다. Spec 041이 소비자를
새 contract로 이동한 뒤 Spec 045가 old contract와 stale references를 제거한다.
`validation-surfaces.json`은 validation routing을 소유하므로 역할 semantic contract와 합치지 않는다.

### Surface projection contract

| Surface | Required provider-native projection | Reasoning/tool boundary |
| --- | --- | --- |
| local/Antigravity | `name`, `description`, `model`을 가진 local role file과 shared asset reference | Antigravity/local capability만 주장하며 Gemini native로 재해석하지 않는다. |
| Claude | Official subagent schema의 `name`, `description`, `model`, `tools`; `effort`·`maxTurns` 등은 cutoff schema가 허용할 때만 사용 | Claude settings/hooks의 native permission을 다른 provider에 일반화하지 않는다. |
| Codex | role `name`, `description`, `developer_instructions`, `model`, `model_reasoning_effort`와 project config | Sandbox/approval 및 agent config를 사용하고 Claude-style hook enforcement를 주장하지 않는다. |
| Gemini | Official subagent schema의 `name`, `description`, `kind`, `tools`, `model`, `max_turns`, `timeout_mins`와 project settings | Reasoning/model config는 settings schema에 두며, subagent recursion과 unsupported permission을 가정하지 않는다. |

이 field 목록은 live documentation에서 관찰한 implementation candidate다. Cutoff 시점
지원 사실은 dated tag/release/snapshot으로 별도 증명하고, 그렇지 못한 field는 observation-time
confidence와 native schema/config canary를 통과하기 전 contract-required로 승격하지 않는다.

Provider schema 근거는 Claude
[subagents](https://code.claude.com/docs/en/sub-agents)·[configuration](https://code.claude.com/docs/en/configuration)·
[hooks](https://code.claude.com/docs/en/hooks), Codex
[subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)·
[configuration](https://learn.chatgpt.com/docs/config-file/config-reference),
Gemini [subagents](https://geminicli.com/docs/core/subagents/)·
[hooks](https://geminicli.com/docs/hooks/reference/)·
[generation settings](https://geminicli.com/docs/cli/generation-settings/)다.

### Roster, model and effort decision

Canonical roster는 기존 `code-reviewer`, `doc-writer`, `gitops-reviewer`, `incident-responder`,
`k8s-implementer`, `network-reviewer`, `observability-reviewer`, `security-auditor`, `supervisor`,
`wiki-curator`에 `docs-researcher`, `quality-engineer`를 추가한다. 각 역할은 네 surface에 하나씩
투영하되 provider syntax 외 semantic 차이는 금지한다.

구체 model/effort는 role마다 다음 순서로 결정한다.

1. Correctness/security blast radius와 독립 판단 필요성.
2. Context 크기, long-horizon planning, tool concurrency와 structured-output 요구.
3. Provider schema가 지원하는 effort/reasoning enum 및 model compatibility.
4. 역할 fixture의 pass rate, false-positive/false-negative, latency와 비용.
5. Canary가 보고한 actual model/runtime과 fallback 동작.

높은 위험의 supervisor/security/incident 또는 복합 architecture 역할은 강한 reasoning 후보로,
bounded editing·formatting·index 역할은 비용/latency가 낮은 후보로 시작할 수 있으나 이는 기본
가설일 뿐이다. `docs-researcher`는 source fidelity와 cutoff 정확성, `quality-engineer`는 fixture
판별력과 deterministic evidence를 우선한다. Claude는 account-available
`opus`/`fable`/`sonnet`/`haiku`, Codex는 installed runtime이 문서화한 `gpt-5.6` 계열과
balanced candidate, Gemini는 `gemini-3-pro-preview`/`gemini-3-flash-preview`/Auto를
후보로 비교한다. 모델 이름이나 provider benchmark만으로 역할에 배정하지 않고 Spec
042/044의 schema·canary·동일 corpus eval이 exact ID와 effort를 확정한다.

### Runtime evidence and strict closure

각 Claude/Codex/Gemini canary는 CLI version, installation source, auth mode의 비밀 아닌 식별자,
project-root discovery, known role discovery, controlled prompt/result, selected/actual model,
exit status와 timestamp를 기록한다. Token, credential path/content, shell history, full transcript는
기록하지 않는다. Repo-static PASS는 runtime PASS를 대체하지 않는다. 각 provider의
runtime-readiness claim은 해당 canary PASS가 필요하다. Repository-local closure는
`ABSENT`/`DEFER`에 limitation, owner와 retry trigger가 있을 때 허용하되 runtime readiness는
열린 상태로 유지한다.

## Data Architecture

### Canonical entities

- **Role**: stable ID, purpose, input/output, responsibility, prohibited action, permission, stop
  condition, handoff, required evidence, eval fixture와 model-fitness dimensions.
- **Surface projection**: role ID, provider, native path, schema metadata, model/effort mapping과
  capability limitation. Role semantic을 복제하지 않고 contract를 참조한다.
- **Provider baseline**: cutoff, official source, CLI/config schema, candidate models, effort enum,
  MCP/tool policy와 transition risk.
- **Canary result**: provider/version/auth-mode, role-discovery/run outcome, actual model, timestamp,
  redacted failure class. PASS/FAIL evidence이지 credential store가 아니다.
- **Checkpoint**: task ID, attempt counters, normalized failure signature, completed/remaining work,
  validation summary, next action과 escalation reason. Prompt transcript와 secret은 금지한다.
- **Eval decision**: role/fixture/provider/model/effort, score, latency/cost observation, admission or
  rejection rationale와 reviewer.

### State and integrity flow

`PRD/ARD/ADR → Spec → machine contract → provider projection → static validation → authenticated
canary/eval → CI/QA → closure` 순서를 사용한다. Specs 038–040은 이 프로그램의 문서·CI 기반을
먼저 닫고, Specs 041–046은 contract, provider, loop, roster, cutover, closure 순서로 선행
evidence를 소비한다.

동일 failure signature는 normalized command/exit/finding key로 계산한다. 같은 signature 자동
재시도는 최대 2회, task 전체 자동 recovery는 기본 최대 3회다. 동일 결과가 2회 반복되어
progress delta가 없으면 checkpoint를 기록하고 stop/escalate한다. Compaction은 결정, 증거,
remaining work만 보존하고 secret, auth data, raw/full transcript를 버린다.

## Infrastructure & Deployment

- 격리된 `.worktrees/**` worktree와 logical branch/commit을 기본 실행 단위로 사용한다.
- Project-local provider config는 secret-free defaults, role layer와 allowlisted MCP/tool만 추적한다.
  User auth/config는 저장소 밖에 남고 migration script가 임의로 덮어쓰지 않는다.
- Provider canary는 local/manual lane에서 인증 후 실행한다. GitHub Actions에는 Claude/Codex/Gemini
  credential을 추가하지 않는다.
- Spec 039의 baseline workflow/QA를 먼저 완료한다. Spec 045의 agent-governance lane은
  contract/schema, 12/48 parity, provider config parse, eval fixture, legacy/orphan pattern을 검사하며
  `permissions` 최소화와 third-party action full commit SHA를 사용한다. 근거는
  [GitHub secure use](https://docs.github.com/en/actions/reference/security/secure-use)다.
- Local QA는 targeted → affected → staged → tests →
  [`pre-commit run --all-files`](https://pre-commit.com/) → formatter review → rerun →
  `git diff --check`/scope review 순서다. 실패 수정 뒤 관련 lane을 다시 실행한다.
- Spec 046은 repository quality gate, all-files, 세 provider canary record, 12/48,
  eval/model fitness, zero-legacy, independent whole-branch review와 clean tree를 요구한다.
  `ABSENT`/`DEFER` provider record는 runtime readiness PASS가 아니며 owner/trigger가 필수다.

## Traceability

### Lifecycle Traceability

The table below maps the proposed delta to draft ADR-0019; it is not a current-
decision map. Accepted ADR-0013 remains the current implementation decision
until Spec 046 closes and the lifecycle transition is approved.

| Upstream requirement | Quality attribute or boundary | ADR / Spec |
| --- | --- | --- |
| [REQ-PRD-FUN-01](../../01.requirements/003-workspace-agent-governance-platform.md) | Stage 00 durable policy와 owner graph | [Proposed ADR 0019](../decisions/0019-provider-native-agent-harness-and-loop-model.md) |
| [REQ-PRD-FUN-02](../../01.requirements/003-workspace-agent-governance-platform.md) | Thin gateway와 provider projection | [Proposed ADR 0019](../decisions/0019-provider-native-agent-harness-and-loop-model.md) |
| [REQ-PRD-FUN-03](../../01.requirements/003-workspace-agent-governance-platform.md) | Skill provenance와 gap evidence | [Proposed ADR 0019](../decisions/0019-provider-native-agent-harness-and-loop-model.md) |
| [REQ-PRD-FUN-04](../../01.requirements/003-workspace-agent-governance-platform.md) | Strategy axis와 scope owner | [Proposed ADR 0019](../decisions/0019-provider-native-agent-harness-and-loop-model.md) |
| [REQ-PRD-FUN-05](../../01.requirements/003-workspace-agent-governance-platform.md) | Execution/checkpoint/handoff evidence | [Proposed ADR 0019](../decisions/0019-provider-native-agent-harness-and-loop-model.md) |
| [REQ-PRD-FUN-06](../../01.requirements/003-workspace-agent-governance-platform.md) | Form/profile와 routing contract | [Proposed ADR 0019](../decisions/0019-provider-native-agent-harness-and-loop-model.md) |
| [REQ-PRD-FUN-07](../../01.requirements/003-workspace-agent-governance-platform.md) | GitOps, secret, privilege와 approval boundary | [Proposed ADR 0019](../decisions/0019-provider-native-agent-harness-and-loop-model.md) |
| [REQ-PRD-FUN-08](../../01.requirements/003-workspace-agent-governance-platform.md) | Four-surface projection | [Proposed ADR 0019](../decisions/0019-provider-native-agent-harness-and-loop-model.md) |
| [REQ-PRD-FUN-09](../../01.requirements/003-workspace-agent-governance-platform.md) | Provider schema/model/effort/MCP와 canary | [Proposed ADR 0019](../decisions/0019-provider-native-agent-harness-and-loop-model.md) |
| [REQ-PRD-FUN-10](../../01.requirements/003-workspace-agent-governance-platform.md) | Machine harness contract/schema | [Proposed ADR 0019](../decisions/0019-provider-native-agent-harness-and-loop-model.md) |
| [REQ-PRD-FUN-11](../../01.requirements/003-workspace-agent-governance-platform.md) | Bounded loop/checkpoint/compaction | [Proposed ADR 0019](../decisions/0019-provider-native-agent-harness-and-loop-model.md) |
| [REQ-PRD-FUN-12](../../01.requirements/003-workspace-agent-governance-platform.md) | 12-role/48-adapter, eval/admission | [Proposed ADR 0019](../decisions/0019-provider-native-agent-harness-and-loop-model.md) |
| [REQ-PRD-FUN-13](../../01.requirements/003-workspace-agent-governance-platform.md) | CI/QA/all-files evidence | [Proposed ADR 0019](../decisions/0019-provider-native-agent-harness-and-loop-model.md) |
| [REQ-PRD-FUN-14](../../01.requirements/003-workspace-agent-governance-platform.md) | Legacy cutover/current-owner integrity | [Proposed ADR 0019](../decisions/0019-provider-native-agent-harness-and-loop-model.md) |
| [REQ-PRD-FUN-15](../../01.requirements/003-workspace-agent-governance-platform.md) | Evidence-only external role admission | [Proposed ADR 0019](../decisions/0019-provider-native-agent-harness-and-loop-model.md) |
| [REQ-PRD-MET-01](../../01.requirements/003-workspace-agent-governance-platform.md) | Owner graph consistency | [Proposed ADR 0019](../decisions/0019-provider-native-agent-harness-and-loop-model.md) |
| [REQ-PRD-MET-02](../../01.requirements/003-workspace-agent-governance-platform.md) | Reciprocal lifecycle chain | [Proposed ADR 0019](../decisions/0019-provider-native-agent-harness-and-loop-model.md) |
| [REQ-PRD-MET-03](../../01.requirements/003-workspace-agent-governance-platform.md) | Gateway/evidence-class separation | [Proposed ADR 0019](../decisions/0019-provider-native-agent-harness-and-loop-model.md) |
| [REQ-PRD-MET-04](../../01.requirements/003-workspace-agent-governance-platform.md) | Repository static gate | [Proposed ADR 0019](../decisions/0019-provider-native-agent-harness-and-loop-model.md) |
| [REQ-PRD-MET-05](../../01.requirements/003-workspace-agent-governance-platform.md) | Template form authority | [Proposed ADR 0019](../decisions/0019-provider-native-agent-harness-and-loop-model.md) |
| [REQ-PRD-MET-06](../../01.requirements/003-workspace-agent-governance-platform.md) | 12/48 exact parity | [Proposed ADR 0019](../decisions/0019-provider-native-agent-harness-and-loop-model.md) |
| [REQ-PRD-MET-07](../../01.requirements/003-workspace-agent-governance-platform.md) | Three-provider strict canary closure | [Proposed ADR 0019](../decisions/0019-provider-native-agent-harness-and-loop-model.md) |
| [REQ-PRD-MET-08](../../01.requirements/003-workspace-agent-governance-platform.md) | Contract/schema/provider parity | [Proposed ADR 0019](../decisions/0019-provider-native-agent-harness-and-loop-model.md) |
| [REQ-PRD-MET-09](../../01.requirements/003-workspace-agent-governance-platform.md) | Recovery fixture and safe resume | [Proposed ADR 0019](../decisions/0019-provider-native-agent-harness-and-loop-model.md) |
| [REQ-PRD-MET-10](../../01.requirements/003-workspace-agent-governance-platform.md) | Eval/model-fitness evidence | [Proposed ADR 0019](../decisions/0019-provider-native-agent-harness-and-loop-model.md) |
| [REQ-PRD-MET-11](../../01.requirements/003-workspace-agent-governance-platform.md) | CI and all-files gate | [Proposed ADR 0019](../decisions/0019-provider-native-agent-harness-and-loop-model.md) |
| [REQ-PRD-MET-12](../../01.requirements/003-workspace-agent-governance-platform.md) | Zero stale legacy/orphan reference | [Proposed ADR 0019](../decisions/0019-provider-native-agent-harness-and-loop-model.md) |

- **PRD**: [PRD 003](../../01.requirements/003-workspace-agent-governance-platform.md)
- **Current decision**: [ADR 0013](../decisions/0013-stage-00-canonical-adapter-model.md)
- **Proposed successor decision**: [Proposed ADR 0019](../decisions/0019-provider-native-agent-harness-and-loop-model.md)
- **Prerequisites**: [Spec 038](../../03.specs/038-reference-information-architecture/spec.md),
  [Spec 039](../../03.specs/039-github-ci-qa-evidence/spec.md),
  [Spec 040](../../03.specs/040-contract-cutover-and-program-closure/spec.md)
- **Delivery sequence**: [Spec 041](../../03.specs/041-stage-00-agent-governance-contract/spec.md),
  [Spec 042](../../03.specs/042-provider-native-runtime-and-model-evidence/spec.md),
  [Spec 043](../../03.specs/043-agent-harness-loop-lifecycle/spec.md),
  [Spec 044](../../03.specs/044-agent-roster-evaluation-and-admission/spec.md),
  [Spec 045](../../03.specs/045-agent-governance-ci-qa-cutover/spec.md),
  [Spec 046](../../03.specs/046-agent-governance-program-closure/spec.md)
- **Agent design**: [Workspace Agent Roster and Projection Design](../../03.specs/041-stage-00-agent-governance-contract/agent-design.md)
