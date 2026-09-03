---
title: 'Provider-Native Agent Harness and Loop Model'
version: "1.0.0"
type: sdlc/architecture-decision
layer: "architecture"
status: superseded
owner: platform
updated: 2026-08-01
artifact_id: "ADR-0019"
superseded_by: "ADR-0030"
---

# ADR-0019: Provider-Native Agent Harness and Loop Model

## Overview

이 ADR은 Stage 00 canonical governance를 local/Antigravity, Claude, Codex, Gemini의 네
surface에 투영하고, 단일 machine harness contract, 역할별 model/effort, bounded execution
loop, eval과 strict runtime evidence로 운영한다는 결정을 기록한다. Spec 046의
repository-local terminal transition에서 이 결정은 `accepted` current decision이 되었다.
ADR-0013은 계속 `accepted`이며, earlier tranche 실행을 지배한 historical predecessor로
보존된다.

고정 외부 사실 관찰 기준은 **2026-07-10 10:00 Asia/Seoul**
(`2026-07-10T01:00:00Z`)이다.

## Context

ADR-0013은 Stage 00 canonical core와 provider adapter 분리를 정착시켰지만, 당시 Gemini CLI
native surface는 absent/`DEFER`였고 machine semantic contract는 10개 역할과 3개 adapter
surface만 다뤘다. 현재 프로그램은 Gemini native project surface, provider config/MCP,
role-specific model/effort, authenticated canary, retry/checkpoint/compaction, eval/admission 및
agent-governance CI를 하나의 lifecycle로 닫아야 한다.

