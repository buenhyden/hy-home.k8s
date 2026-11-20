---
title: "Documentation Update Prompt Contract"
version: "1.0.0"
type: "governance/prompt"
status: "draft"
owner: "platform"
updated: "2026-11-20"
---

# Documentation Update Prompt Contract

## 문서 개요

### 목적과 독자

이 prompt 계약은 Documentation Update Prompt Contract 요청을 구성하는 작성자와 그 결과를 검토하는 역할에게 입력·출력 경계를 제공한다. 요청 목적은 [Overview](#overview)에 기록한다.

### 책임과 적용 범위

platform은 이 prompt 계약을 유지한다. 허용 권한은 [Authority Boundary](#authority-boundary), 필수 입력은 [Inputs](#inputs)에 기록하며 실행 권한을 추가하지 않는다.

## 내용 계약

### 입력과 전제

입력과 전제는 아래 역할별 본문의 해당 절에 기록한다.

### 본문과 규칙

#### Overview

Identifier `doc-update`. Assemble the request that locates the canonical owner
for a change and proposes a difference against it, so a correction lands at the
one document that owns the statement instead of being copied into several.

#### Authority Boundary

Profile selection, section contracts and lifecycle states belong to the Stage 99
registry and the document authoring policy. This contract routes a request to
them; it defines no form and overrides no profile.

#### Inputs

| Input | Command | Why it is needed |
| --- | --- | --- |
| Changed path set | `git status --porcelain` | Identifies which owners the change touches |
| Local difference | `git diff` | Shows what statement became untrue |
| Owner candidates | `git ls-files docs/README.md 'docs/**/README.md' '.agents/*.md' '.agents/**/*.md'` | Supplies the routers that name canonical owners |

The subject input is `Changed path set`. When it is empty the contract
refuses, because no statement has changed owner.

#### Output

A proposed difference against one named owner path, with the reason the
statement changed. Where more than one document states the same fact, the
output names the single owner and the duplicates to remove rather than editing
each copy.

#### Validation

The proposal is judged by the document contract registry and the markdown
profile validator on the target path, and by link and owner validation when it
changes a route. Retired subjects are not rewritten to match a new form.

#### Refusal Conditions

The builder enforces only the empty-subject refusal; the requesting agent
enforces the remaining conditions below.

- No owner can be resolved for the statement, which means the owner must be
  decided before the text is written.
- The target is a retired subject in an Archived Lineage row, a file under
  unvalidated `docs/98.archive/`, or Git history, none of which is rewritten.
- The proposal would create a second document stating the same contract.

#### Related Documents

- [Common Prompt Contracts](README.md)
- [Document Authoring](../../docs/00.workspace/03.process/document-authoring.md)
- Document profiles and templates (`docs/99.templates/README.md`)

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
