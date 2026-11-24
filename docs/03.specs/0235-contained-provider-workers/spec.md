---
title: "Contained Provider Workers"
version: "0.1.0"
type: "sdlc/spec"
status: "draft"
owner: "platform"
updated: "2026-11-24"
artifact_id: "SPEC-0235"
---

# Contained Provider Workers Technical Specification (Spec)

## 문서 개요

### 목적과 독자

This Spec states the P12 change contract for the parallel work dispatcher.
The platform owner and reviewers use it to judge whether real Claude and
Codex workers start only under a current request brief, run inside a whole
process and file boundary, and produce results the integration owner can
check.

### 책임과 적용 범위

This Spec owns the P12 behavior and acceptance criteria. The [Plan](plan.md)
owns the work order, risks and rollback, and the
[Task](01.tasks/tsk-0001-contained-provider-workers.md) owns execution and
evidence.

## 내용 계약

### 입력과 전제

The operator entered `prompts/P12-PARALLEL.md` from package
`workspace_governance_remediation_1_2_0_20261123` (`package_version: 1.2.0`)
on 2026-11-24 at `main@f6520ba0`. Design D12 and findings K23-02 and K23-12
keep the existing task graph, path leases, fencing, fresh integration clone,
shared admission and launch receipt, and ask for real provider adapters, a
cgroup or whole-process sandbox that reclaims `setsid` descendants and
refuses writes outside the clone, and one observed run of two meaningful
independent workers. Residue W10-H02 and W10-H03 were open. The Codex account
had reached its usage limit until 2026-11-27 12:53.

### 본문과 규칙

#### Overview

##### Goal

A plan unit may name provider `claude` or `codex` with a prompt and a model,
and Claude also a spending cap. The dispatcher builds the installed CLI's
own argv, passes the prompt on stdin, and starts the unit only while the
named P08 request brief is current. Each provider worker runs in a systemd
user scope inside a bwrap mount namespace. Command workers are unchanged.

###### Owning Requirements

[REQ-0003-FR-0002](../../01.requirements/0003-workspace-agent-governance-platform.md)
requires one shared implementation behind thin provider surfaces.
[AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md)
keeps one store and one dispatcher per Git common directory; no new
architecture decision is needed.

##### Consumers

`scripts/work_parallel.py` (`run --request`, `sweep`),
`scripts/request_brief.py` (`current`), the
[delegated development workflow](../../../.agents/workflows/delegated-development.md)
and the [scripts index](../../../scripts/README.md).

#### Scope

##### In Scope

- Provider unit fields, CLI argv, stdin prompt and result parsing.
- P08 brief freshness before each provider start.
- The scope and bwrap boundary, its stop on finish, timeout, cancel and
  sweep, and a disk check at collection.
- One live run of two independent Claude workers.

##### Out of Scope

Containing command workers, a hard disk quota, network isolation, the
analysis of worker timing (P13), and a Codex live run while its quota is
used up.

#### Behavior Contract

##### Inputs and Outputs

A provider unit has `provider`, `prompt` (at most 16 KiB), `model` and, for
Claude, `budget_usd` (above 0, at most 10). Claude runs `-p --output-format
json --safe-mode --strict-mcp-config --tools Read,Edit,Write --permission-mode
acceptEdits --no-session-persistence --max-budget-usd`; Codex runs `exec
--json --ephemeral --skip-git-repo-check --sandbox workspace-write --cd`. The
scope caps memory, swap, one CPU, 512 tasks and the unit timeout plus 30
seconds. bwrap binds the host read-only, a private `/tmp`, the CLI binary and
the writable clone, and passes only `PATH`, `HOME`, `LANG`, `TMPDIR` and the
dispatcher's own variables. The report adds each unit's provider, scope,
session, cost, turns and usage.

##### Failure Behavior

A provider unit without a current brief is refused with `PARALLEL_BRIEF`; a
missing CLI with `PARALLEL_EXEC`; a CLI error or missing result marks the unit
failed with `PARALLEL_RESULT`; a clone above 1024 MiB is refused with
`PARALLEL_DISK`. A lease is released only after the scope is gone.

#### Acceptance Criteria

##### Criteria

| Criterion ID | Expected Result |
| --- | --- |
| AC-0001 | Provider units are validated, mapped to the installed CLI options with the prompt on stdin, parsed for session, cost and usage, and started only under a current P08 request brief. |
| AC-0002 | A provider worker's writes stay in its clone, its environment is cleared, and finishing, timeout, cancel or sweep ends its whole scope, `setsid` descendants included. |
| AC-0003 | Two meaningful independent Claude workers run with overlapping active intervals, and the integration owner checks and applies their combined result. |
| AC-0004 | One Codex worker runs through the same adapter and boundary and returns a parsed result. |

##### Verification Strategy

| Check ID | Guarantee | Input | Trust Boundary | Required When | Evidence |
| --- | --- | --- | --- | --- | --- |
| CHK-PARALLEL | Plan, argv, parsing, freshness, containment and reclaim | Temporary repositories and a stand-in CLI | Local host | Every dispatcher change | `work-parallel-regressions` |
| CHK-BRIEF | Brief freshness for dispatch | Temporary repositories | Module behavior only | Every brief change | `tests.test_request_brief` |
| CHK-LIVE | Real provider workers, overlap and integration | Live account and user systemd | Local host only | Once per provider | Task Results |

###### Normative and Evidence

The [delegated development workflow](../../../.agents/workflows/delegated-development.md)
states the dispatcher rule. Design D12 and K23-12 are dated inputs.

###### Historical and Navigation

None apply.

##### Lifecycle Traceability

| Requirement ID | Spec criterion | Architecture | Verification method |
| --- | --- | --- | --- |
| [REQ-0003-FR-0002](../../01.requirements/0003-workspace-agent-governance-platform.md) | AC-0001 | [AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md) | Dispatcher and brief regressions |
| [REQ-0003-FR-0002](../../01.requirements/0003-workspace-agent-governance-platform.md) | AC-0002 | [AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md) | Containment regressions |
| [REQ-0003-FR-0002](../../01.requirements/0003-workspace-agent-governance-platform.md) | AC-0003 | [AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md) | Live observation |
| [REQ-0003-FR-0002](../../01.requirements/0003-workspace-agent-governance-platform.md) | AC-0004 | [AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md) | Live observation |

## 적용과 확인

### 적용 방법

Write a plan with provider units, record the request brief, and run
`scripts/work_parallel.py run --request <id>`; review `candidate.patch`
before applying it.

### 확인 기준

Regressions prove module and local containment behavior; live observations
show real provider workers.

## 관계와 출처

### 관련 문서

| Relation | Target |
| --- | --- |
| requires | [Workspace governance requirements](../../01.requirements/0003-workspace-agent-governance-platform.md) |
| designs | [AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md) |

### 외부 근거

Design D12 is a dated input; the installed `claude` 2.1.331 and `codex-cli`
0.172.0 help output fixed the argv. No external standard is adopted.
