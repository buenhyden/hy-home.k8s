---
title: "r10 Local Governance and Delivery Remediation"
version: "0.4.0"
type: "sdlc/spec"
status: "approved"
owner: "platform"
updated: "2026-10-16"
layer: "specs"
artifact_id: "SPEC-0115"
---

# r10 Local Governance and Delivery Remediation Technical Specification (Spec)

## Overview

The 2026-10-15 r10 request asks for an evidence-led review and scoped repair of
the current local governance, documents, validation, delivery and Kubernetes
assurance surfaces. [REQ-0003](../../01.requirements/0003-workspace-agent-governance-platform.md),
[REQ-0004](../../01.requirements/0004-current-local-gitops-platform.md),
[AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md)
and [AD-0007](../../02.architecture/descriptions/0007-current-local-gitops-platform.md)
are current upstream owners. The [Plan](plan.md) orders eight purposes, and
[Task 0001](tasks/tsk-0001-r10-local-remediation.md) holds findings, actual
execution and criterion decisions. The scoped local specification is approved
for this request after independent review under the user's direct local
authorization. This does not adopt a new WGOV common edition or approve a
remote or live action.

The 2026-10-16 r13 follow-up is tracked by
[Task 0002](tasks/tsk-0002-r13-follow-up.md). The prior r10 approval and Task
0001's terminal acceptance remain historical facts, not decisions for the r13
delta. The r13 request directly authorizes scoped reversible local
investigation, repair, validation and logical commits. Task 0002 owns
independent review and new criterion decisions.

The user's later 2026-10-16 authorization adds a bounded residual verification
stream for the exact local commit `8d8fa1e5`, its main-targeting draft PR and
named CI jobs, plus two read-only live verifier runs with the explicitly supplied
kubeconfig. [Task 0003](tasks/tsk-0003-r13-residual-verification.md) owns only
this follow-up's actual evidence and VAL-R13-004 decision. Tasks 0001 and 0002
retain their terminal decisions.

## Strategic Boundaries & Non-goals

- Inspect current `main`, index, worktree, consumers and original evidence
  before changing a contract. Preserve unrelated edits and terminal Task facts.
- Repair only confirmed local conflicts at their current owner and dependent
  readers, validators, tests and navigation. A common WGOV heading, language or
  lifecycle change is a proposal for its common owner until a new edition is
  decided and adopted. The recorded `WGOV-CORE / 3.0.0` approval is not
  approval of changed semantics or full local adoption.
- Preserve the nine completed SPEC-0114 work units, accepted criteria and raw
  `NOT_RUN` observations. New provider runtime findings have their own dated
  evidence; a failed `bwrap` launch is not sandbox enforcement.
- No secret-value read, private memory database inspection, global or managed
  configuration edit, live cluster or Vault operation, deployment, remote
  mutation, data deletion, history rewrite or unilateral common-edition claim.
  Protected external actions follow their own current authority. The later
  authorization above applies only to its exact remote delivery and read-only
  live GET verification targets; it grants no merge, deployment or mutation of
  cluster resources.

## Contracts

- Each r10 material finding records its source path and revision, observation
  class, impact, disposition, current owner and criterion in Task 0001. The r13
  delta uses Task 0002. Static, recorded, reproduced, inferred and inaccessible
  evidence remain distinct.
- The Stage 99 Registry, schema and selected templates own local document
  form. Spec holds changed behavior and acceptance, Plan holds order and
  intended checks, and Task holds actual results and sole criterion decisions.
  Completed or sealed history retains its original evidence.
- The local candidate adapter admits a new Task's first recorded actual
  nonterminal `draft`, `ready`, `in-progress` or `blocked` row when its current scoped
  authorization, prerequisites and observed state are recorded in Task
  Inputs. A new terminal Task remains invalid; later transitions and
  acceptance are unchanged. No synthetic draft commit is required, and this
  extension is not a WGOV-CORE 3.0.0 reapproval or full local adoption.
- `Local candidate Spec/Plan direct draft-to-approved transition after actual batch review and approval`
  admits this reviewed local Spec/Plan approval
  directly from draft. First creation remains draft-only, and approval says
  nothing about Task completion, Archive eligibility or common adoption.
- A selected check runs once per identical input and trust boundary. Local
  purpose QA, hosted `ci-summary` metadata, hosted `style-pr`, provider-native
  enforcement and live Kubernetes behavior each require their own evidence.
- End one-use checks only after their continuing protection transfers and
  callers, registration, dedicated helpers, fixtures and tests are reconciled.
  Retained Archive bodies and held units are not rewritten.
