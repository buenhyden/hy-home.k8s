---
name: "ops-runbook"
description: "Use when authoring or reviewing operations runbooks for bootstrap, recovery, deployment, backup, and incident procedures in hy-home.k8s."
metadata:
  title: "Ops Runbook"
  version: "1.1.1"
  type: "governance/skill"
  status: "active"
  owner: "platform"
  updated: "2026-11-13"
disable-model-invocation: true
---

Read `.agents/governance/approval-and-safety.md` and the selected role before
using this procedure. Skill invocation does not authorize additional actions.

# ops-runbook

## Purpose and Trigger

### When to Use

Author and review operations runbooks (`docs/05.operations/runbooks/`) for this repository's
Linux server + k3d + ArgoCD platform. Ensure runbooks are executable, verifiable, and safe for operator
use without requiring cluster access delegation.

### When Not to Use

- Authoring an execution plan or task unit; use `execution-plan` or `task-breakdown`.
- Tracing requirements or architecture decisions; use `requirements-to-design`.
- Diagnosing a live incident without an existing runbook; use `incident-postmortem` after.

#### Safety Rules

- Never include plaintext Kubernetes secrets or OpenBao tokens in runbook steps.
- Every bootstrap-boundary action (k3d create, ArgoCD install, root app apply) must state
  the exact `kubectl apply` or `helm install` command and its scope.
- Break-glass actions must record scope, rollback, and verification evidence in the runbook.

## Procedure

### Steps

1. Identify the runbook type and the runbook index
   (`docs/05.operations/runbooks/README.md`). Resolve its `operation/runbook`
   profile through `docs-stage-routing`; the Stage 99 owner supplies the path
   grammar and the form
   (registry entry; see [Stage 99 templates](../../../docs/99.templates/README.md)). Runbooks are
   Korean-first per the registry `document_language`. A read-only reviewer returns findings and writes nothing.
2. Under Preconditions, state the required cluster state, credentials, and
   environment variables.
3. Under Steps > Actions, list every step with the exact command, expected
   output, and failure signal; put the stop and additional-approval conditions
   under Stop Conditions.
4. Under Validation, include a check after each destructive or irreversible
   action and the post-conditions that confirm success.
5. Under Recovery, put non-rollback recovery under Recovery Procedures, undo
   each step in reverse order under Rollback, and name the escalation owner
   under Escalation.
6. Link the relevant Argo CD apps, OpenBao paths, or
   ExternalSecret/ClusterSecretStore (`vault-backend`) resources inline by type:
   normative links in Preconditions > Authority and Access, evidence links in
   Validation > Evidence, and navigation links in Purpose > Scope.
7. An authorized author saves the file at the resolved runbook profile path.
8. Update `docs/05.operations/runbooks/README.md` to include the new runbook link.

Section names and order follow the Runbook form: Purpose; Preconditions;
Steps; Validation; Recovery.

### Failure Handling

None is stated in this document.

## Inputs and Outputs

### Inputs

None is stated in this document.

### Outputs

None is stated in this document.

## Verification

### Checks

None is stated in this document.

### Completion and Handoff

None is stated in this document.
