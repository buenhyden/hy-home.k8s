---
title: "agents Template Definition"
version: "0.1.0"
type: "common/template-agents-guide"
status: "draft"
owner: "platform"
updated: "2026-11-20"
---

# agents Template Definition

## 문서 개요

### 목적과 독자

<!-- 작성 규칙: Give authors one form for the agent instructions of a directory that state its scope and instruction precedence, intake and execution, authority and external-effect boundaries, and checks and reporting. -->

### 책임과 적용 범위

<!-- 작성 규칙: An AGENTS.md owns the agent instructions of its directory and the root gateway for Codex; policy, role and skill authority stay with their owners and are linked, not copied. -->

## 내용 계약

### 입력과 전제

<!-- 작성 규칙: 이 문서를 작성할 때 필요한 실제 입력, 권한과 전제를 밝힌다. -->

### 본문과 규칙

<!-- 작성 규칙: 아래 역할별 절의 내용과 표를 해당 문서의 실제 사실로 채운다. -->

~~~~~~~native-payload
# {{AGENTS_SCOPE_NAME}}

## Scope

### Allowed Scope

<!-- Author prompt: name the directory, the writes and the roles these instructions cover, separate facts from assumptions, and link the role and projection owners. -->

#### Non-goals

<!-- Author prompt: state the work outside this directory and the parent boundaries that still apply, or state that the file names none. -->

### Instruction Precedence

#### Canonical Sources

<!-- Author prompt: link the current policies, their versions and their precedence for this directory instead of copying their text. -->

## Workflow

### Intake

#### Local Obligations

<!-- Author prompt: list the obligations and prohibitions that apply here as numbered rules, each with its basis, and add no rule beyond the owning policy. -->

### Execution

<!-- Author prompt: state how an agent inspects inputs, plans and makes the smallest change in this directory, and link the procedure owner. -->

## Boundaries

### Authority

#### Stop and Escalate

<!-- Author prompt: state the conflicts, failures and cancellations that stop work here, how to recover, and who owns the next step. -->

### Secrets and External Effects

#### Protected Actions

<!-- Author prompt: name the secret, deletion, external-write and approval boundaries that apply here, and link their owner. -->

## Verification

### Checks

<!-- Author prompt: list the checks by impact with their exact commands, environment, and pass and fail meaning. -->

### Reporting

#### Evidence and Limits

<!-- Author prompt: separate observed results from checks not run and from accepted limits, and name where the evidence is recorded. -->

#### Handoff

<!-- Author prompt: state how work is handed to the active Task, the next writer or an interface owner, or state that the file names none. -->
~~~~~~~

## 적용과 확인

### 적용 방법

<!-- 작성 규칙: 실제 사용 방법과 적용 대상을 설명한다. -->

### 확인 기준

<!-- 작성 규칙: 이 문서 유형에 해당하는 확인 방법과 한계를 적는다. -->

## 관계와 출처

### 관련 문서

<!-- 작성 규칙: 현재 정본의 관계와 탐색 링크만 연결한다. 실제 의미 관계가 있으면 Relation에 requires/designs/implements/verifies/operates/defines/cites 중 하나를, Target에 현재 문서의 상대 Markdown 링크 하나를 적는다. 단순 탐색 링크는 표 밖에 둔다. -->

| Relation | Target |
| --- | --- |

### 외부 근거

<!-- 작성 규칙: 외부 근거가 있으면 출처와 채택 범위를 적고, 없으면 그 이유를 명시한다. -->
