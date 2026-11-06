---
title: "SDLC Governance Audit"
version: "0.2.0"
type: "reference/audit-pack"
status: "published"
owner: "platform"
updated: "2026-11-06"
artifact_id: "AUD-0001"
---

# SDLC Governance Audit

## Overview

이 pack은 Requirement, Architecture, Spec, Plan, Task를 잇는 개발 거버넌스가
실제로 어떻게 적용되는지 2026-11-06에 감사한 기록이다. 독자는 거버넌스를 고치는
운영자와 문서 작성자이며, 대상은 `.agents/governance/`, `docs/99.templates/`,
`docs/01.requirements/`부터 `docs/03.specs/`까지, 그리고 provider gateway다.

## Scope

포함 범위는 문서 역할, 문서 사이의 추적성, 단계 전이 조건, Architecture 통제,
충돌 처리 규칙, 에이전트 지침이 실제로 로드되는 경로다. 제품 manifest, live
cluster, hosted CI 실행, provider runtime의 동작은 제외한다. 관찰은 `main`
`3ec90be8` 시점의 저장소 정적 상태로 한정한다.

## Audit Contract

관측 날짜는 2026-11-06이고 기준선은 `main` `3ec90be8`이다. 방법은 정책 원문과
Stage 99 registry의 profile 계약을 읽고, 해당 validator와 문서 단위 테스트를
실행하는 것이다. 이 pack은 정책을 정의하지 않는다. 확인하지 못한 증거는 보고서의
Verification State에 UNKNOWN으로 남긴다.

## Structure

직접 멤버는 아래 Report Index 하나로 찾는다.

## Report Index

- [m0001 SDLC governance audit](./m0001-sdlc-governance-audit.md): 인벤토리,
  발견 사항, 개선 기록, 검증 상태를 맡는다.
- [m0002 AGENTS.md loading addendum](./m0002-agents-md-loading-addendum.md): 2026-11-06
  provider의 `AGENTS.md` 로드 방식, guard 출력(F-08~F-10)을 맡는다.

## Usage

먼저 Audit Contract와 Evidence Boundary를 읽고, 보고서에서 발견 사항과 그 처분을
확인한다. 현재 규칙은 보고서가 아니라
[SDLC 정책](../../../../.agents/governance/sdlc.md)에서 읽는다.

## Review and Closure

검토 owner는 platform이다. SDLC 정책이나 Stage 99의 SDLC profile이 바뀌면 다시
감사한다. 보고서의 결정 대기 항목이 처리되면 pack을 `retired`로 옮긴다.

## Evidence Boundary

여기 기록한 결과는 저장소 정적 검사 결과뿐이다. hosted CI, provider runtime,
자격 증명, live cluster 증거는 포함하지 않으며 이 결과로 대신하지 않는다.

## Related Documents

- [Audits collection](../README.md)
- [SDLC 정책](../../../../.agents/governance/sdlc.md)
- SPEC-0146 (completed; summarized in the [REQ-0003 Archived Lineage](../../../01.requirements/0003-workspace-agent-governance-platform.md#archived-lineage))
