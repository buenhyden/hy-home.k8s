---
title: "Native Request Brief"
version: "0.1.0"
type: "sdlc/spec"
status: "draft"
owner: "platform"
updated: "2026-11-24"
artifact_id: "SPEC-0231"
---

# Native Request Brief Technical Specification (Spec)

## 문서 개요

### 목적과 독자

This Spec states the P08 change contract for the brief a provider shows the
user before its first change. The platform owner, reviewers and implementers
use it to judge whether a request is bound to a shown brief before any
change, without a new approval step for clear work.

### 책임과 적용 범위

This Spec owns the P08 behavior and acceptance criteria. The [Plan](plan.md)
owns the work order, risks and rollback, and the
[Task](01.tasks/tsk-0001-native-request-brief.md) owns execution and
evidence.

## 내용 계약

### 입력과 전제

The operator entered `prompts/P08-NATIVE-BRIEF.md` from package
`workspace_governance_remediation_1_2_0_20261123` (`package_version: 1.2.0`)
on 2026-11-24 at `main@210587c2c089c941d127f086018c70814017a678`. Its D08
design and the k8s finding K23-07 state the gap: a worker handoff check
exists, but neither provider binds the current request to a brief the user
sees before the first change. Installed clients are Claude Code 2.1.330 and
Codex CLI 0.171.0. P07 keeps its own open runtime blocker under SPEC-0229;
this change does not depend on it.

### 본문과 규칙

#### Overview

##### Goal

Each provider receives the request through its `UserPromptSubmit` hook,
binds it to the session, generation, Codex turn, workspace, branch and a
policy digest, and lets read-only discovery run at once. Before the first
change the model shows the user a brief in its reply and records it; the
shared write guard refuses a detected change until then and shows the
recorded brief to the user on the first admitted change. A changed request,
a stale receipt or another workspace is refused.

###### Owning Requirements

[REQ-0003-FR-0002, FR-0025 and FR-0026](../../01.requirements/0003-workspace-agent-governance-platform.md)
require thin provider adapters over one shared implementation, oversight
before changes and separate repository, provider-runtime and user evidence.
[AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md)
keeps the shared write guard as the one pre-action boundary; this change adds
a module beside it and needs no new architecture decision.

##### Consumers

`.claude/settings.json`, `.codex/hooks.json` and their adapters,
`scripts/provider_write_guard.py`, `scripts/validate-agent-governance.py`
and the model in both providers.

#### Scope

##### In Scope

- `scripts/request_brief.py` with intake, record and admit.
- `UserPromptSubmit` adapters and registrations for both providers, and the
  governance check that pins them.
- First-change admission in the shared write guard for each change it
  detects.
- Regressions, provider notes and one representative native observation per
  provider.

##### Out of Scope

The worker handoff check `scripts/validate-execution-brief.py`, P06 review
routes, P07 runtime work, other workspaces and P09–P17. Shell writes the
guard does not detect stay outside this boundary.

#### Behavior Contract

##### Inputs and Outputs

Intake reads the hook payload and keeps one receipt per provider session in
the private `request-briefs` directory of the Git common directory: a
SHA-256 digest of the prompt, never its text, the generation, Codex turn,
workspace, branch, policy digest and times. It returns model context naming
the request. `record` takes the brief as JSON (goal, scope, keep, change,
questions, checks) and binds it to the named current request. On the first
admitted change the guard returns the brief as the hook's `systemMessage`.

##### Failure Behavior

A change the guard detects is refused with `BRIEF-MISSING` (no receipt or
session), `BRIEF-NOT-SHOWN` (no recorded brief), `BRIEF-STALE` (a later
request, another Codex turn, or a branch or policy change before the first
change) or `BRIEF-WORKSPACE` (another repository). Intake never blocks a
prompt; a failed intake leaves the change refused.

#### Acceptance Criteria

##### Criteria

| Criterion ID | Expected Result |
| --- | --- |
| AC-0001 | Read-only discovery runs without a brief; a detected change is refused until the current request has a recorded brief, and is admitted after it with the brief sent to the user once. |
| AC-0002 | A changed request, a stale or missing receipt, another Codex turn, a branch or policy change before the first change and another workspace are refused. |
| AC-0003 | Each provider's installed client delivers the intake hook and shows the brief, or the unobserved or failed surface is recorded as such. |

##### Verification Strategy

| Check ID | Guarantee | Input | Trust Boundary | Required When | Evidence |
| --- | --- | --- | --- | --- | --- |
| CHK-UNIT | Intake, record and admit refuse and admit as specified | Temporary Git repositories | Module behavior; no provider runtime | Every change to the module | `tooling` suite |
| CHK-GUARD | The guard refuses and admits through the module for both adapters | Provider-shaped payloads | Hook program only; no client delivery | Every guard change | `tooling` suite |
| CHK-HOOK | Both registrations run only the intake adapter | Provider settings | Configuration only | Every hook registration change | `agent-governance` |
| CHK-NATIVE | The installed client delivered intake, refused and admitted a change and showed the brief | Real sessions | One representative observation per provider | Once for this change | Task Results |

###### Normative and Evidence

The [Claude provider note](../../../.claude/provider.md) and
[Codex provider note](../../../.codex/provider.md) own the native claims.
The package D08 design is a dated input.

###### Historical and Navigation

None apply.

##### Lifecycle Traceability

| Requirement ID | Spec criterion | Architecture | Verification method |
| --- | --- | --- | --- |
| [REQ-0003-FR-0025](../../01.requirements/0003-workspace-agent-governance-platform.md) | AC-0001 | [AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md) | Module and guard regressions |
| [REQ-0003-FR-0025](../../01.requirements/0003-workspace-agent-governance-platform.md) | AC-0002 | [AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md) | Module and guard regressions |
| [REQ-0003-FR-0002](../../01.requirements/0003-workspace-agent-governance-platform.md) | AC-0001 | [AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md) | Hook registration check |
| [REQ-0003-FR-0026](../../01.requirements/0003-workspace-agent-governance-platform.md) | AC-0003 | [AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md) | Recorded native observations |

## 적용과 확인

### 적용 방법

Both providers apply this contract through their tracked hook registrations;
the model follows the intake context it receives.

### 확인 기준

Regressions prove the program behavior; only the native observations in the
Task show what an installed client delivered and displayed.

## 관계와 출처

### 관련 문서

| Relation | Target |
| --- | --- |
| requires | [Workspace governance requirements](../../01.requirements/0003-workspace-agent-governance-platform.md) |
| designs | [AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md) |

### 외부 근거

The package D08 design and its hook research (KREF-08, KREF-09) are dated
inputs; vendor hook references grant no authority.
