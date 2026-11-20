---
title: "Commit Message Prompt Contract"
version: "1.0.0"
type: "governance/prompt"
status: "draft"
owner: "platform"
updated: "2026-11-20"
---

# Commit Message Prompt Contract

## 문서 개요

### 목적과 독자

이 prompt 계약은 Commit Message Prompt Contract 요청을 구성하는 작성자와 그 결과를 검토하는 역할에게 입력·출력 경계를 제공한다. 요청 목적은 [Overview](#overview)에 기록한다.

### 책임과 적용 범위

platform은 이 prompt 계약을 유지한다. 허용 권한은 [Authority Boundary](#authority-boundary), 필수 입력은 [Inputs](#inputs)에 기록하며 실행 권한을 추가하지 않는다.

## 내용 계약

### 입력과 전제

입력과 전제는 아래 역할별 본문의 해당 절에 기록한다.

### 본문과 규칙

#### Overview

Identifier `commit-message`. Assemble the request that produces a Conventional
Commit draft for work already staged. The draft is a proposal the user accepts,
edits or discards; nothing in this contract commits, amends or stages.

#### Authority Boundary

This contract shapes a request. It grants no permission to commit, and it does
not restate the Git policy that owns commit scope and history rules. The
builder that reads it runs only the commands named below.

#### Inputs

| Input | Command | Why it is needed |
| --- | --- | --- |
| Staged difference | `git diff --cached` | The subject of the message; the working tree is deliberately excluded |
| Staged path set | `git diff --cached --name-only` | Lets the draft name the owner boundary the change sits in |
| Current branch | `git rev-parse --abbrev-ref HEAD` | Supplies the active work context |

No other command is declared, and the builder runs no command outside this
list.

The subject input is `Staged difference`. When it is empty the contract
refuses and no draft is produced.

#### Output

One Conventional Commit message: a `type(scope): summary` subject in the
imperative, with optional scope. The type is one of the `.cz.toml`
`schema_pattern` types: `feat`, `fix`, `refactor`, `style`, `docs`, `test`,
`build`, `ci`, `perf`, `revert`, `chore`, `release`, `deps`. Use `type!:` or `type(scope)!:` only when the
staged change actually breaks the public contract; a
`BREAKING CHANGE:` or `BREAKING-CHANGE:` footer can describe that impact.
Unicode subject text, type capitalization and final punctuation are allowed
by the `.cz.toml` authored grammar. The subject must contain nonblank text
without embedded header line breaks; subject length and capitalization are
guidance rather than extra gates. Include a body for a
reason not obvious from the subject. Invent no trailing metadata or evidence
the staged difference does not show.

#### Validation

The draft is judged by Commitizen using [`.cz.toml`](../../.cz.toml).
Generation is not validation. Selected staged file QA checks the exact index;
the separate paired commit-msg checks validate the actual candidate message. A PR
title or hosted `style-pr` result is no substitute for that check, including
for a merge commit message. Follow
the [Git policy](../../docs/00.workspace/03.process/git.md)
for validating the actual candidate message and observing active hooks;
workstation configuration is Task evidence, never a shared policy assumption.

#### Refusal Conditions

The builder enforces only the empty-subject refusal; the requesting agent
enforces the remaining conditions below.

- The staged difference is empty. No draft is produced, because a message
  describing nothing is worse than no message.
- A commit message the user has already written is present. The contract never
  rewrites an authored message.
- The request would require reading unstaged or untracked content to describe
  the change.

#### Related Documents

- [Common Prompt Contracts](README.md)
- [Git Policy](../../docs/00.workspace/03.process/git.md)
- [Prompt input builder](../../scripts/prompt-input.py)

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
