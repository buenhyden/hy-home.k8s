---
title: "00.workspace/03.process"
version: "0.1.0"
type: "common/readme"
status: "active"
owner: "platform"
updated: "2026-11-19"
---

# 00.workspace/03.process

## Responsibility

### Purpose

> 개발·문서·전달의 의미와 순서를 소유하는 공통 절차 collection이다.

#### Inputs and Outputs

##### In Scope

- SDLC, 문서 작성, 문서 수명주기, Git 공통 기준
- 저장소 전달 절차(main 릴리스 준비)

##### Out of Scope

- 에이전트 전달 명령(`.agents/governance/git.md`)
- 제품 운영 Runbook

### Excluded Responsibilities

에이전트의 실행 차이와 제품 운영 절차는 이 collection이 소유하지 않는다.

## Current Contents

### Paths

| Path | Purpose |
| --- | --- |
| [sdlc.md](./sdlc.md) | SDLC 단계, 변경 종류, 책임 계층(SDLC-R036) |
| [document-authoring.md](./document-authoring.md) | 문서 작성과 stage 라우팅 |
| [document-lifecycle.md](./document-lifecycle.md) | 문서 상태, 처분, 이동(DOCLIFE-R023) |
| [git.md](./git.md) | 커밋·브랜치·릴리스·Git 시점 공통 기준 |
| [`./0012-main-release-preparation-runbook.md`](./0012-main-release-preparation-runbook.md) | main CHANGELOG 준비와 SemVer Release 게시 절차 |

### Owners

규칙 ID는 문서마다 한 owner를 가진다. GIT-R011~R013은 `.agents/governance/git.md`가 소유한다.

## Usage

### Entry Points

1. 규칙 변경은 해당 정책의 규칙 ID를 유지하고 Registry `policy_rule_ids` 기록과 함께 바꾼다.

#### Upstream and Downstream

- [Workspace README](../README.md)
- [Quality](../04.quality/README.md)

#### Policy and Templates

- [Rule form](../../99.templates/02.templates/93.common/rule.template.md)

### Checks

정책 변경은 governance 문서 변경으로 선택되는 검사를 따른다.
