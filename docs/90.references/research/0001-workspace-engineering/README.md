---
title: "Workspace Engineering Research Pack"
version: "0.3.0"
type: "reference/research-pack"
status: "in-review"
owner: "platform"
updated: "2026-10-05"
artifact_id: "RES-0001"
---
# Workspace Engineering Research Pack

## Overview

이 단일 pack은 workspace engineering의 외부 공식 문서·표준·원저자 자료와
upstream 구현을 비교하고, 후속 workspace 조사에 필요한 질문과 증거 계약을
정리한다. 독자는 개발자, 운영자, 문서 작성자와 AI agent다. 현재 외부 지식을
먼저 읽고 과거 로컬 관찰은 관찰 당시의 증거로 구분하여 읽는다.

## Scope

이 pack은 아래 연구 계약과 보고서 색인에 명시한 주제와 출처를 포함한다.
실행 승인, 현재 정책, hosted·provider·live 결과는 증거 범위에서 제외한다.

## Research Contract

제품 동작은 해당 provider·제품 surface의 공식 문서와 구현, 표준·방법론은
표준기관과 원저자 자료로 확인한다. 구현 사례는 가능한 경우 revision과 license를
기록한다. 검색 요약이나 URL 응답 성공만으로 기술 주장을 검증하지 않는다.
게시일·수정일·실제 확인일과 제품·버전·채널·selector는 보고서와 출처 원장이
소유한다. 유료 표준의 초록과 접근 실패는 확인 범위의 한계로 남긴다.

### External Finding Vocabulary

| 값 | 이 연구에서의 범위 |
| --- | --- |
| `Verified` | 명시한 제품·버전·관찰 범위의 주장을 직접 읽은 출처가 뒷받침한다. |
| `Partial` | 주장 중 일부만 뒷받침되며 미확인 범위와 필요한 다음 증거를 명시한다. |
| `Unverified` | 확인 가능한 근거가 부족하여 주장을 확정하지 않는다. |
| `DEFER` | 필요한 접근·권한·환경·증거가 없어 판정을 보류하고 재개 조건을 남긴다. |
| `Contradicted` | 확인한 근거가 기존 주장과 충돌하며 정정·철회 범위를 명시한다. |

이 값은 외부 주장의 판정이다. 과거 로컬 `Verified`나 문서 QA 결과를 새 외부
확인일만으로 갱신하지 않는다. 미완료 외부 조사를 `DEFER`로 표시한 것만으로
전체 연구가 완료되는 것은 아니다.

### Separate Evidence Axes

| 축 | 기록 방법 |
| --- | --- |
| 외부 주장 판정 | 위 다섯 값과 그 주장의 출처·범위·한계를 기록한다. |
| 출처 갱신 결과 | `new`는 새로 수용한 근거, `changed`는 비교 범위의 변화, `unchanged`는 실제 관련 본문 비교에서 변화가 없었던 결과, `unreachable`은 필요한 본문에 접근하지 못한 결과다. |
| 이번 workspace 관찰 | 항상 `not observed in this cycle`이다. 후보 경로는 후속 조사 selector이며 현재 실태 판정이 아니다. |
| 문서 QA | 실제 실행한 검사와 snapshot의 `PASS / FAIL / SKIP / DEFER`를 실행 Task에 기록한다. 연구 사실 판정과 별개다. |

상충하는 외부 자료는 제품·버전·채널·관찰일로 나누며 해결되지 않은 차이를
남긴다. 문서에 없다는 이유만으로 미지원이라고 단정하지 않는다. 조건부 적용
제안은 외부 사실 및 과거 로컬 관찰과 구분한다.

## Structure

직접 멤버와 그 연구 책임은 아래 보고서 색인에서 찾는다. 각 멤버의 날짜와
판정은 멤버 본문이 소유하며 이 anchor는 별도 실행 상태를 기록하지 않는다.

## Report Index

