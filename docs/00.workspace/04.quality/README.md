---
title: "00.workspace/04.quality"
version: "0.1.0"
type: "common/readme"
status: "active"
owner: "platform"
updated: "2026-11-19"
---

# 00.workspace/04.quality

## Responsibility

### Purpose

> 품질·형식·수용·검토와 보호 행위·승인 기준 collection이다.

#### Inputs and Outputs

##### In Scope

- 품질과 완료 기준, 검토 등급과 재검토 조건
- 형식·lint 기준
- 보호 행위와 승인 의미(W 범위 SAFE 규칙)
- CI/CD QA 안내(GDE-0010)

##### Out of Scope

- 에이전트의 실행 직전 확인·위임·권한 집행(`.agents/governance/approval-and-safety.md`)

### Excluded Responsibilities

검사 구현은 `scripts/`와 `.github/workflows/`, 에이전트 실행 차이는 `.agents/governance/`가 소유한다.

## Current Contents

### Paths

| Path | Purpose |
| --- | --- |
| [quality.md](./quality.md) | 품질·검증·완료·인계 기준 |
| [formatting-and-linting.md](./formatting-and-linting.md) | 형식·lint 기준 |
| [approval-and-safety.md](./approval-and-safety.md) | 보호 행위와 승인(SAFE W 규칙) |
| [`./0010-ci-cd-qa-reference-guide.md`](./0010-ci-cd-qa-reference-guide.md) | 로컬·호스팅 QA 경계와 증적 해석 안내 |

### Owners

SAFE-R011, R012, R017~R019는 `.agents/governance/approval-and-safety.md`가 소유한다.

## Usage

### Entry Points

1. 검사 의무는 quality 정책과 `scripts/validation/registry.json`이 소유하며 GDE-0010은 그 안내만 한다.

#### Upstream and Downstream

- [Workspace README](../README.md)
- [Process](../03.process/README.md)

#### Policy and Templates

- [Rule form](../../99.templates/02.templates/93.common/rule.template.md)

### Checks

정책 변경은 governance 문서 변경으로 선택되는 검사를 따른다.
