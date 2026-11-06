---
name: "ops-runbook"
description: "Use when authoring or reviewing operations runbooks for bootstrap, recovery, deployment, backup, and incident procedures in hy-home.k8s."
metadata:
  title: "Ops Runbook"
  version: "1.0.2"
  type: "governance/skill"
  status: "active"
  owner: "platform"
  updated: "2026-11-06"
disable-model-invocation: true
---

Read `.agents/governance/approval-and-safety.md` and the selected role before
using this procedure. Skill invocation does not authorize additional actions.

# ops-runbook

## Purpose

Author and review operations runbooks (`docs/05.operations/runbooks/`) for this repository's
Linux server + k3d + ArgoCD platform. Ensure runbooks are executable, verifiable, and safe for operator
use without requiring cluster access delegation.

## When NOT to Use

- Authoring an execution plan or task unit; use `execution-plan` or `task-breakdown`.
- Tracing requirements or architecture decisions; use `requirements-to-design`.
- Diagnosing a live incident without an existing runbook; use `incident-postmortem` after.

## Workflow Steps

1. Identify the runbook type and the runbook index
   (`docs/05.operations/runbooks/README.md`). Resolve its `operation/runbook`
   profile through `docs-stage-routing`; the Stage 99 owner supplies the path
   grammar and the form
   (registry entry; see [Stage 99 templates](../../../docs/99.templates/README.md)). Runbooks are
   Korean-first per the registry `document_language`. A read-only reviewer returns findings and writes nothing.
2. Under Trigger and Preconditions, state the required cluster state,
   credentials, and environment variables.
3. Under Procedure, list every step with the exact command, expected output,
   and failure signal.
4. Under Verification, include a check after each destructive or irreversible
   action and the post-conditions that confirm success.
5. Under Recovery and Escalation, undo each step in reverse order and name the
   escalation owner.
6. Under Related Documents, link the relevant Argo CD apps, OpenBao paths, or
   ExternalSecret/ClusterSecretStore (`vault-backend`) resources.
7. An authorized author saves the file at the resolved runbook profile path.
8. Update `docs/05.operations/runbooks/README.md` to include the new runbook link.

Section names and order follow the profile: Purpose; Trigger and
Preconditions; Procedure; Verification; Recovery and Escalation; Related
Documents.

## Safety Rules

- Never include plaintext Kubernetes secrets or OpenBao tokens in runbook steps.
- Every bootstrap-boundary action (k3d create, ArgoCD install, root app apply) must state
  the exact `kubectl apply` or `helm install` command and its scope.
- Break-glass actions must record scope, rollback, and verification evidence in the runbook.
