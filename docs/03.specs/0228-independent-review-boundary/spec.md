---
title: "Independent Review and Read-Only Boundary"
version: "0.1.1"
type: "sdlc/spec"
status: "draft"
owner: "platform"
updated: "2026-11-20"
artifact_id: "SPEC-0228"
---

# Independent Review and Read-Only Boundary Technical Specification (Spec)

## 문서 개요

### 목적과 독자

This change makes risk-based review, review carry, and the actual read-only
reviewer boundary agree. Authors, nonimplementing reviewers, operators and
quality tools use the resulting contract.

### 책임과 적용 범위

This Spec owns the P06 change and its acceptance criteria. [Quality](../../00.workspace/04.quality/quality.md)
owns durable risk and review meaning, [approval and safety](../../00.workspace/04.quality/approval-and-safety.md)
owns authority, and provider notes own native observations. This draft is
neither implementation approval nor criterion acceptance.

## 내용 계약

### 입력과 전제

The current user request selects P06-INDEPENDENT-REVIEW from the 1.1.0 input
package and authorizes scoped implementation, verification and Git delivery.
The package's D06, D07, decisions, execution contract, questions, sources and
k8s profile/findings are design evidence. Intake began on
`codex/p01-ci-routing` at `598d8e4a47f21cc68f494155febb1227bf6bf12f`.
The eleven earlier streams and P00–P05 have been delivered; their matching
behavior is reused. [SPEC-0223](../0223-work-residue-handoff/01.tasks/tsk-0001-work-residue-handoff.md)
retains the current reviewer failure and the 30-entry residue disposition.

### 본문과 규칙

#### Overview

##### Goal

Require a fresh nonimplementer review for medium risk and an actually confined
read-only independent review for high risk, based on impact and authority.
Reviewers receive the original requirement, design, candidate diff, consumers,
failure conditions and known limits in a fresh context. Review carry applies
only when added material is genuinely result-only evidence. Actual native
permission and source-write results remain separate from role text and static
validation.

###### Owning Requirements

[REQ-0003-FR-0007, FR-0009, FR-0010, FR-0018, FR-0026 and NFR-0002](../../01.requirements/0003-workspace-agent-governance-platform.md)
require least privilege, separate runtime evidence, permission ownership,
risk-classed review and honest check results. [AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md)
separates policy, provider translation, validation and observed runtime. No
new structural decision or ADR is needed for the bounded P06 correction.

##### Consumers

The review role and prompt, provider notes and native configuration, quality
and process policies, `scripts/review_delta.py` and its focused tests, the
Stage 99 workspace binding, current Task evidence and P07 environment handoff
consume this contract. A reviewer verdict informs the change owner; it does
not grant protected-action approval or user acceptance.

#### Scope

##### In Scope

Current k8s risk and independent-review policy; the existing review packet and
carry classifier; Codex and Claude supported reviewer routing; an environment
guide at the current Stage 00 owner; focused negative tests for false carry and
false approval; actual bounded native observations where the environment is
available; existing SPEC-0223 Task/ledger disposition and this package's
document and validation bindings.

##### Out of Scope

Repeating accepted streams; mandatory second paid reviewer for low-risk edits;
running both providers for every change; product cluster deployment or actual
secrets; new subscription, model upgrade, global trust or credential change;
P07 environment implementation, later prompts, P17 history rewrite and early
deletion of the input package.

#### Behavior Contract

##### Inputs and Outputs

Risk follows impact and authority, not filename or line count. Low risk uses
author checks and selected automation. Medium risk receives focused review by
a nonimplementer in a new context. High risk receives that independent judgment
under a verified read-only source boundary. A different role name, static
permission projection, PASS result or repeated author conclusion is insufficient.
The review packet names actual input identity, risk, scope, execution surface,
requirements and design, candidate diff, consumers, tests, failures, findings
and unobserved conditions. Judgment, context and permission independence are
recorded separately. `no findings` applies only to the reviewed scope.

