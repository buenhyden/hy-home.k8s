---
title: "Project Map"
version: "1.0.0"
type: "governance/knowledge"
status: "draft"
owner: "platform"
updated: "2026-11-20"
---

# Project Map

## 문서 개요

### 목적과 독자

이 지식 문서는 Project Map에서 현재 소유 경로를 찾는 작업자와 검토자의 탐색을 돕는다. 개요는 [Overview](#overview)에 기록한다.

### 책임과 적용 범위

platform은 이 지식 지도를 유지한다. 권한 경계는 [Authority Boundary](#authority-boundary), 실제 포인터는 [Pointer Index](#pointer-index)에 기록한다.

## 내용 계약

### 입력과 전제

입력과 전제는 아래 역할별 본문의 해당 절에 기록한다.

### 본문과 규칙

#### Overview

A reader who does not yet know this repository asks which top-level tree owns
what, and which file to open first inside it. This map answers that question and
nothing else.

#### Authority Boundary

Every row points; none decides. The owner named in a row keeps its own scope,
approval boundary and validation contract, and this document restates none of
them. A disagreement between a row and its owner is resolved by the owner.

#### Pointer Index

| Area | Owner path | Entry path | Stays valid while |
| --- | --- | --- | --- |
| Common governance | `.agents/` | `.agents/README.md` | Provider-neutral policy, roles, skills and lifecycle procedures stay here and native adapters stay outside |
| Claude adapter | `.claude/` | `.claude/README.md` | Claude remains a tracked provider surface |
| Codex adapter | `.codex/` | `.codex/README.md` | Codex remains a tracked provider surface |
| Documentation | `docs/` | `docs/README.md` | The stage contract keeps one canonical owner per document purpose |
| Desired state | `gitops/` | `gitops/README.md` | ArgoCD reconciliation stays the normal change path |
| Cluster bootstrap | `infrastructure/` | `infrastructure/README.md` | The local k3d platform is created from tracked assets |
| Policy rules | `policy/` | `policy/README.md` | Policy rules stay separate from the lanes that run them |
| Reference material | `examples/` | `examples/README.md` | Examples stay reference-only and are not deployed |
| Repository tooling | `scripts/` | `scripts/README.md` | Validation routing stays registry-owned |
| Tooling tests | `tests/` | `tests/README.md` | Each validator keeps an independent top-level test |
| Agent evaluation evidence | `.agents/evaluations/` | `.agents/evaluations/README.md` | Actual paired evaluation evidence stays here; the registered evaluator role owns the assessment |
| Local workspace notes | `_workspace/` | `_workspace/README.md` | Only the README files are tracked; working content stays outside shared policy |
| Local sensitive files | `secrets/` | `secrets/README.md` | No secret value is tracked in this repository |
| Hosted surface | `.github/` | `.github/repository-surface.md` | Hosted execution stays separate from repository-static evidence |

#### Validation and Refresh

Every owner and entry path above must exist in the tree; a missing path fails
the knowledge validator. Refresh a row when its tree gains or loses ownership,
not on a schedule. Adding or removing a top-level tree invalidates this map.

#### Related Documents

- [Common Knowledge](README.md)
- [Domain Index](domains.md)
- [Common Agent Governance](../README.md)

## 적용과 확인

### 적용 방법

아래 역할별 본문에 기록된 사용 조건과 절차를 적용한다.

### 확인 기준

아래 역할별 본문의 검증·확인 조건과 그 한계에 따른다.

## 관계와 출처

### 관련 문서

관련 문서와 정본 링크는 아래 역할별 본문에서 확인한다.

### 외부 근거

외부 근거가 사용된 경우 아래 역할별 본문의 출처와 적용 범위에서 확인한다.
