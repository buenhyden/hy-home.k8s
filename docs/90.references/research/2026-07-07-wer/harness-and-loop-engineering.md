---
title: 'Reference: Harness and Loop Engineering Research'
type: content/reference
status: draft
owner: platform
updated: 2026-07-09
---

# Reference: Harness and Loop Engineering Research

## Overview

이 문서는 AI 에이전트가 소프트웨어 엔지니어로서 동작할 때 요구되는 하네스 엔지니어링(Harness Engineering) 및 루프 엔지니어링(Loop Engineering)의 핵심 개념과 요소를 분석한다. 또한 `hy-home.k8s` 워크스페이스에 이들을 실제로 이식하기 위해 필요한 구체적 체계, 환경, 규칙을 정적 참조로 기술한다.

본 문서는 2026-07-07 기준 공식 OpenAI/Codex, Anthropic/Claude Code, Google/Gemini, MCP 명세 및 리포지토리 실제 증적을 분석한 최신 내용을 바탕으로 작성되었다.

이 문서는 설명용 참고 문서로서, 실제 에이전트 런타임 제어권이나 리포지토리 실행 제약 조건 정책을 직접 규정하지 않는다.

## Purpose

- 하네스 엔지니어링 및 루프 엔지니어링의 주요 학술/산업적 연구를 요약하고, 워크스페이스 적용 모델과의 매핑 제공.
- 에이전트가 스스로의 행위 환경과 제어 루프를 깊이 이해하도록 lookup Context 역할 수행.
- 에이전트 행위를 구속하는 환경적 요구 조건(WSL2, k3d, GitOps) 및 도구의 신뢰 범위 식별.

## Reference Type

- Type: durable-concept / external-standard-snapshot
- Source checked: 2026-07-07 (OpenAI harness engineering and MCP security sources re-verified 2026-07-09)
- Refresh trigger: 프로바이더 하네스/루프 관련 아티클 릴리즈, MCP 보안 권고안 개정, 리포지토리 정적 검증 도구셋 변경.

## Authority Boundary

- **Authoritative for**:
  - 하네스 및 루프 엔지니어링 요소 정의와 조사 내용.
  - 외부 하네스/루프 개념이 본 워크스페이스의 4요소 모델(Instruction, Constraints, Feedback, Knowledge)에 어떻게 이식되는지에 대한 설명.
- **Not authoritative for**:
  - 실제 에이전트 로스터 지정 (`harness-catalog.md`가 소유).
  - 실제 실행 시 통제 제약 조건 (`rules/` 및 `.claude/settings.json` 등이 소유).

## Scope

- 하네스 엔지니어링 요소 및 분석, 루프 엔지니어링 요소 및 분석, 워크스페이스 적용을 위한 체계/환경/규칙, MCP 도구 경계의 보안성 분석.
- 실 클러스터 상의 동적 테스트나 런타임 인프라 상태 변경 제외.

## Definitions / Facts

### 1. 하네스 엔지니어링(Harness Engineering)에 대한 요소 조사 및 분석

하네스 엔지니어링은 AI 에이전트가 주도적으로 작업을 완료할 수 있도록 에이전트를 둘러싼 리포지토리 환경, 도구, 제약 조건, 지식 저장소 등을 에이전트 친화적으로 디자인하는 것을 의미한다. 엔지니어의 Leverage는 코드 개별 행을 직접 작성하는 데서 에이전트가 안전하고 정확하게 기동할 수 있는 '하네스(마구, 안전 벨트)'를 설계하는 데로 이동한다.

주요 하네스 구성 요소는 다음과 같다:

