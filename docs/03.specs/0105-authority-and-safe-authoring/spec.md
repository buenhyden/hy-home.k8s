---
title: "Common Authority and Safe Authoring"
version: "1.4.0"
type: "sdlc/spec"
status: "completed"
owner: "platform"
updated: "2026-10-08"
layer: "specs"
artifact_id: "SPEC-0105"
---

# Common Authority and Safe Authoring Technical Specification (Spec)

## Overview

P01 repairs the existing approval and execution contracts so explicitly scoped
local authoring can proceed without weakening protected execution boundaries.
The request owner authorized reversible local changes and logical commits;
remote publication, live operations, secrets and private settings remain outside
this work unit. There is no open Stage 03 predecessor. SPEC-0104 stays historical.

## Strategic Boundaries & Non-goals

Use current common governance, registry, Stage 99, provider adapters and their
actual consumers. Add no parallel policy, approval service or progress ledger.
Preserve reviewer permissions, native sandbox controls and frozen evidence.
No remote push, PR, merge, archive disposition or deployment is authorized.

## Contracts

- Approval and safety owns authorization; agent execution owns instruction
  precedence and conflict routing; quality owns validation and resource limits.
- Approved documents, redacted examples, synthetic inputs and metadata are
  authoring. Executing a command written in them is a separate operation.
- A review, well-formed record, Git object or historical approval authenticates
  no current operator permission. Missing, mismatched or revoked authority
  blocks only the dependent protected action, not independent safe work.
- An explicit request to repair policy may revise that policy and its consumers
  within the approved scope. It grants no new native capability or self-directed
  role expansion.
- Read-only reviewers report and hand off; an approved writer owns repairs.
- Budget limits never become security denies. Required checks need preflight
  tool, environment and resource readiness, without wrappers or command variants
  used to evade a control.

## Core Design

Trace policy → role → skill → provider → hook → executable and retain a before /
after comparison with exact source and consumer in the [Task](tasks/tsk-0001-authority-and-authoring.md).
Converge rules at their existing owner and update only conflicting consumers.
Use the supported human/operator approval route when no authenticated machine
input exists. Implement no assertion that a repository record authenticates it.

The authorized follow-up [Task](tasks/tsk-0002-quoted-secret-output.md) closes
one observed VAL-P01-002 scanner gap: paired single- or double-quoted YAML/JSON
values after `-o` or `--output` remain raw Secret output. The same existing
decision and prose prohibition grammar apply. VAL-P01-006 covers its local
verification and handoff; the original Task's evidence remains intact.

The separately authorized [authority evidence follow-up](tasks/tsk-0003-authority-evidence-follow-up.md)
rechecks current facts and the SPEC-0106 closing evidence under VAL-P01-001,
VAL-P01-003, VAL-P01-004, VAL-P01-005 and VAL-P01-006. It preserves both
completed Tasks and the existing approval, runtime and historical evidence
boundaries. Its current Task alone records execution and acceptance.

The 2026-10-08 [current-contract follow-up](tasks/tsk-0004-current-contract-review.md)
uses VAL-P01-001, VAL-P01-003, VAL-P01-005 and VAL-P01-006 for the new
P01 source/consumer comparison, local policy clarification, RUN-0012 review,
and bounded delivery. It records unresolved shared-edition authority and
server-setting approval separately. This completed parent and its earlier
Tasks retain their existing acceptance; they do not certify the new scope.

## Data Modeling & Storage Strategy

Stage 99 continues to own document shape and lifecycle. Spec owns this contract,
Plan owns order and risk, Task owns observations and results. Git owns recovery.
New records start in their admitted initial states; historical bytes are frozen.

## Interfaces & Data Structures

Approval decisions bind the actual actor, operation, subject and reviewed
revision, current validity/revocation and the approval source. Preserve any
existing bounded path/payload contracts. Distinguish structural validation from
authentication in consumer outputs and documentation; an unconnected input is
an evidence gap, never fabricated authorization.

## Edge Cases & Error Handling

Commands cited as warnings or operator instructions must not be graded as
executed actions merely because their words occur. Actual unauthorized action
claims and malformed/path-escaping input retain deterministic failures.
Unavailable history or a stale source never produces approval or historical
integrity PASS. Changed implementation inputs require refreshed evidence.

## Failure Modes & Fallback / Human Escalation

Use native approval escalation for a bounded authorized operation when supported;
never alter sandbox/trust configuration or switch wrappers to bypass denial.
Report unavailable required execution as FAIL/DEFER with its next owner. Stop
protected actions whose approval source cannot be verified by the operator.

## Verification Commands

Run focused positive/negative tests for changed executable semantics, then
`python3 scripts/qa.py quick`, exact-index `staged` for each logical commit,
actual Commitizen message validation, and one final local `full` because no
remote delivery is authorized. Record tool resolution and actual outcomes in
the Task. Independent read-only review checks meaning beyond automation.

For the separately authorized SPEC-0105-TSK-0003 documentation follow-up,
the current request instead limits local validation to affected selection,
exact-index staged checks, current lifecycle completion and commit-message
checks, plus independent read-only review. Its affected execution and local
full QA are excluded for this follow-up only; record them as `NOT_RUN`, not
as prior or current PASS. The original Tasks' requirements and observations
above remain historical facts.

## Success Criteria & Verification Plan

For the current-contract follow-up, select affected contract/document checks,
exact-index style and non-style checks, and actual message validation under
the current quality policy. Retired full/ci sweeps and blanket unit discovery
are outside this follow-up. No new prose-mirroring test is required.

| Criterion | Acceptance evidence |
| --- | --- |
| VAL-P01-001 | One action comparison with source, consumer, owner and disposition |
| VAL-P01-002 | Safe authoring cases pass; protected execution cases remain denied |
| VAL-P01-003 | Approval structure/authentication and historical recovery are distinguished; missing/mismatch/revocation cannot authorize an action |
| VAL-P01-004 | Reviewer remains read-only; routine review supplies quality rather than permission |
| VAL-P01-005 | Safety and resource owners are distinct; required-check preflight and no-bypass evidence |
| VAL-P01-006 | Logical commits, actual checks, independent review, delivery limits and rollback recorded |

## Traceability

Input: the current user's P01 request and
[REQ-0003](../../01.requirements/0003-workspace-agent-governance-platform.md).
Existing structure: [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md)
and [ADR-0047](../../02.architecture/decisions/0047-agent-contract-and-resource-ownership.md).
No new architecture decision is needed for repairing their existing boundaries.
Execution order belongs to the [Plan](plan.md).

### Lifecycle Traceability

| Requirement ID | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-0003-FR-0001](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-P01-001 | Owner and consumer review |
| [REQ-0003-FR-0007](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-P01-002 | Focused boundary tests |
| [REQ-0003-FR-0007](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-P01-003 | Approval route review |
| [REQ-0003-FR-0010](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-P01-004 | Registry/projection validation and independent review |
| [REQ-0003-FR-0016](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-P01-005 | Runner and resource boundary inspection |
| [REQ-0003-FR-0018](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-P01-006 | Task command, index and commit evidence |