- Shared memory may retain reusable decision context, never Task state,
  approval, PASS or acceptance. No time-based expiry or cleanup of that store
  is introduced by this work.
- A mandatory local `pre-commit` and `commit-msg` chain fails closed on an
  absent executable, hook setup error or failed selected check. It distinguishes
  required hook errors from ordinary unset optional configuration, runs each
  canonical check once for one input, and refuses recursive or duplicated
  chaining. The default pre-commit route invokes one selected staged-QA
  aggregator; formatting hooks that write the real worktree are manual-only.
  Its selected producers cover the actual memory and provider guard changes
  when those paths are in scope.
- Reusing a memory idempotency key with a different request is a conflict;
  exact retries preserve the prior safe result. Source refresh binds to the
  caller worktree and rejects paths escaping through symlinks. Every SQLite
  reconnect enforces its page bound. Backup is serialized and bounded, checks
  schema, workspace identity, revision count and conflicts, and preserves the
  last good snapshot on failure.
- Live verifier evidence rejects NotReady, unhealthy or OutOfSync resources.
  Any TLS check either validates peer trust or explicitly reports a narrower
  transport-only observation. Unused PostgreSQL ESO grants and stale readers
  are removed only after confirming current consumers.
- The r13 follow-up traces each material P01–P08 candidate to current source,
  revision, observation class, disposition, affected consumer and current
  owner in Task 0002. A candidate becomes a defect only after confirmation.
  Changed local contracts and their selected QA/CI consumers move together;
  unchanged protections need no churn. New common headings or lifecycle
  meanings need a separate common-edition decision before adoption.
- The hosted PR metadata producer binds actual merge identity and parents and
  checks every commit in the base-to-head range against trusted-base message
  grammar; the workflow separately checks its PR branch-prefix policy.
  Candidate commit objects are read as data; checked-out candidate
  modules and configuration are not executed by that producer. Its canonical
  Python logic and inline workflow projection must agree. The workflow itself
  remains a separate hosted trust boundary requiring actual protection and
  run evidence.
- A repeated stale memory conflict with the same idempotency key returns its
  recorded safe result without another retained conflict or quota charge.
  Retained conflict history includes its source references.
- GitOps source verification compares exact Application source fields. The
  external-service verifier checks the complete declared Service and every
  same-service EndpointSlice route, port, address and readiness state; static
  source tests do not establish live cluster behavior.

## Core Design

Classify each r10 observation against current source and the existing
SPEC-0105 to SPEC-0114 outcomes. Route a confirmed gap to the narrowest
authoritative owner, implement its dependent change as one reviewable unit,
then attach focused evidence to the owning request Task. Keep common-edition
proposals and unobserved remote or live claims pending at their own owner.

## Data Modeling & Storage Strategy

Task 0001 retains r10 inventory, execution and criterion decisions. Task 0002
owns the r13 follow-up inventory, selected check inputs and results, review
disposition and next owner; source data and raw secret-bearing logs do not move
into the repository.
Git retains source and rollback history. Stage 98 retains only eligible,
approved whole units under its existing catalog and hold rules.

## Interfaces & Data Structures

The local inputs are the r10 and r13 requests, current Git state, Stage 99
profiles, the active requirement and architecture owners, package Tasks,
validation registry and actual provider/CI records. Each request's findings
and check facts stay in its own Task inventory and Evidence columns. No new
schema or parallel progress ledger is introduced by this Spec.

## Edge Cases & Error Handling

An inaccessible original, absent tool, stale receipt, wrong snapshot or
unknown actor remains `DEFER` or `NOT_RUN` with reason and next owner. A
negative test that correctly rejects an input may be test `PASS` while the
input itself is rejected. A failed historical check is retained and resolved
only by a later matching result that names it. Repo-static PASS does not imply
native, hosted or live success.

## Failure Modes & Fallback / Human Escalation

Stop a dependent protected action on missing authority, revocation, sandbox
failure or a required gate failure; continue independent local work. Repair a
regression with a forward corrective source change; any later memory-engine
downgrade needs the compatibility and backup review described in Task 0001.
Refer a new
WGOV edition to buenhyden and each adapter owner, a contested architecture
decision to the architect, and live or remote operations to the responsible
operator with an exact target and reviewed revision.

## Verification Commands

Use the selected `scripts/qa.py staged` profile on an actual staged input,
plus affected named tests and validators. Check the exact Task document with
the document profile, link and lifecycle readers after factual updates.
Record selected tool versions, inputs and results in the owning request Task.
A hosted run, Codex sandbox, memory runtime or live cluster check is reported only when
actually observed in its own trust boundary.

## Success Criteria & Verification Plan

