---
title: "Common Authority and Safe Authoring"
version: "1.6.0"
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

P03 clarifies the pending follow-up without broadening its permissions.
The literal local meanings of VAL-P01-001/003/005/006 can be accepted from
their actual comparison, approval-route, resource and delivery evidence.
VAL-P01-007 separately owns the P01 request's remaining common-source,
edition decision and actual adoption outcome. VAL-P01-008 owns the required/
style result observation for the next authorized actual PR and the open
workflow-control HIGH acceptance prerequisite if that PR changes control
inputs. No absent PR is manufactured, no setting read-back is PR PASS, and
no new workflow repair or server permission follows from this criterion.
WORK-008 remains blocked on these protected/event-dependent lanes while
independent local P03 work proceeds. All original failures, approvals and
criterion memberships remain in the Task's dated migration provenance.

The 2026-10-09 P07 [provider-governance follow-up](tasks/tsk-0005-provider-context-and-skill-governance.md)
uses VAL-P01-009 for a separate local review of neutral/provider ownership,
model and context rules, skill consumers, loop and workspace boundaries, and
their actual validators. It does not reopen completed Tasks or absorb Task
0004's common-edition and protected server obligations. The proposed
`WGOV-CORE / 3.0.0-draft.3` is a shared review input, not an approved source
or a provider-runtime result. The new Task owns P07 execution and evidence.

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
| VAL-P01-007 | The one common source and reviewed edition have a real owner decision, source revision and approval reference; actual local and joint adoption are recorded separately. Missing approval or unobserved adapters remain pending with their owners, not fabricated PASS or an intake prerequisite. |
| VAL-P01-008 | Observe actual required/style results on the next authorized PR input. Before accepting a workflow/control-changing PR or Release relying on these gates, independently verify control integrity for that actual input. An operator-reviewed settings transition needs its own exact approval and read-back and cannot substitute for integrity proof. Until the event and proof exist, retain DEFER/FAIL and next owners; this conditional criterion grants no PR, workflow, server or Release execution authority. |
| VAL-P01-009 | On the actual P07 input, distinguish neutral role, capability, skill, context, loop and work-handoff meaning from provider-native model, effort, discovery, hook and permission configuration. Repair verified owner/consumer conflicts, including business/session deadline or reserve wording, while preserving real provider limits, cancellation, technical process safety, protected approvals and no-progress stops. The new Task connects focused boundary regressions, exact-index/message checks, independent review, local integration and remaining owners. Static files do not establish native runtime behavior, final common approval or four-repository adoption. |

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
| N/A — current explicit P01 common-source/edition/adoption request | VAL-P01-007 | WORK-008 / Task0004 EVD-003; actual source-owner decision, edition identity and separate local/joint adoption |
| N/A — current P01 actual-PR inspection and subsequent HIGH/workflow-PR review request | VAL-P01-008 | WORK-008 / Task0004 EVD-008/009/010; conditional actual-input required/style and independent control proof, with no new execution authority |
| [REQ-0003-FR-0010](../../01.requirements/0003-workspace-agent-governance-platform.md), [REQ-0003-FR-0011](../../01.requirements/0003-workspace-agent-governance-platform.md), [REQ-0003-FR-0026](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-P01-009 | WORK-009 / Task0005; neutral/provider/skill/context/workspace owner and consumer comparison, focused changed-boundary checks, exact local validation and reviewed handoff; native and common adoption remain separate |
