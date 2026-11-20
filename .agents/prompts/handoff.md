---
title: "Handoff Prompt Contract"
version: "1.0.0"
type: "governance/prompt"
status: "draft"
owner: "platform"
updated: "2026-11-20"
---

# Handoff Prompt Contract

## 문서 개요

### 목적과 독자

이 prompt 계약은 Handoff Prompt Contract 요청을 구성하는 작성자와 그 결과를 검토하는 역할에게 입력·출력 경계를 제공한다. 요청 목적은 [Overview](#overview)에 기록한다.

### 책임과 적용 범위

platform은 이 prompt 계약을 유지한다. 허용 권한은 [Authority Boundary](#authority-boundary), 필수 입력은 [Inputs](#inputs)에 기록하며 실행 권한을 추가하지 않는다.

## 내용 계약

### 입력과 전제

입력과 전제는 아래 역할별 본문의 해당 절에 기록한다.

### 본문과 규칙

#### Overview

Identifier `handoff`. Assemble the request that produces a work handoff for the
owning Task, so the next owner receives the same fields every time rather than
whatever the session happened to remember.

#### Authority Boundary

The handoff fields belong to the
[quality policy](../../docs/00.workspace/04.quality/quality.md#handoff-evidence-contract); this
contract reuses them and redefines none. A handoff records authority; it never
grants it, and a recorded boundary is not a standing authorization.

#### Inputs

| Input | Command | Why it is needed |
| --- | --- | --- |
| Branch | `git rev-parse --abbrev-ref HEAD` | Part of the snapshot the evidence describes |
| Head commit | `git rev-parse HEAD` | Part of the snapshot the evidence describes |
| Changed path set | `git status --porcelain` | The scope the handoff covers |
| Committed scope | `git log --oneline -20` | The most recent logical units, bounded rather than diffed against a base |

The subject input is `Branch`. When it is empty the contract refuses, because
a handoff without a snapshot describes no state.

#### Output

The handoff fields the quality policy lists, in its order, each either filled or
explicitly marked `none` or `DEFER` with a reason. No field is omitted.

The operator supplies facts not available to these read-only commands, such as
the resume checks the [resume decision](../governance/context-and-memory.md#resume-decision)
lists; the assembler must not invent them or authenticate approval. Failed, timed-out, over-limit or invalid-encoding
input produces no draft; no partial stdout or raw stderr is retained.

The committed scope is bounded rather than diffed against a base branch. A base
ref is a property of the checkout, not of the contract: a clone that carries
only the working branch has no `main`, and a contract that assumes one fails
there instead of producing a handoff.

#### Validation

A produced handoff is reviewed against the quality policy's field list before it
is written into the owning Task. A field that silently disappeared fails review.

#### Refusal Conditions

The builder enforces only the empty-subject refusal; the requesting agent
enforces the remaining conditions below.

- No acceptance identifier or owning Task is supplied, so the handoff would have
  no destination.
- The request asks for a lane result that was not observed, which would report
  an unobserved result as evidence.
- The request asks to include credentials, environment dumps or raw provider
  transcripts.

#### Related Documents

- [Common Prompt Contracts](README.md)
- [Quality and Evidence Policy](../../docs/00.workspace/04.quality/quality.md)
- [Work Lifecycle](../workflows/work-lifecycle.md)

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
