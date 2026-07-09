---
title: 'Reference: AI Agents Roster and Gap Analysis Research'
type: content/reference
status: draft
owner: platform
updated: 2026-07-07
---

# Reference: AI Agents Roster and Gap Analysis Research

## Overview

이 문서는 `hy-home.k8s` 워크스페이스에 구현된 AI 에이전트 로스터(Roster)를 리포지토리 실제 코드 증적(Repo-backed evidence) 기준으로 정리한다. 또한 외부 오픈소스 에이전트 페르소나 모음집인 `msitarzewski/agency-agents`를 분석하여 두 체계의 구조적 차이점을 비교하고, 에이전트 보완/추가 관점의 gap analysis 결과를 기술한다.

특히, 2026-07-04 일자 분석에서 신규 에이전트 도입 후보(Adopt candidate)로 제안되었던 Observability(SRE) 및 Network 에이전트가 2026-07-06에 실제로 구현(`observability-reviewer` 및 `network-reviewer` 추가)되어 Gap이 성공적으로 폐쇄(Closed)된 과정을 기록으로 보존한다.

본 문서는 설명용 참고 문서이며, 실제 리포지토리의 에이전트 런타임 구성이나 모델 매핑 정책을 재설정하지 않는다.

## Purpose

- 워크스페이스 내 에이전트 로스터 및 프로바이더별 어댑터 구성의 최신 상태를 기록.
- 외부 에이전트 페르소나 규격인 `agency-agents`와의 호환성 및 한계를 규명하여 무분별한 외부 파일 도입 차단.
- 이전 리서치 결과의 제안 사항이 실제 개발 스펙(SDD)으로 연계되어 Gap을 해소하는 환류(Feedback) 과정을 증명.

## Reference Type

- Type: dated-implementation-audit / external-standard-snapshot
- Source checked: 2026-07-07
- Refresh trigger: `harness-catalog.md` 내 에이전트 로스터 변경, `model-policy.md` 내 모델 계층 정책 수정, 프로바이더별 에이전트 매핑 수정.

## Authority Boundary

- **Authoritative for**:
  - 2026-07-07 기준 리포지토리 내 에이전트 로스터 및 프로바이더 어댑터 목록 요약.
  - 외부 `agency-agents` 규격 분석 자료 및 로컬 규격과의 비교표.
- **Not authoritative for**:
  - 에이전트 실행 및 런타임 로스터 정의 (`harness-catalog.md`가 단독 지배).
  - 에이전트가 사용하는 실제 모델 지정 (`model-policy.md`가 단독 지배).

## Scope

- 로컬 에이전트 10종의 역할 및 모델 계층 정보, `agency-agents` 페르소나 수, 배포 구조, 파일 규격 분석, 로컬-외부 포맷 비교, gap analysis 결과 및 Gap 폐쇄 증적.
- 에이전트 런타임 툴체인 변경 및 실 클러스터 조작 제외.

## Definitions / Facts

### 1. 워크스페이스 AI 에이전트 로스터 (Repo-backed Roster)

2026-07-07 기준 워크스페이스가 공식 수용하는 로컬 에이전트는 총 10종이며, 3대 프로바이더 어댑터(`.claude/agents/*.md`, `.agents/agents/*.md`, `.codex/agents/*.toml`)에 동기화되어 매핑되어 있다.

| 에이전트 명                  | 역할 및 책임 범위                                                                    | 모델 계층                  |
| ---------------------------- | ------------------------------------------------------------------------------------ | -------------------------- |
| **`supervisor`**             | 전체 계획(Plan) 수립, 서브에이전트 호출 제어, 완료 조건 검증                         | `top` (Pro/Opus 급)        |
| **`k8s-implementer`**        | 쿠버네티스 선언형 매니페스트(YAML) 및 Kustomize 구성 작성                            | `worker` (Flash/Sonnet 급) |
| **`gitops-reviewer`**        | GitOps 매니페스트 아키텍처, ArgoCD 동기화/보안 적합성 검사                           | `worker` (Flash/Sonnet 급) |
| **`code-reviewer`**          | YAML syntax, Helm values, 쉘 스크립트 작성 품질 검사                                 | `worker` (Flash/Sonnet 급) |
| **`security-auditor`**       | 쿠버네티스 RBAC, NetworkPolicy gap, secrets 노출 여부 정적 감사                      | `worker` (Flash/Sonnet 급) |
| **`incident-responder`**     | 장애 포스트모템 작성 지원, 타임라인 복구, 근본 원인 분석(RCA) 지원                   | `worker` (Flash/Sonnet 급) |
| **`doc-writer`**             | SDD 템플릿 적합성, 문서 taxonomy 위상, 언어 경계 준수 가이드                         | `worker` (Flash/Sonnet 급) |
| **`wiki-curator`**           | LLM Wiki 인덱스 및 canonical owner 링크 최신성 자동 갱신 및 유지                     | `worker` (Flash/Sonnet 급) |
| **`observability-reviewer`** | 모니터링 매니페스트(Prometheus/Grafana/Alloy), SLO 사양 검사 (2026-07-06 추가)       | `worker` (Flash/Sonnet 급) |
| **`network-reviewer`**       | Traefik, Ingress, NetworkPolicy 포트 및 Ingress TLS 설정 정적 검사 (2026-07-06 추가) | `worker` (Flash/Sonnet 급) |