`review_delta.py` may carry an earlier review across an appended factual result
row when the change creates no requirement, acceptance, authority or other
semantic obligation. Appended normative Task prose, approval/authority rows,
new Tasks and new ledger obligations trigger focused re-review. A later meaning
change reopens only its affected slice; an evidence-only commit does not repeat
an unchanged review or native model call.

A native route records provider/version, entry path, parent and child control,
effective tool inventory including shell, file, MCP and hook capabilities,
source scope, actual source-write result (`denied`, `allowed` or `unobserved`),
and boundary state (`enforced`, `failed`, `unobserved` or `unsupported`). Its
probe reads the permitted dummy source, rejects a source write and an
outside-scope fake sentinel read, and confirms that a network-capable tool
cannot make an external connection; a denied socket creation is sufficient
for that restricted surface. A high-risk review requires a verified primary
or separately verified alternative read-only boundary and focused judgment;
recording a failed route alone cannot satisfy it. The
Desktop→SSH workspace-write/null-profile observation stays a failed route.
A separately verified CLI route may serve current review without changing that
historical result. Source config, role text, hook delivery and synthetic tests
are distinct evidence lanes. Read-only review cannot write source, deploy,
merge, read real secrets or use unneeded external tools; owned scratch output
is separate from source writes.

Within the existing account and limits, select one supported Codex and one
Claude main route and obtain one representative actual successful read, denied
dummy-source write and focused review per missing provider boundary. Run them
sequentially, at most 600 seconds each and at most six turns where supported,
with an initial attempt and one post-repair confirmation inside the same
limits. Reuse an actual identical-condition result. Unknown cost is `null` with
a reason, never zero by inference. Native readiness failure cannot be renamed
`unobserved` after an actual attempt; an environment-dependent denial may be
handed to P07 immediately after setup with its failed state and repair scope.

##### Failure Behavior

An allowed source write, missing effective read-only boundary or false carry
blocks the affected high-risk review. Route to a separately verified read-only
parent or whole-process boundary; if none exists, record `failed` and stop that
review claim. Unsupported native capability is `unsupported` only with
installed-client evidence. An unrun probe is `unobserved`. A PASS, hash,
reviewer verdict, role name or agent-declared approval cannot satisfy the
human-owned approval or criterion decision; the existing scoped execution
receipt remains distinct. Actual cost, account or support limits stop only the
dependent native probe. Preserve prior failed observations and route other
safe work to the current owner.
The static receipt validator rejects known bare nonhuman reference shapes and
missing receipts; it does not authenticate a self-declared `actor`. The
operator checks the original trusted user interaction, exact current scope,
validity and revocation before treating a receipt as human authorization.

#### Acceptance Criteria

##### Criteria

| Criterion ID | Expected Result |
| --- | --- |
| AC-0001 | Risk classification uses impact and authority; low, medium and high review routes, actual packet inputs and three independence dimensions are explicit and proportionate. |
| AC-0002 | Result-only evidence carries review, while normative Task append, authority or acceptance changes, a new Task and a new ledger obligation demand focused re-review in regression tests. |
| AC-0003 | Known bare reviewer verdict, PASS, hash and role references and missing receipts are rejected structurally; human approval requires a separately checked original trusted user interaction, current scope, validity and revocation, and criterion acceptance remains distinct from that approval and native permissions. |
| AC-0004 | A high-risk review uses a verified primary or alternative read-only route with effective shell/file/MCP/hook inventory, permitted source read, denied dummy source write and outside-scope sentinel read, no external connection through a network-capable tool, and focused judgment; failed/unobserved/unsupported routes remain separate, including the original Desktop→SSH failure. |
| AC-0005 | Current quality, process, provider and role consumers agree; needed environment instructions and Task/ledger handoff name owners without claiming static checks prove enforcement. |
| AC-0006 | Focused checks and bounded native attempts use actual inputs, version, limits and results; integration, runtime success and user acceptance are reported separately, and P07 is the next prompt only for environment-dependent observation. |