| 보고서 | 연구 책임 |
| --- | --- |
| [Workspace governance](m0001-workspace-governance-and-common-agent-environment.md) | instruction 계층, 공통 정본·provider adapter, context 공유와 handoff |
| [Harness and loop](m0002-harness-and-loop-engineering.md) | harness 구성, loop 전이·종료·예산·재시도·복구 |
| [Provider surfaces](m0003-provider-implementation-status.md) | Claude·Codex 제품별 공식 기능, discovery·권한·hook·IDE·SDK 비교 |
| [SDLC and document contracts](m0004-spec-driven-sdlc-and-document-contracts.md) | spec-driven 원칙, 문서 family·lifecycle·추적성, 프로젝트·이슈 관리 |
| [Documentation architecture](m0005-documentation-architecture-and-diataxis.md) | Diátaxis·C4·ADR·arc42·README의 목적과 독자별 선택 |
| [LLM-WIKI and knowledge routing](m0006-llm-wiki-and-knowledge-routing.md) | 원저자 제안, 지식 탐색·retrieval 선택지와 freshness·보안 |
| [Infrastructure and security](m0007-kubernetes-infrastructure-and-security.md) | Kubernetes·GitOps·인프라·공급망·보안·복구의 외부 계약 |
| [CI/CD and QA](m0008-ci-cd-github-actions-and-qa.md) | delivery, GitHub Actions, Git hooks, QA와 Verification/Validation |
| [AI agents and agency-agents](m0009-ai-agents-and-agency-agents.md) | 역할·persona·skill·권한·위임 경계, upstream 구조·license·선택 전략 |
| [Model routing](m0010-agent-model-routing-and-configuration.md) | 제품별 모델·설정·비용·한도·fallback·평가 |
| [Memory management](m0011-agent-memory-tiers-and-management.md) | 단기·장기·도메인 기억, 수명·승격·정정·삭제·복구 |
| [Source coverage](m0012-source-coverage.md) | 원 요청·requirement·claim·source 대응, 갱신·이관 처분과 역사적 증거 |
| [Scope application index](m0013-scope-application-index.md) | 외부 근거를 scope별 후속 조사 질문·selector·합격 기준·승인 경계에 연결 |

## Usage

먼저 연구 계약과 증거 경계를 확인한 뒤 보고서 색인에서 필요한 멤버를 읽는다.
갱신은 아래 승계 절차를 따르며 연구 근거를 현재 실행 승인으로 사용하지 않는다.

## Refresh and Succession

주제 보고서의 담당자가 해당 출처의 release·version·설정 schema·표준 revision·
URL 이동·내용 충돌·재검토 trigger를 확인하여 본문을 갱신한다. 현재 지식을 앞에
종합하고 날짜별 addendum을 반복하여 쌓지 않는다. 과거 관찰 날짜, 판단 범위,
정정·대체 관계와 Git 기반 복구 provenance를 보존한다.

기존 pack·member identity와 source·claim·requirement ID를 유지한다. 주제 이동은
원 경로·anchor·ID, 이유, 후속 위치와 활성 소비자 cutover를 출처 원장에 기록한
뒤 처리한다. 출처·주장·coverage 식별자 배정은 통합 담당자 한 명이 맡는다.
새 발견은 기존 주장을 보완하는지 대체하는지 명시하며, 원 요청의 반복 항목도
대응을 보존한다. 후속 scope 조사 설계는 실태 조사 실행과 별도로 인계한다.

## Evidence Boundary

이번 작업은 외부 연구와 후속 조사 설계다. workspace 기능·설정·운영 실태,
provider discovery·model resolution·hook 실행, hosted CI와 live cluster 효과를
관찰하지 않는다. 과거 로컬 경로와 판정은 역사적 증거이며 현재 load 지시가
아니다. credential·secret 값·개인 기억·대화 로그를 수집하지 않는다.

문서 검증은 변경 문서의 repository-static QA만 입증한다. 연구 발견과 조건부
제안은 활성 정책, 구현 계약, 실행 승인이나 도구 도입 결정으로 승격되지 않는다.
현재 로컬 권한은 공통 거버넌스와 각 stage의 정본 owner가 소유한다.

## Related Documents

- [Research collection](../README.md)
- [Agent Governance Hub](../../../../.agents/README.md)
- [Requirements](../../../01.requirements/README.md)
- [Architecture](../../../02.architecture/README.md)
- [Specs](../../../03.specs/README.md)
- [Operations](../../../05.operations/README.md)
- [Research template and profile owner](../../../99.templates/README.md)
