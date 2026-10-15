---
title: "r13 Residual Verification"
version: "0.1.0"
type: "sdlc/task"
status: "in-progress"
owner: "platform"
updated: "2026-10-16"
layer: "specs"
artifact_id: "SPEC-0115-TSK-0003"
parent_ids: ["SPEC-0115-PLAN-0001"]
---

# Task: r13 Residual Verification

## Overview

Execute only [VAL-R13-004](../spec.md#success-criteria--verification-plan) and
[WORK-012](../plan.md#work-breakdown) after the completed local r13 delivery.
[Task 0001](tsk-0001-r10-local-remediation.md) and
[Task 0002](tsk-0002-r13-follow-up.md) retain their terminal evidence and
criterion decisions. This Task owns the later exact remote, selected live and
residual-lane observations; a local source or API status does not establish a
new common edition, native isolation, protected workflow control or deployment.

## Inputs

- The user's direct 2026-10-16 follow-up in this conversation authorized
  remote push of exact local commit
  `8d8fa1e54e1032476fb98215747b5d3579a33322`, a draft PR targeting
  `main`, and its CI run. It also supplied kubeconfig path
  `/home/hyunyoun/.kube/config` for two scoped read-only live verifier runs.
  It did not authorize merge, deployment, cluster mutation, secret reads or
  broad live validation.
- The approved local source is commit `8d8fa1e5` on
  `codex/r13-follow-up`; PR [#149](https://github.com/buenhyden/hy-home.k8s/pull/149)
  is draft, targets `main` at `8488e109`, and has head `8d8fa1e5`. The CI
  transport owner reported a push and remote SHA read-back matching that exact
  commit. The PR's first hosted run subsequently completed on the exact head
  and merge candidate; its named leaf evidence is recorded below.
- The live preflight owner confirmed context `k3d-hyhome` from the explicit
  kubeconfig immediately before each selected verifier. Both verifiers used
  read-only Kubernetes GET operations and exited zero. Their results concern
  the observed cluster state, not deployment of `8d8fa1e5`.
- `WORK-012` is first recorded `in-progress` because the scoped user authority,
  exact local delivery, draft PR and two selected live outcomes are already
  observed. The hosted leaves have since passed, but the criterion decision
  remains pending until this new document input receives independent review
  and normal local validation/delivery.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-012 | [VAL-R13-004](../spec.md#success-criteria--verification-plan) | Verify the authorized exact PR and selected live checks; classify and hand off separate residual lanes | platform | frontmatter | NOT_RUN | EVD-001–007 record exact authorization, remote delivery, selected live and hosted PASS; independent document review and normal local delivery remain pending |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-R13-004](../spec.md#success-criteria--verification-plan) | WORK-012 | Current scoped authorization | User's 2026-10-16 follow-up, exact commit `8d8fa1e5`, `main` draft PR/CI, explicit kubeconfig and two read-only verifier targets | PASS | Current conversation authorization and Task Inputs; no merge, deployment or live mutation authority | yes | none |
| EVD-002 | [VAL-R13-004](../spec.md#success-criteria--verification-plan) | WORK-012 | Exact remote branch delivery | Local `8d8fa1e54e1032476fb98215747b5d3579a33322` on `codex/r13-follow-up` | PASS | CI transport owner's push and remote branch SHA read-back matched the exact commit; this is delivery identity, not hosted CI or deployment evidence | yes | none |
| EVD-003 | [VAL-R13-004](../spec.md#success-criteria--verification-plan) | WORK-012 | Draft PR identity | [PR #149](https://github.com/buenhyden/hy-home.k8s/pull/149), base `main` at `8488e109`, head `8d8fa1e5` | PASS | Remote draft PR creation observed by CI transport owner; review and merge are separate future decisions | yes | none |
| EVD-004 | [VAL-R13-004](../spec.md#success-criteria--verification-plan) | WORK-012 | Selected live GitOps GET verifier | Explicit kubeconfig path above; context `k3d-hyhome` confirmed immediately before `verify-gitops.sh` | PASS | Live preflight owner observed exit 0: root Application source `gitops/apps/root`, revision `main`, and the ten applications explicitly named by the script Healthy/Synced. No reconciled commit SHA or full hierarchy/deployment claim | yes | none |
| EVD-005 | [VAL-R13-004](../spec.md#success-criteria--verification-plan) | WORK-012 | Selected live external-service GET verifier | Same explicit kubeconfig and immediately reconfirmed `k3d-hyhome` context before `verify-external-services.sh` | PASS | Live preflight owner observed exit 0 for all four declared Service/EndpointSlice contracts; no HTTPS, authentication, ESO or end-to-end connectivity result | yes | none |
| EVD-006 | [VAL-R13-004](../spec.md#success-criteria--verification-plan) | WORK-012 | Hosted ci-summary named leaves | Draft PR #149; head `8d8fa1e54e1032476fb98215747b5d3579a33322`, base `8488e1098c2eac8c0db469c4eb59457d471575a8`, merge candidate `e888366545de231198cfa0fc1095cfec48296883`; `pull_request` run `38818750923` attempt 1; GitHub Actions App `15368` | PASS | [ci-summary job 116709856569](https://github.com/buenhyden/hy-home.k8s/actions/runs/38818750923/job/116709856569) completed success. Named `Validate branch metadata` and `Validate PR title and commit range against reviewed base` leaf steps succeeded; filtered job log reported `branch-policy PASS`, `pr-title PASS` and `pr-commits PASS` for 8 commits. This is hosted evidence for this PR input, not independent workflow protection or deployment | yes | none |
| EVD-007 | [VAL-R13-004](../spec.md#success-criteria--verification-plan) | WORK-012 | Hosted style-pr named leaves | Same PR #149 head/base/merge candidate; `pull_request` run `38818750923` attempt 1 | PASS | [style-pr job 116709856386](https://github.com/buenhyden/hy-home.k8s/actions/runs/38818750923/job/116709856386) completed success. Named `Bind base and select changed files`, `Install pinned style runner`, and `Lint and format changed files` leaf steps succeeded; none was skipped or neutral. This does not certify local purpose QA, independent workflow protection or deployment | yes | none |
| EVD-008 | [VAL-R13-004](../spec.md#success-criteria--verification-plan) | WORK-012 | Native sandbox startup | `codex-cli 0.162.1`, `codex sandbox -- /usr/bin/true` on this host | FAIL | Native check owner observed `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted`; startup did not establish isolation. Native/provider owner retains this separate unresolved lane | no | none |
| EVD-009 | [VAL-R13-004](../spec.md#success-criteria--verification-plan) | WORK-012 | Independent common-source authentication | Previously named `Project-Template/.agents/governance/standards.md` at revision `bc5b70556c57198768119f94c287f93c87964482`; absent local 67-path bundle | DEFER | Read-only original-source fetch returned 404. The recorded `WGOV-CORE 3.0.0` approval and C07-only local acceptance remain distinct from the overall candidate adapter or a new common edition; the 404 does not revoke the prior C07 decision. `buenhyden` and source owner hold any new common-edition decision | no | none |
| EVD-010 | [VAL-R13-004](../spec.md#success-criteria--verification-plan) | WORK-012 | Independent workflow protection | PR-editable `ci.yml` and inline metadata projection; observed `main` required contexts `ci-summary` and `style-pr` from App `15368`, four active tag-only rulesets and `rules/branches/main=[]` | DEFER | Those branch/context observations do not establish an independently protected workflow producer. CI/repository owner retains HIGH risk and any reviewed remote control change | no | none |
| EVD-011 | [VAL-R13-004](../spec.md#success-criteria--verification-plan) | WORK-012 | Global hooksPath provenance | User-relayed global-key query produced no stdout; exit status was not provided, while native automatic review denied the tool's exact global-key read | DEFER | No empty/unset PASS or global hook-chain claim follows from absent stdout; local Git operator owns a bounded provenance observation if needed | no | none |
| EVD-012 | [VAL-R13-004](../spec.md#success-criteria--verification-plan) | WORK-012 | Broader live assurance | Full `run-all.sh`, HTTPS/authentication, ESO and NetworkPolicy checks outside the two selected GET runs | NOT_RUN | Responsible GitOps/security operators own any later approved targeted verification; selected EVD-004/005 do not establish these outcomes | no | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-R13-004](../spec.md#success-criteria--verification-plan) | pending | EVD-001, EVD-002, EVD-003, EVD-004, EVD-005, EVD-006, EVD-007 | Required selected remote, hosted and live checks passed on their named inputs. Review this new Task and its lane handoffs, validate the actual local document index, then decide. Native, common-source, global-hook, independent workflow-protection and broader live outcomes remain separate unresolved owner work. | platform and CI transport owner; GitOps, native, common and local Git owners for their lanes |

## Approval and Safety Boundaries

- **Allowed Paths**: This Spec/Plan/Task package for factual follow-up; read-only
  remote PR/CI inspection and the two explicitly scoped live GET verifiers under
  the user's current authorization.
- **Forbidden Paths**: Terminal Tasks 0001/0002, sealed Archive payloads,
  credentials, private memory data, global configuration and unrelated source.
- **Approval Required**: The user's 2026-10-16 message authorized the exact
  `8d8fa1e5` push, draft PR/CI and two kubeconfig-bound read-only verifier
  runs. CI transport owner and live preflight owner executed those scopes;
  EVD-002–005 record their results. Merge, deployment, remote protection or
  permission changes, and live mutation require a separate exact decision.
- **Static Validation**: Selected Stage 99 profile, relationship, link and
  lifecycle checks on the actual document index, independent review and normal
  local commit hooks for this factual package.
- **Live Validation**: Only EVD-004/005 have actual PASS; the broader checks
  listed in EVD-012 remain unrun.
- **Secret / Vault Handling**: The kubeconfig path and context are named only;
  do not read or print kubeconfig contents, Secret values or private memory.
- **Rollback Plan**: Correct or revert only this follow-up document delta
  after reviewing consumers; keep terminal Task evidence and remote PR history.
- **Evidence Location**: This Task owns the new criterion's sole acceptance
  decision; producing hosted runs and live commands retain their own raw output.

## Verification Summary

The exact remote push and draft PR were observed, as were two selected read-only
live verifier PASS results on the confirmed `k3d-hyhome` context. Both named
hosted jobs and their selected leaf steps passed on PR #149's first run. Task
0003 remains in progress pending document review and normal local delivery.
Native sandbox startup failed; independent
common-source authentication, global hooksPath provenance, protected workflow
control and broader live assurance remain separate owner-bound limits. No merge,
deployment or full live-health conclusion is recorded here.