- **모델 계층 정책 (Model Policy)**: `top` 계층(Gemini 3.1 Pro 등)은 기획/감독 역할을 수행하는 `supervisor`만 사용하며, 나머지 9개 실행/검사 전문 에이전트는 `worker` 계층(Gemini 3.5 Flash 등)을 사용하는 2계층 분할을 원칙으로 삼는다.

### 2. 외부 에이전트 분석: `msitarzewski/agency-agents` (External Catalog Scan)

- **개요**: 147개 이상의 마크다운 정의 특화 AI 에이전트 페르소나를 17개 전문 분야(engineering, design, product 등)로 나누어 제공하는 오픈소스 라이브러리.
- **특징**: 특정 프롬프트 프레임워크에 종속되지 않고, Claude Code, Cursor, Aider, Copilot, Gemini CLI 등 다양한 도구로 내보내기(conversion)할 수 있는 쉘 툴과 설정 포맷(`divisions.json`, `tools.json`)을 내포한다.
- **포맷 차이**:
  - **`agency-agents`**: 에이전트의 페르소나, Critical Rules, vibe 및 전달 방식 중심의 묘사 중심 텍스트. 모델 사양이나 사용 툴(Tools) 리스트가 선언되지 않음.
  - **로컬 어댑터**: 하네스 제어를 위한 구체적 `model` 할당, 최소 권한의 `tools` 목록 지정, JIT 거버넌스를 로딩하는 `@import` scope 규정, postflight 체크리스트 결합.

### 3. 계약 규격 비교 (Local Roster vs Agency-Agents)

| 항목                | hy-home.k8s 로컬 로스터                    | msitarzewski/agency-agents       |
| ------------------- | ------------------------------------------ | -------------------------------- |
| **에이전트 수**     | 10종 고정 (역할 기반 격리)                 | 147종 이상 (페르소나 기반 확장)  |
| **최소 권한 제제**  | 어댑터 별 명시적 `tools:` 바인딩           | 없음 (임의 툴 실행 가능성 존재)  |
| **거버넌스 통합**   | `@import` 지시어로 Stage 00 정책 상속      | 없음 (개별 독립형 페르소나 선언) |
| **다중 프로바이더** | md(Claude/Gemini), toml(Codex) 삼각 동기화 | CLI 변환 스크립트 기반 생성      |
| **모델 계층 분배**  | 2계층(top/worker) 정책 강제                | 없음                             |

따라서 외부 `agency-agents` 파일을 수정이나 보완 없이 워크스페이스에 직접 복사하여 로드하는 것은 거버넌스 및 보안 위반이다. 외부의 우수한 페르소나를 수용할 때는 로컬 어댑터 구조에 맞추어 `tools`, `model`, `guardrails`, `postflight` 설정을 추가로 주입하는 변환 가공 단계가 필수적이다.

### 4. Gap Analysis 및 Gap 폐쇄 결과 (Gap-Closure Analysis)

#### 1) 2026-07-04 리서치 제안 사항의 환류 (Gap-Closure)

이전 분석에서 다음의 2개 에이전트 도입 필요성이 강력히 대두되었다.

- **SRE/Observability 에이전트**: 플랫폼의 Prometheus, Grafana, Alloy 매니페스트를 검증하고 SLO 문서를 관리할 전담 에이전트 필요성 지적.
- **Network Engineer 에이전트**: Traefik ingress-route 설정, NetworkPolicy egress 사양, Ingress TLS 포트 검증을 담당할 에이전트 필요성 지적.

이 제안은 **`docs/03.specs/024-observability-and-network-review-agents/`** 스펙을 통해 실제 개발 작업으로 상정되었으며, **2026-07-06**에 `observability-reviewer` 및 `network-reviewer` 2종 에이전트 어댑터 세트가 3대 프로바이더 전체 경로에 반영되면서 **Gap이 완벽히 해결(Closed)되었음**을 확인하였다.

#### 2) 향후 보완/수정 및 신규 추가 후보 (Future Candidates)

- **`incident-responder` 보완 (Adapt)**: `agency-agents` SRE 페르소나에 묘사된 SLO Burn-rate 용어 및 심각도 분류를 사고 기록 템플릿 검증에 점진 반영하되, 정적 수준을 넘어선 실시간 모니터링 조작 기능은 제외한다.
- **`code-reviewer` 보완 (Adapt)**: 외부 페르소나의 '성공 메트릭(success metrics)' 사상을 코드 리뷰 산출물로 환류하여, 리뷰 검출 건수 대비 증적 인용 횟수(citation count)를 의무 기입하도록 어댑터 guardrail을 보강한다.
- **`security-auditor` 보완 (Adapt)**: 외부의 'compliance-auditor' 사상을 차용해 pre-commit 설정의 CIS Kubernetes Benchmark 정적 린트 위반 체크 항목 검사를 code audit 단계에 추가 규정한다.

