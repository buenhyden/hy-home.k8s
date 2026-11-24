---
title: "Delegated Development"
version: "2.0.0"
type: "governance/skill"
status: "active"
owner: "platform"
updated: "2026-11-20"
---

# Delegated Development

## 문서 개요

### 목적과 독자

작업자는 아래에 적힌 조건과 범위에서 위임 개발 절차를 사용한다.

### 책임과 적용 범위

이 절차의 적용 조건과 권한은 [사용 시점](#when-to-use)과 [권한 경계](#authority-boundary)에 따른다.

## 내용 계약

### 입력과 전제

단계를 수행하기 전에 현재 요청과 명시된 입력을 읽는다.

### 본문과 규칙

#### Trigger

##### When to Use

Delegate bounded work through a supported runtime mechanism while preserving
responsibility, least privilege, and independent evidence.

Related documents: [Roles](../roles/README.md),
[Model Selection](../governance/model-selection.md),
[Work Lifecycle](work-lifecycle.md) and
[Approval and Safety](../../docs/00.workspace/04.quality/approval-and-safety.md).

###### Inputs

Neutral role and skill content lives in common governance; Claude and Codex
projections add native metadata only. Tracked files do not prove that a runtime
discovers, loads, or enforces them. Delegation requires explicit user or
applicable instruction authorization and an available runtime mechanism.

##### When Not to Use

This procedure names no repository work it must not be used for; if such a case is found, state it here.

##### Authority Boundary

The [agent registry](../roles/registry.json) owns exact role IDs,
permission classes, handoff edges, capability-tier references, skill references,
and projection paths. This procedure explains their use without duplicating the
roster or tool inventory.

#### Procedure

##### Steps

1. Resolve the role, permission class, skills, and native projection from the
   registry. Read that projection and its imported responsibility owners.
2. Give the worker one concrete task, allowed paths, acceptance IDs,
   dependencies, validation expectations, and next owner. State that other
   workers' changes must be preserved.
   Carry the current request reference and revision, applicable authority and
   execution conditions from the Task. Authoring or review of draft inputs
   follows writing scope. Dependent implementation or operation needs current
   execution authority. Recheck the binding on resume and stop the dependent
   action if approval is stale or revoked.
   Before handing a worker a mutation, resuming a worker after a correction
   or compaction, or making a state change for it, re-confirm the current
   request from its source and run the explicit preflight
   `scripts/validate-execution-brief.py` with the worker's brief. A refusal
   stops only the refused action. A read-only investigation or review handoff
   and a clear low-risk task proceed on the short brief in the handoff itself,
   with no per-file re-approval. The preflight checks correspondence and
   scope only. It grants no authority, and a provider path that does not call
   it is an enforcement gap, not a check.
3. Treat write scope as the intersection of authorization, registry permission,
   responsibility boundary, and task ownership. Read-only roles remain
   read-only; an orchestration role delegates mutation rather than acquiring it.
4. Do not inline a replacement role definition, expand tools, or silently route
   to an undeclared handoff. Escalate an unresolved responsibility or authority
   conflict to the supervising workflow or human.
5. Run independent tasks concurrently only when their ownership is disjoint;
   serialize dependent implementation and reconcile shared boundaries.
   `scripts/work_parallel.py` enforces this for command workers: it locks each
   unit's owned paths and named shared resources with fencing generations,
   runs each attempt in its own clone, refuses a result outside the owned
   paths or from an expired attempt, and reruns the integration check on the
   combined candidate. For command workers a clone separates files only: they
   still run with the caller's own permissions, outside any sandbox. A
   worker's own PASS never replaces the integration check.
   A plan unit may instead name provider `claude` or `codex` with a prompt, a
   model and, for `claude`, a `budget_usd` cap. It starts only when
   `run --request <id>` names a P08 request whose brief is recorded and
   current. Each provider worker runs in its own systemd user scope that caps
   memory, CPU, tasks and run time, and stopping the scope ends every
   descendant. Inside it, bwrap mounts the host read-only except the clone and
   a private `/tmp`, and starts from an empty environment. Host reads and the
   network stay open because the provider needs its API, and disk use is
   checked when the result is collected, not enforced as a quota.
6. Require returning workers to report the
   [quality handoff fields](../../docs/00.workspace/04.quality/quality.md#handoff-evidence-contract).
   Review actual changes and commands; a worker's assertion alone is not
   verification. Reconcile the worker snapshot, file hashes and outstanding
   writes using the [resume decision](../governance/context-and-memory.md#resume-decision).
   A partial result or conflicting writer stops dependent work; preserve its
   verified subset, command limits, approval state and next owner in the Task.
7. Keep durable results in the owning Task and bounded temporary coordination
   in approved ignored scratch. Progress authority follows [context and memory](../governance/context-and-memory.md#objective).

Subagents never perform live mutation or secret-value operations. A higher
capability tier does not grant broader permission. Provider-native runtime
evidence remains distinct from repository-static projection parity.

##### Failure Handling

Failure handling is stated in steps 4 and 6 of Steps.

#### Outputs

##### Artifacts

This procedure defines no output format of its own beyond the results its Steps describe; if it needs one, define it here.

##### Handoff

Completion and handoff are stated in steps 6 and 7 of Steps.

#### Verification

##### Checks

Run registry, projection/config, and semantic/permission checks when a role,
import, permission, handoff, skill, or provider projection changes. Confirm the
actual provider mechanism separately before claiming native delegation.

##### Limits

The static checks do not confirm native delegation, because the actual provider mechanism must be confirmed separately. Tracked files do not prove that a runtime discovers, loads or enforces them, provider-native runtime evidence remains distinct from repository-static projection parity, and a higher capability tier does not grant broader permission.

## 적용과 확인

### 적용 방법

각 단계와 실패 처리 규칙을 명시된 조건에 따라 적용한다.

### 확인 기준

지정된 검사를 실행하고 실제 근거 수준을 보고한다.

## 관계와 출처

### 관련 문서

본문의 관련 문서가 정책과 책임 소유자를 연결한다.

### 외부 근거

인용된 저장소 소유 문서가 이 절차를 정한다. 외부 자료는 참고 근거다.
