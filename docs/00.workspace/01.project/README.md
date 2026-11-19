---
title: "00.workspace/01.project"
version: "0.1.0"
type: "common/readme"
status: "active"
owner: "platform"
updated: "2026-11-19"
---

# 00.workspace/01.project

## Responsibility

### Purpose

> 작업 시스템의 범위, 소유, 공통 어휘의 진입점이다.

이 폴더는 사람과 에이전트가 같은 뜻으로 쓰는 용어(TERM ID)의 정본을 둔다. 작업 시스템의 범위와 책임 계층(W·P·R·C·A·I·T)은 SDLC 정책 SDLC-R036이, 장기 요구는 REQ-0003이 소유하며 여기서는 그 정본으로 연결한다.

#### Inputs and Outputs

##### In Scope

- 공통 어휘와 각 용어의 정책 owner
- 범위·소유 정의로 가는 경로

##### Out of Scope

- 규칙 본문(각 정책이 소유)
- 제품 요구(Stage 01 제품 요구 문서)

### Excluded Responsibilities

이 폴더는 규칙을 서술하지 않는다. 규칙은 `../03.process/`와 `../04.quality/` 정책이, 에이전트 실행 차이는 `.agents/governance/`가 소유한다.

## Current Contents

### Paths

| Path | Purpose |
| --- | --- |
| [glossary.md](./glossary.md) | 공통 거버넌스 용어의 의미, TERM ID, 정책 owner와 계약 판본 |

### Owners

| 찾는 것 | 정본 |
| --- | --- |
| 책임 계층과 범위 | `../03.process/sdlc.md`의 SDLC-R036 |
| 작업 시스템의 장기 요구 | [REQ-0003](../../01.requirements/0003-workspace-agent-governance-platform.md) |
| 용어의 뜻 | [glossary.md](./glossary.md) |

## Usage

### Entry Points

1. 용어를 추가·변경할 때는 TERM ID를 재발급하지 않고 계약 판본을 갱신한다.
2. 양식은 `docs/99.templates/02.templates/00.workspace/vocabulary.template.md`를 따른다.

#### Upstream and Downstream

- [Workspace README](../README.md)
- [Requirements README](../../01.requirements/README.md)

#### Policy and Templates

- [Vocabulary form](../../99.templates/02.templates/00.workspace/vocabulary.template.md)

### Checks

knowledge 검사(`scripts/validate-knowledge-surface.py`)가 glossary의 TERM 중복, owner 누락, 정책 본문 복제를 검사한다.
