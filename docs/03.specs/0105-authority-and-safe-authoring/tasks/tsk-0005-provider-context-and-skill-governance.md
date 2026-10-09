---
title: "Provider, Context and Skill Governance Follow-up"
version: "0.2.0"
type: "sdlc/task"
status: "ready"
owner: "platform"
updated: "2026-10-09"
layer: "specs"
artifact_id: "SPEC-0105-TSK-0005"
parent_ids: ["SPEC-0105-PLAN-0001"]
---

# Task: Provider, Context and Skill Governance Follow-up

## Overview

This Task owns the new P07 local execution for
[WORK-009](../plan.md#work-breakdown) and
[VAL-P01-009](../spec.md#success-criteria--verification-plan). The completed
parent Spec and Plan route this follow-up without restarting earlier Tasks.
[Task 0004](tsk-0004-current-contract-review.md) remains blocked on its own
common-edition and protected actual-PR/control obligations; P07 local work
does not decide them.

## Inputs

- Intake observed clean local `main` at
  `34828945b1ce084b7287dfeebde757ff8500af7a`, with empty index and no
  unstaged changes. The isolated branch `codex/p07-provider-governance` and
  `.worktrees/p07-provider-governance` start at that commit. Ignored
  checkout-root `_workspace/p07-provider-governance/intake-input.json`
  records the initial writer/scope map; it is an intake observation, not an
  implementation or validation result.
- The Spec/Plan/Task draft intake passed six selected exact-index gates with
  rc 0 on tree `10880150f683f214770ec6f312e276fcb750abac`, with the index
  unchanged. `_workspace/p07-provider-governance/intake-index-qa.json` has
  SHA-256 `3293114f1b361f0a7d72f435155762cd1608d00126f44b67fdce583fc773b6b8`
  and its log SHA-256 is
  `8f26ad19d28212bb67255b0fad2e5d7567ee35f12d30718515f2742307cfb4e6`.
  The actual message SHA-256
  `3c123c3563eef49f0af0eddbb5d291738e5bef77136a8fb29af9a391e2ff7a11`
  passed the pinned message check; a normal commit created
  `c718b2d653d9adcbcacbe8a30ce346041888bf4f` at that tree.
  `_workspace/p07-provider-governance/intake-commit.json` has SHA-256
  `db179411defc7da0e1294b78e3ce583da59c2c7092f2eafdab7621a141abf99d`.
  These are intake-document results, not P07 implementation or native proof.
- The current user's P07 request authorizes scoped local investigation,
  policy and consumer repair, selected validation, normal logical commits,
  local main integration and owned cleanup. Remote push, PR, dispatch,
  deployment, tag/Release, paid runtime, trust bypass, private/global
  configuration and credential operations are outside this authorization.
- [SPEC-0105](../spec.md), [Plan WORK-009](../plan.md#work-breakdown),
  [REQ-0003](../../../01.requirements/0003-workspace-agent-governance-platform.md)
  and [AD-0006](../../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md)
  give the current change lineage. Neutral owners are
  [model selection](../../../../.agents/governance/model-selection.md),
  [context and memory](../../../../.agents/governance/context-and-memory.md),
  [work lifecycle](../../../../.agents/workflows/work-lifecycle.md) and the
  [role registry](../../../../.agents/roles/registry.json). Native facts and
  configuration belong to [Codex](../../../../.codex/provider.md) and
  [Claude](../../../../.claude/provider.md) provider surfaces.
- The attached `WGOV-CORE / 3.0.0-draft.2` is a proposal. The user's C02
  correction directs first establishment of one common candidate when no
  existing approved source is found. The same review candidate
  `3.0.0-draft.3` has proposed owner `buenhyden` and proposed
  Project-Template path `.agents/governance/shared-standard.md`; no final
  approved source revision, approval reference, local adoption or joint
  four-repository adoption is established here. C01/C03/C08/C10 guide
  comparison, not native authority or an intake prerequisite.
- Initial read-only observations: the current model-selection policy still
  refers to stopping at an observed elapsed/shared budget and to a remaining
  retry budget, while work-lifecycle and quality already reject business
  deadlines, session timeboxes and reserve approvals. The neutral registry
  stores concrete per-provider model/effort bindings consumed by schema,
  validator, tests and projections. Whether those values migrate to native
  owners is a coupled design and consumer decision; no file move or native
  runtime result is presumed from this intake.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-009 | [VAL-P01-009](../spec.md#success-criteria--verification-plan) | Compare current neutral/native model, skill, context, loop and workspace owners; repair verified local conflicts with affected consumers and evidence | platform | frontmatter | NOT_RUN | EVD-P07-001 through EVD-P07-005 are planned checks; no P07 implementation result yet |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-P07-001 | [VAL-P01-009](../spec.md#success-criteria--verification-plan) | WORK-009 | Neutral and native model/provider ownership | Current registry, schema, validator, provider notes/configuration and projections; focused mismatched-owner and valid-control cases | NOT_RUN | Pending exact source, commands and results in this Task | yes | none |
| EVD-P07-002 | [VAL-P01-009](../spec.md#success-criteria--verification-plan) | WORK-009 | Skill package, caller and hook boundary | Current registered skill packages, actual callers, sidecars, hook adapters and trust/cancellation paths; focused changed-behavior and refusal cases | NOT_RUN | Pending inventory, commands and results in this Task | yes | none |
| EVD-P07-003 | [VAL-P01-009](../spec.md#success-criteria--verification-plan) | WORK-009 | Context, memory, loop and workspace boundaries | Current model/context/workflow policies, memory pointers and temporary workspace consumers; actual budget, no-progress, cancellation and technical-limit distinctions | NOT_RUN | Pending source/consumer comparison and selected checks in this Task | yes | none |
| EVD-P07-004 | [VAL-P01-009](../spec.md#success-criteria--verification-plan) | WORK-009 | Provider-runtime and common-edition boundary | Repository-static input versus dated native observation, unavailable protected session and proposed common edition; separate next owners and no synthetic PASS | NOT_RUN | Pending evidence classification and actual limitations in this Task | yes | none |
| EVD-P07-005 | [VAL-P01-009](../spec.md#success-criteria--verification-plan) | WORK-009 | Final local index, message, review and integration | Final changed index, selected named regressions, actual candidate message, independent reviewers and local main input when source exists | NOT_RUN | Pending exact checks, review, normal commits and observed integration in this Task and Git | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-P01-009](../spec.md#success-criteria--verification-plan) | pending | EVD-P07-001, EVD-P07-002, EVD-P07-003, EVD-P07-004, EVD-P07-005 | Establish current owner/consumer conflicts, repair only confirmed local scope, then decide once from changed-input checks, review and local integration; keep native and common approval lanes separate | platform for local policy/consumers; native operator for protected runtime; buenhyden/common-standard owner for final edition |

## Approval and Safety Boundaries

- **Allowed Paths**: this Spec package, assigned neutral governance/workflow,
  role/skill registry and provider-static consumers, their focused tests and
  existing navigation touched by the change, with one writer per file.
- **Forbidden Paths**: frozen Archive payloads, another writer's in-progress
  files, unrelated private/global configuration, credentials, secrets and live
  Kubernetes/Vault resources.
- **Approval Required**: scoped local inspection/repair, normal commits,
  main integration and owned cleanup are in the current request. Remote or
  paid execution, settings, trust, publication, dispatch, deployment and
  secret/live actions need their own actual authorization; this Task grants
  none of them.
- **Static Validation**: select focused negative and valid-control cases for
  changed behavior, profile/link checks for authored documents, and current
  exact-index/message gates from the actual validation registry. Preserve
  failure inputs and same-check resolutions.
- **Live Validation**: DEFER provider-native discovery, hook delivery,
  authenticated model resolution and remote/live results without their
  authorized environment and actual observed input.
- **Secret / Vault Handling**: read non-secret repository declarations and
  public metadata only; do not read, print, store or transmit credentials or
  private provider configuration.
- **Rollback Plan**: forward-correct the isolated branch and preserve previous
  Task evidence; protected external actions would need their own operator
  recovery decision.
- **Evidence Location**: this Task, reviewed Git commits and bounded ignored
  command receipts; no parallel progress ledger.

## Verification Summary

The intake documents passed their six selected exact-index gates, actual
message check and normal commit. P07 policy/consumer implementation and its
required planned checks remain unrun on the new input. No native session,
common approval, remote action or local integration is recorded as PASS.
Previous package results remain dated evidence at their original owners.
