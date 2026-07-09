---
title: 'Reference: Provider Harness Implementation Status Research'
type: content/reference
status: draft
owner: platform
updated: 2026-07-09
---

# Reference: Provider Harness Implementation Status Research

## Overview

이 문서는 Claude Code, Codex/OpenAI, Gemini/Google의 AI 에이전트 하네스/루프 실행 기능(Upstream capability)과 `hy-home.k8s` 워크스페이스에 구현된 프로바이더 어댑터(Adapter) 상태를 비교 분석하여 정리한다.

2026-07-07 기준의 최신 공식 문서와 리포지토리 실제 구성 상태를 바탕으로 작성되었으며, 특히 최근 spec-driven 설계 후 완료된 `observability-reviewer`와 `network-reviewer` 에이전트의 3대 프로바이더 어댑터 형상 동기화 상태를 상세 분석에 포함하였다.

이 문서는 참고 자료이며, 실제 프로바이더의 런타임 제어 설정이나 워크스페이스 정책을 재정의하지 않는다.

## Purpose

- 프로바이더별 에이전트 구동 기능의 차이점과 공통점을 조사 및 분석하여 기술적 baseline 제공.
- 각 프로바이더 고유 기능(Upstream features)과 본 워크스페이스에서 수용하는 실제 구현체(Local adapter status) 간의 경계를 식별.
- 3대 프로바이더(Claude, Codex, Gemini)의 공통 환경 및 규칙 체계 구축 방안 제시.

## Reference Type

- Type: durable-concept / external-standard-snapshot / dated-implementation-audit
- Source checked: 2026-07-07
- Refresh trigger: Claude Code, Codex/OpenAI, Gemini CLI, Google ADK/Enterprise Agent Platform 등의 업데이트 및 리포지토리 어댑터 변경.

## Authority Boundary

- **Authoritative for**:
  - 2026-07-07 기준 프로바이더별 업스트림 기능 비교 및 리포지토리 내 구현 상태 기술.
  - 공통 거버넌스 코어와 프로바이더별 어댑터 매핑 정의.
- **Not authoritative for**:
  - 실제 에이전트 실행 및 툴 권한 제어.
  - 프로바이더 설정 파일 직접 수정 권한.

## Scope

- Claude Code, Codex/OpenAI, Gemini CLI 및 Google ADK의 지시 파일, 서브에이전트, 훅 자동화, 스킬 확장, MCP 툴 연동, 샌드박싱/권한 제어 비교.
- 3대 프로바이더 공통 체계 구축의 요소 및 현황.
- 실제 런타임 클러스터 조작 및 Vault 비밀정보 갱신 제외.

## Definitions / Facts

### 1. 프로바이더 기능 비교 및 분석 (Provider Capability Matrix)

| 구분                          | Claude Code                                                                                                        | Codex/OpenAI                                                                                                       | Gemini/Google CLI & ADK                                                                    |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------ |
| **지시 파일 & 설정**          | Hierarchical settings (`.claude.json`), project/user/local config 지원.                                            | `config.toml` 프로젝트/사용자 레이어, `AGENTS.md`를 포함한 규칙 로딩.                                              | `GEMINI.md` 컨텍스트 파일 자동 탐색 및 비대화형 자동화 지원.                               |
| **서브에이전트 (Delegation)** | `.claude/agents/*.md` 기반 specialized agents 구동, model/tool/permissions 위임 제어.                              | `.codex/agents/*.toml` 양식을 지닌 프로젝트 레벨 서브에이전트 구동 및 샌드박스 상속.                               | Google ADK를 통한 멀티에이전트 그래프 구성. Gemini CLI는 단순 스크립트 비대화형 위임 지원. |
| **훅 & 자동화 (Hooks)**       | SessionStart, PreToolUse, PostToolUse, Stop, SubagentStop, PreCompact 훅이 exit-code를 통해 모델 동작을 통제 가능. | `hooks.json`에 선언된 수명주기 쉘 명령 연동 및 샌드박스 가두기 지원.                                               | `.agents/hooks.json` 기반 수명주기 이벤트 정의 및 쉘 트리거 연동.                          |
| **스킬 & 확장 (Skills)**      | `SKILL.md` 구조의 project/plugin 스킬 로딩 지원.                                                                   | `.agents/skills/`를 통해 model-specific progressive disclosure 지원.                                               | Google ADK 내 Graph Workflows 및 Custom Tools/Skills 연동 지원.                            |
| **MCP & 툴 연동**             | Local/project-specific `.mcp.json` 연동 및 서브에이전트 전용 툴 매핑 지원.                                         | `config.toml` 내 STDIO/HTTP MCP 서버 연동 및 인증 연동 지원.                                                       | Gemini CLI 내 외부 MCP 서버 연동 및 ADK 내 복합 툴 에코시스템 지원.                        |
| **샌드박싱 & 권한**           | Filesystem/Network 제한 설정 및 CLI 툴 실행 시 동적 허용/차단.                                                     | `read-only`, `workspace-write`, `danger-full-access` 샌드박스 모드 및 untrusted command 차단.                      | 개발자가 설계한 도구 스펙(spec) 및 ADK 런타임 보안 정책 준수.                              |
| **Reasoning / Effort 제어**   | 에이전트 frontmatter의 provider-native model tier 제어(`opus 4.8` / `sonnet 4.6` / `haiku 4.5`).                   | `model_reasoning_effort` 명시 선언(`gpt-5.5`: none/low/medium/high/xhigh, `gpt-5.3-codex`: low/medium/high/xhigh). | `harness-catalog.md`에 기록된 provider-native high/medium tier 라벨.                       |