- **Instruction / Settings (지시 및 설정)**: 에이전트의 정체성, 행동 수칙, JIT 거버넌스 가이드라인 등을 담은 진입점 파일.
- **Architecture Constraints (구조적 제약)**: 파일 쓰기가 허용되는 경로의 제한, plaintext secret 생성 금지, live cluster 직접 변경 제한 등의 안전 규정.
- **Feedback Loops (피드백 루프)**: 린터, 구문 분석기, 정적 테스터 등을 활용해 변경 결과를 실시간으로 모델에 피드백해주는 정적/동적 검증 스크립트.
- **Knowledge Stores (지식 저장소)**: 이전 세션에서의 수행 이력(progress ledger)이나, 컴포넌트별 spec, architecture 문서들의 중앙 저장소.

OpenAI의 harness engineering 논의(2026-07-09 확인)는 하네스를 "모델을 둘러싼 전체 계약(the full contract around the model)"으로 정의하며, 그 구성으로 **instructions, tools, routing, output requirements, validation checks**를 명시한다. 핵심 원칙은 "humans steer while agents execute"이며, 실패가 발생했을 때 해법은 "더 열심히 시도"가 아니라 "어떤 capability가 빠졌고 그것을 에이전트에게 어떻게 legible(가독)하고 enforceable(강제 가능)하게 만들 것인가"를 묻는 것이다. 본 워크스페이스의 4요소 모델(Instruction, Constraints, Feedback, Knowledge)은 이 계약을 리포지토리 정적 검증 가능한 형태로 이식한 구현이다.

### 2. 루프 엔지니어링(Loop Engineering)에 대한 요소 조사 및 분석

루프 엔지니어링은 에이전트가 최초의 요구사항 분석(Intake)에서 시작하여 최종 검증 및 Handoff까지 안전하게 도달하도록 통제 사이클(Control Cycle)을 구조화하는 일이다.
일반적인 에이전트 실행 루프는 다음과 같다:

1. **Observe (관찰)**: 현재 워크스페이스 상태, Spec 문서, 이슈 레코드 및 Validator 실행 결과를 읽음.
2. **Plan (계획)**: 변경할 최소 범위 식별, 성공 기준 수립, 위험 요인 도출 및 구현 계획서 작성.
3. **Act (행위)**: least-privilege 도구를 사용하여 대상 경로의 파일 수정 및 신규 생성.
4. **Verify (검증)**: static validator를 활용해 구문 오류, 린트 및 거버넌스 위반 여부를 즉각 평가.
5. **Learn (학습/피드백)**: 발생한 오류 원인이나 compact progress 내용을 progress memory에 기록해 다음 세션으로 전달.

단순 `Prompt-Response`의 일회성 사이클이 아니라, `Observable evidence -> constrained execution -> verification -> meta-learning`의 피드백 제어 루프를 설계하는 것이 핵심이다.

#### 루프 종료 조건 및 안전 경계 (Loop Termination & Safety Bounds)

제어 루프는 무한히 도는 것이 아니라 **bounded loop**여야 하며, 종료 조건과 안전 경계가 명시되어야 한다. 종료 조건이 없으면 루프는 검증 실패를 반복하거나(비수렴), 미완료 상태에서 Handoff되어 다음 세션에 위험을 전가한다. 본 워크스페이스는 이 경계를 `docs/00.agent-governance/hooks/lifecycle-guard.sh`가 wiring된 lifecycle 훅으로 구현한다.

- **정상 종료 (Verify 통과 → Learn → Stop)**: static validator가 통과하고 progress ledger에 결과가 기록되면 루프는 정상 종료한다. 이것이 에이전트 완료의 최우선 기준(정적 검증 통과)이다.
- **차단 종료 (Stop / SubagentStop = block)**: `lifecycle-guard.sh`는 Stop 및 SubagentStop 시점에서 **객관적 repo-state 검증 실패를 block**할 수 있고, 미커밋 tracked 변경에 대해 작업 단위 커밋 규율을 권고한다. 즉 검증 실패는 조용히 종료되지 않고 루프를 되돌린다.
- **비차단 경계 (PreCompact = advisory)**: PreCompact 시점은 **advisory**이며 compaction을 막지 않는다. 미커밋 변경·권고 검증·커밋 규율을 보고할 뿐 검증 증적을 대체하지 않는다. 따라서 컨텍스트 압축이 검증을 우회하는 경로가 되지 않는다.
- **Handoff 경계**: 루프가 미완료로 종료될 때는 남은 위험과 다음 단계를 progress memory에 기록해, 다음 세션이 Observe 단계에서 이를 복원하도록 한다. 이는 5단계 루프의 Learn을 세션 간 경계로 확장한 것이다.