[OpenAI Harness Engineering](https://openai.com/index/harness-engineering/)은 짧은 agent map,
repository knowledge SSoT, 기계적 invariant, 격리된 worktree와 반복 feedback이 agent-first
개발의 신뢰성을 만든다고 설명한다. Claude
[subagent](https://code.claude.com/docs/en/sub-agents)·[configuration](https://code.claude.com/docs/en/configuration)·
[hook](https://code.claude.com/docs/en/hooks), Codex
[subagent](https://learn.chatgpt.com/docs/agent-configuration/subagents)·
[configuration](https://learn.chatgpt.com/docs/config-file/config-reference),
Gemini [subagent](https://geminicli.com/docs/core/subagents/)·
[hook](https://geminicli.com/docs/hooks/reference/)는
서로 다른 native schema와 enforcement 경계를 제공한다. 따라서 공통 semantic을 공유하되
provider syntax와 실제 runtime evidence는 분리해야 한다.

후보군은 Claude의 account-available `opus`/`fable`/`sonnet`/`haiku`, Codex의 documented
`gpt-5.6` 및 balanced candidates, Gemini의 `gemini-3-pro-preview`/
`gemini-3-flash-preview`/Auto다. 구체 ID와 effort는 provider 문서, installed client의
native parse, account availability와 동일 corpus eval로 결정한다. 모델 발표나 최신 이름은
특정 역할 적합성을 증명하지 않으며, tracked `.gemini/**`의 존재와 authenticated runtime
readiness를 같은 claim으로 둘 수 없다.

활성 Specs [038](../../98.archive/completed/03.specs/0038-reference-information-architecture/spec.md),
[039](../../98.archive/completed/03.specs/0039-github-ci-qa-evidence/spec.md),
[040](../../98.archive/completed/03.specs/0040-contract-cutover-and-program-closure/spec.md)은 reference IA, baseline
CI/QA와 기존 program closure를 소유한다. 이 세 Spec이 완료되기 전에는 새 adapter나 legacy
cutover를 시작하지 않는다.

## Decision

다음을 **accepted current architecture**로 채택한다. Specs 041–046은 foundation-first
순서로 구현·검증되었고, Spec 046의 repository-local closure contract와 독립 검토를 거친
terminal lifecycle change가 이 결정을 수락했다.

### Canonical contract and four projections

- Durable policy는 `docs/00.agent-governance/**`가 소유하고 root/provider gateway는 짧은 map으로 유지한다.
- `docs/00.agent-governance/contracts/harness-contract.json`과 schema를 역할 semantic,
  surface projection, evidence, permission, stop와 handoff의 단일 machine owner로 둔다.
- `.agents/**`는 shared assets 및 local/Antigravity adapter이고 Gemini native surface가 아니다.
- `.claude/**`, `.codex/**`, `.gemini/**`는 각각 provider-native syntax를 표현한다. Common
  semantic을 복제하거나 unsupported native capability를 주장하지 않는다.
- Spec 041이 구형 역할 의미 계약의 소비자를 전환했고 Spec 045가
  zero-consumer 증거 뒤 그 compatibility 입력을 제거한다.
  `scripts/validation/registry.json`은 validation routing owner로 별도 유지한다.

### Provider-native metadata, config and evidence

- Claude adapter candidate fields are `name`, `description`, `model`, `tools`; `effort`와
  `maxTurns`는 dated cutoff evidence 또는 native schema canary가 허용할 때만 사용한다.
- Codex adapter candidate fields are `name`, `description`, `developer_instructions`, `model`,
  `model_reasoning_effort`와 project config다. Dated evidence 또는 native config validation
  전에는 cutoff-proven field라고 주장하지 않는다.
- Gemini의 현재 repo-static adapter fields는 Spec 044가 닫힌 형태로 소유하는
  `name`, `description`, `kind`, `max_turns`, `timeout_mins`다. Spec 042의
  `tools`/`model` 목록은 observation-time candidate 이력이며, generic tool alias와
  exact model/reasoning은 model-fitness contract와 native canary가 별도로 소유한다.
- Project config/MCP는 tracked secret-free baseline과 allowlist만 소유하고, user credential과
  private config를 수정·수집하지 않는다.
- Repo-static parse, native discovery, authenticated controlled run을 별도 evidence class로 둔다.
  Claude/Codex/Gemini마다 독립 canary record가 필요하다. 해당 provider runtime readiness는
  PASS만 증명하며, repository-local closure는 `ABSENT`/`DEFER`에 limitation, owner와 retry
  trigger가 있을 때 허용한다.

### Role-specific model and effort

- 모든 역할에 한 모델을 강제하지 않는다. Complexity, risk/blast radius, context, tool use,
  latency/cost, provider-supported effort enum과 eval 결과를 입력으로 role별 결정을 내린다.
- Model page나 release announcement는 candidate availability 근거이고, 역할 배정은 Spec 042
  schema/canary와 Spec 044 fixture/model-fitness가 확정한다.
- Fallback은 silent substitution이 아니라 실제 model, reason과 capability limitation을 evidence에 남긴다.

### Bounded loop and recoverable state

- 동일 normalized failure signature의 자동 재시도는 최대 2회다.
- Task 전체 자동 recovery는 기본 최대 3회다.
- 동일 결과가 2회 반복되고 progress delta가 없으면 즉시 stop/escalate한다.
- `.agent-work/checkpoint.json`은 ignored transient state로서 task ID, attempt, failure class,
  completed/remaining work, validation summary, next action만 보존한다.
- Checkpoint와 compaction에는 credential, token, auth path/content, shell history와 full/raw
  transcript를 저장하지 않는다. Resume는 current repository state를 다시 읽고 checkpoint를
  보조 evidence로만 사용한다.

### Roster, eval and admission

- 기존 10개 canonical role에 `docs-researcher`, `quality-engineer`를 추가한 12-role roster를 둔다.
- 네 surface에 역할당 하나의 adapter를 투영하여 목표 cardinality를 48로 고정한다.
- 각 역할은 input/output, responsibility, prohibited action, permission, stop, handoff,
  required evidence, eval fixture와 model-fitness evidence를 갖는다.
- [agency-agents](https://github.com/msitarzewski/agency-agents)는 아이디어 catalog일 뿐이다.
  새 역할은 repository gap과 위 admission contract를 fixture가 증명할 때만 추가한다.

### CI, QA and cutover

- Spec 039가 baseline GitHub CI/QA evidence를 먼저 닫고, Spec 045는 contract/schema,
  12/48 parity, provider config parse, eval fixture 및 legacy/orphan detection을 위한
  agent-governance static lane을 추가한다.
- GitHub Actions는 least privilege와 third-party action full commit SHA 원칙을 따른다
  ([GitHub secure use](https://docs.github.com/en/actions/reference/security/secure-use)).
- Provider credential은 GitHub-hosted CI에 추가하지 않고 authenticated canary는 local/manual
  lane에서 실행해 secret-free 결과만 기록한다.
- Local QA는 targeted → affected → staged → tests →
  [`pre-commit run --all-files`](https://pre-commit.com/) → formatter review → rerun →
  diff/scope review 순서로 실행한다.
- Consumer-first migration 후 old contract/schema, duplicate roster·matrix, stale 10/30/3,
  `.gemini`-surface-absent claim 및 obsolete runtime/model claim을 active surface에서
  제거한다. 실제 provider runtime `ABSENT`/`DEFER` evidence는 별도 class로 보존한다.

### Delivery order and replacement gate

1. Spec 041: Stage 00 machine contract와 consumer migration foundation.
2. Spec 042: Provider-native surface, config/MCP, cutoff model evidence와 authenticated canary.
3. Spec 043: Harness loop, retry, checkpoint, compaction, resume/handoff fixture.
4. Spec 044: 12-role/48-adapter roster, eval/admission와 role model fitness.
5. Spec 045: Agent-governance CI/QA 및 legacy/current-owner cutover.
6. Spec 046: Strict closure, independent whole-branch review와 ADR replacement readiness.

Spec 046의 repository-local evidence는 repository quality gate, all-files QA, 세 provider
canary record의 독립 classification, 12/48 parity, configured model/evaluation readiness,
zero stale legacy와 독립 검토를 닫았다. 이 terminal transition은 ADR-0019를 current
decision으로 수락하지만, `ABSENT`/`DEFER` record는 해당 provider runtime readiness를
계속 열어 둔다. AGPC-005의 local `main` integration과 worktree cleanup도 별도 operational
handoff로 남아 있으며 이 accepted decision을 external 또는 runtime PASS로 확장하지 않는다.

## Explicit Non-goals

- ADR-0013의 historical context를 다시 쓰거나 accepted predecessor evidence를 삭제하는 것.
- 네 provider별 독립 governance, roster 또는 QA/model vocabulary를 만드는 것.
- Unverified field/model을 provider config에 추측으로 추가하는 것.
- Provider CLI/auth 전환을 우회하거나 credential을 repository/CI에 저장하는 것.
- Agent retry를 완료 보장 수단으로 무한 반복하거나 checkpoint에 전체 대화를 보존하는 것.
- Eval 없이 외부 catalog 역할을 추가하거나 48개보다 많은 adapter를 목표로 부풀리는 것.
- Live Kubernetes/external service 변경 또는 이 프로그램과 무관한 source/template 개편.

## Consequences

### Positive

- 한 machine contract가 역할 semantic과 네 surface parity를 기계적으로 검증한다.
- Provider-native capability와 runtime readiness의 과장된 claim을 방지한다.
- 역할별 model/effort를 성능·위험·비용 evidence로 조정할 수 있다.
- Bounded retry와 compact checkpoint가 무한 loop, context bloat와 불투명한 handoff를 줄인다.
- Eval/admission과 CI가 agent roster와 governance drift를 feedback loop로 되돌린다.
- Consumer-first legacy cutover가 duplicate current owner와 stale cross-link를 제거한다.

### Costs and trade-offs

- 12 roles를 네 syntax로 유지하므로 48 adapter의 parity validator와 fixture 유지 비용이 생긴다.
- 세 provider canary record를 유지해야 하며 unavailable provider는 runtime-readiness follow-up을 남긴다.
- Provider model/schema 갱신은 cutoff ledger, config parse, canary와 eval을 반복해야 한다.
- 동일 semantic도 provider의 tool, hook, sandbox, recursion 차이 때문에 enforcement level은 다를 수 있다.
- Strict loop ceiling은 자동 복구 가능한 작업도 조기에 human escalation할 수 있지만, 반복 무진행보다 관측 가능성을 우선한다.

### Operational implications

- ADR-0019 acceptance 이후에도 current runtime claim은 구현된 repository evidence와 분리된
  provider/runtime evidence class를 따라야 한다.
- Spec별 implementer, requirements reviewer, quality/security reviewer와 root verification을 분리한다.
- Model/effort 또는 canary 결과는 provider note와 evaluation evidence를 함께 갱신한다.
- External facts가 기준 시점 이후 변경되어도 기록을 소급 수정하지 않고 새 evidence refresh를 남긴다.

## Alternatives

### ADR-0013을 직접 수정하고 Gemini만 추가

- 장점: 문서와 migration 범위가 작다.
- 기각 이유: historical accepted decision의 absent/DEFER 맥락이 사라지고 contract, loop, eval,
  provider별 canary readiness와 replacement gate를 하나의 새 결정으로 추적할 수 없다.

### Provider별 독립 roster와 model policy

- 장점: 각 provider의 native 기능과 release cadence에 빠르게 최적화할 수 있다.
- 기각 이유: 역할 semantic, stop/handoff, QA와 current-owner가 네 군데로 분기되어 drift와
  과장된 capability claim을 기계적으로 막기 어렵다.

### Repo-static validation만으로 runtime readiness까지 closure

- 장점: credential과 CLI 설치 없이 CI에서 재현하기 쉽다.
- 기각 이유: 파일 parse는 provider discovery, authentication, selected model과 controlled
  run을 증명하지 못한다. Repository-local closure와 provider-runtime readiness를 같은 PASS로
  합치지 않는다.

### Unbounded retry와 transcript 기반 resume

- 장점: 사람 개입 전 Agent가 더 오래 시도하고 상세 context를 보존한다.
- 기각 이유: 동일 실패 반복, 비용 폭증, secret/context leakage와 stale-state 재사용 위험이 커진다.

### agency-agents roster를 직접 채택

- 장점: 많은 전문 역할을 빠르게 확보할 수 있다.
- 기각 이유: 외부 persona catalog는 이 repository의 permission, stop, handoff, GitOps와 eval
  요구를 증명하지 않으며 역할 수와 유지 표면만 불필요하게 늘린다.

## Traceability

### Lifecycle Traceability

| Decision lineage | Replacement relation | Affected Spec |
| --- | --- | --- |
| [ARD 0006](../descriptions/0006-workspace-agent-governance-platform.md) | ADR-0019가 accepted current decision이며 [ADR 0013](0013-stage-00-canonical-adapter-model.md)은 earlier tranche의 accepted historical predecessor다. | [Spec 041](../../98.archive/completed/03.specs/0041-stage-00-agent-governance-contract/spec.md) |
| N/A — shared ARD 0006 source above | Provider adoption은 accepted history를 보존하는 conditional replacement다. | [Spec 042](../../98.archive/completed/03.specs/0042-provider-native-runtime-and-model-evidence/spec.md) |
| N/A — shared ARD 0006 source above | Loop lifecycle은 accepted ADR-0019의 repository-static contract다. | [Spec 043](../../98.archive/completed/03.specs/0043-agent-harness-loop-lifecycle/spec.md) |
| N/A — shared ARD 0006 source above | Roster/eval은 exact parity evidence가 있어야 replacement에 포함된다. | [Spec 044](../../98.archive/completed/03.specs/0044-agent-roster-evaluation-and-admission/spec.md) |
| [ADR 0013](0013-stage-00-canonical-adapter-model.md) | Consumer-first cutover 후 old 3-surface 결정을 historical record로 보존한다. | [Spec 045](../../98.archive/completed/03.specs/0045-agent-governance-ci-qa-cutover/spec.md) |
| N/A — shared ADR 0013 source above | Spec 046 repository-local terminal transition이 current decision을 ADR-0019로 전환했고 external lane은 분리된 상태로 남는다. | [Spec 046](../../98.archive/completed/03.specs/0046-agent-governance-program-closure/spec.md) |

- **PRD**: [PRD 003](../../01.requirements/0003-workspace-agent-governance-platform.md)
- **ARD**: ARD 0006 (linked in the lifecycle table above)
- **Current accepted decision**: ADR 0019 (this record)
- **Historical accepted predecessor**: ADR 0013 (linked in the lifecycle table above)
- **Prerequisites**: [Spec 038](../../98.archive/completed/03.specs/0038-reference-information-architecture/spec.md),
  [Spec 039](../../98.archive/completed/03.specs/0039-github-ci-qa-evidence/spec.md),
  [Spec 040](../../98.archive/completed/03.specs/0040-contract-cutover-and-program-closure/spec.md)
- **Agent design**: [Workspace Agent Governance Program Design](../../98.archive/completed/03.specs/0041-stage-00-agent-governance-contract/spec.md)
