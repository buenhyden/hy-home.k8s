---
title: "Current Operations Quality and Architecture Review"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "platform"
updated: "2026-10-09"
layer: "specs"
artifact_id: "SPEC-0106-TSK-0018"
parent_ids: ["SPEC-0106-PLAN-0001"]
---

# Task: Current Operations Quality and Architecture Review

## Overview

This Task owns the new P08 local execution for
[WORK-018](../plan.md#work-breakdown) and
[VAL-P08-018](../spec.md#success-criteria--verification-plan). The completed
Spec/Plan and historical Tasks remain at their recorded decisions.
[P02 Task0016](tsk-0016-shared-profile-migration.md) owns form migration;
[P03 Task0017](tsk-0017-task-acceptance-and-current-review.md) owns its
execution-state review. Their P08 handoff is an input, not current product
or live validation.

## Inputs

- At intake, local `main` is clean at
  `4ce1bf78b1536592db7fae65c233ee5a341b0375`, with an empty index and
  no unstaged change. The owned branch `codex/p08-operations-quality` and
  `.worktrees/p08-operations-quality` begin there. Ignored checkout-root
  `_workspace/p08-operations-quality/intake-observation.json` records the
  current path/status inventory; it is not an implementation result.
- The actual Stage 99 Registry selects `operation/guide`, `operation/policy`
  and `operation/runbook` with their corresponding
  `docs/99.templates/templates/operations/{guide,policy,runbook}.template.md`
  forms. Each role has a distinct ordered six-section core, substantive body
  requirement and `Related Documents` / `Lifecycle Traceability` relation.
  A new form's `draft` is its creation default, not a command to reset a
  current instance. Incident and Postmortem forms remain supported but have
  no current authored instance at this intake.
- All 16 actual current instances have one of the three registered profiles,
  `platform` owner, `active` status, stable GDE/POL/RUN ID, six required H2
  sections and one role-specific traceability table. P02 documented their
  format/content migration separately from product and live truth. This
  inventory is a dated input, not proof that every instruction or threshold
  remains valid.
- [REQ-0004](../../../01.requirements/0004-current-local-gitops-platform.md)
  is the existing in-review platform product requirement; it owns quality
  scenarios, metric formulas, units, environments and decision thresholds.
  [AD-0007](../../../02.architecture/descriptions/0007-current-local-gitops-platform.md)
  is the existing active architecture description; it owns current source
  paths, topology and what evidence each boundary can support, without
  duplicating requirement thresholds. Preserve these statuses and connect
  authorized owner edits and operating consumers to their actual source.
- The same `WGOV-CORE / 3.0.0-draft.3` review candidate remains proposed
  with owner `buenhyden` and one proposed Project-Template source. Its
  content digest identifies draft review bytes, not an approved source or
  adoption. No final common source revision, approval reference, local or
  four-repository adoption is established by this Task.
- The current P08 request authorizes scoped local document/source review,
  supported policy and consumer correction, selected QA, independent review,
  normal logical commits, clean local main integration and owned worktree
  cleanup. It grants no remote write, Release, live cluster, external service,
  secret or private/provider setting action. Before an operator-only check,
  record the actual target, reviewed revision, authority and safe evidence
  path instead of inferring execution from the runbook.

### Current operating corpus and next comparison

The file paths below are current authored bodies, not new templates. Keep each
row's ID, `active` state and current link or justified exclusion unless a
source-bound decision requires a change. P02's row review remains historical
evidence; P08 records its own profile, form, content, owner, references,
status and actual-evidence disposition per row before acceptance.

| Current ID and body | Current operating meaning | P08 comparison and boundary |
| --- | --- | --- |
| [GDE-0010](../../../05.operations/guides/0010-ci-cd-qa-reference-guide.md) | Local QA, hosted style and runtime handoff guidance | Compare current validation registry, P05 CI/QA producers and hosted evidence; keep the RUN-0011/0012 routes, distinguish static versus actual PR/live results. |
| [POL-0001](../../../05.operations/policies/0001-k8s-gitops-operations-policy.md) | Platform GitOps controls and exception owners | Compare current desired-state, AppProject and external exception source; preserve the historical compatibility anchor and active authority. |
| [POL-0003](../../../05.operations/policies/0003-service-mesh-cert-manager-policy.md) | cert-manager, Istio and Kiali controls | Check the stated istiod CPU/memory request and 128Mi exception floor against current values and supported reason; preserve justified no-reciprocal-source exclusion until real lineage exists. |
| [POL-0004](../../../05.operations/policies/0004-rollouts-notifications-headlamp-policy.md) | Rollouts, Notifications and Headlamp controls | Compare current secret ownership and manual promotion boundary with RUN-0004 and manifests; retain historical SPEC-0004/0005 exclusion. |
| [POL-0005](../../../05.operations/policies/0005-observability-platform-operations-policy.md) | Metrics/logging access and control register | Compare current platform/external observability responsibilities and RUN-0007/0008/0009, without inferring actual metrics or logs. |
| [POL-0007](../../../05.operations/policies/0007-app-gitops-onboarding-policy.md) | Workload admission and security/network/GitOps modules | Compare current workload and application routes with RUN-0010 and implementation; do not report deployment or secret checks from static files. |
| [RUN-0001](../../../05.operations/runbooks/0001-argocd-platform-bootstrap-runbook.md) | ArgoCD bootstrap and external EndpointSlice recovery | Compare actual bootstrap manifests and POL-0001; keep external reconciliation operator-bound. |
| [RUN-0002](../../../05.operations/runbooks/0002-argocd-eso-vault-recovery-runbook.md) | ESO/Vault diagnosis, CoreDNS/CA recovery and break-glass route | Compare non-secret references and failure branches; do not read values or execute recovery. |
| [RUN-0003](../../../05.operations/runbooks/0003-platform-expansion-bootstrap-runbook.md) | cert-manager/Istio/Kiali prechecks and recovery | Compare symptom branches, resource floor and POL-0003 before changing a threshold; no live reset or sync. |
| [RUN-0004](../../../05.operations/runbooks/0004-rollouts-notifications-headlamp-runbook.md) | Headlamp access and rollout recovery | Confirm token-safe instructions and POL-0004 promotion/secret boundary; no token issuance. |
| [RUN-0007](../../../05.operations/runbooks/0007-kiali-observability-connectivity-runbook.md) | Kiali external dependencies and connectivity | Compare route, port, TLS, EndpointSlice and egress source to current external-service interface; no availability claim. |
| [RUN-0008](../../../05.operations/runbooks/0008-argocd-metrics-prometheus-runbook.md) | ArgoCD metrics target/relabel diagnosis | Compare current target labels/ports and POL-0005; RUN-0009 keeps its own query-helper owner. |
| [RUN-0009](../../../05.operations/runbooks/0009-k8s-observability-runbook.md) | Alloy metrics/logs/remote-write diagnosis | Compare current workload, queries and POL-0005; do not inspect external credentials or infer delivered telemetry. |
| [RUN-0010](../../../05.operations/runbooks/0010-github-app-gitops-onboarding-runbook.md) | GitHub App workload onboarding, TLS and canary | Compare current sample/app path and CA-validated status-only checks with POL-0007; no push or cluster deployment. |
| [RUN-0011](../../../05.operations/runbooks/0011-reference-maintenance-runbook.md) | Stage 90 reference and Archive disposition | Compare current Stage 90/98 reader and approval route; leave frozen bytes and retention units unchanged. |
| [RUN-0012](../../../05.operations/runbooks/0012-main-release-preparation-runbook.md) | Main release preparation and guarded publication | Compare actual P06 release CLI and SPEC-0107 link; preserve `active` 1.2.0 and separate preview, write, publication and read-back. No actual Release is implied. |

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-018 | [VAL-P08-018](../spec.md#success-criteria--verification-plan) | Review all current operating content and architectural/product evidence, repair supported local drift and hand off distinct live/common decisions | platform | frontmatter | NOT_RUN | EVD-P08-018-001 through EVD-P08-018-004 are planned, not passed |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-P08-018-001 | [VAL-P08-018](../spec.md#success-criteria--verification-plan) | WORK-018 | Sixteen-document seven-axis and product-source comparison | Actual 16 bodies, current Stage 99 form/reader, in-review REQ-0004 quality owner, active AD-0007 source/evidence boundary, source manifests/contracts and P02 handoff; each changed quality statement needs scenario, formula/metric, unit, environment and threshold or named missing owner | NOT_RUN | Pending per-document dispositions and source revisions in this Task | yes | none |
| EVD-P08-018-002 | [VAL-P08-018](../spec.md#success-criteria--verification-plan) | WORK-018 | Current owner, reference and lifecycle preservation | Actual IDs, active states, reciprocal links or justified exclusions, current operations routers and related Spec/Plan/Task evidence | NOT_RUN | Pending changed-input relationship, link, status and semantic review | yes | none |
| EVD-P08-018-003 | [VAL-P08-018](../spec.md#success-criteria--verification-plan) | WORK-018 | Selected final local document and message checks | Final changed index, registered profile/content/link/lifecycle/style leaves, actual message and independent review | NOT_RUN | Pending commands, revisions, results, failures and resolutions in this Task | yes | none |
| EVD-P08-018-004 | [VAL-P08-018](../spec.md#success-criteria--verification-plan) | WORK-018 | Local finish and protected evidence boundary | Actual normal commits and clean main input; separate hosted, external/live, release, secret, common edition and archive-disposition decisions | NOT_RUN | Pending local integration receipt and named next owners; no protected result claimed | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-P08-018](../spec.md#success-criteria--verification-plan) | pending | EVD-P08-018-001, EVD-P08-018-002, EVD-P08-018-003, EVD-P08-018-004 | Decide once after all current-document dispositions, supported repairs, selected checks, review and actual local integration; retain any missing operator, common or remote lane separately | platform for local operating content and Task; relevant service operators for protected observations; buenhyden/common-standard owner for final edition |

## Approval and Safety Boundaries

- **Allowed Paths**: this Spec package; the assigned in-review
  `docs/01.requirements/0004-current-local-gitops-platform.md` requirement
  owner; the active `docs/02.architecture/descriptions/0007-current-local-gitops-platform.md`
  only through its architect writer; assigned current Stage 05 Guide, Policy
  and Runbook bodies and affected navigation. Other source or consumer files
  require a confirmed coupling and their own writer. One writer owns each file;
  operations prose consumes REQ quality decisions and AD source boundaries
  without becoming another threshold owner.
- **Forbidden Paths**: completed Task0016/0017 evidence, frozen Archive bodies,
  unrelated private/global state, credentials, secrets, live Kubernetes/Vault
  and another writer's current files.
- **Approval Required**: current P08 local inspection, supported authoring,
  selected checks, normal logical commits, clean local main integration and
  owned cleanup are the recorded scope. Remote write, PR, Release, tag,
  deployment, external paid/live work, server setting or Archive unit
  disposition needs its own actual authority and reviewed target.
- **Static Validation**: first classify actual source revisions and selected
  document profiles; run changed-input profile, substantive-content,
  relationship, link, lifecycle and applicable style checks, independent
  semantic/security review where the content warrants it, then final-index
  lint/format and actual message checks. Preserve failed inputs and explicit
  same-check resolutions.
- **Live Validation**: NOT_RUN at intake. A manifest or completed Task is not
  a service availability, deployment, secret, external API or release result;
  missing protected inputs are handed to their actual operator.
- **Secret / Vault Handling**: review names, paths and non-secret metadata
  only; do not read, print or store secret values or execute a raw-token
  producing step.
- **Rollback Plan**: forward-correct owned draft content and preserve earlier
  evidence; an operator decides protected runtime recovery separately.
- **Evidence Location**: this Task and bounded actual command/Git receipts;
  no second progress ledger.

## Verification Summary

At intake, clean main, the Stage 99 profile/form map and the 16 current
operating bodies have been inspected for routing and status. No P08 document
repair, independent acceptance review, selected QA, normal commit, local
integration or live result is claimed yet. Task0016/0017's completed local
results remain their own historical evidence; common edition approval,
native/live and remote outcomes remain distinct future decisions.
