---
title: "00.workspace/06.maintenance"
version: "0.1.0"
type: "common/readme"
status: "active"
owner: "platform"
updated: "2026-11-19"
---

# 00.workspace/06.maintenance

## Responsibility

### Purpose

> 작업 시스템의 반복 유지보수·진단·복구 절차 collection이다.

#### Inputs and Outputs

##### In Scope

- 참고 자료(Stage 90) 유지보수 Runbook

##### Out of Scope

- 제품 운영 Runbook(`docs/05.operations/03.runbooks/`)

### Excluded Responsibilities

제품 운영 절차는 Stage 05가 소유한다.

## Current Contents

### Paths

| Path | Purpose |
| --- | --- |
| [`./0011-reference-maintenance-runbook.md`](./0011-reference-maintenance-runbook.md) | Stage 90 Audit/Data/Research pack 유지보수 |

### Owners

이 collection은 분류 표를 따로 두지 않는다.

## Usage

### Entry Points

1. 새 Runbook은 `docs/99.templates/02.templates/05.operations/runbook.template.md`에서 시작한다.

#### Upstream and Downstream

- [Workspace README](../README.md)
- [References README](../../90.references/README.md)

#### Policy and Templates

- [Runbook form](../../99.templates/02.templates/05.operations/runbook.template.md)

### Checks

RUN 번호는 제품 Runbook과 하나의 순서를 공유한다.