#### 3) 신규 에이전트 추가 후보 (Addition Candidates)

`agency-agents` 17개 전문 분야를 WSL2+k3d ArgoCD GitOps 플랫폼 목적에 맞추어 평가한 신규 추가 후보 판정이다. `Closed`는 이미 구현 완료, `Adapt`는 기존 에이전트로 흡수, `Skip`은 워크스페이스 범위 밖을 의미한다. 외부 패턴 자체는 비권장 시장 분석(non-authoritative)이며, 라우팅 경로만 repo-backed 사실이다.

| 외부 패턴                                               | 판정       | 근거 및 라우팅                                                                                                                                            |
| ------------------------------------------------------- | ---------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `engineering-sre` (SLO/observability)                   | **Closed** | 2026-07-06 `observability-reviewer`로 구현 완료. `gitops/platform/monitoring/` 및 Prometheus/Grafana/Alloy 매니페스트 검증 소유.                          |
| `engineering-network-engineer`                          | **Closed** | 2026-07-06 `network-reviewer`로 구현 완료. Traefik/Ingress TLS/NetworkPolicy 정적 감사 소유.                                                              |
| `engineering-devops-automator`                          | Adapt      | CI/파이프라인 유지보수는 `supervisor` + `k8s-implementer` + validators로 이미 분산됨. 신규 에이전트 불필요; 파이프라인 유지 프롬프트는 기존 scope로 흡수. |
| `security-compliance-auditor`                           | Adapt      | compliance 체크리스트 관점은 `security-auditor` guardrail 확장으로 수용. 현 로스터 규모에서 2번째 보안 에이전트는 부적절.                                 |
| `testing-api-tester`, `testing-performance-benchmarker` | Skip       | 이 플랫폼 repo에는 애플리케이션 API 표면이 없음. 테스트는 repo-static/shell 기반.                                                                         |
| `engineering-technical-writer`                          | Skip       | `doc-writer` + Stage 99 템플릿 계약이 더 강한 라우팅으로 이미 커버.                                                                                       |
| `engineering-codebase-onboarding-engineer`              | Skip       | `wiki-curator` + graphify 출력이 온보딩 표면 소유.                                                                                                        |
| `agents-orchestrator`, `studio-producer`                | Skip       | supervisor tier + `harness-catalog.md`가 오케스트레이션 소유. catalog-agent 오케스트레이션은 거버넌스를 중복시킴.                                         |

2026-07-07 기준 워크스페이스 범위에서 즉시 추가가 정당화되는 신규 에이전트는 남아 있지 않다(observability/network 폐쇄로 열린 Adopt 후보 소진). 향후 신규 에이전트를 추가할 때는 다음 라우팅을 준수한다.

- 로스터/tier 변경은 `model-policy.md`와 `harness-catalog.md`를 먼저 갱신한 뒤 어댑터를 만든다.
- 신규 에이전트는 `docs/03.specs/`에 agent-design 스펙과 Stage 04 task를 먼저 작성한 후 어댑터 파일(`.claude/agents/*.md`, `.agents/agents/*.md`, `.codex/agents/*.toml`)을 동시 정렬한다.
- 외부 페르소나 도입 시 persona-memory 블록을 제거하고 tier `model`, 최소 권한 `tools:`, scope `@import`, guardrails, postflight를 주입한다.
- 도입/거절 결정은 `docs/00.agent-governance/memory/progress.md`에 기록한다.

## Sources

- msitarzewski/agency-agents repository (<https://github.com/msitarzewski/agency-agents>)
- agency-agents divisions list: specialized, engineering, security (<https://raw.githubusercontent.com/msitarzewski/agency-agents/main/divisions.json>)
- [Local Harness Catalog](../../../00.agent-governance/harness-catalog.md)
- [Model Policy](../../../00.agent-governance/model-policy.md)
- [Observability and Network Review Agents Task Record](../../../04.execution/tasks/2026-07-06-observability-and-network-review-agents.md)

## Review and Freshness

- Review cadence: on agent roster or external standard change
- Last reviewed: 2026-07-07
- Next review trigger: 에이전트 역할 개편, `agency-agents` 메이저 리팩토링 발생 시

## Related Documents

- **Parent research README**: [README.md](../README.md)
- **References README**: [../../README.md](../../README.md)
- **Workspace baseline**: [workspace-governance-baseline.md](workspace-governance-baseline.md)
- **Harness Catalog**: [../../../00.agent-governance/harness-catalog.md](../../../00.agent-governance/harness-catalog.md)
- **Subagent Protocol**: [../../../00.agent-governance/subagent-protocol.md](../../../00.agent-governance/subagent-protocol.md)