### 2. Claude, Codex, Gemini 공통 환경 및 규칙 체계 구축 방안

리포지토리는 세 프로바이더의 기계적 구조(Markdown, TOML, JSON) 차이에도 불구하고, 거버넌스와 일관성 확보를 위해 **"Canonical Core + Provider Adapter + Validation Evidence"** 모델을 수립하여 공통 체계를 구축하였다.

#### 1) 공통 환경 구축의 4대 요소

- **SSoT Governance Core**: 모든 거버넌스 규칙과 체크리스트는 `docs/00.agent-governance/rules/` 아래에 단일 마크다운 소스로 작성되어, 프로바이더에 의해 로드되거나 static validator에 의해 검증된다.
- **Shared local assets**: 에이전트 스킬, 워크플로우, 출력 스타일 양식 등은 프로바이더 중립적인 `.agents/{skills,workflows,output-styles}/`에 원본을 유지하고, Claude와 Codex는 이 경로를 symlink(혹은 provider-native view)로 바라보게 구성해 중복 작성을 원천 방지한다.
- **Shared Hook Script Engine**: 프로바이더 고유의 hook trigger 포맷(`.claude/settings.json`, `.codex/hooks.json`, `.agents/hooks.json`)이 발생했을 때, 실제 동작하는 쉘 검증 로직은 `docs/00.agent-governance/hooks/*.sh`로 위임하여 단일한 검증 결과를 내도록 통일했다.
- **Unified Validation Gate**: `validate-repo-quality-gates.sh`를 활용해 세 프로바이더의 어댑터 구조 정합성(Parity)을 상시 확인하며, 어느 어댑터를 통해 커밋되더라도 동일한 수준의 정적/보안 가드레일을 통과하도록 강제한다.

#### 2) 구현 현황 및 에이전트 형상 동기화 (Observability / Network)

최근 `observability-reviewer`와 `network-reviewer` 에이전트가 로스터에 추가되는 과정에서 공통 체계 구축 방안이 다음과 같이 증명되었다:

- **Harness Catalog**: `docs/00.agent-governance/harness-catalog.md`에 두 에이전트의 정의와 `worker` tier model mapping이 단일하게 수립되었다.
- **Parity Adapters**: `.claude/agents/observability-reviewer.md`, `.agents/agents/observability-reviewer.md` (Gemini), `.codex/agents/observability-reviewer.toml` (Codex)이 동시에 생성되어 mirror-parity를 충족했다.
- **Scope Alignment**: 세 파일은 각기 다른 런타임 문법을 지님에도 불구하고, `@import "docs/00.agent-governance/scopes/observability.md"`와 같이 단일한 영역 범위를 호출하도록 일관성 있게 정규화되었다.

### 3. Upstream Capability vs Local Adapter Status

- **Claude Code**: 업스트림은 매우 엄격한 native permission gating 및 동적 hook blocking을 지원한다. 로컬에서는 `.claude/settings.json`을 통해 파괴적인 git 명령어(push, reset 등)를 Deny-list로 설정하여 Native Layer에서 직접 차단하고, `validate-harness.sh`를 hooks에 바인딩해 검증 피드백을 제공한다.
- **Codex/OpenAI**: 업스트림은 샌드박싱 모드(`read-only`, `workspace-write` 등)를 통해 쓰기 경로 자체를 봉쇄하고 network-outbound를 통제한다. 로컬 어댑터에서는 `.codex/hooks.json`이 차단 게이트웨이라기보다는 정적 검증 및 컨텍스트 피드백 연결용으로 배포되어 있으며, CLI validation 명령어가 커밋 직전에 explicit하게 가동된다.
- **Gemini/Google CLI**: 업스트림은 컨텍스트 로더(`GEMINI.md`)와 간단한 도구 연동을 소유한다. 로컬 어댑터에서는 `.agents/agents/*.md` 양식을 통해 역할 및 postflight 체크리스트를 주입받아 거버넌스를 이행하며, `.agents/hooks.json`이 local validation pipeline을 연동해 동작 규칙을 준수하도록 유도한다.

## Sources

- Anthropic Claude Code settings and hooks reference (<https://code.claude.com/docs/>)
- OpenAI Codex configuration reference and sandboxing (<https://developers.openai.com/codex/>)
- Google Gemini CLI commands reference and Google ADK platform docs (<https://adk.dev/>)
- MCP Specifications and Security tutorials (<https://modelcontextprotocol.io/>)
- [Local Harness Catalog](../../../00.agent-governance/harness-catalog.md)
- [Harness Implementation Map](../../../00.agent-governance/harness-implementation-map.md)
- [Observability and Network Review Agents Task Record](../../../04.execution/tasks/2026-07-06-observability-and-network-review-agents.md)

## Review and Freshness

- Review cadence: 프로바이더 API/CLI 메이저 패치 혹은 리포지토리 어댑터 규칙 변경 시
- Last reviewed: 2026-07-09
- Next review trigger: 프로바이더 버전 갱신, 에이전트 신규 배치 시

## Related Documents

- **Parent research README**: [README.md](../README.md)
- **References README**: [../../README.md](../../README.md)
- **Workspace baseline**: [workspace-governance-baseline.md](workspace-governance-baseline.md)
- **Harness reference**: [harness-and-loop-engineering.md](harness-and-loop-engineering.md)
- **Model Policy**: [../../../00.agent-governance/model-policy.md](../../../00.agent-governance/model-policy.md)
- **Harness Catalog**: [../../../00.agent-governance/harness-catalog.md](../../../00.agent-governance/harness-catalog.md)