핵심은 "언제 멈추는가"를 모델의 재량이 아니라 **repo-state 기반 훅 계약**으로 못박아, 루프가 legible(가독)하고 enforceable(강제 가능)한 종료 경계를 갖도록 하는 것이다.

### 3. 워크스페이스 적용을 위한 체계, 환경, 규칙 분석

워크스페이스 `hy-home.k8s`에 하네스 및 루프 엔지니어링을 적용하기 위해서는 다음 3가지 핵심 축이 갖춰져야 한다.

#### 체계 (System)

- **SDD Lifecycle 체계**: 모든 작업은 요구사항(01.requirements) -> 아키텍처(02.architecture) -> 명세(03.specs) -> 실행(04.execution) -> 운영(05.operations)의 흐름으로 물리적/논리적으로 분리 및 정렬된다.
- **Canonical-Core & Adapter 체계**: provider가 Claude, Codex, Gemini로 나뉘더라도 Role 정의, 4요소 모델, progress memory, shared templates 등은 하나의 SSoT(`.agents/`)에 집중하고, 각 프로바이더는 thin adapter만 소유해 파편화를 방지한다.

#### 환경 (Environment)

- **Local Dev Sandbox**: WSL2 Ubuntu 및 Docker, k3d 환경을 통해 로컬 클러스터를 격리한다.
- **GitOps Desired State Boundary**: 리포지토리 내의 파일이 시스템의 '진실된 최종 목표 상태(Desired State)'이며, k3d 클러스터 내의 실제 상태는 이 파일 상태에 반응하는 종속자일 뿐이다. 따라서 정적 검증 통과가 에이전트 완료의 최우선 기준이 된다.
- **Static Validation Engine**: `validate-repo-quality-gates.sh`를 포함한 스크립트 도구와 `.pre-commit-config.yaml` 환경이 자동 피드백을 실시간으로 제공한다.

#### 규칙 (Rules)

- **No Direct Live Mutation**: 에이전트가 직접 cluster에 리소스를 배포(`kubectl apply`)하거나 Vault에 비밀 정보를 밀어넣는 등의 stateful 변경 작업을 금지한다. 에이전트는 오직 PR-Ready 리포지토리 변경만을 생산한다.
- **Template Routing Rule**: 생성되는 모든 문서는 [Template Routing Contract](../../../99.templates/support/template-routing.md)에 지정된 target pattern과 mapping template을 1:1로 일치시켜야 한다.
- **Commit Discipline**: 작업 논리 단위별 개별 커밋(logical branch-commit flow)을 엄격히 준수한다.

### 4. MCP 및 도구 경계의 보안성 분석

Model Context Protocol(MCP)은 도구(Tools), 지식(Resources), 프롬프트(Prompts)를 모델에 제공하는 공통 규격이다. 공식 MCP Security Best Practices(2025-06-18 명세 계열, 2026-07-09 확인)가 명시한 주요 위협 분류와 규범적 완화책은 다음과 같다. 규범 강도(MUST/SHOULD)는 원문 표기를 따른다.

