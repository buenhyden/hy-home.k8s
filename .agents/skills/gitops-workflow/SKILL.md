---
name: "gitops-workflow"
description: "Use when onboarding, updating, or diagnosing workloads through the repository-backed GitOps and ArgoCD path."
metadata:
  title: "GitOps Workflow"
  version: "1.0.2"
  type: "governance/skill"
  status: "active"
  owner: "platform"
  updated: "2026-11-06"
disable-model-invocation: true
---

Read `.agents/governance/approval-and-safety.md` and the selected role before
using this procedure. Skill invocation does not authorize additional actions.

# gitops-workflow

## Purpose

Define the approved GitOps path for workload onboarding, change review, and sync diagnosis in `hy-home.k8s`.

## When NOT to Use

- Choosing how the change rolls out; use `deployment-strategies`.
- Running the repository validation lanes; use `k8s-validate`.
- Reviewing the manifests for security anti-patterns; use `vulnerability-patterns`.

## Workflow Steps

1. Define the target workload or GitOps object and confirm the repository path.
2. For an external endpoint change, use `external-service-contract-audit` to
   compare the current declarations and consumer before a scoped edit. Apply
   repository-backed changes only; live reconciliation remains operator-owned.
3. Run the validation path through `k8s-validate`.
4. Review release structure, sync targets, and rollout safety.
5. To diagnose a sync problem, read the Application, its source manifests and
   recorded sync status read-only, and report the cause and the repository change
   that would fix it; do not mutate live state.
6. Report PR and Argo CD reconciliation readiness. Creating a PR or triggering reconciliation requires separate explicit authorization.

## Constraints

- GitOps-first is mandatory.
- Direct `kubectl apply` or similar drift-causing mutation is not allowed,
  except in documented bootstrap or break-glass runbooks.
- A read-only role (such as `gitops-reviewer`) returns findings and routes any
  edit to the implementation owner.
- Repository structure and ArgoCD targeting must stay cluster-specific.
- Secret management must follow approved resources only.

## Expected Outputs

- Clear next steps for onboarding, updating, or diagnosing a workload
- Validation prerequisites and review expectations
- A concise checklist for PR and reconciliation readiness

## Failure Handling

- If repository ownership is unclear, escalate to the supervising owner.
- If security findings block progress, hand off to the security review owner.
- If validation fails, stop and route through `k8s-validate` remediation before continuing.
