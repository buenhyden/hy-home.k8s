---
name: "gitops-workflow"
description: "Use when onboarding, updating, or diagnosing workloads through the repository-backed GitOps and ArgoCD path."
disable-model-invocation: true
---

Read `.agents/governance/approval-and-safety.md` and the selected role before
using this procedure. Skill invocation does not authorize additional actions.

# gitops-workflow

## Purpose

Define the approved GitOps path for workload onboarding, change review, and sync diagnosis in `hy-home.k8s`.

## Trigger Phrases

- "onboard a workload"
- "review the GitOps path"
- "diagnose an ArgoCD sync problem"
- "prepare a GitOps-safe change"

## Workflow Steps

1. Define the target workload or GitOps object and confirm the repository path.
2. Apply or update repository-backed manifests only; do not mutate the cluster directly.
3. Run the validation path through `k8s-validate`.
4. Review release structure, sync targets, and rollout safety.
5. Report PR and Argo CD reconciliation readiness. Creating a PR or triggering reconciliation requires separate explicit authorization.

## Constraints

- GitOps-first is mandatory.
- Direct `kubectl apply` or similar drift-causing mutation is not allowed.
- Repository structure and ArgoCD targeting must stay cluster-specific.
- Secret management must follow approved resources only.

## Expected Outputs

- Clear next steps for onboarding, updating, or diagnosing a workload
- Validation prerequisites and review expectations
- A concise checklist for PR and reconciliation readiness

## Failure Handling

- If repository ownership is unclear, escalate to `supervisor.md`.
- If security findings block progress, escalate to `security-auditor.md`.
- If validation fails, stop and route through `k8s-validate` remediation before continuing.