| Criterion | Acceptance evidence |
| --- | --- |
| VAL-R10-001 | P01 baseline and WGOV approval/source/local adoption are distinguished; each confirmed conflict has a current owner and disposition. |
| VAL-R10-002 | P02 changed current documents conform to their selected Stage 99 profiles; the local first-recorded nonterminal Task rule accepts actual authorized state and rejects terminal creation without synthetic history; proposed common semantics remain unadopted until decided. |
| VAL-R10-003 | P03 Task evidence preserves completed work and failures, corrects stale current summaries, and keeps execution, acceptance and integration separate. |
| VAL-R10-004 | P04 whole-unit Archive and one-use QA decisions use current eligibility, holds, promotion and consumer checks; any actual cutover passes Archive integrity. |
| VAL-R10-005 | P05 affected local purpose QA and hosted metadata/style contracts have distinct inputs and evidence; mandatory pre-commit and commit-msg fail closed on errors, distinguish unset optional settings, avoid duplicate/recursive producers, run one selected staged QA by default without worktree-writing file hooks, and select memory/provider checks when changed. |
| VAL-R10-006 | P06 source, commit/PR title, release producer and remote protection claims match observed authority and actual revisions. |
| VAL-R10-007 | P07 memory retries reject same-key different requests, source refresh uses the caller worktree and rejects external symlinks, every reconnect is page bounded, and backup is serialized, bounded and verified without losing a good snapshot; native config, hook delivery and sandbox behavior remain separate evidence. |
| VAL-R10-008 | P08 live verifiers reject NotReady, unhealthy and OutOfSync state, TLS trust is validated or its transport-only limit stated, unused PostgreSQL ESO access and stale readers are reconciled, and static checks stay separate from live acceptance. |
| VAL-R13-001 | The r13 comparison baseline, prior r10 acceptance and PR #148 integration are distinguished; material P01–P08 candidates have source/revision, observation class, disposition and owner in Task 0002. |
| VAL-R13-002 | Confirmed local defects are repaired at current owners with affected callers and selected QA/CI inputs; each changed behavior has focused before/after evidence and selected validation on its actual input, without weakening a unique required protection. |
| VAL-R13-003 | Lasting meaning is promoted to its current owner and whole-unit retention is assessed against links, holds and eligibility; actual delivery and criterion decisions are recorded only in Task 0002, with common-edition, remote, native and live claims separately observed or deferred. |
| VAL-R13-004 | Task 0003 records the exact authorized commit, remote draft PR and named `ci-summary`/`style-pr` leaf outcomes, plus the two selected live verifier results, with revision, target, trust boundary, approval scope and current owner. Required hosted leaves and selected live checks need actual PASS evidence before local acceptance; unobserved or failed required outcomes keep this criterion pending. Common-source, native sandbox, global-hook provenance, independent workflow protection and broader live checks remain separately classified and handed to their owners, without promotion to PASS. |

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-0003-FR-0026](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-R10-001 | Source and approval comparison |
| [REQ-0003-FR-0026](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-R10-003 | Actual Task and integration receipts |
| [REQ-0003-FR-0026](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-R10-006 | Dated hosted and producer evidence |
| [REQ-0003-FR-0026](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-R10-007 | Actual provider observations and separated claims |
| [REQ-0003-FR-0006](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-R10-002 | Selected Stage 99 profile and link checks |
| [REQ-0003-FR-0027](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-R10-004 | Archive eligibility, current consumers and integrity |
| [REQ-0003-FR-0017](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-R10-005 | Local selected QA and separate hosted evidence |
| [REQ-0003-FR-0022](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-R10-007 | Memory owner and focused failure checks |
| [REQ-0004-FR-0001](../../01.requirements/0004-current-local-gitops-platform.md) | VAL-R10-008 | Declared/rendered K8s and direct-runtime evidence split |
| [REQ-0003-FR-0026](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-R13-001 | Current Git/source comparison and Task 0002 finding trace |
| [REQ-0003-FR-0017](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-R13-002 | Affected producer/caller map, focused regression and selected QA |
| [REQ-0003-FR-0027](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-R13-003 | Current-owner and whole-unit retention review |
| [REQ-0003-FR-0026](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-R13-003 | Separate dated local, hosted, provider and live evidence |
| [REQ-0003-FR-0017](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-R13-004 | Exact PR revision, named hosted job/leaf results and protection limit in Task 0003 |
| [REQ-0004-FR-0001](../../01.requirements/0004-current-local-gitops-platform.md) | VAL-R13-004 | Authorized read-only selected live verifier inputs and outcomes in Task 0003 |