- **Local MCP Server Compromise (로컬 서버 침해)**: 로컬 실행 MCP server는 클라이언트 권한을 상속해 임의 명령을 실행할 수 있다. one-click 로컬 서버 구성은 실행 전 정확한 명령 전문을 표시하는 명시적 사용자 동의를 **MUST** 구현하고, 서버는 sandboxing(컨테이너/chroot)과 `stdio` transport로 접근을 제한(**SHOULD**)한다. 워크스페이스는 신뢰할 수 없는 MCP server 연동을 금지하고 sandboxed command execution + 디렉터리 경로 제약을 적용한다.
- **Token Passthrough (토큰 통과 안티패턴)**: MCP server는 자신에게 발급되지 않은 토큰을 수락해 downstream API로 통과시켜서는 **MUST NOT** 안 된다. rate limiting·audience 검증 등 보안 통제를 우회시키기 때문이다.
- **Confused Deputy (혼동된 대리자)**: static client ID + dynamic client registration + consent cookie 조합에서 동의 화면이 건너뛰어져 authorization code가 탈취될 수 있다. proxy server는 third-party 인가 이전에 per-client consent를 **MUST** 강제하고 `redirect_uri` 정확 일치 검증과 단회용 `state` 검증을 적용한다.
- **SSRF (서버측 요청 위조)**: 악성 MCP server가 metadata URL로 내부 자원(`169.254.169.254` 클라우드 메타데이터, 사설 IP 대역)을 겨냥할 수 있다. 클라이언트는 OAuth URL에 HTTPS를 강제하고 사설/링크로컬 IP 대역(`10/8`, `172.16/12`, `192.168/16`, `169.254/16`)을 차단(**SHOULD**)하며 egress proxy 사용을 권장한다.
- **Session Hijacking (세션 탈취)**: 서버는 인증에 세션을 사용해서는 **MUST NOT** 안 되고, 안전한 비결정적 세션 ID를 **MUST** 사용하며, 세션 데이터를 `<user_id>:<session_id>` 형태로 사용자 식별자에 바인딩(**SHOULD**)한다.
- **OAuth Authorization URL Validation (인가 URL 검증)**: 악성 server가 제공한 `javascript:`·`data:`·`file:` scheme URL은 XSS/RCE로 이어질 수 있다. 클라이언트는 `http(s)` scheme만 허용(운영은 HTTPS)하고 위험 scheme을 거부(**MUST**)하며, URL 개방 시 셸 실행을 금지(**MUST NOT**)한다.
- **Scope Minimization (스코프 최소화)**: 광범위 스코프(`*`, `full-access`) 선발급을 피하고, 최소 baseline 스코프로 시작해 권한 작업이 처음 시도될 때 `WWW-Authenticate` challenge로 점진 상향하는 least-privilege 모델을 적용한다. 이는 워크스페이스 도구/서브에이전트 `tools:`의 최소 권한 바인딩과 동일 원칙이다.

## Sources

- OpenAI: Harness engineering: leveraging Codex in an agent-first world (<https://openai.com/index/harness-engineering/>)
- OpenAI: Unrolling the Codex agent loop (<https://openai.com/index/unrolling-the-codex-agent-loop/>)
- Anthropic Claude Code settings and hooks (<https://code.claude.com/docs/>)
- Google Gemini CLI Reference and ADK framework (<https://adk.dev/>)
- Model Context Protocol Specification v2025-06-18 (<https://modelcontextprotocol.io/specification/2025-06-18>)
- MCP Security Best Practices (<https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices>)
- [Local Harness Catalog](../../../00.agent-governance/harness-catalog.md)
- [Lifecycle Guard Hook](../../../00.agent-governance/hooks/lifecycle-guard.sh)

## Review and Freshness

- Review cadence: on source or catalog change
- Last reviewed: 2026-07-09
- Next review trigger: MCP 보안 권고안 업데이트, 프로바이더 에이전트 루프 관련 아티클 릴리즈

## Related Documents

- **Parent research README**: [README.md](../README.md)
- **References README**: [../../README.md](../../README.md)
- **Workspace baseline**: [workspace-governance-baseline.md](workspace-governance-baseline.md)
- **Harness Catalog**: [../../../00.agent-governance/harness-catalog.md](../../../00.agent-governance/harness-catalog.md)
- **Implementation Map**: [../../../00.agent-governance/harness-implementation-map.md](../../../00.agent-governance/harness-implementation-map.md)