##### Verification Strategy

| Check ID | Guarantee | Input | Trust Boundary | Required When | Evidence |
| --- | --- | --- | --- | --- | --- |
| review-delta | Semantic additions cannot silently carry a previous review | Focused positive/negative diff fixtures | Local classifier only | Classifier change | Task Results |
| approval-negative | Known bare verdict/hash/role shapes and absent receipts are rejected, without claiming static actor authentication | Lifecycle approval fixtures and human interaction review | Repository shape check plus human-owned authority | Approval consumer change | Task Results |
| review-contract | Risk, packet, provider and owner meanings are consistent | Changed policies, prompt, provider notes and diff | Semantic review | Contract change | Task Results |
| native-boundary | Actual allowed read, denied source write and outside-scope read, blocked external connection, effective tool inventory and focused review are observed on a named confined route | Installed clients, isolated temporary source and fake sentinel | Provider runtime; no other route inferred | Supported selected route available | Task Results or explicit P07 handoff |
| document-contract | New package and current owners satisfy profile, lifecycle and links | Exact changed docs and Stage 99 binding | Repository static | Document change | Task Results |
| selected-qa | Affected registered checks pass on their named candidate | Reviewed local index and hosted PR candidate | Local/hosted, not native | Delivery | Task Results and PR run |

###### Normative and Evidence

[Quality](../../00.workspace/04.quality/quality.md),
[approval and safety](../../00.workspace/04.quality/approval-and-safety.md),
[SDLC](../../00.workspace/03.process/sdlc.md), and the
[SPEC-0223 Task](../0223-work-residue-handoff/01.tasks/tsk-0001-work-residue-handoff.md)
own current rules and residue evidence. Package D06/D07 and the user Q03
decision are design inputs; installed-client observations belong to this
Task or the named environment handoff.

###### Historical and Navigation

The [P05 Spec](../0227-docs-sdlc-reconciliation/spec.md) and Task record
previous scope and PR integration. Neither gives P06 native enforcement or
user acceptance.

##### Lifecycle Traceability

| Requirement ID | Spec criterion | Architecture | Verification method |
| --- | --- | --- | --- |
| [REQ-0003-FR-0018](../../01.requirements/0003-workspace-agent-governance-platform.md) | AC-0001 | [AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md) | Risk and packet review |
| [REQ-0003-FR-0018](../../01.requirements/0003-workspace-agent-governance-platform.md) | AC-0002 | [AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md) | Review-delta positive/negative cases |
| [REQ-0003-FR-0007](../../01.requirements/0003-workspace-agent-governance-platform.md) | AC-0003 | [AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md) | Approval negative cases and receipt review |
| [REQ-0003-FR-0009](../../01.requirements/0003-workspace-agent-governance-platform.md) | AC-0004 | [AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md) | Named native route and dummy-source probe |
| [REQ-0003-FR-0010](../../01.requirements/0003-workspace-agent-governance-platform.md) | AC-0005 | [AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md) | Consumer and document checks |
| [REQ-0003-FR-0026](../../01.requirements/0003-workspace-agent-governance-platform.md) | AC-0006 | [AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md) | Actual Task, PR and native evidence lanes |

## 적용과 확인

### 적용 방법

Follow the [Plan](plan.md) for this P06 change. A reviewer uses the current
quality and provider owners and records only its observed route and scope.

### 확인 기준

Selected static checks prove their own inputs. Native enforcement, hosted
integration and operator acceptance each require their own evidence.

## 관계와 출처

### 관련 문서

| Relation | Target |
| --- | --- |
| requires | [REQ-0003](../../01.requirements/0003-workspace-agent-governance-platform.md) |
| designs | [AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md) |
| implements | [P06 Plan](plan.md) |

### 외부 근거

The package's D06/D07 summarize dated primary Codex, Claude and review
sources. Their capability claims must be checked against installed clients;
the repository policy and observed Task results own local adoption.
