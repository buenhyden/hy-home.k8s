---
title: 'Workspace Agent Governance Platform Architecture Description'
type: sdlc/ad
status: active
owner: platform
updated: 2026-08-30
artifact_id: "AD-0006"
---

# Workspace Agent Governance Platform Architecture Description (AD)

## Overview

이 문서는 Stage 00 human governance, provider-neutral machine authority,
provider projection, execution loop와 evidence gate의 경계를 정의한다.
[ADR-0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md)과
[Spec 0054](../../03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md)가
current terminal authority다. Codex와 Claude만 남기는 실제 surface cutover는
WP-003 소유이며 이 문서는 완료되지 않은 cutover를 현재 구현으로 주장하지 않는다.
설계의 고정 외부 사실 관찰 기준은 **2026-07-10 10:00 Asia/Seoul**
(`2026-07-10T01:00:00Z`)이며, concrete provider schema와
model 값은 official primary source와 native parse/runtime evidence가 함께 입증할 때만
provider-runtime current가 된다.

[OpenAI Harness Engineering](https://openai.com/index/harness-engineering/)의 짧은 map,
repo-local system of record, 기계적 invariant, 격리 환경과 feedback loop 원칙을 이 저장소의
Stage 00, schema validator, worktree와 SDLC evidence에 맞게 적용한다. 이 사례는 방향 근거이지
다른 provider의 native capability를 대신하는 증거가 아니다.

## Boundaries & Non-goals

### Owns

- `docs/00.agent-governance/**`의 durable human policy, 역할 책임, provider 차이와 lifecycle 경계.
- 하나의 provider-neutral role/permission/handoff machine owner를 두고 projection이 공통 policy를 복제하지 않는 구조.
- 현재 registry inventory에서 role과 adapter 집합을 도출하고 고정 cardinality를 권위로 사용하지 않는 규칙.
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

- provider별 독립 governance fork를 만드는 것.
- `.agents/**`를 Gemini CLI native evidence로 취급하는 것.
- Provider-authenticated canary를 GitHub-hosted secret lane으로 실행하는 것.
- 모든 역할에 같은 model/effort를 적용하거나 모델명을 “최신”이라는 이유만으로 자동 승격하는 것.
- `agency-agents` prompt/persona를 vendoring하거나 외부 catalog를 admission authority로 삼는 것.
- Live cluster/service mutation, secret material 수집, unrelated application 또는 GitOps 개편.

## Quality Attributes

| Attribute | Architecture requirement | Measure |
| --- | --- | --- |
| Consistency | Provider-neutral registry가 역할 semantic과 admitted surface projection의 유일한 machine owner다. | Registry-derived parity와 duplicate owner 0건 |
| Verifiability | Static shape, native discovery와 authenticated run을 별도 evidence class로 관리한다. | Contract/schema/config PASS와 admitted-provider별 독립 canary record; PASS만 runtime readiness |
| Reliability | 동일 실패의 무한 반복을 차단하고 재현 가능한 state만 checkpoint한다. | 동일 signature retry ≤2, task recovery ≤3, 동일 결과 2회면 stop |
| Security | Least privilege, GitOps-first, secret-free evidence와 명시적 external-action approval을 적용한다. | Secret/auth/transcript 저장 0건, CI write permission 불필요, action full SHA |
| Evolvability | Provider schema/model 변화는 cutoff ledger, eval과 canary를 통해 갱신한다. | Source date·model compatibility·fitness fixture 없는 승격 0건 |
| Legibility | Root/provider gateway는 map이고 durable rule은 Stage 00에 한 번만 존재한다. | Duplicate policy/stale current claim 0건, cross-link validator PASS |
| Recoverability | Compact checkpoint가 안전한 resume와 human escalation을 지원한다. | Redacted checkpoint schema와 recovery fixture PASS |
| Operability | Local QA와 CI가 같은 contract/schema/parity failure를 진단한다. | Targeted→all-files lane 및 repository quality gate PASS |

## System Overview & Context

### Historical predecessor context

The provider names, surface topology, roster counts, model candidates, and
canary cardinalities below preserve the 2026-08-01 predecessor implementation
context only. They are non-authoritative for current topology and must not be
used to admit a provider or derive a roster. ADR-0030 and Spec 0054 own the
current boundary; WP-003 will migrate or remove these tracked surfaces after
consumer-zero proof.

### Logical components

| Component | Canonical owner | Responsibility | Evidence |
| --- | --- | --- | --- |
| Governance map | `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, provider baseline | 짧은 bootstrap과 deeper owner routing | Thin-gateway/duplicate-policy lint |
| Durable policy | `docs/00.agent-governance/**` | scope, role, model, quality, approval, lifecycle | Document profile/current-owner/cross-link validation |
| Machine harness contract | `.agents/registry.json` plus `.agents/contracts/agent-registry.schema.json` | roles, semantics, surface projection, evidence, stop/handoff | JSON schema, semantic/parity validators |
| Shared/local surface | `.agents/**` | shared skill/workflow/output style와 local/Antigravity adapter | Parse, link and role projection checks |
| Claude surface | `.claude/**` | Claude-native agent/settings/hooks projection | Static schema plus authenticated Claude canary |
| Codex surface | `.codex/**` | Codex-native agents/project config projection | TOML parse plus authenticated Codex canary |
| Gemini surface | `.gemini/**` | Gemini-native agents/project settings projection | Frontmatter/JSON parse plus authenticated Gemini canary |
| Loop state | `.agent-work/checkpoint.json` | ignored, redacted, bounded recovery state | Checkpoint schema and recovery fixtures |
| Eval/QA evidence | tests, scripts, `.github/**`, SDLC Task | admission, fitness, parity, CI/all-files evidence | Local/CI command result and logical commit |

구형 역할 의미 contract와 schema는 새 contract의 병행 SSoT가 아니다.
Spec 041이 소비자를 새 contract로 이동했고 Spec 045가 zero-consumer 증거
뒤 compatibility 입력과 stale references를 제거한다.
`validation-surfaces.json`은 validation routing을 소유하므로 역할 semantic contract와 합치지 않는다.

### Surface projection contract

| Surface | Required provider-native projection | Reasoning/tool boundary |
| --- | --- | --- |
| local/Antigravity | `name`, `description`, `model`을 가진 local role file과 shared asset reference | Antigravity/local capability만 주장하며 Gemini native로 재해석하지 않는다. |
| Claude | Official subagent schema의 `name`, `description`, `model`, `tools`; `effort`·`maxTurns` 등은 cutoff schema가 허용할 때만 사용 | Claude settings/hooks의 native permission을 다른 provider에 일반화하지 않는다. |
| Codex | role `name`, `description`, `developer_instructions`, `model`, `model_reasoning_effort`와 project config | Sandbox/approval 및 agent config를 사용하고 Claude-style hook enforcement를 주장하지 않는다. |
| Gemini | Spec 044가 현재 repo-static contract로 허용한 `name`, `description`, `kind`, `max_turns`, `timeout_mins`와 최소 project settings | Generic tool alias와 exact model은 model-fitness candidate/runtime evidence가 소유하며, native parser/canary 전에는 adapter field로 승격하지 않는다. |

Spec 042가 기록한 더 넓은 live-documentation field 목록은 observation-time
candidate 이력이다. 현재 repository contract는 Spec 044의 닫힌 5필드 Gemini
projection이 소유한다. Cutoff 시점 지원 사실은 dated tag/release/snapshot으로
별도 증명하고, 그렇지 못한 field는 native schema/config canary를 통과하기 전
contract-required로 승격하지 않는다.

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

`Requirement Package/AD/ADR → Spec → machine contract → provider projection → static validation → authenticated
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
- Provider canary는 local/manual lane에서 인증 후 실행한다. 현재 Codex와 Claude의
  provider set 및 필요한 canary record는 registry에서 도출하며, GitHub Actions에는 provider
  credential을 추가하지 않는다.
- Spec 039의 baseline workflow/QA를 먼저 완료한다. 현재 agent-governance lane은
  registry-derived contract/schema parity, Codex·Claude provider config parse, eval fixture,
  legacy/orphan pattern을 검사하며 `permissions` 최소화와 third-party action full commit SHA를
  사용한다. 근거는 [GitHub secure use](https://docs.github.com/en/actions/reference/security/secure-use)다.
- Local QA는 targeted → affected → staged → tests →
  [`pre-commit run --all-files`](https://pre-commit.com/) → formatter review → rerun →
  `git diff --check`/scope review 순서다. 실패 수정 뒤 관련 lane을 다시 실행한다.
- Spec 0054의 current closure는 repository quality gate, all-files, registry-derived Codex·Claude
  canary record, eval/model fitness, zero-legacy, independent whole-branch review와 clean tree를
  요구한다. `ABSENT`/`DEFER` provider record는 runtime readiness PASS가 아니며 owner/trigger가
  필수다. 이전 three-provider/12/48 closure 수치는 historical predecessor evidence일 뿐 current
  acceptance 기준이 아니다.

## Traceability

### Lifecycle Traceability

The table below retains the implemented predecessor delta while routing its
current interpretation to ADR-0030 and Spec 0054. ADR-0019 and ADR-0013 remain
historical predecessors; their fixed provider/cardinality clauses are not
current authority.

| Upstream requirement | Quality attribute or boundary | ADR / Spec |
| --- | --- | --- |
| [REQ-0003-FR-0001](../../01.requirements/0003-workspace-agent-governance-platform.md) | Stage 00 durable policy와 owner graph | [ADR 0019](../decisions/0019-provider-native-agent-harness-and-loop-model.md) |
| [REQ-0003-FR-0002](../../01.requirements/0003-workspace-agent-governance-platform.md) | Thin gateway와 provider projection | [ADR 0019](../decisions/0019-provider-native-agent-harness-and-loop-model.md) |
| [REQ-0003-FR-0003](../../01.requirements/0003-workspace-agent-governance-platform.md) | Skill provenance와 gap evidence | [ADR 0019](../decisions/0019-provider-native-agent-harness-and-loop-model.md) |
| [REQ-0003-FR-0004](../../01.requirements/0003-workspace-agent-governance-platform.md) | Strategy axis와 scope owner | [ADR 0019](../decisions/0019-provider-native-agent-harness-and-loop-model.md) |
| [REQ-0003-FR-0005](../../01.requirements/0003-workspace-agent-governance-platform.md) | Execution/checkpoint/handoff evidence | [ADR 0019](../decisions/0019-provider-native-agent-harness-and-loop-model.md) |
| [REQ-0003-FR-0006](../../01.requirements/0003-workspace-agent-governance-platform.md) | Form/profile와 routing contract | [ADR 0019](../decisions/0019-provider-native-agent-harness-and-loop-model.md) |
| [REQ-0003-FR-0007](../../01.requirements/0003-workspace-agent-governance-platform.md) | GitOps, secret, privilege와 approval boundary | [ADR 0019](../decisions/0019-provider-native-agent-harness-and-loop-model.md) |
| [REQ-0003-FR-0008](../../01.requirements/0003-workspace-agent-governance-platform.md) | Registry-derived admitted-provider projection | [ADR 0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md) |
| [REQ-0003-FR-0009](../../01.requirements/0003-workspace-agent-governance-platform.md) | Provider schema/model/effort/MCP와 canary | [ADR 0019](../decisions/0019-provider-native-agent-harness-and-loop-model.md) |
| [REQ-0003-FR-0010](../../01.requirements/0003-workspace-agent-governance-platform.md) | Machine harness contract/schema | [ADR 0019](../decisions/0019-provider-native-agent-harness-and-loop-model.md) |
| [REQ-0003-FR-0011](../../01.requirements/0003-workspace-agent-governance-platform.md) | Bounded loop/checkpoint/compaction | [ADR 0019](../decisions/0019-provider-native-agent-harness-and-loop-model.md) |
| [REQ-0003-NFR-0001](../../01.requirements/0003-workspace-agent-governance-platform.md) | Registry-derived parity and eval/admission | [ADR 0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md) |
| [REQ-0003-NFR-0002](../../01.requirements/0003-workspace-agent-governance-platform.md) | CI/QA/all-files evidence | [ADR 0019](../decisions/0019-provider-native-agent-harness-and-loop-model.md) |
| [REQ-0003-IF-0001](../../01.requirements/0003-workspace-agent-governance-platform.md) | Legacy cutover/current-owner integrity | [ADR 0019](../decisions/0019-provider-native-agent-harness-and-loop-model.md) |
| [REQ-0003-IF-0002](../../01.requirements/0003-workspace-agent-governance-platform.md) | Evidence-only external role admission | [ADR 0019](../decisions/0019-provider-native-agent-harness-and-loop-model.md) |
| N/A — [Acceptance criterion 01](../../01.requirements/0003-workspace-agent-governance-platform.md) remains package-owned | Owner graph consistency | [ADR 0019](../decisions/0019-provider-native-agent-harness-and-loop-model.md) |
| N/A — [Acceptance criterion 02](../../01.requirements/0003-workspace-agent-governance-platform.md) remains package-owned | Reciprocal lifecycle chain | [ADR 0019](../decisions/0019-provider-native-agent-harness-and-loop-model.md) |
| N/A — [Acceptance criterion 03](../../01.requirements/0003-workspace-agent-governance-platform.md) remains package-owned | Gateway/evidence-class separation | [ADR 0019](../decisions/0019-provider-native-agent-harness-and-loop-model.md) |
| N/A — [Acceptance criterion 04](../../01.requirements/0003-workspace-agent-governance-platform.md) remains package-owned | Repository static gate | [ADR 0019](../decisions/0019-provider-native-agent-harness-and-loop-model.md) |
| N/A — [Acceptance criterion 05](../../01.requirements/0003-workspace-agent-governance-platform.md) remains package-owned | Template form authority | [ADR 0019](../decisions/0019-provider-native-agent-harness-and-loop-model.md) |
| N/A — [Acceptance criterion 06](../../01.requirements/0003-workspace-agent-governance-platform.md) remains package-owned | Registry-derived role/provider parity | [ADR 0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md) |
| N/A — [Acceptance criterion 07](../../01.requirements/0003-workspace-agent-governance-platform.md) remains package-owned | Admitted-provider independent canary classification and readiness evidence | [ADR 0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md) |
| N/A — [Acceptance criterion 08](../../01.requirements/0003-workspace-agent-governance-platform.md) remains package-owned | Contract/schema/provider parity | [ADR 0019](../decisions/0019-provider-native-agent-harness-and-loop-model.md) |
| N/A — [Acceptance criterion 09](../../01.requirements/0003-workspace-agent-governance-platform.md) remains package-owned | Recovery fixture and safe resume | [ADR 0019](../decisions/0019-provider-native-agent-harness-and-loop-model.md) |
| N/A — [Acceptance criterion 10](../../01.requirements/0003-workspace-agent-governance-platform.md) remains package-owned | Eval/model-fitness evidence | [ADR 0019](../decisions/0019-provider-native-agent-harness-and-loop-model.md) |
| N/A — [Acceptance criterion 11](../../01.requirements/0003-workspace-agent-governance-platform.md) remains package-owned | CI and all-files gate | [ADR 0019](../decisions/0019-provider-native-agent-harness-and-loop-model.md) |
| N/A — [Acceptance criterion 12](../../01.requirements/0003-workspace-agent-governance-platform.md) remains package-owned | Zero stale legacy/orphan reference | [ADR 0019](../decisions/0019-provider-native-agent-harness-and-loop-model.md) |

- **Requirement Package**: [REQ-0003](../../01.requirements/0003-workspace-agent-governance-platform.md)
- **Current terminal decision**: [ADR 0030](../decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md)
- **Current implementation authority**: [Spec 0054](../../03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md)
- **Historical accepted predecessor**: [ADR 0019](../decisions/0019-provider-native-agent-harness-and-loop-model.md)
- **Historical accepted predecessor**: [ADR 0013](../decisions/0013-stage-00-canonical-adapter-model.md)
- **Prerequisites**: [Spec 038](../../03.specs/0038-reference-information-architecture/spec.md),
  [Spec 039](../../03.specs/0039-github-ci-qa-evidence/spec.md),
  [Spec 040](../../03.specs/0040-contract-cutover-and-program-closure/spec.md)
- **Delivery sequence**: [Spec 041](../../03.specs/0041-stage-00-agent-governance-contract/spec.md),
  [Spec 042](../../03.specs/0042-provider-native-runtime-and-model-evidence/spec.md),
  [Spec 043](../../03.specs/0043-agent-harness-loop-lifecycle/spec.md),
  [Spec 044](../../03.specs/0044-agent-roster-evaluation-and-admission/spec.md),
  [Spec 045](../../03.specs/0045-agent-governance-ci-qa-cutover/spec.md),
  [Spec 046](../../03.specs/0046-agent-governance-program-closure/spec.md)
- **Agent design**: [Workspace Agent Governance Program Design](../../03.specs/0041-stage-00-agent-governance-contract/spec.md)
