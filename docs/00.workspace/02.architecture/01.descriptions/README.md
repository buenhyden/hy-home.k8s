---
title: "00.workspace/02.architecture/01.descriptions"
version: "0.1.0"
type: "common/readme"
status: "active"
owner: "platform"
updated: "2026-11-19"
---

# 00.workspace/02.architecture/01.descriptions

## Responsibility

### Purpose

> 작업 시스템 Architecture Description collection이다.

AD-0006은 문서·역할·QA Registry, 도구, CI, 제공자 어댑터의 경계와 흐름, 상태와 신뢰 경계를 설명한다.

#### Inputs and Outputs

##### In Scope

- 작업 시스템 AD

##### Out of Scope

- 제품 AD(AD-0004, AD-0005, AD-0007)

### Excluded Responsibilities

제품 AD는 `docs/02.architecture/01.descriptions/`가 소유한다.

## Current Contents

### Paths

| Path | Purpose |
| --- | --- |
| [`./0006-workspace-agent-governance-platform.md`](./0006-workspace-agent-governance-platform.md) | 작업 시스템(문서·에이전트·QA·전달) 구조와 신뢰 경계 |

### Owners

이 collection은 분류 표를 따로 두지 않는다.

## Usage

### Entry Points

1. 새 AD는 `docs/99.templates/02.templates/02.architecture/description.template.md`에서 시작한다.

#### Upstream and Downstream

- [Workspace architecture](../README.md)
- [Workspace decisions](../02.decisions/README.md)

#### Policy and Templates

- [Description form](../../../99.templates/02.templates/02.architecture/description.template.md)

### Checks

AD 번호는 제품 AD와 하나의 순서를 공유한다.
